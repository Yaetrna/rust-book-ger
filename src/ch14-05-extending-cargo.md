## Cargo mit eigenen Befehlen erweitern {#extending-cargo-with-custom-commands}

Cargo ist so entworfen, dass du es um neue Unterbefehle erweitern kannst, ohne
es ändern zu müssen. Heißt eine Binärdatei in deinem `$PATH` `cargo-something`,
kannst du sie mit `cargo something` ausführen, als wäre sie ein Unterbefehl von
Cargo. Solche eigenen Befehle werden auch aufgelistet, wenn du `cargo --list`
ausführst. Dass man Erweiterungen mit `cargo install` installieren und dann
genau wie die eingebauten Werkzeuge von Cargo ausführen kann, ist ein äußerst
praktischer Vorteil des Designs von Cargo!

## Zusammenfassung {#summary}

Code mit Cargo und [crates.io](https://crates.io/)<!-- ignore --> zu teilen, ist
Teil dessen, was das Rust-Ökosystem für viele verschiedene Aufgaben nützlich
macht. Die Standardbibliothek von Rust ist klein und stabil, aber Crates lassen
sich leicht teilen, verwenden und verbessern, und zwar in einem anderen Zeitplan
als die Sprache. Hab keine Scheu, Code, der dir nützt, auf
[crates.io](https://crates.io/)<!-- ignore
--> zu teilen; wahrscheinlich nützt er auch jemand anderem!
