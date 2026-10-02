## Listen von Werten in Vektoren speichern {#storing-lists-of-values-with-vectors}

Der erste Collection-Typ, den wir uns ansehen, ist `Vec<T>`, auch Vektor
genannt. In Vektoren kannst du mehr als einen Wert in einer einzigen
Datenstruktur speichern, die alle Werte im Speicher nebeneinander ablegt.
Vektoren können nur Werte desselben Typs speichern. Sie sind nützlich, wenn du
eine Liste von Einträgen hast, etwa die Textzeilen einer Datei oder die Preise
der Artikel in einem Warenkorb.

### Einen neuen Vektor erstellen {#creating-a-new-vector}

Um einen neuen, leeren Vektor zu erstellen, rufen wir die Funktion `Vec::new`
auf, wie in Listing 8-1 gezeigt.

<Listing number="8-1" caption="Einen neuen, leeren Vektor erstellen, der Werte vom Typ `i32` aufnehmen soll">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-01/src/main.rs:here}}
```

</Listing>

Beachte, dass wir hier eine Typannotation hinzugefügt haben. Da wir keine Werte
in diesen Vektor einfügen, weiß Rust nicht, welche Art von Elementen wir
speichern wollen. Das ist ein wichtiger Punkt. Vektoren sind mit Generics
implementiert; wie du Generics mit deinen eigenen Typen verwendest, behandeln
wir in Kapitel 10. Für den Moment genügt es zu wissen, dass der Typ `Vec<T>` aus
der Standardbibliothek jeden Typ aufnehmen kann. Wenn wir einen Vektor für einen
bestimmten Typ erstellen, können wir den Typ in spitzen Klammern angeben. In
Listing 8-1 haben wir Rust mitgeteilt, dass der `Vec<T>` in `v` Elemente vom Typ
`i32` enthalten wird.

Häufiger erstellst du einen `Vec<T>` mit Anfangswerten, und Rust leitet den Typ
der Werte ab, die du speichern willst, sodass du diese Typannotation selten
brauchst. Rust stellt praktischerweise das Makro `vec!` bereit, das einen neuen
Vektor mit den Werten erzeugt, die du ihm übergibst. Listing 8-2 erstellt einen
neuen `Vec<i32>`, der die Werte `1`, `2` und `3` enthält. Der Ganzzahltyp ist
`i32`, weil das der Standard-Ganzzahltyp ist, wie wir im Abschnitt
[„Datentypen“][data-types]<!-- ignore --> in Kapitel 3 besprochen haben.

<Listing number="8-2" caption="Einen neuen Vektor mit Werten erstellen">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-02/src/main.rs:here}}
```

</Listing>

Da wir `i32`-Anfangswerte angegeben haben, kann Rust ableiten, dass `v` den Typ
`Vec<i32>` hat, und die Typannotation ist nicht nötig. Als Nächstes sehen wir
uns an, wie man einen Vektor verändert.

### Einen Vektor aktualisieren {#updating-a-vector}

Um einen Vektor zu erstellen und ihm dann Elemente hinzuzufügen, können wir die
Methode `push` verwenden, wie in Listing 8-3 gezeigt.

<Listing number="8-3" caption="Mit der Methode `push` Werte zu einem Vektor hinzufügen">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-03/src/main.rs:here}}
```

</Listing>

Wie bei jeder Variable müssen wir sie mit dem Schlüsselwort `mut` veränderlich
(_mutable_) machen, wenn wir ihren Wert ändern können wollen, wie in Kapitel 3
besprochen. Die Zahlen, die wir hineinlegen, sind alle vom Typ `i32`, und Rust
leitet das aus den Daten ab, also brauchen wir die Annotation `Vec<i32>` nicht.

### Elemente von Vektoren lesen {#reading-elements-of-vectors}

Es gibt zwei Möglichkeiten, auf einen Wert zu verweisen, der in einem Vektor
gespeichert ist: per Indexierung oder mit der Methode `get`. In den folgenden
Beispielen haben wir die Typen der Werte, die diese Funktionen zurückgeben, zur
besseren Verständlichkeit annotiert.

Listing 8-4 zeigt beide Möglichkeiten, auf einen Wert in einem Vektor
zuzugreifen: mit der Indexierungssyntax und mit der Methode `get`.

<Listing number="8-4" caption="Mit der Indexierungssyntax und mit der Methode `get` auf ein Element in einem Vektor zugreifen">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-04/src/main.rs:here}}
```

</Listing>

Beachte hier ein paar Details. Wir verwenden den Indexwert `2`, um das dritte
Element zu erhalten, weil Vektoren über Zahlen indexiert werden, beginnend bei
null. Mit `&` und `[]` erhalten wir eine Referenz auf das Element am Indexwert.
Wenn wir die Methode `get` mit dem Index als Argument verwenden, erhalten wir
eine `Option<&T>`, die wir mit `match` verwenden können.

Rust bietet diese beiden Möglichkeiten, auf ein Element zu verweisen, damit du
wählen kannst, wie sich das Programm verhält, wenn du versuchst, einen Indexwert
außerhalb des Bereichs der vorhandenen Elemente zu verwenden. Sehen wir uns als
Beispiel an, was passiert, wenn wir einen Vektor mit fünf Elementen haben und
dann mit jeder der beiden Techniken versuchen, auf ein Element an Index 100
zuzugreifen, wie in Listing 8-5 gezeigt.

<Listing number="8-5" caption="Versuch, in einem Vektor mit fünf Elementen auf das Element an Index 100 zuzugreifen">

```rust,should_panic,panics
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-05/src/main.rs:here}}
```

</Listing>

Wenn wir diesen Code ausführen, löst die erste Methode mit `[]` einen Panic aus,
weil sie auf ein nicht vorhandenes Element verweist. Diese Methode eignet sich
am besten, wenn dein Programm abstürzen soll, sobald versucht wird, auf ein
Element hinter dem Ende des Vektors zuzugreifen.

Wenn der Methode `get` ein Index außerhalb des Vektors übergeben wird, gibt sie
`None` zurück, ohne einen Panic auszulösen. Diese Methode würdest du verwenden,
wenn ein Zugriff auf ein Element außerhalb des Bereichs des Vektors unter
normalen Umständen gelegentlich vorkommen kann. Dein Code enthält dann Logik, um
entweder `Some(&element)` oder `None` zu behandeln, wie in Kapitel 6 besprochen.
Der Index könnte zum Beispiel von einer Person stammen, die eine Zahl eingibt.
Gibt sie versehentlich eine zu große Zahl ein und das Programm erhält einen
`None`-Wert, könntest du ihr sagen, wie viele Einträge der aktuelle Vektor hat,
und ihr eine weitere Chance geben, einen gültigen Wert einzugeben. Das wäre
benutzerfreundlicher, als das Programm wegen eines Tippfehlers abstürzen zu
lassen!

Wenn das Programm eine gültige Referenz hat, setzt der Borrow-Checker die
Ownership- und Borrowing-Regeln (siehe Kapitel 4) durch, um sicherzustellen,
dass diese Referenz und alle anderen Referenzen auf den Inhalt des Vektors
gültig bleiben. Erinnere dich an die Regel, dass du im selben Gültigkeitsbereich
(_scope_) keine veränderlichen und unveränderlichen (_immutable_) Referenzen
haben kannst. Diese Regel greift in Listing 8-6, wo wir eine unveränderliche
Referenz auf das erste Element eines Vektors halten und versuchen, am Ende ein
Element hinzuzufügen. Dieses Programm funktioniert nicht, wenn wir später in der
Funktion auch noch auf dieses Element verweisen wollen.

<Listing number="8-6" caption="Versuch, einem Vektor ein Element hinzuzufügen, während eine Referenz auf einen Eintrag gehalten wird">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-06/src/main.rs:here}}
```

</Listing>

Das Kompilieren dieses Codes führt zu diesem Fehler:

```console
{{#include ../listings/ch08-common-collections/listing-08-06/output.txt}}
```

Der Code in Listing 8-6 sieht vielleicht so aus, als müsste er funktionieren:
Warum sollte sich eine Referenz auf das erste Element für Änderungen am Ende des
Vektors interessieren? Dieser Fehler liegt an der Funktionsweise von Vektoren:
Da Vektoren die Werte im Speicher nebeneinander ablegen, kann es beim Hinzufügen
eines neuen Elements am Ende des Vektors nötig sein, neuen Speicher zu
allozieren und die alten Elemente an den neuen Ort zu kopieren, falls nicht
genug Platz ist, um alle Elemente dort nebeneinander abzulegen, wo der Vektor
gerade gespeichert ist. In diesem Fall würde die Referenz auf das erste Element
auf freigegebenen Speicher zeigen. Die Borrowing-Regeln verhindern, dass
Programme in diese Situation geraten.

> Note: Mehr zu den Implementierungsdetails des Typs `Vec<T>` findest du im
> [„Rustonomicon“][nomicon].

### Über die Werte in einem Vektor iterieren {#iterating-over-the-values-in-a-vector}

Um nacheinander auf jedes Element eines Vektors zuzugreifen, würden wir über
alle Elemente iterieren, statt mit Indizes einzeln auf sie zuzugreifen. Listing
8-7 zeigt, wie man mit einer `for`-Schleife unveränderliche Referenzen auf jedes
Element in einem Vektor von `i32`-Werten erhält und sie ausgibt.

<Listing number="8-7" caption="Jedes Element in einem Vektor ausgeben, indem mit einer `for`-Schleife über die Elemente iteriert wird">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-07/src/main.rs:here}}
```

</Listing>

Um die Zahl zu lesen, auf die `i` verweist, müssen wir mit dem
Dereferenzierungsoperator `*` zum Wert in `i` gelangen, bevor wir 1 dazuaddieren
können, wie in
[„Das Dereferenzieren eines Zeigers greift auf seine Daten zu“][deref]
beschrieben.

Wir können auch über veränderliche Referenzen auf jedes Element in einem
veränderlichen Vektor iterieren, um alle Elemente zu ändern. Die `for`-Schleife
in Listing 8-8 addiert zu jedem Element `50`.

<Listing number="8-8" caption="Über veränderliche Referenzen auf die Elemente eines Vektors iterieren">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-08/src/main.rs:here}}
```

</Listing>

Um den Wert zu ändern, auf den die veränderliche Referenz verweist, verwenden
wir wieder den Dereferenzierungsoperator `*`, um zum Wert in `i` zu gelangen,
bevor wir den Operator `+=` verwenden können.

{{#quiz ../quizzes/ch08-01-vec-sec1.toml}}

### Iteratoren sicher verwenden {#safely-using-iterators}

Wie Iteratoren funktionieren, besprechen wir ausführlicher in Kapitel 13.2
[„Eine Folge von Elementen mit Iteratoren verarbeiten“](ch13-02-iterators.html).
Ein wichtiges Detail vorab: Iteratoren enthalten einen Zeiger auf Daten
innerhalb des Vektors. Wie Iteratoren funktionieren, sehen wir, wenn wir eine
for-Schleife in die entsprechenden Methodenaufrufe von [`Vec::iter`] und
[`Iterator::next`] auflösen (den syntaktischen Zucker entfernen):

```aquascope,interpreter,horizontal
#fn main() {
#use std::slice::Iter;  
let mut v: Vec<i32>         = vec![1, 2];
let mut iter: Iter<'_, i32> = v.iter();`[]`
let n1: &i32                = iter.next().unwrap();`[]`
let n2: &i32                = iter.next().unwrap();`[]`
let end: Option<&i32>       = iter.next();`[]`
#}
```

Beachte, dass der Iterator `iter` ein Zeiger ist, der sich durch jedes Element
des Vektors bewegt. Die Methode `next` rückt den Iterator weiter und gibt eine
optionale Referenz auf das vorherige Element zurück, entweder `Some` (das wir
mit unwrap auspacken) oder am Ende des Vektors `None`.

Dieses Detail ist wichtig, um Vektoren sicher zu verwenden. Angenommen, wir
wollten einen Vektor an Ort und Stelle verdoppeln, sodass etwa aus `[1, 2]` der
Vektor `[1, 2, 1, 2]` wird. Eine naive Implementierung könnte so aussehen,
annotiert mit den Berechtigungen, die der Compiler ableitet:

```aquascope,permissions,stepper,boundaries,shouldFail
fn dup_in_place(v: &mut Vec<i32>) {
    for n_ref in v.iter() {`(focus,paths:*v)`
        v.push(*n_ref);`{}`
    }
}
```

Beachte, dass `v.iter()` die Berechtigung @Perm{write} von `*v` entfernt. Daher
fehlt der Operation `v.push(..)` die erwartete Berechtigung @Perm{write}. Der
Rust-Compiler weist dieses Programm mit einer entsprechenden Fehlermeldung
zurück:

```text
error[E0502]: cannot borrow `*v` as mutable because it is also borrowed as immutable
 --> test.rs:3:9
  |
2 |     for n_ref in v.iter() {
  |                  --------
  |                  |
  |                  immutable borrow occurs here
  |                  immutable borrow later used here
3 |         v.push(*n_ref);
  |         ^^^^^^^^^^^^^^ mutable borrow occurs here
```

Wie wir in Kapitel 4 besprochen haben, steckt hinter diesem Fehler das
Sicherheitsproblem, freigegebenen Speicher zu lesen. Sobald `v.push(1)`
ausgeführt wird, legt der Vektor seinen Inhalt neu an und macht den Zeiger des
Iterators ungültig. Damit Iteratoren sicher verwendet werden können, erlaubt
Rust also nicht, während der Iteration Elemente zum Vektor hinzuzufügen oder
daraus zu entfernen.

<!-- TODO: add loop support and make this diagram look reasonable -->
<!-- ```aquascope,interpreter,shouldFail,horizontal
fn dup_in_place(v: &mut Vec<i32>) {`[]`
    for n_ref in v.iter() {
        v.push(*n_ref);
    }`[]`
}
fn main() {
    let mut v = vec![1, 2, 3];
    dup_in_place(&mut v);
}
``` -->

Eine Möglichkeit, ohne Zeiger über einen Vektor zu iterieren, ist ein Bereich
(_range_), wie wir ihn für String-Slices in
[Kapitel 4.4](ch04-04-slices.html#range-syntax) verwendet haben. Der Bereich
`0 .. v.len()` ist zum Beispiel ein Iterator über alle Indizes eines Vektors
`v`, wie hier zu sehen:

```aquascope,interpreter,horizontal
#fn main() {
#use std::ops::Range; 
let mut v: Vec<i32>        = vec![1, 2];
let mut iter: Range<usize> = 0 .. v.len();`[]`
let i1: usize              = iter.next().unwrap();
let n1: &i32               = &v[i1];`[]`
#}
```

### Mit einem Enum mehrere Typen speichern {#using-an-enum-to-store-multiple-types}

Vektoren können nur Werte desselben Typs speichern. Das kann unpraktisch sein;
es gibt durchaus Anwendungsfälle, in denen man eine Liste von Einträgen
unterschiedlicher Typen speichern muss. Zum Glück sind die Varianten eines Enums
unter demselben Enum-Typ definiert. Wenn wir also einen Typ brauchen, der
Elemente unterschiedlicher Typen darstellt, können wir ein Enum definieren und
verwenden!

Angenommen, wir wollen Werte aus einer Zeile einer Tabellenkalkulation lesen, in
der einige Spalten der Zeile Ganzzahlen, einige Gleitkommazahlen und einige
Strings enthalten. Wir können ein Enum definieren, dessen Varianten die
unterschiedlichen Werttypen aufnehmen, und alle Enum-Varianten gelten als
derselbe Typ: der des Enums. Dann können wir einen Vektor erstellen, der dieses
Enum aufnimmt und damit letztlich unterschiedliche Typen. Das haben wir in
Listing 8-9 gezeigt.

<Listing number="8-9" caption="Ein Enum definieren, um Werte unterschiedlicher Typen in einem Vektor zu speichern">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-09/src/main.rs:here}}
```

</Listing>

Rust muss zur Kompilierzeit wissen, welche Typen im Vektor stehen werden, damit
es genau weiß, wie viel Speicher auf dem Heap für jedes Element benötigt wird.
Wir müssen außerdem explizit angeben, welche Typen in diesem Vektor erlaubt
sind. Würde Rust erlauben, dass ein Vektor beliebige Typen enthält, bestünde die
Gefahr, dass einer oder mehrere der Typen bei den Operationen auf den Elementen
des Vektors Fehler verursachen. Ein Enum zusammen mit einem `match`-Ausdruck
bedeutet, dass Rust zur Kompilierzeit sicherstellt, dass jeder mögliche Fall
behandelt wird, wie in Kapitel 6 besprochen.

Wenn du die vollständige Menge der Typen, die ein Programm zur Laufzeit in einem
Vektor speichern soll, nicht kennst, funktioniert die Enum-Technik nicht.
Stattdessen kannst du ein Trait-Objekt verwenden, das wir in Kapitel 18
behandeln.

Nachdem wir einige der gängigsten Arten besprochen haben, Vektoren zu verwenden,
sieh dir unbedingt [die API-Dokumentation][vec-api]<!-- ignore --> mit all den
vielen nützlichen Methoden an, die die Standardbibliothek für `Vec<T>`
definiert. Zusätzlich zu `push` gibt es zum Beispiel eine Methode `pop`, die das
letzte Element entfernt und zurückgibt.

### Wird ein Vektor verworfen, werden seine Elemente verworfen {#dropping-a-vector-drops-its-elements}

Wie jedes andere `struct` wird ein Vektor freigegeben, wenn er den
Gültigkeitsbereich verlässt, wie in Listing 8-10 annotiert.

<Listing number="8-10" caption="Zeigt, wo der Vektor und seine Elemente verworfen werden">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-10/src/main.rs:here}}
```

</Listing>

Wenn der Vektor verworfen (_dropped_) wird, wird auch sein gesamter Inhalt
verworfen, das heißt, die Ganzzahlen, die er enthält, werden aufgeräumt. Der
Borrow-Checker stellt sicher, dass alle Referenzen auf den Inhalt eines Vektors
nur verwendet werden, solange der Vektor selbst gültig ist.

Weiter geht es mit dem nächsten Collection-Typ: `String`!

{{#quiz ../quizzes/ch08-01-vec-sec2.toml}}

[data-types]: ch03-02-data-types.html#data-types
[nomicon]: https://doc.rust-lang.org/nomicon/vec/vec.html
[vec-api]: https://doc.rust-lang.org/std/vec/struct.Vec.html
[deref]: ch04-02-references-and-borrowing.html#dereferencing-a-pointer-accesses-its-data
[`Vec::iter`]: https://doc.rust-lang.org/std/vec/struct.Vec.html#method.iter
[`Iterator::next`]: https://doc.rust-lang.org/std/iter/trait.Iterator.html#tymethod.next
