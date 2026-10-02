<!-- Old headings. Do not remove or links may break. -->

<a id="using-trait-objects-that-allow-for-values-of-different-types"></a>

## Mit Trait-Objekten über gemeinsames Verhalten abstrahieren {#using-trait-objects-to-abstract-over-shared-behavior}

In Kapitel 8 haben wir erwähnt, dass eine Einschränkung von Vektoren darin
besteht, dass sie nur Elemente eines einzigen Typs speichern können. In Listing
8-9 haben wir einen Workaround geschaffen, indem wir ein Enum `SpreadsheetCell`
definiert haben, das Varianten für Ganzzahlen, Gleitkommazahlen und Text hatte.
Dadurch konnten wir in jeder Zelle unterschiedliche Datentypen speichern und
trotzdem einen Vektor haben, der eine Zeile von Zellen darstellte. Das ist eine
völlig gute Lösung, wenn unsere austauschbaren Elemente eine feste Menge von
Typen sind, die wir kennen, wenn unser Code kompiliert wird.

Manchmal möchten wir aber, dass die Benutzer unserer Bibliothek die Menge der
Typen erweitern können, die in einer bestimmten Situation gültig sind. Um zu
zeigen, wie wir das erreichen können, erstellen wir als Beispiel ein Werkzeug
für eine grafische Benutzeroberfläche (GUI), das eine Liste von Elementen
durchläuft und für jedes davon eine Methode `draw` aufruft, um es auf den
Bildschirm zu zeichnen – eine gängige Technik bei GUI-Werkzeugen. Wir erstellen
einen Library-Crate namens `gui`, der die Struktur einer GUI-Bibliothek enthält.
Dieser Crate könnte einige Typen zur Verwendung bereitstellen, etwa `Button`
oder `TextField`. Darüber hinaus werden Benutzer von `gui` eigene Typen
erstellen wollen, die gezeichnet werden können: Zum Beispiel könnte eine
Programmiererin ein `Image` hinzufügen und ein anderer Programmierer eine
`SelectBox`.

Beim Schreiben der Bibliothek können wir nicht alle Typen kennen und definieren,
die andere Programmierer vielleicht erstellen möchten. Wir wissen aber, dass
`gui` viele Werte unterschiedlicher Typen verwalten und für jeden dieser
unterschiedlich typisierten Werte eine Methode `draw` aufrufen muss. Es muss
nicht genau wissen, was passiert, wenn wir die Methode `draw` aufrufen, sondern
nur, dass der Wert diese Methode zum Aufrufen bereitstellt.

Um das in einer Sprache mit Vererbung zu tun, könnten wir eine Klasse namens
`Component` definieren, die eine Methode namens `draw` hat. Die anderen Klassen,
etwa `Button`, `Image` und `SelectBox`, würden von `Component` erben und damit
die Methode `draw` erben. Sie könnten jeweils die Methode `draw` überschreiben,
um ihr eigenes Verhalten zu definieren, aber das Framework könnte alle Typen so
behandeln, als wären sie `Component`-Instanzen, und `draw` auf ihnen aufrufen.
Weil Rust aber keine Vererbung hat, brauchen wir eine andere Möglichkeit, die
Bibliothek `gui` zu strukturieren, damit Benutzer neue Typen erstellen können,
die mit der Bibliothek kompatibel sind.

### Einen Trait für gemeinsames Verhalten definieren {#defining-a-trait-for-common-behavior}

Um das Verhalten zu implementieren, das `gui` haben soll, definieren wir einen
Trait namens `Draw`, der eine Methode namens `draw` hat. Dann können wir einen
Vektor definieren, der ein Trait-Objekt aufnimmt. Ein _Trait-Objekt_ zeigt
sowohl auf eine Instanz eines Typs, der unseren angegebenen Trait implementiert,
als auch auf eine Tabelle, mit der zur Laufzeit Trait-Methoden dieses Typs
nachgeschlagen werden. Wir erstellen ein Trait-Objekt, indem wir eine Art Zeiger
angeben, etwa eine Referenz oder einen Smart-Pointer `Box<T>`, dann das
Schlüsselwort `dyn` und dann den betreffenden Trait. (Warum Trait-Objekte einen
Zeiger verwenden müssen, besprechen wir im Abschnitt
[„Typen mit dynamischer
Größe und der Trait `Sized`“][dynamically-sized]<!-- ignore --> in Kapitel 20.)
Wir können Trait-Objekte anstelle eines generischen oder konkreten Typs
verwenden. Wo immer wir ein Trait-Objekt verwenden, stellt das Typsystem von
Rust zur Kompilierzeit sicher, dass jeder in diesem Kontext verwendete Wert den
Trait des Trait-Objekts implementiert. Folglich müssen wir zur Kompilierzeit
nicht alle möglichen Typen kennen.

Wir haben erwähnt, dass wir in Rust darauf verzichten, Structs und Enums
„Objekte“ zu nennen, um sie von den Objekten anderer Sprachen zu unterscheiden.
In einem Struct oder Enum sind die Daten in den Feldern des Structs und das
Verhalten in `impl`-Blöcken getrennt, während in anderen Sprachen die Daten und
das Verhalten, zu einem Konzept vereint, oft als Objekt bezeichnet werden.
Trait-Objekte unterscheiden sich von Objekten in anderen Sprachen darin, dass
wir einem Trait-Objekt keine Daten hinzufügen können. Trait-Objekte sind nicht
so allgemein nützlich wie Objekte in anderen Sprachen: Ihr spezifischer Zweck
ist es, Abstraktion über gemeinsames Verhalten zu ermöglichen.

Listing 18-3 zeigt, wie man einen Trait namens `Draw` mit einer Methode namens
`draw` definiert.

<Listing number="18-3" file-name="src/lib.rs" caption="Definition des Traits `Draw`">

```rust,noplayground
{{#rustdoc_include ../listings/ch18-oop/listing-18-03/src/lib.rs}}
```

</Listing>

Diese Syntax sollte dir aus unseren Ausführungen in Kapitel 10 darüber, wie man
Traits definiert, bekannt vorkommen. Als Nächstes kommt neue Syntax: Listing
18-4 definiert ein Struct namens `Screen`, das einen Vektor namens `components`
enthält. Dieser Vektor hat den Typ `Box<dyn Draw>`, der ein Trait-Objekt ist; er
steht stellvertretend für jeden Typ innerhalb einer `Box`, der den Trait `Draw`
implementiert.

<Listing number="18-4" file-name="src/lib.rs" caption="Definition des Structs `Screen` mit einem Feld `components`, das einen Vektor von Trait-Objekten enthält, die den Trait `Draw` implementieren">

```rust,noplayground
{{#rustdoc_include ../listings/ch18-oop/listing-18-04/src/lib.rs:here}}
```

</Listing>

Für das Struct `Screen` definieren wir eine Methode namens `run`, die für jede
ihrer `components` die Methode `draw` aufruft, wie in Listing 18-5 gezeigt.

<Listing number="18-5" file-name="src/lib.rs" caption="Eine Methode `run` für `Screen`, die für jede Komponente die Methode `draw` aufruft">

```rust,noplayground
{{#rustdoc_include ../listings/ch18-oop/listing-18-05/src/lib.rs:here}}
```

</Listing>

Das funktioniert anders, als ein Struct zu definieren, das einen generischen
Typparameter mit Trait-Bounds verwendet. Ein generischer Typparameter kann
jeweils nur durch einen einzigen konkreten Typ ersetzt werden, während
Trait-Objekte es erlauben, dass zur Laufzeit mehrere konkrete Typen die Stelle
des Trait-Objekts einnehmen. Wir hätten das Struct `Screen` zum Beispiel mit
einem generischen Typ und einem Trait-Bound definieren können, wie in Listing
18-6.

<Listing number="18-6" file-name="src/lib.rs" caption="Eine alternative Implementierung des Structs `Screen` und seiner Methode `run` mit Generics und Trait-Bounds">

```rust,noplayground
{{#rustdoc_include ../listings/ch18-oop/listing-18-06/src/lib.rs:here}}
```

</Listing>

Das beschränkt uns auf eine `Screen`-Instanz mit einer Liste von Komponenten,
die alle vom Typ `Button` oder alle vom Typ `TextField` sind. Wenn du immer nur
homogene Collections hast, sind Generics und Trait-Bounds vorzuziehen, weil die
Definitionen zur Kompilierzeit monomorphisiert werden, um die konkreten Typen zu
verwenden.

Mit der Methode, die Trait-Objekte verwendet, kann dagegen eine `Screen`-Instanz
einen `Vec<T>` enthalten, der sowohl eine `Box<Button>` als auch eine
`Box<TextField>` enthält. Sehen wir uns an, wie das funktioniert, und sprechen
wir dann über die Auswirkungen auf die Laufzeit-Performance.

### Den Trait implementieren {#implementing-the-trait}

Jetzt fügen wir einige Typen hinzu, die den Trait `Draw` implementieren. Wir
stellen den Typ `Button` bereit. Auch hier geht es über den Rahmen dieses Buches
hinaus, tatsächlich eine GUI-Bibliothek zu implementieren, daher hat die Methode
`draw` in ihrem Rumpf keine sinnvolle Implementierung. Um sich vorzustellen, wie
die Implementierung aussehen könnte: Ein Struct `Button` könnte Felder für
`width`, `height` und `label` haben, wie in Listing 18-7 gezeigt.

<Listing number="18-7" file-name="src/lib.rs" caption="Ein Struct `Button`, das den Trait `Draw` implementiert">

```rust,noplayground
{{#rustdoc_include ../listings/ch18-oop/listing-18-07/src/lib.rs:here}}
```

</Listing>

Die Felder `width`, `height` und `label` von `Button` unterscheiden sich von den
Feldern anderer Komponenten; ein Typ `TextField` könnte zum Beispiel dieselben
Felder plus ein Feld `placeholder` haben. Jeder der Typen, die wir auf dem
Bildschirm zeichnen wollen, implementiert den Trait `Draw`, verwendet aber in
der Methode `draw` unterschiedlichen Code, um festzulegen, wie dieser bestimmte
Typ gezeichnet wird, wie es `Button` hier tut (wie erwähnt ohne den eigentlichen
GUI-Code). Der Typ `Button` könnte zum Beispiel einen zusätzlichen `impl`-Block
mit Methoden dafür haben, was passiert, wenn ein Benutzer auf die Schaltfläche
klickt. Solche Methoden treffen auf Typen wie `TextField` nicht zu.

Wenn jemand, der unsere Bibliothek verwendet, sich entscheidet, ein Struct
`SelectBox` mit den Feldern `width`, `height` und `options` zu implementieren,
müsste diese Person den Trait `Draw` ebenfalls für den Typ `SelectBox`
implementieren, wie in Listing 18-8 gezeigt.

<Listing number="18-8" file-name="src/main.rs" caption="Ein anderer Crate, der `gui` verwendet und den Trait `Draw` für ein Struct `SelectBox` implementiert">

```rust,ignore
{{#rustdoc_include ../listings/ch18-oop/listing-18-08/src/main.rs:here}}
```

</Listing>

### Den Trait verwenden {#using-the-trait}

Wer unsere Bibliothek verwendet, kann jetzt eine Funktion `main` schreiben, um
eine `Screen`-Instanz zu erstellen. Zur `Screen`-Instanz lassen sich eine
`SelectBox` und ein `Button` hinzufügen, indem man beide jeweils in eine
`Box<T>` legt, sodass sie zu Trait-Objekten werden. Dann kann man die Methode
`run` auf der `Screen`-Instanz aufrufen, die `draw` für jede der Komponenten
aufruft. Listing 18-9 zeigt diese Implementierung.

<Listing number="18-9" file-name="src/main.rs" caption="Trait-Objekte verwenden, um Werte unterschiedlicher Typen zu speichern, die denselben Trait implementieren">

```rust,ignore
{{#rustdoc_include ../listings/ch18-oop/listing-18-09/src/main.rs:here}}
```

</Listing>

Als wir die Bibliothek geschrieben haben, wussten wir nicht, dass jemand den Typ
`SelectBox` hinzufügen könnte, aber unsere `Screen`-Implementierung konnte mit
dem neuen Typ arbeiten und ihn zeichnen, weil `SelectBox` den Trait `Draw`
implementiert, was bedeutet, dass er die Methode `draw` implementiert.

Dieses Konzept – sich nur um die Nachrichten zu kümmern, auf die ein Wert
reagiert, statt um den konkreten Typ des Werts – ähnelt dem Konzept des _Duck
Typing_ in dynamisch typisierten Sprachen: Wenn es wie eine Ente läuft und wie
eine Ente quakt, dann muss es eine Ente sein! In der Implementierung von `run`
für `Screen` in Listing 18-5 muss `run` nicht wissen, welchen konkreten Typ jede
Komponente hat. Es prüft nicht, ob eine Komponente eine Instanz von `Button`
oder von `SelectBox` ist, sondern ruft einfach die Methode `draw` für die
Komponente auf. Indem wir `Box<dyn Draw>` als Typ der Werte im Vektor
`components` angegeben haben, haben wir festgelegt, dass `Screen` Werte braucht,
für die wir die Methode `draw` aufrufen können.

Der Vorteil, Trait-Objekte und das Typsystem von Rust zu verwenden, um Code zu
schreiben, der Code mit Duck Typing ähnelt, besteht darin, dass wir nie zur
Laufzeit prüfen müssen, ob ein Wert eine bestimmte Methode implementiert, oder
uns Sorgen um Fehler machen müssen, wenn ein Wert eine Methode nicht
implementiert, wir sie aber trotzdem aufrufen. Rust kompiliert unseren Code
nicht, wenn die Werte die Traits nicht implementieren, die die Trait-Objekte
brauchen.

Listing 18-10 zeigt zum Beispiel, was passiert, wenn wir versuchen, einen
`Screen` mit einem `String` als Komponente zu erstellen.

<Listing number="18-10" file-name="src/main.rs" caption="Versuch, einen Typ zu verwenden, der den Trait des Trait-Objekts nicht implementiert">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch18-oop/listing-18-10/src/main.rs}}
```

</Listing>

Wir bekommen diesen Fehler, weil `String` den Trait `Draw` nicht implementiert:

```console
{{#include ../listings/ch18-oop/listing-18-10/output.txt}}
```

Dieser Fehler teilt uns mit, dass wir entweder etwas an `Screen` übergeben, das
wir nicht übergeben wollten, und daher einen anderen Typ übergeben sollten, oder
dass wir `Draw` für `String` implementieren sollten, damit `Screen` `draw` dafür
aufrufen kann.

<!-- BEGIN INTERVENTION: cce62358-5291-4eb3-84d6-fbc570873ee3 -->

### Trait-Objekte und Typinferenz {#trait-objects-and-type-inference}

Ein Nachteil von Trait-Objekten ist ihr Zusammenspiel mit der Typinferenz.
Betrachte zum Beispiel die Typinferenz für `Vec<T>`. Wenn `T` kein Trait-Objekt
ist, muss Rust nur den Typ eines einzigen Elements im Vektor kennen, um `T`
abzuleiten. Ein leerer Vektor verursacht daher einen Typinferenzfehler:

```rust,ignore,does_not_compile
# fn main() {
let v = vec![];
// error[E0282]: type annotations needed for `Vec<T>`
# }
```

Fügt man aber ein Element hinzu, kann Rust den Typ des Vektors ableiten:

```rust,ignore
# fn main() {
let v = vec!["Hello world"];
// ok, v : Vec<&str>
# }
```

Bei Trait-Objekten ist die Typinferenz kniffliger. Angenommen, wir versuchen,
das Array `components` aus Listing 18-9 wie folgt in eine eigene Variable
auszulagern:

```rust,ignore,does_not_compile
fn main() {
    let components = vec![
        Box::new(SelectBox { /* .. */ }),
        Box::new(Button { /* .. */ }),
    ];
    let screen = Screen { components };
    screen.run();
}
```

<span class="caption">Listing 18-11: Das Auslagern des Arrays mit den
Komponenten verursacht einen Typfehler</span>

Durch dieses Refactoring kompiliert das Programm nicht mehr! Der Compiler lehnt
dieses Programm mit folgendem Fehler ab:

```text
error[E0308]: mismatched types
   --> test.rs:55:14
    |
55  |       Box::new(Button {
    |  _____--------_^
    | |     |
    | |     arguments to this function are incorrect
56  | |       width: 50,
57  | |       height: 10,
58  | |       label: String::from("OK"),
59  | |     }),
    | |_____^ expected `SelectBox`, found `Button`
```

In Listing 18-09 versteht der Compiler, dass der Vektor `components` den Typ
`Vec<Box<dyn Draw>>` haben muss, weil das in der Definition des Structs `Screen`
so angegeben ist. In Listing 18-11 verliert der Compiler diese Information aber
an der Stelle, an der `components` definiert wird. Um das Problem zu beheben,
musst du dem Typinferenz-Algorithmus einen Hinweis geben. Das kann entweder über
eine explizite Umwandlung (_cast_) eines beliebigen Elements des Vektors
geschehen, etwa so:

```rust,ignore
let components = vec![
    Box::new(SelectBox { /* .. */ }) as Box<dyn Draw>,
    Box::new(Button { /* .. */ }),
];
```

Oder über eine Typannotation an der let-Bindung, etwa so:

```rust,ignore
let components: Vec<Box<dyn Draw>> = vec![
    Box::new(SelectBox { /* .. */ }),
    Box::new(Button { /* .. */ }),
];
```

Im Allgemeinen ist es gut zu wissen, dass Trait-Objekte bei der Typinferenz zu
einer schlechteren Entwicklererfahrung für die Nutzer einer API führen können.

<!-- END INTERVENTION: cce62358-5291-4eb3-84d6-fbc570873ee3 -->

<!-- Old headings. Do not remove or links may break. -->

<a id="trait-objects-perform-dynamic-dispatch"></a>

### Dynamischen Dispatch durchführen {#performing-dynamic-dispatch}

Erinnere dich an unsere Diskussion im Abschnitt
[„Performance von Code mit
Generics“][performance-of-code-using-generics]<!-- ignore --> in Kapitel 10 über
den Prozess der Monomorphisierung, den der Compiler bei Generics durchführt: Der
Compiler erzeugt nicht-generische Implementierungen von Funktionen und Methoden
für jeden konkreten Typ, den wir anstelle eines generischen Typparameters
verwenden. Der Code, der aus der Monomorphisierung hervorgeht, führt _statischen
Dispatch_ durch, das heißt, der Compiler weiß zur Kompilierzeit, welche Methode
du aufrufst. Das Gegenteil davon ist _dynamischer Dispatch_, bei dem der
Compiler zur Kompilierzeit nicht feststellen kann, welche Methode du aufrufst.
In Fällen von dynamischem Dispatch erzeugt der Compiler Code, der zur Laufzeit
weiß, welche Methode aufgerufen werden muss.

Wenn wir Trait-Objekte verwenden, muss Rust dynamischen Dispatch verwenden. Der
Compiler kennt nicht alle Typen, die mit dem Code verwendet werden könnten, der
Trait-Objekte verwendet, und weiß daher nicht, welche auf welchem Typ
implementierte Methode er aufrufen soll. Stattdessen verwendet Rust zur Laufzeit
die Zeiger im Trait-Objekt, um herauszufinden, welche Methode aufgerufen werden
muss. Dieses Nachschlagen verursacht Laufzeitkosten, die bei statischem Dispatch
nicht anfallen. Dynamischer Dispatch verhindert außerdem, dass der Compiler den
Code einer Methode inlinen kann, was wiederum manche Optimierungen verhindert,
und Rust hat einige Regeln dazu, wo du dynamischen Dispatch verwenden kannst und
wo nicht, die sogenannte _dyn-Kompatibilität_ (_dyn compatibility_). Diese
Regeln gehen über den Rahmen dieser Diskussion hinaus, aber du kannst
[in der Referenz][dyn-compatibility]<!-- ignore --> mehr darüber lesen. Wir
haben allerdings zusätzliche Flexibilität in dem Code gewonnen, den wir in
Listing 18-5 geschrieben haben und in Listing 18-9 unterstützen konnten, es ist
also ein Kompromiss, den man abwägen muss.

{{#quiz ../quizzes/ch17-02-trait-objects.toml}}

[performance-of-code-using-generics]: ch10-01-syntax.html#performance-of-code-using-generics
[dynamically-sized]: ch20-03-advanced-types.html#dynamically-sized-types-and-the-sized-trait
[dyn-compatibility]: https://doc.rust-lang.org/reference/items/traits.html#dyn-compatibility
