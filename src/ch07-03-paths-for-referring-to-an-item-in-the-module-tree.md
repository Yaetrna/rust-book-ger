## Pfade, um auf ein Element im Modulbaum zu verweisen {#paths-for-referring-to-an-item-in-the-module-tree}

Um Rust zu zeigen, wo ein Element in einem Modulbaum zu finden ist, verwenden
wir einen Pfad, so wie wir einen Pfad verwenden, wenn wir uns in einem
Dateisystem bewegen. Um eine Funktion aufzurufen, müssen wir ihren Pfad kennen.

Ein Pfad kann zwei Formen haben:

- Ein _absoluter Pfad_ ist der vollständige Pfad ab einer Crate-Root
  (Wurzeldatei des Crates); bei Code aus einem externen Crate beginnt der
  absolute Pfad mit dem Namen des Crates, und bei Code aus dem aktuellen Crate
  beginnt er mit dem Literal `crate`.
- Ein _relativer Pfad_ beginnt beim aktuellen Modul und verwendet `self`,
  `super` oder einen Bezeichner im aktuellen Modul.

Auf absolute wie relative Pfade folgen ein oder mehrere Bezeichner, getrennt
durch doppelte Doppelpunkte (`::`).

Zurück zu Listing 7-1: Sagen wir, wir wollen die Funktion `add_to_waitlist`
aufrufen. Das ist dieselbe Frage wie: Was ist der Pfad der Funktion
`add_to_waitlist`? Listing 7-3 enthält Listing 7-1, wobei einige Module und
Funktionen entfernt sind.

Wir zeigen zwei Möglichkeiten, die Funktion `add_to_waitlist` aus einer neuen
Funktion `eat_at_restaurant` aufzurufen, die in der Crate-Root definiert ist.
Diese Pfade sind korrekt, aber es gibt noch ein anderes Problem, das verhindert,
dass dieses Beispiel in dieser Form kompiliert. Warum, erklären wir gleich.

Die Funktion `eat_at_restaurant` ist Teil der öffentlichen API unseres
Library-Crates, daher kennzeichnen wir sie mit dem Schlüsselwort `pub`. Im
Abschnitt [„Pfade mit dem Schlüsselwort `pub` offenlegen“][pub]<!-- ignore -->
gehen wir ausführlicher auf `pub` ein.

<Listing number="7-3" file-name="src/lib.rs" caption="Die Funktion `add_to_waitlist` mit absoluten und relativen Pfaden aufrufen">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-03/src/lib.rs}}
```

</Listing>

Beim ersten Aufruf der Funktion `add_to_waitlist` in `eat_at_restaurant`
verwenden wir einen absoluten Pfad. Die Funktion `add_to_waitlist` ist im selben
Crate definiert wie `eat_at_restaurant`, daher können wir einen absoluten Pfad
mit dem Schlüsselwort `crate` beginnen. Dann führen wir nacheinander jedes Modul
auf, bis wir bei `add_to_waitlist` ankommen. Du kannst dir ein Dateisystem mit
derselben Struktur vorstellen: Wir würden den Pfad
`/front_of_house/hosting/add_to_waitlist` angeben, um das Programm
`add_to_waitlist` auszuführen; den Namen `crate` zu verwenden, um bei der
Crate-Root zu beginnen, ist so, als würdest du in deiner Shell mit `/` bei der
Wurzel des Dateisystems beginnen.

Beim zweiten Aufruf von `add_to_waitlist` in `eat_at_restaurant` verwenden wir
einen relativen Pfad. Der Pfad beginnt mit `front_of_house`, dem Namen des
Moduls, das auf derselben Ebene des Modulbaums definiert ist wie
`eat_at_restaurant`. Hier wäre das Gegenstück im Dateisystem der Pfad
`front_of_house/hosting/add_to_waitlist`. Beginnt ein Pfad mit einem Modulnamen,
ist er relativ.

Ob du einen relativen oder einen absoluten Pfad verwendest, entscheidest du je
nach Projekt, und es hängt davon ab, ob du den Code, der ein Element definiert,
eher getrennt von dem Code verschieben wirst, der das Element verwendet, oder
zusammen mit ihm. Würden wir zum Beispiel das Modul `front_of_house` und die
Funktion `eat_at_restaurant` in ein Modul namens `customer_experience`
verschieben, müssten wir den absoluten Pfad zu `add_to_waitlist` anpassen, aber
der relative Pfad wäre weiterhin gültig. Würden wir dagegen die Funktion
`eat_at_restaurant` allein in ein Modul namens `dining` verschieben, bliebe der
absolute Pfad zum Aufruf von `add_to_waitlist` gleich, aber der relative Pfad
müsste angepasst werden. Wir bevorzugen im Allgemeinen absolute Pfade, weil wir
Codedefinitionen und Aufrufe von Elementen eher unabhängig voneinander
verschieben wollen.

Versuchen wir, Listing 7-3 zu kompilieren, und finden wir heraus, warum es noch
nicht kompiliert! Die Fehler, die wir bekommen, siehst du in Listing 7-4.

<Listing number="7-4" caption="Compilerfehler beim Bauen des Codes in Listing 7-3">

```console
{{#include ../listings/ch07-managing-growing-projects/listing-07-03/output.txt}}
```

</Listing>

Die Fehlermeldungen besagen, dass das Modul `hosting` privat ist. Mit anderen
Worten: Wir haben die richtigen Pfade für das Modul `hosting` und die Funktion
`add_to_waitlist`, aber Rust lässt uns sie nicht verwenden, weil es keinen
Zugriff auf die privaten Bereiche hat. In Rust sind alle Elemente (Funktionen,
Methoden, Structs, Enums, Module und Konstanten) standardmäßig gegenüber ihren
Elternmodulen privat. Wenn du ein Element wie eine Funktion oder ein Struct
privat machen willst, legst du es in ein Modul.

Elemente in einem Elternmodul können die privaten Elemente in Kindmodulen nicht
verwenden, aber Elemente in Kindmodulen können die Elemente in ihren
Vorfahrenmodulen verwenden. Das liegt daran, dass Kindmodule ihre
Implementierungsdetails umhüllen und verbergen, aber den Kontext sehen können,
in dem sie definiert sind. Um bei unserer Metapher zu bleiben: Stell dir die
Sichtbarkeitsregeln (_privacy rules_) wie das Hinterzimmer eines Restaurants
vor: Was dort vor sich geht, bleibt den Gästen des Restaurants verborgen, aber
die Geschäftsführung kann alles in dem Restaurant sehen und tun, das sie
betreibt.

Rust hat sich dafür entschieden, dass das Modulsystem so funktioniert, damit das
Verbergen innerer Implementierungsdetails der Standard ist. So weißt du, welche
Teile des inneren Codes du ändern kannst, ohne den äußeren Code kaputtzumachen.
Rust gibt dir aber die Möglichkeit, innere Teile des Codes von Kindmodulen
gegenüber äußeren Vorfahrenmodulen offenzulegen, indem du ein Element mit dem
Schlüsselwort `pub` öffentlich machst.

### Pfade mit dem Schlüsselwort `pub` offenlegen {#exposing-paths-with-the-pub-keyword}

Kehren wir zum Fehler in Listing 7-4 zurück, der uns mitgeteilt hat, dass das
Modul `hosting` privat ist. Wir wollen, dass die Funktion `eat_at_restaurant` im
Elternmodul Zugriff auf die Funktion `add_to_waitlist` im Kindmodul hat, also
kennzeichnen wir das Modul `hosting` mit dem Schlüsselwort `pub`, wie in Listing
7-5 gezeigt.

<Listing number="7-5" file-name="src/lib.rs" caption="Das Modul `hosting` als `pub` deklarieren, um es aus `eat_at_restaurant` heraus zu verwenden">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-05/src/lib.rs:here}}
```

</Listing>

Leider führt der Code in Listing 7-5 immer noch zu Compilerfehlern, wie Listing
7-6 zeigt.

<Listing number="7-6" caption="Compilerfehler beim Bauen des Codes in Listing 7-5">

```console
{{#include ../listings/ch07-managing-growing-projects/listing-07-05/output.txt}}
```

</Listing>

Was ist passiert? Das Schlüsselwort `pub` vor `mod hosting` macht das Modul
öffentlich. Wenn wir nach dieser Änderung auf `front_of_house` zugreifen können,
können wir auch auf `hosting` zugreifen. Aber der _Inhalt_ von `hosting` ist
immer noch privat; ein Modul öffentlich zu machen, macht nicht seinen Inhalt
öffentlich. Das Schlüsselwort `pub` an einem Modul erlaubt nur Code in seinen
Vorfahrenmodulen, auf das Modul zu verweisen, nicht aber, auf seinen inneren
Code zuzugreifen. Da Module Container sind, können wir nicht viel erreichen,
indem wir nur das Modul öffentlich machen; wir müssen weitergehen und auch eines
oder mehrere der Elemente im Modul öffentlich machen.

Die Fehler in Listing 7-6 besagen, dass die Funktion `add_to_waitlist` privat
ist. Die Sichtbarkeitsregeln gelten für Structs, Enums, Funktionen und Methoden
ebenso wie für Module.

Machen wir also auch die Funktion `add_to_waitlist` öffentlich, indem wir vor
ihrer Definition das Schlüsselwort `pub` einfügen, wie in Listing 7-7.

<Listing number="7-7" file-name="src/lib.rs" caption="Durch das Schlüsselwort `pub` an `mod hosting` und `fn add_to_waitlist` können wir die Funktion aus `eat_at_restaurant` aufrufen.">

```rust,noplayground,test_harness
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-07/src/lib.rs:here}}
```

</Listing>

Jetzt kompiliert der Code! Um zu sehen, warum wir diese Pfade in
`eat_at_restaurant` unter Beachtung der Sichtbarkeitsregeln verwenden können,
nachdem wir das Schlüsselwort `pub` hinzugefügt haben, sehen wir uns den
absoluten und den relativen Pfad an.

Beim absoluten Pfad beginnen wir mit `crate`, der Wurzel des Modulbaums unseres
Crates. Das Modul `front_of_house` ist in der Crate-Root definiert.
`front_of_house` ist zwar nicht öffentlich, aber da die Funktion
`eat_at_restaurant` im selben Modul definiert ist wie `front_of_house` (das
heißt, `eat_at_restaurant` und `front_of_house` sind Geschwister), können wir
aus `eat_at_restaurant` auf `front_of_house` verweisen. Als Nächstes kommt das
Modul `hosting`, das mit `pub` gekennzeichnet ist. Wir können auf das
Elternmodul von `hosting` zugreifen, also können wir auf `hosting` zugreifen.
Schließlich ist die Funktion `add_to_waitlist` mit `pub` gekennzeichnet, und wir
können auf ihr Elternmodul zugreifen, also funktioniert dieser Funktionsaufruf!

Beim relativen Pfad ist die Logik dieselbe wie beim absoluten Pfad, abgesehen
vom ersten Schritt: Statt bei der Crate-Root beginnt der Pfad bei
`front_of_house`. Das Modul `front_of_house` ist im selben Modul definiert wie
`eat_at_restaurant`, also funktioniert der relative Pfad, der in dem Modul
beginnt, in dem `eat_at_restaurant` definiert ist. Da `hosting` und
`add_to_waitlist` mit `pub` gekennzeichnet sind, funktioniert dann auch der Rest
des Pfades, und dieser Funktionsaufruf ist gültig!

Wenn du vorhast, dein Library-Crate zu teilen, damit andere Projekte deinen Code
verwenden können, ist deine öffentliche API dein Vertrag mit den Nutzerinnen und
Nutzern deines Crates, der festlegt, wie sie mit deinem Code interagieren
können. Es gibt viele Überlegungen dazu, wie man Änderungen an der öffentlichen
API so handhabt, dass andere sich leichter auf dein Crate stützen können. Diese
Überlegungen gehen über den Rahmen dieses Buchs hinaus; wenn dich das Thema
interessiert, sieh dir [die Rust API Guidelines][api-guidelines] an.

> #### Bewährte Vorgehensweisen für Pakete mit einer Binärdatei und einer Bibliothek {#best-practices-for-packages-with-a-binary-and-a-library}
>
> Wir haben erwähnt, dass ein Paket sowohl eine Binary-Crate-Root _src/main.rs_
> als auch eine Library-Crate-Root _src/lib.rs_ enthalten kann und dass beide
> Crates standardmäßig den Namen des Pakets tragen. Typischerweise enthalten
> Pakete, die nach diesem Schema sowohl ein Library- als auch ein Binary-Crate
> haben, im Binary-Crate gerade so viel Code, dass eine ausführbare Datei
> gestartet wird, die Code aus dem Library-Crate aufruft. So profitieren andere
> Projekte von möglichst viel der Funktionalität, die das Paket bereitstellt,
> weil der Code des Library-Crates geteilt werden kann.
>
> Der Modulbaum sollte in _src/lib.rs_ definiert werden. Dann können alle
> öffentlichen Elemente im Binary-Crate verwendet werden, indem Pfade mit dem
> Namen des Pakets beginnen. Das Binary-Crate wird zu einem Nutzer des
> Library-Crates, genau so, wie ein völlig externes Crate das Library-Crate
> verwenden würde: Es kann nur die öffentliche API verwenden. Das hilft dir,
> eine gute API zu entwerfen; du bist nicht nur Autor, sondern auch Nutzer!
>
> In [Kapitel 12][ch12]<!-- ignore --> zeigen wir diese Art der Organisation an
> einem Kommandozeilenprogramm, das sowohl ein Binary-Crate als auch ein
> Library-Crate enthält.

{{#quiz ../quizzes/ch07-03-paths-sec1.toml}}

### Relative Pfade mit `super` beginnen {#starting-relative-paths-with-super}

Wir können relative Pfade bilden, die im Elternmodul beginnen statt im aktuellen
Modul oder in der Crate-Root, indem wir `super` an den Anfang des Pfades setzen.
Das ist so, als würde man einen Dateisystempfad mit der Syntax `..` beginnen,
die bedeutet, ins Elternverzeichnis zu gehen. Mit `super` können wir auf ein
Element verweisen, von dem wir wissen, dass es im Elternmodul liegt. Das kann es
erleichtern, den Modulbaum umzuordnen, wenn das Modul eng mit dem Elternmodul
zusammenhängt, das Elternmodul aber eines Tages an eine andere Stelle im
Modulbaum verschoben werden könnte.

Betrachte den Code in Listing 7-8, der die Situation modelliert, in der ein Koch
eine falsche Bestellung korrigiert und sie persönlich zum Gast bringt. Die
Funktion `fix_incorrect_order`, die im Modul `back_of_house` definiert ist, ruft
die Funktion `deliver_order` auf, die im Elternmodul definiert ist, indem sie
den Pfad zu `deliver_order` angibt, beginnend mit `super`.

<Listing number="7-8" file-name="src/lib.rs" caption="Eine Funktion mit einem relativen Pfad aufrufen, der mit `super` beginnt">

```rust,noplayground,test_harness
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-08/src/lib.rs}}
```

</Listing>

Die Funktion `fix_incorrect_order` liegt im Modul `back_of_house`, also können
wir mit `super` zum Elternmodul von `back_of_house` gehen, das in diesem Fall
`crate` ist, die Wurzel. Von dort aus suchen wir `deliver_order` und finden es.
Erfolg! Wir gehen davon aus, dass das Modul `back_of_house` und die Funktion
`deliver_order` wahrscheinlich in derselben Beziehung zueinander bleiben und
gemeinsam verschoben werden, falls wir den Modulbaum des Crates umorganisieren.
Deshalb haben wir `super` verwendet, damit wir in Zukunft weniger Stellen im
Code anpassen müssen, falls dieser Code in ein anderes Modul verschoben wird.

### Structs und Enums öffentlich machen {#making-structs-and-enums-public}

Wir können `pub` auch verwenden, um Structs und Enums als öffentlich zu
kennzeichnen, aber bei der Verwendung von `pub` mit Structs und Enums gibt es
ein paar zusätzliche Details. Wenn wir `pub` vor eine Struct-Definition setzen,
machen wir das Struct öffentlich, aber die Felder des Structs bleiben privat.
Wir können jedes Feld einzeln öffentlich machen oder nicht. In Listing 7-9 haben
wir ein öffentliches Struct `back_of_house::Breakfast` mit einem öffentlichen
Feld `toast`, aber einem privaten Feld `seasonal_fruit` definiert. Das
modelliert den Fall in einem Restaurant, in dem der Gast die Brotsorte zum Essen
auswählen kann, aber die Küche je nach Saison und Vorrat entscheidet, welches
Obst dazu serviert wird. Das verfügbare Obst wechselt schnell, daher können
Gäste das Obst nicht auswählen und nicht einmal sehen, welches Obst sie
bekommen.

<Listing number="7-9" file-name="src/lib.rs" caption="Ein Struct mit einigen öffentlichen und einigen privaten Feldern">

```rust,noplayground
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-09/src/lib.rs}}
```

</Listing>

Da das Feld `toast` im Struct `back_of_house::Breakfast` öffentlich ist, können
wir in `eat_at_restaurant` mit Punktnotation in das Feld `toast` schreiben und
aus ihm lesen. Beachte, dass wir das Feld `seasonal_fruit` in
`eat_at_restaurant` nicht verwenden können, weil `seasonal_fruit` privat ist.
Versuch, die Zeile, die den Wert des Feldes `seasonal_fruit` ändert,
einzukommentieren, und sieh dir an, welchen Fehler du bekommst!

Beachte außerdem: Da `back_of_house::Breakfast` ein privates Feld hat, muss das
Struct eine öffentliche assoziierte Funktion bereitstellen, die eine Instanz von
`Breakfast` erzeugt (wir haben sie hier `summer` genannt). Hätte `Breakfast`
keine solche Funktion, könnten wir in `eat_at_restaurant` keine Instanz von
`Breakfast` erzeugen, weil wir den Wert des privaten Feldes `seasonal_fruit` in
`eat_at_restaurant` nicht setzen könnten.

Machen wir dagegen ein Enum öffentlich, sind anschließend alle seine Varianten
öffentlich. Wir brauchen das `pub` nur vor dem Schlüsselwort `enum`, wie in
Listing 7-10 gezeigt.

<Listing number="7-10" file-name="src/lib.rs" caption="Wird ein Enum als öffentlich gekennzeichnet, sind alle seine Varianten öffentlich.">

```rust,noplayground
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-10/src/lib.rs}}
```

</Listing>

Da wir das Enum `Appetizer` öffentlich gemacht haben, können wir die Varianten
`Soup` und `Salad` in `eat_at_restaurant` verwenden.

Enums sind nicht sehr nützlich, wenn ihre Varianten nicht öffentlich sind; es
wäre lästig, alle Enum-Varianten jedes Mal mit `pub` annotieren zu müssen, daher
sind Enum-Varianten standardmäßig öffentlich. Structs sind oft auch dann
nützlich, wenn ihre Felder nicht öffentlich sind, daher folgen Struct-Felder der
allgemeinen Regel, dass alles standardmäßig privat ist, sofern es nicht mit
`pub` annotiert ist.

Es gibt noch eine Situation mit `pub`, die wir nicht behandelt haben, und das
ist unser letztes Feature des Modulsystems: das Schlüsselwort `use`. Wir
behandeln zuerst `use` für sich allein und zeigen dann, wie man `pub` und `use`
kombiniert.

{{#quiz ../quizzes/ch07-03-paths-sec2.toml}}

[pub]: ch07-03-paths-for-referring-to-an-item-in-the-module-tree.html#exposing-paths-with-the-pub-keyword
[api-guidelines]: https://rust-lang.github.io/api-guidelines/
[ch12]: ch12-00-an-io-project.html
