## Cargo-Workspaces {#cargo-workspaces}

In Kapitel 12 haben wir ein Paket gebaut, das ein Binary-Crate und ein
Library-Crate enthielt. Während sich dein Projekt weiterentwickelt, stellst du
vielleicht fest, dass das Library-Crate immer größer wird und du dein Paket
weiter in mehrere Library-Crates aufteilen willst. Cargo bietet ein Feature
namens _Workspaces_, das helfen kann, mehrere zusammengehörige Pakete zu
verwalten, die gemeinsam entwickelt werden.

### Einen Workspace erstellen {#creating-a-workspace}

Ein _Workspace_ ist eine Menge von Paketen, die dieselbe _Cargo.lock_ und
dasselbe Ausgabeverzeichnis teilen. Erstellen wir ein Projekt mit einem
Workspace – wir verwenden trivialen Code, damit wir uns auf die Struktur des
Workspaces konzentrieren können. Es gibt mehrere Möglichkeiten, einen Workspace
zu strukturieren, daher zeigen wir nur eine gängige. Wir haben einen Workspace
mit einer Binärdatei und zwei Bibliotheken. Die Binärdatei, die die
Hauptfunktionalität bereitstellt, hängt von den beiden Bibliotheken ab. Eine
Bibliothek stellt eine Funktion `add_one` bereit und die andere eine Funktion
`add_two`. Diese drei Crates gehören zum selben Workspace. Wir beginnen damit,
ein neues Verzeichnis für den Workspace anzulegen:

```console
$ mkdir add
$ cd add
```

Als Nächstes legen wir im Verzeichnis _add_ die Datei _Cargo.toml_ an, die den
gesamten Workspace konfiguriert. Diese Datei hat keinen Abschnitt `[package]`.
Stattdessen beginnt sie mit einem Abschnitt `[workspace]`, mit dem wir dem
Workspace Mitglieder hinzufügen können. Außerdem achten wir darauf, in unserem
Workspace die neueste Version des Resolver-Algorithmus von Cargo zu verwenden,
indem wir den Wert `resolver` auf `"3"` setzen:

<span class="filename">Dateiname: Cargo.toml</span>

```toml
{{#include ../listings/ch14-more-about-cargo/no-listing-01-workspace/add/Cargo.toml}}
```

Als Nächstes erstellen wir das Binary-Crate `adder`, indem wir im Verzeichnis
_add_ `cargo new` ausführen:

<!-- manual-regeneration
cd listings/ch14-more-about-cargo/output-only-01-adder-crate/add
remove `members = ["adder"]` from Cargo.toml
rm -rf adder
cargo new adder
copy output below
-->

```console
$ cargo new adder
     Created binary (application) `adder` package
      Adding `adder` as member of workspace at `file:///projects/add`
```

Führt man `cargo new` innerhalb eines Workspaces aus, wird das neu erstellte
Paket außerdem automatisch dem Schlüssel `members` in der Definition
`[workspace]` in der _Cargo.toml_ des Workspaces hinzugefügt, etwa so:

```toml
{{#include ../listings/ch14-more-about-cargo/output-only-01-adder-crate/add/Cargo.toml}}
```

An dieser Stelle können wir den Workspace mit `cargo build` bauen. Die Dateien
in deinem Verzeichnis _add_ sollten so aussehen:

```text
├── Cargo.lock
├── Cargo.toml
├── adder
│   ├── Cargo.toml
│   └── src
│       └── main.rs
└── target
```

Der Workspace hat auf der obersten Ebene ein Verzeichnis _target_, in dem die
kompilierten Artefakte abgelegt werden; das Paket `adder` hat kein eigenes
Verzeichnis _target_. Selbst wenn wir `cargo build` im Verzeichnis _adder_
ausführen würden, würden die kompilierten Artefakte trotzdem in _add/target_
statt in _add/adder/target_ landen. Cargo strukturiert das Verzeichnis _target_
in einem Workspace so, weil die Crates in einem Workspace voneinander abhängen
sollen. Hätte jedes Crate sein eigenes Verzeichnis _target_, müsste jedes Crate
alle anderen Crates im Workspace neu kompilieren, um die Artefakte in seinem
eigenen Verzeichnis _target_ abzulegen. Durch ein gemeinsames Verzeichnis
_target_ vermeiden die Crates unnötiges Neubauen.

### Das zweite Paket im Workspace erstellen {#creating-the-second-package-in-the-workspace}

Als Nächstes erstellen wir ein weiteres Mitgliedspaket im Workspace und nennen
es `add_one`. Erzeuge ein neues Library-Crate namens `add_one`:

<!-- manual-regeneration
cd listings/ch14-more-about-cargo/output-only-02-add-one/add
remove `"add_one"` from `members` list in Cargo.toml
rm -rf add_one
cargo new add_one --lib
copy output below
-->

```console
$ cargo new add_one --lib
     Created library `add_one` package
      Adding `add_one` as member of workspace at `file:///projects/add`
```

Die _Cargo.toml_ auf oberster Ebene enthält jetzt den Pfad _add_one_ in der
Liste `members`:

<span class="filename">Dateiname: Cargo.toml</span>

```toml
{{#include ../listings/ch14-more-about-cargo/no-listing-02-workspace-with-two-crates/add/Cargo.toml}}
```

Dein Verzeichnis _add_ sollte jetzt diese Verzeichnisse und Dateien enthalten:

```text
├── Cargo.lock
├── Cargo.toml
├── add_one
│   ├── Cargo.toml
│   └── src
│       └── lib.rs
├── adder
│   ├── Cargo.toml
│   └── src
│       └── main.rs
└── target
```

Fügen wir in der Datei _add_one/src/lib.rs_ eine Funktion `add_one` hinzu:

<span class="filename">Dateiname: add_one/src/lib.rs</span>

```rust,noplayground
{{#rustdoc_include ../listings/ch14-more-about-cargo/no-listing-02-workspace-with-two-crates/add/add_one/src/lib.rs}}
```

Jetzt können wir das Paket `adder` mit unserer Binärdatei vom Paket `add_one`
mit unserer Bibliothek abhängen lassen. Zuerst müssen wir in _adder/Cargo.toml_
eine Pfadabhängigkeit auf `add_one` hinzufügen.

<span class="filename">Dateiname: adder/Cargo.toml</span>

```toml
{{#include ../listings/ch14-more-about-cargo/no-listing-02-workspace-with-two-crates/add/adder/Cargo.toml:6:7}}
```

Cargo nimmt nicht an, dass Crates in einem Workspace voneinander abhängen, daher
müssen wir die Abhängigkeitsbeziehungen explizit angeben.

Als Nächstes verwenden wir die Funktion `add_one` (aus dem Crate `add_one`) im
Crate `adder`. Öffne die Datei _adder/src/main.rs_ und ändere die Funktion
`main` so, dass sie die Funktion `add_one` aufruft, wie in Listing 14-7.

<Listing number="14-7" file-name="adder/src/main.rs" caption="Das Library-Crate `add_one` aus dem Crate `adder` verwenden">

```rust,ignore
{{#rustdoc_include ../listings/ch14-more-about-cargo/listing-14-07/add/adder/src/main.rs}}
```

</Listing>

Bauen wir den Workspace, indem wir im Verzeichnis _add_ auf oberster Ebene
`cargo build` ausführen!

<!-- manual-regeneration
cd listings/ch14-more-about-cargo/listing-14-07/add
cargo build
copy output below; the output updating script doesn't handle subdirectories in paths properly
-->

```console
$ cargo build
   Compiling add_one v0.1.0 (file:///projects/add/add_one)
   Compiling adder v0.1.0 (file:///projects/add/adder)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.22s
```

Um das Binary-Crate aus dem Verzeichnis _add_ auszuführen, können wir mit dem
Argument `-p` und dem Paketnamen bei `cargo run` angeben, welches Paket im
Workspace wir ausführen wollen:

<!-- manual-regeneration
cd listings/ch14-more-about-cargo/listing-14-07/add
cargo run -p adder
copy output below; the output updating script doesn't handle subdirectories in paths properly
-->

```console
$ cargo run -p adder
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.00s
     Running `target/debug/adder`
Hello, world! 10 plus one is 11!
```

Das führt den Code in _adder/src/main.rs_ aus, der vom Crate `add_one` abhängt.

<!-- Old headings. Do not remove or links may break. -->

<a id="depending-on-an-external-package-in-a-workspace"></a>

### Von einem externen Paket abhängen {#depending-on-an-external-package}

Beachte, dass der Workspace nur eine einzige Datei _Cargo.lock_ auf oberster
Ebene hat statt einer _Cargo.lock_ im Verzeichnis jedes Crates. Das stellt
sicher, dass alle Crates dieselbe Version aller Abhängigkeiten verwenden. Fügen
wir das Paket `rand` zu den Dateien _adder/Cargo.toml_ und _add_one/Cargo.toml_
hinzu, löst Cargo beide zu einer einzigen Version von `rand` auf und hält diese
in der einen _Cargo.lock_ fest. Dass alle Crates im Workspace dieselben
Abhängigkeiten verwenden, bedeutet, dass die Crates immer miteinander kompatibel
sind. Fügen wir das Crate `rand` zum Abschnitt `[dependencies]` in der Datei
_add_one/Cargo.toml_ hinzu, damit wir das Crate `rand` im Crate `add_one`
verwenden können:

<!-- When updating the version of `rand` used, also update the version of
`rand` used in these files so they all match:
* ch02-00-guessing-game-tutorial.md
* ch07-04-bringing-paths-into-scope-with-the-use-keyword.md
-->

<span class="filename">Dateiname: add_one/Cargo.toml</span>

```toml
{{#include ../listings/ch14-more-about-cargo/no-listing-03-workspace-with-external-dependency/add/add_one/Cargo.toml:6:7}}
```

Jetzt können wir der Datei _add_one/src/lib.rs_ `use rand;` hinzufügen, und wenn
wir den gesamten Workspace mit `cargo build` im Verzeichnis _add_ bauen, wird
das Crate `rand` eingebunden und kompiliert. Wir bekommen eine Warnung, weil wir
nicht auf das `rand` verweisen, das wir in den Gültigkeitsbereich (_scope_)
gebracht haben:

<!-- manual-regeneration
cd listings/ch14-more-about-cargo/no-listing-03-workspace-with-external-dependency/add
cargo build
copy output below; the output updating script doesn't handle subdirectories in paths properly
-->

```console
$ cargo build
    Updating crates.io index
  Downloaded rand v0.8.5
   --snip--
   Compiling rand v0.8.5
   Compiling add_one v0.1.0 (file:///projects/add/add_one)
warning: unused import: `rand`
 --> add_one/src/lib.rs:1:5
  |
1 | use rand;
  |     ^^^^
  |
  = note: `#[warn(unused_imports)]` on by default

warning: `add_one` (lib) generated 1 warning (run `cargo fix --lib -p add_one` to apply 1 suggestion)
   Compiling adder v0.1.0 (file:///projects/add/adder)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.95s
```

Die _Cargo.lock_ auf oberster Ebene enthält jetzt Informationen über die
Abhängigkeit von `add_one` von `rand`. Obwohl `rand` irgendwo im Workspace
verwendet wird, können wir es in anderen Crates im Workspace aber nicht
verwenden, solange wir `rand` nicht auch zu deren _Cargo.toml_-Dateien
hinzufügen. Fügen wir zum Beispiel der Datei _adder/src/main.rs_ des Pakets
`adder` `use rand;` hinzu, erhalten wir einen Fehler:

<!-- manual-regeneration
cd listings/ch14-more-about-cargo/output-only-03-use-rand/add
cargo build
copy output below; the output updating script doesn't handle subdirectories in paths properly
-->

```console
$ cargo build
  --snip--
   Compiling adder v0.1.0 (file:///projects/add/adder)
error[E0432]: unresolved import `rand`
 --> adder/src/main.rs:2:5
  |
2 | use rand;
  |     ^^^^ no external crate `rand`
```

Um das zu beheben, bearbeite die Datei _Cargo.toml_ des Pakets `adder` und gib
an, dass `rand` auch für dieses Paket eine Abhängigkeit ist. Beim Bauen des
Pakets `adder` wird `rand` in _Cargo.lock_ zur Liste der Abhängigkeiten von
`adder` hinzugefügt, aber es werden keine zusätzlichen Kopien von `rand`
heruntergeladen. Cargo stellt sicher, dass jedes Crate in jedem Paket im
Workspace, das das Paket `rand` verwendet, dieselbe Version verwendet, solange
sie kompatible Versionen von `rand` angeben. Das spart uns Platz und stellt
sicher, dass die Crates im Workspace miteinander kompatibel sind.

Geben Crates im Workspace inkompatible Versionen derselben Abhängigkeit an, löst
Cargo jede davon auf, versucht aber trotzdem, so wenige Versionen wie möglich
aufzulösen.

Beachte, dass Cargo Kompatibilität nur im Rahmen der Regeln der
[semantischen Versionierung][Semantic Versioning] sicherstellt. Angenommen, ein
Workspace hat ein Crate, das von `rand` 0.8.0 abhängt, und ein anderes Crate,
das von `rand` 0.8.1 abhängt. Nach den Semver-Regeln ist 0.8.1 mit 0.8.0
kompatibel, daher hängen beide Crates von 0.8.1 ab (oder möglicherweise von
einem neueren Patch wie 0.8.2). Hängt aber ein Crate von `rand` 0.7.0 und ein
anderes von `rand` 0.8.0 ab, sind diese Versionen nach Semver inkompatibel.
Daher verwendet Cargo für jedes Crate eine andere Version von `rand`.

### Einem Workspace einen Test hinzufügen {#adding-a-test-to-a-workspace}

Als weitere Verbesserung fügen wir im Crate `add_one` einen Test für die
Funktion `add_one::add_one` hinzu:

<span class="filename">Dateiname: add_one/src/lib.rs</span>

```rust,noplayground
{{#rustdoc_include ../listings/ch14-more-about-cargo/no-listing-04-workspace-with-tests/add/add_one/src/lib.rs}}
```

Führe jetzt `cargo test` im Verzeichnis _add_ auf oberster Ebene aus. Führt man
`cargo test` in einem so strukturierten Workspace aus, werden die Tests aller
Crates im Workspace ausgeführt:

<!-- manual-regeneration
cd listings/ch14-more-about-cargo/no-listing-04-workspace-with-tests/add
cargo test
copy output below; the output updating script doesn't handle subdirectories in
paths properly
-->

```console
$ cargo test
   Compiling add_one v0.1.0 (file:///projects/add/add_one)
   Compiling adder v0.1.0 (file:///projects/add/adder)
    Finished `test` profile [unoptimized + debuginfo] target(s) in 0.20s
     Running unittests src/lib.rs (target/debug/deps/add_one-93c49ee75dc46543)

running 1 test
test tests::it_works ... ok

test result: ok. 1 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s

     Running unittests src/main.rs (target/debug/deps/adder-3a47283c568d2b6a)

running 0 tests

test result: ok. 0 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s

   Doc-tests add_one

running 0 tests

test result: ok. 0 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s
```

Der erste Abschnitt der Ausgabe zeigt, dass der Test `it_works` im Crate
`add_one` bestanden hat. Der nächste Abschnitt zeigt, dass im Crate `adder`
keine Tests gefunden wurden, und der letzte Abschnitt zeigt, dass im Crate
`add_one` keine Dokumentationstests gefunden wurden.

Wir können auch vom Verzeichnis auf oberster Ebene aus die Tests eines
bestimmten Crates in einem Workspace ausführen, indem wir das Flag `-p`
verwenden und den Namen des Crates angeben, das wir testen wollen:

<!-- manual-regeneration
cd listings/ch14-more-about-cargo/no-listing-04-workspace-with-tests/add
cargo test -p add_one
copy output below; the output updating script doesn't handle subdirectories in paths properly
-->

```console
$ cargo test -p add_one
    Finished `test` profile [unoptimized + debuginfo] target(s) in 0.00s
     Running unittests src/lib.rs (target/debug/deps/add_one-93c49ee75dc46543)

running 1 test
test tests::it_works ... ok

test result: ok. 1 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s

   Doc-tests add_one

running 0 tests

test result: ok. 0 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s
```

Diese Ausgabe zeigt, dass `cargo test` nur die Tests für das Crate `add_one` und
nicht die Tests des Crates `adder` ausgeführt hat.

Wenn du die Crates im Workspace auf
[crates.io](https://crates.io/)<!-- ignore --> veröffentlichst, muss jedes Crate
im Workspace einzeln veröffentlicht werden. Wie bei `cargo test` können wir ein
bestimmtes Crate in unserem Workspace veröffentlichen, indem wir das Flag `-p`
verwenden und den Namen des Crates angeben, das wir veröffentlichen wollen.

Füge zur zusätzlichen Übung diesem Workspace auf ähnliche Weise wie beim Crate
`add_one` ein Crate `add_two` hinzu!

Wenn dein Projekt wächst, solltest du einen Workspace in Betracht ziehen: Damit
kannst du mit kleineren, leichter verständlichen Komponenten arbeiten statt mit
einem großen Klumpen Code. Außerdem kann es die Koordination zwischen Crates
erleichtern, sie in einem Workspace zu halten, wenn sie oft gleichzeitig
geändert werden.

{{#quiz ../quizzes/ch14-03-cargo-workspaces.toml}}

[Semantic Versioning]: https://semver.org/
