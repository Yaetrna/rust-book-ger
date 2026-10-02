## Ein Beispielprogramm mit Structs {#an-example-program-using-structs}

Um zu verstehen, wann wir Structs verwenden möchten, schreiben wir ein Programm,
das den Flächeninhalt eines Rechtecks berechnet. Wir beginnen mit einzelnen
Variablen und refaktorisieren das Programm dann, bis wir stattdessen Structs
verwenden.

Legen wir mit Cargo ein neues Binary-Projekt namens _rectangles_ an, das die
Breite und Höhe eines Rechtecks in Pixeln entgegennimmt und den Flächeninhalt
des Rechtecks berechnet. Listing 5-8 zeigt ein kurzes Programm, das genau das in
der Datei _src/main.rs_ unseres Projekts auf eine Weise erledigt.

<Listing number="5-8" file-name="src/main.rs" caption="Den Flächeninhalt eines Rechtecks berechnen, dessen Breite und Höhe in getrennten Variablen angegeben sind">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-08/src/main.rs:all}}
```

</Listing>

Führe dieses Programm nun mit `cargo run` aus:

```console
{{#include ../listings/ch05-using-structs-to-structure-related-data/listing-05-08/output.txt}}
```

Dieser Code berechnet den Flächeninhalt des Rechtecks erfolgreich, indem er die
Funktion `area` mit beiden Abmessungen aufruft, aber wir können noch mehr tun,
um diesen Code klar und lesbar zu machen.

Das Problem mit diesem Code zeigt sich in der Signatur von `area`:

```rust,ignore
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-08/src/main.rs:here}}
```

Die Funktion `area` soll den Flächeninhalt eines einzigen Rechtecks berechnen,
aber die Funktion, die wir geschrieben haben, hat zwei Parameter, und nirgends
in unserem Programm ist klar, dass die Parameter zusammengehören. Es wäre
lesbarer und leichter zu handhaben, Breite und Höhe zusammenzufassen. Eine
Möglichkeit dafür haben wir bereits im Abschnitt
[„Der Tupeltyp“][the-tuple-type]<!-- ignore --> in Kapitel 3 besprochen: Tupel.

### Mit Tupeln refaktorisieren {#refactoring-with-tuples}

Listing 5-9 zeigt eine weitere Version unseres Programms, die Tupel verwendet.

<Listing number="5-9" file-name="src/main.rs" caption="Breite und Höhe des Rechtecks mit einem Tupel angeben">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-09/src/main.rs}}
```

</Listing>

In einer Hinsicht ist dieses Programm besser. Mit Tupeln können wir etwas
Ordnung hineinbringen, und wir übergeben jetzt nur noch ein Argument. In anderer
Hinsicht ist diese Version aber weniger klar: Tupel benennen ihre Elemente
nicht, also müssen wir auf die Teile des Tupels per Index zugreifen, was unsere
Berechnung weniger offensichtlich macht.

Breite und Höhe zu verwechseln, spielt für die Flächenberechnung keine Rolle,
aber wenn wir das Rechteck auf dem Bildschirm zeichnen wollen, schon! Wir
müssten uns merken, dass `width` der Tupelindex `0` und `height` der Tupelindex
`1` ist. Für andere, die unseren Code verwenden, wäre das noch schwieriger
herauszufinden und im Kopf zu behalten. Weil wir die Bedeutung unserer Daten im
Code nicht ausgedrückt haben, schleichen sich jetzt leichter Fehler ein.

<!-- Old headings. Do not remove or links may break. -->

<a id="refactoring-with-structs-adding-more-meaning"></a>

### Mit Structs refaktorisieren {#refactoring-with-structs}

Wir verwenden Structs, um den Daten durch Beschriftungen Bedeutung zu geben. Wir
können das verwendete Tupel in ein Struct umwandeln, das einen Namen für das
Ganze und Namen für die Teile hat, wie in Listing 5-10 gezeigt.

<Listing number="5-10" file-name="src/main.rs" caption="Ein Struct `Rectangle` definieren">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-10/src/main.rs}}
```

</Listing>

Hier haben wir ein Struct definiert und `Rectangle` genannt. Innerhalb der
geschweiften Klammern haben wir die Felder `width` und `height` definiert, die
beide den Typ `u32` haben. Dann haben wir in `main` eine bestimmte Instanz von
`Rectangle` erzeugt, die eine Breite von `30` und eine Höhe von `50` hat.

Unsere Funktion `area` ist jetzt mit einem einzigen Parameter definiert, den wir
`rectangle` genannt haben und dessen Typ ein unveränderlicher (_immutable_)
Borrow einer Instanz des Structs `Rectangle` ist. Wie in Kapitel 4 erwähnt,
wollen wir das Struct ausleihen (_borrow_), statt seine Ownership zu übernehmen.
So behält `main` seine Ownership und kann `rect1` weiterverwenden; deshalb
verwenden wir das `&` in der Funktionssignatur und beim Aufruf der Funktion.

Die Funktion `area` greift auf die Felder `width` und `height` der
`Rectangle`-Instanz zu (beachte, dass der Zugriff auf Felder einer ausgeliehenen
Struct-Instanz die Feldwerte nicht verschiebt (_move_); deshalb sieht man oft
Borrows von Structs). Unsere Funktionssignatur für `area` sagt jetzt genau, was
wir meinen: Berechne den Flächeninhalt von `Rectangle` mithilfe seiner Felder
`width` und `height`. Das drückt aus, dass Breite und Höhe zusammengehören, und
gibt den Werten aussagekräftige Namen, statt die Tupelindizes `0` und `1` zu
verwenden. Ein Gewinn an Klarheit.

<!-- Old headings. Do not remove or links may break. -->

<a id="adding-useful-functionality-with-derived-traits"></a>

### Funktionalität mit abgeleiteten Traits hinzufügen {#adding-functionality-with-derived-traits}

Es wäre nützlich, eine Instanz von `Rectangle` beim Debuggen unseres Programms
ausgeben und die Werte aller ihrer Felder sehen zu können. Listing 5-11
versucht, das [Makro `println!`][println]<!-- ignore --> zu verwenden, wie wir
es in den vorherigen Kapiteln getan haben. Das funktioniert jedoch nicht.

<Listing number="5-11" file-name="src/main.rs" caption="Versuch, eine `Rectangle`-Instanz auszugeben">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-11/src/main.rs}}
```

</Listing>

Wenn wir diesen Code kompilieren, bekommen wir einen Fehler mit dieser
Kernaussage:

```text
{{#include ../listings/ch05-using-structs-to-structure-related-data/listing-05-11/output.txt:3}}
```

Das Makro `println!` beherrscht viele Arten der Formatierung, und standardmäßig
weisen die geschweiften Klammern `println!` an, die Formatierung `Display` zu
verwenden: eine Ausgabe, die direkt für Endnutzerinnen und Endnutzer gedacht
ist. Die primitiven Typen, die wir bisher gesehen haben, implementieren
`Display` standardmäßig, weil es nur eine Art gibt, wie man einem Benutzer eine
`1` oder einen anderen primitiven Typ zeigen möchte. Bei Structs ist dagegen
weniger klar, wie `println!` die Ausgabe formatieren soll, weil es mehr
Darstellungsmöglichkeiten gibt: Willst du Kommas oder nicht? Willst du die
geschweiften Klammern ausgeben? Sollen alle Felder angezeigt werden? Wegen
dieser Mehrdeutigkeit versucht Rust nicht zu erraten, was wir wollen, und
Structs haben keine vorgegebene Implementierung von `Display`, die mit
`println!` und dem Platzhalter `{}` verwendet werden könnte.

Wenn wir die Fehlermeldungen weiterlesen, finden wir diesen hilfreichen Hinweis:

```text
{{#include ../listings/ch05-using-structs-to-structure-related-data/listing-05-11/output.txt:9:10}}
```

Probieren wir es aus! Der Aufruf des Makros `println!` sieht jetzt so aus:
`println!("rect1 is
{rect1:?}");`. Mit der Angabe `:?` innerhalb der geschweiften
Klammern teilen wir `println!` mit, dass wir ein Ausgabeformat namens `Debug`
verwenden wollen. Der Trait `Debug` ermöglicht es uns, unser Struct auf eine
Weise auszugeben, die für Entwicklerinnen und Entwickler nützlich ist, sodass
wir seinen Wert beim Debuggen unseres Codes sehen können.

Kompiliere den Code mit dieser Änderung. Mist! Wir bekommen immer noch einen
Fehler:

```text
{{#include ../listings/ch05-using-structs-to-structure-related-data/output-only-01-debug/output.txt:3}}
```

Aber auch hier gibt uns der Compiler einen hilfreichen Hinweis:

```text
{{#include ../listings/ch05-using-structs-to-structure-related-data/output-only-01-debug/output.txt:9:10}}
```

Rust _bringt_ Funktionalität zum Ausgeben von Debug-Informationen mit, aber wir
müssen uns explizit dafür entscheiden, diese Funktionalität für unser Struct
verfügbar zu machen. Dazu fügen wir direkt vor der Struct-Definition das äußere
Attribut `#[derive(Debug)]` hinzu, wie in Listing 5-12 gezeigt.

<Listing number="5-12" file-name="src/main.rs" caption="Das Attribut zum Ableiten des Traits `Debug` hinzufügen und die `Rectangle`-Instanz mit der Debug-Formatierung ausgeben">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-12/src/main.rs}}
```

</Listing>

Wenn wir das Programm jetzt ausführen, bekommen wir keine Fehler mehr und sehen
folgende Ausgabe:

```console
{{#include ../listings/ch05-using-structs-to-structure-related-data/listing-05-12/output.txt}}
```

Schön! Es ist nicht die hübscheste Ausgabe, aber sie zeigt die Werte aller
Felder dieser Instanz, was beim Debuggen definitiv hilft. Bei größeren Structs
ist eine etwas leichter lesbare Ausgabe nützlich; in solchen Fällen können wir
im `println!`-String `{:#?}` statt `{:?}` verwenden. In diesem Beispiel erzeugt
der Stil `{:#?}` folgende Ausgabe:

```console
{{#include ../listings/ch05-using-structs-to-structure-related-data/output-only-02-pretty-debug/output.txt}}
```

Eine weitere Möglichkeit, einen Wert im Format `Debug` auszugeben, ist das
[Makro `dbg!`][dbg]<!-- ignore -->. Es übernimmt die Ownership eines Ausdrucks
(im Gegensatz zu `println!`, das eine Referenz nimmt), gibt Datei und
Zeilennummer der Stelle aus, an der der Aufruf von `dbg!` in deinem Code steht,
zusammen mit dem Ergebniswert dieses Ausdrucks, und gibt die Ownership des Werts
zurück.

> Note: Der Aufruf des Makros `dbg!` schreibt in den Standardfehlerstrom der
> Konsole (`stderr`), im Gegensatz zu `println!`, das in den
> Standardausgabestrom der Konsole (`stdout`) schreibt. Mehr über `stderr` und
> `stdout` erfährst du im
> [Abschnitt „Fehler auf die Standardfehlerausgabe umleiten“ in Kapitel 12][err]<!-- ignore -->.

Hier ist ein Beispiel, in dem uns der Wert interessiert, der dem Feld `width`
zugewiesen wird, sowie der Wert des gesamten Structs in `rect1`:

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/no-listing-05-dbg-macro/src/main.rs}}
```

Wir können `dbg!` um den Ausdruck `30 * scale` setzen, und weil `dbg!` die
Ownership des Werts des Ausdrucks zurückgibt, erhält das Feld `width` denselben
Wert, als stünde der Aufruf von `dbg!` gar nicht da. Wir wollen nicht, dass
`dbg!` die Ownership von `rect1` übernimmt, daher verwenden wir im nächsten
Aufruf eine Referenz auf `rect1`. So sieht die Ausgabe dieses Beispiels aus:

```console
{{#include ../listings/ch05-using-structs-to-structure-related-data/no-listing-05-dbg-macro/output.txt}}
```

Wir sehen, dass der erste Teil der Ausgabe aus Zeile 10 von _src/main.rs_
stammt, wo wir den Ausdruck `30 * scale` debuggen, und dass sein Ergebniswert
`60` ist (die für Ganzzahlen implementierte `Debug`-Formatierung gibt nur ihren
Wert aus). Der Aufruf von `dbg!` in Zeile 14 von _src/main.rs_ gibt den Wert von
`&rect1` aus, also das Struct `Rectangle`. Diese Ausgabe verwendet die hübsche
`Debug`-Formatierung des Typs `Rectangle`. Das Makro `dbg!` kann wirklich
hilfreich sein, wenn du herausfinden willst, was dein Code tut!

Neben dem Trait `Debug` stellt Rust eine Reihe von Traits bereit, die wir mit
dem Attribut `derive` verwenden können und die unseren eigenen Typen nützliches
Verhalten hinzufügen können. Diese Traits und ihr Verhalten sind in
[Anhang C][app-c]<!-- ignore --> aufgeführt. Wie man diese Traits mit eigenem
Verhalten implementiert und wie man eigene Traits erstellt, behandeln wir in
Kapitel 10. Neben `derive` gibt es noch viele weitere Attribute; mehr dazu
findest du im [Abschnitt „Attributes“ der Rust-Referenz][attributes].

Unsere Funktion `area` ist sehr spezifisch: Sie berechnet nur den Flächeninhalt
von Rechtecken. Es wäre hilfreich, dieses Verhalten enger an unser Struct
`Rectangle` zu binden, weil es mit keinem anderen Typ funktioniert. Sehen wir
uns an, wie wir diesen Code weiter refaktorisieren können, indem wir die
Funktion `area` in eine Methode `area` umwandeln, die auf unserem Typ
`Rectangle` definiert ist.

{{#quiz ../quizzes/ch05-02-example-structs.toml}}

[the-tuple-type]: ch03-02-data-types.html#the-tuple-type
[app-c]: appendix-03-derivable-traits.md
[println]: https://doc.rust-lang.org/std/macro.println.html
[dbg]: https://doc.rust-lang.org/std/macro.dbg.html
[err]: ch12-06-writing-to-stderr-instead-of-stdout.html
[attributes]: https://doc.rust-lang.org/reference/attributes.html
