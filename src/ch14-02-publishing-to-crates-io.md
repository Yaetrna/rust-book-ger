## Ein Crate auf Crates.io veröffentlichen {#publishing-a-crate-to-cratesio}

Wir haben Pakete von [crates.io](https://crates.io/)<!-- ignore --> als
Abhängigkeiten unseres Projekts verwendet, aber du kannst deinen Code auch mit
anderen teilen, indem du deine eigenen Pakete veröffentlichst. Die
Crate-Registry auf [crates.io](https://crates.io/)<!-- ignore --> verteilt den
Quellcode deiner Pakete, daher hostet sie in erster Linie Open-Source-Code.

Rust und Cargo haben Features, die es anderen erleichtern, dein veröffentlichtes
Paket zu finden und zu verwenden. Einige dieser Features besprechen wir als
Nächstes, und dann erklären wir, wie man ein Paket veröffentlicht.

### Nützliche Dokumentationskommentare schreiben {#making-useful-documentation-comments}

Deine Pakete genau zu dokumentieren, hilft anderen Nutzern zu verstehen, wie und
wann sie sie verwenden sollen, daher lohnt es sich, Zeit in das Schreiben von
Dokumentation zu investieren. In Kapitel 3 haben wir besprochen, wie man
Rust-Code mit zwei Schrägstrichen, `//`, kommentiert. Rust hat außerdem eine
besondere Art von Kommentar für Dokumentation, praktischerweise
_Dokumentationskommentar_ (_documentation comment_) genannt, aus dem
HTML-Dokumentation erzeugt wird. Das HTML zeigt den Inhalt der
Dokumentationskommentare für Elemente der öffentlichen API an und richtet sich
an Programmierende, die wissen wollen, wie man dein Crate _verwendet_, und
nicht, wie dein Crate _implementiert_ ist.

Dokumentationskommentare verwenden drei Schrägstriche, `///`, statt zwei und
unterstützen Markdown-Notation zum Formatieren des Textes. Setze
Dokumentationskommentare direkt vor das Element, das sie dokumentieren. Listing
14-1 zeigt Dokumentationskommentare für eine Funktion `add_one` in einem Crate
namens `my_crate`.

<Listing number="14-1" file-name="src/lib.rs" caption="Ein Dokumentationskommentar für eine Funktion">

```rust,ignore
{{#rustdoc_include ../listings/ch14-more-about-cargo/listing-14-01/src/lib.rs}}
```

</Listing>

Hier beschreiben wir, was die Funktion `add_one` tut, beginnen einen Abschnitt
mit der Überschrift `Examples` und geben dann Code an, der zeigt, wie man die
Funktion `add_one` verwendet. Aus diesem Dokumentationskommentar können wir mit
`cargo doc` die HTML-Dokumentation erzeugen. Dieser Befehl führt das mit Rust
ausgelieferte Werkzeug `rustdoc` aus und legt die erzeugte HTML-Dokumentation im
Verzeichnis _target/doc_ ab.

Bequemerweise baut `cargo doc --open` das HTML für die Dokumentation deines
aktuellen Crates (sowie die Dokumentation aller Abhängigkeiten deines Crates)
und öffnet das Ergebnis in einem Webbrowser. Navigiere zur Funktion `add_one`,
und du siehst, wie der Text in den Dokumentationskommentaren dargestellt wird,
wie in Abbildung 14-1 gezeigt.

<img alt="Gerenderte HTML-Dokumentation für die Funktion `add_one` von `my_crate`" src="img/trpl14-01.png" class="center" />

<span class="caption">Abbildung 14-1: Die HTML-Dokumentation für die Funktion
`add_one`</span>

#### Häufig verwendete Abschnitte {#commonly-used-sections}

Wir haben in Listing 14-1 die Markdown-Überschrift `# Examples` verwendet, um im
HTML einen Abschnitt mit dem Titel „Examples“ zu erzeugen. Hier sind einige
andere Abschnitte, die Crate-Autoren häufig in ihrer Dokumentation verwenden:

- **Panics**: Die Szenarien, in denen die dokumentierte Funktion einen Panic
  auslösen könnte. Aufrufer der Funktion, deren Programme keinen Panic auslösen
  sollen, sollten sicherstellen, dass sie die Funktion in diesen Situationen
  nicht aufrufen.
- **Errors**: Gibt die Funktion ein `Result` zurück, kann es für Aufrufer
  hilfreich sein, die Arten von Fehlern zu beschreiben, die auftreten können,
  und unter welchen Bedingungen diese Fehler zurückgegeben werden, damit sie
  Code schreiben können, der die verschiedenen Arten von Fehlern unterschiedlich
  behandelt.
- **Safety**: Ist der Aufruf der Funktion `unsafe` (unsicheren Code besprechen
  wir in Kapitel 20), sollte es einen Abschnitt geben, der erklärt, warum die
  Funktion unsicher ist, und die Invarianten behandelt, deren Einhaltung die
  Funktion von ihren Aufrufern erwartet.

Die meisten Dokumentationskommentare brauchen nicht alle diese Abschnitte, aber
diese Checkliste erinnert dich an die Aspekte deines Codes, die Nutzer
interessieren werden.

#### Dokumentationskommentare als Tests {#documentation-comments-as-tests}

Beispiel-Codeblöcke in deinen Dokumentationskommentaren können zeigen, wie man
deine Bibliothek verwendet, und haben einen zusätzlichen Vorteil: `cargo test`
führt die Codebeispiele in deiner Dokumentation als Tests aus! Nichts ist besser
als Dokumentation mit Beispielen. Aber nichts ist schlimmer als Beispiele, die
nicht funktionieren, weil sich der Code geändert hat, seit die Dokumentation
geschrieben wurde. Führen wir `cargo test` mit der Dokumentation für die
Funktion `add_one` aus Listing 14-1 aus, sehen wir in den Testergebnissen einen
Abschnitt, der so aussieht:

<!-- manual-regeneration
cd listings/ch14-more-about-cargo/listing-14-01/
cargo test
copy just the doc-tests section below
-->

```text
   Doc-tests my_crate

running 1 test
test src/lib.rs - add_one (line 5) ... ok

test result: ok. 1 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.27s
```

Ändern wir nun entweder die Funktion oder das Beispiel so, dass das `assert_eq!`
im Beispiel einen Panic auslöst, und führen `cargo test` erneut aus, sehen wir,
dass die Dokumentationstests erkennen, dass Beispiel und Code nicht mehr
zueinander passen!

<!-- Old headings. Do not remove or links may break. -->

<a id="commenting-contained-items"></a>

#### Kommentare für umschließende Elemente {#contained-item-comments}

Die Art von Dokumentationskommentar `//!` fügt die Dokumentation dem Element
hinzu, das die Kommentare _enthält_, statt den Elementen, die den Kommentaren
_folgen_. Diese Dokumentationskommentare verwenden wir typischerweise in der
Crate-Root-Datei (Wurzeldatei des Crates, nach Konvention _src/lib.rs_) oder in
einem Modul, um das Crate oder das Modul als Ganzes zu dokumentieren.

Um zum Beispiel Dokumentation hinzuzufügen, die den Zweck des Crates `my_crate`
beschreibt, das die Funktion `add_one` enthält, fügen wir am Anfang der Datei
_src/lib.rs_ Dokumentationskommentare hinzu, die mit `//!` beginnen, wie in
Listing 14-2 gezeigt.

<Listing number="14-2" file-name="src/lib.rs" caption="Die Dokumentation für das Crate `my_crate` als Ganzes">

```rust,ignore
{{#rustdoc_include ../listings/ch14-more-about-cargo/listing-14-02/src/lib.rs:here}}
```

</Listing>

Beachte, dass nach der letzten Zeile, die mit `//!` beginnt, kein Code steht. Da
wir die Kommentare mit `//!` statt mit `///` begonnen haben, dokumentieren wir
das Element, das diesen Kommentar enthält, und nicht ein Element, das auf diesen
Kommentar folgt. In diesem Fall ist dieses Element die Datei _src/lib.rs_, also
die Crate-Root. Diese Kommentare beschreiben das gesamte Crate.

Wenn wir `cargo doc --open` ausführen, erscheinen diese Kommentare auf der
Startseite der Dokumentation für `my_crate` oberhalb der Liste der öffentlichen
Elemente im Crate, wie in Abbildung 14-2 gezeigt.

Dokumentationskommentare innerhalb von Elementen sind besonders nützlich, um
Crates und Module zu beschreiben. Erkläre damit den übergeordneten Zweck des
Containers, damit deine Nutzer die Organisation des Crates verstehen.

<img alt="Gerenderte HTML-Dokumentation mit einem Kommentar für das Crate als Ganzes" src="img/trpl14-02.png" class="center" />

<span class="caption">Abbildung 14-2: Die gerenderte Dokumentation für
`my_crate`, einschließlich des Kommentars, der das Crate als Ganzes
beschreibt</span>

{{#quiz ../quizzes/ch14-02-publishing-to-crates-io-sec1.toml}}

<!-- Old headings. Do not remove or links may break. -->

<a id="exporting-a-convenient-public-api-with-pub-use"></a>

### Eine bequeme öffentliche API exportieren {#exporting-a-convenient-public-api}

Die Struktur deiner öffentlichen API ist ein wichtiger Gesichtspunkt beim
Veröffentlichen eines Crates. Wer dein Crate verwendet, kennt die Struktur
weniger gut als du und hat vielleicht Schwierigkeiten, die gesuchten Teile zu
finden, wenn dein Crate eine große Modulhierarchie hat.

In Kapitel 7 haben wir behandelt, wie man Elemente mit dem Schlüsselwort `pub`
öffentlich macht und wie man Elemente mit dem Schlüsselwort `use` in einen
Gültigkeitsbereich (_scope_) bringt. Die Struktur, die für dich bei der
Entwicklung eines Crates sinnvoll ist, ist für deine Nutzer aber vielleicht
nicht sehr bequem. Vielleicht möchtest du deine Structs in einer Hierarchie mit
mehreren Ebenen organisieren, aber dann haben Leute, die einen Typ verwenden
wollen, den du tief in der Hierarchie definiert hast, vielleicht Schwierigkeiten
herauszufinden, dass dieser Typ existiert. Außerdem ärgert es sie vielleicht,
`use
my_crate::some_module::another_module::UsefulType;` statt
`use
my_crate::UsefulType;` eingeben zu müssen.

Die gute Nachricht: Wenn die Struktur für andere aus einer anderen Bibliothek
heraus _nicht_ bequem zu verwenden ist, musst du deine interne Organisation
nicht umbauen: Stattdessen kannst du Elemente mit `pub use` reexportieren, um
eine öffentliche Struktur zu schaffen, die sich von deiner privaten Struktur
unterscheidet. _Reexportieren_ (_re-exporting_) nimmt ein öffentliches Element
an einer Stelle und macht es an einer anderen Stelle öffentlich, als wäre es
stattdessen dort definiert.

Angenommen, wir haben eine Bibliothek namens `art` geschrieben, um künstlerische
Konzepte zu modellieren. In dieser Bibliothek gibt es zwei Module: ein Modul
`kinds` mit zwei Enums namens `PrimaryColor` und `SecondaryColor` und ein Modul
`utils` mit einer Funktion namens `mix`, wie in Listing 14-3 gezeigt.

<Listing number="14-3" file-name="src/lib.rs" caption="Eine Bibliothek `art` mit Elementen, die in den Modulen `kinds` und `utils` organisiert sind">

```rust,noplayground,test_harness
{{#rustdoc_include ../listings/ch14-more-about-cargo/listing-14-03/src/lib.rs:here}}
```

</Listing>

Abbildung 14-3 zeigt, wie die von `cargo doc` erzeugte Startseite der
Dokumentation für dieses Crate aussähe.

<img alt="Gerenderte Dokumentation für das Crate `art`, die die Module `kinds` und `utils` auflistet" src="img/trpl14-03.png" class="center" />

<span class="caption">Abbildung 14-3: Die Startseite der Dokumentation für
`art`, die die Module `kinds` und `utils` auflistet</span>

Beachte, dass die Typen `PrimaryColor` und `SecondaryColor` nicht auf der
Startseite aufgeführt sind, ebenso wenig die Funktion `mix`. Wir müssen auf
`kinds` und `utils` klicken, um sie zu sehen.

Ein anderes Crate, das von dieser Bibliothek abhängt, bräuchte
`use`-Anweisungen, die die Elemente aus `art` in den Gültigkeitsbereich bringen
und dabei die derzeit definierte Modulstruktur angeben. Listing 14-4 zeigt ein
Beispiel für ein Crate, das die Elemente `PrimaryColor` und `mix` aus dem Crate
`art` verwendet.

<Listing number="14-4" file-name="src/main.rs" caption="Ein Crate, das die Elemente des Crates `art` mit dessen exportierter interner Struktur verwendet">

```rust,ignore
{{#rustdoc_include ../listings/ch14-more-about-cargo/listing-14-04/src/main.rs}}
```

</Listing>

Wer den Code in Listing 14-4 geschrieben hat, der das Crate `art` verwendet,
musste herausfinden, dass `PrimaryColor` im Modul `kinds` und `mix` im Modul
`utils` liegt. Die Modulstruktur des Crates `art` ist für die Entwickler, die am
Crate `art` arbeiten, relevanter als für diejenigen, die es verwenden. Die
interne Struktur enthält keine nützlichen Informationen für jemanden, der
verstehen will, wie man das Crate `art` verwendet, sondern sorgt eher für
Verwirrung, weil Entwickler, die es verwenden, herausfinden müssen, wo sie
suchen müssen, und die Modulnamen in den `use`-Anweisungen angeben müssen.

Um die interne Organisation aus der öffentlichen API zu entfernen, können wir
den Code des Crates `art` aus Listing 14-3 ändern und `pub use`-Anweisungen
hinzufügen, die die Elemente auf oberster Ebene reexportieren, wie in Listing
14-5 gezeigt.

<Listing number="14-5" file-name="src/lib.rs" caption="`pub use`-Anweisungen hinzufügen, um Elemente zu reexportieren">

```rust,ignore
{{#rustdoc_include ../listings/ch14-more-about-cargo/listing-14-05/src/lib.rs:here}}
```

</Listing>

Die API-Dokumentation, die `cargo doc` für dieses Crate erzeugt, listet die
Re-Exporte jetzt auf der Startseite auf und verlinkt sie, wie in Abbildung 14-4
gezeigt, sodass die Typen `PrimaryColor` und `SecondaryColor` und die Funktion
`mix` leichter zu finden sind.

<img alt="Gerenderte Dokumentation für das Crate `art` mit den Re-Exporten auf der Startseite" src="img/trpl14-04.png" class="center" />

<span class="caption">Abbildung 14-4: Die Startseite der Dokumentation für
`art`, die die Re-Exporte auflistet</span>

Die Nutzer des Crates `art` können weiterhin die interne Struktur aus Listing
14-3 sehen und verwenden, wie in Listing 14-4 gezeigt, oder sie können die
bequemere Struktur aus Listing 14-5 verwenden, wie in Listing 14-6 gezeigt.

<Listing number="14-6" file-name="src/main.rs" caption="Ein Programm, das die reexportierten Elemente aus dem Crate `art` verwendet">

```rust,ignore
{{#rustdoc_include ../listings/ch14-more-about-cargo/listing-14-06/src/main.rs:here}}
```

</Listing>

Wenn es viele verschachtelte Module gibt, kann das Reexportieren der Typen auf
oberster Ebene mit `pub use` einen erheblichen Unterschied für die Erfahrung der
Leute machen, die das Crate verwenden. Eine weitere häufige Verwendung von
`pub use` ist, Definitionen einer Abhängigkeit im aktuellen Crate zu
reexportieren, um die Definitionen dieses Crates zum Teil der öffentlichen API
deines Crates zu machen.

Eine nützliche Struktur für eine öffentliche API zu schaffen, ist eher eine
Kunst als eine Wissenschaft, und du kannst schrittweise die API finden, die für
deine Nutzer am besten funktioniert. `pub use` gibt dir Flexibilität bei der
internen Strukturierung deines Crates und entkoppelt diese interne Struktur von
dem, was du deinen Nutzern präsentierst. Sieh dir den Code einiger Crates an,
die du installiert hast, um zu sehen, ob sich ihre interne Struktur von ihrer
öffentlichen API unterscheidet.

### Ein Konto auf Crates.io einrichten {#setting-up-a-cratesio-account}

Bevor du Crates veröffentlichen kannst, musst du ein Konto auf
[crates.io](https://crates.io/)<!-- ignore --> anlegen und ein API-Token
erhalten. Besuche dazu die Startseite auf
[crates.io](https://crates.io/)<!-- ignore --> und melde dich über ein
GitHub-Konto an. (Ein GitHub-Konto ist derzeit Voraussetzung, aber die Website
könnte künftig andere Möglichkeiten unterstützen, ein Konto anzulegen.) Sobald
du angemeldet bist, besuche deine Kontoeinstellungen unter
[https://crates.io/me/](https://crates.io/me/)<!-- ignore --> und hol dir deinen
API-Schlüssel. Führe dann den Befehl `cargo login` aus und füge deinen
API-Schlüssel ein, wenn du dazu aufgefordert wirst, etwa so:

```console
$ cargo login
abcdefghijklmnopqrstuvwxyz012345
```

Dieser Befehl teilt Cargo dein API-Token mit und speichert es lokal in
_~/.cargo/credentials.toml_. Beachte, dass dieses Token geheim ist: Gib es an
niemanden weiter. Falls du es aus irgendeinem Grund doch mit jemandem teilst,
solltest du es widerrufen und auf [crates.io](https://crates.io/)<!-- ignore
--> ein neues Token erzeugen.

### Einem neuen Crate Metadaten hinzufügen {#adding-metadata-to-a-new-crate}

Angenommen, du hast ein Crate, das du veröffentlichen willst. Vor dem
Veröffentlichen musst du im Abschnitt `[package]` der Datei _Cargo.toml_ des
Crates einige Metadaten hinzufügen.

Dein Crate braucht einen eindeutigen Namen. Solange du lokal an einem Crate
arbeitest, kannst du es nennen, wie du willst. Crate-Namen auf
[crates.io](https://crates.io/)<!-- ignore --> werden aber nach dem Prinzip „Wer
zuerst kommt, mahlt zuerst“ vergeben. Sobald ein Crate-Name vergeben ist, kann
niemand sonst ein Crate mit diesem Namen veröffentlichen. Bevor du versuchst,
ein Crate zu veröffentlichen, suche nach dem Namen, den du verwenden willst. Ist
der Name bereits vergeben, musst du einen anderen Namen finden und das Feld
`name` in der Datei _Cargo.toml_ im Abschnitt `[package]` so ändern, dass der
neue Name für die Veröffentlichung verwendet wird, etwa so:

<span class="filename">Dateiname: Cargo.toml</span>

```toml
[package]
name = "guessing_game"
```

Selbst wenn du einen eindeutigen Namen gewählt hast, bekommst du, wenn du an
dieser Stelle `cargo publish` ausführst, um das Crate zu veröffentlichen, eine
Warnung und dann einen Fehler:

<!-- manual-regeneration
Create a new package with an unregistered name, making no further modifications
  to the generated package, so it is missing the description and license fields.
cargo publish
copy just the relevant lines below
-->

```console
$ cargo publish
    Updating crates.io index
warning: manifest has no description, license, license-file, documentation, homepage or repository.
See https://doc.rust-lang.org/cargo/reference/manifest.html#package-metadata for more info.
--snip--
error: failed to publish to registry at https://crates.io

Caused by:
  the remote server responded with an error (status 400 Bad Request): missing or empty metadata fields: description, license. Please see https://doc.rust-lang.org/cargo/reference/manifest.html for more information on configuring these fields
```

Das führt zu einem Fehler, weil dir einige wichtige Informationen fehlen: Eine
Beschreibung und eine Lizenz sind erforderlich, damit andere wissen, was dein
Crate tut und unter welchen Bedingungen sie es verwenden dürfen. Füge in
_Cargo.toml_ eine Beschreibung hinzu, die nur aus ein oder zwei Sätzen besteht,
weil sie zusammen mit deinem Crate in Suchergebnissen erscheint. Für das Feld
`license` musst du einen _Lizenzbezeichner_ (_license identifier value_)
angeben. Die [Software Package Data Exchange (SPDX) der Linux Foundation][spdx]
listet die Bezeichner auf, die du für diesen Wert verwenden kannst. Um zum
Beispiel anzugeben, dass du dein Crate unter der MIT-Lizenz lizenziert hast,
füge den Bezeichner `MIT` hinzu:

<span class="filename">Dateiname: Cargo.toml</span>

```toml
[package]
name = "guessing_game"
license = "MIT"
```

Willst du eine Lizenz verwenden, die nicht in der SPDX vorkommt, musst du den
Text dieser Lizenz in eine Datei schreiben, die Datei in dein Projekt aufnehmen
und dann mit `license-file` den Namen dieser Datei angeben, statt den Schlüssel
`license` zu verwenden.

Eine Beratung dazu, welche Lizenz für dein Projekt angemessen ist, geht über den
Rahmen dieses Buchs hinaus. Viele Leute in der Rust-Community lizenzieren ihre
Projekte auf dieselbe Weise wie Rust, nämlich mit der Doppellizenz
`MIT OR Apache-2.0`. Diese Praxis zeigt, dass du auch mehrere Lizenzbezeichner,
getrennt durch `OR`, angeben kannst, um mehrere Lizenzen für dein Projekt zu
haben.

Mit einem eindeutigen Namen, der Version, deiner Beschreibung und einer Lizenz
könnte die Datei _Cargo.toml_ für ein Projekt, das zur Veröffentlichung bereit
ist, so aussehen:

<span class="filename">Dateiname: Cargo.toml</span>

```toml
[package]
name = "guessing_game"
version = "0.1.0"
edition = "2024"
description = "A fun game where you guess what number the computer has chosen."
license = "MIT OR Apache-2.0"

[dependencies]
```

[Die Dokumentation von Cargo](https://doc.rust-lang.org/cargo/) beschreibt
weitere Metadaten, die du angeben kannst, damit andere dein Crate leichter
finden und verwenden können.

### Auf Crates.io veröffentlichen {#publishing-to-cratesio}

Nachdem du ein Konto angelegt, dein API-Token gespeichert, einen Namen für dein
Crate gewählt und die erforderlichen Metadaten angegeben hast, bist du bereit
zum Veröffentlichen! Beim Veröffentlichen eines Crates wird eine bestimmte
Version auf [crates.io](https://crates.io/)<!-- ignore --> hochgeladen, damit
andere sie verwenden können.

Sei vorsichtig, denn eine Veröffentlichung ist _dauerhaft_. Die Version kann nie
überschrieben werden, und der Code kann außer unter bestimmten Umständen nicht
gelöscht werden. Ein wichtiges Ziel von Crates.io ist es, als dauerhaftes Archiv
von Code zu dienen, damit die Builds aller Projekte, die von Crates auf
[crates.io](https://crates.io/)<!-- ignore --> abhängen, weiterhin
funktionieren. Das Löschen von Versionen zu erlauben, würde es unmöglich machen,
dieses Ziel zu erreichen. Die Zahl der Crate-Versionen, die du veröffentlichen
kannst, ist aber nicht begrenzt.

Führe den Befehl `cargo publish` erneut aus. Jetzt sollte er erfolgreich sein:

<!-- manual-regeneration
go to some valid crate, publish a new version
cargo publish
copy just the relevant lines below
-->

```console
$ cargo publish
    Updating crates.io index
   Packaging guessing_game v0.1.0 (file:///projects/guessing_game)
    Packaged 6 files, 1.2KiB (895.0B compressed)
   Verifying guessing_game v0.1.0 (file:///projects/guessing_game)
   Compiling guessing_game v0.1.0
(file:///projects/guessing_game/target/package/guessing_game-0.1.0)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.19s
   Uploading guessing_game v0.1.0 (file:///projects/guessing_game)
    Uploaded guessing_game v0.1.0 to registry `crates-io`
note: waiting for `guessing_game v0.1.0` to be available at registry
`crates-io`.
You may press ctrl-c to skip waiting; the crate should be available shortly.
   Published guessing_game v0.1.0 at registry `crates-io`
```

Herzlichen Glückwunsch! Du hast deinen Code jetzt mit der Rust-Community
geteilt, und jeder kann dein Crate ganz einfach als Abhängigkeit zu seinem
Projekt hinzufügen.

### Eine neue Version eines bestehenden Crates veröffentlichen {#publishing-a-new-version-of-an-existing-crate}

Wenn du Änderungen an deinem Crate vorgenommen hast und bereit bist, eine neue
Version zu veröffentlichen, änderst du den Wert `version` in deiner Datei
_Cargo.toml_ und veröffentlichst erneut. Entscheide anhand der
[Regeln der semantischen Versionierung][semver] und der Art deiner Änderungen,
welche nächste Versionsnummer angemessen ist. Führe dann `cargo publish` aus, um
die neue Version hochzuladen.

<!-- Old headings. Do not remove or links may break. -->

<a id="removing-versions-from-cratesio-with-cargo-yank"></a>
<a id="deprecating-versions-from-cratesio-with-cargo-yank"></a>

### Versionen auf Crates.io als veraltet kennzeichnen {#deprecating-versions-from-cratesio}

Du kannst frühere Versionen eines Crates zwar nicht entfernen, aber verhindern,
dass künftige Projekte sie als neue Abhängigkeit hinzufügen. Das ist nützlich,
wenn eine Crate-Version aus irgendeinem Grund fehlerhaft ist. In solchen
Situationen unterstützt Cargo das Zurückziehen (_yanking_) einer Crate-Version.

Das _Zurückziehen_ einer Version verhindert, dass neue Projekte von dieser
Version abhängen, während alle bestehenden Projekte, die davon abhängen,
weiterlaufen können. Im Wesentlichen bedeutet ein Yank, dass alle Projekte mit
einer _Cargo.lock_ nicht kaputtgehen und alle künftig erzeugten
_Cargo.lock_-Dateien die zurückgezogene Version nicht verwenden.

Um eine Version eines Crates zurückzuziehen, führe im Verzeichnis des Crates,
das du zuvor veröffentlicht hast, `cargo yank` aus und gib an, welche Version du
zurückziehen willst. Haben wir zum Beispiel ein Crate namens `guessing_game` in
Version 1.0.1 veröffentlicht und wollen es zurückziehen, würden wir im
Projektverzeichnis von `guessing_game` Folgendes ausführen:

<!-- manual-regeneration:
cargo yank carol-test --version 2.1.0
cargo yank carol-test --version 2.1.0 --undo
-->

```console
$ cargo yank --vers 1.0.1
    Updating crates.io index
        Yank guessing_game@1.0.1
```

Indem du dem Befehl `--undo` hinzufügst, kannst du ein Zurückziehen auch
rückgängig machen und Projekten wieder erlauben, von einer Version abzuhängen:

```console
$ cargo yank --vers 1.0.1 --undo
    Updating crates.io index
      Unyank guessing_game@1.0.1
```

Ein Yank löscht _keinen_ Code. Er kann zum Beispiel keine versehentlich
hochgeladenen Geheimnisse löschen. Passiert das, musst du diese Geheimnisse
sofort zurücksetzen.

{{#quiz ../quizzes/ch14-02-publishing-to-crates-io-sec2.toml}}

[spdx]: https://spdx.org/licenses/
[semver]: https://semver.org/
