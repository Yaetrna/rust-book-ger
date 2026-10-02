## Eine Datei lesen {#reading-a-file}

Jetzt fügen wir Funktionalität hinzu, um die Datei zu lesen, die im Argument
`file_path` angegeben ist. Zuerst brauchen wir eine Beispieldatei zum Testen:
Wir verwenden eine Datei mit etwas Text über mehrere Zeilen und einigen
wiederholten Wörtern. Listing 12-3 enthält ein Gedicht von Emily Dickinson, das
sich gut eignet! Lege auf der obersten Ebene deines Projekts eine Datei namens
_poem.txt_ an und gib das Gedicht „I’m Nobody! Who are you?“ ein.

<Listing number="12-3" file-name="poem.txt" caption="Ein Gedicht von Emily Dickinson ist ein guter Testfall.">

```text
{{#include ../listings/ch12-an-io-project/listing-12-03/poem.txt}}
```

</Listing>

Wenn der Text vorhanden ist, bearbeite _src/main.rs_ und füge Code hinzu, der
die Datei liest, wie in Listing 12-4 gezeigt.

<Listing number="12-4" file-name="src/main.rs" caption="Den Inhalt der Datei lesen, die im zweiten Argument angegeben ist">

```rust,should_panic,noplayground
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-04/src/main.rs:here}}
```

</Listing>

Zuerst binden wir mit einer `use`-Anweisung einen relevanten Teil der
Standardbibliothek ein: Wir brauchen `std::fs`, um mit Dateien umzugehen.

In `main` nimmt die neue Anweisung `fs::read_to_string` den `file_path`, öffnet
diese Datei und gibt einen Wert vom Typ `std::io::Result<String>` zurück, der
den Inhalt der Datei enthält.

Danach fügen wir wieder eine vorübergehende `println!`-Anweisung hinzu, die den
Wert von `contents` ausgibt, nachdem die Datei gelesen wurde, damit wir prüfen
können, ob das Programm bis hierher funktioniert.

Führen wir diesen Code mit einem beliebigen String als erstem
Kommandozeilenargument aus (weil wir den Suchteil noch nicht implementiert
haben) und mit der Datei _poem.txt_ als zweitem Argument:

```console
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-04/output.txt}}
```

Großartig! Der Code hat den Inhalt der Datei gelesen und dann ausgegeben. Aber
der Code hat einige Schwächen. Im Moment hat die Funktion `main` mehrere
Verantwortlichkeiten: Im Allgemeinen sind Funktionen übersichtlicher und
leichter zu warten, wenn jede Funktion nur für eine Idee verantwortlich ist. Das
andere Problem ist, dass wir Fehler nicht so gut behandeln, wie wir könnten. Das
Programm ist noch klein, daher sind diese Schwächen kein großes Problem, aber
wenn das Programm wächst, wird es schwieriger, sie sauber zu beheben. Es ist
eine gute Praxis, bei der Entwicklung eines Programms früh mit dem Refactoring
zu beginnen, weil sich kleinere Mengen Code viel leichter refaktorisieren
lassen. Das machen wir als Nächstes.
