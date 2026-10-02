<!-- Old headings. Do not remove or links may break. -->

<a id="using-message-passing-to-transfer-data-between-threads"></a>

## Daten per Nachrichtenübermittlung zwischen Threads übertragen {#transfer-data-between-threads-with-message-passing}

Ein zunehmend beliebter Ansatz, sichere Nebenläufigkeit zu gewährleisten, ist
die Nachrichtenübermittlung (_message passing_), bei der Threads oder Akteure
kommunizieren, indem sie einander Nachrichten mit Daten senden. Hier ist die
Idee als Slogan aus
[der Dokumentation der Sprache Go](https://golang.org/doc/effective_go.html#concurrency):
„Kommuniziere nicht, indem du Speicher teilst; teile stattdessen Speicher, indem
du kommunizierst.“

Für Nebenläufigkeit mit Nachrichtenübermittlung stellt die Standardbibliothek
von Rust eine Implementierung von Kanälen bereit. Ein _Kanal_ (_channel_) ist
ein allgemeines Programmierkonzept, mit dem Daten von einem Thread an einen
anderen gesendet werden.

Du kannst dir einen Kanal beim Programmieren wie einen Wasserlauf mit einer
Fließrichtung vorstellen, etwa einen Bach oder einen Fluss. Setzt du etwas wie
eine Gummiente in einen Fluss, treibt sie flussabwärts bis zum Ende des
Wasserwegs.

Ein Kanal hat zwei Hälften: einen Sender und einen Empfänger. Die Senderhälfte
ist die Stelle flussaufwärts, an der du die Gummiente in den Fluss setzt, und
die Empfängerhälfte ist die Stelle flussabwärts, an der die Gummiente ankommt.
Ein Teil deines Codes ruft auf dem Sender Methoden mit den Daten auf, die du
senden willst, und ein anderer Teil prüft das empfangende Ende auf eintreffende
Nachrichten. Ein Kanal gilt als _geschlossen_, wenn entweder die Sender- oder
die Empfängerhälfte verworfen (_dropped_) wird.

Hier arbeiten wir uns zu einem Programm vor, das einen Thread hat, der Werte
erzeugt und sie durch einen Kanal schickt, und einen anderen Thread, der die
Werte empfängt und ausgibt. Wir senden einfache Werte über einen Kanal zwischen
Threads, um das Feature zu veranschaulichen. Sobald du mit der Technik vertraut
bist, kannst du Kanäle für beliebige Threads verwenden, die miteinander
kommunizieren müssen, etwa für ein Chatsystem oder ein System, in dem viele
Threads Teile einer Berechnung durchführen und die Teile an einen Thread senden,
der die Ergebnisse zusammenführt.

Zuerst erzeugen wir in Listing 16-6 einen Kanal, ohne etwas damit zu tun.
Beachte, dass das noch nicht kompiliert, weil Rust nicht erkennen kann, welchen
Typ von Werten wir über den Kanal senden wollen.

<Listing number="16-6" file-name="src/main.rs" caption="Einen Kanal erzeugen und die beiden Hälften `tx` und `rx` zuweisen">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch16-fearless-concurrency/listing-16-06/src/main.rs}}
```

</Listing>

Wir erzeugen einen neuen Kanal mit der Funktion `mpsc::channel`; `mpsc` steht
für _multiple producer, single consumer_ (mehrere Produzenten, ein Konsument).
Kurz gesagt bedeutet die Art, wie die Standardbibliothek von Rust Kanäle
implementiert, dass ein Kanal mehrere _sendende_ Enden haben kann, die Werte
erzeugen, aber nur ein _empfangendes_ Ende, das diese Werte verbraucht. Stell
dir mehrere Bäche vor, die zu einem großen Fluss zusammenfließen: Alles, was
einen der Bäche hinuntergeschickt wird, landet am Ende in einem Fluss. Wir
beginnen vorerst mit einem einzigen Produzenten, fügen aber mehrere Produzenten
hinzu, sobald dieses Beispiel funktioniert.

Die Funktion `mpsc::channel` gibt ein Tupel zurück, dessen erstes Element das
sendende Ende ist – der Sender – und dessen zweites Element das empfangende Ende
ist – der Empfänger. Die Abkürzungen `tx` und `rx` werden in vielen Bereichen
traditionell für _transmitter_ (Sender) bzw. _receiver_ (Empfänger) verwendet,
daher benennen wir unsere Variablen so, um das jeweilige Ende zu kennzeichnen.
Wir verwenden eine `let`-Anweisung mit einem Pattern, das die Tupel
destrukturiert; die Verwendung von Patterns in `let`-Anweisungen und das
Destrukturieren besprechen wir in Kapitel 19. Vorerst genügt es zu wissen, dass
eine `let`-Anweisung auf diese Weise eine bequeme Möglichkeit ist, die Teile des
von `mpsc::channel` zurückgegebenen Tupels herauszuholen.

Verschieben (_move_) wir das sendende Ende in einen erzeugten Thread und lassen
es einen String senden, sodass der erzeugte Thread mit dem Haupt-Thread
kommuniziert, wie in Listing 16-7 gezeigt. Das ist so, als würde man
flussaufwärts eine Gummiente in den Fluss setzen oder eine Chatnachricht von
einem Thread an einen anderen senden.

<Listing number="16-7" file-name="src/main.rs" caption='`tx` in einen erzeugten Thread verschieben und `"hi"` senden'>

```rust
{{#rustdoc_include ../listings/ch16-fearless-concurrency/listing-16-07/src/main.rs}}
```

</Listing>

Wieder verwenden wir `thread::spawn`, um einen neuen Thread zu erzeugen, und
dann `move`, um `tx` in die Closure zu verschieben, sodass der erzeugte Thread
`tx` besitzt. Der erzeugte Thread muss den Sender besitzen, um Nachrichten über
den Kanal senden zu können.

Der Sender hat eine Methode `send`, die den Wert nimmt, den wir senden wollen.
Die Methode `send` gibt einen Typ `Result<T, E>` zurück; wurde der Empfänger
also bereits verworfen und gibt es kein Ziel für einen Wert, gibt die
Sendeoperation einen Fehler zurück. In diesem Beispiel rufen wir `unwrap` auf,
um im Fehlerfall einen Panic auszulösen. In einer echten Anwendung würden wir
den Fehler aber richtig behandeln: Lies in Kapitel 9 noch einmal nach, welche
Strategien es für eine richtige Fehlerbehandlung gibt.

In Listing 16-8 holen wir den Wert im Haupt-Thread aus dem Empfänger. Das ist
so, als würde man die Gummiente am Ende des Flusses aus dem Wasser holen oder
eine Chatnachricht empfangen.

<Listing number="16-8" file-name="src/main.rs" caption='Den Wert `"hi"` im Haupt-Thread empfangen und ausgeben'>

```rust
{{#rustdoc_include ../listings/ch16-fearless-concurrency/listing-16-08/src/main.rs}}
```

</Listing>

Der Empfänger hat zwei nützliche Methoden: `recv` und `try_recv`. Wir verwenden
`recv`, kurz für _receive_ (empfangen), das die Ausführung des Haupt-Threads
blockiert und wartet, bis ein Wert durch den Kanal geschickt wird. Sobald ein
Wert gesendet wurde, gibt `recv` ihn in einem `Result<T, E>` zurück. Wird der
Sender geschlossen, gibt `recv` einen Fehler zurück, um zu signalisieren, dass
keine weiteren Werte kommen.

Die Methode `try_recv` blockiert nicht, sondern gibt sofort ein `Result<T, E>`
zurück: einen `Ok`-Wert mit einer Nachricht, falls eine verfügbar ist, und einen
`Err`-Wert, falls diesmal keine Nachrichten da sind. `try_recv` ist nützlich,
wenn dieser Thread während des Wartens auf Nachrichten andere Arbeit zu
erledigen hat: Wir könnten eine Schleife schreiben, die immer wieder `try_recv`
aufruft, eine Nachricht behandelt, falls eine verfügbar ist, und andernfalls
eine Weile andere Arbeit erledigt, bevor sie erneut prüft.

Wir haben in diesem Beispiel der Einfachheit halber `recv` verwendet; der
Haupt-Thread hat außer dem Warten auf Nachrichten nichts zu tun, daher ist es
angemessen, den Haupt-Thread zu blockieren.

Wenn wir den Code in Listing 16-8 ausführen, sehen wir den Wert, den der
Haupt-Thread ausgibt:

<!-- Not extracting output because changes to this output aren't significant;
the changes are likely to be due to the threads running differently rather than
changes in the compiler -->

```text
Got: hi
```

Perfekt!

<!-- Old headings. Do not remove or links may break. -->

<a id="channels-and-ownership-transference"></a>

### Ownership über Kanäle übertragen {#transferring-ownership-through-channels}

Die Ownership-Regeln spielen beim Senden von Nachrichten eine entscheidende
Rolle, weil sie dir helfen, sicheren, nebenläufigen Code zu schreiben. Fehler in
der nebenläufigen Programmierung zu verhindern, ist der Vorteil davon, in deinen
Rust-Programmen durchgehend über Ownership nachzudenken. Machen wir ein
Experiment, um zu zeigen, wie Kanäle und Ownership zusammenwirken, um Probleme
zu verhindern: Wir versuchen, einen Wert `val` im erzeugten Thread zu verwenden,
_nachdem_ wir ihn durch den Kanal geschickt haben. Versuch, den Code in Listing
16-9 zu kompilieren, um zu sehen, warum dieser Code nicht erlaubt ist.

<Listing number="16-9" file-name="src/main.rs" caption="Versuch, `val` zu verwenden, nachdem wir es durch den Kanal geschickt haben">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch16-fearless-concurrency/listing-16-09/src/main.rs}}
```

</Listing>

Hier versuchen wir, `val` auszugeben, nachdem wir es mit `tx.send` durch den
Kanal geschickt haben. Das zu erlauben, wäre eine schlechte Idee: Sobald der
Wert an einen anderen Thread gesendet wurde, könnte dieser Thread ihn verändern
oder verwerfen, bevor wir versuchen, den Wert erneut zu verwenden. Die
Änderungen des anderen Threads könnten wegen inkonsistenter oder nicht
existierender Daten Fehler oder unerwartete Ergebnisse verursachen. Rust gibt
uns aber einen Fehler, wenn wir versuchen, den Code in Listing 16-9 zu
kompilieren:

```console
{{#include ../listings/ch16-fearless-concurrency/listing-16-09/output.txt}}
```

Unser Nebenläufigkeitsfehler hat einen Fehler zur Kompilierzeit verursacht. Die
Funktion `send` übernimmt die Ownership ihres Parameters, und wenn der Wert
verschoben wird, übernimmt der Empfänger die Ownership. Das verhindert, dass wir
den Wert nach dem Senden versehentlich erneut verwenden; das Ownership-System
prüft, dass alles in Ordnung ist.

<!-- Old headings. Do not remove or links may break. -->

<a id="sending-multiple-values-and-seeing-the-receiver-waiting"></a>

### Mehrere Werte senden {#sending-multiple-values}

Der Code in Listing 16-8 hat kompiliert und lief, hat uns aber nicht deutlich
gezeigt, dass zwei getrennte Threads über den Kanal miteinander sprechen.

In Listing 16-10 haben wir einige Änderungen vorgenommen, die beweisen, dass der
Code in Listing 16-8 nebenläufig läuft: Der erzeugte Thread sendet jetzt mehrere
Nachrichten und pausiert zwischen den Nachrichten jeweils eine Sekunde.

<Listing number="16-10" file-name="src/main.rs" caption="Mehrere Nachrichten senden und zwischen ihnen pausieren">

```rust,noplayground
{{#rustdoc_include ../listings/ch16-fearless-concurrency/listing-16-10/src/main.rs}}
```

</Listing>

Diesmal hat der erzeugte Thread einen Vektor von Strings, den wir an den
Haupt-Thread senden wollen. Wir iterieren über sie, senden jeden einzeln und
pausieren dazwischen jeweils, indem wir die Funktion `thread::sleep` mit einem
`Duration`-Wert von einer Sekunde aufrufen.

Im Haupt-Thread rufen wir die Funktion `recv` nicht mehr explizit auf:
Stattdessen behandeln wir `rx` als Iterator. Jeden empfangenen Wert geben wir
aus. Wird der Kanal geschlossen, endet die Iteration.

Wenn du den Code in Listing 16-10 ausführst, solltest du folgende Ausgabe sehen,
mit einer Pause von einer Sekunde zwischen den Zeilen:

<!-- Not extracting output because changes to this output aren't significant;
the changes are likely to be due to the threads running differently rather than
changes in the compiler -->

```text
Got: hi
Got: from
Got: the
Got: thread
```

Da wir in der `for`-Schleife im Haupt-Thread keinen Code haben, der pausiert
oder verzögert, können wir erkennen, dass der Haupt-Thread darauf wartet, Werte
vom erzeugten Thread zu empfangen.

<!-- Old headings. Do not remove or links may break. -->

<a id="creating-multiple-producers-by-cloning-the-transmitter"></a>

### Mehrere Produzenten erzeugen {#creating-multiple-producers}

Wir haben vorhin erwähnt, dass `mpsc` ein Akronym für _multiple producer, single
consumer_ ist. Setzen wir `mpsc` ein und erweitern den Code in Listing 16-10 so,
dass mehrere Threads erzeugt werden, die alle Werte an denselben Empfänger
senden. Das geht, indem wir den Sender klonen, wie in Listing 16-11 gezeigt.

<Listing number="16-11" file-name="src/main.rs" caption="Mehrere Nachrichten von mehreren Produzenten senden">

```rust,noplayground
{{#rustdoc_include ../listings/ch16-fearless-concurrency/listing-16-11/src/main.rs:here}}
```

</Listing>

Diesmal rufen wir `clone` auf dem Sender auf, bevor wir den ersten Thread
erzeugen. Dadurch erhalten wir einen neuen Sender, den wir an den ersten
erzeugten Thread übergeben können. Den ursprünglichen Sender übergeben wir an
einen zweiten erzeugten Thread. So haben wir zwei Threads, die jeweils
unterschiedliche Nachrichten an den einen Empfänger senden.

Wenn du den Code ausführst, sollte deine Ausgabe ungefähr so aussehen:

<!-- Not extracting output because changes to this output aren't significant;
the changes are likely to be due to the threads running differently rather than
changes in the compiler -->

```text
Got: hi
Got: more
Got: from
Got: messages
Got: for
Got: the
Got: thread
Got: you
```

Je nach System siehst du die Werte vielleicht in einer anderen Reihenfolge. Das
macht Nebenläufigkeit sowohl interessant als auch schwierig. Wenn du mit
`thread::sleep` experimentierst und ihm in den verschiedenen Threads
unterschiedliche Werte gibst, wird jeder Lauf noch nichtdeterministischer und
erzeugt jedes Mal eine andere Ausgabe.

Nachdem wir uns angesehen haben, wie Kanäle funktionieren, sehen wir uns eine
andere Methode der Nebenläufigkeit an.

{{#quiz ../quizzes/ch16-02-message-passing.toml}}
