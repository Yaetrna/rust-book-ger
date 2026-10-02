## Generische Datentypen {#generic-data-types}

Mit Generics erstellen wir Definitionen für Elemente wie Funktionssignaturen
oder Structs, die wir dann mit vielen verschiedenen konkreten Datentypen
verwenden können. Sehen wir uns zuerst an, wie man Funktionen, Structs, Enums
und Methoden mit Generics definiert. Dann besprechen wir, wie sich Generics auf
die Performance des Codes auswirken.

### In Funktionsdefinitionen {#in-function-definitions}

Wenn wir eine Funktion definieren, die Generics verwendet, setzen wir die
Generics in die Signatur der Funktion, dort, wo wir normalerweise die Datentypen
der Parameter und des Rückgabewerts angeben würden. Dadurch wird unser Code
flexibler und bietet den Aufrufern unserer Funktion mehr Funktionalität, während
Codeduplizierung vermieden wird.

Um mit unserer Funktion `largest` weiterzumachen, zeigt Listing 10-4 zwei
Funktionen, die beide den größten Wert in einem Slice finden. Diese fassen wir
dann zu einer einzigen Funktion zusammen, die Generics verwendet.

<Listing number="10-4" file-name="src/main.rs" caption="Zwei Funktionen, die sich nur in ihren Namen und den Typen in ihren Signaturen unterscheiden">

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-04/src/main.rs:here}}
```

</Listing>

Die Funktion `largest_i32` ist die, die wir in Listing 10-3 extrahiert haben und
die den größten `i32` in einem Slice findet. Die Funktion `largest_char` findet
den größten `char` in einem Slice. Die Funktionsrümpfe enthalten denselben Code,
also beseitigen wir die Duplizierung, indem wir in einer einzigen Funktion einen
generischen Typparameter einführen.

Um die Typen in einer neuen, einzigen Funktion zu parametrisieren, müssen wir
den Typparameter benennen, genau wie wir es bei den Wertparametern einer
Funktion tun. Du kannst jeden Bezeichner als Namen für einen Typparameter
verwenden. Wir verwenden aber `T`, weil Typparameternamen in Rust nach
Konvention kurz sind, oft nur ein Buchstabe, und die Namenskonvention für Typen
in Rust UpperCamelCase ist. `T`, kurz für _Typ_ (_type_), ist die Standardwahl
der meisten Rust-Programmierenden.

Wenn wir einen Parameter im Rumpf der Funktion verwenden, müssen wir den
Parameternamen in der Signatur deklarieren, damit der Compiler weiß, was dieser
Name bedeutet. Ebenso müssen wir, wenn wir einen Typparameternamen in einer
Funktionssignatur verwenden, den Typparameternamen deklarieren, bevor wir ihn
verwenden. Um die generische Funktion `largest` zu definieren, setzen wir
Deklarationen von Typnamen in spitze Klammern, `<>`, zwischen den Namen der
Funktion und die Parameterliste, etwa so:

```rust,ignore
fn largest<T>(list: &[T]) -> &T {
```

Wir lesen diese Definition so: „Die Funktion `largest` ist generisch über einen
Typ `T`.“ Diese Funktion hat einen Parameter namens `list`, der ein Slice von
Werten vom Typ `T` ist. Die Funktion `largest` gibt eine Referenz auf einen Wert
desselben Typs `T` zurück.

Listing 10-5 zeigt die zusammengefasste Definition der Funktion `largest`, die
den generischen Datentyp in ihrer Signatur verwendet. Das Listing zeigt
außerdem, wie wir die Funktion entweder mit einem Slice von `i32`-Werten oder
mit `char`-Werten aufrufen können. Beachte, dass dieser Code noch nicht
kompiliert.

<Listing number="10-5" file-name="src/main.rs" caption="Die Funktion `largest` mit generischen Typparametern; das kompiliert noch nicht">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-05/src/main.rs}}
```

</Listing>

Wenn wir diesen Code jetzt kompilieren, erhalten wir diesen Fehler:

```console
{{#include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-05/output.txt}}
```

<!-- BEGIN INTERVENTION: 0aad53ff-89d7-4d14-8e3d-c17809220252 -->

Das Problem ist hier: Wenn `largest` einen Slice `&[T]` als Eingabe nimmt, kann
die Funktion _nichts_ über den Typ `T` annehmen. Er könnte `i32` sein, er könnte
`String` sein, er könnte
[`File`](https://doc.rust-lang.org/std/fs/struct.File.html) sein. `largest`
setzt aber voraus, dass sich `T` mit `>` vergleichen lässt (d. h., dass `T`
`PartialOrd` implementiert, einen Trait, den wir im nächsten Abschnitt
besprechen). Manche Typen wie `i32` und `String` sind vergleichbar, andere Typen
wie `File` dagegen nicht.

In einer Sprache wie C++ mit
[Templates](https://en.cppreference.com/w/cpp/language/templates) würde sich der
Compiler nicht über die Implementierung von `largest` beschweren, sondern
stattdessen über den Versuch, `largest` z. B. auf einem Datei-Slice `&[File]`
aufzurufen. Rust verlangt dagegen, dass du die erwarteten Fähigkeiten
generischer Typen von vornherein angibst. Muss `T` vergleichbar sein, muss
`largest` das sagen. Deshalb besagt dieser Compilerfehler, dass `largest` erst
kompiliert, wenn `T` eingeschränkt ist.

Anders als in Sprachen wie Java, in denen alle Objekte eine Reihe grundlegender
Methoden wie
[`Object.toString()`](https://docs.oracle.com/javase/7/docs/api/java/lang/Object.html#toString())
haben, gibt es in Rust außerdem keine grundlegenden Methoden. Ohne
Einschränkungen hat ein generischer Typ `T` keine Fähigkeiten: Er kann nicht
ausgegeben, geklont oder verändert werden (verworfen (_dropped_) werden kann er
allerdings).

<!-- END INTERVENTION -->

### In Struct-Definitionen {#in-struct-definitions}

Wir können auch Structs so definieren, dass sie in einem oder mehreren Feldern
einen generischen Typparameter verwenden, und zwar mit der Syntax `<>`. Listing
10-6 definiert ein Struct `Point<T>`, das `x`- und `y`-Koordinaten eines
beliebigen Typs enthält.

<Listing number="10-6" file-name="src/main.rs" caption="Ein Struct `Point<T>`, das `x`- und `y`-Werte vom Typ `T` enthält">

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-06/src/main.rs}}
```

</Listing>

Die Syntax für Generics in Struct-Definitionen ähnelt der in
Funktionsdefinitionen. Zuerst deklarieren wir den Namen des Typparameters in
spitzen Klammern direkt nach dem Namen des Structs. Dann verwenden wir den
generischen Typ in der Struct-Definition dort, wo wir sonst konkrete Datentypen
angeben würden.

Beachte: Da wir nur einen generischen Typ verwendet haben, um `Point<T>` zu
definieren, besagt diese Definition, dass das Struct `Point<T>` generisch über
einen Typ `T` ist und die Felder `x` und `y` _beide_ denselben Typ haben,
welcher das auch sein mag. Erzeugen wir eine Instanz von `Point<T>`, die Werte
unterschiedlicher Typen enthält, wie in Listing 10-7, kompiliert unser Code
nicht.

<Listing number="10-7" file-name="src/main.rs" caption="Die Felder `x` und `y` müssen denselben Typ haben, weil beide denselben generischen Datentyp `T` haben.">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-07/src/main.rs}}
```

</Listing>

Wenn wir in diesem Beispiel `x` den Ganzzahlwert `5` zuweisen, teilen wir dem
Compiler mit, dass der generische Typ `T` für diese Instanz von `Point<T>` eine
Ganzzahl sein wird. Wenn wir dann `4.0` für `y` angeben, das wir mit demselben
Typ wie `x` definiert haben, erhalten wir einen Fehler wegen nicht
übereinstimmender Typen wie diesen:

```console
{{#include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-07/output.txt}}
```

Um ein Struct `Point` zu definieren, in dem `x` und `y` beide generisch sind,
aber unterschiedliche Typen haben können, können wir mehrere generische
Typparameter verwenden. In Listing 10-8 ändern wir die Definition von `Point`
zum Beispiel so, dass sie generisch über die Typen `T` und `U` ist, wobei `x`
vom Typ `T` und `y` vom Typ `U` ist.

<Listing number="10-8" file-name="src/main.rs" caption="Ein `Point<T, U>`, das über zwei Typen generisch ist, sodass `x` und `y` Werte unterschiedlicher Typen sein können">

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-08/src/main.rs}}
```

</Listing>

Jetzt sind alle gezeigten Instanzen von `Point` erlaubt! Du kannst in einer
Definition so viele generische Typparameter verwenden, wie du willst, aber mehr
als ein paar machen deinen Code schwer lesbar. Wenn du feststellst, dass du in
deinem Code viele generische Typen brauchst, kann das ein Hinweis darauf sein,
dass dein Code in kleinere Teile umstrukturiert werden sollte.

### In Enum-Definitionen {#in-enum-definitions}

Wie bei Structs können wir Enums so definieren, dass sie in ihren Varianten
generische Datentypen enthalten. Sehen wir uns noch einmal das Enum `Option<T>`
aus der Standardbibliothek an, das wir in Kapitel 6 verwendet haben:

```rust
enum Option<T> {
    Some(T),
    None,
}
```

Diese Definition sollte jetzt verständlicher für dich sein. Wie du siehst, ist
das Enum `Option<T>` generisch über den Typ `T` und hat zwei Varianten: `Some`,
die einen Wert vom Typ `T` enthält, und eine Variante `None`, die keinen Wert
enthält. Mit dem Enum `Option<T>` können wir das abstrakte Konzept eines
optionalen Werts ausdrücken, und da `Option<T>` generisch ist, können wir diese
Abstraktion verwenden, egal welchen Typ der optionale Wert hat.

Enums können auch mehrere generische Typen verwenden. Die Definition des Enums
`Result`, die wir in Kapitel 9 verwendet haben, ist ein Beispiel dafür:

```rust
enum Result<T, E> {
    Ok(T),
    Err(E),
}
```

Das Enum `Result` ist generisch über zwei Typen, `T` und `E`, und hat zwei
Varianten: `Ok`, die einen Wert vom Typ `T` enthält, und `Err`, die einen Wert
vom Typ `E` enthält. Durch diese Definition lässt sich das Enum `Result` bequem
überall verwenden, wo wir eine Operation haben, die erfolgreich sein (einen Wert
eines Typs `T` zurückgeben) oder fehlschlagen (einen Fehler eines Typs `E`
zurückgeben) kann. Genau das haben wir verwendet, um in Listing 9-3 eine Datei
zu öffnen: Dort wurde `T` mit dem Typ `std::fs::File` gefüllt, wenn die Datei
erfolgreich geöffnet wurde, und `E` mit dem Typ `std::io::Error`, wenn es
Probleme beim Öffnen der Datei gab.

Wenn du in deinem Code Situationen mit mehreren Struct- oder Enum-Definitionen
erkennst, die sich nur in den Typen der Werte unterscheiden, die sie enthalten,
kannst du Duplizierung vermeiden, indem du stattdessen generische Typen
verwendest.

### In Methodendefinitionen {#in-method-definitions}

Wir können Methoden auf Structs und Enums implementieren (wie in Kapitel 5) und
auch in ihren Definitionen generische Typen verwenden. Listing 10-9 zeigt das
Struct `Point<T>`, das wir in Listing 10-6 definiert haben, mit einer darauf
implementierten Methode namens `x`.

<Listing number="10-9" file-name="src/main.rs" caption="Eine Methode namens `x` auf dem Struct `Point<T>` implementieren, die eine Referenz auf das Feld `x` vom Typ `T` zurückgibt">

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-09/src/main.rs}}
```

</Listing>

Hier haben wir auf `Point<T>` eine Methode namens `x` definiert, die eine
Referenz auf die Daten im Feld `x` zurückgibt.

Beachte, dass wir `T` direkt nach `impl` deklarieren müssen, damit wir mit `T`
angeben können, dass wir Methoden auf dem Typ `Point<T>` implementieren. Indem
wir `T` nach `impl` als generischen Typ deklarieren, kann Rust erkennen, dass
der Typ in den spitzen Klammern bei `Point` ein generischer und kein konkreter
Typ ist. Wir hätten für diesen generischen Parameter einen anderen Namen wählen
können als für den generischen Parameter in der Struct-Definition, aber
denselben Namen zu verwenden ist üblich. Wenn du eine Methode in einem `impl`
schreibst, das einen generischen Typ deklariert, wird diese Methode für jede
Instanz des Typs definiert, egal welcher konkrete Typ am Ende für den
generischen Typ eingesetzt wird.

Wir können beim Definieren von Methoden auf dem Typ auch Einschränkungen für
generische Typen angeben. Wir könnten zum Beispiel Methoden nur auf
`Point<f32>`-Instanzen implementieren statt auf `Point<T>`-Instanzen mit
beliebigem generischem Typ. In Listing 10-10 verwenden wir den konkreten Typ
`f32`, das heißt, wir deklarieren nach `impl` keine Typen.

<Listing number="10-10" file-name="src/main.rs" caption="Ein `impl`-Block, der nur für ein Struct mit einem bestimmten konkreten Typ für den generischen Typparameter `T` gilt">

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-10/src/main.rs:here}}
```

</Listing>

Dieser Code bedeutet, dass der Typ `Point<f32>` eine Methode
`distance_from_origin` hat; andere Instanzen von `Point<T>`, bei denen `T` nicht
vom Typ `f32` ist, haben diese Methode nicht. Die Methode misst, wie weit unser
Punkt vom Punkt mit den Koordinaten (0.0, 0.0) entfernt ist, und verwendet
mathematische Operationen, die nur für Gleitkommatypen verfügbar sind.

<!-- BEGIN INTERVENTION: 694bb2d0-f2e6-4b0b-a3e7-2d9f9e8b3d09 -->

Auf diese Weise kannst du nicht gleichzeitig spezifische _und_ generische
Methoden mit demselben Namen implementieren. Würdest du zum Beispiel eine
allgemeine Methode `distance_from_origin` für alle Typen `T` und eine
spezifische `distance_from_origin` für `f32` implementieren, würde der Compiler
dein Programm zurückweisen: Rust weiß nicht, welche Implementierung es verwenden
soll, wenn du `Point<f32>::distance_from_origin` aufrufst. Allgemeiner gesagt
hat Rust keine vererbungsähnlichen Mechanismen zum Spezialisieren von Methoden,
wie du sie vielleicht aus einer objektorientierten Sprache kennst – mit einer
Ausnahme (Standardmethoden von Traits), die im nächsten Abschnitt besprochen
wird.

<!-- END INTERVENTION -->

Die generischen Typparameter in einer Struct-Definition sind nicht immer
dieselben wie die, die du in den Methodensignaturen desselben Structs
verwendest. Listing 10-11 verwendet die generischen Typen `X1` und `Y1` für das
Struct `Point` und `X2` und `Y2` für die Signatur der Methode `mixup`, um das
Beispiel deutlicher zu machen. Die Methode erzeugt eine neue `Point`-Instanz mit
dem `x`-Wert aus dem `Point` in `self` (vom Typ `X1`) und dem `y`-Wert aus dem
übergebenen `Point` (vom Typ `Y2`).

<Listing number="10-11" file-name="src/main.rs" caption="Eine Methode, die andere generische Typen verwendet als die Definition ihres Structs">

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-11/src/main.rs}}
```

</Listing>

In `main` haben wir einen `Point` definiert, der einen `i32` für `x` (mit dem
Wert `5`) und einen `f64` für `y` (mit dem Wert `10.4`) hat. Die Variable `p2`
ist ein Struct `Point`, das einen String-Slice für `x` (mit dem Wert `"Hello"`)
und einen `char` für `y` (mit dem Wert `c`) hat. Rufen wir `mixup` auf `p1` mit
dem Argument `p2` auf, erhalten wir `p3`, das einen `i32` für `x` hat, weil `x`
aus `p1` stammt. Die Variable `p3` hat einen `char` für `y`, weil `y` aus `p2`
stammt. Der Aufruf des Makros `println!` gibt `p3.x = 5, p3.y = c` aus.

Dieses Beispiel soll eine Situation zeigen, in der manche generischen Parameter
mit `impl` und manche mit der Methodendefinition deklariert werden. Hier werden
die generischen Parameter `X1` und `Y1` nach `impl` deklariert, weil sie zur
Struct-Definition gehören. Die generischen Parameter `X2` und `Y2` werden nach
`fn mixup` deklariert, weil sie nur für die Methode relevant sind.

### Performance von Code mit Generics {#performance-of-code-using-generics}

Vielleicht fragst du dich, ob generische Typparameter Kosten zur Laufzeit
verursachen. Die gute Nachricht ist: Mit generischen Typen läuft dein Programm
nicht langsamer, als es mit konkreten Typen laufen würde.

Rust erreicht das durch eine Monomorphisierung des Codes mit Generics zur
Kompilierzeit. _Monomorphisierung_ (_monomorphization_) ist der Vorgang,
generischen Code in spezifischen Code umzuwandeln, indem die konkreten Typen
eingesetzt werden, die beim Kompilieren verwendet werden. Dabei tut der Compiler
das Gegenteil der Schritte, mit denen wir die generische Funktion in Listing
10-5 erstellt haben: Der Compiler sieht sich alle Stellen an, an denen
generischer Code aufgerufen wird, und erzeugt Code für die konkreten Typen, mit
denen der generische Code aufgerufen wird.

Sehen wir uns an, wie das funktioniert, und verwenden dafür das generische Enum
`Option<T>` der Standardbibliothek:

```rust
let integer = Some(5);
let float = Some(5.0);
```

Wenn Rust diesen Code kompiliert, führt es eine Monomorphisierung durch. Dabei
liest der Compiler die Werte, die in `Option<T>`-Instanzen verwendet wurden, und
erkennt zwei Arten von `Option<T>`: Die eine ist `i32` und die andere `f64`.
Daher erweitert er die generische Definition von `Option<T>` zu zwei
Definitionen, die auf `i32` und `f64` spezialisiert sind, und ersetzt so die
generische Definition durch die spezifischen.

Die monomorphisierte Version des Codes sieht ungefähr so aus (der Compiler
verwendet andere Namen als die, die wir hier zur Veranschaulichung verwenden):

<Listing file-name="src/main.rs">

```rust
enum Option_i32 {
    Some(i32),
    None,
}

enum Option_f64 {
    Some(f64),
    None,
}

fn main() {
    let integer = Option_i32::Some(5);
    let float = Option_f64::Some(5.0);
}
```

</Listing>

Das generische `Option<T>` wird durch die spezifischen Definitionen ersetzt, die
der Compiler erzeugt. Da Rust generischen Code in Code kompiliert, der in jeder
Instanz den Typ angibt, zahlen wir für die Verwendung von Generics keine Kosten
zur Laufzeit. Wenn der Code läuft, verhält er sich genauso, als hätten wir jede
Definition von Hand dupliziert. Durch die Monomorphisierung sind die Generics
von Rust zur Laufzeit äußerst effizient.

{{#quiz ../quizzes/ch10-01-generics.toml}}
