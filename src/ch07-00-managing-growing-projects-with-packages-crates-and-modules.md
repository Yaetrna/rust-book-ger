<!-- Old headings. Do not remove or links may break. -->

<a id="managing-growing-projects-with-packages-crates-and-modules"></a>

# Pakete, Crates und Module {#packages-crates-and-modules}

Wenn du große Programme schreibst, wird es immer wichtiger, deinen Code zu
organisieren. Indem du zusammengehörige Funktionalität gruppierst und Code mit
unterschiedlichen Features trennst, machst du klar, wo der Code zu finden ist,
der ein bestimmtes Feature implementiert, und wo du hingehen musst, um zu
ändern, wie ein Feature funktioniert.

Die Programme, die wir bisher geschrieben haben, bestanden aus einem Modul in
einer Datei. Wenn ein Projekt wächst, solltest du den Code organisieren, indem
du ihn auf mehrere Module und dann auf mehrere Dateien aufteilst. Ein Paket kann
mehrere Binary-Crates und optional ein Library-Crate enthalten. Wenn ein Paket
wächst, kannst du Teile in separate Crates auslagern, die zu externen
Abhängigkeiten werden. Dieses Kapitel behandelt all diese Techniken. Für sehr
große Projekte, die aus einer Reihe zusammenhängender Pakete bestehen, die sich
gemeinsam weiterentwickeln, bietet Cargo Workspaces, die wir in
[„Cargo-Workspaces“][workspaces]<!-- ignore --> in Kapitel 14 behandeln.

Außerdem besprechen wir die Kapselung von Implementierungsdetails, mit der du
Code auf einer höheren Ebene wiederverwenden kannst: Sobald du eine Operation
implementiert hast, kann anderer Code deinen Code über seine öffentliche
Schnittstelle aufrufen, ohne wissen zu müssen, wie die Implementierung
funktioniert. Wie du Code schreibst, legt fest, welche Teile öffentlich sind und
von anderem Code verwendet werden können und welche Teile private
Implementierungsdetails sind, die du dir vorbehältst zu ändern. Auch das ist
eine Möglichkeit, die Menge an Details zu begrenzen, die du im Kopf behalten
musst.

Ein verwandtes Konzept ist der Gültigkeitsbereich (_scope_): Der verschachtelte
Kontext, in dem Code geschrieben ist, hat eine Menge von Namen, die als „im
Gültigkeitsbereich“ definiert sind. Beim Lesen, Schreiben und Kompilieren von
Code müssen Programmierende und Compiler wissen, ob sich ein bestimmter Name an
einer bestimmten Stelle auf eine Variable, eine Funktion, ein Struct, ein Enum,
ein Modul, eine Konstante oder ein anderes Element bezieht und was dieses
Element bedeutet. Du kannst Gültigkeitsbereiche erzeugen und ändern, welche
Namen im Gültigkeitsbereich liegen und welche nicht. Du kannst nicht zwei
Elemente mit demselben Namen im selben Gültigkeitsbereich haben; für
Namenskonflikte gibt es Werkzeuge, um sie aufzulösen.

Rust hat eine Reihe von Features, mit denen du die Organisation deines Codes
steuern kannst, darunter, welche Details nach außen sichtbar sind, welche
Details privat sind und welche Namen in den einzelnen Gültigkeitsbereichen
deiner Programme existieren. Zu diesen Features, die manchmal zusammenfassend
als _Modulsystem_ bezeichnet werden, gehören:

- **Pakete**: Ein Feature von Cargo, mit dem du Crates bauen, testen und teilen
  kannst
- **Crates**: Ein Baum von Modulen, der eine Bibliothek oder eine ausführbare
  Datei erzeugt
- **Module und use**: Damit steuerst du die Organisation, den Gültigkeitsbereich
  und die Sichtbarkeit von Pfaden
- **Pfade**: Eine Möglichkeit, ein Element zu benennen, etwa ein Struct, eine
  Funktion oder ein Modul

In diesem Kapitel behandeln wir all diese Features, besprechen, wie sie
zusammenspielen, und erklären, wie du mit ihnen Gültigkeitsbereiche verwaltest.
Am Ende solltest du das Modulsystem gut verstehen und wie ein Profi mit
Gültigkeitsbereichen arbeiten können!

[workspaces]: ch14-03-cargo-workspaces.html
