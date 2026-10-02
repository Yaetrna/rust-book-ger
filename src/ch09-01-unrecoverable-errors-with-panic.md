## Nicht behebbare Fehler mit `panic!` {#unrecoverable-errors-with-panic}

Manchmal passieren in deinem Code schlimme Dinge, und du kannst nichts dagegen
tun. Für diese Fälle hat Rust das Makro `panic!`. In der Praxis gibt es zwei
Wege, einen Panic auszulösen: indem man etwas tut, das unseren Code einen Panic
auslösen lässt (etwa auf ein Array hinter seinem Ende zuzugreifen), oder indem
man das Makro `panic!` explizit aufruft. In beiden Fällen lösen wir in unserem
Programm einen Panic aus. Standardmäßig geben diese Panics eine Fehlermeldung
aus, wickeln den Stack ab, räumen ihn auf und beenden das Programm. Über eine
Umgebungsvariable kannst du Rust außerdem den Aufrufstack anzeigen lassen, wenn
ein Panic auftritt, damit sich die Ursache des Panics leichter aufspüren lässt.

> ### Als Reaktion auf einen Panic den Stack abwickeln oder abbrechen {#unwinding-the-stack-or-aborting-in-response-to-a-panic}
>
> Standardmäßig beginnt das Programm bei einem Panic mit dem _Abwickeln_
> (_unwinding_). Das bedeutet, dass Rust den Stack zurück nach oben durchläuft
> und die Daten jeder Funktion aufräumt, auf die es dabei trifft. Dieses
> Zurücklaufen und Aufräumen ist allerdings viel Arbeit. Rust erlaubt dir daher,
> stattdessen sofort _abzubrechen_ (_aborting_), wodurch das Programm ohne
> Aufräumen beendet wird.
>
> Den Speicher, den das Programm verwendet hat, muss dann das Betriebssystem
> aufräumen. Wenn die resultierende Binärdatei in deinem Projekt so klein wie
> möglich sein muss, kannst du bei einem Panic vom Abwickeln auf das Abbrechen
> umschalten, indem du `panic = 'abort'` in die passenden `[profile]`-Abschnitte
> deiner Datei _Cargo.toml_ einträgst. Wenn du zum Beispiel im Release-Modus bei
> einem Panic abbrechen willst, füge Folgendes hinzu:
>
> ```toml
> [profile.release]
> panic = 'abort'
> ```

Versuchen wir, `panic!` in einem einfachen Programm aufzurufen:

<Listing file-name="src/main.rs">

```rust,should_panic,panics
{{#rustdoc_include ../listings/ch09-error-handling/no-listing-01-panic/src/main.rs}}
```

</Listing>

Wenn du das Programm ausführst, siehst du etwa Folgendes:

```console
{{#include ../listings/ch09-error-handling/no-listing-01-panic/output.txt}}
```

Der Aufruf von `panic!` verursacht die Fehlermeldung in den letzten beiden
Zeilen. Die erste Zeile zeigt unsere Panic-Meldung und die Stelle in unserem
Quellcode, an der der Panic aufgetreten ist: _src/main.rs:2:5_ gibt an, dass es
die zweite Zeile, fünftes Zeichen, unserer Datei _src/main.rs_ ist.

In diesem Fall gehört die angegebene Zeile zu unserem Code, und wenn wir zu
dieser Zeile gehen, sehen wir den Aufruf des Makros `panic!`. In anderen Fällen
steht der Aufruf von `panic!` vielleicht in Code, den unser Code aufruft, und
der Dateiname und die Zeilennummer in der Fehlermeldung verweisen auf den Code
von jemand anderem, in dem das Makro `panic!` aufgerufen wird, nicht auf die
Zeile unseres Codes, die letztlich zum Aufruf von `panic!` geführt hat.

<!-- Old headings. Do not remove or links may break. -->

<a id="using-a-panic-backtrace"></a>

Wir können den Backtrace der Funktionen verwenden, aus denen der Aufruf von
`panic!` stammt, um herauszufinden, welcher Teil unseres Codes das Problem
verursacht. Um zu verstehen, wie man einen `panic!`-Backtrace verwendet, sehen
wir uns ein weiteres Beispiel an, bei dem ein Aufruf von `panic!` wegen eines
Bugs in unserem Code aus einer Bibliothek kommt, statt dass unser Code das Makro
direkt aufruft. Listing 9-1 enthält Code, der versucht, auf einen Index in einem
Vektor zuzugreifen, der außerhalb des Bereichs gültiger Indizes liegt.

<Listing number="9-1" file-name="src/main.rs" caption="Versuch, auf ein Element hinter dem Ende eines Vektors zuzugreifen, was einen Aufruf von `panic!` verursacht">

```rust,should_panic,panics
{{#rustdoc_include ../listings/ch09-error-handling/listing-09-01/src/main.rs}}
```

</Listing>

Hier versuchen wir, auf das 100. Element unseres Vektors zuzugreifen (das an
Index 99 liegt, weil die Indexierung bei null beginnt), aber der Vektor hat nur
drei Elemente. In dieser Situation löst Rust einen Panic aus. `[]` soll ein
Element zurückgeben, aber wenn du einen ungültigen Index übergibst, gibt es kein
Element, das Rust hier korrekterweise zurückgeben könnte.

In C ist der Versuch, über das Ende einer Datenstruktur hinaus zu lesen,
undefiniertes Verhalten. Du bekommst vielleicht das, was an der Speicherstelle
steht, die diesem Element in der Datenstruktur entsprechen würde, obwohl der
Speicher nicht zu dieser Struktur gehört. Das nennt man _Buffer Overread_ (Lesen
über das Pufferende hinaus), und es kann zu Sicherheitslücken führen, wenn ein
Angreifer den Index so manipulieren kann, dass er Daten liest, die hinter der
Datenstruktur gespeichert sind und die er nicht lesen dürfte.

Um dein Programm vor dieser Art von Sicherheitslücke zu schützen, stoppt Rust
die Ausführung und weigert sich weiterzumachen, wenn du versuchst, ein Element
an einem nicht existierenden Index zu lesen. Probieren wir es aus:

```console
{{#include ../listings/ch09-error-handling/listing-09-01/output.txt}}
```

Dieser Fehler verweist auf Zeile 4 unserer Datei _main.rs_, in der wir
versuchen, auf Index 99 des Vektors in `v` zuzugreifen.

Die Zeile `note:` sagt uns, dass wir die Umgebungsvariable `RUST_BACKTRACE`
setzen können, um einen Backtrace dessen zu erhalten, was genau zu dem Fehler
geführt hat. Ein _Backtrace_ ist eine Liste aller Funktionen, die aufgerufen
wurden, um an diesen Punkt zu gelangen. Backtraces funktionieren in Rust wie in
anderen Sprachen: Der Schlüssel zum Lesen des Backtraces ist, oben anzufangen
und so lange zu lesen, bis du Dateien siehst, die du geschrieben hast. Das ist
die Stelle, an der das Problem seinen Ursprung hat. Die Zeilen oberhalb dieser
Stelle sind Code, den dein Code aufgerufen hat; die Zeilen darunter sind Code,
der deinen Code aufgerufen hat. Diese Zeilen davor und danach können Code aus
dem Kern von Rust, Code der Standardbibliothek oder Crates enthalten, die du
verwendest. Versuchen wir, einen Backtrace zu erhalten, indem wir die
Umgebungsvariable `RUST_BACKTRACE` auf einen beliebigen Wert außer `0` setzen.
Listing 9-2 zeigt eine Ausgabe, die der ähnelt, die du sehen wirst.

<!-- manual-regeneration
cd listings/ch09-error-handling/listing-09-01
RUST_BACKTRACE=1 cargo run
copy the backtrace output below
check the backtrace number mentioned in the text below the listing
-->

<Listing number="9-2" caption="Der Backtrace, der durch einen Aufruf von `panic!` erzeugt und angezeigt wird, wenn die Umgebungsvariable `RUST_BACKTRACE` gesetzt ist">

```console
$ RUST_BACKTRACE=1 cargo run
thread 'main' panicked at src/main.rs:4:6:
index out of bounds: the len is 3 but the index is 99
stack backtrace:
   0: rust_begin_unwind
             at /rustc/4d91de4e48198da2e33413efdcd9cd2cc0c46688/library/std/src/panicking.rs:692:5
   1: core::panicking::panic_fmt
             at /rustc/4d91de4e48198da2e33413efdcd9cd2cc0c46688/library/core/src/panicking.rs:75:14
   2: core::panicking::panic_bounds_check
             at /rustc/4d91de4e48198da2e33413efdcd9cd2cc0c46688/library/core/src/panicking.rs:273:5
   3: <usize as core::slice::index::SliceIndex<[T]>>::index
             at file:///home/.rustup/toolchains/1.85/lib/rustlib/src/rust/library/core/src/slice/index.rs:274:10
   4: core::slice::index::<impl core::ops::index::Index<I> for [T]>::index
             at file:///home/.rustup/toolchains/1.85/lib/rustlib/src/rust/library/core/src/slice/index.rs:16:9
   5: <alloc::vec::Vec<T,A> as core::ops::index::Index<I>>::index
             at file:///home/.rustup/toolchains/1.85/lib/rustlib/src/rust/library/alloc/src/vec/mod.rs:3361:9
   6: panic::main
             at ./src/main.rs:4:6
   7: core::ops::function::FnOnce::call_once
             at file:///home/.rustup/toolchains/1.85/lib/rustlib/src/rust/library/core/src/ops/function.rs:250:5
note: Some details are omitted, run with `RUST_BACKTRACE=full` for a verbose backtrace.
```

</Listing>

Das ist eine Menge Ausgabe! Die genaue Ausgabe kann je nach Betriebssystem und
Rust-Version anders aussehen. Um Backtraces mit diesen Informationen zu
erhalten, müssen Debug-Symbole aktiviert sein. Debug-Symbole sind standardmäßig
aktiviert, wenn du `cargo build` oder `cargo run` ohne das Flag `--release`
verwendest, wie wir es hier tun.

In der Ausgabe in Listing 9-2 verweist Zeile 6 des Backtraces auf die Zeile in
unserem Projekt, die das Problem verursacht: Zeile 4 von _src/main.rs_. Wenn
unser Programm keinen Panic auslösen soll, sollten wir unsere Untersuchung an
der Stelle beginnen, auf die die erste Zeile verweist, in der eine von uns
geschriebene Datei erwähnt wird. In Listing 9-1, wo wir absichtlich Code
geschrieben haben, der einen Panic auslöst, behebt man den Panic, indem man kein
Element außerhalb des Bereichs der Vektorindizes anfordert. Wenn dein Code
künftig einen Panic auslöst, musst du herausfinden, welche Aktion der Code mit
welchen Werten ausführt, die den Panic verursacht, und was der Code stattdessen
tun sollte.

Wir kommen im Abschnitt
[„`panic!` oder nicht `panic!`?“][to-panic-or-not-to-panic]<!-- ignore -->
später in diesem Kapitel auf `panic!` zurück und darauf, wann wir `panic!` zur
Behandlung von Fehlerzuständen verwenden sollten und wann nicht. Als Nächstes
sehen wir uns an, wie man einen Fehler mit `Result` behebt.

{{#quiz ../quizzes/ch09-01-panic.toml}}

[to-panic-or-not-to-panic]: ch09-03-to-panic-or-not-to-panic.html#to-panic-or-not-to-panic
