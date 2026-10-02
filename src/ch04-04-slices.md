## Der Slice-Typ {#the-slice-type}

Mit _Slices_ kannst du auf eine zusammenhängende Folge von Elementen in einer
[Collection](ch08-00-common-collections.md) verweisen statt auf die ganze
Collection. Ein Slice ist eine Art Referenz, also ein nicht-besitzender Zeiger.

Um zu zeigen, warum Slices nützlich sind, lösen wir eine kleine
Programmieraufgabe: Schreibe eine Funktion, die einen String mit durch
Leerzeichen getrennten Wörtern entgegennimmt und das erste Wort zurückgibt, das
sie in diesem String findet. Findet die Funktion kein Leerzeichen im String,
muss der ganze String ein einziges Wort sein, also soll der gesamte String
zurückgegeben werden. Ohne Slices würden wir die Signatur der Funktion
vielleicht so schreiben:

```rust,ignore
fn first_word(s: &String) -> ?
```

Die Funktion `first_word` hat einen `&String` als Parameter. Wir wollen keine
Ownership des Strings, also ist das in Ordnung. Aber was sollen wir zurückgeben?
Wir haben eigentlich keine Möglichkeit, über einen _Teil_ eines Strings zu
sprechen. Wir könnten aber den Index des Wortendes zurückgeben, das durch ein
Leerzeichen markiert ist. Probieren wir das aus, wie in Listing 4-7 gezeigt.

<span class="filename">Dateiname: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch04-understanding-ownership/listing-04-07/src/main.rs:here}}
```

<span class="caption">Listing 4-7: Die Funktion `first_word`, die einen
Byte-Index in den Parameter vom Typ `String` zurückgibt</span>

Weil wir den `String` Element für Element durchgehen und prüfen müssen, ob ein
Wert ein Leerzeichen ist, wandeln wir unseren `String` mit der Methode
`as_bytes` in ein Array von Bytes um:

```rust,ignore
{{#rustdoc_include ../listings/ch04-understanding-ownership/listing-04-07/src/main.rs:as_bytes}}
```

Als Nächstes erzeugen wir mit der Methode `iter` einen Iterator über das
Byte-Array:

```rust,ignore
{{#rustdoc_include ../listings/ch04-understanding-ownership/listing-04-07/src/main.rs:iter}}
```

Iteratoren besprechen wir ausführlicher in [Kapitel 13][ch13]<!-- ignore -->.
Vorerst genügt es zu wissen, dass `iter` eine Methode ist, die jedes Element
einer Collection zurückgibt, und dass `enumerate` das Ergebnis von `iter`
umhüllt und jedes Element stattdessen als Teil eines Tupels zurückgibt. Das
erste Element des von `enumerate` zurückgegebenen Tupels ist der Index, das
zweite eine Referenz auf das Element. Das ist etwas bequemer, als den Index
selbst zu berechnen.

Weil die Methode `enumerate` ein Tupel zurückgibt, können wir Patterns
verwenden, um dieses Tupel zu destrukturieren. Über Patterns sprechen wir
ausführlicher in [Kapitel 6][ch6]<!-- ignore -->. In der `for`-Schleife geben
wir ein Pattern an, das `i` für den Index im Tupel und `&item` für das einzelne
Byte im Tupel hat. Weil wir von `.iter().enumerate()` eine Referenz auf das
Element bekommen, verwenden wir `&` im Pattern.

Innerhalb der `for`-Schleife suchen wir mit der Syntax für Byte-Literale nach
dem Byte, das das Leerzeichen darstellt. Finden wir ein Leerzeichen, geben wir
die Position zurück. Andernfalls geben wir mit `s.len()` die Länge des Strings
zurück:

```rust,ignore
{{#rustdoc_include ../listings/ch04-understanding-ownership/listing-04-07/src/main.rs:inside_for}}
```

Jetzt haben wir eine Möglichkeit, den Index des Endes des ersten Worts im String
herauszufinden, aber es gibt ein Problem. Wir geben einen `usize` für sich
allein zurück, aber diese Zahl ist nur im Kontext des `&String` sinnvoll. Anders
gesagt: Weil sie ein vom `String` getrennter Wert ist, gibt es keine Garantie,
dass sie in Zukunft noch gültig ist. Betrachte das Programm in Listing 4-8, das
die Funktion `first_word` aus Listing 4-7 verwendet.

<span class="filename">Dateiname: src/main.rs</span>

```aquascope,interpreter+permissions,boundaries,stepper,horizontal
fn first_word(s: &String) -> usize {
    let bytes = s.as_bytes();

    for (i, &item) in bytes.iter().enumerate() {
        if item == b' ' {
            return i;
        }
    }

    s.len()
}

fn main() {
    let mut s = String::from("hello world");`(focus)`
    let word = first_word(&s);`[]`
    s.clear();`[]``{}`    
}
``` 

<span class="caption">Listing 4-8: Das Ergebnis des Aufrufs von `first_word`
speichern und dann den Inhalt des `String` ändern</span>

Dieses Programm lässt sich ohne Fehler kompilieren, weil `s` nach dem Aufruf von
`first_word` seine Write-Berechtigungen behält. Weil `word` überhaupt nicht mit
dem Zustand von `s` verbunden ist, enthält `word` weiterhin den Wert `5`. Wir
könnten versuchen, mit diesem Wert `5` und der Variable `s` das erste Wort
herauszuholen, aber das wäre ein Bug, denn der Inhalt von `s` hat sich geändert,
seit wir `5` in `word` gespeichert haben.

Sich darum kümmern zu müssen, dass der Index in `word` nicht aus dem Takt mit
den Daten in `s` gerät, ist mühsam und fehleranfällig! Die Verwaltung dieser
Indizes wird noch zerbrechlicher, wenn wir eine Funktion `second_word`
schreiben. Ihre Signatur müsste so aussehen:

```rust,ignore
fn second_word(s: &String) -> (usize, usize) {
```

Jetzt verfolgen wir einen Start- _und_ einen Endindex und haben noch mehr Werte,
die aus Daten in einem bestimmten Zustand berechnet wurden, aber überhaupt nicht
an diesen Zustand gebunden sind. Wir haben drei voneinander unabhängige
Variablen herumschwirren, die synchron gehalten werden müssen.

Zum Glück hat Rust eine Lösung für dieses Problem: String-Slices.

### String-Slices {#string-slices}

Ein _String-Slice_ ist eine Referenz auf einen Teil eines `String` und sieht so
aus:

```aquascope,interpreter
#fn main() {
let s = String::from("hello world");

let hello: &str = &s[0..5];
let world: &str = &s[6..11];
let s2: &String = &s; `[]`
#}
```

Statt einer Referenz auf den gesamten `String` (wie `s2`) ist `hello` eine
Referenz auf einen Teil des `String`, der durch das zusätzliche `[0..5]`
angegeben wird. Wir erzeugen Slices mit einem Bereich in eckigen Klammern, indem
wir `[starting_index..ending_index]` angeben, wobei `starting_index` die erste
Position im Slice ist und `ending_index` um eins größer als die letzte Position
im Slice.

Slices sind besondere Referenzen, weil sie „fette“ Zeiger (_fat pointers_) sind,
also Zeiger mit Metadaten. Hier sind die Metadaten die Länge des Slices. Wir
können diese Metadaten sehen, indem wir unsere Visualisierung so umstellen, dass
sie einen Blick in das Innere der Datenstrukturen von Rust erlaubt:

```aquascope,interpreter,concreteTypes,hideCode
fn main() {
    let s = String::from("hello world");

    let hello: &str = &s[0..5];
    let world: &str = &s[6..11];
    let s2: &String = &s; // not a slice, for comparison
    `[]`
}
```

Beachte, dass die Variablen `hello` und `world` beide ein Feld `ptr` und ein
Feld `len` haben, die zusammen die unterstrichenen Bereiche des Strings auf dem
Heap festlegen. Hier siehst du auch, wie ein `String` tatsächlich aussieht: Ein
String ist ein Vektor von Bytes (`Vec<u8>`), der eine Länge `len` und einen
Puffer `buf` enthält, der wiederum einen Zeiger `ptr` und eine Kapazität `cap`
hat.

Weil Slices Referenzen sind, ändern sie auch die Berechtigungen auf die
referenzierten Daten. Beachte zum Beispiel unten, dass `s` die Write- und
Own-Berechtigungen verliert, wenn `hello` als Slice von `s` erzeugt wird:

```aquascope,permissions,stepper,boundaries
fn main() {
    let mut s = String::from("hello");
    let hello: &str = &s[0..5];
    println!("{hello}");
    s.push_str(" world");
}
```

#### Bereichssyntax {#range-syntax}

Wenn du bei Index null beginnen willst, kannst du in der Bereichssyntax `..` von
Rust den Wert vor den beiden Punkten weglassen. Diese beiden sind also gleich:

```rust
let s = String::from("hello");

let slice = &s[0..2];
let slice = &s[..2];
```

Genauso kannst du die abschließende Zahl weglassen, wenn dein Slice das letzte
Byte des `String` einschließt. Diese beiden sind also gleich:

```rust
let s = String::from("hello");

let len = s.len();

let slice = &s[3..len];
let slice = &s[3..];
```

Du kannst auch beide Werte weglassen, um einen Slice des gesamten Strings zu
bekommen. Diese beiden sind also gleich:

```rust
let s = String::from("hello");

let len = s.len();

let slice = &s[0..len];
let slice = &s[..];
```

> Note: Die Bereichsindizes eines String-Slices müssen an gültigen
> UTF-8-Zeichengrenzen liegen. Wenn du versuchst, einen String-Slice mitten in
> einem Multibyte-Zeichen zu erzeugen, wird dein Programm mit einem Fehler
> beendet. Um String-Slices einzuführen, gehen wir in diesem Abschnitt nur von
> ASCII aus; eine gründlichere Besprechung des Umgangs mit UTF-8 findest du im
> Abschnitt
> [„UTF-8-kodierten Text mit Strings speichern“][strings]<!-- ignore --> in
> Kapitel 8.

#### `first_word` mit String-Slices neu schreiben {#rewriting-first_word-with-string-slices}

Mit all diesen Informationen schreiben wir `first_word` so um, dass es einen
Slice zurückgibt. Der Typ für „String-Slice“ wird als `&str` geschrieben:

<span class="filename">Dateiname: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch04-understanding-ownership/no-listing-18-first-word-slice/src/main.rs:here}}
```

Den Index des Wortendes ermitteln wir auf dieselbe Weise wie in Listing 4-7,
indem wir nach dem ersten Vorkommen eines Leerzeichens suchen. Wenn wir ein
Leerzeichen finden, geben wir einen String-Slice zurück und verwenden dabei den
Anfang des Strings und den Index des Leerzeichens als Start- und Endindex.

Wenn wir jetzt `first_word` aufrufen, bekommen wir einen einzigen Wert zurück,
der an die zugrunde liegenden Daten gebunden ist. Der Wert besteht aus einer
Referenz auf den Startpunkt des Slices und der Anzahl der Elemente im Slice.

Einen Slice zurückzugeben, würde auch für eine Funktion `second_word`
funktionieren:

```rust,ignore
fn second_word(s: &String) -> &str {
```

Jetzt haben wir eine unkomplizierte API, die viel schwerer falsch zu verwenden
ist, weil der Compiler sicherstellt, dass die Referenzen in den `String` gültig
bleiben. Erinnerst du dich an den Bug im Programm in Listing 4-8, als wir den
Index des Endes des ersten Worts ermittelt, dann aber den String geleert haben,
sodass unser Index ungültig war? Dieser Code war logisch falsch, zeigte aber
keine unmittelbaren Fehler. Die Probleme wären erst später aufgetaucht, wenn wir
weiter versucht hätten, den Index des ersten Worts mit einem geleerten String zu
verwenden. Slices machen diesen Bug unmöglich und zeigen uns viel früher, dass
wir ein Problem mit unserem Code haben. Zum Beispiel:

<span class="filename">Dateiname: src/main.rs</span>

```aquascope,permissions,boundaries,stepper,shouldFail
#fn first_word(s: &String) -> &str {
#    let bytes = s.as_bytes();
#
#    for (i, &item) in bytes.iter().enumerate() {
#        if item == b' ' {
#            return &s[0..i];
#        }
#    }
#
#    &s[..]
#}
fn main() {
    let mut s = String::from("hello world");
    let word = first_word(&s);`(focus,paths:s)`
    s.clear();`{}`
    println!("the first word is: {}", word);
}
```

Du siehst, dass der Aufruf von `first_word` jetzt `s` die Write-Berechtigung
entzieht, was uns daran hindert, `s.clear()` aufzurufen. Hier ist der
Compilerfehler:

```console
{{#include ../listings/ch04-understanding-ownership/no-listing-19-slice-error/output.txt}}
```

Erinnere dich an die Borrowing-Regeln: Wenn wir eine unveränderliche
(_immutable_) Referenz auf etwas haben, können wir nicht zusätzlich eine
veränderliche (_mutable_) Referenz erzeugen. Weil `clear` den `String` kürzen
muss, braucht es eine veränderliche Referenz. Das `println!` nach dem Aufruf von
`clear` verwendet die Referenz in `word`, also muss die unveränderliche Referenz
an dieser Stelle noch aktiv sein. Rust verbietet, dass die veränderliche
Referenz in `clear` und die unveränderliche Referenz in `word` gleichzeitig
existieren, und das Kompilieren schlägt fehl. Rust hat nicht nur unsere API
einfacher benutzbar gemacht, sondern auch eine ganze Klasse von Fehlern schon
zur Kompilierzeit beseitigt!

#### String-Literale sind Slices {#string-literals-are-slices}

Erinnere dich, dass wir darüber gesprochen haben, dass String-Literale in der
Binärdatei gespeichert werden. Da wir jetzt Slices kennen, können wir
String-Literale richtig verstehen:

```rust
let s = "Hello, world!";
```

Der Typ von `s` ist hier `&str`: Es ist ein Slice, der auf genau diese Stelle
der Binärdatei zeigt. Deshalb sind String-Literale auch unveränderlich; `&str`
ist eine unveränderliche Referenz.

#### String-Slices als Parameter {#string-slices-as-parameters}

Die Erkenntnis, dass du Slices von Literalen und von `String`-Werten bilden
kannst, führt uns zu einer weiteren Verbesserung von `first_word`, nämlich ihrer
Signatur:

```rust,ignore
fn first_word(s: &String) -> &str {
```

Erfahrenere Rustaceans würden stattdessen die Signatur aus Listing 4-9
schreiben, weil wir dieselbe Funktion dann sowohl mit `&String`-Werten als auch
mit `&str`-Werten verwenden können.

```rust,ignore
{{#rustdoc_include ../listings/ch04-understanding-ownership/listing-04-09/src/main.rs:here}}
```

<span class="caption">Listing 4-9: Die Funktion `first_word` verbessern, indem
wir für den Typ des Parameters `s` einen String-Slice verwenden</span>

Wenn wir einen String-Slice haben, können wir ihn direkt übergeben. Wenn wir
einen `String` haben, können wir einen Slice des `String` oder eine Referenz auf
den `String` übergeben. Diese Flexibilität nutzt _Deref-Coercions_, ein Feature,
das wir im Abschnitt
[„Implizite Deref-Coercions bei Funktionen und Methoden“][deref-coercions]<!--ignore-->
in Kapitel 15 behandeln.

Eine Funktion so zu definieren, dass sie einen String-Slice statt einer Referenz
auf einen `String` nimmt, macht unsere API allgemeiner und nützlicher, ohne
Funktionalität einzubüßen:

<span class="filename">Dateiname: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch04-understanding-ownership/listing-04-09/src/main.rs:usage}}
```

### Andere Slices {#other-slices}

String-Slices sind, wie du dir vorstellen kannst, speziell für Strings gedacht.
Es gibt aber auch einen allgemeineren Slice-Typ. Betrachte dieses Array:

```rust
let a = [1, 2, 3, 4, 5];
```

Genauso wie wir auf einen Teil eines Strings verweisen wollen, möchten wir
vielleicht auf einen Teil eines Arrays verweisen. Das würden wir so machen:

```rust
let a = [1, 2, 3, 4, 5];

let slice = &a[1..3];

assert_eq!(slice, &[2, 3]);
```

Dieser Slice hat den Typ `&[i32]`. Er funktioniert genauso wie String-Slices: Er
speichert eine Referenz auf das erste Element und eine Länge. Diese Art von
Slice wirst du für alle möglichen anderen Collections verwenden. Wir besprechen
diese Collections ausführlich, wenn es in Kapitel 8 um Vektoren geht.

{{#quiz ../quizzes/ch04-04-slices.toml}}

## Zusammenfassung {#summary}

Slices sind eine besondere Art von Referenz, die auf Teilbereiche einer Folge
verweisen, etwa eines Strings oder eines Vektors. Zur Laufzeit wird ein Slice
als „fetter Zeiger“ dargestellt, der einen Zeiger auf den Anfang des Bereichs
und die Länge des Bereichs enthält. Ein Vorteil von Slices gegenüber
indexbasierten Bereichen ist, dass ein Slice nicht ungültig werden kann, während
er verwendet wird.

[ch13]: ch13-02-iterators.html
[ch6]: ch06-02-match.html#patterns-that-bind-to-values
[strings]: ch08-02-strings.html#storing-utf-8-encoded-text-with-strings
[deref-coercions]: ch15-02-deref.html#implicit-deref-coercions-with-functions-and-methods
