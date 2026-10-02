<!-- Old headings. Do not remove or links may break. -->

<a id="streams"></a>

## Streams: Futures in Folge {#streams-futures-in-sequence}

Erinnere dich daran, wie wir früher in diesem Kapitel im Abschnitt
[„Nachrichtenübermittlung“][17-02-messages]<!-- ignore --> den Empfänger unseres
asynchronen Kanals verwendet haben. Die asynchrone Methode `recv` erzeugt im
Lauf der Zeit eine Folge von Elementen. Das ist ein Beispiel für ein viel
allgemeineres Schema, das als _Stream_ bezeichnet wird. Viele Konzepte lassen
sich auf natürliche Weise als Streams darstellen: Elemente, die in einer
Warteschlange verfügbar werden, Datenblöcke, die schrittweise aus dem
Dateisystem geladen werden, wenn der gesamte Datensatz zu groß für den Speicher
des Computers ist, oder Daten, die im Lauf der Zeit über das Netzwerk
eintreffen. Weil Streams Futures sind, können wir sie mit jeder anderen Art von
Future verwenden und auf interessante Weise kombinieren. Zum Beispiel können wir
Ereignisse bündeln, um nicht zu viele Netzwerkaufrufe auszulösen, Timeouts für
Folgen langwieriger Operationen festlegen oder Ereignisse der Benutzeroberfläche
drosseln, um unnötige Arbeit zu vermeiden.

Eine Folge von Elementen haben wir schon in Kapitel 13 gesehen, als wir uns im
Abschnitt [„Der Trait Iterator und die Methode `next`“][iterator-trait]<!--
ignore --> den Iterator-Trait angesehen haben, aber zwischen Iteratoren und dem
Empfänger des asynchronen Kanals gibt es zwei Unterschiede. Der erste
Unterschied ist die Zeit: Iteratoren sind synchron, während der Empfänger des
Kanals asynchron ist. Der zweite Unterschied ist die API. Wenn wir direkt mit
`Iterator` arbeiten, rufen wir seine synchrone Methode `next` auf. Speziell beim
Stream `trpl::Receiver` haben wir stattdessen eine asynchrone Methode `recv`
aufgerufen. Ansonsten fühlen sich diese APIs sehr ähnlich an, und diese
Ähnlichkeit ist kein Zufall. Ein Stream ist so etwas wie eine asynchrone Form
der Iteration. Während `trpl::Receiver` aber speziell auf den Empfang von
Nachrichten wartet, ist die allgemeine Stream-API viel breiter angelegt: Sie
liefert das nächste Element so, wie `Iterator` es tut, aber asynchron.

Die Ähnlichkeit zwischen Iteratoren und Streams in Rust bedeutet, dass wir aus
jedem Iterator tatsächlich einen Stream erzeugen können. Wie bei einem Iterator
können wir mit einem Stream arbeiten, indem wir seine Methode `next` aufrufen
und dann auf die Ausgabe warten, wie in Listing 17-21, das noch nicht
kompiliert.

<Listing number="17-21" caption="Einen Stream aus einem Iterator erzeugen und seine Werte ausgeben" file-name="src/main.rs">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch17-async-await/listing-17-21/src/main.rs:stream}}
```

</Listing>

Wir beginnen mit einem Array von Zahlen, das wir in einen Iterator umwandeln,
auf dem wir dann `map` aufrufen, um alle Werte zu verdoppeln. Dann wandeln wir
den Iterator mit der Funktion `trpl::stream_from_iter` in einen Stream um.
Anschließend durchlaufen wir die Elemente des Streams mit der
`while let`-Schleife, sobald sie eintreffen.

Leider kompiliert der Code nicht, wenn wir versuchen, ihn auszuführen, sondern
meldet, dass keine Methode `next` verfügbar ist:

<!-- manual-regeneration
cd listings/ch17-async-await/listing-17-21
cargo build
copy only the error output
-->

```text
error[E0599]: no method named `next` found for struct `tokio_stream::iter::Iter` in the current scope
  --> src/main.rs:10:40
   |
10 |         while let Some(value) = stream.next().await {
   |                                        ^^^^
   |
   = help: items from traits can only be used if the trait is in scope
help: the following traits which provide `next` are implemented but not in scope; perhaps you want to import one of them
   |
1  + use crate::trpl::StreamExt;
   |
1  + use futures_util::stream::stream::StreamExt;
   |
1  + use std::iter::Iterator;
   |
1  + use std::str::pattern::Searcher;
   |
help: there is a method `try_next` with a similar name
   |
10 |         while let Some(value) = stream.try_next().await {
   |                                        ~~~~~~~~
```

Wie diese Ausgabe erklärt, liegt der Grund für den Compilerfehler darin, dass
wir den richtigen Trait im Gültigkeitsbereich (_scope_) brauchen, um die Methode
`next` verwenden zu können. Nach unserer bisherigen Diskussion würdest du
vernünftigerweise erwarten, dass dieser Trait `Stream` ist, tatsächlich ist es
aber `StreamExt`. `Ext` ist die Abkürzung für _extension_ (Erweiterung) und ein
gängiges Schema in der Rust-Community, um einen Trait durch einen anderen zu
erweitern.

Der Trait `Stream` definiert eine Low-Level-Schnittstelle, die die Traits
`Iterator` und `Future` im Grunde kombiniert. `StreamExt` stellt auf Basis von
`Stream` eine höhere Ebene von APIs bereit, darunter die Methode `next` sowie
weitere Hilfsmethoden, die denen des Traits `Iterator` ähneln. `Stream` und
`StreamExt` sind noch nicht Teil der Standardbibliothek von Rust, aber die
meisten Crates im Ökosystem verwenden ähnliche Definitionen.

Um den Compilerfehler zu beheben, fügen wir eine `use`-Anweisung für
`trpl::StreamExt` hinzu, wie in Listing 17-22.

<Listing number="17-22" caption="Einen Iterator erfolgreich als Grundlage für einen Stream verwenden" file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-22/src/main.rs:all}}
```

</Listing>

Wenn all diese Teile zusammengefügt sind, funktioniert dieser Code so, wie wir
es wollen! Und mehr noch: Jetzt, da `StreamExt` im Gültigkeitsbereich ist,
können wir all seine Hilfsmethoden verwenden, genau wie bei Iteratoren.

{{#quiz ../quizzes/async-04-streams.toml}}

[17-02-messages]: ch17-02-concurrency-with-async.html#message-passing
[iterator-trait]: ch13-02-iterators.html#the-iterator-trait-and-the-next-method
