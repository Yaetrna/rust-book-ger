## Anhang A: Schlüsselwörter {#appendix-a-keywords}

Die folgenden Listen enthalten Schlüsselwörter, die für die aktuelle oder
künftige Verwendung durch die Sprache Rust reserviert sind. Daher können sie
nicht als Bezeichner verwendet werden (außer als Raw-Bezeichner, wie wir im
Abschnitt [„Raw-Bezeichner“][raw-identifiers]<!-- ignore --> besprechen).
_Bezeichner_ (_identifiers_) sind Namen von Funktionen, Variablen, Parametern,
Struct-Feldern, Modulen, Crates, Konstanten, Makros, statischen Werten,
Attributen, Typen, Traits oder Lifetimes.

[raw-identifiers]: #raw-identifiers

### Derzeit verwendete Schlüsselwörter {#keywords-currently-in-use}

Es folgt eine Liste der derzeit verwendeten Schlüsselwörter mit einer
Beschreibung ihrer Funktion.

- **`as`**: Primitive Typumwandlung durchführen, den bestimmten Trait eindeutig
  machen, der ein Element enthält, oder Elemente in `use`-Anweisungen
  umbenennen.
- **`async`**: Ein `Future` zurückgeben, statt den aktuellen Thread zu
  blockieren.
- **`await`**: Die Ausführung anhalten, bis das Ergebnis eines `Future` bereit
  ist.
- **`break`**: Eine Schleife sofort verlassen.
- **`const`**: Konstante Elemente oder konstante Raw-Pointer definieren.
- **`continue`**: Mit der nächsten Schleifeniteration fortfahren.
- **`crate`**: Verweist in einem Modulpfad auf die Crate-Root.
- **`dyn`**: Dynamischer Dispatch an ein Trait-Objekt.
- **`else`**: Alternative für die Kontrollflusskonstrukte `if` und `if let`.
- **`enum`**: Ein Enum definieren.
- **`extern`**: Eine externe Funktion oder Variable einbinden.
- **`false`**: Boolesches Literal für falsch.
- **`fn`**: Eine Funktion oder den Funktionszeigertyp definieren.
- **`for`**: Über Elemente eines Iterators iterieren, einen Trait implementieren
  oder eine Lifetime höheren Rangs angeben.
- **`if`**: Abhängig vom Ergebnis eines bedingten Ausdrucks verzweigen.
- **`impl`**: Eigene Funktionalität oder Trait-Funktionalität implementieren.
- **`in`**: Teil der Syntax der `for`-Schleife.
- **`let`**: Eine Variable binden.
- **`loop`**: Bedingungslos in einer Schleife laufen.
- **`match`**: Einen Wert mit Patterns abgleichen.
- **`mod`**: Ein Modul definieren.
- **`move`**: Eine Closure die Ownership an allem übernehmen lassen, was sie
  erfasst.
- **`mut`**: Veränderlichkeit bei Referenzen, Raw-Pointern oder
  Pattern-Bindungen kennzeichnen.
- **`pub`**: Öffentliche Sichtbarkeit bei Struct-Feldern, `impl`-Blöcken oder
  Modulen kennzeichnen.
- **`ref`**: Per Referenz binden.
- **`return`**: Aus einer Funktion zurückkehren.
- **`Self`**: Ein Typalias für den Typ, den wir definieren oder implementieren.
- **`self`**: Subjekt einer Methode oder aktuelles Modul.
- **`static`**: Globale Variable oder Lifetime, die die gesamte
  Programmausführung überdauert.
- **`struct`**: Ein Struct definieren.
- **`super`**: Elternmodul des aktuellen Moduls.
- **`trait`**: Einen Trait definieren.
- **`true`**: Boolesches Literal für wahr.
- **`type`**: Einen Typalias oder assoziierten Typ definieren.
- **`union`**: Eine [Union][union]<!-- ignore --> definieren; ist nur in einer
  Union-Deklaration ein Schlüsselwort.
- **`unsafe`**: Unsicheren Code, unsichere Funktionen, Traits oder
  Implementierungen kennzeichnen.
- **`use`**: Symbole in den Gültigkeitsbereich (_scope_) bringen.
- **`where`**: Klauseln kennzeichnen, die einen Typ einschränken.
- **`while`**: Abhängig vom Ergebnis eines Ausdrucks in einer Schleife laufen.

[union]: https://doc.rust-lang.org/reference/items/unions.html

### Für die künftige Verwendung reservierte Schlüsselwörter {#keywords-reserved-for-future-use}

Die folgenden Schlüsselwörter haben noch keine Funktion, sind aber von Rust für
eine mögliche künftige Verwendung reserviert:

- `abstract`
- `become`
- `box`
- `do`
- `final`
- `gen`
- `macro`
- `override`
- `priv`
- `try`
- `typeof`
- `unsized`
- `virtual`
- `yield`

### Raw-Bezeichner {#raw-identifiers}

_Raw-Bezeichner_ (_raw identifiers_) sind die Syntax, mit der du Schlüsselwörter
dort verwenden kannst, wo sie normalerweise nicht erlaubt wären. Du verwendest
einen Raw-Bezeichner, indem du einem Schlüsselwort `r#` voranstellst.

Zum Beispiel ist `match` ein Schlüsselwort. Wenn du versuchst, die folgende
Funktion zu kompilieren, die `match` als Namen verwendet:

<span class="filename">Dateiname: src/main.rs</span>

```rust,ignore,does_not_compile
fn match(needle: &str, haystack: &str) -> bool {
    haystack.contains(needle)
}
```

bekommst du diesen Fehler:

```text
error: expected identifier, found keyword `match`
 --> src/main.rs:4:4
  |
4 | fn match(needle: &str, haystack: &str) -> bool {
  |    ^^^^^ expected identifier, found keyword
```

Der Fehler zeigt, dass du das Schlüsselwort `match` nicht als Bezeichner der
Funktion verwenden kannst. Um `match` als Funktionsnamen zu verwenden, musst du
die Syntax für Raw-Bezeichner verwenden, etwa so:

<span class="filename">Dateiname: src/main.rs</span>

```rust
fn r#match(needle: &str, haystack: &str) -> bool {
    haystack.contains(needle)
}

fn main() {
    assert!(r#match("foo", "foobar"));
}
```

Dieser Code kompiliert ohne Fehler. Beachte das Präfix `r#` beim Funktionsnamen
in seiner Definition und dort, wo die Funktion in `main` aufgerufen wird.

Mit Raw-Bezeichnern kannst du jedes beliebige Wort als Bezeichner verwenden,
selbst wenn dieses Wort ein reserviertes Schlüsselwort ist. Das gibt uns mehr
Freiheit bei der Wahl von Bezeichnernamen und ermöglicht es uns außerdem, mit
Programmen zusammenzuarbeiten, die in einer Sprache geschrieben sind, in der
diese Wörter keine Schlüsselwörter sind. Darüber hinaus ermöglichen es
Raw-Bezeichner, Bibliotheken zu verwenden, die in einer anderen Rust-Edition
geschrieben sind als dein Crate. Zum Beispiel ist `try` in der Edition 2015 kein
Schlüsselwort, in den Editionen 2018, 2021 und 2024 aber schon. Wenn du von
einer Bibliothek abhängst, die mit der Edition 2015 geschrieben ist und eine
Funktion `try` hat, musst du die Syntax für Raw-Bezeichner verwenden, in diesem
Fall `r#try`, um diese Funktion in späteren Editionen aus deinem Code
aufzurufen. Weitere Informationen zu Editionen findest du in
[Anhang E][appendix-e]<!-- ignore -->.

[appendix-e]: appendix-05-editions.html
