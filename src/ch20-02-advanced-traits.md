## Fortgeschrittene Traits {#advanced-traits}

Traits haben wir zuerst im Abschnitt
[„Gemeinsames Verhalten mit Traits definieren“][traits]<!-- ignore --> in
Kapitel 10 behandelt, sind dort aber nicht auf die fortgeschritteneren Details
eingegangen. Jetzt, da du mehr über Rust weißt, können wir ins Detail gehen.

<!-- Old headings. Do not remove or links may break. -->

<a id="specifying-placeholder-types-in-trait-definitions-with-associated-types"></a>
<a id="associated-types"></a>

### Traits mit assoziierten Typen definieren {#defining-traits-with-associated-types}

_Assoziierte Typen_ (_associated types_) verbinden einen Typ-Platzhalter mit
einem Trait, sodass die Methodendefinitionen des Traits diese Platzhaltertypen
in ihren Signaturen verwenden können. Der Implementierer eines Traits gibt für
die jeweilige Implementierung den konkreten Typ an, der anstelle des
Platzhaltertyps verwendet werden soll. Auf diese Weise können wir einen Trait
definieren, der einige Typen verwendet, ohne genau wissen zu müssen, welche
Typen das sind, bis der Trait implementiert wird.

Die meisten fortgeschrittenen Features in diesem Kapitel haben wir als selten
benötigt beschrieben. Assoziierte Typen liegen irgendwo in der Mitte: Sie werden
seltener verwendet als die im Rest des Buches erklärten Features, aber häufiger
als viele der anderen in diesem Kapitel besprochenen Features.

Ein Beispiel für einen Trait mit einem assoziierten Typ ist der Trait
`Iterator`, den die Standardbibliothek bereitstellt. Der assoziierte Typ heißt
`Item` und steht für den Typ der Werte, über die der Typ iteriert, der den Trait
`Iterator` implementiert. Die Definition des Traits `Iterator` sieht so aus wie
in Listing 20-13.

<Listing number="20-13" caption="Die Definition des Traits `Iterator`, der einen assoziierten Typ `Item` hat">

```rust,noplayground
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-13/src/lib.rs}}
```

</Listing>

Der Typ `Item` ist ein Platzhalter, und die Definition der Methode `next` zeigt,
dass sie Werte vom Typ `Option<Self::Item>` zurückgibt. Implementierer des
Traits `Iterator` geben den konkreten Typ für `Item` an, und die Methode `next`
gibt eine `Option` zurück, die einen Wert dieses konkreten Typs enthält.

Assoziierte Typen mögen wie ein ähnliches Konzept wie Generics erscheinen, da
Letztere es uns ermöglichen, eine Funktion zu definieren, ohne anzugeben, mit
welchen Typen sie umgehen kann. Um den Unterschied zwischen den beiden Konzepten
zu untersuchen, sehen wir uns eine Implementierung des Traits `Iterator` für
einen Typ namens `Counter` an, die angibt, dass der Typ `Item` `u32` ist:

<Listing file-name="src/lib.rs">

```rust,ignore
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-22-iterator-on-counter/src/lib.rs:ch19}}
```

</Listing>

Diese Syntax scheint mit der von Generics vergleichbar zu sein. Warum definieren
wir den Trait `Iterator` also nicht einfach mit Generics, wie in Listing 20-14
gezeigt?

<Listing number="20-14" caption="Eine hypothetische Definition des Traits `Iterator` mit Generics">

```rust,noplayground
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-14/src/lib.rs}}
```

</Listing>

Der Unterschied ist, dass wir bei der Verwendung von Generics wie in Listing
20-14 die Typen in jeder Implementierung annotieren müssen; weil wir auch
`Iterator<String> for Counter` oder für jeden anderen Typ implementieren können,
könnten wir mehrere Implementierungen von `Iterator` für `Counter` haben. Mit
anderen Worten: Wenn ein Trait einen generischen Parameter hat, kann er für
einen Typ mehrfach implementiert werden, wobei sich jedes Mal die konkreten
Typen der generischen Typparameter ändern. Wenn wir die Methode `next` auf
`Counter` verwenden, müssten wir Typannotationen angeben, um festzulegen, welche
Implementierung von `Iterator` wir verwenden wollen.

Mit assoziierten Typen müssen wir keine Typen annotieren, weil wir einen Trait
nicht mehrfach für einen Typ implementieren können. In Listing 20-13 mit der
Definition, die assoziierte Typen verwendet, können wir nur einmal festlegen,
welchen Typ `Item` haben wird, weil es nur ein einziges
`impl Iterator for Counter` geben kann. Wir müssen nicht überall, wo wir `next`
auf `Counter` aufrufen, angeben, dass wir einen Iterator über `u32`-Werte
wollen.

Assoziierte Typen werden außerdem Teil des Vertrags des Traits: Implementierer
des Traits müssen einen Typ bereitstellen, der für den Platzhalter des
assoziierten Typs steht. Assoziierte Typen haben oft einen Namen, der
beschreibt, wie der Typ verwendet wird, und es ist eine gute Praxis, den
assoziierten Typ in der API-Dokumentation zu dokumentieren.

<!-- Old headings. Do not remove or links may break. -->

<a id="default-generic-type-parameters-and-operator-overloading"></a>

### Generische Standardparameter und Operatorüberladung verwenden {#using-default-generic-parameters-and-operator-overloading}

Wenn wir generische Typparameter verwenden, können wir für den generischen Typ
einen konkreten Standardtyp angeben. Dadurch müssen Implementierer des Traits
keinen konkreten Typ angeben, wenn der Standardtyp passt. Einen Standardtyp gibt
man bei der Deklaration eines generischen Typs mit der Syntax
`<PlaceholderType=ConcreteType>` an.

Ein großartiges Beispiel für eine Situation, in der diese Technik nützlich ist,
ist die _Operatorüberladung_ (_operator overloading_), bei der du das Verhalten
eines Operators (etwa `+`) in bestimmten Situationen anpasst.

Rust erlaubt es dir nicht, eigene Operatoren zu erstellen oder beliebige
Operatoren zu überladen. Du kannst aber die in `std::ops` aufgeführten
Operationen und zugehörigen Traits überladen, indem du die Traits
implementierst, die zum Operator gehören. In Listing 20-15 überladen wir zum
Beispiel den Operator `+`, um zwei `Point`-Instanzen zu addieren. Das tun wir,
indem wir den Trait `Add` für ein Struct `Point` implementieren.

<Listing number="20-15" file-name="src/main.rs" caption="Den Trait `Add` implementieren, um den Operator `+` für `Point`-Instanzen zu überladen">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-15/src/main.rs}}
```

</Listing>

Die Methode `add` addiert die `x`-Werte zweier `Point`-Instanzen und die
`y`-Werte zweier `Point`-Instanzen, um einen neuen `Point` zu erzeugen. Der
Trait `Add` hat einen assoziierten Typ namens `Output`, der den Typ bestimmt,
den die Methode `add` zurückgibt.

Der generische Standardtyp in diesem Code befindet sich im Trait `Add`. Hier ist
seine Definition:

```rust
trait Add<Rhs=Self> {
    type Output;

    fn add(self, rhs: Rhs) -> Self::Output;
}
```

Dieser Code sollte dir im Großen und Ganzen bekannt vorkommen: ein Trait mit
einer Methode und einem assoziierten Typ. Neu ist `Rhs=Self`: Diese Syntax nennt
man _Standard-Typparameter_ (_default type parameters_). Der generische
Typparameter `Rhs` (kurz für „right-hand side“, also die rechte Seite) legt den
Typ des Parameters `rhs` in der Methode `add` fest. Wenn wir beim Implementieren
des Traits `Add` keinen konkreten Typ für `Rhs` angeben, ist der Typ von `Rhs`
standardmäßig `Self`, also der Typ, für den wir `Add` implementieren.

Als wir `Add` für `Point` implementiert haben, haben wir den Standard für `Rhs`
verwendet, weil wir zwei `Point`-Instanzen addieren wollten. Sehen wir uns ein
Beispiel für eine Implementierung des Traits `Add` an, bei der wir den Typ `Rhs`
anpassen wollen, statt den Standard zu verwenden.

Wir haben zwei Structs, `Millimeters` und `Meters`, die Werte in
unterschiedlichen Einheiten enthalten. Diese dünne Hülle um einen bestehenden
Typ in einem anderen Struct ist als _Newtype-Pattern_ bekannt, das wir im
Abschnitt
[„Externe Traits mit dem Newtype-Pattern
implementieren“][newtype]<!-- ignore --> genauer beschreiben. Wir wollen Werte
in Millimetern zu Werten in Metern addieren und die Implementierung von `Add`
die Umrechnung korrekt durchführen lassen. Wir können `Add` für `Millimeters`
mit `Meters` als `Rhs` implementieren, wie in Listing 20-16 gezeigt.

<Listing number="20-16" file-name="src/lib.rs" caption="Den Trait `Add` für `Millimeters` implementieren, um `Millimeters` und `Meters` zu addieren">

```rust,noplayground
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-16/src/lib.rs}}
```

</Listing>

Um `Millimeters` und `Meters` zu addieren, geben wir `impl Add<Meters>` an, um
den Wert des Typparameters `Rhs` festzulegen, statt den Standard `Self` zu
verwenden.

Standard-Typparameter verwendest du hauptsächlich auf zwei Arten:

1. Um einen Typ zu erweitern, ohne bestehenden Code zu beschädigen
2. Um in bestimmten Fällen Anpassungen zu ermöglichen, die die meisten Benutzer
   nicht brauchen

Der Trait `Add` der Standardbibliothek ist ein Beispiel für den zweiten Zweck:
Normalerweise addierst du zwei gleichartige Typen, aber der Trait `Add` bietet
die Möglichkeit, darüber hinaus Anpassungen vorzunehmen. Ein
Standard-Typparameter in der Definition des Traits `Add` bedeutet, dass du den
zusätzlichen Parameter meistens nicht angeben musst. Mit anderen Worten: Ein
bisschen Implementierungs-Boilerplate entfällt, was die Verwendung des Traits
erleichtert.

Der erste Zweck ähnelt dem zweiten, nur umgekehrt: Wenn du einem bestehenden
Trait einen Typparameter hinzufügen möchtest, kannst du ihm einen Standard
geben, um die Funktionalität des Traits erweitern zu können, ohne den
bestehenden Implementierungscode zu beschädigen.

<!-- Old headings. Do not remove or links may break. -->

<a id="fully-qualified-syntax-for-disambiguation-calling-methods-with-the-same-name"></a>
<a id="disambiguating-between-methods-with-the-same-name"></a>

### Zwischen gleichnamigen Methoden unterscheiden {#disambiguating-between-identically-named-methods}

Nichts in Rust hindert einen Trait daran, eine Methode mit demselben Namen wie
eine Methode eines anderen Traits zu haben, und Rust hindert dich auch nicht
daran, beide Traits für einen Typ zu implementieren. Es ist auch möglich, direkt
auf dem Typ eine Methode mit demselben Namen wie Methoden aus Traits zu
implementieren.

Wenn du gleichnamige Methoden aufrufst, musst du Rust mitteilen, welche du
verwenden willst. Betrachte den Code in Listing 20-17, in dem wir zwei Traits
definiert haben, `Pilot` und `Wizard`, die beide eine Methode namens `fly`
haben. Dann implementieren wir beide Traits für einen Typ `Human`, auf dem
bereits eine Methode namens `fly` implementiert ist. Jede Methode `fly` tut
etwas anderes.

<Listing number="20-17" file-name="src/main.rs" caption="Zwei Traits werden mit einer Methode `fly` definiert und für den Typ `Human` implementiert, und eine Methode `fly` wird direkt auf `Human` implementiert.">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-17/src/main.rs:here}}
```

</Listing>

Wenn wir `fly` auf einer Instanz von `Human` aufrufen, ruft der Compiler
standardmäßig die Methode auf, die direkt auf dem Typ implementiert ist, wie in
Listing 20-18 gezeigt.

<Listing number="20-18" file-name="src/main.rs" caption="`fly` auf einer Instanz von `Human` aufrufen">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-18/src/main.rs:here}}
```

</Listing>

Wenn du diesen Code ausführst, wird `*waving arms furiously*` ausgegeben, was
zeigt, dass Rust die Methode `fly` aufgerufen hat, die direkt auf `Human`
implementiert ist.

Um die Methoden `fly` aus dem Trait `Pilot` oder dem Trait `Wizard` aufzurufen,
müssen wir eine explizitere Syntax verwenden, um anzugeben, welche Methode `fly`
wir meinen. Listing 20-19 zeigt diese Syntax.

<Listing number="20-19" file-name="src/main.rs" caption="Angeben, welche Methode `fly` welches Traits wir aufrufen wollen">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-19/src/main.rs:here}}
```

</Listing>

Wenn wir den Namen des Traits vor dem Methodennamen angeben, ist für Rust klar,
welche Implementierung von `fly` wir aufrufen wollen. Wir könnten auch
`Human::fly(&person)` schreiben, was dem `person.fly()` entspricht, das wir in
Listing 20-19 verwendet haben, aber das ist etwas länger zu schreiben, wenn wir
nicht unterscheiden müssen.

Wenn du diesen Code ausführst, wird Folgendes ausgegeben:

```console
{{#include ../listings/ch20-advanced-features/listing-20-19/output.txt}}
```

Weil die Methode `fly` einen Parameter `self` nimmt, könnte Rust, wenn wir zwei
_Typen_ hätten, die beide einen _Trait_ implementieren, anhand des Typs von
`self` herausfinden, welche Implementierung eines Traits verwendet werden soll.

Assoziierte Funktionen, die keine Methoden sind, haben jedoch keinen Parameter
`self`. Wenn es mehrere Typen oder Traits gibt, die Nicht-Methoden-Funktionen
mit demselben Funktionsnamen definieren, weiß Rust nicht immer, welchen Typ du
meinst, es sei denn, du verwendest die vollständig qualifizierte Syntax (_fully
qualified syntax_). In Listing 20-20 erstellen wir zum Beispiel einen Trait für
ein Tierheim, das alle Hundewelpen Spot nennen möchte. Wir erstellen einen Trait
`Animal` mit einer assoziierten Nicht-Methoden-Funktion `baby_name`. Der Trait
`Animal` ist für das Struct `Dog` implementiert, auf dem wir außerdem direkt
eine assoziierte Nicht-Methoden-Funktion `baby_name` bereitstellen.

<Listing number="20-20" file-name="src/main.rs" caption="Ein Trait mit einer assoziierten Funktion und ein Typ mit einer gleichnamigen assoziierten Funktion, der den Trait ebenfalls implementiert">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-20/src/main.rs}}
```

</Listing>

Den Code, der alle Welpen Spot nennt, implementieren wir in der assoziierten
Funktion `baby_name`, die auf `Dog` definiert ist. Der Typ `Dog` implementiert
außerdem den Trait `Animal`, der Merkmale beschreibt, die alle Tiere haben.
Hundebabys heißen Welpen (_puppies_), und das wird in der Implementierung des
Traits `Animal` für `Dog` in der Funktion `baby_name` ausgedrückt, die zum Trait
`Animal` gehört.

In `main` rufen wir die Funktion `Dog::baby_name` auf, die die direkt auf `Dog`
definierte assoziierte Funktion aufruft. Dieser Code gibt Folgendes aus:

```console
{{#include ../listings/ch20-advanced-features/listing-20-20/output.txt}}
```

Diese Ausgabe ist nicht das, was wir wollten. Wir wollen die Funktion
`baby_name` aufrufen, die Teil des Traits `Animal` ist, den wir für `Dog`
implementiert haben, sodass der Code `A baby dog is called a puppy` ausgibt. Die
Technik, den Namen des Traits anzugeben, die wir in Listing 20-19 verwendet
haben, hilft hier nicht; wenn wir `main` in den Code von Listing 20-21 ändern,
bekommen wir einen Kompilierfehler.

<Listing number="20-21" file-name="src/main.rs" caption="Versuch, die Funktion `baby_name` aus dem Trait `Animal` aufzurufen, wobei Rust nicht weiß, welche Implementierung es verwenden soll">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-21/src/main.rs:here}}
```

</Listing>

Weil `Animal::baby_name` keinen Parameter `self` hat und es andere Typen geben
könnte, die den Trait `Animal` implementieren, kann Rust nicht herausfinden,
welche Implementierung von `Animal::baby_name` wir wollen. Wir bekommen diesen
Compilerfehler:

```console
{{#include ../listings/ch20-advanced-features/listing-20-21/output.txt}}
```

Um eindeutig zu machen und Rust mitzuteilen, dass wir die Implementierung von
`Animal` für `Dog` verwenden wollen und nicht die Implementierung von `Animal`
für einen anderen Typ, müssen wir die vollständig qualifizierte Syntax
verwenden. Listing 20-22 zeigt, wie man die vollständig qualifizierte Syntax
verwendet.

<Listing number="20-22" file-name="src/main.rs" caption="Mit vollständig qualifizierter Syntax angeben, dass wir die Funktion `baby_name` aus dem Trait `Animal` in ihrer Implementierung für `Dog` aufrufen wollen">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-22/src/main.rs:here}}
```

</Listing>

Wir geben Rust innerhalb der spitzen Klammern eine Typannotation, die angibt,
dass wir die Methode `baby_name` aus dem Trait `Animal` in ihrer Implementierung
für `Dog` aufrufen wollen, indem wir sagen, dass wir den Typ `Dog` für diesen
Funktionsaufruf als `Animal` behandeln wollen. Dieser Code gibt jetzt aus, was
wir wollen:

```console
{{#include ../listings/ch20-advanced-features/listing-20-22/output.txt}}
```

Im Allgemeinen ist die vollständig qualifizierte Syntax wie folgt definiert:

```rust,ignore
<Type as Trait>::function(receiver_if_method, next_arg, ...);
```

Bei assoziierten Funktionen, die keine Methoden sind, gäbe es keinen `receiver`:
Es gäbe nur die Liste der anderen Argumente. Du könntest die vollständig
qualifizierte Syntax überall dort verwenden, wo du Funktionen oder Methoden
aufrufst. Du darfst jedoch jeden Teil dieser Syntax weglassen, den Rust aus
anderen Informationen im Programm herausfinden kann. Diese ausführlichere Syntax
musst du nur in Fällen verwenden, in denen es mehrere Implementierungen mit
demselben Namen gibt und Rust Hilfe braucht, um zu erkennen, welche
Implementierung du aufrufen willst.

<!-- Old headings. Do not remove or links may break. -->

<a id="using-supertraits-to-require-one-traits-functionality-within-another-trait"></a>

### Supertraits verwenden {#using-supertraits}

Manchmal schreibst du vielleicht eine Trait-Definition, die von einem anderen
Trait abhängt: Damit ein Typ den ersten Trait implementieren kann, willst du
verlangen, dass dieser Typ auch den zweiten Trait implementiert. Das würdest du
tun, damit deine Trait-Definition die assoziierten Elemente des zweiten Traits
nutzen kann. Der Trait, auf den sich deine Trait-Definition stützt, heißt
_Supertrait_ deines Traits.

Angenommen, wir wollen zum Beispiel einen Trait `OutlinePrint` mit einer Methode
`outline_print` erstellen, die einen gegebenen Wert so formatiert ausgibt, dass
er von Sternchen eingerahmt ist. Das heißt, bei einem Struct `Point`, das den
Standardbibliotheks-Trait `Display` so implementiert, dass `(x, y)` herauskommt,
soll beim Aufruf von `outline_print` auf einer `Point`-Instanz mit `1` für `x`
und `3` für `y` Folgendes ausgegeben werden:

```text
**********
*        *
* (1, 3) *
*        *
**********
```

In der Implementierung der Methode `outline_print` wollen wir die Funktionalität
des Traits `Display` verwenden. Daher müssen wir angeben, dass der Trait
`OutlinePrint` nur für Typen funktioniert, die auch `Display` implementieren und
die Funktionalität bereitstellen, die `OutlinePrint` braucht. Das können wir in
der Trait-Definition tun, indem wir `OutlinePrint: Display` angeben. Diese
Technik ähnelt dem Hinzufügen eines Trait-Bounds zum Trait. Listing 20-23 zeigt
eine Implementierung des Traits `OutlinePrint`.

<Listing number="20-23" file-name="src/main.rs" caption="Den Trait `OutlinePrint` implementieren, der die Funktionalität von `Display` voraussetzt">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-23/src/main.rs:here}}
```

</Listing>

Weil wir angegeben haben, dass `OutlinePrint` den Trait `Display` voraussetzt,
können wir die Funktion `to_string` verwenden, die automatisch für jeden Typ
implementiert ist, der `Display` implementiert. Würden wir versuchen,
`to_string` zu verwenden, ohne nach dem Traitnamen einen Doppelpunkt und den
Trait `Display` anzugeben, bekämen wir einen Fehler, der besagt, dass für den
Typ `&Self` im aktuellen Gültigkeitsbereich (_scope_) keine Methode namens
`to_string` gefunden wurde.

Sehen wir uns an, was passiert, wenn wir versuchen, `OutlinePrint` für einen Typ
zu implementieren, der `Display` nicht implementiert, etwa das Struct `Point`:

<Listing file-name="src/main.rs">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-02-impl-outlineprint-for-point/src/main.rs:here}}
```

</Listing>

Wir bekommen einen Fehler, der besagt, dass `Display` erforderlich, aber nicht
implementiert ist:

```console
{{#include ../listings/ch20-advanced-features/no-listing-02-impl-outlineprint-for-point/output.txt}}
```

Um das zu beheben, implementieren wir `Display` für `Point` und erfüllen so die
Einschränkung, die `OutlinePrint` verlangt:

<Listing file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-03-impl-display-for-point/src/main.rs:here}}
```

</Listing>

Dann kompiliert die Implementierung des Traits `OutlinePrint` für `Point`
erfolgreich, und wir können `outline_print` auf einer `Point`-Instanz aufrufen,
um sie innerhalb eines Rahmens aus Sternchen anzuzeigen.

<!-- Old headings. Do not remove or links may break. -->

<a id="using-the-newtype-pattern-to-implement-external-traits-on-external-types"></a>
<a id="using-the-newtype-pattern-to-implement-external-traits"></a>

### Externe Traits mit dem Newtype-Pattern implementieren {#implementing-external-traits-with-the-newtype-pattern}

Im Abschnitt
[„Einen Trait für einen Typ implementieren“][implementing-a-trait-on-a-type]<!--
ignore --> in Kapitel 10 haben wir die Orphan-Rule erwähnt, die besagt, dass wir
einen Trait für einen Typ nur implementieren dürfen, wenn entweder der Trait
oder der Typ oder beide lokal in unserem Crate sind. Diese Einschränkung lässt
sich mit dem Newtype-Pattern umgehen, bei dem man in einem Tupel-Struct einen
neuen Typ erzeugt. (Tupel-Structs haben wir im Abschnitt
[„Verschiedene Typen mit Tupel-Structs erzeugen“][tuple-structs]<!-- ignore -->
in Kapitel 5 behandelt.) Das Tupel-Struct hat ein Feld und ist eine dünne Hülle
um den Typ, für den wir einen Trait implementieren wollen. Dann ist der
Wrapper-Typ lokal in unserem Crate, und wir können den Trait für den Wrapper
implementieren. _Newtype_ ist ein Begriff, der aus der Programmiersprache
Haskell stammt. Die Verwendung dieses Patterns kostet zur Laufzeit keine
Performance, und der Wrapper-Typ wird zur Kompilierzeit entfernt.

Angenommen, wir wollen als Beispiel `Display` für `Vec<T>` implementieren, was
uns die Orphan-Rule direkt verbietet, weil der Trait `Display` und der Typ
`Vec<T>` außerhalb unseres Crates definiert sind. Wir können ein Struct
`Wrapper` erstellen, das eine Instanz von `Vec<T>` enthält; dann können wir
`Display` für `Wrapper` implementieren und den Wert `Vec<T>` verwenden, wie in
Listing 20-24 gezeigt.

<Listing number="20-24" file-name="src/main.rs" caption="Einen Typ `Wrapper` um `Vec<String>` erstellen, um `Display` zu implementieren">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-24/src/main.rs}}
```

</Listing>

Die Implementierung von `Display` verwendet `self.0`, um auf den inneren
`Vec<T>` zuzugreifen, weil `Wrapper` ein Tupel-Struct ist und `Vec<T>` das
Element mit dem Index 0 im Tupel ist. Dann können wir die Funktionalität des
Traits `Display` für `Wrapper` verwenden.

Der Nachteil dieser Technik ist, dass `Wrapper` ein neuer Typ ist und daher die
Methoden des Werts, den er enthält, nicht hat. Wir müssten alle Methoden von
`Vec<T>` direkt auf `Wrapper` implementieren, sodass die Methoden an `self.0`
delegieren, wodurch wir `Wrapper` genau wie einen `Vec<T>` behandeln könnten.
Wenn wir wollten, dass der neue Typ jede Methode hat, die der innere Typ hat,
wäre es eine Lösung, den Trait `Deref` für `Wrapper` so zu implementieren, dass
er den inneren Typ zurückgibt (wie man den Trait `Deref` implementiert, haben
wir im Abschnitt
[„Smart-Pointer wie normale Referenzen
behandeln“][smart-pointer-deref]<!-- ignore --> in Kapitel 15 besprochen). Wenn
wir nicht wollten, dass der Typ `Wrapper` alle Methoden des inneren Typs hat –
etwa um das Verhalten des Typs `Wrapper` einzuschränken –, müssten wir nur die
Methoden, die wir tatsächlich wollen, manuell implementieren.

Dieses Newtype-Pattern ist auch dann nützlich, wenn keine Traits beteiligt sind.
Wechseln wir den Fokus und sehen uns einige fortgeschrittene Möglichkeiten an,
mit dem Typsystem von Rust zu interagieren.

{{#quiz ../quizzes/ch19-03-advanced-traits.toml}}

[newtype]: ch20-02-advanced-traits.html#implementing-external-traits-with-the-newtype-pattern
[implementing-a-trait-on-a-type]: ch10-02-traits.html#implementing-a-trait-on-a-type
[traits]: ch10-02-traits.html
[smart-pointer-deref]: ch15-02-deref.html#treating-smart-pointers-like-regular-references
[tuple-structs]: ch05-01-defining-structs.html#creating-different-types-with-tuple-structs
