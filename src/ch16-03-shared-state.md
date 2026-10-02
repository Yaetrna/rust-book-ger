## Nebenläufigkeit mit geteiltem Zustand {#shared-state-concurrency}

Nachrichtenübermittlung ist eine gute Art, mit Nebenläufigkeit umzugehen, aber
nicht die einzige. Eine andere Methode wäre, dass mehrere Threads auf dieselben
geteilten Daten zugreifen. Betrachte noch einmal diesen Teil des Slogans aus der
Dokumentation der Sprache Go: „Kommuniziere nicht, indem du Speicher teilst.“

Wie sähe es aus, durch das Teilen von Speicher zu kommunizieren? Und warum
würden Anhänger der Nachrichtenübermittlung davor warnen, Speicher zu teilen?

In gewisser Weise ähneln Kanäle in jeder Programmiersprache einer einzigen
Ownership, denn sobald du einen Wert durch einen Kanal geschickt hast, solltest
du diesen Wert nicht mehr verwenden. Nebenläufigkeit mit geteiltem Speicher ist
wie mehrfache Ownership: Mehrere Threads können gleichzeitig auf dieselbe
Speicherstelle zugreifen. Wie du in Kapitel 15 gesehen hast, wo Smart-Pointer
mehrfache Ownership möglich gemacht haben, kann mehrfache Ownership die
Komplexität erhöhen, weil diese verschiedenen Owner verwaltet werden müssen. Das
Typsystem und die Ownership-Regeln von Rust helfen sehr dabei, diese Verwaltung
korrekt umzusetzen. Sehen wir uns als Beispiel Mutexe an, eines der gängigeren
Nebenläufigkeitsprimitive für geteilten Speicher.

<!-- Old headings. Do not remove or links may break. -->

<a id="using-mutexes-to-allow-access-to-data-from-one-thread-at-a-time"></a>

### Zugriff mit Mutexen steuern {#controlling-access-with-mutexes}

_Mutex_ ist eine Abkürzung für _mutual exclusion_ (gegenseitiger Ausschluss),
denn ein Mutex erlaubt zu jedem Zeitpunkt nur einem Thread den Zugriff auf
bestimmte Daten. Um auf die Daten in einem Mutex zuzugreifen, muss ein Thread
zuerst signalisieren, dass er Zugriff haben will, indem er darum bittet, den
Lock des Mutex zu erhalten. Der _Lock_ ist eine Datenstruktur, die Teil des
Mutex ist und festhält, wer gerade exklusiven Zugriff auf die Daten hat. Daher
sagt man, dass der Mutex die Daten, die er enthält, über das Locking-System
_bewacht_ (_guarding_).

Mutexe haben den Ruf, schwer zu verwenden zu sein, weil man sich zwei Regeln
merken muss:

1. Du musst versuchen, den Lock zu erhalten, bevor du die Daten verwendest.
2. Wenn du mit den Daten fertig bist, die der Mutex bewacht, musst du die Daten
   entsperren, damit andere Threads den Lock erhalten können.

Als Metapher aus dem echten Leben für einen Mutex stell dir eine
Podiumsdiskussion auf einer Konferenz mit nur einem Mikrofon vor. Bevor jemand
auf dem Podium sprechen kann, muss er darum bitten oder signalisieren, dass er
das Mikrofon benutzen will. Wer das Mikrofon bekommt, kann so lange sprechen,
wie er will, und gibt das Mikrofon dann an die nächste Person auf dem Podium
weiter, die sprechen möchte. Vergisst jemand, das Mikrofon weiterzugeben, wenn
er fertig ist, kann niemand sonst sprechen. Geht die Verwaltung des gemeinsamen
Mikrofons schief, funktioniert das Podium nicht wie geplant!

Die Verwaltung von Mutexen korrekt hinzubekommen, kann unglaublich knifflig
sein, weshalb so viele Leute von Kanälen begeistert sind. Dank des Typsystems
und der Ownership-Regeln von Rust kannst du beim Sperren und Entsperren aber
keine Fehler machen.

#### Die API von `Mutex<T>` {#the-api-of-mutext}

Als Beispiel dafür, wie man einen Mutex verwendet, beginnen wir damit, einen
Mutex in einem Kontext mit einem einzigen Thread zu verwenden, wie in Listing
16-12 gezeigt.

<Listing number="16-12" file-name="src/main.rs" caption="Die API von `Mutex<T>` der Einfachheit halber in einem Kontext mit einem einzigen Thread erkunden">

```rust
{{#rustdoc_include ../listings/ch16-fearless-concurrency/listing-16-12/src/main.rs}}
```

</Listing>

Wie bei vielen Typen erzeugen wir einen `Mutex<T>` mit der assoziierten Funktion
`new`. Um auf die Daten im Mutex zuzugreifen, verwenden wir die Methode `lock`,
um den Lock zu erhalten. Dieser Aufruf blockiert den aktuellen Thread, sodass er
keine Arbeit verrichten kann, bis wir an der Reihe sind, den Lock zu erhalten.

Der Aufruf von `lock` würde fehlschlagen, wenn ein anderer Thread, der den Lock
hält, einen Panic ausgelöst hätte. In diesem Fall könnte niemand jemals den Lock
erhalten, daher haben wir uns entschieden, `unwrap` zu verwenden und diesen
Thread in dieser Situation einen Panic auslösen zu lassen.

Nachdem wir den Lock erhalten haben, können wir den Rückgabewert, hier `num`
genannt, als veränderliche (_mutable_) Referenz auf die Daten darin behandeln.
Das Typsystem stellt sicher, dass wir einen Lock erhalten, bevor wir den Wert in
`m` verwenden. Der Typ von `m` ist `Mutex<i32>`, nicht `i32`, daher _müssen_ wir
`lock` aufrufen, um den `i32`-Wert verwenden zu können. Wir können das nicht
vergessen; das Typsystem lässt uns sonst nicht auf den inneren `i32` zugreifen.

Der Aufruf von `lock` gibt einen Typ namens `MutexGuard` zurück, verpackt in ein
`LockResult`, das wir mit dem Aufruf von `unwrap` behandelt haben. Der Typ
`MutexGuard` implementiert `Deref`, um auf unsere inneren Daten zu zeigen;
außerdem hat der Typ eine `Drop`-Implementierung, die den Lock automatisch
freigibt, wenn ein `MutexGuard` den Gültigkeitsbereich (_scope_) verlässt, was
am Ende des inneren Gültigkeitsbereichs geschieht. Dadurch laufen wir nicht
Gefahr, zu vergessen, den Lock freizugeben, und den Mutex für andere Threads zu
blockieren, denn die Freigabe des Locks geschieht automatisch.

Nachdem der Lock verworfen (_dropped_) wurde, können wir den Wert des Mutex
ausgeben und sehen, dass wir den inneren `i32` auf `6` ändern konnten.

<!-- Old headings. Do not remove or links may break. -->

<a id="sharing-a-mutext-between-multiple-threads"></a>

#### Gemeinsamer Zugriff auf `Mutex<T>` {#shared-access-to-mutext}

Versuchen wir jetzt, mit `Mutex<T>` einen Wert zwischen mehreren Threads zu
teilen. Wir starten 10 Threads und lassen jeden einen Zählerwert um 1 erhöhen,
sodass der Zähler von 0 auf 10 steigt. Das Beispiel in Listing 16-13 führt zu
einem Compilerfehler, und wir nutzen diesen Fehler, um mehr über die Verwendung
von `Mutex<T>` zu lernen und darüber, wie Rust uns hilft, ihn korrekt zu
verwenden.

<Listing number="16-13" file-name="src/main.rs" caption="Zehn Threads, die jeweils einen von einem `Mutex<T>` bewachten Zähler erhöhen">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch16-fearless-concurrency/listing-16-13/src/main.rs}}
```

</Listing>

Wir erzeugen eine Variable `counter`, die einen `i32` in einem `Mutex<T>`
enthält, wie in Listing 16-12. Als Nächstes erzeugen wir 10 Threads, indem wir
über einen Zahlenbereich iterieren. Wir verwenden `thread::spawn` und geben
allen Threads dieselbe Closure: eine, die den Zähler in den Thread verschiebt
(_moves_), durch Aufruf der Methode `lock` einen Lock auf dem `Mutex<T>` erhält
und dann 1 zum Wert im Mutex addiert. Wenn ein Thread seine Closure fertig
ausgeführt hat, verlässt `num` den Gültigkeitsbereich und gibt den Lock frei,
sodass ein anderer Thread ihn erhalten kann.

Im Haupt-Thread sammeln wir alle Join-Handles. Dann rufen wir, wie in Listing
16-2, auf jedem Handle `join` auf, um sicherzustellen, dass alle Threads fertig
werden. An dieser Stelle erhält der Haupt-Thread den Lock und gibt das Ergebnis
dieses Programms aus.

Wir haben angedeutet, dass dieses Beispiel nicht kompiliert. Finden wir jetzt
heraus, warum!

```console
{{#include ../listings/ch16-fearless-concurrency/listing-16-13/output.txt}}
```

Die Fehlermeldung besagt, dass der Wert `counter` in der vorherigen Iteration
der Schleife verschoben wurde. Rust sagt uns, dass wir die Ownership des Locks
`counter` nicht in mehrere Threads verschieben können. Beheben wir den
Compilerfehler mit der Methode der mehrfachen Ownership, die wir in Kapitel 15
besprochen haben.

#### Mehrfache Ownership mit mehreren Threads {#multiple-ownership-with-multiple-threads}

In Kapitel 15 haben wir einem Wert mehrere Owner gegeben, indem wir mit dem
Smart-Pointer `Rc<T>` einen Wert mit Referenzzählung erzeugt haben. Machen wir
hier dasselbe und sehen, was passiert. In Listing 16-14 verpacken wir den
`Mutex<T>` in `Rc<T>` und klonen das `Rc<T>`, bevor wir die Ownership in den
Thread verschieben.

<Listing number="16-14" file-name="src/main.rs" caption="Versuch, mit `Rc<T>` mehreren Threads zu erlauben, den `Mutex<T>` zu besitzen">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch16-fearless-concurrency/listing-16-14/src/main.rs}}
```

</Listing>

Wieder kompilieren wir und bekommen … andere Fehler! Der Compiler bringt uns
eine Menge bei:

```console
{{#include ../listings/ch16-fearless-concurrency/listing-16-14/output.txt}}
```

Wow, diese Fehlermeldung ist sehr wortreich! Das ist der wichtige Teil, auf den
du achten solltest:
`` `Rc<Mutex<i32>>` cannot be sent between threads safely ``. Der Compiler sagt
uns auch den Grund:
`` the trait `Send` is not implemented for
`Rc<Mutex<i32>>` ``. Über `Send`
sprechen wir im nächsten Abschnitt: Es ist einer der Traits, die sicherstellen,
dass die Typen, die wir mit Threads verwenden, für den Einsatz in nebenläufigen
Situationen gedacht sind.

Leider ist `Rc<T>` nicht sicher über Threads hinweg teilbar. Wenn `Rc<T>` den
Referenzzähler verwaltet, erhöht es den Zähler bei jedem Aufruf von `clone` und
verringert ihn, wenn ein Klon verworfen wird. Es verwendet aber keine
Nebenläufigkeitsprimitive, um sicherzustellen, dass Änderungen am Zähler nicht
von einem anderen Thread unterbrochen werden können. Das könnte zu falschen
Zählerständen führen – subtilen Bugs, die wiederum zu Speicherlecks führen
könnten oder dazu, dass ein Wert verworfen wird, bevor wir mit ihm fertig sind.
Was wir brauchen, ist ein Typ, der genau wie `Rc<T>` ist, Änderungen am
Referenzzähler aber threadsicher vornimmt.

#### Atomare Referenzzählung mit `Arc<T>` {#atomic-reference-counting-with-arct}

Zum Glück _ist_ `Arc<T>` ein Typ wie `Rc<T>`, der sich in nebenläufigen
Situationen sicher verwenden lässt. Das _a_ steht für _atomic_ (atomar), es
handelt sich also um einen Typ mit _atomarer Referenzzählung_ (_atomically
reference-counted_). Atomics sind eine weitere Art von Nebenläufigkeitsprimitiv,
die wir hier nicht im Detail behandeln: Weitere Details findest du in der
Dokumentation der Standardbibliothek zu
[`std::sync::atomic`][atomic]<!-- ignore -->. Vorerst musst du nur wissen, dass
Atomics wie primitive Typen funktionieren, sich aber sicher über Threads hinweg
teilen lassen.

Vielleicht fragst du dich dann, warum nicht alle primitiven Typen atomar sind
und warum die Typen der Standardbibliothek nicht standardmäßig `Arc<T>`
verwenden. Der Grund ist, dass Threadsicherheit eine Performance-Einbuße mit
sich bringt, die du nur zahlen willst, wenn du sie wirklich brauchst. Führst du
nur Operationen auf Werten innerhalb eines einzigen Threads aus, kann dein Code
schneller laufen, wenn er die Garantien von Atomics nicht durchsetzen muss.

Kehren wir zu unserem Beispiel zurück: `Arc<T>` und `Rc<T>` haben dieselbe API,
daher korrigieren wir unser Programm, indem wir die `use`-Zeile, den Aufruf von
`new` und den Aufruf von `clone` ändern. Der Code in Listing 16-15 kompiliert
und läuft endlich.

<Listing number="16-15" file-name="src/main.rs" caption="Den `Mutex<T>` mit einem `Arc<T>` umhüllen, um die Ownership über mehrere Threads hinweg teilen zu können">

```rust
{{#rustdoc_include ../listings/ch16-fearless-concurrency/listing-16-15/src/main.rs}}
```

</Listing>

Dieser Code gibt Folgendes aus:

<!-- Not extracting output because changes to this output aren't significant;
the changes are likely to be due to the threads running differently rather than
changes in the compiler -->

```text
Result: 10
```

Geschafft! Wir haben von 0 bis 10 gezählt, was vielleicht nicht sehr
beeindruckend wirkt, aber uns viel über `Mutex<T>` und Threadsicherheit
beigebracht hat. Du könntest die Struktur dieses Programms auch für
kompliziertere Operationen verwenden als nur das Erhöhen eines Zählers. Mit
dieser Strategie kannst du eine Berechnung in unabhängige Teile zerlegen, diese
Teile auf Threads verteilen und dann mit einem `Mutex<T>` jeden Thread das
Endergebnis mit seinem Teil aktualisieren lassen.

Beachte: Wenn du einfache numerische Operationen durchführst, gibt es einfachere
Typen als `Mutex<T>`, die das
[Modul `std::sync::atomic` der Standardbibliothek][atomic]<!-- ignore -->
bereitstellt. Diese Typen bieten sicheren, nebenläufigen, atomaren Zugriff auf
primitive Typen. Wir haben für dieses Beispiel `Mutex<T>` mit einem primitiven
Typ verwendet, damit wir uns darauf konzentrieren konnten, wie `Mutex<T>`
funktioniert.

<!-- Old headings. Do not remove or links may break. -->

<a id="similarities-between-refcelltrct-and-mutextarct"></a>

### `RefCell<T>`/`Rc<T>` und `Mutex<T>`/`Arc<T>` im Vergleich {#comparing-refcelltrct-and-mutextarct}

Vielleicht ist dir aufgefallen, dass `counter` unveränderlich (_immutable_) ist,
wir aber eine veränderliche Referenz auf den Wert darin erhalten konnten; das
bedeutet, dass `Mutex<T>` innere Veränderlichkeit bietet, wie es die
`Cell`-Familie tut. So wie wir in Kapitel 15 mit `RefCell<T>` den Inhalt eines
`Rc<T>` verändern konnten, verändern wir mit `Mutex<T>` den Inhalt eines
`Arc<T>`.

Ein weiteres Detail ist zu beachten: Rust kann dich bei der Verwendung von
`Mutex<T>` nicht vor allen Arten von Logikfehlern schützen. Erinnere dich aus
Kapitel 15, dass die Verwendung von `Rc<T>` die Gefahr von Referenzzyklen mit
sich brachte, bei denen zwei `Rc<T>`-Werte aufeinander verweisen und
Speicherlecks verursachen. Ähnlich birgt `Mutex<T>` die Gefahr von _Deadlocks_.
Sie treten auf, wenn eine Operation zwei Ressourcen sperren muss und zwei
Threads jeweils einen der Locks erhalten haben, sodass sie ewig aufeinander
warten. Wenn dich Deadlocks interessieren, versuch, ein Rust-Programm mit einem
Deadlock zu schreiben; recherchiere dann Strategien zur Vermeidung von Deadlocks
bei Mutexen in beliebigen Sprachen und versuch, sie in Rust umzusetzen. Die
API-Dokumentation der Standardbibliothek zu `Mutex<T>` und `MutexGuard` bietet
nützliche Informationen.

Wir runden dieses Kapitel ab, indem wir über die Traits `Send` und `Sync`
sprechen und darüber, wie wir sie mit eigenen Typen verwenden können.

{{#quiz ../quizzes/ch16-03-shared-state.toml}}

[atomic]: https://doc.rust-lang.org/std/sync/atomic/index.html
