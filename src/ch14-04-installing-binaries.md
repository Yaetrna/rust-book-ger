<!-- Old headings. Do not remove or links may break. -->

<a id="installing-binaries-from-cratesio-with-cargo-install"></a>

## Binärdateien mit `cargo install` installieren {#installing-binaries-with-cargo-install}

Mit dem Befehl `cargo install` kannst du Binary-Crates lokal installieren und
verwenden. Das soll keine Systempakete ersetzen; es ist als bequeme Möglichkeit
für Rust-Entwicklerinnen und -Entwickler gedacht, Werkzeuge zu installieren, die
andere auf [crates.io](https://crates.io/)<!-- ignore --> geteilt haben.
Beachte, dass du nur Pakete installieren kannst, die Binary-Targets haben. Ein
_Binary-Target_ ist das ausführbare Programm, das erzeugt wird, wenn das Crate
eine Datei _src/main.rs_ oder eine andere als Binärdatei angegebene Datei hat,
im Gegensatz zu einem Library-Target, das für sich allein nicht ausführbar ist,
sich aber dafür eignet, in andere Programme eingebunden zu werden. Normalerweise
enthalten Crates in der README-Datei Informationen darüber, ob ein Crate eine
Bibliothek ist, ein Binary-Target hat oder beides.

Alle mit `cargo install` installierten Binärdateien werden im Ordner _bin_ des
Installationsverzeichnisses gespeichert. Hast du Rust mit _rustup.rs_
installiert und keine eigenen Konfigurationen, ist dieses
Verzeichnis *$HOME/.cargo/bin*. Stell sicher, dass dieses Verzeichnis in deinem `$PATH`enthalten ist, damit du Programme ausführen kannst, die du mit`cargo
install` installiert hast.

In Kapitel 12 haben wir zum Beispiel erwähnt, dass es eine Rust-Implementierung
des Werkzeugs `grep` namens `ripgrep` zum Durchsuchen von Dateien gibt. Um
`ripgrep` zu installieren, können wir Folgendes ausführen:

<!-- manual-regeneration
cargo install something you don't have, copy relevant output below
-->

```console
$ cargo install ripgrep
    Updating crates.io index
  Downloaded ripgrep v14.1.1
  Downloaded 1 crate (213.6 KB) in 0.40s
  Installing ripgrep v14.1.1
--snip--
   Compiling grep v0.3.2
    Finished `release` profile [optimized + debuginfo] target(s) in 6.73s
  Installing ~/.cargo/bin/rg
   Installed package `ripgrep v14.1.1` (executable `rg`)
```

Die vorletzte Zeile der Ausgabe zeigt den Ort und den Namen der installierten
Binärdatei, die im Fall von `ripgrep` `rg` heißt. Solange das
Installationsverzeichnis wie erwähnt in deinem `$PATH` enthalten ist, kannst du
dann `rg --help` ausführen und ein schnelleres, rostigeres Werkzeug zum
Durchsuchen von Dateien verwenden!
