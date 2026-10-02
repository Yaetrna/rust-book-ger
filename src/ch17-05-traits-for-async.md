<!-- Old headings. Do not remove or links may break. -->

<a id="digging-into-the-traits-for-async"></a>

## Ein genauerer Blick auf die Traits für Async {#a-closer-look-at-the-traits-for-async}

Im Lauf des Kapitels haben wir die Traits `Future`, `Stream` und `StreamExt` auf
verschiedene Weise verwendet. Bisher haben wir es aber vermieden, zu tief in die
Details einzusteigen, wie sie funktionieren oder wie sie zusammenpassen, was für
deine tägliche Arbeit mit Rust meistens auch in Ordnung ist. Manchmal wirst du
aber auf Situationen stoßen, in denen du ein paar weitere Details dieser Traits
verstehen musst, zusammen mit dem Typ `Pin` und dem Trait `Unpin`. In diesem
Abschnitt steigen wir gerade so tief ein, dass es in solchen Szenarien hilft,
und überlassen den _wirklich_ tiefen Einstieg anderer Dokumentation.

<!-- Old headings. Do not remove or links may break. -->

<a id="future"></a>

### Der Trait `Future` {#the-future-trait}

Sehen wir uns zunächst genauer an, wie der Trait `Future` funktioniert. So
definiert Rust ihn:

```rust
use std::pin::Pin;
use std::task::{Context, Poll};

pub trait Future {
    type Output;

    fn poll(self: Pin<&mut Self>, cx: &mut Context<'_>) -> Poll<Self::Output>;
}
```

Diese Trait-Definition enthält eine ganze Reihe neuer Typen und auch etwas
Syntax, die wir noch nicht gesehen haben, also gehen wir die Definition Stück
für Stück durch.

Erstens gibt der assoziierte Typ `Output` von `Future` an, zu welchem Wert das
Future aufgelöst wird. Das entspricht dem assoziierten Typ `Item` des Traits
`Iterator`. Zweitens hat `Future` die Methode `poll`, die für ihren Parameter
`self` eine spezielle `Pin`-Referenz und eine veränderliche (_mutable_) Referenz
auf einen `Context`-Typ nimmt und ein `Poll<Self::Output>` zurückgibt. Über
`Pin` und `Context` sprechen wir gleich noch ausführlicher. Konzentrieren wir
uns vorerst darauf, was die Methode zurückgibt, den Typ `Poll`:

```rust
pub enum Poll<T> {
    Ready(T),
    Pending,
}
```

Dieser Typ `Poll` ähnelt einer `Option`. Er hat eine Variante mit einem Wert,
`Ready(T)`, und eine ohne, `Pending`. `Poll` bedeutet aber etwas ganz anderes
als `Option`! Die Variante `Pending` zeigt an, dass das Future noch Arbeit zu
erledigen hat, sodass der Aufrufer später erneut nachsehen muss. Die Variante
`Ready` zeigt an, dass das `Future` seine Arbeit erledigt hat und der Wert `T`
verfügbar ist.

> Note: Es ist selten nötig, `poll` direkt aufzurufen, aber wenn du es doch tun
> musst, denk daran, dass der Aufrufer bei den meisten Futures `poll` nicht
> erneut aufrufen sollte, nachdem das Future `Ready` zurückgegeben hat. Viele
> Futures lösen einen Panic aus, wenn sie erneut gepollt werden, nachdem sie
> fertig geworden sind. Futures, die sicher erneut gepollt werden können, sagen
> das ausdrücklich in ihrer Dokumentation. Das ähnelt dem Verhalten von
> `Iterator::next`.

Wenn du Code siehst, der `await` verwendet, kompiliert Rust ihn unter der Haube
zu Code, der `poll` aufruft. Wenn du dir noch einmal Listing 17-4 ansiehst, in
dem wir den Seitentitel für eine einzelne URL ausgegeben haben, sobald er
aufgelöst war, kompiliert Rust das zu etwas, das ungefähr (wenn auch nicht
genau) so aussieht:

```rust,ignore
match page_title(url).poll() {
    Ready(page_title) => match page_title {
        Some(title) => println!("The title for {url} was {title}"),
        None => println!("{url} had no title"),
    }
    Pending => {
        // But what goes here?
    }
}
```

Was sollen wir tun, wenn das Future noch `Pending` ist? Wir brauchen eine
Möglichkeit, es wieder und wieder und wieder zu versuchen, bis das Future
endlich fertig ist. Mit anderen Worten: Wir brauchen eine Schleife:

```rust,ignore
let mut page_title_fut = page_title(url);
loop {
    match page_title_fut.poll() {
        Ready(value) => match page_title {
            Some(title) => println!("The title for {url} was {title}"),
            None => println!("{url} had no title"),
        }
        Pending => {
            // continue
        }
    }
}
```

Würde Rust es aber genau zu diesem Code kompilieren, wäre jedes `await`
blockierend – genau das Gegenteil dessen, was wir erreichen wollten! Stattdessen
stellt Rust sicher, dass die Schleife die Kontrolle an etwas abgeben kann, das
die Arbeit an diesem Future unterbrechen kann, um an anderen Futures zu
arbeiten, und dieses dann später erneut prüft. Wie wir gesehen haben, ist dieses
Etwas eine Async-Runtime, und diese Planungs- und Koordinationsarbeit ist eine
ihrer Hauptaufgaben.

Im Abschnitt
[„Daten per Nachrichtenübermittlung zwischen zwei Tasks
senden“][message-passing]<!-- ignore --> haben wir beschrieben, wie auf
`rx.recv` gewartet wird. Der Aufruf von `recv` gibt ein Future zurück, und das
Abwarten des Futures pollt es. Wir haben angemerkt, dass eine Runtime das Future
pausiert, bis es entweder mit `Some(message)` oder, wenn der Kanal geschlossen
wird, mit `None` fertig ist. Mit unserem tieferen Verständnis des Traits
`Future` und insbesondere von `Future::poll` können wir sehen, wie das
funktioniert. Die Runtime weiß, dass das Future nicht fertig ist, wenn es
`Poll::Pending` zurückgibt. Umgekehrt weiß die Runtime, dass das Future fertig
_ist_, und treibt es voran, wenn `poll` `Poll::Ready(Some(message))` oder
`Poll::Ready(None)` zurückgibt.

Die genauen Details, wie eine Runtime das tut, gehen über den Rahmen dieses
Buches hinaus, aber entscheidend ist, die grundlegende Mechanik von Futures zu
verstehen: Eine Runtime _pollt_ jedes Future, für das sie verantwortlich ist,
und legt das Future wieder schlafen, wenn es noch nicht fertig ist.

<!-- Old headings. Do not remove or links may break. -->

<a id="pinning-and-the-pin-and-unpin-traits"></a>
<a id="the-pin-and-unpin-traits"></a>

### Der Typ `Pin` und der Trait `Unpin` {#the-pin-type-and-the-unpin-trait}

In Listing 17-13 haben wir das Makro `trpl::join!` verwendet, um auf drei
Futures zu warten. Häufig hat man aber eine Collection wie einen Vektor, die
eine Anzahl von Futures enthält, die erst zur Laufzeit bekannt ist. Ändern wir
Listing 17-13 zum Code in Listing 17-23, der die drei Futures in einen Vektor
legt und stattdessen die Funktion `trpl::join_all` aufruft, was noch nicht
kompiliert.

<Listing number="17-23" caption="Auf Futures in einer Collection warten"  file-name="src/main.rs">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch17-async-await/listing-17-23/src/main.rs:here}}
```

</Listing>

Wir legen jedes Future in eine `Box`, um sie zu _Trait-Objekten_ zu machen,
genau wie im Abschnitt „Fehler aus `run` zurückgeben“ in Kapitel 12.
(Trait-Objekte behandeln wir ausführlich in Kapitel 18.) Mit Trait-Objekten
können wir jedes der anonymen Futures, die von diesen Typen erzeugt werden, als
denselben Typ behandeln, weil sie alle den Trait `Future` implementieren.

Das mag überraschen. Schließlich gibt keiner der async-Blöcke etwas zurück,
sodass jeder ein `Future<Output = ()>` erzeugt. Denk aber daran, dass `Future`
ein Trait ist und der Compiler für jeden async-Block ein eigenes Enum erzeugt,
selbst wenn sie identische Ausgabetypen haben. So wie du nicht zwei verschiedene
handgeschriebene Structs in einen `Vec` legen kannst, kannst du auch keine vom
Compiler erzeugten Enums mischen.

Dann übergeben wir die Collection von Futures an die Funktion `trpl::join_all`
und warten auf das Ergebnis. Das kompiliert jedoch nicht; hier ist der relevante
Teil der Fehlermeldungen.

<!-- manual-regeneration
cd listings/ch17-async-await/listing-17-23
cargo build
copy *only* the final `error` block from the errors
-->

```text
error[E0277]: `dyn Future<Output = ()>` cannot be unpinned
  --> src/main.rs:48:33
   |
48 |         trpl::join_all(futures).await;
   |                                 ^^^^^ the trait `Unpin` is not implemented for `dyn Future<Output = ()>`
   |
   = note: consider using the `pin!` macro
           consider using `Box::pin` if you need to access the pinned value outside of the current scope
   = note: required for `Box<dyn Future<Output = ()>>` to implement `Future`
note: required by a bound in `futures_util::future::join_all::JoinAll`
  --> file:///home/.cargo/registry/src/index.crates.io-1949cf8c6b5b557f/futures-util-0.3.30/src/future/join_all.rs:29:8
   |
27 | pub struct JoinAll<F>
   |            ------- required by a bound in this struct
28 | where
29 |     F: Future,
   |        ^^^^^^ required by this bound in `JoinAll`
```

Der Hinweis in dieser Fehlermeldung sagt uns, dass wir das Makro `pin!`
verwenden sollen, um die Werte zu _fixieren_ (_pin_), was bedeutet, sie in den
Typ `Pin` zu legen, der garantiert, dass die Werte im Speicher nicht verschoben
(_moved_) werden. Laut Fehlermeldung ist das Fixieren nötig, weil
`dyn Future<Output = ()>` den Trait `Unpin` implementieren muss, was es derzeit
nicht tut.

Die Funktion `trpl::join_all` gibt ein Struct namens `JoinAll` zurück. Dieses
Struct ist generisch über einen Typ `F`, der darauf beschränkt ist, den Trait
`Future` zu implementieren. Wenn wir direkt mit `await` auf ein Future warten,
wird das Future implizit fixiert. Deshalb müssen wir `pin!` nicht überall
verwenden, wo wir auf Futures warten wollen.

Hier warten wir jedoch nicht direkt auf ein Future. Stattdessen konstruieren wir
ein neues Future, JoinAll, indem wir eine Collection von Futures an die Funktion
`join_all` übergeben. Die Signatur von `join_all` verlangt, dass die Typen der
Elemente in der Collection alle den Trait `Future` implementieren, und `Box<T>`
implementiert `Future` nur, wenn das `T`, das es umhüllt, ein Future ist, das
den Trait `Unpin` implementiert.

Das ist eine Menge zu verdauen! Um es wirklich zu verstehen, tauchen wir etwas
tiefer ein, wie der Trait `Future` tatsächlich funktioniert, insbesondere in
Bezug auf das Fixieren. Sieh dir noch einmal die Definition des Traits `Future`
an:

```rust
use std::pin::Pin;
use std::task::{Context, Poll};

pub trait Future {
    type Output;

    // Required method
    fn poll(self: Pin<&mut Self>, cx: &mut Context<'_>) -> Poll<Self::Output>;
}
```

Der Parameter `cx` und sein Typ `Context` sind der Schlüssel dazu, wie eine
Runtime tatsächlich weiß, wann sie ein bestimmtes Future prüfen muss, während
sie dennoch lazy bleibt. Auch hier gehen die Details, wie das funktioniert, über
den Rahmen dieses Kapitels hinaus, und darüber musst du im Allgemeinen nur
nachdenken, wenn du eine eigene `Future`-Implementierung schreibst. Wir
konzentrieren uns stattdessen auf den Typ von `self`, da wir hier zum ersten Mal
eine Methode sehen, bei der `self` eine Typannotation hat. Eine Typannotation
für `self` funktioniert wie Typannotationen für andere Funktionsparameter, aber
mit zwei wesentlichen Unterschieden:

- Sie teilt Rust mit, welchen Typ `self` haben muss, damit die Methode
  aufgerufen werden kann.
- Es kann nicht irgendein Typ sein. Er ist beschränkt auf den Typ, für den die
  Methode implementiert ist, eine Referenz oder einen Smart-Pointer auf diesen
  Typ oder einen `Pin`, der eine Referenz auf diesen Typ umhüllt.

Mehr zu dieser Syntax sehen wir in [Kapitel 18][ch-18]<!-- ignore -->. Vorerst
genügt es zu wissen, dass wir, wenn wir ein Future pollen wollen, um zu prüfen,
ob es `Pending` oder `Ready(Output)` ist, eine in `Pin` gehüllte veränderliche
Referenz auf den Typ brauchen.

`Pin` ist ein Wrapper für zeigerähnliche Typen wie `&`, `&mut`, `Box` und `Rc`.
(Technisch gesehen funktioniert `Pin` mit Typen, die die Traits `Deref` oder
`DerefMut` implementieren, aber das ist praktisch gleichbedeutend damit, nur mit
Referenzen und Smart-Pointern zu arbeiten.) `Pin` ist selbst kein Zeiger und hat
kein eigenes Verhalten, wie es `Rc` und `Arc` mit der Referenzzählung haben; es
ist ein reines Werkzeug, mit dem der Compiler Einschränkungen bei der Verwendung
von Zeigern durchsetzen kann.

Wenn wir uns daran erinnern, dass `await` mithilfe von Aufrufen von `poll`
implementiert ist, erklärt das allmählich die Fehlermeldung, die wir vorhin
gesehen haben, aber darin ging es um `Unpin`, nicht um `Pin`. Wie genau hängt
`Pin` also mit `Unpin` zusammen, und warum braucht `Future` `self` in einem
`Pin`-Typ, um `poll` aufzurufen?

Erinnere dich daran, dass eine Reihe von Await-Punkten in einem Future, wie
früher in diesem Kapitel beschrieben, zu einem Zustandsautomaten kompiliert wird
und der Compiler dafür sorgt, dass dieser Zustandsautomat alle normalen
Sicherheitsregeln von Rust einhält, einschließlich Borrowing und Ownership.
Damit das funktioniert, sieht sich Rust an, welche Daten zwischen einem
Await-Punkt und entweder dem nächsten Await-Punkt oder dem Ende des async-Blocks
benötigt werden. Dann erzeugt es eine entsprechende Variante im kompilierten
Zustandsautomaten. Jede Variante erhält den Zugriff, den sie auf die Daten
braucht, die in diesem Abschnitt des Quellcodes verwendet werden, sei es, indem
sie die Ownership an diesen Daten übernimmt, oder indem sie eine veränderliche
oder unveränderliche (_immutable_) Referenz darauf erhält.

So weit, so gut: Wenn wir bei der Ownership oder den Referenzen in einem
bestimmten async-Block etwas falsch machen, sagt uns das der Borrow-Checker.
Wenn wir das Future, das diesem Block entspricht, verschieben wollen – etwa in
einen `Vec`, um es an `join_all` zu übergeben –, wird es kniffliger.

Wenn wir ein Future verschieben (_move_) – sei es, indem wir es in eine
Datenstruktur legen, um es mit `join_all` als Iterator zu verwenden, oder indem
wir es aus einer Funktion zurückgeben –, bedeutet das tatsächlich, den
Zustandsautomaten zu verschieben, den Rust für uns erzeugt. Und anders als die
meisten anderen Typen in Rust können die Futures, die Rust für async-Blöcke
erzeugt, in den Feldern einer beliebigen Variante Referenzen auf sich selbst
enthalten, wie in der vereinfachten Darstellung in Abbildung 17-4 gezeigt.

<figure>

<img alt="Eine einspaltige Tabelle mit drei Zeilen, die ein Future fut1 darstellt, das in den ersten beiden Zeilen die Datenwerte 0 und 1 enthält und bei dem ein Pfeil von der dritten Zeile zurück auf die zweite Zeile zeigt, was eine interne Referenz innerhalb des Futures darstellt." src="img/trpl17-04.svg" class="center" />

<figcaption>Abbildung 17-4: Ein selbstreferenzieller Datentyp</figcaption>

</figure>

Standardmäßig ist es jedoch unsicher, ein Objekt zu verschieben, das eine
Referenz auf sich selbst hat, weil Referenzen immer auf die tatsächliche
Speicheradresse dessen zeigen, worauf sie verweisen (siehe Abbildung 17-5). Wenn
du die Datenstruktur selbst verschiebst, zeigen diese internen Referenzen
weiterhin auf die alte Stelle. Diese Speicherstelle ist nun aber ungültig. Zum
einen wird ihr Wert nicht aktualisiert, wenn du Änderungen an der Datenstruktur
vornimmst. Zum anderen – und das ist wichtiger – kann der Computer diesen
Speicher jetzt für andere Zwecke wiederverwenden! Du könntest später völlig
unzusammenhängende Daten lesen.

<figure>

<img alt="Zwei Tabellen, die zwei Futures fut1 und fut2 darstellen, jede mit einer Spalte und drei Zeilen, und die das Ergebnis zeigen, nachdem ein Future aus fut1 in fut2 verschoben wurde. Die erste, fut1, ist ausgegraut und hat in jeder Zeile ein Fragezeichen, was unbekannten Speicher darstellt. Die zweite, fut2, hat 0 und 1 in der ersten und zweiten Zeile und einen Pfeil, der von ihrer dritten Zeile zurück auf die zweite Zeile von fut1 zeigt, was einen Zeiger darstellt, der auf die alte Speicherstelle des Futures vor dem Verschieben verweist." src="img/trpl17-05.svg" class="center" />

<figcaption>Abbildung 17-5: Das unsichere Ergebnis, wenn ein selbstreferenzieller Datentyp verschoben wird</figcaption>

</figure>

Theoretisch könnte der Rust-Compiler versuchen, jede Referenz auf ein Objekt zu
aktualisieren, wann immer es verschoben wird, aber das könnte viel zusätzlichen
Performance-Aufwand bedeuten, besonders wenn ein ganzes Netz von Referenzen
aktualisiert werden muss. Wenn wir stattdessen sicherstellen könnten, dass sich
die betreffende Datenstruktur _im Speicher nicht bewegt_, müssten wir keine
Referenzen aktualisieren. Genau dafür ist der Borrow-Checker von Rust da: In
sicherem Code verhindert er, dass du ein Element verschiebst, auf das eine
aktive Referenz besteht.

`Pin` baut darauf auf, um uns genau die Garantie zu geben, die wir brauchen.
Wenn wir einen Wert _fixieren_, indem wir einen Zeiger auf diesen Wert in `Pin`
hüllen, kann er sich nicht mehr bewegen. Wenn du also `Pin<Box<SomeType>>` hast,
fixierst du tatsächlich den Wert `SomeType`, _nicht_ den Zeiger `Box`. Abbildung
17-6 veranschaulicht diesen Vorgang.

<figure>

<img alt="Drei Kästen nebeneinander. Der erste ist mit „Pin“ beschriftet, der zweite mit „b1“ und der dritte mit „pinned“. Innerhalb von „pinned“ befindet sich eine Tabelle mit der Beschriftung „fut“ und einer einzigen Spalte; sie stellt ein Future mit Zellen für jeden Teil der Datenstruktur dar. Ihre erste Zelle hat den Wert „0“, aus ihrer zweiten Zelle kommt ein Pfeil, der auf die vierte und letzte Zelle zeigt, die den Wert „1“ enthält, und die dritte Zelle hat gestrichelte Linien und Auslassungspunkte, die andeuten, dass die Datenstruktur weitere Teile haben kann. Insgesamt stellt die Tabelle „fut“ ein Future dar, das selbstreferenziell ist. Ein Pfeil verlässt den Kasten „Pin“, geht durch den Kasten „b1“ und endet innerhalb des Kastens „pinned“ an der Tabelle „fut“." src="img/trpl17-06.svg" class="center" />

<figcaption>Abbildung 17-6: Eine `Box` fixieren, die auf einen selbstreferenziellen Future-Typ zeigt</figcaption>

</figure>

Tatsächlich kann sich der Zeiger `Box` weiterhin frei bewegen. Denk daran: Uns
geht es darum sicherzustellen, dass die Daten, auf die letztlich verwiesen wird,
an ihrem Platz bleiben. Wenn sich ein Zeiger bewegt, _die Daten, auf die er
zeigt_, aber an derselben Stelle bleiben, wie in Abbildung 17-7, gibt es kein
potenzielles Problem. (Sieh dir als eigenständige Übung die Dokumentation der
Typen sowie des Moduls `std::pin` an und versuche herauszufinden, wie du das mit
einem `Pin` machen würdest, der eine `Box` umhüllt.) Entscheidend ist, dass sich
der selbstreferenzielle Typ selbst nicht bewegen kann, weil er weiterhin fixiert
ist.

<figure>

<img alt="Vier Kästen in grob drei Spalten, identisch mit dem vorherigen Diagramm bis auf eine Änderung in der zweiten Spalte. Jetzt gibt es in der zweiten Spalte zwei Kästen mit den Beschriftungen „b1“ und „b2“, „b1“ ist ausgegraut, und der Pfeil von „Pin“ geht durch „b2“ statt durch „b1“, was anzeigt, dass der Zeiger von „b1“ nach „b2“ verschoben wurde, die Daten in „pinned“ aber nicht." src="img/trpl17-07.svg" class="center" />

<figcaption>Abbildung 17-7: Eine `Box` verschieben, die auf einen selbstreferenziellen Future-Typ zeigt</figcaption>

</figure>

Die meisten Typen lassen sich jedoch völlig sicher verschieben, selbst wenn sie
sich hinter einem `Pin`-Zeiger befinden. Über das Fixieren müssen wir nur
nachdenken, wenn Elemente interne Referenzen haben. Primitive Werte wie Zahlen
und Boolesche Werte sind sicher, weil sie offensichtlich keine internen
Referenzen haben. Das gilt auch für die meisten Typen, mit denen du in Rust
normalerweise arbeitest. Einen `Vec` kannst du zum Beispiel ohne Bedenken
verschieben. Nach dem, was wir bisher gesehen haben, müsstest du bei einem
`Pin<Vec<String>>` alles über die sicheren, aber einschränkenden APIs von `Pin`
erledigen, obwohl ein `Vec<String>` immer sicher verschoben werden kann, wenn es
keine anderen Referenzen darauf gibt. Wir brauchen eine Möglichkeit, dem
Compiler mitzuteilen, dass es in solchen Fällen in Ordnung ist, Elemente zu
verschieben – und hier kommt `Unpin` ins Spiel.

`Unpin` ist ein Marker-Trait, ähnlich wie die Traits `Send` und `Sync`, die wir
in Kapitel 16 gesehen haben, und hat daher keine eigene Funktionalität.
Marker-Traits existieren nur, um dem Compiler mitzuteilen, dass es sicher ist,
den Typ, der einen bestimmten Trait implementiert, in einem bestimmten Kontext
zu verwenden. `Unpin` teilt dem Compiler mit, dass ein bestimmter Typ _keine_
Garantien darüber einhalten muss, ob der betreffende Wert sicher verschoben
werden kann.

<!--
  The inline `<code>` in the next block is to allow the inline `<em>` inside it,
  matching what NoStarch does style-wise, and emphasizing within the text here
  that it is something distinct from a normal type.
-->

Genau wie bei `Send` und `Sync` implementiert der Compiler `Unpin` automatisch
für alle Typen, bei denen er beweisen kann, dass es sicher ist. Ein Sonderfall,
wiederum ähnlich wie bei `Send` und `Sync`, liegt vor, wenn `Unpin` für einen
Typ _nicht_ implementiert ist. Die Notation dafür ist
<code>impl !Unpin for <em>SomeType</em></code>, wobei
<code><em>SomeType</em></code> der Name eines Typs ist, der diese Garantien
_tatsächlich_ einhalten muss, um sicher zu sein, wann immer ein Zeiger auf
diesen Typ in einem `Pin` verwendet wird.

Mit anderen Worten: Beim Verhältnis zwischen `Pin` und `Unpin` gibt es zwei
Dinge zu beachten. Erstens ist `Unpin` der „normale“ Fall und `!Unpin` der
Sonderfall. Zweitens spielt es _nur_ dann eine Rolle, ob ein Typ `Unpin` oder
`!Unpin` implementiert, wenn du einen fixierten Zeiger auf diesen Typ wie
<code>Pin<&mut
<em>SomeType</em>></code> verwendest.

Um das konkret zu machen, denk an einen `String`: Er hat eine Länge und die
Unicode-Zeichen, aus denen er besteht. Wir können einen `String` in `Pin`
hüllen, wie in Abbildung 17-8 zu sehen. `String` implementiert jedoch
automatisch `Unpin`, wie die meisten anderen Typen in Rust auch.

<figure>

<img alt="Ein Kasten mit der Beschriftung „Pin“ links, von dem ein Pfeil zu einem Kasten mit der Beschriftung „String“ rechts führt. Der Kasten „String“ enthält die Daten 5usize, die die Länge des Strings darstellen, und die Buchstaben „h“, „e“, „l“, „l“ und „o“, die die Zeichen des Strings „hello“ darstellen, der in dieser String-Instanz gespeichert ist. Ein gepunktetes Rechteck umgibt den Kasten „String“ und seine Beschriftung, aber nicht den Kasten „Pin“." src="img/trpl17-08.svg" class="center" />

<figcaption>Abbildung 17-8: Einen `String` fixieren; die gepunktete Linie zeigt an, dass der `String` den Trait `Unpin` implementiert und daher nicht fixiert ist</figcaption>

</figure>

Daher können wir Dinge tun, die unzulässig wären, wenn `String` stattdessen
`!Unpin` implementieren würde, etwa einen String an genau derselben
Speicherstelle durch einen anderen ersetzen, wie in Abbildung 17-9. Das verletzt
den Vertrag von `Pin` nicht, weil `String` keine internen Referenzen hat, die
das Verschieben unsicher machen würden. Genau deshalb implementiert er `Unpin`
statt `!Unpin`.

<figure>

<img alt="Dieselben String-Daten „hello“ aus dem vorherigen Beispiel, jetzt mit „s1“ beschriftet und ausgegraut. Der Kasten „Pin“ aus dem vorherigen Beispiel zeigt jetzt auf eine andere String-Instanz, die mit „s2“ beschriftet ist, gültig ist, eine Länge von 7usize hat und die Zeichen des Strings „goodbye“ enthält. s2 ist von einem gepunkteten Rechteck umgeben, weil auch er den Trait Unpin implementiert." src="img/trpl17-09.svg" class="center" />

<figcaption>Abbildung 17-9: Den `String` im Speicher durch einen völlig anderen `String` ersetzen</figcaption>

</figure>

Jetzt wissen wir genug, um die Fehler zu verstehen, die für den Aufruf von
`join_all` in Listing 17-23 gemeldet wurden. Ursprünglich haben wir versucht,
die von async-Blöcken erzeugten Futures in einen
`Vec<Box<dyn Future<Output = ()>>>` zu verschieben, aber wie wir gesehen haben,
können diese Futures interne Referenzen haben, sodass sie `Unpin` nicht
automatisch implementieren. Sobald wir sie fixieren, können wir den
resultierenden `Pin`-Typ in den `Vec` legen und sicher sein, dass die zugrunde
liegenden Daten in den Futures _nicht_ verschoben werden. Listing 17-24 zeigt,
wie man den Code korrigiert, indem man dort, wo jedes der drei Futures definiert
wird, das Makro `pin!` aufruft und den Typ des Trait-Objekts anpasst.

<Listing number="17-24" caption="Die Futures fixieren, damit sie in den Vektor verschoben werden können">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-24/src/main.rs:here}}
```

</Listing>

Dieses Beispiel kompiliert und läuft jetzt, und wir könnten zur Laufzeit Futures
zum Vektor hinzufügen oder daraus entfernen und sie alle zusammenführen.

`Pin` und `Unpin` sind vor allem beim Bau von Bibliotheken auf niedrigerer Ebene
wichtig oder wenn du selbst eine Runtime baust, weniger für alltäglichen
Rust-Code. Wenn du diese Traits aber in Fehlermeldungen siehst, hast du jetzt
eine bessere Vorstellung davon, wie du deinen Code korrigieren kannst!

> Note: Diese Kombination aus `Pin` und `Unpin` ermöglicht es, eine ganze Klasse
> komplexer Typen in Rust sicher zu implementieren, die sonst schwierig wären,
> weil sie selbstreferenziell sind. Typen, die `Pin` erfordern, tauchen heute am
> häufigsten in asynchronem Rust auf, aber hin und wieder begegnen sie dir auch
> in anderen Kontexten.
>
> Die Einzelheiten, wie `Pin` und `Unpin` funktionieren, und die Regeln, die sie
> einhalten müssen, werden ausführlich in der API-Dokumentation von `std::pin`
> behandelt; wenn du mehr darüber erfahren möchtest, ist das ein guter
> Ausgangspunkt.
>
> Wenn du noch genauer verstehen willst, wie die Dinge unter der Haube
> funktionieren, sieh dir die Kapitel [2][under-the-hood]<!-- ignore --> und
> [4][pinning]<!-- ignore --> von
> [_Asynchronous Programming in Rust_][async-book] an.

### Der Trait `Stream` {#the-stream-trait}

Jetzt, da du die Traits `Future`, `Pin` und `Unpin` besser verstehst, können wir
uns dem Trait `Stream` zuwenden. Wie du früher in diesem Kapitel gelernt hast,
ähneln Streams asynchronen Iteratoren. Anders als für `Iterator` und `Future`
gibt es für `Stream` zum Zeitpunkt der Entstehung dieses Textes jedoch keine
Definition in der Standardbibliothek, aber es _gibt_ eine sehr verbreitete
Definition aus dem Crate `futures`, die im gesamten Ökosystem verwendet wird.

Sehen wir uns noch einmal die Definitionen der Traits `Iterator` und `Future`
an, bevor wir betrachten, wie ein Trait `Stream` sie zusammenführen könnte. Von
`Iterator` haben wir die Idee einer Folge: Seine Methode `next` liefert eine
`Option<Self::Item>`. Von `Future` haben wir die Idee der Bereitschaft im Lauf
der Zeit: Seine Methode `poll` liefert ein `Poll<Self::Output>`. Um eine Folge
von Elementen darzustellen, die im Lauf der Zeit bereit werden, definieren wir
einen Trait `Stream`, der diese Merkmale zusammenführt:

```rust
use std::pin::Pin;
use std::task::{Context, Poll};

trait Stream {
    type Item;

    fn poll_next(
        self: Pin<&mut Self>,
        cx: &mut Context<'_>
    ) -> Poll<Option<Self::Item>>;
}
```

Der Trait `Stream` definiert einen assoziierten Typ namens `Item` für den Typ
der Elemente, die der Stream erzeugt. Das ähnelt `Iterator`, wo es null bis
viele Elemente geben kann, und unterscheidet sich von `Future`, wo es immer
genau ein `Output` gibt, selbst wenn es der Unit-Typ `()` ist.

`Stream` definiert außerdem eine Methode, um diese Elemente abzurufen. Wir
nennen sie `poll_next`, um deutlich zu machen, dass sie auf dieselbe Weise pollt
wie `Future::poll` und auf dieselbe Weise eine Folge von Elementen erzeugt wie
`Iterator::next`. Ihr Rückgabetyp kombiniert `Poll` mit `Option`. Der äußere Typ
ist `Poll`, weil auf Bereitschaft geprüft werden muss, genau wie bei einem
Future. Der innere Typ ist `Option`, weil signalisiert werden muss, ob es
weitere Nachrichten gibt, genau wie bei einem Iterator.

Etwas sehr Ähnliches wie diese Definition wird wahrscheinlich irgendwann Teil
der Standardbibliothek von Rust werden. In der Zwischenzeit ist es Teil des
Werkzeugkastens der meisten Runtimes, sodass du dich darauf verlassen kannst,
und alles, was wir als Nächstes behandeln, sollte im Allgemeinen zutreffen!

In den Beispielen, die wir im Abschnitt
[„Streams: Futures in Folge“][streams]<!--
ignore --> gesehen haben, haben wir aber weder `poll_next` _noch_ `Stream`
verwendet, sondern `next` und `StreamExt`. Wir _könnten_ natürlich direkt mit
der API `poll_next` arbeiten, indem wir eigene `Stream`-Zustandsautomaten von
Hand schreiben, genauso wie wir mit Futures direkt über ihre Methode `poll`
arbeiten _könnten_. Mit `await` ist es aber viel angenehmer, und der Trait
`StreamExt` stellt die Methode `next` bereit, sodass wir genau das tun können:

```rust
{{#rustdoc_include ../listings/ch17-async-await/no-listing-stream-ext/src/lib.rs:here}}
```

<!--
TODO: update this if/when tokio/etc. update their MSRV and switch to using async functions
in traits, since the lack thereof is the reason they do not yet have this.
-->

> Note: Die tatsächliche Definition, die wir früher im Kapitel verwendet haben,
> sieht etwas anders aus, weil sie Rust-Versionen unterstützt, die
> async-Funktionen in Traits noch nicht unterstützten. Daher sieht sie so aus:
>
> ```rust,ignore
> fn next(&mut self) -> Next<'_, Self> where Self: Unpin;
> ```
>
> Dieser Typ `Next` ist ein `struct`, das `Future` implementiert und es uns
> ermöglicht, die Lifetime der Referenz auf `self` mit `Next<'_, Self>` zu
> benennen, sodass `await` mit dieser Methode funktionieren kann.

Der Trait `StreamExt` ist auch die Heimat all der interessanten Methoden, die
für Streams zur Verfügung stehen. `StreamExt` wird automatisch für jeden Typ
implementiert, der `Stream` implementiert, aber diese Traits sind getrennt
definiert, damit die Community an komfortablen APIs weiterarbeiten kann, ohne
den grundlegenden Trait zu beeinträchtigen.

In der Version von `StreamExt`, die im Crate `trpl` verwendet wird, definiert
der Trait nicht nur die Methode `next`, sondern stellt auch eine
Standardimplementierung von `next` bereit, die die Details des Aufrufs von
`Stream::poll_next` korrekt behandelt. Das bedeutet, dass du selbst dann, wenn
du deinen eigenen Streaming-Datentyp schreiben musst, _nur_ `Stream`
implementieren musst, und dann kann jeder, der deinen Datentyp verwendet,
automatisch `StreamExt` und seine Methoden damit verwenden.

Das ist alles, was wir zu den Details dieser Traits auf niedrigerer Ebene
behandeln werden. Betrachten wir zum Schluss, wie Futures (einschließlich
Streams), Tasks und Threads zusammenpassen!

{{#quiz ../quizzes/async-05-traits-for-async.toml}}

[message-passing]: ch17-02-concurrency-with-async.md#sending-data-between-two-tasks-using-message-passing
[ch-18]: ch18-00-oop.html
[async-book]: https://rust-lang.github.io/async-book/
[under-the-hood]: https://rust-lang.github.io/async-book/02_execution/01_chapter.html
[pinning]: https://rust-lang.github.io/async-book/04_pinning/01_chapter.html
[first-async]: ch17-01-futures-and-syntax.html#our-first-async-program
[any-number-futures]: ch17-03-more-futures.html#working-with-any-number-of-futures
[streams]: ch17-04-streams.html
