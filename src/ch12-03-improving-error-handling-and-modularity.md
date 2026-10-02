## Refactoring für bessere Modularität und Fehlerbehandlung {#refactoring-to-improve-modularity-and-error-handling}

Um unser Programm zu verbessern, beheben wir vier Probleme, die mit der Struktur
des Programms und seinem Umgang mit möglichen Fehlern zu tun haben. Erstens
erledigt unsere Funktion `main` jetzt zwei Aufgaben: Sie parst Argumente und
liest Dateien. Wenn unser Programm wächst, nimmt die Zahl der einzelnen Aufgaben
zu, die die Funktion `main` erledigt. Je mehr Verantwortlichkeiten eine Funktion
bekommt, desto schwieriger lässt sich über sie nachdenken, desto schwerer lässt
sie sich testen und desto schwerer lässt sie sich ändern, ohne einen ihrer Teile
kaputtzumachen. Am besten trennt man Funktionalität so, dass jede Funktion für
eine Aufgabe verantwortlich ist.

Dieses Problem hängt auch mit dem zweiten Problem zusammen: `query` und
`file_path` sind zwar Konfigurationsvariablen unseres Programms, Variablen wie
`contents` werden aber verwendet, um die Logik des Programms auszuführen. Je
länger `main` wird, desto mehr Variablen müssen wir in den Gültigkeitsbereich
(_scope_) bringen; und je mehr Variablen wir im Gültigkeitsbereich haben, desto
schwerer lässt sich der Zweck jeder einzelnen im Blick behalten. Am besten fasst
man die Konfigurationsvariablen in einer Struktur zusammen, um ihren Zweck
deutlich zu machen.

Das dritte Problem ist, dass wir `expect` verwendet haben, um eine Fehlermeldung
auszugeben, wenn das Lesen der Datei fehlschlägt, die Fehlermeldung aber nur
`Should have been
able to read the file` ausgibt. Das Lesen einer Datei kann auf
verschiedene Weise fehlschlagen: Die Datei könnte zum Beispiel fehlen, oder wir
haben keine Berechtigung, sie zu öffnen. Im Moment würden wir unabhängig von der
Situation immer dieselbe Fehlermeldung ausgeben, was dem Benutzer keinerlei
Information geben würde!

Viertens verwenden wir `expect`, um einen Fehler zu behandeln, und wenn der
Benutzer unser Programm ohne genügend Argumente ausführt, bekommt er von Rust
einen Fehler `index out of bounds`, der das Problem nicht klar erklärt. Am
besten wäre es, wenn sich der gesamte Code zur Fehlerbehandlung an einer Stelle
befände, damit künftige Maintainer nur eine Stelle im Code ansehen müssen, falls
sich die Logik der Fehlerbehandlung ändern muss. Den gesamten Code zur
Fehlerbehandlung an einer Stelle zu haben, stellt außerdem sicher, dass wir
Meldungen ausgeben, die für unsere Endbenutzer sinnvoll sind.

Gehen wir diese vier Probleme an, indem wir unser Projekt refaktorisieren.

<!-- Old headings. Do not remove or links may break. -->

<a id="separation-of-concerns-for-binary-projects"></a>

### Belange in Binary-Projekten trennen {#separating-concerns-in-binary-projects}

Das organisatorische Problem, der Funktion `main` die Verantwortung für mehrere
Aufgaben zu übertragen, kommt in vielen Binary-Projekten vor. Daher finden es
viele Rust-Programmierende nützlich, die einzelnen Belange (_concerns_) eines
Binärprogramms aufzuteilen, wenn die Funktion `main` groß zu werden beginnt.
Dieser Vorgang hat folgende Schritte:

- Teile dein Programm in eine Datei _main.rs_ und eine Datei _lib.rs_ auf und
  verschiebe die Logik deines Programms nach _lib.rs_.
- Solange die Logik zum Parsen der Kommandozeile klein ist, kann sie in der
  Funktion `main` bleiben.
- Wenn die Logik zum Parsen der Kommandozeile kompliziert zu werden beginnt,
  lagere sie aus der Funktion `main` in andere Funktionen oder Typen aus.

Die Verantwortlichkeiten, die nach diesem Vorgang in der Funktion `main`
verbleiben, sollten sich auf Folgendes beschränken:

- Die Logik zum Parsen der Kommandozeile mit den Argumentwerten aufrufen
- Alle sonstige Konfiguration vornehmen
- Eine Funktion `run` in _lib.rs_ aufrufen
- Den Fehler behandeln, falls `run` einen Fehler zurückgibt

Bei diesem Schema geht es um die Trennung von Belangen: _main.rs_ kümmert sich
um das Ausführen des Programms und _lib.rs_ um die gesamte Logik der
eigentlichen Aufgabe. Da du die Funktion `main` nicht direkt testen kannst,
lässt dich diese Struktur die gesamte Logik deines Programms testen, indem du
sie aus der Funktion `main` herauslöst. Der Code, der in der Funktion `main`
verbleibt, ist klein genug, um seine Korrektheit durch Lesen zu überprüfen.
Bauen wir unser Programm nach diesem Vorgehen um.

#### Den Argument-Parser extrahieren {#extracting-the-argument-parser}

Wir lagern die Funktionalität zum Parsen der Argumente in eine Funktion aus, die
`main` aufruft. Listing 12-5 zeigt den neuen Anfang der Funktion `main`, die
eine neue Funktion `parse_config` aufruft, die wir in _src/main.rs_ definieren.

<Listing number="12-5" file-name="src/main.rs" caption="Eine Funktion `parse_config` aus `main` extrahieren">

```rust,ignore
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-05/src/main.rs:here}}
```

</Listing>

Wir sammeln die Kommandozeilenargumente weiterhin in einem Vektor, aber statt in
der Funktion `main` den Argumentwert an Index 1 der Variable `query` und den
Argumentwert an Index 2 der Variable `file_path` zuzuweisen, übergeben wir den
gesamten Vektor an die Funktion `parse_config`. Die Funktion `parse_config`
enthält dann die Logik, die bestimmt, welches Argument in welche Variable kommt,
und gibt die Werte an `main` zurück. Wir legen die Variablen `query` und
`file_path` weiterhin in `main` an, aber `main` ist nicht mehr dafür
verantwortlich, festzulegen, wie Kommandozeilenargumente und Variablen einander
entsprechen.

Dieser Umbau mag für unser kleines Programm übertrieben wirken, aber wir
refaktorisieren in kleinen, schrittweisen Schritten. Führe das Programm nach
dieser Änderung erneut aus, um zu prüfen, ob das Parsen der Argumente noch
funktioniert. Es ist gut, den Fortschritt oft zu prüfen, damit sich die Ursache
von Problemen leichter finden lässt, wenn sie auftreten.

#### Konfigurationswerte gruppieren {#grouping-configuration-values}

Mit einem weiteren kleinen Schritt können wir die Funktion `parse_config` weiter
verbessern. Im Moment geben wir ein Tupel zurück, zerlegen dieses Tupel aber
sofort wieder in seine einzelnen Teile. Das ist ein Zeichen dafür, dass wir
vielleicht noch nicht die richtige Abstraktion haben.

Ein weiterer Hinweis darauf, dass es Raum für Verbesserungen gibt, ist der Teil
`config` von `parse_config`, der nahelegt, dass die beiden zurückgegebenen Werte
zusammengehören und beide Teil eines Konfigurationswerts sind. Diese Bedeutung
bringen wir in der Struktur der Daten derzeit nur dadurch zum Ausdruck, dass wir
die beiden Werte in einem Tupel gruppieren; stattdessen legen wir die beiden
Werte in einem Struct ab und geben jedem Feld des Structs einen aussagekräftigen
Namen. Dadurch verstehen künftige Maintainer dieses Codes leichter, wie die
verschiedenen Werte zusammenhängen und welchen Zweck sie haben.

Listing 12-6 zeigt die Verbesserungen an der Funktion `parse_config`.

<Listing number="12-6" file-name="src/main.rs" caption="`parse_config` so refaktorisieren, dass es eine Instanz eines Structs `Config` zurückgibt">

```rust,should_panic,noplayground
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-06/src/main.rs:here}}
```

</Listing>

Wir haben ein Struct namens `Config` mit den Feldern `query` und `file_path`
hinzugefügt. Die Signatur von `parse_config` zeigt jetzt an, dass die Funktion
einen `Config`-Wert zurückgibt. Im Rumpf von `parse_config`, wo wir früher
String-Slices zurückgegeben haben, die auf `String`-Werte in `args` verweisen,
definieren wir `Config` jetzt so, dass es besessene `String`-Werte enthält. Die
Variable `args` in `main` ist der Owner der Argumentwerte und lässt die Funktion
`parse_config` sie nur ausleihen (_borrow_). Würde `Config` versuchen, die
Ownership der Werte in `args` zu übernehmen, würden wir also die
Borrowing-Regeln von Rust verletzen.

Es gibt mehrere Möglichkeiten, mit den `String`-Daten umzugehen; der einfachste,
wenn auch etwas ineffiziente Weg ist, auf den Werten die Methode `clone`
aufzurufen. Dadurch wird eine vollständige Kopie der Daten erstellt, die der
`Config`-Instanz gehört, was mehr Zeit und Speicher kostet, als eine Referenz
auf die String-Daten zu speichern. Das Klonen der Daten macht unseren Code aber
auch sehr unkompliziert, weil wir die Lifetimes der Referenzen nicht verwalten
müssen; unter diesen Umständen ist es ein lohnender Kompromiss, ein wenig
Performance für mehr Einfachheit aufzugeben.

> ### Die Abwägungen bei der Verwendung von `clone` {#the-trade-offs-of-using-clone}
>
> Viele Rustaceans neigen dazu, `clone` zum Beheben von Ownership-Problemen
> wegen der Laufzeitkosten zu vermeiden. In [Kapitel 13][ch13]<!-- ignore -->
> lernst du, wie du in solchen Situationen effizientere Methoden verwendest.
> Vorerst ist es aber in Ordnung, ein paar Strings zu kopieren, um
> weiterzukommen, denn du erstellst diese Kopien nur einmal, und dein Dateipfad
> und dein Suchstring sind sehr klein. Ein funktionierendes, etwas ineffizientes
> Programm ist besser, als zu versuchen, Code im ersten Anlauf bis ins Letzte zu
> optimieren. Wenn du mehr Erfahrung mit Rust hast, fällt es dir leichter,
> gleich mit der effizientesten Lösung zu beginnen, aber vorerst ist es völlig
> in Ordnung, `clone` aufzurufen.

Wir haben `main` so angepasst, dass es die von `parse_config` zurückgegebene
`Config`-Instanz in einer Variable namens `config` ablegt, und den Code, der
vorher die einzelnen Variablen `query` und `file_path` verwendet hat, so
angepasst, dass er jetzt stattdessen die Felder des Structs `Config` verwendet.

Jetzt drückt unser Code deutlicher aus, dass `query` und `file_path`
zusammengehören und dass ihr Zweck ist, die Funktionsweise des Programms zu
konfigurieren. Jeder Code, der diese Werte verwendet, weiß, dass er sie in der
Instanz `config` in den Feldern findet, die nach ihrem Zweck benannt sind.

#### Einen Konstruktor für `Config` erstellen {#creating-a-constructor-for-config}

Bisher haben wir die Logik zum Parsen der Kommandozeilenargumente aus `main`
extrahiert und in die Funktion `parse_config` gelegt. Dabei haben wir erkannt,
dass die Werte `query` und `file_path` zusammengehören und dass diese Beziehung
in unserem Code ausgedrückt werden sollte. Dann haben wir ein Struct `Config`
hinzugefügt, um den gemeinsamen Zweck von `query` und `file_path` zu benennen
und die Namen der Werte als Feldnamen des Structs aus der Funktion
`parse_config` zurückgeben zu können.

Da der Zweck der Funktion `parse_config` jetzt ist, eine `Config`-Instanz zu
erzeugen, können wir `parse_config` von einer gewöhnlichen Funktion in eine
Funktion namens `new` umwandeln, die dem Struct `Config` zugeordnet ist. Dadurch
wird der Code idiomatischer. Instanzen von Typen der Standardbibliothek wie
`String` erzeugen wir durch den Aufruf von `String::new`. Ebenso können wir,
wenn wir `parse_config` in eine `Config` zugeordnete Funktion `new` umwandeln,
Instanzen von `Config` durch den Aufruf von `Config::new` erzeugen. Listing 12-7
zeigt die nötigen Änderungen.

<Listing number="12-7" file-name="src/main.rs" caption="`parse_config` in `Config::new` umwandeln">

```rust,should_panic,noplayground
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-07/src/main.rs:here}}
```

</Listing>

Wir haben `main` an der Stelle, an der wir `parse_config` aufgerufen haben, so
angepasst, dass es stattdessen `Config::new` aufruft. Wir haben den Namen von
`parse_config` in `new` geändert und die Funktion in einen `impl`-Block
verschoben, der die Funktion `new` mit `Config` verknüpft. Versuch, diesen Code
erneut zu kompilieren, um sicherzugehen, dass er funktioniert.

### Die Fehlerbehandlung korrigieren {#fixing-the-error-handling}

Jetzt kümmern wir uns darum, unsere Fehlerbehandlung zu korrigieren. Erinnere
dich: Der Versuch, auf die Werte im Vektor `args` an Index 1 oder Index 2
zuzugreifen, löst einen Panic aus, wenn der Vektor weniger als drei Einträge
enthält. Führe das Programm ohne Argumente aus; das sieht so aus:

```console
{{#include ../listings/ch12-an-io-project/listing-12-07/output.txt}}
```

Die Zeile `index out of bounds: the len is 1 but the index is 1` ist eine
Fehlermeldung für Programmierende. Sie hilft unseren Endbenutzern nicht zu
verstehen, was sie stattdessen tun sollten. Ändern wir das jetzt.

#### Die Fehlermeldung verbessern {#improving-the-error-message}

In Listing 12-8 fügen wir der Funktion `new` eine Prüfung hinzu, die
sicherstellt, dass der Slice lang genug ist, bevor auf Index 1 und Index 2
zugegriffen wird. Ist der Slice nicht lang genug, löst das Programm einen Panic
aus und zeigt eine bessere Fehlermeldung an.

<Listing number="12-8" file-name="src/main.rs" caption="Eine Prüfung der Anzahl der Argumente hinzufügen">

```rust,ignore
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-08/src/main.rs:here}}
```

</Listing>

Dieser Code ähnelt
[der Funktion `Guess::new`, die wir in Listing 9-13 geschrieben haben][ch9-custom-types]<!-- ignore -->,
in der wir `panic!` aufgerufen haben, wenn das Argument `value` außerhalb des
Bereichs gültiger Werte lag. Statt hier auf einen Wertebereich zu prüfen, prüfen
wir, ob die Länge von `args` mindestens `3` beträgt, und der Rest der Funktion
kann unter der Annahme arbeiten, dass diese Bedingung erfüllt ist. Hat `args`
weniger als drei Einträge, ist diese Bedingung `true`, und wir rufen das Makro
`panic!` auf, um das Programm sofort zu beenden.

Führen wir das Programm mit diesen paar zusätzlichen Codezeilen in `new` erneut
ohne Argumente aus, um zu sehen, wie der Fehler jetzt aussieht:

```console
{{#include ../listings/ch12-an-io-project/listing-12-08/output.txt}}
```

Diese Ausgabe ist besser: Wir haben jetzt eine vernünftige Fehlermeldung. Wir
haben aber auch überflüssige Informationen, die wir unseren Benutzern nicht
geben wollen. Vielleicht ist die Technik aus Listing 9-13 hier nicht die beste:
Ein Aufruf von `panic!` ist für ein Programmierproblem angemessener als für ein
Problem bei der Benutzung,
[wie in Kapitel 9 besprochen][ch9-error-guidelines]<!-- ignore -->. Stattdessen
verwenden wir die andere Technik, die du in Kapitel 9 kennengelernt hast –
[die Rückgabe eines `Result`][ch9-result]<!-- ignore -->, das entweder Erfolg
oder einen Fehler anzeigt.

<!-- Old headings. Do not remove or links may break. -->

<a id="returning-a-result-from-new-instead-of-calling-panic"></a>

#### Ein `Result` zurückgeben, statt `panic!` aufzurufen {#returning-a-result-instead-of-calling-panic}

Wir können stattdessen einen `Result`-Wert zurückgeben, der im Erfolgsfall eine
`Config`-Instanz enthält und im Fehlerfall das Problem beschreibt. Außerdem
ändern wir den Namen der Funktion von `new` in `build`, weil viele
Programmierende erwarten, dass `new`-Funktionen nie fehlschlagen. Wenn
`Config::build` mit `main` kommuniziert, können wir mit dem Typ `Result`
signalisieren, dass es ein Problem gab. Dann können wir `main` so ändern, dass
es eine `Err`-Variante in einen praktischeren Fehler für unsere Benutzer
umwandelt, ohne den umgebenden Text über `thread
'main'` und `RUST_BACKTRACE`,
den ein Aufruf von `panic!` verursacht.

Listing 12-9 zeigt die Änderungen, die wir am Rückgabewert der Funktion, die wir
jetzt `Config::build` nennen, und am Rumpf der Funktion vornehmen müssen, um ein
`Result` zurückzugeben. Beachte, dass das erst kompiliert, wenn wir auch `main`
anpassen, was wir im nächsten Listing tun.

<Listing number="12-9" file-name="src/main.rs" caption="Ein `Result` aus `Config::build` zurückgeben">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-09/src/main.rs:here}}
```

</Listing>

Unsere Funktion `build` gibt ein `Result` zurück, mit einer `Config`-Instanz im
Erfolgsfall und einem String-Literal im Fehlerfall. Unsere Fehlerwerte sind
immer String-Literale mit der Lifetime `'static`.

Wir haben im Rumpf der Funktion zwei Änderungen vorgenommen: Statt `panic!`
aufzurufen, wenn der Benutzer nicht genügend Argumente übergibt, geben wir jetzt
einen `Err`-Wert zurück, und wir haben den Rückgabewert `Config` in ein `Ok`
verpackt. Durch diese Änderungen entspricht die Funktion ihrer neuen
Typsignatur.

Gibt `Config::build` einen `Err`-Wert zurück, kann die Funktion `main` den
`Result`-Wert behandeln, den die Funktion `build` zurückgibt, und den Prozess im
Fehlerfall sauberer beenden.

<!-- Old headings. Do not remove or links may break. -->

<a id="calling-confignew-and-handling-errors"></a>

#### `Config::build` aufrufen und Fehler behandeln {#calling-configbuild-and-handling-errors}

Um den Fehlerfall zu behandeln und eine benutzerfreundliche Meldung auszugeben,
müssen wir `main` so anpassen, dass es das von `Config::build` zurückgegebene
`Result` behandelt, wie in Listing 12-10 gezeigt. Außerdem nehmen wir `panic!`
die Verantwortung dafür ab, das Kommandozeilenwerkzeug mit einem Fehlercode
ungleich null zu beenden, und implementieren das stattdessen von Hand. Ein
Exit-Status ungleich null ist eine Konvention, um dem Prozess, der unser
Programm aufgerufen hat, zu signalisieren, dass das Programm mit einem
Fehlerzustand beendet wurde.

<Listing number="12-10" file-name="src/main.rs" caption="Mit einem Fehlercode beenden, wenn das Erzeugen einer `Config` fehlschlägt">

```rust,ignore
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-10/src/main.rs:here}}
```

</Listing>

In diesem Listing haben wir eine Methode verwendet, die wir noch nicht im Detail
behandelt haben: `unwrap_or_else`, die von der Standardbibliothek für
`Result<T, E>` definiert ist. Mit `unwrap_or_else` können wir eine eigene
Fehlerbehandlung ohne `panic!` definieren. Ist das `Result` ein `Ok`-Wert,
verhält sich diese Methode ähnlich wie `unwrap`: Sie gibt den inneren Wert
zurück, den `Ok` umschließt. Ist der Wert dagegen ein `Err`-Wert, ruft diese
Methode den Code in der Closure auf, einer anonymen Funktion, die wir definieren
und als Argument an `unwrap_or_else` übergeben. Closures behandeln wir
ausführlicher in [Kapitel 13][ch13]<!-- ignore -->. Vorerst musst du nur wissen,
dass `unwrap_or_else` den inneren Wert des `Err`, in diesem Fall den statischen
String `"not enough arguments"`, den wir in Listing 12-9 hinzugefügt haben, an
unsere Closure im Argument `err` übergibt, das zwischen den senkrechten Strichen
steht. Der Code in der Closure kann dann den Wert `err` verwenden, wenn er
ausgeführt wird.

Wir haben eine neue `use`-Zeile hinzugefügt, um `process` aus der
Standardbibliothek in den Gültigkeitsbereich zu bringen. Der Code in der
Closure, der im Fehlerfall ausgeführt wird, besteht nur aus zwei Zeilen: Wir
geben den Wert `err` aus und rufen dann `process::exit` auf. Die Funktion
`process::exit` beendet das Programm sofort und gibt die übergebene Zahl als
Exit-Statuscode zurück. Das ähnelt der auf `panic!` basierenden Behandlung, die
wir in Listing 12-8 verwendet haben, aber wir bekommen nicht mehr die ganze
zusätzliche Ausgabe. Probieren wir es aus:

```console
{{#include ../listings/ch12-an-io-project/listing-12-10/output.txt}}
```

Großartig! Diese Ausgabe ist viel freundlicher für unsere Benutzer.

<!-- Old headings. Do not remove or links may break. -->

<a id="extracting-logic-from-the-main-function"></a>

### Logik aus `main` extrahieren {#extracting-logic-from-main}

Nachdem wir das Refactoring des Konfigurations-Parsens abgeschlossen haben,
wenden wir uns der Logik des Programms zu. Wie in
[„Belange in Binary-Projekten trennen“](#separation-of-concerns-for-binary-projects)<!-- ignore -->
angekündigt, extrahieren wir eine Funktion namens `run`, die die gesamte Logik
enthält, die derzeit in der Funktion `main` steht und nichts mit dem Einrichten
der Konfiguration oder der Fehlerbehandlung zu tun hat. Wenn wir fertig sind,
ist die Funktion `main` knapp und lässt sich leicht durch Ansehen überprüfen,
und wir können Tests für die gesamte übrige Logik schreiben.

Listing 12-11 zeigt die kleine, schrittweise Verbesserung, eine Funktion `run`
zu extrahieren.

<Listing number="12-11" file-name="src/main.rs" caption="Eine Funktion `run` extrahieren, die den Rest der Programmlogik enthält">

```rust,ignore
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-11/src/main.rs:here}}
```

</Listing>

Die Funktion `run` enthält jetzt die gesamte verbleibende Logik aus `main`,
beginnend mit dem Lesen der Datei. Die Funktion `run` nimmt die `Config`-Instanz
als Argument.

<!-- Old headings. Do not remove or links may break. -->

<a id="returning-errors-from-the-run-function"></a>

#### Fehler aus `run` zurückgeben {#returning-errors-from-run}

Nachdem die verbleibende Programmlogik in die Funktion `run` ausgelagert ist,
können wir die Fehlerbehandlung verbessern, wie wir es bei `Config::build` in
Listing 12-9 getan haben. Statt das Programm durch den Aufruf von `expect` einen
Panic auslösen zu lassen, gibt die Funktion `run` ein `Result<T, E>` zurück,
wenn etwas schiefgeht. So können wir die Logik zur Fehlerbehandlung weiter
benutzerfreundlich in `main` bündeln. Listing 12-12 zeigt die Änderungen, die
wir an der Signatur und am Rumpf von `run` vornehmen müssen.

<Listing number="12-12" file-name="src/main.rs" caption="Die Funktion `run` so ändern, dass sie `Result` zurückgibt">

```rust,ignore
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-12/src/main.rs:here}}
```

</Listing>

Wir haben hier drei wesentliche Änderungen vorgenommen. Erstens haben wir den
Rückgabetyp der Funktion `run` in `Result<(), Box<dyn Error>>` geändert. Diese
Funktion hat vorher den Unit-Typ `()` zurückgegeben, und den behalten wir als
Rückgabewert im Fall `Ok` bei.

Für den Fehlertyp haben wir das Trait-Objekt `Box<dyn Error>` verwendet (und
`std::error::Error` mit einer `use`-Anweisung am Anfang in den
Gültigkeitsbereich gebracht). Trait-Objekte behandeln wir in
[Kapitel 18][ch18]<!-- ignore -->. Vorerst genügt es zu wissen, dass
`Box<dyn Error>` bedeutet, dass die Funktion einen Typ zurückgibt, der den Trait
`Error` implementiert, wir aber nicht angeben müssen, welchen konkreten Typ der
Rückgabewert hat. Das gibt uns die Flexibilität, Fehlerwerte zurückzugeben, die
in verschiedenen Fehlerfällen unterschiedliche Typen haben können. Das
Schlüsselwort `dyn` ist die Kurzform von _dynamisch_ (_dynamic_).

Zweitens haben wir den Aufruf von `expect` zugunsten des Operators `?` entfernt,
wie wir in [Kapitel 9][ch9-question-mark]<!-- ignore --> besprochen haben. Statt
bei einem Fehler `panic!` auszulösen, gibt `?` den Fehlerwert aus der aktuellen
Funktion zurück, damit der Aufrufer ihn behandeln kann.

Drittens gibt die Funktion `run` im Erfolgsfall jetzt einen `Ok`-Wert zurück.
Wir haben den Erfolgstyp der Funktion `run` in der Signatur als `()` deklariert,
das heißt, wir müssen den Wert des Unit-Typs in den `Ok`-Wert verpacken. Diese
Syntax `Ok(())` sieht anfangs vielleicht etwas seltsam aus. Aber `()` so zu
verwenden, ist die idiomatische Art anzuzeigen, dass wir `run` nur wegen seiner
Seiteneffekte aufrufen; es gibt keinen Wert zurück, den wir brauchen.

Wenn du diesen Code ausführst, kompiliert er, zeigt aber eine Warnung an:

```console
{{#include ../listings/ch12-an-io-project/listing-12-12/output.txt}}
```

Rust teilt uns mit, dass unser Code den `Result`-Wert ignoriert hat und dass der
`Result`-Wert darauf hinweisen könnte, dass ein Fehler aufgetreten ist. Wir
prüfen aber nicht, ob es einen Fehler gab, und der Compiler erinnert uns daran,
dass wir hier wahrscheinlich Code zur Fehlerbehandlung haben wollten! Beheben
wir dieses Problem jetzt.

#### Von `run` zurückgegebene Fehler in `main` behandeln {#handling-errors-returned-from-run-in-main}

Wir prüfen auf Fehler und behandeln sie mit einer Technik, die der ähnelt, die
wir in Listing 12-10 bei `Config::build` verwendet haben, mit einem kleinen
Unterschied:

<span class="filename">Dateiname: src/main.rs</span>

```rust,ignore
{{#rustdoc_include ../listings/ch12-an-io-project/no-listing-01-handling-errors-in-main/src/main.rs:here}}
```

Wir verwenden `if let` statt `unwrap_or_else`, um zu prüfen, ob `run` einen
`Err`-Wert zurückgibt, und rufen in diesem Fall `process::exit(1)` auf. Die
Funktion `run` gibt keinen Wert zurück, den wir auf dieselbe Weise mit `unwrap`
auspacken wollen, wie `Config::build` die `Config`-Instanz zurückgibt. Da `run`
im Erfolgsfall `()` zurückgibt, interessiert uns nur, ob ein Fehler auftritt,
also brauchen wir `unwrap_or_else` nicht, um den ausgepackten Wert
zurückzugeben, der ohnehin nur `()` wäre.

Die Rümpfe von `if let` und der Funktion `unwrap_or_else` sind in beiden Fällen
gleich: Wir geben den Fehler aus und beenden das Programm.

### Code in ein Library-Crate aufteilen {#splitting-code-into-a-library-crate}

Unser Projekt `minigrep` sieht bisher gut aus! Jetzt teilen wir die Datei
_src/main.rs_ auf und legen etwas Code in die Datei _src/lib.rs_. So können wir
den Code testen und haben eine Datei _src/main.rs_ mit weniger
Verantwortlichkeiten.

Definieren wir den Code, der für das Durchsuchen von Text verantwortlich ist, in
_src/lib.rs_ statt in _src/main.rs_. Dadurch können wir (oder jeder andere, der
unsere Bibliothek `minigrep` verwendet) die Suchfunktion aus mehr Kontexten
aufrufen als nur aus unserer Binärdatei `minigrep`.

Definieren wir zuerst die Signatur der Funktion `search` in _src/lib.rs_, wie in
Listing 12-13 gezeigt, mit einem Rumpf, der das Makro `unimplemented!` aufruft.
Die Signatur erklären wir ausführlicher, wenn wir die Implementierung ergänzen.

<Listing number="12-13" file-name="src/lib.rs" caption="Die Funktion `search` in *src/lib.rs* definieren">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-13/src/lib.rs}}
```

</Listing>

Wir haben das Schlüsselwort `pub` an der Funktionsdefinition verwendet, um
`search` als Teil der öffentlichen API unseres Library-Crates zu kennzeichnen.
Wir haben jetzt ein Library-Crate, das wir aus unserem Binary-Crate verwenden
und das wir testen können!

Nun müssen wir den in _src/lib.rs_ definierten Code in den Gültigkeitsbereich
des Binary-Crates in _src/main.rs_ bringen und aufrufen, wie in Listing 12-14
gezeigt.

<Listing number="12-14" file-name="src/main.rs" caption="Die Funktion `search` des Library-Crates `minigrep` in *src/main.rs* verwenden">

```rust,ignore
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-14/src/main.rs:here}}
```

</Listing>

Wir fügen eine Zeile `use minigrep::search` hinzu, um die Funktion `search` aus
dem Library-Crate in den Gültigkeitsbereich des Binary-Crates zu bringen. Dann
geben wir in der Funktion `run` nicht mehr den Inhalt der Datei aus, sondern
rufen die Funktion `search` auf und übergeben den Wert `config.query` und
`contents` als Argumente. Anschließend gibt `run` mit einer `for`-Schleife jede
Zeile aus, die `search` zurückgibt und die zur Suchanfrage passt. Das ist auch
ein guter Zeitpunkt, die `println!`-Aufrufe in der Funktion `main` zu entfernen,
die die Suchanfrage und den Dateipfad angezeigt haben, damit unser Programm nur
die Suchergebnisse ausgibt (sofern keine Fehler auftreten).

Beachte, dass die Suchfunktion alle Ergebnisse in einem Vektor sammelt, den sie
zurückgibt, bevor irgendetwas ausgegeben wird. Bei dieser Implementierung kann
es beim Durchsuchen großer Dateien lange dauern, bis Ergebnisse angezeigt
werden, weil die Ergebnisse nicht ausgegeben werden, sobald sie gefunden werden;
eine mögliche Lösung mit Iteratoren besprechen wir in Kapitel 13.

Puh! Das war viel Arbeit, aber wir haben uns gut für die Zukunft aufgestellt.
Jetzt lassen sich Fehler viel leichter behandeln, und wir haben den Code
modularer gemacht. Fast unsere gesamte Arbeit findet von nun an in _src/lib.rs_
statt.

Nutzen wir diese neu gewonnene Modularität und tun etwas, das mit dem alten Code
schwierig gewesen wäre, mit dem neuen Code aber einfach ist: Wir schreiben
einige Tests!

[ch13]: ch13-00-functional-features.html
[ch9-custom-types]: ch09-03-to-panic-or-not-to-panic.html#creating-custom-types-for-validation
[ch9-error-guidelines]: ch09-03-to-panic-or-not-to-panic.html#guidelines-for-error-handling
[ch9-result]: ch09-02-recoverable-errors-with-result.html
[ch18]: ch18-00-oop.html
[ch9-question-mark]: ch09-02-recoverable-errors-with-result.html#a-shortcut-for-propagating-errors-the--operator
