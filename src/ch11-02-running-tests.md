## Steuern, wie Tests ausgeführt werden {#controlling-how-tests-are-run}

So wie `cargo run` deinen Code kompiliert und dann die resultierende Binärdatei
ausführt, kompiliert `cargo test` deinen Code im Testmodus und führt die
resultierende Test-Binärdatei aus. Standardmäßig führt die von `cargo test`
erzeugte Binärdatei alle Tests parallel aus und fängt die Ausgabe ab, die
während der Testläufe erzeugt wird. So wird die Ausgabe nicht angezeigt, und die
Ausgabe zu den Testergebnissen lässt sich leichter lesen. Du kannst aber
Kommandozeilenoptionen angeben, um dieses Standardverhalten zu ändern.

Manche Kommandozeilenoptionen gehen an `cargo test`, andere an die resultierende
Test-Binärdatei. Um diese beiden Arten von Argumenten zu trennen, gibst du die
Argumente für `cargo test` an, gefolgt vom Trennzeichen `--` und dann den
Argumenten für die Test-Binärdatei. `cargo test --help` zeigt die Optionen an,
die du mit `cargo test` verwenden kannst, und `cargo test -- --help` zeigt die
Optionen an, die du nach dem Trennzeichen verwenden kannst. Diese Optionen sind
außerdem im [Abschnitt „Tests“ von _The `rustc` Book_][tests] dokumentiert.

[tests]: https://doc.rust-lang.org/rustc/tests/index.html

### Tests parallel oder nacheinander ausführen {#running-tests-in-parallel-or-consecutively}

Wenn du mehrere Tests ausführst, laufen sie standardmäßig parallel in Threads.
Dadurch sind sie schneller fertig, und du bekommst früher Rückmeldung. Da die
Tests gleichzeitig laufen, musst du sicherstellen, dass deine Tests nicht
voneinander oder von gemeinsamem Zustand abhängen, auch nicht von einer
gemeinsamen Umgebung wie dem aktuellen Arbeitsverzeichnis oder
Umgebungsvariablen.

Angenommen, jeder deiner Tests führt Code aus, der auf der Festplatte eine Datei
namens _test-output.txt_ anlegt und Daten in diese Datei schreibt. Dann liest
jeder Test die Daten aus dieser Datei und sichert zu, dass die Datei einen
bestimmten Wert enthält, der in jedem Test ein anderer ist. Da die Tests
gleichzeitig laufen, könnte ein Test die Datei überschreiben, während ein
anderer Test die Datei gerade schreibt und liest. Der zweite Test schlägt dann
fehl, nicht weil der Code falsch ist, sondern weil sich die Tests bei der
parallelen Ausführung gegenseitig gestört haben. Eine Lösung ist,
sicherzustellen, dass jeder Test in eine andere Datei schreibt; eine andere ist,
die Tests nacheinander auszuführen.

Wenn du die Tests nicht parallel ausführen willst oder die Anzahl der
verwendeten Threads genauer steuern möchtest, kannst du der Test-Binärdatei das
Flag `--test-threads` und die gewünschte Anzahl von Threads übergeben. Sieh dir
folgendes Beispiel an:

```console
$ cargo test -- --test-threads=1
```

Wir setzen die Anzahl der Test-Threads auf `1` und weisen das Programm damit an,
keine Parallelität zu verwenden. Die Tests mit einem Thread auszuführen, dauert
länger als die parallele Ausführung, aber die Tests stören sich nicht
gegenseitig, wenn sie Zustand teilen.

### Ausgaben von Funktionen anzeigen {#showing-function-output}

Besteht ein Test, fängt die Testbibliothek von Rust standardmäßig alles ab, was
auf die Standardausgabe geschrieben wird. Rufen wir zum Beispiel in einem Test
`println!` auf und der Test besteht, sehen wir die Ausgabe von `println!` nicht
im Terminal; wir sehen nur die Zeile, die anzeigt, dass der Test bestanden hat.
Schlägt ein Test fehl, sehen wir alles, was auf die Standardausgabe geschrieben
wurde, zusammen mit dem Rest der Fehlermeldung.

Als Beispiel enthält Listing 11-10 eine alberne Funktion, die den Wert ihres
Parameters ausgibt und 10 zurückgibt, sowie einen Test, der besteht, und einen
Test, der fehlschlägt.

<Listing number="11-10" file-name="src/lib.rs" caption="Tests für eine Funktion, die `println!` aufruft">

```rust,panics,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/listing-11-10/src/lib.rs}}
```

</Listing>

Wenn wir diese Tests mit `cargo test` ausführen, sehen wir folgende Ausgabe:

```console
{{#include ../listings/ch11-writing-automated-tests/listing-11-10/output.txt}}
```

Beachte, dass wir in dieser Ausgabe nirgends `I got the value 4` sehen, was
ausgegeben wird, wenn der bestehende Test läuft. Diese Ausgabe wurde abgefangen.
Die Ausgabe des fehlgeschlagenen Tests, `I got the value 8`, erscheint im
Abschnitt der Testzusammenfassung, der auch die Ursache für das Fehlschlagen des
Tests zeigt.

Wollen wir auch die ausgegebenen Werte bestandener Tests sehen, können wir Rust
mit `--show-output` anweisen, auch die Ausgabe erfolgreicher Tests anzuzeigen:

```console
$ cargo test -- --show-output
```

Wenn wir die Tests in Listing 11-10 erneut mit dem Flag `--show-output`
ausführen, sehen wir folgende Ausgabe:

```console
{{#include ../listings/ch11-writing-automated-tests/output-only-01-show-output/output.txt}}
```

### Eine Teilmenge von Tests nach Namen ausführen {#running-a-subset-of-tests-by-name}

Eine vollständige Testsuite auszuführen, kann manchmal lange dauern. Wenn du an
Code in einem bestimmten Bereich arbeitest, willst du vielleicht nur die Tests
ausführen, die diesen Code betreffen. Du kannst auswählen, welche Tests
ausgeführt werden, indem du `cargo test` den Namen oder die Namen der
gewünschten Tests als Argument übergibst.

Um zu zeigen, wie man eine Teilmenge von Tests ausführt, erstellen wir zuerst
drei Tests für unsere Funktion `add_two`, wie in Listing 11-11 gezeigt, und
wählen aus, welche davon ausgeführt werden.

<Listing number="11-11" file-name="src/lib.rs" caption="Drei Tests mit drei verschiedenen Namen">

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/listing-11-11/src/lib.rs}}
```

</Listing>

Führen wir die Tests ohne Argumente aus, laufen, wie wir vorhin gesehen haben,
alle Tests parallel:

```console
{{#include ../listings/ch11-writing-automated-tests/listing-11-11/output.txt}}
```

#### Einzelne Tests ausführen {#running-single-tests}

Wir können `cargo test` den Namen einer beliebigen Testfunktion übergeben, um
nur diesen Test auszuführen:

```console
{{#include ../listings/ch11-writing-automated-tests/output-only-02-single-test/output.txt}}
```

Nur der Test mit dem Namen `one_hundred` wurde ausgeführt; die anderen beiden
Tests passten nicht zu diesem Namen. Die Testausgabe teilt uns mit, dass es
weitere Tests gab, die nicht ausgeführt wurden, indem sie am Ende
`2 filtered out` anzeigt.

Auf diese Weise können wir nicht die Namen mehrerer Tests angeben; nur der erste
Wert, der `cargo test` übergeben wird, wird verwendet. Es gibt aber eine
Möglichkeit, mehrere Tests auszuführen.

#### Filtern, um mehrere Tests auszuführen {#filtering-to-run-multiple-tests}

Wir können einen Teil eines Testnamens angeben, und jeder Test, dessen Name zu
diesem Wert passt, wird ausgeführt. Da zum Beispiel die Namen von zwei unserer
Tests `add` enthalten, können wir diese beiden mit `cargo test add` ausführen:

```console
{{#include ../listings/ch11-writing-automated-tests/output-only-03-multiple-tests/output.txt}}
```

Dieser Befehl hat alle Tests mit `add` im Namen ausgeführt und den Test namens
`one_hundred` herausgefiltert. Beachte außerdem, dass das Modul, in dem ein Test
steht, Teil des Testnamens wird, sodass wir alle Tests in einem Modul ausführen
können, indem wir nach dem Namen des Moduls filtern.

<!-- Old headings. Do not remove or links may break. -->

<a id="ignoring-some-tests-unless-specifically-requested"></a>

### Tests ignorieren, sofern sie nicht ausdrücklich angefordert werden {#ignoring-tests-unless-specifically-requested}

Manchmal kann die Ausführung einiger bestimmter Tests sehr zeitaufwendig sein,
sodass du sie bei den meisten Läufen von `cargo test` ausschließen willst. Statt
alle Tests, die du ausführen willst, als Argumente aufzulisten, kannst du die
zeitaufwendigen Tests stattdessen mit dem Attribut `ignore` annotieren, um sie
auszuschließen, wie hier gezeigt:

<span class="filename">Dateiname: src/lib.rs</span>

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/no-listing-11-ignore-a-test/src/lib.rs:here}}
```

Nach `#[test]` fügen wir dem Test, den wir ausschließen wollen, die Zeile
`#[ignore]` hinzu. Wenn wir unsere Tests jetzt ausführen, läuft `it_works`, aber
`expensive_test` nicht:

```console
{{#include ../listings/ch11-writing-automated-tests/no-listing-11-ignore-a-test/output.txt}}
```

Die Funktion `expensive_test` wird als `ignored` aufgeführt. Wollen wir nur die
ignorierten Tests ausführen, können wir `cargo test -- --ignored` verwenden:

```console
{{#include ../listings/ch11-writing-automated-tests/output-only-04-running-ignored/output.txt}}
```

Indem du steuerst, welche Tests laufen, kannst du sicherstellen, dass deine
Ergebnisse von `cargo test` schnell zurückkommen. Wenn es an der Zeit ist, die
Ergebnisse der `ignored`-Tests zu prüfen, und du Zeit hast, auf die Ergebnisse
zu warten, kannst du stattdessen `cargo test -- --ignored` ausführen. Willst du
alle Tests ausführen, egal ob sie ignoriert werden oder nicht, kannst du
`cargo test -- --include-ignored` ausführen.

{{#quiz ../quizzes/ch11-02-running-tests.toml}}
