## Code mit Threads gleichzeitig ausführen {#using-threads-to-run-code-simultaneously}

In den meisten heutigen Betriebssystemen wird der Code eines ausgeführten
Programms in einem _Prozess_ ausgeführt, und das Betriebssystem verwaltet
mehrere Prozesse gleichzeitig. Innerhalb eines Programms kannst du ebenfalls
unabhängige Teile haben, die gleichzeitig laufen. Die Features, die diese
unabhängigen Teile ausführen, heißen _Threads_. Ein Webserver könnte zum
Beispiel mehrere Threads haben, damit er auf mehr als eine Anfrage gleichzeitig
antworten kann.

Die Berechnung in deinem Programm auf mehrere Threads aufzuteilen, um mehrere
Aufgaben gleichzeitig auszuführen, kann die Performance verbessern, erhöht aber
auch die Komplexität. Da Threads gleichzeitig laufen können, gibt es keine
inhärente Garantie dafür, in welcher Reihenfolge Teile deines Codes in
verschiedenen Threads ausgeführt werden. Das kann zu Problemen führen, etwa:

- Race-Conditions, bei denen Threads in einer inkonsistenten Reihenfolge auf
  Daten oder Ressourcen zugreifen
- Deadlocks, bei denen zwei Threads aufeinander warten, sodass keiner der beiden
  weitermachen kann
- Bugs, die nur in bestimmten Situationen auftreten und sich schwer zuverlässig
  reproduzieren und beheben lassen

Rust versucht, die negativen Auswirkungen der Verwendung von Threads
abzumildern, aber das Programmieren in einem Kontext mit mehreren Threads
erfordert weiterhin sorgfältiges Nachdenken und eine Codestruktur, die sich von
der in Programmen mit einem einzigen Thread unterscheidet.

Programmiersprachen implementieren Threads auf verschiedene Weise, und viele
Betriebssysteme stellen eine API bereit, die die Programmiersprache aufrufen
kann, um neue Threads zu erzeugen. Die Standardbibliothek von Rust verwendet ein
_1:1_-Modell der Thread-Implementierung, bei dem ein Programm einen
Betriebssystem-Thread pro Sprach-Thread verwendet. Es gibt Crates, die andere
Thread-Modelle implementieren, die andere Kompromisse eingehen als das
1:1-Modell. (Auch das async-System von Rust, das wir im nächsten Kapitel sehen,
bietet einen weiteren Ansatz für Nebenläufigkeit.)

### Einen neuen Thread mit `spawn` erzeugen {#creating-a-new-thread-with-spawn}

Um einen neuen Thread zu erzeugen, rufen wir die Funktion `thread::spawn` auf
und übergeben ihr eine Closure (über Closures haben wir in Kapitel 13
gesprochen), die den Code enthält, den wir im neuen Thread ausführen wollen. Das
Beispiel in Listing 16-1 gibt etwas Text aus einem Haupt-Thread und anderen Text
aus einem neuen Thread aus.

<Listing number="16-1" file-name="src/main.rs" caption="Einen neuen Thread erzeugen, der etwas ausgibt, während der Haupt-Thread etwas anderes ausgibt">

```rust
{{#rustdoc_include ../listings/ch16-fearless-concurrency/listing-16-01/src/main.rs}}
```

</Listing>

Beachte: Wenn der Haupt-Thread eines Rust-Programms fertig ist, werden alle
erzeugten Threads beendet, egal ob sie fertig sind oder nicht. Die Ausgabe
dieses Programms kann jedes Mal etwas anders aussehen, wird aber ungefähr so
aussehen:

<!-- Not extracting output because changes to this output aren't significant;
the changes are likely to be due to the threads running differently rather than
changes in the compiler -->

```text
hi number 1 from the main thread!
hi number 1 from the spawned thread!
hi number 2 from the main thread!
hi number 2 from the spawned thread!
hi number 3 from the main thread!
hi number 3 from the spawned thread!
hi number 4 from the main thread!
hi number 4 from the spawned thread!
hi number 5 from the spawned thread!
```

Die Aufrufe von `thread::sleep` zwingen einen Thread, seine Ausführung für kurze
Zeit anzuhalten, sodass ein anderer Thread laufen kann. Die Threads wechseln
sich wahrscheinlich ab, aber das ist nicht garantiert: Es hängt davon ab, wie
dein Betriebssystem die Threads einplant. In diesem Lauf hat der Haupt-Thread
zuerst ausgegeben, obwohl die Ausgabeanweisung des erzeugten Threads im Code
zuerst steht. Und obwohl wir dem erzeugten Thread gesagt haben, er solle
ausgeben, bis `i` gleich `9` ist, kam er nur bis `5`, bevor der Haupt-Thread
beendet wurde.

Wenn du diesen Code ausführst und nur Ausgaben des Haupt-Threads oder keine
Überschneidungen siehst, versuch, die Zahlen in den Bereichen zu erhöhen, um dem
Betriebssystem mehr Gelegenheiten zu geben, zwischen den Threads zu wechseln.

<!-- Old headings. Do not remove or links may break. -->

<a id="waiting-for-all-threads-to-finish-using-join-handles"></a>

### Warten, bis alle Threads fertig sind {#waiting-for-all-threads-to-finish}

Der Code in Listing 16-1 beendet den erzeugten Thread nicht nur meistens
vorzeitig, weil der Haupt-Thread endet; da es keine Garantie für die Reihenfolge
gibt, in der Threads laufen, können wir auch nicht garantieren, dass der
erzeugte Thread überhaupt ausgeführt wird!

Das Problem, dass der erzeugte Thread nicht läuft oder vorzeitig endet, können
wir beheben, indem wir den Rückgabewert von `thread::spawn` in einer Variable
speichern. Der Rückgabetyp von `thread::spawn` ist `JoinHandle<T>`. Ein
`JoinHandle<T>` ist ein besessener Wert, der, wenn wir die Methode `join` auf
ihm aufrufen, wartet, bis sein Thread fertig ist. Listing 16-2 zeigt, wie man
das `JoinHandle<T>` des in Listing 16-1 erzeugten Threads verwendet und `join`
aufruft, um sicherzustellen, dass der erzeugte Thread fertig wird, bevor `main`
endet.

<Listing number="16-2" file-name="src/main.rs" caption="Ein `JoinHandle<T>` von `thread::spawn` speichern, um zu garantieren, dass der Thread bis zum Ende ausgeführt wird">

```rust
{{#rustdoc_include ../listings/ch16-fearless-concurrency/listing-16-02/src/main.rs}}
```

</Listing>

Der Aufruf von `join` auf dem Handle blockiert den aktuell laufenden Thread, bis
der durch das Handle dargestellte Thread beendet ist. Einen Thread zu
_blockieren_ bedeutet, dass er daran gehindert wird, Arbeit zu verrichten oder
sich zu beenden. Da wir den Aufruf von `join` hinter die `for`-Schleife des
Haupt-Threads gesetzt haben, sollte Listing 16-2 eine Ausgabe ähnlich dieser
erzeugen:

<!-- Not extracting output because changes to this output aren't significant;
the changes are likely to be due to the threads running differently rather than
changes in the compiler -->

```text
hi number 1 from the main thread!
hi number 2 from the main thread!
hi number 1 from the spawned thread!
hi number 3 from the main thread!
hi number 2 from the spawned thread!
hi number 4 from the main thread!
hi number 3 from the spawned thread!
hi number 4 from the spawned thread!
hi number 5 from the spawned thread!
hi number 6 from the spawned thread!
hi number 7 from the spawned thread!
hi number 8 from the spawned thread!
hi number 9 from the spawned thread!
```

Die beiden Threads wechseln sich weiterhin ab, aber der Haupt-Thread wartet
wegen des Aufrufs von `handle.join()` und endet erst, wenn der erzeugte Thread
fertig ist.

Sehen wir uns aber an, was passiert, wenn wir `handle.join()` stattdessen vor
die `for`-Schleife in `main` verschieben, etwa so:

<Listing file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch16-fearless-concurrency/no-listing-01-join-too-early/src/main.rs}}
```

</Listing>

Der Haupt-Thread wartet, bis der erzeugte Thread fertig ist, und führt dann
seine `for`-Schleife aus, sodass die Ausgabe nicht mehr verschränkt ist, wie
hier zu sehen:

<!-- Not extracting output because changes to this output aren't significant;
the changes are likely to be due to the threads running differently rather than
changes in the compiler -->

```text
hi number 1 from the spawned thread!
hi number 2 from the spawned thread!
hi number 3 from the spawned thread!
hi number 4 from the spawned thread!
hi number 5 from the spawned thread!
hi number 6 from the spawned thread!
hi number 7 from the spawned thread!
hi number 8 from the spawned thread!
hi number 9 from the spawned thread!
hi number 1 from the main thread!
hi number 2 from the main thread!
hi number 3 from the main thread!
hi number 4 from the main thread!
```

Kleine Details, etwa wo `join` aufgerufen wird, können beeinflussen, ob deine
Threads gleichzeitig laufen oder nicht.

### `move`-Closures mit Threads verwenden {#using-move-closures-with-threads}

Wir verwenden das Schlüsselwort `move` oft mit Closures, die an `thread::spawn`
übergeben werden, weil die Closure dann die Ownership der Werte übernimmt, die
sie aus der Umgebung verwendet, und so die Ownership dieser Werte von einem
Thread an einen anderen überträgt. In
[„Referenzen erfassen oder Ownership übertragen“][capture]<!-- ignore
--> in Kapitel 13 haben wir `move` im Zusammenhang mit Closures besprochen.
Jetzt konzentrieren wir uns mehr auf das Zusammenspiel von `move` und
`thread::spawn`.

Beachte, dass die Closure, die wir in Listing 16-1 an `thread::spawn` übergeben,
keine Argumente nimmt: Wir verwenden im Code des erzeugten Threads keine Daten
aus dem Haupt-Thread. Um Daten aus dem Haupt-Thread im erzeugten Thread zu
verwenden, muss die Closure des erzeugten Threads die benötigten Werte erfassen.
Listing 16-3 zeigt einen Versuch, im Haupt-Thread einen Vektor zu erzeugen und
ihn im erzeugten Thread zu verwenden. Das funktioniert aber noch nicht, wie du
gleich sehen wirst.

<Listing number="16-3" file-name="src/main.rs" caption="Versuch, einen vom Haupt-Thread erzeugten Vektor in einem anderen Thread zu verwenden">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch16-fearless-concurrency/listing-16-03/src/main.rs}}
```

</Listing>

Die Closure verwendet `v`, erfasst `v` also und macht es zum Teil der Umgebung
der Closure. Da `thread::spawn` diese Closure in einem neuen Thread ausführt,
sollten wir in diesem neuen Thread auf `v` zugreifen können. Wenn wir dieses
Beispiel kompilieren, erhalten wir aber folgenden Fehler:

```console
{{#include ../listings/ch16-fearless-concurrency/listing-16-03/output.txt}}
```

Rust _leitet ab_, wie `v` erfasst wird, und da `println!` nur eine Referenz auf
`v` braucht, versucht die Closure, `v` auszuleihen (_borrow_). Es gibt aber ein
Problem: Rust kann nicht erkennen, wie lange der erzeugte Thread läuft, und weiß
daher nicht, ob die Referenz auf `v` immer gültig sein wird.

Listing 16-4 zeigt ein Szenario, in dem eine Referenz auf `v` mit höherer
Wahrscheinlichkeit ungültig wird.

<Listing number="16-4" file-name="src/main.rs" caption="Ein Thread mit einer Closure, die versucht, eine Referenz auf `v` aus einem Haupt-Thread zu erfassen, der `v` verwirft">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch16-fearless-concurrency/listing-16-04/src/main.rs}}
```

</Listing>

Würde Rust uns diesen Code ausführen lassen, könnte der erzeugte Thread sofort
in den Hintergrund geschoben werden, ohne überhaupt zu laufen. Der erzeugte
Thread enthält eine Referenz auf `v`, aber der Haupt-Thread verwirft (_drops_)
`v` sofort mit der Funktion `drop`, die wir in Kapitel 15 besprochen haben. Wenn
der erzeugte Thread dann mit der Ausführung beginnt, ist `v` nicht mehr gültig,
also ist auch eine Referenz darauf ungültig. Oh nein!

Um den Compilerfehler in Listing 16-3 zu beheben, können wir dem Rat der
Fehlermeldung folgen:

<!-- manual-regeneration
after automatic regeneration, look at listings/ch16-fearless-concurrency/listing-16-03/output.txt and copy the relevant part
-->

```text
help: to force the closure to take ownership of `v` (and any other referenced variables), use the `move` keyword
  |
6 |     let handle = thread::spawn(move || {
  |                                ++++
```

Indem wir vor die Closure das Schlüsselwort `move` setzen, zwingen wir die
Closure, die Ownership der Werte zu übernehmen, die sie verwendet, statt Rust
ableiten zu lassen, dass sie die Werte ausleihen soll. Die in Listing 16-5
gezeigte Änderung von Listing 16-3 kompiliert und läuft wie beabsichtigt.

<Listing number="16-5" file-name="src/main.rs" caption="Mit dem Schlüsselwort `move` erzwingen, dass eine Closure die Ownership der Werte übernimmt, die sie verwendet">

```rust
{{#rustdoc_include ../listings/ch16-fearless-concurrency/listing-16-05/src/main.rs}}
```

</Listing>

Vielleicht sind wir versucht, dasselbe zu tun, um den Code in Listing 16-4, in
dem der Haupt-Thread `drop` aufgerufen hat, mit einer `move`-Closure zu
korrigieren. Diese Korrektur funktioniert aber nicht, weil das, was Listing 16-4
versucht, aus einem anderen Grund verboten ist. Würden wir der Closure `move`
hinzufügen, würden wir `v` in die Umgebung der Closure verschieben (_move_) und
könnten im Haupt-Thread nicht mehr `drop` darauf aufrufen. Stattdessen bekämen
wir diesen Compilerfehler:

```console
{{#include ../listings/ch16-fearless-concurrency/output-only-01-move-drop/output.txt}}
```

Die Ownership-Regeln von Rust haben uns wieder gerettet! Wir haben vom Code in
Listing 16-3 einen Fehler bekommen, weil Rust konservativ war und `v` für den
Thread nur ausgeliehen hat, was bedeutete, dass der Haupt-Thread die Referenz
des erzeugten Threads theoretisch ungültig machen konnte. Indem wir Rust
anweisen, die Ownership von `v` in den erzeugten Thread zu verschieben,
garantieren wir Rust, dass der Haupt-Thread `v` nicht mehr verwenden wird.
Ändern wir Listing 16-4 auf dieselbe Weise, verletzen wir die Ownership-Regeln,
wenn wir versuchen, `v` im Haupt-Thread zu verwenden. Das Schlüsselwort `move`
überschreibt den konservativen Standard von Rust, auszuleihen; es lässt uns die
Ownership-Regeln nicht verletzen.

Nachdem wir behandelt haben, was Threads sind und welche Methoden die Thread-API
bereitstellt, sehen wir uns einige Situationen an, in denen wir Threads
verwenden können.

{{#quiz ../quizzes/ch16-01-threads.toml}}

[capture]: ch13-01-closures.html#capturing-references-or-moving-ownership
