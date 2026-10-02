# Gängige Collections {#common-collections}

Die Standardbibliothek von Rust enthält eine Reihe sehr nützlicher
Datenstrukturen, die _Collections_ genannt werden. Die meisten anderen
Datentypen stellen einen bestimmten Wert dar, Collections dagegen können mehrere
Werte enthalten. Anders als bei den eingebauten Array- und Tupel-Typen werden
die Daten, auf die diese Collections zeigen, auf dem Heap gespeichert. Das
bedeutet, dass die Datenmenge zur Kompilierzeit nicht bekannt sein muss und
während der Programmausführung wachsen oder schrumpfen kann. Jede Art von
Collection hat unterschiedliche Fähigkeiten und Kosten, und für deine aktuelle
Situation eine passende auszuwählen, ist eine Fähigkeit, die du mit der Zeit
entwickelst. In diesem Kapitel besprechen wir drei Collections, die in
Rust-Programmen sehr häufig verwendet werden:

- Ein _Vektor_ erlaubt dir, eine variable Anzahl von Werten nebeneinander zu
  speichern.
- Ein _String_ ist eine Collection von Zeichen. Den Typ `String` haben wir schon
  erwähnt, aber in diesem Kapitel sprechen wir ausführlich über ihn.
- Eine _Hash-Map_ erlaubt dir, einen Wert mit einem bestimmten Schlüssel zu
  verknüpfen. Sie ist eine bestimmte Implementierung der allgemeineren
  Datenstruktur namens _Map_.

Mehr über die anderen Arten von Collections, die die Standardbibliothek
bereitstellt, erfährst du in [der Dokumentation][collections].

Wir besprechen, wie man Vektoren, Strings und Hash-Maps erstellt und
aktualisiert und was jede davon besonders macht.

[collections]: https://doc.rust-lang.org/std/collections/index.html
