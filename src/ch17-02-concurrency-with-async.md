<!-- Old headings. Do not remove or links may break. -->

<a id="concurrency-with-async"></a>

## Nebenläufigkeit mit Async anwenden {#applying-concurrency-with-async}

In diesem Abschnitt wenden wir Async auf einige derselben Herausforderungen der
Nebenläufigkeit an, die wir in Kapitel 16 mit Threads angegangen sind. Da wir
dort bereits über viele der zentralen Ideen gesprochen haben, konzentrieren wir
uns in diesem Abschnitt darauf, was sich zwischen Threads und Futures
unterscheidet.

In vielen Fällen sind die APIs für Nebenläufigkeit mit Async denen für Threads
sehr ähnlich. In anderen Fällen unterscheiden sie sich deutlich. Selbst wenn die
APIs bei Threads und Async ähnlich _aussehen_, verhalten sie sich oft
unterschiedlich – und sie haben fast immer unterschiedliche
Performance-Merkmale.

<!-- Old headings. Do not remove or links may break. -->

<a id="counting"></a>

### Einen neuen Task mit `spawn_task` erzeugen {#creating-a-new-task-with-spawn_task}

Die erste Operation, die wir im Abschnitt
[„Einen neuen Thread mit `spawn` erzeugen“][thread-spawn]<!-- ignore --> in
Kapitel 16 angegangen sind, war das Hochzählen in zwei getrennten Threads.
Machen wir dasselbe mit Async. Das Crate `trpl` stellt eine Funktion
`spawn_task` bereit, die der API `thread::spawn` sehr ähnlich sieht, und eine
Funktion `sleep`, die eine asynchrone Version der API `thread::sleep` ist.
Zusammen können wir damit das Zählbeispiel implementieren, wie in Listing 17-6
gezeigt.

<Listing number="17-6" caption="Einen neuen Task erzeugen, der etwas ausgibt, während der Haupt-Task etwas anderes ausgibt" file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-06/src/main.rs:all}}
```

</Listing>

Als Ausgangspunkt richten wir unsere Funktion `main` mit `trpl::block_on` ein,
damit unsere Funktion auf oberster Ebene asynchron sein kann.

> Note: Ab hier enthält jedes Beispiel in diesem Kapitel genau diesen
> umhüllenden Code mit `trpl::block_on` in `main`, daher lassen wir ihn oft weg,
> so wie wir es bei `main` tun. Denk daran, ihn in deinen Code aufzunehmen!

Dann schreiben wir in diesem Block zwei Schleifen, die jeweils einen Aufruf von
`trpl::sleep` enthalten, der eine halbe Sekunde (500 Millisekunden) wartet,
bevor die nächste Nachricht gesendet wird. Eine Schleife legen wir in den Rumpf
eines `trpl::spawn_task` und die andere in eine `for`-Schleife auf oberster
Ebene. Außerdem fügen wir hinter den `sleep`-Aufrufen ein `await` hinzu.

Dieser Code verhält sich ähnlich wie die Implementierung mit Threads –
einschließlich der Tatsache, dass die Nachrichten in deinem eigenen Terminal
beim Ausführen in einer anderen Reihenfolge erscheinen können:

<!-- Not extracting output because changes to this output aren't significant;
the changes are likely to be due to the threads running differently rather than
changes in the compiler -->

```text
hi number 1 from the second task!
hi number 1 from the first task!
hi number 2 from the first task!
hi number 2 from the second task!
hi number 3 from the first task!
hi number 3 from the second task!
hi number 4 from the first task!
hi number 4 from the second task!
hi number 5 from the first task!
```

Diese Version endet, sobald die `for`-Schleife im Rumpf des asynchronen
Hauptblocks fertig ist, weil der von `spawn_task` erzeugte Task beendet wird,
wenn die Funktion `main` endet. Soll er laufen, bis der Task fertig ist, musst
du ein Join-Handle verwenden, um zu warten, bis der erste Task fertig ist. Bei
Threads haben wir die Methode `join` verwendet, um zu „blockieren“, bis der
Thread fertig war. In Listing 17-7 können wir dafür `await` verwenden, weil das
Task-Handle selbst ein Future ist. Sein Typ `Output` ist ein `Result`, daher
packen wir es nach dem Abwarten auch mit unwrap aus.

<Listing number="17-7" caption="`await` mit einem Join-Handle verwenden, um einen Task vollständig auszuführen" file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-07/src/main.rs:handle}}
```

</Listing>

Diese angepasste Version läuft, bis _beide_ Schleifen fertig sind:

<!-- Not extracting output because changes to this output aren't significant;
the changes are likely to be due to the threads running differently rather than
changes in the compiler -->

```text
hi number 1 from the second task!
hi number 1 from the first task!
hi number 2 from the first task!
hi number 2 from the second task!
hi number 3 from the first task!
hi number 3 from the second task!
hi number 4 from the first task!
hi number 4 from the second task!
hi number 5 from the first task!
hi number 6 from the first task!
hi number 7 from the first task!
hi number 8 from the first task!
hi number 9 from the first task!
```

Bisher sieht es so aus, als lieferten Async und Threads ähnliche Ergebnisse, nur
mit anderer Syntax: `await` statt eines Aufrufs von `join` auf dem Join-Handle
und das Abwarten der `sleep`-Aufrufe.

Der größere Unterschied ist, dass wir dafür keinen weiteren
Betriebssystem-Thread erzeugen mussten. Tatsächlich müssen wir hier nicht einmal
einen Task erzeugen. Da async-Blöcke zu anonymen Futures kompiliert werden,
können wir jede Schleife in einen async-Block legen und die Runtime mit der
Funktion `trpl::join` beide vollständig ausführen lassen.

Im Abschnitt
[„Warten, bis alle Threads fertig sind“][join-handles]<!-- ignore --> in Kapitel
16 haben wir gezeigt, wie man die Methode `join` auf dem Typ `JoinHandle`
verwendet, der beim Aufruf von `std::thread::spawn` zurückgegeben wird. Die
Funktion `trpl::join` ist ähnlich, aber für Futures. Übergibst du ihr zwei
Futures, erzeugt sie ein einziges neues Future, dessen Ausgabe ein Tupel mit der
Ausgabe jedes übergebenen Futures ist, sobald _beide_ fertig sind. In Listing
17-8 verwenden wir daher `trpl::join`, um zu warten, bis sowohl `fut1` als auch
`fut2` fertig sind. Wir warten _nicht_ `fut1` und `fut2` ab, sondern das neue
Future, das `trpl::join` erzeugt. Die Ausgabe ignorieren wir, weil sie nur ein
Tupel mit zwei Unit-Werten ist.

<Listing number="17-8" caption="Mit `trpl::join` zwei anonyme Futures abwarten" file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-08/src/main.rs:join}}
```

</Listing>

Wenn wir das ausführen, sehen wir, dass beide Futures vollständig ausgeführt
werden:

<!-- Not extracting output because changes to this output aren't significant;
the changes are likely to be due to the threads running differently rather than
changes in the compiler -->

```text
hi number 1 from the first task!
hi number 1 from the second task!
hi number 2 from the first task!
hi number 2 from the second task!
hi number 3 from the first task!
hi number 3 from the second task!
hi number 4 from the first task!
hi number 4 from the second task!
hi number 5 from the first task!
hi number 6 from the first task!
hi number 7 from the first task!
hi number 8 from the first task!
hi number 9 from the first task!
```

Jetzt siehst du jedes Mal genau dieselbe Reihenfolge, was sich stark von dem
unterscheidet, was wir bei Threads und bei `trpl::spawn_task` in Listing 17-7
gesehen haben. Das liegt daran, dass die Funktion `trpl::join` _fair_ ist: Sie
prüft jedes Future gleich oft, wechselt zwischen ihnen ab und lässt nie eines
vorauseilen, wenn das andere bereit ist. Bei Threads entscheidet das
Betriebssystem, welcher Thread geprüft wird und wie lange er laufen darf. Bei
asynchronem Rust entscheidet die Runtime, welcher Task geprüft wird. (In der
Praxis werden die Details kompliziert, weil eine Async-Runtime unter der Haube
Betriebssystem-Threads verwenden kann, um Nebenläufigkeit zu verwalten. Fairness
zu garantieren, kann für eine Runtime daher mehr Arbeit bedeuten – aber es ist
trotzdem möglich!) Runtimes müssen Fairness nicht für jede Operation garantieren
und bieten oft verschiedene APIs, mit denen du wählen kannst, ob du Fairness
willst oder nicht.

Probier einige dieser Variationen beim Abwarten der Futures aus und sieh dir an,
was sie bewirken:

- Entferne den async-Block um eine oder beide Schleifen.
- Warte jeden async-Block direkt nach seiner Definition ab.
- Verpacke nur die erste Schleife in einen async-Block und warte das
  resultierende Future nach dem Rumpf der zweiten Schleife ab.

Als zusätzliche Herausforderung versuch herauszufinden, welche Ausgabe es in
jedem Fall geben wird, _bevor_ du den Code ausführst!

<!-- Old headings. Do not remove or links may break. -->

<a id="message-passing"></a>
<a id="counting-up-on-two-tasks-using-message-passing"></a>

### Daten per Nachrichtenübermittlung zwischen zwei Tasks senden {#sending-data-between-two-tasks-using-message-passing}

Auch das Teilen von Daten zwischen Futures wird dir vertraut vorkommen: Wir
verwenden wieder Nachrichtenübermittlung, diesmal aber mit asynchronen Versionen
der Typen und Funktionen. Wir gehen einen etwas anderen Weg als im Abschnitt
[„Daten per Nachrichtenübermittlung zwischen Threads übertragen“][message-passing-threads]<!-- ignore -->
in Kapitel 16, um einige der wesentlichen Unterschiede zwischen Nebenläufigkeit
mit Threads und mit Futures zu veranschaulichen. In Listing 17-9 beginnen wir
mit nur einem einzigen async-Block – wir erzeugen _keinen_ separaten Task, so
wie wir einen separaten Thread erzeugt haben.

<Listing number="17-9" caption="Einen asynchronen Kanal erzeugen und die beiden Hälften `tx` und `rx` zuweisen" file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-09/src/main.rs:channel}}
```

</Listing>

Hier verwenden wir `trpl::channel`, eine asynchrone Version der Kanal-API mit
mehreren Produzenten und einem Konsumenten, die wir in Kapitel 16 mit Threads
verwendet haben. Die asynchrone Version der API unterscheidet sich nur wenig von
der Version mit Threads: Sie verwendet einen veränderlichen (_mutable_) statt
eines unveränderlichen (_immutable_) Empfängers `rx`, und ihre Methode `recv`
erzeugt ein Future, das wir abwarten müssen, statt den Wert direkt zu erzeugen.
Jetzt können wir Nachrichten vom Sender an den Empfänger senden. Beachte, dass
wir keinen separaten Thread und nicht einmal einen Task erzeugen müssen; wir
müssen nur den Aufruf `rx.recv` abwarten.

Die synchrone Methode `Receiver::recv` in `std::mpsc::channel` blockiert, bis
sie eine Nachricht empfängt. Die Methode `trpl::Receiver::recv` tut das nicht,
weil sie asynchron ist. Statt zu blockieren, gibt sie die Kontrolle an die
Runtime zurück, bis entweder eine Nachricht empfangen wird oder die Sendeseite
des Kanals geschlossen wird. Den Aufruf `send` warten wir dagegen nicht ab, weil
er nicht blockiert. Das muss er auch nicht, weil der Kanal, in den wir senden,
unbegrenzt ist.

> Note: Da all dieser asynchrone Code in einem async-Block in einem Aufruf von
> `trpl::block_on` läuft, kann alles darin Blockieren vermeiden. Der Code
> _außerhalb_ davon blockiert aber, bis die Funktion `block_on` zurückkehrt.
> Genau das ist der Sinn der Funktion `trpl::block_on`: Mit ihr kannst du
> _wählen_, wo auf eine Menge asynchronen Codes blockiert wird und wo damit der
> Übergang zwischen synchronem und asynchronem Code liegt.

Beachte zwei Dinge an diesem Beispiel. Erstens kommt die Nachricht sofort an.
Zweitens verwenden wir hier zwar ein Future, aber es gibt noch keine
Nebenläufigkeit. Alles im Listing geschieht nacheinander, genauso wie es ohne
Futures geschehen würde.

Kümmern wir uns um den ersten Punkt, indem wir eine Reihe von Nachrichten senden
und zwischen ihnen schlafen, wie in Listing 17-10 gezeigt.

<!-- We cannot test this one because it never stops! -->

<Listing number="17-10" caption="Mehrere Nachrichten über den asynchronen Kanal senden und empfangen und zwischen den Nachrichten mit einem `await` schlafen" file-name="src/main.rs">

```rust,ignore
{{#rustdoc_include ../listings/ch17-async-await/listing-17-10/src/main.rs:many-messages}}
```

</Listing>

Neben dem Senden der Nachrichten müssen wir sie auch empfangen. Da wir in diesem
Fall wissen, wie viele Nachrichten kommen, könnten wir das von Hand tun, indem
wir `rx.recv().await` viermal aufrufen. In der Praxis warten wir aber meist auf
eine _unbekannte_ Anzahl von Nachrichten, daher müssen wir so lange warten, bis
wir feststellen, dass keine Nachrichten mehr kommen.

In Listing 16-10 haben wir eine `for`-Schleife verwendet, um alle Elemente zu
verarbeiten, die von einem synchronen Kanal empfangen wurden. Rust hat aber noch
keine Möglichkeit, eine `for`-Schleife mit einer _asynchron erzeugten_ Folge von
Elementen zu verwenden, daher müssen wir eine Schleife verwenden, die wir noch
nicht gesehen haben: die bedingte Schleife `while let`. Sie ist die
Schleifenversion des Konstrukts `if let`, das wir im Abschnitt
[„Knapper Kontrollfluss mit `if
let` und `let...else`“][if-let]<!-- ignore --> in
Kapitel 6 gesehen haben. Die Schleife wird so lange ausgeführt, wie das
angegebene Pattern auf den Wert passt.

Der Aufruf `rx.recv` erzeugt ein Future, das wir abwarten. Die Runtime pausiert
das Future, bis es bereit ist. Sobald eine Nachricht ankommt, wird das Future zu
`Some(message)` aufgelöst, und zwar so oft, wie eine Nachricht ankommt. Wenn der
Kanal geschlossen wird, wird das Future, unabhängig davon, ob _überhaupt_
Nachrichten angekommen sind, stattdessen zu `None` aufgelöst, um anzuzeigen,
dass es keine weiteren Werte gibt und wir daher mit dem Polling aufhören sollten
– also mit dem Abwarten.

Die Schleife `while let` führt all das zusammen. Ist das Ergebnis des Aufrufs
`rx.recv().await` `Some(message)`, erhalten wir Zugriff auf die Nachricht und
können sie im Schleifenrumpf verwenden, genau wie bei `if let`. Ist das Ergebnis
`None`, endet die Schleife. Jedes Mal, wenn die Schleife einen Durchlauf
abschließt, trifft sie wieder auf den Await-Punkt, sodass die Runtime sie erneut
pausiert, bis eine weitere Nachricht ankommt.

Der Code sendet und empfängt jetzt erfolgreich alle Nachrichten. Leider gibt es
noch einige Probleme. Zum einen kommen die Nachrichten nicht im Abstand von
einer halben Sekunde an. Sie kommen alle auf einmal an, 2 Sekunden (2.000
Millisekunden) nachdem wir das Programm gestartet haben. Zum anderen endet
dieses Programm nie! Stattdessen wartet es ewig auf neue Nachrichten. Du musst
es mit <kbd>Strg</kbd>-<kbd>C</kbd> beenden.

#### Code innerhalb eines async-Blocks wird linear ausgeführt {#code-within-one-async-block-executes-linearly}

Untersuchen wir zuerst, warum die Nachrichten alle auf einmal nach der vollen
Verzögerung ankommen und nicht mit Verzögerungen zwischen den einzelnen
Nachrichten. Innerhalb eines async-Blocks ist die Reihenfolge, in der die
Schlüsselwörter `await` im Code stehen, auch die Reihenfolge, in der sie bei der
Programmausführung ausgeführt werden.

In Listing 17-10 gibt es nur einen async-Block, daher läuft alles darin linear.
Es gibt immer noch keine Nebenläufigkeit. Alle Aufrufe von `tx.send` geschehen,
unterbrochen von allen Aufrufen von `trpl::sleep` und deren Await-Punkten. Erst
dann kommt die Schleife `while let` dazu, einen der `await`-Punkte bei den
`recv`-Aufrufen zu durchlaufen.

Um das gewünschte Verhalten zu erhalten, bei dem die Schlafverzögerung zwischen
den einzelnen Nachrichten stattfindet, müssen wir die Operationen mit `tx` und
`rx` in eigene async-Blöcke legen, wie in Listing 17-11 gezeigt. Dann kann die
Runtime sie mit `trpl::join` jeweils getrennt ausführen, genau wie in Listing
17-8. Wieder warten wir das Ergebnis des Aufrufs von `trpl::join` ab, nicht die
einzelnen Futures. Würden wir die einzelnen Futures nacheinander abwarten,
landeten wir einfach wieder bei einem sequenziellen Ablauf – genau dem, was wir
_nicht_ wollen.

<!-- We cannot test this one because it never stops! -->

<Listing number="17-11" caption="`send` und `recv` in eigene `async`-Blöcke aufteilen und die Futures für diese Blöcke abwarten" file-name="src/main.rs">

```rust,ignore
{{#rustdoc_include ../listings/ch17-async-await/listing-17-11/src/main.rs:futures}}
```

</Listing>

Mit dem angepassten Code in Listing 17-11 werden die Nachrichten im Abstand von
500 Millisekunden ausgegeben statt alle auf einmal nach 2 Sekunden.

#### Ownership in einen async-Block verschieben {#moving-ownership-into-an-async-block}

Das Programm endet aber immer noch nie, weil die Schleife `while let` auf
folgende Weise mit `trpl::join` zusammenwirkt:

- Das von `trpl::join` zurückgegebene Future ist erst fertig, wenn _beide_
  übergebenen Futures fertig sind.
- Das Future `tx_fut` ist fertig, sobald es nach dem Senden der letzten
  Nachricht in `vals` fertig geschlafen hat.
- Das Future `rx_fut` ist erst fertig, wenn die Schleife `while let` endet.
- Die Schleife `while let` endet erst, wenn das Abwarten von `rx.recv` `None`
  liefert.
- Das Abwarten von `rx.recv` gibt erst `None` zurück, wenn das andere Ende des
  Kanals geschlossen ist.
- Der Kanal wird nur geschlossen, wenn wir `rx.close` aufrufen oder wenn die
  Senderseite `tx` verworfen (_dropped_) wird.
- Wir rufen `rx.close` nirgends auf, und `tx` wird erst verworfen, wenn der
  äußerste async-Block endet, der an `trpl::block_on` übergeben wird.
- Der Block kann nicht enden, weil er darauf wartet, dass `trpl::join` fertig
  wird, womit wir wieder am Anfang dieser Liste sind.

Im Moment _leiht_ der async-Block, in dem wir die Nachrichten senden, `tx` nur
aus (_borrows_), weil das Senden einer Nachricht keine Ownership erfordert.
Könnten wir `tx` aber in diesen async-Block _verschieben_ (_move_), würde es
verworfen, sobald dieser Block endet. Im Abschnitt
[„Referenzen erfassen oder Ownership übertragen“][capture-or-move]<!-- ignore -->
in Kapitel 13 hast du gelernt, wie man das Schlüsselwort `move` mit Closures
verwendet, und wie im Abschnitt
[„`move`-Closures mit Threads verwenden“][move-threads]<!-- ignore --> in
Kapitel 16 besprochen, müssen wir bei der Arbeit mit Threads oft Daten in
Closures verschieben. Dieselbe grundlegende Dynamik gilt für async-Blöcke, daher
funktioniert das Schlüsselwort `move` mit async-Blöcken genauso wie mit
Closures.

In Listing 17-12 ändern wir den Block, der zum Senden von Nachrichten verwendet
wird, von `async` in `async move`.

<Listing number="17-12" caption="Eine überarbeitete Version des Codes aus Listing 17-11, die sich nach Abschluss korrekt beendet" file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-12/src/main.rs:with-move}}
```

</Listing>

Wenn wir _diese_ Version des Codes ausführen, endet sie ordnungsgemäß, nachdem
die letzte Nachricht gesendet und empfangen wurde. Sehen wir uns als Nächstes
an, was sich ändern müsste, um Daten von mehr als einem Future zu senden.

#### Mehrere Futures mit dem Makro `join!` zusammenführen {#joining-a-number-of-futures-with-the-join-macro}

Dieser asynchrone Kanal ist ebenfalls ein Kanal mit mehreren Produzenten, daher
können wir `clone` auf `tx` aufrufen, wenn wir Nachrichten von mehreren Futures
senden wollen, wie in Listing 17-13 gezeigt.

<Listing number="17-13" caption="Mehrere Produzenten mit async-Blöcken verwenden" file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-13/src/main.rs:here}}
```

</Listing>

Zuerst klonen wir `tx` und erzeugen so außerhalb des ersten async-Blocks `tx1`.
Wir verschieben `tx1` in diesen Block, genau wie zuvor `tx`. Später verschieben
wir dann das ursprüngliche `tx` in einen _neuen_ async-Block, in dem wir weitere
Nachrichten mit einer etwas längeren Verzögerung senden. Diesen neuen
async-Block setzen wir zufällig hinter den async-Block zum Empfangen von
Nachrichten, er könnte aber genauso gut davor stehen. Entscheidend ist die
Reihenfolge, in der die Futures abgewartet werden, nicht die, in der sie erzeugt
werden.

Beide async-Blöcke zum Senden von Nachrichten müssen `async move`-Blöcke sein,
damit sowohl `tx` als auch `tx1` verworfen werden, wenn diese Blöcke fertig
sind. Andernfalls landen wir wieder in derselben Endlosschleife, mit der wir
begonnen haben.

Schließlich wechseln wir von `trpl::join` zu `trpl::join!`, um das zusätzliche
Future zu behandeln: Das Makro `join!` wartet eine beliebige Anzahl von Futures
ab, deren Anzahl wir zur Kompilierzeit kennen. Wie man eine Collection mit einer
unbekannten Anzahl von Futures abwartet, besprechen wir später in diesem
Kapitel.

Jetzt sehen wir alle Nachrichten beider sendenden Futures, und da die sendenden
Futures nach dem Senden leicht unterschiedliche Verzögerungen verwenden, werden
die Nachrichten auch in diesen unterschiedlichen Abständen empfangen:

<!-- Not extracting output because changes to this output aren't significant;
the changes are likely to be due to the threads running differently rather than
changes in the compiler -->

```text
received 'hi'
received 'more'
received 'from'
received 'the'
received 'messages'
received 'future'
received 'for'
received 'you'
```

Wir haben untersucht, wie man mit Nachrichtenübermittlung Daten zwischen Futures
sendet, wie Code innerhalb eines async-Blocks sequenziell läuft, wie man
Ownership in einen async-Block verschiebt und wie man mehrere Futures
zusammenführt. Besprechen wir als Nächstes, wie und warum man der Runtime
mitteilt, dass sie zu einem anderen Task wechseln kann.

{{#quiz ../quizzes/async-02-concurrency-with-async.toml}}

[thread-spawn]: ch16-01-threads.html#creating-a-new-thread-with-spawn
[join-handles]: ch16-01-threads.html#waiting-for-all-threads-to-finish
[message-passing-threads]: ch16-02-message-passing.html
[if-let]: ch06-03-if-let.html
[capture-or-move]: ch13-01-closures.html#capturing-references-or-moving-ownership
[move-threads]: ch16-01-threads.html#using-move-closures-with-threads
