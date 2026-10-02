<!-- Old headings. Do not remove or links may break. -->

<a id="closures-anonymous-functions-that-can-capture-their-environment"></a>
<a id="closures-anonymous-functions-that-capture-their-environment"></a>

## Closures {#closures}

Closures in Rust sind anonyme Funktionen, die du in einer Variable speichern
oder anderen Funktionen als Argumente übergeben kannst. Du kannst die Closure an
einer Stelle erstellen und sie dann an anderer Stelle aufrufen, um sie in einem
anderen Kontext auszuwerten. Anders als Funktionen können Closures Werte aus dem
Gültigkeitsbereich (_scope_) erfassen, in dem sie definiert sind. Wir zeigen,
wie diese Features von Closures die Wiederverwendung von Code und die Anpassung
von Verhalten ermöglichen.

<!-- Old headings. Do not remove or links may break. -->

<a id="creating-an-abstraction-of-behavior-with-closures"></a>
<a id="refactoring-using-functions"></a>
<a id="refactoring-with-closures-to-store-code"></a>
<a id="capturing-the-environment-with-closures"></a>

### Die Umgebung erfassen {#capturing-the-environment}

Zuerst sehen wir uns an, wie wir mit Closures Werte aus der Umgebung, in der sie
definiert sind, zur späteren Verwendung erfassen (_capture_) können. Das
Szenario ist folgendes: Von Zeit zu Zeit verschenkt unsere T-Shirt-Firma als
Werbeaktion ein exklusives T-Shirt in limitierter Auflage an jemanden auf
unserer Mailingliste. Personen auf der Mailingliste können ihrem Profil optional
ihre Lieblingsfarbe hinzufügen. Hat die Person, die für ein kostenloses T-Shirt
ausgewählt wurde, ihre Lieblingsfarbe angegeben, bekommt sie ein T-Shirt in
dieser Farbe. Hat die Person keine Lieblingsfarbe angegeben, bekommt sie die
Farbe, von der die Firma gerade am meisten hat.

Es gibt viele Möglichkeiten, das zu implementieren. Für dieses Beispiel
verwenden wir ein Enum namens `ShirtColor` mit den Varianten `Red` und `Blue`
(der Einfachheit halber beschränken wir die Zahl der verfügbaren Farben). Den
Bestand der Firma stellen wir mit einem Struct `Inventory` dar, das ein Feld
namens `shirts` mit einem `Vec<ShirtColor>` hat, der die derzeit vorrätigen
T-Shirt-Farben darstellt. Die auf `Inventory` definierte Methode `giveaway`
erhält die optionale Farbvorliebe der Person, die das kostenlose T-Shirt
gewonnen hat, und gibt die T-Shirt-Farbe zurück, die die Person bekommt. Dieser
Aufbau ist in Listing 13-1 gezeigt.

<Listing number="13-1" file-name="src/main.rs" caption="Die Werbeaktion der T-Shirt-Firma">

```rust,noplayground
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-01/src/main.rs}}
```

</Listing>

Der in `main` definierte `store` hat für diese Aktion in limitierter Auflage
noch zwei blaue und ein rotes T-Shirt zu verteilen. Wir rufen die Methode
`giveaway` für einen Benutzer mit einer Vorliebe für ein rotes T-Shirt und für
einen Benutzer ohne Vorliebe auf.

Auch dieser Code ließe sich auf viele Arten implementieren. Um uns auf Closures
zu konzentrieren, haben wir uns hier an Konzepte gehalten, die du bereits
kennst, mit Ausnahme des Rumpfs der Methode `giveaway`, der eine Closure
verwendet. In der Methode `giveaway` erhalten wir die Vorliebe des Benutzers als
Parameter vom Typ `Option<ShirtColor>` und rufen auf `user_preference` die
Methode `unwrap_or_else` auf. Die
[Methode `unwrap_or_else` auf `Option<T>`][unwrap-or-else]<!-- ignore --> ist in
der Standardbibliothek definiert. Sie nimmt ein Argument: eine Closure ohne
Argumente, die einen Wert `T` zurückgibt (denselben Typ, der in der Variante
`Some` der `Option<T>` gespeichert ist, in diesem Fall `ShirtColor`). Ist die
`Option<T>` die Variante `Some`, gibt `unwrap_or_else` den Wert aus dem `Some`
zurück. Ist die `Option<T>` die Variante `None`, ruft `unwrap_or_else` die
Closure auf und gibt den Wert zurück, den die Closure zurückgibt.

Wir geben den Closure-Ausdruck `|| self.most_stocked()` als Argument an
`unwrap_or_else` an. Das ist eine Closure, die selbst keine Parameter nimmt
(hätte die Closure Parameter, stünden sie zwischen den beiden senkrechten
Strichen). Der Rumpf der Closure ruft `self.most_stocked()` auf. Wir definieren
die Closure hier, und die Implementierung von `unwrap_or_else` wertet die
Closure später aus, falls das Ergebnis gebraucht wird.

Dieser Code gibt Folgendes aus:

```console
{{#include ../listings/ch13-functional-features/listing-13-01/output.txt}}
```

Ein interessanter Aspekt dabei ist, dass wir eine Closure übergeben haben, die
`self.most_stocked()` auf der aktuellen `Inventory`-Instanz aufruft. Die
Standardbibliothek musste nichts über die von uns definierten Typen `Inventory`
oder `ShirtColor` wissen oder über die Logik, die wir in diesem Szenario
verwenden wollen. Die Closure erfasst eine unveränderliche (_immutable_)
Referenz auf die `Inventory`-Instanz `self` und übergibt sie zusammen mit dem
von uns angegebenen Code an die Methode `unwrap_or_else`. Funktionen dagegen
können ihre Umgebung nicht auf diese Weise erfassen.

<!-- Old headings. Do not remove or links may break. -->

<a id="closure-type-inference-and-annotation"></a>

### Typen von Closures ableiten und annotieren {#inferring-and-annotating-closure-types}

Es gibt weitere Unterschiede zwischen Funktionen und Closures. Bei Closures
musst du die Typen der Parameter oder des Rückgabewerts normalerweise nicht
annotieren, wie es bei `fn`-Funktionen nötig ist. Bei Funktionen sind
Typannotationen erforderlich, weil die Typen Teil einer expliziten Schnittstelle
sind, die deinen Nutzern offenliegt. Diese Schnittstelle streng festzulegen, ist
wichtig, damit alle sich einig sind, welche Typen von Werten eine Funktion
verwendet und zurückgibt. Closures dagegen werden nicht in einer solchen
offenliegenden Schnittstelle verwendet: Sie werden in Variablen gespeichert und
verwendet, ohne dass man sie benennt und den Nutzern unserer Bibliothek
offenlegt.

Closures sind typischerweise kurz und nur in einem engen Kontext relevant statt
in beliebigen Szenarien. Innerhalb dieser begrenzten Kontexte kann der Compiler
die Typen der Parameter und den Rückgabetyp ableiten, ähnlich wie er die Typen
der meisten Variablen ableiten kann (es gibt seltene Fälle, in denen der
Compiler auch bei Closures Typannotationen braucht).

Wie bei Variablen können wir Typannotationen hinzufügen, wenn wir die
Explizitheit und Klarheit erhöhen wollen, auf Kosten von mehr Ausführlichkeit
als unbedingt nötig. Die Typen einer Closure zu annotieren, sähe aus wie die
Definition in Listing 13-2. In diesem Beispiel definieren wir eine Closure und
speichern sie in einer Variable, statt die Closure an der Stelle zu definieren,
an der wir sie als Argument übergeben, wie in Listing 13-1.

<Listing number="13-2" file-name="src/main.rs" caption="Optionale Typannotationen für die Typen der Parameter und des Rückgabewerts der Closure hinzufügen">

```rust
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-02/src/main.rs:here}}
```

</Listing>

Mit Typannotationen ähnelt die Syntax von Closures stärker der Syntax von
Funktionen. Hier definieren wir zum Vergleich eine Funktion, die 1 zu ihrem
Parameter addiert, und eine Closure mit demselben Verhalten. Wir haben einige
Leerzeichen eingefügt, um die entsprechenden Teile untereinander auszurichten.
Das zeigt, wie ähnlich die Syntax von Closures der Syntax von Funktionen ist,
abgesehen von den senkrechten Strichen und der Menge an optionaler Syntax:

```rust,ignore
fn  add_one_v1   (x: u32) -> u32 { x + 1 }
let add_one_v2 = |x: u32| -> u32 { x + 1 };
let add_one_v3 = |x|             { x + 1 };
let add_one_v4 = |x|               x + 1  ;
```

Die erste Zeile zeigt eine Funktionsdefinition und die zweite eine vollständig
annotierte Closure-Definition. In der dritten Zeile entfernen wir die
Typannotationen aus der Closure-Definition. In der vierten Zeile entfernen wir
die geschweiften Klammern, die optional sind, weil der Rumpf der Closure nur
einen Ausdruck hat. Das alles sind gültige Definitionen, die beim Aufruf
dasselbe Verhalten erzeugen. Die Zeilen `add_one_v3` und `add_one_v4` erfordern,
dass die Closures ausgewertet werden, damit der Code kompiliert, weil die Typen
aus ihrer Verwendung abgeleitet werden. Das ähnelt `let v = Vec::new();`, das
entweder Typannotationen braucht oder Werte eines Typs, die in den `Vec`
eingefügt werden, damit Rust den Typ ableiten kann.

Bei Closure-Definitionen leitet der Compiler für jeden ihrer Parameter und für
ihren Rückgabewert einen konkreten Typ ab. Listing 13-3 zeigt zum Beispiel die
Definition einer kurzen Closure, die einfach den Wert zurückgibt, den sie als
Parameter erhält. Diese Closure ist außer für dieses Beispiel nicht sehr
nützlich. Beachte, dass wir der Definition keine Typannotationen hinzugefügt
haben. Da es keine Typannotationen gibt, können wir die Closure mit jedem Typ
aufrufen, was wir hier beim ersten Mal mit `String` getan haben. Versuchen wir
dann, `example_closure` mit einer Ganzzahl aufzurufen, erhalten wir einen
Fehler.

<Listing number="13-3" file-name="src/main.rs" caption="Versuch, eine Closure, deren Typen abgeleitet werden, mit zwei verschiedenen Typen aufzurufen">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-03/src/main.rs:here}}
```

</Listing>

Der Compiler gibt uns diesen Fehler:

```console
{{#include ../listings/ch13-functional-features/listing-13-03/output.txt}}
```

Beim ersten Aufruf von `example_closure` mit dem `String`-Wert leitet der
Compiler ab, dass der Typ von `x` und der Rückgabetyp der Closure `String` sind.
Diese Typen werden dann in der Closure in `example_closure` festgeschrieben, und
wir erhalten einen Typfehler, wenn wir als Nächstes versuchen, einen anderen Typ
mit derselben Closure zu verwenden.

{{#quiz ../quizzes/ch13-01-closures-sec1.toml}}

### Referenzen erfassen oder Ownership übertragen {#capturing-references-or-moving-ownership}

Closures können Werte aus ihrer Umgebung auf drei Arten erfassen, die direkt den
drei Arten entsprechen, wie eine Funktion einen Parameter nehmen kann:
unveränderlich ausleihen (_borrow_), veränderlich (_mutable_) ausleihen und die
Ownership übernehmen. Die Closure entscheidet anhand dessen, was der Rumpf der
Funktion mit den erfassten Werten tut, welche davon sie verwendet.

In Listing 13-4 definieren wir eine Closure, die eine unveränderliche Referenz
auf den Vektor namens `list` erfasst, weil sie nur eine unveränderliche Referenz
braucht, um den Wert auszugeben.

<Listing number="13-4" file-name="src/main.rs" caption="Eine Closure definieren und aufrufen, die eine unveränderliche Referenz erfasst">

```rust
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-04/src/main.rs}}
```

</Listing>

Dieses Beispiel zeigt auch, dass eine Variable an eine Closure-Definition
gebunden werden kann und wir die Closure später aufrufen können, indem wir den
Variablennamen und Klammern verwenden, als wäre der Variablenname ein
Funktionsname.

Da wir mehrere unveränderliche Referenzen auf `list` gleichzeitig haben können,
ist `list` im Code vor der Closure-Definition, nach der Closure-Definition, aber
vor dem Aufruf der Closure, und nach dem Aufruf der Closure weiterhin
zugänglich. Dieser Code kompiliert, läuft und gibt Folgendes aus:

```console
{{#include ../listings/ch13-functional-features/listing-13-04/output.txt}}
```

Als Nächstes ändern wir in Listing 13-5 den Rumpf der Closure so, dass er dem
Vektor `list` ein Element hinzufügt. Die Closure erfasst jetzt eine
veränderliche (_mutable_) Referenz.

<Listing number="13-5" file-name="src/main.rs" caption="Eine Closure definieren und aufrufen, die eine veränderliche Referenz erfasst">

```rust
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-05/src/main.rs}}
```

</Listing>

Dieser Code kompiliert, läuft und gibt Folgendes aus:

```console
{{#include ../listings/ch13-functional-features/listing-13-05/output.txt}}
```

Beachte, dass zwischen der Definition und dem Aufruf der Closure
`borrows_mutably` kein `println!` mehr steht: Wenn `borrows_mutably` definiert
wird, erfasst sie eine veränderliche Referenz auf `list`. Nach dem Aufruf der
Closure verwenden wir sie nicht mehr, also endet die veränderliche Ausleihe.
Zwischen der Closure-Definition und dem Aufruf der Closure ist eine
unveränderliche Ausleihe zum Ausgeben nicht erlaubt, weil bei einer
veränderlichen Ausleihe keine anderen Ausleihen erlaubt sind. Füg dort ein
`println!` hinzu und sieh dir an, welche Fehlermeldung du bekommst!

Wenn du erzwingen willst, dass die Closure die Ownership der Werte übernimmt,
die sie aus der Umgebung verwendet, obwohl der Rumpf der Closure die Ownership
eigentlich nicht braucht, kannst du vor der Parameterliste das Schlüsselwort
`move` verwenden.

Diese Technik ist vor allem nützlich, wenn man eine Closure an einen neuen
Thread übergibt, um die Daten zu verschieben (_move_), sodass sie dem neuen
Thread gehören. Threads und warum man sie verwenden möchte, besprechen wir
ausführlich in Kapitel 16, wenn es um Nebenläufigkeit geht. Vorerst sehen wir
uns kurz an, wie man einen neuen Thread mit einer Closure startet, die das
Schlüsselwort `move` braucht. Listing 13-6 zeigt Listing 13-4, abgeändert,
sodass der Vektor in einem neuen Thread statt im Haupt-Thread ausgegeben wird.

<Listing number="13-6" file-name="src/main.rs" caption="Mit `move` erzwingen, dass die Closure für den Thread die Ownership von `list` übernimmt">

```rust
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-06/src/main.rs}}
```

</Listing>

Wir starten einen neuen Thread und geben ihm eine Closure als Argument mit, die
er ausführen soll. Der Rumpf der Closure gibt die Liste aus. In Listing 13-4 hat
die Closure `list` nur über eine unveränderliche Referenz erfasst, weil das der
geringste Zugriff auf `list` ist, der zum Ausgeben nötig ist. In diesem Beispiel
braucht der Rumpf der Closure zwar immer noch nur eine unveränderliche Referenz,
aber wir müssen angeben, dass `list` in die Closure verschoben werden soll,
indem wir das Schlüsselwort `move` an den Anfang der Closure-Definition setzen.
Würde der Haupt-Thread vor dem Aufruf von `join` auf dem neuen Thread weitere
Operationen ausführen, könnte der neue Thread fertig werden, bevor der Rest des
Haupt-Threads fertig ist, oder der Haupt-Thread könnte zuerst fertig werden.
Würde der Haupt-Thread die Ownership von `list` behalten, aber vor dem neuen
Thread enden und `list` verwerfen (_drop_), wäre die unveränderliche Referenz im
Thread ungültig. Daher verlangt der Compiler, dass `list` in die Closure
verschoben wird, die dem neuen Thread übergeben wird, damit die Referenz gültig
bleibt. Versuch, das Schlüsselwort `move` zu entfernen oder `list` nach der
Definition der Closure im Haupt-Thread zu verwenden, und sieh dir an, welche
Compilerfehler du bekommst!

<!-- Old headings. Do not remove or links may break. -->

<a id="storing-closures-using-generic-parameters-and-the-fn-traits"></a>
<a id="limitations-of-the-cacher-implementation"></a>
<a id="moving-captured-values-out-of-the-closure-and-the-fn-traits"></a>
<a id="moving-captured-values-out-of-closures-and-the-fn-traits"></a>

### Erfasste Werte aus Closures herausverschieben {#moving-captured-values-out-of-closures}

Sobald eine Closure eine Referenz oder die Ownership eines Werts aus der
Umgebung erfasst hat, in der sie definiert ist (und damit beeinflusst hat, was
gegebenenfalls _in_ die Closure verschoben wird), legt der Code im Rumpf der
Closure fest, was mit den Referenzen oder Werten passiert, wenn die Closure
später ausgewertet wird (und damit, was gegebenenfalls _aus_ der Closure
herausverschoben wird).

Ein Closure-Rumpf kann Folgendes tun: einen erfassten Wert aus der Closure
herausverschieben, den erfassten Wert verändern, den Wert weder verschieben noch
verändern oder von vornherein nichts aus der Umgebung erfassen.

Wie eine Closure Werte aus der Umgebung erfasst und behandelt, beeinflusst,
welche Traits die Closure implementiert, und über Traits können Funktionen und
Structs angeben, welche Arten von Closures sie verwenden können. Closures
implementieren automatisch einen, zwei oder alle drei dieser `Fn`-Traits,
aufeinander aufbauend, je nachdem, wie der Rumpf der Closure mit den Werten
umgeht:

- `FnOnce` gilt für Closures, die einmal aufgerufen werden können. Alle Closures
  implementieren mindestens diesen Trait, weil alle Closures aufgerufen werden
  können. Eine Closure, die erfasste Werte aus ihrem Rumpf herausverschiebt,
  implementiert nur `FnOnce` und keinen der anderen `Fn`-Traits, weil sie nur
  einmal aufgerufen werden kann.
- `FnMut` gilt für Closures, die keine erfassten Werte aus ihrem Rumpf
  herausverschieben, die erfassten Werte aber möglicherweise verändern. Diese
  Closures können mehr als einmal aufgerufen werden.
- `Fn` gilt für Closures, die keine erfassten Werte aus ihrem Rumpf
  herausverschieben und erfasste Werte nicht verändern, sowie für Closures, die
  nichts aus ihrer Umgebung erfassen. Diese Closures können mehr als einmal
  aufgerufen werden, ohne ihre Umgebung zu verändern, was wichtig ist, etwa wenn
  eine Closure mehrmals nebenläufig aufgerufen wird.

Sehen wir uns die Definition der Methode `unwrap_or_else` auf `Option<T>` an,
die wir in Listing 13-1 verwendet haben:

```rust,ignore
impl<T> Option<T> {
    pub fn unwrap_or_else<F>(self, f: F) -> T
    where
        F: FnOnce() -> T
    {
        match self {
            Some(x) => x,
            None => f(),
        }
    }
}
```

Erinnere dich, dass `T` der generische Typ ist, der für den Typ des Werts in der
Variante `Some` einer `Option` steht. Dieser Typ `T` ist auch der Rückgabetyp
der Funktion `unwrap_or_else`: Code, der `unwrap_or_else` zum Beispiel auf einer
`Option<String>` aufruft, erhält einen `String`.

Beachte als Nächstes, dass die Funktion `unwrap_or_else` den zusätzlichen
generischen Typparameter `F` hat. Der Typ `F` ist der Typ des Parameters namens
`f`, also der Closure, die wir beim Aufruf von `unwrap_or_else` übergeben.

Der Trait-Bound für den generischen Typ `F` ist `FnOnce() -> T`. Das bedeutet,
dass `F` einmal aufgerufen werden können, keine Argumente nehmen und ein `T`
zurückgeben muss. `FnOnce` im Trait-Bound drückt die Einschränkung aus, dass
`unwrap_or_else` `f` nicht mehr als einmal aufruft. Im Rumpf von
`unwrap_or_else` sehen wir, dass `f` nicht aufgerufen wird, wenn die `Option`
`Some` ist. Ist die `Option` `None`, wird `f` einmal aufgerufen. Da alle
Closures `FnOnce` implementieren, akzeptiert `unwrap_or_else` alle drei Arten
von Closures und ist so flexibel wie möglich.

> Note: Wenn das, was wir tun wollen, kein Erfassen eines Werts aus der Umgebung
> erfordert, können wir dort, wo wir etwas brauchen, das einen der `Fn`-Traits
> implementiert, statt einer Closure den Namen einer Funktion verwenden. Auf
> einem `Option<Vec<T>>`-Wert könnten wir zum Beispiel
> `unwrap_or_else(Vec::new)` aufrufen, um einen neuen, leeren Vektor zu
> erhalten, wenn der Wert `None` ist. Der Compiler implementiert für eine
> Funktionsdefinition automatisch die `Fn`-Traits, die jeweils zutreffen.

Sehen wir uns jetzt die Methode `sort_by_key` der Standardbibliothek an, die auf
Slices definiert ist, um zu sehen, worin sie sich von `unwrap_or_else`
unterscheidet und warum `sort_by_key` für den Trait-Bound `FnMut` statt `FnOnce`
verwendet. Die Closure erhält ein Argument in Form einer Referenz auf das
aktuell betrachtete Element im Slice und gibt einen Wert vom Typ `K` zurück, der
sich ordnen lässt. Diese Funktion ist nützlich, wenn du einen Slice nach einem
bestimmten Attribut jedes Elements sortieren willst. In Listing 13-7 haben wir
eine Liste von `Rectangle`-Instanzen und verwenden `sort_by_key`, um sie
aufsteigend nach ihrem Attribut `width` zu ordnen.

<Listing number="13-7" file-name="src/main.rs" caption="Rechtecke mit `sort_by_key` nach ihrer Breite ordnen">

```rust
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-07/src/main.rs}}
```

</Listing>

Dieser Code gibt Folgendes aus:

```console
{{#include ../listings/ch13-functional-features/listing-13-07/output.txt}}
```

`sort_by_key` ist so definiert, dass es eine `FnMut`-Closure nimmt, weil es die
Closure mehrmals aufruft: einmal für jedes Element im Slice. Die Closure
`|r|
r.width` erfasst, verändert oder verschiebt nichts aus ihrer Umgebung,
erfüllt also die Anforderungen des Trait-Bounds.

Listing 13-8 zeigt dagegen ein Beispiel für eine Closure, die nur den Trait
`FnOnce` implementiert, weil sie einen Wert aus der Umgebung herausverschiebt.
Der Compiler lässt uns diese Closure nicht mit `sort_by_key` verwenden.

<Listing number="13-8" file-name="src/main.rs" caption="Versuch, eine `FnOnce`-Closure mit `sort_by_key` zu verwenden">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-08/src/main.rs}}
```

</Listing>

Das ist ein konstruierter, umständlicher Weg (der nicht funktioniert), um zu
zählen, wie oft `sort_by_key` die Closure beim Sortieren von `list` aufruft.
Dieser Code versucht zu zählen, indem er `value` – einen `String` aus der
Umgebung der Closure – in den Vektor `sort_operations` einfügt. Die Closure
erfasst `value` und verschiebt `value` dann aus der Closure heraus, indem sie
die Ownership von `value` an den Vektor `sort_operations` überträgt. Diese
Closure kann einmal aufgerufen werden; ein zweiter Aufruf würde nicht
funktionieren, weil `value` dann nicht mehr in der Umgebung wäre, um erneut in
`sort_operations` eingefügt zu werden! Daher implementiert diese Closure nur
`FnOnce`. Wenn wir versuchen, diesen Code zu kompilieren, erhalten wir diesen
Fehler, dass `value` nicht aus der Closure herausverschoben werden kann, weil
die Closure `FnMut` implementieren muss:

```console
{{#include ../listings/ch13-functional-features/listing-13-08/output.txt}}
```

Der Fehler verweist auf die Zeile im Rumpf der Closure, die `value` aus der
Umgebung herausverschiebt. Um das zu beheben, müssen wir den Rumpf der Closure
so ändern, dass er keine Werte aus der Umgebung herausverschiebt. Einen Zähler
in der Umgebung zu halten und seinen Wert im Rumpf der Closure zu erhöhen, ist
ein einfacherer Weg, um zu zählen, wie oft die Closure aufgerufen wird. Die
Closure in Listing 13-9 funktioniert mit `sort_by_key`, weil sie nur eine
veränderliche Referenz auf den Zähler `num_sort_operations` erfasst und daher
mehr als einmal aufgerufen werden kann.

<Listing number="13-9" file-name="src/main.rs" caption="Eine `FnMut`-Closure mit `sort_by_key` zu verwenden, ist erlaubt.">

```rust
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-09/src/main.rs}}
```

</Listing>

<!-- TODO: consider adding a section on the use<> operator -->

Zusammengefasst sind die `Fn`-Traits wichtig, wenn man Funktionen oder Typen
definiert oder verwendet, die Closures nutzen. Im nächsten Abschnitt besprechen
wir Iteratoren. Viele Iterator-Methoden nehmen Closures als Argumente, also
behalte diese Details über Closures im Hinterkopf, während wir weitermachen!

{{#quiz ../quizzes/ch13-01-closures-sec2.toml}}

[unwrap-or-else]: https://doc.rust-lang.org/std/option/enum.Option.html#method.unwrap_or_else
[lifetime elision]: ch10-03-lifetime-syntax.html#lifetime-elision
