## Makros {#macros}

Wir haben im ganzen Buch Makros wie `println!` verwendet, aber noch nicht
vollständig untersucht, was ein Makro ist und wie es funktioniert. Der Begriff
_Makro_ bezeichnet eine Familie von Features in Rust – deklarative Makros mit
`macro_rules!` und drei Arten prozeduraler Makros:

- Benutzerdefinierte `#[derive]`-Makros, die Code festlegen, der mit dem
  Attribut `derive` bei Structs und Enums hinzugefügt wird
- Attributähnliche Makros, die benutzerdefinierte Attribute definieren, die bei
  jedem Element verwendet werden können
- Funktionsähnliche Makros, die wie Funktionsaufrufe aussehen, aber auf den
  Tokens arbeiten, die als ihr Argument angegeben werden

Wir sprechen der Reihe nach über jede dieser Arten, aber sehen wir uns zuerst
an, warum wir überhaupt Makros brauchen, wenn wir doch schon Funktionen haben.

### Der Unterschied zwischen Makros und Funktionen {#the-difference-between-macros-and-functions}

Im Grunde sind Makros eine Möglichkeit, Code zu schreiben, der anderen Code
schreibt, was als _Metaprogrammierung_ bezeichnet wird. In Anhang C besprechen
wir das Attribut `derive`, das für dich eine Implementierung verschiedener
Traits erzeugt. Außerdem haben wir im ganzen Buch die Makros `println!` und
`vec!` verwendet. All diese Makros werden _expandiert_, um mehr Code zu erzeugen
als den Code, den du von Hand geschrieben hast.

Metaprogrammierung ist nützlich, um die Menge an Code zu reduzieren, die du
schreiben und pflegen musst, was auch eine der Aufgaben von Funktionen ist.
Makros haben jedoch einige zusätzliche Fähigkeiten, die Funktionen nicht haben.

Eine Funktionssignatur muss die Anzahl und den Typ der Parameter der Funktion
deklarieren. Makros können dagegen eine variable Anzahl von Parametern nehmen:
Wir können `println!("hello")` mit einem Argument oder
`println!("hello {}", name)` mit zwei Argumenten aufrufen. Außerdem werden
Makros expandiert, bevor der Compiler die Bedeutung des Codes interpretiert,
sodass ein Makro zum Beispiel einen Trait für einen gegebenen Typ implementieren
kann. Eine Funktion kann das nicht, weil sie zur Laufzeit aufgerufen wird und
ein Trait zur Kompilierzeit implementiert werden muss.

Der Nachteil, ein Makro statt einer Funktion zu implementieren, ist, dass
Makrodefinitionen komplexer sind als Funktionsdefinitionen, weil du Rust-Code
schreibst, der Rust-Code schreibt. Wegen dieser Indirektion sind
Makrodefinitionen im Allgemeinen schwerer zu lesen, zu verstehen und zu pflegen
als Funktionsdefinitionen.

Ein weiterer wichtiger Unterschied zwischen Makros und Funktionen ist, dass du
Makros definieren oder in den Gültigkeitsbereich (_scope_) bringen musst,
_bevor_ du sie in einer Datei aufrufst, im Gegensatz zu Funktionen, die du
überall definieren und überall aufrufen kannst.

<!-- Old headings. Do not remove or links may break. -->

<a id="declarative-macros-with-macro_rules-for-general-metaprogramming"></a>

### Deklarative Makros für allgemeine Metaprogrammierung {#declarative-macros-for-general-metaprogramming}

Die am weitesten verbreitete Form von Makros in Rust ist das _deklarative
Makro_. Diese werden manchmal auch als „Makros nach Beispiel“ (_macros by
example_), „`macro_rules!`-Makros“ oder einfach nur „Makros“ bezeichnet. Im Kern
ermöglichen es deklarative Makros, etwas Ähnliches wie einen `match`-Ausdruck in
Rust zu schreiben. Wie in Kapitel 6 besprochen, sind `match`-Ausdrücke
Kontrollstrukturen, die einen Ausdruck nehmen, den resultierenden Wert des
Ausdrucks mit Patterns vergleichen und dann den Code ausführen, der zum
passenden Pattern gehört. Makros vergleichen ebenfalls einen Wert mit Patterns,
denen bestimmter Code zugeordnet ist: In dieser Situation ist der Wert der
literale Rust-Quellcode, der dem Makro übergeben wird; die Patterns werden mit
der Struktur dieses Quellcodes verglichen; und der Code, der zu einem Pattern
gehört, ersetzt bei einer Übereinstimmung den Code, der dem Makro übergeben
wurde. All das geschieht während des Kompilierens.

Um ein Makro zu definieren, verwendest du das Konstrukt `macro_rules!`. Sehen
wir uns an, wie man `macro_rules!` verwendet, indem wir betrachten, wie das
Makro `vec!` definiert ist. In Kapitel 8 haben wir behandelt, wie wir mit dem
Makro `vec!` einen neuen Vektor mit bestimmten Werten erzeugen können. Das
folgende Makro erzeugt zum Beispiel einen neuen Vektor, der drei Ganzzahlen
enthält:

```rust
let v: Vec<u32> = vec![1, 2, 3];
```

Wir könnten das Makro `vec!` auch verwenden, um einen Vektor aus zwei Ganzzahlen
oder einen Vektor aus fünf String-Slices zu erzeugen. Mit einer Funktion könnten
wir das nicht, weil wir die Anzahl oder den Typ der Werte nicht im Voraus kennen
würden.

Listing 20-35 zeigt eine leicht vereinfachte Definition des Makros `vec!`.

<Listing number="20-35" file-name="src/lib.rs" caption="Eine vereinfachte Version der Definition des Makros `vec!`">

```rust,noplayground
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-35/src/lib.rs}}
```

</Listing>

> Note: Die tatsächliche Definition des Makros `vec!` in der Standardbibliothek
> enthält Code, der im Voraus die richtige Menge Speicher alloziert. Dieser Code
> ist eine Optimierung, die wir hier weglassen, um das Beispiel einfacher zu
> halten.

Die Annotation `#[macro_export]` gibt an, dass dieses Makro verfügbar gemacht
werden soll, sobald der Crate, in dem das Makro definiert ist, in den
Gültigkeitsbereich gebracht wird. Ohne diese Annotation kann das Makro nicht in
den Gültigkeitsbereich gebracht werden.

Dann beginnen wir die Makrodefinition mit `macro_rules!` und dem Namen des
Makros, das wir definieren, _ohne_ das Ausrufezeichen. Auf den Namen, in diesem
Fall `vec`, folgen geschweifte Klammern, die den Rumpf der Makrodefinition
umschließen.

Die Struktur im Rumpf von `vec!` ähnelt der Struktur eines `match`-Ausdrucks.
Hier haben wir einen Arm mit dem Pattern `( $( $x:expr ),* )`, gefolgt von `=>`
und dem Codeblock, der zu diesem Pattern gehört. Wenn das Pattern passt, wird
der zugehörige Codeblock ausgegeben. Da dies das einzige Pattern in diesem Makro
ist, gibt es nur eine gültige Art der Übereinstimmung; jedes andere Pattern
führt zu einem Fehler. Komplexere Makros haben mehr als einen Arm.

Die gültige Pattern-Syntax in Makrodefinitionen unterscheidet sich von der in
Kapitel 19 behandelten Pattern-Syntax, weil Makro-Patterns mit der Struktur von
Rust-Code statt mit Werten abgeglichen werden. Gehen wir durch, was die Teile
des Patterns in Listing 20-29 bedeuten; die vollständige Syntax für
Makro-Patterns findest du in der [Rust-Referenz][ref].

Zuerst verwenden wir ein Klammerpaar, um das ganze Pattern zu umschließen. Mit
einem Dollarzeichen (`$`) deklarieren wir eine Variable im Makrosystem, die den
Rust-Code enthält, der auf das Pattern passt. Das Dollarzeichen macht deutlich,
dass es sich um eine Makrovariable und nicht um eine normale Rust-Variable
handelt. Als Nächstes kommt ein Klammerpaar, das Werte erfasst, die auf das
Pattern innerhalb der Klammern passen, um sie im Ersetzungscode zu verwenden.
Innerhalb von `$()` steht `$x:expr`, das auf jeden Rust-Ausdruck passt und dem
Ausdruck den Namen `$x` gibt.

Das Komma nach `$()` gibt an, dass zwischen jeder Instanz des Codes, die auf den
Code in `$()` passt, ein literales Komma als Trennzeichen stehen muss. Das `*`
gibt an, dass das Pattern auf null oder mehr Vorkommen dessen passt, was vor dem
`*` steht.

Wenn wir dieses Makro mit `vec![1, 2, 3];` aufrufen, passt das Pattern `$x`
dreimal, mit den drei Ausdrücken `1`, `2` und `3`.

Sehen wir uns nun das Pattern im Rumpf des Codes an, der zu diesem Arm gehört:
`temp_vec.push()` innerhalb von `$()*` wird für jeden Teil erzeugt, der auf
`$()` im Pattern passt, null- oder mehrmals, je nachdem, wie oft das Pattern
passt. Das `$x` wird durch jeden passenden Ausdruck ersetzt. Wenn wir dieses
Makro mit `vec![1, 2, 3];` aufrufen, ist der erzeugte Code, der diesen
Makroaufruf ersetzt, der folgende:

```rust,ignore
{
    let mut temp_vec = Vec::new();
    temp_vec.push(1);
    temp_vec.push(2);
    temp_vec.push(3);
    temp_vec
}
```

Wir haben ein Makro definiert, das beliebig viele Argumente beliebigen Typs
nehmen und Code erzeugen kann, um einen Vektor mit den angegebenen Elementen zu
erstellen.

Um mehr darüber zu erfahren, wie man Makros schreibt, sieh in der
Online-Dokumentation oder anderen Ressourcen nach, etwa in
[„The Little Book of Rust Macros“][tlborm], das von Daniel Keep begonnen und von
Lukas Wirth fortgeführt wurde.

### Prozedurale Makros, um Code aus Attributen zu erzeugen {#procedural-macros-for-generating-code-from-attributes}

Die zweite Form von Makros ist das prozedurale Makro, das sich eher wie eine
Funktion verhält (und eine Art Prozedur ist). _Prozedurale Makros_ nehmen Code
als Eingabe, verarbeiten diesen Code und erzeugen Code als Ausgabe, statt wie
deklarative Makros mit Patterns abzugleichen und den Code durch anderen Code zu
ersetzen. Die drei Arten prozeduraler Makros sind benutzerdefinierte
`derive`-Makros, attributähnliche und funktionsähnliche Makros, und alle
funktionieren auf ähnliche Weise.

Beim Erstellen prozeduraler Makros müssen die Definitionen in einem eigenen
Crate mit einem speziellen Crate-Typ liegen. Das hat komplexe technische Gründe,
die wir in Zukunft hoffentlich beseitigen können. In Listing 20-36 zeigen wir,
wie man ein prozedurales Makro definiert, wobei `some_attribute` ein Platzhalter
für die Verwendung einer bestimmten Makro-Art ist.

<Listing number="20-36" file-name="src/lib.rs" caption="Ein Beispiel für die Definition eines prozeduralen Makros">

```rust,ignore
use proc_macro::TokenStream;

#[some_attribute]
pub fn some_name(input: TokenStream) -> TokenStream {
}
```

</Listing>

Die Funktion, die ein prozedurales Makro definiert, nimmt einen `TokenStream`
als Eingabe und erzeugt einen `TokenStream` als Ausgabe. Der Typ `TokenStream`
ist im Crate `proc_macro` definiert, der zu Rust gehört, und stellt eine Folge
von Tokens dar. Das ist der Kern des Makros: Der Quellcode, auf dem das Makro
arbeitet, bildet den Eingabe-`TokenStream`, und der Code, den das Makro erzeugt,
ist der Ausgabe-`TokenStream`. Die Funktion hat außerdem ein Attribut, das
angibt, welche Art von prozeduralem Makro wir erstellen. Wir können mehrere
Arten prozeduraler Makros im selben Crate haben.

Sehen wir uns die verschiedenen Arten prozeduraler Makros an. Wir beginnen mit
einem benutzerdefinierten `derive`-Makro und erklären dann die kleinen
Abweichungen, die die anderen Formen unterscheiden.

<!-- Old headings. Do not remove or links may break. -->

<a id="how-to-write-a-custom-derive-macro"></a>

### Benutzerdefinierte `derive`-Makros {#custom-derive-macros}

Erstellen wir einen Crate namens `hello_macro`, der einen Trait namens
`HelloMacro` mit einer assoziierten Funktion namens `hello_macro` definiert.
Statt unsere Benutzer den Trait `HelloMacro` für jeden ihrer Typen
implementieren zu lassen, stellen wir ein prozedurales Makro bereit, damit
Benutzer ihren Typ mit `#[derive(HelloMacro)]` annotieren können, um eine
Standardimplementierung der Funktion `hello_macro` zu erhalten. Die
Standardimplementierung gibt `Hello, Macro! My name is
TypeName!` aus, wobei
`TypeName` der Name des Typs ist, für den dieser Trait definiert wurde. Mit
anderen Worten: Wir schreiben einen Crate, mit dem ein anderer Programmierer
Code wie in Listing 20-37 schreiben kann, der unseren Crate verwendet.

<Listing number="20-37" file-name="src/main.rs" caption="Der Code, den ein Benutzer unseres Crates schreiben kann, wenn er unser prozedurales Makro verwendet">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-37/src/main.rs}}
```

</Listing>

Dieser Code gibt `Hello, Macro! My name is Pancakes!` aus, wenn wir fertig sind.
Der erste Schritt besteht darin, einen neuen Library-Crate zu erstellen, etwa
so:

```console
$ cargo new hello_macro --lib
```

Als Nächstes definieren wir in Listing 20-38 den Trait `HelloMacro` und seine
assoziierte Funktion.

<Listing file-name="src/lib.rs" number="20-38" caption="Ein einfacher Trait, den wir mit dem `derive`-Makro verwenden werden">

```rust,noplayground
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-38/hello_macro/src/lib.rs}}
```

</Listing>

Wir haben einen Trait und seine Funktion. An diesem Punkt könnte ein Benutzer
unseres Crates den Trait implementieren, um die gewünschte Funktionalität zu
erreichen, wie in Listing 20-39.

<Listing number="20-39" file-name="src/main.rs" caption="Wie es aussähe, wenn Benutzer eine manuelle Implementierung des Traits `HelloMacro` schreiben würden">

```rust,ignore
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-39/pancakes/src/main.rs}}
```

</Listing>

Dann müssten sie jedoch für jeden Typ, den sie mit `hello_macro` verwenden
wollen, den Implementierungsblock schreiben; diese Arbeit wollen wir ihnen
ersparen.

Außerdem können wir die Funktion `hello_macro` noch nicht mit einer
Standardimplementierung versehen, die den Namen des Typs ausgibt, für den der
Trait implementiert ist: Rust hat keine Reflection-Fähigkeiten und kann daher
den Namen des Typs nicht zur Laufzeit nachschlagen. Wir brauchen ein Makro, um
zur Kompilierzeit Code zu erzeugen.

Der nächste Schritt ist, das prozedurale Makro zu definieren. Zum Zeitpunkt der
Entstehung dieses Textes müssen prozedurale Makros in einem eigenen Crate
liegen. Irgendwann wird diese Einschränkung vielleicht aufgehoben. Die
Konvention für die Strukturierung von Crates und Makro-Crates lautet: Für einen
Crate namens `foo` heißt ein Crate mit einem benutzerdefinierten prozeduralen
`derive`-Makro `foo_derive`. Beginnen wir einen neuen Crate namens
`hello_macro_derive` innerhalb unseres Projekts `hello_macro`:

```console
$ cargo new hello_macro_derive --lib
```

Unsere beiden Crates sind eng miteinander verwandt, daher erstellen wir den
Crate für das prozedurale Makro innerhalb des Verzeichnisses unseres Crates
`hello_macro`. Wenn wir die Trait-Definition in `hello_macro` ändern, müssen wir
auch die Implementierung des prozeduralen Makros in `hello_macro_derive` ändern.
Die beiden Crates müssen separat veröffentlicht werden, und Programmierer, die
diese Crates verwenden, müssen beide als Abhängigkeiten hinzufügen und beide in
den Gültigkeitsbereich bringen. Wir könnten stattdessen den Crate `hello_macro`
`hello_macro_derive` als Abhängigkeit verwenden lassen und den Code des
prozeduralen Makros re-exportieren. Durch die Art, wie wir das Projekt
strukturiert haben, können Programmierer `hello_macro` aber auch dann verwenden,
wenn sie die `derive`-Funktionalität nicht wollen.

Wir müssen den Crate `hello_macro_derive` als Crate für prozedurale Makros
deklarieren. Außerdem brauchen wir Funktionalität aus den Crates `syn` und
`quote`, wie du gleich sehen wirst, daher müssen wir sie als Abhängigkeiten
hinzufügen. Füge Folgendes zur Datei _Cargo.toml_ von `hello_macro_derive`
hinzu:

<Listing file-name="hello_macro_derive/Cargo.toml">

```toml
{{#include ../listings/ch20-advanced-features/listing-20-40/hello_macro/hello_macro_derive/Cargo.toml:6:12}}
```

</Listing>

Um mit der Definition des prozeduralen Makros zu beginnen, füge den Code aus
Listing 20-40 in deine Datei _src/lib.rs_ für den Crate `hello_macro_derive`
ein. Beachte, dass dieser Code erst kompiliert, wenn wir eine Definition für die
Funktion `impl_hello_macro` hinzufügen.

<Listing number="20-40" file-name="hello_macro_derive/src/lib.rs" caption="Code, den die meisten Crates für prozedurale Makros brauchen, um Rust-Code zu verarbeiten">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-40/hello_macro/hello_macro_derive/src/lib.rs}}
```

</Listing>

Beachte, dass wir den Code in die Funktion `hello_macro_derive`, die für das
Parsen des `TokenStream` zuständig ist, und die Funktion `impl_hello_macro`
aufgeteilt haben, die für die Umwandlung des Syntaxbaums zuständig ist: Das
macht das Schreiben eines prozeduralen Makros bequemer. Der Code in der äußeren
Funktion (hier `hello_macro_derive`) ist für fast jeden Crate mit prozeduralen
Makros, den du siehst oder erstellst, derselbe. Der Code, den du im Rumpf der
inneren Funktion (hier `impl_hello_macro`) angibst, unterscheidet sich je nach
Zweck deines prozeduralen Makros.

Wir haben drei neue Crates eingeführt: `proc_macro`, [`syn`][syn]<!-- ignore -->
und [`quote`][quote]<!-- ignore -->. Der Crate `proc_macro` gehört zu Rust,
daher mussten wir ihn nicht zu den Abhängigkeiten in _Cargo.toml_ hinzufügen.
Der Crate `proc_macro` ist die API des Compilers, mit der wir Rust-Code aus
unserem Code heraus lesen und verändern können.

Der Crate `syn` parst Rust-Code aus einem String in eine Datenstruktur, auf der
wir Operationen ausführen können. Der Crate `quote` wandelt
`syn`-Datenstrukturen wieder in Rust-Code um. Diese Crates machen es viel
einfacher, jede Art von Rust-Code zu parsen, die wir verarbeiten möchten: Einen
vollständigen Parser für Rust-Code zu schreiben, ist keine einfache Aufgabe.

Die Funktion `hello_macro_derive` wird aufgerufen, wenn ein Benutzer unserer
Bibliothek `#[derive(HelloMacro)]` bei einem Typ angibt. Das ist möglich, weil
wir die Funktion `hello_macro_derive` hier mit `proc_macro_derive` annotiert und
den Namen `HelloMacro` angegeben haben, der unserem Traitnamen entspricht; das
ist die Konvention, der die meisten prozeduralen Makros folgen.

Die Funktion `hello_macro_derive` wandelt den `input` zunächst von einem
`TokenStream` in eine Datenstruktur um, die wir dann interpretieren und auf der
wir Operationen ausführen können. Hier kommt `syn` ins Spiel. Die Funktion
`parse` in `syn` nimmt einen `TokenStream` und gibt ein Struct `DeriveInput`
zurück, das den geparsten Rust-Code darstellt. Listing 20-41 zeigt die
relevanten Teile des Structs `DeriveInput`, das wir beim Parsen des Strings
`struct Pancakes;` erhalten.

<Listing number="20-41" caption="Die `DeriveInput`-Instanz, die wir beim Parsen des Codes mit dem Attribut des Makros in Listing 20-37 erhalten">

```rust,ignore
DeriveInput {
    // --snip--

    ident: Ident {
        ident: "Pancakes",
        span: #0 bytes(95..103)
    },
    data: Struct(
        DataStruct {
            struct_token: Struct,
            fields: Unit,
            semi_token: Some(
                Semi
            )
        }
    )
}
```

</Listing>

Die Felder dieses Structs zeigen, dass der geparste Rust-Code ein Unit-Struct
mit dem `ident` (_identifier_, also dem Namen) `Pancakes` ist. Dieses Struct hat
weitere Felder, um alle möglichen Arten von Rust-Code zu beschreiben; mehr
Informationen findest du in der
[`syn`-Dokumentation zu `DeriveInput`][syn-docs].

Bald definieren wir die Funktion `impl_hello_macro`, in der wir den neuen
Rust-Code aufbauen, den wir einfügen wollen. Beachte aber vorher, dass die
Ausgabe unseres `derive`-Makros ebenfalls ein `TokenStream` ist. Der
zurückgegebene `TokenStream` wird dem Code hinzugefügt, den die Benutzer unseres
Crates schreiben, sodass sie beim Kompilieren ihres Crates die zusätzliche
Funktionalität erhalten, die wir im veränderten `TokenStream` bereitstellen.

Vielleicht ist dir aufgefallen, dass wir `unwrap` aufrufen, damit die Funktion
`hello_macro_derive` einen Panic auslöst, wenn der Aufruf der Funktion
`syn::parse` hier fehlschlägt. Unser prozedurales Makro muss bei Fehlern einen
Panic auslösen, weil `proc_macro_derive`-Funktionen einen `TokenStream` statt
eines `Result` zurückgeben müssen, um der API für prozedurale Makros zu
entsprechen. Wir haben dieses Beispiel vereinfacht, indem wir `unwrap`
verwenden; in Produktivcode solltest du mit `panic!` oder `expect` genauere
Fehlermeldungen darüber ausgeben, was schiefgelaufen ist.

Jetzt, da wir den Code haben, um den annotierten Rust-Code aus einem
`TokenStream` in eine `DeriveInput`-Instanz umzuwandeln, erzeugen wir den Code,
der den Trait `HelloMacro` für den annotierten Typ implementiert, wie in Listing
20-42 gezeigt.

<Listing number="20-42" file-name="hello_macro_derive/src/lib.rs" caption="Den Trait `HelloMacro` mithilfe des geparsten Rust-Codes implementieren">

```rust,ignore
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-42/hello_macro/hello_macro_derive/src/lib.rs:here}}
```

</Listing>

Mit `ast.ident` erhalten wir eine Instanz des Structs `Ident`, die den Namen
(Bezeichner) des annotierten Typs enthält. Das Struct in Listing 20-41 zeigt,
dass das `ident`, das wir erhalten, wenn wir die Funktion `impl_hello_macro` auf
den Code in Listing 20-37 anwenden, im Feld `ident` den Wert `"Pancakes"` hat.
Die Variable `name` in Listing 20-42 enthält also eine Instanz des Structs
`Ident`, die ausgegeben den String `"Pancakes"` ergibt, den Namen des Structs in
Listing 20-37.

Mit dem Makro `quote!` können wir den Rust-Code definieren, den wir zurückgeben
wollen. Der Compiler erwartet etwas anderes als das direkte Ergebnis der
Ausführung des Makros `quote!`, daher müssen wir es in einen `TokenStream`
umwandeln. Das tun wir, indem wir die Methode `into` aufrufen, die diese
Zwischendarstellung verbraucht und einen Wert des benötigten Typs `TokenStream`
zurückgibt.

Das Makro `quote!` bietet außerdem einige sehr praktische Template-Mechanismen:
Wir können `#name` eingeben, und `quote!` ersetzt es durch den Wert in der
Variablen `name`. Du kannst sogar Wiederholungen ähnlich wie bei normalen Makros
verwenden. Eine gründliche Einführung findest du in
[der Dokumentation des Crates `quote`][quote-docs].

Unser prozedurales Makro soll eine Implementierung unseres Traits `HelloMacro`
für den Typ erzeugen, den der Benutzer annotiert hat und den wir mit `#name`
erhalten können. Die Trait-Implementierung hat die eine Funktion `hello_macro`,
deren Rumpf die Funktionalität enthält, die wir bereitstellen wollen: die
Ausgabe von `Hello, Macro! My name is`, gefolgt vom Namen des annotierten Typs.

Das hier verwendete Makro `stringify!` ist in Rust eingebaut. Es nimmt einen
Rust-Ausdruck wie `1 + 2` und wandelt ihn zur Kompilierzeit in ein
String-Literal wie `"1 + 2"` um. Das unterscheidet sich von `format!` oder
`println!`, die Makros sind, die den Ausdruck auswerten und das Ergebnis dann in
einen `String` umwandeln. Es ist möglich, dass die Eingabe `#name` ein Ausdruck
ist, der wörtlich ausgegeben werden soll, daher verwenden wir `stringify!`. Die
Verwendung von `stringify!` spart außerdem eine Allokation, weil `#name` zur
Kompilierzeit in ein String-Literal umgewandelt wird.

An diesem Punkt sollte `cargo build` sowohl in `hello_macro` als auch in
`hello_macro_derive` erfolgreich durchlaufen. Verbinden wir diese Crates mit dem
Code in Listing 20-37, um das prozedurale Makro in Aktion zu sehen! Erstelle mit
`cargo new pancakes` ein neues Binary-Projekt in deinem Verzeichnis _projects_.
Wir müssen `hello_macro` und `hello_macro_derive` als Abhängigkeiten in der
_Cargo.toml_ des Crates `pancakes` hinzufügen. Wenn du deine Versionen von
`hello_macro` und `hello_macro_derive` auf
[crates.io](https://crates.io/)<!-- ignore --> veröffentlichst, wären sie
normale Abhängigkeiten; wenn nicht, kannst du sie wie folgt als
`path`-Abhängigkeiten angeben:

```toml
{{#include ../listings/ch20-advanced-features/no-listing-21-pancakes/pancakes/Cargo.toml:6:8}}
```

Füge den Code aus Listing 20-37 in _src/main.rs_ ein und führe `cargo run` aus:
Es sollte `Hello, Macro! My name is Pancakes!` ausgeben. Die Implementierung des
Traits `HelloMacro` aus dem prozeduralen Makro wurde eingefügt, ohne dass der
Crate `pancakes` sie implementieren musste; `#[derive(HelloMacro)]` hat die
Trait-Implementierung hinzugefügt.

Sehen wir uns als Nächstes an, wie sich die anderen Arten prozeduraler Makros
von benutzerdefinierten `derive`-Makros unterscheiden.

### Attributähnliche Makros {#attribute-like-macros}

Attributähnliche Makros ähneln benutzerdefinierten `derive`-Makros, aber statt
Code für das Attribut `derive` zu erzeugen, ermöglichen sie es dir, neue
Attribute zu erstellen. Außerdem sind sie flexibler: `derive` funktioniert nur
für Structs und Enums; Attribute können auch auf andere Elemente angewendet
werden, etwa auf Funktionen. Hier ist ein Beispiel für die Verwendung eines
attributähnlichen Makros. Angenommen, du hast ein Attribut namens `route`, mit
dem du Funktionen annotierst, wenn du ein Framework für Webanwendungen
verwendest:

```rust,ignore
#[route(GET, "/")]
fn index() {
```

Dieses Attribut `#[route]` würde vom Framework als prozedurales Makro definiert.
Die Signatur der Funktion, die das Makro definiert, sähe so aus:

```rust,ignore
#[proc_macro_attribute]
pub fn route(attr: TokenStream, item: TokenStream) -> TokenStream {
```

Hier haben wir zwei Parameter vom Typ `TokenStream`. Der erste ist für den
Inhalt des Attributs: den Teil `GET, "/"`. Der zweite ist der Rumpf des
Elements, an dem das Attribut hängt: in diesem Fall `fn index() {}` und der Rest
des Funktionsrumpfs.

Abgesehen davon funktionieren attributähnliche Makros genauso wie
benutzerdefinierte `derive`-Makros: Du erstellst einen Crate mit dem Crate-Typ
`proc-macro` und implementierst eine Funktion, die den gewünschten Code erzeugt!

### Funktionsähnliche Makros {#function-like-macros}

Funktionsähnliche Makros definieren Makros, die wie Funktionsaufrufe aussehen.
Ähnlich wie `macro_rules!`-Makros sind sie flexibler als Funktionen; sie können
zum Beispiel eine unbekannte Anzahl von Argumenten nehmen. `macro_rules!`-Makros
können jedoch nur mit der match-ähnlichen Syntax definiert werden, die wir
vorhin im Abschnitt
[„Deklarative Makros für allgemeine Metaprogrammierung“][decl]<!-- ignore -->
besprochen haben. Funktionsähnliche Makros nehmen einen Parameter vom Typ
`TokenStream`, und ihre Definition verändert diesen `TokenStream` mit Rust-Code,
so wie es die beiden anderen Arten prozeduraler Makros tun. Ein Beispiel für ein
funktionsähnliches Makro ist ein Makro `sql!`, das etwa so aufgerufen werden
könnte:

```rust,ignore
let sql = sql!(SELECT * FROM posts WHERE id=1);
```

Dieses Makro würde die SQL-Anweisung darin parsen und prüfen, ob sie syntaktisch
korrekt ist, was eine viel komplexere Verarbeitung ist, als ein
`macro_rules!`-Makro leisten kann. Das Makro `sql!` würde so definiert:

```rust,ignore
#[proc_macro]
pub fn sql(input: TokenStream) -> TokenStream {
```

Diese Definition ähnelt der Signatur des benutzerdefinierten `derive`-Makros:
Wir erhalten die Tokens, die innerhalb der Klammern stehen, und geben den Code
zurück, den wir erzeugen wollten.

{{#quiz ../quizzes/ch19-06-macros.toml}}

## Zusammenfassung {#summary}

Puh! Jetzt hast du einige Rust-Features in deinem Werkzeugkasten, die du
wahrscheinlich nicht oft verwenden wirst, von denen du aber weißt, dass sie in
ganz bestimmten Situationen zur Verfügung stehen. Wir haben mehrere komplexe
Themen vorgestellt, damit du diese Konzepte und diese Syntax wiedererkennst,
wenn sie dir in Vorschlägen von Fehlermeldungen oder im Code anderer Leute
begegnen. Nutze dieses Kapitel als Referenz, die dich zu Lösungen führt.

Als Nächstes setzen wir alles, was wir im Lauf des Buches besprochen haben, in
die Praxis um und machen noch ein weiteres Projekt!

[ref]: https://doc.rust-lang.org/reference/macros-by-example.html
[tlborm]: https://veykril.github.io/tlborm/
[syn]: https://crates.io/crates/syn
[quote]: https://crates.io/crates/quote
[syn-docs]: https://docs.rs/syn/2.0/syn/struct.DeriveInput.html
[quote-docs]: https://docs.rs/quote
[decl]: #declarative-macros-with-macro_rules-for-general-metaprogramming
