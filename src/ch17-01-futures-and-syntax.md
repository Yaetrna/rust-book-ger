## Futures und die Async-Syntax {#futures-and-the-async-syntax}

Die zentralen Elemente der asynchronen Programmierung in Rust sind _Futures_ und
die Schlüsselwörter `async` und `await` von Rust.

Ein _Future_ ist ein Wert, der jetzt vielleicht noch nicht bereit ist, aber
irgendwann in der Zukunft bereit sein wird. (Dasselbe Konzept gibt es in vielen
Sprachen, manchmal unter anderen Namen wie _Task_ oder _Promise_.) Rust stellt
einen Trait `Future` als Baustein bereit, damit verschiedene asynchrone
Operationen mit unterschiedlichen Datenstrukturen, aber mit einer gemeinsamen
Schnittstelle implementiert werden können. In Rust sind Futures Typen, die den
Trait `Future` implementieren. Jedes Future enthält seine eigenen Informationen
darüber, welcher Fortschritt erzielt wurde und was „bereit“ bedeutet.

Du kannst das Schlüsselwort `async` auf Blöcke und Funktionen anwenden, um
anzugeben, dass sie unterbrochen und fortgesetzt werden können. Innerhalb eines
async-Blocks oder einer async-Funktion kannst du mit dem Schlüsselwort `await`
ein _Future abwarten_ (_await_), also darauf warten, dass es bereit wird. Jede
Stelle, an der du innerhalb eines async-Blocks oder einer async-Funktion ein
Future abwartest, ist eine mögliche Stelle, an der dieser Block oder diese
Funktion pausieren und fortgesetzt werden kann. Den Vorgang, bei einem Future
nachzufragen, ob sein Wert schon verfügbar ist, nennt man _Polling_.

Einige andere Sprachen wie C# und JavaScript verwenden für asynchrone
Programmierung ebenfalls die Schlüsselwörter `async` und `await`. Wenn du diese
Sprachen kennst, fallen dir vielleicht einige wesentliche Unterschiede in der
Art auf, wie Rust die Syntax handhabt. Dafür gibt es gute Gründe, wie wir sehen
werden!

Wenn wir asynchrones Rust schreiben, verwenden wir meistens die Schlüsselwörter
`async` und `await`. Rust kompiliert sie in gleichwertigen Code, der den Trait
`Future` verwendet, ähnlich wie es `for`-Schleifen in gleichwertigen Code
kompiliert, der den Trait `Iterator` verwendet. Da Rust den Trait `Future`
bereitstellt, kannst du ihn aber auch für deine eigenen Datentypen
implementieren, wenn du das brauchst. Viele der Funktionen, die wir in diesem
Kapitel sehen, geben Typen mit eigenen Implementierungen von `Future` zurück.
Wir kehren am Ende des Kapitels zur Definition des Traits zurück und sehen uns
genauer an, wie er funktioniert, aber diese Details genügen, um weiterzukommen.

Das wirkt vielleicht alles etwas abstrakt, also schreiben wir unser erstes
asynchrones Programm: einen kleinen Web-Scraper. Wir übergeben zwei URLs auf der
Kommandozeile, rufen beide nebenläufig ab und geben das Ergebnis desjenigen
zurück, der zuerst fertig ist. Dieses Beispiel enthält einiges an neuer Syntax,
aber keine Sorge – wir erklären unterwegs alles, was du wissen musst.

## Unser erstes asynchrones Programm {#our-first-async-program}

Damit sich dieses Kapitel auf das Lernen von Async konzentriert und nicht auf
das Jonglieren mit Teilen des Ökosystems, haben wir das Crate `trpl` erstellt
(`trpl` ist kurz für „The Rust Programming Language“). Es reexportiert alle
Typen, Traits und Funktionen, die du brauchst, hauptsächlich aus den Crates
[`futures`][futures-crate]<!-- ignore --> und [`tokio`][tokio]<!-- ignore -->.
Das Crate `futures` ist ein offizielles Zuhause für Experimente mit asynchronem
Code in Rust, und dort wurde ursprünglich auch der Trait `Future` entworfen.
Tokio ist heute die am weitesten verbreitete Async-Runtime in Rust, besonders
für Webanwendungen. Es gibt noch andere großartige Runtimes, und sie eignen sich
für deine Zwecke vielleicht besser. Wir verwenden für `trpl` unter der Haube das
Crate `tokio`, weil es gut getestet und weit verbreitet ist.

In manchen Fällen benennt `trpl` die ursprünglichen APIs auch um oder verpackt
sie, damit du dich auf die Details konzentrieren kannst, die für dieses Kapitel
relevant sind. Wenn du verstehen willst, was das Crate tut, empfehlen wir dir,
dir [seinen Quellcode][crate-source] anzusehen. Dort siehst du, aus welchem
Crate jeder Re-Export stammt, und wir haben ausführliche Kommentare
hinterlassen, die erklären, was das Crate tut.

Erstelle ein neues Binärprojekt namens `hello-async` und füge das Crate `trpl`
als Abhängigkeit hinzu:

```console
$ cargo new hello-async
$ cd hello-async
$ cargo add trpl
```

Jetzt können wir die verschiedenen Bausteine aus `trpl` verwenden, um unser
erstes asynchrones Programm zu schreiben. Wir bauen ein kleines
Kommandozeilenwerkzeug, das zwei Webseiten abruft, aus jeder das Element
`<title>` herausholt und den Titel der Seite ausgibt, die diesen ganzen Vorgang
zuerst abschließt.

### Die Funktion page_title definieren {#defining-the-page_title-function}

Beginnen wir mit einer Funktion, die eine Seiten-URL als Parameter nimmt, eine
Anfrage daran sendet und den Text des Elements `<title>` zurückgibt (siehe
Listing 17-1).

<Listing number="17-1" file-name="src/main.rs" caption="Eine async-Funktion definieren, die das Titel-Element aus einer HTML-Seite holt">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-01/src/main.rs:all}}
```

</Listing>

Zuerst definieren wir eine Funktion namens `page_title` und kennzeichnen sie mit
dem Schlüsselwort `async`. Dann verwenden wir die Funktion `trpl::get`, um die
übergebene URL abzurufen, und fügen das Schlüsselwort `await` hinzu, um die
Antwort abzuwarten. Um den Text der `response` zu erhalten, rufen wir ihre
Methode `text` auf und warten sie erneut mit dem Schlüsselwort `await` ab. Beide
Schritte sind asynchron. Bei der Funktion `get` müssen wir darauf warten, dass
der Server den ersten Teil seiner Antwort zurücksendet, der HTTP-Header, Cookies
und so weiter enthält und getrennt vom Rumpf der Antwort geliefert werden kann.
Besonders wenn der Rumpf sehr groß ist, kann es einige Zeit dauern, bis alles
angekommen ist. Da wir darauf warten müssen, dass die Antwort _vollständig_
ankommt, ist auch die Methode `text` asynchron.

Wir müssen beide Futures explizit abwarten, weil Futures in Rust _lazy_ (träge)
sind: Sie tun nichts, bis du sie mit dem Schlüsselwort `await` dazu aufforderst.
(Tatsächlich zeigt Rust eine Compilerwarnung an, wenn du ein Future nicht
verwendest.) Das erinnert dich vielleicht an die Besprechung von Iteratoren im
Abschnitt
[„Eine Folge von Elementen mit Iteratoren verarbeiten“][iterators-lazy]<!-- ignore -->
in Kapitel 13. Iteratoren tun nichts, solange du nicht ihre Methode `next`
aufrufst – ob direkt oder über `for`-Schleifen oder Methoden wie `map`, die
unter der Haube `next` verwenden. Ebenso tun Futures nichts, solange du sie
nicht explizit dazu aufforderst. Durch diese Trägheit kann Rust vermeiden,
asynchronen Code auszuführen, bevor er tatsächlich gebraucht wird.

> Note: Das unterscheidet sich von dem Verhalten, das wir bei `thread::spawn` im
> Abschnitt
> [„Einen neuen Thread mit spawn erzeugen“][thread-spawn]<!-- ignore --> in
> Kapitel 16 gesehen haben, wo die Closure, die wir an einen anderen Thread
> übergeben haben, sofort zu laufen begann. Es unterscheidet sich auch davon,
> wie viele andere Sprachen Async angehen. Für Rust ist es aber wichtig, um
> seine Performance-Garantien bieten zu können, genau wie bei Iteratoren.

Sobald wir `response_text` haben, können wir es mit `Html::parse` in eine
Instanz des Typs `Html` parsen. Statt eines rohen Strings haben wir jetzt einen
Datentyp, mit dem wir das HTML als reichhaltigere Datenstruktur bearbeiten
können. Insbesondere können wir mit der Methode `select_first` das erste
Vorkommen eines bestimmten CSS-Selektors finden. Indem wir den String `"title"`
übergeben, erhalten wir das erste Element `<title>` im Dokument, falls es eines
gibt. Da es möglicherweise kein passendes Element gibt, gibt `select_first` eine
`Option<ElementRef>` zurück. Schließlich verwenden wir die Methode
`Option::map`, mit der wir mit dem Element in der `Option` arbeiten können,
falls es vorhanden ist, und nichts tun, falls nicht. (Wir könnten hier auch
einen `match`-Ausdruck verwenden, aber `map` ist idiomatischer.) Im Rumpf der
Funktion, die wir an `map` übergeben, rufen wir `inner_html` auf dem `title`
auf, um seinen Inhalt zu erhalten, einen `String`. Am Ende haben wir eine
`Option<String>`.

Beachte, dass das Schlüsselwort `await` in Rust _hinter_ dem Ausdruck steht, den
du abwartest, nicht davor. Es ist also ein _Postfix_-Schlüsselwort. Das weicht
vielleicht davon ab, was du gewohnt bist, wenn du `async` in anderen Sprachen
verwendet hast, aber in Rust lässt sich so viel angenehmer mit Methodenketten
arbeiten. Daher könnten wir den Rumpf von `page_title` so ändern, dass die
Funktionsaufrufe `trpl::get` und `text` mit `await` dazwischen verkettet werden,
wie in Listing 17-2 gezeigt.

<Listing number="17-2" file-name="src/main.rs" caption="Verketten mit dem Schlüsselwort `await`">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-02/src/main.rs:chaining}}
```

</Listing>

Damit haben wir erfolgreich unsere erste async-Funktion geschrieben! Bevor wir
in `main` Code hinzufügen, der sie aufruft, sprechen wir noch etwas mehr
darüber, was wir geschrieben haben und was es bedeutet.

Wenn Rust einen mit dem Schlüsselwort `async` gekennzeichneten _Block_ sieht,
kompiliert es ihn in einen eindeutigen, anonymen Datentyp, der den Trait
`Future` implementiert. Wenn Rust eine mit `async` gekennzeichnete _Funktion_
sieht, kompiliert es sie in eine nicht asynchrone Funktion, deren Rumpf ein
async-Block ist. Der Rückgabetyp einer async-Funktion ist der Typ des anonymen
Datentyps, den der Compiler für diesen async-Block erzeugt.

`async fn` zu schreiben, ist also gleichwertig damit, eine Funktion zu
schreiben, die ein _Future_ des Rückgabetyps zurückgibt. Für den Compiler ist
eine Funktionsdefinition wie `async fn page_title` in Listing 17-1 ungefähr
gleichwertig mit einer nicht asynchronen Funktion, die so definiert ist:

```rust
# extern crate trpl; // required for mdbook test
use std::future::Future;
use trpl::Html;

fn page_title(url: &str) -> impl Future<Output = Option<String>> {
    async move {
        let text = trpl::get(url).await.text().await;
        Html::parse(&text)
            .select_first("title")
            .map(|title| title.inner_html())
    }
}
```

Gehen wir die einzelnen Teile der umgewandelten Version durch:

- Sie verwendet die Syntax `impl Trait`, die wir in Kapitel 10 im Abschnitt
  [„Traits als Parameter verwenden“][impl-trait]<!-- ignore --> besprochen
  haben.
- Der zurückgegebene Wert implementiert den Trait `Future` mit einem
  assoziierten Typ `Output`. Beachte, dass der Typ `Output` `Option<String>`
  ist, also derselbe wie der ursprüngliche Rückgabetyp der Version `async fn`
  von `page_title`.
- Der gesamte Code, der im Rumpf der ursprünglichen Funktion aufgerufen wird,
  ist in einen `async move`-Block verpackt. Denk daran, dass Blöcke Ausdrücke
  sind. Dieser ganze Block ist der Ausdruck, den die Funktion zurückgibt.
- Dieser async-Block erzeugt einen Wert vom Typ `Option<String>`, wie eben
  beschrieben. Dieser Wert passt zum Typ `Output` im Rückgabetyp. Das ist genau
  wie bei anderen Blöcken, die du gesehen hast.
- Der neue Funktionsrumpf ist wegen der Art, wie er den Parameter `url`
  verwendet, ein `async move`-Block. (Über `async` im Vergleich zu `async move`
  sprechen wir später in diesem Kapitel noch ausführlich.)

Jetzt können wir `page_title` in `main` aufrufen.

<!-- Old headings. Do not remove or links may break. -->

<a id ="determining-a-single-pages-title"></a>

### Eine async-Funktion mit einer Runtime ausführen {#executing-an-async-function-with-a-runtime}

Zuerst holen wir den Titel einer einzelnen Seite, wie in Listing 17-3 gezeigt.
Leider kompiliert dieser Code noch nicht.

<Listing number="17-3" file-name="src/main.rs" caption="Die Funktion `page_title` aus `main` mit einem vom Benutzer angegebenen Argument aufrufen">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch17-async-await/listing-17-03/src/main.rs:main}}
```

</Listing>

Wir folgen demselben Schema, mit dem wir im Abschnitt
[„Kommandozeilenargumente entgegennehmen“][cli-args]<!-- ignore --> in Kapitel
12 Kommandozeilenargumente erhalten haben. Dann übergeben wir das URL-Argument
an `page_title` und warten das Ergebnis ab. Da der vom Future erzeugte Wert eine
`Option<String>` ist, verwenden wir einen `match`-Ausdruck, um unterschiedliche
Meldungen auszugeben, je nachdem, ob die Seite einen `<title>` hatte.

Das Schlüsselwort `await` können wir nur in async-Funktionen oder -Blöcken
verwenden, und Rust lässt uns die besondere Funktion `main` nicht als `async`
kennzeichnen.

<!-- manual-regeneration
cd listings/ch17-async-await/listing-17-03
cargo build
copy just the compiler error
-->

```text
error[E0752]: `main` function is not allowed to be `async`
 --> src/main.rs:6:1
  |
6 | async fn main() {
  | ^^^^^^^^^^^^^^^ `main` function is not allowed to be `async`
```

`main` kann nicht als `async` gekennzeichnet werden, weil asynchroner Code eine
_Runtime_ braucht: ein Rust-Crate, das die Details der Ausführung asynchronen
Codes verwaltet. Die Funktion `main` eines Programms kann eine Runtime
_initialisieren_, ist aber _selbst_ keine Runtime. (Warum das so ist, sehen wir
gleich noch genauer.) Jedes Rust-Programm, das asynchronen Code ausführt, hat
mindestens eine Stelle, an der es eine Runtime einrichtet, die die Futures
ausführt.

Die meisten Sprachen, die Async unterstützen, bringen eine Runtime mit, Rust
aber nicht. Stattdessen gibt es viele verschiedene Async-Runtimes, von denen
jede andere Kompromisse eingeht, die zu ihrem jeweiligen Anwendungsfall passen.
Ein Webserver mit hohem Durchsatz, vielen CPU-Kernen und viel RAM hat zum
Beispiel ganz andere Anforderungen als ein Mikrocontroller mit einem einzigen
Kern, wenig RAM und ohne die Möglichkeit, auf dem Heap zu allozieren. Die
Crates, die diese Runtimes bereitstellen, bieten oft auch asynchrone Versionen
gängiger Funktionalität wie Datei- oder Netzwerk-I/O.

Hier und im Rest dieses Kapitels verwenden wir die Funktion `block_on` aus dem
Crate `trpl`, die ein Future als Argument nimmt und den aktuellen Thread
blockiert, bis dieses Future vollständig ausgeführt ist. Hinter den Kulissen
richtet der Aufruf von `block_on` mit dem Crate `tokio` eine Runtime ein, die
das übergebene Future ausführt (das Verhalten von `block_on` aus dem Crate
`trpl` ähnelt den `block_on`-Funktionen anderer Runtime-Crates). Sobald das
Future fertig ist, gibt `block_on` den Wert zurück, den das Future erzeugt hat.

Wir könnten das von `page_title` zurückgegebene Future direkt an `block_on`
übergeben und, sobald es fertig ist, per Pattern-Matching auf die resultierende
`Option<String>` prüfen, wie wir es in Listing 17-3 versucht haben. In den
meisten Beispielen dieses Kapitels (und in den meisten asynchronen Codes in der
Praxis) machen wir aber mehr als nur einen async-Funktionsaufruf, daher
übergeben wir stattdessen einen `async`-Block und warten das Ergebnis des
Aufrufs von `page_title` explizit ab, wie in Listing 17-4.

<Listing number="17-4" caption="Einen async-Block mit `trpl::block_on` abwarten" file-name="src/main.rs">

<!-- should_panic,noplayground because mdbook test does not pass args -->

```rust,should_panic,noplayground
{{#rustdoc_include ../listings/ch17-async-await/listing-17-04/src/main.rs:run}}
```

</Listing>

Wenn wir diesen Code ausführen, erhalten wir das Verhalten, das wir ursprünglich
erwartet hatten:

<!-- manual-regeneration
cd listings/ch17-async-await/listing-17-04
cargo build # skip all the build noise
cargo run -- "https://www.rust-lang.org"
# copy the output here
-->

```console
$ cargo run -- "https://www.rust-lang.org"
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.05s
     Running `target/debug/async_await 'https://www.rust-lang.org'`
The title for https://www.rust-lang.org was
            Rust Programming Language
```

Puh – endlich haben wir funktionierenden asynchronen Code! Bevor wir aber den
Code hinzufügen, der zwei Websites gegeneinander antreten lässt, wenden wir uns
kurz wieder der Funktionsweise von Futures zu.

Jeder _Await-Punkt_ (_await point_) – also jede Stelle, an der der Code das
Schlüsselwort `await` verwendet – ist eine Stelle, an der die Kontrolle an die
Runtime zurückgegeben wird. Damit das funktioniert, muss Rust den Zustand
festhalten, der zum async-Block gehört, damit die Runtime andere Arbeit anstoßen
und dann zurückkehren kann, wenn sie bereit ist, wieder zu versuchen, den ersten
Block voranzubringen. Das ist ein unsichtbarer Zustandsautomat (_state
machine_), als hättest du ein Enum wie dieses geschrieben, um an jedem
Await-Punkt den aktuellen Zustand zu speichern:

```rust
{{#rustdoc_include ../listings/ch17-async-await/no-listing-state-machine/src/lib.rs:enum}}
```

Den Code für den Übergang zwischen den einzelnen Zuständen von Hand zu
schreiben, wäre aber mühsam und fehleranfällig, besonders wenn du dem Code
später mehr Funktionalität und mehr Zustände hinzufügen musst. Zum Glück erzeugt
und verwaltet der Rust-Compiler die Datenstrukturen des Zustandsautomaten für
asynchronen Code automatisch. Die normalen Borrowing- und Ownership-Regeln für
Datenstrukturen gelten weiterhin, und erfreulicherweise übernimmt der Compiler
auch deren Prüfung für uns und liefert nützliche Fehlermeldungen. Einige davon
sehen wir uns später in diesem Kapitel an.

Letztlich muss irgendetwas diesen Zustandsautomaten ausführen, und dieses Etwas
ist eine Runtime. (Deshalb stößt du bei der Beschäftigung mit Runtimes
vielleicht auf Erwähnungen von _Executors_: Ein Executor ist der Teil einer
Runtime, der für die Ausführung des asynchronen Codes verantwortlich ist.)

Jetzt siehst du, warum uns der Compiler in Listing 17-3 daran gehindert hat,
`main` selbst zu einer async-Funktion zu machen. Wäre `main` eine
async-Funktion, müsste etwas anderes den Zustandsautomaten für das Future
verwalten, das `main` zurückgibt, aber `main` ist der Startpunkt des Programms!
Stattdessen haben wir in `main` die Funktion `trpl::block_on` aufgerufen, um
eine Runtime einzurichten und das vom `async`-Block zurückgegebene Future
auszuführen, bis es fertig ist.

> Note: Manche Runtimes stellen Makros bereit, mit denen du eine async-Funktion
> `main` schreiben _kannst_. Diese Makros schreiben `async fn main() { ... }` zu
> einer normalen `fn
> main` um, die dasselbe tut, was wir in Listing 17-4 von
> Hand getan haben: eine Funktion aufrufen, die ein Future vollständig ausführt,
> so wie es `trpl::block_on` tut.

Setzen wir diese Teile jetzt zusammen und sehen, wie wir nebenläufigen Code
schreiben können.

<!-- Old headings. Do not remove or links may break. -->

<a id="racing-our-two-urls-against-each-other"></a>

### Zwei URLs nebenläufig gegeneinander antreten lassen {#racing-two-urls-against-each-other-concurrently}

In Listing 17-5 rufen wir `page_title` mit zwei verschiedenen URLs auf, die auf
der Kommandozeile übergeben werden, und lassen sie gegeneinander antreten, indem
wir das Future auswählen, das zuerst fertig wird.

<Listing number="17-5" caption="`page_title` für zwei URLs aufrufen, um zu sehen, welche zuerst zurückkommt" file-name="src/main.rs">

<!-- should_panic,noplayground because mdbook does not pass args -->

```rust,should_panic,noplayground
{{#rustdoc_include ../listings/ch17-async-await/listing-17-05/src/main.rs:all}}
```

</Listing>

Wir beginnen damit, `page_title` für jede der vom Benutzer angegebenen URLs
aufzurufen. Die resultierenden Futures speichern wir als `title_fut_1` und
`title_fut_2`. Denk daran, dass diese noch nichts tun, weil Futures lazy sind
und wir sie noch nicht abgewartet haben. Dann übergeben wir die Futures an
`trpl::select`, das einen Wert zurückgibt, der anzeigt, welches der übergebenen
Futures zuerst fertig wird.

> Note: Unter der Haube baut `trpl::select` auf einer allgemeineren Funktion
> `select` auf, die im Crate `futures` definiert ist. Die Funktion `select` des
> Crates `futures` kann vieles, was die Funktion `trpl::select` nicht kann, hat
> aber auch zusätzliche Komplexität, die wir vorerst überspringen können.

Jedes der beiden Futures kann rechtmäßig „gewinnen“, daher ergibt es keinen
Sinn, ein `Result` zurückzugeben. Stattdessen gibt `trpl::select` einen Typ
zurück, den wir noch nicht gesehen haben: `trpl::Either`. Der Typ `Either`
ähnelt einem `Result` insofern, als er zwei Fälle hat. Anders als bei `Result`
gibt es in `Either` aber keinen eingebauten Begriff von Erfolg oder Fehlschlag.
Stattdessen verwendet es `Left` und `Right`, um „das eine oder das andere“
anzuzeigen:

```rust
enum Either<A, B> {
    Left(A),
    Right(B),
}
```

Die Funktion `select` gibt `Left` mit der Ausgabe dieses Futures zurück, wenn
das erste Argument gewinnt, und `Right` mit der Ausgabe des zweiten
Future-Arguments, wenn _dieses_ gewinnt. Das entspricht der Reihenfolge, in der
die Argumente beim Aufruf der Funktion stehen: Das erste Argument steht links
vom zweiten Argument.

Außerdem passen wir `page_title` so an, dass es dieselbe übergebene URL
zurückgibt. Hat die Seite, die zuerst zurückkommt, keinen `<title>`, den wir
auflösen können, können wir so trotzdem eine aussagekräftige Meldung ausgeben.
Mit diesen Informationen schließen wir ab, indem wir unsere `println!`-Ausgabe
so anpassen, dass sie sowohl anzeigt, welche URL zuerst fertig war, als auch,
welchen `<title>` die Webseite unter dieser URL hat, falls sie einen hat.

Du hast jetzt einen kleinen funktionierenden Web-Scraper gebaut! Wähle ein paar
URLs aus und führe das Kommandozeilenwerkzeug aus. Vielleicht stellst du fest,
dass manche Websites durchweg schneller sind als andere, während in anderen
Fällen die schnellere Website von Lauf zu Lauf wechselt. Wichtiger ist, dass du
die Grundlagen der Arbeit mit Futures gelernt hast, sodass wir jetzt genauer
erkunden können, was wir mit Async tun können.

{{#quiz ../quizzes/async-01-futures-and-syntax.toml}}

[impl-trait]: ch10-02-traits.html#traits-as-parameters
[iterators-lazy]: ch13-02-iterators.html
[thread-spawn]: ch16-01-threads.html#creating-a-new-thread-with-spawn
[cli-args]: ch12-01-accepting-command-line-arguments.html

<!-- TODO: map source link version to version of Rust? -->

[crate-source]: https://github.com/rust-lang/book/tree/main/packages/trpl
[futures-crate]: https://crates.io/crates/futures
[tokio]: https://tokio.rs
