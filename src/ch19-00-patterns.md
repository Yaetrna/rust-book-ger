# Patterns und Matching {#patterns-and-matching}

Patterns sind eine spezielle Syntax in Rust, mit der man die Struktur von Typen,
sowohl komplexen als auch einfachen, abgleichen kann. Wenn du Patterns zusammen
mit `match`-Ausdrücken und anderen Konstrukten verwendest, hast du mehr
Kontrolle über den Kontrollfluss eines Programms. Ein Pattern besteht aus einer
Kombination der folgenden Bestandteile:

- Literale
- Destrukturierte Arrays, Enums, Structs oder Tupel
- Variablen
- Wildcards
- Platzhalter

Beispiele für Patterns sind `x`, `(a, 3)` und `Some(Color::Red)`. In den
Kontexten, in denen Patterns gültig sind, beschreiben diese Bestandteile die
Form von Daten. Unser Programm gleicht dann Werte mit den Patterns ab, um
festzustellen, ob es die richtige Form von Daten hat, um ein bestimmtes
Codestück weiter auszuführen.

Um ein Pattern zu verwenden, vergleichen wir es mit einem Wert. Wenn das Pattern
auf den Wert passt, verwenden wir die Teile des Werts in unserem Code. Erinnere
dich an die `match`-Ausdrücke in Kapitel 6, die Patterns verwendet haben, etwa
das Beispiel mit der Münzsortiermaschine. Wenn der Wert der Form des Patterns
entspricht, können wir die benannten Teile verwenden. Wenn nicht, wird der Code,
der zum Pattern gehört, nicht ausgeführt.

Dieses Kapitel ist eine Referenz zu allem, was mit Patterns zu tun hat. Wir
behandeln die Stellen, an denen Patterns gültig sind, den Unterschied zwischen
abweisbaren (_refutable_) und unabweisbaren (_irrefutable_) Patterns und die
verschiedenen Arten von Pattern-Syntax, die dir begegnen können. Am Ende des
Kapitels weißt du, wie du mit Patterns viele Konzepte klar ausdrücken kannst.
