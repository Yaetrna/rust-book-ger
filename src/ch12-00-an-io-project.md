# Ein I/O-Projekt: Ein Kommandozeilenprogramm bauen {#an-io-project-building-a-command-line-program}

Dieses Kapitel ist eine Wiederholung der vielen Fähigkeiten, die du bisher
gelernt hast, und eine Erkundung einiger weiterer Features der
Standardbibliothek. Wir bauen ein Kommandozeilenwerkzeug, das mit Datei- und
Kommandozeilen-Ein-/Ausgabe arbeitet, um einige der Rust-Konzepte zu üben, die
du jetzt beherrschst.

> **Hinweis:** In diesem Kapitel gibt es keine Quiz, da es nur als praktische
> Schritt-für-Schritt-Anleitung gedacht ist.

Die Geschwindigkeit, die Sicherheit, die Ausgabe als einzelne Binärdatei und die
plattformübergreifende Unterstützung von Rust machen es zu einer idealen Sprache
für Kommandozeilenwerkzeuge. Für unser Projekt erstellen wir daher unsere eigene
Version des klassischen Kommandozeilen-Suchwerkzeugs `grep` (**g**lobally search
a **r**egular **e**xpression and **p**rint, also global nach einem regulären
Ausdruck suchen und ausgeben). Im einfachsten Anwendungsfall durchsucht `grep`
eine angegebene Datei nach einem angegebenen String. Dazu nimmt `grep` einen
Dateipfad und einen String als Argumente. Dann liest es die Datei, findet die
Zeilen in dieser Datei, die das String-Argument enthalten, und gibt diese Zeilen
aus.

Dabei zeigen wir, wie unser Kommandozeilenwerkzeug die Terminal-Features nutzen
kann, die viele andere Kommandozeilenwerkzeuge verwenden. Wir lesen den Wert
einer Umgebungsvariable, damit der Benutzer das Verhalten unseres Werkzeugs
konfigurieren kann. Außerdem geben wir Fehlermeldungen auf den
Standardfehlerstrom der Konsole (`stderr`) statt auf die Standardausgabe
(`stdout`) aus, damit der Benutzer zum Beispiel erfolgreiche Ausgaben in eine
Datei umleiten und Fehlermeldungen trotzdem auf dem Bildschirm sehen kann.

Andrew Gallant, ein Mitglied der Rust-Community, hat bereits eine voll
ausgestattete, sehr schnelle Version von `grep` namens `ripgrep` erstellt. Im
Vergleich dazu ist unsere Version ziemlich einfach, aber dieses Kapitel
vermittelt dir einiges an Hintergrundwissen, das du brauchst, um ein praxisnahes
Projekt wie `ripgrep` zu verstehen.

Unser `grep`-Projekt kombiniert eine Reihe von Konzepten, die du bisher gelernt
hast:

- Code organisieren ([Kapitel 7][ch7]<!-- ignore -->)
- Vektoren und Strings verwenden ([Kapitel 8][ch8]<!-- ignore -->)
- Fehler behandeln ([Kapitel 9][ch9]<!-- ignore -->)
- Traits und Lifetimes verwenden, wo es sinnvoll ist
  ([Kapitel 10][ch10]<!-- ignore -->)
- Tests schreiben ([Kapitel 11][ch11]<!-- ignore -->)

Außerdem stellen wir kurz Closures, Iteratoren und Trait-Objekte vor, die
[Kapitel 13][ch13]<!-- ignore --> und [Kapitel 18][ch18]<!-- ignore -->
ausführlich behandeln.

[ch7]: ch07-00-managing-growing-projects-with-packages-crates-and-modules.html
[ch8]: ch08-00-common-collections.html
[ch9]: ch09-00-error-handling.html
[ch10]: ch10-00-generics.html
[ch11]: ch11-00-testing.html
[ch13]: ch13-00-functional-features.html
[ch18]: ch18-00-oop.html
