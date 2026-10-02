## Datentypen {#data-types}

Jeder Wert in Rust hat einen bestimmten _Datentyp_, der Rust mitteilt, welche Art von Daten angegeben ist, damit es weiß, wie es mit diesen Daten umgehen soll. Wir betrachten zwei Gruppen von Datentypen: skalare und zusammengesetzte.

Denk daran, dass Rust eine _statisch typisierte_ Sprache ist: Es muss die Typen aller Variablen zur Kompilierzeit kennen. Der Compiler kann in der Regel anhand des Werts und seiner Verwendung ableiten, welchen Typ wir verwenden wollen. Wenn viele Typen möglich sind, etwa als wir im Abschnitt [„Den Tipp mit der Geheimzahl vergleichen“][comparing-the-guess-to-the-secret-number]<!-- ignore --> in Kapitel 2 einen `String` mit `parse` in einen numerischen Typ umgewandelt haben, müssen wir eine Typannotation hinzufügen, etwa so:

```rust
let guess: u32 = "42".parse().expect("Not a number!");
```

Fügen wir die Typannotation `: u32` aus dem vorherigen Code nicht hinzu, zeigt Rust den folgenden Fehler an. Er bedeutet, dass der Compiler mehr Informationen von uns braucht, um zu wissen, welchen Typ wir verwenden wollen:

```console
{{#include ../listings/ch03-common-programming-concepts/output-only-01-no-type-annotations/output.txt}}
```

Für andere Datentypen wirst du andere Typannotationen sehen.

### Skalare Typen {#scalar-types}

Ein _skalarer_ Typ stellt einen einzelnen Wert dar. Rust hat vier primäre skalare Typen: Ganzzahlen, Gleitkommazahlen, boolesche Werte und Zeichen. Vielleicht kennst du sie aus anderen Programmiersprachen. Sehen wir uns an, wie sie in Rust funktionieren.

#### Ganzzahltypen {#integer-types}

Eine _Ganzzahl_ ist eine Zahl ohne Nachkommaanteil. In Kapitel 2 haben wir einen Ganzzahltyp verwendet, den Typ `u32`. Diese Typdeklaration gibt an, dass der zugehörige Wert eine vorzeichenlose Ganzzahl sein soll (vorzeichenbehaftete Ganzzahltypen beginnen mit `i` statt mit `u`), die 32 Bit Platz belegt. Tabelle 3-1 zeigt die eingebauten Ganzzahltypen in Rust. Mit jeder dieser Varianten können wir den Typ eines Ganzzahlwerts deklarieren.

<span class="caption">Tabelle 3-1: Ganzzahltypen in Rust</span>

| Länge               | Vorzeichenbehaftet | Vorzeichenlos |
| ------------------- | ------------------ | ------------- |
| 8 Bit               | `i8`               | `u8`          |
| 16 Bit              | `i16`              | `u16`         |
| 32 Bit              | `i32`              | `u32`         |
| 64 Bit              | `i64`              | `u64`         |
| 128 Bit             | `i128`             | `u128`        |
| Architekturabhängig | `isize`            | `usize`       |

Jede Variante kann vorzeichenbehaftet oder vorzeichenlos sein und hat eine explizite Größe. _Vorzeichenbehaftet_ (_signed_) und _vorzeichenlos_ (_unsigned_) beziehen sich darauf, ob die Zahl negativ sein kann – mit anderen Worten, ob die Zahl ein Vorzeichen braucht (vorzeichenbehaftet) oder ob sie immer nur positiv ist und daher ohne Vorzeichen dargestellt werden kann (vorzeichenlos). Das ist wie beim Schreiben von Zahlen auf Papier: Wenn das Vorzeichen eine Rolle spielt, wird eine Zahl mit Plus- oder Minuszeichen geschrieben; wenn man aber sicher annehmen kann, dass die Zahl positiv ist, wird sie ohne Vorzeichen geschrieben. Vorzeichenbehaftete Zahlen werden in der [Zweierkomplement][twos-complement]<!-- ignore -->-Darstellung gespeichert.

Jede vorzeichenbehaftete Variante kann Zahlen von −(2<sup>n − 1</sup>) bis einschließlich 2<sup>n −
1</sup> − 1 speichern, wobei _n_ die Anzahl der Bits ist, die diese Variante verwendet. Ein `i8` kann also Zahlen von −(2<sup>7</sup>) bis 2<sup>7</sup> − 1 speichern, also von −128 bis 127. Vorzeichenlose Varianten können Zahlen von 0 bis 2<sup>n</sup> − 1 speichern, ein `u8` also Zahlen von 0 bis 2<sup>8</sup> − 1, das heißt von 0 bis 255.

Außerdem hängen die Typen `isize` und `usize` von der Architektur des Computers ab, auf dem dein Programm läuft: 64 Bit auf einer 64-Bit-Architektur und 32 Bit auf einer 32-Bit-Architektur.

Du kannst Ganzzahlliterale in jeder der in Tabelle 3-2 gezeigten Formen schreiben. Beachte, dass Zahlenliterale, die mehrere numerische Typen haben können, ein Typsuffix wie `57u8` erlauben, um den Typ festzulegen. Zahlenliterale können außerdem `_` als visuelles Trennzeichen verwenden, um die Zahl leichter lesbar zu machen, etwa `1_000`; das hat denselben Wert, als hättest du `1000` angegeben.

<span class="caption">Tabelle 3-2: Ganzzahlliterale in Rust</span>

| Zahlenliteral   | Beispiel      |
| --------------- | ------------- |
| Dezimal         | `98_222`      |
| Hexadezimal     | `0xff`        |
| Oktal           | `0o77`        |
| Binär           | `0b1111_0000` |
| Byte (nur `u8`) | `b'A'`        |

Woher weißt du also, welchen Ganzzahltyp du verwenden sollst? Wenn du unsicher bist, sind die Standardwerte von Rust in der Regel ein guter Ausgangspunkt: Ganzzahltypen sind standardmäßig `i32`. Hauptsächlich verwendest du `isize` oder `usize`, wenn du irgendeine Art von Collection indizierst.

> ##### Ganzzahlüberlauf {#integer-overflow}
>
> Angenommen, du hast eine Variable vom Typ `u8`, die Werte zwischen 0 und 255 aufnehmen kann. Wenn du versuchst, die Variable auf einen Wert außerhalb dieses Bereichs zu ändern, etwa 256, kommt es zu einem _Ganzzahlüberlauf_ (_integer overflow_), was zu einem von zwei Verhaltensweisen führen kann. Wenn du im Debug-Modus kompilierst, baut Rust Prüfungen auf Ganzzahlüberlauf ein, die dein Programm zur Laufzeit einen _Panic_ auslösen lassen, wenn dieses Verhalten auftritt. Rust verwendet den Begriff _Panic_ (_panicking_), wenn ein Programm mit einem Fehler beendet wird; wir besprechen Panics ausführlicher im Abschnitt [„Nicht behebbare Fehler mit `panic!`“][unrecoverable-errors-with-panic]<!-- ignore --> in Kapitel 9.
>
> Wenn du im Release-Modus mit dem Flag `--release` kompilierst, baut Rust _keine_ Prüfungen auf Ganzzahlüberlauf ein, die Panics auslösen. Stattdessen führt Rust bei einem Überlauf einen _Zweierkomplement-Umbruch_ (_two’s complement wrapping_) durch. Kurz gesagt: Werte, die größer als der Maximalwert des Typs sind, „laufen über“ und beginnen wieder beim Minimalwert des Typs. Bei einem `u8` wird der Wert 256 zu 0, der Wert 257 zu 1 und so weiter. Das Programm löst keinen Panic aus, aber die Variable hat einen Wert, den du vermutlich nicht erwartet hast. Sich auf das Umbruchverhalten beim Ganzzahlüberlauf zu verlassen, gilt als Fehler.
>
> Um die Möglichkeit eines Überlaufs explizit zu behandeln, kannst du diese Methodenfamilien verwenden, die die Standardbibliothek für primitive numerische Typen bereitstellt:
>
> - Mit den Methoden `wrapping_*`, etwa `wrapping_add`, in allen Modi umbrechen.
> - Mit den Methoden `checked_*` bei einem Überlauf den Wert `None` zurückgeben.
> - Mit den Methoden `overflowing_*` den Wert und einen booleschen Wert zurückgeben, der angibt, ob ein Überlauf stattgefunden hat.
> - Mit den Methoden `saturating_*` beim Minimal- oder Maximalwert des Werts sättigen.

#### Gleitkommatypen {#floating-point-types}

Rust hat außerdem zwei primitive Typen für _Gleitkommazahlen_, also Zahlen mit Nachkommastellen. Die Gleitkommatypen von Rust sind `f32` und `f64`, die 32 bzw. 64 Bit groß sind. Der Standardtyp ist `f64`, weil er auf modernen CPUs ungefähr so schnell ist wie `f32`, aber eine höhere Genauigkeit bietet. Alle Gleitkommatypen sind vorzeichenbehaftet.

Hier ist ein Beispiel, das Gleitkommazahlen in Aktion zeigt:

<span class="filename">Dateiname: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-06-floating-point/src/main.rs}}
```

Gleitkommazahlen werden gemäß dem Standard IEEE-754 dargestellt.

#### Numerische Operationen {#numeric-operations}

Rust unterstützt für alle Zahlentypen die grundlegenden mathematischen Operationen, die du erwarten würdest: Addition, Subtraktion, Multiplikation, Division und Rest. Die Ganzzahldivision schneidet in Richtung null auf die nächste Ganzzahl ab. Der folgende Code zeigt, wie du jede numerische Operation in einer `let`-Anweisung verwenden würdest:

<span class="filename">Dateiname: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-07-numeric-operations/src/main.rs}}
```

Jeder Ausdruck in diesen Anweisungen verwendet einen mathematischen Operator und wird zu einem einzelnen Wert ausgewertet, der dann an eine Variable gebunden wird. [Anhang B][appendix_b]<!-- ignore --> enthält eine Liste aller Operatoren, die Rust bereitstellt.

#### Der boolesche Typ {#the-boolean-type}

Wie in den meisten anderen Programmiersprachen hat ein boolescher Typ in Rust zwei mögliche Werte: `true` und `false`. Boolesche Werte sind ein Byte groß. Der boolesche Typ wird in Rust mit `bool` angegeben. Zum Beispiel:

<span class="filename">Dateiname: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-08-boolean/src/main.rs}}
```

Hauptsächlich werden boolesche Werte in Bedingungen verwendet, etwa in einem `if`-Ausdruck. Wie `if`-Ausdrücke in Rust funktionieren, behandeln wir im Abschnitt [„Kontrollfluss“][control-flow]<!-- ignore -->.

#### Der Zeichentyp {#the-character-type}

Der Typ `char` ist der grundlegendste alphabetische Typ der Sprache. Hier sind einige Beispiele für die Deklaration von `char`-Werten:

<span class="filename">Dateiname: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-09-char/src/main.rs}}
```

Beachte, dass wir `char`-Literale mit einfachen Anführungszeichen angeben, im Gegensatz zu String-Literalen, die doppelte Anführungszeichen verwenden. Der Typ `char` von Rust ist 4 Byte groß und stellt einen Unicode-Skalarwert dar, kann also weit mehr als nur ASCII darstellen. Buchstaben mit Akzent, chinesische, japanische und koreanische Schriftzeichen, Emojis und Leerzeichen ohne Breite sind in Rust alles gültige `char`-Werte. Unicode-Skalarwerte reichen von `U+0000` bis `U+D7FF` und von `U+E000` bis einschließlich `U+10FFFF`. Ein „Zeichen“ ist in Unicode allerdings eigentlich kein Konzept, daher stimmt deine menschliche Vorstellung davon, was ein „Zeichen“ ist, möglicherweise nicht mit dem überein, was ein `char` in Rust ist. Wir besprechen dieses Thema ausführlich in [„UTF-8-kodierten Text mit Strings speichern“][strings]<!-- ignore --> in Kapitel 8.

{{#quiz ../quizzes/ch03-02-data-types-sec1-scalar.toml}}

### Zusammengesetzte Typen {#compound-types}

_Zusammengesetzte Typen_ können mehrere Werte zu einem Typ gruppieren. Rust hat zwei primitive zusammengesetzte Typen: Tupel und Arrays.

#### Der Tupeltyp {#the-tuple-type}

Ein _Tupel_ ist eine allgemeine Möglichkeit, mehrere Werte mit unterschiedlichen Typen zu einem zusammengesetzten Typ zu gruppieren. Tupel haben eine feste Länge: Einmal deklariert, können sie weder wachsen noch schrumpfen.

Wir erzeugen ein Tupel, indem wir eine kommagetrennte Liste von Werten in runde Klammern schreiben. Jede Position im Tupel hat einen Typ, und die Typen der verschiedenen Werte im Tupel müssen nicht gleich sein. In diesem Beispiel haben wir optionale Typannotationen hinzugefügt:

<span class="filename">Dateiname: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-10-tuples/src/main.rs}}
```

Die Variable `tup` wird an das gesamte Tupel gebunden, weil ein Tupel als ein einzelnes zusammengesetztes Element gilt. Um die einzelnen Werte aus einem Tupel herauszuholen, können wir Pattern-Matching verwenden, um einen Tupelwert zu destrukturieren, etwa so:

<span class="filename">Dateiname: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-11-destructuring-tuples/src/main.rs}}
```

Dieses Programm erzeugt zuerst ein Tupel und bindet es an die Variable `tup`. Dann verwendet es ein Pattern mit `let`, um `tup` in drei separate Variablen `x`, `y` und `z` aufzuteilen. Das nennt man _Destrukturierung_ (_destructuring_), weil das einzelne Tupel in drei Teile zerlegt wird. Schließlich gibt das Programm den Wert von `y` aus, also `6.4`.

Wir können auch direkt auf ein Tupelelement zugreifen, indem wir einen Punkt (`.`) gefolgt vom Index des gewünschten Werts verwenden. Zum Beispiel:

<span class="filename">Dateiname: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-12-tuple-indexing/src/main.rs}}
```

Dieses Programm erzeugt das Tupel `x` und greift dann über die jeweiligen Indizes auf jedes Element des Tupels zu. Wie in den meisten Programmiersprachen ist der erste Index in einem Tupel 0.

Das Tupel ohne Werte hat einen besonderen Namen: _Unit_. Dieser Wert und sein zugehöriger Typ werden beide als `()` geschrieben und stellen einen leeren Wert oder einen leeren Rückgabetyp dar. Ausdrücke geben implizit den Unit-Wert zurück, wenn sie keinen anderen Wert zurückgeben.

Außerdem können wir einzelne Elemente eines veränderlichen (_mutable_) Tupels ändern. Zum Beispiel:

<span class="filename">Dateiname: src/main.rs</span>

```rust
fn main() {
    let mut x: (i32, i32) = (1, 2);
    x.0 = 0;
    x.1 += 5;
}
```

Dieses Programm setzt das erste Element auf null und addiert fünf zum zweiten Element. Der endgültige Wert von `x` ist `(0, 7)`.

#### Der Array-Typ {#the-array-type}

Eine weitere Möglichkeit, eine Sammlung mehrerer Werte zu haben, ist ein _Array_. Anders als bei einem Tupel muss jedes Element eines Arrays denselben Typ haben. Anders als Arrays in manchen anderen Sprachen haben Arrays in Rust eine feste Länge.

Wir schreiben die Werte eines Arrays als kommagetrennte Liste in eckige Klammern:

<span class="filename">Dateiname: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-13-arrays/src/main.rs}}
```

Arrays sind nützlich, wenn deine Daten auf dem Stack alloziert werden sollen, wie bei den anderen Typen, die wir bisher gesehen haben, statt auf dem Heap (mehr zu Stack und Heap in [Kapitel 4][stack-and-heap]<!-- ignore -->), oder wenn du sicherstellen willst, dass du immer eine feste Anzahl von Elementen hast. Ein Array ist allerdings nicht so flexibel wie der Vektortyp. Ein Vektor ist ein ähnlicher Collection-Typ aus der Standardbibliothek, der wachsen und schrumpfen _darf_, weil sein Inhalt auf dem Heap liegt. Wenn du unsicher bist, ob du ein Array oder einen Vektor verwenden sollst, solltest du wahrscheinlich einen Vektor verwenden. [Kapitel 8][vectors]<!-- ignore --> behandelt Vektoren ausführlicher.

Arrays sind aber nützlicher, wenn du weißt, dass sich die Anzahl der Elemente nicht ändern muss. Wenn du zum Beispiel in einem Programm die Namen der Monate verwendest, würdest du wahrscheinlich eher ein Array als einen Vektor nehmen, weil du weißt, dass es immer 12 Elemente enthalten wird:

```rust
let months = ["January", "February", "March", "April", "May", "June", "July",
              "August", "September", "October", "November", "December"];
```

Den Typ eines Arrays schreibst du mit eckigen Klammern, die den Typ jedes Elements, ein Semikolon und dann die Anzahl der Elemente im Array enthalten, etwa so:

```rust
let a: [i32; 5] = [1, 2, 3, 4, 5];
```

Hier ist `i32` der Typ jedes Elements. Nach dem Semikolon gibt die Zahl `5` an, dass das Array fünf Elemente enthält.

Du kannst ein Array auch so initialisieren, dass jedes Element denselben Wert enthält, indem du den Anfangswert angibst, gefolgt von einem Semikolon und dann der Länge des Arrays in eckigen Klammern, wie hier gezeigt:

```rust
let a = [3; 5];
```

Das Array namens `a` enthält `5` Elemente, die alle anfänglich auf den Wert `3` gesetzt sind. Das ist dasselbe wie `let a = [3, 3, 3, 3, 3];`, nur kürzer.

<!-- Old headings. Do not remove or links may break. -->

<a id="accessing-array-elements"></a>

#### Auf Array-Elemente zugreifen {#array-element-access}

Ein Array ist ein einzelner Speicherblock bekannter, fester Größe, der auf dem Stack alloziert werden kann. Du kannst über Indizierung auf die Elemente eines Arrays zugreifen, etwa so:

<span class="filename">Dateiname: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-14-array-indexing/src/main.rs}}
```

In diesem Beispiel erhält die Variable namens `first` den Wert `1`, weil das der Wert am Index `[0]` im Array ist. Die Variable namens `second` erhält den Wert `2` vom Index `[1]` im Array.

#### Ungültiger Zugriff auf Array-Elemente {#invalid-array-element-access}

Sehen wir uns an, was passiert, wenn du versuchst, auf ein Element jenseits des Endes eines Arrays zuzugreifen. Angenommen, du führst diesen Code aus, der wie das Ratespiel in Kapitel 2 einen Array-Index vom Benutzer einliest:

<span class="filename">Dateiname: src/main.rs</span>

```rust,ignore,panics
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-15-invalid-array-access/src/main.rs}}
```

Dieser Code lässt sich erfolgreich kompilieren. Wenn du ihn mit `cargo run` ausführst und `0`, `1`, `2`, `3` oder `4` eingibst, gibt das Programm den entsprechenden Wert an diesem Index im Array aus. Gibst du stattdessen eine Zahl jenseits des Array-Endes ein, etwa `10`, siehst du eine Ausgabe wie diese:

<!-- manual-regeneration
cd listings/ch03-common-programming-concepts/no-listing-15-invalid-array-access
cargo run
10
-->

```console
thread 'main' panicked at src/main.rs:19:19:
index out of bounds: the len is 5 but the index is 10
note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace
```

Das Programm führte an der Stelle, an der ein ungültiger Wert in der Indizierungsoperation verwendet wurde, zu einem Laufzeitfehler. Das Programm wurde mit einer Fehlermeldung beendet und hat die abschließende `println!`-Anweisung nicht ausgeführt. Wenn du versuchst, per Indizierung auf ein Element zuzugreifen, prüft Rust, ob der angegebene Index kleiner als die Länge des Arrays ist. Ist der Index größer oder gleich der Länge, löst Rust einen Panic aus. Diese Prüfung muss zur Laufzeit stattfinden, besonders in diesem Fall, denn der Compiler kann unmöglich wissen, welchen Wert ein Benutzer eingeben wird, wenn er den Code später ausführt.

Das ist ein Beispiel für die Prinzipien der Speichersicherheit von Rust in Aktion. In vielen Low-Level-Sprachen findet eine solche Prüfung nicht statt, und wenn du einen falschen Index angibst, kann auf ungültigen Speicher zugegriffen werden. Rust schützt dich vor dieser Art von Fehler, indem es sofort beendet wird, statt den Speicherzugriff zuzulassen und weiterzulaufen. Kapitel 9 behandelt die Fehlerbehandlung von Rust genauer und zeigt, wie du lesbaren, sicheren Code schreibst, der weder einen Panic auslöst noch ungültige Speicherzugriffe zulässt.

{{#quiz ../quizzes/ch03-02-data-types-sec2-compound.toml}}

[comparing-the-guess-to-the-secret-number]: ch02-00-guessing-game-tutorial.html#comparing-the-guess-to-the-secret-number
[twos-complement]: https://en.wikipedia.org/wiki/Two%27s_complement
[control-flow]: ch03-05-control-flow.html#control-flow
[strings]: ch08-02-strings.html#storing-utf-8-encoded-text-with-strings
[stack-and-heap]: ch04-01-what-is-ownership.html
[vectors]: ch08-01-vectors.html
[unrecoverable-errors-with-panic]: ch09-01-unrecoverable-errors-with-panic.html
[wrapping]: https://doc.rust-lang.org/std/num/struct.Wrapping.html
[appendix_b]: appendix-02-operators.md
