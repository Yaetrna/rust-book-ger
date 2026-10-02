# Status der deutschen Übersetzung

## Basis

- Upstream: <https://github.com/cognitive-engineering-lab/rust-book>
- Basis-Commit: `88250e0392cef0622f318e35469108d68694c1f7`
  („Merge pull request #394 from cognitive-engineering-lab/dev“)
- Arbeitsbranch: `de-translation`

Alle Prüfungen in `translation/check.py` vergleichen gegen diesen Commit.

## Einstellungen

| Einstellung           | Wert                                     |
| --------------------- | ---------------------------------------- |
| Anrede                | „du“ (klein); „wir“, wo das Buch spricht |
| Code-Kommentare       | KEEP (Code bleibt byte-identisch)        |
| Checkpoint nach Pilot | ON                                       |

## Fortschritt

Legende: ✅ übersetzt und geprüft · 🔶 in Arbeit · ⬜ offen

| Teil                                      | Dateien                                      | Status |
| ----------------------------------------- | -------------------------------------------- | ------ |
| `src/SUMMARY.md`                          | –                                            | ✅     |
| Vorspann                                  | experiment-intro, title-page, foreword, ch00 | ✅     |
| Kapitel 1                                 | ch01-* mit Quizzen                           | ✅     |
| Kapitel 2                                 | ch02-00                                      | ✅     |
| Kapitel 3                                 | ch03-* mit Quizzen                           | ✅     |
| Kapitel 4                                 | ch04-* mit Quizzen                           | ✅     |
| Kapitel 5                                 | ch05-* mit Quizzen                           | ✅     |
| Kapitel 6                                 | ch06-* mit Quizzen                           | ✅     |
| Kapitel 7                                 | ch07-* mit Quizzen                           | ✅     |
| Kapitel 8                                 | ch08-* mit Quizzen                           | ✅     |
| Kapitel 9                                 | ch09-* mit Quizzen                           | ✅     |
| Kapitel 10                                | ch10-* mit Quizzen                           | ✅     |
| Kapitel 11                                | ch11-* mit Quizzen                           | ✅     |
| Kapitel 12–21, Anhänge, end-of-experiment | –                                            | ⬜     |

`book.toml`: `language = "de"`, Titel „Die Programmiersprache Rust“ (freigegeben).

**Checkpoint:** Pilot freigegeben. Entscheidungen dazu:

- Titel „Die Programmiersprache Rust“, auch in Zeile 1 von `src/SUMMARY.md`.
- `src/title-page.md:14` („only available online and in English“) wird beim
  Übersetzen sinngemäß angepasst, nicht wörtlich übersetzt.
- „Hello, World!“ / „Hello, Cargo!“ bleiben.
- `> Note:` bleibt englisch, bis der Präprozessor geändert ist.
- Glossen für Compiler-Begriffe pro Seite (kann sich noch ändern).
- Push auf den eigenen Fork erlaubt (kein PR).

## Werkzeuge und Build

Seit dem Checkpoint wird mit denselben Werkzeugen wie in CI gebaut:

- mdBook 0.5.2, mdbook-quiz 0.5.0 („full“), Aquascope 0.4.0 (Release-Binaries).
- Toolchain `nightly-2026-05-01` mit `rust-src`, `rustc-dev`,
  `llvm-tools-preview`, `miri`; `cargo +nightly-2026-05-01 miri setup`;
  `LD_LIBRARY_PATH=$(rustup run nightly-2026-05-01 rustc --print target-libdir)`.
- mdbook-trpl-note / mdbook-trpl-listing aus `packages/mdbook-trpl` per
  `cargo run` (wie in `book.toml`).
- dprint 0.50.2 mit `@dprint/markdown` 0.17.8 (aus npm, da
  `plugins.dprint.dev` im Sandbox-Netz gesperrt ist).
- Python 3.11 + `markdown-it-py` 3.0.0 + `mdit-py-plugins` für `check.py`.

## Wiederaufnahme nach Unterbrechung

1. `git log --oneline 88250e0..de-translation` zeigt die erledigten Kapitel.
2. Die Tabelle oben aktualisieren.
3. Vor jedem Kapitel `translation/GLOSSARY.md` lesen.
4. Nach jeder Datei: `python3 translation/check.py <datei> <quizze>` und
   `python3 translation/check.py --review <datei>`.

## Vorwärtsverweise

Links auf Abschnitte, die noch nicht übersetzt sind. Beim Übersetzen des Ziels
die Überschrift so wählen, dass sie zum Linktext passt (oder den Linktext
anpassen).

| Ziel                                                         | Linktext                                                     | Quelle  |
| ------------------------------------------------------------ | ------------------------------------------------------------ | ------- |
| ch14-02#exporting-a-convenient-public-api-with-pub-use       | „Eine bequeme öffentliche API exportieren“                   | ch07-04 |
| ch11-01#how-to-write-tests                                   | „Wie man Tests schreibt“                                     | ch07-04 |
| ch10-03#validating-references-with-lifetimes                 | „Referenzen mit Lifetimes validieren“                        | ch08-03 |
| ch18-02#using-trait-objects-to-abstract-over-shared-behavior | „Mit Trait-Objekten über gemeinsames Verhalten abstrahieren“ | ch09-02 |
| ch18-03#encoding-states-and-behavior-as-types                | „Zustände und Verhalten als Typen kodieren“                  | ch09-03 |
| ch13-02 (Seite)                                              | „Eine Folge von Elementen mit Iteratoren verarbeiten“        | ch08-01 |
| ch14-02#documentation-comments-as-tests                      | „Dokumentationskommentare als Tests“                         | ch11-01 |
