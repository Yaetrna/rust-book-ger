<!-- Old headings. Do not remove or links may break. -->

<a id="defining-modules-to-control-scope-and-privacy"></a>

## Gültigkeitsbereich und Sichtbarkeit mit Modulen steuern {#control-scope-and-privacy-with-modules}

In diesem Abschnitt sprechen wir über Module und andere Teile des Modulsystems,
nämlich _Pfade_, mit denen du Elemente benennen kannst; das Schlüsselwort `use`,
das einen Pfad in den Gültigkeitsbereich (_scope_) bringt; und das Schlüsselwort
`pub`, mit dem du Elemente öffentlich machst. Außerdem besprechen wir das
Schlüsselwort `as`, externe Pakete und den Glob-Operator.

### Spickzettel zu Modulen {#modules-cheat-sheet}

Bevor wir zu den Details von Modulen und Pfaden kommen, geben wir hier einen
kurzen Überblick darüber, wie Module, Pfade, das Schlüsselwort `use` und das
Schlüsselwort `pub` im Compiler funktionieren und wie die meisten
Entwicklerinnen und Entwickler ihren Code organisieren. Wir gehen im Laufe
dieses Kapitels Beispiele für jede dieser Regeln durch, aber hier kannst du gut
nachschlagen, wenn du dich daran erinnern willst, wie Module funktionieren.

- **Bei der Crate-Root beginnen**: Beim Kompilieren eines Crates sucht der
  Compiler zuerst in der Crate-Root-Datei (normalerweise _src/lib.rs_ für ein
  Library-Crate und _src/main.rs_ für ein Binary-Crate) nach Code zum
  Kompilieren.
- **Module deklarieren**: In der Crate-Root-Datei kannst du neue Module
  deklarieren; sagen wir, du deklarierst ein Modul „garden“ mit `mod garden;`.
  Der Compiler sucht den Code des Moduls an diesen Stellen:
  - Inline, in geschweiften Klammern, die das Semikolon nach `mod
    garden`
    ersetzen
  - In der Datei _src/garden.rs_
  - In der Datei _src/garden/mod.rs_
- **Untermodule deklarieren**: In jeder Datei außer der Crate-Root kannst du
  Untermodule deklarieren. Du könntest zum Beispiel `mod vegetables;` in
  _src/garden.rs_ deklarieren. Der Compiler sucht den Code des Untermoduls in
  dem Verzeichnis, das nach dem Elternmodul benannt ist, an diesen Stellen:
  - Inline, direkt nach `mod vegetables`, in geschweiften Klammern statt des
    Semikolons
  - In der Datei _src/garden/vegetables.rs_
  - In der Datei _src/garden/vegetables/mod.rs_
- **Pfade zu Code in Modulen**: Sobald ein Modul Teil deines Crates ist, kannst
  du von überall sonst im selben Crate auf Code in diesem Modul verweisen,
  solange die Sichtbarkeitsregeln es erlauben, indem du den Pfad zum Code
  verwendest. Ein Typ `Asparagus` im Modul garden vegetables wäre zum Beispiel
  unter `crate::garden::vegetables::Asparagus` zu finden.
- **Privat oder öffentlich**: Code innerhalb eines Moduls ist standardmäßig vor
  seinen Elternmodulen verborgen (privat). Um ein Modul öffentlich zu machen,
  deklariere es mit `pub mod` statt mit `mod`. Um auch Elemente innerhalb eines
  öffentlichen Moduls öffentlich zu machen, setze `pub` vor ihre Deklarationen.
- **Das Schlüsselwort `use`**: Innerhalb eines Gültigkeitsbereichs erzeugt das
  Schlüsselwort `use` Abkürzungen zu Elementen, damit sich lange Pfade nicht
  wiederholen. In jedem Gültigkeitsbereich, der auf
  `crate::garden::vegetables::Asparagus` verweisen kann, kannst du mit
  `use
  crate::garden::vegetables::Asparagus;` eine Abkürzung erzeugen, und von
  da an musst du nur noch `Asparagus` schreiben, um diesen Typ im
  Gültigkeitsbereich zu verwenden.

Hier erstellen wir ein Binary-Crate namens `backyard`, das diese Regeln
veranschaulicht. Das Verzeichnis des Crates, das ebenfalls _backyard_ heißt,
enthält diese Dateien und Verzeichnisse:

```text
backyard
├── Cargo.lock
├── Cargo.toml
└── src
    ├── garden
    │   └── vegetables.rs
    ├── garden.rs
    └── main.rs
```

Die Crate-Root-Datei ist in diesem Fall _src/main.rs_ und enthält:

<Listing file-name="src/main.rs">

```rust,noplayground,ignore
{{#rustdoc_include ../listings/ch07-managing-growing-projects/quick-reference-example/src/main.rs}}
```

</Listing>

Die Zeile `pub mod garden;` weist den Compiler an, den Code einzubinden, den er
in _src/garden.rs_ findet, nämlich:

<Listing file-name="src/garden.rs">

```rust,noplayground,ignore
{{#rustdoc_include ../listings/ch07-managing-growing-projects/quick-reference-example/src/garden.rs}}
```

</Listing>

Hier bedeutet `pub mod vegetables;`, dass auch der Code in
_src/garden/vegetables.rs_ eingebunden wird. Dieser Code lautet:

```rust,noplayground,ignore
{{#rustdoc_include ../listings/ch07-managing-growing-projects/quick-reference-example/src/garden/vegetables.rs}}
```

Sehen wir uns nun die Details dieser Regeln an und zeigen sie in Aktion!

### Zusammengehörigen Code in Modulen gruppieren {#grouping-related-code-in-modules}

Mit _Modulen_ können wir Code innerhalb eines Crates organisieren, damit er
lesbar und leicht wiederverwendbar ist. Module erlauben uns außerdem, die
_Sichtbarkeit_ (_privacy_) von Elementen zu steuern, denn Code innerhalb eines
Moduls ist standardmäßig privat. Private Elemente sind interne
Implementierungsdetails, die nicht für die Verwendung von außen zur Verfügung
stehen. Wir können Module und die Elemente darin öffentlich machen; dadurch
legen wir sie offen, sodass externer Code sie verwenden und von ihnen abhängen
kann.

Schreiben wir als Beispiel ein Library-Crate, das die Funktionalität eines
Restaurants bereitstellt. Wir definieren die Signaturen der Funktionen, lassen
ihre Rümpfe aber leer, um uns auf die Organisation des Codes zu konzentrieren
statt auf die Implementierung eines Restaurants.

In der Gastronomie werden manche Bereiche eines Restaurants als Front of House
und andere als Back of House bezeichnet. Das _Front of House_ ist dort, wo die
Gäste sind; dazu gehört, wo die Gastgeber die Gäste platzieren, das
Servicepersonal Bestellungen und Zahlungen entgegennimmt und die Barkeeper
Getränke mixen. Das _Back of House_ ist dort, wo die Köchinnen und Köche in der
Küche arbeiten, das Spülpersonal aufräumt und die Geschäftsführung
Verwaltungsarbeit erledigt.

Um unser Crate auf diese Weise zu strukturieren, können wir seine Funktionen in
verschachtelten Modulen organisieren. Erstelle eine neue Bibliothek namens
`restaurant`, indem du `cargo new
restaurant --lib` ausführst. Gib dann den Code
aus Listing 7-1 in _src/lib.rs_ ein, um einige Module und Funktionssignaturen zu
definieren; dieser Code ist der Front-of-House-Bereich.

<Listing number="7-1" file-name="src/lib.rs" caption="Ein Modul `front_of_house`, das weitere Module enthält, die wiederum Funktionen enthalten">

```rust,noplayground
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-01/src/lib.rs}}
```

</Listing>

Wir definieren ein Modul mit dem Schlüsselwort `mod`, gefolgt vom Namen des
Moduls (in diesem Fall `front_of_house`). Der Rumpf des Moduls steht dann in
geschweiften Klammern. Innerhalb von Modulen können wir weitere Module
platzieren, wie hier die Module `hosting` und `serving`. Module können auch
Definitionen anderer Elemente enthalten, etwa Structs, Enums, Konstanten, Traits
und, wie in Listing 7-1, Funktionen.

Mit Modulen können wir zusammengehörige Definitionen gruppieren und benennen,
warum sie zusammengehören. Programmierende, die diesen Code verwenden, können
sich anhand der Gruppen durch den Code bewegen, statt alle Definitionen
durchlesen zu müssen, und finden so die für sie relevanten Definitionen
leichter. Programmierende, die diesem Code neue Funktionalität hinzufügen,
wüssten, wo sie den Code platzieren müssen, damit das Programm organisiert
bleibt.

Wir haben vorhin erwähnt, dass _src/main.rs_ und _src/lib.rs_ _Crate-Roots_
genannt werden. Der Grund für diesen Namen ist, dass der Inhalt jeder dieser
beiden Dateien ein Modul namens `crate` an der Wurzel der Modulstruktur des
Crates bildet, die als _Modulbaum_ bezeichnet wird.

Listing 7-2 zeigt den Modulbaum für die Struktur in Listing 7-1.

<Listing number="7-2" caption="Der Modulbaum für den Code in Listing 7-1">

```text
crate
 └── front_of_house
     ├── hosting
     │   ├── add_to_waitlist
     │   └── seat_at_table
     └── serving
         ├── take_order
         ├── serve_order
         └── take_payment
```

</Listing>

Dieser Baum zeigt, wie manche Module in anderen Modulen verschachtelt sind; zum
Beispiel ist `hosting` in `front_of_house` verschachtelt. Der Baum zeigt auch,
dass manche Module _Geschwister_ sind, also im selben Modul definiert sind;
`hosting` und `serving` sind Geschwister, die in `front_of_house` definiert
sind. Ist Modul A in Modul B enthalten, sagen wir, dass Modul A das _Kind_ von
Modul B ist und dass Modul B das _Elternmodul_ von Modul A ist. Beachte, dass
der gesamte Modulbaum unter dem impliziten Modul namens `crate` wurzelt.

Der Modulbaum erinnert dich vielleicht an den Verzeichnisbaum des Dateisystems
auf deinem Computer; das ist ein sehr treffender Vergleich! Genau wie
Verzeichnisse in einem Dateisystem verwendest du Module, um deinen Code zu
organisieren. Und genau wie Dateien in einem Verzeichnis brauchen wir eine
Möglichkeit, unsere Module zu finden.

{{#quiz ../quizzes/ch07-02-modules.toml}}
