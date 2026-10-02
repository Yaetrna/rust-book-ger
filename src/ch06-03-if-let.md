## Knapper Kontrollfluss mit `if let` und `let...else` {#concise-control-flow-with-if-let-and-letelse}

Mit der Syntax `if let` kannst du `if` und `let` zu einer weniger umständlichen
Form kombinieren, um Werte zu behandeln, die auf ein Pattern passen, und den
Rest zu ignorieren. Betrachte das Programm in Listing 6-6, das per
Pattern-Matching einen `Option<u8>`-Wert in der Variable `config_max` prüft,
aber nur dann Code ausführen will, wenn der Wert die Variante `Some` ist.

<Listing number="6-6" caption="Ein `match`, das nur dann Code ausführen soll, wenn der Wert `Some` ist">

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/listing-06-06/src/main.rs:here}}
```

</Listing>

Ist der Wert `Some`, geben wir den Wert in der Variante `Some` aus, indem wir
ihn im Pattern an die Variable `max` binden. Mit dem Wert `None` wollen wir
nichts tun. Um den `match`-Ausdruck zufriedenzustellen, müssen wir nach der
Verarbeitung nur einer Variante `_ =>
()` hinzufügen, was lästiger
Boilerplate-Code ist.

Stattdessen könnten wir das mit `if let` kürzer schreiben. Der folgende Code
verhält sich genauso wie das `match` in Listing 6-6:

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-12-if-let/src/main.rs:here}}
```

Die Syntax `if let` nimmt ein Pattern und einen Ausdruck, getrennt durch ein
Gleichheitszeichen. Sie funktioniert genauso wie ein `match`, wobei der Ausdruck
dem `match` übergeben wird und das Pattern dessen erster Arm ist. In diesem Fall
ist das Pattern `Some(max)`, und `max` bindet an den Wert im `Some`. Wir können
`max` dann im Rumpf des `if let`-Blocks genauso verwenden, wie wir `max` im
entsprechenden `match`-Arm verwendet haben. Der Code im `if let`-Block wird nur
ausgeführt, wenn der Wert auf das Pattern passt.

`if let` bedeutet weniger Tipparbeit, weniger Einrückung und weniger
Boilerplate-Code. Dafür verlierst du die Vollständigkeitsprüfung, die `match`
erzwingt und die sicherstellt, dass du keinen Fall vergisst. Ob du `match` oder
`if
let` wählst, hängt davon ab, was du in deiner konkreten Situation tust und ob
der Gewinn an Knappheit den Verlust der Vollständigkeitsprüfung aufwiegt.

Anders gesagt kannst du dir `if let` als syntaktischen Zucker für ein `match`
vorstellen, das Code ausführt, wenn der Wert auf ein Pattern passt, und alle
anderen Werte ignoriert.

Wir können zu einem `if let` ein `else` hinzufügen. Der Codeblock, der zum
`else` gehört, ist derselbe wie der Codeblock, der zum Fall `_` im
`match`-Ausdruck gehören würde, der dem `if let` mit `else` entspricht. Erinnere
dich an die Definition des Enums `Coin` in Listing 6-4, in der die Variante
`Quarter` zusätzlich einen `UsState`-Wert enthielt. Wollten wir alle Münzen
zählen, die keine Quarters sind, und gleichzeitig den Bundesstaat der Quarters
ausrufen, könnten wir das mit einem `match`-Ausdruck tun, etwa so:

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-13-count-and-announce-match/src/main.rs:here}}
```

Oder wir könnten einen Ausdruck mit `if let` und `else` verwenden, etwa so:

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-14-count-and-announce-if-let-else/src/main.rs:here}}
```

## Mit `let...else` auf dem „Happy Path“ bleiben {#staying-on-the-happy-path-with-letelse}

Ein gängiges Schema ist, eine Berechnung durchzuführen, wenn ein Wert vorhanden
ist, und andernfalls einen Standardwert zurückzugeben. Um bei unserem Beispiel
mit Münzen mit einem `UsState`-Wert zu bleiben: Wenn wir je nachdem, wie alt der
Bundesstaat auf dem Quarter ist, etwas Lustiges sagen wollten, könnten wir auf
`UsState` eine Methode einführen, die das Alter eines Bundesstaats prüft, etwa
so:

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/listing-06-07/src/main.rs:state}}
```

Dann könnten wir `if let` verwenden, um per Pattern-Matching die Art der Münze
zu prüfen und im Rumpf der Bedingung eine Variable `state` einzuführen, wie in
Listing 6-7.

<Listing number="6-7" caption="Mit Bedingungen, die in einem `if let` verschachtelt sind, prüfen, ob ein Bundesstaat im Jahr 1900 schon existierte">

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/listing-06-07/src/main.rs:describe}}
```

</Listing>

Das erledigt die Aufgabe, verlagert die Arbeit aber in den Rumpf der
`if
let`-Anweisung, und wenn die zu erledigende Arbeit komplizierter ist, lässt
sich womöglich schwer nachvollziehen, wie genau die Verzweigungen auf oberster
Ebene zusammenhängen. Wir könnten auch ausnutzen, dass Ausdrücke einen Wert
erzeugen, um entweder den `state` aus dem `if let` zu erzeugen oder vorzeitig
zurückzukehren, wie in Listing 6-8. (Etwas Ähnliches könntest du auch mit einem
`match` machen.)

<Listing number="6-8" caption="Mit `if let` einen Wert erzeugen oder vorzeitig zurückkehren">

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/listing-06-08/src/main.rs:describe}}
```

</Listing>

Auf seine eigene Weise ist auch das etwas mühsam nachzuvollziehen! Ein Zweig des
`if
let` erzeugt einen Wert, und der andere kehrt ganz aus der Funktion zurück.

Damit sich dieses gängige Schema schöner ausdrücken lässt, hat Rust
`let...else`. Die Syntax `let...else` nimmt links ein Pattern und rechts einen
Ausdruck, sehr ähnlich wie `if let`, hat aber keinen `if`-Zweig, sondern nur
einen `else`-Zweig. Passt das Pattern, bindet es den Wert aus dem Pattern im
äußeren Gültigkeitsbereich (_scope_). Passt das Pattern _nicht_, fließt das
Programm in den `else`-Arm, der aus der Funktion zurückkehren muss.

In Listing 6-9 siehst du, wie Listing 6-8 aussieht, wenn man `let...else` statt
`if let` verwendet.

<Listing number="6-9" caption="Mit `let...else` den Ablauf durch die Funktion verdeutlichen">

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/listing-06-09/src/main.rs:describe}}
```

</Listing>

Beachte, dass die Funktion auf diese Weise im Hauptrumpf auf dem „Happy Path“
bleibt, ohne dass sich der Kontrollfluss für zwei Zweige so stark unterscheidet
wie beim `if let`.

Wenn dein Programm in einer Situation Logik enthält, die mit einem `match` zu
umständlich auszudrücken wäre, denk daran, dass `if let` und `let...else`
ebenfalls in deinem Rust-Werkzeugkasten liegen.

{{#quiz ../quizzes/ch06-03-if-let.toml}}

## Zusammenfassung {#summary}

Wir haben jetzt behandelt, wie du mit Enums eigene Typen erstellst, die einer
aus einer Menge aufgezählter Werte sein können. Wir haben gezeigt, wie dir der
Typ `Option<T>` der Standardbibliothek hilft, mit dem Typsystem Fehler zu
verhindern. Wenn Enum-Werte Daten enthalten, kannst du je nachdem, wie viele
Fälle du behandeln musst, `match` oder `if let` verwenden, um diese Werte
herauszuholen und zu verwenden.

Deine Rust-Programme können jetzt mit Structs und Enums Konzepte deines
Anwendungsbereichs ausdrücken. Eigene Typen in deiner API zu verwenden, sorgt
für Typsicherheit: Der Compiler stellt sicher, dass deine Funktionen nur Werte
des Typs bekommen, den die jeweilige Funktion erwartet.

Um deinen Nutzerinnen und Nutzern eine gut organisierte API zu bieten, die
unkompliziert zu verwenden ist und genau das bereitstellt, was sie brauchen,
wenden wir uns nun den Modulen von Rust zu.
