# Grundlagen der asynchronen Programmierung: Async, Await, Futures und Streams {#fundamentals-of-asynchronous-programming-async-await-futures-and-streams}

Viele Operationen, um die wir den Computer bitten, können eine Weile dauern. Es
wäre schön, wenn wir etwas anderes tun könnten, während wir darauf warten, dass
diese langwierigen Prozesse abgeschlossen werden. Moderne Computer bieten zwei
Techniken, um an mehr als einer Operation gleichzeitig zu arbeiten: Parallelität
und Nebenläufigkeit. Die Logik unserer Programme ist aber größtenteils linear
geschrieben. Wir würden gern die Operationen angeben können, die ein Programm
ausführen soll, sowie Stellen, an denen eine Funktion pausieren und stattdessen
ein anderer Teil des Programms laufen könnte, ohne vorab genau festlegen zu
müssen, in welcher Reihenfolge und auf welche Weise jedes Stück Code laufen
soll. _Asynchrone Programmierung_ ist eine Abstraktion, mit der wir unseren Code
in Form möglicher Pausenpunkte und späterer Ergebnisse ausdrücken können und die
sich für uns um die Details der Koordination kümmert.

Dieses Kapitel baut auf der Verwendung von Threads für Parallelität und
Nebenläufigkeit aus Kapitel 16 auf und stellt einen alternativen Ansatz zum
Schreiben von Code vor: die Futures und Streams von Rust, die Syntax `async` und
`await`, mit der wir ausdrücken können, wie Operationen asynchron sein könnten,
und die Crates von Drittanbietern, die asynchrone Runtimes implementieren: Code,
der die Ausführung asynchroner Operationen verwaltet und koordiniert.

Betrachten wir ein Beispiel. Angenommen, du exportierst ein Video, das du von
einer Familienfeier erstellt hast, eine Operation, die zwischen Minuten und
Stunden dauern kann. Der Videoexport nutzt so viel CPU- und GPU-Leistung, wie er
kann. Hättest du nur einen CPU-Kern und würde dein Betriebssystem diesen Export
nicht pausieren, bis er abgeschlossen ist – würde es den Export also _synchron_
ausführen –, könntest du nichts anderes auf deinem Computer tun, solange diese
Aufgabe läuft. Das wäre ziemlich frustrierend. Zum Glück kann das Betriebssystem
deines Computers den Export unsichtbar oft genug unterbrechen, damit du
gleichzeitig andere Arbeit erledigen kannst, und tut das auch.

Angenommen, du lädst jetzt ein Video herunter, das jemand anderes geteilt hat.
Auch das kann eine Weile dauern, beansprucht aber nicht so viel CPU-Zeit. In
diesem Fall muss die CPU warten, bis Daten aus dem Netzwerk ankommen. Du kannst
zwar mit dem Lesen der Daten beginnen, sobald sie ankommen, aber es kann einige
Zeit dauern, bis alle da sind. Selbst wenn alle Daten vorhanden sind, kann es
bei einem recht großen Video mindestens ein oder zwei Sekunden dauern, alles zu
laden. Das klingt vielleicht nicht nach viel, ist aber eine sehr lange Zeit für
einen modernen Prozessor, der jede Sekunde Milliarden von Operationen ausführen
kann. Auch hier unterbricht dein Betriebssystem dein Programm unsichtbar, damit
die CPU andere Arbeit erledigen kann, während sie darauf wartet, dass der
Netzwerkaufruf abgeschlossen wird.

Der Videoexport ist ein Beispiel für eine _CPU-gebundene_ (_CPU-bound_) oder
_rechengebundene_ (_compute-bound_) Operation. Sie ist durch die mögliche
Datenverarbeitungsgeschwindigkeit des Computers in der CPU oder GPU begrenzt und
dadurch, wie viel dieser Geschwindigkeit er der Operation widmen kann. Der
Videodownload ist ein Beispiel für eine _I/O-gebundene_ (_I/O-bound_) Operation,
weil er durch die Geschwindigkeit der _Ein- und Ausgabe_ des Computers begrenzt
ist; er kann nur so schnell sein, wie die Daten über das Netzwerk gesendet
werden können.

In beiden Beispielen bieten die unsichtbaren Unterbrechungen des Betriebssystems
eine Form von Nebenläufigkeit. Diese Nebenläufigkeit findet allerdings nur auf
der Ebene des gesamten Programms statt: Das Betriebssystem unterbricht ein
Programm, damit andere Programme Arbeit erledigen können. Da wir unsere
Programme auf einer viel feineren Ebene verstehen als das Betriebssystem, können
wir in vielen Fällen Gelegenheiten für Nebenläufigkeit erkennen, die das
Betriebssystem nicht sehen kann.

Wenn wir zum Beispiel ein Werkzeug zum Verwalten von Dateidownloads bauen,
sollten wir unser Programm so schreiben können, dass das Starten eines Downloads
die Benutzeroberfläche nicht blockiert, und Benutzer sollten mehrere Downloads
gleichzeitig starten können. Viele APIs von Betriebssystemen für die Interaktion
mit dem Netzwerk sind aber _blockierend_ (_blocking_); das heißt, sie blockieren
den Fortschritt des Programms, bis die Daten, die sie verarbeiten, vollständig
bereit sind.

> Note: Genau genommen funktionieren _die meisten_ Funktionsaufrufe so. Der
> Begriff _blockierend_ ist aber meist Funktionsaufrufen vorbehalten, die mit
> Dateien, dem Netzwerk oder anderen Ressourcen des Computers interagieren, denn
> das sind die Fälle, in denen ein einzelnes Programm davon profitieren würde,
> dass die Operation _nicht_ blockierend ist.

Wir könnten das Blockieren unseres Haupt-Threads vermeiden, indem wir für jeden
Download einen eigenen Thread erzeugen. Der Mehraufwand an Systemressourcen, den
diese Threads verbrauchen, würde aber irgendwann zum Problem. Besser wäre es,
wenn der Aufruf gar nicht erst blockieren würde und wir stattdessen eine Reihe
von Aufgaben definieren könnten, die unser Programm erledigen soll, und die
Runtime die beste Reihenfolge und Art ihrer Ausführung wählen ließen.

Genau das bietet uns die Abstraktion _async_ (kurz für _asynchron_) von Rust. In
diesem Kapitel lernst du alles über Async, während wir folgende Themen
behandeln:

- Wie man die Syntax `async` und `await` von Rust verwendet und asynchrone
  Funktionen mit einer Runtime ausführt
- Wie man mit dem Async-Modell einige der Herausforderungen löst, die wir uns in
  Kapitel 16 angesehen haben
- Wie Multithreading und Async einander ergänzende Lösungen bieten, die du in
  vielen Fällen kombinieren kannst

Bevor wir sehen, wie Async in der Praxis funktioniert, müssen wir aber einen
kurzen Umweg machen und die Unterschiede zwischen Parallelität und
Nebenläufigkeit besprechen.

## Parallelität und Nebenläufigkeit {#parallelism-and-concurrency}

Bisher haben wir Parallelität und Nebenläufigkeit weitgehend als austauschbar
behandelt. Jetzt müssen wir sie genauer unterscheiden, weil die Unterschiede zum
Tragen kommen, sobald wir mit der Arbeit beginnen.

Denk an die verschiedenen Arten, wie ein Team die Arbeit an einem
Softwareprojekt aufteilen könnte. Du könntest einem einzelnen Mitglied mehrere
Aufgaben zuweisen, jedem Mitglied eine Aufgabe zuweisen oder eine Mischung aus
beiden Ansätzen verwenden.

Wenn eine einzelne Person an mehreren verschiedenen Aufgaben arbeitet, bevor
eine davon abgeschlossen ist, ist das _Nebenläufigkeit_ (_concurrency_). Eine
Art, Nebenläufigkeit umzusetzen, ähnelt dem Fall, dass du zwei verschiedene
Projekte auf deinem Computer ausgecheckt hast und zum anderen Projekt wechselst,
wenn dir bei einem langweilig wird oder du nicht weiterkommst. Du bist nur eine
Person und kannst daher nicht genau gleichzeitig an beiden Aufgaben vorankommen,
aber du kannst Multitasking betreiben und abwechselnd an einer der Aufgaben
vorankommen, indem du zwischen ihnen wechselst (siehe Abbildung 17-1).

<figure>

<img src="img/trpl17-01.svg" class="center" alt="Ein Diagramm mit übereinander angeordneten Kästen, beschriftet mit Task A und Task B, in denen Rauten für Teilaufgaben stehen. Pfeile zeigen von A1 auf B1, von B1 auf A2, von A2 auf B2, von B2 auf A3, von A3 auf A4 und von A4 auf B3. Die Pfeile zwischen den Teilaufgaben kreuzen die Kästen zwischen Task A und Task B." />

<figcaption>Abbildung 17-1: Ein nebenläufiger Arbeitsablauf, bei dem zwischen Task A und Task B gewechselt wird</figcaption>

</figure>

Wenn das Team eine Gruppe von Aufgaben aufteilt, indem jedes Mitglied eine
Aufgabe übernimmt und allein daran arbeitet, ist das _Parallelität_
(_parallelism_). Jede Person im Team kann genau gleichzeitig vorankommen (siehe
Abbildung 17-2).

<figure>

<img src="img/trpl17-02.svg" class="center" alt="Ein Diagramm mit übereinander angeordneten Kästen, beschriftet mit Task A und Task B, in denen Rauten für Teilaufgaben stehen. Pfeile zeigen von A1 auf A2, von A2 auf A3, von A3 auf A4, von B1 auf B2 und von B2 auf B3. Keine Pfeile kreuzen zwischen den Kästen für Task A und Task B." />

<figcaption>Abbildung 17-2: Ein paralleler Arbeitsablauf, bei dem an Task A und Task B unabhängig voneinander gearbeitet wird</figcaption>

</figure>

Bei beiden Arbeitsabläufen musst du vielleicht zwischen verschiedenen Aufgaben
koordinieren. Vielleicht dachtest du, die einer Person zugewiesene Aufgabe sei
völlig unabhängig von der Arbeit aller anderen, aber tatsächlich muss eine
andere Person im Team zuerst ihre Aufgabe abschließen. Ein Teil der Arbeit
konnte parallel erledigt werden, ein Teil war aber tatsächlich _seriell_: Er
konnte nur in einer Reihe erledigt werden, eine Aufgabe nach der anderen, wie in
Abbildung 17-3.

<figure>

<img src="img/trpl17-03.svg" class="center" alt="Ein Diagramm mit übereinander angeordneten Kästen, beschriftet mit Task A und Task B, in denen Rauten für Teilaufgaben stehen. In Task A zeigen Pfeile von A1 auf A2, von A2 auf zwei dicke senkrechte Striche wie ein Pause-Symbol und von diesem Symbol auf A3. In Task B zeigen Pfeile von B1 auf B2, von B2 auf B3, von B3 auf A3 und von B3 auf B4." />

<figcaption>Abbildung 17-3: Ein teilweise paralleler Arbeitsablauf, bei dem an Task A und Task B unabhängig voneinander gearbeitet wird, bis Task A3 auf die Ergebnisse von Task B3 warten muss.</figcaption>

</figure>

Ebenso stellst du vielleicht fest, dass eine deiner eigenen Aufgaben von einer
anderen deiner Aufgaben abhängt. Jetzt ist auch deine nebenläufige Arbeit
seriell geworden.

Parallelität und Nebenläufigkeit können sich auch überschneiden. Erfährst du,
dass eine Kollegin nicht weiterkommt, bis du eine deiner Aufgaben abgeschlossen
hast, konzentrierst du wahrscheinlich all deine Anstrengungen auf diese Aufgabe,
um deine Kollegin „freizumachen“. Ihr könnt dann nicht mehr parallel arbeiten,
und du kannst auch nicht mehr nebenläufig an deinen eigenen Aufgaben arbeiten.

Dieselbe grundlegende Dynamik spielt bei Software und Hardware eine Rolle. Auf
einer Maschine mit einem einzigen CPU-Kern kann die CPU nur eine Operation
gleichzeitig ausführen, aber trotzdem nebenläufig arbeiten. Mit Werkzeugen wie
Threads, Prozessen und Async kann der Computer eine Tätigkeit pausieren und zu
anderen wechseln, bevor er irgendwann wieder zur ersten Tätigkeit zurückkehrt.
Auf einer Maschine mit mehreren CPU-Kernen kann er Arbeit auch parallel
erledigen. Ein Kern kann eine Aufgabe ausführen, während ein anderer Kern eine
völlig unabhängige ausführt, und diese Operationen geschehen tatsächlich
gleichzeitig.

Async-Code läuft in Rust normalerweise nebenläufig. Je nach Hardware,
Betriebssystem und verwendeter Async-Runtime (mehr zu Async-Runtimes in Kürze)
kann diese Nebenläufigkeit unter der Haube auch Parallelität nutzen.

Sehen wir uns jetzt an, wie asynchrone Programmierung in Rust tatsächlich
funktioniert.
