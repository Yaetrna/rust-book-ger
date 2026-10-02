## UTF-8-kodierten Text in Strings speichern {#storing-utf-8-encoded-text-with-strings}

Über Strings haben wir in Kapitel 4 gesprochen, aber jetzt sehen wir sie uns
genauer an. Neue Rustaceans bleiben bei Strings häufig aus einer Kombination von
drei Gründen hängen: der Neigung von Rust, mögliche Fehler offenzulegen, der
Tatsache, dass Strings eine kompliziertere Datenstruktur sind, als viele
Programmierende annehmen, und UTF-8. Diese Faktoren wirken auf eine Weise
zusammen, die schwierig erscheinen kann, wenn du von anderen Programmiersprachen
kommst.

Wir besprechen Strings im Zusammenhang mit Collections, weil Strings als
Collection von Bytes implementiert sind, plus einige Methoden, die nützliche
Funktionalität bereitstellen, wenn diese Bytes als Text interpretiert werden. In
diesem Abschnitt sprechen wir über die Operationen auf `String`, die jeder
Collection-Typ hat, etwa Erstellen, Aktualisieren und Lesen. Außerdem besprechen
wir, worin sich `String` von den anderen Collections unterscheidet, nämlich dass
die Indexierung eines `String` dadurch kompliziert wird, dass Menschen und
Computer `String`-Daten unterschiedlich interpretieren.

<!-- Old headings. Do not remove or links may break. -->

<a id="what-is-a-string"></a>

### Strings definieren {#defining-strings}

Zuerst definieren wir, was wir mit dem Begriff _String_ meinen. Rust hat in der
Kernsprache nur einen String-Typ, nämlich den String-Slice `str`, der meist in
seiner ausgeliehenen (_borrowed_) Form `&str` zu sehen ist. In Kapitel 4 haben
wir über String-Slices gesprochen, also Referenzen auf UTF-8-kodierte
String-Daten, die woanders gespeichert sind. String-Literale zum Beispiel werden
in der Binärdatei des Programms gespeichert und sind daher String-Slices.

Der Typ `String`, der von der Standardbibliothek von Rust bereitgestellt wird
statt in die Kernsprache eingebaut zu sein, ist ein wachstumsfähiger,
veränderlicher (_mutable_), besitzender, UTF-8-kodierter String-Typ. Wenn
Rustaceans in Rust von „Strings“ sprechen, können sie entweder den Typ `String`
oder den String-Slice-Typ `&str` meinen, nicht nur einen dieser Typen. Obwohl es
in diesem Abschnitt hauptsächlich um `String` geht, werden beide Typen in der
Standardbibliothek von Rust intensiv verwendet, und sowohl `String` als auch
String-Slices sind UTF-8-kodiert.

### Einen neuen String erstellen {#creating-a-new-string}

Viele der Operationen, die es für `Vec<T>` gibt, sind auch für `String`
verfügbar, weil `String` tatsächlich als Wrapper um einen Vektor von Bytes
implementiert ist, mit einigen zusätzlichen Garantien, Einschränkungen und
Fähigkeiten. Ein Beispiel für eine Funktion, die mit `Vec<T>` und `String`
gleich funktioniert, ist die Funktion `new` zum Erzeugen einer Instanz, wie in
Listing 8-11 gezeigt.

<Listing number="8-11" caption="Einen neuen, leeren `String` erstellen">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-11/src/main.rs:here}}
```

</Listing>

Diese Zeile erstellt einen neuen, leeren String namens `s`, in den wir dann
Daten laden können. Oft haben wir Anfangsdaten, mit denen der String beginnen
soll. Dafür verwenden wir die Methode `to_string`, die für jeden Typ verfügbar
ist, der den Trait `Display` implementiert, wie es String-Literale tun. Listing
8-12 zeigt zwei Beispiele.

<Listing number="8-12" caption="Mit der Methode `to_string` einen `String` aus einem String-Literal erstellen">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-12/src/main.rs:here}}
```

</Listing>

Dieser Code erstellt einen String, der `initial contents` enthält.

Wir können auch die Funktion `String::from` verwenden, um einen `String` aus
einem String-Literal zu erstellen. Der Code in Listing 8-13 ist gleichwertig zum
Code in Listing 8-12, der `to_string` verwendet.

<Listing number="8-13" caption="Mit der Funktion `String::from` einen `String` aus einem String-Literal erstellen">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-13/src/main.rs:here}}
```

</Listing>

Da Strings für so viele Dinge verwendet werden, können wir viele verschiedene
generische APIs für Strings verwenden, was uns viele Möglichkeiten bietet.
Einige davon wirken vielleicht überflüssig, aber sie haben alle ihre
Berechtigung! In diesem Fall tun `String::from` und `to_string` dasselbe, welche
du wählst, ist also eine Frage des Stils und der Lesbarkeit.

Denk daran, dass Strings UTF-8-kodiert sind, also können wir beliebige korrekt
kodierte Daten in ihnen ablegen, wie in Listing 8-14 gezeigt.

<Listing number="8-14" caption="Grüße in verschiedenen Sprachen in Strings speichern">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-14/src/main.rs:here}}
```

</Listing>

All das sind gültige `String`-Werte.

### Einen String aktualisieren {#updating-a-string}

Ein `String` kann wachsen und sein Inhalt kann sich ändern, genau wie der Inhalt
eines `Vec<T>`, wenn du weitere Daten hineinschiebst. Außerdem kannst du bequem
den Operator `+` oder das Makro `format!` verwenden, um `String`-Werte zu
verketten.

<!-- Old headings. Do not remove or links may break. -->

<a id="appending-to-a-string-with-push_str-and-push"></a>

#### Mit `push_str` oder `push` anhängen {#appending-with-push_str-or-push}

Wir können einen `String` wachsen lassen, indem wir mit der Methode `push_str`
einen String-Slice anhängen, wie in Listing 8-15 gezeigt.

<Listing number="8-15" caption="Mit der Methode `push_str` einen String-Slice an einen `String` anhängen">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-15/src/main.rs:here}}
```

</Listing>

Nach diesen beiden Zeilen enthält `s` den Text `foobar`. Die Methode `push_str`
nimmt einen String-Slice, weil wir nicht unbedingt die Ownership des Parameters
übernehmen wollen. Im Code in Listing 8-16 wollen wir zum Beispiel `s2`
weiterverwenden können, nachdem wir seinen Inhalt an `s1` angehängt haben.

<Listing number="8-16" caption="Einen String-Slice verwenden, nachdem sein Inhalt an einen `String` angehängt wurde">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-16/src/main.rs:here}}
```

</Listing>

Würde die Methode `push_str` die Ownership von `s2` übernehmen, könnten wir
seinen Wert in der letzten Zeile nicht ausgeben. Dieser Code funktioniert aber
wie erwartet!

Die Methode `push` nimmt ein einzelnes Zeichen als Parameter und fügt es dem
`String` hinzu. Listing 8-17 fügt einem `String` mit der Methode `push` den
Buchstaben _l_ hinzu.

<Listing number="8-17" caption="Einem `String`-Wert mit `push` ein Zeichen hinzufügen">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-17/src/main.rs:here}}
```

</Listing>

Danach enthält `s` den Text `lol`.

<!-- Old headings. Do not remove or links may break. -->

<a id="concatenation-with-the--operator-or-the-format-macro"></a>

#### Mit `+` oder `format!` verketten {#concatenating-with--or-format}

Oft willst du zwei vorhandene Strings kombinieren. Eine Möglichkeit dafür ist
der Operator `+`, wie in Listing 8-18 gezeigt.

<Listing number="8-18" caption="Mit dem Operator `+` zwei `String`-Werte zu einem neuen `String`-Wert kombinieren">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-18/src/main.rs:here}}
```

</Listing>

Der String `s3` enthält `Hello, world!`. Dass `s1` nach der Addition nicht mehr
gültig ist und dass wir eine Referenz auf `s2` verwendet haben, hat mit der
Signatur der Methode zu tun, die aufgerufen wird, wenn wir den Operator `+`
verwenden. Der Operator `+` verwendet die Methode `add`, deren Signatur ungefähr
so aussieht:

```rust,ignore
fn add(self, s: &str) -> String {
```

In der Standardbibliothek ist `add` mit Generics und assoziierten Typen
definiert. Hier haben wir konkrete Typen eingesetzt, und genau das passiert,
wenn wir diese Methode mit `String`-Werten aufrufen. Generics besprechen wir in
Kapitel 10. Diese Signatur liefert uns die Hinweise, die wir brauchen, um die
kniffligen Stellen des Operators `+` zu verstehen.

Erstens hat `s2` ein `&`, das heißt, wir addieren eine Referenz auf den zweiten
String zum ersten String. Das liegt am Parameter `s` der Funktion `add`: Wir
können nur einen String-Slice zu einem `String` addieren; zwei `String`-Werte
können wir nicht addieren. Aber Moment – der Typ von `&s2` ist `&String`, nicht
`&str`, wie im zweiten Parameter von `add` angegeben. Warum kompiliert Listing
8-18 also?

Wir können `&s2` im Aufruf von `add` verwenden, weil der Compiler das Argument
`&String` in einen `&str` umwandeln (_coerce_) kann. Wenn wir die Methode `add`
aufrufen, verwendet Rust eine Deref-Coercion, die hier `&s2` in `&s2[..]`
umwandelt. Deref-Coercion besprechen wir ausführlicher in Kapitel 15. Da `add`
die Ownership des Parameters `s` nicht übernimmt, ist `s2` nach dieser Operation
immer noch ein gültiger `String`.

<!-- BEGIN INTERVENTION: f1ab2171-96f0-4380-b16d-9055a9a00415 -->

Zweitens sehen wir in der Signatur, dass `add` die Ownership von `self`
übernimmt, weil `self` _kein_ `&` hat. Das bedeutet, dass `s1` in Listing 8-18
in den Aufruf von `add` verschoben (_moved_) wird und danach nicht mehr gültig
ist. Obwohl `let s3 = s1 + &s2;` so aussieht, als würde es beide Strings
kopieren und einen neuen erzeugen, tut diese Anweisung stattdessen Folgendes:

1. `add` übernimmt die Ownership von `s1`,
2. hängt eine Kopie des Inhalts von `s2` an `s1` an
3. und gibt dann die Ownership von `s1` zurück.

Hat `s1` genug Kapazität für `s2`, finden keine Speicherallokationen statt. Hat
`s1` dagegen nicht genug Kapazität für `s2`, nimmt `s1` intern eine größere
Speicherallokation vor, in die beide Strings passen.

<!-- END INTERVENTION -->

Wenn wir mehrere Strings verketten müssen, wird das Verhalten des Operators `+`
unhandlich:

```rust
{{#rustdoc_include ../listings/ch08-common-collections/no-listing-01-concat-multiple-strings/src/main.rs:here}}
```

An dieser Stelle ist `s` gleich `tic-tac-toe`. Bei all den Zeichen `+` und `"`
ist schwer zu erkennen, was vor sich geht. Um Strings auf kompliziertere Weise
zu kombinieren, können wir stattdessen das Makro `format!` verwenden:

```rust
{{#rustdoc_include ../listings/ch08-common-collections/no-listing-02-format/src/main.rs:here}}
```

Auch dieser Code setzt `s` auf `tic-tac-toe`. Das Makro `format!` funktioniert
wie `println!`, gibt die Ausgabe aber nicht auf dem Bildschirm aus, sondern gibt
einen `String` mit dem Inhalt zurück. Die Version des Codes mit `format!` ist
viel leichter zu lesen, und der Code, den das Makro `format!` erzeugt, verwendet
Referenzen, sodass dieser Aufruf die Ownership keines seiner Parameter
übernimmt.

{{#quiz ../quizzes/ch08-02-string-sec1.toml}}

### Strings indexieren {#indexing-into-strings}

In vielen anderen Programmiersprachen ist es eine gültige und gängige Operation,
auf einzelne Zeichen eines Strings über ihren Index zuzugreifen. Wenn du in Rust
aber versuchst, mit der Indexierungssyntax auf Teile eines `String` zuzugreifen,
bekommst du einen Fehler. Betrachte den ungültigen Code in Listing 8-19.

<Listing number="8-19" caption="Versuch, die Indexierungssyntax mit einem `String` zu verwenden">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-19/src/main.rs:here}}
```

</Listing>

Dieser Code führt zu folgendem Fehler:

```console
{{#include ../listings/ch08-common-collections/listing-08-19/output.txt}}
```

Der Fehler sagt alles: Strings in Rust unterstützen keine Indexierung. Aber
warum nicht? Um diese Frage zu beantworten, müssen wir besprechen, wie Rust
Strings im Speicher ablegt.

#### Interne Darstellung {#internal-representation}

Ein `String` ist ein Wrapper um einen `Vec<u8>`. Sehen wir uns einige unserer
korrekt UTF-8-kodierten Beispielstrings aus Listing 8-14 an. Zuerst diesen:

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-14/src/main.rs:spanish}}
```

In diesem Fall ist `len` gleich `4`, das heißt, der Vektor, der den String
`"Hola"` speichert, ist 4 Bytes lang. Jeder dieser Buchstaben belegt in UTF-8
kodiert 1 Byte. Die folgende Zeile überrascht dich aber vielleicht (beachte,
dass dieser String mit dem kyrillischen Großbuchstaben _Se_ beginnt, nicht mit
der Zahl 3):

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-14/src/main.rs:russian}}
```

Wenn man dich fragen würde, wie lang der String ist, würdest du vielleicht 12
sagen. Tatsächlich lautet die Antwort von Rust 24: So viele Bytes braucht man,
um „Здравствуйте“ in UTF-8 zu kodieren, weil jeder Unicode-Skalarwert in diesem
String 2 Bytes Speicher belegt. Ein Index in die Bytes des Strings entspricht
daher nicht immer einem gültigen Unicode-Skalarwert. Betrachte zur
Veranschaulichung diesen ungültigen Rust-Code:

```rust,ignore,does_not_compile
let hello = "Здравствуйте";
let answer = &hello[0];
```

Du weißt bereits, dass `answer` nicht `З` sein wird, der erste Buchstabe. In
UTF-8 kodiert ist das erste Byte von `З` gleich `208` und das zweite `151`, also
müsste `answer` eigentlich `208` sein, aber `208` ist für sich allein kein
gültiges Zeichen. `208` zurückzugeben ist wahrscheinlich nicht das, was jemand
will, der nach dem ersten Buchstaben dieses Strings fragt; es sind aber die
einzigen Daten, die Rust an Byte-Index 0 hat. Im Allgemeinen will man nicht,
dass der Byte-Wert zurückgegeben wird, selbst wenn der String nur lateinische
Buchstaben enthält: Wäre `&"hi"[0]` gültiger Code, der den Byte-Wert zurückgibt,
würde er `104` zurückgeben, nicht `h`.

Die Antwort ist also: Um zu vermeiden, dass ein unerwarteter Wert zurückgegeben
wird und Bugs entstehen, die vielleicht nicht sofort entdeckt werden, kompiliert
Rust diesen Code gar nicht erst und verhindert Missverständnisse früh im
Entwicklungsprozess.

<!-- Old headings. Do not remove or links may break. -->

<a id="bytes-and-scalar-values-and-grapheme-clusters-oh-my"></a>

#### Bytes, Skalarwerte und Graphem-Cluster {#bytes-scalar-values-and-grapheme-clusters}

Ein weiterer Punkt zu UTF-8 ist, dass es aus Sicht von Rust eigentlich drei
relevante Arten gibt, Strings zu betrachten: als Bytes, als Skalarwerte und als
Graphem-Cluster (das, was wir am ehesten _Buchstaben_ nennen würden).

Betrachten wir das Hindi-Wort „नमस्ते“ in der Devanagari-Schrift, wird es als
Vektor von `u8`-Werten gespeichert, der so aussieht:

```text
[224, 164, 168, 224, 164, 174, 224, 164, 184, 224, 165, 141, 224, 164, 164,
224, 165, 135]
```

Das sind 18 Bytes, und so speichern Computer diese Daten letztlich. Betrachten
wir sie als Unicode-Skalarwerte, also als das, was der Typ `char` in Rust ist,
sehen diese Bytes so aus:

```text
['न', 'म', 'स', '्', 'त', 'े']
```

Hier gibt es sechs `char`-Werte, aber der vierte und der sechste sind keine
Buchstaben: Es sind diakritische Zeichen, die für sich allein keinen Sinn
ergeben. Betrachten wir sie schließlich als Graphem-Cluster, erhalten wir das,
was ein Mensch als die vier Buchstaben bezeichnen würde, aus denen das
Hindi-Wort besteht:

```text
["न", "म", "स्", "ते"]
```

Rust bietet verschiedene Möglichkeiten, die rohen String-Daten zu
interpretieren, die Computer speichern, sodass jedes Programm die Interpretation
wählen kann, die es braucht, egal in welcher menschlichen Sprache die Daten
vorliegen.

Ein letzter Grund, warum Rust uns nicht erlaubt, einen `String` zu indexieren,
um ein Zeichen zu erhalten, ist, dass von Indexierungsoperationen erwartet wird,
dass sie immer konstante Zeit (O(1)) brauchen. Bei einem `String` lässt sich
diese Performance aber nicht garantieren, weil Rust den Inhalt vom Anfang bis
zum Index durchlaufen müsste, um festzustellen, wie viele gültige Zeichen es
gibt.

### Strings in Slices zerlegen {#slicing-strings}

Einen String zu indexieren ist oft keine gute Idee, weil nicht klar ist, welchen
Rückgabetyp die String-Indexierung haben sollte: einen Byte-Wert, ein Zeichen,
ein Graphem-Cluster oder einen String-Slice. Wenn du wirklich Indizes verwenden
musst, um String-Slices zu erzeugen, verlangt Rust daher, dass du genauer
angibst, was du willst.

Statt mit `[]` und einer einzelnen Zahl zu indexieren, kannst du `[]` mit einem
Bereich (_range_) verwenden, um einen String-Slice zu erzeugen, der bestimmte
Bytes enthält:

```rust
let hello = "Здравствуйте";

let s = &hello[0..4];
```

Hier ist `s` ein `&str`, der die ersten 4 Bytes des Strings enthält. Wir haben
vorhin erwähnt, dass jedes dieser Zeichen 2 Bytes groß ist, also ist `s` gleich
`Зд`.

Würden wir versuchen, mit etwas wie `&hello[0..1]` nur einen Teil der Bytes
eines Zeichens herauszuschneiden, würde Rust zur Laufzeit einen Panic auslösen,
genauso wie bei einem Zugriff auf einen ungültigen Index in einem Vektor:

```console
{{#include ../listings/ch08-common-collections/output-only-01-not-char-boundary/output.txt}}
```

Sei vorsichtig, wenn du String-Slices mit Bereichen erzeugst, denn das kann dein
Programm zum Absturz bringen.

<!-- Old headings. Do not remove or links may break. -->

<a id="methods-for-iterating-over-strings"></a>

### Über Strings iterieren {#iterating-over-strings}

Am besten arbeitest du mit Teilen von Strings, indem du explizit angibst, ob du
Zeichen oder Bytes willst. Für einzelne Unicode-Skalarwerte verwendest du die
Methode `chars`. Ruft man `chars` auf „Зд“ auf, werden zwei Werte vom Typ `char`
getrennt und zurückgegeben, und du kannst über das Ergebnis iterieren, um auf
jedes Element zuzugreifen:

```rust
for c in "Зд".chars() {
    println!("{c}");
}
```

Dieser Code gibt Folgendes aus:

```text
З
д
```

Alternativ gibt die Methode `bytes` jedes rohe Byte zurück, was für deinen
Anwendungsbereich passend sein könnte:

```rust
for b in "Зд".bytes() {
    println!("{b}");
}
```

Dieser Code gibt die 4 Bytes aus, aus denen dieser String besteht:

```text
208
151
208
180
```

Denk aber unbedingt daran, dass gültige Unicode-Skalarwerte aus mehr als 1 Byte
bestehen können.

Graphem-Cluster aus Strings zu gewinnen, wie bei der Devanagari-Schrift, ist
komplex, daher stellt die Standardbibliothek diese Funktionalität nicht bereit.
Auf [crates.io](https://crates.io/)<!-- ignore --> gibt es Crates, falls du
diese Funktionalität brauchst.

<!-- Old headings. Do not remove or links may break. -->

<a id="strings-are-not-so-simple"></a>

### Mit der Komplexität von Strings umgehen {#handling-the-complexities-of-strings}

Zusammengefasst: Strings sind kompliziert. Verschiedene Programmiersprachen
treffen unterschiedliche Entscheidungen darüber, wie sie diese Komplexität den
Programmierenden präsentieren. Rust hat sich dafür entschieden, den korrekten
Umgang mit `String`-Daten zum Standardverhalten aller Rust-Programme zu machen.
Das bedeutet, dass Programmierende sich im Voraus mehr Gedanken über den Umgang
mit UTF-8-Daten machen müssen. Dieser Kompromiss legt mehr von der Komplexität
von Strings offen, als in anderen Programmiersprachen sichtbar ist, erspart dir
aber, später im Entwicklungszyklus Fehler mit Nicht-ASCII-Zeichen behandeln zu
müssen.

Die gute Nachricht ist, dass die Standardbibliothek viel Funktionalität bietet,
die auf den Typen `String` und `&str` aufbaut und hilft, diese komplexen
Situationen korrekt zu behandeln. Sieh dir unbedingt die Dokumentation an, etwa
zu nützlichen Methoden wie `contains` zum Suchen in einem String und `replace`
zum Ersetzen von Teilen eines Strings durch einen anderen String.

Wechseln wir zu etwas etwas weniger Komplexem: Hash-Maps!

{{#quiz ../quizzes/ch08-02-string-sec2.toml}}
