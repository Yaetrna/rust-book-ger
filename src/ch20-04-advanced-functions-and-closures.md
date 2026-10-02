## Fortgeschrittene Funktionen und Closures {#advanced-functions-and-closures}

Dieser Abschnitt untersucht einige fortgeschrittene Features im Zusammenhang mit
Funktionen und Closures, darunter Funktionszeiger und das Zurückgeben von
Closures.

### Funktionszeiger {#function-pointers}

Wir haben darüber gesprochen, wie man Closures an Funktionen übergibt; du kannst
auch normale Funktionen an Funktionen übergeben! Diese Technik ist nützlich,
wenn du eine Funktion übergeben willst, die du bereits definiert hast, statt
eine neue Closure zu definieren. Funktionen werden in den Typ `fn` (mit kleinem
_f_) umgewandelt, nicht zu verwechseln mit dem Closure-Trait `Fn`. Der Typ `fn`
heißt _Funktionszeiger_ (_function pointer_). Durch die Übergabe von Funktionen
mit Funktionszeigern kannst du Funktionen als Argumente anderer Funktionen
verwenden.

Die Syntax, um anzugeben, dass ein Parameter ein Funktionszeiger ist, ähnelt der
von Closures, wie in Listing 20-28 gezeigt, wo wir eine Funktion `add_one`
definiert haben, die zu ihrem Parameter 1 addiert. Die Funktion `do_twice` nimmt
zwei Parameter: einen Funktionszeiger auf eine beliebige Funktion, die einen
Parameter vom Typ `i32` nimmt und ein `i32` zurückgibt, und einen `i32`-Wert.
Die Funktion `do_twice` ruft die Funktion `f` zweimal auf, übergibt ihr jeweils
den Wert `arg` und addiert dann die Ergebnisse der beiden Funktionsaufrufe. Die
Funktion `main` ruft `do_twice` mit den Argumenten `add_one` und `5` auf.

<Listing number="20-28" file-name="src/main.rs" caption="Den Typ `fn` verwenden, um einen Funktionszeiger als Argument entgegenzunehmen">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-28/src/main.rs}}
```

</Listing>

Dieser Code gibt `The answer is: 12` aus. Wir geben an, dass der Parameter `f`
in `do_twice` ein `fn` ist, das einen Parameter vom Typ `i32` nimmt und ein
`i32` zurückgibt. Dann können wir `f` im Rumpf von `do_twice` aufrufen. In
`main` können wir den Funktionsnamen `add_one` als erstes Argument an `do_twice`
übergeben.

Anders als Closures ist `fn` ein Typ und kein Trait, daher geben wir `fn` direkt
als Parametertyp an, statt einen generischen Typparameter mit einem der
`Fn`-Traits als Trait-Bound zu deklarieren.

Funktionszeiger implementieren alle drei Closure-Traits (`Fn`, `FnMut` und
`FnOnce`), sodass du einen Funktionszeiger immer als Argument an eine Funktion
übergeben kannst, die eine Closure erwartet. Am besten schreibst du Funktionen
mit einem generischen Typ und einem der Closure-Traits, damit deine Funktionen
sowohl Funktionen als auch Closures akzeptieren können.

Ein Beispiel dafür, wann du nur `fn` und keine Closures akzeptieren möchtest,
ist jedoch die Interaktion mit externem Code, der keine Closures hat:
C-Funktionen können Funktionen als Argumente akzeptieren, aber C hat keine
Closures.

Als Beispiel dafür, wo du entweder eine inline definierte Closure oder eine
benannte Funktion verwenden könntest, sehen wir uns eine Verwendung der Methode
`map` an, die der Trait `Iterator` in der Standardbibliothek bereitstellt. Um
mit der Methode `map` einen Vektor von Zahlen in einen Vektor von Strings
umzuwandeln, könnten wir eine Closure verwenden, wie in Listing 20-29.

<Listing number="20-29" caption="Eine Closure mit der Methode `map` verwenden, um Zahlen in Strings umzuwandeln">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-29/src/main.rs:here}}
```

</Listing>

Oder wir könnten statt der Closure eine Funktion als Argument an `map` angeben.
Listing 20-30 zeigt, wie das aussehen würde.

<Listing number="20-30" caption="Die Funktion `String::to_string` mit der Methode `map` verwenden, um Zahlen in Strings umzuwandeln">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-30/src/main.rs:here}}
```

</Listing>

Beachte, dass wir die vollständig qualifizierte Syntax verwenden müssen, über
die wir im Abschnitt [„Fortgeschrittene Traits“][advanced-traits]<!-- ignore -->
gesprochen haben, weil es mehrere Funktionen namens `to_string` gibt.

Hier verwenden wir die Funktion `to_string`, die im Trait `ToString` definiert
ist und die die Standardbibliothek für jeden Typ implementiert hat, der
`Display` implementiert.

Erinnere dich aus dem Abschnitt [„Enum-Werte“][enum-values]<!-- ignore --> in
Kapitel 6, dass der Name jeder Enum-Variante, die wir definieren, auch zu einer
Initialisierungsfunktion wird. Wir können diese Initialisierungsfunktionen als
Funktionszeiger verwenden, die die Closure-Traits implementieren, sodass wir die
Initialisierungsfunktionen als Argumente für Methoden angeben können, die
Closures nehmen, wie in Listing 20-31 zu sehen.

<Listing number="20-31" caption="Einen Enum-Initialisierer mit der Methode `map` verwenden, um aus Zahlen eine `Status`-Instanz zu erzeugen">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-31/src/main.rs:here}}
```

</Listing>

Hier erzeugen wir mit der Initialisierungsfunktion von `Status::Value`
`Status::Value`-Instanzen aus jedem `u32`-Wert im Bereich, auf dem `map`
aufgerufen wird. Manche bevorzugen diesen Stil, andere verwenden lieber
Closures. Beide werden zum selben Code kompiliert, also verwende den Stil, der
für dich klarer ist.

### Closures zurückgeben {#returning-closures}

Closures werden durch Traits dargestellt, was bedeutet, dass du Closures nicht
direkt zurückgeben kannst. In den meisten Fällen, in denen du einen Trait
zurückgeben möchtest, kannst du stattdessen den konkreten Typ, der den Trait
implementiert, als Rückgabewert der Funktion verwenden. Mit Closures geht das
aber normalerweise nicht, weil sie keinen konkreten Typ haben, der sich
zurückgeben lässt; du darfst zum Beispiel den Funktionszeiger `fn` nicht als
Rückgabetyp verwenden, wenn die Closure Werte aus ihrem Gültigkeitsbereich
(_scope_) erfasst.

Stattdessen verwendest du normalerweise die Syntax `impl Trait`, die wir in
Kapitel 10 kennengelernt haben. Du kannst jeden Funktionstyp zurückgeben, indem
du `Fn`, `FnOnce` und `FnMut` verwendest. Der Code in Listing 20-32 kompiliert
zum Beispiel problemlos.

<Listing number="20-32" caption="Mit der Syntax `impl Trait` eine Closure aus einer Funktion zurückgeben">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-32/src/lib.rs}}
```

</Listing>

Wie wir jedoch im Abschnitt
[„Typen von Closures ableiten und annotieren“][closure-types]<!-- ignore --> in
Kapitel 13 angemerkt haben, ist jede Closure auch ein eigener, eigenständiger
Typ. Wenn du mit mehreren Funktionen arbeiten musst, die dieselbe Signatur, aber
unterschiedliche Implementierungen haben, musst du für sie ein Trait-Objekt
verwenden. Betrachte, was passiert, wenn du Code wie in Listing 20-33 schreibst.

<Listing file-name="src/main.rs" number="20-33" caption="Einen `Vec<T>` von Closures erstellen, die von Funktionen definiert werden, die `impl Fn`-Typen zurückgeben">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-33/src/main.rs}}
```

</Listing>

Hier haben wir zwei Funktionen, `returns_closure` und
`returns_initialized_closure`, die beide `impl Fn(i32) -> i32` zurückgeben.
Beachte, dass sich die Closures, die sie zurückgeben, unterscheiden, obwohl sie
denselben Typ implementieren. Wenn wir versuchen, das zu kompilieren, teilt uns
Rust mit, dass es nicht funktioniert:

```text
{{#include ../listings/ch20-advanced-features/listing-20-33/output.txt}}
```

Die Fehlermeldung sagt uns, dass Rust jedes Mal, wenn wir ein `impl Trait`
zurückgeben, einen eigenen _opaken Typ_ (_opaque type_) erzeugt, also einen Typ,
bei dem wir weder in die Details dessen hineinsehen können, was Rust für uns
konstruiert, noch den Typ erraten können, den Rust erzeugt, um ihn selbst zu
schreiben. Obwohl diese Funktionen also Closures zurückgeben, die denselben
Trait `Fn(i32) -> i32` implementieren, sind die opaken Typen, die Rust für jede
erzeugt, verschieden. (Das ähnelt der Art, wie Rust für verschiedene
async-Blöcke unterschiedliche konkrete Typen erzeugt, selbst wenn sie denselben
Ausgabetyp haben, wie wir im Abschnitt
[„Der Typ `Pin` und der Trait `Unpin`“][future-types]<!-- ignore --> in Kapitel
17 gesehen haben.) Eine Lösung für dieses Problem haben wir inzwischen schon
einige Male gesehen: Wir können ein Trait-Objekt verwenden, wie in Listing
20-34.

<Listing number="20-34" caption="Einen `Vec<T>` von Closures erstellen, die von Funktionen definiert werden, die `Box<dyn Fn>` zurückgeben, sodass sie denselben Typ haben">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-34/src/main.rs:here}}
```

</Listing>

Dieser Code kompiliert problemlos. Mehr über Trait-Objekte erfährst du im
Abschnitt
[„Mit Trait-Objekten über gemeinsames Verhalten
abstrahieren“][trait-objects]<!-- ignore --> in Kapitel 18.

Als Nächstes sehen wir uns Makros an!

{{#quiz ../quizzes/ch19-05-advanced-functions-and-closures.toml}}

[advanced-traits]: ch20-02-advanced-traits.html#advanced-traits
[enum-values]: ch06-01-defining-an-enum.html#enum-values
[closure-types]: ch13-01-closures.html#closure-type-inference-and-annotation
[future-types]: ch17-03-more-futures.html
[trait-objects]: ch18-02-trait-objects.html
