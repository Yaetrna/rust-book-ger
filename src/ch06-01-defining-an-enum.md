## Ein Enum definieren {#defining-an-enum}

Während Structs dir eine Möglichkeit geben, zusammengehörige Felder und Daten zu
gruppieren, wie ein `Rectangle` mit seiner `width` und `height`, geben dir Enums
eine Möglichkeit auszudrücken, dass ein Wert einer aus einer Menge möglicher
Werte ist. Wir möchten zum Beispiel sagen, dass `Rectangle` eine aus einer Menge
möglicher Formen ist, zu der auch `Circle` und `Triangle` gehören. Dafür lässt
uns Rust diese Möglichkeiten als Enum kodieren.

Sehen wir uns eine Situation an, die wir in Code ausdrücken möchten, und warum
Enums in diesem Fall nützlich und besser geeignet sind als Structs. Angenommen,
wir müssen mit IP-Adressen arbeiten. Derzeit werden zwei wichtige Standards für
IP-Adressen verwendet: Version vier und Version sechs. Weil das die einzigen
Möglichkeiten für IP-Adressen sind, auf die unser Programm stoßen wird, können
wir alle möglichen Varianten _aufzählen_ (_enumerate_); daher hat die
Enumeration ihren Namen.

Jede IP-Adresse kann entweder eine Adresse der Version vier oder der Version
sechs sein, aber nicht beides gleichzeitig. Diese Besonderheit von IP-Adressen
macht die Datenstruktur Enum passend, weil ein Enum-Wert nur eine seiner
Varianten sein kann. Adressen der Version vier und der Version sechs sind im
Grunde trotzdem beides IP-Adressen, daher sollten sie als derselbe Typ behandelt
werden, wenn der Code Situationen verarbeitet, die für jede Art von IP-Adresse
gelten.

Wir können dieses Konzept in Code ausdrücken, indem wir eine Enumeration
`IpAddrKind` definieren und die möglichen Arten auflisten, die eine IP-Adresse
haben kann, `V4` und `V6`. Das sind die Varianten des Enums:

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-01-defining-enums/src/main.rs:def}}
```

`IpAddrKind` ist jetzt ein benutzerdefinierter Datentyp, den wir an anderer
Stelle in unserem Code verwenden können.

### Enum-Werte {#enum-values}

Wir können Instanzen jeder der beiden Varianten von `IpAddrKind` so erzeugen:

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-01-defining-enums/src/main.rs:instance}}
```

Beachte, dass die Varianten des Enums im Namensraum seines Bezeichners liegen
und wir die beiden mit einem doppelten Doppelpunkt trennen. Das ist nützlich,
weil jetzt beide Werte `IpAddrKind::V4` und `IpAddrKind::V6` denselben Typ
haben: `IpAddrKind`. Wir können dann zum Beispiel eine Funktion definieren, die
ein beliebiges `IpAddrKind` nimmt:

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-01-defining-enums/src/main.rs:fn}}
```

Und wir können diese Funktion mit jeder der beiden Varianten aufrufen:

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-01-defining-enums/src/main.rs:fn_call}}
```

Enums haben noch weitere Vorteile. Wenn wir weiter über unseren IP-Adresstyp
nachdenken, haben wir im Moment keine Möglichkeit, die eigentlichen _Daten_ der
IP-Adresse zu speichern; wir wissen nur, welche _Art_ von Adresse es ist. Da du
in Kapitel 5 gerade Structs kennengelernt hast, könntest du versucht sein,
dieses Problem mit Structs zu lösen, wie in Listing 6-1 gezeigt.

```aquascope,interpreter
#fn main() {
enum IpAddrKind {
    V4,
    V6,
}

struct IpAddr {
    kind: IpAddrKind,
    address: String,
}

let home = IpAddr {
    kind: IpAddrKind::V4,
    address: String::from("127.0.0.1"),
};

let loopback = IpAddr {
    kind: IpAddrKind::V6,
    address: String::from("::1"),
};`[]`
#}
```

Hier haben wir ein Struct `IpAddr` mit zwei Feldern definiert: einem Feld `kind`
vom Typ `IpAddrKind` (dem Enum, das wir vorhin definiert haben) und einem Feld
`address` vom Typ `String`. Wir haben zwei Instanzen dieses Structs. Die erste
ist `home` und hat den Wert `IpAddrKind::V4` als `kind` mit den zugehörigen
Adressdaten `127.0.0.1`. Die zweite Instanz ist `loopback`. Sie hat die andere
Variante von `IpAddrKind` als Wert für `kind`, nämlich `V6`, und die zugehörige
Adresse `::1`. Wir haben ein Struct verwendet, um die Werte `kind` und `address`
zu bündeln, sodass die Variante jetzt mit dem Wert verknüpft ist.

Dasselbe Konzept nur mit einem Enum darzustellen, ist jedoch knapper: Statt
eines Enums innerhalb eines Structs können wir Daten direkt in jede
Enum-Variante legen. Diese neue Definition des Enums `IpAddr` besagt, dass die
Varianten `V4` und `V6` beide zugehörige `String`-Werte haben:

```aquascope,interpreter
#fn main() {    
enum IpAddr {
    V4(String),
    V6(String),
}

let home = IpAddr::V4(String::from("127.0.0.1"));

let loopback = IpAddr::V6(String::from("::1"));`[]`
#}
```

Wir hängen die Daten direkt an jede Variante des Enums, also ist kein
zusätzliches Struct nötig. Hier sieht man auch leichter ein weiteres Detail der
Funktionsweise von Enums: Der Name jeder Enum-Variante, die wir definieren, wird
zugleich zu einer Funktion, die eine Instanz des Enums erzeugt. Das heißt,
`IpAddr::V4()` ist ein Funktionsaufruf, der ein `String`-Argument nimmt und eine
Instanz des Typs `IpAddr` zurückgibt. Diese Konstruktorfunktion wird automatisch
definiert, wenn wir das Enum definieren.

Ein Enum statt eines Structs zu verwenden, hat noch einen weiteren Vorteil: Jede
Variante kann unterschiedliche Typen und Mengen zugehöriger Daten haben.
IP-Adressen der Version vier haben immer vier numerische Bestandteile mit Werten
zwischen 0 und 255. Wollten wir `V4`-Adressen als vier `u8`-Werte speichern,
`V6`-Adressen aber weiterhin als einen einzigen `String`-Wert ausdrücken, ginge
das mit einem Struct nicht. Enums meistern diesen Fall mühelos:

```aquascope,interpreter
#fn main() {
enum IpAddr {
    V4(u8, u8, u8, u8),
    V6(String),
}

let home = IpAddr::V4(127, 0, 0, 1);

let loopback = IpAddr::V6(String::from("::1"));`[]`
#}

```

Wir haben verschiedene Möglichkeiten gezeigt, Datenstrukturen zu definieren, um
IP-Adressen der Version vier und der Version sechs zu speichern. Wie sich
herausstellt, kommt es aber so häufig vor, dass man IP-Adressen speichern und
kodieren möchte, um welche Art es sich handelt, dass
[die Standardbibliothek eine Definition hat, die wir verwenden können!][IpAddr]<!-- ignore -->
Sehen wir uns an, wie die Standardbibliothek `IpAddr` definiert. Sie hat genau
das Enum und die Varianten, die wir definiert und verwendet haben, aber sie
bettet die Adressdaten in Form zweier verschiedener Structs in die Varianten
ein, die für jede Variante unterschiedlich definiert sind:

```rust
struct Ipv4Addr {
    // --snip--
}

struct Ipv6Addr {
    // --snip--
}

enum IpAddr {
    V4(Ipv4Addr),
    V6(Ipv6Addr),
}
```

Dieser Code veranschaulicht, dass du beliebige Daten in eine Enum-Variante legen
kannst: zum Beispiel Strings, numerische Typen oder Structs. Du kannst sogar ein
weiteres Enum hineinlegen! Außerdem sind Typen der Standardbibliothek oft nicht
viel komplizierter als das, was du dir selbst ausdenken würdest.

Beachte: Obwohl die Standardbibliothek eine Definition für `IpAddr` enthält,
können wir trotzdem ohne Konflikt unsere eigene Definition erzeugen und
verwenden, weil wir die Definition der Standardbibliothek nicht in unseren
Gültigkeitsbereich (_scope_) gebracht haben. Mehr darüber, wie man Typen in den
Gültigkeitsbereich bringt, besprechen wir in Kapitel 7.

Sehen wir uns in Listing 6-2 ein weiteres Beispiel für ein Enum an: Dieses hat
eine große Vielfalt an Typen in seinen Varianten.

<Listing number="6-2" caption="Ein Enum `Message`, dessen Varianten jeweils unterschiedliche Mengen und Typen von Werten speichern">

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/listing-06-02/src/main.rs:here}}
```

</Listing>

Dieses Enum hat vier Varianten mit unterschiedlichen Typen:

- `Quit`: Hat überhaupt keine zugehörigen Daten
- `Move`: Hat benannte Felder, wie ein Struct
- `Write`: Enthält einen einzelnen `String`
- `ChangeColor`: Enthält drei `i32`-Werte

Ein Enum mit Varianten wie denen in Listing 6-2 zu definieren, ähnelt dem
Definieren verschiedener Struct-Definitionen, nur dass das Enum nicht das
Schlüsselwort `struct` verwendet und alle Varianten unter dem Typ `Message`
zusammengefasst sind. Die folgenden Structs könnten dieselben Daten aufnehmen
wie die vorherigen Enum-Varianten:

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-04-structs-similar-to-message-enum/src/main.rs:here}}
```

Würden wir aber die verschiedenen Structs verwenden, von denen jedes seinen
eigenen Typ hat, könnten wir nicht so leicht eine Funktion definieren, die jede
dieser Arten von Nachrichten nimmt, wie mit dem in Listing 6-2 definierten Enum
`Message`, das ein einziger Typ ist.

Es gibt noch eine weitere Gemeinsamkeit von Enums und Structs: So wie wir mit
`impl` Methoden auf Structs definieren können, können wir auch Methoden auf
Enums definieren. Hier ist eine Methode namens `call`, die wir auf unserem Enum
`Message` definieren könnten:

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-05-methods-on-enums/src/main.rs:here}}
```

Der Rumpf der Methode würde `self` verwenden, um den Wert zu bekommen, auf dem
wir die Methode aufgerufen haben. In diesem Beispiel haben wir eine Variable `m`
mit dem Wert `Message::Write(String::from("hello"))` erzeugt, und genau das ist
`self` im Rumpf der Methode `call`, wenn `m.call()` ausgeführt wird.

Sehen wir uns ein weiteres Enum der Standardbibliothek an, das sehr verbreitet
und nützlich ist: `Option`.

<!-- Old headings. Do not remove or links may break. -->

<a id="the-option-enum-and-its-advantages-over-null-values"></a>

### Das Enum `Option` {#the-option-enum}

Dieser Abschnitt sieht sich als Fallstudie `Option` an, ein weiteres Enum, das
die Standardbibliothek definiert. Der Typ `Option` kodiert das sehr häufige
Szenario, in dem ein Wert etwas oder nichts sein kann.

Wenn du zum Beispiel das erste Element einer nicht leeren Liste anforderst,
bekommst du einen Wert. Wenn du das erste Element einer leeren Liste anforderst,
bekommst du nichts. Dieses Konzept mit dem Typsystem auszudrücken, bedeutet,
dass der Compiler prüfen kann, ob du alle Fälle behandelt hast, die du behandeln
solltest; diese Funktionalität kann Bugs verhindern, die in anderen
Programmiersprachen äußerst häufig sind.

Beim Design von Programmiersprachen denkt man oft darüber nach, welche Features
man aufnimmt, aber die Features, die man weglässt, sind ebenso wichtig. Rust hat
nicht das Null-Feature, das viele andere Sprachen haben. _Null_ ist ein Wert,
der bedeutet, dass dort kein Wert ist. In Sprachen mit Null können Variablen
immer in einem von zwei Zuständen sein: null oder nicht null.

In seinem Vortrag „Null References: The Billion Dollar Mistake“ aus dem Jahr
2009 sagte Tony Hoare, der Erfinder von Null, Folgendes:

> Ich nenne es meinen Milliarden-Dollar-Fehler. Damals entwarf ich das erste
> umfassende Typsystem für Referenzen in einer objektorientierten Sprache. Mein
> Ziel war sicherzustellen, dass jede Verwendung von Referenzen absolut sicher
> ist und vom Compiler automatisch geprüft wird. Aber ich konnte der Versuchung
> nicht widerstehen, eine Null-Referenz einzubauen, einfach weil sie so leicht
> zu implementieren war. Das hat zu unzähligen Fehlern, Sicherheitslücken und
> Systemabstürzen geführt, die in den letzten vierzig Jahren vermutlich Schmerz
> und Schaden in Höhe von einer Milliarde Dollar verursacht haben.

Das Problem mit Null-Werten ist: Wenn du versuchst, einen Null-Wert als
Nicht-Null-Wert zu verwenden, bekommst du irgendeine Art von Fehler. Weil diese
Unterscheidung „null oder nicht null“ allgegenwärtig ist, macht man diese Art
von Fehler äußerst leicht.

Das Konzept, das Null auszudrücken versucht, ist aber trotzdem nützlich: Null
ist ein Wert, der aus irgendeinem Grund gerade ungültig oder nicht vorhanden
ist.

Das Problem liegt nicht wirklich am Konzept, sondern an der konkreten
Implementierung. Deshalb hat Rust keine Nulls, wohl aber ein Enum, das das
Konzept kodieren kann, dass ein Wert vorhanden oder nicht vorhanden ist. Dieses
Enum ist `Option<T>`, und es ist
[in der Standardbibliothek][option]<!-- ignore --> wie folgt definiert:

```rust
enum Option<T> {
    None,
    Some(T),
}
```

Das Enum `Option<T>` ist so nützlich, dass es sogar im Prelude enthalten ist; du
musst es nicht explizit in den Gültigkeitsbereich bringen. Auch seine Varianten
sind im Prelude enthalten: Du kannst `Some` und `None` direkt ohne das Präfix
`Option::` verwenden. Das Enum `Option<T>` ist trotzdem nur ein ganz normales
Enum, und `Some(T)` und `None` sind weiterhin Varianten des Typs `Option<T>`.

Die Syntax `<T>` ist ein Feature von Rust, über das wir noch nicht gesprochen
haben. Es ist ein generischer Typparameter, und Generics behandeln wir in
Kapitel 10 ausführlicher. Vorerst genügt es zu wissen, dass `<T>` bedeutet, dass
die Variante `Some` des Enums `Option` ein Datenstück beliebigen Typs aufnehmen
kann und dass jeder konkrete Typ, der anstelle von `T` verwendet wird, den
gesamten Typ `Option<T>` zu einem anderen Typ macht. Hier sind einige Beispiele
dafür, wie `Option`-Werte Zahlentypen und Zeichentypen aufnehmen:

```aquascope,interpreter
#fn main() {
let some_number = Some(5);
let some_char = Some('e');

let absent_number: Option<i32> = None;`[]`
#}
```

Der Typ von `some_number` ist `Option<i32>`. Der Typ von `some_char` ist
`Option<char>`, ein anderer Typ. Rust kann diese Typen ableiten, weil wir einen
Wert innerhalb der Variante `Some` angegeben haben. Für `absent_number` verlangt
Rust, dass wir den gesamten Typ `Option` annotieren: Der Compiler kann nicht
ableiten, welchen Typ die entsprechende Variante `Some` enthalten wird, wenn er
nur einen `None`-Wert sieht. Hier teilen wir Rust mit, dass `absent_number` vom
Typ `Option<i32>` sein soll.

Wenn wir einen `Some`-Wert haben, wissen wir, dass ein Wert vorhanden ist, und
der Wert steckt im `Some`. Wenn wir einen `None`-Wert haben, bedeutet das in
gewissem Sinne dasselbe wie Null: Wir haben keinen gültigen Wert. Warum ist
`Option<T>` also besser als Null?

Kurz gesagt: Weil `Option<T>` und `T` (wobei `T` ein beliebiger Typ sein kann)
verschiedene Typen sind, lässt uns der Compiler einen `Option<T>`-Wert nicht so
verwenden, als wäre er sicher ein gültiger Wert. Dieser Code lässt sich zum
Beispiel nicht kompilieren, weil er versucht, einen `i8` zu einer `Option<i8>`
zu addieren:

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-07-cant-use-option-directly/src/main.rs:here}}
```

Wenn wir diesen Code ausführen, bekommen wir eine Fehlermeldung wie diese:

```console
{{#include ../listings/ch06-enums-and-pattern-matching/no-listing-07-cant-use-option-directly/output.txt}}
```

Heftig! Im Endeffekt bedeutet diese Fehlermeldung, dass Rust nicht versteht, wie
man einen `i8` und eine `Option<i8>` addiert, weil es verschiedene Typen sind.
Wenn wir in Rust einen Wert eines Typs wie `i8` haben, stellt der Compiler
sicher, dass wir immer einen gültigen Wert haben. Wir können zuversichtlich
weitermachen, ohne vor der Verwendung dieses Werts auf Null prüfen zu müssen.
Nur wenn wir eine `Option<i8>` haben (oder welchen Werttyp wir auch immer
verwenden), müssen wir uns darum kümmern, dass möglicherweise kein Wert
vorhanden ist, und der Compiler stellt sicher, dass wir diesen Fall behandeln,
bevor wir den Wert verwenden.

Anders gesagt: Du musst eine `Option<T>` in ein `T` umwandeln, bevor du
`T`-Operationen damit ausführen kannst. Im Allgemeinen hilft das, eines der
häufigsten Probleme mit Null zu erkennen: anzunehmen, dass etwas nicht null ist,
obwohl es das tatsächlich ist.

Wenn das Risiko wegfällt, fälschlicherweise einen Nicht-Null-Wert anzunehmen,
kannst du deinem Code mehr vertrauen. Um einen Wert zu haben, der möglicherweise
null sein kann, musst du dich explizit dafür entscheiden, indem du den Typ
dieses Werts zu `Option<T>` machst. Wenn du diesen Wert dann verwendest, musst
du den Fall, dass der Wert null ist, explizit behandeln. Überall, wo ein Wert
einen Typ hat, der keine `Option<T>` ist, _kannst_ du sicher annehmen, dass der
Wert nicht null ist. Das war eine bewusste Designentscheidung für Rust, um die
Verbreitung von Null einzuschränken und die Sicherheit von Rust-Code zu erhöhen.

Wie bekommst du also den `T`-Wert aus einer `Some`-Variante heraus, wenn du
einen Wert vom Typ `Option<T>` hast, damit du diesen Wert verwenden kannst? Das
Enum `Option<T>` hat eine große Zahl von Methoden, die in einer Vielzahl von
Situationen nützlich sind; du findest sie in
[seiner Dokumentation][docs]<!-- ignore -->. Dich mit den Methoden von
`Option<T>` vertraut zu machen, wird auf deiner Reise mit Rust äußerst nützlich
sein.

Um einen `Option<T>`-Wert zu verwenden, möchtest du im Allgemeinen Code haben,
der jede Variante behandelt. Du möchtest Code, der nur ausgeführt wird, wenn du
einen `Some(T)`-Wert hast, und dieser Code darf das innere `T` verwenden. Und du
möchtest anderen Code, der nur ausgeführt wird, wenn du einen `None`-Wert hast,
und diesem Code steht kein `T`-Wert zur Verfügung. Der `match`-Ausdruck ist ein
Kontrollflusskonstrukt, das genau das tut, wenn man es mit Enums verwendet: Er
führt je nachdem, welche Variante des Enums er hat, unterschiedlichen Code aus,
und dieser Code kann die Daten im passenden Wert verwenden.

{{#quiz ../quizzes/ch06-01-defining-an-enum.toml}}

[IpAddr]: https://doc.rust-lang.org/std/net/enum.IpAddr.html
[option]: https://doc.rust-lang.org/std/option/enum.Option.html
[docs]: https://doc.rust-lang.org/std/option/enum.Option.html
