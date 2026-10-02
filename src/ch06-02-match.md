<!-- Old headings. Do not remove or links may break. -->

<a id="the-match-control-flow-operator"></a>

## Das Kontrollflusskonstrukt `match` {#the-match-control-flow-construct}

Rust hat ein äußerst mächtiges Kontrollflusskonstrukt namens `match`, mit dem du
einen Wert mit einer Reihe von Patterns vergleichen und dann abhängig davon,
welches Pattern passt, Code ausführen kannst. Patterns können aus Literalwerten,
Variablennamen, Platzhaltern und vielem mehr bestehen;
[Kapitel 19][ch19-00-patterns]<!-- ignore --> behandelt alle verschiedenen Arten
von Patterns und was sie tun. Die Stärke von `match` kommt von der
Ausdruckskraft der Patterns und davon, dass der Compiler bestätigt, dass alle
möglichen Fälle behandelt werden.

Stell dir einen `match`-Ausdruck wie eine Münzsortiermaschine vor: Münzen
rutschen eine Bahn mit unterschiedlich großen Löchern hinunter, und jede Münze
fällt durch das erste Loch, in das sie passt. Auf dieselbe Weise durchlaufen
Werte jedes Pattern in einem `match`, und beim ersten Pattern, in das der Wert
„passt“, fällt der Wert in den zugehörigen Codeblock, der dann ausgeführt wird.

Wo wir gerade von Münzen sprechen: Verwenden wir sie als Beispiel für `match`!
Wir können eine Funktion schreiben, die eine unbekannte US-Münze nimmt und
ähnlich wie die Zählmaschine bestimmt, um welche Münze es sich handelt, und
ihren Wert in Cent zurückgibt, wie in Listing 6-3 gezeigt.

<Listing number="6-3" caption="Ein Enum und ein `match`-Ausdruck, dessen Patterns die Varianten des Enums sind">

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/listing-06-03/src/main.rs:here}}
```

</Listing>

Zerlegen wir das `match` in der Funktion `value_in_cents`. Zuerst schreiben wir
das Schlüsselwort `match`, gefolgt von einem Ausdruck, in diesem Fall dem Wert
`coin`. Das wirkt sehr ähnlich wie ein Bedingungsausdruck mit `if`, aber es gibt
einen großen Unterschied: Bei `if` muss die Bedingung zu einem booleschen Wert
ausgewertet werden, hier kann es aber jeder beliebige Typ sein. Der Typ von
`coin` ist in diesem Beispiel das Enum `Coin`, das wir in der ersten Zeile
definiert haben.

Als Nächstes kommen die Arme des `match`. Ein Arm hat zwei Teile: ein Pattern
und etwas Code. Der erste Arm hier hat als Pattern den Wert `Coin::Penny` und
dann den Operator `=>`, der das Pattern vom auszuführenden Code trennt. Der Code
ist in diesem Fall einfach der Wert `1`. Jeder Arm ist durch ein Komma vom
nächsten getrennt.

Wenn der `match`-Ausdruck ausgeführt wird, vergleicht er den Ergebniswert der
Reihe nach mit dem Pattern jedes Arms. Passt ein Pattern auf den Wert, wird der
zu diesem Pattern gehörende Code ausgeführt. Passt das Pattern nicht auf den
Wert, geht die Ausführung zum nächsten Arm weiter, ganz wie bei einer
Münzsortiermaschine. Wir können so viele Arme haben, wie wir brauchen: In
Listing 6-3 hat unser `match` vier Arme.

Der zu jedem Arm gehörende Code ist ein Ausdruck, und der Ergebniswert des
Ausdrucks im passenden Arm ist der Wert, der für den gesamten `match`-Ausdruck
zurückgegeben wird.

Geschweifte Klammern verwenden wir normalerweise nicht, wenn der Code eines Arms
kurz ist, wie in Listing 6-3, wo jeder Arm nur einen Wert zurückgibt. Wenn du in
einem Arm mehrere Codezeilen ausführen willst, musst du geschweifte Klammern
verwenden, und das Komma nach dem Arm ist dann optional. Der folgende Code gibt
zum Beispiel jedes Mal „Lucky penny!“ aus, wenn die Methode mit einem
`Coin::Penny` aufgerufen wird, gibt aber trotzdem den letzten Wert des Blocks
zurück, `1`:

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-08-match-arm-multiple-lines/src/main.rs:here}}
```

### Patterns, die an Werte binden {#patterns-that-bind-to-values}

Ein weiteres nützliches Feature von Match-Armen ist, dass sie an die Teile der
Werte binden können, die auf das Pattern passen. So können wir Werte aus
Enum-Varianten herausholen.

Ändern wir als Beispiel eine unserer Enum-Varianten so, dass sie Daten enthält.
Von 1999 bis 2008 prägten die Vereinigten Staaten Quarter-Münzen mit
unterschiedlichen Motiven für jeden der 50 Bundesstaaten auf einer Seite. Keine
anderen Münzen erhielten Motive der Bundesstaaten, also haben nur Quarters
diesen zusätzlichen Wert. Wir können diese Information zu unserem `enum`
hinzufügen, indem wir die Variante `Quarter` so ändern, dass sie einen
`UsState`-Wert enthält, wie wir es in Listing 6-4 getan haben.

<Listing number="6-4" caption="Ein Enum `Coin`, in dem die Variante `Quarter` zusätzlich einen `UsState`-Wert enthält">

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/listing-06-04/src/main.rs:here}}
```

</Listing>

Stellen wir uns vor, dass jemand aus unserem Freundeskreis versucht, alle 50
Bundesstaaten-Quarters zu sammeln. Während wir unser Kleingeld nach Münzart
sortieren, rufen wir auch den Namen des Bundesstaats aus, der zu jedem Quarter
gehört, damit er der Sammlung hinzugefügt werden kann, falls er noch fehlt.

Im Match-Ausdruck dieses Codes fügen wir dem Pattern, das auf Werte der Variante
`Coin::Quarter` passt, eine Variable namens `state` hinzu. Wenn ein
`Coin::Quarter` passt, wird die Variable `state` an den Wert des Bundesstaats
dieses Quarters gebunden. Dann können wir `state` im Code dieses Arms verwenden,
etwa so:

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-09-variable-in-pattern/src/main.rs:here}}
```

Würden wir `value_in_cents(Coin::Quarter(UsState::Alaska))` aufrufen, wäre
`coin` gleich `Coin::Quarter(UsState::Alaska)`. Wenn wir diesen Wert mit jedem
der Arme vergleichen, passt keiner, bis wir `Coin::Quarter(state)` erreichen. An
dieser Stelle ist `state` an den Wert `UsState::Alaska` gebunden. Diese Bindung
können wir dann im `println!`-Ausdruck verwenden und so den inneren
Bundesstaatswert aus der Variante `Quarter` des Enums `Coin` herausholen.

<!-- Old headings. Do not remove or links may break. -->

<a id="matching-with-optiont"></a>

### Das `match`-Pattern für `Option<T>` {#the-optiont-match-pattern}

Im vorherigen Abschnitt wollten wir bei der Verwendung von `Option<T>` den
inneren `T`-Wert aus dem Fall `Some` herausholen; wir können `Option<T>` auch
mit `match` behandeln, wie wir es mit dem Enum `Coin` getan haben! Statt Münzen
vergleichen wir die Varianten von `Option<T>`, aber die Funktionsweise des
`match`-Ausdrucks bleibt dieselbe.

Angenommen, wir wollen eine Funktion schreiben, die eine `Option<i32>` nimmt
und, falls darin ein Wert steckt, 1 zu diesem Wert addiert. Steckt kein Wert
darin, soll die Funktion den Wert `None` zurückgeben und gar nicht erst
versuchen, Operationen auszuführen.

Dank `match` ist diese Funktion sehr leicht zu schreiben und sieht aus wie in
Listing 6-5.

<Listing number="6-5" caption="Eine Funktion, die einen `match`-Ausdruck auf eine `Option<i32>` anwendet">

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/listing-06-05/src/main.rs:here}}
```

</Listing>

Sehen wir uns die erste Ausführung von `plus_one` genauer an. Wenn wir
`plus_one(five)` aufrufen, hat die Variable `x` im Rumpf von `plus_one` den Wert
`Some(5)`. Diesen vergleichen wir dann mit jedem Arm:

```rust,ignore
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/listing-06-05/src/main.rs:first_arm}}
```

Der Wert `Some(5)` passt nicht auf das Pattern `None`, also machen wir mit dem
nächsten Arm weiter:

```rust,ignore
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/listing-06-05/src/main.rs:second_arm}}
```

Passt `Some(5)` auf `Some(i)`? Ja! Wir haben dieselbe Variante. Das `i` bindet
an den Wert in `Some`, also nimmt `i` den Wert `5` an. Dann wird der Code im Arm
ausgeführt: Wir addieren 1 zum Wert von `i` und erzeugen einen neuen `Some`-Wert
mit unserer Summe `6` darin.

Betrachten wir nun den zweiten Aufruf von `plus_one` in Listing 6-5, bei dem `x`
gleich `None` ist. Wir betreten das `match` und vergleichen mit dem ersten Arm:

```rust,ignore
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/listing-06-05/src/main.rs:first_arm}}
```

Er passt! Es gibt keinen Wert, zu dem etwas addiert werden könnte, also hält das
Programm an und gibt den Wert `None` auf der rechten Seite von `=>` zurück. Weil
der erste Arm gepasst hat, werden keine weiteren Arme verglichen.

`match` und Enums zu kombinieren, ist in vielen Situationen nützlich. Dieses
Schema wirst du in Rust-Code oft sehen: `match` auf ein Enum anwenden, eine
Variable an die Daten darin binden und dann abhängig davon Code ausführen. Am
Anfang ist es etwas knifflig, aber sobald du dich daran gewöhnt hast, wirst du
es dir in allen Sprachen wünschen. Es gehört durchweg zu den Lieblingsfeatures
der Nutzerinnen und Nutzer.

### Match-Ausdrücke sind erschöpfend {#matches-are-exhaustive}

Es gibt noch einen weiteren Aspekt von `match`, den wir besprechen müssen: Die
Patterns der Arme müssen alle Möglichkeiten abdecken. Betrachte diese Version
unserer Funktion `plus_one`, die einen Bug hat und sich nicht kompilieren lässt:

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-10-non-exhaustive-match/src/main.rs:here}}
```

Wir haben den Fall `None` nicht behandelt, also verursacht dieser Code einen
Bug. Zum Glück ist es ein Bug, den Rust erkennen kann. Wenn wir versuchen,
diesen Code zu kompilieren, bekommen wir diesen Fehler:

```console
{{#include ../listings/ch06-enums-and-pattern-matching/no-listing-10-non-exhaustive-match/output.txt}}
```

Rust weiß, dass wir nicht jeden möglichen Fall abgedeckt haben, und weiß sogar,
welches Pattern wir vergessen haben! Match-Ausdrücke sind in Rust _erschöpfend_
(_exhaustive_): Wir müssen jede einzelne Möglichkeit abdecken, damit der Code
gültig ist. Gerade bei `Option<T>` schützt uns Rust, indem es verhindert, dass
wir vergessen, den Fall `None` explizit zu behandeln, davor, einen Wert
anzunehmen, wo wir vielleicht Null haben – und macht damit den vorhin
besprochenen Milliarden-Dollar-Fehler unmöglich.

### Auffang-Patterns und der Platzhalter `_` {#catch-all-patterns-and-the-_-placeholder}

Mit Enums können wir auch für einige bestimmte Werte besondere Aktionen
ausführen und für alle anderen Werte eine Standardaktion. Stell dir vor, wir
implementieren ein Spiel, in dem sich deine Spielfigur nicht bewegt, sondern
einen schicken neuen Hut bekommt, wenn du eine 3 würfelst. Würfelst du eine 7,
verliert deine Spielfigur einen schicken Hut. Bei allen anderen Werten bewegt
sich deine Spielfigur entsprechend viele Felder auf dem Spielbrett. Hier ist ein
`match`, das diese Logik implementiert. Das Würfelergebnis ist dabei fest
einprogrammiert statt zufällig, und alle übrige Logik wird durch Funktionen ohne
Rumpf dargestellt, weil ihre tatsächliche Implementierung den Rahmen dieses
Beispiels sprengen würde:

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-15-binding-catchall/src/main.rs:here}}
```

Bei den ersten beiden Armen sind die Patterns die Literalwerte `3` und `7`. Beim
letzten Arm, der jeden anderen möglichen Wert abdeckt, ist das Pattern die
Variable, die wir `other` genannt haben. Der Code, der für den Arm `other`
ausgeführt wird, verwendet die Variable, indem er sie an die Funktion
`move_player` übergibt.

Dieser Code lässt sich kompilieren, obwohl wir nicht alle möglichen Werte
aufgeführt haben, die ein `u8` haben kann, weil das letzte Pattern auf alle
Werte passt, die nicht ausdrücklich aufgeführt sind. Dieses Auffang-Pattern
erfüllt die Anforderung, dass `match` erschöpfend sein muss. Beachte, dass wir
den Auffang-Arm ans Ende setzen müssen, weil die Patterns der Reihe nach
ausgewertet werden. Hätten wir den Auffang-Arm weiter vorn platziert, würden die
anderen Arme nie ausgeführt; deshalb warnt uns Rust, wenn wir nach einem
Auffang-Arm weitere Arme hinzufügen!

Rust hat außerdem ein Pattern, das wir verwenden können, wenn wir einen
Auffang-Arm wollen, den Wert im Auffang-Pattern aber nicht _verwenden_ wollen:
`_` ist ein besonderes Pattern, das auf jeden Wert passt und nicht an diesen
Wert bindet. Damit teilen wir Rust mit, dass wir den Wert nicht verwenden
werden, sodass Rust uns nicht vor einer unbenutzten Variable warnt.

Ändern wir die Spielregeln: Wenn du jetzt etwas anderes als eine 3 oder eine 7
würfelst, musst du noch einmal würfeln. Wir brauchen den aufgefangenen Wert
nicht mehr, also können wir unseren Code so ändern, dass er `_` statt der
Variable namens `other` verwendet:

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-16-underscore-catchall/src/main.rs:here}}
```

Auch dieses Beispiel erfüllt die Anforderung der Vollständigkeit, weil wir im
letzten Arm alle anderen Werte ausdrücklich ignorieren; wir haben nichts
vergessen.

Schließlich ändern wir die Spielregeln noch einmal, sodass in deinem Zug nichts
weiter passiert, wenn du etwas anderes als eine 3 oder eine 7 würfelst. Das
können wir ausdrücken, indem wir den Unit-Wert (den leeren Tupeltyp, den wir im
Abschnitt [„Der Tupeltyp“][tuples]<!-- ignore --> erwähnt haben) als Code für
den Arm `_` verwenden:

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-17-underscore-unit/src/main.rs:here}}
```

Hier teilen wir Rust ausdrücklich mit, dass wir keinen anderen Wert verwenden
werden, der nicht auf ein Pattern in einem früheren Arm passt, und dass wir in
diesem Fall keinen Code ausführen wollen.

Mehr über Patterns und Matching erfährst du in
[Kapitel 19][ch19-00-patterns]<!-- ignore -->.

<!-- BEGIN INTERVENTION: 1e4f082c-ffa4-4d33-8726-2dbcd72e1aa2 -->

### Wie Match-Ausdrücke mit Ownership zusammenspielen {#how-matches-interact-with-ownership}

Wenn ein Enum nicht kopierbare Daten wie einen String enthält, solltest du
darauf achten, ob ein Match-Ausdruck diese Daten verschiebt (_move_) oder
ausleiht (_borrow_). Dieses Programm mit einer `Option<String>` lässt sich zum
Beispiel kompilieren:

```aquascope,permissions,stepper,boundaries
# fn main() {
let opt: Option<String> = 
    Some(String::from("Hello world"));

match opt {
    Some(_) => println!("Some!"),
    None => println!("None!")
};

println!("{:?}", opt);
# }
```

Ersetzen wir aber den Platzhalter in `Some(_)` durch einen Variablennamen, etwa
`Some(s)`, lässt sich das Programm NICHT kompilieren:

```aquascope,permissions,stepper,boundaries,shouldFail
#fn main() {
let opt: Option<String> = 
    Some(String::from("Hello world"));

match opt {
    // _ became s
    Some(s) => println!("Some: {}", s),
    None => println!("None!")
};

println!("{:?}", opt);`{}`
#}
```

`opt` ist ein schlichtes Enum – sein Typ ist `Option<String>` und keine Referenz
wie `&Option<String>`. Ein Match-Ausdruck auf `opt` verschiebt deshalb nicht
ignorierte Felder wie `s`. Beachte, wie `opt` im zweiten Programm die Read- und
Own-Berechtigung früher verliert als im ersten. Nach dem Match-Ausdruck wurden
die Daten in `opt` verschoben, daher ist es nicht erlaubt, `opt` im `println` zu
lesen.

Wenn wir in `opt` hineinschauen wollen, ohne seinen Inhalt zu verschieben, ist
die idiomatische Lösung, das Pattern-Matching auf eine Referenz anzuwenden:

```aquascope,permissions,stepper,boundaries
#fn main() {
let opt: Option<String> = 
    Some(String::from("Hello world"));

// opt became &opt
match &opt {
    Some(s) => println!("Some: {}", s),
    None => println!("None!")
};

println!("{:?}", opt);
#}
```

Rust „schiebt“ die Referenz vom äußeren Enum, `&Option<String>`, „nach unten“
zum inneren Feld, `&String`. Deshalb hat `s` den Typ `&String`, und `opt` kann
nach dem Match-Ausdruck weiterverwendet werden. Um diesen Mechanismus des
„Nach-unten-Schiebens“ besser zu verstehen, sieh dir den Abschnitt über
[Bindungsmodi (_binding modes_)](https://doc.rust-lang.org/reference/patterns.html#binding-modes)
in der Rust-Referenz an.

<!-- END INTERVENTION -->

{{#quiz ../quizzes/ch06-02-match.toml}}

[tuples]: ch03-02-data-types.html#the-tuple-type
[ch19-00-patterns]: ch19-00-patterns.html
