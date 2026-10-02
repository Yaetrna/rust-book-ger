# Einführung {#introduction}

> Note: Diese Auflage des Buchs entspricht
> [The Rust Programming Language][nsprust], das gedruckt und als E-Book bei
> [No Starch Press][nsp] erhältlich ist.

[nsprust]: https://nostarch.com/rust-programming-language-3rd-edition
[nsp]: https://nostarch.com/

Willkommen bei _The Rust Programming Language_, einem einführenden Buch über
Rust. Die Programmiersprache Rust hilft dir dabei, schnellere und zuverlässigere
Software zu schreiben. Im Design von Programmiersprachen stehen
High-Level-Ergonomie und Low-Level-Kontrolle oft im Widerspruch zueinander; Rust
stellt diesen Konflikt infrage. Indem Rust leistungsstarke technische
Möglichkeiten mit einer großartigen Developer Experience verbindet, gibt es dir
die Möglichkeit, Low-Level-Details (wie die Speichernutzung) zu kontrollieren,
ohne all die Mühe, die traditionell mit solcher Kontrolle verbunden ist.

## Für wen Rust gedacht ist {#who-rust-is-for}

Rust ist aus verschiedenen Gründen für viele Menschen ideal. Sehen wir uns
einige der wichtigsten Gruppen an.

### Entwicklungsteams {#teams-of-developers}

Rust erweist sich als produktives Werkzeug für die Zusammenarbeit in großen
Entwicklungsteams, deren Mitglieder unterschiedlich viel über
Systemprogrammierung wissen. Low-Level-Code ist anfällig für verschiedene
subtile Fehler, die sich in den meisten anderen Sprachen nur durch umfangreiche
Tests und sorgfältige Code-Reviews erfahrener Entwicklerinnen und Entwickler
aufspüren lassen. In Rust übernimmt der Compiler die Rolle eines Türstehers: Er
weigert sich, Code mit diesen schwer fassbaren Fehlern zu kompilieren,
einschließlich Nebenläufigkeitsfehlern. Indem das Team mit dem Compiler
zusammenarbeitet, kann es seine Zeit auf die Logik des Programms konzentrieren,
statt Fehlern hinterherzujagen.

Rust bringt außerdem zeitgemäße Entwicklungswerkzeuge in die Welt der
Systemprogrammierung:

- Cargo, der mitgelieferte Abhängigkeitsmanager und das Build-Werkzeug, macht
  das Hinzufügen, Kompilieren und Verwalten von Abhängigkeiten im gesamten
  Rust-Ökosystem mühelos und einheitlich.
- Das Formatierungswerkzeug `rustfmt` sorgt für einen einheitlichen
  Programmierstil über alle Entwicklerinnen und Entwickler hinweg.
- Der Rust Language Server ermöglicht die Integration in Entwicklungsumgebungen
  (IDEs) für Codevervollständigung und Fehlermeldungen direkt im Code.

Mit diesen und weiteren Werkzeugen aus dem Rust-Ökosystem können Entwicklerinnen
und Entwickler produktiv arbeiten, während sie Code auf Systemebene schreiben.

### Studierende {#students}

Rust ist für Studierende und alle, die sich für Systemkonzepte interessieren.
Mit Rust haben viele Menschen Themen wie die Entwicklung von Betriebssystemen
kennengelernt. Die Community ist sehr einladend und beantwortet gern Fragen von
Studierenden. Mit Projekten wie diesem Buch wollen die Rust-Teams Systemkonzepte
mehr Menschen zugänglich machen, besonders denen, die neu beim Programmieren
sind.

### Unternehmen {#companies}

Hunderte große und kleine Unternehmen setzen Rust in der Produktion für
vielfältige Aufgaben ein, darunter Kommandozeilenwerkzeuge, Webdienste,
DevOps-Werkzeuge, eingebettete Geräte, Audio- und Videoanalyse und
-transkodierung, Kryptowährungen, Bioinformatik, Suchmaschinen, Anwendungen für
das Internet der Dinge, maschinelles Lernen und sogar wesentliche Teile des
Webbrowsers Firefox.

### Open-Source-Entwicklerinnen und -Entwickler {#open-source-developers}

Rust ist für Menschen, die die Programmiersprache Rust, die Community,
Entwicklungswerkzeuge und Bibliotheken mitgestalten wollen. Wir würden uns
freuen, wenn du zur Sprache Rust beiträgst.

### Menschen, denen Geschwindigkeit und Stabilität wichtig sind {#people-who-value-speed-and-stability}

Rust ist für Menschen, die sich von einer Sprache Geschwindigkeit und Stabilität
wünschen. Mit Geschwindigkeit meinen wir sowohl, wie schnell Rust-Code laufen
kann, als auch, wie schnell du mit Rust Programme schreiben kannst. Die
Prüfungen des Rust-Compilers sorgen für Stabilität, wenn Features hinzukommen
oder Code refaktorisiert wird. Das steht im Gegensatz zu fragilem Legacy-Code in
Sprachen ohne diese Prüfungen, den Entwicklerinnen und Entwickler oft nur ungern
anfassen. Indem Rust Zero-Cost-Abstraktionen anstrebt – höhere Features, die zu
ebenso schnellem Low-Level-Code kompiliert werden wie von Hand geschriebener
Code –, bemüht es sich, sicheren Code auch zu schnellem Code zu machen.

Die Sprache Rust möchte auch viele weitere Nutzerinnen und Nutzer unterstützen;
die hier genannten sind nur einige der wichtigsten Gruppen. Insgesamt ist es das
größte Ziel von Rust, die Kompromisse abzuschaffen, die Programmiererinnen und
Programmierer seit Jahrzehnten hingenommen haben, indem es Sicherheit _und_
Produktivität, Geschwindigkeit _und_ Ergonomie bietet. Probier Rust aus und
finde heraus, ob seine Entscheidungen für dich passen.

## Für wen dieses Buch gedacht ist {#who-this-book-is-for}

Dieses Buch setzt voraus, dass du schon in einer anderen Programmiersprache Code
geschrieben hast, macht aber keine Annahmen darüber, in welcher. Wir haben
versucht, den Stoff für Menschen mit ganz unterschiedlichem
Programmierhintergrund zugänglich zu machen. Wir verbringen nicht viel Zeit
damit, darüber zu sprechen, was Programmieren _ist_ oder wie man darüber
nachdenkt. Wenn du ganz neu beim Programmieren bist, ist dir mit einem Buch, das
speziell eine Einführung ins Programmieren bietet, besser gedient.

## Wie du dieses Buch verwendest {#how-to-use-this-book}

Im Allgemeinen geht dieses Buch davon aus, dass du es der Reihe nach von vorn
bis hinten liest. Spätere Kapitel bauen auf Konzepten aus früheren Kapiteln auf,
und frühere Kapitel gehen bei einem Thema vielleicht nicht in die Tiefe, greifen
es aber in einem späteren Kapitel wieder auf.

In diesem Buch findest du zwei Arten von Kapiteln: Konzeptkapitel und
Projektkapitel. In Konzeptkapiteln lernst du einen Aspekt von Rust kennen. In
Projektkapiteln bauen wir gemeinsam kleine Programme und wenden an, was du bis
dahin gelernt hast. Kapitel 2, Kapitel 12 und Kapitel 21 sind Projektkapitel;
die übrigen sind Konzeptkapitel.

**Kapitel 1** erklärt, wie du Rust installierst, wie du ein „Hello,
world!“-Programm schreibst und wie du Cargo verwendest, den Paketmanager und das
Build-Werkzeug von Rust. **Kapitel 2** ist eine praktische Einführung in das
Schreiben eines Programms in Rust, bei der du ein Zahlenratespiel baust. Hier
behandeln wir Konzepte nur im Überblick; spätere Kapitel liefern weitere
Details. Wenn du sofort selbst Hand anlegen willst, ist Kapitel 2 genau das
Richtige. Wenn du besonders gründlich lernst und lieber jedes Detail kennst,
bevor du weitermachst, möchtest du Kapitel 2 vielleicht überspringen und direkt
zu **Kapitel 3** gehen, das Features von Rust behandelt, die denen anderer
Programmiersprachen ähneln; danach kannst du zu Kapitel 2 zurückkehren, wenn du
an einem Projekt arbeiten möchtest, in dem du die gelernten Details anwendest.

In **Kapitel 4** lernst du das Ownership-System von Rust kennen. **Kapitel 5**
behandelt Structs und Methoden. **Kapitel 6** behandelt Enums, `match`-Ausdrücke
sowie die Kontrollflusskonstrukte `if let` und `let...else`. Mit Structs und
Enums erstellst du eigene Typen.

In **Kapitel 7** lernst du das Modulsystem von Rust kennen und die
Sichtbarkeitsregeln, mit denen du deinen Code und seine öffentliche
Programmierschnittstelle (API) organisierst. **Kapitel 8** behandelt einige
gängige Collection-Datenstrukturen, die die Standardbibliothek bereitstellt:
Vektoren, Strings und Hash-Maps. **Kapitel 9** erkundet die Philosophie und die
Techniken der Fehlerbehandlung in Rust.

**Kapitel 10** taucht in Generics, Traits und Lifetimes ein, mit denen du Code
definieren kannst, der für mehrere Typen gilt. In **Kapitel 11** dreht sich
alles ums Testen, das auch mit den Sicherheitsgarantien von Rust nötig ist, um
sicherzustellen, dass die Logik deines Programms korrekt ist. In **Kapitel 12**
bauen wir unsere eigene Implementierung eines Teils der Funktionalität des
Kommandozeilenwerkzeugs `grep`, das Text in Dateien sucht. Dafür verwenden wir
viele der Konzepte, die wir in den vorherigen Kapiteln besprochen haben.

**Kapitel 13** erkundet Closures und Iteratoren: Features von Rust, die aus
funktionalen Programmiersprachen stammen. In **Kapitel 14** sehen wir uns Cargo
genauer an und sprechen über bewährte Vorgehensweisen, um deine Bibliotheken mit
anderen zu teilen. **Kapitel 15** behandelt Smart-Pointer, die die
Standardbibliothek bereitstellt, und die Traits, die ihre Funktionalität
ermöglichen.

In **Kapitel 16** gehen wir verschiedene Modelle der nebenläufigen
Programmierung durch und sprechen darüber, wie Rust dir hilft, furchtlos mit
mehreren Threads zu programmieren. In **Kapitel 17** bauen wir darauf auf und
erkunden die Syntax von async und await in Rust, zusammen mit Tasks, Futures und
Streams und dem leichtgewichtigen Nebenläufigkeitsmodell, das sie ermöglichen.

**Kapitel 18** betrachtet, wie sich Rust-Idiome zu Prinzipien der
objektorientierten Programmierung verhalten, die du vielleicht kennst. **Kapitel
19** ist eine Referenz zu Patterns und Pattern-Matching, mit denen sich Ideen in
Rust-Programmen auf mächtige Weise ausdrücken lassen. **Kapitel 20** enthält ein
bunt gemischtes Buffet fortgeschrittener Themen, darunter Unsafe Rust, Makros
und mehr über Lifetimes, Traits, Typen, Funktionen und Closures.

In **Kapitel 21** schließen wir ein Projekt ab, in dem wir einen
Low-Level-Webserver mit mehreren Threads implementieren!

Am Ende enthalten einige Anhänge nützliche Informationen über die Sprache in
einem eher nachschlageartigen Format. **Anhang A** behandelt die Schlüsselwörter
von Rust, **Anhang B** die Operatoren und Symbole von Rust, **Anhang C** die
ableitbaren Traits der Standardbibliothek, **Anhang D** einige nützliche
Entwicklungswerkzeuge, und **Anhang E** erklärt die Editionen von Rust. In
**Anhang F** findest du Übersetzungen des Buchs, und in **Anhang G** erklären
wir, wie Rust entsteht und was Nightly Rust ist.

Es gibt keine falsche Art, dieses Buch zu lesen: Wenn du vorspringen willst, nur
zu! Vielleicht musst du zu früheren Kapiteln zurückspringen, falls dir etwas
unklar ist. Aber mach es so, wie es für dich am besten funktioniert.

<span id="ferris"></span>

Ein wichtiger Teil beim Lernen von Rust ist es, die Fehlermeldungen lesen zu
lernen, die der Compiler anzeigt: Sie führen dich zu funktionierendem Code.
Deshalb zeigen wir viele Beispiele, die sich nicht kompilieren lassen, zusammen
mit der Fehlermeldung, die der Compiler in der jeweiligen Situation anzeigt.
Wenn du also ein beliebiges Beispiel eingibst und ausführst, lässt es sich
möglicherweise nicht kompilieren! Lies unbedingt den umgebenden Text, um zu
sehen, ob das Beispiel, das du ausführen willst, einen Fehler erzeugen soll. In
den meisten Fällen führen wir dich zur korrekten Version von Code, der sich
nicht kompilieren lässt. Ferris hilft dir außerdem dabei, Code zu erkennen, der
nicht funktionieren soll:

| Ferris                                                                                                                           | Bedeutung                                         |
| -------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------- |
| <img src="img/ferris/does_not_compile.svg" class="ferris-explain" alt="Ferris mit einem Fragezeichen"/>                          | Dieser Code lässt sich nicht kompilieren!         |
| <img src="img/ferris/panics.svg" class="ferris-explain" alt="Ferris, die Hände in die Luft werfend"/>                            | Dieser Code löst einen Panic aus!                 |
| <img src="img/ferris/not_desired_behavior.svg" class="ferris-explain" alt="Ferris mit einer erhobenen Schere, schulterzuckend"/> | Dieser Code zeigt nicht das gewünschte Verhalten. |

In den meisten Fällen führen wir dich zur korrekten Version von Code, der sich
nicht kompilieren lässt.

## Quellcode {#source-code}

Die Quelldateien, aus denen dieses Buch erzeugt wird, findest du auf
[GitHub][book].

[book]: https://github.com/rust-lang/book/tree/main/src
