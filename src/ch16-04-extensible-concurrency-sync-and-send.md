<!-- Old headings. Do not remove or links may break. -->

<a id="extensible-concurrency-with-the-sync-and-send-traits"></a>
<a id="extensible-concurrency-with-the-send-and-sync-traits"></a>

## Erweiterbare Nebenläufigkeit mit `Send` und `Sync` {#extensible-concurrency-with-send-and-sync}

Interessanterweise war fast jedes Nebenläufigkeits-Feature, über das wir bisher
in diesem Kapitel gesprochen haben, Teil der Standardbibliothek und nicht der
Sprache. Deine Möglichkeiten, mit Nebenläufigkeit umzugehen, sind nicht auf die
Sprache oder die Standardbibliothek beschränkt; du kannst eigene
Nebenläufigkeits-Features schreiben oder solche verwenden, die andere
geschrieben haben.

Zu den zentralen Nebenläufigkeitskonzepten, die in die Sprache statt in die
Standardbibliothek eingebettet sind, gehören jedoch die `std::marker`-Traits
`Send` und `Sync`.

<!-- Old headings. Do not remove or links may break. -->

<a id="allowing-transference-of-ownership-between-threads-with-send"></a>

### Ownership zwischen Threads übertragen {#transferring-ownership-between-threads}

Der Marker-Trait `Send` zeigt an, dass die Ownership von Werten des Typs, der
`Send` implementiert, zwischen Threads übertragen werden kann. Fast jeder
Rust-Typ implementiert `Send`, aber es gibt einige Ausnahmen, darunter `Rc<T>`:
Dieser Typ kann `Send` nicht implementieren, denn wenn du einen `Rc<T>`-Wert
klonst und versuchst, die Ownership des Klons an einen anderen Thread zu
übertragen, könnten beide Threads gleichzeitig den Referenzzähler aktualisieren.
Aus diesem Grund ist `Rc<T>` für den Einsatz in Situationen mit einem einzigen
Thread implementiert, in denen du die Performance-Einbuße der Threadsicherheit
nicht zahlen willst.

Daher stellen das Typsystem und die Trait-Bounds von Rust sicher, dass du nie
versehentlich einen `Rc<T>`-Wert auf unsichere Weise über Threads hinweg senden
kannst. Als wir das in Listing 16-14 versucht haben, haben wir den Fehler
`` the trait `Send` is not implemented
for `Rc<Mutex<i32>>` `` bekommen. Als wir
zu `Arc<T>` gewechselt sind, das `Send` implementiert, hat der Code kompiliert.

Jeder Typ, der vollständig aus `Send`-Typen besteht, wird automatisch ebenfalls
als `Send` gekennzeichnet. Fast alle primitiven Typen sind `Send`, abgesehen von
Rohzeigern (_raw pointers_), die wir in Kapitel 20 besprechen.

<!-- Old headings. Do not remove or links may break. -->

<a id="allowing-access-from-multiple-threads-with-sync"></a>

### Zugriff aus mehreren Threads {#accessing-from-multiple-threads}

Der Marker-Trait `Sync` zeigt an, dass es sicher ist, aus mehreren Threads auf
den Typ zu verweisen, der `Sync` implementiert. Mit anderen Worten: Jeder Typ
`T` implementiert `Sync`, wenn `&T` (eine unveränderliche (_immutable_) Referenz
auf `T`) `Send` implementiert, die Referenz also sicher an einen anderen Thread
gesendet werden kann. Ähnlich wie bei `Send` implementieren alle primitiven
Typen `Sync`, und Typen, die vollständig aus Typen bestehen, die `Sync`
implementieren, implementieren ebenfalls `Sync`.

<!-- BEGIN INTERVENTION: 43081862-aac8-4e18-9c55-1107ea4c7cc1 -->

`Sync` ist das Konzept in Rust, das der umgangssprachlichen Bedeutung von
„threadsicher“ am nächsten kommt, also dass bestimmte Daten von mehreren
nebenläufigen Threads sicher verwendet werden können. Getrennte Traits `Send`
und `Sync` gibt es, weil ein Typ manchmal das eine, beides oder keines von
beiden sein kann. Zum Beispiel:

- Der Smart-Pointer `Rc<T>` ist aus den oben beschriebenen Gründen weder `Send`
  noch `Sync`.
- Der Typ `RefCell<T>` (über den wir in Kapitel 15 gesprochen haben) und die
  Familie der verwandten `Cell<T>`-Typen sind `Send` (wenn `T: Send`), aber
  nicht `Sync`. Eine `RefCell` kann über eine Thread-Grenze gesendet werden,
  aber nicht nebenläufig verwendet werden, weil die Implementierung der
  Borrow-Prüfung, die `RefCell<T>` zur Laufzeit durchführt, nicht threadsicher
  ist.
- Der Smart-Pointer `Mutex<T>` ist `Send` und `Sync` und kann verwendet werden,
  um mehreren Threads gemeinsamen Zugriff zu geben, wie du im Abschnitt
  [„Gemeinsamer Zugriff auf `Mutex<T>`“][sharing-a-mutext-between-multiple-threads]<!-- ignore -->
  gesehen hast.
- Der Typ `MutexGuard<'a, T>`, den `Mutex::lock` zurückgibt, ist `Sync` (wenn
  `T: Sync`), aber nicht `Send`. Er ist gezielt nicht `Send`, weil
  [manche Plattformen vorschreiben, dass Mutexe von demselben Thread entsperrt werden, der sie gesperrt hat][mutex-guards-are-not-send].

<!-- END INTERVENTION: 43081862-aac8-4e18-9c55-1107ea4c7cc1 -->

### `Send` und `Sync` manuell zu implementieren, ist unsicher {#implementing-send-and-sync-manually-is-unsafe}

Da Typen, die vollständig aus anderen Typen bestehen, die die Traits `Send` und
`Sync` implementieren, automatisch ebenfalls `Send` und `Sync` implementieren,
müssen wir diese Traits nicht manuell implementieren. Als Marker-Traits haben
sie nicht einmal Methoden, die man implementieren müsste. Sie sind nur nützlich,
um Invarianten im Zusammenhang mit Nebenläufigkeit durchzusetzen.

Diese Traits manuell zu implementieren, bedeutet, unsicheren Rust-Code zu
schreiben. Über die Verwendung von unsicherem Rust-Code sprechen wir in Kapitel
20; vorerst ist die wichtige Information, dass das Erstellen neuer nebenläufiger
Typen, die nicht aus `Send`- und `Sync`-Teilen bestehen, sorgfältiges Nachdenken
erfordert, um die Sicherheitsgarantien einzuhalten.
[„The Rustonomicon“][nomicon] enthält mehr Informationen über diese Garantien
und darüber, wie man sie einhält.

## Zusammenfassung {#summary}

Das ist nicht das letzte Mal, dass dir in diesem Buch Nebenläufigkeit begegnet:
Das nächste Kapitel konzentriert sich auf asynchrone Programmierung, und das
Projekt in Kapitel 21 verwendet die Konzepte aus diesem Kapitel in einer
realistischeren Situation als die kleineren Beispiele hier.

Wie bereits erwähnt, ist nur sehr wenig davon, wie Rust mit Nebenläufigkeit
umgeht, Teil der Sprache, daher sind viele Lösungen für Nebenläufigkeit als
Crates implementiert. Diese entwickeln sich schneller als die
Standardbibliothek, also such unbedingt online nach aktuellen, modernen Crates
für Situationen mit mehreren Threads.

Die Standardbibliothek von Rust stellt Kanäle für die Nachrichtenübermittlung
und Smart-Pointer-Typen wie `Mutex<T>` und `Arc<T>` bereit, die sich in
nebenläufigen Kontexten sicher verwenden lassen. Das Typsystem und der
Borrow-Checker stellen sicher, dass Code, der diese Lösungen verwendet, nicht in
Data-Races oder ungültigen Referenzen endet. Sobald dein Code kompiliert, kannst
du dich darauf verlassen, dass er problemlos in mehreren Threads läuft, ohne die
schwer aufzuspürenden Bugs, die in anderen Sprachen häufig sind. Nebenläufige
Programmierung ist kein Konzept mehr, vor dem man sich fürchten muss: Zieh los
und mach deine Programme nebenläufig, furchtlos!

{{#quiz ../quizzes/ch16-04-extensible-concurrency-send-and-sync.toml}}

[sharing-a-mutext-between-multiple-threads]: ch16-03-shared-state.html#sharing-a-mutext-between-multiple-threads
[nomicon]: https://doc.rust-lang.org/nomicon/index.html
[mutex-guards-are-not-send]: https://github.com/rust-lang/rust/issues/23465#issuecomment-82730326
