# Furchtlose Nebenläufigkeit {#fearless-concurrency}

Nebenläufige Programmierung sicher und effizient zu handhaben, ist ein weiteres
wichtiges Ziel von Rust. _Nebenläufige Programmierung_ (_concurrent
programming_), bei der verschiedene Teile eines Programms unabhängig voneinander
ausgeführt werden, und _parallele Programmierung_ (_parallel programming_), bei
der verschiedene Teile eines Programms gleichzeitig ausgeführt werden, werden
immer wichtiger, da immer mehr Computer ihre mehreren Prozessoren nutzen. In der
Vergangenheit war das Programmieren in diesen Kontexten schwierig und
fehleranfällig. Rust hofft, das zu ändern.

Anfangs dachte das Rust-Team, dass die Gewährleistung von Speichersicherheit und
die Vermeidung von Nebenläufigkeitsproblemen zwei getrennte Herausforderungen
seien, die mit unterschiedlichen Methoden gelöst werden müssten. Mit der Zeit
stellte das Team fest, dass das Ownership- und das Typsystem eine
leistungsfähige Sammlung von Werkzeugen sind, um Probleme mit Speichersicherheit
_und_ Nebenläufigkeit zu bewältigen! Durch Ownership und Typprüfung sind viele
Nebenläufigkeitsfehler in Rust Fehler zur Kompilierzeit statt zur Laufzeit.
Statt also viel Zeit damit zu verbringen, die genauen Umstände zu reproduzieren,
unter denen ein Nebenläufigkeitsbug zur Laufzeit auftritt, kompiliert
fehlerhafter Code gar nicht erst und zeigt einen Fehler an, der das Problem
erklärt. Dadurch kannst du deinen Code korrigieren, während du daran arbeitest,
statt womöglich erst, nachdem er in Produktion gegangen ist. Wir haben diesen
Aspekt von Rust _furchtlose Nebenläufigkeit_ (_fearless concurrency_) getauft.
Mit furchtloser Nebenläufigkeit kannst du Code schreiben, der frei von subtilen
Bugs ist und sich leicht refaktorisieren lässt, ohne neue Bugs einzuführen.

> Note: Der Einfachheit halber bezeichnen wir viele der Probleme als
> _nebenläufig_, statt genauer _nebenläufig und/oder parallel_ zu sagen. Ersetze
> in diesem Kapitel _nebenläufig_ bitte gedanklich durch _nebenläufig und/oder
> parallel_. Im nächsten Kapitel, in dem die Unterscheidung wichtiger ist, sind
> wir genauer.

Viele Sprachen sind dogmatisch, was die Lösungen angeht, die sie zur Behandlung
nebenläufiger Probleme anbieten. Erlang hat zum Beispiel elegante Funktionalität
für Nebenläufigkeit mit Nachrichtenübermittlung, aber nur obskure Möglichkeiten,
Zustand zwischen Threads zu teilen. Nur eine Teilmenge möglicher Lösungen zu
unterstützen, ist eine vernünftige Strategie für Sprachen auf höherer Ebene,
weil eine Sprache auf höherer Ebene verspricht, dass man davon profitiert, etwas
Kontrolle für Abstraktionen aufzugeben. Von Sprachen auf niedrigerer Ebene wird
dagegen erwartet, dass sie in jeder Situation die Lösung mit der besten
Performance bieten und weniger Abstraktionen über der Hardware haben. Daher
bietet Rust eine Vielzahl von Werkzeugen, um Probleme so zu modellieren, wie es
für deine Situation und deine Anforderungen angemessen ist.

Diese Themen behandeln wir in diesem Kapitel:

- Wie man Threads erzeugt, um mehrere Codeteile gleichzeitig auszuführen
- Nebenläufigkeit mit _Nachrichtenübermittlung_ (_message passing_), bei der
  Kanäle Nachrichten zwischen Threads senden
- Nebenläufigkeit mit _geteiltem Zustand_ (_shared state_), bei der mehrere
  Threads Zugriff auf bestimmte Daten haben
- Die Traits `Sync` und `Send`, die die Nebenläufigkeitsgarantien von Rust auf
  benutzerdefinierte Typen sowie auf Typen der Standardbibliothek ausdehnen
