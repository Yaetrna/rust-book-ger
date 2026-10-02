## Module auf verschiedene Dateien aufteilen {#separating-modules-into-different-files}

Bisher haben alle Beispiele in diesem Kapitel mehrere Module in einer Datei
definiert. Wenn Module groß werden, möchtest du ihre Definitionen vielleicht in
eine separate Datei verschieben, damit man sich im Code leichter zurechtfindet.

Gehen wir zum Beispiel vom Code in Listing 7-17 aus, der mehrere
Restaurant-Module hatte. Wir lagern Module in Dateien aus, statt alle Module in
der Crate-Root-Datei (der Wurzeldatei des Crates) zu definieren. In diesem Fall
ist die Crate-Root-Datei _src/lib.rs_, aber dieses Vorgehen funktioniert auch
bei Binary-Crates, deren Crate-Root-Datei _src/main.rs_ ist.

Zuerst lagern wir das Modul `front_of_house` in eine eigene Datei aus. Entferne
den Code innerhalb der geschweiften Klammern des Moduls `front_of_house`, sodass
nur die Deklaration `mod front_of_house;` übrig bleibt und _src/lib.rs_ den Code
aus Listing 7-21 enthält. Beachte, dass das erst kompiliert, wenn wir in Listing
7-22 die Datei _src/front_of_house.rs_ erstellen.

<Listing number="7-21" file-name="src/lib.rs" caption="Das Modul `front_of_house` deklarieren, dessen Rumpf in *src/front_of_house.rs* stehen wird">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-21-and-22/src/lib.rs}}
```

</Listing>

Als Nächstes legst du den Code, der in den geschweiften Klammern stand, in eine
neue Datei namens _src/front_of_house.rs_, wie in Listing 7-22 gezeigt. Der
Compiler weiß, dass er in dieser Datei suchen muss, weil er in der Crate-Root
auf die Moduldeklaration mit dem Namen `front_of_house` gestoßen ist.

<Listing number="7-22" file-name="src/front_of_house.rs" caption="Definitionen innerhalb des Moduls `front_of_house` in *src/front_of_house.rs*">

```rust,ignore
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-21-and-22/src/front_of_house.rs}}
```

</Listing>

Beachte, dass du eine Datei mit einer `mod`-Deklaration nur _einmal_ in deinem
Modulbaum laden musst. Sobald der Compiler weiß, dass die Datei zum Projekt
gehört (und dank der Stelle, an der du die `mod`-Anweisung platziert hast, weiß,
wo im Modulbaum der Code liegt), sollten andere Dateien in deinem Projekt über
einen Pfad zu der Stelle, an der sie deklariert wurde, auf den Code der
geladenen Datei verweisen, wie im Abschnitt
[„Pfade, um auf ein Element im Modulbaum zu verweisen“][paths]<!-- ignore -->
beschrieben. Mit anderen Worten: `mod` ist _keine_ „include“-Operation, wie du
sie vielleicht aus anderen Programmiersprachen kennst.

Als Nächstes lagern wir das Modul `hosting` in eine eigene Datei aus. Das
Vorgehen ist etwas anders, weil `hosting` ein Kindmodul von `front_of_house` ist
und nicht des Wurzelmoduls. Wir legen die Datei für `hosting` in ein neues
Verzeichnis, das nach seinen Vorfahren im Modulbaum benannt ist, in diesem Fall
_src/front_of_house_.

Um mit dem Verschieben von `hosting` zu beginnen, ändern wir
_src/front_of_house.rs_ so, dass es nur noch die Deklaration des Moduls
`hosting` enthält:

<Listing file-name="src/front_of_house.rs">

```rust,ignore
{{#rustdoc_include ../listings/ch07-managing-growing-projects/no-listing-02-extracting-hosting/src/front_of_house.rs}}
```

</Listing>

Dann erstellen wir ein Verzeichnis _src/front_of_house_ und eine Datei
_hosting.rs_, die die Definitionen aus dem Modul `hosting` enthält:

<Listing file-name="src/front_of_house/hosting.rs">

```rust,ignore
{{#rustdoc_include ../listings/ch07-managing-growing-projects/no-listing-02-extracting-hosting/src/front_of_house/hosting.rs}}
```

</Listing>

Würden wir _hosting.rs_ stattdessen in das Verzeichnis _src_ legen, würde der
Compiler erwarten, dass der Code aus _hosting.rs_ zu einem Modul `hosting`
gehört, das in der Crate-Root deklariert ist, und nicht als Kind des Moduls
`front_of_house`. Durch die Regeln des Compilers, welche Dateien er für den Code
welcher Module prüft, entsprechen die Verzeichnisse und Dateien dem Modulbaum
genauer.

> ### Alternative Dateipfade {#alternate-file-paths}
>
> Bisher haben wir die idiomatischsten Dateipfade behandelt, die der
> Rust-Compiler verwendet, aber Rust unterstützt auch eine ältere Art von
> Dateipfaden. Für ein Modul namens `front_of_house`, das in der Crate-Root
> deklariert ist, sucht der Compiler den Code des Moduls in:
>
> - _src/front_of_house.rs_ (was wir behandelt haben)
> - _src/front_of_house/mod.rs_ (älterer, weiterhin unterstützter Pfad)
>
> Für ein Modul namens `hosting`, das ein Untermodul von `front_of_house` ist,
> sucht der Compiler den Code des Moduls in:
>
> - _src/front_of_house/hosting.rs_ (was wir behandelt haben)
> - _src/front_of_house/hosting/mod.rs_ (älterer, weiterhin unterstützter Pfad)
>
> Wenn du beide Stile für dasselbe Modul verwendest, bekommst du einen
> Compilerfehler. Beide Stile gemischt für verschiedene Module im selben Projekt
> zu verwenden, ist erlaubt, kann aber Leute verwirren, die sich in deinem
> Projekt zurechtfinden müssen.
>
> Der Hauptnachteil des Stils mit Dateien namens _mod.rs_ ist, dass dein Projekt
> am Ende viele Dateien namens _mod.rs_ haben kann, was verwirrend werden kann,
> wenn du sie gleichzeitig in deinem Editor geöffnet hast.

Wir haben den Code jedes Moduls in eine separate Datei verschoben, und der
Modulbaum bleibt gleich. Die Funktionsaufrufe in `eat_at_restaurant`
funktionieren ohne jede Änderung, auch wenn die Definitionen in verschiedenen
Dateien stehen. Mit dieser Technik kannst du Module in neue Dateien verschieben,
wenn sie größer werden.

Beachte, dass sich auch die Anweisung `pub use crate::front_of_house::hosting`
in _src/lib.rs_ nicht geändert hat und dass `use` keinen Einfluss darauf hat,
welche Dateien als Teil des Crates kompiliert werden. Das Schlüsselwort `mod`
deklariert Module, und Rust sucht den Code, der in ein Modul gehört, in einer
Datei mit demselben Namen wie das Modul.

{{#quiz ../quizzes/ch07-05-files.toml}}

## Zusammenfassung {#summary}

Mit Rust kannst du ein Paket in mehrere Crates und ein Crate in Module
aufteilen, sodass du aus einem Modul auf Elemente verweisen kannst, die in einem
anderen Modul definiert sind. Dazu gibst du absolute oder relative Pfade an.
Diese Pfade kannst du mit einer `use`-Anweisung in den Gültigkeitsbereich
(_scope_) bringen, damit du bei mehrfacher Verwendung des Elements in diesem
Gültigkeitsbereich einen kürzeren Pfad verwenden kannst. Modulcode ist
standardmäßig privat, aber du kannst Definitionen öffentlich machen, indem du
das Schlüsselwort `pub` hinzufügst.

Im nächsten Kapitel sehen wir uns einige Collection-Datenstrukturen der
Standardbibliothek an, die du in deinem sauber organisierten Code verwenden
kannst.

[paths]: ch07-03-paths-for-referring-to-an-item-in-the-module-tree.html
