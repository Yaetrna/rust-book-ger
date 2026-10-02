## Kommandozeilenargumente entgegennehmen {#accepting-command-line-arguments}

Legen wir wie immer mit `cargo new` ein neues Projekt an. Wir nennen unser
Projekt `minigrep`, um es von dem Werkzeug `grep` zu unterscheiden, das du
vielleicht schon auf deinem System hast:

```console
$ cargo new minigrep
     Created binary (application) `minigrep` project
$ cd minigrep
```

Die erste Aufgabe ist, `minigrep` seine zwei Kommandozeilenargumente
entgegennehmen zu lassen: den Dateipfad und einen String, nach dem gesucht
werden soll. Wir wollen unser Programm also mit `cargo run` ausführen können,
gefolgt von zwei Bindestrichen, die anzeigen, dass die folgenden Argumente für
unser Programm und nicht für `cargo` bestimmt sind, einem String, nach dem
gesucht werden soll, und einem Pfad zu einer Datei, die durchsucht werden soll,
etwa so:

```console
$ cargo run -- searchstring example-filename.txt
```

Im Moment kann das von `cargo new` erzeugte Programm keine Argumente
verarbeiten, die wir ihm übergeben. Einige vorhandene Bibliotheken auf
[crates.io](https://crates.io/) können beim Schreiben eines Programms helfen,
das Kommandozeilenargumente entgegennimmt, aber da du dieses Konzept gerade erst
lernst, implementieren wir diese Fähigkeit selbst.

### Die Werte der Argumente lesen {#reading-the-argument-values}

Damit `minigrep` die Werte der Kommandozeilenargumente lesen kann, die wir ihm
übergeben, brauchen wir die Funktion `std::env::args` aus der Standardbibliothek
von Rust. Diese Funktion gibt einen Iterator über die Kommandozeilenargumente
zurück, die an `minigrep` übergeben wurden. Iteratoren behandeln wir ausführlich
in [Kapitel 13][ch13]<!-- ignore
-->. Vorerst musst du nur zwei Details über Iteratoren wissen: Iteratoren
erzeugen eine Folge von Werten, und wir können auf einem Iterator die Methode
`collect` aufrufen, um ihn in eine Collection umzuwandeln, etwa einen Vektor,
der alle Elemente enthält, die der Iterator erzeugt.

Mit dem Code in Listing 12-1 kann dein Programm `minigrep` alle
Kommandozeilenargumente lesen, die ihm übergeben werden, und die Werte dann in
einem Vektor sammeln.

<Listing number="12-1" file-name="src/main.rs" caption="Die Kommandozeilenargumente in einem Vektor sammeln und ausgeben">

```rust
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-01/src/main.rs}}
```

</Listing>

Zuerst bringen wir das Modul `std::env` mit einer `use`-Anweisung in den
Gültigkeitsbereich (_scope_), damit wir seine Funktion `args` verwenden können.
Beachte, dass die Funktion `std::env::args` in zwei Modulebenen verschachtelt
ist. Wie wir in [Kapitel 7][ch7-idiomatic-use]<!-- ignore --> besprochen haben,
bringen wir in Fällen, in denen die gewünschte Funktion in mehr als einem Modul
verschachtelt ist, das Elternmodul statt der Funktion in den Gültigkeitsbereich.
Dadurch können wir problemlos auch andere Funktionen aus `std::env` verwenden.
Es ist auch weniger mehrdeutig, als `use std::env::args` hinzuzufügen und die
Funktion dann nur mit `args` aufzurufen, denn `args` könnte leicht mit einer
Funktion verwechselt werden, die im aktuellen Modul definiert ist.

> ### Die Funktion `args` und ungültiges Unicode {#the-args-function-and-invalid-unicode}
>
> Beachte, dass `std::env::args` einen Panic auslöst, wenn ein Argument
> ungültiges Unicode enthält. Muss dein Programm Argumente mit ungültigem
> Unicode akzeptieren, verwende stattdessen `std::env::args_os`. Diese Funktion
> gibt einen Iterator zurück, der `OsString`-Werte statt `String`-Werten
> erzeugt. Wir haben uns hier der Einfachheit halber für `std::env::args`
> entschieden, weil sich `OsString`-Werte je nach Plattform unterscheiden und
> komplizierter zu handhaben sind als `String`-Werte.

In der ersten Zeile von `main` rufen wir `env::args` auf und verwenden sofort
`collect`, um den Iterator in einen Vektor umzuwandeln, der alle vom Iterator
erzeugten Werte enthält. Mit der Funktion `collect` können wir viele Arten von
Collections erzeugen, daher annotieren wir den Typ von `args` explizit, um
anzugeben, dass wir einen Vektor von Strings wollen. Auch wenn du in Rust nur
sehr selten Typen annotieren musst, ist `collect` eine Funktion, bei der du das
oft tun musst, weil Rust nicht ableiten kann, welche Art von Collection du
willst.

Schließlich geben wir den Vektor mit dem Debug-Makro aus. Führen wir den Code
zuerst ohne Argumente und dann mit zwei Argumenten aus:

```console
{{#include ../listings/ch12-an-io-project/listing-12-01/output.txt}}
```

```console
{{#include ../listings/ch12-an-io-project/output-only-01-with-args/output.txt}}
```

Beachte, dass der erste Wert im Vektor `"target/debug/minigrep"` ist, der Name
unserer Binärdatei. Das entspricht dem Verhalten der Argumentliste in C und
erlaubt Programmen, bei ihrer Ausführung den Namen zu verwenden, mit dem sie
aufgerufen wurden. Es ist oft praktisch, Zugriff auf den Programmnamen zu haben,
falls du ihn in Meldungen ausgeben oder das Verhalten des Programms davon
abhängig machen willst, mit welchem Kommandozeilen-Alias das Programm aufgerufen
wurde. Für die Zwecke dieses Kapitels ignorieren wir ihn aber und speichern nur
die beiden Argumente, die wir brauchen.

### Die Werte der Argumente in Variablen speichern {#saving-the-argument-values-in-variables}

Das Programm kann jetzt auf die Werte zugreifen, die als Kommandozeilenargumente
angegeben wurden. Nun müssen wir die Werte der beiden Argumente in Variablen
speichern, damit wir sie im restlichen Programm verwenden können. Das tun wir in
Listing 12-2.

<Listing number="12-2" file-name="src/main.rs" caption="Variablen anlegen, die das Suchargument und das Dateipfad-Argument aufnehmen">

```rust,should_panic,noplayground
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-02/src/main.rs}}
```

</Listing>

Wie wir beim Ausgeben des Vektors gesehen haben, belegt der Name des Programms
den ersten Wert im Vektor bei `args[0]`, daher beginnen wir mit den Argumenten
bei Index 1. Das erste Argument, das `minigrep` nimmt, ist der String, nach dem
wir suchen, also legen wir eine Referenz auf das erste Argument in der Variable
`query` ab. Das zweite Argument ist der Dateipfad, also legen wir eine Referenz
auf das zweite Argument in der Variable `file_path` ab.

Wir geben die Werte dieser Variablen vorübergehend aus, um zu belegen, dass der
Code wie beabsichtigt funktioniert. Führen wir dieses Programm erneut mit den
Argumenten `test` und `sample.txt` aus:

```console
{{#include ../listings/ch12-an-io-project/listing-12-02/output.txt}}
```

Großartig, das Programm funktioniert! Die Werte der Argumente, die wir brauchen,
werden in den richtigen Variablen gespeichert. Später fügen wir etwas
Fehlerbehandlung hinzu, um mit bestimmten möglichen Fehlersituationen umzugehen,
etwa wenn der Benutzer keine Argumente angibt; vorerst ignorieren wir diese
Situation und kümmern uns stattdessen darum, Dateien lesen zu können.

[ch13]: ch13-00-functional-features.html
[ch7-idiomatic-use]: ch07-04-bringing-paths-into-scope-with-the-use-keyword.html#creating-idiomatic-use-paths
