## Kontrollfluss {#control-flow}

Die Möglichkeit, Code abhängig davon auszuführen, ob eine Bedingung `true` ist,
und die Möglichkeit, Code wiederholt auszuführen, solange eine Bedingung `true`
ist, sind grundlegende Bausteine der meisten Programmiersprachen. Die gängigsten
Konstrukte, mit denen du den Ausführungsfluss von Rust-Code steuern kannst, sind
`if`-Ausdrücke und Schleifen.

### `if`-Ausdrücke {#if-expressions}

Mit einem `if`-Ausdruck kannst du deinen Code abhängig von Bedingungen
verzweigen. Du gibst eine Bedingung an und sagst dann: „Wenn diese Bedingung
erfüllt ist, führe diesen Codeblock aus. Wenn sie nicht erfüllt ist, führe
diesen Codeblock nicht aus.“

Lege in deinem Verzeichnis _projects_ ein neues Projekt namens _branches_ an, um
den `if`-Ausdruck zu erkunden. Gib in die Datei _src/main.rs_ Folgendes ein:

<span class="filename">Dateiname: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-26-if-true/src/main.rs}}
```

Alle `if`-Ausdrücke beginnen mit dem Schlüsselwort `if`, gefolgt von einer
Bedingung. In diesem Fall prüft die Bedingung, ob die Variable `number` einen
Wert kleiner als 5 hat. Den Codeblock, der ausgeführt werden soll, wenn die
Bedingung `true` ist, setzen wir direkt nach der Bedingung in geschweifte
Klammern. Die Codeblöcke, die zu den Bedingungen in `if`-Ausdrücken gehören,
werden manchmal _Arme_ genannt, genau wie die Arme in `match`-Ausdrücken, die
wir im Abschnitt
[„Den Tipp mit der Geheimzahl vergleichen“][comparing-the-guess-to-the-secret-number]<!-- ignore -->
in Kapitel 2 besprochen haben.

Optional können wir auch einen `else`-Ausdruck hinzufügen, wie wir es hier getan
haben, um dem Programm einen alternativen Codeblock zu geben, der ausgeführt
wird, falls die Bedingung zu `false` ausgewertet wird. Wenn du keinen
`else`-Ausdruck angibst und die Bedingung `false` ist, überspringt das Programm
einfach den `if`-Block und macht mit dem nächsten Codeteil weiter.

Führe diesen Code aus; du solltest folgende Ausgabe sehen:

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-26-if-true/output.txt}}
```

Ändern wir den Wert von `number` auf einen Wert, der die Bedingung `false`
macht, und sehen wir, was passiert:

```rust,ignore
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-27-if-false/src/main.rs:here}}
```

Führe das Programm erneut aus und sieh dir die Ausgabe an:

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-27-if-false/output.txt}}
```

Erwähnenswert ist auch, dass die Bedingung in diesem Code ein `bool` sein
_muss_. Ist die Bedingung kein `bool`, bekommen wir einen Fehler. Versuch zum
Beispiel, folgenden Code auszuführen:

<span class="filename">Dateiname: src/main.rs</span>

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-28-if-condition-must-be-bool/src/main.rs}}
```

Die `if`-Bedingung wird diesmal zum Wert `3` ausgewertet, und Rust meldet einen
Fehler:

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-28-if-condition-must-be-bool/output.txt}}
```

Der Fehler zeigt an, dass Rust ein `bool` erwartet, aber eine Ganzzahl bekommen
hat. Anders als Sprachen wie Ruby oder JavaScript versucht Rust nicht
automatisch, nicht-boolesche Typen in einen booleschen Wert umzuwandeln. Du
musst explizit sein und `if` immer einen booleschen Wert als Bedingung geben.
Wenn wir zum Beispiel wollen, dass der `if`-Codeblock nur ausgeführt wird, wenn
eine Zahl ungleich `0` ist, können wir den `if`-Ausdruck so ändern:

<span class="filename">Dateiname: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-29-if-not-equal-0/src/main.rs}}
```

Dieser Code gibt `number was something other than zero` aus.

#### Mehrere Bedingungen mit `else if` behandeln {#handling-multiple-conditions-with-else-if}

Du kannst mehrere Bedingungen verwenden, indem du `if` und `else` zu einem
`else if`-Ausdruck kombinierst. Zum Beispiel:

<span class="filename">Dateiname: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-30-else-if/src/main.rs}}
```

Dieses Programm hat vier mögliche Pfade. Wenn du es ausführst, solltest du
folgende Ausgabe sehen:

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-30-else-if/output.txt}}
```

Wenn dieses Programm ausgeführt wird, prüft es nacheinander jeden `if`-Ausdruck
und führt den ersten Rumpf aus, dessen Bedingung zu `true` ausgewertet wird.
Beachte: Obwohl 6 durch 2 teilbar ist, sehen wir weder die Ausgabe
`number is divisible by 2` noch den Text `number is not divisible by 4, 3, or 2`
aus dem `else`-Block. Das liegt daran, dass Rust nur den Block für die erste
`true`-Bedingung ausführt und, sobald es eine gefunden hat, den Rest gar nicht
mehr prüft.

Zu viele `else if`-Ausdrücke können deinen Code unübersichtlich machen; wenn du
mehr als einen hast, solltest du deinen Code vielleicht refaktorisieren. Kapitel
6 beschreibt für solche Fälle ein mächtiges Verzweigungskonstrukt von Rust
namens `match`.

#### `if` in einer `let`-Anweisung verwenden {#using-if-in-a-let-statement}

Weil `if` ein Ausdruck ist, können wir es auf der rechten Seite einer
`let`-Anweisung verwenden, um das Ergebnis einer Variable zuzuweisen, wie in
Listing 3-2.

<Listing number="3-2" file-name="src/main.rs" caption="Das Ergebnis eines `if`-Ausdrucks einer Variable zuweisen">

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/listing-03-02/src/main.rs}}
```

</Listing>

Die Variable `number` wird an einen Wert gebunden, der vom Ergebnis des
`if`-Ausdrucks abhängt. Führe diesen Code aus, um zu sehen, was passiert:

```console
{{#include ../listings/ch03-common-programming-concepts/listing-03-02/output.txt}}
```

Denk daran, dass Codeblöcke zum letzten Ausdruck in ihnen ausgewertet werden und
dass Zahlen für sich genommen ebenfalls Ausdrücke sind. In diesem Fall hängt der
Wert des gesamten `if`-Ausdrucks davon ab, welcher Codeblock ausgeführt wird.
Das bedeutet, dass die Werte, die als Ergebnis aus jedem Arm des `if`
hervorgehen können, denselben Typ haben müssen; in Listing 3-2 waren die
Ergebnisse sowohl des `if`-Arms als auch des `else`-Arms `i32`-Ganzzahlen.
Passen die Typen nicht zusammen, wie im folgenden Beispiel, bekommen wir einen
Fehler:

<span class="filename">Dateiname: src/main.rs</span>

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-31-arms-must-return-same-type/src/main.rs}}
```

Wenn wir versuchen, diesen Code zu kompilieren, bekommen wir einen Fehler. Die
Arme `if` und `else` haben Werttypen, die nicht zueinander passen, und Rust
zeigt genau an, wo im Programm das Problem liegt:

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-31-arms-must-return-same-type/output.txt}}
```

Der Ausdruck im `if`-Block wird zu einer Ganzzahl ausgewertet, der Ausdruck im
`else`-Block zu einem String. Das funktioniert nicht, denn Variablen müssen
einen einzigen Typ haben, und Rust muss zur Kompilierzeit sicher wissen, welchen
Typ die Variable `number` hat. Kennt der Compiler den Typ von `number`, kann er
prüfen, ob der Typ überall gültig ist, wo wir `number` verwenden. Das könnte
Rust nicht, wenn der Typ von `number` erst zur Laufzeit feststünde; der Compiler
wäre komplexer und könnte weniger Garantien über den Code geben, wenn er für
jede Variable mehrere hypothetische Typen verfolgen müsste.

{{#quiz ../quizzes/ch03-05-control-flow-sec1-if.toml}}

### Wiederholung mit Schleifen {#repetition-with-loops}

Oft ist es nützlich, einen Codeblock mehr als einmal auszuführen. Für diese
Aufgabe bietet Rust mehrere _Schleifen_, die den Code im Schleifenrumpf bis zum
Ende durchlaufen und dann sofort wieder von vorn beginnen. Um mit Schleifen zu
experimentieren, legen wir ein neues Projekt namens _loops_ an.

Rust hat drei Arten von Schleifen: `loop`, `while` und `for`. Probieren wir jede
davon aus.

#### Code mit `loop` wiederholen {#repeating-code-with-loop}

Das Schlüsselwort `loop` weist Rust an, einen Codeblock immer wieder
auszuführen, entweder für immer oder bis du ihm explizit sagst, dass es aufhören
soll.

Ändere als Beispiel die Datei _src/main.rs_ in deinem Verzeichnis _loops_ so:

<span class="filename">Dateiname: src/main.rs</span>

```rust,ignore
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-32-loop/src/main.rs}}
```

Wenn wir dieses Programm ausführen, sehen wir `again!` immer wieder ausgegeben,
bis wir das Programm von Hand anhalten. Die meisten Terminals unterstützen die
Tastenkombination <kbd>ctrl</kbd>-<kbd>C</kbd>, um ein Programm abzubrechen, das
in einer Endlosschleife feststeckt. Probier es aus:

<!-- manual-regeneration
cd listings/ch03-common-programming-concepts/no-listing-32-loop
cargo run
CTRL-C
-->

```console
$ cargo run
   Compiling loops v0.1.0 (file:///projects/loops)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.08s
     Running `target/debug/loops`
again!
again!
again!
again!
^Cagain!
```

Das Symbol `^C` zeigt an, wo du <kbd>ctrl</kbd>-<kbd>C</kbd> gedrückt hast.

Ob du nach dem `^C` noch das Wort `again!` siehst, hängt davon ab, wo sich der
Code in der Schleife befand, als er das Unterbrechungssignal erhielt.

Zum Glück bietet Rust auch eine Möglichkeit, eine Schleife per Code zu
verlassen. Du kannst das Schlüsselwort `break` in die Schleife schreiben, um dem
Programm mitzuteilen, wann es die Ausführung der Schleife beenden soll. Erinnere
dich: Genau das haben wir im Ratespiel im Abschnitt
[„Nach einem richtigen Tipp beenden“][quitting-after-a-correct-guess]<!-- ignore -->
in Kapitel 2 getan, um das Programm zu beenden, wenn der Benutzer das Spiel
durch Erraten der richtigen Zahl gewonnen hatte.

Im Ratespiel haben wir außerdem `continue` verwendet, das in einer Schleife das
Programm anweist, den restlichen Code in dieser Iteration der Schleife zu
überspringen und mit der nächsten Iteration weiterzumachen.

#### Werte aus Schleifen zurückgeben {#returning-values-from-loops}

Eine Verwendung von `loop` ist, eine Operation erneut zu versuchen, von der du
weißt, dass sie fehlschlagen könnte, etwa zu prüfen, ob ein Thread seine Arbeit
erledigt hat. Möglicherweise musst du das Ergebnis dieser Operation aus der
Schleife an den Rest deines Codes weitergeben. Dazu kannst du den Wert, der
zurückgegeben werden soll, hinter den `break`-Ausdruck schreiben, mit dem du die
Schleife beendest; dieser Wert wird aus der Schleife zurückgegeben, sodass du
ihn verwenden kannst, wie hier gezeigt:

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-33-return-value-from-loop/src/main.rs}}
```

Vor der Schleife deklarieren wir eine Variable namens `counter` und
initialisieren sie mit `0`. Dann deklarieren wir eine Variable namens `result`,
die den von der Schleife zurückgegebenen Wert aufnimmt. Bei jeder Iteration der
Schleife addieren wir `1` zur Variable `counter` und prüfen dann, ob `counter`
gleich `10` ist. Ist das der Fall, verwenden wir das Schlüsselwort `break` mit
dem Wert `counter * 2`. Nach der Schleife beenden wir mit einem Semikolon die
Anweisung, die den Wert `result` zuweist. Schließlich geben wir den Wert in
`result` aus, der in diesem Fall `20` ist.

Du kannst auch aus einer Schleife heraus `return` verwenden. Während `break` nur
die aktuelle Schleife verlässt, verlässt `return` immer die aktuelle Funktion.

> _Hinweis:_ Das Semikolon nach `break counter * 2` ist technisch gesehen
> optional. `break` ähnelt `return` sehr: Beide können optional einen Ausdruck
> als Argument nehmen, und beide ändern den Kontrollfluss. Code nach einem
> `break` oder `return` wird nie ausgeführt, daher behandelt der Rust-Compiler
> einen `break`-Ausdruck und einen `return`-Ausdruck so, als hätten sie den Wert
> Unit, also `()`.

<!-- Old headings. Do not remove or links may break. -->

<a id="loop-labels-to-disambiguate-between-multiple-loops"></a>

#### Mit Schleifenlabels eindeutig machen {#disambiguating-with-loop-labels}

Wenn du Schleifen in Schleifen hast, beziehen sich `break` und `continue` auf
die innerste Schleife an dieser Stelle. Optional kannst du einer Schleife ein
_Schleifenlabel_ (_loop label_) geben, das du dann mit `break` oder `continue`
verwenden kannst, um anzugeben, dass sich diese Schlüsselwörter auf die
gekennzeichnete Schleife statt auf die innerste Schleife beziehen.
Schleifenlabels müssen mit einem einfachen Anführungszeichen beginnen. Hier ist
ein Beispiel mit zwei verschachtelten Schleifen:

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-32-5-loop-labels/src/main.rs}}
```

Die äußere Schleife hat das Label `'counting_up` und zählt von 0 bis 2 hoch. Die
innere Schleife ohne Label zählt von 10 auf 9 herunter. Das erste `break`, das
kein Label angibt, verlässt nur die innere Schleife. Die Anweisung
`break
'counting_up;` verlässt die äußere Schleife. Dieser Code gibt Folgendes
aus:

```console
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-32-5-loop-labels/output.txt}}
```

<!-- Old headings. Do not remove or links may break. -->

<a id="conditional-loops-with-while"></a>

#### Bedingte Schleifen mit while vereinfachen {#streamlining-conditional-loops-with-while}

Ein Programm muss oft innerhalb einer Schleife eine Bedingung auswerten. Solange
die Bedingung `true` ist, läuft die Schleife. Sobald die Bedingung nicht mehr
`true` ist, ruft das Programm `break` auf und beendet die Schleife. Ein solches
Verhalten lässt sich mit einer Kombination aus `loop`, `if`, `else` und `break`
implementieren; wenn du magst, kannst du das jetzt in einem Programm
ausprobieren. Dieses Pattern ist jedoch so verbreitet, dass Rust dafür ein
eingebautes Sprachkonstrukt hat, die `while`-Schleife. In Listing 3-3 verwenden
wir `while`, um das Programm dreimal in einer Schleife laufen zu lassen, dabei
jedes Mal herunterzuzählen und nach der Schleife eine Nachricht auszugeben und
zu beenden.

<Listing number="3-3" file-name="src/main.rs" caption="Eine `while`-Schleife verwenden, um Code auszuführen, solange eine Bedingung zu `true` ausgewertet wird">

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/listing-03-03/src/main.rs}}
```

</Listing>

Dieses Konstrukt erspart viel Verschachtelung, die nötig wäre, wenn du `loop`,
`if`, `else` und `break` verwenden würdest, und es ist übersichtlicher. Solange
eine Bedingung zu `true` ausgewertet wird, läuft der Code; andernfalls wird die
Schleife verlassen.

#### Mit `for` durch eine Collection iterieren {#looping-through-a-collection-with-for}

Du kannst das Konstrukt `while` auch verwenden, um über die Elemente einer
Collection wie eines Arrays zu iterieren. Die Schleife in Listing 3-4 gibt zum
Beispiel jedes Element im Array `a` aus.

<Listing number="3-4" file-name="src/main.rs" caption="Mit einer `while`-Schleife durch jedes Element einer Collection iterieren">

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/listing-03-04/src/main.rs}}
```

</Listing>

Hier zählt der Code die Elemente im Array hoch. Er beginnt bei Index `0` und
läuft dann in der Schleife, bis er den letzten Index im Array erreicht (also bis
`index < 5` nicht mehr `true` ist). Dieser Code gibt jedes Element im Array aus:

```console
{{#include ../listings/ch03-common-programming-concepts/listing-03-04/output.txt}}
```

Wie erwartet erscheinen alle fünf Array-Werte im Terminal. Obwohl `index`
irgendwann den Wert `5` erreicht, hört die Schleife auf, bevor sie versucht,
einen sechsten Wert aus dem Array zu holen.

Dieser Ansatz ist allerdings fehleranfällig; wir könnten einen Panic im Programm
verursachen, wenn der Indexwert oder die Testbedingung falsch ist. Wenn du zum
Beispiel die Definition des Arrays `a` auf vier Elemente änderst, aber vergisst,
die Bedingung auf `while index < 4` anzupassen, löst der Code einen Panic aus.
Außerdem ist er langsam, weil der Compiler Laufzeitcode hinzufügt, der bei jedem
Schleifendurchlauf prüft, ob der Index innerhalb der Grenzen des Arrays liegt.

Als knappere Alternative kannst du eine `for`-Schleife verwenden und Code für
jedes Element einer Collection ausführen. Eine `for`-Schleife sieht aus wie der
Code in Listing 3-5.

<Listing number="3-5" file-name="src/main.rs" caption="Mit einer `for`-Schleife durch jedes Element einer Collection iterieren">

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/listing-03-05/src/main.rs}}
```

</Listing>

Wenn wir diesen Code ausführen, sehen wir dieselbe Ausgabe wie in Listing 3-4.
Wichtiger ist, dass wir jetzt die Sicherheit des Codes erhöht und die Gefahr von
Bugs beseitigt haben, die entstehen könnten, wenn wir über das Ende des Arrays
hinausgehen oder nicht weit genug gehen und Elemente auslassen. Aus
`for`-Schleifen erzeugter Maschinencode kann außerdem effizienter sein, weil der
Index nicht bei jeder Iteration mit der Länge des Arrays verglichen werden muss.

Mit der `for`-Schleife müsstest du nicht daran denken, anderen Code zu ändern,
wenn du die Anzahl der Werte im Array änderst, wie es bei der Methode aus
Listing 3-4 nötig wäre.

Sicherheit und Knappheit machen `for`-Schleifen zum meistverwendeten
Schleifenkonstrukt in Rust. Selbst in Situationen, in denen du Code eine
bestimmte Anzahl von Malen ausführen willst, wie im Countdown-Beispiel mit der
`while`-Schleife in Listing 3-3, würden die meisten Rustaceans eine
`for`-Schleife verwenden. Dazu verwendet man eine `Range` aus der
Standardbibliothek, die alle Zahlen der Reihe nach erzeugt, beginnend bei einer
Zahl und endend vor einer anderen.

So würde der Countdown mit einer `for`-Schleife und einer weiteren Methode
aussehen, über die wir noch nicht gesprochen haben, `rev`, die den Bereich
umkehrt:

<span class="filename">Dateiname: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-34-for-range/src/main.rs}}
```

Dieser Code ist etwas schöner, oder?

{{#quiz ../quizzes/ch03-05-control-flow-sec2-loops.toml}}

## Zusammenfassung {#summary}

Geschafft! Das war ein umfangreiches Kapitel: Du hast Variablen, skalare und
zusammengesetzte Datentypen, Funktionen, Kommentare, `if`-Ausdrücke und
Schleifen kennengelernt! Um die Konzepte aus diesem Kapitel zu üben, versuch,
Programme zu bauen, die Folgendes tun:

- Temperaturen zwischen Fahrenheit und Celsius umrechnen.
- Die _n_-te Fibonacci-Zahl erzeugen.
- Den Text des Weihnachtslieds „The Twelve Days of Christmas“ ausgeben und dabei
  die Wiederholungen im Lied ausnutzen.

Wenn du bereit bist weiterzumachen, sprechen wir über ein Konzept in Rust, das
es in anderen Programmiersprachen üblicherweise _nicht_ gibt: Ownership.

[comparing-the-guess-to-the-secret-number]: ch02-00-guessing-game-tutorial.html#comparing-the-guess-to-the-secret-number
[quitting-after-a-correct-guess]: ch02-00-guessing-game-tutorial.html#quitting-after-a-correct-guess
