# Ein Ratespiel programmieren {#programming-a-guessing-game}

Lass uns direkt in Rust einsteigen und gemeinsam ein praktisches Projekt
durcharbeiten! Dieses Kapitel stellt dir einige gängige Rust-Konzepte vor, indem
es zeigt, wie du sie in einem echten Programm verwendest. Du lernst `let`,
`match`, Methoden, assoziierte Funktionen, externe Crates und mehr kennen! In
den folgenden Kapiteln erkunden wir diese Ideen genauer. In diesem Kapitel übst
du nur die Grundlagen.

Wir implementieren ein klassisches Einsteigerproblem der Programmierung: ein
Ratespiel. So funktioniert es: Das Programm erzeugt eine zufällige Ganzzahl
zwischen 1 und 100. Dann fordert es den Spieler oder die Spielerin auf, einen
Tipp einzugeben. Nach der Eingabe zeigt das Programm an, ob der Tipp zu niedrig
oder zu hoch ist. Ist der Tipp richtig, gibt das Spiel eine Glückwunschnachricht
aus und beendet sich.

> **Hinweis:** In diesem Kapitel gibt es keine Quiz, denn es soll dir nur ein
> Gefühl für die Sprache vermitteln.

## Ein neues Projekt anlegen {#setting-up-a-new-project}

Um ein neues Projekt anzulegen, wechselst du in das Verzeichnis _projects_, das
du in Kapitel 1 erstellt hast, und legst mit Cargo ein neues Projekt an, etwa
so:

```console
$ cargo new guessing_game
$ cd guessing_game
```

Der erste Befehl, `cargo new`, nimmt den Namen des Projekts (`guessing_game`)
als erstes Argument. Der zweite Befehl wechselt in das Verzeichnis des neuen
Projekts.

Sieh dir die erzeugte Datei _Cargo.toml_ an:

<!-- manual-regeneration
cd listings/ch02-guessing-game-tutorial
rm -rf no-listing-01-cargo-new
cargo new no-listing-01-cargo-new --name guessing_game
cd no-listing-01-cargo-new
cargo run > output.txt 2>&1
cd ../../..
-->

<span class="filename">Dateiname: Cargo.toml</span>

```toml
{{#include ../listings/ch02-guessing-game-tutorial/no-listing-01-cargo-new/Cargo.toml}}
```

Wie du in Kapitel 1 gesehen hast, erzeugt `cargo new` ein „Hello,
world!“-Programm für dich. Sieh dir die Datei _src/main.rs_ an:

<span class="filename">Dateiname: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/no-listing-01-cargo-new/src/main.rs}}
```

Kompilieren wir nun dieses „Hello, world!“-Programm und führen es im selben
Schritt mit dem Befehl `cargo run` aus:

```console
{{#include ../listings/ch02-guessing-game-tutorial/no-listing-01-cargo-new/output.txt}}
```

Der Befehl `run` ist praktisch, wenn du ein Projekt schnell weiterentwickeln
willst, wie wir es in diesem Spiel tun: Jede Iteration wird kurz getestet, bevor
es mit der nächsten weitergeht.

Öffne die Datei _src/main.rs_ erneut. Du schreibst den gesamten Code in diese
Datei.

## Einen Tipp verarbeiten {#processing-a-guess}

Der erste Teil des Ratespiels fragt nach einer Benutzereingabe, verarbeitet
diese Eingabe und prüft, ob sie die erwartete Form hat. Zunächst lassen wir den
Spieler einen Tipp eingeben. Gib den Code aus Listing 2-1 in _src/main.rs_ ein.

<Listing number="2-1" file-name="src/main.rs" caption="Code, der einen Tipp vom Benutzer einliest und ausgibt">

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/listing-02-01/src/main.rs:all}}
```

</Listing>

Dieser Code enthält viele Informationen, also gehen wir ihn Zeile für Zeile
durch. Um eine Benutzereingabe zu erhalten und das Ergebnis anschließend
auszugeben, müssen wir die Ein-/Ausgabe-Bibliothek `io` in den
Gültigkeitsbereich (_scope_) bringen. Die Bibliothek `io` stammt aus der
Standardbibliothek, die als `std` bekannt ist:

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/listing-02-01/src/main.rs:io}}
```

Standardmäßig bringt Rust eine Reihe von Elementen, die in der
Standardbibliothek definiert sind, in den Gültigkeitsbereich jedes Programms.
Diese Menge heißt _Prelude_, und du kannst ihren gesamten Inhalt
[in der Dokumentation der Standardbibliothek][prelude] nachsehen.

Wenn ein Typ, den du verwenden willst, nicht im Prelude enthalten ist, musst du
ihn explizit mit einer `use`-Anweisung in den Gültigkeitsbereich bringen. Die
Bibliothek `std::io` bietet dir eine Reihe nützlicher Features, darunter die
Möglichkeit, Benutzereingaben entgegenzunehmen.

Wie du in Kapitel 1 gesehen hast, ist die Funktion `main` der Einstiegspunkt in
das Programm:

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/listing-02-01/src/main.rs:main}}
```

Die Syntax `fn` deklariert eine neue Funktion; die runden Klammern `()` zeigen
an, dass es keine Parameter gibt; und die geschweifte Klammer `{` leitet den
Rumpf der Funktion ein.

Wie du ebenfalls in Kapitel 1 gelernt hast, ist `println!` ein Makro, das einen
String auf dem Bildschirm ausgibt:

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/listing-02-01/src/main.rs:print}}
```

Dieser Code gibt eine Aufforderung aus, die erklärt, worum es im Spiel geht, und
um eine Eingabe bittet.

### Werte in Variablen speichern {#storing-values-with-variables}

Als Nächstes erzeugen wir eine _Variable_, um die Benutzereingabe zu speichern,
etwa so:

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/listing-02-01/src/main.rs:string}}
```

Jetzt wird das Programm interessant! In dieser kleinen Zeile passiert eine
Menge. Wir verwenden die Anweisung `let`, um die Variable zu erzeugen. Hier ist
ein weiteres Beispiel:

```rust,ignore
let apples = 5;
```

Diese Zeile erzeugt eine neue Variable namens `apples` und bindet sie an den
Wert `5`. In Rust sind Variablen standardmäßig unveränderlich (_immutable_):
Sobald wir der Variable einen Wert gegeben haben, ändert sich dieser Wert nicht
mehr. Wir besprechen dieses Konzept ausführlich im Abschnitt
[„Variablen und Veränderlichkeit“][variables-and-mutability]<!-- ignore --> in
Kapitel 3. Um eine Variable veränderlich (_mutable_) zu machen, schreiben wir
`mut` vor den Variablennamen:

```rust,ignore
let apples = 5; // immutable
let mut bananas = 5; // mutable
```

> Note: Die Syntax `//` leitet einen Kommentar ein, der bis zum Ende der Zeile
> reicht. Rust ignoriert alles in Kommentaren. Wir besprechen Kommentare
> ausführlicher in [Kapitel 3][comments]<!-- ignore -->.

Zurück zum Ratespiel: Du weißt jetzt, dass `let mut guess` eine veränderliche
Variable namens `guess` einführt. Das Gleichheitszeichen (`=`) sagt Rust, dass
wir jetzt etwas an die Variable binden wollen. Rechts vom Gleichheitszeichen
steht der Wert, an den `guess` gebunden wird, nämlich das Ergebnis des Aufrufs
von `String::new`, einer Funktion, die eine neue Instanz eines `String`
zurückgibt. [`String`][string]<!-- ignore --> ist ein String-Typ aus der
Standardbibliothek, ein wachsendes, UTF-8-kodiertes Stück Text.

Die Syntax `::` in der Zeile mit `::new` zeigt an, dass `new` eine assoziierte
Funktion des Typs `String` ist. Eine _assoziierte Funktion_ ist eine Funktion,
die auf einem Typ implementiert ist, in diesem Fall auf `String`. Diese Funktion
`new` erzeugt einen neuen, leeren String. Eine Funktion `new` findest du bei
vielen Typen, weil das ein gängiger Name für eine Funktion ist, die einen neuen
Wert irgendeiner Art erzeugt.

Insgesamt hat die Zeile `let mut guess = String::new();` also eine veränderliche
Variable erzeugt, die gerade an eine neue, leere Instanz eines `String` gebunden
ist. Puh!

### Benutzereingaben entgegennehmen {#receiving-user-input}

Erinnere dich: Wir haben die Ein-/Ausgabe-Funktionalität der Standardbibliothek
mit `use std::io;` in der ersten Zeile des Programms eingebunden. Jetzt rufen
wir die Funktion `stdin` aus dem Modul `io` auf, mit der wir Benutzereingaben
verarbeiten können:

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/listing-02-01/src/main.rs:read}}
```

Hätten wir das Modul `io` nicht am Anfang des Programms mit `use std::io;`
importiert, könnten wir die Funktion trotzdem verwenden, indem wir den
Funktionsaufruf als `std::io::stdin` schreiben. Die Funktion `stdin` gibt eine
Instanz von [`std::io::Stdin`][iostdin]<!-- ignore --> zurück, einem Typ, der
ein Handle auf die Standardeingabe deines Terminals darstellt.

Als Nächstes ruft die Zeile `.read_line(&mut guess)` die Methode
[`read_line`][read_line]<!-- ignore --> auf dem Handle der Standardeingabe auf,
um eine Eingabe vom Benutzer zu erhalten. Außerdem übergeben wir `&mut guess`
als Argument an `read_line`, um der Methode mitzuteilen, in welchem String sie
die Benutzereingabe speichern soll. Die Aufgabe von `read_line` ist es, alles,
was der Benutzer in die Standardeingabe tippt, an einen String anzuhängen (ohne
dessen Inhalt zu überschreiben); deshalb übergeben wir diesen String als
Argument. Das String-Argument muss veränderlich sein, damit die Methode den
Inhalt des Strings ändern kann.

Das `&` zeigt an, dass dieses Argument eine _Referenz_ ist. Referenzen
ermöglichen es mehreren Teilen deines Codes, auf dasselbe Datenstück
zuzugreifen, ohne diese Daten mehrfach in den Speicher kopieren zu müssen.
Referenzen sind ein komplexes Feature, und einer der großen Vorteile von Rust
ist, wie sicher und einfach die Verwendung von Referenzen ist. Für dieses
Programm musst du nicht viele dieser Details kennen. Vorerst genügt es zu
wissen, dass Referenzen, wie Variablen, standardmäßig unveränderlich sind.
Deshalb musst du `&mut guess` statt `&guess` schreiben, um sie veränderlich zu
machen. (Kapitel 4 erklärt Referenzen ausführlicher.)

<!-- Old headings. Do not remove or links may break. -->

<a id="handling-potential-failure-with-the-result-type"></a>

### Mögliche Fehler mit `Result` behandeln {#handling-potential-failure-with-result}

Wir arbeiten immer noch an dieser Codezeile. Wir besprechen jetzt eine dritte
Textzeile, aber beachte, dass sie immer noch Teil einer einzigen logischen
Codezeile ist. Der nächste Teil ist diese Methode:

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/listing-02-01/src/main.rs:expect}}
```

Wir hätten diesen Code auch so schreiben können:

```rust,ignore
io::stdin().read_line(&mut guess).expect("Failed to read line");
```

Eine einzige lange Zeile ist allerdings schwer zu lesen, daher ist es am besten,
sie aufzuteilen. Wenn du eine Methode mit der Syntax `.method_name()` aufrufst,
ist es oft sinnvoll, einen Zeilenumbruch und weitere Leerzeichen einzufügen, um
lange Zeilen aufzubrechen. Besprechen wir nun, was diese Zeile tut.

Wie schon erwähnt, schreibt `read_line` alles, was der Benutzer eingibt, in den
String, den wir übergeben, gibt aber außerdem einen `Result`-Wert zurück.
[`Result`][result]<!-- ignore --> ist eine
[_Enumeration_][enums]<!-- ignore -->, oft _Enum_ genannt, also ein Typ, der
sich in einem von mehreren möglichen Zuständen befinden kann. Jeden möglichen
Zustand nennen wir eine _Variante_.

[Kapitel 6][enums]<!-- ignore --> behandelt Enums ausführlicher. Der Zweck
dieser `Result`-Typen ist es, Informationen zur Fehlerbehandlung zu kodieren.

Die Varianten von `Result` sind `Ok` und `Err`. Die Variante `Ok` zeigt an, dass
die Operation erfolgreich war, und enthält den erfolgreich erzeugten Wert. Die
Variante `Err` bedeutet, dass die Operation fehlgeschlagen ist, und enthält
Informationen darüber, wie oder warum sie fehlgeschlagen ist.

Werte vom Typ `Result` haben, wie Werte jedes Typs, Methoden, die auf ihnen
definiert sind. Eine Instanz von `Result` hat eine
[Methode `expect`][expect]<!-- ignore -->, die du aufrufen kannst. Ist diese
Instanz von `Result` ein `Err`-Wert, lässt `expect` das Programm abstürzen und
zeigt die Nachricht an, die du `expect` als Argument übergeben hast. Wenn die
Methode `read_line` ein `Err` zurückgibt, liegt das wahrscheinlich an einem
Fehler des zugrunde liegenden Betriebssystems. Ist diese Instanz von `Result`
ein `Ok`-Wert, nimmt `expect` den Rückgabewert, den `Ok` enthält, und gibt dir
genau diesen Wert zurück, damit du ihn verwenden kannst. In diesem Fall ist
dieser Wert die Anzahl der Bytes in der Benutzereingabe.

Wenn du `expect` nicht aufrufst, lässt sich das Programm zwar kompilieren, aber
du bekommst eine Warnung:

```console
{{#include ../listings/ch02-guessing-game-tutorial/no-listing-02-without-expect/output.txt}}
```

Rust warnt, dass du den von `read_line` zurückgegebenen `Result`-Wert nicht
verwendet hast, was darauf hindeutet, dass das Programm einen möglichen Fehler
nicht behandelt hat.

Der richtige Weg, die Warnung zu unterdrücken, ist, tatsächlich Code zur
Fehlerbehandlung zu schreiben. In unserem Fall wollen wir das Programm aber
einfach abstürzen lassen, wenn ein Problem auftritt, also können wir `expect`
verwenden. Wie du dich von Fehlern erholst, lernst du in
[Kapitel 9][recover]<!-- ignore -->.

### Werte mit Platzhaltern in `println!` ausgeben {#printing-values-with-println-placeholders}

Abgesehen von der schließenden geschweiften Klammer gibt es im bisherigen Code
nur noch eine Zeile zu besprechen:

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/listing-02-01/src/main.rs:print_guess}}
```

Diese Zeile gibt den String aus, der jetzt die Benutzereingabe enthält. Das Paar
geschweifter Klammern `{}` ist ein Platzhalter: Stell dir `{}` als kleine
Krabbenzangen vor, die einen Wert festhalten. Wenn du den Wert einer Variable
ausgibst, kann der Variablenname innerhalb der geschweiften Klammern stehen.
Wenn du das Ergebnis eines ausgewerteten Ausdrucks ausgibst, setzt du leere
geschweifte Klammern in den Format-String und lässt auf den Format-String eine
kommagetrennte Liste von Ausdrücken folgen, die in derselben Reihenfolge in die
leeren Platzhalter eingesetzt werden. Eine Variable und das Ergebnis eines
Ausdrucks in einem einzigen Aufruf von `println!` auszugeben, sähe so aus:

```rust
let x = 5;
let y = 10;

println!("x = {x} and y + 2 = {}", y + 2);
```

Dieser Code würde `x = 5 and y + 2 = 12` ausgeben.

### Den ersten Teil testen {#testing-the-first-part}

Testen wir den ersten Teil des Ratespiels. Führe es mit `cargo run` aus:

<!-- manual-regeneration
cd listings/ch02-guessing-game-tutorial/listing-02-01/
cargo clean
cargo run
input 6 -->

```console
$ cargo run
   Compiling guessing_game v0.1.0 (file:///projects/guessing_game)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 6.44s
     Running `target/debug/guessing_game`
Guess the number!
Please input your guess.
6
You guessed: 6
```

Damit ist der erste Teil des Spiels fertig: Wir lesen eine Eingabe von der
Tastatur ein und geben sie anschließend aus.

## Eine Geheimzahl erzeugen {#generating-a-secret-number}

Als Nächstes müssen wir eine Geheimzahl erzeugen, die der Benutzer zu erraten
versucht. Die Geheimzahl sollte jedes Mal anders sein, damit das Spiel auch
mehrmals Spaß macht. Wir verwenden eine Zufallszahl zwischen 1 und 100, damit
das Spiel nicht zu schwierig wird. Rust enthält in seiner Standardbibliothek
noch keine Funktionalität für Zufallszahlen. Das Rust-Team stellt aber ein
[Crate `rand`][randcrate] mit dieser Funktionalität bereit.

<!-- Old headings. Do not remove or links may break. -->

<a id="using-a-crate-to-get-more-functionality"></a>

### Funktionalität mit einem Crate erweitern {#increasing-functionality-with-a-crate}

Denk daran, dass ein Crate eine Sammlung von Rust-Quelldateien ist. Das Projekt,
das wir bauen, ist ein Binary-Crate, also eine ausführbare Datei. Das Crate
`rand` ist ein Library-Crate: Es enthält Code, der in anderen Programmen
verwendet werden soll und nicht eigenständig ausgeführt werden kann.

Bei der Koordination externer Crates zeigt Cargo erst richtig, was es kann.
Bevor wir Code schreiben können, der `rand` verwendet, müssen wir die Datei
_Cargo.toml_ ändern, um das Crate `rand` als Abhängigkeit aufzunehmen. Öffne
diese Datei jetzt und füge die folgende Zeile ganz unten ein, unterhalb der
Abschnittsüberschrift `[dependencies]`, die Cargo für dich angelegt hat. Gib
`rand` unbedingt genau so an wie wir hier, mit dieser Versionsnummer, sonst
funktionieren die Codebeispiele in diesem Tutorial möglicherweise nicht:

<!-- When updating the version of `rand` used, also update the version of
`rand` used in these files so they all match:
* ch07-04-bringing-paths-into-scope-with-the-use-keyword.md
* ch14-03-cargo-workspaces.md
-->

<span class="filename">Dateiname: Cargo.toml</span>

```toml
{{#include ../listings/ch02-guessing-game-tutorial/listing-02-02/Cargo.toml:8:}}
```

In der Datei _Cargo.toml_ gehört alles, was auf eine Überschrift folgt, zu
diesem Abschnitt, bis ein anderer Abschnitt beginnt. Unter `[dependencies]`
teilst du Cargo mit, von welchen externen Crates dein Projekt abhängt und welche
Versionen dieser Crates du benötigst. In diesem Fall geben wir das Crate `rand`
mit der semantischen Versionsangabe `0.8.5` an. Cargo versteht
[Semantic Versioning][semver]<!-- ignore --> (manchmal _SemVer_ genannt), einen
Standard für das Schreiben von Versionsnummern. Die Angabe `0.8.5` ist
eigentlich eine Kurzform für `^0.8.5` und bedeutet jede Version, die mindestens
0.8.5, aber kleiner als 0.9.0 ist.

Cargo geht davon aus, dass diese Versionen öffentliche APIs haben, die mit
Version 0.8.5 kompatibel sind, und diese Angabe stellt sicher, dass du das
neueste Patch-Release bekommst, das sich noch mit dem Code in diesem Kapitel
kompilieren lässt. Bei Version 0.9.0 oder höher ist nicht garantiert, dass sie
dieselbe API hat, die die folgenden Beispiele verwenden.

Bauen wir nun, ohne den Code zu ändern, das Projekt, wie in Listing 2-2 gezeigt.

<!-- manual-regeneration
cd listings/ch02-guessing-game-tutorial/listing-02-02/
rm Cargo.lock
cargo clean
cargo build -->

<Listing number="2-2" caption="Die Ausgabe von `cargo build`, nachdem das Crate `rand` als Abhängigkeit hinzugefügt wurde">

```console
$ cargo build
  Updating crates.io index
   Locking 15 packages to latest Rust 1.85.0 compatible versions
    Adding rand v0.8.5 (available: v0.9.0)
 Compiling proc-macro2 v1.0.93
 Compiling unicode-ident v1.0.17
 Compiling libc v0.2.170
 Compiling cfg-if v1.0.0
 Compiling byteorder v1.5.0
 Compiling getrandom v0.2.15
 Compiling rand_core v0.6.4
 Compiling quote v1.0.38
 Compiling syn v2.0.98
 Compiling zerocopy-derive v0.7.35
 Compiling zerocopy v0.7.35
 Compiling ppv-lite86 v0.2.20
 Compiling rand_chacha v0.3.1
 Compiling rand v0.8.5
 Compiling guessing_game v0.1.0 (file:///projects/guessing_game)
  Finished `dev` profile [unoptimized + debuginfo] target(s) in 2.48s
```

</Listing>

Möglicherweise siehst du andere Versionsnummern (die dank SemVer aber alle mit
dem Code kompatibel sind) und andere Zeilen (je nach Betriebssystem), und die
Zeilen können in einer anderen Reihenfolge stehen.

Wenn wir eine externe Abhängigkeit einbinden, holt Cargo die neuesten Versionen
von allem, was diese Abhängigkeit braucht, aus der _Registry_, einer Kopie der
Daten von [Crates.io][cratesio]. Auf Crates.io veröffentlichen Menschen im
Rust-Ökosystem ihre Open-Source-Rust-Projekte, damit andere sie nutzen können.

Nach dem Aktualisieren der Registry prüft Cargo den Abschnitt `[dependencies]`
und lädt alle aufgeführten Crates herunter, die noch nicht heruntergeladen sind.
Obwohl wir in diesem Fall nur `rand` als Abhängigkeit angegeben haben, hat Cargo
auch andere Crates geholt, die `rand` zum Funktionieren braucht. Nach dem
Herunterladen der Crates kompiliert Rust sie und kompiliert dann das Projekt mit
den verfügbaren Abhängigkeiten.

Wenn du `cargo build` sofort noch einmal ausführst, ohne etwas zu ändern,
bekommst du außer der Zeile `Finished` keine Ausgabe. Cargo weiß, dass es die
Abhängigkeiten bereits heruntergeladen und kompiliert hat und dass du in deiner
Datei _Cargo.toml_ nichts an ihnen geändert hast. Cargo weiß außerdem, dass du
nichts an deinem Code geändert hast, also kompiliert es auch diesen nicht neu.
Da es nichts zu tun gibt, beendet es sich einfach.

Wenn du die Datei _src/main.rs_ öffnest, eine kleine Änderung vornimmst, sie
dann speicherst und erneut baust, siehst du nur zwei Ausgabezeilen:

<!-- manual-regeneration
cd listings/ch02-guessing-game-tutorial/listing-02-02/
touch src/main.rs
cargo build -->

```console
$ cargo build
   Compiling guessing_game v0.1.0 (file:///projects/guessing_game)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.13s
```

Diese Zeilen zeigen, dass Cargo den Build nur um deine kleine Änderung an der
Datei _src/main.rs_ aktualisiert. Deine Abhängigkeiten haben sich nicht
geändert, also weiß Cargo, dass es wiederverwenden kann, was es für sie bereits
heruntergeladen und kompiliert hat.

<!-- Old headings. Do not remove or links may break. -->

<a id="ensuring-reproducible-builds-with-the-cargo-lock-file"></a>

#### Reproduzierbare Builds sicherstellen {#ensuring-reproducible-builds}

Cargo hat einen Mechanismus, der sicherstellt, dass du jedes Mal dasselbe
Artefakt erhältst, wenn du oder jemand anderes deinen Code baut: Cargo verwendet
nur die Versionen der Abhängigkeiten, die du angegeben hast, bis du etwas
anderes festlegst. Angenommen, nächste Woche erscheint Version 0.8.6 des Crates
`rand`, und diese Version enthält eine wichtige Fehlerkorrektur, aber auch eine
Regression, die deinen Code kaputt macht. Für diesen Fall erzeugt Rust die Datei
_Cargo.lock_, wenn du `cargo build` zum ersten Mal ausführst; diese Datei haben
wir jetzt im Verzeichnis _guessing_game_.

Wenn du ein Projekt zum ersten Mal baust, ermittelt Cargo alle Versionen der
Abhängigkeiten, die die Kriterien erfüllen, und schreibt sie in die Datei
_Cargo.lock_. Wenn du dein Projekt später baust, sieht Cargo, dass die Datei
_Cargo.lock_ existiert, und verwendet die dort angegebenen Versionen, statt die
ganze Arbeit der Versionsermittlung erneut zu machen. So bekommst du automatisch
einen reproduzierbaren Build. Anders gesagt: Dank der Datei _Cargo.lock_ bleibt
dein Projekt bei 0.8.5, bis du explizit aktualisierst. Weil die Datei
_Cargo.lock_ für reproduzierbare Builds wichtig ist, wird sie oft zusammen mit
dem restlichen Code deines Projekts in die Versionskontrolle eingecheckt.

#### Ein Crate auf eine neue Version aktualisieren {#updating-a-crate-to-get-a-new-version}

Wenn du ein Crate _doch_ aktualisieren willst, bietet Cargo den Befehl `update`,
der die Datei _Cargo.lock_ ignoriert und alle neuesten Versionen ermittelt, die
zu deinen Angaben in _Cargo.toml_ passen. Diese Versionen schreibt Cargo dann in
die Datei _Cargo.lock_. Ansonsten sucht Cargo standardmäßig nur nach Versionen
größer als 0.8.5 und kleiner als 0.9.0. Hätte das Crate `rand` die beiden neuen
Versionen 0.8.6 und 0.999.0 veröffentlicht, würdest du beim Ausführen von
`cargo update` Folgendes sehen:

<!-- manual-regeneration
cd listings/ch02-guessing-game-tutorial/listing-02-02/
cargo update
assuming there is a new 0.8.x version of rand; otherwise use another update
as a guide to creating the hypothetical output shown here -->

```console
$ cargo update
    Updating crates.io index
     Locking 1 package to latest Rust 1.85.0 compatible version
    Updating rand v0.8.5 -> v0.8.6 (available: v0.999.0)
```

Cargo ignoriert das Release 0.999.0. Du würdest jetzt auch eine Änderung in
deiner Datei _Cargo.lock_ bemerken, die festhält, dass du nun Version 0.8.6 des
Crates `rand` verwendest. Um `rand` in Version 0.999.0 oder eine beliebige
Version der Reihe 0.999._x_ zu verwenden, müsstest du die Datei _Cargo.toml_
stattdessen so ändern (nimm diese Änderung aber nicht wirklich vor, denn die
folgenden Beispiele gehen davon aus, dass du `rand` 0.8 verwendest):

```toml
[dependencies]
rand = "0.999.0"
```

Wenn du das nächste Mal `cargo build` ausführst, aktualisiert Cargo die Registry
der verfügbaren Crates und bewertet deine Anforderungen an `rand` entsprechend
der neuen angegebenen Version neu.

Über [Cargo][doccargo]<!-- ignore --> und
[sein Ökosystem][doccratesio]<!-- ignore --> gäbe es noch viel mehr zu sagen;
darauf gehen wir in Kapitel 14 ein. Vorerst ist das aber alles, was du wissen
musst. Cargo macht es sehr einfach, Bibliotheken wiederzuverwenden, sodass
Rustaceans kleinere Projekte schreiben können, die aus einer Reihe von Paketen
zusammengesetzt sind.

### Eine Zufallszahl erzeugen {#generating-a-random-number}

Fangen wir an, `rand` zu verwenden, um eine Zahl zum Raten zu erzeugen. Der
nächste Schritt ist, _src/main.rs_ zu aktualisieren, wie in Listing 2-3 gezeigt.

<Listing number="2-3" file-name="src/main.rs" caption="Code zum Erzeugen einer Zufallszahl hinzufügen">

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/listing-02-03/src/main.rs:all}}
```

</Listing>

Zuerst fügen wir die Zeile `use rand::Rng;` hinzu. Der Trait `Rng` definiert
Methoden, die Zufallszahlengeneratoren implementieren, und dieser Trait muss im
Gültigkeitsbereich sein, damit wir diese Methoden verwenden können. Kapitel 10
behandelt Traits ausführlich.

Als Nächstes fügen wir in der Mitte zwei Zeilen hinzu. In der ersten Zeile rufen
wir die Funktion `rand::thread_rng` auf, die uns den konkreten
Zufallszahlengenerator liefert, den wir verwenden werden: einen, der lokal zum
aktuellen Ausführungs-Thread ist und vom Betriebssystem initialisiert wird. Dann
rufen wir die Methode `gen_range` auf dem Zufallszahlengenerator auf. Diese
Methode ist durch den Trait `Rng` definiert, den wir mit der Anweisung
`use rand::Rng;` in den Gültigkeitsbereich gebracht haben. Die Methode
`gen_range` nimmt einen Bereichsausdruck als Argument und erzeugt eine
Zufallszahl in diesem Bereich. Die Art von Bereichsausdruck, die wir hier
verwenden, hat die Form `start..=end` und schließt die untere und die obere
Grenze ein, also müssen wir `1..=100` angeben, um eine Zahl zwischen 1 und 100
anzufordern.

> Note: Du weißt nicht einfach so, welche Traits du verwenden und welche
> Methoden und Funktionen eines Crates du aufrufen sollst; deshalb hat jedes
> Crate eine Dokumentation mit Anleitungen zu seiner Verwendung. Ein weiteres
> praktisches Feature von Cargo: Der Befehl `cargo doc
> --open` baut lokal die
> Dokumentation aller deiner Abhängigkeiten und öffnet sie in deinem Browser.
> Wenn dich zum Beispiel weitere Funktionalität des Crates `rand` interessiert,
> führe `cargo doc --open` aus und klicke in der Seitenleiste links auf `rand`.

Die zweite neue Zeile gibt die Geheimzahl aus. Das ist während der Entwicklung
nützlich, um das Programm testen zu können, aber wir löschen sie in der
endgültigen Version. Es ist kein richtiges Spiel, wenn das Programm die Antwort
gleich beim Start ausgibt!

Führe das Programm ein paarmal aus:

<!-- manual-regeneration
cd listings/ch02-guessing-game-tutorial/listing-02-03/
cargo run
4
cargo run
5
-->

```console
$ cargo run
   Compiling guessing_game v0.1.0 (file:///projects/guessing_game)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.02s
     Running `target/debug/guessing_game`
Guess the number!
The secret number is: 7
Please input your guess.
4
You guessed: 4

$ cargo run
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.02s
     Running `target/debug/guessing_game`
Guess the number!
The secret number is: 83
Please input your guess.
5
You guessed: 5
```

Du solltest verschiedene Zufallszahlen bekommen, und alle sollten zwischen 1 und
100 liegen. Gut gemacht!

## Den Tipp mit der Geheimzahl vergleichen {#comparing-the-guess-to-the-secret-number}

Jetzt, da wir eine Benutzereingabe und eine Zufallszahl haben, können wir sie
vergleichen. Dieser Schritt ist in Listing 2-4 gezeigt. Beachte, dass sich
dieser Code noch nicht kompilieren lässt; warum, erklären wir gleich.

<Listing number="2-4" file-name="src/main.rs" caption="Die möglichen Rückgabewerte beim Vergleich zweier Zahlen behandeln">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/listing-02-04/src/main.rs:here}}
```

</Listing>

Zuerst fügen wir eine weitere `use`-Anweisung hinzu, die einen Typ namens
`std::cmp::Ordering` aus der Standardbibliothek in den Gültigkeitsbereich
bringt. Der Typ `Ordering` ist ein weiteres Enum und hat die Varianten `Less`,
`Greater` und `Equal`. Das sind die drei möglichen Ergebnisse, wenn du zwei
Werte vergleichst.

Dann fügen wir unten fünf neue Zeilen hinzu, die den Typ `Ordering` verwenden.
Die Methode `cmp` vergleicht zwei Werte und kann auf allem aufgerufen werden,
was sich vergleichen lässt. Sie nimmt eine Referenz auf das, womit du
vergleichen willst: Hier vergleicht sie `guess` mit `secret_number`. Dann gibt
sie eine Variante des Enums `Ordering` zurück, das wir mit der `use`-Anweisung
in den Gültigkeitsbereich gebracht haben. Wir verwenden einen
[`match`][match]<!-- ignore -->-Ausdruck, um anhand der Variante von `Ordering`,
die der Aufruf von `cmp` mit den Werten in `guess` und `secret_number`
zurückgegeben hat, zu entscheiden, was als Nächstes passiert.

Ein `match`-Ausdruck besteht aus _Armen_. Ein Arm besteht aus einem _Pattern_,
mit dem verglichen wird, und dem Code, der ausgeführt werden soll, wenn der an
`match` übergebene Wert auf das Pattern dieses Arms passt. Rust nimmt den an
`match` übergebenen Wert und geht der Reihe nach die Patterns der Arme durch.
Patterns und das Konstrukt `match` sind mächtige Features von Rust: Mit ihnen
kannst du eine Vielzahl von Situationen ausdrücken, auf die dein Code treffen
kann, und sie stellen sicher, dass du alle behandelst. Diese Features werden in
Kapitel 6 bzw. Kapitel 19 ausführlich behandelt.

Gehen wir ein Beispiel mit dem hier verwendeten `match`-Ausdruck durch.
Angenommen, der Benutzer hat 50 geraten, und die zufällig erzeugte Geheimzahl
ist diesmal 38.

Wenn der Code 50 mit 38 vergleicht, gibt die Methode `cmp` `Ordering::Greater`
zurück, weil 50 größer als 38 ist. Der `match`-Ausdruck erhält den Wert
`Ordering::Greater` und beginnt, die Patterns der einzelnen Arme zu prüfen. Er
sieht sich das Pattern des ersten Arms an, `Ordering::Less`, und stellt fest,
dass der Wert `Ordering::Greater` nicht auf `Ordering::Less` passt; also
ignoriert er den Code in diesem Arm und geht zum nächsten Arm. Das Pattern des
nächsten Arms ist `Ordering::Greater`, und das passt _tatsächlich_ auf
`Ordering::Greater`! Der zugehörige Code in diesem Arm wird ausgeführt und gibt
`Too big!` auf dem Bildschirm aus. Der `match`-Ausdruck endet nach dem ersten
passenden Arm, sieht sich in diesem Szenario den letzten Arm also gar nicht mehr
an.

Der Code in Listing 2-4 lässt sich allerdings noch nicht kompilieren. Probieren
wir es aus:

<!--
The error numbers in this output should be that of the code **WITHOUT** the
anchor or snip comments
-->

```console
{{#include ../listings/ch02-guessing-game-tutorial/listing-02-04/output.txt}}
```

Im Kern besagt der Fehler, dass die Typen nicht zusammenpassen (_mismatched
types_). Rust hat ein starkes, statisches Typsystem. Es hat aber auch
Typinferenz. Als wir `let mut guess = String::new()` geschrieben haben, konnte
Rust ableiten, dass `guess` ein `String` sein sollte, und hat uns den Typ nicht
schreiben lassen. Die `secret_number` dagegen ist ein Zahlentyp. Einige
Zahlentypen von Rust können einen Wert zwischen 1 und 100 haben: `i32`, eine
32-Bit-Zahl; `u32`, eine vorzeichenlose 32-Bit-Zahl; `i64`, eine 64-Bit-Zahl;
und weitere. Wenn nichts anderes angegeben ist, verwendet Rust standardmäßig
`i32`; das ist der Typ von `secret_number`, es sei denn, du fügst an anderer
Stelle Typinformationen hinzu, aufgrund derer Rust einen anderen Zahlentyp
ableitet. Der Grund für den Fehler ist, dass Rust einen String und einen
Zahlentyp nicht vergleichen kann.

Letztlich wollen wir den `String`, den das Programm als Eingabe liest, in einen
Zahlentyp umwandeln, damit wir ihn numerisch mit der Geheimzahl vergleichen
können. Dazu fügen wir diese Zeile in den Rumpf der Funktion `main` ein:

<span class="filename">Dateiname: src/main.rs</span>

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/no-listing-03-convert-string-to-number/src/main.rs:here}}
```

Die Zeile lautet:

```rust,ignore
let guess: u32 = guess.trim().parse().expect("Please type a number!");
```

Wir erzeugen eine Variable namens `guess`. Aber Moment, hat das Programm nicht
schon eine Variable namens `guess`? Hat es, aber praktischerweise erlaubt Rust
uns, den bisherigen Wert von `guess` mit einem neuen zu überschatten. Mit
_Shadowing_ können wir den Variablennamen `guess` wiederverwenden, statt zum
Beispiel zwei verschiedene Variablen wie `guess_str` und `guess` anlegen zu
müssen. Wir behandeln das in [Kapitel 3][shadowing]<!-- ignore -->
ausführlicher; vorerst genügt es zu wissen, dass dieses Feature oft verwendet
wird, wenn du einen Wert von einem Typ in einen anderen umwandeln willst.

Wir binden diese neue Variable an den Ausdruck `guess.trim().parse()`. Das
`guess` im Ausdruck bezieht sich auf die ursprüngliche Variable `guess`, die die
Eingabe als String enthielt. Die Methode `trim` auf einer `String`-Instanz
entfernt alle Leerraumzeichen am Anfang und am Ende; das müssen wir tun, bevor
wir den String in einen `u32` umwandeln können, der nur numerische Daten
enthalten kann. Der Benutzer muss <kbd>enter</kbd> drücken, um `read_line`
zufriedenzustellen und seinen Tipp einzugeben, wodurch dem String ein
Zeilenumbruchzeichen hinzugefügt wird. Wenn der Benutzer zum Beispiel
<kbd>5</kbd> tippt und <kbd>enter</kbd> drückt, sieht `guess` so aus: `5\n`. Das
`\n` steht für „Zeilenumbruch“. (Unter Windows ergibt das Drücken von
<kbd>enter</kbd> einen Wagenrücklauf und einen Zeilenumbruch, `\r\n`.) Die
Methode `trim` entfernt `\n` bzw. `\r\n`, sodass nur `5` übrig bleibt.

Die [Methode `parse` auf Strings][parse]<!-- ignore --> wandelt einen String in
einen anderen Typ um. Hier verwenden wir sie, um einen String in eine Zahl
umzuwandeln. Wir müssen Rust mit `let guess: u32` den genauen Zahlentyp
mitteilen, den wir wollen. Der Doppelpunkt (`:`) nach `guess` sagt Rust, dass
wir den Typ der Variable annotieren. Rust hat einige eingebaute Zahlentypen; der
hier verwendete `u32` ist eine vorzeichenlose 32-Bit-Ganzzahl. Für eine kleine
positive Zahl ist das eine gute Standardwahl. Andere Zahlentypen lernst du in
[Kapitel 3][integers]<!-- ignore --> kennen.

Außerdem bedeuten die Annotation `u32` in diesem Beispielprogramm und der
Vergleich mit `secret_number`, dass Rust ableitet, dass auch `secret_number` ein
`u32` sein sollte. Jetzt findet der Vergleich also zwischen zwei Werten
desselben Typs statt!

Die Methode `parse` funktioniert nur mit Zeichen, die sich logisch in Zahlen
umwandeln lassen, und kann daher leicht Fehler verursachen. Enthielte der String
zum Beispiel `A👍%`, gäbe es keine Möglichkeit, ihn in eine Zahl umzuwandeln.
Weil das fehlschlagen kann, gibt die Methode `parse` einen `Result`-Typ zurück,
ähnlich wie die Methode `read_line` (wie weiter oben in
[„Mögliche Fehler mit `Result` behandeln“](#handling-potential-failure-with-result)<!-- ignore -->
besprochen). Wir behandeln dieses `Result` auf dieselbe Weise, indem wir wieder
die Methode `expect` verwenden. Gibt `parse` die `Result`-Variante `Err` zurück,
weil es aus dem String keine Zahl erzeugen konnte, bringt der Aufruf von
`expect` das Spiel zum Absturz und gibt die Nachricht aus, die wir ihm mitgeben.
Kann `parse` den String erfolgreich in eine Zahl umwandeln, gibt es die Variante
`Ok` von `Result` zurück, und `expect` gibt die gewünschte Zahl aus dem
`Ok`-Wert zurück.

Führen wir das Programm jetzt aus:

<!-- manual-regeneration
cd listings/ch02-guessing-game-tutorial/no-listing-03-convert-string-to-number/
touch src/main.rs
cargo run
  76
-->

```console
$ cargo run
   Compiling guessing_game v0.1.0 (file:///projects/guessing_game)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.26s
     Running `target/debug/guessing_game`
Guess the number!
The secret number is: 58
Please input your guess.
  76
You guessed: 76
Too big!
```

Klasse! Obwohl vor dem Tipp Leerzeichen eingegeben wurden, hat das Programm
trotzdem erkannt, dass der Benutzer 76 geraten hat. Führe das Programm ein
paarmal aus, um das unterschiedliche Verhalten bei verschiedenen Eingaben zu
überprüfen: Rate die Zahl richtig, rate eine zu hohe Zahl und rate eine zu
niedrige Zahl.

Der Großteil des Spiels funktioniert jetzt, aber der Benutzer kann nur einmal
raten. Ändern wir das, indem wir eine Schleife hinzufügen!

## Mehrere Tipps mit einer Schleife ermöglichen {#allowing-multiple-guesses-with-looping}

Das Schlüsselwort `loop` erzeugt eine Endlosschleife. Wir fügen eine Schleife
hinzu, um den Benutzern mehr Möglichkeiten zum Raten der Zahl zu geben:

<span class="filename">Dateiname: src/main.rs</span>

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/no-listing-04-looping/src/main.rs:here}}
```

Wie du siehst, haben wir alles ab der Eingabeaufforderung für den Tipp in eine
Schleife verschoben. Rücke die Zeilen innerhalb der Schleife unbedingt um
jeweils weitere vier Leerzeichen ein und führe das Programm erneut aus. Das
Programm fragt jetzt endlos nach einem weiteren Tipp, was tatsächlich ein neues
Problem mit sich bringt: Anscheinend kann der Benutzer das Spiel nicht beenden!

Der Benutzer könnte das Programm jederzeit mit der Tastenkombination
<kbd>ctrl</kbd>-<kbd>C</kbd> abbrechen. Es gibt aber noch einen anderen Weg,
diesem unersättlichen Monster zu entkommen, wie bei der Besprechung von `parse`
in
[„Den Tipp mit der Geheimzahl vergleichen“](#comparing-the-guess-to-the-secret-number)<!-- ignore -->
erwähnt: Wenn der Benutzer eine Antwort eingibt, die keine Zahl ist, stürzt das
Programm ab. Das können wir nutzen, um dem Benutzer das Beenden zu ermöglichen,
wie hier gezeigt:

<!-- manual-regeneration
cd listings/ch02-guessing-game-tutorial/no-listing-04-looping/
touch src/main.rs
cargo run
(too small guess)
(too big guess)
(correct guess)
quit
-->

```console
$ cargo run
   Compiling guessing_game v0.1.0 (file:///projects/guessing_game)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.23s
     Running `target/debug/guessing_game`
Guess the number!
The secret number is: 59
Please input your guess.
45
You guessed: 45
Too small!
Please input your guess.
60
You guessed: 60
Too big!
Please input your guess.
59
You guessed: 59
You win!
Please input your guess.
quit

thread 'main' panicked at src/main.rs:28:47:
Please type a number!: ParseIntError { kind: InvalidDigit }
note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace
```

Mit `quit` lässt sich das Spiel beenden, aber wie du merkst, auch mit jeder
anderen Eingabe, die keine Zahl ist. Das ist, gelinde gesagt, nicht optimal; wir
wollen, dass das Spiel auch dann endet, wenn die richtige Zahl geraten wurde.

### Nach einem richtigen Tipp beenden {#quitting-after-a-correct-guess}

Programmieren wir das Spiel so, dass es sich beendet, wenn der Benutzer gewinnt,
indem wir eine `break`-Anweisung hinzufügen:

<span class="filename">Dateiname: src/main.rs</span>

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/no-listing-05-quitting/src/main.rs:here}}
```

Mit der Zeile `break` nach `You win!` verlässt das Programm die Schleife, wenn
der Benutzer die Geheimzahl richtig errät. Die Schleife zu verlassen bedeutet
auch, das Programm zu verlassen, weil die Schleife der letzte Teil von `main`
ist.

### Ungültige Eingaben behandeln {#handling-invalid-input}

Um das Verhalten des Spiels weiter zu verfeinern, lassen wir das Programm nicht
abstürzen, wenn der Benutzer etwas eingibt, das keine Zahl ist, sondern lassen
das Spiel solche Eingaben ignorieren, damit der Benutzer weiterraten kann. Dazu
ändern wir die Zeile, in der `guess` von einem `String` in einen `u32`
umgewandelt wird, wie in Listing 2-5 gezeigt.

<Listing number="2-5" file-name="src/main.rs" caption="Einen Tipp, der keine Zahl ist, ignorieren und nach einem neuen Tipp fragen, statt das Programm abstürzen zu lassen">

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/listing-02-05/src/main.rs:here}}
```

</Listing>

Wir wechseln von einem Aufruf von `expect` zu einem `match`-Ausdruck, um bei
einem Fehler nicht mehr abzustürzen, sondern den Fehler zu behandeln. Denk
daran, dass `parse` einen `Result`-Typ zurückgibt und `Result` ein Enum mit den
Varianten `Ok` und `Err` ist. Wir verwenden hier einen `match`-Ausdruck, genau
wie beim `Ordering`-Ergebnis der Methode `cmp`.

Wenn `parse` den String erfolgreich in eine Zahl umwandeln kann, gibt es einen
`Ok`-Wert zurück, der die entstandene Zahl enthält. Dieser `Ok`-Wert passt auf
das Pattern des ersten Arms, und der `match`-Ausdruck gibt einfach den Wert
`num` zurück, den `parse` erzeugt und in den `Ok`-Wert gepackt hat. Diese Zahl
landet genau da, wo wir sie haben wollen: in der neuen Variable `guess`, die wir
erzeugen.

Wenn `parse` den String _nicht_ in eine Zahl umwandeln kann, gibt es einen
`Err`-Wert zurück, der weitere Informationen über den Fehler enthält. Der
`Err`-Wert passt nicht auf das Pattern `Ok(num)` im ersten `match`-Arm, wohl
aber auf das Pattern `Err(_)` im zweiten Arm. Der Unterstrich `_` ist ein
Auffangwert; in diesem Beispiel sagen wir, dass wir auf alle `Err`-Werte passen
wollen, egal welche Informationen sie enthalten. Das Programm führt also den
Code des zweiten Arms aus, `continue`, der das Programm anweist, zur nächsten
Iteration der `loop` zu gehen und nach einem weiteren Tipp zu fragen. Im
Endeffekt ignoriert das Programm also alle Fehler, auf die `parse` stoßen
könnte!

Jetzt sollte im Programm alles wie erwartet funktionieren. Probieren wir es aus:

<!-- manual-regeneration
cd listings/ch02-guessing-game-tutorial/listing-02-05/
cargo run
(too small guess)
(too big guess)
foo
(correct guess)
-->

```console
$ cargo run
   Compiling guessing_game v0.1.0 (file:///projects/guessing_game)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.13s
     Running `target/debug/guessing_game`
Guess the number!
The secret number is: 61
Please input your guess.
10
You guessed: 10
Too small!
Please input your guess.
99
You guessed: 99
Too big!
Please input your guess.
foo
Please input your guess.
61
You guessed: 61
You win!
```

Großartig! Mit einer letzten kleinen Anpassung stellen wir das Ratespiel fertig.
Erinnere dich: Das Programm gibt immer noch die Geheimzahl aus. Das war zum
Testen praktisch, verdirbt aber das Spiel. Löschen wir das `println!`, das die
Geheimzahl ausgibt. Listing 2-6 zeigt den endgültigen Code.

<Listing number="2-6" file-name="src/main.rs" caption="Vollständiger Code des Ratespiels">

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/listing-02-06/src/main.rs}}
```

</Listing>

Damit hast du das Ratespiel erfolgreich gebaut. Herzlichen Glückwunsch!

## Zusammenfassung {#summary}

Dieses Projekt war ein praktischer Weg, dir viele neue Rust-Konzepte
vorzustellen: `let`, `match`, Funktionen, die Verwendung externer Crates und
mehr. In den nächsten Kapiteln lernst du diese Konzepte genauer kennen. Kapitel
3 behandelt Konzepte, die die meisten Programmiersprachen haben, wie Variablen,
Datentypen und Funktionen, und zeigt, wie du sie in Rust verwendest. Kapitel 4
erkundet Ownership, ein Feature, das Rust von anderen Sprachen unterscheidet.
Kapitel 5 behandelt Structs und die Methodensyntax, und Kapitel 6 erklärt, wie
Enums funktionieren.

[prelude]: https://doc.rust-lang.org/std/prelude/index.html
[variables-and-mutability]: ch03-01-variables-and-mutability.html#variables-and-mutability
[comments]: ch03-04-comments.html
[string]: https://doc.rust-lang.org/std/string/struct.String.html
[iostdin]: https://doc.rust-lang.org/std/io/struct.Stdin.html
[read_line]: https://doc.rust-lang.org/std/io/struct.Stdin.html#method.read_line
[result]: https://doc.rust-lang.org/std/result/enum.Result.html
[enums]: ch06-00-enums.html
[expect]: https://doc.rust-lang.org/std/result/enum.Result.html#method.expect
[recover]: ch09-02-recoverable-errors-with-result.html
[randcrate]: https://crates.io/crates/rand
[semver]: http://semver.org
[cratesio]: https://crates.io/
[doccargo]: https://doc.rust-lang.org/cargo/
[doccratesio]: https://doc.rust-lang.org/cargo/reference/publishing.html
[match]: ch06-02-match.html
[shadowing]: ch03-01-variables-and-mutability.html#shadowing
[parse]: https://doc.rust-lang.org/std/primitive.str.html#method.parse
[integers]: ch03-02-data-types.html#integer-types
