## Mit `Box<T>` auf Daten im Heap zeigen {#using-boxt-to-point-to-data-on-the-heap}

Der einfachste Smart-Pointer ist eine Box, deren Typ `Box<T>` geschrieben wird.
Mit _Boxen_ kannst du Daten auf dem Heap statt auf dem Stack speichern. Was auf
dem Stack bleibt, ist der Zeiger auf die Daten im Heap. In Kapitel 4 kannst du
den Unterschied zwischen Stack und Heap noch einmal nachlesen.

Boxen verursachen keinen Performance-Mehraufwand, abgesehen davon, dass sie ihre
Daten auf dem Heap statt auf dem Stack speichern. Sie haben aber auch nicht
viele zusätzliche Fähigkeiten. Du verwendest sie am häufigsten in diesen
Situationen:

- Wenn du einen Typ hast, dessen Größe zur Kompilierzeit nicht bekannt sein
  kann, und du einen Wert dieses Typs in einem Kontext verwenden willst, der
  eine genaue Größe verlangt
- Wenn du eine große Datenmenge hast und die Ownership übertragen, dabei aber
  sicherstellen willst, dass die Daten nicht kopiert werden
- Wenn du einen Wert besitzen willst und dir nur wichtig ist, dass sein Typ
  einen bestimmten Trait implementiert, nicht, dass er einen bestimmten Typ hat

Die erste Situation zeigen wir in
[„Rekursive Typen mit Boxen ermöglichen“](#enabling-recursive-types-with-boxes)<!-- ignore -->.
Im zweiten Fall kann das Übertragen der Ownership einer großen Datenmenge lange
dauern, weil die Daten auf dem Stack herumkopiert werden. Um die Performance in
dieser Situation zu verbessern, können wir die große Datenmenge in einer Box auf
dem Heap speichern. Dann wird nur die kleine Menge an Zeigerdaten auf dem Stack
herumkopiert, während die Daten, auf die er verweist, an einer Stelle auf dem
Heap bleiben. Der dritte Fall heißt _Trait-Objekt_ (_trait object_), und
[„Mit Trait-Objekten über gemeinsames Verhalten abstrahieren“][trait-objects]<!-- ignore -->
in Kapitel 18 ist diesem Thema gewidmet. Was du hier lernst, wendest du in
diesem Abschnitt also wieder an!

<!-- Old headings. Do not remove or links may break. -->

<a id="using-boxt-to-store-data-on-the-heap"></a>

### Daten auf dem Heap speichern {#storing-data-on-the-heap}

Bevor wir den Anwendungsfall der Speicherung auf dem Heap für `Box<T>`
besprechen, behandeln wir die Syntax und den Umgang mit Werten, die in einer
`Box<T>` gespeichert sind.

Listing 15-1 zeigt, wie man mit einer Box einen `i32`-Wert auf dem Heap
speichert.

<Listing number="15-1" file-name="src/main.rs" caption="Einen `i32`-Wert mit einer Box auf dem Heap speichern">

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-01/src/main.rs}}
```

</Listing>

Wir definieren die Variable `b` so, dass sie den Wert einer `Box` hat, die auf
den Wert `5` zeigt, der auf dem Heap alloziert ist. Dieses Programm gibt `b = 5`
aus; in diesem Fall können wir auf die Daten in der Box ähnlich zugreifen, als
lägen die Daten auf dem Stack. Wie jeder besessene Wert wird eine Box
freigegeben, wenn sie den Gültigkeitsbereich (_scope_) verlässt, wie `b` am Ende
von `main`. Die Freigabe betrifft sowohl die Box (die auf dem Stack gespeichert
ist) als auch die Daten, auf die sie zeigt (die auf dem Heap gespeichert sind).

Einen einzelnen Wert auf den Heap zu legen, ist nicht sehr nützlich, daher wirst
du Boxen nicht oft auf diese Weise für sich allein verwenden. Werte wie einen
einzelnen `i32` auf dem Stack zu haben, wo sie standardmäßig gespeichert werden,
ist in den meisten Situationen angemessener. Sehen wir uns einen Fall an, in dem
wir mit Boxen Typen definieren können, die wir ohne Boxen nicht definieren
dürften.

### Rekursive Typen mit Boxen ermöglichen {#enabling-recursive-types-with-boxes}

Ein Wert eines _rekursiven Typs_ (_recursive type_) kann einen anderen Wert
desselben Typs als Teil seiner selbst enthalten. Rekursive Typen sind ein
Problem, weil Rust zur Kompilierzeit wissen muss, wie viel Platz ein Typ belegt.
Die Verschachtelung von Werten rekursiver Typen könnte aber theoretisch
unendlich weitergehen, daher kann Rust nicht wissen, wie viel Platz der Wert
braucht. Da Boxen eine bekannte Größe haben, können wir rekursive Typen
ermöglichen, indem wir eine Box in die rekursive Typdefinition einfügen.

Als Beispiel für einen rekursiven Typ sehen wir uns die Cons-Liste an. Das ist
ein Datentyp, der häufig in funktionalen Programmiersprachen vorkommt. Der
Cons-Listen-Typ, den wir definieren, ist abgesehen von der Rekursion einfach;
daher sind die Konzepte im Beispiel, mit dem wir arbeiten, immer dann nützlich,
wenn du in komplexere Situationen mit rekursiven Typen gerätst.

<!-- Old headings. Do not remove or links may break. -->

<a id="more-information-about-the-cons-list"></a>

#### Die Cons-Liste verstehen {#understanding-the-cons-list}

Eine _Cons-Liste_ ist eine Datenstruktur aus der Programmiersprache Lisp und
ihren Dialekten. Sie besteht aus verschachtelten Paaren und ist die Lisp-Version
einer verketteten Liste. Ihr Name stammt von der Funktion `cons` (kurz für
_construct function_, Konstruktionsfunktion) in Lisp, die aus ihren zwei
Argumenten ein neues Paar konstruiert. Indem wir `cons` auf ein Paar aus einem
Wert und einem anderen Paar aufrufen, können wir Cons-Listen aus rekursiven
Paaren konstruieren.

Hier ist zum Beispiel eine Pseudocode-Darstellung einer Cons-Liste, die die
Liste `1, 2, 3` enthält, wobei jedes Paar in Klammern steht:

```text
(1, (2, (3, Nil)))
```

Jeder Eintrag in einer Cons-Liste enthält zwei Elemente: den Wert des aktuellen
Eintrags und den nächsten Eintrag. Der letzte Eintrag in der Liste enthält nur
einen Wert namens `Nil` ohne nächsten Eintrag. Eine Cons-Liste wird durch
rekursives Aufrufen der Funktion `cons` erzeugt. Der übliche Name für den
Basisfall der Rekursion ist `Nil`. Beachte, dass das nicht dasselbe ist wie das
in Kapitel 6 besprochene Konzept „null“ oder „nil“, also ein ungültiger oder
fehlender Wert.

Die Cons-Liste ist in Rust keine häufig verwendete Datenstruktur. Wenn du in
Rust eine Liste von Einträgen hast, ist `Vec<T>` meistens die bessere Wahl.
Andere, komplexere rekursive Datentypen _sind_ in verschiedenen Situationen
nützlich, aber wenn wir in diesem Kapitel mit der Cons-Liste beginnen, können
wir ohne viel Ablenkung erkunden, wie wir mit Boxen einen rekursiven Datentyp
definieren können.

Listing 15-2 enthält eine Enum-Definition für eine Cons-Liste. Beachte, dass
dieser Code noch nicht kompiliert, weil der Typ `List` keine bekannte Größe hat,
wie wir zeigen werden.

<Listing number="15-2" file-name="src/main.rs" caption="Der erste Versuch, ein Enum zu definieren, das eine Cons-Liste von `i32`-Werten darstellt">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-02/src/main.rs:here}}
```

</Listing>

> Note: Für dieses Beispiel implementieren wir eine Cons-Liste, die nur
> `i32`-Werte enthält. Wir hätten sie mit Generics implementieren können, wie in
> Kapitel 10 besprochen, um einen Cons-Listen-Typ zu definieren, der Werte
> beliebigen Typs speichern kann.

Mit dem Typ `List` die Liste `1, 2, 3` zu speichern, sähe aus wie der Code in
Listing 15-3.

<Listing number="15-3" file-name="src/main.rs" caption="Das Enum `List` verwenden, um die Liste `1, 2, 3` zu speichern">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-03/src/main.rs:here}}
```

</Listing>

Der erste `Cons`-Wert enthält `1` und einen weiteren `List`-Wert. Dieser
`List`-Wert ist ein weiterer `Cons`-Wert, der `2` und einen weiteren `List`-Wert
enthält. Dieser `List`-Wert ist noch ein `Cons`-Wert, der `3` und einen
`List`-Wert enthält, der schließlich `Nil` ist, die nicht rekursive Variante,
die das Ende der Liste signalisiert.

Wenn wir versuchen, den Code in Listing 15-3 zu kompilieren, erhalten wir den
Fehler aus Listing 15-4.

<Listing number="15-4" caption="Der Fehler, den wir beim Versuch erhalten, ein rekursives Enum zu definieren">

```console
{{#include ../listings/ch15-smart-pointers/listing-15-03/output.txt}}
```

</Listing>

Der Fehler zeigt, dass dieser Typ „unendlich groß ist“ (_has infinite size_).
Der Grund ist, dass wir `List` mit einer rekursiven Variante definiert haben:
Sie enthält direkt einen weiteren Wert ihrer selbst. Daher kann Rust nicht
herausfinden, wie viel Platz es zum Speichern eines `List`-Werts braucht.
Schlüsseln wir auf, warum wir diesen Fehler bekommen. Zuerst sehen wir uns an,
wie Rust entscheidet, wie viel Platz es zum Speichern eines Werts eines nicht
rekursiven Typs braucht.

#### Die Größe eines nicht rekursiven Typs berechnen {#computing-the-size-of-a-non-recursive-type}

Erinnere dich an das Enum `Message`, das wir in Listing 6-2 definiert haben, als
wir in Kapitel 6 Enum-Definitionen besprochen haben:

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/listing-06-02/src/main.rs:here}}
```

Um festzustellen, wie viel Platz für einen `Message`-Wert alloziert werden muss,
geht Rust jede der Varianten durch, um zu sehen, welche Variante den meisten
Platz braucht. Rust sieht, dass `Message::Quit` keinen Platz braucht,
`Message::Move` genug Platz, um zwei `i32`-Werte zu speichern, und so weiter. Da
nur eine Variante verwendet wird, braucht ein `Message`-Wert höchstens den
Platz, den das Speichern seiner größten Variante benötigt.

Vergleiche das mit dem, was passiert, wenn Rust versucht festzustellen, wie viel
Platz ein rekursiver Typ wie das Enum `List` in Listing 15-2 braucht. Der
Compiler sieht sich zuerst die Variante `Cons` an, die einen Wert vom Typ `i32`
und einen Wert vom Typ `List` enthält. Daher braucht `Cons` so viel Platz wie
die Größe eines `i32` plus die Größe einer `List`. Um herauszufinden, wie viel
Speicher der Typ `List` braucht, sieht sich der Compiler die Varianten an,
beginnend mit der Variante `Cons`. Die Variante `Cons` enthält einen Wert vom
Typ `i32` und einen Wert vom Typ `List`, und dieser Vorgang setzt sich unendlich
fort, wie in Abbildung 15-1 gezeigt.

<img alt="Eine unendliche Cons-Liste: ein mit ‚Cons‘ beschriftetes Rechteck, das in zwei kleinere Rechtecke geteilt ist. Das erste kleinere Rechteck trägt die Beschriftung ‚i32‘, das zweite die Beschriftung ‚Cons‘ und eine kleinere Version des äußeren ‚Cons‘-Rechtecks. Die ‚Cons‘-Rechtecke enthalten immer kleinere Versionen ihrer selbst, bis das kleinste Rechteck in angemessener Größe ein Unendlichkeitszeichen enthält, das anzeigt, dass sich diese Wiederholung endlos fortsetzt." src="img/trpl15-01.svg" class="center" style="width: 50%;" />

<span class="caption">Abbildung 15-1: Eine unendliche `List` aus unendlich
vielen `Cons`-Varianten</span>

<!-- Old headings. Do not remove or links may break. -->

<a id="using-boxt-to-get-a-recursive-type-with-a-known-size"></a>

#### Einen rekursiven Typ mit bekannter Größe erhalten {#getting-a-recursive-type-with-a-known-size}

Da Rust nicht herausfinden kann, wie viel Platz für rekursiv definierte Typen
alloziert werden muss, gibt der Compiler einen Fehler mit diesem hilfreichen
Vorschlag aus:

<!-- manual-regeneration
after doing automatic regeneration, look at listings/ch15-smart-pointers/listing-15-03/output.txt and copy the relevant line
-->

```text
help: insert some indirection (e.g., a `Box`, `Rc`, or `&`) to break the cycle
  |
2 |     Cons(i32, Box<List>),
  |               ++++    +
```

In diesem Vorschlag bedeutet _Indirektion_ (_indirection_), dass wir einen Wert
nicht direkt speichern, sondern die Datenstruktur so ändern sollten, dass sie
den Wert indirekt speichert, indem sie stattdessen einen Zeiger auf den Wert
speichert.

Da eine `Box<T>` ein Zeiger ist, weiß Rust immer, wie viel Platz eine `Box<T>`
braucht: Die Größe eines Zeigers ändert sich nicht mit der Menge der Daten, auf
die er zeigt. Das bedeutet, dass wir in die Variante `Cons` eine `Box<T>` legen
können statt direkt einen weiteren `List`-Wert. Die `Box<T>` zeigt auf den
nächsten `List`-Wert, der auf dem Heap liegt statt innerhalb der Variante
`Cons`. Konzeptionell haben wir immer noch eine Liste, die aus Listen besteht,
die andere Listen enthalten, aber diese Implementierung ähnelt jetzt eher dem
Anordnen der Einträge nebeneinander statt ineinander.

Wir können die Definition des Enums `List` in Listing 15-2 und die Verwendung
von `List` in Listing 15-3 in den Code in Listing 15-5 ändern, der kompiliert.

<Listing number="15-5" file-name="src/main.rs" caption="Die Definition von `List`, die `Box<T>` verwendet, um eine bekannte Größe zu haben">

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-05/src/main.rs}}
```

</Listing>

Die Variante `Cons` braucht die Größe eines `i32` plus den Platz zum Speichern
der Zeigerdaten der Box. Die Variante `Nil` speichert keine Werte, braucht also
weniger Platz auf dem Stack als die Variante `Cons`. Wir wissen jetzt, dass
jeder `List`-Wert die Größe eines `i32` plus die Größe der Zeigerdaten einer Box
belegt. Durch die Box haben wir die unendliche, rekursive Kette durchbrochen,
sodass der Compiler herausfinden kann, welche Größe er zum Speichern eines
`List`-Werts braucht. Abbildung 15-2 zeigt, wie die Variante `Cons` jetzt
aussieht.

<img alt="Ein mit ‚Cons‘ beschriftetes Rechteck, das in zwei kleinere Rechtecke geteilt ist. Das erste kleinere Rechteck trägt die Beschriftung ‚i32‘, das zweite die Beschriftung ‚Box‘ mit einem inneren Rechteck, das die Beschriftung ‚usize‘ enthält und die endliche Größe des Zeigers der Box darstellt." src="img/trpl15-02.svg" class="center" />

<span class="caption">Abbildung 15-2: Eine `List`, die nicht unendlich groß ist,
weil `Cons` eine `Box` enthält</span>

Boxen stellen nur die Indirektion und die Allokation auf dem Heap bereit; sie
haben keine anderen besonderen Fähigkeiten, wie wir sie bei den anderen
Smart-Pointer-Typen sehen werden. Sie haben aber auch nicht den
Performance-Mehraufwand, den diese besonderen Fähigkeiten verursachen, und
können daher in Fällen wie der Cons-Liste nützlich sein, in denen die
Indirektion das einzige Feature ist, das wir brauchen. Weitere Anwendungsfälle
für Boxen sehen wir uns in Kapitel 18 an.

Der Typ `Box<T>` ist ein Smart-Pointer, weil er den Trait `Deref` implementiert,
wodurch sich `Box<T>`-Werte wie Referenzen behandeln lassen. Wenn ein
`Box<T>`-Wert den Gültigkeitsbereich verlässt, werden dank der Implementierung
des Traits `Drop` auch die Heap-Daten aufgeräumt, auf die die Box zeigt. Diese
beiden Traits sind für die Funktionalität der anderen Smart-Pointer-Typen, die
wir im Rest dieses Kapitels besprechen, sogar noch wichtiger. Sehen wir uns
diese beiden Traits genauer an.

{{#quiz ../quizzes/ch15-01-box.toml}}

[trait-objects]: ch18-02-trait-objects.html#using-trait-objects-to-abstract-over-shared-behavior
