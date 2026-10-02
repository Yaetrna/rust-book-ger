## Pakete und Crates {#packages-and-crates}

Die ersten Teile des Modulsystems, die wir behandeln, sind Pakete und Crates.

Ein _Crate_ ist die kleinste Codemenge, die der Rust-Compiler auf einmal
betrachtet. Selbst wenn du `rustc` statt `cargo` ausführst und eine einzelne
Quellcodedatei übergibst (wie wir es ganz am Anfang in
[„Grundlagen eines Rust-Programms“][basics]<!-- ignore --> in Kapitel 1 getan
haben), betrachtet der Compiler diese Datei als Crate. Crates können Module
enthalten, und die Module können in anderen Dateien definiert sein, die mit dem
Crate kompiliert werden, wie wir in den kommenden Abschnitten sehen werden.

Ein Crate kann in einer von zwei Formen vorliegen: als Binary-Crate oder als
Library-Crate. _Binary-Crates_ sind Programme, die du zu einer ausführbaren
Datei kompilieren und dann ausführen kannst, etwa ein Kommandozeilenprogramm
oder ein Server. Jedes muss eine Funktion namens `main` haben, die festlegt, was
passiert, wenn die ausführbare Datei läuft. Alle Crates, die wir bisher erstellt
haben, waren Binary-Crates.

_Library-Crates_ haben keine Funktion `main` und werden nicht zu einer
ausführbaren Datei kompiliert. Stattdessen definieren sie Funktionalität, die
mit mehreren Projekten geteilt werden soll. Das Crate `rand`, das wir in
[Kapitel 2][rand]<!-- ignore --> verwendet haben, stellt zum Beispiel
Funktionalität zum Erzeugen von Zufallszahlen bereit. Wenn Rustaceans „Crate“
sagen, meinen sie meistens ein Library-Crate, und sie verwenden „Crate“
austauschbar mit dem allgemeinen Programmierkonzept einer „Bibliothek“.

Die _Crate-Root_ (die Wurzeldatei des Modulbaums) ist eine Quelldatei, bei der
der Rust-Compiler beginnt und die das Wurzelmodul deines Crates bildet (Module
erklären wir ausführlich in
[„Gültigkeitsbereich und Sichtbarkeit mit Modulen steuern“][modules]<!-- ignore -->).

Ein _Paket_ ist ein Bündel aus einem oder mehreren Crates, das eine Menge an
Funktionalität bereitstellt. Ein Paket enthält eine Datei _Cargo.toml_, die
beschreibt, wie diese Crates gebaut werden. Cargo ist selbst ein Paket, das das
Binary-Crate für das Kommandozeilenwerkzeug enthält, mit dem du deinen Code
gebaut hast. Das Paket Cargo enthält außerdem ein Library-Crate, von dem das
Binary-Crate abhängt. Andere Projekte können vom Library-Crate von Cargo
abhängen, um dieselbe Logik zu verwenden wie das Kommandozeilenwerkzeug Cargo.

Ein Paket kann beliebig viele Binary-Crates enthalten, aber höchstens ein
Library-Crate. Ein Paket muss mindestens ein Crate enthalten, egal ob Library-
oder Binary-Crate.

Gehen wir durch, was passiert, wenn wir ein Paket erstellen. Zuerst geben wir
den Befehl `cargo new my-project` ein:

```console
$ cargo new my-project
     Created binary (application) `my-project` package
$ ls my-project
Cargo.toml
src
$ ls my-project/src
main.rs
```

Nachdem wir `cargo new my-project` ausgeführt haben, sehen wir uns mit `ls` an,
was Cargo erstellt. Im Verzeichnis _my-project_ gibt es eine Datei _Cargo.toml_,
die uns ein Paket gibt. Es gibt auch ein Verzeichnis _src_, das _main.rs_
enthält. Öffne _Cargo.toml_ in deinem Texteditor und beachte, dass _src/main.rs_
nirgends erwähnt wird. Cargo folgt der Konvention, dass _src/main.rs_ die
Crate-Root eines Binary-Crates mit demselben Namen wie das Paket ist. Ebenso
weiß Cargo: Wenn das Paketverzeichnis _src/lib.rs_ enthält, enthält das Paket
ein Library-Crate mit demselben Namen wie das Paket, und _src/lib.rs_ ist dessen
Crate-Root. Cargo übergibt die Crate-Root-Dateien an `rustc`, um die Bibliothek
oder die Binärdatei zu bauen.

Hier haben wir ein Paket, das nur _src/main.rs_ enthält, also nur ein
Binary-Crate namens `my-project`. Enthält ein Paket _src/main.rs_ und
_src/lib.rs_, hat es zwei Crates: ein Binary- und ein Library-Crate, beide mit
demselben Namen wie das Paket. Ein Paket kann mehrere Binary-Crates haben, indem
man Dateien im Verzeichnis _src/bin_ ablegt: Jede Datei wird zu einem eigenen
Binary-Crate.

{{#quiz ../quizzes/ch07-01-packages-and-crates.toml}}

[basics]: ch01-02-hello-world.html#rust-program-basics
[modules]: ch07-02-defining-modules-to-control-scope-and-privacy.html
[rand]: ch02-00-guessing-game-tutorial.html#generating-a-random-number
