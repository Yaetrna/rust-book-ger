## Fortgeschrittene Typen {#advanced-types}

Das Typsystem von Rust hat einige Features, die wir bisher erwähnt, aber noch
nicht besprochen haben. Wir beginnen mit Newtypes im Allgemeinen und
untersuchen, warum sie als Typen nützlich sind. Dann gehen wir zu Typaliassen
über, einem Feature, das Newtypes ähnelt, aber eine etwas andere Semantik hat.
Außerdem besprechen wir den Typ `!` und Typen mit dynamischer Größe.

<!-- Old headings. Do not remove or links may break. -->

<a id="using-the-newtype-pattern-for-type-safety-and-abstraction"></a>

### Typsicherheit und Abstraktion mit dem Newtype-Pattern {#type-safety-and-abstraction-with-the-newtype-pattern}

Dieser Abschnitt setzt voraus, dass du den früheren Abschnitt
[„Externe Traits
mit dem Newtype-Pattern implementieren“][newtype]<!-- ignore --> gelesen hast.
Das Newtype-Pattern ist auch für Aufgaben nützlich, die über die bisher
besprochenen hinausgehen, etwa um statisch sicherzustellen, dass Werte nie
verwechselt werden, und um die Einheiten eines Werts anzugeben. Ein Beispiel für
die Verwendung von Newtypes zur Angabe von Einheiten hast du in Listing 20-16
gesehen: Erinnere dich, dass die Structs `Millimeters` und `Meters` `u32`-Werte
in einen Newtype gehüllt haben. Würden wir eine Funktion mit einem Parameter vom
Typ `Millimeters` schreiben, könnten wir kein Programm kompilieren, das
versehentlich versucht, diese Funktion mit einem Wert vom Typ `Meters` oder
einem einfachen `u32` aufzurufen.

Wir können das Newtype-Pattern auch verwenden, um einige Implementierungsdetails
eines Typs zu abstrahieren: Der neue Typ kann eine öffentliche API
bereitstellen, die sich von der API des privaten inneren Typs unterscheidet.

Newtypes können auch die interne Implementierung verbergen. Wir könnten zum
Beispiel einen Typ `People` bereitstellen, der eine `HashMap<i32, String>`
umhüllt, die die ID einer Person zusammen mit ihrem Namen speichert. Code, der
`People` verwendet, würde nur mit der öffentlichen API interagieren, die wir
bereitstellen, etwa einer Methode, um der Collection `People` einen Namen als
String hinzuzufügen; dieser Code müsste nicht wissen, dass wir Namen intern eine
`i32`-ID zuweisen. Das Newtype-Pattern ist eine leichtgewichtige Möglichkeit,
Kapselung zu erreichen, um Implementierungsdetails zu verbergen, was wir im
Abschnitt
[„Kapselung, die Implementierungsdetails
verbirgt“][encapsulation-that-hides-implementation-details]<!-- ignore --> in
Kapitel 18 besprochen haben.

<!-- Old headings. Do not remove or links may break. -->

<a id="creating-type-synonyms-with-type-aliases"></a>

### Typsynonyme und Typaliasse {#type-synonyms-and-type-aliases}

Rust bietet die Möglichkeit, einen _Typalias_ (_type alias_) zu deklarieren, um
einem bestehenden Typ einen anderen Namen zu geben. Dafür verwenden wir das
Schlüsselwort `type`. Wir können zum Beispiel den Alias `Kilometers` für `i32`
so erstellen:

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-04-kilometers-alias/src/main.rs:here}}
```

Jetzt ist der Alias `Kilometers` ein _Synonym_ für `i32`; anders als die Typen
`Millimeters` und `Meters`, die wir in Listing 20-16 erstellt haben, ist
`Kilometers` kein separater, neuer Typ. Werte vom Typ `Kilometers` werden
genauso behandelt wie Werte vom Typ `i32`:

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-04-kilometers-alias/src/main.rs:there}}
```

Weil `Kilometers` und `i32` derselbe Typ sind, können wir Werte beider Typen
addieren und `Kilometers`-Werte an Funktionen übergeben, die `i32`-Parameter
nehmen. Mit dieser Methode bekommen wir jedoch nicht die Vorteile der
Typprüfung, die uns das zuvor besprochene Newtype-Pattern bietet. Mit anderen
Worten: Wenn wir irgendwo `Kilometers`- und `i32`-Werte verwechseln, gibt uns
der Compiler keinen Fehler.

Der Hauptanwendungsfall für Typsynonyme ist, Wiederholungen zu reduzieren. Wir
könnten zum Beispiel einen langen Typ wie diesen haben:

```rust,ignore
Box<dyn Fn() + Send + 'static>
```

Diesen langen Typ überall im Code in Funktionssignaturen und als Typannotation
zu schreiben, kann ermüdend und fehleranfällig sein. Stell dir ein Projekt vor,
das voller Code wie in Listing 20-25 ist.

<Listing number="20-25" caption="Einen langen Typ an vielen Stellen verwenden">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-25/src/main.rs:here}}
```

</Listing>

Ein Typalias macht diesen Code handhabbarer, indem er die Wiederholung
reduziert. In Listing 20-26 haben wir für den langen Typ einen Alias namens
`Thunk` eingeführt und können alle Verwendungen des Typs durch den kürzeren
Alias `Thunk` ersetzen.

<Listing number="20-26" caption="Einen Typalias `Thunk` einführen, um Wiederholungen zu reduzieren">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-26/src/main.rs:here}}
```

</Listing>

Dieser Code ist viel leichter zu lesen und zu schreiben! Ein aussagekräftiger
Name für einen Typalias kann auch helfen, deine Absicht zu vermitteln (_Thunk_
ist ein Wort für Code, der zu einem späteren Zeitpunkt ausgewertet wird, daher
ist es ein passender Name für eine Closure, die gespeichert wird).

Typaliasse werden auch häufig mit dem Typ `Result<T, E>` verwendet, um
Wiederholungen zu reduzieren. Betrachte das Modul `std::io` in der
Standardbibliothek. I/O-Operationen geben oft ein `Result<T, E>` zurück, um
Situationen zu behandeln, in denen Operationen fehlschlagen. Diese Bibliothek
hat ein Struct `std::io::Error`, das alle möglichen I/O-Fehler darstellt. Viele
der Funktionen in `std::io` geben `Result<T, E>` zurück, wobei `E`
`std::io::Error` ist, etwa diese Funktionen im Trait `Write`:

```rust,noplayground
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-05-write-trait/src/lib.rs}}
```

Das `Result<..., Error>` wiederholt sich oft. Deshalb hat `std::io` diese
Deklaration eines Typalias:

```rust,noplayground
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-06-result-alias/src/lib.rs:here}}
```

Weil diese Deklaration im Modul `std::io` steht, können wir den vollständig
qualifizierten Alias `std::io::Result<T>` verwenden, also ein `Result<T, E>`,
bei dem `E` mit `std::io::Error` ausgefüllt ist. Die Funktionssignaturen des
Traits `Write` sehen dann so aus:

```rust,noplayground
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-06-result-alias/src/lib.rs:there}}
```

Der Typalias hilft auf zweierlei Weise: Er macht Code leichter zu schreiben,
_und_ er gibt uns eine einheitliche Schnittstelle in ganz `std::io`. Weil er ein
Alias ist, ist er nur ein weiteres `Result<T, E>`, was bedeutet, dass wir alle
Methoden, die mit `Result<T, E>` funktionieren, auch damit verwenden können,
ebenso wie spezielle Syntax wie den Operator `?`.

### Der Never-Typ, der nie zurückkehrt {#the-never-type-that-never-returns}

Rust hat einen speziellen Typ namens `!`, der im Jargon der Typtheorie als
_leerer Typ_ (_empty type_) bekannt ist, weil er keine Werte hat. Wir nennen ihn
lieber den _Never-Typ_ (_never type_), weil er an der Stelle des Rückgabetyps
steht, wenn eine Funktion nie zurückkehrt. Hier ist ein Beispiel:

```rust,noplayground
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-07-never-type/src/lib.rs:here}}
```

Dieser Code wird gelesen als „die Funktion `bar` kehrt nie zurück“ (wörtlich:
„gibt never zurück“). Funktionen, die nie zurückkehren, heißen _divergierende
Funktionen_ (_diverging functions_). Wir können keine Werte vom Typ `!`
erzeugen, daher kann `bar` unmöglich jemals zurückkehren.

Aber wozu dient ein Typ, für den man nie Werte erzeugen kann? Erinnere dich an
den Code aus Listing 2-5, einem Teil des Zahlenratespiels; einen Ausschnitt
davon haben wir hier in Listing 20-27 wiedergegeben.

<Listing number="20-27" caption="Ein `match` mit einem Arm, der mit `continue` endet">

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/listing-02-05/src/main.rs:ch19}}
```

</Listing>

Damals haben wir einige Details in diesem Code übersprungen. Im Abschnitt
[„Das Kontrollflusskonstrukt `match`“][the-match-control-flow-construct]<!-- ignore -->
in Kapitel 6 haben wir besprochen, dass alle `match`-Arme denselben Typ
zurückgeben müssen. Der folgende Code funktioniert also zum Beispiel nicht:

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-08-match-arms-different-types/src/main.rs:here}}
```

Der Typ von `guess` müsste in diesem Code eine Ganzzahl _und_ ein String sein,
und Rust verlangt, dass `guess` nur einen einzigen Typ hat. Was gibt `continue`
also zurück? Wie konnten wir in Listing 20-27 aus einem Arm ein `u32`
zurückgeben und einen anderen Arm haben, der mit `continue` endet?

Wie du vielleicht schon vermutet hast, hat `continue` einen `!`-Wert. Das heißt,
wenn Rust den Typ von `guess` berechnet, betrachtet es beide Match-Arme, den
ersten mit einem Wert vom Typ `u32` und den zweiten mit einem `!`-Wert. Weil `!`
nie einen Wert haben kann, entscheidet Rust, dass der Typ von `guess` `u32` ist.

Formal beschreibt man dieses Verhalten so, dass Ausdrücke vom Typ `!` in jeden
anderen Typ umgewandelt (_coerced_) werden können. Wir dürfen diesen `match`-Arm
mit `continue` beenden, weil `continue` keinen Wert zurückgibt; stattdessen gibt
es die Kontrolle an den Anfang der Schleife zurück, sodass wir im Fall `Err`
`guess` nie einen Wert zuweisen.

Der Never-Typ ist auch mit dem Makro `panic!` nützlich. Erinnere dich an die
Funktion `unwrap`, die wir auf `Option<T>`-Werten aufrufen, um einen Wert zu
erhalten oder einen Panic auszulösen, mit dieser Definition:

```rust,ignore
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-09-unwrap-definition/src/lib.rs:here}}
```

In diesem Code passiert dasselbe wie im `match` in Listing 20-27: Rust sieht,
dass `val` den Typ `T` und `panic!` den Typ `!` hat, also ist das Ergebnis des
gesamten `match`-Ausdrucks `T`. Dieser Code funktioniert, weil `panic!` keinen
Wert erzeugt, sondern das Programm beendet. Im Fall `None` geben wir aus
`unwrap` keinen Wert zurück, daher ist dieser Code gültig.

Ein letzter Ausdruck, der den Typ `!` hat, ist eine Schleife:

```rust,ignore
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-10-loop-returns-never/src/main.rs:here}}
```

Hier endet die Schleife nie, also ist `!` der Wert des Ausdrucks. Das wäre
jedoch nicht der Fall, wenn wir ein `break` einfügen würden, weil die Schleife
enden würde, sobald sie das `break` erreicht.

### Typen mit dynamischer Größe und der Trait `Sized` {#dynamically-sized-types-and-the-sized-trait}

Rust muss bestimmte Details über seine Typen kennen, etwa wie viel Speicherplatz
für einen Wert eines bestimmten Typs zu allozieren ist. Dadurch ist eine Ecke
seines Typsystems anfangs etwas verwirrend: das Konzept der _Typen mit
dynamischer Größe_ (_dynamically sized types_). Diese Typen, die manchmal als
_DSTs_ oder _Typen ohne Größe_ (_unsized types_) bezeichnet werden, ermöglichen
es uns, Code mit Werten zu schreiben, deren Größe wir erst zur Laufzeit kennen
können.

Sehen wir uns die Details eines Typs mit dynamischer Größe namens `str` an, den
wir im ganzen Buch verwendet haben. Richtig, nicht `&str`, sondern `str` für
sich allein ist ein DST. In vielen Fällen, etwa beim Speichern von Text, den ein
Benutzer eingegeben hat, können wir erst zur Laufzeit wissen, wie lang der
String ist. Das bedeutet, dass wir weder eine Variable vom Typ `str` erzeugen
noch ein Argument vom Typ `str` entgegennehmen können. Betrachte den folgenden
Code, der nicht funktioniert:

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-11-cant-create-str/src/main.rs:here}}
```

Rust muss wissen, wie viel Speicher für jeden Wert eines bestimmten Typs zu
allozieren ist, und alle Werte eines Typs müssen dieselbe Menge Speicher
belegen. Würde Rust uns erlauben, diesen Code zu schreiben, müssten diese beiden
`str`-Werte gleich viel Platz einnehmen. Sie haben aber unterschiedliche Längen:
`s1` braucht 12 Bytes Speicher und `s2` 15. Deshalb ist es nicht möglich, eine
Variable zu erzeugen, die einen Typ mit dynamischer Größe enthält.

Was tun wir also? In diesem Fall kennst du die Antwort schon: Wir geben `s1` und
`s2` den Typ String-Slice (`&str`) statt `str`. Erinnere dich aus dem Abschnitt
[„String-Slices“][string-slices]<!-- ignore --> in Kapitel 4, dass die
Datenstruktur eines Slices nur die Startposition und die Länge des Slices
speichert. Während `&T` also ein einzelner Wert ist, der die Speicheradresse
speichert, an der sich das `T` befindet, besteht ein String-Slice aus _zwei_
Werten: der Adresse des `str` und seiner Länge. Daher können wir die Größe eines
String-Slice-Werts zur Kompilierzeit kennen: Sie ist doppelt so groß wie ein
`usize`. Das heißt, wir kennen die Größe eines String-Slices immer, egal wie
lang der String ist, auf den er verweist. Im Allgemeinen werden Typen mit
dynamischer Größe in Rust auf diese Weise verwendet: Sie haben zusätzliche
Metadaten, die die Größe der dynamischen Information speichern. Die goldene
Regel für Typen mit dynamischer Größe lautet, dass wir Werte solcher Typen immer
hinter eine Art Zeiger legen müssen.

Wir können `str` mit allen möglichen Zeigern kombinieren, zum Beispiel
`Box<str>` oder `Rc<str>`. Tatsächlich hast du das schon gesehen, aber mit einem
anderen Typ mit dynamischer Größe: Traits. Jeder Trait ist ein Typ mit
dynamischer Größe, auf den wir über den Namen des Traits verweisen können. Im
Abschnitt
[„Mit Trait-Objekten über gemeinsames Verhalten
abstrahieren“][using-trait-objects-to-abstract-over-shared-behavior]<!--
ignore --> in Kapitel 18 haben wir erwähnt, dass wir Traits, um sie als
Trait-Objekte zu verwenden, hinter einen Zeiger legen müssen, etwa `&dyn Trait`
oder `Box<dyn
Trait>` (`Rc<dyn Trait>` würde auch funktionieren).

Um mit DSTs zu arbeiten, stellt Rust den Trait `Sized` bereit, mit dem bestimmt
wird, ob die Größe eines Typs zur Kompilierzeit bekannt ist oder nicht. Dieser
Trait ist automatisch für alles implementiert, dessen Größe zur Kompilierzeit
bekannt ist. Außerdem fügt Rust jeder generischen Funktion implizit einen Bound
auf `Sized` hinzu. Das heißt, eine generische Funktionsdefinition wie diese:

```rust,ignore
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-12-generic-fn-definition/src/lib.rs}}
```

wird tatsächlich so behandelt, als hätten wir Folgendes geschrieben:

```rust,ignore
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-13-generic-implicit-sized-bound/src/lib.rs}}
```

Standardmäßig funktionieren generische Funktionen nur mit Typen, deren Größe zur
Kompilierzeit bekannt ist. Mit der folgenden speziellen Syntax kannst du diese
Einschränkung jedoch lockern:

```rust,ignore
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-14-generic-maybe-sized/src/lib.rs}}
```

Ein Trait-Bound auf `?Sized` bedeutet: „`T` kann `Sized` sein oder auch nicht.“
Diese Notation überschreibt den Standard, dass generische Typen zur
Kompilierzeit eine bekannte Größe haben müssen. Die Syntax `?Trait` mit dieser
Bedeutung gibt es nur für `Sized`, nicht für andere Traits.

Beachte auch, dass wir den Typ des Parameters `t` von `T` in `&T` geändert
haben. Weil der Typ möglicherweise nicht `Sized` ist, müssen wir ihn hinter
einer Art Zeiger verwenden. In diesem Fall haben wir eine Referenz gewählt.

Als Nächstes sprechen wir über Funktionen und Closures!

{{#quiz ../quizzes/ch19-04-advanced-types.toml}}

[encapsulation-that-hides-implementation-details]: ch18-01-what-is-oo.html#encapsulation-that-hides-implementation-details
[string-slices]: ch04-04-slices.html#string-slices
[the-match-control-flow-construct]: ch06-02-match.html#the-match-control-flow-construct
[using-trait-objects-to-abstract-over-shared-behavior]: ch18-02-trait-objects.html#using-trait-objects-to-abstract-over-shared-behavior
[newtype]: ch20-02-advanced-traits.html#implementing-external-traits-with-the-newtype-pattern
