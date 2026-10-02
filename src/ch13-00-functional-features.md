# Funktionale Sprachfeatures: Iteratoren und Closures {#functional-language-features-iterators-and-closures}

Das Design von Rust ist von vielen bestehenden Sprachen und Techniken
inspiriert, und ein wichtiger Einfluss ist die _funktionale Programmierung_.
Programmieren im funktionalen Stil bedeutet oft, Funktionen als Werte zu
verwenden, indem man sie als Argumente übergibt, aus anderen Funktionen
zurückgibt, Variablen zur späteren Ausführung zuweist und so weiter.

In diesem Kapitel diskutieren wir nicht, was funktionale Programmierung ist oder
nicht ist, sondern besprechen einige Features von Rust, die Features in vielen
Sprachen ähneln, die oft als funktional bezeichnet werden.

Konkret behandeln wir:

- _Closures_, ein funktionsähnliches Konstrukt, das du in einer Variable
  speichern kannst
- _Iteratoren_, eine Möglichkeit, eine Folge von Elementen zu verarbeiten
- Wie man Closures und Iteratoren verwendet, um das I/O-Projekt aus Kapitel 12
  zu verbessern
- Die Performance von Closures und Iteratoren (Spoiler: Sie sind schneller, als
  du vielleicht denkst!)

Wir haben bereits einige andere Features von Rust behandelt, etwa
Pattern-Matching und Enums, die ebenfalls vom funktionalen Stil beeinflusst
sind. Da es ein wichtiger Teil des Schreibens von schnellem, idiomatischem
Rust-Code ist, Closures und Iteratoren zu beherrschen, widmen wir ihnen dieses
ganze Kapitel.
