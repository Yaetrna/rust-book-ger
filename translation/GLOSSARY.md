# Glossar für die deutsche Übersetzung

Dieses Glossar ist verbindlich. Vor jedem Kapitel lesen; neue Begriffe hier
eintragen, **bevor** sie im Text verwendet werden. Ändert sich eine
Entscheidung, müssen alle bereits übersetzten Dateien nachgezogen werden
(Änderungen unten unter „Änderungsprotokoll“ festhalten).

## Entscheidungsregel

In dieser Reihenfolge anwenden:

1. **Code jeder Art** (Schlüsselwörter, Bezeichner, Typ-/Trait-/Makro-/
   Crate-Namen, Attribute, Befehle, Flags, Pfade, Compiler- und
   Cargo-Ausgaben): nie übersetzen, Backticks exakt wie im Original.
2. **Rust-spezifischer Begriff oder ein Begriff, der in der deutschsprachigen
   Rust-Community normalerweise englisch verwendet wird:** englisch lassen,
   aber als deutsches Nomen behandeln: großschreiben, festes Genus,
   Komposita mit Bindestrich (Trait-Objekt, Borrow-Checker,
   Lifetime-Parameter, `impl`-Block).
3. **Allgemeines Programmiervokabular mit etabliertem deutschem Begriff:**
   übersetzen (Funktion, Variable, Referenz, Typ, Wert, Schleife, Ausdruck).
4. **Unsicher?** Englisch lassen, beim ersten Auftreten kurz auf Deutsch
   erklären, hier mit Status `offen` eintragen.

Keine Terminologie aus anderen deutschen Rust-Übersetzungen übernehmen.

**Status:** `fest` = Vorgabe des Auftrags · `entschieden` = im Lauf der
Übersetzung festgelegt · `offen` = vorläufig (englisch + Glosse), bitte prüfen.

## 1. Englisch beibehalten (Rust-Begriffe)

| Englisch                                              | Deutsch                           | Genus / Plural                      | Hinweis                                                                      | Status      |
| ----------------------------------------------------- | --------------------------------- | ----------------------------------- | ---------------------------------------------------------------------------- | ----------- |
| trait                                                 | Trait                             | der / die Traits                    | nie „Eigenschaft“, „Merkmal“                                                 | fest        |
| trait object                                          | Trait-Objekt                      | das / die Trait-Objekte             |                                                                              | fest        |
| trait bound                                           | Trait-Bound                       | der / die Trait-Bounds              |                                                                              | fest        |
| supertrait                                            | Supertrait                        | der / die Supertraits               |                                                                              | entschieden |
| crate                                                 | Crate                             | das / die Crates                    | nie „Kiste“                                                                  | fest        |
| binary crate                                          | Binary-Crate                      | das / die Binary-Crates             | Cargo-Ausgabe sagt „binary“                                                  | entschieden |
| library crate                                         | Library-Crate                     | das / die Library-Crates            | Cargo-Ausgabe sagt „library“                                                 | entschieden |
| crate root                                            | Crate-Root                        | die / die Crate-Roots               | beim ersten Auftreten: „Crate-Root (die Wurzeldatei des Modulbaums)“         | offen       |
| struct                                                | Struct                            | das / die Structs                   | nie „Struktur“                                                               | fest        |
| tuple struct                                          | Tupel-Struct                      | das / die Tupel-Structs             |                                                                              | entschieden |
| unit-like struct                                      | Unit-artiges Struct               | das / die Unit-artigen Structs      |                                                                              | entschieden |
| enum                                                  | Enum                              | das / die Enums                     | nie „Aufzählung“                                                             | fest        |
| closure                                               | Closure                           | die / die Closures                  | nie „Abschluss“                                                              | fest        |
| lifetime                                              | Lifetime                          | die / die Lifetimes                 | nie „Lebensdauer“; Lifetime-Parameter, Lifetime-Annotation, Lifetime-Elision | fest        |
| ownership                                             | Ownership                         | die / –                             | nie „Eigentümerschaft“                                                       | fest        |
| owner                                                 | Owner                             | der / die Owner                     | nie „Eigentümer“                                                             | fest        |
| borrowing                                             | Borrowing                         | das / –                             | Verb: ausleihen                                                              | fest        |
| borrow (Nomen)                                        | Borrow                            | der / die Borrows                   |                                                                              | fest        |
| borrow checker                                        | Borrow-Checker                    | der / die Borrow-Checker            | nie „Ausleihprüfer“                                                          | fest        |
| move (Nomen)                                          | Move                              | der / die Moves                     | Verb: verschieben                                                            | fest        |
| slice                                                 | Slice                             | der / die Slices                    |                                                                              | fest        |
| string slice                                          | String-Slice                      | der / die String-Slices             |                                                                              | fest        |
| string                                                | String                            | der / die Strings                   | nie „Zeichenkette“                                                           | fest        |
| stack                                                 | Stack                             | der / die Stacks                    | nie „Stapelspeicher“                                                         | fest        |
| heap                                                  | Heap                              | der / die Heaps                     | nie „Haldenspeicher“                                                         | fest        |
| (stack) frame                                         | Frame, Stack-Frame                | der / die Frames                    |                                                                              | fest        |
| box                                                   | Box                               | die / die Boxen                     |                                                                              | fest        |
| smart pointer                                         | Smart-Pointer                     | der / die Smart-Pointer             | nie „intelligenter Zeiger“                                                   | fest        |
| raw pointer                                           | Raw-Pointer                       | der / die Raw-Pointer               | analog zu Smart-Pointer                                                      | entschieden |
| pattern                                               | Pattern                           | das / die Patterns                  | nie „Muster“                                                                 | fest        |
| pattern matching                                      | Pattern-Matching                  | das / –                             |                                                                              | fest        |
| match arm                                             | Arm, `match`-Arm                  | der / die Arme                      | gleiches Wort im Deutschen                                                   | entschieden |
| match expression / match (ohne Backticks im Original) | Match-Ausdruck, Match-Arm         | der                                 | mit Backticks im Original: `match`-Ausdruck; nie Backticks ergänzen          | entschieden |
| match guard                                           | Match-Guard                       | der / die Match-Guards              |                                                                              | entschieden |
| generics                                              | Generics                          | die (Pl.)                           | Adjektiv „generic“ → „generisch“ (generischer Typ, generische Funktion)      | fest        |
| iterator                                              | Iterator                          | der / die Iteratoren                |                                                                              | fest        |
| panic (Nomen)                                         | Panic                             | der / die Panics                    | nie „Panik“; Verb: „einen Panic auslösen“                                    | fest        |
| shadowing                                             | Shadowing                         | das / –                             |                                                                              | fest        |
| aliasing                                              | Aliasing                          | das / –                             |                                                                              | fest        |
| alias (Nomen)                                         | Alias                             | der / die Aliasse                   | „data is aliased“ → „auf die Daten gibt es Aliasse“ o. ä.                    | entschieden |
| workspace                                             | Workspace                         | der / die Workspaces                |                                                                              | fest        |
| thread                                                | Thread                            | der / die Threads                   |                                                                              | fest        |
| future                                                | Future                            | das / die Futures                   |                                                                              | fest        |
| stream (async)                                        | Stream                            | der / die Streams                   |                                                                              | entschieden |
| task (async)                                          | Task                              | der / die Tasks                     |                                                                              | entschieden |
| runtime (async-Bibliothek)                            | Runtime                           | die / die Runtimes                  | nur für Async-Runtimes; Zeitpunkt „runtime“ → Laufzeit                       | entschieden |
| executor                                              | Executor                          | der / die Executors                 |                                                                              | entschieden |
| place                                                 | Place                             | der / die Places                    | alles, was links in einer Zuweisung stehen kann                              | fest        |
| prelude                                               | Prelude                           | das / die Preludes                  |                                                                              | entschieden |
| edition                                               | Edition                           | die / die Editionen                 | Rust 2024 Edition → Rust-Edition 2024                                        | entschieden |
| hash map                                              | Hash-Map                          | die / die Hash-Maps                 | Typ `HashMap<K, V>`                                                          | entschieden |
| collection                                            | Collection                        | die / die Collections               | wie `std::collections`                                                       | entschieden |
| array                                                 | Array                             | das / die Arrays                    | nicht „Feld“ (Verwechslung mit _field_)                                      | entschieden |
| deref coercion                                        | Deref-Coercion                    | die / die Deref-Coercions           |                                                                              | entschieden |
| newtype                                               | Newtype, Newtype-Pattern          | der / das                           |                                                                              | entschieden |
| design pattern                                        | Design-Pattern                    | das / die Design-Patterns           | nicht „Entwurfsmuster“ (hält den Review-Grep auf „Muster“ sauber)            | entschieden |
| state pattern                                         | State-Pattern                     | das / –                             |                                                                              | entschieden |
| builder pattern                                       | Builder-Pattern                   | das / –                             |                                                                              | entschieden |
| orphan rule                                           | Orphan-Rule                       | die / –                             |                                                                              | entschieden |
| blanket implementation                                | Blanket-Implementierung           | die / die Blanket-Implementierungen |                                                                              | entschieden |
| dispatch (static/dynamic)                             | statischer / dynamischer Dispatch | der / –                             |                                                                              | entschieden |
| zero-cost abstraction                                 | Zero-Cost-Abstraktion             | die / die Zero-Cost-Abstraktionen   |                                                                              | entschieden |
| garbage collection                                    | Garbage-Collection                | die / –                             | wie in der deutschen Wikipedia                                               | entschieden |
| garbage collector                                     | Garbage-Collector                 | der / die Garbage-Collectors        |                                                                              | entschieden |
| data race                                             | Data-Race                         | das / die Data-Races                |                                                                              | entschieden |
| race condition                                        | Race-Condition                    | die / die Race-Conditions           |                                                                              | entschieden |
| deadlock                                              | Deadlock                          | der / die Deadlocks                 |                                                                              | entschieden |
| mutex                                                 | Mutex                             | der / die Mutexe                    |                                                                              | entschieden |
| use-after-free                                        | Use-after-free                    | das / –                             |                                                                              | entschieden |
| double free                                           | Double-Free                       | das / –                             |                                                                              | entschieden |
| registry                                              | Registry                          | die / die Registrys                 | crates.io-Registry                                                           | entschieden |
| toolchain                                             | Toolchain                         | die / die Toolchains                |                                                                              | entschieden |
| release channel                                       | Stable, Beta, Nightly             | –                                   | Kanalnamen bleiben englisch                                                  | entschieden |
| getter                                                | Getter                            | der / die Getter                    |                                                                              | entschieden |
| feature flag                                          | Feature-Flag                      | das / die Feature-Flags             |                                                                              | entschieden |
| unsafe Rust                                           | Unsafe Rust                       | –                                   | Eigenname des Sprachteils; Code: `unsafe`-Block, `unsafe`-Funktion           | entschieden |
| refactoring                                           | Refactoring                       | das / die Refactorings              | Verb: refaktorisieren                                                        | entschieden |
| feature (Sprachfeature)                               | Feature                           | das / die Features                  | „language feature“ → Sprachfeature; nicht „Merkmal“, nicht „Eigenschaft“     | entschieden |
| push (die Operation)                                  | Push                              | der / die Pushes                    | nur ohne Backticks im Original; mit Backticks bleibt es `push`               | entschieden |

## 2. Übersetzt

| Englisch                                   | Deutsch                                            | Genus / Plural                    | Hinweis                                                | Status      |
| ------------------------------------------ | -------------------------------------------------- | --------------------------------- | ------------------------------------------------------ | ----------- |
| package                                    | Paket                                              | das / die Pakete                  |                                                        | fest        |
| module                                     | Modul                                              | das / die Module                  |                                                        | fest        |
| module tree                                | Modulbaum                                          | der / die Modulbäume              |                                                        | entschieden |
| macro                                      | Makro                                              | das / die Makros                  | deklaratives / prozedurales Makro                      | fest        |
| reference                                  | Referenz                                           | die / die Referenzen              |                                                        | fest        |
| immutable / shared reference               | unveränderliche / geteilte Referenz                | die                               | _shared reference_ beim ersten Auftreten englisch dazu | entschieden |
| mutable / unique reference                 | veränderliche / exklusive Referenz                 | die                               | _unique_ heißt hier „exklusiv“; englisch dazu          | entschieden |
| dangling reference                         | hängende Referenz                                  | die / die hängenden Referenzen    | (_dangling reference_) beim ersten Auftreten           | entschieden |
| pointer                                    | Zeiger                                             | der / die Zeiger                  |                                                        | fest        |
| non-owning pointer                         | nicht-besitzender Zeiger                           | der                               |                                                        | entschieden |
| owned pointer                              | besitzender Zeiger                                 | der                               |                                                        | entschieden |
| function pointer                           | Funktionszeiger                                    | der / die Funktionszeiger         |                                                        | entschieden |
| mutable / immutable                        | veränderlich / unveränderlich                      | –                                 | Glosse pro Seite, siehe Abschnitt 5                    | fest        |
| mutability                                 | Veränderlichkeit                                   | die / –                           |                                                        | entschieden |
| interior mutability                        | innere Veränderlichkeit                            | die / –                           | beim ersten Auftreten: (_interior mutability_)         | offen       |
| mutate / mutation                          | verändern / Veränderung                            | die / die Veränderungen           |                                                        | entschieden |
| scope                                      | Gültigkeitsbereich                                 | der / die Gültigkeitsbereiche     | nie „out of scope“; Glosse pro Seite                   | fest        |
| permission                                 | Berechtigung                                       | die / die Berechtigungen          |                                                        | fest        |
| undefined behavior                         | undefiniertes Verhalten                            | das / –                           |                                                        | fest        |
| compile time                               | Kompilierzeit                                      | die / –                           |                                                        | fest        |
| runtime (Zeitpunkt)                        | Laufzeit                                           | die / –                           |                                                        | fest        |
| statement                                  | Anweisung                                          | die / die Anweisungen             |                                                        | fest        |
| expression                                 | Ausdruck                                           | der / die Ausdrücke               |                                                        | fest        |
| field                                      | Feld                                               | das / die Felder                  |                                                        | fest        |
| variant                                    | Variante                                           | die / die Varianten               |                                                        | fest        |
| associated function                        | assoziierte Funktion                               | die / die assoziierten Funktionen |                                                        | fest        |
| associated type                            | assoziierter Typ                                   | der / die assoziierten Typen      |                                                        | entschieden |
| method                                     | Methode                                            | die / die Methoden                |                                                        | entschieden |
| method call                                | Methodenaufruf                                     | der / die Methodenaufrufe         |                                                        | entschieden |
| receiver                                   | Empfänger                                          | der / die Empfänger               | für Methoden und Kanäle                                | entschieden |
| allocate / deallocate                      | allozieren / freigeben                             | –                                 |                                                        | fest        |
| allocation / deallocation                  | Allokation / Freigabe                              | die                               |                                                        | entschieden |
| allocator                                  | Allokator                                          | der / die Allokatoren             |                                                        | entschieden |
| concurrency                                | Nebenläufigkeit                                    | die / –                           |                                                        | fest        |
| parallelism                                | Parallelität                                       | die / –                           |                                                        | entschieden |
| listing                                    | Listing                                            | das / die Listings                |                                                        | fest        |
| type                                       | Typ                                                | der / die Typen                   |                                                        | entschieden |
| value                                      | Wert                                               | der / die Werte                   |                                                        | entschieden |
| variable                                   | Variable                                           | die / die Variablen               |                                                        | entschieden |
| function                                   | Funktion                                           | die / die Funktionen              |                                                        | entschieden |
| parameter / argument                       | Parameter / Argument                               | der / das                         |                                                        | entschieden |
| return value                               | Rückgabewert                                       | der / die Rückgabewerte           |                                                        | entschieden |
| signature                                  | Signatur                                           | die / die Signaturen              |                                                        | entschieden |
| implement / implementation                 | implementieren / Implementierung                   | die                               | `impl`-Block                                           | entschieden |
| default implementation                     | Standardimplementierung                            | die                               |                                                        | entschieden |
| type annotation                            | Typannotation                                      | die / die Typannotationen         |                                                        | entschieden |
| type inference                             | Typinferenz                                        | die / –                           |                                                        | entschieden |
| type alias                                 | Typalias                                           | der / die Typaliasse              |                                                        | entschieden |
| dynamically sized type                     | Typ mit dynamischer Größe                          | der                               | (_dynamically sized type_, DST)                        | entschieden |
| never type                                 | Never-Typ                                          | der / –                           |                                                        | entschieden |
| unit type                                  | Unit-Typ                                           | der / –                           |                                                        | entschieden |
| loop                                       | Schleife                                           | die / die Schleifen               |                                                        | entschieden |
| loop label                                 | Schleifenlabel                                     | das / die Schleifenlabels         |                                                        | entschieden |
| control flow                               | Kontrollfluss                                      | der / –                           |                                                        | entschieden |
| branch                                     | Zweig                                              | der / die Zweige                  |                                                        | entschieden |
| condition                                  | Bedingung                                          | die / die Bedingungen             |                                                        | entschieden |
| tuple                                      | Tupel                                              | das / die Tupel                   |                                                        | entschieden |
| vector                                     | Vektor                                             | der / die Vektoren                | Typ `Vec<T>`                                           | entschieden |
| integer                                    | Ganzzahl                                           | die / die Ganzzahlen              | Ganzzahltyp, Ganzzahlüberlauf                          | entschieden |
| floating-point number                      | Gleitkommazahl                                     | die / die Gleitkommazahlen        |                                                        | entschieden |
| Boolean                                    | boolescher Wert                                    | der                               |                                                        | entschieden |
| character                                  | Zeichen                                            | das / die Zeichen                 |                                                        | entschieden |
| literal                                    | Literal                                            | das / die Literale                |                                                        | entschieden |
| range                                      | Bereich                                            | der / die Bereiche                | (_range_) beim ersten Auftreten                        | entschieden |
| keyword                                    | Schlüsselwort                                      | das / die Schlüsselwörter         |                                                        | entschieden |
| identifier                                 | Bezeichner                                         | der / die Bezeichner              |                                                        | entschieden |
| operator                                   | Operator                                           | der / die Operatoren              | Dereferenzierungsoperator, Fragezeichen-Operator       | entschieden |
| attribute                                  | Attribut                                           | das / die Attribute               |                                                        | entschieden |
| comment / doc comment                      | Kommentar / Dokumentationskommentar                | der                               |                                                        | entschieden |
| bracket(s)                                 | Klammer(n)                                         | die                               | geschweifte / eckige / spitze / runde Klammern         | entschieden |
| semicolon                                  | Semikolon                                          | das / die Semikolons              |                                                        | entschieden |
| placeholder                                | Platzhalter                                        | der / die Platzhalter             |                                                        | entschieden |
| binding                                    | Bindung                                            | die / die Bindungen               |                                                        | entschieden |
| destructure                                | destrukturieren / Destrukturierung                 | die                               |                                                        | entschieden |
| dereference                                | dereferenzieren / Dereferenzierung                 | die                               |                                                        | entschieden |
| path                                       | Pfad                                               | der / die Pfade                   |                                                        | entschieden |
| public / private                           | öffentlich / privat                                | –                                 |                                                        | entschieden |
| privacy / visibility                       | Sichtbarkeit                                       | die / –                           |                                                        | entschieden |
| re-export                                  | Re-Export / reexportieren                          | der                               |                                                        | entschieden |
| item (Modulsystem)                         | Element                                            | das / die Elemente                | Funktion, Struct, Modul usw.                           | entschieden |
| parent / child module                      | Elternmodul / Kindmodul                            | das / die …module                 |                                                        | entschieden |
| submodule                                  | Untermodul                                         | das / die Untermodule             |                                                        | entschieden |
| ancestor module                            | Vorfahrenmodul                                     | das / die Vorfahrenmodule         |                                                        | entschieden |
| sibling (Module)                           | Geschwister                                        | die (Pl.)                         |                                                        | entschieden |
| module tree                                | Modulbaum                                          | der / die Modulbäume              |                                                        | entschieden |
| glob operator                              | Glob-Operator                                      | der / –                           |                                                        | entschieden |
| front / back of house                      | Front of House / Back of House                     | das                               | Gastronomiebegriffe, englisch belassen                 | entschieden |
| grapheme cluster                           | Graphem-Cluster                                    | das / die Graphem-Cluster         |                                                        | entschieden |
| Unicode scalar value                       | Unicode-Skalarwert                                 | der / die …werte                  |                                                        | entschieden |
| wrapper                                    | Wrapper                                            | der / die Wrapper                 | „ein Wrapper um …“                                     | entschieden |
| hashing function / hasher                  | Hashfunktion / Hasher                              | die / der                         |                                                        | entschieden |
| Pig Latin                                  | Pig Latin                                          | das                               | Sprachspiel, englische Beispielwörter bleiben          | entschieden |
| propagate (errors)                         | weitergeben / Weitergabe                           | die                               | (_propagating_) bei der Einführung                     | entschieden |
| file handle                                | Datei-Handle                                       | das / die Datei-Handles           |                                                        | entschieden |
| question mark operator                     | Fragezeichen-Operator / Operator `?`               | der                               |                                                        | entschieden |
| unwinding / aborting (panic)               | Abwickeln / Abbrechen                              | das                               | (_unwinding_) / (_aborting_) bei der Einführung        | entschieden |
| backtrace                                  | Backtrace                                          | der / die Backtraces              |                                                        | entschieden |
| contract (API)                             | Vertrag                                            | der / die Verträge                |                                                        | entschieden |
| buffer overread                            | Buffer Overread                                    | der                               | Glosse „Lesen über das Pufferende hinaus“              | entschieden |
| coherence                                  | Kohärenz                                           | die                               | (_coherence_) bei der Einführung                       | entschieden |
| implementor                                | Implementierer                                     | der / die Implementierer          | Typ, der einen Trait implementiert                     | entschieden |
| where clause                               | `where`-Klausel                                    | die / die `where`-Klauseln        |                                                        | entschieden |
| input / output lifetimes                   | Eingabe-Lifetimes / Ausgabe-Lifetimes              | die                               |                                                        | entschieden |
| lifetime elision rules                     | Regeln zur Lifetime-Elision / Elisionsregeln       | die                               |                                                        | entschieden |
| static lifetime                            | statische Lifetime / Lifetime `'static`            | die                               |                                                        | entschieden |
| pattern (allgemein, kein Pattern-Matching) | Schema / Muster vermeiden                          | das / die Schemata                | „Muster“ kollidiert mit Pattern; „Schema“ nehmen       | entschieden |
| assert / assertion                         | zusichern / Assertion                              | die / die Assertions              | (_assert_) bei der Einführung                          | entschieden |
| test runner / test harness                 | Testrunner / Test-Harness                          | der / das                         |                                                        | entschieden |
| pass / fail (test)                         | bestehen / fehlschlagen                            | –                                 |                                                        | entschieden |
| doc test                                   | Dokumentationstest                                 | der / die Dokumentationstests     | Ausgabe `Doc-tests` bleibt                             | entschieden |
| separation of concerns / concern           | Trennung der Belange / Belang                      | die / der                         | (_concerns_) bei der Einführung                        | entschieden |
| case-sensitive / case-insensitive          | mit / ohne Beachtung der Groß- und Kleinschreibung | –                                 |                                                        | entschieden |
| standard output / standard error           | Standardausgabe / Standardfehlerausgabe            | die                               | `stdout` / `stderr` bleiben                            | entschieden |
| maintainer                                 | Maintainer                                         | der / die Maintainer              |                                                        | entschieden |
| exit status / exit code                    | Exit-Status / Exit-Code                            | der                               |                                                        | entschieden |
| capture (closure)                          | erfassen                                           | –                                 | (_capture_) bei der Einführung                         | entschieden |
| environment (closure)                      | Umgebung                                           | die                               |                                                        | entschieden |
| lazy (iterator)                            | lazy (träge)                                       | –                                 | Glosse „träge“ bei der Einführung                      | entschieden |
| consume (iterator)                         | verbrauchen                                        | –                                 | (_consumes_) bei der Einführung                        | entschieden |
| consuming adapter / iterator adapter       | verbrauchender Adapter / Iterator-Adapter          | der                               |                                                        | entschieden |
| documentation comment                      | Dokumentationskommentar                            | der                               |                                                        | entschieden |
| yank (crate version)                       | zurückziehen / Yank                                | der                               | Befehl `cargo yank` bleibt                             | entschieden |
| binary target / library target             | Binary-Target / Library-Target                     | das                               |                                                        | entschieden |
| Figure N-M (caption)                       | Abbildung N-M                                      | die                               | handgeschriebene Bildunterschriften                    | entschieden |
| standard library                           | Standardbibliothek                                 | die / –                           |                                                        | entschieden |
| dependency                                 | Abhängigkeit                                       | die / die Abhängigkeiten          |                                                        | entschieden |
| compiler                                   | Compiler                                           | der / die Compiler                |                                                        | entschieden |
| error / error message                      | Fehler / Fehlermeldung                             | der / die                         |                                                        | entschieden |
| recoverable / unrecoverable                | behebbar / nicht behebbar                          | –                                 |                                                        | entschieden |
| test / unit test / integration test        | Test / Unit-Test / Integrationstest                | der                               |                                                        | entschieden |
| test-driven development                    | testgetriebene Entwicklung                         | die / –                           |                                                        | entschieden |
| release profile                            | Release-Profil                                     | das / die Release-Profile         |                                                        | entschieden |
| command line                               | Kommandozeile                                      | die / –                           |                                                        | entschieden |
| terminal                                   | Terminal                                           | das / die Terminals               |                                                        | entschieden |
| environment variable                       | Umgebungsvariable                                  | die / die Umgebungsvariablen      |                                                        | entschieden |
| standard output / error                    | Standardausgabe / Standardfehlerausgabe            | die                               |                                                        | entschieden |
| memory                                     | Speicher                                           | der / –                           |                                                        | entschieden |
| memory safety                              | Speichersicherheit                                 | die / –                           |                                                        | entschieden |
| memory leak                                | Speicherleck                                       | das / die Speicherlecks           |                                                        | entschieden |
| address                                    | Adresse                                            | die / die Adressen                |                                                        | entschieden |
| capacity / length                          | Kapazität / Länge                                  | die                               |                                                        | entschieden |
| reference counting                         | Referenzzählung                                    | die / –                           |                                                        | entschieden |
| reference cycle                            | Referenzzyklus                                     | der / die Referenzzyklen          |                                                        | entschieden |
| weak reference                             | schwache Referenz                                  | die                               |                                                        | entschieden |
| channel                                    | Kanal                                              | der / die Kanäle                  |                                                        | entschieden |
| message passing                            | Nachrichtenübermittlung                            | die / –                           | (_message passing_) beim ersten Auftreten              | entschieden |
| atomic                                     | atomar                                             | –                                 |                                                        | entschieden |
| abstraction                                | Abstraktion                                        | die / die Abstraktionen           |                                                        | entschieden |
| encapsulation                              | Kapselung                                          | die / –                           |                                                        | entschieden |
| inheritance                                | Vererbung                                          | die / –                           |                                                        | entschieden |
| polymorphism                               | Polymorphie                                        | die / –                           |                                                        | entschieden |
| object-oriented                            | objektorientiert                                   | –                                 |                                                        | entschieden |
| invariant                                  | Invariante                                         | die / die Invarianten             |                                                        | entschieden |
| monomorphization                           | Monomorphisierung                                  | die / –                           |                                                        | entschieden |
| fully qualified syntax                     | vollständig qualifizierte Syntax                   | die / –                           |                                                        | entschieden |
| syntactic sugar                            | syntaktischer Zucker                               | der / –                           |                                                        | entschieden |
| constructor                                | Konstruktor                                        | der / die Konstruktoren           |                                                        | entschieden |
| procedural / declarative macro             | prozedurales / deklaratives Makro                  | das                               |                                                        | entschieden |
| derive / derivable                         | ableiten / ableitbar                               | –                                 | (_derive_) beim ersten Auftreten; Code: `#[derive]`    | entschieden |
| diagram                                    | Diagramm                                           | das / die Diagramme               |                                                        | entschieden |
| quiz                                       | Quiz                                               | das / die Quiz                    | Plural nach Duden; „Quizfragen“ für einzelne Fragen    | entschieden |
| case study                                 | Fallstudie                                         | die / die Fallstudien             |                                                        | entschieden |
| read-only                                  | schreibgeschützt / nur lesbar                      | –                                 |                                                        | entschieden |
| live (Referenz „is live“)                  | lebendig                                           | –                                 | „solange `t` lebendig ist“                             | entschieden |
| in use                                     | in Gebrauch                                        | –                                 |                                                        | entschieden |
| invalidate                                 | ungültig machen                                    | –                                 |                                                        | entschieden |
| downgrade                                  | herabstufen                                        | –                                 |                                                        | entschieden |
| aliased (Daten)                            | einen Alias haben                                  | –                                 | „data is aliased“ → „die Daten haben einen Alias“      | entschieden |
| aliased data                               | gemeinsam genutzte Daten                           | die (Pl.)                         | wenn „Daten mit Alias“ holprig wäre                    | entschieden |
| snippet                                    | Codeausschnitt                                     | der / die Codeausschnitte         |                                                        | entschieden |
| dereference operator                       | Dereferenzierungsoperator                          | der                               |                                                        | entschieden |
| method-call syntax                         | Syntax für Methodenaufrufe                         | die                               |                                                        | entschieden |
| if-statement / then-block                  | if-Anweisung / then-Block / else-Block             | die / der                         | ohne Backticks, wie im Original                        | entschieden |
| ampersand                                  | Ampersand                                          | das / die Ampersands              | `&`; „Ampersand-Operator“                              | entschieden |

## 3. Verben

| Englisch                | Deutsch                                                               | Hinweis                                                                   | Status      |
| ----------------------- | --------------------------------------------------------------------- | ------------------------------------------------------------------------- | ----------- |
| move                    | verschieben                                                           | nie „moven“, „gemoved“                                                    | fest        |
| borrow                  | ausleihen                                                             | nie „borrowen“, „geborrowt“                                               | fest        |
| own                     | besitzen                                                              | „owned data“ je nach Kontext umschreiben („Daten, die … besitzt“)         | fest        |
| drop                    | verwerfen                                                             | Funktion `drop` bleibt Code                                               | fest        |
| clone                   | klonen                                                                |                                                                           | fest        |
| panic                   | einen Panic auslösen                                                  | nie „panicken“                                                            | fest        |
| match (Pattern)         | passen (auf), übereinstimmen                                          | nie „matchen“                                                             | entschieden |
| await                   | abwarten (_await_)                                                    | Schlüsselwort `await` bleibt Code                                         | offen       |
| pin                     | fixieren (_pin_)                                                      | Typ `Pin` bleibt Code                                                     | offen       |
| refutable / irrefutable | refutable / irrefutable (Glosse: „kann fehlschlagen“ / „passt immer“) | Compiler: „refutable pattern in local binding“; Alternative „widerlegbar“ | offen       |
| compile                 | kompilieren                                                           |                                                                           | entschieden |
| refactor                | refaktorisieren                                                       |                                                                           | entschieden |

## 4. Begriffe dieses Buchs

| Englisch                               | Deutsch                               | Hinweis                                                                  | Status      |
| -------------------------------------- | ------------------------------------- | ------------------------------------------------------------------------ | ----------- |
| Box deallocation principle             | _Prinzip der Box-Freigabe_            | bei der Definition englischen Namen in Klammern ergänzen                 | entschieden |
| Moved heap data principle              | _Prinzip der verschobenen Heap-Daten_ | dito                                                                     | entschieden |
| Pointer Safety Principle               | _Prinzip der Zeigersicherheit_        | dito                                                                     | entschieden |
| Ownership Inventory #N                 | Ownership-Inventur #N                 | Kapiteltitel                                                             | offen       |
| L1, L2, … (Diagramm-Marken)            | L1, L2, …                             | stehen so in den Diagrammen                                              | fest        |
| question mark crab                     | Fragezeichen-Krabbe                   | Ferris mit Fragezeichen                                                  | entschieden |
| Hello, World! / Hello, Cargo!          | unverändert                           | Namen der Beispielprogramme (die Ausgabe bleibt englisch)                | entschieden |
| Kapiteltitel in Querverweisen          | wie in `src/SUMMARY.md`               | z. B. [„Referenzen mit Lifetimes validieren“](…)                         | entschieden |
| `> Note: …` (von `trpl-note` erkannt)  | `> Note: …` unverändert, Rest deutsch | Präfix wird vom Präprozessor erkannt; siehe Bericht                      | fest        |
| `*Note:*`, `**Note:**`, `<i>Note:</i>` | _Hinweis:_                            | werden von keinem Werkzeug ausgewertet                                   | entschieden |
| `<span class="filename">Filename: …`   | Dateiname: …                          | handgeschriebene Spans; `<Listing file-name>` erzeugt weiter „Filename:“ | offen       |

## 5. Berechtigungen (Aquascope)

Die Diagramme zeigen die Buchstaben R, W, O, F und Beschriftungen wie Stack und
Heap. Sie lassen sich nicht übersetzen, also passt sich der Text an.

| Englisch   | Deutsch im Text      | Hinweis                                       | Status |
| ---------- | -------------------- | --------------------------------------------- | ------ |
| permission | Berechtigung         |                                               | fest   |
| Read (R)   | Read (R, lesen)      | Glosse an der Stelle, die sie einführt        | fest   |
| Write (W)  | Write (W, schreiben) | dito                                          | fest   |
| Own (O)    | Own (O, besitzen)    | dito                                          | fest   |
| Flow (F)   | Flow (F, fließen)    | dito                                          | fest   |
| `@Perm{…}` | unverändert          | Aquascope-Markup im Fließtext, byte-identisch | fest   |

## 6. Glossen für Compiler-Begriffe

Compiler-Meldungen bleiben englisch. Beim **ersten Auftreten auf jeder Seite**
(eine `.md`-Datei) bekommen diese übersetzten Begriffe das englische Wort in
Klammern und kursiv:

| Deutsch                       | Glosse                      |
| ----------------------------- | --------------------------- |
| verschieben / verschoben      | (_move_) / (_moved_)        |
| ausleihen / ausgeliehen       | (_borrow_) / (_borrowed_)   |
| Gültigkeitsbereich            | (_scope_)                   |
| verwerfen / verworfen         | (_drop_) / (_dropped_)      |
| veränderlich / unveränderlich | (_mutable_) / (_immutable_) |

Weitere Begriffe (z. B. Anweisung/Ausdruck, Feld, Variante) bekommen die Glosse
dort, wo das Buch sie definiert.

## 7. Typografie

- Anführungszeichen „…“, innen ‚…‘.
- Gedankenstrich: Halbgeviertstrich mit Leerzeichen „ – “ statt „—“ bzw.
  `&mdash;`.
- „z. B.“, „d. h.“, „u. a.“ mit Leerzeichen.
- Dezimalkomma im Fließtext, nie in Code, Ausgaben oder Versionsnummern.
- Englische Begriffe in Klammern kursiv: „verschoben (_moved_)“.

## Änderungsprotokoll

| Datum   | Begriff                                                                                                           | alt | neu             | betroffene Dateien |
| ------- | ----------------------------------------------------------------------------------------------------------------- | --- | --------------- | ------------------ |
| Kap. 7  | item, parent/child module, submodule, ancestor, sibling, module tree, glob operator, front/back of house          | –   | neu aufgenommen | ch07-*             |
| Kap. 8  | grapheme cluster, Unicode scalar value, wrapper, hashing function/hasher, Pig Latin                               | –   | neu aufgenommen | ch08-*             |
| Kap. 9  | propagate, file handle, question mark operator, unwinding/aborting, backtrace, getter, contract, buffer overread  | –   | neu aufgenommen | ch09-*             |
| Kap. 10 | coherence, implementor, where clause, input/output lifetimes, elision rules, static lifetime, pattern (allgemein) | –   | neu aufgenommen | ch10-*             |
| Kap. 11 | assert/assertion, test runner/harness, pass/fail, doc test                                                        | –   | neu aufgenommen | ch11-*             |
| Kap. 12 | separation of concerns, case-(in)sensitive, stdout/stderr, maintainer, exit status                                | –   | neu aufgenommen | ch12-*             |
| Kap. 13 | capture, environment, lazy, consume, consuming/iterator adapter                                                   | –   | neu aufgenommen | ch13-*             |
| Kap. 14 | release profile, documentation comment, yank, binary/library target, registry, Figure                             | –   | neu aufgenommen | ch14-*             |
