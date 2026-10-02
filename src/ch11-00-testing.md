# Automatisierte Tests schreiben {#writing-automated-tests}

In seinem Essay „The Humble Programmer“ von 1972 sagte Edsger W. Dijkstra, dass
„Programmtests ein sehr wirksames Mittel sein können, um das Vorhandensein von
Bugs zu zeigen, aber hoffnungslos unzureichend sind, um ihre Abwesenheit zu
zeigen“. Das heißt nicht, dass wir nicht versuchen sollten, so viel wie möglich
zu testen!

Die _Korrektheit_ (_correctness_) unserer Programme ist das Ausmaß, in dem unser
Code das tut, was wir beabsichtigen. Rust wurde mit großem Augenmerk auf die
Korrektheit von Programmen entworfen, aber Korrektheit ist komplex und nicht
leicht zu beweisen. Das Typsystem von Rust trägt einen großen Teil dieser Last,
kann aber nicht alles abfangen. Deshalb unterstützt Rust das Schreiben
automatisierter Softwaretests.

Angenommen, wir schreiben eine Funktion `add_two`, die zu der Zahl, die ihr
übergeben wird, 2 addiert. Die Signatur dieser Funktion akzeptiert eine Ganzzahl
als Parameter und gibt eine Ganzzahl als Ergebnis zurück. Wenn wir diese
Funktion implementieren und kompilieren, führt Rust die gesamte Typprüfung und
Borrow-Prüfung durch, die du bisher kennengelernt hast, um zum Beispiel
sicherzustellen, dass wir dieser Funktion keinen `String`-Wert und keine
ungültige Referenz übergeben. Rust _kann_ aber nicht prüfen, ob diese Funktion
genau das tut, was wir beabsichtigen, nämlich den Parameter plus 2 zurückzugeben
und nicht etwa den Parameter plus 10 oder den Parameter minus 50! Hier kommen
Tests ins Spiel.

Wir können Tests schreiben, die zum Beispiel zusichern, dass der Rückgabewert
`5` ist, wenn wir `3` an die Funktion `add_two` übergeben. Diese Tests können
wir immer dann ausführen, wenn wir unseren Code ändern, um sicherzustellen, dass
sich bestehendes korrektes Verhalten nicht geändert hat.

Testen ist eine komplexe Fähigkeit: Wir können zwar nicht in einem Kapitel jedes
Detail dazu behandeln, wie man gute Tests schreibt, besprechen in diesem Kapitel
aber die Mechanik der Testwerkzeuge von Rust. Wir sprechen über die Annotationen
und Makros, die dir beim Schreiben deiner Tests zur Verfügung stehen, über das
Standardverhalten und die Optionen beim Ausführen deiner Tests und darüber, wie
man Tests in Unit-Tests und Integrationstests organisiert.
