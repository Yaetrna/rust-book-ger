## Variablen und Veränderlichkeit {#variables-and-mutability}

Wie im Abschnitt [„Werte in Variablen speichern“][storing-values-with-variables]<!-- ignore --> erwähnt, sind Variablen standardmäßig unveränderlich (_immutable_). Das ist einer von vielen Anstößen, die Rust dir gibt, damit du deinen Code so schreibst, dass er die Sicherheit und die einfache Nebenläufigkeit nutzt, die Rust bietet. Du hast aber trotzdem die Möglichkeit, deine Variablen veränderlich (_mutable_) zu machen. Sehen wir uns an, wie und warum Rust dich ermutigt, Unveränderlichkeit zu bevorzugen, und warum du manchmal darauf verzichten möchtest.

Wenn eine Variable unveränderlich ist, kannst du einen Wert, sobald er an einen Namen gebunden ist, nicht mehr ändern. Um das zu veranschaulichen, erzeuge in deinem Verzeichnis _projects_ mit `cargo new variables` ein neues Projekt namens _variables_.

Öffne dann in deinem neuen Verzeichnis _variables_ die Datei _src/main.rs_ und ersetze ihren Code durch den folgenden Code, der sich noch nicht kompilieren lässt:

<span class="filename">Dateiname: src/main.rs</span>

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-01-variables-are-immutable/src/main.rs}}
```

Speichere das Programm und führe es mit `cargo run` aus. Du solltest eine Fehlermeldung zu einem Unveränderlichkeitsfehler erhalten, wie in dieser Ausgabe gezeigt:

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-01-variables-are-immutable/output.txt}}
```

Dieses Beispiel zeigt, wie der Compiler dir hilft, Fehler in deinen Programmen zu finden. Compilerfehler können frustrierend sein, aber eigentlich bedeuten sie nur, dass dein Programm noch nicht sicher das tut, was du willst; sie bedeuten _nicht_, dass du keine gute Programmiererin oder kein guter Programmierer bist! Auch erfahrene Rustaceans bekommen Compilerfehler.

Du hast die Fehlermeldung `` cannot assign twice to immutable variable `x` `` (einer unveränderlichen Variable kann nicht zweimal etwas zugewiesen werden) erhalten, weil du versucht hast, der unveränderlichen Variable `x` einen zweiten Wert zuzuweisen.

Es ist wichtig, dass wir Fehler zur Kompilierzeit bekommen, wenn wir versuchen, einen als unveränderlich gekennzeichneten Wert zu ändern, denn genau diese Situation kann zu Bugs führen. Wenn ein Teil unseres Codes davon ausgeht, dass sich ein Wert nie ändert, und ein anderer Teil unseres Codes diesen Wert ändert, tut der erste Teil des Codes möglicherweise nicht das, wofür er gedacht ist. Die Ursache eines solchen Bugs lässt sich im Nachhinein oft schwer aufspüren, besonders wenn das zweite Codestück den Wert nur _manchmal_ ändert. Der Rust-Compiler garantiert: Wenn du angibst, dass sich ein Wert nicht ändert, ändert er sich wirklich nicht, sodass du das nicht selbst im Blick behalten musst. Dadurch lässt sich dein Code leichter nachvollziehen.

Veränderlichkeit kann aber sehr nützlich sein und das Schreiben von Code bequemer machen. Obwohl Variablen standardmäßig unveränderlich sind, kannst du sie veränderlich machen, indem du `mut` vor den Variablennamen schreibst, wie du es in [Kapitel 2][storing-values-with-variables]<!-- ignore --> getan hast. Das Hinzufügen von `mut` vermittelt künftigen Leserinnen und Lesern des Codes außerdem eine Absicht: Es zeigt an, dass andere Teile des Codes den Wert dieser Variable ändern werden.

Ändern wir _src/main.rs_ zum Beispiel wie folgt:

<span class="filename">Dateiname: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-02-adding-mut/src/main.rs}}
```

Wenn wir das Programm jetzt ausführen, erhalten wir Folgendes:

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-02-adding-mut/output.txt}}
```

Mit `mut` dürfen wir den an `x` gebundenen Wert von `5` auf `6` ändern. Letztlich entscheidest du selbst, ob du Veränderlichkeit verwendest oder nicht, je nachdem, was du in der jeweiligen Situation am klarsten findest.

{{#quiz ../quizzes/ch03-01-variables-and-mutability-sec1-variables.toml}}

<!-- Old headings. Do not remove or links may break. -->

<a id="constants"></a>

### Konstanten deklarieren {#declaring-constants}

Wie unveränderliche Variablen sind _Konstanten_ Werte, die an einen Namen gebunden sind und sich nicht ändern dürfen, aber es gibt ein paar Unterschiede zwischen Konstanten und Variablen.

Erstens darfst du `mut` nicht mit Konstanten verwenden. Konstanten sind nicht nur standardmäßig unveränderlich – sie sind immer unveränderlich. Du deklarierst Konstanten mit dem Schlüsselwort `const` statt mit dem Schlüsselwort `let`, und der Typ des Werts _muss_ annotiert werden. Typen und Typannotationen behandeln wir im nächsten Abschnitt, [„Datentypen“][data-types]<!-- ignore -->, also mach dir jetzt noch keine Gedanken über die Details. Merk dir nur, dass du den Typ immer annotieren musst.

Konstanten können in jedem Gültigkeitsbereich (_scope_) deklariert werden, auch im globalen Gültigkeitsbereich. Dadurch eignen sie sich für Werte, die viele Teile des Codes kennen müssen.

Der letzte Unterschied ist, dass Konstanten nur auf einen konstanten Ausdruck gesetzt werden dürfen, nicht auf das Ergebnis eines Werts, der erst zur Laufzeit berechnet werden könnte.

Hier ist ein Beispiel für die Deklaration einer Konstante:

```rust
const THREE_HOURS_IN_SECONDS: u32 = 60 * 60 * 3;
```

Die Konstante heißt `THREE_HOURS_IN_SECONDS`, und ihr Wert ist das Ergebnis der Multiplikation von 60 (der Anzahl der Sekunden in einer Minute) mit 60 (der Anzahl der Minuten in einer Stunde) mit 3 (der Anzahl der Stunden, die wir in diesem Programm zählen wollen). Die Namenskonvention von Rust für Konstanten ist, nur Großbuchstaben zu verwenden und Wörter mit Unterstrichen zu trennen. Der Compiler kann eine begrenzte Menge von Operationen zur Kompilierzeit auswerten. Dadurch können wir diesen Wert so ausschreiben, dass er leichter zu verstehen und zu überprüfen ist, statt die Konstante auf den Wert 10.800 zu setzen. Im [Abschnitt der Rust-Referenz zur konstanten Auswertung][const-eval] erfährst du mehr darüber, welche Operationen beim Deklarieren von Konstanten verwendet werden können.

Konstanten sind während der gesamten Laufzeit eines Programms gültig, innerhalb des Gültigkeitsbereichs, in dem sie deklariert wurden. Das macht Konstanten nützlich für Werte aus dem Anwendungsbereich, die mehrere Teile des Programms kennen müssen, etwa die maximale Punktzahl, die ein Spieler in einem Spiel erreichen darf, oder die Lichtgeschwindigkeit.

Fest einprogrammierte Werte, die im ganzen Programm verwendet werden, als Konstanten zu benennen, hilft dabei, die Bedeutung dieses Werts an künftige Betreuerinnen und Betreuer des Codes weiterzugeben. Außerdem gibt es dann nur eine einzige Stelle in deinem Code, die du ändern musst, falls der fest einprogrammierte Wert in Zukunft aktualisiert werden muss.

{{#quiz ../quizzes/ch03-01-variables-and-mutability-sec2-constants.toml}}

### Shadowing {#shadowing}

Wie du im Ratespiel-Tutorial in [Kapitel 2][comparing-the-guess-to-the-secret-number]<!-- ignore --> gesehen hast, kannst du eine neue Variable mit demselben Namen wie eine vorherige Variable deklarieren. Rustaceans sagen, dass die erste Variable von der zweiten _überschattet_ (_shadowed_) wird. Das bedeutet, dass der Compiler die zweite Variable sieht, wenn du den Namen der Variable verwendest. Im Endeffekt stellt die zweite Variable die erste in den Schatten und zieht alle Verwendungen des Variablennamens auf sich, bis sie entweder selbst überschattet wird oder der Gültigkeitsbereich endet. Wir können eine Variable überschatten, indem wir denselben Variablennamen verwenden und das Schlüsselwort `let` wiederholen, wie folgt:

<span class="filename">Dateiname: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-03-shadowing/src/main.rs}}
```

Dieses Programm bindet `x` zunächst an den Wert `5`. Dann erzeugt es durch Wiederholen von `let x =` eine neue Variable `x`, nimmt den ursprünglichen Wert und addiert `1`, sodass `x` den Wert `6` hat. Anschließend überschattet innerhalb eines inneren Gültigkeitsbereichs, der mit den geschweiften Klammern erzeugt wird, die dritte `let`-Anweisung `x` ebenfalls und erzeugt eine neue Variable, indem sie den vorherigen Wert mit `2` multipliziert, sodass `x` den Wert `12` hat. Wenn dieser Gültigkeitsbereich endet, endet auch das innere Shadowing, und `x` ist wieder `6`. Wenn wir dieses Programm ausführen, gibt es Folgendes aus:

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-03-shadowing/output.txt}}
```

Shadowing unterscheidet sich davon, eine Variable als `mut` zu markieren, denn wir bekommen einen Fehler zur Kompilierzeit, wenn wir versehentlich versuchen, dieser Variable ohne das Schlüsselwort `let` etwas neu zuzuweisen. Mit `let` können wir einige Umwandlungen an einem Wert vornehmen, aber die Variable ist unveränderlich, sobald diese Umwandlungen abgeschlossen sind.

Der andere Unterschied zwischen `mut` und Shadowing ist: Weil wir beim erneuten Verwenden des Schlüsselworts `let` tatsächlich eine neue Variable erzeugen, können wir den Typ des Werts ändern und trotzdem denselben Namen wiederverwenden. Angenommen, unser Programm fordert einen Benutzer auf, durch Eingabe von Leerzeichen anzugeben, wie viele Leerzeichen er zwischen einem Text haben möchte, und wir wollen diese Eingabe dann als Zahl speichern:

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-04-shadowing-can-change-types/src/main.rs:here}}
```

Die erste Variable `spaces` hat einen String-Typ, die zweite Variable `spaces` einen Zahlentyp. Shadowing erspart uns also, uns verschiedene Namen wie `spaces_str` und `spaces_num` ausdenken zu müssen; stattdessen können wir den einfacheren Namen `spaces` wiederverwenden. Wenn wir dafür jedoch `mut` verwenden wollen, wie hier gezeigt, bekommen wir einen Fehler zur Kompilierzeit:

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-05-mut-cant-change-types/src/main.rs:here}}
```

Der Fehler besagt, dass wir den Typ einer Variable nicht verändern dürfen:

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-05-mut-cant-change-types/output.txt}}
```

Nachdem wir uns angesehen haben, wie Variablen funktionieren, sehen wir uns weitere Datentypen an, die sie haben können.

{{#quiz ../quizzes/ch03-01-variables-and-mutability-sec3-shadowing.toml}}

[comparing-the-guess-to-the-secret-number]: ch02-00-guessing-game-tutorial.html#comparing-the-guess-to-the-secret-number
[data-types]: ch03-02-data-types.html#data-types
[storing-values-with-variables]: ch02-00-guessing-game-tutorial.html#storing-values-with-variables
[const-eval]: https://doc.rust-lang.org/reference/const_eval.html
