<!-- Old headings. Do not remove or links may break. -->

<a id="comparing-performance-loops-vs-iterators"></a>

## Performance von Schleifen und Iteratoren {#performance-in-loops-vs-iterators}

Um zu entscheiden, ob du Schleifen oder Iteratoren verwenden solltest, musst du
wissen, welche Implementierung schneller ist: die Version der Funktion `search`
mit einer expliziten `for`-Schleife oder die Version mit Iteratoren.

Wir haben einen Benchmark durchgeführt, bei dem wir den gesamten Inhalt von _The
Adventures of Sherlock Holmes_ von Sir Arthur Conan Doyle in einen `String`
geladen und im Inhalt nach dem Wort _the_ gesucht haben. Hier sind die
Ergebnisse des Benchmarks für die Version von `search` mit der `for`-Schleife
und die Version mit Iteratoren:

```text
test bench_search_for  ... bench:  19,620,300 ns/iter (+/- 915,700)
test bench_search_iter ... bench:  19,234,900 ns/iter (+/- 657,200)
```

Die beiden Implementierungen haben eine ähnliche Performance! Wir erklären den
Benchmark-Code hier nicht, weil es nicht darum geht zu beweisen, dass die beiden
Versionen gleichwertig sind, sondern ein allgemeines Gefühl dafür zu bekommen,
wie sich diese beiden Implementierungen in Sachen Performance vergleichen.

Für einen umfassenderen Benchmark solltest du verschiedene Texte
unterschiedlicher Größe als `contents`, verschiedene Wörter und Wörter
unterschiedlicher Länge als `query` und alle möglichen anderen Variationen
prüfen. Worauf es ankommt: Iteratoren sind zwar eine Abstraktion auf hoher
Ebene, werden aber zu ungefähr demselben Code kompiliert, als hättest du den
Code auf niedrigerer Ebene selbst geschrieben. Iteratoren sind eine der
_Zero-Cost-Abstraktionen_ (_zero-cost abstractions_) von Rust, womit wir meinen,
dass die Verwendung der Abstraktion keinen zusätzlichen Laufzeitaufwand
verursacht. Das entspricht der Art, wie Bjarne Stroustrup, der ursprüngliche
Designer und Implementierer von C++, „Zero-Overhead“ in seinem Keynote-Vortrag
„Foundations of C++“ auf der ETAPS 2012 definiert:

> Im Allgemeinen folgen C++-Implementierungen dem Zero-Overhead-Prinzip: Was du
> nicht verwendest, dafür zahlst du nicht. Und weiter: Was du verwendest,
> könntest du von Hand nicht besser programmieren.

In vielen Fällen wird Rust-Code mit Iteratoren zu demselben Assembler-Code
kompiliert, den du von Hand schreiben würdest. Optimierungen wie das Abrollen
von Schleifen (_loop unrolling_) und das Entfernen von Grenzprüfungen beim
Array-Zugriff greifen und machen den resultierenden Code äußerst effizient.
Jetzt, da du das weißt, kannst du Iteratoren und Closures ohne Bedenken
verwenden! Sie lassen Code abstrakter wirken, kosten dafür aber keine
Performance zur Laufzeit.

## Zusammenfassung {#summary}

Closures und Iteratoren sind Features von Rust, die von Ideen funktionaler
Programmiersprachen inspiriert sind. Sie tragen dazu bei, dass Rust Ideen auf
hoher Ebene klar ausdrücken kann und dabei die Performance von Code auf
niedriger Ebene erreicht. Closures und Iteratoren sind so implementiert, dass
die Performance zur Laufzeit nicht beeinträchtigt wird. Das ist Teil des Ziels
von Rust, Zero-Cost-Abstraktionen bereitzustellen.

Nachdem wir die Ausdrucksstärke unseres I/O-Projekts verbessert haben, sehen wir
uns einige weitere Features von `cargo` an, mit denen wir das Projekt mit der
Welt teilen können.
