## Merkmale objektorientierter Sprachen {#characteristics-of-object-oriented-languages}

In der Programmier-Community gibt es keinen Konsens darüber, welche Features
eine Sprache haben muss, um als objektorientiert zu gelten. Rust ist von vielen
Programmierparadigmen beeinflusst, auch von OOP; zum Beispiel haben wir in
Kapitel 13 die Features untersucht, die aus der funktionalen Programmierung
stammen. Man kann argumentieren, dass OOP-Sprachen bestimmte gemeinsame Merkmale
haben, nämlich Objekte, Kapselung und Vererbung. Sehen wir uns an, was jedes
dieser Merkmale bedeutet und ob Rust es unterstützt.

### Objekte enthalten Daten und Verhalten {#objects-contain-data-and-behavior}

Das Buch _Design Patterns: Elements of Reusable Object-Oriented Software_ von
Erich Gamma, Richard Helm, Ralph Johnson und John Vlissides (Addison-Wesley,
1994), umgangssprachlich als das Buch der _Gang of Four_ bezeichnet, ist ein
Katalog objektorientierter Design-Patterns. Es definiert OOP so:

> Objektorientierte Programme bestehen aus Objekten. Ein **Objekt** bündelt
> sowohl Daten als auch die Prozeduren, die auf diesen Daten arbeiten. Die
> Prozeduren werden typischerweise **Methoden** oder **Operationen** genannt.

Nach dieser Definition ist Rust objektorientiert: Structs und Enums haben Daten,
und `impl`-Blöcke stellen Methoden für Structs und Enums bereit. Auch wenn
Structs und Enums mit Methoden nicht Objekte _heißen_, bieten sie laut der
Objektdefinition der Gang of Four dieselbe Funktionalität.

### Kapselung, die Implementierungsdetails verbirgt {#encapsulation-that-hides-implementation-details}

Ein weiterer Aspekt, der häufig mit OOP in Verbindung gebracht wird, ist die
Idee der _Kapselung_, was bedeutet, dass die Implementierungsdetails eines
Objekts für Code, der dieses Objekt verwendet, nicht zugänglich sind. Daher kann
man mit einem Objekt nur über seine öffentliche API interagieren; Code, der das
Objekt verwendet, sollte nicht in das Innere des Objekts greifen und Daten oder
Verhalten direkt ändern können. So kann der Programmierer das Innere eines
Objekts ändern und refaktorisieren, ohne den Code ändern zu müssen, der das
Objekt verwendet.

Wie man Kapselung steuert, haben wir in Kapitel 7 besprochen: Mit dem
Schlüsselwort `pub` können wir entscheiden, welche Module, Typen, Funktionen und
Methoden in unserem Code öffentlich sein sollen, und standardmäßig ist alles
andere privat. Wir können zum Beispiel ein Struct `AveragedCollection`
definieren, das ein Feld mit einem Vektor von `i32`-Werten hat. Das Struct kann
außerdem ein Feld haben, das den Durchschnitt der Werte im Vektor enthält,
sodass der Durchschnitt nicht jedes Mal bei Bedarf berechnet werden muss, wenn
ihn jemand braucht. Mit anderen Worten: `AveragedCollection` speichert den
berechneten Durchschnitt für uns zwischen. Listing 18-1 enthält die Definition
des Structs `AveragedCollection`.

<Listing number="18-1" file-name="src/lib.rs" caption="Ein Struct `AveragedCollection`, das eine Liste von Ganzzahlen und den Durchschnitt der Elemente in der Collection verwaltet">

```rust,noplayground
{{#rustdoc_include ../listings/ch18-oop/listing-18-01/src/lib.rs}}
```

</Listing>

Das Struct ist mit `pub` gekennzeichnet, damit anderer Code es verwenden kann,
aber die Felder innerhalb des Structs bleiben privat. Das ist in diesem Fall
wichtig, weil wir sicherstellen wollen, dass der Durchschnitt jedes Mal
aktualisiert wird, wenn ein Wert zur Liste hinzugefügt oder daraus entfernt
wird. Das erreichen wir, indem wir die Methoden `add`, `remove` und `average`
für das Struct implementieren, wie in Listing 18-2 gezeigt.

<Listing number="18-2" file-name="src/lib.rs" caption="Implementierungen der öffentlichen Methoden `add`, `remove` und `average` für `AveragedCollection`">

```rust,noplayground
{{#rustdoc_include ../listings/ch18-oop/listing-18-02/src/lib.rs:here}}
```

</Listing>

Die öffentlichen Methoden `add`, `remove` und `average` sind die einzigen
Möglichkeiten, auf Daten in einer Instanz von `AveragedCollection` zuzugreifen
oder sie zu verändern. Wenn mit der Methode `add` ein Element zu `list`
hinzugefügt oder mit der Methode `remove` entfernt wird, rufen die
Implementierungen beider Methoden die private Methode `update_average` auf, die
sich darum kümmert, auch das Feld `average` zu aktualisieren.

Wir lassen die Felder `list` und `average` privat, damit externer Code keine
Möglichkeit hat, Elemente direkt zum Feld `list` hinzuzufügen oder daraus zu
entfernen; andernfalls könnte das Feld `average` aus dem Takt geraten, wenn sich
`list` ändert. Die Methode `average` gibt den Wert im Feld `average` zurück,
sodass externer Code den `average` lesen, aber nicht verändern kann.

Weil wir die Implementierungsdetails des Structs `AveragedCollection` gekapselt
haben, können wir Aspekte wie die Datenstruktur in Zukunft leicht ändern. Wir
könnten zum Beispiel für das Feld `list` ein `HashSet<i32>` statt eines
`Vec<i32>` verwenden. Solange die Signaturen der öffentlichen Methoden `add`,
`remove` und `average` gleich bleiben, müsste Code, der `AveragedCollection`
verwendet, nicht geändert werden. Würden wir `list` stattdessen öffentlich
machen, wäre das nicht unbedingt der Fall: `HashSet<i32>` und `Vec<i32>` haben
unterschiedliche Methoden zum Hinzufügen und Entfernen von Elementen, sodass der
externe Code wahrscheinlich geändert werden müsste, wenn er `list` direkt
verändert.

Wenn Kapselung ein notwendiger Aspekt ist, damit eine Sprache als
objektorientiert gilt, dann erfüllt Rust diese Anforderung. Die Möglichkeit,
`pub` für verschiedene Teile des Codes zu verwenden oder nicht, ermöglicht die
Kapselung von Implementierungsdetails.

### Vererbung als Typsystem und zur gemeinsamen Nutzung von Code {#inheritance-as-a-type-system-and-as-code-sharing}

_Vererbung_ ist ein Mechanismus, durch den ein Objekt Elemente aus der
Definition eines anderen Objekts erben kann und so die Daten und das Verhalten
des Elternobjekts erhält, ohne dass du sie erneut definieren musst.

Wenn eine Sprache Vererbung haben muss, um objektorientiert zu sein, dann ist
Rust keine solche Sprache. Es gibt keine Möglichkeit, ohne ein Makro ein Struct
zu definieren, das die Felder und Methodenimplementierungen des Eltern-Structs
erbt.

Wenn du es aber gewohnt bist, Vererbung in deinem Programmier-Werkzeugkasten zu
haben, kannst du in Rust andere Lösungen verwenden, je nachdem, warum du
überhaupt zur Vererbung greifst.

Für Vererbung entscheidet man sich hauptsächlich aus zwei Gründen. Der eine ist
die Wiederverwendung von Code: Du kannst ein bestimmtes Verhalten für einen Typ
implementieren, und Vererbung ermöglicht es dir, diese Implementierung für einen
anderen Typ wiederzuverwenden. In begrenztem Umfang kannst du das in Rust-Code
mit Standardimplementierungen von Trait-Methoden tun, die du in Listing 10-14
gesehen hast, als wir eine Standardimplementierung der Methode `summarize` zum
Trait `Summary` hinzugefügt haben. Für jeden Typ, der den Trait `Summary`
implementiert, ist die Methode `summarize` ohne weiteren Code verfügbar. Das
ähnelt einer Elternklasse, die eine Implementierung einer Methode hat, und einer
erbenden Kindklasse, die die Implementierung der Methode ebenfalls hat. Wir
können die Standardimplementierung der Methode `summarize` auch überschreiben,
wenn wir den Trait `Summary` implementieren, was dem Überschreiben der
Implementierung einer von einer Elternklasse geerbten Methode in einer
Kindklasse ähnelt.

Der andere Grund für Vererbung betrifft das Typsystem: Ein Kindtyp soll an
denselben Stellen verwendet werden können wie der Elterntyp. Das wird auch
_Polymorphie_ genannt, was bedeutet, dass du zur Laufzeit mehrere Objekte
gegeneinander austauschen kannst, wenn sie bestimmte Merkmale teilen.

> ### Polymorphie {#polymorphism}
>
> Für viele Menschen ist Polymorphie gleichbedeutend mit Vererbung. Tatsächlich
> ist sie aber ein allgemeineres Konzept, das sich auf Code bezieht, der mit
> Daten mehrerer Typen arbeiten kann. Bei Vererbung sind diese Typen im
> Allgemeinen Unterklassen.
>
> Rust verwendet stattdessen generische Typen, um über verschiedene mögliche
> Typen zu abstrahieren, und Trait-Bounds, um Einschränkungen dafür festzulegen,
> was diese Typen bereitstellen müssen. Das wird manchmal _beschränkte
> parametrische Polymorphie_ (_bounded parametric polymorphism_) genannt.

Rust hat sich für andere Vor- und Nachteile entschieden, indem es keine
Vererbung anbietet. Bei Vererbung besteht oft die Gefahr, dass mehr Code als
nötig gemeinsam genutzt wird. Unterklassen sollten nicht immer alle Merkmale
ihrer Elternklasse teilen, tun es mit Vererbung aber. Das kann das Design eines
Programms weniger flexibel machen. Außerdem entsteht die Möglichkeit, Methoden
auf Unterklassen aufzurufen, die keinen Sinn ergeben oder Fehler verursachen,
weil die Methoden auf die Unterklasse nicht zutreffen. Hinzu kommt, dass manche
Sprachen nur _Einfachvererbung_ erlauben (eine Unterklasse kann also nur von
einer Klasse erben), was die Flexibilität des Programmdesigns weiter
einschränkt.

Aus diesen Gründen verfolgt Rust einen anderen Ansatz und verwendet statt
Vererbung Trait-Objekte, um Polymorphie zur Laufzeit zu erreichen. Sehen wir uns
an, wie Trait-Objekte funktionieren.

{{#quiz ../quizzes/ch17-01-what-is-oo.toml}}
