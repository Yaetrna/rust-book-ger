## Hello, World!

Nachdem du Rust installiert hast, ist es Zeit, dein erstes Rust-Programm zu
schreiben. Wenn man eine neue Sprache lernt, schreibt man traditionell ein
kleines Programm, das den Text `Hello, world!` auf dem Bildschirm ausgibt, und
genau das machen wir hier auch!

> Note: Dieses Buch setzt grundlegende Vertrautheit mit der Kommandozeile
> voraus. Rust stellt keine besonderen Anforderungen an deinen Editor, deine
> Werkzeuge oder den Ort, an dem dein Code liegt. Wenn du also lieber eine IDE
> als die Kommandozeile verwendest, nimm gern deine Lieblings-IDE. Viele IDEs
> unterstützen Rust inzwischen in gewissem Umfang; Details findest du in der
> Dokumentation deiner IDE. Das Rust-Team hat sich darauf konzentriert, mit
> `rust-analyzer` eine hervorragende IDE-Unterstützung zu ermöglichen. Mehr dazu
> findest du in [Anhang D][devtools]<!-- ignore -->.

<!-- Old headings. Do not remove or links may break. -->

<a id="creating-a-project-directory"></a>

### Ein Projektverzeichnis anlegen {#project-directory-setup}

Als Erstes legst du ein Verzeichnis an, in dem du deinen Rust-Code speicherst.
Für Rust spielt es keine Rolle, wo dein Code liegt, aber für die Übungen und
Projekte in diesem Buch empfehlen wir, in deinem Home-Verzeichnis ein
Verzeichnis _projects_ anzulegen und alle deine Projekte dort aufzubewahren.

Öffne ein Terminal und gib die folgenden Befehle ein, um ein Verzeichnis
_projects_ und darin ein Verzeichnis für das Projekt „Hello, world!“ anzulegen.

Unter Linux, macOS und in PowerShell unter Windows gibst du Folgendes ein:

```console
$ mkdir ~/projects
$ cd ~/projects
$ mkdir hello_world
$ cd hello_world
```

In der Windows-CMD gibst du Folgendes ein:

```cmd
> mkdir "%USERPROFILE%\projects"
> cd /d "%USERPROFILE%\projects"
> mkdir hello_world
> cd hello_world
```

<!-- Old headings. Do not remove or links may break. -->

<a id="writing-and-running-a-rust-program"></a>

### Grundlagen eines Rust-Programms {#rust-program-basics}

Lege als Nächstes eine neue Quelldatei an und nenne sie _main.rs_. Rust-Dateien
enden immer mit der Endung _.rs_. Wenn dein Dateiname aus mehr als einem Wort
besteht, trennt man die Wörter üblicherweise mit einem Unterstrich. Verwende
also zum Beispiel _hello_world.rs_ statt _helloworld.rs_.

Öffne nun die gerade erstellte Datei _main.rs_ und gib den Code aus Listing 1-1
ein.

<Listing number="1-1" file-name="main.rs" caption="Ein Programm, das `Hello, world!` ausgibt">

```rust
fn main() {
    println!("Hello, world!");
}
```

</Listing>

Speichere die Datei und wechsle zurück in dein Terminalfenster im Verzeichnis
_~/projects/hello_world_. Unter Linux oder macOS gibst du die folgenden Befehle
ein, um die Datei zu kompilieren und auszuführen:

```console
$ rustc main.rs
$ ./main
Hello, world!
```

Unter Windows gibst du statt `./main` den Befehl `.\main` ein:

```powershell
> rustc main.rs
> .\main
Hello, world!
```

Unabhängig von deinem Betriebssystem sollte der String `Hello, world!` im
Terminal ausgegeben werden. Falls du diese Ausgabe nicht siehst, findest du im
Teil [„Fehlerbehebung“][troubleshooting]<!-- ignore --> des Abschnitts zur
Installation Möglichkeiten, Hilfe zu bekommen.

Wenn `Hello, world!` ausgegeben wurde: Glückwunsch! Du hast offiziell ein
Rust-Programm geschrieben. Damit bist du Rust-Programmiererin oder
Rust-Programmierer – willkommen!

<!-- Old headings. Do not remove or links may break. -->

<a id="anatomy-of-a-rust-program"></a>

### Der Aufbau eines Rust-Programms {#the-anatomy-of-a-rust-program}

Sehen wir uns dieses „Hello, world!“-Programm im Detail an. Hier ist das erste
Teil des Puzzles:

```rust
fn main() {

}
```

Diese Zeilen definieren eine Funktion namens `main`. Die Funktion `main` ist
besonders: Sie ist in jedem ausführbaren Rust-Programm immer der erste Code, der
ausgeführt wird. Die erste Zeile deklariert hier eine Funktion namens `main`,
die keine Parameter hat und nichts zurückgibt. Gäbe es Parameter, stünden sie
innerhalb der runden Klammern (`()`).

Der Funktionsrumpf ist von `{}` umschlossen. Rust verlangt geschweifte Klammern
um alle Funktionsrümpfe. Es ist guter Stil, die öffnende geschweifte Klammer in
dieselbe Zeile wie die Funktionsdeklaration zu setzen, mit einem Leerzeichen
dazwischen.

> Note: Wenn du dich in allen Rust-Projekten an einen einheitlichen Stil halten
> willst, kannst du ein automatisches Formatierungswerkzeug namens `rustfmt`
> verwenden, das deinen Code in einem bestimmten Stil formatiert (mehr zu
> `rustfmt` in [Anhang D][devtools]<!-- ignore -->). Das Rust-Team liefert
> dieses Werkzeug wie `rustc` mit der Standarddistribution von Rust aus, es
> sollte also bereits auf deinem Rechner installiert sein!

Der Rumpf der Funktion `main` enthält folgenden Code:

```rust
println!("Hello, world!");
```

Diese Zeile erledigt die ganze Arbeit in diesem kleinen Programm: Sie gibt Text
auf dem Bildschirm aus. Dabei fallen drei wichtige Details auf.

Erstens ruft `println!` ein Rust-Makro auf. Würde stattdessen eine Funktion
aufgerufen, stünde dort `println` (ohne das `!`). Rust-Makros sind eine
Möglichkeit, Code zu schreiben, der Code erzeugt, um die Syntax von Rust zu
erweitern; wir besprechen sie in [Kapitel 20][ch20-macros]<!-- ignore -->
ausführlicher. Vorerst musst du nur wissen, dass ein `!` bedeutet, dass du ein
Makro statt einer normalen Funktion aufrufst, und dass Makros nicht immer
denselben Regeln folgen wie Funktionen.

Zweitens siehst du den String `"Hello, world!"`. Wir übergeben diesen String als
Argument an `println!`, und der String wird auf dem Bildschirm ausgegeben.

Drittens beenden wir die Zeile mit einem Semikolon (`;`), das anzeigt, dass
dieser Ausdruck zu Ende ist und der nächste beginnen kann. Die meisten Zeilen in
Rust-Code enden mit einem Semikolon.

<!-- Old headings. Do not remove or links may break. -->

<a id="compiling-and-running-are-separate-steps"></a>

### Kompilieren und Ausführen {#compilation-and-execution}

Du hast gerade ein neu erstelltes Programm ausgeführt, also sehen wir uns jeden
Schritt dieses Vorgangs an.

Bevor du ein Rust-Programm ausführen kannst, musst du es mit dem Rust-Compiler
kompilieren, indem du den Befehl `rustc` eingibst und ihm den Namen deiner
Quelldatei übergibst, etwa so:

```console
$ rustc main.rs
```

Wenn du Erfahrung mit C oder C++ hast, wird dir auffallen, dass das ähnlich wie
`gcc` oder `clang` funktioniert. Nach erfolgreichem Kompilieren gibt Rust eine
ausführbare Binärdatei aus.

Unter Linux, macOS und in PowerShell unter Windows kannst du die ausführbare
Datei sehen, indem du in deiner Shell den Befehl `ls` eingibst:

```console
$ ls
main  main.rs
```

Unter Linux und macOS siehst du zwei Dateien. In PowerShell unter Windows siehst
du dieselben drei Dateien, die du auch mit CMD sehen würdest. In der Windows-CMD
würdest du Folgendes eingeben:

```cmd
> dir /B %= the /B option says to only show the file names =%
main.exe
main.pdb
main.rs
```

Hier siehst du die Quellcodedatei mit der Endung _.rs_, die ausführbare Datei
(_main.exe_ unter Windows, auf allen anderen Plattformen _main_) und unter
Windows zusätzlich eine Datei mit Debug-Informationen mit der Endung _.pdb_. Von
hier aus führst du die Datei _main_ bzw. _main.exe_ aus, etwa so:

```console
$ ./main # or .\main on Windows
```

Wenn deine _main.rs_ dein „Hello, world!“-Programm enthält, gibt diese Zeile
`Hello,
world!` in deinem Terminal aus.

Wenn du eher mit einer dynamischen Sprache wie Ruby, Python oder JavaScript
vertraut bist, bist du es vielleicht nicht gewohnt, ein Programm in getrennten
Schritten zu kompilieren und auszuführen. Rust ist eine _ahead-of-time_
kompilierte Sprache: Du kannst ein Programm kompilieren und die ausführbare
Datei an jemand anderen weitergeben, und diese Person kann sie ausführen, auch
ohne Rust installiert zu haben. Wenn du jemandem eine _.rb_-, _.py_- oder
_.js_-Datei gibst, muss diese Person eine Ruby-, Python- bzw.
JavaScript-Implementierung installiert haben. Dafür brauchst du in diesen
Sprachen nur einen einzigen Befehl, um dein Programm zu kompilieren und
auszuführen. Im Sprachdesign ist alles ein Kompromiss.

Für einfache Programme reicht es, nur mit `rustc` zu kompilieren, aber wenn dein
Projekt wächst, willst du alle Optionen verwalten und das Teilen deines Codes
einfach machen. Als Nächstes stellen wir dir das Werkzeug Cargo vor, das dir
hilft, echte Rust-Programme zu schreiben.

{{#quiz ../quizzes/ch01-02-hello-world.toml}}

[troubleshooting]: ch01-01-installation.html#troubleshooting
[devtools]: appendix-04-useful-development-tools.html
[ch20-macros]: ch20-05-macros.html
