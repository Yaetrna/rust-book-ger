## Anhang D: Nützliche Entwicklungswerkzeuge {#appendix-d-useful-development-tools}

In diesem Anhang sprechen wir über einige nützliche Entwicklungswerkzeuge, die
das Rust-Projekt bereitstellt. Wir sehen uns die automatische Formatierung,
schnelle Möglichkeiten zum Anwenden von Korrekturen für Warnungen, einen Linter
und die Integration in IDEs an.

### Automatische Formatierung mit `rustfmt` {#automatic-formatting-with-rustfmt}

Das Werkzeug `rustfmt` formatiert deinen Code gemäß dem Code-Stil der Community
um. Viele gemeinschaftliche Projekte verwenden `rustfmt`, um Diskussionen
darüber zu vermeiden, welcher Stil beim Schreiben von Rust verwendet werden
soll: Alle formatieren ihren Code mit diesem Werkzeug.

Rust-Installationen enthalten standardmäßig `rustfmt`, daher solltest du die
Programme `rustfmt` und `cargo-fmt` bereits auf deinem System haben. Diese
beiden Befehle verhalten sich ähnlich wie `rustc` und `cargo`: `rustfmt`
ermöglicht eine feinere Steuerung, und `cargo-fmt` versteht die Konventionen
eines Projekts, das Cargo verwendet. Um ein beliebiges Cargo-Projekt zu
formatieren, gib Folgendes ein:

```console
$ cargo fmt
```

Dieser Befehl formatiert den gesamten Rust-Code im aktuellen Crate neu. Dabei
sollte sich nur der Code-Stil ändern, nicht die Semantik des Codes. Weitere
Informationen zu `rustfmt` findest du in [seiner Dokumentation][rustfmt].

### Deinen Code mit `rustfix` korrigieren {#fix-your-code-with-rustfix}

Das Werkzeug `rustfix` ist in Rust-Installationen enthalten und kann
Compilerwarnungen automatisch beheben, für die es einen klaren Weg zur Korrektur
gibt, der wahrscheinlich dem entspricht, was du willst. Du hast wahrscheinlich
schon Compilerwarnungen gesehen. Betrachte zum Beispiel diesen Code:

<span class="filename">Dateiname: src/main.rs</span>

```rust
fn main() {
    let mut x = 42;
    println!("{x}");
}
```

Hier definieren wir die Variable `x` als veränderlich (_mutable_), verändern sie
aber nie. Rust warnt uns davor:

```console
$ cargo build
   Compiling myprogram v0.1.0 (file:///projects/myprogram)
warning: variable does not need to be mutable
 --> src/main.rs:2:9
  |
2 |     let mut x = 0;
  |         ----^
  |         |
  |         help: remove this `mut`
  |
  = note: `#[warn(unused_mut)]` on by default
```

Die Warnung schlägt vor, das Schlüsselwort `mut` zu entfernen. Wir können diesen
Vorschlag mit dem Werkzeug `rustfix` automatisch anwenden, indem wir den Befehl
`cargo
fix` ausführen:

```console
$ cargo fix
    Checking myprogram v0.1.0 (file:///projects/myprogram)
      Fixing src/main.rs (1 fix)
    Finished dev [unoptimized + debuginfo] target(s) in 0.59s
```

Wenn wir uns _src/main.rs_ erneut ansehen, sehen wir, dass `cargo fix` den Code
geändert hat:

<span class="filename">Dateiname: src/main.rs</span>

```rust
fn main() {
    let x = 42;
    println!("{x}");
}
```

Die Variable `x` ist jetzt unveränderlich (_immutable_), und die Warnung
erscheint nicht mehr.

Du kannst den Befehl `cargo fix` auch verwenden, um deinen Code zwischen
verschiedenen Rust-Editionen zu überführen. Editionen werden in
[Anhang E][editions]<!--
ignore --> behandelt.

### Mehr Lints mit Clippy {#more-lints-with-clippy}

Das Werkzeug Clippy ist eine Sammlung von Lints zur Analyse deines Codes, damit
du häufige Fehler finden und deinen Rust-Code verbessern kannst. Clippy ist in
Standard-Rust-Installationen enthalten.

Um die Lints von Clippy auf ein beliebiges Cargo-Projekt anzuwenden, gib
Folgendes ein:

```console
$ cargo clippy
```

Angenommen, du schreibst ein Programm, das eine Näherung einer mathematischen
Konstante wie Pi verwendet, so wie dieses Programm:

<Listing file-name="src/main.rs">

```rust
fn main() {
    let x = 3.1415;
    let r = 8.0;
    println!("the area of the circle is {}", x * r * r);
}
```

</Listing>

Wenn du `cargo clippy` auf dieses Projekt anwendest, erhältst du diesen Fehler:

```text
error: approximate value of `f{32, 64}::consts::PI` found
 --> src/main.rs:2:13
  |
2 |     let x = 3.1415;
  |             ^^^^^^
  |
  = note: `#[deny(clippy::approx_constant)]` on by default
  = help: consider using the constant directly
  = help: for further information visit https://rust-lang.github.io/rust-clippy/master/index.html#approx_constant
```

Dieser Fehler teilt dir mit, dass in Rust bereits eine genauere Konstante `PI`
definiert ist und dass dein Programm korrekter wäre, wenn du stattdessen diese
Konstante verwenden würdest. Du würdest deinen Code dann so ändern, dass er die
Konstante `PI` verwendet.

Der folgende Code führt in Clippy zu keinen Fehlern oder Warnungen:

<Listing file-name="src/main.rs">

```rust
fn main() {
    let x = std::f64::consts::PI;
    let r = 8.0;
    println!("the area of the circle is {}", x * r * r);
}
```

</Listing>

Weitere Informationen zu Clippy findest du in [seiner Dokumentation][clippy].

### IDE-Integration mit `rust-analyzer` {#ide-integration-using-rust-analyzer}

Für die IDE-Integration empfiehlt die Rust-Community
[`rust-analyzer`][rust-analyzer]<!-- ignore -->. Dieses Werkzeug ist eine
Sammlung compilerorientierter Hilfsprogramme, die das
[Language Server Protocol][lsp]<!--
ignore --> sprechen, eine Spezifikation, über die IDEs und Programmiersprachen
miteinander kommunizieren. Verschiedene Clients können `rust-analyzer`
verwenden, etwa [das Rust-analyzer-Plug-in für Visual Studio Code][vscode].

Besuche die [Homepage][rust-analyzer]<!-- ignore --> des Projekts
`rust-analyzer`, um Installationsanweisungen zu erhalten, und installiere dann
die Unterstützung für den Language Server in deiner IDE. Deine IDE erhält dann
Fähigkeiten wie Autovervollständigung, Sprung zur Definition und Fehleranzeigen
direkt im Code.

[rustfmt]: https://github.com/rust-lang/rustfmt
[editions]: appendix-05-editions.md
[clippy]: https://github.com/rust-lang/rust-clippy
[rust-analyzer]: https://rust-analyzer.github.io
[lsp]: http://langserver.org/
[vscode]: https://marketplace.visualstudio.com/items?itemName=rust-lang.rust-analyzer
