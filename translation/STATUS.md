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

| Datei                                     | Quizze                                                   | Status |
| ----------------------------------------- | -------------------------------------------------------- | ------ |
| `src/SUMMARY.md`                          | –                                                        | ✅     |
| `src/ch04-02-references-and-borrowing.md` | `ch04-02-references-sec{1-basics,2-perms,3-safety}.toml` | ✅     |
| alle übrigen Dateien in `src/`            | alle übrigen Dateien in `quizzes/`                       | ⬜     |

`book.toml`: `language = "de"`, Titel „Die Programmiersprache Rust“ (freigegeben).

`src/experiment-intro.md`: nur der Übersetzerhinweis ist ergänzt; die Seite
selbst ist noch nicht übersetzt.

**Checkpoint:** Pilot freigegeben. Entscheidungen dazu:

- Titel „Die Programmiersprache Rust“, auch in Zeile 1 von `src/SUMMARY.md`.
- `src/title-page.md:14` („only available online and in English“) wird beim
  Übersetzen sinngemäß angepasst, nicht wörtlich übersetzt.
- „Hello, World!“ / „Hello, Cargo!“ bleiben.
- `> Note:` bleibt englisch, bis der Präprozessor geändert ist.
- Glossen für Compiler-Begriffe pro Seite (kann sich noch ändern).
- Push auf den eigenen Fork erlaubt (kein PR).

## Werkzeuge und Build (Pilot)

- mdBook 0.5.2 (Release-Binary, wie in CI).
- mdbook-quiz 0.5.0, lokal **ohne** das Feature `aquascope` gebaut
  (`cargo install mdbook-quiz --version 0.5.0 --no-default-features`). Das
  „full“-Release-Binary braucht beim Start die Aquascope-Nightly-Toolchain.
- mdbook-aquascope: **nicht installiert** (braucht `nightly-2026-05-01` mit
  `rustc-dev` und `miri`). Für den Build wird ein Durchreich-Stub verwendet. Die
  `aquascope`-Blöcke werden darum nicht als Diagramme gerendert; ihre
  Byte-Identität prüft `check.py`.
- mdbook-trpl-note / mdbook-trpl-listing: aus `packages/mdbook-trpl` per
  `cargo run` (wie in `book.toml` konfiguriert).
- dprint 0.50.2 mit `@dprint/markdown` 0.17.8 (gleiche Plugin-Version wie in
  `dprint.jsonc`, lokal aus npm, da `plugins.dprint.dev` im Sandbox-Netz
  gesperrt ist).
- Python 3.11 + `markdown-it-py` 3.0.0 für `check.py`.

## Wiederaufnahme nach Unterbrechung

1. `git log --oneline 88250e0..de-translation` zeigt die erledigten Kapitel.
2. Die Tabelle oben aktualisieren.
3. Vor jedem Kapitel `translation/GLOSSARY.md` lesen.
4. Nach jeder Datei: `python3 translation/check.py <datei> <quizze>` und
   `python3 translation/check.py --review <datei>`.
