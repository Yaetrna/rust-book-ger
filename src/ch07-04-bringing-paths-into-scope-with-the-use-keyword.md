## Pfade mit dem Schlüsselwort `use` in den Gültigkeitsbereich bringen {#bringing-paths-into-scope-with-the-use-keyword}

Die Pfade zum Aufrufen von Funktionen ausschreiben zu müssen, kann sich unbequem
und repetitiv anfühlen. In Listing 7-7 mussten wir, egal ob wir den absoluten
oder den relativen Pfad zur Funktion `add_to_waitlist` gewählt hatten, jedes
Mal, wenn wir `add_to_waitlist` aufrufen wollten, auch `front_of_house` und
`hosting` angeben. Zum Glück gibt es eine Möglichkeit, das zu vereinfachen: Wir
können mit dem Schlüsselwort `use` einmal eine Abkürzung zu einem Pfad erzeugen
und dann überall sonst im Gültigkeitsbereich (_scope_) den kürzeren Namen
verwenden.

In Listing 7-11 bringen wir das Modul `crate::front_of_house::hosting` in den
Gültigkeitsbereich der Funktion `eat_at_restaurant`, sodass wir nur noch
`hosting::add_to_waitlist` angeben müssen, um die Funktion `add_to_waitlist` in
`eat_at_restaurant` aufzurufen.

<Listing number="7-11" file-name="src/lib.rs" caption="Ein Modul mit `use` in den Gültigkeitsbereich bringen">

```rust,noplayground,test_harness
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-11/src/lib.rs}}
```

</Listing>

`use` und einen Pfad in einem Gültigkeitsbereich hinzuzufügen, ähnelt dem
Anlegen eines symbolischen Links im Dateisystem. Durch das Hinzufügen von
`use crate::front_of_house::hosting` in der Crate-Root ist `hosting` in diesem
Gültigkeitsbereich nun ein gültiger Name, als wäre das Modul `hosting` in der
Crate-Root definiert worden. Auch bei Pfaden, die mit `use` in den
Gültigkeitsbereich gebracht werden, wird wie bei allen anderen Pfaden die
Sichtbarkeit geprüft.

Beachte, dass `use` die Abkürzung nur für den jeweiligen Gültigkeitsbereich
erzeugt, in dem das `use` steht. Listing 7-12 verschiebt die Funktion
`eat_at_restaurant` in ein neues Kindmodul namens `customer`, das dann ein
anderer Gültigkeitsbereich ist als der der `use`-Anweisung, sodass der
Funktionsrumpf nicht kompiliert.

<Listing number="7-12" file-name="src/lib.rs" caption="Eine `use`-Anweisung gilt nur in dem Gültigkeitsbereich, in dem sie steht.">

```rust,noplayground,test_harness,does_not_compile,ignore
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-12/src/lib.rs}}
```

</Listing>

Der Compilerfehler zeigt, dass die Abkürzung innerhalb des Moduls `customer`
nicht mehr gilt:

```console
{{#include ../listings/ch07-managing-growing-projects/listing-07-12/output.txt}}
```

Beachte, dass es außerdem eine Warnung gibt, dass das `use` in seinem
Gültigkeitsbereich nicht mehr verwendet wird! Um dieses Problem zu beheben,
verschiebe das `use` ebenfalls in das Modul `customer` oder verweise im
Kindmodul `customer` mit `super::hosting` auf die Abkürzung im Elternmodul.

### Idiomatische `use`-Pfade erstellen {#creating-idiomatic-use-paths}

Vielleicht hast du dich bei Listing 7-11 gefragt, warum wir
`use
crate::front_of_house::hosting` angegeben und dann in `eat_at_restaurant`
`hosting::add_to_waitlist` aufgerufen haben, statt den `use`-Pfad bis zur
Funktion `add_to_waitlist` auszuschreiben, um dasselbe Ergebnis zu erzielen, wie
in Listing 7-13.

<Listing number="7-13" file-name="src/lib.rs" caption="Die Funktion `add_to_waitlist` mit `use` in den Gültigkeitsbereich bringen, was nicht idiomatisch ist">

```rust,noplayground,test_harness
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-13/src/lib.rs}}
```

</Listing>

Obwohl Listing 7-11 und Listing 7-13 dasselbe erreichen, ist Listing 7-11 die
idiomatische Art, eine Funktion mit `use` in den Gültigkeitsbereich zu bringen.
Bringen wir das Elternmodul der Funktion mit `use` in den Gültigkeitsbereich,
müssen wir beim Aufruf der Funktion das Elternmodul angeben. Das Elternmodul
beim Aufruf anzugeben, macht deutlich, dass die Funktion nicht lokal definiert
ist, und hält die Wiederholung des vollständigen Pfades trotzdem gering. Beim
Code in Listing 7-13 ist unklar, wo `add_to_waitlist` definiert ist.

Wenn wir dagegen Structs, Enums und andere Elemente mit `use` einbinden, ist es
idiomatisch, den vollständigen Pfad anzugeben. Listing 7-14 zeigt die
idiomatische Art, das Struct `HashMap` der Standardbibliothek in den
Gültigkeitsbereich eines Binary-Crates zu bringen.

<Listing number="7-14" file-name="src/main.rs" caption="`HashMap` auf idiomatische Weise in den Gültigkeitsbereich bringen">

```rust
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-14/src/main.rs}}
```

</Listing>

Hinter diesem Idiom steckt kein zwingender Grund: Es ist einfach die Konvention,
die sich herausgebildet hat, und die Leute haben sich daran gewöhnt, Rust-Code
so zu lesen und zu schreiben.

Die Ausnahme von diesem Idiom ist, wenn wir mit `use`-Anweisungen zwei Elemente
mit demselben Namen in den Gültigkeitsbereich bringen, denn das erlaubt Rust
nicht. Listing 7-15 zeigt, wie man zwei `Result`-Typen in den Gültigkeitsbereich
bringt, die denselben Namen, aber unterschiedliche Elternmodule haben, und wie
man auf sie verweist.

<Listing number="7-15" file-name="src/lib.rs" caption="Um zwei Typen mit demselben Namen in denselben Gültigkeitsbereich zu bringen, muss man ihre Elternmodule verwenden.">

```rust,noplayground
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-15/src/lib.rs:here}}
```

</Listing>

Wie du siehst, unterscheiden die Elternmodule die beiden `Result`-Typen. Würden
wir stattdessen `use std::fmt::Result` und `use std::io::Result` angeben, hätten
wir zwei `Result`-Typen im selben Gültigkeitsbereich, und Rust wüsste nicht,
welchen wir meinen, wenn wir `Result` verwenden.

### Mit dem Schlüsselwort `as` neue Namen vergeben {#providing-new-names-with-the-as-keyword}

Es gibt noch eine andere Lösung für das Problem, zwei Typen mit demselben Namen
mit `use` in denselben Gültigkeitsbereich zu bringen: Nach dem Pfad können wir
`as` und einen neuen lokalen Namen, einen _Alias_, für den Typ angeben. Listing
7-16 zeigt eine andere Schreibweise für den Code in Listing 7-15, bei der einer
der beiden `Result`-Typen mit `as` umbenannt wird.

<Listing number="7-16" file-name="src/lib.rs" caption="Einen Typ umbenennen, wenn er mit dem Schlüsselwort `as` in den Gültigkeitsbereich gebracht wird">

```rust,noplayground
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-16/src/lib.rs:here}}
```

</Listing>

In der zweiten `use`-Anweisung haben wir für den Typ `std::io::Result` den neuen
Namen `IoResult` gewählt, der nicht mit dem `Result` aus `std::fmt` kollidiert,
das wir ebenfalls in den Gültigkeitsbereich gebracht haben. Listing 7-15 und
Listing 7-16 gelten beide als idiomatisch, die Wahl liegt also bei dir!

### Namen mit `pub use` reexportieren {#re-exporting-names-with-pub-use}

Wenn wir einen Namen mit dem Schlüsselwort `use` in den Gültigkeitsbereich
bringen, ist der Name in dem Gültigkeitsbereich, in den wir ihn importiert
haben, privat. Damit Code außerhalb dieses Gültigkeitsbereichs auf diesen Namen
verweisen kann, als wäre er in diesem Gültigkeitsbereich definiert worden,
können wir `pub` und `use` kombinieren. Diese Technik heißt _Reexportieren_
(_re-exporting_), weil wir ein Element in den Gültigkeitsbereich bringen, es
aber gleichzeitig anderen zur Verfügung stellen, damit sie es in ihren
Gültigkeitsbereich bringen können.

Listing 7-17 zeigt den Code aus Listing 7-11, wobei `use` im Wurzelmodul zu
`pub use` geändert wurde.

<Listing number="7-17" file-name="src/lib.rs" caption="Einen Namen mit `pub use` jedem Code aus einem neuen Gültigkeitsbereich zur Verfügung stellen">

```rust,noplayground,test_harness
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-17/src/lib.rs}}
```

</Listing>

Vor dieser Änderung hätte externer Code die Funktion `add_to_waitlist` über den
Pfad `restaurant::front_of_house::hosting::add_to_waitlist()` aufrufen müssen,
wofür außerdem das Modul `front_of_house` mit `pub` hätte gekennzeichnet sein
müssen. Da dieses `pub
use` das Modul `hosting` nun aus dem Wurzelmodul
reexportiert hat, kann externer Code stattdessen den Pfad
`restaurant::hosting::add_to_waitlist()` verwenden.

Reexportieren ist nützlich, wenn sich die interne Struktur deines Codes davon
unterscheidet, wie Programmierende, die deinen Code aufrufen, über den
Anwendungsbereich denken würden. In der Restaurant-Metapher etwa denken die
Leute, die das Restaurant betreiben, in „Front of House“ und „Back of House“.
Gäste, die ein Restaurant besuchen, denken über die Bereiche des Restaurants
aber wahrscheinlich nicht in diesen Begriffen. Mit `pub
use` können wir unseren
Code mit einer Struktur schreiben, aber eine andere Struktur offenlegen. Dadurch
ist unsere Bibliothek sowohl für Programmierende, die an der Bibliothek
arbeiten, als auch für Programmierende, die die Bibliothek aufrufen, gut
organisiert. Ein weiteres Beispiel für `pub use` und dafür, wie es sich auf die
Dokumentation deines Crates auswirkt, sehen wir uns in
[„Eine bequeme öffentliche API exportieren“][ch14-pub-use]<!-- ignore --> in
Kapitel 14 an.

### Externe Pakete verwenden {#using-external-packages}

In Kapitel 2 haben wir ein Ratespiel programmiert, das ein externes Paket namens
`rand` verwendet hat, um Zufallszahlen zu erhalten. Um `rand` in unserem Projekt
zu verwenden, haben wir diese Zeile zu _Cargo.toml_ hinzugefügt:

<!-- When updating the version of `rand` used, also update the version of
`rand` used in these files so they all match:
* ch02-00-guessing-game-tutorial.md
* ch14-03-cargo-workspaces.md
-->

<Listing file-name="Cargo.toml">

```toml
{{#include ../listings/ch02-guessing-game-tutorial/listing-02-02/Cargo.toml:9:}}
```

</Listing>

Wird `rand` in _Cargo.toml_ als Abhängigkeit hinzugefügt, lädt Cargo das Paket
`rand` und alle Abhängigkeiten von [crates.io](https://crates.io/) herunter und
stellt `rand` unserem Projekt zur Verfügung.

Um dann Definitionen aus `rand` in den Gültigkeitsbereich unseres Pakets zu
bringen, haben wir eine `use`-Zeile hinzugefügt, die mit dem Namen des Crates,
`rand`, beginnt, und die Elemente aufgelistet, die wir in den Gültigkeitsbereich
bringen wollten. Erinnere dich: In
[„Eine Zufallszahl erzeugen“][rand]<!-- ignore --> in Kapitel 2 haben wir den
Trait `Rng` in den Gültigkeitsbereich gebracht und die Funktion
`rand::thread_rng` aufgerufen:

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/listing-02-03/src/main.rs:ch07-04}}
```

Mitglieder der Rust-Community haben auf [crates.io](https://crates.io/) viele
Pakete bereitgestellt, und um eines davon in dein Paket einzubinden, sind immer
dieselben Schritte nötig: Du führst es in der Datei _Cargo.toml_ deines Pakets
auf und bringst mit `use` Elemente aus seinen Crates in den Gültigkeitsbereich.

Beachte, dass auch die Standardbibliothek `std` ein Crate ist, das außerhalb
unseres Pakets liegt. Da die Standardbibliothek mit der Sprache Rust
ausgeliefert wird, müssen wir _Cargo.toml_ nicht ändern, um `std` einzubinden.
Wir müssen aber mit `use` auf sie verweisen, um Elemente daraus in den
Gültigkeitsbereich unseres Pakets zu bringen. Für `HashMap` würden wir zum
Beispiel diese Zeile verwenden:

```rust
use std::collections::HashMap;
```

Das ist ein absoluter Pfad, der mit `std` beginnt, dem Namen des Crates der
Standardbibliothek.

<!-- Old headings. Do not remove or links may break. -->

<a id="using-nested-paths-to-clean-up-large-use-lists"></a>

### Verschachtelte Pfade, um `use`-Listen aufzuräumen {#using-nested-paths-to-clean-up-use-lists}

Wenn wir mehrere Elemente verwenden, die im selben Crate oder im selben Modul
definiert sind, kann es in unseren Dateien viel vertikalen Platz einnehmen,
jedes Element in einer eigenen Zeile aufzuführen. Diese beiden `use`-Anweisungen
aus dem Ratespiel in Listing 2-4 bringen zum Beispiel Elemente aus `std` in den
Gültigkeitsbereich:

<Listing file-name="src/main.rs">

```rust,ignore
{{#rustdoc_include ../listings/ch07-managing-growing-projects/no-listing-01-use-std-unnested/src/main.rs:here}}
```

</Listing>

Stattdessen können wir mit verschachtelten Pfaden dieselben Elemente in einer
Zeile in den Gültigkeitsbereich bringen. Dazu geben wir den gemeinsamen Teil des
Pfades an, gefolgt von zwei Doppelpunkten und dann geschweiften Klammern um eine
Liste der Teile der Pfade, die sich unterscheiden, wie in Listing 7-18 gezeigt.

<Listing number="7-18" file-name="src/main.rs" caption="Einen verschachtelten Pfad angeben, um mehrere Elemente mit demselben Präfix in den Gültigkeitsbereich zu bringen">

```rust,ignore
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-18/src/main.rs:here}}
```

</Listing>

In größeren Programmen kann es die Anzahl der nötigen einzelnen
`use`-Anweisungen erheblich verringern, wenn man viele Elemente aus demselben
Crate oder Modul mit verschachtelten Pfaden in den Gültigkeitsbereich bringt!

Wir können einen verschachtelten Pfad auf jeder Ebene eines Pfades verwenden.
Das ist nützlich, wenn man zwei `use`-Anweisungen zusammenführt, die einen
Teilpfad gemeinsam haben. Listing 7-19 zeigt zum Beispiel zwei
`use`-Anweisungen: eine, die `std::io` in den Gültigkeitsbereich bringt, und
eine, die `std::io::Write` in den Gültigkeitsbereich bringt.

<Listing number="7-19" file-name="src/lib.rs" caption="Zwei `use`-Anweisungen, bei denen die eine ein Teilpfad der anderen ist">

```rust,noplayground
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-19/src/lib.rs}}
```

</Listing>

Der gemeinsame Teil dieser beiden Pfade ist `std::io`, und das ist der
vollständige erste Pfad. Um diese beiden Pfade zu einer `use`-Anweisung
zusammenzuführen, können wir im verschachtelten Pfad `self` verwenden, wie in
Listing 7-20 gezeigt.

<Listing number="7-20" file-name="src/lib.rs" caption="Die Pfade aus Listing 7-19 zu einer `use`-Anweisung zusammenführen">

```rust,noplayground
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-20/src/lib.rs}}
```

</Listing>

Diese Zeile bringt `std::io` und `std::io::Write` in den Gültigkeitsbereich.

<!-- Old headings. Do not remove or links may break. -->

<a id="the-glob-operator"></a>

### Elemente mit dem Glob-Operator importieren {#importing-items-with-the-glob-operator}

Wenn wir _alle_ öffentlichen Elemente, die in einem Pfad definiert sind, in den
Gültigkeitsbereich bringen wollen, können wir diesen Pfad gefolgt vom
Glob-Operator `*` angeben:

```rust
use std::collections::*;
```

Diese `use`-Anweisung bringt alle öffentlichen Elemente, die in
`std::collections` definiert sind, in den aktuellen Gültigkeitsbereich. Sei
vorsichtig mit dem Glob-Operator! Mit Glob lässt sich schwerer erkennen, welche
Namen im Gültigkeitsbereich sind und wo ein Name, den dein Programm verwendet,
definiert wurde. Außerdem ändert sich, wenn die Abhängigkeit ihre Definitionen
ändert, auch das, was du importiert hast. Das kann beim Aktualisieren der
Abhängigkeit zu Compilerfehlern führen, zum Beispiel wenn die Abhängigkeit eine
Definition mit demselben Namen hinzufügt wie eine deiner Definitionen im selben
Gültigkeitsbereich.

Der Glob-Operator wird oft beim Testen verwendet, um alles, was getestet wird,
in das Modul `tests` zu bringen; darüber sprechen wir in
[„Wie man Tests schreibt“][writing-tests]<!-- ignore --> in Kapitel 11. Der
Glob-Operator wird manchmal auch als Teil des Prelude-Schemas verwendet: Mehr
Informationen zu diesem Schema findest du in
[der Dokumentation der Standardbibliothek](https://doc.rust-lang.org/std/prelude/index.html#other-preludes)<!-- ignore -->.

{{#quiz ../quizzes/ch07-04-use.toml}}

[ch14-pub-use]: ch14-02-publishing-to-crates-io.html#exporting-a-convenient-public-api-with-pub-use
[rand]: ch02-00-guessing-game-tutorial.html#generating-a-random-number
[writing-tests]: ch11-01-writing-tests.html#how-to-write-tests
