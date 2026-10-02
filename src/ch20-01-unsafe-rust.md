## Unsafe Rust {#unsafe-rust}

Für den gesamten Code, den wir bisher besprochen haben, wurden die
Speichersicherheitsgarantien von Rust zur Kompilierzeit durchgesetzt. In Rust
verbirgt sich jedoch eine zweite Sprache, die diese Speichersicherheitsgarantien
nicht durchsetzt: Sie heißt _Unsafe Rust_ und funktioniert genau wie normales
Rust, verleiht uns aber zusätzliche Superkräfte.

Unsafe Rust gibt es, weil statische Analyse von Natur aus konservativ ist. Wenn
der Compiler zu bestimmen versucht, ob Code die Garantien einhält, ist es
besser, einige gültige Programme zurückzuweisen, als einige ungültige Programme
zu akzeptieren. Auch wenn der Code in Ordnung sein _könnte_, weist der
Rust-Compiler ihn zurück, wenn er nicht genug Informationen hat, um sicher zu
sein. In diesen Fällen kannst du unsicheren Code verwenden, um dem Compiler zu
sagen: „Vertrau mir, ich weiß, was ich tue.“ Sei aber gewarnt, dass du Unsafe
Rust auf eigenes Risiko verwendest: Wenn du unsicheren Code falsch verwendest,
können Probleme aufgrund von Speicherunsicherheit auftreten, etwa die
Dereferenzierung eines Nullzeigers.

Ein weiterer Grund, warum Rust ein unsicheres Alter Ego hat, ist, dass die
zugrunde liegende Computerhardware von Natur aus unsicher ist. Würde Rust dich
keine unsicheren Operationen ausführen lassen, könntest du bestimmte Aufgaben
nicht erledigen. Rust muss dir systemnahe Programmierung ermöglichen, etwa die
direkte Interaktion mit dem Betriebssystem oder sogar das Schreiben eines
eigenen Betriebssystems. Die Arbeit mit systemnaher Programmierung ist eines der
Ziele der Sprache. Sehen wir uns an, was wir mit Unsafe Rust tun können und wie
das geht.

<!-- Old headings. Do not remove or links may break. -->

<a id="unsafe-superpowers"></a>

### Unsichere Superkräfte einsetzen {#performing-unsafe-superpowers}

Um zu Unsafe Rust zu wechseln, verwendest du das Schlüsselwort `unsafe` und
beginnst dann einen neuen Block, der den unsicheren Code enthält. In Unsafe Rust
kannst du fünf Aktionen ausführen, die in sicherem Rust nicht möglich sind und
die wir _unsichere Superkräfte_ (_unsafe superpowers_) nennen. Zu diesen
Superkräften gehört die Fähigkeit,

1. einen Raw-Pointer zu dereferenzieren,
1. eine unsichere Funktion oder Methode aufzurufen,
1. auf eine veränderliche (_mutable_) statische Variable zuzugreifen oder sie zu
   verändern,
1. einen unsicheren Trait zu implementieren,
1. auf Felder von `union`s zuzugreifen.

Es ist wichtig zu verstehen, dass `unsafe` weder den Borrow-Checker abschaltet
noch irgendeine der anderen Sicherheitsprüfungen von Rust deaktiviert: Wenn du
in unsicherem Code eine Referenz verwendest, wird sie trotzdem geprüft. Das
Schlüsselwort `unsafe` gibt dir nur Zugriff auf diese fünf Features, die der
Compiler dann nicht auf Speichersicherheit prüft. Innerhalb eines unsicheren
Blocks hast du also immer noch ein gewisses Maß an Sicherheit.

Außerdem bedeutet `unsafe` nicht, dass der Code innerhalb des Blocks
zwangsläufig gefährlich ist oder auf jeden Fall Probleme mit der
Speichersicherheit haben wird: Die Absicht ist, dass du als Programmierer dafür
sorgst, dass der Code innerhalb eines `unsafe`-Blocks auf gültige Weise auf den
Speicher zugreift.

Menschen sind fehlbar, und Fehler werden passieren, aber weil diese fünf
unsicheren Operationen in Blöcken stehen müssen, die mit `unsafe` annotiert
sind, weißt du, dass alle Fehler im Zusammenhang mit der Speichersicherheit in
einem `unsafe`-Block liegen müssen. Halte `unsafe`-Blöcke klein; du wirst später
dankbar sein, wenn du Speicherfehler untersuchst.

Um unsicheren Code so weit wie möglich zu isolieren, ist es am besten, solchen
Code in eine sichere Abstraktion einzuschließen und eine sichere API
bereitzustellen; darauf gehen wir später im Kapitel ein, wenn wir unsichere
Funktionen und Methoden untersuchen. Teile der Standardbibliothek sind als
sichere Abstraktionen über geprüftem unsicherem Code implementiert. Unsicheren
Code in eine sichere Abstraktion zu hüllen, verhindert, dass sich Verwendungen
von `unsafe` an all die Stellen ausbreiten, an denen du oder deine Benutzer die
mit `unsafe`-Code implementierte Funktionalität verwenden möchten, weil die
Verwendung einer sicheren Abstraktion sicher ist.

Sehen wir uns die fünf unsicheren Superkräfte der Reihe nach an. Außerdem
betrachten wir einige Abstraktionen, die eine sichere Schnittstelle zu
unsicherem Code bereitstellen.

### Einen Raw-Pointer dereferenzieren {#dereferencing-a-raw-pointer}

Im Abschnitt
[„Der Borrow-Checker findet Berechtigungsverletzungen“][permission-violations]<!-- ignore -->
in Kapitel 4 haben wir beschrieben, wie der Compiler sicherstellt, dass
Referenzen immer gültig sind. Unsafe Rust hat zwei neue Typen namens
_Raw-Pointer_ (_raw pointers_), die Referenzen ähneln. Wie Referenzen können
Raw-Pointer unveränderlich (_immutable_) oder veränderlich (_mutable_) sein und
werden als `*const
T` bzw. `*mut T` geschrieben. Das Sternchen ist nicht der
Dereferenzierungsoperator, sondern Teil des Typnamens. Im Zusammenhang mit
Raw-Pointern bedeutet _unveränderlich_, dass dem Zeiger nach der
Dereferenzierung nicht direkt etwas zugewiesen werden kann.

Anders als Referenzen und Smart-Pointer

- dürfen Raw-Pointer die Borrowing-Regeln ignorieren, indem es sowohl
  unveränderliche als auch veränderliche Zeiger oder mehrere veränderliche
  Zeiger auf dieselbe Stelle gibt,
- ist nicht garantiert, dass Raw-Pointer auf gültigen Speicher zeigen,
- dürfen Raw-Pointer null sein,
- implementieren Raw-Pointer kein automatisches Aufräumen.

Indem du darauf verzichtest, dass Rust diese Garantien durchsetzt, kannst du
garantierte Sicherheit gegen höhere Performance eintauschen oder gegen die
Möglichkeit, mit einer anderen Sprache oder mit Hardware zu interagieren, für
die die Garantien von Rust nicht gelten.

Listing 20-1 zeigt, wie man einen unveränderlichen und einen veränderlichen
Raw-Pointer erzeugt.

<Listing number="20-1" caption="Raw-Pointer mit den Raw-Borrow-Operatoren erzeugen">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-01/src/main.rs:here}}
```

</Listing>

Beachte, dass wir das Schlüsselwort `unsafe` in diesem Code nicht verwenden. Wir
können Raw-Pointer in sicherem Code erzeugen; wir können Raw-Pointer nur nicht
außerhalb eines unsicheren Blocks dereferenzieren, wie du gleich sehen wirst.

Wir haben die Raw-Pointer mit den Raw-Borrow-Operatoren (_raw borrow operators_)
erzeugt: `&raw const num` erzeugt einen unveränderlichen Raw-Pointer vom Typ
`*const i32`, und `&raw mut num` erzeugt einen veränderlichen Raw-Pointer vom
Typ `*mut
i32`. Weil wir sie direkt aus einer lokalen Variablen erzeugt haben,
wissen wir, dass diese bestimmten Raw-Pointer gültig sind, aber diese Annahme
können wir nicht über jeden beliebigen Raw-Pointer treffen.

Um das zu demonstrieren, erzeugen wir als Nächstes einen Raw-Pointer, bei dessen
Gültigkeit wir uns nicht so sicher sein können, indem wir mit dem Schlüsselwort
`as` einen Wert umwandeln, statt den Raw-Borrow-Operator zu verwenden. Listing
20-2 zeigt, wie man einen Raw-Pointer auf eine beliebige Stelle im Speicher
erzeugt. Der Versuch, beliebigen Speicher zu verwenden, ist undefiniert: An
dieser Adresse könnten Daten liegen oder auch nicht, der Compiler könnte den
Code so optimieren, dass gar kein Speicherzugriff stattfindet, oder das Programm
könnte mit einem Segmentation Fault abbrechen. Normalerweise gibt es keinen
guten Grund, solchen Code zu schreiben, besonders in Fällen, in denen du
stattdessen einen Raw-Borrow-Operator verwenden kannst, aber es ist möglich.

<Listing number="20-2" caption="Einen Raw-Pointer auf eine beliebige Speicheradresse erzeugen">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-02/src/main.rs:here}}
```

</Listing>

Erinnere dich, dass wir Raw-Pointer in sicherem Code erzeugen können, sie aber
nicht dereferenzieren und die Daten lesen können, auf die sie zeigen. In Listing
20-3 verwenden wir den Dereferenzierungsoperator `*` auf einem Raw-Pointer, was
einen `unsafe`-Block erfordert.

<Listing number="20-3" caption="Raw-Pointer innerhalb eines `unsafe`-Blocks dereferenzieren">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-03/src/main.rs:here}}
```

</Listing>

Einen Zeiger zu erzeugen, richtet keinen Schaden an; erst wenn wir versuchen,
auf den Wert zuzugreifen, auf den er zeigt, könnten wir es mit einem ungültigen
Wert zu tun bekommen.

Beachte auch, dass wir in Listing 20-1 und 20-3 Raw-Pointer vom Typ `*const i32`
und `*mut
i32` erzeugt haben, die beide auf dieselbe Speicherstelle zeigten, an
der `num` gespeichert ist. Hätten wir stattdessen versucht, eine unveränderliche
und eine veränderliche Referenz auf `num` zu erzeugen, hätte der Code nicht
kompiliert, weil die Ownership-Regeln von Rust keine veränderliche Referenz
gleichzeitig mit unveränderlichen Referenzen erlauben. Mit Raw-Pointern können
wir einen veränderlichen und einen unveränderlichen Zeiger auf dieselbe Stelle
erzeugen und Daten über den veränderlichen Zeiger ändern, wodurch möglicherweise
ein Data-Race entsteht. Sei vorsichtig!

Warum solltest du bei all diesen Gefahren überhaupt Raw-Pointer verwenden? Ein
wichtiger Anwendungsfall ist die Interaktion mit C-Code, wie du im nächsten
Abschnitt sehen wirst. Ein anderer Fall ist der Aufbau sicherer Abstraktionen,
die der Borrow-Checker nicht versteht. Wir stellen unsichere Funktionen vor und
sehen uns dann ein Beispiel für eine sichere Abstraktion an, die unsicheren Code
verwendet.

### Eine unsichere Funktion oder Methode aufrufen {#calling-an-unsafe-function-or-method}

Die zweite Art von Operation, die du in einem unsicheren Block ausführen kannst,
ist der Aufruf unsicherer Funktionen. Unsichere Funktionen und Methoden sehen
genauso aus wie normale Funktionen und Methoden, haben aber vor dem Rest der
Definition ein zusätzliches `unsafe`. Das Schlüsselwort `unsafe` zeigt in diesem
Kontext an, dass die Funktion Anforderungen hat, die wir einhalten müssen, wenn
wir sie aufrufen, weil Rust nicht garantieren kann, dass wir diese Anforderungen
erfüllt haben. Indem wir eine unsichere Funktion innerhalb eines `unsafe`-Blocks
aufrufen, sagen wir, dass wir die Dokumentation dieser Funktion gelesen haben
und die Verantwortung dafür übernehmen, die Verträge der Funktion einzuhalten.

Hier ist eine unsichere Funktion namens `dangerous`, die in ihrem Rumpf nichts
tut:

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-01-unsafe-fn/src/main.rs:here}}
```

Wir müssen die Funktion `dangerous` innerhalb eines separaten `unsafe`-Blocks
aufrufen. Wenn wir versuchen, `dangerous` ohne den `unsafe`-Block aufzurufen,
bekommen wir einen Fehler:

```console
{{#include ../listings/ch20-advanced-features/output-only-01-missing-unsafe/output.txt}}
```

Mit dem `unsafe`-Block versichern wir Rust, dass wir die Dokumentation der
Funktion gelesen haben, verstehen, wie man sie richtig verwendet, und überprüft
haben, dass wir den Vertrag der Funktion erfüllen.

Um im Rumpf einer `unsafe`-Funktion unsichere Operationen auszuführen, musst du
weiterhin einen `unsafe`-Block verwenden, genau wie in einer normalen Funktion,
und der Compiler warnt dich, wenn du das vergisst. Das hilft uns,
`unsafe`-Blöcke so klein wie möglich zu halten, da unsichere Operationen
vielleicht nicht im ganzen Funktionsrumpf nötig sind.

#### Eine sichere Abstraktion über unsicherem Code erstellen {#creating-a-safe-abstraction-over-unsafe-code}

Nur weil eine Funktion unsicheren Code enthält, müssen wir nicht die ganze
Funktion als unsicher kennzeichnen. Tatsächlich ist es eine gängige Abstraktion,
unsicheren Code in eine sichere Funktion zu hüllen. Sehen wir uns als Beispiel
die Funktion `split_at_mut` aus der Standardbibliothek an, die etwas unsicheren
Code erfordert. Wir untersuchen, wie wir sie implementieren könnten. Diese
sichere Methode ist für veränderliche Slices definiert: Sie nimmt einen Slice
und macht zwei daraus, indem sie den Slice an dem als Argument übergebenen Index
teilt. Listing 20-4 zeigt, wie man `split_at_mut` verwendet.

<Listing number="20-4" caption="Die sichere Funktion `split_at_mut` verwenden">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-04/src/main.rs:here}}
```

</Listing>

Wir können diese Funktion nicht nur mit sicherem Rust implementieren. Ein
Versuch könnte ungefähr wie Listing 20-5 aussehen, das nicht kompiliert. Der
Einfachheit halber implementieren wir `split_at_mut` als Funktion statt als
Methode und nur für Slices von `i32`-Werten statt für einen generischen Typ `T`.

<Listing number="20-5" caption="Ein Versuch, `split_at_mut` nur mit sicherem Rust zu implementieren">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-05/src/main.rs:here}}
```

</Listing>

Diese Funktion ermittelt zuerst die Gesamtlänge des Slices. Dann sichert sie zu,
dass der als Parameter übergebene Index innerhalb des Slices liegt, indem sie
prüft, ob er kleiner oder gleich der Länge ist. Die Zusicherung bedeutet: Wenn
wir einen Index übergeben, der größer als die Länge ist, um den Slice daran zu
teilen, löst die Funktion einen Panic aus, bevor sie versucht, diesen Index zu
verwenden.

Dann geben wir zwei veränderliche Slices in einem Tupel zurück: einen vom Anfang
des ursprünglichen Slices bis zum Index `mid` und einen weiteren von `mid` bis
zum Ende des Slices.

Wenn wir versuchen, den Code in Listing 20-5 zu kompilieren, bekommen wir einen
Fehler:

```console
{{#include ../listings/ch20-advanced-features/listing-20-05/output.txt}}
```

Der Borrow-Checker von Rust kann nicht verstehen, dass wir verschiedene Teile
des Slices ausleihen (_borrowing_); er weiß nur, dass wir zweimal aus demselben
Slice ausleihen. Verschiedene Teile eines Slices auszuleihen, ist grundsätzlich
in Ordnung, weil sich die beiden Slices nicht überlappen, aber Rust ist nicht
schlau genug, um das zu wissen. Wenn wir wissen, dass Code in Ordnung ist, Rust
es aber nicht weiß, ist es Zeit, zu unsicherem Code zu greifen.

Listing 20-6 zeigt, wie man einen `unsafe`-Block, einen Raw-Pointer und einige
Aufrufe unsicherer Funktionen verwendet, damit die Implementierung von
`split_at_mut` funktioniert.

<Listing number="20-6" caption="Unsicheren Code in der Implementierung der Funktion `split_at_mut` verwenden">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-06/src/main.rs:here}}
```

</Listing>

Erinnere dich aus dem Abschnitt [„Der Slice-Typ“][the-slice-type]<!-- ignore -->
in Kapitel 4 daran, dass ein Slice ein Zeiger auf Daten und die Länge des Slices
ist. Wir verwenden die Methode `len`, um die Länge eines Slices zu erhalten, und
die Methode `as_mut_ptr`, um auf den Raw-Pointer eines Slices zuzugreifen. Weil
wir in diesem Fall einen veränderlichen Slice von `i32`-Werten haben, gibt
`as_mut_ptr` einen Raw-Pointer vom Typ `*mut i32` zurück, den wir in der
Variablen `ptr` gespeichert haben.

Wir behalten die Zusicherung bei, dass der Index `mid` innerhalb des Slices
liegt. Dann kommen wir zum unsicheren Code: Die Funktion
`slice::from_raw_parts_mut` nimmt einen Raw-Pointer und eine Länge und erzeugt
einen Slice. Wir verwenden diese Funktion, um einen Slice zu erzeugen, der bei
`ptr` beginnt und `mid` Elemente lang ist. Dann rufen wir die Methode `add` auf
`ptr` mit `mid` als Argument auf, um einen Raw-Pointer zu erhalten, der bei
`mid` beginnt, und wir erzeugen einen Slice mit diesem Zeiger und der Anzahl der
verbleibenden Elemente nach `mid` als Länge.

Die Funktion `slice::from_raw_parts_mut` ist unsicher, weil sie einen
Raw-Pointer nimmt und darauf vertrauen muss, dass dieser Zeiger gültig ist. Die
Methode `add` auf Raw-Pointern ist ebenfalls unsicher, weil sie darauf vertrauen
muss, dass die versetzte Stelle ebenfalls ein gültiger Zeiger ist. Daher mussten
wir einen `unsafe`-Block um unsere Aufrufe von `slice::from_raw_parts_mut` und
`add` setzen, damit wir sie aufrufen konnten. Wenn wir uns den Code ansehen und
die Zusicherung hinzufügen, dass `mid` kleiner oder gleich `len` sein muss,
können wir feststellen, dass alle innerhalb des `unsafe`-Blocks verwendeten
Raw-Pointer gültige Zeiger auf Daten innerhalb des Slices sind. Das ist eine
akzeptable und angemessene Verwendung von `unsafe`.

Beachte, dass wir die resultierende Funktion `split_at_mut` nicht als `unsafe`
kennzeichnen müssen und dass wir diese Funktion aus sicherem Rust aufrufen
können. Wir haben eine sichere Abstraktion über den unsicheren Code erstellt,
mit einer Implementierung der Funktion, die `unsafe`-Code auf sichere Weise
verwendet, weil sie nur gültige Zeiger aus den Daten erzeugt, auf die diese
Funktion Zugriff hat.

Im Gegensatz dazu würde die Verwendung von `slice::from_raw_parts_mut` in
Listing 20-7 wahrscheinlich abstürzen, wenn der Slice verwendet wird. Dieser
Code nimmt eine beliebige Speicherstelle und erzeugt einen Slice, der 10.000
Elemente lang ist.

<Listing number="20-7" caption="Einen Slice aus einer beliebigen Speicherstelle erzeugen">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-07/src/main.rs:here}}
```

</Listing>

Wir besitzen den Speicher an dieser beliebigen Stelle nicht, und es gibt keine
Garantie, dass der von diesem Code erzeugte Slice gültige `i32`-Werte enthält.
Der Versuch, `values` so zu verwenden, als wäre es ein gültiger Slice, führt zu
undefiniertem Verhalten.

#### `extern`-Funktionen verwenden, um externen Code aufzurufen {#using-extern-functions-to-call-external-code}

Manchmal muss dein Rust-Code mit Code interagieren, der in einer anderen Sprache
geschrieben ist. Dafür hat Rust das Schlüsselwort `extern`, das die Erstellung
und Verwendung eines _Foreign Function Interface (FFI)_ erleichtert. Das ist
eine Möglichkeit für eine Programmiersprache, Funktionen zu definieren und einer
anderen (fremden) Programmiersprache zu ermöglichen, diese Funktionen
aufzurufen.

Listing 20-8 zeigt, wie man eine Anbindung an die Funktion `abs` aus der
C-Standardbibliothek einrichtet. Funktionen, die innerhalb von `extern`-Blöcken
deklariert werden, sind aus Rust-Code im Allgemeinen unsicher aufzurufen, daher
müssen `extern`-Blöcke ebenfalls als `unsafe` gekennzeichnet werden. Der Grund
ist, dass andere Sprachen die Regeln und Garantien von Rust nicht durchsetzen
und Rust sie nicht prüfen kann, sodass die Verantwortung für die Sicherheit beim
Programmierer liegt.

<Listing number="20-8" file-name="src/main.rs" caption="Eine in einer anderen Sprache definierte `extern`-Funktion deklarieren und aufrufen">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-08/src/main.rs}}
```

</Listing>

Innerhalb des Blocks `unsafe extern "C"` listen wir die Namen und Signaturen der
externen Funktionen aus einer anderen Sprache auf, die wir aufrufen wollen. Der
Teil `"C"` legt fest, welches _Application Binary Interface (ABI)_ die externe
Funktion verwendet: Das ABI definiert, wie die Funktion auf Assembler-Ebene
aufgerufen wird. Das ABI `"C"` ist das gebräuchlichste und folgt dem ABI der
Programmiersprache C. Informationen über alle ABIs, die Rust unterstützt,
findest du in [der Rust-Referenz][ABI].

Jedes Element, das innerhalb eines `unsafe extern`-Blocks deklariert wird, ist
implizit unsicher. Manche FFI-Funktionen _sind_ jedoch sicher aufzurufen. Die
Funktion `abs` aus der C-Standardbibliothek hat zum Beispiel keine Auswirkungen
auf die Speichersicherheit, und wir wissen, dass sie mit jedem `i32` aufgerufen
werden kann. In solchen Fällen können wir mit dem Schlüsselwort `safe` sagen,
dass diese bestimmte Funktion sicher aufzurufen ist, obwohl sie in einem
`unsafe extern`-Block steht. Sobald wir diese Änderung vornehmen, erfordert ihr
Aufruf keinen `unsafe`-Block mehr, wie in Listing 20-9 gezeigt.

<Listing number="20-9" file-name="src/main.rs" caption="Eine Funktion innerhalb eines `unsafe extern`-Blocks ausdrücklich als `safe` kennzeichnen und sicher aufrufen">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-09/src/main.rs}}
```

</Listing>

Eine Funktion als `safe` zu kennzeichnen, macht sie nicht von sich aus sicher!
Es ist vielmehr ein Versprechen, das du Rust gibst, dass sie sicher ist. Es
bleibt deine Verantwortung, dafür zu sorgen, dass dieses Versprechen gehalten
wird!

#### Rust-Funktionen aus anderen Sprachen aufrufen {#calling-rust-functions-from-other-languages}

Wir können `extern` auch verwenden, um eine Schnittstelle zu erstellen, über die
andere Sprachen Rust-Funktionen aufrufen können. Statt einen ganzen
`extern`-Block zu erstellen, fügen wir das Schlüsselwort `extern` hinzu und
geben das zu verwendende ABI direkt vor dem Schlüsselwort `fn` der betreffenden
Funktion an. Außerdem müssen wir eine Annotation `#[unsafe(no_mangle)]`
hinzufügen, um dem Rust-Compiler mitzuteilen, dass er den Namen dieser Funktion
nicht verändern (_mangle_) soll. _Mangling_ bedeutet, dass ein Compiler den
Namen, den wir einer Funktion gegeben haben, in einen anderen Namen ändert, der
mehr Informationen für andere Teile des Kompiliervorgangs enthält, aber für
Menschen schlechter lesbar ist. Der Compiler jeder Programmiersprache verändert
Namen auf etwas andere Weise, damit also eine Rust-Funktion von anderen Sprachen
aus benannt werden kann, müssen wir das Name Mangling des Rust-Compilers
abschalten. Das ist unsicher, weil es ohne das eingebaute Mangling zu
Namenskollisionen zwischen Bibliotheken kommen kann, daher liegt es in unserer
Verantwortung sicherzustellen, dass der gewählte Name ohne Mangling sicher
exportiert werden kann.

Im folgenden Beispiel machen wir die Funktion `call_from_c` für C-Code
zugänglich, nachdem sie zu einer gemeinsam genutzten Bibliothek kompiliert und
von C aus gelinkt wurde:

```
#[unsafe(no_mangle)]
pub extern "C" fn call_from_c() {
    println!("Just called a Rust function from C!");
}
```

Diese Verwendung von `extern` erfordert `unsafe` nur im Attribut, nicht beim
`extern`-Block.

### Auf eine veränderliche statische Variable zugreifen oder sie verändern {#accessing-or-modifying-a-mutable-static-variable}

In diesem Buch haben wir noch nicht über globale Variablen gesprochen, die Rust
zwar unterstützt, die aber mit den Ownership-Regeln von Rust problematisch sein
können. Wenn zwei Threads auf dieselbe veränderliche globale Variable zugreifen,
kann das ein Data-Race verursachen.

In Rust heißen globale Variablen _statische_ Variablen. Listing 20-10 zeigt ein
Beispiel für die Deklaration und Verwendung einer statischen Variablen mit einem
String-Slice als Wert.

<Listing number="20-10" file-name="src/main.rs" caption="Eine unveränderliche statische Variable definieren und verwenden">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-10/src/main.rs}}
```

</Listing>

Statische Variablen ähneln Konstanten, die wir im Abschnitt
[„Konstanten deklarieren“][constants]<!-- ignore --> in Kapitel 3 besprochen
haben. Die Namen statischer Variablen werden gemäß Konvention in
`SCREAMING_SNAKE_CASE` geschrieben. Statische Variablen können nur Referenzen
mit der Lifetime `'static` speichern, was bedeutet, dass der Rust-Compiler die
Lifetime herausfinden kann und wir sie nicht explizit annotieren müssen. Der
Zugriff auf eine unveränderliche statische Variable ist sicher.

Ein feiner Unterschied zwischen Konstanten und unveränderlichen statischen
Variablen ist, dass Werte in einer statischen Variablen eine feste Adresse im
Speicher haben. Die Verwendung des Werts greift immer auf dieselben Daten zu.
Konstanten dürfen ihre Daten dagegen bei jeder Verwendung duplizieren. Ein
weiterer Unterschied ist, dass statische Variablen veränderlich sein können. Der
Zugriff auf veränderliche statische Variablen und ihre Veränderung ist
_unsicher_. Listing 20-11 zeigt, wie man eine veränderliche statische Variable
namens `COUNTER` deklariert, auf sie zugreift und sie verändert.

<Listing number="20-11" file-name="src/main.rs" caption="Das Lesen aus oder Schreiben in eine veränderliche statische Variable ist unsicher.">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-11/src/main.rs}}
```

</Listing>

Wie bei normalen Variablen geben wir die Veränderlichkeit mit dem Schlüsselwort
`mut` an. Jeder Code, der aus `COUNTER` liest oder hineinschreibt, muss
innerhalb eines `unsafe`-Blocks stehen. Der Code in Listing 20-11 kompiliert und
gibt wie erwartet `COUNTER: 3` aus, weil er nur einen Thread hat. Würden mehrere
Threads auf `COUNTER` zugreifen, käme es wahrscheinlich zu Data-Races, daher ist
das undefiniertes Verhalten. Deshalb müssen wir die ganze Funktion als `unsafe`
kennzeichnen und die Sicherheitseinschränkung dokumentieren, damit jeder, der
die Funktion aufruft, weiß, was er sicher tun darf und was nicht.

Wann immer wir eine unsichere Funktion schreiben, ist es idiomatisch, einen
Kommentar zu schreiben, der mit `SAFETY` beginnt und erklärt, was der Aufrufer
tun muss, um die Funktion sicher aufzurufen. Ebenso ist es idiomatisch, bei
jeder unsicheren Operation einen Kommentar zu schreiben, der mit `SAFETY`
beginnt und erklärt, wie die Sicherheitsregeln eingehalten werden.

Außerdem verbietet der Compiler standardmäßig über einen Compiler-Lint jeden
Versuch, Referenzen auf eine veränderliche statische Variable zu erzeugen. Du
musst entweder ausdrücklich auf den Schutz dieses Lints verzichten, indem du
eine Annotation `#[allow(static_mut_refs)]` hinzufügst, oder über einen
Raw-Pointer, der mit einem der Raw-Borrow-Operatoren erzeugt wurde, auf die
veränderliche statische Variable zugreifen. Das schließt Fälle ein, in denen die
Referenz unsichtbar erzeugt wird, etwa wenn sie im `println!` in diesem
Codelisting verwendet wird. Die Anforderung, dass Referenzen auf veränderliche
statische Variablen über Raw-Pointer erzeugt werden müssen, macht die
Sicherheitsanforderungen für ihre Verwendung deutlicher.

Bei veränderlichen Daten, auf die global zugegriffen werden kann, ist es schwer
sicherzustellen, dass es keine Data-Races gibt, weshalb Rust veränderliche
statische Variablen als unsicher betrachtet. Wo möglich, sind die
Nebenläufigkeitstechniken und threadsicheren Smart-Pointer vorzuziehen, die wir
in Kapitel 16 besprochen haben, damit der Compiler prüft, dass Datenzugriffe aus
verschiedenen Threads sicher erfolgen.

### Einen unsicheren Trait implementieren {#implementing-an-unsafe-trait}

Wir können `unsafe` verwenden, um einen unsicheren Trait zu implementieren. Ein
Trait ist unsicher, wenn mindestens eine seiner Methoden eine Invariante hat,
die der Compiler nicht überprüfen kann. Wir deklarieren einen Trait als
`unsafe`, indem wir das Schlüsselwort `unsafe` vor `trait` setzen und auch die
Implementierung des Traits als `unsafe` kennzeichnen, wie in Listing 20-12
gezeigt.

<Listing number="20-12" caption="Einen unsicheren Trait definieren und implementieren">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-12/src/main.rs:here}}
```

</Listing>

Mit `unsafe impl` versprechen wir, dass wir die Invarianten einhalten, die der
Compiler nicht überprüfen kann.

Erinnere dich als Beispiel an die Marker-Traits `Send` und `Sync`, die wir im
Abschnitt
[„Erweiterbare Nebenläufigkeit mit `Send` und `Sync`“][send-and-sync]<!-- ignore -->
in Kapitel 16 besprochen haben: Der Compiler implementiert diese Traits
automatisch, wenn unsere Typen vollständig aus anderen Typen bestehen, die
`Send` und `Sync` implementieren. Wenn wir einen Typ implementieren, der einen
Typ enthält, der `Send` oder `Sync` nicht implementiert, etwa Raw-Pointer, und
wir diesen Typ als `Send` oder `Sync` kennzeichnen wollen, müssen wir `unsafe`
verwenden. Rust kann nicht überprüfen, ob unser Typ die Garantien einhält, dass
er sicher zwischen Threads gesendet oder aus mehreren Threads verwendet werden
kann; daher müssen wir diese Prüfungen manuell durchführen und das mit `unsafe`
kenntlich machen.

### Auf Felder einer Union zugreifen {#accessing-fields-of-a-union}

Die letzte Aktion, die nur mit `unsafe` funktioniert, ist der Zugriff auf Felder
einer Union. Eine _Union_ ähnelt einem `struct`, aber in einer bestimmten
Instanz wird jeweils nur ein deklariertes Feld verwendet. Unions werden vor
allem für die Anbindung an Unions in C-Code verwendet. Der Zugriff auf Felder
einer Union ist unsicher, weil Rust den Typ der Daten, die gerade in der
Union-Instanz gespeichert sind, nicht garantieren kann. Mehr über Unions
erfährst du in [der Rust-Referenz][unions].

### Miri verwenden, um unsicheren Code zu prüfen {#using-miri-to-check-unsafe-code}

Wenn du unsicheren Code schreibst, möchtest du vielleicht prüfen, ob das, was du
geschrieben hast, tatsächlich sicher und korrekt ist. Eine der besten
Möglichkeiten dafür ist Miri, ein offizielles Rust-Werkzeug zum Erkennen von
undefiniertem Verhalten. Während der Borrow-Checker ein _statisches_ Werkzeug
ist, das zur Kompilierzeit arbeitet, ist Miri ein _dynamisches_ Werkzeug, das
zur Laufzeit arbeitet. Es prüft deinen Code, indem es dein Programm oder seine
Testsuite ausführt und erkennt, wenn du die Regeln verletzt, die es darüber
kennt, wie Rust funktionieren soll.

Für Miri brauchst du einen Nightly-Build von Rust (worüber wir in
[Anhang G: Wie Rust entsteht und „Nightly Rust“][nightly]<!-- ignore --> mehr
sprechen). Du kannst sowohl eine Nightly-Version von Rust als auch das Werkzeug
Miri installieren, indem du `rustup
+nightly component add miri` eingibst. Das
ändert nicht, welche Rust-Version dein Projekt verwendet; es fügt deinem System
nur das Werkzeug hinzu, damit du es verwenden kannst, wenn du möchtest. Du
kannst Miri auf ein Projekt anwenden, indem du `cargo +nightly miri run` oder
`cargo +nightly miri test` eingibst.

Ein Beispiel dafür, wie hilfreich das sein kann: Betrachte, was passiert, wenn
wir Miri auf Listing 20-7 anwenden.

```console
{{#include ../listings/ch20-advanced-features/listing-20-07/output.txt}}
```

Miri warnt uns zu Recht, dass wir eine Ganzzahl in einen Zeiger umwandeln, was
ein Problem sein könnte, aber Miri kann nicht feststellen, ob ein Problem
besteht, weil es nicht weiß, woher der Zeiger stammt. Dann gibt Miri einen
Fehler an der Stelle aus, an der Listing 20-7 undefiniertes Verhalten hat, weil
wir einen hängenden Zeiger (_dangling pointer_) haben. Dank Miri wissen wir
jetzt, dass das Risiko undefinierten Verhaltens besteht, und können darüber
nachdenken, wie wir den Code sicher machen. In manchen Fällen kann Miri sogar
Empfehlungen geben, wie sich Fehler beheben lassen.

Miri findet nicht alles, was du beim Schreiben von unsicherem Code falsch machen
kannst. Miri ist ein Werkzeug zur dynamischen Analyse, daher findet es nur
Probleme in Code, der tatsächlich ausgeführt wird. Das bedeutet, dass du es in
Verbindung mit guten Testtechniken verwenden musst, um dein Vertrauen in den
unsicheren Code, den du geschrieben hast, zu stärken. Miri deckt außerdem nicht
jede mögliche Art ab, auf die dein Code unsound (fehlerhaft) sein kann.

Anders ausgedrückt: Wenn Miri ein Problem _findet_, weißt du, dass es einen Bug
gibt, aber nur weil Miri einen Bug _nicht_ findet, heißt das nicht, dass es kein
Problem gibt. Es kann aber eine Menge finden. Probiere es mit den anderen
Beispielen für unsicheren Code in diesem Kapitel aus und sieh dir an, was es
meldet!

Mehr über Miri erfährst du in [seinem GitHub-Repository][miri].

<!-- Old headings. Do not remove or links may break. -->

<a id="when-to-use-unsafe-code"></a>

### Unsicheren Code richtig verwenden {#using-unsafe-code-correctly}

`unsafe` zu verwenden, um eine der fünf eben besprochenen Superkräfte zu nutzen,
ist weder falsch noch verpönt, aber es ist kniffliger, `unsafe`-Code korrekt zu
schreiben, weil der Compiler nicht dabei helfen kann, die Speichersicherheit
einzuhalten. Wenn du einen Grund hast, `unsafe`-Code zu verwenden, kannst du das
tun, und die ausdrückliche Annotation `unsafe` macht es leichter, die Ursache
von Problemen aufzuspüren, wenn sie auftreten. Wann immer du unsicheren Code
schreibst, kannst du Miri verwenden, um sicherer zu sein, dass der Code, den du
geschrieben hast, die Regeln von Rust einhält.

Für eine viel tiefere Auseinandersetzung damit, wie man effektiv mit Unsafe Rust
arbeitet, lies den offiziellen Leitfaden von Rust zu `unsafe`,
[The Rustonomicon][nomicon].

{{#quiz ../quizzes/ch19-01-unsafe-rust.toml}}

[permission-violations]: ch04-02-references-and-borrowing.html#the-borrow-checker-finds-permission-violations
[ABI]: https://doc.rust-lang.org/reference/items/external-blocks.html#abi
[the-slice-type]: ch04-04-slices.html#the-slice-type
[constants]: ch03-01-variables-and-mutability.html#declaring-constants
[send-and-sync]: ch16-04-extensible-concurrency-sync-and-send.html
[the-slice-type]: ch04-03-slices.html#the-slice-type
[unions]: https://doc.rust-lang.org/reference/items/unions.html
[miri]: https://github.com/rust-lang/miri
[editions]: appendix-05-editions.html
[nightly]: appendix-07-nightly-rust.html
[nomicon]: https://doc.rust-lang.org/nomicon/
