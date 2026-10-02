# Was ist an diesem Buch anders? {#whats-different-about-this-book}

<!-- de:translator-note:start -->

> **Hinweis zur Übersetzung:** Dies ist eine inoffizielle deutsche Übersetzung der experimentellen Ausgabe von _The Rust Programming Language_ des Cognitive Engineering Lab der Brown University. Grundlage ist der Commit [`88250e0`](https://github.com/cognitive-engineering-lab/rust-book/commit/88250e0392cef0622f318e35469108d68694c1f7) von <https://github.com/cognitive-engineering-lab/rust-book>. Rust-spezifische Begriffe wie Trait, Crate, Ownership oder Borrow-Checker bleiben bewusst englisch, damit du sie in Compiler-Meldungen und in der Dokumentation wiedererkennst.

<!-- de:translator-note:end -->

<div style="display: flex; gap: 2em"> 

Dieses Buch ist ein experimenteller Fork von [_The Rust Programming Language_](http://doc.rust-lang.org/book/), den Forschende am <a href="https://cel.cs.brown.edu/">Cognitive Engineering Lab</a> der Brown University erstellt haben. Falls du neugierig bist: Diese Seite erklärt, was dieses Buch vom ursprünglichen TRPL-Buch unterscheidet. Wenn du aber einfach nur mit Rust loslegen willst, kannst du diese Seite gern überspringen und später zurückkommen.

<div style="display: flex; flex-direction: column; justify-content: center">
  <img src="img/experiment/brown-logo.png" style="min-width: 150px" />
</div>

</div>

## Interaktive Elemente {#interactive-mechanics}

Dieses Buch bietet dir Möglichkeiten, dich beim Lernen aktiv mit Rust auseinanderzusetzen. Zum einen begegnen dir Quiz wie das folgende. Probier es aus, indem du auf „Start“ klickst.

{{#quiz ../quizzes/example-quiz.toml}}

Wenn du eine Frage falsch beantwortest, kannst du das Quiz entweder wiederholen oder dir die richtigen Antworten ansehen. Wir empfehlen dir, das Quiz so lange zu wiederholen, bis du 100 % erreichst – du kannst den Inhalt vor einem neuen Versuch auch gern noch einmal durchgehen. Beachte, dass du das Quiz nicht mehr wiederholen kannst, sobald du dir die richtigen Antworten angesehen hast.

Zum anderen kannst du beliebige Textstellen markieren und deine Gedanken dazu festhalten. Sobald du Text ausgewählt hast, klickst du auf die Schaltfläche ✏️ und hinterlässt optional einen Kommentar.

👉 Markiere doch mal diesen Text! 👈

> **Hinweis:** Deine Markierungen verschwinden, wenn wir den markierten Inhalt ändern. Außerdem werden deine Markierungen in einem Cookie gespeichert. Wenn du Cookies blockierst oder den Browser wechselst, siehst du deine bisherigen Markierungen nicht mehr.

## Inhaltliche Änderungen {#content-changes}

Inhaltlich ist dieses Buch dem TRPL-Buch größtenteils ähnlich, und wir gleichen die beiden Bücher alle paar Monate ab. Der größte Unterschied ist das Kapitel [Ownership verstehen][understanding-ownership]. Dieses Buch erklärt Ownership mit Ideen und Visualisierungen, die laut unserer Forschung dein Verständnis von Rust besser fördern als das ursprüngliche Buch. Du wirst viele Diagramme wie die folgenden sehen, die das Verhalten von Rust zur Kompilierzeit und zur Laufzeit mit [Aquascope][aquascope] veranschaulichen:

```aquascope,interpreter,horizontal
#fn main() {
let mut s = String::from("Hello world");`[]`
let hello = &s[0..5];`[]`
s.push_str("!");`[]`
drop(s);`[]`
#}
```

Über Ownership hinaus haben wir eine Reihe kleiner Änderungen am Buch vorgenommen, um Missverständnisse anzugehen, die wir in den Quizantworten beobachtet haben. Wenn dir in einem Quiz oder an einer anderen Stelle des Buchs ein Problem auffällt, kannst du in unserem GitHub-Repository ein Issue anlegen: <https://github.com/cognitive-engineering-lab/rust-book>

_Möchtest du an weiteren Experimenten teilnehmen, die Rust leichter erlernbar und benutzbar machen sollen? Dann melde dich hier an:_ <https://forms.gle/U3jEUkb2fGXykp1DA>

## Veröffentlichungen {#publications}

Bisher sind aus diesem Experiment zwei frei zugängliche Veröffentlichungen hervorgegangen. Schau sie dir an, wenn dich die wissenschaftliche Forschung hinter diesem Buch interessiert:

- [„Profiling Programming Language Learning“](https://dl.acm.org/doi/10.1145/3649812) <br />
  [Will Crichton][will] und [Shriram Krishnamurthi][shriram]. OOPSLA 2024. (Distinguished Paper.)

- [„A Grounded Conceptual Model for Ownership Types in Rust“](https://dl.acm.org/doi/10.1145/3622841) <br />
  [Will Crichton][will], [Gavin Gray][gavin] und [Shriram Krishnamurthi][shriram]. OOPSLA 2023. (SIGPLAN Research Highlight und Communications of the ACM Research Highlight.)

## Danksagung {#acknowledgments}

Diese Arbeit wurde teilweise von der DARPA im Rahmen der Vereinbarung Nr. HR00112420354, teilweise von der NSF unter der Förderungsnummer CCF-2227863 und teilweise von Amazon Web Services unterstützt. Alle in diesem Material geäußerten Meinungen, Ergebnisse, Schlussfolgerungen und Empfehlungen sind die der Autoren und spiegeln nicht unbedingt die Ansichten unserer Geldgeber wider. Wir danken Carol Nichols und der Rust Foundation dafür, dass sie das Experiment bekannt gemacht haben. TRPL ist das Ergebnis der harten Arbeit vieler Menschen, lange bevor wir mit diesem Experiment begonnen haben.

[understanding-ownership]: ch04-00-understanding-ownership.html
[aquascope]: https://cognitive-engineering-lab.github.io/aquascope/
[will]: https://willcrichton.net/
[gavin]: https://gavinleroy.com/
[shriram]: https://cs.brown.edu/people/sk/
