## Abweisbarkeit: Ob ein Pattern möglicherweise nicht passt {#refutability-whether-a-pattern-might-fail-to-match}

Patterns gibt es in zwei Formen: abweisbar (_refutable_) und unabweisbar
(_irrefutable_). Patterns, die auf jeden möglichen übergebenen Wert passen, sind
_unabweisbar_. Ein Beispiel wäre `x` in der Anweisung `let x = 5;`, weil `x` auf
alles passt und daher nicht fehlschlagen kann. Patterns, die für einen möglichen
Wert nicht passen können, sind _abweisbar_. Hier sind einige Beispiele:

<!-- BEGIN INTERVENTION: 3c29eb2d-cbe9-4a2c-99b8-aa5c6467c8b4 -->

- Im Ausdruck `if let Some(x) = a_value` ist `Some(x)` abweisbar. Wenn der Wert
  in der Variablen `a_value` `None` statt `Some` ist, passt das Pattern
  `Some(x)` nicht.
- Im Ausdruck `if let &[x, ..] = a_slice` ist `&[x, ..]` abweisbar. Wenn der
  Wert in der Variablen `a_slice` null Elemente hat, passt das Pattern
  `&[x, ..]` nicht.

<!-- END INTERVENTION: 3c29eb2d-cbe9-4a2c-99b8-aa5c6467c8b4 -->

Funktionsparameter, `let`-Anweisungen und `for`-Schleifen können nur
unabweisbare Patterns akzeptieren, weil das Programm nichts Sinnvolles tun kann,
wenn Werte nicht passen. Die Ausdrücke `if let` und `while let` sowie die
Anweisung `let...else` akzeptieren abweisbare und unabweisbare Patterns, aber
der Compiler warnt vor unabweisbaren Patterns, weil sie per Definition dazu
gedacht sind, ein mögliches Fehlschlagen zu behandeln: Die Funktionalität einer
Bedingung liegt darin, sich je nach Erfolg oder Fehlschlag unterschiedlich zu
verhalten.

Im Allgemeinen solltest du dir über die Unterscheidung zwischen abweisbaren und
unabweisbaren Patterns keine Gedanken machen müssen; du musst aber mit dem
Konzept der Abweisbarkeit (_refutability_) vertraut sein, damit du reagieren
kannst, wenn es dir in einer Fehlermeldung begegnet. In diesen Fällen musst du
je nach beabsichtigtem Verhalten des Codes entweder das Pattern oder das
Konstrukt ändern, mit dem du das Pattern verwendest.

Sehen wir uns ein Beispiel dafür an, was passiert, wenn wir versuchen, ein
abweisbares Pattern dort zu verwenden, wo Rust ein unabweisbares Pattern
verlangt, und umgekehrt. Listing 19-8 zeigt eine `let`-Anweisung, aber als
Pattern haben wir `Some(x)` angegeben, ein abweisbares Pattern. Wie du
vielleicht erwartest, kompiliert dieser Code nicht.

<Listing number="19-8" caption="Versuch, ein abweisbares Pattern mit `let` zu verwenden">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-08/src/main.rs:here}}
```

</Listing>

Wäre `some_option_value` ein `None`-Wert, würde er nicht auf das Pattern
`Some(x)` passen, das heißt, das Pattern ist abweisbar. Die `let`-Anweisung kann
aber nur ein unabweisbares Pattern akzeptieren, weil der Code mit einem
`None`-Wert nichts Gültiges anfangen kann. Zur Kompilierzeit beschwert sich
Rust, dass wir versucht haben, ein abweisbares Pattern dort zu verwenden, wo ein
unabweisbares Pattern erforderlich ist:

```console
{{#include ../listings/ch19-patterns-and-matching/listing-19-08/output.txt}}
```

Weil wir mit dem Pattern `Some(x)` nicht jeden gültigen Wert abgedeckt haben
(und nicht abdecken konnten!), erzeugt Rust zu Recht einen Compilerfehler.

Wenn wir ein abweisbares Pattern haben, wo ein unabweisbares Pattern gebraucht
wird, können wir das beheben, indem wir den Code ändern, der das Pattern
verwendet: Statt `let` können wir `let...else` verwenden. Wenn das Pattern dann
nicht passt, behandelt der Code in den geschweiften Klammern den Wert. Listing
19-9 zeigt, wie man den Code in Listing 19-8 korrigiert.

<Listing number="19-9" caption="`let...else` und einen Block mit abweisbaren Patterns statt `let` verwenden">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-09/src/main.rs:here}}
```

</Listing>

Wir haben dem Code einen Ausweg gegeben! Dieser Code ist völlig gültig, auch
wenn das bedeutet, dass wir kein unabweisbares Pattern verwenden können, ohne
eine Warnung zu bekommen. Wenn wir `let...else` ein Pattern geben, das immer
passt, etwa `x`, wie in Listing 19-10 gezeigt, gibt der Compiler eine Warnung
aus.

<Listing number="19-10" caption="Versuch, ein unabweisbares Pattern mit `let...else` zu verwenden">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-10/src/main.rs:here}}
```

</Listing>

Rust beschwert sich, dass es keinen Sinn ergibt, `let...else` mit einem
unabweisbaren Pattern zu verwenden:

```console
{{#include ../listings/ch19-patterns-and-matching/listing-19-10/output.txt}}
```

Aus diesem Grund müssen Match-Arme abweisbare Patterns verwenden, mit Ausnahme
des letzten Arms, der alle verbleibenden Werte mit einem unabweisbaren Pattern
abdecken sollte. Rust erlaubt es uns, in einem `match` mit nur einem Arm ein
unabweisbares Pattern zu verwenden, aber diese Syntax ist nicht besonders
nützlich und könnte durch eine einfachere `let`-Anweisung ersetzt werden.

Jetzt, da du weißt, wo man Patterns verwendet und was der Unterschied zwischen
abweisbaren und unabweisbaren Patterns ist, behandeln wir die gesamte Syntax,
mit der wir Patterns erstellen können.

{{#quiz ../quizzes/ch18-02-refutability.toml}}
