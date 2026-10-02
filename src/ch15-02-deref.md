<!-- Old headings. Do not remove or links may break. -->

<a id="treating-smart-pointers-like-regular-references-with-the-deref-trait"></a>
<a id="treating-smart-pointers-like-regular-references-with-deref"></a>

## Smart-Pointer wie normale Referenzen behandeln {#treating-smart-pointers-like-regular-references}

Wenn du den Trait `Deref` implementierst, kannst du das Verhalten des
_Dereferenzierungsoperators_ `*` anpassen (nicht zu verwechseln mit dem
Multiplikations- oder dem Glob-Operator). Indem du `Deref` so implementierst,
dass sich ein Smart-Pointer wie eine normale Referenz behandeln lässt, kannst du
Code schreiben, der mit Referenzen arbeitet, und diesen Code auch mit
Smart-Pointern verwenden.

Sehen wir uns zuerst an, wie der Dereferenzierungsoperator mit normalen
Referenzen funktioniert. Dann versuchen wir, einen eigenen Typ zu definieren,
der sich wie `Box<T>` verhält, und sehen, warum der Dereferenzierungsoperator
bei unserem neu definierten Typ nicht wie bei einer Referenz funktioniert. Wir
erkunden, wie die Implementierung des Traits `Deref` es Smart-Pointern
ermöglicht, ähnlich wie Referenzen zu funktionieren. Dann sehen wir uns das
Feature Deref-Coercion von Rust an und wie wir damit entweder mit Referenzen
oder mit Smart-Pointern arbeiten können.

<!-- Old headings. Do not remove or links may break. -->

<a id="following-the-pointer-to-the-value-with-the-dereference-operator"></a>
<a id="following-the-pointer-to-the-value"></a>

### Der Referenz zum Wert folgen {#following-the-reference-to-the-value}

Eine normale Referenz ist eine Art von Zeiger, und man kann sich einen Zeiger
als Pfeil auf einen Wert vorstellen, der woanders gespeichert ist. In Listing
15-6 erzeugen wir eine Referenz auf einen `i32`-Wert und verwenden dann den
Dereferenzierungsoperator, um der Referenz zum Wert zu folgen.

<Listing number="15-6" file-name="src/main.rs" caption="Mit dem Dereferenzierungsoperator einer Referenz auf einen `i32`-Wert folgen">

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-06/src/main.rs}}
```

</Listing>

Die Variable `x` enthält den `i32`-Wert `5`. Wir setzen `y` gleich einer
Referenz auf `x`. Wir können zusichern, dass `x` gleich `5` ist. Wollen wir aber
eine Assertion über den Wert in `y` machen, müssen wir `*y` verwenden, um der
Referenz zu dem Wert zu folgen, auf den sie zeigt (daher _dereferenzieren_),
damit der Compiler den tatsächlichen Wert vergleichen kann. Sobald wir `y`
dereferenzieren, haben wir Zugriff auf den Ganzzahlwert, auf den `y` zeigt, und
können ihn mit `5` vergleichen.

Würden wir stattdessen versuchen, `assert_eq!(5, y);` zu schreiben, bekämen wir
diesen Kompilierfehler:

```console
{{#include ../listings/ch15-smart-pointers/output-only-01-comparing-to-reference/output.txt}}
```

Eine Zahl mit einer Referenz auf eine Zahl zu vergleichen, ist nicht erlaubt,
weil es verschiedene Typen sind. Wir müssen den Dereferenzierungsoperator
verwenden, um der Referenz zu dem Wert zu folgen, auf den sie zeigt.

### `Box<T>` wie eine Referenz verwenden {#using-boxt-like-a-reference}

Wir können den Code in Listing 15-6 so umschreiben, dass er statt einer Referenz
eine `Box<T>` verwendet; der Dereferenzierungsoperator auf der `Box<T>` in
Listing 15-7 funktioniert genauso wie der Dereferenzierungsoperator auf der
Referenz in Listing 15-6.

<Listing number="15-7" file-name="src/main.rs" caption="Den Dereferenzierungsoperator auf eine `Box<i32>` anwenden">

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-07/src/main.rs}}
```

</Listing>

Der Hauptunterschied zwischen Listing 15-7 und Listing 15-6 ist, dass wir `y`
hier auf eine Instanz einer Box setzen, die auf einen kopierten Wert von `x`
zeigt, statt auf eine Referenz, die auf den Wert von `x` zeigt. In der letzten
Assertion können wir den Dereferenzierungsoperator verwenden, um dem Zeiger der
Box auf dieselbe Weise zu folgen wie damals, als `y` eine Referenz war. Als
Nächstes erkunden wir, was das Besondere an `Box<T>` ist, das uns erlaubt, den
Dereferenzierungsoperator zu verwenden, indem wir unseren eigenen Box-Typ
definieren.

### Einen eigenen Smart-Pointer definieren {#defining-our-own-smart-pointer}

Bauen wir einen Wrapper-Typ ähnlich dem Typ `Box<T>` aus der Standardbibliothek,
um zu erleben, wie sich Smart-Pointer-Typen standardmäßig anders verhalten als
Referenzen. Dann sehen wir uns an, wie man die Möglichkeit hinzufügt, den
Dereferenzierungsoperator zu verwenden.

> Note: Es gibt einen großen Unterschied zwischen dem Typ `MyBox<T>`, den wir
> gleich bauen, und dem echten `Box<T>`: Unsere Version speichert ihre Daten
> nicht auf dem Heap. In diesem Beispiel konzentrieren wir uns auf `Deref`,
> daher ist weniger wichtig, wo die Daten tatsächlich gespeichert werden, als
> das zeigerähnliche Verhalten.

Der Typ `Box<T>` ist letztlich als Tupel-Struct mit einem Element definiert,
daher definiert Listing 15-8 einen Typ `MyBox<T>` auf dieselbe Weise. Außerdem
definieren wir eine Funktion `new`, die der auf `Box<T>` definierten Funktion
`new` entspricht.

<Listing number="15-8" file-name="src/main.rs" caption="Einen Typ `MyBox<T>` definieren">

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-08/src/main.rs:here}}
```

</Listing>

Wir definieren ein Struct namens `MyBox` und deklarieren einen generischen
Parameter `T`, weil unser Typ Werte beliebigen Typs aufnehmen soll. Der Typ
`MyBox` ist ein Tupel-Struct mit einem Element vom Typ `T`. Die Funktion
`MyBox::new` nimmt einen Parameter vom Typ `T` und gibt eine `MyBox`-Instanz
zurück, die den übergebenen Wert enthält.

Versuchen wir, die Funktion `main` aus Listing 15-7 zu Listing 15-8 hinzuzufügen
und sie so zu ändern, dass sie statt `Box<T>` den von uns definierten Typ
`MyBox<T>` verwendet. Der Code in Listing 15-9 kompiliert nicht, weil Rust nicht
weiß, wie man `MyBox` dereferenziert.

<Listing number="15-9" file-name="src/main.rs" caption="Versuch, `MyBox<T>` genauso zu verwenden wie Referenzen und `Box<T>`">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-09/src/main.rs:here}}
```

</Listing>

Hier ist der resultierende Kompilierfehler:

```console
{{#include ../listings/ch15-smart-pointers/listing-15-09/output.txt}}
```

Unser Typ `MyBox<T>` kann nicht dereferenziert werden, weil wir diese Fähigkeit
für unseren Typ nicht implementiert haben. Um das Dereferenzieren mit dem
Operator `*` zu ermöglichen, implementieren wir den Trait `Deref`.

<!-- Old headings. Do not remove or links may break. -->

<a id="treating-a-type-like-a-reference-by-implementing-the-deref-trait"></a>

### Den Trait `Deref` implementieren {#implementing-the-deref-trait}

Wie in [„Einen Trait für einen Typ implementieren“][impl-trait]<!-- ignore -->
in Kapitel 10 besprochen, müssen wir zum Implementieren eines Traits
Implementierungen für die erforderlichen Methoden des Traits bereitstellen. Der
Trait `Deref` aus der Standardbibliothek verlangt, dass wir eine Methode namens
`deref` implementieren, die `self` ausleiht (_borrows_) und eine Referenz auf
die inneren Daten zurückgibt. Listing 15-10 enthält eine Implementierung von
`Deref`, die wir der Definition von `MyBox<T>` hinzufügen.

<Listing number="15-10" file-name="src/main.rs" caption="`Deref` für `MyBox<T>` implementieren">

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-10/src/main.rs:here}}
```

</Listing>

Die Syntax `type Target = T;` definiert einen assoziierten Typ, den der Trait
`Deref` verwendet. Assoziierte Typen sind eine etwas andere Art, einen
generischen Parameter zu deklarieren, aber darum musst du dir vorerst keine
Gedanken machen; wir behandeln sie ausführlicher in Kapitel 20.

Wir füllen den Rumpf der Methode `deref` mit `&self.0`, sodass `deref` eine
Referenz auf den Wert zurückgibt, auf den wir mit dem Operator `*` zugreifen
wollen; erinnere dich aus
[„Verschiedene Typen mit Tupel-Structs erzeugen“][tuple-structs]<!--
ignore --> in Kapitel 5, dass `.0` auf den ersten Wert in einem Tupel-Struct
zugreift. Die Funktion `main` in Listing 15-9, die `*` auf dem `MyBox<T>`-Wert
aufruft, kompiliert jetzt, und die Assertions bestehen!

Ohne den Trait `Deref` kann der Compiler nur `&`-Referenzen dereferenzieren. Die
Methode `deref` gibt dem Compiler die Möglichkeit, einen Wert jedes Typs, der
`Deref` implementiert, zu nehmen und die Methode `deref` aufzurufen, um eine
Referenz zu erhalten, die er zu dereferenzieren weiß.

Als wir in Listing 15-9 `*y` eingegeben haben, hat Rust hinter den Kulissen
tatsächlich diesen Code ausgeführt:

```rust,ignore
*(y.deref())
```

Rust ersetzt den Operator `*` durch einen Aufruf der Methode `deref` und dann
eine einfache Dereferenzierung, sodass wir nicht darüber nachdenken müssen, ob
wir die Methode `deref` aufrufen müssen oder nicht. Mit diesem Feature von Rust
können wir Code schreiben, der genauso funktioniert, egal ob wir eine normale
Referenz oder einen Typ haben, der `Deref` implementiert.

Dass die Methode `deref` eine Referenz auf einen Wert zurückgibt und die
einfache Dereferenzierung außerhalb der Klammern in `*(y.deref())` trotzdem
nötig ist, hat mit dem Ownership-System zu tun. Würde die Methode `deref` den
Wert direkt statt einer Referenz auf den Wert zurückgeben, würde der Wert aus
`self` herausverschoben (_moved_). Wir wollen in diesem Fall und in den meisten
Fällen, in denen wir den Dereferenzierungsoperator verwenden, nicht die
Ownership des inneren Werts in `MyBox<T>` übernehmen.

Beachte, dass der Operator `*` jedes Mal, wenn wir in unserem Code ein `*`
verwenden, nur einmal durch einen Aufruf der Methode `deref` und dann einen
Aufruf des Operators `*` ersetzt wird. Da die Ersetzung des Operators `*` nicht
unendlich rekursiv ist, erhalten wir am Ende Daten vom Typ `i32`, die zur `5` in
`assert_eq!` in Listing 15-9 passen.

<!-- Old headings. Do not remove or links may break. -->

<a id="implicit-deref-coercions-with-functions-and-methods"></a>
<a id="using-deref-coercions-in-functions-and-methods"></a>

### Deref-Coercion in Funktionen und Methoden verwenden {#using-deref-coercion-in-functions-and-methods}

_Deref-Coercion_ wandelt eine Referenz auf einen Typ, der den Trait `Deref`
implementiert, in eine Referenz auf einen anderen Typ um. Deref-Coercion kann
zum Beispiel `&String` in `&str` umwandeln, weil `String` den Trait `Deref` so
implementiert, dass er `&str` zurückgibt. Deref-Coercion ist eine
Bequemlichkeit, die Rust bei Argumenten von Funktionen und Methoden anwendet,
und sie funktioniert nur bei Typen, die den Trait `Deref` implementieren. Sie
geschieht automatisch, wenn wir einer Funktion oder Methode eine Referenz auf
den Wert eines bestimmten Typs als Argument übergeben, der nicht zum
Parametertyp in der Definition der Funktion oder Methode passt. Eine Folge von
Aufrufen der Methode `deref` wandelt den übergebenen Typ in den Typ um, den der
Parameter braucht.

Deref-Coercion wurde zu Rust hinzugefügt, damit Programmierende beim Schreiben
von Funktions- und Methodenaufrufen nicht so viele explizite Referenzen und
Dereferenzierungen mit `&` und `*` hinzufügen müssen. Mit dem Feature
Deref-Coercion können wir außerdem mehr Code schreiben, der sowohl mit
Referenzen als auch mit Smart-Pointern funktioniert.

Um Deref-Coercion in Aktion zu sehen, verwenden wir den Typ `MyBox<T>`, den wir
in Listing 15-8 definiert haben, sowie die Implementierung von `Deref`, die wir
in Listing 15-10 hinzugefügt haben. Listing 15-11 zeigt die Definition einer
Funktion mit einem String-Slice-Parameter.

<Listing number="15-11" file-name="src/main.rs" caption="Eine Funktion `hello` mit dem Parameter `name` vom Typ `&str`">

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-11/src/main.rs:here}}
```

</Listing>

Wir können die Funktion `hello` mit einem String-Slice als Argument aufrufen,
zum Beispiel `hello("Rust");`. Deref-Coercion ermöglicht es, `hello` mit einer
Referenz auf einen Wert vom Typ `MyBox<String>` aufzurufen, wie in Listing 15-12
gezeigt.

<Listing number="15-12" file-name="src/main.rs" caption="`hello` mit einer Referenz auf einen `MyBox<String>`-Wert aufrufen, was dank Deref-Coercion funktioniert">

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-12/src/main.rs:here}}
```

</Listing>

Hier rufen wir die Funktion `hello` mit dem Argument `&m` auf, einer Referenz
auf einen `MyBox<String>`-Wert. Da wir in Listing 15-10 den Trait `Deref` für
`MyBox<T>` implementiert haben, kann Rust `&MyBox<String>` durch Aufruf von
`deref` in `&String` umwandeln. Die Standardbibliothek stellt eine
Implementierung von `Deref` für `String` bereit, die einen String-Slice
zurückgibt; sie steht in der API-Dokumentation zu `Deref`. Rust ruft erneut
`deref` auf, um den `&String` in `&str` umzuwandeln, was zur Definition der
Funktion `hello` passt.

Würde Rust keine Deref-Coercion implementieren, müssten wir den Code in Listing
15-13 statt des Codes in Listing 15-12 schreiben, um `hello` mit einem Wert vom
Typ `&MyBox<String>` aufzurufen.

<Listing number="15-13" file-name="src/main.rs" caption="Der Code, den wir schreiben müssten, wenn Rust keine Deref-Coercion hätte">

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-13/src/main.rs:here}}
```

</Listing>

`(*m)` dereferenziert die `MyBox<String>` zu einem `String`. Dann bilden `&` und
`[..]` einen String-Slice des `String`, der dem gesamten String entspricht, um
zur Signatur von `hello` zu passen. Dieser Code ohne Deref-Coercions ist mit all
diesen Symbolen schwerer zu lesen, zu schreiben und zu verstehen. Mit
Deref-Coercion kann Rust diese Umwandlungen automatisch für uns erledigen.

Wenn der Trait `Deref` für die beteiligten Typen definiert ist, analysiert Rust
die Typen und verwendet `Deref::deref` so oft wie nötig, um eine Referenz zu
erhalten, die zum Typ des Parameters passt. Wie oft `Deref::deref` eingefügt
werden muss, wird zur Kompilierzeit aufgelöst, daher kostet es zur Laufzeit
nichts, Deref-Coercion zu nutzen!

<!-- Old headings. Do not remove or links may break. -->

<a id="how-deref-coercion-interacts-with-mutability"></a>

### Deref-Coercion mit veränderlichen Referenzen {#handling-deref-coercion-with-mutable-references}

Ähnlich wie du mit dem Trait `Deref` den Operator `*` bei unveränderlichen
(_immutable_) Referenzen überschreibst, kannst du mit dem Trait `DerefMut` den
Operator `*` bei veränderlichen (_mutable_) Referenzen überschreiben.

Rust wendet Deref-Coercion an, wenn es in drei Fällen Typen und
Trait-Implementierungen findet:

1. Von `&T` zu `&U`, wenn `T: Deref<Target=U>`
2. Von `&mut T` zu `&mut U`, wenn `T: DerefMut<Target=U>`
3. Von `&mut T` zu `&U`, wenn `T: Deref<Target=U>`

Die ersten beiden Fälle sind gleich, außer dass der zweite Veränderlichkeit
implementiert. Der erste Fall besagt: Hast du ein `&T` und implementiert `T`
`Deref` zu einem Typ `U`, kannst du transparent ein `&U` erhalten. Der zweite
Fall besagt, dass dieselbe Deref-Coercion bei veränderlichen Referenzen
geschieht.

Der dritte Fall ist kniffliger: Rust wandelt auch eine veränderliche Referenz in
eine unveränderliche um. Umgekehrt ist das aber _nicht_ möglich: Unveränderliche
Referenzen werden nie in veränderliche Referenzen umgewandelt. Wegen der
Borrowing-Regeln muss eine veränderliche Referenz, wenn du eine hast, die
einzige Referenz auf diese Daten sein (andernfalls würde das Programm nicht
kompilieren). Eine veränderliche Referenz in eine unveränderliche Referenz
umzuwandeln, verletzt die Borrowing-Regeln nie. Eine unveränderliche Referenz in
eine veränderliche Referenz umzuwandeln, würde voraussetzen, dass die
ursprüngliche unveränderliche Referenz die einzige unveränderliche Referenz auf
diese Daten ist, aber das garantieren die Borrowing-Regeln nicht. Daher kann
Rust nicht annehmen, dass die Umwandlung einer unveränderlichen Referenz in eine
veränderliche Referenz möglich ist.

{{#quiz ../quizzes/ch15-02-deref.toml}}

[impl-trait]: ch10-02-traits.html#implementing-a-trait-on-a-type
[tuple-structs]: ch05-01-defining-structs.html#creating-different-types-with-tuple-structs
