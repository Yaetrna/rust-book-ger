## Anhang C: Ableitbare Traits {#appendix-c-derivable-traits}

An verschiedenen Stellen im Buch haben wir das Attribut `derive` besprochen, das
du auf eine Struct- oder Enum-Definition anwenden kannst. Das Attribut `derive`
erzeugt Code, der einen Trait mit seiner eigenen Standardimplementierung für den
Typ implementiert, den du mit der `derive`-Syntax annotiert hast.

In diesem Anhang stellen wir eine Referenz aller Traits der Standardbibliothek
bereit, die du mit `derive` verwenden kannst. Jeder Abschnitt behandelt:

- Welche Operatoren und Methoden das Ableiten (_deriving_) dieses Traits
  ermöglicht
- Was die durch `derive` bereitgestellte Implementierung des Traits tut
- Was die Implementierung des Traits über den Typ aussagt
- Unter welchen Bedingungen du den Trait implementieren darfst und unter welchen
  nicht
- Beispiele für Operationen, die den Trait erfordern

Wenn du ein anderes Verhalten möchtest als das, das das Attribut `derive`
bereitstellt, findest du in der
[Dokumentation der Standardbibliothek](../std/index.html)<!-- ignore --> zu
jedem Trait Details dazu, wie man ihn manuell implementiert.

Die hier aufgeführten Traits sind die einzigen in der Standardbibliothek
definierten Traits, die mit `derive` für deine Typen implementiert werden
können. Andere in der Standardbibliothek definierte Traits haben kein sinnvolles
Standardverhalten, daher liegt es an dir, sie so zu implementieren, wie es für
dein Vorhaben sinnvoll ist.

Ein Beispiel für einen Trait, der nicht abgeleitet werden kann, ist `Display`,
der die Formatierung für Endbenutzer übernimmt. Du solltest dir immer überlegen,
wie ein Typ einem Endbenutzer angemessen angezeigt wird. Welche Teile des Typs
sollte ein Endbenutzer sehen dürfen? Welche Teile wären für ihn relevant?
Welches Format der Daten wäre für ihn am relevantesten? Der Rust-Compiler hat
diese Einsicht nicht und kann dir daher kein angemessenes Standardverhalten
bieten.

Die Liste der ableitbaren Traits in diesem Anhang ist nicht vollständig:
Bibliotheken können `derive` für ihre eigenen Traits implementieren, wodurch die
Liste der Traits, mit denen du `derive` verwenden kannst, wirklich offen ist.
Die Implementierung von `derive` erfordert ein prozedurales Makro, das im
Abschnitt
[„Benutzerdefinierte `derive`-Makros“][custom-derive-macros]<!-- ignore --> in
Kapitel 20 behandelt wird.

### `Debug` für Ausgaben für Programmierer {#debug-for-programmer-output}

Der Trait `Debug` ermöglicht die Debug-Formatierung in Formatstrings, die du
angibst, indem du `:?` innerhalb von `{}`-Platzhaltern hinzufügst.

Mit dem Trait `Debug` kannst du Instanzen eines Typs zu Debugging-Zwecken
ausgeben, sodass du und andere Programmierer, die deinen Typ verwenden, eine
Instanz an einem bestimmten Punkt der Programmausführung untersuchen können.

Der Trait `Debug` ist zum Beispiel für die Verwendung des Makros `assert_eq!`
erforderlich. Dieses Makro gibt die Werte der als Argumente übergebenen
Instanzen aus, wenn die Gleichheitszusicherung fehlschlägt, damit Programmierer
sehen können, warum die beiden Instanzen nicht gleich waren.

### `PartialEq` und `Eq` für Gleichheitsvergleiche {#partialeq-and-eq-for-equality-comparisons}

Mit dem Trait `PartialEq` kannst du Instanzen eines Typs auf Gleichheit
vergleichen, und er ermöglicht die Verwendung der Operatoren `==` und `!=`.

Das Ableiten von `PartialEq` implementiert die Methode `eq`. Wenn `PartialEq`
für Structs abgeleitet wird, sind zwei Instanzen nur dann gleich, wenn _alle_
Felder gleich sind, und die Instanzen sind ungleich, wenn _irgendein_ Feld
ungleich ist. Bei Enums ist jede Variante gleich sich selbst und ungleich den
anderen Varianten.

Der Trait `PartialEq` ist zum Beispiel bei der Verwendung des Makros
`assert_eq!` erforderlich, das zwei Instanzen eines Typs auf Gleichheit
vergleichen können muss.

Der Trait `Eq` hat keine Methoden. Sein Zweck ist es, zu signalisieren, dass
jeder Wert des annotierten Typs gleich sich selbst ist. Der Trait `Eq` kann nur
auf Typen angewendet werden, die auch `PartialEq` implementieren, wobei aber
nicht alle Typen, die `PartialEq` implementieren, auch `Eq` implementieren
können. Ein Beispiel dafür sind Gleitkommazahltypen: Die Implementierung von
Gleitkommazahlen legt fest, dass zwei Instanzen des Werts „keine Zahl“
(_not-a-number_, `NaN`) nicht gleich sind.

Ein Beispiel dafür, wann `Eq` erforderlich ist, sind die Schlüssel in einer
`HashMap<K, V>`, damit die `HashMap<K, V>` erkennen kann, ob zwei Schlüssel
gleich sind.

### `PartialOrd` und `Ord` für Ordnungsvergleiche {#partialord-and-ord-for-ordering-comparisons}

Mit dem Trait `PartialOrd` kannst du Instanzen eines Typs zum Sortieren
vergleichen. Ein Typ, der `PartialOrd` implementiert, kann mit den Operatoren
`<`, `>`, `<=` und `>=` verwendet werden. Du kannst den Trait `PartialOrd` nur
auf Typen anwenden, die auch `PartialEq` implementieren.

Das Ableiten von `PartialOrd` implementiert die Methode `partial_cmp`, die ein
`Option<Ordering>` zurückgibt, das `None` ist, wenn die übergebenen Werte keine
Ordnung ergeben. Ein Beispiel für einen Wert, der keine Ordnung ergibt, obwohl
die meisten Werte dieses Typs verglichen werden können, ist der Gleitkommawert
`NaN`. Ein Aufruf von `partial_cmp` mit einer beliebigen Gleitkommazahl und dem
Gleitkommawert `NaN` gibt `None` zurück.

Bei Structs vergleicht ein abgeleitetes `PartialOrd` zwei Instanzen, indem es
den Wert jedes Felds in der Reihenfolge vergleicht, in der die Felder in der
Struct-Definition stehen. Bei Enums gelten Varianten, die in der Enum-Definition
früher deklariert sind, als kleiner als später aufgeführte Varianten.

Der Trait `PartialOrd` ist zum Beispiel für die Methode `gen_range` aus dem
Crate `rand` erforderlich, die einen Zufallswert in dem durch einen
Bereichsausdruck angegebenen Bereich erzeugt.

Mit dem Trait `Ord` weißt du, dass für zwei beliebige Werte des annotierten Typs
eine gültige Ordnung existiert. Der Trait `Ord` implementiert die Methode `cmp`,
die ein `Ordering` statt eines `Option<Ordering>` zurückgibt, weil immer eine
gültige Ordnung möglich ist. Du kannst den Trait `Ord` nur auf Typen anwenden,
die auch `PartialOrd` und `Eq` implementieren (und `Eq` erfordert `PartialEq`).
Bei Structs und Enums verhält sich ein abgeleitetes `cmp` genauso wie die
abgeleitete Implementierung von `partial_cmp` bei `PartialOrd`.

Ein Beispiel dafür, wann `Ord` erforderlich ist, ist das Speichern von Werten in
einem `BTreeSet<T>`, einer Datenstruktur, die Daten anhand der
Sortierreihenfolge der Werte speichert.

### `Clone` und `Copy` zum Duplizieren von Werten {#clone-and-copy-for-duplicating-values}

Mit dem Trait `Clone` kannst du ausdrücklich eine tiefe Kopie eines Werts
erstellen, und der Duplizierungsvorgang kann das Ausführen beliebigen Codes und
das Kopieren von Heap-Daten beinhalten.

Das Ableiten von `Clone` implementiert die Methode `clone`, die, wenn sie für
den ganzen Typ implementiert wird, `clone` auf jedem Teil des Typs aufruft. Das
bedeutet, dass alle Felder oder Werte im Typ ebenfalls `Clone` implementieren
müssen, damit `Clone` abgeleitet werden kann.

Ein Beispiel dafür, wann `Clone` erforderlich ist, ist der Aufruf der Methode
`to_vec` auf einem Slice. Der Slice besitzt die Typinstanzen, die er enthält,
nicht, aber der von `to_vec` zurückgegebene Vektor muss seine Instanzen
besitzen, daher ruft `to_vec` `clone` für jedes Element auf. Der im Slice
gespeicherte Typ muss also `Clone` implementieren.

Mit dem Trait `Copy` kannst du einen Wert duplizieren, indem du nur die auf dem
Stack gespeicherten Bits kopierst; beliebiger Code ist dafür nicht nötig.

Der Trait `Copy` definiert keine Methoden, um zu verhindern, dass Programmierer
diese Methoden überladen und damit die Annahme verletzen, dass kein beliebiger
Code ausgeführt wird. So können alle Programmierer davon ausgehen, dass das
Kopieren eines Werts sehr schnell ist.

Du kannst `Copy` für jeden Typ ableiten, dessen Teile alle `Copy`
implementieren. Ein Typ, der `Copy` implementiert, muss auch `Clone`
implementieren, weil ein Typ, der `Copy` implementiert, eine triviale
Implementierung von `Clone` hat, die dieselbe Aufgabe wie `Copy` erfüllt.

Der Trait `Copy` ist selten erforderlich; für Typen, die `Copy` implementieren,
stehen Optimierungen zur Verfügung, sodass du `clone` nicht aufrufen musst, was
den Code prägnanter macht.

Alles, was mit `Copy` möglich ist, kannst du auch mit `Clone` erreichen, aber
der Code ist dann möglicherweise langsamer oder muss an manchen Stellen `clone`
verwenden.

### `Hash` zum Abbilden eines Werts auf einen Wert fester Größe {#hash-for-mapping-a-value-to-a-value-of-fixed-size}

Mit dem Trait `Hash` kannst du eine Instanz eines Typs beliebiger Größe nehmen
und diese Instanz mit einer Hashfunktion auf einen Wert fester Größe abbilden.
Das Ableiten von `Hash` implementiert die Methode `hash`. Die abgeleitete
Implementierung der Methode `hash` kombiniert das Ergebnis des Aufrufs von
`hash` auf jedem Teil des Typs, das heißt, alle Felder oder Werte müssen
ebenfalls `Hash` implementieren, damit `Hash` abgeleitet werden kann.

Ein Beispiel dafür, wann `Hash` erforderlich ist, ist das Speichern von
Schlüsseln in einer `HashMap<K, V>`, um Daten effizient zu speichern.

### `Default` für Standardwerte {#default-for-default-values}

Mit dem Trait `Default` kannst du einen Standardwert für einen Typ erzeugen. Das
Ableiten von `Default` implementiert die Funktion `default`. Die abgeleitete
Implementierung der Funktion `default` ruft die Funktion `default` auf jedem
Teil des Typs auf, das heißt, alle Felder oder Werte im Typ müssen ebenfalls
`Default` implementieren, damit `Default` abgeleitet werden kann.

Die Funktion `Default::default` wird häufig in Kombination mit der
Struct-Update-Syntax verwendet, die im Abschnitt
[„Instanzen mit der Struct-Update-Syntax
erzeugen“][creating-instances-from-other-instances-with-struct-update-syntax]<!--
ignore --> in Kapitel 5 besprochen wird. Du kannst einige Felder eines Structs
anpassen und dann mit `..Default::default()` für die übrigen Felder einen
Standardwert setzen und verwenden.

Der Trait `Default` ist zum Beispiel erforderlich, wenn du die Methode
`unwrap_or_default` auf `Option<T>`-Instanzen verwendest. Wenn die `Option<T>`
`None` ist, gibt die Methode `unwrap_or_default` das Ergebnis von
`Default::default` für den Typ `T` zurück, der in der `Option<T>` gespeichert
ist.

[creating-instances-from-other-instances-with-struct-update-syntax]: ch05-01-defining-structs.html#creating-instances-from-other-instances-with-struct-update-syntax
[stack-only-data-copy]: ch04-01-what-is-ownership.html#stack-only-data-copy
[variables-and-data-interacting-with-clone]: ch04-01-what-is-ownership.html#variables-and-data-interacting-with-clone
[custom-derive-macros]: ch20-05-macros.html#custom-derive-macros
