# Abschlussprojekt: Einen Multithread-Webserver bauen {#final-project-building-a-multithreaded-web-server}

Es war eine lange Reise, aber wir sind am Ende des Buches angekommen. In diesem
Kapitel bauen wir gemeinsam noch ein weiteres Projekt, um einige der Konzepte zu
demonstrieren, die wir in den letzten Kapiteln behandelt haben, und um einige
frühere Lektionen zu wiederholen.

Für unser Abschlussprojekt erstellen wir einen Webserver, der „Hello!“ sagt und
in einem Webbrowser wie Abbildung 21-1 aussieht.

Hier ist unser Plan für den Bau des Webservers:

1. Ein wenig über TCP und HTTP lernen.
2. Auf einem Socket auf TCP-Verbindungen lauschen.
3. Eine kleine Anzahl von HTTP-Anfragen parsen.
4. Eine ordentliche HTTP-Antwort erstellen.
5. Den Durchsatz unseres Servers mit einem Thread-Pool verbessern.

<img alt="Screenshot eines Webbrowsers, der die Adresse 127.0.0.1:8080 aufruft und eine Webseite mit dem Textinhalt „Hello! Hi from Rust“ anzeigt" src="img/trpl21-01.png" class="center" style="width: 50%;" />

<span class="caption">Abbildung 21-1: Unser gemeinsames Abschlussprojekt</span>

Bevor wir anfangen, sollten wir zwei Details erwähnen. Erstens ist die Methode,
die wir verwenden, nicht der beste Weg, einen Webserver mit Rust zu bauen.
Mitglieder der Community haben auf [crates.io](https://crates.io/) eine Reihe
produktionsreifer Crates veröffentlicht, die vollständigere Implementierungen
von Webservern und Thread-Pools bieten, als wir sie bauen werden. Unsere Absicht
in diesem Kapitel ist es aber, dir beim Lernen zu helfen, nicht den einfachen
Weg zu gehen. Weil Rust eine Systemprogrammiersprache ist, können wir die
Abstraktionsebene wählen, auf der wir arbeiten wollen, und können auf eine
niedrigere Ebene gehen, als es in anderen Sprachen möglich oder praktikabel ist.

Zweitens verwenden wir hier weder async noch await. Einen Thread-Pool zu bauen,
ist für sich genommen schon eine ausreichend große Herausforderung, auch ohne
zusätzlich eine Async-Runtime zu bauen! Wir weisen jedoch darauf hin, wie async
und await auf einige der Probleme anwendbar sein könnten, die uns in diesem
Kapitel begegnen. Letztlich verwenden viele Async-Runtimes, wie wir in Kapitel
17 angemerkt haben, Thread-Pools, um ihre Arbeit zu verwalten.

Wir schreiben den einfachen HTTP-Server und den Thread-Pool daher von Hand,
damit du die allgemeinen Ideen und Techniken hinter den Crates kennenlernst, die
du in Zukunft vielleicht verwenden wirst.
