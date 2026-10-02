## Pattern-Syntax {#pattern-syntax}

In diesem Abschnitt tragen wir die gesamte Syntax zusammen, die in Patterns
gültig ist, und besprechen, warum und wann du die einzelnen Formen verwenden
möchtest.

### Literale abgleichen {#matching-literals}

Wie du in Kapitel 6 gesehen hast, kannst du Patterns direkt mit Literalen
abgleichen. Der folgende Code zeigt einige Beispiele:

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/no-listing-01-literals/src/main.rs:here}}
```

Dieser Code gibt `one` aus, weil der Wert in `x` `1` ist. Diese Syntax ist
nützlich, wenn dein Code eine Aktion ausführen soll, sobald er einen bestimmten
konkreten Wert bekommt.

### Benannte Variablen abgleichen {#matching-named-variables}

Benannte Variablen sind unabweisbare Patterns, die auf jeden Wert passen, und
wir haben sie in diesem Buch schon oft verwendet. Es gibt jedoch eine
Komplikation, wenn du benannte Variablen in `match`-, `if let`- oder
`while let`-Ausdrücken verwendest. Weil jeder dieser Ausdrücke einen neuen
Gültigkeitsbereich (_scope_) beginnt, überschatten (_shadow_) Variablen, die als
Teil eines Patterns innerhalb dieser Ausdrücke deklariert werden, gleichnamige
Variablen außerhalb der Konstrukte, wie es bei allen Variablen der Fall ist. In
Listing 19-11 deklarieren wir eine Variable namens `x` mit dem Wert `Some(5)`
und eine Variable `y` mit dem Wert `10`. Dann erstellen wir einen
`match`-Ausdruck für den Wert `x`. Sieh dir die Patterns in den Match-Armen und
das `println!` am Ende an und versuche herauszufinden, was der Code ausgeben
wird, bevor du ihn ausführst oder weiterliest.

<Listing number="19-11" file-name="src/main.rs" caption="Ein `match`-Ausdruck mit einem Arm, der eine neue Variable einführt, die eine bestehende Variable `y` überschattet">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-11/src/main.rs:here}}
```

</Listing>

Gehen wir durch, was passiert, wenn der `match`-Ausdruck ausgeführt wird. Das
Pattern im ersten Match-Arm passt nicht auf den definierten Wert von `x`, also
geht der Code weiter.

Das Pattern im zweiten Match-Arm führt eine neue Variable namens `y` ein, die
auf jeden Wert innerhalb eines `Some`-Werts passt. Weil wir uns innerhalb des
`match`-Ausdrucks in einem neuen Gültigkeitsbereich befinden, ist das eine neue
Variable `y`, nicht das `y`, das wir am Anfang mit dem Wert `10` deklariert
haben. Diese neue Bindung `y` passt auf jeden Wert innerhalb eines `Some`, und
genau das haben wir in `x`. Daher wird dieses neue `y` an den inneren Wert des
`Some` in `x` gebunden. Dieser Wert ist `5`, also wird der Ausdruck für diesen
Arm ausgeführt und gibt `Matched, y = 5` aus.

Wäre `x` ein `None`-Wert statt `Some(5)` gewesen, hätten die Patterns in den
ersten beiden Armen nicht gepasst, und der Wert hätte auf den Unterstrich
gepasst. Wir haben im Pattern des Unterstrich-Arms keine Variable `x`
eingeführt, daher ist das `x` im Ausdruck immer noch das äußere `x`, das nicht
überschattet wurde. In diesem hypothetischen Fall würde der `match`
`Default case,
x = None` ausgeben.

Wenn der `match`-Ausdruck fertig ist, endet sein Gültigkeitsbereich und damit
auch der Gültigkeitsbereich des inneren `y`. Das letzte `println!` erzeugt
`at the end: x = Some(5), y = 10`.

Um einen `match`-Ausdruck zu erstellen, der die Werte des äußeren `x` und `y`
vergleicht, statt eine neue Variable einzuführen, die die bestehende Variable
`y` überschattet, müssten wir stattdessen eine Bedingung mit einem Match-Guard
verwenden. Über Match-Guards sprechen wir später im Abschnitt
[„Bedingungen mit
Match-Guards hinzufügen“](#adding-conditionals-with-match-guards)<!-- ignore -->.

<!-- Old headings. Do not remove or links may break. -->

<a id="multiple-patterns"></a>

### Mehrere Patterns abgleichen {#matching-multiple-patterns}

In `match`-Ausdrücken kannst du mit der Syntax `|`, dem _Oder_-Operator für
Patterns, mehrere Patterns abgleichen. Im folgenden Code gleichen wir zum
Beispiel den Wert von `x` mit den Match-Armen ab, von denen der erste eine
_Oder_-Option hat. Das bedeutet: Wenn der Wert von `x` auf einen der Werte in
diesem Arm passt, wird der Code dieses Arms ausgeführt:

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/no-listing-02-multiple-patterns/src/main.rs:here}}
```

Dieser Code gibt `one or two` aus.

### Wertebereiche mit `..=` abgleichen {#matching-ranges-of-values-with-}

Mit der Syntax `..=` können wir einen inklusiven Wertebereich (_range_)
abgleichen. Wenn im folgenden Code ein Pattern auf einen der Werte im
angegebenen Bereich passt, wird dieser Arm ausgeführt:

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/no-listing-03-ranges/src/main.rs:here}}
```

Wenn `x` `1`, `2`, `3`, `4` oder `5` ist, passt der erste Arm. Für mehrere
Vergleichswerte ist diese Syntax bequemer, als dieselbe Idee mit dem Operator
`|` auszudrücken; würden wir `|` verwenden, müssten wir `1 | 2 |
3 | 4 | 5`
angeben. Einen Bereich anzugeben, ist viel kürzer, besonders wenn wir etwa auf
jede Zahl zwischen 1 und 1.000 prüfen wollen!

Der Compiler prüft zur Kompilierzeit, dass der Bereich nicht leer ist, und weil
`char` und numerische Werte die einzigen Typen sind, bei denen Rust feststellen
kann, ob ein Bereich leer ist oder nicht, sind Bereiche nur mit numerischen
Werten oder `char`-Werten erlaubt.

Hier ist ein Beispiel mit Bereichen von `char`-Werten:

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/no-listing-04-ranges-of-char/src/main.rs:here}}
```

Rust erkennt, dass `'c'` im Bereich des ersten Patterns liegt, und gibt
`early
ASCII letter` aus.

### Destrukturieren, um Werte zu zerlegen {#destructuring-to-break-apart-values}

Wir können Patterns auch verwenden, um Structs, Enums und Tupel zu
destrukturieren und so verschiedene Teile dieser Werte zu verwenden. Gehen wir
die einzelnen Werte durch.

<!-- Old headings. Do not remove or links may break. -->

<a id="destructuring-structs"></a>

#### Structs {#structs}

Listing 19-12 zeigt ein Struct `Point` mit zwei Feldern, `x` und `y`, das wir
mit einem Pattern in einer `let`-Anweisung zerlegen können.

<Listing number="19-12" file-name="src/main.rs" caption="Die Felder eines Structs in einzelne Variablen destrukturieren">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-12/src/main.rs}}
```

</Listing>

Dieser Code erzeugt die Variablen `a` und `b`, die auf die Werte der Felder `x`
und `y` des Structs `p` passen. Dieses Beispiel zeigt, dass die Namen der
Variablen im Pattern nicht mit den Feldnamen des Structs übereinstimmen müssen.
Es ist jedoch üblich, die Variablennamen an die Feldnamen anzugleichen, damit
man sich leichter merken kann, welche Variablen aus welchen Feldern stammen.
Wegen dieser verbreiteten Verwendung und weil `let Point { x: x, y: y } = p;`
viel Wiederholung enthält, hat Rust eine Kurzschreibweise für Patterns, die auf
Struct-Felder passen: Du musst nur den Namen des Struct-Felds angeben, und die
aus dem Pattern erzeugten Variablen haben dieselben Namen. Listing 19-13 verhält
sich genauso wie der Code in Listing 19-12, aber die im `let`-Pattern erzeugten
Variablen sind `x` und `y` statt `a` und `b`.

<Listing number="19-13" file-name="src/main.rs" caption="Struct-Felder mit der Kurzschreibweise für Struct-Felder destrukturieren">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-13/src/main.rs}}
```

</Listing>

Dieser Code erzeugt die Variablen `x` und `y`, die auf die Felder `x` und `y`
der Variablen `p` passen. Im Ergebnis enthalten die Variablen `x` und `y` die
Werte aus dem Struct `p`.

Wir können auch mit Literalwerten als Teil des Struct-Patterns destrukturieren,
statt für alle Felder Variablen zu erzeugen. So können wir einige Felder auf
bestimmte Werte prüfen und gleichzeitig Variablen erzeugen, um die anderen
Felder zu destrukturieren.

In Listing 19-14 haben wir einen `match`-Ausdruck, der `Point`-Werte in drei
Fälle aufteilt: Punkte, die direkt auf der `x`-Achse liegen (was gilt, wenn
`y = 0` ist), auf der `y`-Achse (`x = 0`) oder auf keiner der beiden Achsen.

<Listing number="19-14" file-name="src/main.rs" caption="Destrukturieren und Literalwerte abgleichen in einem einzigen Pattern">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-14/src/main.rs:here}}
```

</Listing>

Der erste Arm passt auf jeden Punkt, der auf der `x`-Achse liegt, indem er
angibt, dass das Feld `y` passt, wenn sein Wert auf das Literal `0` passt. Das
Pattern erzeugt trotzdem eine Variable `x`, die wir im Code für diesen Arm
verwenden können.

Ebenso passt der zweite Arm auf jeden Punkt auf der `y`-Achse, indem er angibt,
dass das Feld `x` passt, wenn sein Wert `0` ist, und er erzeugt eine Variable
`y` für den Wert des Felds `y`. Der dritte Arm gibt keine Literale an, passt
also auf jeden anderen `Point` und erzeugt Variablen für die beiden Felder `x`
und `y`.

In diesem Beispiel passt der Wert `p` auf den zweiten Arm, weil `x` eine `0`
enthält, daher gibt dieser Code `On the y axis at 7` aus.

Denk daran, dass ein `match`-Ausdruck die Arme nicht mehr weiter prüft, sobald
er das erste passende Pattern gefunden hat. Obwohl `Point { x: 0, y: 0 }` also
sowohl auf der `x`-Achse als auch auf der `y`-Achse liegt, würde dieser Code nur
`On the x axis at 0` ausgeben.

<!-- Old headings. Do not remove or links may break. -->

<a id="destructuring-enums"></a>

#### Enums {#enums}

Wir haben in diesem Buch bereits Enums destrukturiert (zum Beispiel in Listing
6-5 in Kapitel 6), aber noch nicht ausdrücklich besprochen, dass das Pattern zum
Destrukturieren eines Enums der Art entspricht, wie die im Enum gespeicherten
Daten definiert sind. In Listing 19-15 verwenden wir als Beispiel das Enum
`Message` aus Listing 6-2 und schreiben ein `match` mit Patterns, die jeden
inneren Wert destrukturieren.

<Listing number="19-15" file-name="src/main.rs" caption="Enum-Varianten destrukturieren, die verschiedene Arten von Werten enthalten">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-15/src/main.rs}}
```

</Listing>

Dieser Code gibt `Change color to red 0, green 160, and blue 255` aus. Versuche,
den Wert von `msg` zu ändern, um den Code der anderen Arme ausgeführt zu sehen.

Bei Enum-Varianten ohne Daten wie `Message::Quit` können wir den Wert nicht
weiter destrukturieren. Wir können nur auf den literalen Wert `Message::Quit`
prüfen, und in diesem Pattern gibt es keine Variablen.

Bei Struct-ähnlichen Enum-Varianten wie `Message::Move` können wir ein Pattern
verwenden, das dem Pattern ähnelt, mit dem wir Structs abgleichen. Nach dem
Variantennamen setzen wir geschweifte Klammern und listen dann die Felder mit
Variablen auf, sodass wir die Teile zerlegen, um sie im Code für diesen Arm zu
verwenden. Hier verwenden wir die Kurzschreibweise wie in Listing 19-13.

Bei Tupel-ähnlichen Enum-Varianten wie `Message::Write`, das ein Tupel mit einem
Element enthält, und `Message::ChangeColor`, das ein Tupel mit drei Elementen
enthält, ähnelt das Pattern dem Pattern, mit dem wir Tupel abgleichen. Die
Anzahl der Variablen im Pattern muss mit der Anzahl der Elemente in der Variante
übereinstimmen, die wir abgleichen.

<!-- Old headings. Do not remove or links may break. -->

<a id="destructuring-nested-structs-and-enums"></a>

#### Verschachtelte Structs und Enums {#nested-structs-and-enums}

Bisher haben unsere Beispiele alle Structs oder Enums abgeglichen, die eine
Ebene tief waren, aber Matching funktioniert auch bei verschachtelten Elementen!
Wir können zum Beispiel den Code in Listing 19-15 so umgestalten, dass er in der
Nachricht `ChangeColor` RGB- und HSV-Farben unterstützt, wie in Listing 19-16
gezeigt.

<Listing number="19-16" caption="Verschachtelte Enums abgleichen">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-16/src/main.rs}}
```

</Listing>

Das Pattern des ersten Arms im `match`-Ausdruck passt auf eine Enum-Variante
`Message::ChangeColor`, die eine Variante `Color::Rgb` enthält; dann bindet das
Pattern die drei inneren `i32`-Werte. Das Pattern des zweiten Arms passt
ebenfalls auf eine Enum-Variante `Message::ChangeColor`, aber das innere Enum
passt stattdessen auf `Color::Hsv`. Wir können diese komplexen Bedingungen in
einem einzigen `match`-Ausdruck angeben, obwohl zwei Enums beteiligt sind.

<!-- Old headings. Do not remove or links may break. -->

<a id="destructuring-structs-and-tuples"></a>

#### Structs und Tupel {#structs-and-tuples}

Wir können Destrukturierungs-Patterns auf noch komplexere Weise mischen,
kombinieren und verschachteln. Das folgende Beispiel zeigt eine komplizierte
Destrukturierung, bei der wir Structs und Tupel in einem Tupel verschachteln und
alle primitiven Werte herausdestrukturieren:

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/no-listing-05-destructuring-structs-and-tuples/src/main.rs:here}}
```

Mit diesem Code können wir komplexe Typen in ihre Bestandteile zerlegen, sodass
wir die Werte, die uns interessieren, einzeln verwenden können.

Das Destrukturieren mit Patterns ist eine bequeme Möglichkeit, Teile von Werten,
etwa den Wert jedes Felds in einem Struct, getrennt voneinander zu verwenden.

### Werte in einem Pattern ignorieren {#ignoring-values-in-a-pattern}

Du hast gesehen, dass es manchmal nützlich ist, Werte in einem Pattern zu
ignorieren, etwa im letzten Arm eines `match`, um einen Auffangfall zu haben,
der eigentlich nichts tut, aber alle verbleibenden möglichen Werte
berücksichtigt. Es gibt einige Möglichkeiten, ganze Werte oder Teile von Werten
in einem Pattern zu ignorieren: das Pattern `_` (das du schon gesehen hast), das
Pattern `_` innerhalb eines anderen Patterns, einen Namen, der mit einem
Unterstrich beginnt, oder `..`, um die übrigen Teile eines Werts zu ignorieren.
Sehen wir uns an, wie und warum man jedes dieser Patterns verwendet.

<!-- Old headings. Do not remove or links may break. -->

<a id="ignoring-an-entire-value-with-_"></a>

#### Einen ganzen Wert mit `_` {#an-entire-value-with-_}

Wir haben den Unterstrich als Wildcard-Pattern verwendet, das auf jeden Wert
passt, sich aber nicht an den Wert bindet. Das ist besonders nützlich als
letzter Arm in einem `match`-Ausdruck, aber wir können es auch in jedem Pattern
verwenden, auch in Funktionsparametern, wie in Listing 19-17 gezeigt.

<Listing number="19-17" file-name="src/main.rs" caption="`_` in einer Funktionssignatur verwenden">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-17/src/main.rs}}
```

</Listing>

Dieser Code ignoriert den als erstes Argument übergebenen Wert `3` vollständig
und gibt `This code only uses the y parameter: 4` aus.

Wenn du einen bestimmten Funktionsparameter nicht mehr brauchst, würdest du in
den meisten Fällen die Signatur so ändern, dass sie den unbenutzten Parameter
nicht mehr enthält. Einen Funktionsparameter zu ignorieren, kann besonders
nützlich sein, wenn du zum Beispiel einen Trait implementierst und eine
bestimmte Typsignatur brauchst, der Funktionsrumpf in deiner Implementierung
aber einen der Parameter nicht benötigt. So vermeidest du eine Compilerwarnung
über unbenutzte Funktionsparameter, die du bekämst, wenn du stattdessen einen
Namen verwenden würdest.

<!-- Old headings. Do not remove or links may break. -->

<a id="ignoring-parts-of-a-value-with-a-nested-_"></a>

#### Teile eines Werts mit einem verschachtelten `_` {#parts-of-a-value-with-a-nested-_}

Wir können `_` auch innerhalb eines anderen Patterns verwenden, um nur einen
Teil eines Werts zu ignorieren, zum Beispiel wenn wir nur einen Teil eines Werts
prüfen wollen, die anderen Teile aber im zugehörigen Code, den wir ausführen
wollen, nicht brauchen. Listing 19-18 zeigt Code, der für die Verwaltung des
Werts einer Einstellung zuständig ist. Die geschäftlichen Anforderungen lauten,
dass der Benutzer eine bestehende Anpassung einer Einstellung nicht
überschreiben darf, die Einstellung aber zurücksetzen und ihr einen Wert geben
kann, wenn sie derzeit nicht gesetzt ist.

<Listing number="19-18" caption="Einen Unterstrich in Patterns verwenden, die auf `Some`-Varianten passen, wenn wir den Wert innerhalb des `Some` nicht brauchen">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-18/src/main.rs:here}}
```

</Listing>

Dieser Code gibt `Can't overwrite an existing customized value` und dann
`setting is Some(5)` aus. Im ersten Match-Arm müssen wir die Werte innerhalb der
beiden `Some`-Varianten weder abgleichen noch verwenden, aber wir müssen den
Fall prüfen, in dem `setting_value` und `new_setting_value` die Variante `Some`
sind. In diesem Fall geben wir den Grund aus, warum `setting_value` nicht
geändert wird, und es wird nicht geändert.

In allen anderen Fällen (wenn entweder `setting_value` oder `new_setting_value`
`None` ist), die durch das Pattern `_` im zweiten Arm ausgedrückt werden, wollen
wir erlauben, dass `setting_value` auf `new_setting_value` gesetzt wird.

Wir können Unterstriche auch an mehreren Stellen innerhalb eines Patterns
verwenden, um bestimmte Werte zu ignorieren. Listing 19-19 zeigt ein Beispiel,
in dem der zweite und vierte Wert in einem Tupel mit fünf Elementen ignoriert
werden.

<Listing number="19-19" caption="Mehrere Teile eines Tupels ignorieren">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-19/src/main.rs:here}}
```

</Listing>

Dieser Code gibt `Some numbers: 2, 8, 32` aus, und die Werte `4` und `16` werden
ignoriert.

<!-- Old headings. Do not remove or links may break. -->

<a id="ignoring-an-unused-variable-by-starting-its-name-with-_"></a>

#### Eine unbenutzte Variable, deren Name mit `_` beginnt {#an-unused-variable-by-starting-its-name-with-_}

Wenn du eine Variable erstellst, sie aber nirgends verwendest, gibt Rust
normalerweise eine Warnung aus, weil eine unbenutzte Variable ein Bug sein
könnte. Manchmal ist es aber nützlich, eine Variable erstellen zu können, die du
noch nicht verwendest, etwa wenn du einen Prototyp baust oder gerade erst mit
einem Projekt beginnst. In dieser Situation kannst du Rust anweisen, dich nicht
vor der unbenutzten Variablen zu warnen, indem du den Namen der Variablen mit
einem Unterstrich beginnst. In Listing 19-20 erstellen wir zwei unbenutzte
Variablen, aber wenn wir diesen Code kompilieren, sollten wir nur für eine davon
eine Warnung bekommen.

<Listing number="19-20" file-name="src/main.rs" caption="Einen Variablennamen mit einem Unterstrich beginnen, um Warnungen über unbenutzte Variablen zu vermeiden">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-20/src/main.rs}}
```

</Listing>

Hier bekommen wir eine Warnung, dass die Variable `y` nicht verwendet wird, aber
keine Warnung, dass `_x` nicht verwendet wird.

Beachte, dass es einen feinen Unterschied gibt, ob man nur `_` verwendet oder
einen Namen, der mit einem Unterstrich beginnt. Die Syntax `_x` bindet den Wert
weiterhin an die Variable, während `_` überhaupt nicht bindet. Um einen Fall zu
zeigen, in dem dieser Unterschied eine Rolle spielt, liefert uns Listing 19-21
einen Fehler.

<Listing number="19-21" caption="Eine unbenutzte Variable, die mit einem Unterstrich beginnt, bindet den Wert trotzdem, was die Ownership am Wert übernehmen kann.">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-21/src/main.rs:here}}
```

</Listing>

Wir bekommen einen Fehler, weil der Wert `s` trotzdem in `_s` verschoben
(_moved_) wird, was uns daran hindert, `s` erneut zu verwenden. Der Unterstrich
allein bindet sich jedoch nie an den Wert. Listing 19-22 kompiliert ohne Fehler,
weil `s` nicht in `_` verschoben wird.

<Listing number="19-22" caption="Ein Unterstrich bindet den Wert nicht.">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-22/src/main.rs:here}}
```

</Listing>

Dieser Code funktioniert problemlos, weil wir `s` nie an etwas binden; es wird
nicht verschoben.

<a id="ignoring-remaining-parts-of-a-value-with-"></a>

#### Die übrigen Teile eines Werts mit `..` {#remaining-parts-of-a-value-with-}

Bei Werten, die viele Teile haben, können wir die Syntax `..` verwenden, um
bestimmte Teile zu verwenden und den Rest zu ignorieren, sodass wir nicht für
jeden ignorierten Wert einen Unterstrich angeben müssen. Das Pattern `..`
ignoriert alle Teile eines Werts, die wir im restlichen Pattern nicht
ausdrücklich abgeglichen haben. In Listing 19-23 haben wir ein Struct `Point`,
das eine Koordinate im dreidimensionalen Raum enthält. Im `match`-Ausdruck
wollen wir nur mit der Koordinate `x` arbeiten und die Werte in den Feldern `y`
und `z` ignorieren.

<Listing number="19-23" caption="Mit `..` alle Felder eines `Point` außer `x` ignorieren">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-23/src/main.rs:here}}
```

</Listing>

Wir geben den Wert `x` an und fügen dann einfach das Pattern `..` ein. Das geht
schneller, als `y: _` und `z: _` aufzulisten, besonders wenn wir mit Structs
arbeiten, die viele Felder haben, in Situationen, in denen nur ein oder zwei
Felder relevant sind.

Die Syntax `..` wird zu so vielen Werten erweitert, wie nötig. Listing 19-24
zeigt, wie man `..` mit einem Tupel verwendet.

<Listing number="19-24" file-name="src/main.rs" caption="Nur den ersten und den letzten Wert in einem Tupel abgleichen und alle anderen Werte ignorieren">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-24/src/main.rs}}
```

</Listing>

In diesem Code werden der erste und der letzte Wert mit `first` und `last`
abgeglichen. Das `..` passt auf alles dazwischen und ignoriert es.

Die Verwendung von `..` muss jedoch eindeutig sein. Wenn unklar ist, welche
Werte abgeglichen und welche ignoriert werden sollen, gibt Rust einen Fehler
aus. Listing 19-25 zeigt ein Beispiel für eine mehrdeutige Verwendung von `..`,
daher kompiliert es nicht.

<Listing number="19-25" file-name="src/main.rs" caption="Ein Versuch, `..` mehrdeutig zu verwenden">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-25/src/main.rs}}
```

</Listing>

Wenn wir dieses Beispiel kompilieren, bekommen wir diesen Fehler:

```console
{{#include ../listings/ch19-patterns-and-matching/listing-19-25/output.txt}}
```

Rust kann unmöglich bestimmen, wie viele Werte im Tupel ignoriert werden sollen,
bevor ein Wert mit `second` abgeglichen wird, und wie viele weitere Werte danach
ignoriert werden sollen. Dieser Code könnte bedeuten, dass wir `2` ignorieren,
`second` an `4` binden und dann `8`, `16` und `32` ignorieren wollen; oder dass
wir `2` und `4` ignorieren, `second` an `8` binden und dann `16` und `32`
ignorieren wollen; und so weiter. Der Variablenname `second` hat für Rust keine
besondere Bedeutung, daher bekommen wir einen Compilerfehler, weil die
Verwendung von `..` an zwei Stellen wie hier mehrdeutig ist.

<!-- Old headings. Do not remove or links may break. -->

<a id="extra-conditionals-with-match-guards"></a>

### Bedingungen mit Match-Guards hinzufügen {#adding-conditionals-with-match-guards}

Ein _Match-Guard_ ist eine zusätzliche `if`-Bedingung, die nach dem Pattern in
einem `match`-Arm angegeben wird und ebenfalls erfüllt sein muss, damit dieser
Arm gewählt wird. Match-Guards sind nützlich, um komplexere Ideen auszudrücken,
als ein Pattern allein erlaubt. Beachte jedoch, dass sie nur in
`match`-Ausdrücken verfügbar sind, nicht in `if let`- oder
`while let`-Ausdrücken.

Die Bedingung kann Variablen verwenden, die im Pattern erzeugt wurden. Listing
19-26 zeigt ein `match`, bei dem der erste Arm das Pattern `Some(x)` und
zusätzlich einen Match-Guard `if x % 2 == 0` hat (der `true` ist, wenn die Zahl
gerade ist).

<Listing number="19-26" caption="Einem Pattern einen Match-Guard hinzufügen">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-26/src/main.rs:here}}
```

</Listing>

Dieses Beispiel gibt `The number 4 is even` aus. Wenn `num` mit dem Pattern im
ersten Arm verglichen wird, passt es, weil `Some(4)` auf `Some(x)` passt. Dann
prüft der Match-Guard, ob der Rest der Division von `x` durch 2 gleich 0 ist,
und weil das der Fall ist, wird der erste Arm gewählt.

Wäre `num` stattdessen `Some(5)` gewesen, wäre der Match-Guard im ersten Arm
`false` gewesen, weil der Rest von 5 geteilt durch 2 gleich 1 ist, was nicht
gleich 0 ist. Rust würde dann zum zweiten Arm übergehen, der passen würde, weil
der zweite Arm keinen Match-Guard hat und daher auf jede `Some`-Variante passt.

Es gibt keine Möglichkeit, die Bedingung `if x % 2 == 0` innerhalb eines
Patterns auszudrücken, daher gibt uns der Match-Guard die Möglichkeit, diese
Logik auszudrücken. Der Nachteil dieser zusätzlichen Ausdruckskraft ist, dass
der Compiler nicht versucht zu prüfen, ob die Arme erschöpfend sind, wenn
Match-Guard-Ausdrücke beteiligt sind.

Bei der Besprechung von Listing 19-11 haben wir erwähnt, dass wir Match-Guards
verwenden könnten, um unser Problem mit dem Überschatten durch Patterns zu
lösen. Erinnere dich, dass wir innerhalb des Patterns im `match`-Ausdruck eine
neue Variable erzeugt haben, statt die Variable außerhalb des `match` zu
verwenden. Diese neue Variable bedeutete, dass wir nicht gegen den Wert der
äußeren Variablen prüfen konnten. Listing 19-27 zeigt, wie wir dieses Problem
mit einem Match-Guard beheben können.

<Listing number="19-27" file-name="src/main.rs" caption="Einen Match-Guard verwenden, um auf Gleichheit mit einer äußeren Variablen zu prüfen">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-27/src/main.rs}}
```

</Listing>

Dieser Code gibt jetzt `Default case, x = Some(5)` aus. Das Pattern im zweiten
Match-Arm führt keine neue Variable `y` ein, die das äußere `y` überschatten
würde, sodass wir das äußere `y` im Match-Guard verwenden können. Statt das
Pattern als `Some(y)` anzugeben, was das äußere `y` überschattet hätte, geben
wir `Some(n)` an. Das erzeugt eine neue Variable `n`, die nichts überschattet,
weil es außerhalb des `match` keine Variable `n` gibt.

Der Match-Guard `if n == y` ist kein Pattern und führt daher keine neuen
Variablen ein. Dieses `y` _ist_ das äußere `y` und kein neues `y`, das es
überschattet, und wir können nach einem Wert suchen, der denselben Wert wie das
äußere `y` hat, indem wir `n` mit `y` vergleichen.

Du kannst in einem Match-Guard auch den _Oder_-Operator `|` verwenden, um
mehrere Patterns anzugeben; die Bedingung des Match-Guards gilt dann für alle
Patterns. Listing 19-28 zeigt den Vorrang, wenn man ein Pattern, das `|`
verwendet, mit einem Match-Guard kombiniert. Das Wichtige an diesem Beispiel
ist, dass der Match-Guard `if y` für `4`, `5` _und_ `6` gilt, auch wenn es so
aussehen könnte, als gelte `if y` nur für `6`.

<Listing number="19-28" caption="Mehrere Patterns mit einem Match-Guard kombinieren">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-28/src/main.rs:here}}
```

</Listing>

Die Match-Bedingung besagt, dass der Arm nur passt, wenn der Wert von `x` gleich
`4`, `5` oder `6` ist _und_ wenn `y` `true` ist. Wenn dieser Code ausgeführt
wird, passt das Pattern des ersten Arms, weil `x` `4` ist, aber der Match-Guard
`if y` ist `false`, also wird der erste Arm nicht gewählt. Der Code geht zum
zweiten Arm über, der passt, und dieses Programm gibt `no` aus. Der Grund ist,
dass die `if`-Bedingung für das ganze Pattern `4 | 5 | 6` gilt, nicht nur für
den letzten Wert `6`. Mit anderen Worten: Der Vorrang eines Match-Guards im
Verhältnis zu einem Pattern verhält sich so:

```text
(4 | 5 | 6) if y => ...
```

und nicht so:

```text
4 | 5 | (6 if y) => ...
```

Nach dem Ausführen des Codes ist das Vorrangverhalten offensichtlich: Würde der
Match-Guard nur auf den letzten Wert in der mit dem Operator `|` angegebenen
Liste von Werten angewendet, hätte der Arm gepasst, und das Programm hätte `yes`
ausgegeben.

<!-- Old headings. Do not remove or links may break. -->

<a id="-bindings"></a>

### `@`-Bindungen verwenden {#using--bindings}

Mit dem _At_-Operator `@` können wir eine Variable erzeugen, die einen Wert
enthält, während wir gleichzeitig prüfen, ob dieser Wert auf ein Pattern passt.
In Listing 19-29 wollen wir prüfen, ob das Feld `id` eines `Message::Hello` im
Bereich `3..=7` liegt. Außerdem wollen wir den Wert an die Variable `id` binden,
damit wir ihn im Code verwenden können, der zum Arm gehört.

<Listing number="19-29" caption="Mit `@` in einem Pattern an einen Wert binden und ihn gleichzeitig prüfen">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-29/src/main.rs:here}}
```

</Listing>

Dieses Beispiel gibt `Found an id in range: 5` aus. Indem wir `id @` vor dem
Bereich `3..=7` angeben, erfassen wir den Wert, der auf den Bereich gepasst hat,
in einer Variablen namens `id` und prüfen gleichzeitig, ob der Wert auf das
Bereichs-Pattern gepasst hat.

Im zweiten Arm, in dem im Pattern nur ein Bereich angegeben ist, hat der Code,
der zum Arm gehört, keine Variable, die den tatsächlichen Wert des Felds `id`
enthält. Der Wert des Felds `id` hätte 10, 11 oder 12 sein können, aber der Code
zu diesem Pattern weiß nicht, welcher es ist. Der Code des Patterns kann den
Wert aus dem Feld `id` nicht verwenden, weil wir den Wert von `id` nicht in
einer Variablen gespeichert haben.

Im letzten Arm, in dem wir eine Variable ohne Bereich angegeben haben, steht der
Wert im Code des Arms in einer Variablen namens `id` zur Verfügung. Der Grund
ist, dass wir die Kurzschreibweise für Struct-Felder verwendet haben. Wir haben
in diesem Arm aber keine Prüfung auf den Wert im Feld `id` angewendet, wie wir
es bei den ersten beiden Armen getan haben: Jeder Wert würde auf dieses Pattern
passen.

Mit `@` können wir innerhalb eines einzigen Patterns einen Wert prüfen und ihn
in einer Variablen speichern.

{{#quiz ../quizzes/ch18-03-pattern-syntax.toml}}

## Zusammenfassung {#summary}

Die Patterns von Rust sind sehr nützlich, um zwischen verschiedenen Arten von
Daten zu unterscheiden. Wenn sie in `match`-Ausdrücken verwendet werden, stellt
Rust sicher, dass deine Patterns jeden möglichen Wert abdecken, sonst kompiliert
dein Programm nicht. Patterns in `let`-Anweisungen und Funktionsparametern
machen diese Konstrukte nützlicher, indem sie es ermöglichen, Werte in kleinere
Teile zu destrukturieren und diese Teile Variablen zuzuweisen. Wir können
einfache oder komplexe Patterns erstellen, die unseren Bedürfnissen entsprechen.

Als Nächstes sehen wir uns im vorletzten Kapitel des Buches einige
fortgeschrittene Aspekte verschiedener Features von Rust an.
