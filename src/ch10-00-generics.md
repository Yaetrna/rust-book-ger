# Generische Typen, Traits und Lifetimes {#generic-types-traits-and-lifetimes}

Jede Programmiersprache hat Werkzeuge, um die Verdopplung von Konzepten wirksam
zu handhaben. In Rust ist eines dieser Werkzeuge _Generics_: abstrakte
Platzhalter für konkrete Typen oder andere Eigenschaften. Wir können das
Verhalten von Generics oder ihre Beziehung zu anderen Generics ausdrücken, ohne
zu wissen, was beim Kompilieren und Ausführen des Codes an ihrer Stelle stehen
wird.

Funktionen können Parameter eines generischen Typs statt eines konkreten Typs
wie `i32` oder `String` nehmen, genauso wie sie Parameter mit unbekannten Werten
nehmen, um denselben Code auf mehreren konkreten Werten auszuführen. Tatsächlich
haben wir Generics bereits verwendet: in Kapitel 6 mit `Option<T>`, in Kapitel 8
mit `Vec<T>` und `HashMap<K, V>` und in Kapitel 9 mit `Result<T, E>`. In diesem
Kapitel erkundest du, wie du mit Generics eigene Typen, Funktionen und Methoden
definierst!

Zuerst sehen wir uns noch einmal an, wie man eine Funktion extrahiert, um
Codeduplizierung zu verringern. Dann verwenden wir dieselbe Technik, um aus zwei
Funktionen, die sich nur in den Typen ihrer Parameter unterscheiden, eine
generische Funktion zu machen. Außerdem erklären wir, wie man generische Typen
in Struct- und Enum-Definitionen verwendet.

Dann lernst du, wie du mit Traits Verhalten auf generische Weise definierst. Du
kannst Traits mit generischen Typen kombinieren, um einen generischen Typ so
einzuschränken, dass er nur Typen mit einem bestimmten Verhalten akzeptiert und
nicht einfach jeden beliebigen Typ.

Zum Schluss besprechen wir _Lifetimes_: eine Art von Generics, die dem Compiler
Informationen darüber geben, wie Referenzen zueinander in Beziehung stehen. Mit
Lifetimes können wir dem Compiler genug Informationen über ausgeliehene
(_borrowed_) Werte geben, damit er in mehr Situationen sicherstellen kann, dass
Referenzen gültig sind, als es ohne unsere Hilfe möglich wäre.

## Duplizierung entfernen, indem man eine Funktion extrahiert {#removing-duplication-by-extracting-a-function}

Mit Generics können wir bestimmte Typen durch einen Platzhalter ersetzen, der
mehrere Typen darstellt, und so Codeduplizierung entfernen. Bevor wir in die
Syntax von Generics eintauchen, sehen wir uns zuerst an, wie man Duplizierung
ohne generische Typen entfernt, indem man eine Funktion extrahiert, die
bestimmte Werte durch einen Platzhalter ersetzt, der mehrere Werte darstellt.
Dann wenden wir dieselbe Technik an, um eine generische Funktion zu extrahieren!
Wenn du dir ansiehst, wie man duplizierten Code erkennt, den man in eine
Funktion extrahieren kann, wirst du auch duplizierten Code erkennen, bei dem man
Generics einsetzen kann.

Wir beginnen mit dem kurzen Programm in Listing 10-1, das die größte Zahl in
einer Liste findet.

<Listing number="10-1" file-name="src/main.rs" caption="Die größte Zahl in einer Liste von Zahlen finden">

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-01/src/main.rs:here}}
```

</Listing>

Wir speichern eine Liste von Ganzzahlen in der Variable `number_list` und legen
eine Referenz auf die erste Zahl der Liste in einer Variable namens `largest`
ab. Dann iterieren wir über alle Zahlen der Liste, und wenn die aktuelle Zahl
größer ist als die in `largest` gespeicherte, ersetzen wir die Referenz in
dieser Variable. Ist die aktuelle Zahl dagegen kleiner oder gleich der bisher
größten Zahl, ändert sich die Variable nicht, und der Code geht zur nächsten
Zahl der Liste über. Nachdem alle Zahlen der Liste betrachtet wurden, sollte
`largest` auf die größte Zahl verweisen, in diesem Fall 100.

Nun sollen wir die größte Zahl in zwei verschiedenen Listen von Zahlen finden.
Dafür könnten wir den Code aus Listing 10-1 duplizieren und dieselbe Logik an
zwei verschiedenen Stellen im Programm verwenden, wie in Listing 10-2 gezeigt.

<Listing number="10-2" file-name="src/main.rs" caption="Code, der die größte Zahl in *zwei* Listen von Zahlen findet">

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-02/src/main.rs}}
```

</Listing>

Dieser Code funktioniert zwar, aber Code zu duplizieren ist mühsam und
fehleranfällig. Außerdem müssen wir daran denken, den Code an mehreren Stellen
anzupassen, wenn wir ihn ändern wollen.

Um diese Duplizierung zu beseitigen, schaffen wir eine Abstraktion, indem wir
eine Funktion definieren, die mit jeder Liste von Ganzzahlen arbeitet, die als
Parameter übergeben wird. Diese Lösung macht unseren Code klarer und lässt uns
das Konzept, die größte Zahl in einer Liste zu finden, abstrakt ausdrücken.

In Listing 10-3 extrahieren wir den Code, der die größte Zahl findet, in eine
Funktion namens `largest`. Dann rufen wir die Funktion auf, um die größte Zahl
in den beiden Listen aus Listing 10-2 zu finden. Wir könnten die Funktion auch
auf jede andere Liste von `i32`-Werten anwenden, die wir künftig haben.

<Listing number="10-3" file-name="src/main.rs" caption="Abstrahierter Code, der die größte Zahl in zwei Listen findet">

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-03/src/main.rs:here}}
```

</Listing>

Die Funktion `largest` hat einen Parameter namens `list`, der für jeden
konkreten Slice von `i32`-Werten steht, den wir an die Funktion übergeben
könnten. Wenn wir die Funktion aufrufen, läuft der Code daher auf den konkreten
Werten, die wir übergeben.

Zusammengefasst sind das die Schritte, mit denen wir den Code von Listing 10-2
zu Listing 10-3 umgebaut haben:

1. Duplizierten Code erkennen.
1. Den duplizierten Code in den Rumpf der Funktion extrahieren und die Eingaben
   und Rückgabewerte dieses Codes in der Funktionssignatur angeben.
1. Die beiden Stellen mit dupliziertem Code so anpassen, dass sie stattdessen
   die Funktion aufrufen.

Als Nächstes wenden wir dieselben Schritte mit Generics an, um Codeduplizierung
zu verringern. So wie der Funktionsrumpf mit einer abstrakten `list` statt mit
konkreten Werten arbeiten kann, erlauben Generics dem Code, mit abstrakten Typen
zu arbeiten.

Angenommen, wir hätten zwei Funktionen: eine, die das größte Element in einem
Slice von `i32`-Werten findet, und eine, die das größte Element in einem Slice
von `char`-Werten findet. Wie würden wir diese Duplizierung beseitigen? Finden
wir es heraus!
