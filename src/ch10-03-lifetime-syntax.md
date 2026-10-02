## Referenzen mit Lifetimes validieren {#validating-references-with-lifetimes}

Lifetimes sind eine weitere Art von Generics, die wir bereits verwendet haben.
Statt sicherzustellen, dass ein Typ das gewünschte Verhalten hat, stellen
Lifetimes sicher, dass Referenzen so lange gültig sind, wie wir sie brauchen.

Ein Detail, das wir im Abschnitt
[„Referenzen und Borrowing“][references-and-borrowing]<!-- ignore --> in Kapitel
4 nicht besprochen haben, ist, dass jede Referenz in Rust eine Lifetime hat,
also den Gültigkeitsbereich (_scope_), in dem diese Referenz gültig ist.
Meistens sind Lifetimes implizit und werden abgeleitet, genau wie Typen meistens
abgeleitet werden. Typen müssen wir nur annotieren, wenn mehrere Typen möglich
sind. Ähnlich müssen wir Lifetimes annotieren, wenn die Lifetimes von Referenzen
auf verschiedene Weise zusammenhängen könnten. Rust verlangt, dass wir diese
Beziehungen mit generischen Lifetime-Parametern annotieren, um sicherzustellen,
dass die tatsächlichen Referenzen, die zur Laufzeit verwendet werden, auf jeden
Fall gültig sind.

Lifetimes zu annotieren ist ein Konzept, das die meisten anderen
Programmiersprachen gar nicht kennen, daher wird es sich ungewohnt anfühlen. Wir
behandeln Lifetimes in diesem Kapitel zwar nicht vollständig, besprechen aber
gängige Situationen, in denen dir die Lifetime-Syntax begegnen kann, damit du
dich mit dem Konzept vertraut machen kannst.

<!-- Old headings. Do not remove or links may break. -->

<a id="preventing-dangling-references-with-lifetimes"></a>

### Hängende Referenzen {#dangling-references}

Das Hauptziel von Lifetimes ist, hängende Referenzen (_dangling references_) zu
verhindern. Dürften sie existieren, würde ein Programm auf andere Daten
verweisen als die, auf die es verweisen soll. Betrachte das Programm in Listing
10-16, das einen äußeren und einen inneren Gültigkeitsbereich hat.

<!-- TODO(aquascope): support for nested scopes -->
<Listing number="10-16" caption="Versuch, eine Referenz zu verwenden, deren Wert den Gültigkeitsbereich verlassen hat">

```rust,ignore,does_not_compile
fn main() {
    let r;

    {
        let x = 5;
        r = &x;
    }

    println!("r: {}", r);
}
```

</Listing>

> Note: Die Beispiele in den Listings 10-16, 10-17 und 10-23 deklarieren
> Variablen, ohne ihnen einen Anfangswert zu geben, sodass der Variablenname im
> äußeren Gültigkeitsbereich existiert. Auf den ersten Blick scheint das im
> Widerspruch dazu zu stehen, dass Rust keine Nullwerte hat. Wenn wir aber
> versuchen, eine Variable zu verwenden, bevor wir ihr einen Wert gegeben haben,
> erhalten wir einen Fehler zur Kompilierzeit, was zeigt, dass Rust tatsächlich
> keine Nullwerte erlaubt.

Der äußere Gültigkeitsbereich deklariert eine Variable namens `r` ohne
Anfangswert, und der innere Gültigkeitsbereich deklariert eine Variable namens
`x` mit dem Anfangswert `5`. Im inneren Gültigkeitsbereich versuchen wir, den
Wert von `r` auf eine Referenz auf `x` zu setzen. Dann endet der innere
Gültigkeitsbereich, und wir versuchen, den Wert in `r` auszugeben. Dieser Code
kompiliert nicht, weil der Wert, auf den `r` verweist, den Gültigkeitsbereich
verlassen hat, bevor wir versuchen, ihn zu verwenden. Hier ist die
Fehlermeldung:

```console
{{#include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-16/output.txt}}
```

Die Fehlermeldung besagt, dass die Variable `x` „nicht lange genug lebt“ (_does
not live long enough_). Der Grund ist, dass `x` den Gültigkeitsbereich verlässt,
wenn der innere Gültigkeitsbereich in Zeile 7 endet. `r` ist im äußeren
Gültigkeitsbereich aber weiterhin gültig; da sein Gültigkeitsbereich größer ist,
sagen wir, dass es „länger lebt“. Würde Rust diesen Code zulassen, würde `r` auf
Speicher verweisen, der freigegeben wurde, als `x` den Gültigkeitsbereich
verlassen hat, und alles, was wir mit `r` versuchen würden, würde nicht korrekt
funktionieren. Wie stellt Rust also fest, dass dieser Code ungültig ist? Es
verwendet einen Borrow-Checker.

### Der Borrow-Checker stellt sicher, dass Daten ihre Referenzen überleben {#the-borrow-checker-ensures-data-outlives-its-references}

Der Rust-Compiler hat einen _Borrow-Checker_, der Gültigkeitsbereiche
vergleicht, um festzustellen, ob alle Ausleihen (_borrows_) gültig sind. Listing
10-17 zeigt denselben Code wie Listing 10-16, aber mit Annotationen, die die
Lifetimes der Variablen zeigen.

<Listing number="10-17" caption="Annotationen der Lifetimes von `r` und `x`, benannt als `'a` bzw. `'b`">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-17/src/main.rs}}
```

</Listing>

Hier haben wir die Lifetime von `r` mit `'a` und die Lifetime von `x` mit `'b`
annotiert. Wie du siehst, ist der innere `'b`-Block viel kleiner als der äußere
Lifetime-Block `'a`. Zur Kompilierzeit vergleicht Rust die Größe der beiden
Lifetimes und sieht, dass `r` die Lifetime `'a` hat, aber auf Speicher mit der
Lifetime `'b` verweist. Das Programm wird zurückgewiesen, weil `'b` kürzer ist
als `'a`: Das Ziel der Referenz lebt nicht so lange wie die Referenz.

Listing 10-18 korrigiert den Code so, dass er keine hängende Referenz hat und
ohne Fehler kompiliert.

<Listing number="10-18" caption="Eine gültige Referenz, weil die Daten eine längere Lifetime haben als die Referenz">

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-18/src/main.rs}}
```

</Listing>

Hier hat `x` die Lifetime `'b`, die in diesem Fall größer ist als `'a`. Das
bedeutet, dass `r` auf `x` verweisen kann, weil Rust weiß, dass die Referenz in
`r` immer gültig ist, solange `x` gültig ist.

Nachdem du weißt, wo die Lifetimes von Referenzen liegen und wie Rust Lifetimes
analysiert, um sicherzustellen, dass Referenzen immer gültig sind, sehen wir uns
generische Lifetimes in Funktionsparametern und Rückgabewerten an.

### Generische Lifetimes in Funktionen {#generic-lifetimes-in-functions}

Wir schreiben eine Funktion, die den längeren von zwei String-Slices zurückgibt.
Diese Funktion nimmt zwei String-Slices und gibt einen einzelnen String-Slice
zurück. Nachdem wir die Funktion `longest` implementiert haben, sollte der Code
in Listing 10-19 `The longest string is abcd` ausgeben.

<Listing number="10-19" file-name="src/main.rs" caption="Eine Funktion `main`, die die Funktion `longest` aufruft, um den längeren von zwei String-Slices zu finden">

```rust,ignore
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-19/src/main.rs}}
```

</Listing>

Beachte, dass die Funktion String-Slices nehmen soll, also Referenzen, und keine
Strings, weil die Funktion `longest` nicht die Ownership ihrer Parameter
übernehmen soll. Mehr dazu, warum die Parameter in Listing 10-19 die richtigen
sind, findest du in
[„String-Slices als Parameter“][string-slices-as-parameters]<!-- ignore --> in
Kapitel 4.

Wenn wir versuchen, die Funktion `longest` wie in Listing 10-20 zu
implementieren, kompiliert sie nicht.

<Listing number="10-20" file-name="src/main.rs" caption="Eine Implementierung der Funktion `longest`, die den längeren von zwei String-Slices zurückgibt, aber noch nicht kompiliert">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-20/src/main.rs:here}}
```

</Listing>

Stattdessen erhalten wir folgenden Fehler, der von Lifetimes spricht:

```console
{{#include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-20/output.txt}}
```

Der Hilfetext zeigt, dass der Rückgabetyp einen generischen Lifetime-Parameter
braucht, weil Rust nicht erkennen kann, ob sich die zurückgegebene Referenz auf
`x` oder auf `y` bezieht. Tatsächlich wissen wir das auch nicht, denn der
`if`-Block im Rumpf dieser Funktion gibt eine Referenz auf `x` zurück und der
`else`-Block eine Referenz auf `y`!

Wenn wir diese Funktion definieren, kennen wir die konkreten Werte nicht, die an
diese Funktion übergeben werden, also wissen wir nicht, ob der `if`-Fall oder
der `else`-Fall ausgeführt wird. Wir kennen auch die konkreten Lifetimes der
übergebenen Referenzen nicht, können uns also nicht wie in den Listings 10-17
und 10-18 die Gültigkeitsbereiche ansehen, um festzustellen, ob die
zurückgegebene Referenz immer gültig ist. Auch der Borrow-Checker kann das nicht
feststellen, weil er nicht weiß, wie die Lifetimes von `x` und `y` mit der
Lifetime des Rückgabewerts zusammenhängen. Um diesen Fehler zu beheben, fügen
wir generische Lifetime-Parameter hinzu, die die Beziehung zwischen den
Referenzen definieren, damit der Borrow-Checker seine Analyse durchführen kann.

### Syntax von Lifetime-Annotationen {#lifetime-annotation-syntax}

Lifetime-Annotationen ändern nicht, wie lange eine der Referenzen lebt. Sie
beschreiben vielmehr die Beziehungen der Lifetimes mehrerer Referenzen
zueinander, ohne die Lifetimes zu beeinflussen. So wie Funktionen jeden Typ
akzeptieren können, wenn die Signatur einen generischen Typparameter angibt,
können Funktionen Referenzen mit jeder Lifetime akzeptieren, wenn ein
generischer Lifetime-Parameter angegeben ist.

Lifetime-Annotationen haben eine etwas ungewöhnliche Syntax: Die Namen von
Lifetime-Parametern müssen mit einem Apostroph (`'`) beginnen und sind
normalerweise kleingeschrieben und sehr kurz, wie generische Typen. Die meisten
verwenden für die erste Lifetime-Annotation den Namen `'a`. Wir setzen
Annotationen von Lifetime-Parametern hinter das `&` einer Referenz und trennen
die Annotation durch ein Leerzeichen vom Typ der Referenz.

Hier sind einige Beispiele – eine Referenz auf einen `i32` ohne
Lifetime-Parameter, eine Referenz auf einen `i32` mit einem Lifetime-Parameter
namens `'a` und eine veränderliche (_mutable_) Referenz auf einen `i32`, die
ebenfalls die Lifetime `'a` hat:

```rust,ignore
&i32        // a reference
&'a i32     // a reference with an explicit lifetime
&'a mut i32 // a mutable reference with an explicit lifetime
```

Eine einzelne Lifetime-Annotation hat für sich genommen nicht viel Bedeutung,
weil die Annotationen Rust mitteilen sollen, wie die generischen
Lifetime-Parameter mehrerer Referenzen zueinander in Beziehung stehen. Sehen wir
uns an, wie die Lifetime-Annotationen im Kontext der Funktion `longest`
zueinander in Beziehung stehen.

<!-- Old headings. Do not remove or links may break. -->

<a id="lifetime-annotations-in-function-signatures"></a>

### In Funktionssignaturen {#in-function-signatures}

Um Lifetime-Annotationen in Funktionssignaturen zu verwenden, müssen wir die
generischen Lifetime-Parameter in spitzen Klammern zwischen Funktionsname und
Parameterliste deklarieren, genau wie bei generischen Typparametern.

Die Signatur soll folgende Einschränkung ausdrücken: Die zurückgegebene Referenz
ist gültig, solange beide Parameter gültig sind. Das ist die Beziehung zwischen
den Lifetimes der Parameter und des Rückgabewerts. Wir nennen die Lifetime `'a`
und fügen sie dann zu jeder Referenz hinzu, wie in Listing 10-21 gezeigt.

<Listing number="10-21" file-name="src/main.rs" caption="Die Definition der Funktion `longest`, die festlegt, dass alle Referenzen in der Signatur dieselbe Lifetime `'a` haben müssen">

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-21/src/main.rs:here}}
```

</Listing>

Dieser Code sollte kompilieren und das gewünschte Ergebnis liefern, wenn wir ihn
mit der Funktion `main` aus Listing 10-19 verwenden.

Die Funktionssignatur teilt Rust jetzt mit, dass die Funktion für eine Lifetime
`'a` zwei Parameter nimmt, die beide String-Slices sind, die mindestens so lange
leben wie die Lifetime `'a`. Die Funktionssignatur teilt Rust außerdem mit, dass
der String-Slice, den die Funktion zurückgibt, mindestens so lange lebt wie die
Lifetime `'a`. In der Praxis bedeutet das, dass die Lifetime der Referenz, die
die Funktion `longest` zurückgibt, gleich der kleineren der Lifetimes der Werte
ist, auf die die Funktionsargumente verweisen. Diese Beziehungen soll Rust bei
der Analyse dieses Codes verwenden.

Denk daran: Wenn wir die Lifetime-Parameter in dieser Funktionssignatur angeben,
ändern wir nicht die Lifetimes der übergebenen oder zurückgegebenen Werte.
Vielmehr legen wir fest, dass der Borrow-Checker alle Werte zurückweisen soll,
die diese Einschränkungen nicht einhalten. Beachte, dass die Funktion `longest`
nicht genau wissen muss, wie lange `x` und `y` leben, sondern nur, dass sich für
`'a` ein Gültigkeitsbereich einsetzen lässt, der diese Signatur erfüllt.

Wenn wir Lifetimes in Funktionen annotieren, stehen die Annotationen in der
Funktionssignatur, nicht im Funktionsrumpf. Die Lifetime-Annotationen werden
Teil des Vertrags der Funktion, ähnlich wie die Typen in der Signatur. Dass
Funktionssignaturen den Lifetime-Vertrag enthalten, bedeutet, dass die Analyse
des Rust-Compilers einfacher sein kann. Gibt es ein Problem mit der Annotation
einer Funktion oder mit ihrem Aufruf, können die Compilerfehler genauer auf den
Teil unseres Codes und die Einschränkungen verweisen. Würde der Rust-Compiler
stattdessen mehr darüber ableiten, welche Beziehungen der Lifetimes wir
beabsichtigt haben, könnte er vielleicht nur auf eine Verwendung unseres Codes
verweisen, die viele Schritte von der Ursache des Problems entfernt ist.

Wenn wir konkrete Referenzen an `longest` übergeben, ist die konkrete Lifetime,
die für `'a` eingesetzt wird, der Teil des Gültigkeitsbereichs von `x`, der sich
mit dem Gültigkeitsbereich von `y` überschneidet. Mit anderen Worten: Die
generische Lifetime `'a` erhält die konkrete Lifetime, die gleich der kleineren
der Lifetimes von `x` und `y` ist. Da wir die zurückgegebene Referenz mit
demselben Lifetime-Parameter `'a` annotiert haben, ist auch die zurückgegebene
Referenz für die Dauer der kleineren der Lifetimes von `x` und `y` gültig.

Sehen wir uns an, wie die Lifetime-Annotationen die Funktion `longest`
einschränken, indem wir Referenzen mit unterschiedlichen konkreten Lifetimes
übergeben. Listing 10-22 ist ein einfaches Beispiel.

<Listing number="10-22" file-name="src/main.rs" caption="Die Funktion `longest` mit Referenzen auf `String`-Werte verwenden, die unterschiedliche konkrete Lifetimes haben">

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-22/src/main.rs:here}}
```

</Listing>

In diesem Beispiel ist `string1` bis zum Ende des äußeren Gültigkeitsbereichs
gültig, `string2` bis zum Ende des inneren Gültigkeitsbereichs, und `result`
verweist auf etwas, das bis zum Ende des inneren Gültigkeitsbereichs gültig ist.
Führ diesen Code aus, und du wirst sehen, dass der Borrow-Checker zustimmt; er
kompiliert und gibt `The longest string
is long string is long` aus.

Als Nächstes probieren wir ein Beispiel, das zeigt, dass die Lifetime der
Referenz in `result` die kleinere Lifetime der beiden Argumente sein muss. Wir
verschieben die Deklaration der Variable `result` aus dem inneren
Gültigkeitsbereich heraus, lassen die Zuweisung des Werts an die Variable
`result` aber im Gültigkeitsbereich mit `string2`. Dann verschieben wir das
`println!`, das `result` verwendet, aus dem inneren Gültigkeitsbereich heraus
hinter dessen Ende. Der Code in Listing 10-23 kompiliert nicht.

<Listing number="10-23" file-name="src/main.rs" caption="Versuch, `result` zu verwenden, nachdem `string2` den Gültigkeitsbereich verlassen hat">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-23/src/main.rs:here}}
```

</Listing>

Wenn wir versuchen, diesen Code zu kompilieren, erhalten wir diesen Fehler:

```console
{{#include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-23/output.txt}}
```

Der Fehler zeigt, dass `string2` bis zum Ende des äußeren Gültigkeitsbereichs
gültig sein müsste, damit `result` für die `println!`-Anweisung gültig ist. Rust
weiß das, weil wir die Lifetimes der Funktionsparameter und Rückgabewerte mit
demselben Lifetime-Parameter `'a` annotiert haben.

Als Menschen können wir uns diesen Code ansehen und erkennen, dass `string1`
länger ist als `string2` und `result` daher eine Referenz auf `string1`
enthalten wird. Da `string1` den Gültigkeitsbereich noch nicht verlassen hat,
ist eine Referenz auf `string1` für die `println!`-Anweisung noch gültig. Der
Compiler kann aber nicht erkennen, dass die Referenz in diesem Fall gültig ist.
Wir haben Rust mitgeteilt, dass die Lifetime der Referenz, die die Funktion
`longest` zurückgibt, gleich der kleineren der Lifetimes der übergebenen
Referenzen ist. Daher verbietet der Borrow-Checker den Code in Listing 10-23,
weil er möglicherweise eine ungültige Referenz enthält.

Versuch, dir weitere Experimente auszudenken, bei denen du die Werte und
Lifetimes der an die Funktion `longest` übergebenen Referenzen variierst und
änderst, wie die zurückgegebene Referenz verwendet wird. Stell vor dem
Kompilieren Hypothesen darüber auf, ob deine Experimente den Borrow-Checker
bestehen werden, und prüf dann, ob du richtig liegst!

{{#quiz ../quizzes/ch10-03-lifetimes-sec1.toml}}

<!-- Old headings. Do not remove or links may break. -->

<a id="thinking-in-terms-of-lifetimes"></a>

### Beziehungen {#relationships}

Wie du Lifetime-Parameter angeben musst, hängt davon ab, was deine Funktion tut.
Würden wir zum Beispiel die Implementierung der Funktion `longest` so ändern,
dass sie immer den ersten Parameter statt des längsten String-Slices zurückgibt,
müssten wir für den Parameter `y` keine Lifetime angeben. Der folgende Code
kompiliert:

<Listing file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-08-only-one-reference-with-lifetime/src/main.rs:here}}
```

</Listing>

Wir haben einen Lifetime-Parameter `'a` für den Parameter `x` und den
Rückgabetyp angegeben, aber nicht für den Parameter `y`, weil die Lifetime von
`y` in keiner Beziehung zur Lifetime von `x` oder des Rückgabewerts steht.

Wenn eine Funktion eine Referenz zurückgibt, muss der Lifetime-Parameter des
Rückgabetyps mit dem Lifetime-Parameter eines der Parameter übereinstimmen.
Verweist die zurückgegebene Referenz _nicht_ auf einen der Parameter, muss sie
auf einen Wert verweisen, der innerhalb dieser Funktion erzeugt wurde. Das wäre
aber eine hängende Referenz, weil der Wert am Ende der Funktion den
Gültigkeitsbereich verlässt. Betrachte diesen Implementierungsversuch der
Funktion `longest`, der nicht kompiliert:

<Listing file-name="src/main.rs">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-09-unrelated-lifetime/src/main.rs:here}}
```

</Listing>

Obwohl wir hier einen Lifetime-Parameter `'a` für den Rückgabetyp angegeben
haben, kompiliert diese Implementierung nicht, weil die Lifetime des
Rückgabewerts überhaupt nicht mit der Lifetime der Parameter zusammenhängt. Hier
ist die Fehlermeldung, die wir erhalten:

```console
{{#include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-09-unrelated-lifetime/output.txt}}
```

Das Problem ist, dass `result` am Ende der Funktion `longest` den
Gültigkeitsbereich verlässt und aufgeräumt wird. Gleichzeitig versuchen wir,
eine Referenz auf `result` aus der Funktion zurückzugeben. Wir können keine
Lifetime-Parameter angeben, die an der hängenden Referenz etwas ändern würden,
und Rust lässt uns keine hängende Referenz erzeugen. In diesem Fall wäre die
beste Lösung, einen besitzenden Datentyp statt einer Referenz zurückzugeben,
sodass die aufrufende Funktion dafür verantwortlich ist, den Wert aufzuräumen.

Letztlich geht es bei der Lifetime-Syntax darum, die Lifetimes verschiedener
Parameter und Rückgabewerte von Funktionen miteinander zu verbinden. Sind sie
verbunden, hat Rust genug Informationen, um speichersichere Operationen zu
erlauben und Operationen zu verbieten, die hängende Zeiger erzeugen oder
anderweitig die Speichersicherheit verletzen würden.

<!-- Old headings. Do not remove or links may break. -->

<a id="lifetime-annotations-in-struct-definitions"></a>

### In Struct-Definitionen {#in-struct-definitions}

Bisher haben alle Structs, die wir definiert haben, besitzende Typen enthalten.
Wir können Structs definieren, die Referenzen enthalten, müssen dann aber an
jeder Referenz in der Struct-Definition eine Lifetime-Annotation hinzufügen.
Listing 10-24 enthält ein Struct namens `ImportantExcerpt`, das einen
String-Slice enthält.

<Listing number="10-24" file-name="src/main.rs" caption="Ein Struct, das eine Referenz enthält und daher eine Lifetime-Annotation braucht">

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-24/src/main.rs}}
```

</Listing>

Dieses Struct hat das einzige Feld `part`, das einen String-Slice enthält, also
eine Referenz. Wie bei generischen Datentypen deklarieren wir den Namen des
generischen Lifetime-Parameters in spitzen Klammern nach dem Namen des Structs,
damit wir den Lifetime-Parameter im Rumpf der Struct-Definition verwenden
können. Diese Annotation bedeutet, dass eine Instanz von `ImportantExcerpt` die
Referenz, die sie in ihrem Feld `part` enthält, nicht überleben kann.

Die Funktion `main` erzeugt hier eine Instanz des Structs `ImportantExcerpt`,
die eine Referenz auf den ersten Satz des `String` enthält, der der Variable
`novel` gehört. Die Daten in `novel` existieren, bevor die Instanz von
`ImportantExcerpt` erzeugt wird. Außerdem verlässt `novel` den
Gültigkeitsbereich erst, nachdem `ImportantExcerpt` den Gültigkeitsbereich
verlassen hat, daher ist die Referenz in der Instanz von `ImportantExcerpt`
gültig.

### Lifetime-Elision {#lifetime-elision}

Du hast gelernt, dass jede Referenz eine Lifetime hat und dass du für Funktionen
oder Structs, die Referenzen verwenden, Lifetime-Parameter angeben musst. Wir
hatten aber in Listing 4-9 eine Funktion, die in Listing 10-25 noch einmal
gezeigt wird und die ohne Lifetime-Annotationen kompiliert hat.

<Listing number="10-25" file-name="src/lib.rs" caption="Eine Funktion, die wir in Listing 4-9 definiert haben und die ohne Lifetime-Annotationen kompiliert hat, obwohl Parameter und Rückgabetyp Referenzen sind">

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-25/src/main.rs:here}}
```

</Listing>

Dass diese Funktion ohne Lifetime-Annotationen kompiliert, hat historische
Gründe: In frühen Versionen von Rust (vor 1.0) hätte dieser Code nicht
kompiliert, weil jede Referenz eine explizite Lifetime brauchte. Damals hätte
man die Funktionssignatur so geschrieben:

```rust,ignore
fn first_word<'a>(s: &'a str) -> &'a str {
```

Nachdem das Rust-Team viel Rust-Code geschrieben hatte, stellte es fest, dass
Rust-Programmierende in bestimmten Situationen immer wieder dieselben
Lifetime-Annotationen eingaben. Diese Situationen waren vorhersehbar und folgten
einigen deterministischen Schemata. Die Entwickler programmierten diese Schemata
in den Code des Compilers, damit der Borrow-Checker die Lifetimes in diesen
Situationen ableiten konnte und keine expliziten Annotationen brauchte.

Dieses Stück Rust-Geschichte ist relevant, weil möglicherweise weitere
deterministische Schemata entstehen und dem Compiler hinzugefügt werden. In
Zukunft könnten noch weniger Lifetime-Annotationen nötig sein.

Die Schemata, die in die Analyse von Referenzen in Rust einprogrammiert sind,
heißen _Regeln zur Lifetime-Elision_ (_lifetime elision rules_). Das sind keine
Regeln, die Programmierende befolgen müssen; es ist eine Reihe bestimmter Fälle,
die der Compiler berücksichtigt, und wenn dein Code zu diesen Fällen passt,
musst du die Lifetimes nicht explizit angeben.

Die Elisionsregeln ermöglichen keine vollständige Ableitung. Gibt es nach der
Anwendung der Regeln durch Rust immer noch Mehrdeutigkeiten darüber, welche
Lifetimes die Referenzen haben, rät der Compiler nicht, welche Lifetime die
übrigen Referenzen haben sollten. Statt zu raten, gibt dir der Compiler einen
Fehler, den du durch Hinzufügen der Lifetime-Annotationen beheben kannst.

Lifetimes an Funktions- oder Methodenparametern heißen _Eingabe-Lifetimes_
(_input lifetimes_), und Lifetimes an Rückgabewerten heißen _Ausgabe-Lifetimes_
(_output lifetimes_).

Der Compiler verwendet drei Regeln, um die Lifetimes der Referenzen
herauszufinden, wenn es keine expliziten Annotationen gibt. Die erste Regel gilt
für Eingabe-Lifetimes, die zweite und dritte Regel für Ausgabe-Lifetimes. Kommt
der Compiler am Ende der drei Regeln an und gibt es immer noch Referenzen, deren
Lifetimes er nicht herausfinden kann, bricht der Compiler mit einem Fehler ab.
Diese Regeln gelten für `fn`-Definitionen ebenso wie für `impl`-Blöcke.

<!-- BEGIN INTERVENTION: d03748df-8dcf-4ec8-bd30-341927544665 -->

Die erste Regel ist, dass der Compiler jeder Lifetime in jedem Eingabetyp einen
eigenen Lifetime-Parameter zuweist. Referenzen wie `&'_ i32` brauchen einen
Lifetime-Parameter, und Structs wie `ImportantExcerpt<'_>` brauchen einen
Lifetime-Parameter. Zum Beispiel:

- Die Funktion `fn foo(x: &i32)` würde einen Lifetime-Parameter erhalten und zu
  `fn foo<'a>(x: &'a i32)` werden.
- Die Funktion `fn foo(x: &i32, y: &i32)` würde zwei Lifetime-Parameter erhalten
  und zu `fn foo<'a, 'b>(x: &'a i32, y: &'b i32)` werden.
- Die Funktion `fn foo(x: &ImportantExcerpt)` würde zwei Lifetime-Parameter
  erhalten und zu `fn foo<'a, 'b>(x: &'a ImportantExcerpt<'b>)` werden.

<!-- END INTERVENTION -->

Die zweite Regel ist: Gibt es genau einen Eingabe-Lifetime-Parameter, wird diese
Lifetime allen Ausgabe-Lifetime-Parametern zugewiesen:
`fn foo<'a>(x: &'a i32)
-> &'a i32`.

Die dritte Regel ist: Gibt es mehrere Eingabe-Lifetime-Parameter, von denen aber
einer `&self` oder `&mut self` ist, weil es sich um eine Methode handelt, wird
die Lifetime von `self` allen Ausgabe-Lifetime-Parametern zugewiesen. Diese
dritte Regel macht Methoden viel angenehmer zu lesen und zu schreiben, weil
weniger Symbole nötig sind.

Stellen wir uns vor, wir wären der Compiler. Wir wenden diese Regeln an, um die
Lifetimes der Referenzen in der Signatur der Funktion `first_word` in Listing
10-25 herauszufinden. Die Signatur beginnt ohne Lifetimes für die Referenzen:

```rust,ignore
fn first_word(s: &str) -> &str {
```

Dann wendet der Compiler die erste Regel an, die festlegt, dass jeder Parameter
seine eigene Lifetime erhält. Wir nennen sie wie üblich `'a`, also lautet die
Signatur jetzt:

```rust,ignore
fn first_word<'a>(s: &'a str) -> &str {
```

Die zweite Regel greift, weil es genau eine Eingabe-Lifetime gibt. Die zweite
Regel legt fest, dass die Lifetime des einen Eingabeparameters der
Ausgabe-Lifetime zugewiesen wird, also lautet die Signatur jetzt:

```rust,ignore
fn first_word<'a>(s: &'a str) -> &'a str {
```

Jetzt haben alle Referenzen in dieser Funktionssignatur Lifetimes, und der
Compiler kann seine Analyse fortsetzen, ohne dass die Lifetimes in dieser
Funktionssignatur annotiert werden müssen.

Sehen wir uns ein weiteres Beispiel an, diesmal mit der Funktion `longest`, die
noch keine Lifetime-Parameter hatte, als wir in Listing 10-20 mit ihr zu
arbeiten begannen:

```rust,ignore
fn longest(x: &str, y: &str) -> &str {
```

Wenden wir die erste Regel an: Jeder Parameter erhält seine eigene Lifetime.
Diesmal haben wir zwei Parameter statt einem, also haben wir zwei Lifetimes:

```rust,ignore
fn longest<'a, 'b>(x: &'a str, y: &'b str) -> &str {
```

Du siehst, dass die zweite Regel nicht greift, weil es mehr als eine
Eingabe-Lifetime gibt. Auch die dritte Regel greift nicht, weil `longest` eine
Funktion und keine Methode ist, also keiner der Parameter `self` ist. Nachdem
wir alle drei Regeln durchgegangen sind, wissen wir immer noch nicht, welche
Lifetime der Rückgabetyp hat. Deshalb haben wir beim Kompilieren des Codes in
Listing 10-20 einen Fehler bekommen: Der Compiler ist die Regeln zur
Lifetime-Elision durchgegangen, konnte aber trotzdem nicht alle Lifetimes der
Referenzen in der Signatur herausfinden.

Da die dritte Regel eigentlich nur in Methodensignaturen greift, sehen wir uns
als Nächstes Lifetimes in diesem Kontext an, um zu verstehen, warum wir dank der
dritten Regel Lifetimes in Methodensignaturen nicht sehr oft annotieren müssen.

<!-- Old headings. Do not remove or links may break. -->

<a id="lifetime-annotations-in-method-definitions"></a>

### In Methodendefinitionen {#in-method-definitions}

Wenn wir Methoden auf einem Struct mit Lifetimes implementieren, verwenden wir
dieselbe Syntax wie bei generischen Typparametern, wie in Listing 10-11 gezeigt.
Wo wir die Lifetime-Parameter deklarieren und verwenden, hängt davon ab, ob sie
mit den Feldern des Structs oder mit den Methodenparametern und Rückgabewerten
zusammenhängen.

Lifetime-Namen für Struct-Felder müssen immer nach dem Schlüsselwort `impl`
deklariert und dann nach dem Namen des Structs verwendet werden, weil diese
Lifetimes Teil des Typs des Structs sind.

In Methodensignaturen innerhalb des `impl`-Blocks können Referenzen an die
Lifetime von Referenzen in den Feldern des Structs gebunden oder davon
unabhängig sein. Außerdem führen die Regeln zur Lifetime-Elision oft dazu, dass
in Methodensignaturen keine Lifetime-Annotationen nötig sind. Sehen wir uns
einige Beispiele mit dem Struct namens `ImportantExcerpt` an, das wir in Listing
10-24 definiert haben.

Zuerst verwenden wir eine Methode namens `level`, deren einziger Parameter eine
Referenz auf `self` ist und deren Rückgabewert ein `i32` ist, also keine
Referenz auf irgendetwas:

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-10-lifetimes-on-methods/src/main.rs:1st}}
```

Die Deklaration des Lifetime-Parameters nach `impl` und seine Verwendung nach
dem Typnamen sind erforderlich, aber wegen der ersten Elisionsregel müssen wir
die Lifetime der Referenz auf `self` nicht annotieren.

Hier ist ein Beispiel, bei dem die dritte Regel zur Lifetime-Elision greift:

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-10-lifetimes-on-methods/src/main.rs:3rd}}
```

Es gibt zwei Eingabe-Lifetimes, also wendet Rust die erste Regel zur
Lifetime-Elision an und gibt sowohl `&self` als auch `announcement` eine eigene
Lifetime. Da einer der Parameter `&self` ist, erhält der Rückgabetyp dann die
Lifetime von `&self`, und alle Lifetimes sind berücksichtigt.

### Die statische Lifetime {#the-static-lifetime}

Eine besondere Lifetime, die wir besprechen müssen, ist `'static`. Sie bedeutet,
dass die betreffende Referenz während der gesamten Laufzeit des Programms leben
_kann_. Alle String-Literale haben die Lifetime `'static`, die wir so annotieren
können:

```rust
let s: &'static str = "I have a static lifetime.";
```

Der Text dieses Strings ist direkt in der Binärdatei des Programms gespeichert,
die immer verfügbar ist. Daher ist die Lifetime aller String-Literale `'static`.

In Fehlermeldungen siehst du vielleicht Vorschläge, die Lifetime `'static` zu
verwenden. Bevor du aber `'static` als Lifetime für eine Referenz angibst,
überleg dir, ob die Referenz, die du hast, tatsächlich während der gesamten
Laufzeit deines Programms lebt und ob du das willst. Meistens kommt eine
Fehlermeldung, die die Lifetime `'static` vorschlägt, von dem Versuch, eine
hängende Referenz zu erzeugen, oder von nicht zueinander passenden Lifetimes. In
solchen Fällen besteht die Lösung darin, diese Probleme zu beheben, nicht darin,
die Lifetime `'static` anzugeben.

<!-- Old headings. Do not remove or links may break. -->

<a id="generic-type-parameters-trait-bounds-and-lifetimes-together"></a>

## Generische Typparameter, Trait-Bounds und Lifetimes {#generic-type-parameters-trait-bounds-and-lifetimes}

Sehen wir uns kurz die Syntax an, mit der man generische Typparameter,
Trait-Bounds und Lifetimes in einer einzigen Funktion angibt!

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-11-generics-traits-and-lifetimes/src/main.rs:here}}
```

Das ist die Funktion `longest` aus Listing 10-21, die den längeren von zwei
String-Slices zurückgibt. Jetzt hat sie aber einen zusätzlichen Parameter namens
`ann` vom generischen Typ `T`, für den jeder Typ eingesetzt werden kann, der den
Trait `Display` implementiert, wie in der `where`-Klausel angegeben. Dieser
zusätzliche Parameter wird mit `{}` ausgegeben, weshalb der Trait-Bound
`Display` nötig ist. Da Lifetimes eine Art von Generics sind, stehen die
Deklarationen des Lifetime-Parameters `'a` und des generischen Typparameters `T`
in derselben Liste in den spitzen Klammern nach dem Funktionsnamen.

{{#quiz ../quizzes/ch10-03-lifetimes-sec2.toml}}

### Zusammenfassung {#summary}

Wir haben in diesem Kapitel viel behandelt! Jetzt, da du generische
Typparameter, Traits und Trait-Bounds sowie generische Lifetime-Parameter
kennst, kannst du Code ohne Wiederholungen schreiben, der in vielen
verschiedenen Situationen funktioniert. Mit generischen Typparametern kannst du
den Code auf verschiedene Typen anwenden. Traits und Trait-Bounds stellen
sicher, dass die Typen, obwohl sie generisch sind, das Verhalten haben, das der
Code braucht. Du hast gelernt, wie du mit Lifetime-Annotationen sicherstellst,
dass dieser flexible Code keine hängenden Referenzen hat. Und diese ganze
Analyse findet zur Kompilierzeit statt und beeinträchtigt die Performance zur
Laufzeit nicht!

Ob du es glaubst oder nicht: Zu den Themen dieses Kapitels gibt es noch viel
mehr zu lernen. Kapitel 18 behandelt Trait-Objekte, eine weitere Möglichkeit,
Traits zu verwenden. Es gibt auch komplexere Szenarien mit
Lifetime-Annotationen, die du nur in sehr fortgeschrittenen Fällen brauchst;
dafür solltest du die [Rust-Referenz][reference] lesen. Als Nächstes lernst du
aber, wie du in Rust Tests schreibst, damit du sicherstellen kannst, dass dein
Code so funktioniert, wie er soll.

[references-and-borrowing]: ch04-02-references-and-borrowing.html#references-and-borrowing
[lifetime-permissions]: ch04-02-references-and-borrowing.html#permissions-are-returned-at-the-end-of-a-references-lifetime
[string-slices-as-parameters]: ch04-04-slices.html#string-slices-as-parameters
[reference]: https://doc.rust-lang.org/reference/trait-bounds.html
