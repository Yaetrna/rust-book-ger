## Hello, Cargo!

Cargo ist das Build-System und der Paketmanager von Rust. Die meisten Rustaceans
verwalten ihre Rust-Projekte mit diesem Werkzeug, weil Cargo dir viele Aufgaben
abnimmt, etwa das Bauen deines Codes, das Herunterladen der Bibliotheken, von
denen dein Code abhängt, und das Bauen dieser Bibliotheken. (Die Bibliotheken,
die dein Code braucht, nennen wir _Abhängigkeiten_.)

Die einfachsten Rust-Programme, wie das, das wir bisher geschrieben haben, haben
keine Abhängigkeiten. Hätten wir das Projekt „Hello, world!“ mit Cargo gebaut,
würde es nur den Teil von Cargo nutzen, der für das Bauen deines Codes zuständig
ist. Wenn du komplexere Rust-Programme schreibst, fügst du Abhängigkeiten hinzu,
und wenn du ein Projekt mit Cargo beginnst, geht das Hinzufügen von
Abhängigkeiten viel leichter.

Da die überwiegende Mehrheit der Rust-Projekte Cargo verwendet, geht der Rest
dieses Buchs davon aus, dass du ebenfalls Cargo verwendest. Cargo wird mit Rust
installiert, wenn du die offiziellen Installationsprogramme aus dem Abschnitt
[„Installation“][installation]<!-- ignore --> verwendet hast. Wenn du Rust auf
anderem Weg installiert hast, prüfe, ob Cargo installiert ist, indem du
Folgendes in dein Terminal eingibst:

```console
$ cargo --version
```

Wenn du eine Versionsnummer siehst, ist es installiert! Wenn du einen Fehler wie
`command
not found` siehst, schau in der Dokumentation deiner
Installationsmethode nach, wie du Cargo separat installierst.

### Ein Projekt mit Cargo erstellen {#creating-a-project-with-cargo}

Lass uns mit Cargo ein neues Projekt erstellen und uns ansehen, wie es sich von
unserem ursprünglichen Projekt „Hello, world!“ unterscheidet. Wechsle zurück in
dein Verzeichnis _projects_ (oder wo auch immer du deinen Code speichern
wolltest). Führe dann, auf jedem Betriebssystem, Folgendes aus:

```console
$ cargo new hello_cargo
$ cd hello_cargo
```

Der erste Befehl erstellt ein neues Verzeichnis und Projekt namens
_hello_cargo_. Wir haben unser Projekt _hello_cargo_ genannt, und Cargo legt
seine Dateien in einem gleichnamigen Verzeichnis an.

Wechsle in das Verzeichnis _hello_cargo_ und lass dir die Dateien anzeigen. Du
siehst, dass Cargo zwei Dateien und ein Verzeichnis für uns erzeugt hat: eine
Datei _Cargo.toml_ und ein Verzeichnis _src_ mit einer Datei _main.rs_ darin.

Außerdem hat es ein neues Git-Repository samt einer Datei _.gitignore_
initialisiert. Git-Dateien werden nicht erzeugt, wenn du `cargo new` innerhalb
eines bestehenden Git-Repositorys ausführst; dieses Verhalten kannst du mit
`cargo new --vcs=git` übersteuern.

> Note: Git ist ein verbreitetes Versionskontrollsystem. Mit dem Flag `--vcs`
> kannst du `cargo new` anweisen, ein anderes oder gar kein
> Versionskontrollsystem zu verwenden. Führe `cargo new --help` aus, um die
> verfügbaren Optionen zu sehen.

Öffne _Cargo.toml_ in einem Texteditor deiner Wahl. Die Datei sollte ähnlich wie
der Code in Listing 1-2 aussehen.

<Listing number="1-2" file-name="Cargo.toml" caption="Inhalt der von `cargo new` erzeugten *Cargo.toml*">

```toml
[package]
name = "hello_cargo"
version = "0.1.0"
edition = "2024"

[dependencies]
```

</Listing>

Diese Datei liegt im Format [_TOML_][toml]<!-- ignore --> (_Tom’s Obvious,
Minimal Language_) vor, dem Konfigurationsformat von Cargo.

Die erste Zeile, `[package]`, ist eine Abschnittsüberschrift, die anzeigt, dass
die folgenden Anweisungen ein Paket konfigurieren. Wenn wir dieser Datei weitere
Informationen hinzufügen, kommen weitere Abschnitte dazu.

Die nächsten drei Zeilen legen die Konfigurationsinformationen fest, die Cargo
zum Kompilieren deines Programms braucht: den Namen, die Version und die zu
verwendende Rust-Edition. Über den Schlüssel `edition` sprechen wir in
[Anhang E][appendix-e]<!-- ignore -->.

Die letzte Zeile, `[dependencies]`, leitet einen Abschnitt ein, in dem du die
Abhängigkeiten deines Projekts aufführst. In Rust nennt man Code-Pakete
_Crates_. Für dieses Projekt brauchen wir keine weiteren Crates, für das erste
Projekt in Kapitel 2 aber schon; dann verwenden wir diesen Abschnitt für
Abhängigkeiten.

Öffne nun _src/main.rs_ und sieh es dir an:

<span class="filename">Dateiname: src/main.rs</span>

```rust
fn main() {
    println!("Hello, world!");
}
```

Cargo hat für dich ein „Hello, world!“-Programm erzeugt, genau wie das, das wir
in Listing 1-1 geschrieben haben! Bisher unterscheiden sich unser Projekt und
das von Cargo erzeugte Projekt darin, dass Cargo den Code in das Verzeichnis
_src_ gelegt hat und dass wir im obersten Verzeichnis eine Konfigurationsdatei
_Cargo.toml_ haben.

Cargo erwartet, dass deine Quelldateien im Verzeichnis _src_ liegen. Das oberste
Projektverzeichnis ist nur für README-Dateien, Lizenzinformationen,
Konfigurationsdateien und alles andere gedacht, was nichts mit deinem Code zu
tun hat. Cargo hilft dir, deine Projekte zu organisieren. Alles hat seinen
Platz, und alles ist an seinem Platz.

Wenn du ein Projekt ohne Cargo begonnen hast, wie wir es beim Projekt „Hello,
world!“ getan haben, kannst du es in ein Projekt umwandeln, das Cargo verwendet.
Verschiebe den Projektcode in das Verzeichnis _src_ und lege eine passende Datei
_Cargo.toml_ an. Eine einfache Möglichkeit, an diese Datei _Cargo.toml_ zu
kommen, ist `cargo init`; der Befehl erzeugt sie automatisch für dich.

### Ein Cargo-Projekt bauen und ausführen {#building-and-running-a-cargo-project}

Sehen wir uns nun an, was anders ist, wenn wir das Programm „Hello, world!“ mit
Cargo bauen und ausführen! Baue dein Projekt aus deinem Verzeichnis
_hello_cargo_ heraus, indem du folgenden Befehl eingibst:

```console
$ cargo build
   Compiling hello_cargo v0.1.0 (file:///projects/hello_cargo)
    Finished dev [unoptimized + debuginfo] target(s) in 2.85 secs
```

Dieser Befehl erzeugt eine ausführbare Datei in _target/debug/hello_cargo_
(unter Windows _target\debug\hello_cargo.exe_) statt in deinem aktuellen
Verzeichnis. Weil standardmäßig ein Debug-Build erstellt wird, legt Cargo die
Binärdatei in einem Verzeichnis namens _debug_ ab. Du kannst die ausführbare
Datei mit diesem Befehl ausführen:

```console
$ ./target/debug/hello_cargo # or .\target\debug\hello_cargo.exe on Windows
Hello, world!
```

Wenn alles klappt, sollte `Hello, world!` im Terminal ausgegeben werden. Wenn du
`cargo
build` zum ersten Mal ausführst, legt Cargo außerdem im obersten
Verzeichnis eine neue Datei an: _Cargo.lock_. Diese Datei hält die genauen
Versionen der Abhängigkeiten in deinem Projekt fest. Dieses Projekt hat keine
Abhängigkeiten, daher ist die Datei recht spärlich. Du wirst diese Datei nie von
Hand ändern müssen; Cargo verwaltet ihren Inhalt für dich.

Wir haben gerade ein Projekt mit `cargo build` gebaut und mit
`./target/debug/hello_cargo` ausgeführt, wir können aber auch `cargo run`
verwenden, um den Code zu kompilieren und die entstandene ausführbare Datei
anschließend auszuführen, alles mit einem einzigen Befehl:

```console
$ cargo run
    Finished dev [unoptimized + debuginfo] target(s) in 0.0 secs
     Running `target/debug/hello_cargo`
Hello, world!
```

`cargo run` ist bequemer, als daran denken zu müssen, `cargo
build` auszuführen
und dann den ganzen Pfad zur Binärdatei zu verwenden; deshalb verwenden die
meisten Entwicklerinnen und Entwickler `cargo
run`.

Beachte, dass wir diesmal keine Ausgabe gesehen haben, die anzeigt, dass Cargo
`hello_cargo` kompiliert. Cargo hat erkannt, dass sich die Dateien nicht
geändert hatten, und daher nicht neu gebaut, sondern nur die Binärdatei
ausgeführt. Hättest du deinen Quellcode geändert, hätte Cargo das Projekt vor
dem Ausführen neu gebaut, und du hättest diese Ausgabe gesehen:

```console
$ cargo run
   Compiling hello_cargo v0.1.0 (file:///projects/hello_cargo)
    Finished dev [unoptimized + debuginfo] target(s) in 0.33 secs
     Running `target/debug/hello_cargo`
Hello, world!
```

Cargo bietet außerdem einen Befehl namens `cargo check`. Dieser Befehl prüft
deinen Code schnell darauf, ob er sich kompilieren lässt, erzeugt aber keine
ausführbare Datei:

```console
$ cargo check
   Checking hello_cargo v0.1.0 (file:///projects/hello_cargo)
    Finished dev [unoptimized + debuginfo] target(s) in 0.32 secs
```

Warum solltest du keine ausführbare Datei wollen? Oft ist `cargo check` viel
schneller als `cargo build`, weil es den Schritt überspringt, eine ausführbare
Datei zu erzeugen. Wenn du deine Arbeit beim Schreiben des Codes ständig
überprüfst, erfährst du mit `cargo check` schneller, ob sich dein Projekt noch
kompilieren lässt! Deshalb führen viele Rustaceans beim Schreiben ihres
Programms regelmäßig `cargo check` aus, um sicherzugehen, dass es sich
kompilieren lässt. Wenn sie die ausführbare Datei dann verwenden wollen, führen
sie `cargo build` aus.

Fassen wir zusammen, was wir bisher über Cargo gelernt haben:

- Mit `cargo new` können wir ein Projekt erstellen.
- Mit `cargo build` können wir ein Projekt bauen.
- Mit `cargo run` können wir ein Projekt in einem Schritt bauen und ausführen.
- Mit `cargo check` können wir ein Projekt auf Fehler prüfen lassen, ohne eine
  Binärdatei zu erzeugen.
- Statt das Ergebnis des Builds im selben Verzeichnis wie unseren Code
  abzulegen, speichert Cargo es im Verzeichnis _target/debug_.

Ein weiterer Vorteil von Cargo ist, dass die Befehle unabhängig vom
Betriebssystem dieselben sind. Ab hier geben wir deshalb keine getrennten
Anweisungen für Linux und macOS bzw. Windows mehr an.

### Für ein Release bauen {#building-for-release}

Wenn dein Projekt endlich bereit für ein Release ist, kannst du es mit
`cargo build
--release` mit Optimierungen kompilieren. Dieser Befehl erzeugt eine
ausführbare Datei in _target/release_ statt in _target/debug_. Die Optimierungen
lassen deinen Rust-Code schneller laufen, verlängern aber die Zeit, die das
Kompilieren deines Programms dauert. Deshalb gibt es zwei verschiedene Profile:
eines für die Entwicklung, wenn du schnell und oft neu bauen willst, und eines
für das fertige Programm, das du an Nutzerinnen und Nutzer weitergibst, das
nicht ständig neu gebaut wird und so schnell wie möglich laufen soll. Wenn du
die Laufzeit deines Codes misst, führe unbedingt `cargo build --release` aus und
miss mit der ausführbaren Datei in _target/release_.

<!-- Old headings. Do not remove or links may break. -->

<a id="cargo-as-convention"></a>

### Die Konventionen von Cargo nutzen {#leveraging-cargos-conventions}

Bei einfachen Projekten bietet Cargo gegenüber `rustc` allein keinen großen
Mehrwert, aber es wird sich bewähren, wenn deine Programme komplexer werden.
Sobald Programme auf mehrere Dateien anwachsen oder eine Abhängigkeit brauchen,
ist es viel einfacher, Cargo den Build koordinieren zu lassen.

Auch wenn das Projekt `hello_cargo` einfach ist, verwendet es jetzt schon einen
Großteil der echten Werkzeuge, die du im Rest deiner Rust-Laufbahn verwenden
wirst. Um an einem beliebigen bestehenden Projekt zu arbeiten, kannst du sogar
die folgenden Befehle verwenden, um den Code mit Git auszuchecken, in das
Verzeichnis des Projekts zu wechseln und zu bauen:

```console
$ git clone example.org/someproject
$ cd someproject
$ cargo build
```

Weitere Informationen zu Cargo findest du in [seiner Dokumentation][cargo].

{{#quiz ../quizzes/ch01-03-hello-cargo.toml}}

## Zusammenfassung {#summary}

Du hast deine Reise mit Rust schon großartig begonnen! In diesem Kapitel hast du
gelernt, wie du:

- die neueste stabile Version von Rust mit `rustup` installierst,
- auf eine neuere Rust-Version aktualisierst,
- die lokal installierte Dokumentation öffnest,
- ein „Hello, world!“-Programm direkt mit `rustc` schreibst und ausführst,
- ein neues Projekt nach den Konventionen von Cargo erstellst und ausführst.

Jetzt ist ein guter Zeitpunkt, ein umfangreicheres Programm zu bauen, um dich an
das Lesen und Schreiben von Rust-Code zu gewöhnen. In Kapitel 2 bauen wir
deshalb ein Ratespiel. Wenn du lieber erst lernen willst, wie gängige
Programmierkonzepte in Rust funktionieren, lies Kapitel 3 und kehre dann zu
Kapitel 2 zurück.

[installation]: ch01-01-installation.html#installation
[toml]: https://toml.io
[appendix-e]: appendix-05-editions.html
[cargo]: https://doc.rust-lang.org/cargo/
