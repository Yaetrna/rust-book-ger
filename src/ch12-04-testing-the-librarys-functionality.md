<!-- Old headings. Do not remove or links may break. -->

<a id="developing-the-librarys-functionality-with-test-driven-development"></a>

## Funktionalität mit testgetriebener Entwicklung hinzufügen {#adding-functionality-with-test-driven-development}

Da die Suchlogik jetzt getrennt von der Funktion `main` in _src/lib.rs_ steht,
ist es viel einfacher, Tests für die Kernfunktionalität unseres Codes zu
schreiben. Wir können Funktionen direkt mit verschiedenen Argumenten aufrufen
und Rückgabewerte prüfen, ohne unsere Binärdatei von der Kommandozeile aus
aufrufen zu müssen.

In diesem Abschnitt fügen wir dem Programm `minigrep` die Suchlogik mithilfe der
testgetriebenen Entwicklung (_test-driven development_, TDD) mit folgenden
Schritten hinzu:

1. Schreib einen Test, der fehlschlägt, und führe ihn aus, um sicherzugehen,
   dass er aus dem erwarteten Grund fehlschlägt.
2. Schreib oder ändere gerade so viel Code, dass der neue Test besteht.
3. Refaktorisiere den Code, den du gerade hinzugefügt oder geändert hast, und
   stell sicher, dass die Tests weiterhin bestehen.
4. Wiederhole ab Schritt 1!

Auch wenn TDD nur eine von vielen Arten ist, Software zu schreiben, kann sie den
Entwurf des Codes vorantreiben. Den Test zu schreiben, bevor du den Code
schreibst, der den Test bestehen lässt, hilft, während des gesamten Vorgangs
eine hohe Testabdeckung beizubehalten.

Wir entwickeln die Implementierung der Funktionalität testgetrieben, die
tatsächlich im Dateiinhalt nach dem Suchstring sucht und eine Liste der Zeilen
erzeugt, die zur Suchanfrage passen. Diese Funktionalität fügen wir in einer
Funktion namens `search` hinzu.

### Einen fehlschlagenden Test schreiben {#writing-a-failing-test}

In _src/lib.rs_ fügen wir wie in [Kapitel 11][ch11-anatomy]<!-- ignore --> ein
Modul `tests` mit einer Testfunktion hinzu. Die Testfunktion legt das Verhalten
fest, das die Funktion `search` haben soll: Sie nimmt eine Suchanfrage und den
zu durchsuchenden Text und gibt nur die Zeilen des Textes zurück, die die
Suchanfrage enthalten. Listing 12-15 zeigt diesen Test.

<Listing number="12-15" file-name="src/lib.rs" caption="Einen fehlschlagenden Test für die Funktion `search` mit der Funktionalität erstellen, die wir gern hätten">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-15/src/lib.rs:here}}
```

</Listing>

Dieser Test sucht nach dem String `"duct"`. Der Text, den wir durchsuchen, hat
drei Zeilen, von denen nur eine `"duct"` enthält (beachte, dass der Backslash
nach dem öffnenden doppelten Anführungszeichen Rust anweist, am Anfang des
Inhalts dieses String-Literals kein Zeilenumbruchzeichen einzufügen). Wir
sichern zu, dass der von der Funktion `search` zurückgegebene Wert nur die Zeile
enthält, die wir erwarten.

Wenn wir diesen Test ausführen, schlägt er derzeit fehl, weil das Makro
`unimplemented!` mit der Meldung „not implemented“ einen Panic auslöst. Gemäß
den Prinzipien von TDD machen wir einen kleinen Schritt und fügen gerade so viel
Code hinzu, dass der Test beim Aufruf der Funktion keinen Panic mehr auslöst:
Wir definieren die Funktion `search` so, dass sie immer einen leeren Vektor
zurückgibt, wie in Listing 12-16 gezeigt. Dann sollte der Test kompilieren und
fehlschlagen, weil ein leerer Vektor nicht mit einem Vektor übereinstimmt, der
die Zeile `"safe,
fast, productive."` enthält.

<Listing number="12-16" file-name="src/lib.rs" caption="Gerade so viel von der Funktion `search` definieren, dass ihr Aufruf keinen Panic auslöst">

```rust,noplayground
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-16/src/lib.rs:here}}
```

</Listing>

Besprechen wir nun, warum wir in der Signatur von `search` eine explizite
Lifetime `'a` definieren und diese Lifetime beim Argument `contents` und beim
Rückgabewert verwenden müssen. Erinnere dich aus
[Kapitel 10][ch10-lifetimes]<!-- ignore -->, dass die Lifetime-Parameter
angeben, welche Lifetime eines Arguments mit der Lifetime des Rückgabewerts
verbunden ist. In diesem Fall geben wir an, dass der zurückgegebene Vektor
String-Slices enthalten soll, die auf Slices des Arguments `contents` verweisen
(und nicht auf das Argument `query`).

Mit anderen Worten: Wir teilen Rust mit, dass die von der Funktion `search`
zurückgegebenen Daten so lange leben wie die Daten, die der Funktion `search` im
Argument `contents` übergeben werden. Das ist wichtig! Die Daten, auf die ein
Slice _verweist_, müssen gültig sein, damit die Referenz gültig ist; nimmt der
Compiler an, dass wir String-Slices von `query` statt von `contents` bilden,
führt er seine Sicherheitsprüfungen falsch durch.

Wenn wir die Lifetime-Annotationen vergessen und versuchen, diese Funktion zu
kompilieren, erhalten wir diesen Fehler:

```console
{{#include ../listings/ch12-an-io-project/output-only-02-missing-lifetimes/output.txt}}
```

Rust kann nicht wissen, welchen der beiden Parameter wir für die Ausgabe
brauchen, also müssen wir es ihm explizit mitteilen. Beachte, dass der Hilfetext
vorschlägt, für alle Parameter und den Ausgabetyp denselben Lifetime-Parameter
anzugeben, was falsch ist! Da `contents` der Parameter ist, der unseren gesamten
Text enthält, und wir die passenden Teile dieses Textes zurückgeben wollen,
wissen wir, dass `contents` der einzige Parameter ist, der über die
Lifetime-Syntax mit dem Rückgabewert verbunden werden sollte.

Andere Programmiersprachen verlangen nicht, dass du Argumente in der Signatur
mit Rückgabewerten verbindest, aber mit der Zeit fällt dir diese Praxis
leichter. Vergleiche dieses Beispiel ruhig mit den Beispielen im Abschnitt
[„Referenzen mit Lifetimes validieren“][validating-references-with-lifetimes]<!-- ignore -->
in Kapitel 10.

### Code schreiben, der den Test bestehen lässt {#writing-code-to-pass-the-test}

Derzeit schlägt unser Test fehl, weil wir immer einen leeren Vektor zurückgeben.
Um das zu beheben und `search` zu implementieren, muss unser Programm diese
Schritte ausführen:

1. Über jede Zeile des Inhalts iterieren.
2. Prüfen, ob die Zeile unseren Suchstring enthält.
3. Wenn ja, sie zur Liste der Werte hinzufügen, die wir zurückgeben.
4. Wenn nicht, nichts tun.
5. Die Liste der passenden Ergebnisse zurückgeben.

Gehen wir jeden Schritt durch und beginnen mit dem Iterieren über die Zeilen.

#### Mit der Methode `lines` über Zeilen iterieren {#iterating-through-lines-with-the-lines-method}

Rust hat eine hilfreiche Methode, um zeilenweise über Strings zu iterieren, die
praktischerweise `lines` heißt und wie in Listing 12-17 gezeigt funktioniert.
Beachte, dass das noch nicht kompiliert.

<Listing number="12-17" file-name="src/lib.rs" caption="Über jede Zeile in `contents` iterieren">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-17/src/lib.rs:here}}
```

</Listing>

Die Methode `lines` gibt einen Iterator zurück. Über Iteratoren sprechen wir
ausführlich in [Kapitel 13][ch13-iterators]<!-- ignore -->. Erinnere dich aber,
dass du diese Art, einen Iterator zu verwenden, in
[Listing 3-5][ch3-iter]<!-- ignore --> gesehen hast, wo wir eine `for`-Schleife
mit einem Iterator verwendet haben, um für jedes Element einer Collection Code
auszuführen.

#### Jede Zeile nach der Suchanfrage durchsuchen {#searching-each-line-for-the-query}

Als Nächstes prüfen wir, ob die aktuelle Zeile unseren Suchstring enthält. Zum
Glück haben Strings eine hilfreiche Methode namens `contains`, die das für uns
erledigt! Füge in der Funktion `search` einen Aufruf der Methode `contains`
hinzu, wie in Listing 12-18 gezeigt. Beachte, dass auch das noch nicht
kompiliert.

<Listing number="12-18" file-name="src/lib.rs" caption="Funktionalität hinzufügen, die prüft, ob die Zeile den String in `query` enthält">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-18/src/lib.rs:here}}
```

</Listing>

Im Moment bauen wir die Funktionalität schrittweise auf. Damit der Code
kompiliert, müssen wir aus dem Rumpf einen Wert zurückgeben, wie wir es in der
Funktionssignatur angekündigt haben.

#### Passende Zeilen speichern {#storing-matching-lines}

Um diese Funktion fertigzustellen, brauchen wir eine Möglichkeit, die passenden
Zeilen zu speichern, die wir zurückgeben wollen. Dazu können wir vor der
`for`-Schleife einen veränderlichen (_mutable_) Vektor anlegen und die Methode
`push` aufrufen, um eine `line` im Vektor zu speichern. Nach der `for`-Schleife
geben wir den Vektor zurück, wie in Listing 12-19 gezeigt.

<Listing number="12-19" file-name="src/lib.rs" caption="Die passenden Zeilen speichern, damit wir sie zurückgeben können">

```rust,ignore
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-19/src/lib.rs:here}}
```

</Listing>

Jetzt sollte die Funktion `search` nur die Zeilen zurückgeben, die `query`
enthalten, und unser Test sollte bestehen. Führen wir den Test aus:

```console
{{#include ../listings/ch12-an-io-project/listing-12-19/output.txt}}
```

Unser Test besteht, also wissen wir, dass es funktioniert!

An dieser Stelle könnten wir Möglichkeiten erwägen, die Implementierung der
Suchfunktion zu refaktorisieren, während die Tests weiterhin bestehen, damit die
Funktionalität gleich bleibt. Der Code in der Suchfunktion ist nicht allzu
schlecht, nutzt aber einige nützliche Features von Iteratoren nicht. Wir kehren
in [Kapitel 13][ch13-iterators]<!-- ignore --> zu diesem Beispiel zurück, wo wir
Iteratoren ausführlich erkunden, und sehen uns an, wie man es verbessern kann.

Jetzt sollte das gesamte Programm funktionieren! Probieren wir es aus, zuerst
mit einem Wort, das genau eine Zeile aus dem Gedicht von Emily Dickinson
zurückgeben sollte: _frog_.

```console
{{#include ../listings/ch12-an-io-project/no-listing-02-using-search-in-run/output.txt}}
```

Klasse! Probieren wir jetzt ein Wort, das zu mehreren Zeilen passt, etwa _body_:

```console
{{#include ../listings/ch12-an-io-project/output-only-03-multiple-matches/output.txt}}
```

Und schließlich stellen wir sicher, dass wir keine Zeilen erhalten, wenn wir
nach einem Wort suchen, das nirgends im Gedicht vorkommt, etwa
_monomorphization_:

```console
{{#include ../listings/ch12-an-io-project/output-only-04-no-matches/output.txt}}
```

Hervorragend! Wir haben unsere eigene Miniversion eines klassischen Werkzeugs
gebaut und viel darüber gelernt, wie man Anwendungen strukturiert. Außerdem
haben wir einiges über Dateiein- und -ausgabe, Lifetimes, Tests und das Parsen
der Kommandozeile gelernt.

Um dieses Projekt abzurunden, zeigen wir kurz, wie man mit Umgebungsvariablen
arbeitet und wie man auf die Standardfehlerausgabe schreibt. Beides ist
nützlich, wenn du Kommandozeilenprogramme schreibst.

[validating-references-with-lifetimes]: ch10-03-lifetime-syntax.html#validating-references-with-lifetimes
[ch11-anatomy]: ch11-01-writing-tests.html#the-anatomy-of-a-test-function
[ch10-lifetimes]: ch10-03-lifetime-syntax.html
[ch3-iter]: ch03-05-control-flow.html#looping-through-a-collection-with-for
[ch13-iterators]: ch13-02-iterators.html
