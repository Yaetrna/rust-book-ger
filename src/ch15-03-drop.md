## Mit dem Trait `Drop` beim Aufräumen Code ausführen {#running-code-on-cleanup-with-the-drop-trait}

Der zweite für das Smart-Pointer-Pattern wichtige Trait ist `Drop`. Mit ihm
kannst du anpassen, was passiert, wenn ein Wert gleich den Gültigkeitsbereich
(_scope_) verlässt. Du kannst für jeden Typ eine Implementierung des Traits
`Drop` bereitstellen, und dieser Code kann verwendet werden, um Ressourcen wie
Dateien oder Netzwerkverbindungen freizugeben.

Wir stellen `Drop` im Zusammenhang mit Smart-Pointern vor, weil die
Funktionalität des Traits `Drop` fast immer bei der Implementierung eines
Smart-Pointers verwendet wird. Wird zum Beispiel eine `Box<T>` verworfen
(_dropped_), gibt sie den Platz auf dem Heap frei, auf den die Box zeigt.

In manchen Sprachen müssen Programmierende bei manchen Typen jedes Mal Code
aufrufen, um Speicher oder Ressourcen freizugeben, wenn sie eine Instanz dieser
Typen nicht mehr brauchen. Beispiele sind Datei-Handles, Sockets und Locks.
Vergessen sie das, kann das System überlastet werden und abstürzen. In Rust
kannst du festlegen, dass ein bestimmtes Stück Code ausgeführt wird, wann immer
ein Wert den Gültigkeitsbereich verlässt, und der Compiler fügt diesen Code
automatisch ein. Dadurch musst du nicht darauf achten, überall im Programm, wo
eine Instanz eines bestimmten Typs nicht mehr gebraucht wird, Aufräumcode zu
platzieren – und trotzdem verlierst du keine Ressourcen!

Den Code, der ausgeführt werden soll, wenn ein Wert den Gültigkeitsbereich
verlässt, gibst du an, indem du den Trait `Drop` implementierst. Der Trait
`Drop` verlangt, dass du eine Methode namens `drop` implementierst, die eine
veränderliche (_mutable_) Referenz auf `self` nimmt. Um zu sehen, wann Rust
`drop` aufruft, implementieren wir `drop` vorerst mit `println!`-Anweisungen.

Listing 15-14 zeigt ein Struct `CustomSmartPointer`, dessen einzige eigene
Funktionalität ist, dass es `Dropping CustomSmartPointer!` ausgibt, wenn die
Instanz den Gültigkeitsbereich verlässt, um zu zeigen, wann Rust die Methode
`drop` ausführt.

<Listing number="15-14" file-name="src/main.rs" caption="Ein Struct `CustomSmartPointer`, das den Trait `Drop` implementiert, in dem wir unseren Aufräumcode unterbringen würden">

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-14/src/main.rs}}
```

</Listing>

Der Trait `Drop` ist im Prelude enthalten, daher müssen wir ihn nicht in den
Gültigkeitsbereich bringen. Wir implementieren den Trait `Drop` für
`CustomSmartPointer` und stellen eine Implementierung der Methode `drop` bereit,
die `println!` aufruft. In den Rumpf der Methode `drop` würdest du die Logik
schreiben, die ausgeführt werden soll, wenn eine Instanz deines Typs den
Gültigkeitsbereich verlässt. Wir geben hier etwas Text aus, um sichtbar zu
machen, wann Rust `drop` aufruft.

In `main` erzeugen wir zwei Instanzen von `CustomSmartPointer` und geben dann
`CustomSmartPointers created` aus. Am Ende von `main` verlassen unsere Instanzen
von `CustomSmartPointer` den Gültigkeitsbereich, und Rust ruft den Code auf, den
wir in die Methode `drop` geschrieben haben, wodurch unsere abschließende
Meldung ausgegeben wird. Beachte, dass wir die Methode `drop` nicht explizit
aufrufen mussten.

Wenn wir dieses Programm ausführen, sehen wir folgende Ausgabe:

```console
{{#include ../listings/ch15-smart-pointers/listing-15-14/output.txt}}
```

Rust hat `drop` automatisch für uns aufgerufen, als unsere Instanzen den
Gültigkeitsbereich verlassen haben, und dabei den von uns angegebenen Code
ausgeführt. Variablen werden in umgekehrter Reihenfolge ihrer Erzeugung
verworfen, daher wurde `d` vor `c` verworfen. Dieses Beispiel soll dir
anschaulich zeigen, wie die Methode `drop` funktioniert; normalerweise würdest
du statt einer Ausgabemeldung den Aufräumcode angeben, den dein Typ ausführen
muss.

<!-- Old headings. Do not remove or links may break. -->

<a id="dropping-a-value-early-with-std-mem-drop"></a>

Leider ist es nicht ganz einfach, die automatische `drop`-Funktionalität
abzuschalten. Normalerweise ist es nicht nötig, `drop` abzuschalten; der ganze
Sinn des Traits `Drop` ist ja, dass er automatisch erledigt wird. Gelegentlich
möchtest du einen Wert aber vielleicht früher aufräumen. Ein Beispiel sind
Smart-Pointer, die Locks verwalten: Du möchtest vielleicht die Methode `drop`
erzwingen, die den Lock freigibt, damit anderer Code im selben
Gültigkeitsbereich den Lock erhalten kann. Rust erlaubt dir nicht, die Methode
`drop` des Traits `Drop` manuell aufzurufen; stattdessen musst du die Funktion
`std::mem::drop` aus der Standardbibliothek aufrufen, wenn du erzwingen willst,
dass ein Wert vor dem Ende seines Gültigkeitsbereichs verworfen wird.

Der Versuch, die Methode `drop` des Traits `Drop` manuell aufzurufen, indem wir
die Funktion `main` aus Listing 15-14 ändern, funktioniert nicht, wie Listing
15-15 zeigt.

<Listing number="15-15" file-name="src/main.rs" caption="Versuch, die Methode `drop` aus dem Trait `Drop` manuell aufzurufen, um früher aufzuräumen">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-15/src/main.rs:here}}
```

</Listing>

Wenn wir versuchen, diesen Code zu kompilieren, erhalten wir diesen Fehler:

```console
{{#include ../listings/ch15-smart-pointers/listing-15-15/output.txt}}
```

Diese Fehlermeldung besagt, dass wir `drop` nicht explizit aufrufen dürfen. Die
Fehlermeldung verwendet den Begriff _Destruktor_ (_destructor_), den allgemeinen
Programmierbegriff für eine Funktion, die eine Instanz aufräumt. Ein
_Destruktor_ ist das Gegenstück zu einem _Konstruktor_, der eine Instanz
erzeugt. Die Funktion `drop` in Rust ist ein bestimmter Destruktor.

Rust lässt uns `drop` nicht explizit aufrufen, weil Rust am Ende von `main`
trotzdem automatisch `drop` auf dem Wert aufrufen würde. Das würde einen
Double-Free-Fehler verursachen, weil Rust versuchen würde, denselben Wert
zweimal aufzuräumen.

Wir können das automatische Einfügen von `drop`, wenn ein Wert den
Gültigkeitsbereich verlässt, nicht abschalten, und wir können die Methode `drop`
nicht explizit aufrufen. Müssen wir also erzwingen, dass ein Wert früher
aufgeräumt wird, verwenden wir die Funktion `std::mem::drop`.

Die Funktion `std::mem::drop` unterscheidet sich von der Methode `drop` im Trait
`Drop`. Wir rufen sie auf, indem wir den Wert, dessen Verwerfen wir erzwingen
wollen, als Argument übergeben. Die Funktion ist im Prelude enthalten, daher
können wir `main` in Listing 15-15 so ändern, dass es die Funktion `drop`
aufruft, wie in Listing 15-16 gezeigt.

<Listing number="15-16" file-name="src/main.rs" caption="`std::mem::drop` aufrufen, um einen Wert explizit zu verwerfen, bevor er den Gültigkeitsbereich verlässt">

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-16/src/main.rs:here}}
```

</Listing>

Dieser Code gibt Folgendes aus:

```console
{{#include ../listings/ch15-smart-pointers/listing-15-16/output.txt}}
```

Der Text ``Dropping CustomSmartPointer with data `some data`!`` wird zwischen
den Texten `CustomSmartPointer created` und
`CustomSmartPointer dropped before
the end of main` ausgegeben, was zeigt, dass
der Code der Methode `drop` an dieser Stelle aufgerufen wird, um `c` zu
verwerfen.

Du kannst Code, der in einer Implementierung des Traits `Drop` angegeben ist,
auf viele Arten verwenden, um das Aufräumen bequem und sicher zu machen: Du
könntest damit zum Beispiel deinen eigenen Speicherallokator erstellen! Mit dem
Trait `Drop` und dem Ownership-System von Rust musst du nicht ans Aufräumen
denken, weil Rust das automatisch erledigt.

Du musst dir auch keine Sorgen über Probleme machen, die entstehen, wenn
versehentlich Werte aufgeräumt werden, die noch verwendet werden: Das
Ownership-System, das sicherstellt, dass Referenzen immer gültig sind, stellt
auch sicher, dass `drop` nur einmal aufgerufen wird, wenn der Wert nicht mehr
verwendet wird.

Nachdem wir `Box<T>` und einige Merkmale von Smart-Pointern untersucht
haben, sehen wir uns einige andere Smart-Pointer an, die in der
Standardbibliothek definiert sind.

{{#quiz ../quizzes/ch15-03-drop.toml}}
