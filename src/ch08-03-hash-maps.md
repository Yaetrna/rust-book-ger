## Schlüssel mit zugehörigen Werten in Hash-Maps speichern {#storing-keys-with-associated-values-in-hash-maps}

Die letzte unserer gängigen Collections ist die Hash-Map. Der Typ
`HashMap<K, V>` speichert eine Zuordnung von Schlüsseln vom Typ `K` zu Werten
vom Typ `V` mithilfe einer _Hashfunktion_, die bestimmt, wie diese Schlüssel und
Werte im Speicher abgelegt werden. Viele Programmiersprachen unterstützen diese
Art von Datenstruktur, verwenden aber oft einen anderen Namen, etwa _Hash_,
_Map_, _Objekt_, _Hashtabelle_, _Dictionary_ oder _assoziatives Array_, um nur
einige zu nennen.

Hash-Maps sind nützlich, wenn du Daten nicht über einen Index nachschlagen
willst, wie bei Vektoren, sondern über einen Schlüssel, der einen beliebigen Typ
haben kann. In einem Spiel könntest du zum Beispiel den Punktestand jedes Teams
in einer Hash-Map festhalten, in der jeder Schlüssel der Name eines Teams und
jeder Wert der Punktestand des Teams ist. Mit dem Namen eines Teams kannst du
dann seinen Punktestand abrufen.

In diesem Abschnitt gehen wir die grundlegende API von Hash-Maps durch, aber in
den Funktionen, die die Standardbibliothek für `HashMap<K, V>` definiert,
verbergen sich noch viele weitere nützliche Dinge. Wie immer findest du mehr
Informationen in der Dokumentation der Standardbibliothek.

### Eine neue Hash-Map erstellen {#creating-a-new-hash-map}

Eine Möglichkeit, eine leere Hash-Map zu erstellen, ist `new`, und Elemente fügt
man mit `insert` hinzu. In Listing 8-20 halten wir die Punktestände von zwei
Teams namens _Blue_ und _Yellow_ fest. Das Team Blue beginnt mit 10 Punkten, das
Team Yellow mit 50.

<Listing number="8-20" caption="Eine neue Hash-Map erstellen und einige Schlüssel und Werte einfügen">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-20/src/main.rs:here}}
```

</Listing>

Beachte, dass wir zuerst `HashMap` aus dem Collections-Teil der
Standardbibliothek mit `use` einbinden müssen. Von unseren drei gängigen
Collections wird diese am seltensten verwendet, daher gehört sie nicht zu den
Features, die im Prelude automatisch in den Gültigkeitsbereich (_scope_)
gebracht werden. Hash-Maps werden von der Standardbibliothek auch weniger
unterstützt; es gibt zum Beispiel kein eingebautes Makro, um sie zu erzeugen.

Genau wie Vektoren speichern Hash-Maps ihre Daten auf dem Heap. Diese `HashMap`
hat Schlüssel vom Typ `String` und Werte vom Typ `i32`. Wie Vektoren sind
Hash-Maps homogen: Alle Schlüssel müssen denselben Typ haben, und alle Werte
müssen denselben Typ haben.

### Auf Werte in einer Hash-Map zugreifen {#accessing-values-in-a-hash-map}

Wir können einen Wert aus der Hash-Map holen, indem wir seinen Schlüssel an die
Methode `get` übergeben, wie in Listing 8-21 gezeigt.

<Listing number="8-21" caption="Auf den Punktestand des Teams Blue zugreifen, der in der Hash-Map gespeichert ist">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-21/src/main.rs:here}}
```

</Listing>

Hier hat `score` den Wert, der dem Team Blue zugeordnet ist, und das Ergebnis
ist `10`. Die Methode `get` gibt eine `Option<&V>` zurück; gibt es in der
Hash-Map keinen Wert für diesen Schlüssel, gibt `get` `None` zurück. Dieses
Programm behandelt die `Option`, indem es `copied` aufruft, um eine
`Option<i32>` statt einer `Option<&i32>` zu erhalten, und dann `unwrap_or`, um
`score` auf null zu setzen, falls `scores` keinen Eintrag für den Schlüssel hat.

Wir können über jedes Schlüssel-Wert-Paar in einer Hash-Map ähnlich iterieren
wie bei Vektoren, nämlich mit einer `for`-Schleife:

```rust
{{#rustdoc_include ../listings/ch08-common-collections/no-listing-03-iterate-over-hashmap/src/main.rs:here}}
```

Dieser Code gibt jedes Paar in beliebiger Reihenfolge aus:

```text
Yellow: 50
Blue: 10
```

<!-- Old headings. Do not remove or links may break. -->

<a id="hash-maps-and-ownership"></a>

### Ownership in Hash-Maps verwalten {#managing-ownership-in-hash-maps}

Bei Typen, die den Trait `Copy` implementieren, wie `i32`, werden die Werte in
die Hash-Map kopiert. Bei besessenen Werten wie `String` werden die Werte
verschoben (_moved_), und die Hash-Map wird zum Owner dieser Werte, wie in
Listing 8-22 gezeigt.

<Listing number="8-22" caption="Zeigt, dass Schlüssel und Werte der Hash-Map gehören, sobald sie eingefügt sind">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-22/src/main.rs:here}}
```

</Listing>

Wir können die Variablen `field_name` und `field_value` nicht mehr verwenden,
nachdem sie mit dem Aufruf von `insert` in die Hash-Map verschoben wurden.

Wenn wir Referenzen auf Werte in die Hash-Map einfügen, werden die Werte nicht
in die Hash-Map verschoben. Die Werte, auf die die Referenzen zeigen, müssen
mindestens so lange gültig sein wie die Hash-Map. Über diese Themen sprechen wir
mehr in
[„Referenzen mit Lifetimes validieren“][validating-references-with-lifetimes]<!-- ignore -->
in Kapitel 10.

### Eine Hash-Map aktualisieren {#updating-a-hash-map}

Die Anzahl der Schlüssel-Wert-Paare kann zwar wachsen, aber jedem eindeutigen
Schlüssel kann zu jedem Zeitpunkt nur ein Wert zugeordnet sein (umgekehrt gilt
das nicht: Zum Beispiel könnten sowohl für das Team Blue als auch für das Team
Yellow der Wert `10` in der Hash-Map `scores` gespeichert sein).

Wenn du die Daten in einer Hash-Map ändern willst, musst du entscheiden, wie der
Fall behandelt werden soll, dass einem Schlüssel bereits ein Wert zugewiesen
ist. Du könntest den alten Wert durch den neuen ersetzen und den alten Wert
völlig außer Acht lassen. Du könntest den alten Wert behalten und den neuen
ignorieren, sodass der neue Wert nur hinzugefügt wird, wenn der Schlüssel _noch
keinen_ Wert hat. Oder du könntest den alten und den neuen Wert kombinieren.
Sehen wir uns an, wie jede dieser Möglichkeiten funktioniert!

#### Einen Wert überschreiben {#overwriting-a-value}

Wenn wir einen Schlüssel und einen Wert in eine Hash-Map einfügen und dann
denselben Schlüssel mit einem anderen Wert einfügen, wird der Wert, der diesem
Schlüssel zugeordnet ist, ersetzt. Obwohl der Code in Listing 8-23 `insert`
zweimal aufruft, enthält die Hash-Map nur ein Schlüssel-Wert-Paar, weil wir
beide Male den Wert für den Schlüssel des Teams Blue einfügen.

<Listing number="8-23" caption="Einen Wert ersetzen, der unter einem bestimmten Schlüssel gespeichert ist">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-23/src/main.rs:here}}
```

</Listing>

Dieser Code gibt `{"Blue": 25}` aus. Der ursprüngliche Wert `10` wurde
überschrieben.

<!-- Old headings. Do not remove or links may break. -->

<a id="only-inserting-a-value-if-the-key-has-no-value"></a>

#### Schlüssel und Wert nur hinzufügen, wenn der Schlüssel nicht vorhanden ist {#adding-a-key-and-value-only-if-a-key-isnt-present}

Häufig prüft man, ob ein bestimmter Schlüssel bereits mit einem Wert in der
Hash-Map existiert, und handelt dann so: Existiert der Schlüssel in der
Hash-Map, soll der vorhandene Wert bleiben, wie er ist; existiert der Schlüssel
nicht, fügt man ihn mit einem Wert ein.

Hash-Maps haben dafür eine spezielle API namens `entry`, die den zu prüfenden
Schlüssel als Parameter nimmt. Der Rückgabewert der Methode `entry` ist ein Enum
namens `Entry`, das einen Wert darstellt, der existieren kann oder nicht.
Angenommen, wir wollen prüfen, ob dem Schlüssel für das Team Yellow ein Wert
zugeordnet ist. Ist das nicht der Fall, wollen wir den Wert `50` einfügen, und
dasselbe für das Team Blue. Mit der `entry`-API sieht der Code aus wie in
Listing 8-24.

<Listing number="8-24" caption="Mit der Methode `entry` nur einfügen, wenn der Schlüssel noch keinen Wert hat">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-24/src/main.rs:here}}
```

</Listing>

Die Methode `or_insert` auf `Entry` ist so definiert, dass sie eine
veränderliche (_mutable_) Referenz auf den Wert für den zugehörigen
`Entry`-Schlüssel zurückgibt, falls dieser Schlüssel existiert. Andernfalls fügt
sie den Parameter als neuen Wert für diesen Schlüssel ein und gibt eine
veränderliche Referenz auf den neuen Wert zurück. Diese Technik ist viel
sauberer, als die Logik selbst zu schreiben, und kommt außerdem besser mit dem
Borrow-Checker zurecht.

Führt man den Code in Listing 8-24 aus, wird `{"Yellow": 50, "Blue": 10}`
ausgegeben. Der erste Aufruf von `entry` fügt den Schlüssel für das Team Yellow
mit dem Wert `50` ein, weil das Team Yellow noch keinen Wert hat. Der zweite
Aufruf von `entry` ändert die Hash-Map nicht, weil das Team Blue bereits den
Wert `10` hat.

#### Einen Wert auf Basis des alten Werts aktualisieren {#updating-a-value-based-on-the-old-value}

Ein weiterer häufiger Anwendungsfall für Hash-Maps ist, den Wert eines
Schlüssels nachzuschlagen und ihn dann auf Basis des alten Werts zu
aktualisieren. Listing 8-25 zeigt zum Beispiel Code, der zählt, wie oft jedes
Wort in einem Text vorkommt. Wir verwenden eine Hash-Map mit den Wörtern als
Schlüsseln und erhöhen den Wert, um festzuhalten, wie oft wir das Wort schon
gesehen haben. Sehen wir ein Wort zum ersten Mal, fügen wir zuerst den Wert `0`
ein.

<Listing number="8-25" caption="Vorkommen von Wörtern mit einer Hash-Map zählen, die Wörter und Anzahlen speichert">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-25/src/main.rs:here}}
```

</Listing>

Dieser Code gibt `{"world": 2, "hello": 1, "wonderful": 1}` aus. Vielleicht
siehst du dieselben Schlüssel-Wert-Paare in einer anderen Reihenfolge: Erinnere
dich aus [„Auf Werte in einer Hash-Map zugreifen“][access]<!-- ignore -->, dass
über eine Hash-Map in beliebiger Reihenfolge iteriert wird.

Die Methode `split_whitespace` gibt einen Iterator über die durch Leerraum
getrennten Teil-Slices des Werts in `text` zurück. Die Methode `or_insert` gibt
eine veränderliche Referenz (`&mut V`) auf den Wert für den angegebenen
Schlüssel zurück. Hier speichern wir diese veränderliche Referenz in der
Variable `count`. Um diesem Wert etwas zuzuweisen, müssen wir `count` daher
zuerst mit dem Sternchen (`*`) dereferenzieren. Die veränderliche Referenz
verlässt am Ende der `for`-Schleife den Gültigkeitsbereich, daher sind all diese
Änderungen sicher und nach den Borrowing-Regeln erlaubt.

### Hashfunktionen {#hashing-functions}

Standardmäßig verwendet `HashMap` eine Hashfunktion namens _SipHash_, die
Widerstandsfähigkeit gegen Denial-of-Service-Angriffe (DoS) auf Hashtabellen
bieten kann[^siphash]<!-- ignore -->. Das ist nicht der schnellste verfügbare
Hash-Algorithmus, aber der Gewinn an Sicherheit ist den Verlust an Performance
wert. Wenn du ein Profiling deines Codes machst und feststellst, dass die
Standard-Hashfunktion für deine Zwecke zu langsam ist, kannst du zu einer
anderen Funktion wechseln, indem du einen anderen Hasher angibst. Ein _Hasher_
ist ein Typ, der den Trait `BuildHasher` implementiert. Über Traits und ihre
Implementierung sprechen wir in [Kapitel 10][traits]<!-- ignore -->. Du musst
deinen eigenen Hasher nicht unbedingt von Grund auf implementieren; auf
[crates.io](https://crates.io/)<!-- ignore --> gibt es Bibliotheken, die andere
Rust-Nutzer teilen und die Hasher für viele gängige Hash-Algorithmen
bereitstellen.

[^siphash]: [https://en.wikipedia.org/wiki/SipHash](https://en.wikipedia.org/wiki/SipHash)

{{#quiz ../quizzes/ch08-03-hashmap.toml}}

## Zusammenfassung {#summary}

Vektoren, Strings und Hash-Maps bieten einen Großteil der Funktionalität, die
Programme brauchen, wenn du Daten speichern, auf sie zugreifen und sie ändern
musst. Hier sind einige Übungen, die du jetzt lösen können solltest:

1. Verwende für eine Liste von Ganzzahlen einen Vektor und gib den Median (den
   Wert in der Mitte der sortierten Liste) und den Modus (den Wert, der am
   häufigsten vorkommt; eine Hash-Map ist hier hilfreich) der Liste zurück.
1. Wandle Strings in Pig Latin um. Der erste Konsonant jedes Wortes wird ans
   Ende des Wortes verschoben und _ay_ angehängt, sodass aus _first_ das Wort
   _irst-fay_ wird. An Wörter, die mit einem Vokal beginnen, wird stattdessen
   _hay_ angehängt (aus _apple_ wird _apple-hay_). Denk an die Details der
   UTF-8-Kodierung!
1. Erstelle mit einer Hash-Map und Vektoren eine Textschnittstelle, mit der man
   Namen von Angestellten einer Abteilung in einem Unternehmen hinzufügen kann,
   zum Beispiel „Füge Sally zu Entwicklung hinzu“ oder „Füge Amir zu Vertrieb
   hinzu“. Lass dann eine Liste aller Personen in einer Abteilung oder aller
   Personen im Unternehmen nach Abteilung abrufen, alphabetisch sortiert.

Die API-Dokumentation der Standardbibliothek beschreibt Methoden von Vektoren,
Strings und Hash-Maps, die bei diesen Übungen hilfreich sind!

Wir kommen jetzt zu komplexeren Programmen, in denen Operationen fehlschlagen
können, also ist es der perfekte Zeitpunkt, um über Fehlerbehandlung zu
sprechen. Das machen wir als Nächstes!

[validating-references-with-lifetimes]: ch10-03-lifetime-syntax.html#validating-references-with-lifetimes
[access]: #accessing-values-in-a-hash-map
[traits]: ch10-02-traits.html
