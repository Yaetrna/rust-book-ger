## Eine Folge von Elementen mit Iteratoren verarbeiten {#processing-a-series-of-items-with-iterators}

Mit dem Iterator-Schema kannst du nacheinander für jedes Element einer Folge
eine Aufgabe ausführen. Ein Iterator ist für die Logik verantwortlich, über
jedes Element zu iterieren und festzustellen, wann die Folge zu Ende ist. Wenn
du Iteratoren verwendest, musst du diese Logik nicht selbst neu implementieren.

In Rust sind Iteratoren _lazy_ (träge). Das heißt, sie bewirken nichts, bis du
Methoden aufrufst, die den Iterator verbrauchen. Der Code in Listing 13-10
erzeugt zum Beispiel einen Iterator über die Elemente im Vektor `v1`, indem er
die auf `Vec<T>` definierte Methode `iter` aufruft. Dieser Code allein tut
nichts Nützliches.

<Listing number="13-10" file-name="src/main.rs" caption="Einen Iterator erzeugen">

```rust
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-10/src/main.rs:here}}
```

</Listing>

Der Iterator ist in der Variable `v1_iter` gespeichert. Sobald wir einen
Iterator erzeugt haben, können wir ihn auf verschiedene Weise verwenden. In
Listing 3-5 haben wir mit einer `for`-Schleife über ein Array iteriert, um für
jedes seiner Elemente Code auszuführen. Unter der Haube wurde dabei implizit ein
Iterator erzeugt und dann verbraucht, aber wie genau das funktioniert, haben wir
bisher übergangen.

Im Beispiel in Listing 13-11 trennen wir das Erzeugen des Iterators von seiner
Verwendung in der `for`-Schleife. Wird die `for`-Schleife mit dem Iterator in
`v1_iter` aufgerufen, wird jedes Element des Iterators in einer Iteration der
Schleife verwendet, die jeden Wert ausgibt.

<Listing number="13-11" file-name="src/main.rs" caption="Einen Iterator in einer `for`-Schleife verwenden">

```rust
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-11/src/main.rs:here}}
```

</Listing>

In Sprachen, deren Standardbibliotheken keine Iteratoren bereitstellen, würdest
du dieselbe Funktionalität wahrscheinlich so schreiben: Du lässt eine Variable
bei Index 0 beginnen, indexierst mit dieser Variable in den Vektor, um einen
Wert zu erhalten, und erhöhst den Wert der Variable in einer Schleife, bis er
die Gesamtzahl der Elemente im Vektor erreicht.

Iteratoren erledigen diese ganze Logik für dich und verringern so repetitiven
Code, bei dem dir Fehler unterlaufen könnten. Iteratoren geben dir mehr
Flexibilität, dieselbe Logik mit vielen verschiedenen Arten von Folgen zu
verwenden, nicht nur mit Datenstrukturen, die man indexieren kann, wie Vektoren.
Sehen wir uns an, wie Iteratoren das schaffen.

### Der Trait `Iterator` und die Methode `next` {#the-iterator-trait-and-the-next-method}

Alle Iteratoren implementieren einen Trait namens `Iterator`, der in der
Standardbibliothek definiert ist. Die Definition des Traits sieht so aus:

```rust
pub trait Iterator {
    type Item;

    fn next(&mut self) -> Option<Self::Item>;

    // methods with default implementations elided
}
```

Beachte, dass diese Definition neue Syntax verwendet: `type Item` und
`Self::Item`, die einen assoziierten Typ dieses Traits definieren. Über
assoziierte Typen sprechen wir ausführlich in Kapitel 20. Vorerst musst du nur
wissen, dass dieser Code besagt: Wer den Trait `Iterator` implementiert, muss
auch einen Typ `Item` definieren, und dieser Typ `Item` wird im Rückgabetyp der
Methode `next` verwendet. Mit anderen Worten: Der Typ `Item` ist der Typ, den
der Iterator zurückgibt.

Der Trait `Iterator` verlangt von Implementierern nur, eine Methode zu
definieren: die Methode `next`, die jeweils ein Element des Iterators in `Some`
verpackt zurückgibt und, wenn die Iteration vorbei ist, `None` zurückgibt.

Wir können die Methode `next` direkt auf Iteratoren aufrufen; Listing 13-12
zeigt, welche Werte von wiederholten Aufrufen von `next` auf dem aus dem Vektor
erzeugten Iterator zurückgegeben werden.

<Listing number="13-12" file-name="src/lib.rs" caption="Die Methode `next` auf einem Iterator aufrufen">

```rust,noplayground
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-12/src/lib.rs:here}}
```

</Listing>

Beachte, dass wir `v1_iter` veränderlich (_mutable_) machen mussten: Der Aufruf
der Methode `next` auf einem Iterator ändert einen internen Zustand, mit dem der
Iterator festhält, wo in der Folge er sich befindet. Mit anderen Worten: Dieser
Code _verbraucht_ (_consumes_) den Iterator. Jeder Aufruf von `next` verzehrt
ein Element des Iterators. Als wir eine `for`-Schleife verwendet haben, mussten
wir `v1_iter` nicht veränderlich machen, weil die Schleife die Ownership von
`v1_iter` übernommen und ihn hinter den Kulissen veränderlich gemacht hat.

Beachte außerdem, dass die Werte, die wir von den Aufrufen von `next` erhalten,
unveränderliche (_immutable_) Referenzen auf die Werte im Vektor sind. Die
Methode `iter` erzeugt einen Iterator über unveränderliche Referenzen. Wollen
wir einen Iterator erzeugen, der die Ownership von `v1` übernimmt und besessene
Werte zurückgibt, können wir statt `iter` die Methode `into_iter` aufrufen.
Ebenso können wir statt `iter` die Methode `iter_mut` aufrufen, wenn wir über
veränderliche Referenzen iterieren wollen.

### Methoden, die den Iterator verbrauchen {#methods-that-consume-the-iterator}

Der Trait `Iterator` hat eine Reihe verschiedener Methoden mit
Standardimplementierungen aus der Standardbibliothek; mehr über diese Methoden
erfährst du in der API-Dokumentation der Standardbibliothek zum Trait
`Iterator`. Einige dieser Methoden rufen in ihrer Definition die Methode `next`
auf, weshalb du die Methode `next` implementieren musst, wenn du den Trait
`Iterator` implementierst.

Methoden, die `next` aufrufen, heißen _verbrauchende Adapter_ (_consuming
adapters_), weil ihr Aufruf den Iterator aufbraucht. Ein Beispiel ist die
Methode `sum`, die die Ownership des Iterators übernimmt und über die Elemente
iteriert, indem sie wiederholt `next` aufruft, und so den Iterator verbraucht.
Beim Iterieren addiert sie jedes Element zu einer laufenden Summe und gibt die
Summe zurück, wenn die Iteration abgeschlossen ist. Listing 13-13 enthält einen
Test, der die Verwendung der Methode `sum` zeigt.

<Listing number="13-13" file-name="src/lib.rs" caption="Die Methode `sum` aufrufen, um die Summe aller Elemente im Iterator zu erhalten">

```rust,noplayground
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-13/src/lib.rs:here}}
```

</Listing>

Nach dem Aufruf von `sum` dürfen wir `v1_iter` nicht mehr verwenden, weil `sum`
die Ownership des Iterators übernimmt, auf dem wir es aufrufen.

### Methoden, die andere Iteratoren erzeugen {#methods-that-produce-other-iterators}

_Iterator-Adapter_ (_iterator adapters_) sind auf dem Trait `Iterator`
definierte Methoden, die den Iterator nicht verbrauchen. Stattdessen erzeugen
sie andere Iteratoren, indem sie einen Aspekt des ursprünglichen Iterators
ändern.

Listing 13-14 zeigt ein Beispiel für den Aufruf der Iterator-Adapter-Methode
`map`, die eine Closure nimmt, die beim Iterieren für jedes Element aufgerufen
wird. Die Methode `map` gibt einen neuen Iterator zurück, der die veränderten
Elemente erzeugt. Die Closure hier erzeugt einen neuen Iterator, in dem jedes
Element aus dem Vektor um 1 erhöht wird.

<Listing number="13-14" file-name="src/main.rs" caption="Den Iterator-Adapter `map` aufrufen, um einen neuen Iterator zu erzeugen">

```rust,not_desired_behavior
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-14/src/main.rs:here}}
```

</Listing>

Dieser Code erzeugt aber eine Warnung:

```console
{{#include ../listings/ch13-functional-features/listing-13-14/output.txt}}
```

Der Code in Listing 13-14 tut nichts; die von uns angegebene Closure wird nie
aufgerufen. Die Warnung erinnert uns daran, warum: Iterator-Adapter sind lazy,
und wir müssen den Iterator hier verbrauchen.

Um diese Warnung zu beheben und den Iterator zu verbrauchen, verwenden wir die
Methode `collect`, die wir in Listing 12-1 mit `env::args` verwendet haben.
Diese Methode verbraucht den Iterator und sammelt die resultierenden Werte in
einem Collection-Datentyp.

In Listing 13-15 sammeln wir die Ergebnisse der Iteration über den Iterator, den
der Aufruf von `map` zurückgibt, in einem Vektor. Dieser Vektor enthält am Ende
jedes Element aus dem ursprünglichen Vektor, um 1 erhöht.

<Listing number="13-15" file-name="src/main.rs" caption="Die Methode `map` aufrufen, um einen neuen Iterator zu erzeugen, und dann die Methode `collect` aufrufen, um den neuen Iterator zu verbrauchen und einen Vektor zu erzeugen">

```rust
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-15/src/main.rs:here}}
```

</Listing>

Da `map` eine Closure nimmt, können wir jede beliebige Operation angeben, die
für jedes Element ausgeführt werden soll. Das ist ein großartiges Beispiel
dafür, wie du mit Closures ein Verhalten anpassen und dabei das
Iterationsverhalten wiederverwenden kannst, das der Trait `Iterator`
bereitstellt.

Du kannst mehrere Aufrufe von Iterator-Adaptern verketten, um komplexe Aktionen
auf lesbare Weise auszuführen. Da aber alle Iteratoren lazy sind, musst du eine
der verbrauchenden Adapter-Methoden aufrufen, um Ergebnisse aus den Aufrufen der
Iterator-Adapter zu erhalten.

<!-- Old headings. Do not remove or links may break. -->

<a id="using-closures-that-capture-their-environment"></a>

### Closures, die ihre Umgebung erfassen {#closures-that-capture-their-environment}

Viele Iterator-Adapter nehmen Closures als Argumente, und häufig sind die
Closures, die wir Iterator-Adaptern als Argumente übergeben, Closures, die ihre
Umgebung erfassen.

Für dieses Beispiel verwenden wir die Methode `filter`, die eine Closure nimmt.
Die Closure erhält ein Element des Iterators und gibt einen `bool` zurück. Gibt
die Closure `true` zurück, wird der Wert in die von `filter` erzeugte Iteration
aufgenommen. Gibt die Closure `false` zurück, wird der Wert nicht aufgenommen.

In Listing 13-16 verwenden wir `filter` mit einer Closure, die die Variable
`shoe_size` aus ihrer Umgebung erfasst, um über eine Collection von Instanzen
des Structs `Shoe` zu iterieren. Sie gibt nur Schuhe in der angegebenen Größe
zurück.

<Listing number="13-16" file-name="src/lib.rs" caption="Die Methode `filter` mit einer Closure verwenden, die `shoe_size` erfasst">

```rust,noplayground
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-16/src/lib.rs}}
```

</Listing>

Die Funktion `shoes_in_size` übernimmt die Ownership eines Vektors von Schuhen
und eine Schuhgröße als Parameter. Sie gibt einen Vektor zurück, der nur Schuhe
der angegebenen Größe enthält.

Im Rumpf von `shoes_in_size` rufen wir `into_iter` auf, um einen Iterator zu
erzeugen, der die Ownership des Vektors übernimmt. Dann rufen wir `filter` auf,
um diesen Iterator in einen neuen Iterator umzuwandeln, der nur die Elemente
enthält, für die die Closure `true` zurückgibt.

Die Closure erfasst den Parameter `shoe_size` aus der Umgebung und vergleicht
den Wert mit der Größe jedes Schuhs, wobei nur Schuhe der angegebenen Größe
behalten werden. Schließlich sammelt der Aufruf von `collect` die vom
umgewandelten Iterator zurückgegebenen Werte in einem Vektor, den die Funktion
zurückgibt.

Der Test zeigt, dass wir beim Aufruf von `shoes_in_size` nur Schuhe
zurückbekommen, die dieselbe Größe haben wie der angegebene Wert.

{{#quiz ../quizzes/ch13-02-iterators.toml}}
