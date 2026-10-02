# Abschlussbericht: Deutsche Übersetzung

Übersetzung von „The Rust Programming Language: Experimental Edition“ (Fork des
Brown CEL) ins Deutsche, Branch `de-translation` auf `Yaetrna/rust-book-ger`.
Basis-Commit: `88250e0392cef0622f318e35469108d68694c1f7`.

## 1. Stand

| Bereich                                       | Status                             |
| --------------------------------------------- | ---------------------------------- |
| `book.toml` (Titel, `language = "de"`)        | ✅                                 |
| `src/SUMMARY.md` (nur Linktexte)              | ✅                                 |
| Titelseite, Vorwort, Einleitung, Kapitel 1–21 | ✅                                 |
| Ende des Experiments, Anhänge A–G             | ✅                                 |
| Quizze (`quizzes/*.toml`, alle eingebundenen) | ✅ (nur leserseitige Texte)        |
| Glossar (`translation/GLOSSARY.md`)           | ✅, mit Änderungsprotokoll         |
| Fortschritt (`translation/STATUS.md`)         | ✅, keine offenen Vorwärtsverweise |

Alle Kapitel sind einzeln als `de: Kapitel N übersetzt` committet und gepusht.
Unverändert gegenüber der Basis sind: Codeblöcke samt Info-Strings,
Aquascope-Blöcke, Inline-Code, Direktiven, URLs/Linkziele,
Referenzdefinitionen, HTML-Attribute (außer `alt`/`caption`), Compilerausgaben,
Quiz-Schlüssel, `id`s, `type`s und Code in Quizzen. Jede Überschrift trägt ihre
ursprüngliche ID per `{#id}`.

## 2. Durchgeführte Prüfungen

| Prüfung                                                                    | Ergebnis                                                                                                                        |
| -------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| Vollständiger Build (`mdbook build`, Quiz, Aquascope, trpl-Präprozessoren) | Exit 0; Warnungen **identisch** zum Basis-Build (nur 9 bekannte Font-Awesome-/Dateinamen-Meldungen)                             |
| `check.py verify-html` gegen den Basis-Build                               | 0 Fehler, alle 590 Überschriften-IDs vorhanden                                                                                  |
| `check.py check --all` (Struktur, Code, Links, Quiz-Schlüssel)             | 215 Dateien, **0 Fehler**, 28 Warnungen (siehe 4.3)                                                                             |
| `check.py review` (Review-Grep auf erzwungene Übersetzungen)               | 53 Treffer, alle allgemeinsprachlich („Struktur“ 37, „Merkmale“ 12, „Strukturierung“ 2, „Eigenschaften“ 2)                      |
| `check.py english` (übrig gebliebenes Englisch)                            | 0 Treffer (zwei begründete Ausnahmen in `check-exceptions.toml` ergänzt)                                                        |
| dprint (nur übersetzte Dateien)                                            | alle übersetzten Dateien formatiert                                                                                             |
| CI-Lint „local file paths“ (`cargo run --bin lfp src`)                     | bestanden                                                                                                                       |
| `mdbook test --library-path packages/trpl/target/debug/deps` (wie CI)      | bestanden (Exit 0), mit `RUSTUP_TOOLCHAIN=1.90` (siehe Abschnitt 7)                                                             |
| Änderungen außerhalb des Scopes                                            | keine: `listings/`, `packages/`, `js-extensions/`, `theme/`, `ci/`, `nostarch/`, `redirects/`, `*-edition/`, Bilder unverändert |

## 3. Glossaränderungen

Das Glossar wurde vor jedem Kapitel gelesen und neue Begriffe vor ihrer ersten
Verwendung eingetragen. Das vollständige Änderungsprotokoll steht am Ende von
`translation/GLOSSARY.md`. Die wichtigsten Entscheidungen:

- **Kapitel 7–16**: Element (_item_), Eltern-/Kindmodul, Crate-Root (offen),
  weitergeben (_propagate_), Kohärenz, Implementierer, erfassen (_capture_),
  lazy (träge), Release-Profil, innere Veränderlichkeit (offen), furchtlose
  Nebenläufigkeit, Marker-Trait u. v. m.
- **Kapitel 17**: Polling/pollen, Await-Punkt, Zustandsautomat, Runtime, Task,
  aushungern (_starving_), CPU-/I/O-gebunden, selbstreferenziell, Work Stealing.
  `await` → „abwarten“ und `pin` → „fixieren“ von _offen_ auf _entschieden_.
- **Kapitel 18**: Zustandsobjekt, Unter-/Eltern-/Kindklasse, Einfachvererbung,
  Duck Typing, dyn-Kompatibilität, Abwägung beim Design, Nutzer der API.
- **Kapitel 19**: refutable/irrefutable → **abweisbar/unabweisbar** (vorher
  _offen_; jetzt _entschieden_, mit Glosse; Compilerausgabe bleibt englisch).
  Match-Arm, Auffang-Pattern, Wildcard, erschöpfend. Für _shadow_ als Verb wird
  wie in Kapitel 3 „überschatten“ verwendet.
- **Kapitel 20**: unsichere Superkräfte, Raw-Borrow-Operator, statische
  Variable, Union, Name Mangling, Lint, Operatorüberladung,
  Standard-Typparameter, divergierende Funktion, opaker Typ, Metaprogrammierung.
- **Kapitel 21 / Anhänge**: Thread-Pool, Anfrage/Antwort, lauschen, Worker,
  Auftrag (_job_), geordnetes Herunterfahren, Raw-Bezeichner, Release-Kanal,
  Feature-Flag/-Gate.
- **Vereinheitlichungen**: _raw pointer_ ist im ganzen Buch „Raw-Pointer“; in
  `ch16-04` wurde „Rohzeiger“ korrigiert. Der Linktext auf
  `ch20-03#dynamically-sized-types-and-the-sized-trait` in `ch18-02` wurde an
  den Glossarbegriff „Typ mit dynamischer Größe“ angepasst.

## 4. Offene Fragen

### 4.1 Terminologie (Status _offen_ im Glossar)

| Begriff                   | Aktuelle Wahl                    | Fundstelle                                                  | Frage                                                  |
| ------------------------- | -------------------------------- | ----------------------------------------------------------- | ------------------------------------------------------ |
| crate root                | Crate-Root (die)                 | `GLOSSARY.md:41`, `src/ch07-01-packages-and-crates.md:28`   | Genus und ob „Crate-Wurzel“ besser passt               |
| interior mutability       | innere Veränderlichkeit          | `GLOSSARY.md:132`, `src/ch15-05-interior-mutability.md:113` | Etabliert ist auch „Interior Mutability“               |
| unsound                   | unsound (fehlerhaft)             | `GLOSSARY.md:345`, `src/ch20-01-unsafe-rust.md:595`         | Alternative „nicht stichhaltig“/„nicht korrekt“        |
| Ownership Inventory #N    | Ownership-Inventur #N            | `GLOSSARY.md:380`                                           | Kapiteltitel; Alternative „Ownership-Bestandsaufnahme“ |
| `<span class="filename">` | „Dateiname: …“ (handgeschrieben) | `GLOSSARY.md:387`                                           | siehe 5.1: Generierte Spans bleiben „Filename:“        |

### 4.2 Inhaltliche Punkte

- `src/ch17-04-streams.md:23`: Der Linktext lautet „Der Trait Iterator und die
  Methode `next`“, die Zielüberschrift „Der Trait `Iterator` und die Methode
  `next`“. Grund ist die Regel, im Linktext keine Backticks hinzuzufügen; das
  Original setzt hier ebenfalls keine.
- `src/ch20-01-unsafe-rust.md:628/631`: `[the-slice-type]` ist im Original
  doppelt definiert (`ch04-04` und `ch04-03`); es gilt die erste Definition.
  Das ist ein Upstream-Fehler und wurde unverändert übernommen.
- `src/ch18-05-design-challenge.md:55/68`: dprint hat zwei strukturelle
  Kleinigkeiten normalisiert. Der „Daher …“-Absatz war vorher eine
  Lazy-Continuation des letzten Listenpunkts und steht jetzt als eigener
  Absatz. Der HTML-Kommentar hat sein führendes Leerzeichen verloren. Der Checker
  akzeptiert beides, und das Rendering ist gleichwertig.
- `quizzes/async-04-streams.toml:16`: `["D", "E", "F"]` steht im Original ohne
  Backticks. Die geraden Anführungszeichen wurden beibehalten, die
  Checker-Warnung ist bekannt.
- Das Glossieren erfolgt pro Seite beim ersten Vorkommen (Checkpoint-Entscheidung
  „Fine as is“). Die Heuristik des Checkers meldet auch nicht-rusttypische
  Verwendungen von „verschieben“, „ausleihen“ usw.; diese wurden bewusst nicht
  glossiert (siehe 4.3).

### 4.3 Verbleibende Checker-Warnungen (28, alle geprüft)

- 18× „erste Verwendung … ohne Glosse“: alltagssprachliches „verschieben“
  („Datei verschieben“, „Code verschieben“), „Gültigkeitsbereich“ in
  Nebensätzen usw. Bewusst nicht glossiert.
- 8× „Hervorhebungen“ (z. B. `ch01-02:28`, `ch04-01:134`, `ch08-03:249`):
  Kursive Glossen kommen hinzu oder fallen weg, weil eine englische Betonung im
  Deutschen anders gesetzt wird.
- 2× gerade Anführungszeichen (`ch06-04-inventory.md:14`,
  `async-04-streams.toml`): stammen aus dem Original.
- Ein Geviertstrich in `ch19-06-macros.toml` wurde zu „ – “ korrigiert und
  taucht nicht mehr auf.

## 5. Außerhalb des Scopes (nicht geändert, Handlungsbedarf)

### 5.1 Präprozessoren und Tooling (`packages/`)

- **`mdbook-trpl-listing`** erzeugt für `<Listing file-name="…">` weiterhin
  „Filename: …“. Im Buch stehen deshalb 319 generierte „Filename:“-Labels neben
  72 handübersetzten „Dateiname:“-Spans. Eine Lokalisierung bräuchte eine
  Option im Präprozessor (z. B. über `book.language`).
- **`mdbook-trpl-note`** erkennt nur das englische Präfix `> Note:`. Dieses
  Präfix bleibt daher englisch, der Rest des Hinweises ist deutsch.
- **`mdbook-quiz`**: Bedienelemente der Quizze (Buttons, „Question 1“, …) und
  die Darstellung von Compilerfehlern sind Teil des Plugins und bleiben
  englisch.
- **Aquascope**: Die Beschriftungen in den Diagrammen (R/W/O/F, Stack, Heap,
  L1 …) sind nicht übersetzbar; der Text wurde daran angepasst.
- **Bilder** (`src/img/*.svg|png`) enthalten englische Beschriftungen. Nur die
  `alt`-Texte und Bildunterschriften wurden übersetzt.

### 5.2 CI

- **Rechtschreibprüfung** (`ci/spellcheck.sh` mit `ci/dictionary.txt`, aspell
  en_US) würde nahezu jedes deutsche Wort melden. Das Wörterbuch wurde wie
  vereinbart nicht geändert. Für einen grünen CI-Lauf braucht es eine deutsche
  aspell-Sprache oder ein eigenes Wörterbuch; dafür ist eine Entscheidung nötig.
- **`nostarch/book.toml`** soll laut Kommentar in `book.toml` synchron gehalten
  werden. Titel und Sprache wurden dort nicht angepasst, weil `nostarch/` out of
  scope ist.
- **`redirects/`** und die `*-edition`-Ordner sind englisch geblieben.
- **Deployment**: Der Workflow deployt bei Pushes auf `main` nach GitHub Pages.
  Der Fork-Branch heißt `de-translation`, daher ist kein Deployment ausgelöst
  worden.

## 6. Telemetrie

Der Telemetriecode wurde nicht verändert. Befunde:

1. **Das Telemetrie-Skript ist deaktiviert.** In `book.toml` sind
   `js-extensions/packages/telemetry/dist/index.js` und das Consent-Formular
   auskommentiert. `window.telemetry` existiert daher im gebauten Buch nicht.
2. **Würde es aktiviert**, sendete `js-extensions/packages/telemetry/lib/index.ts`
   per `axios.post` an die fest eingebaute URL
   `https://rust-book.willcrichton.net/logs` (siehe `telemetry/build.mjs`). Dazu
   gehören eine zufällige Session-ID (`localStorage["__telemetry_session"]`),
   der Commit-Hash und je nach Aufrufer:
   - Quiz-Antworten (`quiz-embed`: `log("answers", {quizName, quizHash, answers, attempt})`)
   - Bug-Meldungen zu Quizfragen (`log("bug", …)`)
   - Textmarkierungen der Feedback-Erweiterung (`log("feedback", …)`)

   Gesendet wird nur, wenn der Build auf einem Branch `main`/`master` erstellt
   wurde und die Seite nicht auf `localhost` läuft.
3. **Risiko für einen deutschen Fork**: Wird das Skript auf `main` des Forks
   wieder eingeschaltet, landen Daten deutscher Leser beim Forschungsserver des
   Original-Experiments. Weil die Quiz-`id`s absichtlich unverändert sind,
   könnten deutsche Antworten mit den Studiendaten vermischt werden (der
   `quizHash` unterscheidet sich wegen des übersetzten Inhalts). Außerdem gibt
   es keine Einwilligung, solange das Consent-Formular deaktiviert ist.
   Empfehlung: die Telemetrie im Fork deaktiviert lassen oder eine eigene URL mit
   eigener Einwilligung verwenden.
4. **Feedback-Erweiterung** (aktiv): Sie speichert Markierungen nur lokal
   (`localStorage`). `lib/selection.tsx:92` ruft `window.telemetry?.log`
   abgesichert auf. `lib/renderer.tsx:29` ruft dagegen `window.telemetry.log`
   **ohne** `?.` auf; beim Entfernen einer Markierung wirft das bei
   deaktivierter Telemetrie einen `TypeError` in der Konsole. Das ist ein
   Upstream-Fehler und wurde nicht geändert.
5. **Quiz-Antwort-Cache**: `cache-answers = true` speichert Antworten lokal im
   Browser. Das ist unabhängig von der Telemetrie.
6. Die Seite **„Ende des Experiments“** verweist weiterhin auf das
   Original-Experiment (Mastodon-Link). Ob sie im deutschen Fork sinnvoll ist,
   ist eine redaktionelle Entscheidung.

## 7. Nicht oder nur eingeschränkt durchgeführte Prüfungen

- **Rechtschreibprüfung (`ci/spellcheck.sh`)**: nicht ausgeführt. aspell ist
  nicht installiert und das Wörterbuch ist englisch (siehe 5.2).
- **Shellcheck**: nicht relevant, keine Skripte geändert.
- **Linkchecker / `ci/validate.sh`**: sind in der CI auskommentiert und wurden
  nicht ausgeführt. Ersatzweise prüft `check.py` alle Referenzdefinitionen,
  Linkziele und Anker gegen die Basis, und `verify-html` prüft alle
  Überschriften-IDs.
- **`mdbook test`**: bestanden. Beim ersten Lauf schlugen die
  Kapitel-17-Tests mit `E0514` fehl: `trpl` war mit rustc 1.90 gebaut (Pin in
  `rust-toolchain`), mdbook rief rustdoc aber außerhalb des Repos mit der
  Default-Toolchain 1.97 auf. Mit `RUSTUP_TOOLCHAIN=1.90` laufen alle Tests
  durch. Das ist ein Umgebungsproblem und hat nichts mit der Übersetzung zu tun.
- **Inhaltliches Lektorat durch Muttersprachler**: steht aus. Empfohlen ist ein
  Review der Kapitel 17 (Async) und 20 (Unsafe/Makros), weil dort die meisten
  neuen Begriffe festgelegt wurden.

## 8. Hinweise zur Lizenz

Die Lizenzdateien sind unverändert. Auf der Titelseite (`src/title-page.md`)
steht ein Übersetzerhinweis, dass es sich um eine inoffizielle deutsche
Übersetzung des englischen Originals handelt.
