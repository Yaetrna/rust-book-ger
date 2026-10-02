## Anhang E: Editionen {#appendix-e-editions}

In Kapitel 1 hast du gesehen, dass `cargo new` deiner Datei _Cargo.toml_ einige
Metadaten über eine Edition hinzufügt. In diesem Anhang geht es darum, was das
bedeutet!

Die Sprache Rust und ihr Compiler haben einen sechswöchigen Release-Zyklus, das
heißt, Benutzer bekommen einen ständigen Strom neuer Features. Andere
Programmiersprachen veröffentlichen größere Änderungen seltener; Rust
veröffentlicht häufiger kleinere Updates. Nach einer Weile summieren sich all
diese kleinen Änderungen. Aber von Release zu Release kann es schwierig sein,
zurückzublicken und zu sagen: „Wow, zwischen Rust 1.10 und Rust 1.31 hat sich
Rust stark verändert!“

Etwa alle drei Jahre bringt das Rust-Team eine neue Rust-_Edition_ heraus. Jede
Edition bündelt die hinzugekommenen Features in einem klaren Paket mit
vollständig aktualisierter Dokumentation und aktualisierten Werkzeugen. Neue
Editionen werden als Teil des üblichen sechswöchigen Release-Prozesses
ausgeliefert.

Editionen erfüllen für verschiedene Menschen unterschiedliche Zwecke:

- Für aktive Rust-Benutzer bündelt eine neue Edition schrittweise Änderungen in
  einem leicht verständlichen Paket.
- Für Nicht-Benutzer signalisiert eine neue Edition, dass einige wichtige
  Fortschritte hinzugekommen sind, die einen erneuten Blick auf Rust lohnenswert
  machen könnten.
- Für diejenigen, die Rust entwickeln, bietet eine neue Edition einen
  gemeinsamen Bezugspunkt für das gesamte Projekt.

Zum Zeitpunkt der Entstehung dieses Textes sind vier Rust-Editionen verfügbar:
Rust 2015, Rust 2018, Rust 2021 und Rust 2024. Dieses Buch ist mit den Idiomen
der Edition Rust 2024 geschrieben.

Der Schlüssel `edition` in _Cargo.toml_ gibt an, welche Edition der Compiler für
deinen Code verwenden soll. Wenn der Schlüssel nicht vorhanden ist, verwendet
Rust aus Gründen der Abwärtskompatibilität `2015` als Wert für die Edition.

Jedes Projekt kann sich für eine andere Edition als die Standardedition 2015
entscheiden. Editionen können inkompatible Änderungen enthalten, etwa ein neues
Schlüsselwort, das mit Bezeichnern im Code kollidiert. Solange du dich aber
nicht für diese Änderungen entscheidest, kompiliert dein Code weiterhin, auch
wenn du die verwendete Version des Rust-Compilers aktualisierst.

Alle Versionen des Rust-Compilers unterstützen jede Edition, die vor dem Release
dieses Compilers existiert hat, und sie können Crates aller unterstützten
Editionen miteinander verlinken. Änderungen durch Editionen betreffen nur die
Art, wie der Compiler den Code anfänglich parst. Wenn du also Rust 2015
verwendest und eine deiner Abhängigkeiten Rust 2018 verwendet, kompiliert dein
Projekt und kann diese Abhängigkeit verwenden. Die umgekehrte Situation, in der
dein Projekt Rust 2018 und eine Abhängigkeit Rust 2015 verwendet, funktioniert
ebenfalls.

Um es klar zu sagen: Die meisten Features sind in allen Editionen verfügbar.
Entwickler, die eine beliebige Rust-Edition verwenden, sehen weiterhin
Verbesserungen, wenn neue stabile Releases erscheinen. In manchen Fällen,
hauptsächlich wenn neue Schlüsselwörter hinzukommen, sind einige neue Features
aber möglicherweise nur in späteren Editionen verfügbar. Du musst dann die
Edition wechseln, wenn du solche Features nutzen möchtest.

Weitere Details findest du im [_Rust Edition Guide_][edition-guide]. Das ist ein
vollständiges Buch, das die Unterschiede zwischen den Editionen aufzählt und
erklärt, wie du deinen Code mit `cargo fix` automatisch auf eine neue Edition
aktualisierst.

[edition-guide]: https://doc.rust-lang.org/stable/edition-guide
