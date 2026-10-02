## Alles zusammenführen: Futures, Tasks und Threads {#putting-it-all-together-futures-tasks-and-threads}

Wie wir in [Kapitel 16][ch16]<!-- ignore --> gesehen haben, bieten Threads einen
Ansatz für Nebenläufigkeit. In diesem Kapitel haben wir einen weiteren Ansatz
gesehen: async mit Futures und Streams. Wenn du dich fragst, wann du welche
Methode wählen solltest, lautet die Antwort: Es kommt darauf an! Und in vielen
Fällen lautet die Wahl nicht Threads _oder_ async, sondern Threads _und_ async.

Viele Betriebssysteme bieten schon seit Jahrzehnten Thread-basierte
Nebenläufigkeitsmodelle, und viele Programmiersprachen unterstützen sie deshalb.
Diese Modelle haben jedoch auch ihre Nachteile. Auf vielen Betriebssystemen
verbrauchen sie für jeden Thread eine ganze Menge Speicher. Threads sind
außerdem nur eine Option, wenn dein Betriebssystem und deine Hardware sie
unterstützen. Anders als gängige Desktop- und Mobilgeräte haben manche
eingebetteten Systeme überhaupt kein Betriebssystem und daher auch keine
Threads.

Das async-Modell bietet andere – und letztlich ergänzende – Vor- und Nachteile.
Im async-Modell brauchen nebenläufige Operationen keine eigenen Threads.
Stattdessen können sie auf Tasks laufen, so wie wir im Abschnitt über Streams
`trpl::spawn_task` verwendet haben, um Arbeit aus einer synchronen Funktion
heraus anzustoßen. Ein Task ähnelt einem Thread, wird aber nicht vom
Betriebssystem verwaltet, sondern von Code auf Bibliotheksebene: der Runtime.

Es hat einen Grund, dass die APIs zum Erzeugen von Threads und zum Erzeugen von
Tasks so ähnlich sind. Threads bilden eine Grenze für Mengen synchroner
Operationen; Nebenläufigkeit ist _zwischen_ Threads möglich. Tasks bilden eine
Grenze für Mengen _asynchroner_ Operationen; Nebenläufigkeit ist sowohl
_zwischen_ als auch _innerhalb_ von Tasks möglich, weil ein Task in seinem Rumpf
zwischen Futures wechseln kann. Futures schließlich sind die feinste Einheit der
Nebenläufigkeit in Rust, und jedes Future kann einen Baum anderer Futures
darstellen. Die Runtime – genauer gesagt ihr Executor – verwaltet Tasks, und
Tasks verwalten Futures. In dieser Hinsicht ähneln Tasks leichtgewichtigen, von
der Runtime verwalteten Threads mit zusätzlichen Fähigkeiten, die daher rühren,
dass sie von einer Runtime statt vom Betriebssystem verwaltet werden.

Das bedeutet nicht, dass async-Tasks immer besser sind als Threads (oder
umgekehrt). Nebenläufigkeit mit Threads ist in mancher Hinsicht ein einfacheres
Programmiermodell als Nebenläufigkeit mit `async`. Das kann eine Stärke oder
eine Schwäche sein. Threads funktionieren gewissermaßen nach dem Prinzip „fire
and forget“; sie haben kein natives Gegenstück zu einem Future und laufen daher
einfach bis zum Ende, ohne unterbrochen zu werden, außer durch das
Betriebssystem selbst.

Und es zeigt sich, dass Threads und Tasks oft sehr gut zusammenarbeiten, weil
Tasks (zumindest in manchen Runtimes) zwischen Threads verschoben werden können.
Tatsächlich ist die Runtime, die wir verwendet haben – einschließlich der
Funktionen `spawn_blocking` und `spawn_task` –, unter der Haube standardmäßig
multithreaded! Viele Runtimes verwenden einen Ansatz namens _Work Stealing_, um
Tasks transparent zwischen Threads zu verschieben, je nachdem, wie die Threads
gerade ausgelastet sind, und so die Gesamtleistung des Systems zu verbessern.
Dieser Ansatz erfordert tatsächlich Threads _und_ Tasks und damit auch Futures.

Wenn du überlegst, welche Methode du wann verwenden solltest, beachte diese
Faustregeln:

- Wenn sich die Arbeit _sehr gut parallelisieren_ lässt (also CPU-gebunden ist),
  etwa bei der Verarbeitung einer Menge von Daten, bei denen jeder Teil getrennt
  verarbeitet werden kann, sind Threads die bessere Wahl.
- Wenn die Arbeit _stark nebenläufig_ ist (also I/O-gebunden), etwa bei der
  Verarbeitung von Nachrichten aus einer Reihe verschiedener Quellen, die in
  unterschiedlichen Abständen oder mit unterschiedlicher Häufigkeit eintreffen
  können, ist async die bessere Wahl.

Und wenn du sowohl Parallelität als auch Nebenläufigkeit brauchst, musst du dich
nicht zwischen Threads und async entscheiden. Du kannst sie frei miteinander
kombinieren und jedes das tun lassen, was es am besten kann. Listing 17-25 zeigt
zum Beispiel ein recht typisches Beispiel für eine solche Mischung in realem
Rust-Code.

<Listing number="17-25" caption="Nachrichten mit blockierendem Code in einem Thread senden und in einem async-Block auf die Nachrichten warten" file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-25/src/main.rs:all}}
```

</Listing>

Wir erstellen zunächst einen asynchronen Kanal und erzeugen dann einen Thread,
der mit dem Schlüsselwort `move` die Ownership an der Senderseite des Kanals
übernimmt. Innerhalb des Threads senden wir die Zahlen 1 bis 10 und schlafen
zwischen jeder eine Sekunde lang. Schließlich führen wir ein Future aus, das mit
einem async-Block erstellt und an `trpl::block_on` übergeben wird, so wie wir es
im gesamten Kapitel getan haben. In diesem Future warten wir auf diese
Nachrichten, genau wie in den anderen Beispielen zur Nachrichtenübermittlung,
die wir gesehen haben.

Um auf das Szenario zurückzukommen, mit dem wir das Kapitel eröffnet haben:
Stell dir vor, du führst eine Reihe von Videokodierungs-Tasks in einem eigenen
Thread aus (weil Videokodierung rechengebunden ist), benachrichtigst die
Benutzeroberfläche aber über einen asynchronen Kanal, wenn diese Operationen
erledigt sind. Für solche Kombinationen gibt es in realen Anwendungsfällen
unzählige Beispiele.

## Zusammenfassung {#summary}

Das ist nicht das letzte Mal, dass dir in diesem Buch Nebenläufigkeit begegnet.
Das Projekt in [Kapitel 21][ch21]<!-- ignore --> wendet diese Konzepte in einer
realistischeren Situation an als die einfacheren Beispiele, die wir hier
besprochen haben, und vergleicht Problemlösungen mit Threads und mit Tasks und
Futures direkter.

Ganz gleich, welchen dieser Ansätze du wählst: Rust gibt dir die Werkzeuge, die
du brauchst, um sicheren, schnellen, nebenläufigen Code zu schreiben – sei es
für einen Webserver mit hohem Durchsatz oder ein eingebettetes Betriebssystem.

Als Nächstes sprechen wir über idiomatische Wege, Probleme zu modellieren und
Lösungen zu strukturieren, wenn deine Rust-Programme größer werden. Außerdem
besprechen wir, wie die Idiome von Rust mit denen zusammenhängen, die du
vielleicht aus der objektorientierten Programmierung kennst.

[ch16]: http://localhost:3000/ch16-00-concurrency.html
[combining-futures]: ch17-03-more-futures.html#building-our-own-async-abstractions
[streams]: ch17-04-streams.html#composing-streams
[ch21]: ch21-00-final-project-a-web-server.html
