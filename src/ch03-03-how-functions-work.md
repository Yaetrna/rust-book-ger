## Funktionen {#functions}

Funktionen sind in Rust-Code allgegenwärtig. Eine der wichtigsten Funktionen der
Sprache hast du bereits gesehen: die Funktion `main`, den Einstiegspunkt vieler
Programme. Du hast auch schon das Schlüsselwort `fn` gesehen, mit dem du neue
Funktionen deklarierst.

In Rust-Code ist _Snake Case_ der übliche Stil für Funktions- und
Variablennamen: Alle Buchstaben sind klein, und Wörter werden durch Unterstriche
getrennt. Hier ist ein Programm mit einer beispielhaften Funktionsdefinition:

<span class="filename">Dateiname: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-16-functions/src/main.rs}}
```

Wir definieren eine Funktion in Rust, indem wir `fn` schreiben, gefolgt von
einem Funktionsnamen und einem Paar runder Klammern. Die geschweiften Klammern
zeigen dem Compiler, wo der Funktionsrumpf beginnt und endet.

Wir können jede von uns definierte Funktion aufrufen, indem wir ihren Namen
gefolgt von einem Paar runder Klammern schreiben. Weil `another_function` im
Programm definiert ist, kann sie innerhalb der Funktion `main` aufgerufen
werden. Beachte, dass wir `another_function` im Quellcode _nach_ der Funktion
`main` definiert haben; wir hätten sie auch davor definieren können. Rust ist
egal, wo du deine Funktionen definierst; wichtig ist nur, dass sie irgendwo in
einem Gültigkeitsbereich (_scope_) definiert sind, den die aufrufende Stelle
sehen kann.

Lass uns ein neues Binary-Projekt namens _functions_ anlegen, um Funktionen
weiter zu erkunden. Lege das Beispiel mit `another_function` in _src/main.rs_ ab
und führe es aus. Du solltest folgende Ausgabe sehen:

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-16-functions/output.txt}}
```

Die Zeilen werden in der Reihenfolge ausgeführt, in der sie in der Funktion
`main` stehen. Zuerst wird die Nachricht „Hello, world!“ ausgegeben, dann wird
`another_function` aufgerufen und ihre Nachricht ausgegeben.

### Parameter {#parameters}

Wir können Funktionen mit _Parametern_ definieren. Das sind spezielle Variablen,
die Teil der Signatur einer Funktion sind. Wenn eine Funktion Parameter hat,
kannst du ihr konkrete Werte für diese Parameter übergeben. Genau genommen
heißen die konkreten Werte _Argumente_, aber in der Umgangssprache werden die
Wörter _Parameter_ und _Argument_ oft austauschbar verwendet, sowohl für die
Variablen in einer Funktionsdefinition als auch für die konkreten Werte, die
beim Aufruf einer Funktion übergeben werden.

In dieser Version von `another_function` fügen wir einen Parameter hinzu:

<span class="filename">Dateiname: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-17-functions-with-parameters/src/main.rs}}
```

Führe dieses Programm aus; du solltest folgende Ausgabe erhalten:

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-17-functions-with-parameters/output.txt}}
```

Die Deklaration von `another_function` hat einen Parameter namens `x`. Als Typ
von `x` ist `i32` angegeben. Wenn wir `5` an `another_function` übergeben, setzt
das Makro `println!` `5` an die Stelle im Format-String, an der das Paar
geschweifter Klammern mit `x` stand.

In Funktionssignaturen _musst_ du den Typ jedes Parameters deklarieren. Das ist
eine bewusste Entscheidung im Design von Rust: Weil Typannotationen in
Funktionsdefinitionen Pflicht sind, braucht der Compiler sie fast nie an anderer
Stelle im Code, um herauszufinden, welchen Typ du meinst. Außerdem kann der
Compiler hilfreichere Fehlermeldungen ausgeben, wenn er weiß, welche Typen die
Funktion erwartet.

Wenn du mehrere Parameter definierst, trennst du die Parameterdeklarationen mit
Kommas, etwa so:

<span class="filename">Dateiname: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-18-functions-with-multiple-parameters/src/main.rs}}
```

Dieses Beispiel erzeugt eine Funktion namens `print_labeled_measurement` mit
zwei Parametern. Der erste Parameter heißt `value` und ist ein `i32`. Der zweite
heißt `unit_label` und hat den Typ `char`. Die Funktion gibt dann einen Text
aus, der sowohl `value` als auch `unit_label` enthält.

Führen wir diesen Code aus. Ersetze das Programm, das sich gerade in der Datei
_src/main.rs_ deines Projekts _functions_ befindet, durch das vorherige Beispiel
und führe es mit `cargo
run` aus:

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-18-functions-with-multiple-parameters/output.txt}}
```

Weil wir die Funktion mit `5` als Wert für `value` und `'h'` als Wert für
`unit_label` aufgerufen haben, enthält die Programmausgabe diese Werte.

{{#quiz ../quizzes/ch03-03-functions-sec1-parameters.toml}}

### Anweisungen und Ausdrücke {#statements-and-expressions}

Funktionsrümpfe bestehen aus einer Reihe von Anweisungen, die optional mit einem
Ausdruck enden. Die bisher behandelten Funktionen enthielten keinen
abschließenden Ausdruck, aber du hast schon einen Ausdruck als Teil einer
Anweisung gesehen. Weil Rust eine ausdrucksbasierte Sprache ist, ist das ein
wichtiger Unterschied, den man verstehen sollte. Andere Sprachen unterscheiden
nicht auf dieselbe Weise, also sehen wir uns an, was Anweisungen und Ausdrücke
sind und wie sich ihre Unterschiede auf die Rümpfe von Funktionen auswirken.

- _Anweisungen_ (_statements_) sind Befehle, die eine Aktion ausführen und
  keinen Wert zurückgeben.
- _Ausdrücke_ (_expressions_) werden zu einem Ergebniswert ausgewertet.

Sehen wir uns einige Beispiele an. Tatsächlich haben wir Anweisungen und
Ausdrücke bereits verwendet. Eine Variable zu erzeugen und ihr mit dem
Schlüsselwort `let` einen Wert zuzuweisen, ist eine Anweisung. In Listing 3-1
ist `let y = 6;` eine Anweisung.

<Listing number="3-1" file-name="src/main.rs" caption="Eine Deklaration der Funktion `main` mit einer Anweisung">

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/listing-03-01/src/main.rs}}
```

</Listing>

Funktionsdefinitionen sind ebenfalls Anweisungen; das gesamte vorherige Beispiel
ist für sich genommen eine Anweisung. (Wie wir gleich sehen, ist der Aufruf
einer Funktion allerdings keine Anweisung.)

Anweisungen geben keine Werte zurück. Deshalb kannst du eine `let`-Anweisung
nicht einer anderen Variable zuweisen, wie es der folgende Code versucht; du
bekommst einen Fehler:

<span class="filename">Dateiname: src/main.rs</span>

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-19-statements-vs-expressions/src/main.rs}}
```

Wenn du dieses Programm ausführst, sieht der Fehler so aus:

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-19-statements-vs-expressions/output.txt}}
```

Die Anweisung `let y = 6` gibt keinen Wert zurück, also gibt es nichts, woran
`x` gebunden werden könnte. Das unterscheidet sich von anderen Sprachen wie C
und Ruby, in denen die Zuweisung den zugewiesenen Wert zurückgibt. In diesen
Sprachen kannst du `x = y = 6` schreiben, sodass sowohl `x` als auch `y` den
Wert `6` haben; in Rust ist das nicht so.

Ausdrücke werden zu einem Wert ausgewertet und machen den Großteil des
restlichen Codes aus, den du in Rust schreiben wirst. Nimm eine Rechenoperation
wie `5 + 6`: Das ist ein Ausdruck, der zum Wert `11` ausgewertet wird. Ausdrücke
können Teil von Anweisungen sein: In Listing 3-1 ist die `6` in der Anweisung
`let y = 6;` ein Ausdruck, der zum Wert `6` ausgewertet wird. Der Aufruf einer
Funktion ist ein Ausdruck. Der Aufruf eines Makros ist ein Ausdruck. Ein mit
geschweiften Klammern erzeugter neuer Block mit eigenem Gültigkeitsbereich ist
ein Ausdruck, zum Beispiel:

<span class="filename">Dateiname: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-20-blocks-are-expressions/src/main.rs}}
```

Dieser Ausdruck:

```rust,ignore
{
    let x = 3;
    x + 1
}
```

ist ein Block, der in diesem Fall zu `4` ausgewertet wird. Dieser Wert wird als
Teil der `let`-Anweisung an `y` gebunden. Beachte die Zeile `x + 1` ohne
Semikolon am Ende, anders als die meisten Zeilen, die du bisher gesehen hast.
Ausdrücke enden nicht mit einem Semikolon. Wenn du ans Ende eines Ausdrucks ein
Semikolon setzt, machst du ihn zu einer Anweisung, und er gibt dann keinen Wert
zurück. Behalte das im Hinterkopf, wenn du dir als Nächstes Rückgabewerte von
Funktionen und Ausdrücke ansiehst.

### Funktionen mit Rückgabewerten {#functions-with-return-values}

Funktionen können Werte an den Code zurückgeben, der sie aufruft. Wir benennen
Rückgabewerte nicht, aber wir müssen ihren Typ nach einem Pfeil (`->`)
deklarieren. In Rust ist der Rückgabewert der Funktion gleichbedeutend mit dem
Wert des letzten Ausdrucks im Block des Funktionsrumpfs. Du kannst mit dem
Schlüsselwort `return` und der Angabe eines Werts vorzeitig aus einer Funktion
zurückkehren, aber die meisten Funktionen geben den letzten Ausdruck implizit
zurück. Hier ist ein Beispiel für eine Funktion, die einen Wert zurückgibt:

<span class="filename">Dateiname: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-21-function-return-values/src/main.rs}}
```

In der Funktion `five` gibt es keine Funktionsaufrufe, keine Makros und nicht
einmal `let`-Anweisungen – nur die Zahl `5` für sich allein. Das ist in Rust
eine vollkommen gültige Funktion. Beachte, dass auch der Rückgabetyp der
Funktion angegeben ist, als `-> i32`. Führe diesen Code aus; die Ausgabe sollte
so aussehen:

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-21-function-return-values/output.txt}}
```

Die `5` in `five` ist der Rückgabewert der Funktion, weshalb der Rückgabetyp
`i32` ist. Sehen wir uns das genauer an. Zwei Dinge sind wichtig: Erstens zeigt
die Zeile `let x = five();`, dass wir den Rückgabewert einer Funktion verwenden,
um eine Variable zu initialisieren. Weil die Funktion `five` eine `5`
zurückgibt, ist diese Zeile dasselbe wie die folgende:

```rust
let x = 5;
```

Zweitens hat die Funktion `five` keine Parameter und legt den Typ des
Rückgabewerts fest. Der Rumpf der Funktion ist eine einsame `5` ohne Semikolon,
weil sie ein Ausdruck ist, dessen Wert wir zurückgeben wollen.

Sehen wir uns ein weiteres Beispiel an:

<span class="filename">Dateiname: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-22-function-parameter-and-return/src/main.rs}}
```

Dieser Code gibt `The value of x is: 6` aus. Was passiert aber, wenn wir ans
Ende der Zeile mit `x + 1` ein Semikolon setzen und sie damit von einem Ausdruck
in eine Anweisung verwandeln?

<span class="filename">Dateiname: src/main.rs</span>

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-23-statements-dont-return-values/src/main.rs}}
```

Das Kompilieren dieses Codes erzeugt folgenden Fehler:

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-23-statements-dont-return-values/output.txt}}
```

Die Hauptfehlermeldung, `mismatched types` (nicht zusammenpassende Typen), zeigt
das Kernproblem dieses Codes. Laut Definition gibt die Funktion `plus_one` einen
`i32` zurück, aber Anweisungen werden zu keinem Wert ausgewertet, was durch
`()`, den Unit-Typ, ausgedrückt wird. Deshalb wird nichts zurückgegeben, was der
Funktionsdefinition widerspricht und zu einem Fehler führt. In dieser Ausgabe
gibt Rust eine Meldung aus, die helfen kann, das Problem zu beheben: Es schlägt
vor, das Semikolon zu entfernen, was den Fehler beseitigen würde.

{{#quiz ../quizzes/ch03-03-functions-sec2-expressions.toml}}
