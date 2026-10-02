<!-- Old headings. Do not remove or links may break. -->

<a id="turning-our-single-threaded-server-into-a-multithreaded-server"></a>
<a id="from-single-threaded-to-multithreaded-server"></a>

## Vom Single-Thread- zum Multithread-Server {#from-a-single-threaded-to-a-multithreaded-server}

Im Moment verarbeitet der Server jede Anfrage der Reihe nach, das heißt, er
verarbeitet eine zweite Verbindung erst, wenn die Verarbeitung der ersten
Verbindung abgeschlossen ist. Würde der Server immer mehr Anfragen erhalten,
wäre diese serielle Ausführung immer weniger optimal. Wenn der Server eine
Anfrage erhält, deren Verarbeitung lange dauert, müssen nachfolgende Anfragen
warten, bis die lange Anfrage fertig ist, selbst wenn die neuen Anfragen schnell
verarbeitet werden könnten. Das müssen wir beheben, aber zuerst sehen wir uns
das Problem in Aktion an.

<!-- Old headings. Do not remove or links may break. -->

<a id="simulating-a-slow-request-in-the-current-server-implementation"></a>

### Eine langsame Anfrage simulieren {#simulating-a-slow-request}

Wir sehen uns an, wie sich eine langsam verarbeitete Anfrage auf andere Anfragen
an unsere aktuelle Server-Implementierung auswirken kann. Listing 21-10
implementiert die Behandlung einer Anfrage an _/sleep_ mit einer simulierten
langsamen Antwort, die den Server vor dem Antworten fünf Sekunden lang schlafen
lässt.

<Listing number="21-10" file-name="src/main.rs" caption="Eine langsame Anfrage simulieren, indem fünf Sekunden lang geschlafen wird">

```rust,no_run
{{#rustdoc_include ../listings/ch21-web-server/listing-21-10/src/main.rs:here}}
```

</Listing>

Da wir jetzt drei Fälle haben, sind wir von `if` zu `match` gewechselt. Wir
müssen ausdrücklich einen Slice von `request_line` abgleichen, um per
Pattern-Matching mit den String-Literalwerten zu vergleichen; `match` führt
keine automatische Referenzierung und Dereferenzierung durch, wie es die
Gleichheitsmethode tut.

Der erste Arm ist derselbe wie der `if`-Block aus Listing 21-9. Der zweite Arm
passt auf eine Anfrage an _/sleep_. Wenn diese Anfrage eingeht, schläft der
Server fünf Sekunden lang, bevor er die erfolgreiche HTML-Seite rendert. Der
dritte Arm ist derselbe wie der `else`-Block aus Listing 21-9.

Du siehst, wie primitiv unser Server ist: Echte Bibliotheken würden das Erkennen
mehrerer Anfragen viel weniger umständlich handhaben!

Starte den Server mit `cargo run`. Öffne dann zwei Browserfenster: eines für
_http://127.0.0.1:7878_ und das andere für _http://127.0.0.1:7878/sleep_. Wenn
du wie zuvor ein paarmal den URI _/_ eingibst, wirst du sehen, dass er schnell
antwortet. Wenn du aber _/sleep_ eingibst und dann _/_ lädst, wirst du sehen,
dass _/_ wartet, bis `sleep` seine vollen fünf Sekunden geschlafen hat, bevor es
lädt.

Es gibt mehrere Techniken, mit denen wir verhindern könnten, dass sich Anfragen
hinter einer langsamen Anfrage stauen, darunter die Verwendung von async, wie
wir es in Kapitel 17 getan haben; wir werden einen Thread-Pool implementieren.

### Den Durchsatz mit einem Thread-Pool verbessern {#improving-throughput-with-a-thread-pool}

Ein _Thread-Pool_ ist eine Gruppe erzeugter Threads, die bereitstehen und darauf
warten, eine Aufgabe zu bearbeiten. Wenn das Programm eine neue Aufgabe erhält,
weist es die Aufgabe einem der Threads im Pool zu, und dieser Thread verarbeitet
die Aufgabe. Die übrigen Threads im Pool stehen für alle anderen Aufgaben zur
Verfügung, die eingehen, während der erste Thread arbeitet. Wenn der erste
Thread mit der Verarbeitung seiner Aufgabe fertig ist, kehrt er in den Pool der
untätigen Threads zurück und ist bereit, eine neue Aufgabe zu bearbeiten. Mit
einem Thread-Pool kannst du Verbindungen nebenläufig verarbeiten und so den
Durchsatz deines Servers erhöhen.

Wir begrenzen die Anzahl der Threads im Pool auf eine kleine Zahl, um uns vor
DoS-Angriffen zu schützen; würde unser Programm für jede eingehende Anfrage
einen neuen Thread erzeugen, könnte jemand, der 10 Millionen Anfragen an unseren
Server stellt, verheerenden Schaden anrichten, indem er alle Ressourcen unseres
Servers aufbraucht und die Verarbeitung von Anfragen zum Erliegen bringt.

Statt unbegrenzt viele Threads zu erzeugen, lassen wir daher eine feste Anzahl
von Threads im Pool warten. Eingehende Anfragen werden zur Verarbeitung an den
Pool gesendet. Der Pool verwaltet eine Warteschlange eingehender Anfragen. Jeder
Thread im Pool holt sich eine Anfrage aus dieser Warteschlange, bearbeitet die
Anfrage und fragt dann die Warteschlange nach einer weiteren Anfrage. Mit diesem
Design können wir bis zu _`N`_ Anfragen nebenläufig verarbeiten, wobei _`N`_ die
Anzahl der Threads ist. Wenn jeder Thread auf eine langwierige Anfrage
antwortet, können sich nachfolgende Anfragen immer noch in der Warteschlange
stauen, aber wir haben die Anzahl der langwierigen Anfragen erhöht, die wir
bewältigen können, bevor es so weit kommt.

Diese Technik ist nur eine von vielen Möglichkeiten, den Durchsatz eines
Webservers zu verbessern. Weitere Optionen, die du erkunden könntest, sind das
Fork/Join-Modell, das asynchrone I/O-Modell mit einem Thread und das asynchrone
I/O-Modell mit mehreren Threads. Wenn dich dieses Thema interessiert, kannst du
mehr über andere Lösungen lesen und versuchen, sie zu implementieren; mit einer
systemnahen Sprache wie Rust sind all diese Optionen möglich.

Bevor wir mit der Implementierung eines Thread-Pools beginnen, sprechen wir
darüber, wie die Verwendung des Pools aussehen sollte. Wenn du Code entwirfst,
kann es helfen, zuerst die Schnittstelle für die Nutzer zu schreiben, um dein
Design zu lenken. Schreibe die API des Codes so, dass sie so strukturiert ist,
wie du sie aufrufen möchtest; implementiere dann die Funktionalität innerhalb
dieser Struktur, statt erst die Funktionalität zu implementieren und dann die
öffentliche API zu entwerfen.

Ähnlich wie wir im Projekt in Kapitel 12 testgetriebene Entwicklung verwendet
haben, verwenden wir hier compilergetriebene Entwicklung. Wir schreiben den
Code, der die gewünschten Funktionen aufruft, und sehen uns dann die Fehler des
Compilers an, um zu bestimmen, was wir als Nächstes ändern sollten, damit der
Code funktioniert. Bevor wir das tun, untersuchen wir jedoch als Ausgangspunkt
die Technik, die wir nicht verwenden werden.

<!-- Old headings. Do not remove or links may break. -->

<a id="code-structure-if-we-could-spawn-a-thread-for-each-request"></a>

#### Für jede Anfrage einen Thread erzeugen {#spawning-a-thread-for-each-request}

Sehen wir uns zunächst an, wie unser Code aussehen könnte, wenn er für jede
Verbindung einen neuen Thread erzeugen würde. Wie bereits erwähnt, ist das wegen
der Probleme mit einer potenziell unbegrenzten Anzahl erzeugter Threads nicht
unser endgültiger Plan, aber es ist ein Ausgangspunkt, um zuerst einen
funktionierenden Multithread-Server zu bekommen. Dann fügen wir den Thread-Pool
als Verbesserung hinzu, und der Vergleich der beiden Lösungen fällt leichter.

Listing 21-11 zeigt die Änderungen an `main`, mit denen in der `for`-Schleife
für jeden Stream ein neuer Thread erzeugt wird, der ihn bearbeitet.

<Listing number="21-11" file-name="src/main.rs" caption="Für jeden Stream einen neuen Thread erzeugen">

```rust,no_run
{{#rustdoc_include ../listings/ch21-web-server/listing-21-11/src/main.rs:here}}
```

</Listing>

Wie du in Kapitel 16 gelernt hast, erzeugt `thread::spawn` einen neuen Thread
und führt dann den Code in der Closure im neuen Thread aus. Wenn du diesen Code
ausführst und _/sleep_ in deinem Browser lädst und dann _/_ in zwei weiteren
Browser-Tabs, wirst du tatsächlich sehen, dass die Anfragen an _/_ nicht warten
müssen, bis _/sleep_ fertig ist. Wie wir aber erwähnt haben, wird das System
dadurch irgendwann überlastet, weil du ohne jede Begrenzung neue Threads
erzeugen würdest.

Vielleicht erinnerst du dich auch aus Kapitel 17 daran, dass genau das die Art
von Situation ist, in der async und await wirklich glänzen! Behalte das im
Hinterkopf, während wir den Thread-Pool bauen, und überlege, was mit async
anders oder gleich aussehen würde.

<!-- Old headings. Do not remove or links may break. -->

<a id="creating-a-similar-interface-for-a-finite-number-of-threads"></a>

#### Eine begrenzte Anzahl von Threads erzeugen {#creating-a-finite-number-of-threads}

Unser Thread-Pool soll auf eine ähnliche, vertraute Weise funktionieren, sodass
der Wechsel von Threads zu einem Thread-Pool keine großen Änderungen am Code
erfordert, der unsere API verwendet. Listing 21-12 zeigt die hypothetische
Schnittstelle für ein Struct `ThreadPool`, das wir anstelle von `thread::spawn`
verwenden wollen.

<Listing number="21-12" file-name="src/main.rs" caption="Unsere ideale Schnittstelle für `ThreadPool`">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch21-web-server/listing-21-12/src/main.rs:here}}
```

</Listing>

Wir verwenden `ThreadPool::new`, um einen neuen Thread-Pool mit einer
konfigurierbaren Anzahl von Threads zu erstellen, in diesem Fall vier. Dann hat
`pool.execute` in der `for`-Schleife eine ähnliche Schnittstelle wie
`thread::spawn`, indem es eine Closure nimmt, die der Pool für jeden Stream
ausführen soll. Wir müssen `pool.execute` so implementieren, dass es die Closure
nimmt und sie einem Thread im Pool zur Ausführung übergibt. Dieser Code
kompiliert noch nicht, aber wir versuchen es, damit uns der Compiler zeigen
kann, wie wir ihn korrigieren.

<!-- Old headings. Do not remove or links may break. -->

<a id="building-the-threadpool-struct-using-compiler-driven-development"></a>

#### `ThreadPool` mit compilergetriebener Entwicklung bauen {#building-threadpool-using-compiler-driven-development}

Nimm die Änderungen aus Listing 21-12 in _src/main.rs_ vor, und dann lassen wir
uns von den Compilerfehlern aus `cargo check` durch die Entwicklung leiten. Hier
ist der erste Fehler, den wir bekommen:

```console
{{#include ../listings/ch21-web-server/listing-21-12/output.txt}}
```

Großartig! Dieser Fehler sagt uns, dass wir einen Typ oder ein Modul
`ThreadPool` brauchen, also bauen wir jetzt eines. Unsere
`ThreadPool`-Implementierung ist unabhängig von der Art der Arbeit, die unser
Webserver erledigt. Wandeln wir den Crate `hello` daher von einem Binary-Crate
in einen Library-Crate um, der unsere `ThreadPool`-Implementierung enthält.
Nachdem wir zu einem Library-Crate gewechselt sind, könnten wir die separate
Thread-Pool-Bibliothek auch für jede andere Arbeit verwenden, die wir mit einem
Thread-Pool erledigen wollen, nicht nur zum Beantworten von Webanfragen.

Erstelle eine Datei _src/lib.rs_ mit folgendem Inhalt, der einfachsten
Definition eines Structs `ThreadPool`, die wir vorerst haben können:

<Listing file-name="src/lib.rs">

```rust,noplayground
{{#rustdoc_include ../listings/ch21-web-server/no-listing-01-define-threadpool-struct/src/lib.rs}}
```

</Listing>

Bearbeite dann die Datei _main.rs_, um `ThreadPool` aus dem Library-Crate in den
Gültigkeitsbereich (_scope_) zu bringen, indem du den folgenden Code am Anfang
von _src/main.rs_ hinzufügst:

<Listing file-name="src/main.rs">

```rust,ignore
{{#rustdoc_include ../listings/ch21-web-server/no-listing-01-define-threadpool-struct/src/main.rs:here}}
```

</Listing>

Dieser Code funktioniert immer noch nicht, aber prüfen wir ihn erneut, um den
nächsten Fehler zu bekommen, den wir beheben müssen:

```console
{{#include ../listings/ch21-web-server/no-listing-01-define-threadpool-struct/output.txt}}
```

Dieser Fehler zeigt an, dass wir als Nächstes eine assoziierte Funktion namens
`new` für `ThreadPool` erstellen müssen. Außerdem wissen wir, dass `new` einen
Parameter haben muss, der `4` als Argument akzeptieren kann, und eine
`ThreadPool`-Instanz zurückgeben soll. Implementieren wir die einfachste
Funktion `new`, die diese Merkmale hat:

<Listing file-name="src/lib.rs">

```rust,noplayground
{{#rustdoc_include ../listings/ch21-web-server/no-listing-02-impl-threadpool-new/src/lib.rs}}
```

</Listing>

Wir haben `usize` als Typ des Parameters `size` gewählt, weil wir wissen, dass
eine negative Anzahl von Threads keinen Sinn ergibt. Außerdem wissen wir, dass
wir diese `4` als Anzahl der Elemente in einer Collection von Threads verwenden
werden, und genau dafür ist der Typ `usize` da, wie im Abschnitt
[„Ganzzahltypen“][integer-types]<!--
ignore --> in Kapitel 3 besprochen.

Prüfen wir den Code erneut:

```console
{{#include ../listings/ch21-web-server/no-listing-02-impl-threadpool-new/output.txt}}
```

Jetzt tritt der Fehler auf, weil wir keine Methode `execute` auf `ThreadPool`
haben. Erinnere dich an den Abschnitt
[„Eine begrenzte Anzahl von Threads
erzeugen“](#creating-a-finite-number-of-threads)<!-- ignore -->, in dem wir
entschieden haben, dass unser Thread-Pool eine ähnliche Schnittstelle wie
`thread::spawn` haben soll. Außerdem implementieren wir die Funktion `execute`
so, dass sie die übergebene Closure nimmt und sie einem untätigen Thread im Pool
zur Ausführung übergibt.

Wir definieren die Methode `execute` auf `ThreadPool` so, dass sie eine Closure
als Parameter nimmt. Erinnere dich an den Abschnitt
[„Erfasste Werte aus
Closures herausverschieben“][moving-out-of-closures]<!-- ignore --> in Kapitel
13, dass wir Closures mit drei verschiedenen Traits als Parameter nehmen können:
`Fn`, `FnMut` und `FnOnce`. Wir müssen entscheiden, welche Art von Closure wir
hier verwenden. Wir wissen, dass wir am Ende etwas Ähnliches tun werden wie die
Implementierung von `thread::spawn` in der Standardbibliothek, also können wir
uns ansehen, welche Bounds die Signatur von `thread::spawn` für ihren Parameter
hat. Die Dokumentation zeigt uns Folgendes:

```rust,ignore
pub fn spawn<F, T>(f: F) -> JoinHandle<T>
    where
        F: FnOnce() -> T,
        F: Send + 'static,
        T: Send + 'static,
```

Uns interessiert hier der Typparameter `F`; der Typparameter `T` bezieht sich
auf den Rückgabewert, und der interessiert uns nicht. Wir sehen, dass `spawn`
`FnOnce` als Trait-Bound für `F` verwendet. Das ist wahrscheinlich auch das, was
wir wollen, denn wir werden das Argument, das wir in `execute` bekommen,
letztlich an `spawn` übergeben. Wir können außerdem zuversichtlich sein, dass
`FnOnce` der Trait ist, den wir verwenden wollen, weil der Thread, der eine
Anfrage ausführt, die Closure dieser Anfrage nur ein einziges Mal ausführt, was
zum `Once` in `FnOnce` passt.

Der Typparameter `F` hat außerdem den Trait-Bound `Send` und den Lifetime-Bound
`'static`, die in unserer Situation nützlich sind: Wir brauchen `Send`, um die
Closure von einem Thread in einen anderen zu übertragen, und `'static`, weil wir
nicht wissen, wie lange der Thread für die Ausführung brauchen wird. Erstellen
wir eine Methode `execute` auf `ThreadPool`, die einen generischen Parameter vom
Typ `F` mit diesen Bounds nimmt:

<Listing file-name="src/lib.rs">

```rust,noplayground
{{#rustdoc_include ../listings/ch21-web-server/no-listing-03-define-execute/src/lib.rs:here}}
```

</Listing>

Wir verwenden weiterhin das `()` nach `FnOnce`, weil dieses `FnOnce` eine
Closure darstellt, die keine Parameter nimmt und den Unit-Typ `()` zurückgibt.
Genau wie bei Funktionsdefinitionen kann der Rückgabetyp in der Signatur
weggelassen werden, aber selbst wenn wir keine Parameter haben, brauchen wir die
Klammern.

Auch das ist wieder die einfachste Implementierung der Methode `execute`: Sie
tut nichts, aber wir versuchen nur, unseren Code zum Kompilieren zu bringen.
Prüfen wir ihn erneut:

```console
{{#include ../listings/ch21-web-server/no-listing-03-define-execute/output.txt}}
```

Er kompiliert! Beachte aber, dass du im Browser die Fehler siehst, die wir zu
Beginn des Kapitels gesehen haben, wenn du `cargo run` ausprobierst und im
Browser eine Anfrage stellst. Unsere Bibliothek ruft die an `execute` übergebene
Closure noch gar nicht auf!

> Note: Ein Spruch, den du über Sprachen mit strengen Compilern wie Haskell und
> Rust hören wirst, lautet: „Wenn der Code kompiliert, funktioniert er.“ Aber
> dieser Spruch gilt nicht allgemein. Unser Projekt kompiliert, tut aber
> überhaupt nichts! Würden wir ein echtes, vollständiges Projekt bauen, wäre
> jetzt ein guter Zeitpunkt, um mit dem Schreiben von Unit-Tests zu beginnen,
> die prüfen, dass der Code kompiliert _und_ das gewünschte Verhalten hat.

Überlege: Was wäre hier anders, wenn wir statt einer Closure ein Future
ausführen würden?

#### Die Anzahl der Threads in `new` prüfen {#validating-the-number-of-threads-in-new}

Mit den Parametern von `new` und `execute` tun wir noch nichts. Implementieren
wir die Rümpfe dieser Funktionen mit dem gewünschten Verhalten. Denken wir zu
Beginn über `new` nach. Zuvor haben wir für den Parameter `size` einen
vorzeichenlosen Typ gewählt, weil ein Pool mit einer negativen Anzahl von
Threads keinen Sinn ergibt. Ein Pool mit null Threads ergibt aber auch keinen
Sinn, und doch ist null ein völlig gültiger `usize`. Wir fügen Code hinzu, der
prüft, ob `size` größer als null ist, bevor wir eine `ThreadPool`-Instanz
zurückgeben, und lassen das Programm mit dem Makro `assert!` einen Panic
auslösen, wenn es eine Null erhält, wie in Listing 21-13 gezeigt.

<Listing number="21-13" file-name="src/lib.rs" caption="`ThreadPool::new` so implementieren, dass ein Panic ausgelöst wird, wenn `size` null ist">

```rust,noplayground
{{#rustdoc_include ../listings/ch21-web-server/listing-21-13/src/lib.rs:here}}
```

</Listing>

Außerdem haben wir unserem `ThreadPool` mit Dokumentationskommentaren etwas
Dokumentation hinzugefügt. Beachte, dass wir guter Dokumentationspraxis gefolgt
sind, indem wir einen Abschnitt hinzugefügt haben, der die Situationen nennt, in
denen unsere Funktion einen Panic auslösen kann, wie in Kapitel 14 besprochen.
Führe `cargo doc --open` aus und klicke auf das Struct `ThreadPool`, um zu
sehen, wie die erzeugte Dokumentation für `new` aussieht!

Statt das Makro `assert!` hinzuzufügen, wie wir es hier getan haben, könnten wir
`new` in `build` umwandeln und ein `Result` zurückgeben, so wie wir es im
I/O-Projekt in Listing 12-9 mit `Config::build` getan haben. Wir haben aber
entschieden, dass der Versuch, einen Thread-Pool ganz ohne Threads zu erstellen,
in diesem Fall ein nicht behebbarer Fehler sein soll. Wenn du ehrgeizig bist,
versuche, eine Funktion namens `build` mit der folgenden Signatur zu schreiben,
um sie mit der Funktion `new` zu vergleichen:

```rust,ignore
pub fn build(size: usize) -> Result<ThreadPool, PoolCreationError> {
```

#### Platz zum Speichern der Threads schaffen {#creating-space-to-store-the-threads}

Jetzt, da wir sicherstellen können, dass wir eine gültige Anzahl von Threads im
Pool speichern, können wir diese Threads erzeugen und im Struct `ThreadPool`
speichern, bevor wir das Struct zurückgeben. Aber wie „speichern“ wir einen
Thread? Sehen wir uns noch einmal die Signatur von `thread::spawn` an:

```rust,ignore
pub fn spawn<F, T>(f: F) -> JoinHandle<T>
    where
        F: FnOnce() -> T,
        F: Send + 'static,
        T: Send + 'static,
```

Die Funktion `spawn` gibt ein `JoinHandle<T>` zurück, wobei `T` der Typ ist, den
die Closure zurückgibt. Versuchen wir ebenfalls, `JoinHandle` zu verwenden, und
sehen wir, was passiert. In unserem Fall bearbeiten die Closures, die wir an den
Thread-Pool übergeben, die Verbindung und geben nichts zurück, also ist `T` der
Unit-Typ `()`.

Der Code in Listing 21-14 kompiliert, erzeugt aber noch keine Threads. Wir haben
die Definition von `ThreadPool` so geändert, dass sie einen Vektor von
`thread::JoinHandle<()>`-Instanzen enthält, den Vektor mit einer Kapazität von
`size` initialisiert, eine `for`-Schleife eingerichtet, die Code zum Erzeugen
der Threads ausführen wird, und eine `ThreadPool`-Instanz zurückgegeben, die sie
enthält.

<Listing number="21-14" file-name="src/lib.rs" caption="Einen Vektor für `ThreadPool` erstellen, der die Threads aufnimmt">

```rust,ignore,not_desired_behavior
{{#rustdoc_include ../listings/ch21-web-server/listing-21-14/src/lib.rs:here}}
```

</Listing>

Wir haben `std::thread` im Library-Crate in den Gültigkeitsbereich gebracht,
weil wir `thread::JoinHandle` als Typ der Elemente im Vektor in `ThreadPool`
verwenden.

Sobald eine gültige Größe empfangen wurde, erzeugt unser `ThreadPool` einen
neuen Vektor, der `size` Elemente aufnehmen kann. Die Funktion `with_capacity`
erfüllt dieselbe Aufgabe wie `Vec::new`, aber mit einem wichtigen Unterschied:
Sie alloziert vorab Platz im Vektor. Weil wir wissen, dass wir `size` Elemente
im Vektor speichern müssen, ist diese Allokation im Voraus etwas effizienter als
`Vec::new`, das seine Größe ändert, während Elemente eingefügt werden.

Wenn du `cargo check` erneut ausführst, sollte es erfolgreich sein.

<!-- Old headings. Do not remove or links may break. -->

<a id ="a-worker-struct-responsible-for-sending-code-from-the-threadpool-to-a-thread"></a>

#### Code vom `ThreadPool` an einen Thread senden {#sending-code-from-the-threadpool-to-a-thread}

Wir haben in der `for`-Schleife in Listing 21-14 einen Kommentar zum Erzeugen
von Threads hinterlassen. Hier sehen wir uns an, wie wir tatsächlich Threads
erzeugen. Die Standardbibliothek stellt `thread::spawn` zum Erzeugen von Threads
bereit, und `thread::spawn` erwartet Code, den der Thread ausführen soll, sobald
er erzeugt wurde. In unserem Fall wollen wir die Threads aber erzeugen und sie
auf Code _warten_ lassen, den wir später senden. Die Thread-Implementierung der
Standardbibliothek bietet keine Möglichkeit dafür; wir müssen das von Hand
implementieren.

Wir implementieren dieses Verhalten, indem wir zwischen dem `ThreadPool` und den
Threads eine neue Datenstruktur einführen, die dieses neue Verhalten verwaltet.
Wir nennen diese Datenstruktur _Worker_, ein gängiger Begriff in
Pool-Implementierungen. Der `Worker` holt sich Code, der ausgeführt werden muss,
und führt den Code in seinem Thread aus.

Denk an Menschen, die in der Küche eines Restaurants arbeiten: Die Mitarbeiter
warten, bis Bestellungen von Gästen eingehen, und sind dann dafür
verantwortlich, diese Bestellungen anzunehmen und zuzubereiten.

Statt eines Vektors von `JoinHandle<()>`-Instanzen speichern wir im Thread-Pool
Instanzen des Structs `Worker`. Jeder `Worker` speichert eine einzige
`JoinHandle<()>`-Instanz. Dann implementieren wir auf `Worker` eine Methode, die
eine Closure mit auszuführendem Code nimmt und sie zur Ausführung an den bereits
laufenden Thread sendet. Außerdem geben wir jedem `Worker` eine `id`, damit wir
beim Protokollieren oder Debuggen zwischen den verschiedenen `Worker`-Instanzen
im Pool unterscheiden können.

Hier ist der neue Ablauf beim Erstellen eines `ThreadPool`. Den Code, der die
Closure an den Thread sendet, implementieren wir, nachdem wir `Worker` auf diese
Weise eingerichtet haben:

1. Ein Struct `Worker` definieren, das eine `id` und ein `JoinHandle<()>`
   enthält.
2. `ThreadPool` so ändern, dass es einen Vektor von `Worker`-Instanzen enthält.
3. Eine Funktion `Worker::new` definieren, die eine `id`-Nummer nimmt und eine
   `Worker`-Instanz zurückgibt, die die `id` und einen mit einer leeren Closure
   erzeugten Thread enthält.
4. In `ThreadPool::new` den Zähler der `for`-Schleife verwenden, um eine `id` zu
   erzeugen, mit dieser `id` einen neuen `Worker` erstellen und den `Worker` im
   Vektor speichern.

Wenn du eine Herausforderung suchst, versuche, diese Änderungen selbst zu
implementieren, bevor du dir den Code in Listing 21-15 ansiehst.

Bereit? Hier ist Listing 21-15 mit einer Möglichkeit, die vorangehenden
Änderungen vorzunehmen.

<Listing number="21-15" file-name="src/lib.rs" caption="`ThreadPool` so ändern, dass es `Worker`-Instanzen statt direkt Threads enthält">

```rust,noplayground
{{#rustdoc_include ../listings/ch21-web-server/listing-21-15/src/lib.rs:here}}
```

</Listing>

Wir haben den Namen des Felds von `ThreadPool` von `threads` in `workers`
geändert, weil es jetzt `Worker`-Instanzen statt `JoinHandle<()>`-Instanzen
enthält. Wir verwenden den Zähler in der `for`-Schleife als Argument für
`Worker::new` und speichern jeden neuen `Worker` im Vektor namens `workers`.

Externer Code (wie unser Server in _src/main.rs_) muss die
Implementierungsdetails, wie ein Struct `Worker` innerhalb von `ThreadPool`
verwendet wird, nicht kennen, daher machen wir das Struct `Worker` und seine
Funktion `new` privat. Die Funktion `Worker::new` verwendet die `id`, die wir
ihr geben, und speichert eine `JoinHandle<()>`-Instanz, die durch das Erzeugen
eines neuen Threads mit einer leeren Closure entsteht.

> Note: Wenn das Betriebssystem keinen Thread erzeugen kann, weil nicht genug
> Systemressourcen vorhanden sind, löst `thread::spawn` einen Panic aus. Das
> führt dazu, dass unser ganzer Server einen Panic auslöst, obwohl die Erzeugung
> einiger Threads erfolgreich sein könnte. Der Einfachheit halber ist dieses
> Verhalten in Ordnung, aber in einer Thread-Pool-Implementierung für den
> Produktivbetrieb würdest du wahrscheinlich stattdessen
> [`std::thread::Builder`][builder]<!-- ignore --> und seine Methode
> [`spawn`][builder-spawn]<!-- ignore --> verwenden, die ein `Result`
> zurückgibt.

Dieser Code kompiliert und speichert die Anzahl von `Worker`-Instanzen, die wir
als Argument an `ThreadPool::new` übergeben haben. Aber wir verarbeiten _immer
noch nicht_ die Closure, die wir in `execute` bekommen. Sehen wir uns als
Nächstes an, wie das geht.

#### Anfragen über Kanäle an Threads senden {#sending-requests-to-threads-via-channels}

Das nächste Problem, das wir angehen, ist, dass die an `thread::spawn`
übergebenen Closures überhaupt nichts tun. Derzeit bekommen wir die Closure, die
wir ausführen wollen, in der Methode `execute`. Wir müssen `thread::spawn` aber
schon beim Erstellen jedes `Worker` während der Erstellung des `ThreadPool` eine
Closure zum Ausführen übergeben.

Die `Worker`-Structs, die wir gerade erstellt haben, sollen den auszuführenden
Code aus einer Warteschlange holen, die im `ThreadPool` gehalten wird, und
diesen Code zur Ausführung an ihren Thread senden.

Die Kanäle, die wir in Kapitel 16 kennengelernt haben – eine einfache
Möglichkeit, zwischen zwei Threads zu kommunizieren –, wären für diesen
Anwendungsfall perfekt. Wir verwenden einen Kanal als Warteschlange für Aufträge
(_jobs_), und `execute` sendet einen Auftrag vom `ThreadPool` an die
`Worker`-Instanzen, die den Auftrag an ihren Thread senden. Hier ist der Plan:

1. Der `ThreadPool` erzeugt einen Kanal und behält den Sender.
2. Jeder `Worker` behält den Empfänger.
3. Wir erstellen ein neues Struct `Job`, das die Closures enthält, die wir über
   den Kanal senden wollen.
4. Die Methode `execute` sendet den Auftrag, den sie ausführen will, über den
   Sender.
5. In seinem Thread durchläuft der `Worker` seinen Empfänger in einer Schleife
   und führt die Closures aller Aufträge aus, die er empfängt.

Beginnen wir damit, in `ThreadPool::new` einen Kanal zu erzeugen und den Sender
in der `ThreadPool`-Instanz zu halten, wie in Listing 21-16 gezeigt. Das Struct
`Job` enthält vorerst nichts, wird aber der Typ der Elemente sein, die wir über
den Kanal senden.

<Listing number="21-16" file-name="src/lib.rs" caption="`ThreadPool` so ändern, dass es den Sender eines Kanals speichert, der `Job`-Instanzen überträgt">

```rust,noplayground
{{#rustdoc_include ../listings/ch21-web-server/listing-21-16/src/lib.rs:here}}
```

</Listing>

In `ThreadPool::new` erzeugen wir unseren neuen Kanal und lassen den Pool den
Sender halten. Das kompiliert erfolgreich.

Versuchen wir, jedem `Worker` einen Empfänger des Kanals zu übergeben, während
der Thread-Pool den Kanal erzeugt. Wir wissen, dass wir den Empfänger in dem
Thread verwenden wollen, den die `Worker`-Instanzen erzeugen, daher verweisen
wir in der Closure auf den Parameter `receiver`. Der Code in Listing 21-17
kompiliert noch nicht ganz.

<Listing number="21-17" file-name="src/lib.rs" caption="Den Empfänger an jeden `Worker` übergeben">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch21-web-server/listing-21-17/src/lib.rs:here}}
```

</Listing>

Wir haben einige kleine und einfache Änderungen vorgenommen: Wir übergeben den
Empfänger an `Worker::new` und verwenden ihn dann innerhalb der Closure.

Wenn wir versuchen, diesen Code zu prüfen, bekommen wir diesen Fehler:

```console
{{#include ../listings/ch21-web-server/listing-21-17/output.txt}}
```

Der Code versucht, `receiver` an mehrere `Worker`-Instanzen zu übergeben. Das
funktioniert nicht, wie du dich aus Kapitel 16 erinnern wirst: Die
Kanalimplementierung, die Rust bereitstellt, hat mehrere _Produzenten_, aber
einen einzigen _Konsumenten_. Das bedeutet, dass wir nicht einfach das
konsumierende Ende des Kanals klonen können, um diesen Code zu korrigieren. Wir
wollen eine Nachricht auch nicht mehrfach an mehrere Konsumenten senden; wir
wollen eine Liste von Nachrichten mit mehreren `Worker`-Instanzen, sodass jede
Nachricht genau einmal verarbeitet wird.

Außerdem erfordert das Herausnehmen eines Auftrags aus der Warteschlange des
Kanals, den `receiver` zu verändern, daher brauchen die Threads eine sichere
Möglichkeit, `receiver` gemeinsam zu nutzen und zu verändern; andernfalls
könnten Race-Conditions (_race conditions_) auftreten (wie in Kapitel 16
behandelt).

Erinnere dich an die threadsicheren Smart-Pointer aus Kapitel 16: Um die
Ownership über mehrere Threads hinweg zu teilen und den Threads zu erlauben, den
Wert zu verändern, müssen wir `Arc<Mutex<T>>` verwenden. Der Typ `Arc` lässt
mehrere `Worker`-Instanzen den Empfänger besitzen, und `Mutex` stellt sicher,
dass jeweils nur ein `Worker` einen Auftrag vom Empfänger bekommt. Listing 21-18
zeigt die Änderungen, die wir vornehmen müssen.

<Listing number="21-18" file-name="src/lib.rs" caption="Den Empfänger mit `Arc` und `Mutex` unter den `Worker`-Instanzen teilen">

```rust,noplayground
{{#rustdoc_include ../listings/ch21-web-server/listing-21-18/src/lib.rs:here}}
```

</Listing>

In `ThreadPool::new` legen wir den Empfänger in einen `Arc` und einen `Mutex`.
Für jeden neuen `Worker` klonen wir den `Arc`, um den Referenzzähler zu erhöhen,
damit die `Worker`-Instanzen die Ownership am Empfänger teilen können.

Mit diesen Änderungen kompiliert der Code! Wir kommen voran!

#### Die Methode `execute` implementieren {#implementing-the-execute-method}

Implementieren wir endlich die Methode `execute` auf `ThreadPool`. Außerdem
ändern wir `Job` von einem Struct in einen Typalias für ein Trait-Objekt, das
den Typ der Closure enthält, die `execute` erhält. Wie im Abschnitt
[„Typsynonyme und Typaliasse“][type-aliases]<!-- ignore --> in Kapitel 20
besprochen, ermöglichen es Typaliasse, lange Typen zur einfacheren Verwendung
kürzer zu machen. Sieh dir Listing 21-19 an.

<Listing number="21-19" file-name="src/lib.rs" caption="Einen Typalias `Job` für eine `Box` erstellen, die jede Closure enthält, und den Auftrag dann über den Kanal senden">

```rust,noplayground
{{#rustdoc_include ../listings/ch21-web-server/listing-21-19/src/lib.rs:here}}
```

</Listing>

Nachdem wir mit der Closure, die wir in `execute` bekommen, eine neue
`Job`-Instanz erstellt haben, senden wir diesen Auftrag über das sendende Ende
des Kanals. Wir rufen `unwrap` auf `send` auf, für den Fall, dass das Senden
fehlschlägt. Das könnte zum Beispiel passieren, wenn wir die Ausführung all
unserer Threads stoppen, sodass das empfangende Ende keine neuen Nachrichten
mehr empfängt. Im Moment können wir die Ausführung unserer Threads nicht
stoppen: Unsere Threads laufen weiter, solange der Pool existiert. Wir verwenden
`unwrap`, weil wir wissen, dass der Fehlerfall nicht eintreten wird, der
Compiler das aber nicht weiß.

Aber wir sind noch nicht ganz fertig! Im `Worker` _verweist_ unsere an
`thread::spawn` übergebene Closure immer noch nur auf das empfangende Ende des
Kanals. Stattdessen muss die Closure in einer Endlosschleife das empfangende
Ende des Kanals nach einem Auftrag fragen und den Auftrag ausführen, sobald sie
einen bekommt. Nehmen wir die in Listing 21-20 gezeigte Änderung an
`Worker::new` vor.

<Listing number="21-20" file-name="src/lib.rs" caption="Die Aufträge im Thread der `Worker`-Instanz empfangen und ausführen">

```rust,noplayground
{{#rustdoc_include ../listings/ch21-web-server/listing-21-20/src/lib.rs:here}}
```

</Listing>

Hier rufen wir zuerst `lock` auf dem `receiver` auf, um den Mutex zu erwerben,
und dann `unwrap`, um bei Fehlern einen Panic auszulösen. Das Erwerben eines
Locks kann fehlschlagen, wenn sich der Mutex in einem _vergifteten_ (_poisoned_)
Zustand befindet. Das kann passieren, wenn ein anderer Thread einen Panic
ausgelöst hat, während er den Lock hielt, statt den Lock freizugeben. In dieser
Situation ist es richtig, `unwrap` aufzurufen, damit dieser Thread einen Panic
auslöst. Du kannst dieses `unwrap` gern in ein `expect` mit einer Fehlermeldung
ändern, die für dich aussagekräftig ist.

Wenn wir den Lock auf den Mutex bekommen, rufen wir `recv` auf, um einen `Job`
vom Kanal zu empfangen. Ein letztes `unwrap` übergeht auch hier etwaige Fehler,
die auftreten könnten, wenn der Thread, der den Sender hält, beendet wurde,
ähnlich wie die Methode `send` `Err` zurückgibt, wenn der Empfänger beendet
wird.

Der Aufruf von `recv` blockiert. Wenn es also noch keinen Auftrag gibt, wartet
der aktuelle Thread, bis ein Auftrag verfügbar wird. Der `Mutex<T>` stellt
sicher, dass jeweils nur ein `Worker`-Thread versucht, einen Auftrag
anzufordern.

Unser Thread-Pool funktioniert jetzt! Führe ihn mit `cargo run` aus und stelle
einige Anfragen:

<!-- manual-regeneration
cd listings/ch21-web-server/listing-21-20
cargo run
make some requests to 127.0.0.1:7878
Can't automate because the output depends on making requests
-->

```console
$ cargo run
   Compiling hello v0.1.0 (file:///projects/hello)
warning: field `workers` is never read
 --> src/lib.rs:7:5
  |
6 | pub struct ThreadPool {
  |            ---------- field in this struct
7 |     workers: Vec<Worker>,
  |     ^^^^^^^
  |
  = note: `#[warn(dead_code)]` on by default

warning: fields `id` and `thread` are never read
  --> src/lib.rs:48:5
   |
47 | struct Worker {
   |        ------ fields in this struct
48 |     id: usize,
   |     ^^
49 |     thread: thread::JoinHandle<()>,
   |     ^^^^^^

warning: `hello` (lib) generated 2 warnings
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 4.91s
     Running `target/debug/hello`
Worker 0 got a job; executing.
Worker 2 got a job; executing.
Worker 1 got a job; executing.
Worker 3 got a job; executing.
Worker 0 got a job; executing.
Worker 2 got a job; executing.
Worker 1 got a job; executing.
Worker 3 got a job; executing.
Worker 0 got a job; executing.
Worker 2 got a job; executing.
```

Erfolg! Wir haben jetzt einen Thread-Pool, der Verbindungen asynchron ausführt.
Es werden nie mehr als vier Threads erzeugt, sodass unser System nicht
überlastet wird, wenn der Server viele Anfragen erhält. Wenn wir eine Anfrage an
_/sleep_ stellen, kann der Server andere Anfragen bedienen, indem ein anderer
Thread sie ausführt.

> Note: Wenn du _/sleep_ gleichzeitig in mehreren Browserfenstern öffnest,
> werden sie möglicherweise nacheinander im Abstand von fünf Sekunden geladen.
> Manche Webbrowser führen mehrere Instanzen derselben Anfrage aus
> Caching-Gründen nacheinander aus. Diese Einschränkung wird nicht von unserem
> Webserver verursacht.

Das ist ein guter Zeitpunkt, um innezuhalten und zu überlegen, wie der Code in
Listing 21-18, 21-19 und 21-20 anders aussähe, wenn wir für die zu erledigende
Arbeit Futures statt einer Closure verwenden würden. Welche Typen würden sich
ändern? Wie würden sich die Methodensignaturen unterscheiden, falls überhaupt?
Welche Teile des Codes würden gleich bleiben?

Nachdem du in Kapitel 17 und Kapitel 19 die `while let`-Schleife kennengelernt
hast, fragst du dich vielleicht, warum wir den Code des `Worker`-Threads nicht
so geschrieben haben, wie in Listing 21-21 gezeigt.

<Listing number="21-21" file-name="src/lib.rs" caption="Eine alternative Implementierung von `Worker::new` mit `while let`">

```rust,ignore,not_desired_behavior
{{#rustdoc_include ../listings/ch21-web-server/listing-21-21/src/lib.rs:here}}
```

</Listing>

Dieser Code kompiliert und läuft, führt aber nicht zum gewünschten
Thread-Verhalten: Eine langsame Anfrage führt weiterhin dazu, dass andere
Anfragen auf ihre Verarbeitung warten müssen. Der Grund ist etwas subtil: Das
Struct `Mutex` hat keine öffentliche Methode `unlock`, weil die Ownership am
Lock auf der Lifetime des `MutexGuard<T>` innerhalb des
`LockResult<MutexGuard<T>>` basiert, das die Methode `lock` zurückgibt. Zur
Kompilierzeit kann der Borrow-Checker dann die Regel durchsetzen, dass auf eine
durch einen `Mutex` geschützte Ressource nur zugegriffen werden kann, wenn wir
den Lock halten. Diese Implementierung kann aber auch dazu führen, dass der Lock
länger als beabsichtigt gehalten wird, wenn wir nicht auf die Lifetime des
`MutexGuard<T>` achten.

Der Code in Listing 21-20, der
`let job =
receiver.lock().unwrap().recv().unwrap();` verwendet, funktioniert,
weil bei `let` alle temporären Werte, die im Ausdruck rechts vom
Gleichheitszeichen verwendet werden, sofort verworfen (_dropped_) werden, wenn
die `let`-Anweisung endet. `while
let` (sowie `if let` und `match`) verwirft
temporäre Werte dagegen erst am Ende des zugehörigen Blocks. In Listing 21-21
bleibt der Lock für die Dauer des Aufrufs von `job()` gehalten, sodass andere
`Worker`-Instanzen keine Aufträge empfangen können.

[type-aliases]: ch20-03-advanced-types.html#type-synonyms-and-type-aliases
[integer-types]: ch03-02-data-types.html#integer-types
[moving-out-of-closures]: ch13-01-closures.html#moving-captured-values-out-of-closures
[builder]: https://doc.rust-lang.org/std/thread/struct.Builder.html
[builder-spawn]: https://doc.rust-lang.org/std/thread/struct.Builder.html#method.spawn
