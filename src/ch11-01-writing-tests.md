## Wie man Tests schreibt {#how-to-write-tests}

_Tests_ sind Rust-Funktionen, die prüfen, ob der Code, der kein Test ist, wie
erwartet funktioniert. Die Rümpfe von Testfunktionen führen typischerweise diese
drei Aktionen aus:

- Alle benötigten Daten oder Zustände vorbereiten.
- Den Code ausführen, den du testen willst.
- Zusichern (_assert_), dass die Ergebnisse deinen Erwartungen entsprechen.

Sehen wir uns die Features an, die Rust speziell zum Schreiben von Tests mit
diesen Aktionen bereitstellt. Dazu gehören das Attribut `test`, einige Makros
und das Attribut `should_panic`.

<!-- Old headings. Do not remove or links may break. -->

<a id="the-anatomy-of-a-test-function"></a>

### Testfunktionen strukturieren {#structuring-test-functions}

Im einfachsten Fall ist ein Test in Rust eine Funktion, die mit dem Attribut
`test` annotiert ist. Attribute sind Metadaten über Teile von Rust-Code; ein
Beispiel ist das Attribut `derive`, das wir in Kapitel 5 mit Structs verwendet
haben. Um eine Funktion in eine Testfunktion zu verwandeln, füge `#[test]` in
der Zeile vor `fn` hinzu. Wenn du deine Tests mit dem Befehl `cargo test`
ausführst, baut Rust eine Testrunner-Binärdatei, die die annotierten Funktionen
ausführt und meldet, ob jede Testfunktion besteht oder fehlschlägt.

Immer wenn wir mit Cargo ein neues Bibliotheksprojekt anlegen, wird automatisch
ein Testmodul mit einer Testfunktion darin erzeugt. Dieses Modul gibt dir eine
Vorlage für deine Tests, sodass du nicht bei jedem neuen Projekt die genaue
Struktur und Syntax nachschlagen musst. Du kannst beliebig viele weitere
Testfunktionen und Testmodule hinzufügen!

Wir erkunden einige Aspekte der Funktionsweise von Tests, indem wir mit dem
Vorlagentest experimentieren, bevor wir tatsächlich Code testen. Dann schreiben
wir einige praxisnahe Tests, die Code aufrufen, den wir geschrieben haben, und
zusichern, dass sein Verhalten korrekt ist.

Legen wir ein neues Bibliotheksprojekt namens `adder` an, das zwei Zahlen
addiert:

```console
$ cargo new adder --lib
     Created library `adder` project
$ cd adder
```

Der Inhalt der Datei _src/lib.rs_ in deiner Bibliothek `adder` sollte aussehen
wie in Listing 11-1.

<Listing number="11-1" file-name="src/lib.rs" caption="Der Code, den `cargo new` automatisch erzeugt">

<!-- manual-regeneration
cd listings/ch11-writing-automated-tests
rm -rf listing-11-01
cargo new listing-11-01 --lib --name adder
cd listing-11-01
echo "$ cargo test" > output.txt
RUSTFLAGS="-A unused_variables -A dead_code" RUST_TEST_THREADS=1 cargo test >> output.txt 2>&1
git diff output.txt # commit any relevant changes; discard irrelevant ones
cd ../../..
-->

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/listing-11-01/src/lib.rs}}
```

</Listing>

Die Datei beginnt mit einer Beispielfunktion `add`, damit wir etwas zum Testen
haben.

Konzentrieren wir uns vorerst nur auf die Funktion `it_works`. Beachte die
Annotation `#[test]`: Dieses Attribut zeigt an, dass es sich um eine
Testfunktion handelt, damit der Testrunner weiß, dass er diese Funktion als Test
behandeln soll. Wir könnten im Modul `tests` auch Funktionen haben, die keine
Tests sind, etwa um gemeinsame Szenarien vorzubereiten oder gemeinsame
Operationen auszuführen, daher müssen wir immer angeben, welche Funktionen Tests
sind.

Der Rumpf der Beispielfunktion verwendet das Makro `assert_eq!`, um zuzusichern,
dass `result`, das das Ergebnis des Aufrufs von `add` mit 2 und 2 enthält,
gleich 4 ist. Diese Assertion dient als Beispiel für das Format eines typischen
Tests. Führen wir ihn aus, um zu sehen, dass dieser Test besteht.

Der Befehl `cargo test` führt alle Tests in unserem Projekt aus, wie in Listing
11-2 gezeigt.

<Listing number="11-2" caption="Die Ausgabe beim Ausführen des automatisch erzeugten Tests">

```console
{{#include ../listings/ch11-writing-automated-tests/listing-11-01/output.txt}}
```

</Listing>

Cargo hat den Test kompiliert und ausgeführt. Wir sehen die Zeile
`running 1 test`. Die nächste Zeile zeigt den Namen der erzeugten Testfunktion,
`tests::it_works`, und dass das Ergebnis dieses Tests `ok` ist. Die
Gesamtzusammenfassung `test
result: ok.` bedeutet, dass alle Tests bestanden
haben, und der Teil `1
passed; 0 failed` zählt die Tests zusammen, die bestanden
haben oder fehlgeschlagen sind.

Man kann einen Test als ignoriert markieren, damit er in einem bestimmten Fall
nicht ausgeführt wird; das behandeln wir im Abschnitt
[„Tests ignorieren, sofern sie nicht ausdrücklich angefordert werden“][ignoring]<!-- ignore -->
später in diesem Kapitel. Da wir das hier nicht getan haben, zeigt die
Zusammenfassung `0 ignored`. Wir können dem Befehl `cargo test` auch ein
Argument übergeben, um nur Tests auszuführen, deren Name zu einem String passt;
das nennt man _Filtern_, und wir behandeln es im Abschnitt
[„Eine Teilmenge von Tests nach Namen ausführen“][subset]<!-- ignore -->. Hier
haben wir die ausgeführten Tests nicht gefiltert, daher zeigt das Ende der
Zusammenfassung `0 filtered out`.

Die Statistik `0 measured` gilt für Benchmark-Tests, die die Performance messen.
Benchmark-Tests sind zum Zeitpunkt der Entstehung dieses Textes nur in
Nightly-Rust verfügbar. Mehr erfährst du in
[der Dokumentation zu Benchmark-Tests][bench].

Der nächste Teil der Testausgabe, der mit `Doc-tests adder` beginnt, ist für die
Ergebnisse von Dokumentationstests. Wir haben noch keine Dokumentationstests,
aber Rust kann alle Codebeispiele kompilieren, die in unserer API-Dokumentation
vorkommen. Dieses Feature hilft, deine Dokumentation und deinen Code synchron zu
halten! Wie man Dokumentationstests schreibt, besprechen wir im Abschnitt
[„Dokumentationskommentare als Tests“][doc-comments]<!-- ignore --> in
Kapitel 14. Vorerst ignorieren wir die Ausgabe `Doc-tests`.

Passen wir den Test an unsere eigenen Bedürfnisse an. Ändere zuerst den Namen
der Funktion `it_works` in einen anderen Namen, etwa `exploration`, so:

<span class="filename">Dateiname: src/lib.rs</span>

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/no-listing-01-changing-test-name/src/lib.rs}}
```

Führe dann erneut `cargo test` aus. Die Ausgabe zeigt jetzt `exploration` statt
`it_works`:

```console
{{#include ../listings/ch11-writing-automated-tests/no-listing-01-changing-test-name/output.txt}}
```

Jetzt fügen wir einen weiteren Test hinzu, aber diesmal einen Test, der
fehlschlägt! Tests schlagen fehl, wenn etwas in der Testfunktion einen Panic
auslöst. Jeder Test läuft in einem neuen Thread, und wenn der Haupt-Thread
sieht, dass ein Test-Thread beendet wurde, wird der Test als fehlgeschlagen
markiert. In Kapitel 9 haben wir besprochen, dass der einfachste Weg, einen
Panic auszulösen, der Aufruf des Makros `panic!` ist. Gib den neuen Test als
Funktion namens `another` ein, sodass deine Datei _src/lib.rs_ aussieht wie
Listing 11-3.

<Listing number="11-3" file-name="src/lib.rs" caption="Einen zweiten Test hinzufügen, der fehlschlägt, weil wir das Makro `panic!` aufrufen">

```rust,panics,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/listing-11-03/src/lib.rs}}
```

</Listing>

Führe die Tests erneut mit `cargo test` aus. Die Ausgabe sollte aussehen wie in
Listing 11-4, das zeigt, dass unser Test `exploration` bestanden hat und
`another` fehlgeschlagen ist.

<Listing number="11-4" caption="Testergebnisse, wenn ein Test besteht und ein Test fehlschlägt">

```console
{{#include ../listings/ch11-writing-automated-tests/listing-11-03/output.txt}}
```

</Listing>

<!-- manual-regeneration
rg panicked listings/ch11-writing-automated-tests/listing-11-03/output.txt
check the line number of the panic matches the line number in the following paragraph
 -->

Statt `ok` zeigt die Zeile `test tests::another` jetzt `FAILED`. Zwischen den
einzelnen Ergebnissen und der Zusammenfassung erscheinen zwei neue Abschnitte:
Der erste zeigt den genauen Grund für jedes Fehlschlagen eines Tests. In diesem
Fall erfahren wir, dass `tests::another` fehlgeschlagen ist, weil er in Zeile 17
der Datei _src/lib.rs_ einen Panic mit der Meldung `Make
this test fail`
ausgelöst hat. Der nächste Abschnitt listet nur die Namen aller fehlgeschlagenen
Tests auf, was nützlich ist, wenn es viele Tests und viele detaillierte Ausgaben
fehlgeschlagener Tests gibt. Mit dem Namen eines fehlgeschlagenen Tests können
wir genau diesen Test ausführen, um ihn leichter zu debuggen; mehr über
Möglichkeiten, Tests auszuführen, erfährst du im Abschnitt
[„Steuern, wie Tests ausgeführt werden“][controlling-how-tests-are-run]<!-- ignore -->.

Am Ende steht die Zusammenfassungszeile: Insgesamt ist unser Testergebnis
`FAILED`. Ein Test hat bestanden, und ein Test ist fehlgeschlagen.

Nachdem du gesehen hast, wie die Testergebnisse in verschiedenen Szenarien
aussehen, sehen wir uns außer `panic!` einige weitere Makros an, die in Tests
nützlich sind.

<!-- Old headings. Do not remove or links may break. -->

<a id="checking-results-with-the-assert-macro"></a>

### Ergebnisse mit `assert!` prüfen {#checking-results-with-assert}

Das Makro `assert!` aus der Standardbibliothek ist nützlich, wenn du
sicherstellen willst, dass eine Bedingung in einem Test zu `true` ausgewertet
wird. Wir übergeben dem Makro `assert!` ein Argument, das zu einem Boolean
ausgewertet wird. Ist der Wert `true`, passiert nichts, und der Test besteht.
Ist der Wert `false`, ruft das Makro `assert!` `panic!` auf, damit der Test
fehlschlägt. Mit dem Makro `assert!` können wir prüfen, ob unser Code so
funktioniert, wie wir es beabsichtigen.

In Kapitel 5, Listing 5-15, haben wir ein Struct `Rectangle` und eine Methode
`can_hold` verwendet, die hier in Listing 11-5 wiederholt werden. Legen wir
diesen Code in die Datei _src/lib.rs_ und schreiben wir dann mit dem Makro
`assert!` einige Tests dafür.

<Listing number="11-5" file-name="src/lib.rs" caption="Das Struct `Rectangle` und seine Methode `can_hold` aus Kapitel 5">

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/listing-11-05/src/lib.rs}}
```

</Listing>

Die Methode `can_hold` gibt einen Boolean zurück, ist also ein perfekter
Anwendungsfall für das Makro `assert!`. In Listing 11-6 schreiben wir einen
Test, der die Methode `can_hold` prüft: Er erzeugt eine `Rectangle`-Instanz mit
einer Breite von 8 und einer Höhe von 7 und sichert zu, dass sie eine andere
`Rectangle`-Instanz mit einer Breite von 5 und einer Höhe von 1 aufnehmen kann.

<Listing number="11-6" file-name="src/lib.rs" caption="Ein Test für `can_hold`, der prüft, ob ein größeres Rechteck tatsächlich ein kleineres Rechteck aufnehmen kann">

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/listing-11-06/src/lib.rs:here}}
```

</Listing>

Beachte die Zeile `use super::*;` im Modul `tests`. Das Modul `tests` ist ein
gewöhnliches Modul, das den üblichen Sichtbarkeitsregeln folgt, die wir in
Kapitel 7 im Abschnitt
[„Pfade, um auf ein Element im Modulbaum zu verweisen“][paths-for-referring-to-an-item-in-the-module-tree]<!-- ignore -->
behandelt haben. Da das Modul `tests` ein inneres Modul ist, müssen wir den zu
testenden Code im äußeren Modul in den Gültigkeitsbereich (_scope_) des inneren
Moduls bringen. Wir verwenden hier einen Glob, sodass alles, was wir im äußeren
Modul definieren, in diesem Modul `tests` verfügbar ist.

Wir haben unseren Test `larger_can_hold_smaller` genannt und die beiden
benötigten `Rectangle`-Instanzen erzeugt. Dann haben wir das Makro `assert!`
aufgerufen und ihm das Ergebnis des Aufrufs `larger.can_hold(&smaller)`
übergeben. Dieser Ausdruck soll `true` zurückgeben, also sollte unser Test
bestehen. Finden wir es heraus!

```console
{{#include ../listings/ch11-writing-automated-tests/listing-11-06/output.txt}}
```

Er besteht! Fügen wir einen weiteren Test hinzu, der diesmal zusichert, dass ein
kleineres Rechteck kein größeres Rechteck aufnehmen kann:

<span class="filename">Dateiname: src/lib.rs</span>

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/no-listing-02-adding-another-rectangle-test/src/lib.rs:here}}
```

Da das korrekte Ergebnis der Funktion `can_hold` in diesem Fall `false` ist,
müssen wir dieses Ergebnis negieren, bevor wir es an das Makro `assert!`
übergeben. Dadurch besteht unser Test, wenn `can_hold` `false` zurückgibt:

```console
{{#include ../listings/ch11-writing-automated-tests/no-listing-02-adding-another-rectangle-test/output.txt}}
```

Zwei Tests, die bestehen! Sehen wir uns jetzt an, was mit unseren
Testergebnissen passiert, wenn wir einen Bug in unseren Code einbauen. Wir
ändern die Implementierung der Methode `can_hold`, indem wir beim Vergleich der
Breiten das Größer-als-Zeichen (`>`) durch ein Kleiner-als-Zeichen (`<`)
ersetzen:

```rust,not_desired_behavior,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/no-listing-03-introducing-a-bug/src/lib.rs:here}}
```

Das Ausführen der Tests liefert jetzt Folgendes:

```console
{{#include ../listings/ch11-writing-automated-tests/no-listing-03-introducing-a-bug/output.txt}}
```

Unsere Tests haben den Bug gefunden! Da `larger.width` gleich `8` und
`smaller.width` gleich `5` ist, gibt der Vergleich der Breiten in `can_hold`
jetzt `false` zurück: 8 ist nicht kleiner als 5.

<!-- Old headings. Do not remove or links may break. -->

<a id="testing-equality-with-the-assert_eq-and-assert_ne-macros"></a>

### Gleichheit mit `assert_eq!` und `assert_ne!` testen {#testing-equality-with-assert_eq-and-assert_ne}

Eine gängige Art, Funktionalität zu prüfen, ist, das Ergebnis des zu testenden
Codes auf Gleichheit mit dem Wert zu prüfen, den der Code zurückgeben soll. Das
könntest du mit dem Makro `assert!` tun, indem du ihm einen Ausdruck mit dem
Operator `==` übergibst. Das ist aber ein so häufiger Test, dass die
Standardbibliothek zwei Makros bereitstellt – `assert_eq!` und `assert_ne!` –,
mit denen sich dieser Test bequemer durchführen lässt. Diese Makros vergleichen
zwei Argumente auf Gleichheit bzw. Ungleichheit. Schlägt die Assertion fehl,
geben sie außerdem die beiden Werte aus, sodass man leichter sieht, _warum_ der
Test fehlgeschlagen ist; das Makro `assert!` dagegen zeigt nur an, dass es für
den `==`-Ausdruck einen `false`-Wert erhalten hat, ohne die Werte auszugeben,
die zu dem `false`-Wert geführt haben.

In Listing 11-7 schreiben wir eine Funktion namens `add_two`, die `2` zu ihrem
Parameter addiert, und testen diese Funktion dann mit dem Makro `assert_eq!`.

<Listing number="11-7" file-name="src/lib.rs" caption="Die Funktion `add_two` mit dem Makro `assert_eq!` testen">

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/listing-11-07/src/lib.rs}}
```

</Listing>

Prüfen wir, ob er besteht!

```console
{{#include ../listings/ch11-writing-automated-tests/listing-11-07/output.txt}}
```

Wir erzeugen eine Variable namens `result`, die das Ergebnis des Aufrufs
`add_two(2)` enthält. Dann übergeben wir `result` und `4` als Argumente an das
Makro `assert_eq!`. Die Ausgabezeile für diesen Test ist
`test tests::it_adds_two
... ok`, und der Text `ok` zeigt an, dass unser Test
bestanden hat!

Bauen wir einen Bug in unseren Code ein, um zu sehen, wie `assert_eq!` aussieht,
wenn es fehlschlägt. Ändere die Implementierung der Funktion `add_two` so, dass
sie stattdessen `3` addiert:

```rust,not_desired_behavior,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/no-listing-04-bug-in-add-two/src/lib.rs:here}}
```

Führe die Tests erneut aus:

```console
{{#include ../listings/ch11-writing-automated-tests/no-listing-04-bug-in-add-two/output.txt}}
```

Unser Test hat den Bug gefunden! Der Test `tests::it_adds_two` ist
fehlgeschlagen, und die Meldung sagt uns, dass die fehlgeschlagene Assertion
`left == right` war und welche Werte `left` und `right` hatten. Diese Meldung
hilft uns, mit dem Debuggen zu beginnen: Das Argument `left`, in dem wir das
Ergebnis des Aufrufs `add_two(2)` hatten, war `5`, aber das Argument `right` war
`4`. Du kannst dir vorstellen, dass das besonders hilfreich ist, wenn viele
Tests laufen.

Beachte, dass die Parameter von Funktionen für Gleichheits-Assertions in manchen
Sprachen und Test-Frameworks `expected` und `actual` heißen und die Reihenfolge,
in der wir die Argumente angeben, eine Rolle spielt. In Rust heißen sie dagegen
`left` und `right`, und die Reihenfolge, in der wir den erwarteten Wert und den
vom Code erzeugten Wert angeben, spielt keine Rolle. Wir könnten die Assertion
in diesem Test als `assert_eq!(4, result)` schreiben, was zur selben
Fehlermeldung führen würde, die ``assertion `left == right` failed`` anzeigt.

Das Makro `assert_ne!` besteht, wenn die beiden übergebenen Werte nicht gleich
sind, und schlägt fehl, wenn sie gleich sind. Dieses Makro ist am nützlichsten,
wenn wir nicht sicher sind, welchen Wert etwas haben _wird_, aber wissen,
welchen Wert es auf keinen Fall haben _sollte_. Testen wir zum Beispiel eine
Funktion, die ihre Eingabe garantiert auf irgendeine Weise verändert, wobei die
Art der Veränderung vom Wochentag abhängt, an dem wir unsere Tests ausführen,
ist es vielleicht am besten, zuzusichern, dass die Ausgabe der Funktion nicht
gleich der Eingabe ist.

Unter der Oberfläche verwenden die Makros `assert_eq!` und `assert_ne!` die
Operatoren `==` bzw. `!=`. Schlagen die Assertions fehl, geben diese Makros ihre
Argumente mit Debug-Formatierung aus. Das bedeutet, dass die verglichenen Werte
die Traits `PartialEq` und `Debug` implementieren müssen. Alle primitiven Typen
und die meisten Typen der Standardbibliothek implementieren diese Traits. Für
Structs und Enums, die du selbst definierst, musst du `PartialEq`
implementieren, um die Gleichheit dieser Typen zuzusichern. Außerdem musst du
`Debug` implementieren, um die Werte ausgeben zu können, wenn die Assertion
fehlschlägt. Da beide Traits ableitbar sind, wie in Listing 5-12 in Kapitel 5
erwähnt, genügt dafür meist, deiner Struct- oder Enum-Definition die Annotation
`#[derive(PartialEq, Debug)]` hinzuzufügen. Mehr Details zu diesen und anderen
ableitbaren Traits findest du in Anhang C,
[„Ableitbare Traits“][derivable-traits]<!-- ignore -->.

### Eigene Fehlermeldungen hinzufügen {#adding-custom-failure-messages}

Du kannst den Makros `assert!`, `assert_eq!` und `assert_ne!` als optionale
Argumente auch eine eigene Meldung mitgeben, die zusammen mit der Fehlermeldung
ausgegeben wird. Alle Argumente, die nach den erforderlichen Argumenten
angegeben werden, werden an das Makro `format!` weitergereicht (besprochen in
[„Mit `+` oder `format!` verketten“][concatenating]<!--
ignore --> in Kapitel 8), sodass du einen Format-String mit `{}`-Platzhaltern
und Werte für diese Platzhalter übergeben kannst. Eigene Meldungen sind
nützlich, um zu dokumentieren, was eine Assertion bedeutet; schlägt ein Test
fehl, hast du eine bessere Vorstellung davon, wo das Problem im Code liegt.

Angenommen, wir haben eine Funktion, die Leute mit Namen begrüßt, und wir wollen
testen, dass der Name, den wir der Funktion übergeben, in der Ausgabe erscheint:

<span class="filename">Dateiname: src/lib.rs</span>

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/no-listing-05-greeter/src/lib.rs}}
```

Die Anforderungen an dieses Programm sind noch nicht abgestimmt, und wir sind
ziemlich sicher, dass sich der Text `Hello` am Anfang der Begrüßung ändern wird.
Wir haben beschlossen, dass wir den Test nicht anpassen wollen, wenn sich die
Anforderungen ändern. Statt also auf exakte Gleichheit mit dem Wert zu prüfen,
den die Funktion `greeting` zurückgibt, sichern wir nur zu, dass die Ausgabe den
Text des Eingabeparameters enthält.

Bauen wir nun einen Bug in diesen Code ein, indem wir `greeting` so ändern, dass
`name` nicht enthalten ist, und sehen wir uns an, wie das standardmäßige
Fehlschlagen eines Tests aussieht:

```rust,not_desired_behavior,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/no-listing-06-greeter-with-bug/src/lib.rs:here}}
```

Das Ausführen dieses Tests liefert Folgendes:

```console
{{#include ../listings/ch11-writing-automated-tests/no-listing-06-greeter-with-bug/output.txt}}
```

Dieses Ergebnis zeigt nur an, dass die Assertion fehlgeschlagen ist und in
welcher Zeile die Assertion steht. Eine nützlichere Fehlermeldung würde den Wert
aus der Funktion `greeting` ausgeben. Fügen wir eine eigene Fehlermeldung hinzu,
die aus einem Format-String mit einem Platzhalter besteht, der mit dem
tatsächlichen Wert gefüllt wird, den wir von der Funktion `greeting` erhalten
haben:

```rust,ignore
{{#rustdoc_include ../listings/ch11-writing-automated-tests/no-listing-07-custom-failure-message/src/lib.rs:here}}
```

Wenn wir den Test jetzt ausführen, erhalten wir eine aussagekräftigere
Fehlermeldung:

```console
{{#include ../listings/ch11-writing-automated-tests/no-listing-07-custom-failure-message/output.txt}}
```

Wir sehen den Wert, den wir tatsächlich erhalten haben, in der Testausgabe, was
uns beim Debuggen helfen würde: Wir sehen, was passiert ist, statt dessen, was
wir erwartet hatten.

### Mit `should_panic` auf Panics prüfen {#checking-for-panics-with-should_panic}

Neben der Prüfung von Rückgabewerten ist es wichtig zu prüfen, ob unser Code
Fehlerbedingungen so behandelt, wie wir es erwarten. Denk zum Beispiel an den
Typ `Guess`, den wir in Kapitel 9, Listing 9-13, erstellt haben. Anderer Code,
der `Guess` verwendet, verlässt sich auf die Garantie, dass `Guess`-Instanzen
nur Werte zwischen 1 und 100 enthalten. Wir können einen Test schreiben, der
sicherstellt, dass der Versuch, eine `Guess`-Instanz mit einem Wert außerhalb
dieses Bereichs zu erzeugen, einen Panic auslöst.

Dazu fügen wir unserer Testfunktion das Attribut `should_panic` hinzu. Der Test
besteht, wenn der Code in der Funktion einen Panic auslöst; der Test schlägt
fehl, wenn der Code in der Funktion keinen Panic auslöst.

Listing 11-8 zeigt einen Test, der prüft, ob die Fehlerbedingungen von
`Guess::new` dann eintreten, wenn wir es erwarten.

<Listing number="11-8" file-name="src/lib.rs" caption="Testen, ob eine Bedingung einen `panic!` verursacht">

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/listing-11-08/src/lib.rs}}
```

</Listing>

Wir setzen das Attribut `#[should_panic]` hinter das Attribut `#[test]` und vor
die Testfunktion, für die es gilt. Sehen wir uns das Ergebnis an, wenn dieser
Test besteht:

```console
{{#include ../listings/ch11-writing-automated-tests/listing-11-08/output.txt}}
```

Sieht gut aus! Bauen wir nun einen Bug in unseren Code ein, indem wir die
Bedingung entfernen, dass die Funktion `new` einen Panic auslöst, wenn der Wert
größer als 100 ist:

```rust,not_desired_behavior,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/no-listing-08-guess-with-bug/src/lib.rs:here}}
```

Wenn wir den Test in Listing 11-8 ausführen, schlägt er fehl:

```console
{{#include ../listings/ch11-writing-automated-tests/no-listing-08-guess-with-bug/output.txt}}
```

In diesem Fall bekommen wir keine sehr hilfreiche Meldung, aber wenn wir uns die
Testfunktion ansehen, sehen wir, dass sie mit `#[should_panic]` annotiert ist.
Das Fehlschlagen bedeutet, dass der Code in der Testfunktion keinen Panic
verursacht hat.

Tests mit `should_panic` können ungenau sein. Ein `should_panic`-Test würde auch
dann bestehen, wenn der Test aus einem anderen Grund einen Panic auslöst als
dem, den wir erwartet haben. Um `should_panic`-Tests genauer zu machen, können
wir dem Attribut `should_panic` einen optionalen Parameter `expected`
hinzufügen. Das Test-Harness stellt dann sicher, dass die Fehlermeldung den
angegebenen Text enthält. Betrachte zum Beispiel den geänderten Code für `Guess`
in Listing 11-9, in dem die Funktion `new` mit unterschiedlichen Meldungen einen
Panic auslöst, je nachdem, ob der Wert zu klein oder zu groß ist.

<Listing number="11-9" file-name="src/lib.rs" caption="Auf einen `panic!` testen, dessen Panic-Meldung einen bestimmten Teilstring enthält">

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/listing-11-09/src/lib.rs:here}}
```

</Listing>

Dieser Test besteht, weil der Wert, den wir im Parameter `expected` des
Attributs `should_panic` angegeben haben, ein Teilstring der Meldung ist, mit
der die Funktion `Guess::new` einen Panic auslöst. Wir hätten auch die gesamte
erwartete Panic-Meldung angeben können, die in diesem Fall
`Guess value must be less than or equal to
100, got 200` wäre. Was du angibst,
hängt davon ab, wie viel der Panic-Meldung eindeutig oder dynamisch ist und wie
genau dein Test sein soll. In diesem Fall genügt ein Teilstring der
Panic-Meldung, um sicherzustellen, dass der Code in der Testfunktion den Fall
`else if value > 100` ausführt.

Um zu sehen, was passiert, wenn ein `should_panic`-Test mit einer
`expected`-Meldung fehlschlägt, bauen wir erneut einen Bug in unseren Code ein,
indem wir die Rümpfe der Blöcke `if value < 1` und `else if value > 100`
vertauschen:

```rust,ignore,not_desired_behavior
{{#rustdoc_include ../listings/ch11-writing-automated-tests/no-listing-09-guess-with-panic-msg-bug/src/lib.rs:here}}
```

Wenn wir den `should_panic`-Test diesmal ausführen, schlägt er fehl:

```console
{{#include ../listings/ch11-writing-automated-tests/no-listing-09-guess-with-panic-msg-bug/output.txt}}
```

Die Fehlermeldung zeigt, dass dieser Test tatsächlich wie erwartet einen Panic
ausgelöst hat, die Panic-Meldung aber nicht den erwarteten String
`less than or equal
to 100` enthielt. Die Panic-Meldung, die wir in diesem Fall
erhalten haben, war `Guess value must
be greater than or equal to 1, got 200`.
Jetzt können wir herausfinden, wo unser Bug steckt!

### `Result<T, E>` in Tests verwenden {#using-resultt-e-in-tests}

Alle unsere bisherigen Tests lösen einen Panic aus, wenn sie fehlschlagen. Wir
können auch Tests schreiben, die `Result<T, E>` verwenden! Hier ist der Test aus
Listing 11-1, umgeschrieben, sodass er `Result<T,
E>` verwendet und ein `Err`
zurückgibt, statt einen Panic auszulösen:

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/no-listing-10-result-in-tests/src/lib.rs:here}}
```

Die Funktion `it_works` hat jetzt den Rückgabetyp `Result<(), String>`. Im Rumpf
der Funktion rufen wir nicht das Makro `assert_eq!` auf, sondern geben `Ok(())`
zurück, wenn der Test besteht, und ein `Err` mit einem `String` darin, wenn der
Test fehlschlägt.

Wenn Tests ein `Result<T, E>` zurückgeben, kannst du im Rumpf der Tests den
Fragezeichen-Operator verwenden. Das kann eine bequeme Möglichkeit sein, Tests
zu schreiben, die fehlschlagen sollen, wenn eine Operation in ihnen eine
`Err`-Variante zurückgibt.

Bei Tests, die `Result<T,
E>` verwenden, kannst du die Annotation
`#[should_panic]` nicht verwenden. Um zuzusichern, dass eine Operation eine
`Err`-Variante zurückgibt, verwende den Fragezeichen-Operator _nicht_ auf dem
`Result<T, E>`-Wert. Verwende stattdessen `assert!(value.is_err())`.

Nachdem du mehrere Möglichkeiten kennst, Tests zu schreiben, sehen wir uns an,
was passiert, wenn wir unsere Tests ausführen, und erkunden die verschiedenen
Optionen, die wir mit `cargo
test` verwenden können.

{{#quiz ../quizzes/ch11-01-writing-tests.toml}}

[concatenating]: ch08-02-strings.html#concatenating-with--or-format
[bench]: https://doc.rust-lang.org/unstable-book/library-features/test.html
[ignoring]: ch11-02-running-tests.html#ignoring-tests-unless-specifically-requested
[subset]: ch11-02-running-tests.html#running-a-subset-of-tests-by-name
[controlling-how-tests-are-run]: ch11-02-running-tests.html#controlling-how-tests-are-run
[derivable-traits]: appendix-03-derivable-traits.html
[doc-comments]: ch14-02-publishing-to-crates-io.html#documentation-comments-as-tests
[paths-for-referring-to-an-item-in-the-module-tree]: ch07-03-paths-for-referring-to-an-item-in-the-module-tree.html
