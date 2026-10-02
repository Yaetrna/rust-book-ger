## Installation {#installation}

Der erste Schritt ist, Rust zu installieren. Wir laden Rust über `rustup`
herunter, ein Kommandozeilenwerkzeug zum Verwalten von Rust-Versionen und
zugehörigen Werkzeugen. Für den Download brauchst du eine Internetverbindung.

> Note: Falls du `rustup` aus irgendeinem Grund lieber nicht verwenden möchtest,
> findest du auf der
> [Seite zu anderen Installationsmethoden für Rust][otherinstall] weitere
> Möglichkeiten.

Die folgenden Schritte installieren die neueste stabile Version des
Rust-Compilers. Die Stabilitätsgarantien von Rust stellen sicher, dass alle
Beispiele im Buch, die sich kompilieren lassen, sich auch mit neueren
Rust-Versionen weiterhin kompilieren lassen. Die Ausgabe kann sich zwischen
Versionen leicht unterscheiden, weil Rust Fehlermeldungen und Warnungen oft
verbessert. Mit anderen Worten: Jede neuere stabile Rust-Version, die du mit
diesen Schritten installierst, sollte wie erwartet mit dem Inhalt dieses Buchs
funktionieren.

> ### Notation für die Kommandozeile {#command-line-notation}
>
> In diesem Kapitel und im ganzen Buch zeigen wir einige Befehle, die im
> Terminal verwendet werden. Zeilen, die du in ein Terminal eingeben sollst,
> beginnen alle mit `$`. Das Zeichen `$` musst du nicht eintippen; es ist die
> Eingabeaufforderung der Kommandozeile und markiert den Beginn jedes Befehls.
> Zeilen, die nicht mit `$` beginnen, zeigen in der Regel die Ausgabe des
> vorherigen Befehls. Außerdem verwenden PowerShell-spezifische Beispiele `>`
> statt `$`.

### `rustup` unter Linux oder macOS installieren {#installing-rustup-on-linux-or-macos}

Wenn du Linux oder macOS verwendest, öffne ein Terminal und gib folgenden Befehl
ein:

```console
$ curl --proto '=https' --tlsv1.2 https://sh.rustup.rs -sSf | sh
```

Der Befehl lädt ein Skript herunter und startet die Installation des Werkzeugs
`rustup`, das die neueste stabile Version von Rust installiert. Möglicherweise
wirst du nach deinem Passwort gefragt. Wenn die Installation erfolgreich war,
erscheint folgende Zeile:

```text
Rust is installed now. Great!
```

Außerdem brauchst du einen _Linker_, also ein Programm, mit dem Rust seine
kompilierten Ausgaben zu einer Datei zusammenfügt. Wahrscheinlich hast du schon
einen. Wenn du Linker-Fehler bekommst, solltest du einen C-Compiler
installieren, der normalerweise einen Linker mitbringt. Ein C-Compiler ist auch
deshalb nützlich, weil einige verbreitete Rust-Pakete von C-Code abhängen und
einen C-Compiler benötigen.

Unter macOS bekommst du einen C-Compiler, indem du Folgendes ausführst:

```console
$ xcode-select --install
```

Unter Linux solltest du im Allgemeinen GCC oder Clang installieren, wie es in
der Dokumentation deiner Distribution beschrieben ist. Wenn du zum Beispiel
Ubuntu verwendest, kannst du das Paket `build-essential` installieren.

### `rustup` unter Windows installieren {#installing-rustup-on-windows}

Unter Windows gehst du auf
[https://www.rust-lang.org/tools/install][install]<!-- ignore --> und folgst den
Anweisungen zur Installation von Rust. Im Lauf der Installation wirst du
aufgefordert, Visual Studio zu installieren. Das stellt einen Linker und die
nativen Bibliotheken bereit, die zum Kompilieren von Programmen nötig sind. Wenn
du bei diesem Schritt mehr Hilfe brauchst, sieh dir
[https://rust-lang.github.io/rustup/installation/windows-msvc.html][msvc]<!-- ignore -->
an.

Der Rest dieses Buchs verwendet Befehle, die sowohl in _cmd.exe_ als auch in
PowerShell funktionieren. Wo es konkrete Unterschiede gibt, erklären wir, was du
verwenden solltest.

### Fehlerbehebung {#troubleshooting}

Um zu prüfen, ob Rust korrekt installiert ist, öffne eine Shell und gib diese
Zeile ein:

```console
$ rustc --version
```

Du solltest die Versionsnummer, den Commit-Hash und das Commit-Datum der
neuesten veröffentlichten stabilen Version in folgendem Format sehen:

```text
rustc x.y.z (abcabcabc yyyy-mm-dd)
```

Wenn du diese Informationen siehst, hast du Rust erfolgreich installiert! Wenn
nicht, prüfe wie folgt, ob Rust in deiner Systemvariable `PATH` enthalten ist.

In der Windows-CMD verwendest du:

```console
> echo %PATH%
```

In PowerShell verwendest du:

```powershell
> echo $env:Path
```

Unter Linux und macOS verwendest du:

```console
$ echo $PATH
```

Wenn das alles stimmt und Rust trotzdem nicht funktioniert, gibt es eine Reihe
von Stellen, an denen du Hilfe bekommst. Auf [der Community-Seite][community]
erfährst du, wie du mit anderen Rustaceans (ein alberner Spitzname, den wir uns
selbst gegeben haben) in Kontakt kommst.

### Aktualisieren und Deinstallieren {#updating-and-uninstalling}

Sobald Rust über `rustup` installiert ist, ist das Aktualisieren auf eine neu
veröffentlichte Version einfach. Führe in deiner Shell folgendes Update-Skript
aus:

```console
$ rustup update
```

Um Rust und `rustup` zu deinstallieren, führe in deiner Shell folgendes
Deinstallationsskript aus:

```console
$ rustup self uninstall
```

<!-- Old headings. Do not remove or links may break. -->

<a id="local-documentation"></a>

### Die lokale Dokumentation lesen {#reading-the-local-documentation}

Zur Installation von Rust gehört auch eine lokale Kopie der Dokumentation, damit
du sie offline lesen kannst. Führe `rustup doc` aus, um die lokale Dokumentation
in deinem Browser zu öffnen.

Immer wenn die Standardbibliothek einen Typ oder eine Funktion bereitstellt und
du nicht sicher bist, was er oder sie tut oder wie man ihn oder sie verwendet,
schau in der Dokumentation der Programmierschnittstelle (API) nach!

<!-- Old headings. Do not remove or links may break. -->

<a id="text-editors-and-integrated-development-environments"></a>

### Texteditoren und IDEs verwenden {#using-text-editors-and-ides}

Dieses Buch macht keine Annahmen darüber, mit welchen Werkzeugen du Rust-Code
schreibst. So gut wie jeder Texteditor erfüllt seinen Zweck! Viele Texteditoren
und integrierte Entwicklungsumgebungen (IDEs) bringen jedoch eingebaute
Unterstützung für Rust mit. Eine recht aktuelle Liste vieler Editoren und IDEs
findest du jederzeit auf [der Werkzeug-Seite][tools] der Rust-Website.

### Offline mit diesem Buch arbeiten {#working-offline-with-this-book}

In mehreren Beispielen verwenden wir Rust-Pakete, die über die
Standardbibliothek hinausgehen. Um diese Beispiele durchzuarbeiten, brauchst du
entweder eine Internetverbindung, oder du hast diese Abhängigkeiten vorher
heruntergeladen. Um die Abhängigkeiten vorab herunterzuladen, kannst du die
folgenden Befehle ausführen. (Was `cargo` ist und was jeder dieser Befehle genau
macht, erklären wir später ausführlich.)

```console
$ cargo new get-dependencies
$ cd get-dependencies
$ cargo add rand@0.8.5 trpl@0.2.0
```

Dadurch werden die Downloads dieser Pakete zwischengespeichert, sodass du sie
später nicht herunterladen musst. Sobald du diesen Befehl ausgeführt hast, musst
du den Ordner `get-dependencies` nicht behalten. Wenn du diesen Befehl
ausgeführt hast, kannst du im restlichen Buch bei allen `cargo`-Befehlen das
Flag `--offline` verwenden, um diese zwischengespeicherten Versionen zu nutzen,
statt auf das Netzwerk zuzugreifen.

{{#quiz ../quizzes/ch01-01-installation.toml}}

[otherinstall]: https://forge.rust-lang.org/infra/other-installation-methods.html
[install]: https://www.rust-lang.org/tools/install
[msvc]: https://rust-lang.github.io/rustup/installation/windows-msvc.html
[community]: https://www.rust-lang.org/community
[tools]: https://www.rust-lang.org/tools
