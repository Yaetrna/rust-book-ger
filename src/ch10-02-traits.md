<!-- Old headings. Do not remove or links may break. -->

<a id="traits-defining-shared-behavior"></a>

## Gemeinsames Verhalten mit Traits definieren {#defining-shared-behavior-with-traits}

Ein _Trait_ definiert die Funktionalität, die ein bestimmter Typ hat und mit
anderen Typen teilen kann. Mit Traits können wir gemeinsames Verhalten auf
abstrakte Weise definieren. Mit _Trait-Bounds_ können wir festlegen, dass ein
generischer Typ jeder Typ sein kann, der ein bestimmtes Verhalten hat.

> Note: Traits ähneln einem Feature, das in anderen Sprachen oft _Interfaces_
> (Schnittstellen) heißt, wenn auch mit einigen Unterschieden.

### Einen Trait definieren {#defining-a-trait}

Das Verhalten eines Typs besteht aus den Methoden, die wir auf diesem Typ
aufrufen können. Verschiedene Typen teilen dasselbe Verhalten, wenn wir auf
allen diesen Typen dieselben Methoden aufrufen können. Trait-Definitionen sind
eine Möglichkeit, Methodensignaturen zu gruppieren, um eine Menge von
Verhaltensweisen zu definieren, die nötig sind, um einen bestimmten Zweck zu
erfüllen.

Angenommen, wir haben mehrere Structs, die verschiedene Arten und Mengen von
Text enthalten: ein Struct `NewsArticle`, das eine Nachrichtenmeldung von einem
bestimmten Ort enthält, und ein `SocialPost`, der höchstens 280 Zeichen haben
kann, dazu Metadaten, die angeben, ob es ein neuer Beitrag, eine Weiterleitung
oder eine Antwort auf einen anderen Beitrag war.

Wir wollen ein Library-Crate namens `aggregator` für einen Medienaggregator
erstellen, das Zusammenfassungen von Daten anzeigen kann, die in einer
`NewsArticle`- oder `SocialPost`-Instanz gespeichert sein können. Dafür brauchen
wir von jedem Typ eine Zusammenfassung, und diese fordern wir an, indem wir auf
einer Instanz eine Methode `summarize` aufrufen. Listing 10-12 zeigt die
Definition eines öffentlichen Traits `Summary`, der dieses Verhalten ausdrückt.

<Listing number="10-12" file-name="src/lib.rs" caption="Ein Trait `Summary`, der aus dem Verhalten besteht, das eine Methode `summarize` bereitstellt">

```rust,noplayground
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-12/src/lib.rs}}
```

</Listing>

Hier deklarieren wir einen Trait mit dem Schlüsselwort `trait`, gefolgt vom
Namen des Traits, in diesem Fall `Summary`. Außerdem deklarieren wir den Trait
als `pub`, damit auch Crates, die von diesem Crate abhängen, den Trait verwenden
können, wie wir in einigen Beispielen sehen werden. In den geschweiften Klammern
deklarieren wir die Methodensignaturen, die das Verhalten der Typen beschreiben,
die diesen Trait implementieren, in diesem Fall `fn summarize(&self) -> String`.

Nach der Methodensignatur setzen wir ein Semikolon, statt eine Implementierung
in geschweiften Klammern anzugeben. Jeder Typ, der diesen Trait implementiert,
muss für den Rumpf der Methode sein eigenes Verhalten bereitstellen. Der
Compiler stellt sicher, dass jeder Typ, der den Trait `Summary` hat, die Methode
`summarize` mit genau dieser Signatur definiert.

Ein Trait kann in seinem Rumpf mehrere Methoden haben: Die Methodensignaturen
stehen jeweils in einer eigenen Zeile, und jede Zeile endet mit einem Semikolon.

### Einen Trait für einen Typ implementieren {#implementing-a-trait-on-a-type}

Nachdem wir die gewünschten Signaturen der Methoden des Traits `Summary`
definiert haben, können wir ihn für die Typen in unserem Medienaggregator
implementieren. Listing 10-13 zeigt eine Implementierung des Traits `Summary`
für das Struct `NewsArticle`, die die Schlagzeile, den Autor und den Ort
verwendet, um den Rückgabewert von `summarize` zu erzeugen. Für das Struct
`SocialPost` definieren wir `summarize` als den Benutzernamen, gefolgt vom
gesamten Text des Beitrags, wobei wir annehmen, dass der Inhalt des Beitrags
bereits auf 280 Zeichen begrenzt ist.

<Listing number="10-13" file-name="src/lib.rs" caption="Den Trait `Summary` für die Typen `NewsArticle` und `SocialPost` implementieren">

```rust,noplayground
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-13/src/lib.rs:here}}
```

</Listing>

Einen Trait für einen Typ zu implementieren ähnelt dem Implementieren
gewöhnlicher Methoden. Der Unterschied ist, dass wir nach `impl` den Namen des
Traits angeben, den wir implementieren wollen, dann das Schlüsselwort `for`
verwenden und dann den Namen des Typs angeben, für den wir den Trait
implementieren wollen. Innerhalb des `impl`-Blocks stehen die
Methodensignaturen, die die Trait-Definition festgelegt hat. Statt nach jeder
Signatur ein Semikolon zu setzen, verwenden wir geschweifte Klammern und füllen
den Methodenrumpf mit dem konkreten Verhalten, das die Methoden des Traits für
diesen bestimmten Typ haben sollen.

Nachdem die Bibliothek den Trait `Summary` für `NewsArticle` und `SocialPost`
implementiert hat, können Nutzer des Crates die Trait-Methoden auf Instanzen von
`NewsArticle` und `SocialPost` genauso aufrufen wie gewöhnliche Methoden. Der
einzige Unterschied ist, dass der Nutzer neben den Typen auch den Trait in den
Gültigkeitsbereich (_scope_) bringen muss. Hier ist ein Beispiel dafür, wie ein
Binary-Crate unser Library-Crate `aggregator` verwenden könnte:

```rust,ignore
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-01-calling-trait-method/src/main.rs}}
```

Dieser Code gibt
`1 new post: horse_ebooks: of course, as you probably already
know, people` aus.

Andere Crates, die vom Crate `aggregator` abhängen, können den Trait `Summary`
ebenfalls in den Gültigkeitsbereich bringen, um `Summary` für ihre eigenen Typen
zu implementieren. Eine Einschränkung ist zu beachten: Wir können einen Trait
für einen Typ nur implementieren, wenn entweder der Trait oder der Typ oder
beide lokal in unserem Crate definiert sind. Wir können zum Beispiel Traits der
Standardbibliothek wie `Display` für einen eigenen Typ wie `SocialPost` als Teil
der Funktionalität unseres Crates `aggregator` implementieren, weil der Typ
`SocialPost` lokal in unserem Crate `aggregator` definiert ist. Wir können in
unserem Crate `aggregator` auch `Summary` für `Vec<T>` implementieren, weil der
Trait `Summary` lokal in unserem Crate `aggregator` definiert ist.

Externe Traits können wir aber nicht für externe Typen implementieren. Wir
können zum Beispiel den Trait `Display` nicht in unserem Crate `aggregator` für
`Vec<T>` implementieren, weil `Display` und `Vec<T>` beide in der
Standardbibliothek definiert und nicht lokal in unserem Crate `aggregator` sind.
Diese Einschränkung ist Teil eines Prinzips namens _Kohärenz_ (_coherence_),
genauer gesagt der _Orphan-Rule_ (Waisenregel), die so heißt, weil der Elterntyp
nicht vorhanden ist. Diese Regel stellt sicher, dass der Code anderer Leute
deinen Code nicht kaputtmachen kann und umgekehrt. Ohne die Regel könnten zwei
Crates denselben Trait für denselben Typ implementieren, und Rust wüsste nicht,
welche Implementierung es verwenden soll.

<!-- Old headings. Do not remove or links may break. -->

<a id="default-implementations"></a>

### Standardimplementierungen verwenden {#using-default-implementations}

Manchmal ist es nützlich, für einige oder alle Methoden eines Traits ein
Standardverhalten zu haben, statt für jeden Typ Implementierungen aller Methoden
zu verlangen. Wenn wir den Trait dann für einen bestimmten Typ implementieren,
können wir das Standardverhalten jeder Methode beibehalten oder überschreiben.

In Listing 10-14 geben wir für die Methode `summarize` des Traits `Summary`
einen Standard-String an, statt nur die Methodensignatur zu definieren wie in
Listing 10-12.

<Listing number="10-14" file-name="src/lib.rs" caption="Einen Trait `Summary` mit einer Standardimplementierung der Methode `summarize` definieren">

```rust,noplayground
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-14/src/lib.rs:here}}
```

</Listing>

Um Instanzen von `NewsArticle` mit einer Standardimplementierung
zusammenzufassen, geben wir einen leeren `impl`-Block mit
`impl Summary for NewsArticle {}` an.

Obwohl wir die Methode `summarize` nicht mehr direkt auf `NewsArticle`
definieren, haben wir eine Standardimplementierung bereitgestellt und
festgelegt, dass `NewsArticle` den Trait `Summary` implementiert. Daher können
wir die Methode `summarize` weiterhin auf einer Instanz von `NewsArticle`
aufrufen, etwa so:

```rust,ignore
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-02-calling-default-impl/src/main.rs:here}}
```

Dieser Code gibt `New article available! (Read more...)` aus.

Eine Standardimplementierung zu erstellen, erfordert keine Änderung an der
Implementierung von `Summary` für `SocialPost` in Listing 10-13. Der Grund ist,
dass die Syntax zum Überschreiben einer Standardimplementierung dieselbe ist wie
die Syntax zum Implementieren einer Trait-Methode, die keine
Standardimplementierung hat.

Standardimplementierungen können andere Methoden desselben Traits aufrufen, auch
wenn diese anderen Methoden keine Standardimplementierung haben. Auf diese Weise
kann ein Trait viel nützliche Funktionalität bereitstellen und von den
Implementierern nur verlangen, einen kleinen Teil davon anzugeben. Wir könnten
zum Beispiel den Trait `Summary` so definieren, dass er eine Methode
`summarize_author` hat, deren Implementierung verlangt wird, und dann eine
Methode `summarize` mit einer Standardimplementierung definieren, die die
Methode `summarize_author` aufruft:

```rust,noplayground
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-03-default-impl-calls-other-methods/src/lib.rs:here}}
```

Um diese Version von `Summary` zu verwenden, müssen wir nur `summarize_author`
definieren, wenn wir den Trait für einen Typ implementieren:

```rust,ignore
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-03-default-impl-calls-other-methods/src/lib.rs:impl}}
```

Nachdem wir `summarize_author` definiert haben, können wir `summarize` auf
Instanzen des Structs `SocialPost` aufrufen, und die Standardimplementierung von
`summarize` ruft die Definition von `summarize_author` auf, die wir
bereitgestellt haben. Da wir `summarize_author` implementiert haben, hat uns der
Trait `Summary` das Verhalten der Methode `summarize` gegeben, ohne dass wir
weiteren Code schreiben mussten. So sieht das aus:

```rust,ignore
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-03-default-impl-calls-other-methods/src/main.rs:here}}
```

Dieser Code gibt `1 new post: (Read more from @horse_ebooks...)` aus.

Beachte, dass es nicht möglich ist, die Standardimplementierung aus einer
überschreibenden Implementierung derselben Methode heraus aufzurufen.

{{#quiz ../quizzes/ch10-02-traits-sec1.toml}}

<!-- Old headings. Do not remove or links may break. -->

<a id="traits-as-parameters"></a>

### Traits als Parameter verwenden {#using-traits-as-parameters}

Nachdem du weißt, wie man Traits definiert und implementiert, können wir uns
ansehen, wie man mit Traits Funktionen definiert, die viele verschiedene Typen
akzeptieren. Wir verwenden den Trait `Summary`, den wir in Listing 10-13 für die
Typen `NewsArticle` und `SocialPost` implementiert haben, um eine Funktion
`notify` zu definieren, die die Methode `summarize` auf ihrem Parameter `item`
aufruft, der von einem Typ ist, der den Trait `Summary` implementiert. Dafür
verwenden wir die Syntax `impl Trait`, etwa so:

```rust,ignore
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-04-traits-as-parameters/src/lib.rs:here}}
```

Statt eines konkreten Typs für den Parameter `item` geben wir das Schlüsselwort
`impl` und den Namen des Traits an. Dieser Parameter akzeptiert jeden Typ, der
den angegebenen Trait implementiert. Im Rumpf von `notify` können wir auf `item`
alle Methoden aufrufen, die aus dem Trait `Summary` stammen, etwa `summarize`.
Wir können `notify` aufrufen und jede Instanz von `NewsArticle` oder
`SocialPost` übergeben. Code, der die Funktion mit einem anderen Typ aufruft,
etwa einem `String` oder einem `i32`, kompiliert nicht, weil diese Typen
`Summary` nicht implementieren.

<!-- Old headings. Do not remove or links may break. -->

<a id="fixing-the-largest-function-with-trait-bounds"></a>

#### Syntax für Trait-Bounds {#trait-bound-syntax}

Die Syntax `impl Trait` funktioniert für einfache Fälle, ist aber eigentlich
syntaktischer Zucker für eine längere Form, die man _Trait-Bound_ nennt; sie
sieht so aus:

```rust,ignore
pub fn notify<T: Summary>(item: &T) {
    println!("Breaking news! {}", item.summarize());
}
```

Diese längere Form ist gleichwertig zum Beispiel im vorherigen Abschnitt, aber
umständlicher. Wir setzen Trait-Bounds hinter einem Doppelpunkt zur Deklaration
des generischen Typparameters in die spitzen Klammern.

Die Syntax `impl Trait` ist praktisch und sorgt in einfachen Fällen für
knapperen Code, während die vollständigere Trait-Bound-Syntax in anderen Fällen
mehr Komplexität ausdrücken kann. Wir könnten zum Beispiel zwei Parameter haben,
die `Summary` implementieren. Mit der Syntax `impl Trait` sieht das so aus:

```rust,ignore
pub fn notify(item1: &impl Summary, item2: &impl Summary) {
```

`impl Trait` ist angemessen, wenn diese Funktion zulassen soll, dass `item1` und
`item2` unterschiedliche Typen haben (solange beide Typen `Summary`
implementieren). Wollen wir dagegen erzwingen, dass beide Parameter denselben
Typ haben, müssen wir einen Trait-Bound verwenden, etwa so:

```rust,ignore
pub fn notify<T: Summary>(item1: &T, item2: &T) {
```

Der generische Typ `T`, der als Typ der Parameter `item1` und `item2` angegeben
ist, schränkt die Funktion so ein, dass der konkrete Typ der Werte, die als
Argumente für `item1` und `item2` übergeben werden, derselbe sein muss.

<!-- Old headings. Do not remove or links may break. -->

<a id="specifying-multiple-trait-bounds-with-the--syntax"></a>

#### Mehrere Trait-Bounds mit der Syntax `+` {#multiple-trait-bounds-with-the--syntax}

Wir können auch mehr als einen Trait-Bound angeben. Angenommen, `notify` soll
auf `item` sowohl die Display-Formatierung als auch `summarize` verwenden: Dann
geben wir in der Definition von `notify` an, dass `item` sowohl `Display` als
auch `Summary` implementieren muss. Das geht mit der Syntax `+`:

```rust,ignore
pub fn notify(item: &(impl Summary + Display)) {
```

Die Syntax `+` ist auch bei Trait-Bounds für generische Typen gültig:

```rust,ignore
pub fn notify<T: Summary + Display>(item: &T) {
```

Mit den beiden angegebenen Trait-Bounds kann der Rumpf von `notify` `summarize`
aufrufen und `item` mit `{}` formatieren.

#### Übersichtlichere Trait-Bounds mit `where`-Klauseln {#clearer-trait-bounds-with-where-clauses}

Zu viele Trait-Bounds haben ihre Nachteile. Jeder generische Typ hat seine
eigenen Trait-Bounds, daher können Funktionen mit mehreren generischen
Typparametern zwischen dem Funktionsnamen und der Parameterliste viele
Informationen über Trait-Bounds enthalten, was die Funktionssignatur schwer
lesbar macht. Deshalb hat Rust eine alternative Syntax, mit der man Trait-Bounds
in einer `where`-Klausel nach der Funktionssignatur angibt. Statt also das hier
zu schreiben:

```rust,ignore
fn some_function<T: Display + Clone, U: Clone + Debug>(t: &T, u: &U) -> i32 {
```

können wir eine `where`-Klausel verwenden, etwa so:

```rust,ignore
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-07-where-clause/src/lib.rs:here}}
```

Die Signatur dieser Funktion ist weniger überladen: Funktionsname,
Parameterliste und Rückgabetyp stehen nah beieinander, ähnlich wie bei einer
Funktion ohne viele Trait-Bounds.

### Typen zurückgeben, die Traits implementieren {#returning-types-that-implement-traits}

Wir können die Syntax `impl Trait` auch an der Rückgabeposition verwenden, um
einen Wert eines Typs zurückzugeben, der einen Trait implementiert, wie hier
gezeigt:

```rust,ignore
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-05-returning-impl-trait/src/lib.rs:here}}
```

Indem wir `impl Summary` als Rückgabetyp verwenden, legen wir fest, dass die
Funktion `returns_summarizable` einen Typ zurückgibt, der den Trait `Summary`
implementiert, ohne den konkreten Typ zu nennen. In diesem Fall gibt
`returns_summarizable` einen `SocialPost` zurück, aber der Code, der diese
Funktion aufruft, muss das nicht wissen.

Einen Rückgabetyp nur über den Trait anzugeben, den er implementiert, ist
besonders im Zusammenhang mit Closures und Iteratoren nützlich, die wir in
Kapitel 13 behandeln. Closures und Iteratoren erzeugen Typen, die nur der
Compiler kennt, oder Typen, die sehr lang anzugeben sind. Mit der Syntax
`impl Trait` kannst du knapp angeben, dass eine Funktion einen Typ zurückgibt,
der den Trait `Iterator` implementiert, ohne einen sehr langen Typ ausschreiben
zu müssen.

Du kannst `impl Trait` allerdings nur verwenden, wenn du einen einzigen Typ
zurückgibst. Dieser Code zum Beispiel, der entweder einen `NewsArticle` oder
einen `SocialPost` zurückgibt und dessen Rückgabetyp als `impl Summary`
angegeben ist, würde nicht funktionieren:

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-06-impl-trait-returns-one-type/src/lib.rs:here}}
```

Entweder einen `NewsArticle` oder einen `SocialPost` zurückzugeben, ist wegen
Einschränkungen bei der Implementierung der Syntax `impl Trait` im Compiler
nicht erlaubt. Wie man eine Funktion mit diesem Verhalten schreibt, behandeln
wir im Abschnitt
[„Mit Trait-Objekten über gemeinsames Verhalten abstrahieren“][trait-objects]<!-- ignore -->
in Kapitel 18.

### Mit Trait-Bounds Methoden bedingt implementieren {#using-trait-bounds-to-conditionally-implement-methods}

Mit einem Trait-Bound an einem `impl`-Block, der generische Typparameter
verwendet, können wir Methoden bedingt für Typen implementieren, die die
angegebenen Traits implementieren. Der Typ `Pair<T>` in Listing 10-15
implementiert zum Beispiel immer die Funktion `new`, die eine neue Instanz von
`Pair<T>` zurückgibt (erinnere dich aus dem Abschnitt
[„Methodensyntax“][methods]<!-- ignore --> in Kapitel 5, dass `Self` ein
Typalias für den Typ des `impl`-Blocks ist, in diesem Fall `Pair<T>`). Im
nächsten `impl`-Block implementiert `Pair<T>` die Methode `cmp_display` aber
nur, wenn sein innerer Typ `T` den Trait `PartialOrd` implementiert, der
Vergleiche ermöglicht, _und_ den Trait `Display`, der die Ausgabe ermöglicht.

<Listing number="10-15" file-name="src/lib.rs" caption="Methoden auf einem generischen Typ abhängig von Trait-Bounds bedingt implementieren">

```rust,noplayground
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-15/src/lib.rs}}
```

</Listing>

Wir können einen Trait auch bedingt für jeden Typ implementieren, der einen
anderen Trait implementiert. Implementierungen eines Traits für jeden Typ, der
die Trait-Bounds erfüllt, heißen _Blanket-Implementierungen_ (_blanket
implementations_) und werden in der Standardbibliothek von Rust ausgiebig
verwendet. Die Standardbibliothek implementiert zum Beispiel den Trait
`ToString` für jeden Typ, der den Trait `Display` implementiert. Der
`impl`-Block in der Standardbibliothek sieht ähnlich aus wie dieser Code:

```rust,ignore
impl<T: Display> ToString for T {
    // --snip--
}
```

Da die Standardbibliothek diese Blanket-Implementierung hat, können wir die vom
Trait `ToString` definierte Methode `to_string` auf jedem Typ aufrufen, der den
Trait `Display` implementiert. Wir können zum Beispiel Ganzzahlen so in ihre
entsprechenden `String`-Werte umwandeln, weil Ganzzahlen `Display`
implementieren:

```rust
let s = 3.to_string();
```

Blanket-Implementierungen erscheinen in der Dokumentation des Traits im
Abschnitt „Implementors“.

Mit Traits und Trait-Bounds können wir Code schreiben, der generische
Typparameter verwendet, um Duplizierung zu verringern, und dem Compiler trotzdem
mitteilen, dass der generische Typ ein bestimmtes Verhalten haben soll. Der
Compiler kann dann mithilfe der Informationen aus den Trait-Bounds prüfen, ob
alle konkreten Typen, die mit unserem Code verwendet werden, das richtige
Verhalten bereitstellen. In dynamisch typisierten Sprachen würden wir einen
Fehler zur Laufzeit bekommen, wenn wir auf einem Typ eine Methode aufrufen, die
der Typ nicht definiert. Rust verlagert diese Fehler aber in die Kompilierzeit,
sodass wir gezwungen sind, die Probleme zu beheben, bevor unser Code überhaupt
laufen kann. Außerdem müssen wir keinen Code schreiben, der das Verhalten zur
Laufzeit prüft, weil wir es bereits zur Kompilierzeit geprüft haben. Das
verbessert die Performance, ohne dass wir auf die Flexibilität von Generics
verzichten müssen.

{{#quiz ../quizzes/ch10-02-traits-sec2.toml}}

[trait-objects]: ch18-02-trait-objects.html#using-trait-objects-to-abstract-over-shared-behavior
[methods]: ch05-03-method-syntax.html#method-syntax
