## Behebbare Fehler mit `Result` {#recoverable-errors-with-result}

Die meisten Fehler sind nicht so schwerwiegend, dass das Programm komplett
gestoppt werden muss. Wenn eine Funktion fehlschlägt, hat das manchmal einen
Grund, den du leicht deuten und auf den du reagieren kannst. Wenn du zum
Beispiel versuchst, eine Datei zu öffnen, und das fehlschlägt, weil die Datei
nicht existiert, möchtest du die Datei vielleicht anlegen, statt den Prozess zu
beenden.

Erinnere dich aus [„Mögliche Fehler mit `Result` behandeln“][handle_failure]<!--
ignore --> in Kapitel 2, dass das Enum `Result` mit zwei Varianten definiert
ist, `Ok` und `Err`, und zwar so:

```rust
enum Result<T, E> {
    Ok(T),
    Err(E),
}
```

`T` und `E` sind generische Typparameter: Generics besprechen wir ausführlicher
in Kapitel 10. Was du jetzt wissen musst, ist, dass `T` für den Typ des Werts
steht, der im Erfolgsfall in der Variante `Ok` zurückgegeben wird, und `E` für
den Typ des Fehlers, der im Fehlerfall in der Variante `Err` zurückgegeben wird.
Da `Result` diese generischen Typparameter hat, können wir den Typ `Result` und
die darauf definierten Funktionen in vielen verschiedenen Situationen verwenden,
in denen der Erfolgswert und der Fehlerwert, die wir zurückgeben wollen,
unterschiedlich sein können.

Rufen wir eine Funktion auf, die einen `Result`-Wert zurückgibt, weil die
Funktion fehlschlagen könnte. In Listing 9-3 versuchen wir, eine Datei zu
öffnen.

<Listing number="9-3" file-name="src/main.rs" caption="Eine Datei öffnen">

```rust
{{#rustdoc_include ../listings/ch09-error-handling/listing-09-03/src/main.rs}}
```

</Listing>

Der Rückgabetyp von `File::open` ist ein `Result<T, E>`. Den generischen
Parameter `T` hat die Implementierung von `File::open` mit dem Typ des
Erfolgswerts gefüllt, `std::fs::File`, einem Datei-Handle. Der Typ von `E`, der
im Fehlerwert verwendet wird, ist `std::io::Error`. Dieser Rückgabetyp bedeutet,
dass der Aufruf von `File::open` erfolgreich sein und ein Datei-Handle
zurückgeben kann, aus dem wir lesen oder in das wir schreiben können. Der
Funktionsaufruf kann aber auch fehlschlagen: Die Datei existiert vielleicht
nicht, oder wir haben keine Berechtigung, auf die Datei zuzugreifen. Die
Funktion `File::open` braucht eine Möglichkeit, uns mitzuteilen, ob sie
erfolgreich war oder fehlgeschlagen ist, und uns gleichzeitig entweder das
Datei-Handle oder Informationen zum Fehler zu geben. Genau diese Information
vermittelt das Enum `Result`.

Ist `File::open` erfolgreich, ist der Wert in der Variable
`greeting_file_result` eine Instanz von `Ok`, die ein Datei-Handle enthält.
Schlägt es fehl, ist der Wert in `greeting_file_result` eine Instanz von `Err`,
die mehr Informationen darüber enthält, welche Art von Fehler aufgetreten ist.

Wir müssen den Code in Listing 9-3 ergänzen, damit er je nach dem Wert, den
`File::open` zurückgibt, unterschiedlich handelt. Listing 9-4 zeigt eine
Möglichkeit, das `Result` mit einem grundlegenden Werkzeug zu behandeln, dem
`match`-Ausdruck, den wir in Kapitel 6 besprochen haben.

<Listing number="9-4" file-name="src/main.rs" caption="Mit einem `match`-Ausdruck die `Result`-Varianten behandeln, die zurückgegeben werden können">

```rust,should_panic
{{#rustdoc_include ../listings/ch09-error-handling/listing-09-04/src/main.rs}}
```

</Listing>

Beachte, dass das Enum `Result` und seine Varianten wie das Enum `Option` durch
das Prelude in den Gültigkeitsbereich (_scope_) gebracht werden, sodass wir in
den `match`-Armen vor den Varianten `Ok` und `Err` kein `Result::` angeben
müssen.

Ist das Ergebnis `Ok`, gibt dieser Code den inneren Wert `file` aus der Variante
`Ok` zurück, und wir weisen diesen Datei-Handle-Wert dann der Variable
`greeting_file` zu. Nach dem `match` können wir das Datei-Handle zum Lesen oder
Schreiben verwenden.

Der andere Arm des `match` behandelt den Fall, dass wir von `File::open` einen
`Err`-Wert erhalten. In diesem Beispiel haben wir uns entschieden, das Makro
`panic!` aufzurufen. Gibt es in unserem aktuellen Verzeichnis keine Datei namens
_hello.txt_ und führen wir diesen Code aus, sehen wir folgende Ausgabe des
Makros `panic!`:

```console
{{#include ../listings/ch09-error-handling/listing-09-04/output.txt}}
```

Wie üblich sagt uns diese Ausgabe genau, was schiefgelaufen ist.

### Unterschiedliche Fehler per Pattern-Matching unterscheiden {#matching-on-different-errors}

Der Code in Listing 9-4 löst `panic!` aus, egal warum `File::open`
fehlgeschlagen ist. Wir wollen aber bei unterschiedlichen Fehlerursachen
unterschiedlich handeln. Ist `File::open` fehlgeschlagen, weil die Datei nicht
existiert, wollen wir die Datei anlegen und das Handle der neuen Datei
zurückgeben. Ist `File::open` aus einem anderen Grund fehlgeschlagen – zum
Beispiel, weil wir keine Berechtigung hatten, die Datei zu öffnen –, soll der
Code weiterhin auf dieselbe Weise `panic!` auslösen wie in Listing 9-4. Dafür
fügen wir einen inneren `match`-Ausdruck hinzu, wie in Listing 9-5 gezeigt.

<Listing number="9-5" file-name="src/main.rs" caption="Unterschiedliche Arten von Fehlern unterschiedlich behandeln">

<!-- ignore this test because otherwise it creates hello.txt which causes other
tests to fail lol -->

```rust,ignore
{{#rustdoc_include ../listings/ch09-error-handling/listing-09-05/src/main.rs}}
```

</Listing>

Der Typ des Werts, den `File::open` in der Variante `Err` zurückgibt, ist
`io::Error`, ein Struct, das die Standardbibliothek bereitstellt. Dieses Struct
hat eine Methode `kind`, die wir aufrufen können, um einen `io::ErrorKind`-Wert
zu erhalten. Das Enum `io::ErrorKind` wird von der Standardbibliothek
bereitgestellt und hat Varianten für die unterschiedlichen Arten von Fehlern,
die bei einer `io`-Operation auftreten können. Die Variante, die wir verwenden
wollen, ist `ErrorKind::NotFound`, die angibt, dass die Datei, die wir öffnen
wollen, noch nicht existiert. Wir wenden also Pattern-Matching auf
`greeting_file_result` an, haben aber zusätzlich ein inneres Match auf
`error.kind()`.

Die Bedingung, die wir im inneren Match prüfen wollen, ist, ob der von
`error.kind()` zurückgegebene Wert die Variante `NotFound` des Enums `ErrorKind`
ist. Ist das der Fall, versuchen wir, die Datei mit `File::create` anzulegen. Da
aber auch `File::create` fehlschlagen kann, brauchen wir einen zweiten Arm im
inneren `match`-Ausdruck. Kann die Datei nicht angelegt werden, wird eine andere
Fehlermeldung ausgegeben. Der zweite Arm des äußeren `match` bleibt gleich,
sodass das Programm bei jedem Fehler außer der fehlenden Datei einen Panic
auslöst.

> #### Alternativen zu `match` mit `Result<T, E>` {#alternatives-to-using-match-with-resultt-e}
>
> Das ist eine Menge `match`! Der `match`-Ausdruck ist sehr nützlich, aber auch
> sehr elementar. In Kapitel 13 lernst du Closures kennen, die mit vielen der
> auf `Result<T, E>` definierten Methoden verwendet werden. Diese Methoden
> können knapper sein, als `match` zu verwenden, wenn du in deinem Code
> `Result<T, E>`-Werte behandelst.
>
> Hier ist zum Beispiel eine andere Schreibweise für dieselbe Logik wie in
> Listing 9-5, diesmal mit Closures und der Methode `unwrap_or_else`:
>
> <!-- CAN'T EXTRACT SEE https://github.com/rust-lang/mdBook/issues/1127 -->
>
> ```rust,ignore
> use std::fs::File;
> use std::io::ErrorKind;
>
> fn main() {
>     let greeting_file = File::open("hello.txt").unwrap_or_else(|error| {
>         if error.kind() == ErrorKind::NotFound {
>             File::create("hello.txt").unwrap_or_else(|error| {
>                 panic!("Problem creating the file: {error:?}");
>             })
>         } else {
>             panic!("Problem opening the file: {error:?}");
>         }
>     });
> }
> ```
>
> Obwohl sich dieser Code genauso verhält wie Listing 9-5, enthält er keine
> `match`-Ausdrücke und liest sich übersichtlicher. Komm zu diesem Beispiel
> zurück, nachdem du Kapitel 13 gelesen hast, und schlag die Methode
> `unwrap_or_else` in der Dokumentation der Standardbibliothek nach. Viele
> weitere dieser Methoden können riesige, verschachtelte `match`-Ausdrücke
> aufräumen, wenn du mit Fehlern zu tun hast.

{{#quiz ../quizzes/ch09-02-recoverable-errors-sec1.toml}}

<!-- Old headings. Do not remove or links may break. -->

<a id="shortcuts-for-panic-on-error-unwrap-and-expect"></a>

#### Abkürzungen für einen Panic im Fehlerfall {#shortcuts-for-panic-on-error}

`match` funktioniert gut genug, kann aber etwas umständlich sein und drückt die
Absicht nicht immer gut aus. Für den Typ `Result<T, E>` sind viele Hilfsmethoden
definiert, die verschiedene, spezifischere Aufgaben erledigen. Die Methode
`unwrap` ist eine Abkürzung, die genauso implementiert ist wie der
`match`-Ausdruck, den wir in Listing 9-4 geschrieben haben. Ist der
`Result`-Wert die Variante `Ok`, gibt `unwrap` den Wert in `Ok` zurück. Ist das
`Result` die Variante `Err`, ruft `unwrap` für uns das Makro `panic!` auf. Hier
ist ein Beispiel für `unwrap` in Aktion:

<Listing file-name="src/main.rs">

```rust,should_panic
{{#rustdoc_include ../listings/ch09-error-handling/no-listing-04-unwrap/src/main.rs}}
```

</Listing>

Führen wir diesen Code ohne eine Datei _hello.txt_ aus, sehen wir eine
Fehlermeldung vom Aufruf von `panic!`, den die Methode `unwrap` vornimmt:

<!-- manual-regeneration
cd listings/ch09-error-handling/no-listing-04-unwrap
cargo run
copy and paste relevant text
-->

```text
thread 'main' panicked at src/main.rs:4:49:
called `Result::unwrap()` on an `Err` value: Os { code: 2, kind: NotFound, message: "No such file or directory" }
```

Ähnlich lässt uns die Methode `expect` zusätzlich die Fehlermeldung von `panic!`
wählen. Wenn du `expect` statt `unwrap` verwendest und gute Fehlermeldungen
angibst, kannst du deine Absicht ausdrücken und erleichterst es, die Ursache
eines Panics aufzuspüren. Die Syntax von `expect` sieht so aus:

<Listing file-name="src/main.rs">

```rust,should_panic
{{#rustdoc_include ../listings/ch09-error-handling/no-listing-05-expect/src/main.rs}}
```

</Listing>

Wir verwenden `expect` genauso wie `unwrap`: um das Datei-Handle zurückzugeben
oder das Makro `panic!` aufzurufen. Die Fehlermeldung, die `expect` bei seinem
Aufruf von `panic!` verwendet, ist der Parameter, den wir an `expect` übergeben,
statt der Standardmeldung von `panic!`, die `unwrap` verwendet. So sieht das
aus:

<!-- manual-regeneration
cd listings/ch09-error-handling/no-listing-05-expect
cargo run
copy and paste relevant text
-->

```text
thread 'main' panicked at src/main.rs:5:10:
hello.txt should be included in this project: Os { code: 2, kind: NotFound, message: "No such file or directory" }
```

In Code mit Produktionsqualität wählen die meisten Rustaceans `expect` statt
`unwrap` und geben mehr Kontext dazu, warum erwartet wird, dass die Operation
immer erfolgreich ist. Falls sich deine Annahmen jemals als falsch erweisen,
hast du dann mehr Informationen für die Fehlersuche.

### Fehler weitergeben {#propagating-errors}

Wenn die Implementierung einer Funktion etwas aufruft, das fehlschlagen könnte,
kannst du den Fehler, statt ihn in der Funktion selbst zu behandeln, an den
aufrufenden Code zurückgeben, damit dieser entscheiden kann, was zu tun ist. Das
nennt man das _Weitergeben_ (_propagating_) des Fehlers. Es gibt dem aufrufenden
Code mehr Kontrolle, denn dort gibt es vielleicht mehr Informationen oder Logik,
die bestimmen, wie der Fehler behandelt werden soll, als im Kontext deines Codes
verfügbar sind.

Listing 9-6 zeigt zum Beispiel eine Funktion, die einen Benutzernamen aus einer
Datei liest. Existiert die Datei nicht oder kann sie nicht gelesen werden, gibt
diese Funktion diese Fehler an den Code zurück, der die Funktion aufgerufen hat.

<Listing number="9-6" file-name="src/main.rs" caption="Eine Funktion, die mit `match` Fehler an den aufrufenden Code zurückgibt">

<!-- Deliberately not using rustdoc_include here; the `main` function in the
file panics. We do want to include it for reader experimentation purposes, but
don't want to include it for rustdoc testing purposes. -->

```rust
{{#include ../listings/ch09-error-handling/listing-09-06/src/main.rs:here}}
```

</Listing>

Diese Funktion lässt sich viel kürzer schreiben, aber wir machen zunächst vieles
von Hand, um die Fehlerbehandlung zu erkunden; am Ende zeigen wir die kürzere
Variante. Sehen wir uns zuerst den Rückgabetyp der Funktion an:
`Result<String, io::Error>`. Das bedeutet, dass die Funktion einen Wert vom Typ
`Result<T, E>` zurückgibt, bei dem der generische Parameter `T` mit dem
konkreten Typ `String` und der generische Typ `E` mit dem konkreten Typ
`io::Error` gefüllt ist.

Ist diese Funktion ohne Probleme erfolgreich, erhält der Code, der diese
Funktion aufruft, einen `Ok`-Wert, der einen `String` enthält – den `username`,
den diese Funktion aus der Datei gelesen hat. Stößt diese Funktion auf Probleme,
erhält der aufrufende Code einen `Err`-Wert mit einer Instanz von `io::Error`,
die mehr Informationen über die Probleme enthält. Wir haben `io::Error` als
Rückgabetyp dieser Funktion gewählt, weil das zufällig der Typ des Fehlerwerts
ist, den beide Operationen zurückgeben, die wir im Rumpf dieser Funktion
aufrufen und die fehlschlagen können: die Funktion `File::open` und die Methode
`read_to_string`.

Der Rumpf der Funktion beginnt mit dem Aufruf der Funktion `File::open`. Dann
behandeln wir den `Result`-Wert mit einem `match` ähnlich dem `match` in Listing
9-4. Ist `File::open` erfolgreich, wird das Datei-Handle in der Pattern-Variable
`file` zum Wert in der veränderlichen (_mutable_) Variable `username_file`, und
die Funktion läuft weiter. Im Fall `Err` rufen wir nicht `panic!` auf, sondern
verwenden das Schlüsselwort `return`, um vorzeitig aus der gesamten Funktion
zurückzukehren und den Fehlerwert von `File::open`, der sich jetzt in der
Pattern-Variable `e` befindet, als Fehlerwert dieser Funktion an den aufrufenden
Code zurückzugeben.

Wenn wir also ein Datei-Handle in `username_file` haben, erstellt die Funktion
dann einen neuen `String` in der Variable `username` und ruft die Methode
`read_to_string` auf dem Datei-Handle in `username_file` auf, um den Inhalt der
Datei in `username` einzulesen. Die Methode `read_to_string` gibt ebenfalls ein
`Result` zurück, weil sie fehlschlagen kann, obwohl `File::open` erfolgreich
war. Wir brauchen also ein weiteres `match`, um dieses `Result` zu behandeln:
Ist `read_to_string` erfolgreich, war unsere Funktion erfolgreich, und wir geben
den Benutzernamen aus der Datei, der jetzt in `username` steht, in ein `Ok`
verpackt zurück. Schlägt `read_to_string` fehl, geben wir den Fehlerwert auf
dieselbe Weise zurück wie im `match`, das den Rückgabewert von `File::open`
behandelt hat. Wir müssen dabei aber nicht explizit `return` schreiben, weil das
der letzte Ausdruck in der Funktion ist.

Der Code, der diesen Code aufruft, kümmert sich dann darum, entweder einen
`Ok`-Wert mit einem Benutzernamen oder einen `Err`-Wert mit einem `io::Error` zu
erhalten. Was mit diesen Werten geschieht, entscheidet der aufrufende Code.
Erhält er einen `Err`-Wert, könnte er zum Beispiel `panic!` aufrufen und das
Programm abstürzen lassen, einen Standard-Benutzernamen verwenden oder den
Benutzernamen woanders als in einer Datei nachschlagen. Wir haben nicht genug
Informationen darüber, was der aufrufende Code eigentlich tun will, also geben
wir alle Erfolgs- oder Fehlerinformationen nach oben weiter, damit er sie
angemessen behandeln kann.

Dieses Schema der Fehlerweitergabe ist in Rust so verbreitet, dass Rust dafür
den Fragezeichen-Operator `?` bereitstellt, der das erleichtert.

<!-- Old headings. Do not remove or links may break. -->

<a id="a-shortcut-for-propagating-errors-the--operator"></a>

#### Die Abkürzung mit dem Operator `?` {#the--operator-shortcut}

Listing 9-7 zeigt eine Implementierung von `read_username_from_file` mit
derselben Funktionalität wie in Listing 9-6, aber diese Implementierung
verwendet den Operator `?`.

<Listing number="9-7" file-name="src/main.rs" caption="Eine Funktion, die mit dem Operator `?` Fehler an den aufrufenden Code zurückgibt">

<!-- Deliberately not using rustdoc_include here; the `main` function in the
file panics. We do want to include it for reader experimentation purposes, but
don't want to include it for rustdoc testing purposes. -->

```rust
{{#include ../listings/ch09-error-handling/listing-09-07/src/main.rs:here}}
```

</Listing>

Das `?` hinter einem `Result`-Wert ist so definiert, dass es fast genauso
funktioniert wie die `match`-Ausdrücke, die wir in Listing 9-6 zur Behandlung
der `Result`-Werte definiert haben. Ist der Wert des `Result` ein `Ok`, wird der
Wert in `Ok` von diesem Ausdruck zurückgegeben, und das Programm läuft weiter.
Ist der Wert ein `Err`, wird das `Err` von der gesamten Funktion zurückgegeben,
als hätten wir das Schlüsselwort `return` verwendet, sodass der Fehlerwert an
den aufrufenden Code weitergegeben wird.

Es gibt einen Unterschied zwischen dem, was der `match`-Ausdruck aus Listing 9-6
tut, und dem, was der Operator `?` tut: Fehlerwerte, auf die der Operator `?`
angewendet wird, durchlaufen die Funktion `from`, die im Trait `From` der
Standardbibliothek definiert ist und mit der Werte von einem Typ in einen
anderen umgewandelt werden. Wenn der Operator `?` die Funktion `from` aufruft,
wird der erhaltene Fehlertyp in den Fehlertyp umgewandelt, der im Rückgabetyp
der aktuellen Funktion festgelegt ist. Das ist nützlich, wenn eine Funktion
einen einzigen Fehlertyp zurückgibt, der alle Arten darstellt, wie die Funktion
fehlschlagen kann, selbst wenn Teile davon aus vielen verschiedenen Gründen
fehlschlagen können.

Wir könnten zum Beispiel die Funktion `read_username_from_file` in Listing 9-7
so ändern, dass sie einen eigenen Fehlertyp namens `OurError` zurückgibt, den
wir definieren. Definieren wir außerdem `impl From<io::Error> for OurError`, um
eine Instanz von `OurError` aus einem `io::Error` zu erzeugen, dann rufen die
`?`-Operatoren im Rumpf von `read_username_from_file` `from` auf und wandeln die
Fehlertypen um, ohne dass wir der Funktion weiteren Code hinzufügen müssen.

Im Kontext von Listing 9-7 gibt das `?` am Ende des Aufrufs von `File::open` den
Wert in einem `Ok` an die Variable `username_file` zurück. Tritt ein Fehler auf,
kehrt der Operator `?` vorzeitig aus der gesamten Funktion zurück und übergibt
den `Err`-Wert an den aufrufenden Code. Dasselbe gilt für das `?` am Ende des
Aufrufs von `read_to_string`.

Der Operator `?` erspart eine Menge Boilerplate-Code und macht die
Implementierung dieser Funktion einfacher. Wir könnten diesen Code sogar noch
weiter verkürzen, indem wir Methodenaufrufe direkt hinter dem `?` verketten, wie
in Listing 9-8 gezeigt.

<Listing number="9-8" file-name="src/main.rs" caption="Methodenaufrufe hinter dem Operator `?` verketten">

<!-- Deliberately not using rustdoc_include here; the `main` function in the
file panics. We do want to include it for reader experimentation purposes, but
don't want to include it for rustdoc testing purposes. -->

```rust
{{#include ../listings/ch09-error-handling/listing-09-08/src/main.rs:here}}
```

</Listing>

Wir haben das Erzeugen des neuen `String` in `username` an den Anfang der
Funktion verschoben; dieser Teil hat sich nicht geändert. Statt eine Variable
`username_file` anzulegen, haben wir den Aufruf von `read_to_string` direkt an
das Ergebnis von `File::open("hello.txt")?` angehängt. Am Ende des Aufrufs von
`read_to_string` steht weiterhin ein `?`, und wir geben weiterhin einen
`Ok`-Wert mit `username` zurück, wenn sowohl `File::open` als auch
`read_to_string` erfolgreich sind, statt Fehler zurückzugeben. Die
Funktionalität ist wieder dieselbe wie in Listing 9-6 und Listing 9-7; das ist
nur eine andere, ergonomischere Schreibweise.

Listing 9-9 zeigt eine Möglichkeit, das mit `fs::read_to_string` noch kürzer zu
machen.

<Listing number="9-9" file-name="src/main.rs" caption="`fs::read_to_string` verwenden, statt die Datei zu öffnen und dann zu lesen">

<!-- Deliberately not using rustdoc_include here; the `main` function in the
file panics. We do want to include it for reader experimentation purposes, but
don't want to include it for rustdoc testing purposes. -->

```rust
{{#include ../listings/ch09-error-handling/listing-09-09/src/main.rs:here}}
```

</Listing>

Eine Datei in einen String einzulesen ist eine ziemlich häufige Operation, daher
stellt die Standardbibliothek die praktische Funktion `fs::read_to_string`
bereit, die die Datei öffnet, einen neuen `String` erstellt, den Inhalt der
Datei liest, den Inhalt in diesen `String` schreibt und ihn zurückgibt. Mit
`fs::read_to_string` hätten wir natürlich keine Gelegenheit gehabt, die ganze
Fehlerbehandlung zu erklären, also haben wir es zuerst auf dem längeren Weg
gemacht.

<!-- Old headings. Do not remove or links may break. -->

<a id="where-the--operator-can-be-used"></a>

#### Wo man den Operator `?` verwenden kann {#where-to-use-the--operator}

Der Operator `?` kann nur in Funktionen verwendet werden, deren Rückgabetyp mit
dem Wert kompatibel ist, auf den `?` angewendet wird. Das liegt daran, dass der
Operator `?` so definiert ist, dass er einen Wert vorzeitig aus der Funktion
zurückgibt, auf dieselbe Weise wie der `match`-Ausdruck, den wir in Listing 9-6
definiert haben. In Listing 9-6 hat das `match` einen `Result`-Wert verwendet,
und der Arm für die vorzeitige Rückkehr hat einen `Err(e)`-Wert zurückgegeben.
Der Rückgabetyp der Funktion muss ein `Result` sein, damit er mit diesem
`return` kompatibel ist.

Sehen wir uns in Listing 9-10 den Fehler an, den wir bekommen, wenn wir den
Operator `?` in einer Funktion `main` verwenden, deren Rückgabetyp nicht mit dem
Typ des Werts kompatibel ist, auf den wir `?` anwenden.

<Listing number="9-10" file-name="src/main.rs" caption="Der Versuch, `?` in der Funktion `main` zu verwenden, die `()` zurückgibt, kompiliert nicht.">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch09-error-handling/listing-09-10/src/main.rs}}
```

</Listing>

Dieser Code öffnet eine Datei, was fehlschlagen kann. Der Operator `?` folgt auf
den `Result`-Wert, den `File::open` zurückgibt, aber diese Funktion `main` hat
den Rückgabetyp `()`, nicht `Result`. Wenn wir diesen Code kompilieren, erhalten
wir folgende Fehlermeldung:

```console
{{#include ../listings/ch09-error-handling/listing-09-10/output.txt}}
```

Dieser Fehler weist darauf hin, dass wir den Operator `?` nur in einer Funktion
verwenden dürfen, die `Result`, `Option` oder einen anderen Typ zurückgibt, der
`FromResidual` implementiert.

Um den Fehler zu beheben, hast du zwei Möglichkeiten. Die eine ist, den
Rückgabetyp deiner Funktion so zu ändern, dass er mit dem Wert kompatibel ist,
auf den du den Operator `?` anwendest, sofern keine Einschränkungen dagegen
sprechen. Die andere ist, ein `match` oder eine der Methoden von `Result<T, E>`
zu verwenden, um das `Result<T, E>` auf die jeweils passende Weise zu behandeln.

Die Fehlermeldung hat außerdem erwähnt, dass `?` auch mit `Option<T>`-Werten
verwendet werden kann. Wie bei `?` auf einem `Result` kannst du `?` auf einer
`Option` nur in einer Funktion verwenden, die eine `Option` zurückgibt. Das
Verhalten des Operators `?` bei einer `Option<T>` ähnelt seinem Verhalten bei
einem `Result<T, E>`: Ist der Wert `None`, wird an dieser Stelle vorzeitig
`None` aus der Funktion zurückgegeben. Ist der Wert `Some`, ist der Wert in
`Some` der Ergebniswert des Ausdrucks, und die Funktion läuft weiter. Listing
9-11 enthält ein Beispiel für eine Funktion, die das letzte Zeichen der ersten
Zeile im übergebenen Text findet.

<Listing number="9-11" caption="Den Operator `?` auf einen `Option<T>`-Wert anwenden">

```rust
{{#rustdoc_include ../listings/ch09-error-handling/listing-09-11/src/main.rs:here}}
```

</Listing>

Diese Funktion gibt `Option<char>` zurück, weil es möglich ist, dass dort ein
Zeichen steht, aber auch, dass keines dort steht. Dieser Code nimmt das
String-Slice-Argument `text` und ruft darauf die Methode `lines` auf, die einen
Iterator über die Zeilen im String zurückgibt. Da diese Funktion die erste Zeile
untersuchen will, ruft sie `next` auf dem Iterator auf, um den ersten Wert des
Iterators zu erhalten. Ist `text` der leere String, gibt dieser Aufruf von
`next` `None` zurück. In diesem Fall stoppen wir mit `?` und geben `None` aus
`last_char_of_first_line` zurück. Ist `text` nicht der leere String, gibt `next`
einen `Some`-Wert zurück, der einen String-Slice der ersten Zeile in `text`
enthält.

Das `?` holt den String-Slice heraus, und wir können `chars` auf diesem
String-Slice aufrufen, um einen Iterator über seine Zeichen zu erhalten. Uns
interessiert das letzte Zeichen dieser ersten Zeile, also rufen wir `last` auf,
um das letzte Element des Iterators zurückzugeben. Das ist eine `Option`, weil
die erste Zeile der leere String sein könnte, zum Beispiel wenn `text` mit einer
Leerzeile beginnt, aber in anderen Zeilen Zeichen enthält, wie bei `"\nhi"`.
Gibt es aber ein letztes Zeichen in der ersten Zeile, wird es in der Variante
`Some` zurückgegeben. Der Operator `?` in der Mitte gibt uns eine knappe
Möglichkeit, diese Logik auszudrücken, sodass wir die Funktion in einer Zeile
implementieren können. Könnten wir den Operator `?` nicht auf `Option` anwenden,
müssten wir diese Logik mit mehr Methodenaufrufen oder einem `match`-Ausdruck
implementieren.

Beachte, dass du den Operator `?` auf ein `Result` in einer Funktion anwenden
kannst, die `Result` zurückgibt, und den Operator `?` auf eine `Option` in einer
Funktion, die `Option` zurückgibt, aber du kannst die beiden nicht mischen. Der
Operator `?` wandelt ein `Result` nicht automatisch in eine `Option` um oder
umgekehrt; in diesen Fällen kannst du Methoden wie `ok` auf `Result` oder
`ok_or` auf `Option` verwenden, um die Umwandlung explizit vorzunehmen.

Bisher haben alle `main`-Funktionen, die wir verwendet haben, `()`
zurückgegeben. Die Funktion `main` ist besonders, weil sie der Einstiegs- und
Ausstiegspunkt eines ausführbaren Programms ist, und es gibt Einschränkungen
dafür, welchen Rückgabetyp sie haben darf, damit sich das Programm wie erwartet
verhält.

Zum Glück kann `main` auch ein `Result<(), E>` zurückgeben. Listing 9-12 enthält
den Code aus Listing 9-10, aber wir haben den Rückgabetyp von `main` zu
`Result<(), Box<dyn Error>>` geändert und am Ende den Rückgabewert `Ok(())`
hinzugefügt. Dieser Code kompiliert jetzt.

<Listing number="9-12" file-name="src/main.rs" caption="Gibt `main` ein `Result<(), E>` zurück, kann der Operator `?` auf `Result`-Werte angewendet werden.">

```rust,ignore
{{#rustdoc_include ../listings/ch09-error-handling/listing-09-12/src/main.rs}}
```

</Listing>

Der Typ `Box<dyn Error>` ist ein Trait-Objekt, über das wir in
[„Mit Trait-Objekten über gemeinsames Verhalten abstrahieren“][trait-objects]<!-- ignore -->
in Kapitel 18 sprechen. Vorerst kannst du `Box<dyn Error>` als „irgendeine Art
von Fehler“ lesen. `?` auf einen `Result`-Wert in einer Funktion `main` mit dem
Fehlertyp `Box<dyn Error>` anzuwenden, ist erlaubt, weil damit jeder `Err`-Wert
vorzeitig zurückgegeben werden kann. Auch wenn der Rumpf dieser Funktion `main`
immer nur Fehler vom Typ `std::io::Error` zurückgeben wird, bleibt diese
Signatur durch die Angabe von `Box<dyn Error>` korrekt, selbst wenn dem Rumpf
von `main` weiterer Code hinzugefügt wird, der andere Fehler zurückgibt.

Wenn eine Funktion `main` ein `Result<(), E>` zurückgibt, endet die ausführbare
Datei mit dem Wert `0`, wenn `main` `Ok(())` zurückgibt, und mit einem Wert
ungleich null, wenn `main` einen `Err`-Wert zurückgibt. In C geschriebene
ausführbare Programme geben beim Beenden Ganzzahlen zurück: Programme, die
erfolgreich enden, geben die Ganzzahl `0` zurück, und Programme mit Fehler geben
eine Ganzzahl ungleich `0` zurück. Auch Rust gibt aus ausführbaren Programmen
Ganzzahlen zurück, um mit dieser Konvention kompatibel zu sein.

Die Funktion `main` darf beliebige Typen zurückgeben, die
[den Trait `std::process::Termination`][termination]<!-- ignore -->
implementieren, der eine Funktion `report` enthält, die einen `ExitCode`
zurückgibt. Mehr Informationen dazu, wie du den Trait `Termination` für deine
eigenen Typen implementierst, findest du in der Dokumentation der
Standardbibliothek.

Nachdem wir die Details des Aufrufs von `panic!` und der Rückgabe von `Result`
besprochen haben, kehren wir zu der Frage zurück, wie man entscheidet, was in
welchen Fällen angemessen ist.

{{#quiz ../quizzes/ch09-02-recoverable-errors-sec2.toml}}

[handle_failure]: ch02-00-guessing-game-tutorial.html#handling-potential-failure-with-result
[trait-objects]: ch18-02-trait-objects.html#using-trait-objects-to-abstract-over-shared-behavior
[termination]: https://doc.rust-lang.org/std/process/trait.Termination.html
