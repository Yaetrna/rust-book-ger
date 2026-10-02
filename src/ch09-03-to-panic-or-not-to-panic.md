## `panic!` oder nicht `panic!`? {#to-panic-or-not-to-panic}

Wie entscheidest du also, wann du `panic!` aufrufen und wann du `Result`
zurückgeben solltest? Wenn Code einen Panic auslöst, gibt es keine Möglichkeit,
sich davon zu erholen. Du könntest bei jeder Fehlersituation `panic!` aufrufen,
ob es einen möglichen Weg zur Behebung gibt oder nicht, aber dann triffst du
stellvertretend für den aufrufenden Code die Entscheidung, dass eine Situation
nicht behebbar ist. Wenn du dich dafür entscheidest, einen `Result`-Wert
zurückzugeben, lässt du dem aufrufenden Code die Wahl. Der aufrufende Code
könnte versuchen, den Fehler auf eine Weise zu beheben, die für seine Situation
passt, oder er könnte entscheiden, dass ein `Err`-Wert in diesem Fall nicht
behebbar ist, und `panic!` aufrufen, wodurch dein behebbarer Fehler zu einem
nicht behebbaren wird. Daher ist die Rückgabe von `Result` eine gute
Standardwahl, wenn du eine Funktion definierst, die fehlschlagen kann.

In Situationen wie Beispielen, Prototyp-Code und Tests ist es angemessener, Code
zu schreiben, der einen Panic auslöst, statt ein `Result` zurückzugeben. Sehen
wir uns an, warum, und besprechen wir dann Situationen, in denen der Compiler
nicht erkennen kann, dass ein Fehlschlag unmöglich ist, du als Mensch aber
schon. Das Kapitel schließt mit einigen allgemeinen Richtlinien dazu, wie man in
Bibliothekscode entscheidet, ob ein Panic ausgelöst werden soll.

### Beispiele, Prototyp-Code und Tests {#examples-prototype-code-and-tests}

Wenn du ein Beispiel schreibst, um ein Konzept zu veranschaulichen, kann
robuster Code zur Fehlerbehandlung das Beispiel unübersichtlicher machen. In
Beispielen versteht es sich von selbst, dass ein Aufruf einer Methode wie
`unwrap`, die einen Panic auslösen kann, als Platzhalter für die Art gedacht
ist, wie deine Anwendung Fehler behandeln soll. Diese kann je nachdem, was der
Rest deines Codes tut, unterschiedlich ausfallen.

Ebenso sind die Methoden `unwrap` und `expect` sehr praktisch, wenn du einen
Prototyp baust und noch nicht entscheiden willst, wie Fehler behandelt werden
sollen. Sie hinterlassen deutliche Markierungen in deinem Code für den
Zeitpunkt, an dem du dein Programm robuster machen willst.

Schlägt in einem Test ein Methodenaufruf fehl, soll der ganze Test fehlschlagen,
auch wenn diese Methode nicht die getestete Funktionalität ist. Da ein Test
durch `panic!` als fehlgeschlagen markiert wird, ist der Aufruf von `unwrap`
oder `expect` genau das, was passieren sollte.

<!-- Old headings. Do not remove or links may break. -->

<a id="cases-in-which-you-have-more-information-than-the-compiler"></a>

### Wenn du mehr Informationen hast als der Compiler {#when-you-have-more-information-than-the-compiler}

Es wäre auch angemessen, `expect` aufzurufen, wenn du andere Logik hast, die
sicherstellt, dass das `Result` einen `Ok`-Wert hat, der Compiler diese Logik
aber nicht versteht. Du hast trotzdem einen `Result`-Wert, den du behandeln
musst: Die Operation, die du aufrufst, kann im Allgemeinen immer noch
fehlschlagen, auch wenn das in deiner konkreten Situation logisch unmöglich ist.
Wenn du durch manuelles Prüfen des Codes sicherstellen kannst, dass du nie eine
`Err`-Variante haben wirst, ist es völlig in Ordnung, `expect` aufzurufen und im
Argumenttext zu dokumentieren, warum du glaubst, dass du nie eine `Err`-Variante
haben wirst. Hier ist ein Beispiel:

```rust
{{#rustdoc_include ../listings/ch09-error-handling/no-listing-08-unwrap-that-cant-fail/src/main.rs:here}}
```

Wir erzeugen eine `IpAddr`-Instanz, indem wir einen fest codierten String
parsen. Wir sehen, dass `127.0.0.1` eine gültige IP-Adresse ist, also ist es
hier in Ordnung, `expect` zu verwenden. Ein fest codierter, gültiger String
ändert aber nichts am Rückgabetyp der Methode `parse`: Wir erhalten trotzdem
einen `Result`-Wert, und der Compiler zwingt uns weiterhin, das `Result` so zu
behandeln, als wäre die Variante `Err` möglich, weil der Compiler nicht schlau
genug ist, um zu erkennen, dass dieser String immer eine gültige IP-Adresse ist.
Käme der String mit der IP-Adresse von einem Benutzer, statt fest im Programm
codiert zu sein, und _könnte_ daher fehlschlagen, würden wir das `Result` auf
jeden Fall robuster behandeln wollen. Die Annahme zu erwähnen, dass diese
IP-Adresse fest codiert ist, erinnert uns daran, `expect` durch besseren Code
zur Fehlerbehandlung zu ersetzen, falls wir die IP-Adresse künftig aus einer
anderen Quelle beziehen müssen.

### Richtlinien zur Fehlerbehandlung {#guidelines-for-error-handling}

Es ist ratsam, deinen Code einen Panic auslösen zu lassen, wenn er in einen
schlechten Zustand geraten könnte. In diesem Zusammenhang liegt ein _schlechter
Zustand_ vor, wenn eine Annahme, eine Garantie, ein Vertrag oder eine Invariante
verletzt wurde, etwa wenn deinem Code ungültige, widersprüchliche oder fehlende
Werte übergeben werden – und zusätzlich einer oder mehrere der folgenden Punkte
zutreffen:

- Der schlechte Zustand ist etwas Unerwartetes, im Gegensatz zu etwas, das
  wahrscheinlich gelegentlich vorkommt, etwa dass jemand Daten im falschen
  Format eingibt.
- Dein Code muss sich ab diesem Punkt darauf verlassen können, dass er sich
  nicht in diesem schlechten Zustand befindet, statt bei jedem Schritt auf das
  Problem zu prüfen.
- Es gibt keine gute Möglichkeit, diese Information in den Typen zu kodieren,
  die du verwendest. Was wir damit meinen, sehen wir uns an einem Beispiel in
  [„Zustände und Verhalten als Typen kodieren“][encoding]<!-- ignore --> in
  Kapitel 18 an.

Wenn jemand deinen Code aufruft und Werte übergibt, die keinen Sinn ergeben, ist
es am besten, nach Möglichkeit einen Fehler zurückzugeben, damit die Person, die
die Bibliothek verwendet, entscheiden kann, was sie in diesem Fall tun will. In
Fällen, in denen ein Weitermachen unsicher oder schädlich sein könnte, ist es
aber vielleicht die beste Wahl, `panic!` aufzurufen und die Person, die deine
Bibliothek verwendet, auf den Bug in ihrem Code aufmerksam zu machen, damit sie
ihn während der Entwicklung beheben kann. Ebenso ist `panic!` oft angemessen,
wenn du externen Code aufrufst, auf den du keinen Einfluss hast, und dieser
einen ungültigen Zustand zurückgibt, den du nicht beheben kannst.

Wenn ein Fehlschlag jedoch zu erwarten ist, ist es angemessener, ein `Result`
zurückzugeben, als `panic!` aufzurufen. Beispiele sind ein Parser, der
fehlerhafte Daten erhält, oder eine HTTP-Anfrage, die einen Status zurückgibt,
der anzeigt, dass du ein Ratenlimit erreicht hast. In diesen Fällen zeigt die
Rückgabe eines `Result` an, dass ein Fehlschlag eine erwartete Möglichkeit ist,
bei der der aufrufende Code entscheiden muss, wie er sie behandelt.

Wenn dein Code eine Operation ausführt, die Benutzer gefährden könnte, wenn sie
mit ungültigen Werten aufgerufen wird, sollte dein Code zuerst prüfen, ob die
Werte gültig sind, und einen Panic auslösen, wenn sie es nicht sind. Das hat vor
allem Sicherheitsgründe: Der Versuch, mit ungültigen Daten zu arbeiten, kann
deinen Code für Sicherheitslücken anfällig machen. Das ist der Hauptgrund, warum
die Standardbibliothek `panic!` aufruft, wenn du einen Speicherzugriff außerhalb
der Grenzen versuchst: Der Versuch, auf Speicher zuzugreifen, der nicht zur
aktuellen Datenstruktur gehört, ist ein häufiges Sicherheitsproblem. Funktionen
haben oft _Verträge_: Ihr Verhalten ist nur garantiert, wenn die Eingaben
bestimmte Anforderungen erfüllen. Bei einer Vertragsverletzung einen Panic
auszulösen ist sinnvoll, weil eine Vertragsverletzung immer auf einen Bug auf
Seiten des Aufrufers hinweist und keine Art von Fehler ist, die der aufrufende
Code explizit behandeln müssen soll. Tatsächlich gibt es für den aufrufenden
Code keine vernünftige Möglichkeit, sich davon zu erholen; die aufrufenden
_Programmierenden_ müssen den Code korrigieren. Die Verträge einer Funktion
sollten in ihrer API-Dokumentation erklärt werden, besonders wenn eine
Verletzung einen Panic auslöst.

Viele Fehlerprüfungen in all deinen Funktionen wären allerdings umständlich und
lästig. Zum Glück kannst du das Typsystem von Rust (und damit die Typprüfung
durch den Compiler) viele der Prüfungen für dich erledigen lassen. Hat deine
Funktion einen bestimmten Typ als Parameter, kannst du mit der Logik deines
Codes fortfahren und dich darauf verlassen, dass der Compiler bereits
sichergestellt hat, dass du einen gültigen Wert hast. Wenn du zum Beispiel einen
Typ statt einer `Option` hast, erwartet dein Programm, _etwas_ statt _nichts_ zu
haben. Dein Code muss dann nicht zwei Fälle für die Varianten `Some` und `None`
behandeln: Er hat nur einen Fall, in dem definitiv ein Wert vorhanden ist. Code,
der versucht, deiner Funktion nichts zu übergeben, kompiliert gar nicht erst,
also muss deine Funktion diesen Fall zur Laufzeit nicht prüfen. Ein weiteres
Beispiel ist ein vorzeichenloser Ganzzahltyp wie `u32`, der sicherstellt, dass
der Parameter nie negativ ist.

<!-- Old headings. Do not remove or links may break. -->

<a id="creating-custom-types-for-validation"></a>

### Eigene Typen zur Validierung {#custom-types-for-validation}

Führen wir die Idee, mit dem Typsystem von Rust sicherzustellen, dass wir einen
gültigen Wert haben, einen Schritt weiter und sehen uns an, wie man einen
eigenen Typ zur Validierung erstellt. Erinnere dich an das Ratespiel in Kapitel
2, in dem unser Code den Benutzer aufgefordert hat, eine Zahl zwischen 1 und 100
zu raten. Wir haben nie geprüft, ob der Tipp des Benutzers zwischen diesen
Zahlen liegt, bevor wir ihn mit unserer Geheimzahl verglichen haben; wir haben
nur geprüft, ob der Tipp positiv war. In diesem Fall waren die Folgen nicht sehr
schlimm: Unsere Ausgabe „Too high“ oder „Too low“ wäre trotzdem korrekt gewesen.
Es wäre aber eine nützliche Verbesserung, den Benutzer zu gültigen Tipps
hinzuführen und sich anders zu verhalten, wenn er eine Zahl außerhalb des
Bereichs rät, als wenn er zum Beispiel stattdessen Buchstaben eintippt.

Eine Möglichkeit dafür wäre, den Tipp als `i32` statt nur als `u32` zu parsen,
um potenziell negative Zahlen zuzulassen, und dann eine Prüfung hinzuzufügen, ob
die Zahl im Bereich liegt, etwa so:

<Listing file-name="src/main.rs">

```rust,ignore
{{#rustdoc_include ../listings/ch09-error-handling/no-listing-09-guess-out-of-range/src/main.rs:here}}
```

</Listing>

Der `if`-Ausdruck prüft, ob unser Wert außerhalb des Bereichs liegt, teilt dem
Benutzer das Problem mit und ruft `continue` auf, um die nächste Iteration der
Schleife zu beginnen und nach einem weiteren Tipp zu fragen. Nach dem
`if`-Ausdruck können wir mit den Vergleichen zwischen `guess` und der Geheimzahl
fortfahren und wissen dabei, dass `guess` zwischen 1 und 100 liegt.

Das ist aber keine ideale Lösung: Wäre es absolut entscheidend, dass das
Programm nur mit Werten zwischen 1 und 100 arbeitet, und hätte es viele
Funktionen mit dieser Anforderung, wäre eine solche Prüfung in jeder Funktion
mühsam (und könnte die Performance beeinträchtigen).

Stattdessen können wir in einem eigenen Modul einen neuen Typ erstellen und die
Validierungen in eine Funktion legen, die eine Instanz des Typs erzeugt, statt
die Validierungen überall zu wiederholen. So können Funktionen den neuen Typ
gefahrlos in ihren Signaturen verwenden und sich auf die Werte verlassen, die
sie erhalten. Listing 9-13 zeigt eine Möglichkeit, einen Typ `Guess` zu
definieren, der nur dann eine Instanz von `Guess` erzeugt, wenn die Funktion
`new` einen Wert zwischen 1 und 100 erhält.

<Listing number="9-13" caption="Ein Typ `Guess`, der nur mit Werten zwischen 1 und 100 weitermacht" file-name="src/guessing_game.rs">

```rust
{{#rustdoc_include ../listings/ch09-error-handling/listing-09-13/src/guessing_game.rs}}
```

</Listing>

Beachte, dass dieser Code in _src/guessing_game.rs_ voraussetzt, dass in
_src/lib.rs_ eine Moduldeklaration `mod guessing_game;` hinzugefügt wird, die
wir hier nicht gezeigt haben. In der Datei dieses neuen Moduls definieren wir
ein Struct namens `Guess` mit einem Feld namens `value`, das einen `i32`
enthält. Dort wird die Zahl gespeichert.

Dann implementieren wir auf `Guess` eine assoziierte Funktion namens `new`, die
Instanzen von `Guess`-Werten erzeugt. Die Funktion `new` ist so definiert, dass
sie einen Parameter namens `value` vom Typ `i32` hat und ein `Guess` zurückgibt.
Der Code im Rumpf der Funktion `new` prüft `value`, um sicherzustellen, dass der
Wert zwischen 1 und 100 liegt. Besteht `value` diese Prüfung nicht, rufen wir
`panic!` auf. Das macht die Person, die den aufrufenden Code schreibt, darauf
aufmerksam, dass sie einen Bug hat, den sie beheben muss, denn ein `Guess` mit
einem `value` außerhalb dieses Bereichs zu erzeugen, würde den Vertrag
verletzen, auf den sich `Guess::new` verlässt. Die Bedingungen, unter denen
`Guess::new` einen Panic auslösen kann, sollten in der öffentlichen
API-Dokumentation besprochen werden; Dokumentationskonventionen, die in der von
dir erstellten API-Dokumentation auf die Möglichkeit eines `panic!` hinweisen,
behandeln wir in Kapitel 14. Besteht `value` die Prüfung, erzeugen wir ein neues
`Guess`, dessen Feld `value` auf den Parameter `value` gesetzt ist, und geben
das `Guess` zurück.

Als Nächstes implementieren wir eine Methode namens `value`, die `self` ausleiht
(_borrows_), keine weiteren Parameter hat und einen `i32` zurückgibt. Eine
solche Methode wird manchmal _Getter_ genannt, weil ihr Zweck ist, Daten aus
ihren Feldern zu holen und zurückzugeben. Diese öffentliche Methode ist nötig,
weil das Feld `value` des Structs `Guess` privat ist. Es ist wichtig, dass das
Feld `value` privat ist, damit Code, der das Struct `Guess` verwendet, `value`
nicht direkt setzen darf: Code außerhalb des Moduls `guessing_game` _muss_ die
Funktion `Guess::new` verwenden, um eine Instanz von `Guess` zu erzeugen.
Dadurch ist sichergestellt, dass ein `Guess` keinen `value` haben kann, der
nicht von den Bedingungen in der Funktion `Guess::new` geprüft wurde.

Eine Funktion, die einen Parameter hat oder nur Zahlen zwischen 1 und 100
zurückgibt, könnte dann in ihrer Signatur angeben, dass sie ein `Guess` statt
eines `i32` nimmt oder zurückgibt, und müsste in ihrem Rumpf keine zusätzlichen
Prüfungen vornehmen.

{{#quiz ../quizzes/ch09-03-panic-or-not.toml}}

## Zusammenfassung {#summary}

Die Features von Rust zur Fehlerbehandlung sollen dir helfen, robusteren Code zu
schreiben. Das Makro `panic!` signalisiert, dass sich dein Programm in einem
Zustand befindet, den es nicht behandeln kann, und lässt dich den Prozess
anhalten, statt mit ungültigen oder falschen Werten weiterzumachen. Das Enum
`Result` nutzt das Typsystem von Rust, um anzuzeigen, dass Operationen auf eine
Weise fehlschlagen können, von der sich dein Code erholen könnte. Mit `Result`
kannst du Code, der deinen Code aufruft, außerdem mitteilen, dass er möglichen
Erfolg oder Fehlschlag behandeln muss. Wenn du `panic!` und `Result` in den
passenden Situationen verwendest, wird dein Code angesichts unvermeidlicher
Probleme zuverlässiger.

Nachdem du nützliche Arten gesehen hast, wie die Standardbibliothek Generics mit
den Enums `Option` und `Result` verwendet, sprechen wir darüber, wie Generics
funktionieren und wie du sie in deinem Code verwenden kannst.

[encoding]: ch18-03-oo-design-patterns.html#encoding-states-and-behavior-as-types
