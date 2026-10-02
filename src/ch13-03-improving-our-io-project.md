## Unser I/O-Projekt verbessern {#improving-our-io-project}

Mit diesem neuen Wissen über Iteratoren können wir das I/O-Projekt aus Kapitel
12 verbessern, indem wir mit Iteratoren Stellen im Code klarer und knapper
machen. Sehen wir uns an, wie Iteratoren unsere Implementierung der Funktionen
`Config::build` und `search` verbessern können.

### Ein `clone` mithilfe eines Iterators entfernen {#removing-a-clone-using-an-iterator}

In Listing 12-6 haben wir Code hinzugefügt, der einen Slice von `String`-Werten
nahm und eine Instanz des Structs `Config` erzeugte, indem er in den Slice
indexierte und die Werte klonte, sodass das Struct `Config` diese Werte besitzen
konnte. In Listing 13-17 haben wir die Implementierung der Funktion
`Config::build` so wiedergegeben, wie sie in Listing 12-23 war.

<Listing number="13-17" file-name="src/main.rs" caption="Wiedergabe der Funktion `Config::build` aus Listing 12-23">

```rust,ignore
{{#rustdoc_include ../listings/ch13-functional-features/listing-12-23-reproduced/src/main.rs:ch13}}
```

</Listing>

Damals haben wir gesagt, dass wir uns über die ineffizienten `clone`-Aufrufe
keine Sorgen machen sollten, weil wir sie später entfernen würden. Jetzt ist es
so weit!

Wir brauchten hier `clone`, weil wir im Parameter `args` einen Slice mit
`String`-Elementen haben, die Funktion `build` aber `args` nicht besitzt. Um die
Ownership einer `Config`-Instanz zurückgeben zu können, mussten wir die Werte
für die Felder `query` und `file_path` von `Config` klonen, damit die
`Config`-Instanz ihre Werte besitzen kann.

Mit unserem neuen Wissen über Iteratoren können wir die Funktion `build` so
ändern, dass sie als Argument die Ownership eines Iterators übernimmt, statt
einen Slice auszuleihen (_borrow_). Wir verwenden die Funktionalität des
Iterators statt des Codes, der die Länge des Slices prüft und an bestimmte
Stellen indexiert. Das macht deutlicher, was die Funktion `Config::build` tut,
weil der Iterator auf die Werte zugreift.

Sobald `Config::build` die Ownership des Iterators übernimmt und keine
ausleihenden Indexierungsoperationen mehr verwendet, können wir die
`String`-Werte aus dem Iterator in `Config` verschieben (_move_), statt `clone`
aufzurufen und eine neue Allokation vorzunehmen.

#### Den zurückgegebenen Iterator direkt verwenden {#using-the-returned-iterator-directly}

Öffne die Datei _src/main.rs_ deines I/O-Projekts, die so aussehen sollte:

<span class="filename">Dateiname: src/main.rs</span>

```rust,ignore
{{#rustdoc_include ../listings/ch13-functional-features/listing-12-24-reproduced/src/main.rs:ch13}}
```

Zuerst ändern wir den Anfang der Funktion `main` aus Listing 12-24 in den Code
aus Listing 13-18, der diesmal einen Iterator verwendet. Das kompiliert erst,
wenn wir auch `Config::build` anpassen.

<Listing number="13-18" file-name="src/main.rs" caption="Den Rückgabewert von `env::args` an `Config::build` übergeben">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-18/src/main.rs:here}}
```

</Listing>

Die Funktion `env::args` gibt einen Iterator zurück! Statt die Werte des
Iterators in einem Vektor zu sammeln und dann einen Slice an `Config::build` zu
übergeben, übergeben wir die Ownership des von `env::args` zurückgegebenen
Iterators jetzt direkt an `Config::build`.

Als Nächstes müssen wir die Definition von `Config::build` anpassen. Ändern wir
die Signatur von `Config::build` so, dass sie aussieht wie in Listing 13-19. Das
kompiliert immer noch nicht, weil wir den Funktionsrumpf anpassen müssen.

<Listing number="13-19" file-name="src/main.rs" caption="Die Signatur von `Config::build` so anpassen, dass sie einen Iterator erwartet">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-19/src/main.rs:here}}
```

</Listing>

Die Dokumentation der Standardbibliothek zur Funktion `env::args` zeigt, dass
der Typ des zurückgegebenen Iterators `std::env::Args` ist und dass dieser Typ
den Trait `Iterator` implementiert und `String`-Werte zurückgibt.

Wir haben die Signatur der Funktion `Config::build` so angepasst, dass der
Parameter `args` einen generischen Typ mit den Trait-Bounds
`impl Iterator<Item =
String>` statt `&[String]` hat. Diese Verwendung der Syntax
`impl Trait`, die wir im Abschnitt
[„Traits als Parameter verwenden“][impl-trait]<!-- ignore --> in Kapitel 10
besprochen haben, bedeutet, dass `args` jeder Typ sein kann, der den Trait
`Iterator` implementiert und `String`-Elemente zurückgibt.

Da wir die Ownership von `args` übernehmen und `args` durch das Iterieren
verändern, können wir in der Angabe des Parameters `args` das Schlüsselwort
`mut` hinzufügen, um ihn veränderlich (_mutable_) zu machen.

<!-- Old headings. Do not remove or links may break. -->

<a id="using-iterator-trait-methods-instead-of-indexing"></a>

#### Methoden des Traits `Iterator` verwenden {#using-iterator-trait-methods}

Als Nächstes korrigieren wir den Rumpf von `Config::build`. Da `args` den Trait
`Iterator` implementiert, wissen wir, dass wir die Methode `next` darauf
aufrufen können! Listing 13-20 passt den Code aus Listing 12-23 so an, dass er
die Methode `next` verwendet.

<Listing number="13-20" file-name="src/main.rs" caption="Den Rumpf von `Config::build` so ändern, dass er Iterator-Methoden verwendet">

```rust,ignore,noplayground
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-20/src/main.rs:here}}
```

</Listing>

Denk daran, dass der erste Wert im Rückgabewert von `env::args` der Name des
Programms ist. Den wollen wir ignorieren und zum nächsten Wert übergehen, also
rufen wir zuerst `next` auf und tun nichts mit dem Rückgabewert. Dann rufen wir
`next` auf, um den Wert zu erhalten, den wir in das Feld `query` von `Config`
legen wollen. Gibt `next` `Some` zurück, holen wir den Wert mit einem `match`
heraus. Gibt es `None` zurück, wurden nicht genug Argumente angegeben, und wir
kehren vorzeitig mit einem `Err`-Wert zurück. Dasselbe machen wir für den Wert
`file_path`.

<!-- Old headings. Do not remove or links may break. -->

<a id="making-code-clearer-with-iterator-adapters"></a>

### Code mit Iterator-Adaptern verdeutlichen {#clarifying-code-with-iterator-adapters}

Wir können Iteratoren auch in der Funktion `search` unseres I/O-Projekts nutzen,
die hier in Listing 13-21 so wiedergegeben ist, wie sie in Listing 12-19 war.

<Listing number="13-21" file-name="src/lib.rs" caption="Die Implementierung der Funktion `search` aus Listing 12-19">

```rust,ignore
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-19/src/lib.rs:ch13}}
```

</Listing>

Mit Iterator-Adapter-Methoden können wir diesen Code knapper schreiben. Dadurch
vermeiden wir auch einen veränderlichen Zwischenvektor `results`. Der
funktionale Programmierstil bevorzugt es, die Menge an veränderlichem Zustand zu
minimieren, um Code klarer zu machen. Den veränderlichen Zustand zu entfernen,
könnte eine künftige Verbesserung ermöglichen, bei der die Suche parallel
abläuft, weil wir keinen nebenläufigen Zugriff auf den Vektor `results`
verwalten müssten. Listing 13-22 zeigt diese Änderung.

<Listing number="13-22" file-name="src/lib.rs" caption="Iterator-Adapter-Methoden in der Implementierung der Funktion `search` verwenden">

```rust,ignore
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-22/src/lib.rs:here}}
```

</Listing>

Erinnere dich, dass die Funktion `search` alle Zeilen in `contents` zurückgeben
soll, die `query` enthalten. Ähnlich wie das Beispiel mit `filter` in Listing
13-16 verwendet dieser Code den Adapter `filter`, um nur die Zeilen zu behalten,
für die `line.contains(query)` `true` zurückgibt. Dann sammeln wir die passenden
Zeilen mit `collect` in einem weiteren Vektor. Viel einfacher! Nimm ruhig
dieselbe Änderung auch in der Funktion `search_case_insensitive` vor, damit sie
Iterator-Methoden verwendet.

Als weitere Verbesserung kannst du aus der Funktion `search` einen Iterator
zurückgeben, indem du den Aufruf von `collect` entfernst und den Rückgabetyp in
`impl
Iterator<Item = &'a str>` änderst, sodass die Funktion zu einem
Iterator-Adapter wird. Beachte, dass du dann auch die Tests anpassen musst!
Durchsuche vor und nach dieser Änderung eine große Datei mit deinem Werkzeug
`minigrep`, um den Unterschied im Verhalten zu beobachten. Vor dieser Änderung
gibt das Programm keine Ergebnisse aus, bis es alle Ergebnisse gesammelt hat;
nach der Änderung werden die Ergebnisse ausgegeben, sobald eine passende Zeile
gefunden wird, weil die `for`-Schleife in der Funktion `run` davon profitieren
kann, dass der Iterator lazy ist.

<!-- Old headings. Do not remove or links may break. -->

<a id="choosing-between-loops-or-iterators"></a>

### Zwischen Schleifen und Iteratoren wählen {#choosing-between-loops-and-iterators}

Die nächste logische Frage ist, welchen Stil du in deinem eigenen Code wählen
solltest und warum: die ursprüngliche Implementierung in Listing 13-21 oder die
Version mit Iteratoren in Listing 13-22 (vorausgesetzt, wir sammeln alle
Ergebnisse, bevor wir sie zurückgeben, statt den Iterator zurückzugeben). Die
meisten Rust-Programmierenden bevorzugen den Iterator-Stil. Anfangs ist er etwas
schwerer zu durchschauen, aber sobald du ein Gefühl für die verschiedenen
Iterator-Adapter und ihre Funktion entwickelt hast, können Iteratoren leichter
zu verstehen sein. Statt mit den verschiedenen Bestandteilen von Schleifen und
dem Aufbau neuer Vektoren herumzuhantieren, konzentriert sich der Code auf das
übergeordnete Ziel der Schleife. Das abstrahiert einen Teil des alltäglichen
Codes weg, sodass sich die Konzepte leichter erkennen lassen, die für diesen
Code spezifisch sind, etwa die Filterbedingung, die jedes Element im Iterator
erfüllen muss.

Aber sind die beiden Implementierungen wirklich gleichwertig? Intuitiv könnte
man annehmen, dass die Schleife auf niedrigerer Ebene schneller ist. Sprechen
wir über Performance.

[impl-trait]: ch10-02-traits.html#traits-as-parameters
