## Builds mit Release-Profilen anpassen {#customizing-builds-with-release-profiles}

In Rust sind _Release-Profile_ (_release profiles_) vordefinierte, anpassbare
Profile mit unterschiedlichen Konfigurationen, die Programmierenden mehr
Kontrolle über verschiedene Optionen beim Kompilieren von Code geben. Jedes
Profil wird unabhängig von den anderen konfiguriert.

Cargo hat zwei Hauptprofile: das Profil `dev`, das Cargo verwendet, wenn du
`cargo
build` ausführst, und das Profil `release`, das Cargo verwendet, wenn du
`cargo build
--release` ausführst. Das Profil `dev` ist mit guten Standardwerten
für die Entwicklung definiert, und das Profil `release` hat gute Standardwerte
für Release-Builds.

Diese Profilnamen kennst du vielleicht aus der Ausgabe deiner Builds:

<!-- manual-regeneration
anywhere, run:
cargo build
cargo build --release
and ensure output below is accurate
-->

```console
$ cargo build
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.00s
$ cargo build --release
    Finished `release` profile [optimized] target(s) in 0.32s
```

`dev` und `release` sind diese verschiedenen Profile, die der Compiler
verwendet.

Cargo hat für jedes der Profile Standardeinstellungen, die gelten, wenn du in
der Datei _Cargo.toml_ des Projekts keine `[profile.*]`-Abschnitte explizit
hinzugefügt hast. Indem du `[profile.*]`-Abschnitte für die Profile hinzufügst,
die du anpassen willst, überschreibst du eine beliebige Teilmenge der
Standardeinstellungen. Hier sind zum Beispiel die Standardwerte der Einstellung
`opt-level` für die Profile `dev` und `release`:

<span class="filename">Dateiname: Cargo.toml</span>

```toml
[profile.dev]
opt-level = 0

[profile.release]
opt-level = 3
```

Die Einstellung `opt-level` steuert, wie viele Optimierungen Rust auf deinen
Code anwendet, in einem Bereich von 0 bis 3. Mehr Optimierungen verlängern die
Kompilierzeit. Wenn du also gerade entwickelst und deinen Code oft kompilierst,
willst du weniger Optimierungen, um schneller zu kompilieren, auch wenn der
resultierende Code langsamer läuft. Das Standard-`opt-level` für `dev` ist daher
`0`. Wenn du bereit bist, deinen Code zu veröffentlichen, investierst du am
besten mehr Zeit ins Kompilieren. Du kompilierst im Release-Modus nur einmal,
führst das kompilierte Programm aber viele Male aus, daher tauscht der
Release-Modus längere Kompilierzeit gegen schneller laufenden Code. Deshalb ist
das Standard-`opt-level` für das Profil `release` `3`.

Du kannst eine Standardeinstellung überschreiben, indem du in _Cargo.toml_ einen
anderen Wert dafür angibst. Wollen wir zum Beispiel im Entwicklungsprofil die
Optimierungsstufe 1 verwenden, können wir diese beiden Zeilen zur Datei
_Cargo.toml_ unseres Projekts hinzufügen:

<span class="filename">Dateiname: Cargo.toml</span>

```toml
[profile.dev]
opt-level = 1
```

Dieser Code überschreibt die Standardeinstellung `0`. Wenn wir jetzt
`cargo build` ausführen, verwendet Cargo die Standardwerte für das Profil `dev`
plus unsere Anpassung von `opt-level`. Da wir `opt-level` auf `1` gesetzt haben,
wendet Cargo mehr Optimierungen an als standardmäßig, aber nicht so viele wie
bei einem Release-Build.

Die vollständige Liste der Konfigurationsoptionen und Standardwerte für jedes
Profil findest du in
[der Dokumentation von Cargo](https://doc.rust-lang.org/cargo/reference/profiles.html).

{{#quiz ../quizzes/ch14-01-release-profiles.toml}}
