# Fortgeschrittene Features {#advanced-features}

Inzwischen hast du die am häufigsten verwendeten Teile der Programmiersprache
Rust kennengelernt. Bevor wir in Kapitel 21 noch ein weiteres Projekt umsetzen,
sehen wir uns einige Aspekte der Sprache an, denen du hin und wieder begegnen
wirst, die du aber vielleicht nicht jeden Tag verwendest. Du kannst dieses
Kapitel als Nachschlagewerk nutzen, wenn dir etwas Unbekanntes begegnet. Die
hier behandelten Features sind in sehr speziellen Situationen nützlich. Auch
wenn du vielleicht nicht oft zu ihnen greifst, wollen wir sicherstellen, dass du
alle Features kennst, die Rust zu bieten hat.

In diesem Kapitel behandeln wir:

- Unsafe Rust: wie man auf einige Garantien von Rust verzichtet und selbst die
  Verantwortung dafür übernimmt, diese Garantien von Hand einzuhalten
- Fortgeschrittene Traits: assoziierte Typen, Standard-Typparameter, vollständig
  qualifizierte Syntax, Supertraits und das Newtype-Pattern im Zusammenhang mit
  Traits
- Fortgeschrittene Typen: mehr zum Newtype-Pattern, Typaliasse, der Never-Typ
  und Typen mit dynamischer Größe
- Fortgeschrittene Funktionen und Closures: Funktionszeiger und das Zurückgeben
  von Closures
- Makros: Möglichkeiten, Code zu definieren, der zur Kompilierzeit weiteren Code
  definiert

Es ist eine bunte Sammlung von Rust-Features, bei der für jeden etwas dabei ist!
Legen wir los!
