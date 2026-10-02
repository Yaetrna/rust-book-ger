## Alle Stellen, an denen Patterns verwendet werden können {#all-the-places-patterns-can-be-used}

Patterns tauchen in Rust an einer Reihe von Stellen auf, und du hast sie schon
oft verwendet, ohne es zu merken! Dieser Abschnitt bespricht alle Stellen, an
denen Patterns gültig sind.

### `match`-Arme {#match-arms}

Wie in Kapitel 6 besprochen, verwenden wir Patterns in den Armen von
`match`-Ausdrücken. Formal sind `match`-Ausdrücke definiert als das
Schlüsselwort `match`, ein Wert, der abgeglichen wird, und ein oder mehrere
Match-Arme, die aus einem Pattern und einem Ausdruck bestehen, der ausgeführt
wird, wenn der Wert auf das Pattern dieses Arms passt, etwa so:

<!--
  Manually formatted rather than using Markdown intentionally: Markdown does not
  support italicizing code in the body of a block like this!
-->

<pre><code>match <em>VALUE</em> {
    <em>PATTERN</em> => <em>EXPRESSION</em>,
    <em>PATTERN</em> => <em>EXPRESSION</em>,
    <em>PATTERN</em> => <em>EXPRESSION</em>,
}</code></pre>

Hier ist zum Beispiel der `match`-Ausdruck aus Listing 6-5, der einen Wert vom
Typ `Option<i32>` in der Variablen `x` abgleicht:

```rust,ignore
match x {
    None => None,
    Some(i) => Some(i + 1),
}
```

Die Patterns in diesem `match`-Ausdruck sind `None` und `Some(i)` links von
jedem Pfeil.

Eine Anforderung an `match`-Ausdrücke ist, dass sie erschöpfend (_exhaustive_)
sein müssen, in dem Sinne, dass alle Möglichkeiten für den Wert im
`match`-Ausdruck berücksichtigt werden müssen. Eine Möglichkeit,
sicherzustellen, dass du jede Möglichkeit abgedeckt hast, ist ein
Auffang-Pattern für den letzten Arm: Zum Beispiel kann ein Variablenname, der
auf jeden Wert passt, nie fehlschlagen und deckt damit jeden verbleibenden Fall
ab.

Das spezielle Pattern `_` passt auf alles, bindet aber nie an eine Variable,
daher wird es oft im letzten Match-Arm verwendet. Das Pattern `_` kann zum
Beispiel nützlich sein, wenn du jeden nicht angegebenen Wert ignorieren willst.
Das Pattern `_` behandeln wir später in diesem Kapitel im Abschnitt
[„Werte in
einem Pattern ignorieren“][ignoring-values-in-a-pattern]<!-- ignore --> genauer.

### `let`-Anweisungen {#let-statements}

Vor diesem Kapitel haben wir nur ausdrücklich besprochen, wie man Patterns mit
`match` und `if let` verwendet, aber tatsächlich haben wir Patterns auch an
anderen Stellen verwendet, unter anderem in `let`-Anweisungen. Betrachte zum
Beispiel diese einfache Variablenzuweisung mit `let`:

```rust
let x = 5;
```

Jedes Mal, wenn du eine `let`-Anweisung wie diese verwendet hast, hast du
Patterns verwendet, auch wenn es dir vielleicht nicht bewusst war! Formaler
ausgedrückt sieht eine `let`-Anweisung so aus:

<!--
  Manually formatted rather than using Markdown intentionally: Markdown does not
  support italicizing code in the body of a block like this!
-->

<pre>
<code>let <em>PATTERN</em> = <em>EXPRESSION</em>;</code>
</pre>

In Anweisungen wie `let x = 5;` mit einem Variablennamen an der Stelle PATTERN
ist der Variablenname nur eine besonders einfache Form eines Patterns. Rust
vergleicht den Ausdruck mit dem Pattern und weist alle Namen zu, die es findet.
Im Beispiel `let x = 5;` ist `x` also ein Pattern, das bedeutet: „Binde das, was
hier passt, an die Variable `x`.“ Weil der Name `x` das ganze Pattern ist,
bedeutet dieses Pattern im Grunde: „Binde alles an die Variable `x`, egal
welchen Wert es hat.“

Um den Pattern-Matching-Aspekt von `let` deutlicher zu sehen, betrachte Listing
19-1, das ein Pattern mit `let` verwendet, um ein Tupel zu destrukturieren.

<Listing number="19-1" caption="Mit einem Pattern ein Tupel destrukturieren und drei Variablen auf einmal erzeugen">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-01/src/main.rs:here}}
```

</Listing>

Hier gleichen wir ein Tupel mit einem Pattern ab. Rust vergleicht den Wert
`(1, 2, 3)` mit dem Pattern `(x, y, z)` und sieht, dass der Wert auf das Pattern
passt – das heißt, es sieht, dass die Anzahl der Elemente in beiden gleich ist
–, also bindet Rust `1` an `x`, `2` an `y` und `3` an `z`. Du kannst dir dieses
Tupel-Pattern so vorstellen, dass darin drei einzelne Variablen-Patterns
verschachtelt sind.

Wenn die Anzahl der Elemente im Pattern nicht mit der Anzahl der Elemente im
Tupel übereinstimmt, passt der Gesamttyp nicht und wir bekommen einen
Compilerfehler. Listing 19-2 zeigt zum Beispiel einen Versuch, ein Tupel mit
drei Elementen in zwei Variablen zu destrukturieren, was nicht funktioniert.

<Listing number="19-2" caption="Ein falsch konstruiertes Pattern, dessen Variablen nicht zur Anzahl der Elemente im Tupel passen">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-02/src/main.rs:here}}
```

</Listing>

Der Versuch, diesen Code zu kompilieren, führt zu diesem Typfehler:

```console
{{#include ../listings/ch19-patterns-and-matching/listing-19-02/output.txt}}
```

Um den Fehler zu beheben, könnten wir einen oder mehrere Werte im Tupel mit `_`
oder `..` ignorieren, wie du im Abschnitt
[„Werte in einem Pattern
ignorieren“][ignoring-values-in-a-pattern]<!-- ignore --> sehen wirst. Wenn das
Problem darin besteht, dass wir zu viele Variablen im Pattern haben, besteht die
Lösung darin, die Typen passend zu machen, indem wir Variablen entfernen, bis
die Anzahl der Variablen der Anzahl der Elemente im Tupel entspricht.

### Bedingte `if let`-Ausdrücke {#conditional-if-let-expressions}

In Kapitel 6 haben wir besprochen, wie man `if let`-Ausdrücke vor allem als
kürzere Schreibweise für das Gegenstück eines `match` verwendet, das nur auf
einen einzigen Fall prüft. Optional kann `if let` ein zugehöriges `else` haben,
das Code enthält, der ausgeführt wird, wenn das Pattern im `if let` nicht passt.

Listing 19-3 zeigt, dass es auch möglich ist, `if let`-, `else
if`- und
`else if let`-Ausdrücke beliebig zu kombinieren. Das gibt uns mehr Flexibilität
als ein `match`-Ausdruck, in dem wir nur einen einzigen Wert angeben können, der
mit den Patterns verglichen wird. Außerdem verlangt Rust nicht, dass die
Bedingungen in einer Reihe von `if
let`-, `else if`- und `else if let`-Zweigen
miteinander zusammenhängen.

Der Code in Listing 19-3 bestimmt anhand einer Reihe von Prüfungen mehrerer
Bedingungen, welche Farbe dein Hintergrund bekommen soll. Für dieses Beispiel
haben wir Variablen mit fest kodierten Werten erstellt, die ein echtes Programm
aus Benutzereingaben erhalten könnte.

<Listing number="19-3" file-name="src/main.rs" caption="`if let`, `else if`, `else if let` und `else` kombinieren">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-03/src/main.rs}}
```

</Listing>

Wenn der Benutzer eine Lieblingsfarbe angibt, wird diese Farbe als Hintergrund
verwendet. Wenn keine Lieblingsfarbe angegeben ist und heute Dienstag ist, ist
die Hintergrundfarbe grün. Andernfalls, wenn der Benutzer sein Alter als String
angibt und wir es erfolgreich als Zahl parsen können, ist die Farbe je nach Wert
der Zahl entweder lila oder orange. Wenn keine dieser Bedingungen zutrifft, ist
die Hintergrundfarbe blau.

Mit dieser bedingten Struktur können wir komplexe Anforderungen unterstützen.
Mit den fest kodierten Werten, die wir hier haben, gibt dieses Beispiel
`Using
purple as the background color` aus.

Du siehst, dass `if let` auch neue Variablen einführen kann, die bestehende
Variablen überschatten (_shadow_), genauso wie es `match`-Arme können: Die Zeile
`if let Ok(age) = age` führt eine neue Variable `age` ein, die den Wert
innerhalb der Variante `Ok` enthält und die bestehende Variable `age`
überschattet. Das bedeutet, dass wir die Bedingung `if age >
30` innerhalb dieses
Blocks platzieren müssen: Wir können diese beiden Bedingungen nicht zu
`if
let Ok(age) = age && age > 30` kombinieren. Das neue `age`, das wir mit 30
vergleichen wollen, ist erst gültig, wenn der neue Gültigkeitsbereich (_scope_)
mit der geschweiften Klammer beginnt.

Der Nachteil von `if let`-Ausdrücken ist, dass der Compiler nicht prüft, ob sie
erschöpfend sind, während er das bei `match`-Ausdrücken tut. Würden wir den
letzten `else`-Block weglassen und damit die Behandlung einiger Fälle verpassen,
würde uns der Compiler nicht auf den möglichen Logikfehler hinweisen.

### Bedingte `while let`-Schleifen {#while-let-conditional-loops}

Ähnlich aufgebaut wie `if let` erlaubt die bedingte Schleife `while let` einer
`while`-Schleife, so lange zu laufen, wie ein Pattern weiterhin passt. In
Listing 19-4 zeigen wir eine `while let`-Schleife, die auf Nachrichten wartet,
die zwischen Threads gesendet werden, in diesem Fall aber ein `Result` statt
einer `Option` prüft.

<Listing number="19-4" caption="Eine `while let`-Schleife verwenden, um Werte auszugeben, solange `rx.recv()` `Ok` zurückgibt">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-04/src/main.rs:here}}
```

</Listing>

Dieses Beispiel gibt `1`, `2` und dann `3` aus. Die Methode `recv` nimmt die
erste Nachricht aus der Empfängerseite des Kanals und gibt ein `Ok(value)`
zurück. Als wir `recv` in Kapitel 16 zum ersten Mal gesehen haben, haben wir den
Fehler direkt entpackt oder über eine `for`-Schleife wie mit einem Iterator
damit interagiert. Wie Listing 19-4 zeigt, können wir aber auch `while let`
verwenden, weil die Methode `recv` jedes Mal ein `Ok` zurückgibt, wenn eine
Nachricht eintrifft, solange der Sender existiert, und dann ein `Err` erzeugt,
sobald die Senderseite die Verbindung trennt.

### `for`-Schleifen {#for-loops}

In einer `for`-Schleife ist der Wert, der direkt auf das Schlüsselwort `for`
folgt, ein Pattern. In `for x in y` ist zum Beispiel `x` das Pattern. Listing
19-5 zeigt, wie man in einer `for`-Schleife ein Pattern verwendet, um als Teil
der `for`-Schleife ein Tupel zu destrukturieren, also zu zerlegen.

<Listing number="19-5" caption="Ein Pattern in einer `for`-Schleife verwenden, um ein Tupel zu destrukturieren">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-05/src/main.rs:here}}
```

</Listing>

Der Code in Listing 19-5 gibt Folgendes aus:

```console
{{#include ../listings/ch19-patterns-and-matching/listing-19-05/output.txt}}
```

Wir passen einen Iterator mit der Methode `enumerate` so an, dass er einen Wert
und den Index für diesen Wert erzeugt, zusammengefasst in einem Tupel. Der erste
erzeugte Wert ist das Tupel `(0, 'a')`. Wenn dieser Wert mit dem Pattern
`(index,
value)` abgeglichen wird, ist index `0` und value `'a'`, und die erste
Zeile der Ausgabe wird ausgegeben.

### Funktionsparameter {#function-parameters}

Auch Funktionsparameter können Patterns sein. Der Code in Listing 19-6, der eine
Funktion namens `foo` deklariert, die einen Parameter namens `x` vom Typ `i32`
nimmt, sollte dir inzwischen vertraut vorkommen.

<Listing number="19-6" caption="Eine Funktionssignatur, die in den Parametern Patterns verwendet">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-06/src/main.rs:here}}
```

</Listing>

Der Teil `x` ist ein Pattern! Wie bei `let` könnten wir ein Tupel in den
Argumenten einer Funktion mit dem Pattern abgleichen. Listing 19-7 zerlegt die
Werte in einem Tupel, während wir es an eine Funktion übergeben.

<Listing number="19-7" file-name="src/main.rs" caption="Eine Funktion mit Parametern, die ein Tupel destrukturieren">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-07/src/main.rs}}
```

</Listing>

Dieser Code gibt `Current location: (3, 5)` aus. Die Werte `&(3, 5)` passen auf
das Pattern `&(x, y)`, also ist `x` der Wert `3` und `y` der Wert `5`.

Wir können Patterns auch in Parameterlisten von Closures auf dieselbe Weise
verwenden wie in Parameterlisten von Funktionen, weil Closures Funktionen
ähneln, wie in Kapitel 13 besprochen.

Inzwischen hast du mehrere Möglichkeiten gesehen, Patterns zu verwenden, aber
Patterns funktionieren nicht an jeder Stelle, an der wir sie verwenden können,
gleich. An manchen Stellen müssen die Patterns unabweisbar sein; unter anderen
Umständen können sie abweisbar sein. Diese beiden Konzepte besprechen wir als
Nächstes.

{{#quiz ../quizzes/ch18-01-all-the-places-for-patterns.toml}}

[ignoring-values-in-a-pattern]: ch19-03-pattern-syntax.html#ignoring-values-in-a-pattern
