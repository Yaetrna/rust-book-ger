## Geordnetes Herunterfahren und Aufräumen {#graceful-shutdown-and-cleanup}

Der Code in Listing 21-20 beantwortet Anfragen wie beabsichtigt asynchron über
einen Thread-Pool. Wir bekommen einige Warnungen über die Felder `workers`, `id`
und `thread`, die wir nicht direkt verwenden, was uns daran erinnert, dass wir
nichts aufräumen. Wenn wir den Haupt-Thread mit der weniger eleganten Methode
<kbd>ctrl</kbd>-<kbd>C</kbd> anhalten, werden auch alle anderen Threads sofort
gestoppt, selbst wenn sie gerade mitten in der Bearbeitung einer Anfrage sind.

Als Nächstes implementieren wir daher den Trait `Drop`, um auf jedem der Threads
im Pool `join` aufzurufen, damit sie die Anfragen, an denen sie arbeiten,
abschließen können, bevor sie beendet werden. Dann implementieren wir eine
Möglichkeit, den Threads mitzuteilen, dass sie keine neuen Anfragen mehr
annehmen und sich beenden sollen. Um diesen Code in Aktion zu sehen, ändern wir
unseren Server so, dass er nur zwei Anfragen annimmt, bevor er seinen
Thread-Pool geordnet herunterfährt.

Eine Sache fällt dabei auf: Nichts davon betrifft die Teile des Codes, die die
Ausführung der Closures übernehmen, daher wäre hier alles gleich, wenn wir einen
Thread-Pool für eine Async-Runtime verwenden würden.

### Den Trait `Drop` für `ThreadPool` implementieren {#implementing-the-drop-trait-on-threadpool}

Beginnen wir damit, `Drop` für unseren Thread-Pool zu implementieren. Wenn der
Pool verworfen (_dropped_) wird, sollen alle unsere Threads zusammengeführt
(_join_) werden, um sicherzustellen, dass sie ihre Arbeit beenden. Listing 21-22
zeigt einen ersten Versuch einer `Drop`-Implementierung; dieser Code
funktioniert noch nicht ganz.

<Listing number="21-22" file-name="src/lib.rs" caption="Jeden Thread zusammenführen, wenn der Thread-Pool den Gültigkeitsbereich verlässt">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch21-web-server/listing-21-22/src/lib.rs:here}}
```

</Listing>

Zuerst durchlaufen wir alle `workers` des Thread-Pools. Wir verwenden dafür
`&mut`, weil `self` eine veränderliche (_mutable_) Referenz ist und wir außerdem
`worker` verändern können müssen. Für jeden `worker` geben wir eine Nachricht
aus, dass diese bestimmte `Worker`-Instanz heruntergefahren wird, und rufen dann
`join` auf dem Thread dieser `Worker`-Instanz auf. Wenn der Aufruf von `join`
fehlschlägt, verwenden wir `unwrap`, damit Rust einen Panic auslöst und
ungeordnet herunterfährt.

Hier ist der Fehler, den wir beim Kompilieren dieses Codes bekommen:

```console
{{#include ../listings/ch21-web-server/listing-21-22/output.txt}}
```

Der Fehler sagt uns, dass wir `join` nicht aufrufen können, weil wir von jedem
`worker` nur eine veränderliche Ausleihe (_borrow_) haben und `join` die
Ownership an seinem Argument übernimmt. Um dieses Problem zu lösen, müssen wir
den Thread aus der `Worker`-Instanz, die `thread` besitzt, herausverschieben
(_move_), damit `join` den Thread verbrauchen kann. Eine Möglichkeit dafür ist
derselbe Ansatz, den wir in Listing 18-15 verfolgt haben. Würde `Worker` ein
`Option<thread::JoinHandle<()>>` enthalten, könnten wir die Methode `take` auf
der `Option` aufrufen, um den Wert aus der Variante `Some` herauszuverschieben
und an seiner Stelle eine Variante `None` zu hinterlassen. Mit anderen Worten:
Ein laufender `Worker` hätte in `thread` eine Variante `Some`, und wenn wir
einen `Worker` aufräumen wollten, würden wir `Some` durch `None` ersetzen,
sodass der `Worker` keinen Thread mehr zum Ausführen hätte.

Das würde aber _nur_ beim Verwerfen des `Worker` eine Rolle spielen. Im Gegenzug
müssten wir überall, wo wir auf `worker.thread` zugreifen, mit einem
`Option<thread::JoinHandle<()>>` umgehen. Idiomatisches Rust verwendet `Option`
recht häufig, aber wenn du merkst, dass du etwas, von dem du weißt, dass es
immer vorhanden ist, als Workaround wie diesen in eine `Option` hüllst, ist es
eine gute Idee, nach alternativen Ansätzen zu suchen, um deinen Code sauberer
und weniger fehleranfällig zu machen.

In diesem Fall gibt es eine bessere Alternative: die Methode `Vec::drain`. Sie
nimmt einen Bereichsparameter (_range_), der angibt, welche Elemente aus dem
Vektor entfernt werden sollen, und gibt einen Iterator über diese Elemente
zurück. Die Übergabe der Bereichssyntax `..` entfernt _jeden_ Wert aus dem
Vektor.

Wir müssen die `drop`-Implementierung von `ThreadPool` also so aktualisieren:

<Listing file-name="src/lib.rs">

```rust
{{#rustdoc_include ../listings/ch21-web-server/no-listing-04-update-drop-definition/src/lib.rs:here}}
```

</Listing>

Das behebt den Compilerfehler und erfordert keine weiteren Änderungen an unserem
Code. Beachte, dass das unwrap, weil drop während eines Panics aufgerufen werden
kann, ebenfalls einen Panic auslösen und so einen doppelten Panic verursachen
könnte, der das Programm sofort abstürzen lässt und jedes laufende Aufräumen
beendet. Für ein Beispielprogramm ist das in Ordnung, für Produktivcode wird es
aber nicht empfohlen.

### Den Threads signalisieren, nicht mehr auf Aufträge zu lauschen {#signaling-to-the-threads-to-stop-listening-for-jobs}

Mit all den Änderungen, die wir vorgenommen haben, kompiliert unser Code ohne
Warnungen. Die schlechte Nachricht ist aber, dass dieser Code noch nicht so
funktioniert, wie wir es wollen. Der Knackpunkt ist die Logik in den Closures,
die von den Threads der `Worker`-Instanzen ausgeführt werden: Im Moment rufen
wir `join` auf, aber das beendet die Threads nicht, weil sie in einer endlosen
`loop` nach Aufträgen suchen. Wenn wir versuchen, unseren `ThreadPool` mit
unserer aktuellen `drop`-Implementierung zu verwerfen, blockiert der
Haupt-Thread für immer und wartet darauf, dass der erste Thread fertig wird.

Um dieses Problem zu beheben, brauchen wir eine Änderung in der
`drop`-Implementierung von `ThreadPool` und dann eine Änderung in der Schleife
des `Worker`.

Zuerst ändern wir die `drop`-Implementierung von `ThreadPool` so, dass sie den
`sender` ausdrücklich verwirft, bevor sie darauf wartet, dass die Threads fertig
werden. Listing 21-23 zeigt die Änderungen an `ThreadPool`, um `sender`
ausdrücklich zu verwerfen. Anders als beim Thread _müssen_ wir hier eine
`Option` verwenden, um `sender` mit `Option::take` aus `ThreadPool`
herausverschieben zu können.

<Listing number="21-23" file-name="src/lib.rs" caption="`sender` ausdrücklich verwerfen, bevor die `Worker`-Threads zusammengeführt werden">

```rust,noplayground,not_desired_behavior
{{#rustdoc_include ../listings/ch21-web-server/listing-21-23/src/lib.rs:here}}
```

</Listing>

Das Verwerfen von `sender` schließt den Kanal, was anzeigt, dass keine weiteren
Nachrichten gesendet werden. Wenn das passiert, geben alle Aufrufe von `recv`,
die die `Worker`-Instanzen in der Endlosschleife ausführen, einen Fehler zurück.
In Listing 21-24 ändern wir die Schleife des `Worker` so, dass sie in diesem
Fall geordnet verlassen wird, was bedeutet, dass die Threads fertig werden, wenn
die `drop`-Implementierung von `ThreadPool` `join` auf ihnen aufruft.

<Listing number="21-24" file-name="src/lib.rs" caption="Die Schleife ausdrücklich verlassen, wenn `recv` einen Fehler zurückgibt">

```rust,noplayground
{{#rustdoc_include ../listings/ch21-web-server/listing-21-24/src/lib.rs:here}}
```

</Listing>

Um diesen Code in Aktion zu sehen, ändern wir `main` so, dass nur zwei Anfragen
angenommen werden, bevor der Server geordnet heruntergefahren wird, wie in
Listing 21-25 gezeigt.

<Listing number="21-25" file-name="src/main.rs" caption="Den Server nach dem Bedienen von zwei Anfragen herunterfahren, indem die Schleife verlassen wird">

```rust,ignore
{{#rustdoc_include ../listings/ch21-web-server/listing-21-25/src/main.rs:here}}
```

</Listing>

Bei einem echten Webserver würdest du nicht wollen, dass er nach nur zwei
bedienten Anfragen herunterfährt. Dieser Code demonstriert nur, dass das
geordnete Herunterfahren und Aufräumen funktioniert.

Die Methode `take` ist im Trait `Iterator` definiert und begrenzt die Iteration
auf höchstens die ersten beiden Elemente. Der `ThreadPool` verlässt am Ende von
`main` den Gültigkeitsbereich (_scope_), und die `drop`-Implementierung wird
ausgeführt.

Starte den Server mit `cargo run` und stelle drei Anfragen. Die dritte Anfrage
sollte einen Fehler liefern, und in deinem Terminal solltest du eine Ausgabe
ähnlich dieser sehen:

<!-- manual-regeneration
cd listings/ch21-web-server/listing-21-25
cargo run
curl http://127.0.0.1:7878
curl http://127.0.0.1:7878
curl http://127.0.0.1:7878
third request will error because server will have shut down
copy output below
Can't automate because the output depends on making requests
-->

```console
$ cargo run
   Compiling hello v0.1.0 (file:///projects/hello)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.41s
     Running `target/debug/hello`
Worker 0 got a job; executing.
Shutting down.
Shutting down worker 0
Worker 3 got a job; executing.
Worker 1 disconnected; shutting down.
Worker 2 disconnected; shutting down.
Worker 3 disconnected; shutting down.
Worker 0 disconnected; shutting down.
Shutting down worker 1
Shutting down worker 2
Shutting down worker 3
```

Vielleicht siehst du eine andere Reihenfolge der `Worker`-IDs und der
ausgegebenen Nachrichten. An den Nachrichten können wir sehen, wie dieser Code
funktioniert: Die `Worker`-Instanzen 0 und 3 haben die ersten beiden Anfragen
bekommen. Der Server hat nach der zweiten Verbindung aufgehört, Verbindungen
anzunehmen, und die `Drop`-Implementierung auf `ThreadPool` beginnt mit der
Ausführung, bevor `Worker 3` überhaupt mit seinem Auftrag beginnt. Das Verwerfen
von `sender` trennt die Verbindung zu allen `Worker`-Instanzen und weist sie an,
sich zu beenden. Die `Worker`-Instanzen geben jeweils eine Nachricht aus, wenn
ihre Verbindung getrennt wird, und dann ruft der Thread-Pool `join` auf, um
darauf zu warten, dass jeder `Worker`-Thread fertig wird.

Beachte einen interessanten Aspekt dieser speziellen Ausführung: Der
`ThreadPool` hat den `sender` verworfen, und bevor irgendein `Worker` einen
Fehler erhalten hat, haben wir versucht, `Worker 0` zusammenzuführen. `Worker 0`
hatte noch keinen Fehler von `recv` bekommen, also hat der Haupt-Thread
blockiert und darauf gewartet, dass `Worker 0` fertig wird. In der Zwischenzeit
hat `Worker 3` einen Auftrag erhalten, und dann haben alle Threads einen Fehler
erhalten. Als `Worker 0` fertig war, hat der Haupt-Thread darauf gewartet, dass
die übrigen `Worker`-Instanzen fertig werden. Zu diesem Zeitpunkt hatten sie
alle ihre Schleifen verlassen und angehalten.

Glückwunsch! Wir haben unser Projekt jetzt abgeschlossen; wir haben einen
einfachen Webserver, der einen Thread-Pool verwendet, um asynchron zu antworten.
Wir können den Server geordnet herunterfahren, wobei alle Threads im Pool
aufgeräumt werden.

Hier ist der vollständige Code zum Nachschlagen:

<Listing file-name="src/main.rs">

```rust,ignore
{{#rustdoc_include ../listings/ch21-web-server/no-listing-07-final-code/src/main.rs}}
```

</Listing>

<Listing file-name="src/lib.rs">

```rust,noplayground
{{#rustdoc_include ../listings/ch21-web-server/no-listing-07-final-code/src/lib.rs}}
```

</Listing>

Wir könnten hier noch mehr tun! Wenn du dieses Projekt weiter verbessern
möchtest, hier sind einige Ideen:

- Füge `ThreadPool` und seinen öffentlichen Methoden mehr Dokumentation hinzu.
- Füge Tests für die Funktionalität der Bibliothek hinzu.
- Ersetze Aufrufe von `unwrap` durch eine robustere Fehlerbehandlung.
- Verwende `ThreadPool`, um eine andere Aufgabe als das Beantworten von
  Webanfragen zu erledigen.
- Suche auf [crates.io](https://crates.io/) einen Thread-Pool-Crate und
  implementiere stattdessen mit diesem Crate einen ähnlichen Webserver.
  Vergleiche dann seine API und Robustheit mit dem Thread-Pool, den wir
  implementiert haben.

## Zusammenfassung {#summary}

Gut gemacht! Du hast das Ende des Buches erreicht! Wir möchten dir dafür danken,
dass du uns auf dieser Tour durch Rust begleitet hast. Du bist jetzt bereit,
deine eigenen Rust-Projekte umzusetzen und bei den Projekten anderer zu helfen.
Denk daran, dass es eine einladende Community anderer Rustaceans gibt, die dir
gern bei allen Herausforderungen helfen, denen du auf deiner Reise mit Rust
begegnest.
