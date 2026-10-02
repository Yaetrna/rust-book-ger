## `RefCell<T>` und das Pattern der inneren Veränderlichkeit {#refcellt-and-the-interior-mutability-pattern}

_Innere Veränderlichkeit_ (_interior mutability_) ist ein Design-Pattern in
Rust, mit dem du Daten verändern kannst, selbst wenn es unveränderliche
(_immutable_) Referenzen auf diese Daten gibt; normalerweise verbieten die
Borrowing-Regeln das. Um Daten zu verändern, verwendet das Pattern `unsafe`-Code
innerhalb einer Datenstruktur, um die üblichen Regeln von Rust für Veränderung
und Borrowing zu beugen. Unsicherer Code zeigt dem Compiler an, dass wir die
Regeln manuell prüfen, statt uns darauf zu verlassen, dass der Compiler sie für
uns prüft; unsicheren Code besprechen wir ausführlicher in Kapitel 20.

Typen, die das Pattern der inneren Veränderlichkeit verwenden, können wir nur
dann verwenden, wenn wir sicherstellen können, dass die Borrowing-Regeln zur
Laufzeit eingehalten werden, auch wenn der Compiler das nicht garantieren kann.
Der beteiligte `unsafe`-Code wird dann in eine sichere API verpackt, und der
äußere Typ bleibt unveränderlich.

Erkunden wir dieses Konzept anhand des Typs `RefCell<T>`, der dem Pattern der
inneren Veränderlichkeit folgt.

<!-- Old headings. Do not remove or links may break. -->

<a id="enforcing-borrowing-rules-at-runtime-with-refcellt"></a>

### Borrowing-Regeln zur Laufzeit durchsetzen {#enforcing-borrowing-rules-at-runtime}

Anders als `Rc<T>` steht der Typ `RefCell<T>` für eine einzige Ownership an den
Daten, die er enthält. Was unterscheidet `RefCell<T>` also von einem Typ wie
`Box<T>`? Erinnere dich an die Borrowing-Regeln, die du in Kapitel 4 gelernt
hast:

- Zu jedem Zeitpunkt kannst du _entweder_ eine veränderliche (_mutable_)
  Referenz oder beliebig viele unveränderliche Referenzen haben (aber nicht
  beides).
- Referenzen müssen immer gültig sein.

Bei Referenzen und `Box<T>` werden die Invarianten der Borrowing-Regeln zur
Kompilierzeit durchgesetzt. Bei `RefCell<T>` werden diese Invarianten _zur
Laufzeit_ durchgesetzt. Verletzt du diese Regeln bei Referenzen, bekommst du
einen Compilerfehler. Verletzt du diese Regeln bei `RefCell<T>`, löst dein
Programm einen Panic aus und wird beendet.

Die Vorteile der Prüfung der Borrowing-Regeln zur Kompilierzeit sind, dass
Fehler früher im Entwicklungsprozess gefunden werden und die Performance zur
Laufzeit nicht beeinträchtigt wird, weil die gesamte Analyse vorher
abgeschlossen ist. Aus diesen Gründen ist die Prüfung der Borrowing-Regeln zur
Kompilierzeit in den meisten Fällen die beste Wahl, weshalb sie in Rust der
Standard ist.

Der Vorteil der Prüfung der Borrowing-Regeln zur Laufzeit ist dagegen, dass dann
bestimmte speichersichere Szenarien erlaubt sind, die von den Prüfungen zur
Kompilierzeit verboten worden wären. Statische Analyse, wie sie der
Rust-Compiler durchführt, ist naturgemäß konservativ. Manche Eigenschaften von
Code lassen sich durch Analyse des Codes unmöglich erkennen: Das berühmteste
Beispiel ist das Halteproblem, das über den Rahmen dieses Buchs hinausgeht, aber
ein interessantes Thema zum Recherchieren ist.

Da manche Analysen unmöglich sind, weist der Rust-Compiler ein korrektes
Programm möglicherweise zurück, wenn er nicht sicher sein kann, dass der Code
die Ownership-Regeln einhält; in diesem Sinne ist er konservativ. Würde Rust ein
falsches Programm akzeptieren, könnten Nutzer den Garantien von Rust nicht
vertrauen. Weist Rust dagegen ein korrektes Programm zurück, ist das für die
Programmierenden unbequem, aber es kann nichts Katastrophales passieren. Der Typ
`RefCell<T>` ist nützlich, wenn du sicher bist, dass dein Code die
Borrowing-Regeln einhält, der Compiler das aber nicht verstehen und garantieren
kann.

Wie `Rc<T>` ist `RefCell<T>` nur für Szenarien mit einem einzigen Thread gedacht
und gibt dir einen Fehler zur Kompilierzeit, wenn du versuchst, es in einem
Kontext mit mehreren Threads zu verwenden. Wie man die Funktionalität von
`RefCell<T>` in einem Programm mit mehreren Threads erhält, besprechen wir in
Kapitel 16.

Hier ist eine Zusammenfassung der Gründe, `Box<T>`, `Rc<T>` oder `RefCell<T>` zu
wählen:

- `Rc<T>` ermöglicht mehrere Owner derselben Daten; `Box<T>` und `RefCell<T>`
  haben einen einzigen Owner.
- `Box<T>` erlaubt unveränderliche oder veränderliche Ausleihen (_borrows_), die
  zur Kompilierzeit geprüft werden; `Rc<T>` erlaubt nur unveränderliche
  Ausleihen, die zur Kompilierzeit geprüft werden; `RefCell<T>` erlaubt
  unveränderliche oder veränderliche Ausleihen, die zur Laufzeit geprüft werden.
- Da `RefCell<T>` veränderliche Ausleihen erlaubt, die zur Laufzeit geprüft
  werden, kannst du den Wert in der `RefCell<T>` verändern, selbst wenn die
  `RefCell<T>` unveränderlich ist.

Den Wert innerhalb eines unveränderlichen Werts zu verändern, ist das Pattern
der inneren Veränderlichkeit. Sehen wir uns eine Situation an, in der innere
Veränderlichkeit nützlich ist, und untersuchen, wie sie möglich ist.

<!-- Old headings. Do not remove or links may break. -->

<a id="interior-mutability-a-mutable-borrow-to-an-immutable-value"></a>

### Innere Veränderlichkeit verwenden {#using-interior-mutability}

Eine Folge der Borrowing-Regeln ist, dass du einen unveränderlichen Wert nicht
veränderlich ausleihen kannst. Dieser Code kompiliert zum Beispiel nicht:

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch15-smart-pointers/no-listing-01-cant-borrow-immutable-as-mutable/src/main.rs}}
```

Würdest du versuchen, diesen Code zu kompilieren, bekämst du folgenden Fehler:

```console
{{#include ../listings/ch15-smart-pointers/no-listing-01-cant-borrow-immutable-as-mutable/output.txt}}
```

Es gibt aber Situationen, in denen es nützlich wäre, wenn sich ein Wert in
seinen Methoden selbst verändern könnte, für anderen Code aber unveränderlich
erschiene. Code außerhalb der Methoden des Werts könnte den Wert nicht
verändern. `RefCell<T>` ist eine Möglichkeit, innere Veränderlichkeit zu
erhalten, aber `RefCell<T>` umgeht die Borrowing-Regeln nicht vollständig: Der
Borrow-Checker im Compiler erlaubt diese innere Veränderlichkeit, und die
Borrowing-Regeln werden stattdessen zur Laufzeit geprüft. Verletzt du die
Regeln, bekommst du statt eines Compilerfehlers einen `panic!`.

Gehen wir ein praktisches Beispiel durch, in dem wir mit `RefCell<T>` einen
unveränderlichen Wert verändern können, und sehen wir, warum das nützlich ist.

<!-- Old headings. Do not remove or links may break. -->

<a id="a-use-case-for-interior-mutability-mock-objects"></a>

#### Mit Mock-Objekten testen {#testing-with-mock-objects}

Manchmal verwenden Programmierende beim Testen einen Typ anstelle eines anderen
Typs, um ein bestimmtes Verhalten zu beobachten und zuzusichern, dass es korrekt
implementiert ist. Dieser Platzhaltertyp heißt _Test-Double_. Stell ihn dir im
Sinne eines Stunt-Doubles beim Film vor, bei dem eine Person einspringt und
einen Schauspieler bei einer besonders schwierigen Szene vertritt. Test-Doubles
vertreten andere Typen, wenn wir Tests ausführen. _Mock-Objekte_ sind bestimmte
Arten von Test-Doubles, die aufzeichnen, was während eines Tests passiert,
sodass du zusichern kannst, dass die richtigen Aktionen stattgefunden haben.

Rust hat keine Objekte in demselben Sinn, wie andere Sprachen Objekte haben, und
Rust hat keine Mock-Objekt-Funktionalität in die Standardbibliothek eingebaut,
wie es manche anderen Sprachen tun. Du kannst aber durchaus ein Struct
erstellen, das denselben Zweck erfüllt wie ein Mock-Objekt.

Hier ist das Szenario, das wir testen: Wir erstellen eine Bibliothek, die einen
Wert im Verhältnis zu einem Höchstwert verfolgt und Nachrichten sendet, je
nachdem, wie nah der aktuelle Wert am Höchstwert ist. Diese Bibliothek könnte
zum Beispiel verwendet werden, um das Kontingent eines Benutzers an erlaubten
API-Aufrufen zu verfolgen.

Unsere Bibliothek stellt nur die Funktionalität bereit, zu verfolgen, wie nah
ein Wert am Höchstwert ist und welche Nachrichten wann gesendet werden sollen.
Von Anwendungen, die unsere Bibliothek verwenden, wird erwartet, dass sie den
Mechanismus zum Senden der Nachrichten bereitstellen: Die Anwendung könnte die
Nachricht dem Benutzer direkt anzeigen, eine E-Mail senden, eine Textnachricht
senden oder etwas anderes tun. Die Bibliothek muss dieses Detail nicht kennen.
Sie braucht nur etwas, das einen von uns bereitgestellten Trait namens
`Messenger` implementiert. Listing 15-20 zeigt den Code der Bibliothek.

<Listing number="15-20" file-name="src/lib.rs" caption="Eine Bibliothek, die verfolgt, wie nah ein Wert an einem Höchstwert ist, und warnt, wenn der Wert bestimmte Stufen erreicht">

```rust,noplayground
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-20/src/lib.rs}}
```

</Listing>

Ein wichtiger Teil dieses Codes ist, dass der Trait `Messenger` eine Methode
namens `send` hat, die eine unveränderliche Referenz auf `self` und den Text der
Nachricht nimmt. Dieser Trait ist die Schnittstelle, die unser Mock-Objekt
implementieren muss, damit das Mock genauso verwendet werden kann wie ein echtes
Objekt. Der andere wichtige Teil ist, dass wir das Verhalten der Methode
`set_value` auf dem `LimitTracker` testen wollen. Wir können ändern, was wir für
den Parameter `value` übergeben, aber `set_value` gibt nichts zurück, worüber
wir Assertions machen könnten. Wir wollen sagen können: Wenn wir einen
`LimitTracker` mit etwas erzeugen, das den Trait `Messenger` implementiert, und
einen bestimmten Wert für `max` angeben, wird der Messenger angewiesen, die
passenden Nachrichten zu senden, wenn wir verschiedene Zahlen für `value`
übergeben.

Wir brauchen ein Mock-Objekt, das beim Aufruf von `send` keine E-Mail oder
Textnachricht sendet, sondern nur die Nachrichten festhält, die es senden soll.
Wir können eine neue Instanz des Mock-Objekts erzeugen, einen `LimitTracker`
erstellen, der das Mock-Objekt verwendet, die Methode `set_value` auf dem
`LimitTracker` aufrufen und dann prüfen, ob das Mock-Objekt die erwarteten
Nachrichten hat. Listing 15-21 zeigt einen Versuch, ein Mock-Objekt zu
implementieren, das genau das tut, aber der Borrow-Checker lässt es nicht zu.

<Listing number="15-21" file-name="src/lib.rs" caption="Ein Versuch, einen `MockMessenger` zu implementieren, den der Borrow-Checker nicht zulässt">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-21/src/lib.rs:here}}
```

</Listing>

Dieser Testcode definiert ein Struct `MockMessenger` mit einem Feld
`sent_messages`, das einen `Vec` von `String`-Werten enthält, um die Nachrichten
festzuhalten, die es senden soll. Außerdem definieren wir eine assoziierte
Funktion `new`, mit der sich bequem neue `MockMessenger`-Werte erzeugen lassen,
die mit einer leeren Liste von Nachrichten beginnen. Dann implementieren wir den
Trait `Messenger` für `MockMessenger`, damit wir einem `LimitTracker` einen
`MockMessenger` übergeben können. In der Definition der Methode `send` nehmen
wir die als Parameter übergebene Nachricht und speichern sie in der Liste
`sent_messages` des `MockMessenger`.

Im Test prüfen wir, was passiert, wenn der `LimitTracker` angewiesen wird,
`value` auf etwas zu setzen, das mehr als 75 Prozent des Werts `max` beträgt.
Zuerst erzeugen wir einen neuen `MockMessenger`, der mit einer leeren Liste von
Nachrichten beginnt. Dann erzeugen wir einen neuen `LimitTracker` und geben ihm
eine Referenz auf den neuen `MockMessenger` und einen `max`-Wert von `100`. Wir
rufen die Methode `set_value` auf dem `LimitTracker` mit dem Wert `80` auf, was
mehr als 75 Prozent von 100 ist. Dann sichern wir zu, dass die Liste der
Nachrichten, die der `MockMessenger` festhält, jetzt eine Nachricht enthalten
sollte.

Es gibt aber ein Problem mit diesem Test, wie hier zu sehen:

```console
{{#include ../listings/ch15-smart-pointers/listing-15-21/output.txt}}
```

Wir können den `MockMessenger` nicht so verändern, dass er die Nachrichten
festhält, weil die Methode `send` eine unveränderliche Referenz auf `self`
nimmt. Wir können auch nicht dem Vorschlag aus dem Fehlertext folgen und sowohl
in der `impl`-Methode als auch in der Trait-Definition `&mut self` verwenden.
Wir wollen den Trait `Messenger` nicht allein für das Testen ändern. Stattdessen
müssen wir einen Weg finden, wie unser Testcode mit unserem bestehenden Design
korrekt funktioniert.

Das ist eine Situation, in der innere Veränderlichkeit helfen kann! Wir
speichern `sent_messages` in einer `RefCell<T>`, und dann kann die Methode
`send` `sent_messages` verändern, um die Nachrichten zu speichern, die wir
gesehen haben. Listing 15-22 zeigt, wie das aussieht.

<Listing number="15-22" file-name="src/lib.rs" caption="Mit `RefCell<T>` einen inneren Wert verändern, während der äußere Wert als unveränderlich gilt">

```rust,noplayground
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-22/src/lib.rs:here}}
```

</Listing>

Das Feld `sent_messages` hat jetzt den Typ `RefCell<Vec<String>>` statt
`Vec<String>`. In der Funktion `new` erzeugen wir eine neue Instanz von
`RefCell<Vec<String>>` um den leeren Vektor.

Bei der Implementierung der Methode `send` ist der erste Parameter weiterhin
eine unveränderliche Ausleihe von `self`, was zur Trait-Definition passt. Wir
rufen `borrow_mut` auf der `RefCell<Vec<String>>` in `self.sent_messages` auf,
um eine veränderliche Referenz auf den Wert in der `RefCell<Vec<String>>` zu
erhalten, also auf den Vektor. Dann können wir `push` auf der veränderlichen
Referenz auf den Vektor aufrufen, um die während des Tests gesendeten
Nachrichten festzuhalten.

Die letzte Änderung, die wir vornehmen müssen, betrifft die Assertion: Um zu
sehen, wie viele Elemente im inneren Vektor sind, rufen wir `borrow` auf der
`RefCell<Vec<String>>` auf, um eine unveränderliche Referenz auf den Vektor zu
erhalten.

Nachdem du gesehen hast, wie man `RefCell<T>` verwendet, sehen wir uns an, wie
es funktioniert!

<!-- Old headings. Do not remove or links may break. -->

<a id="keeping-track-of-borrows-at-runtime-with-refcellt"></a>

#### Ausleihen zur Laufzeit verfolgen {#tracking-borrows-at-runtime}

Beim Erzeugen unveränderlicher und veränderlicher Referenzen verwenden wir die
Syntax `&` bzw. `&mut`. Bei `RefCell<T>` verwenden wir die Methoden `borrow` und
`borrow_mut`, die Teil der sicheren API von `RefCell<T>` sind. Die Methode
`borrow` gibt den Smart-Pointer-Typ `Ref<T>` zurück, und `borrow_mut` gibt den
Smart-Pointer-Typ `RefMut<T>` zurück. Beide Typen implementieren `Deref`, daher
können wir sie wie normale Referenzen behandeln.

Die `RefCell<T>` hält fest, wie viele Smart-Pointer `Ref<T>` und `RefMut<T>`
gerade aktiv sind. Jedes Mal, wenn wir `borrow` aufrufen, erhöht die
`RefCell<T>` ihren Zähler aktiver unveränderlicher Ausleihen. Verlässt ein
`Ref<T>`-Wert den Gültigkeitsbereich (_scope_), sinkt der Zähler
unveränderlicher Ausleihen um 1. Genau wie bei den Borrowing-Regeln zur
Kompilierzeit erlaubt uns `RefCell<T>` zu jedem Zeitpunkt viele unveränderliche
Ausleihen oder eine veränderliche Ausleihe.

Versuchen wir, diese Regeln zu verletzen, bekommen wir keinen Compilerfehler wie
bei Referenzen, sondern die Implementierung von `RefCell<T>` löst zur Laufzeit
einen Panic aus. Listing 15-23 zeigt eine Abwandlung der Implementierung von
`send` aus Listing 15-22. Wir versuchen absichtlich, zwei veränderliche
Ausleihen im selben Gültigkeitsbereich aktiv zu haben, um zu zeigen, dass
`RefCell<T>` uns das zur Laufzeit verwehrt.

<Listing number="15-23" file-name="src/lib.rs" caption="Zwei veränderliche Referenzen im selben Gültigkeitsbereich erzeugen, um zu sehen, dass `RefCell<T>` einen Panic auslöst">

```rust,ignore,panics
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-23/src/lib.rs:here}}
```

</Listing>

Wir erzeugen eine Variable `one_borrow` für den Smart-Pointer `RefMut<T>`, den
`borrow_mut` zurückgibt. Dann erzeugen wir auf dieselbe Weise eine weitere
veränderliche Ausleihe in der Variable `two_borrow`. Damit gibt es zwei
veränderliche Referenzen im selben Gültigkeitsbereich, was nicht erlaubt ist.
Wenn wir die Tests für unsere Bibliothek ausführen, kompiliert der Code in
Listing 15-23 ohne Fehler, aber der Test schlägt fehl:

```console
{{#include ../listings/ch15-smart-pointers/listing-15-23/output.txt}}
```

Beachte, dass der Code einen Panic mit der Meldung
`already borrowed:
BorrowMutError` ausgelöst hat. So behandelt `RefCell<T>`
Verletzungen der Borrowing-Regeln zur Laufzeit.

Wenn du dich wie hier dafür entscheidest, Borrowing-Fehler zur Laufzeit statt
zur Kompilierzeit abzufangen, findest du Fehler in deinem Code möglicherweise
erst später im Entwicklungsprozess: vielleicht erst, wenn dein Code bereits in
Produktion ist. Außerdem hätte dein Code eine kleine Performance-Einbuße zur
Laufzeit, weil die Ausleihen zur Laufzeit statt zur Kompilierzeit verfolgt
werden. Mit `RefCell<T>` lässt sich aber ein Mock-Objekt schreiben, das sich
selbst verändern kann, um die Nachrichten festzuhalten, die es gesehen hat,
während du es in einem Kontext verwendest, in dem nur unveränderliche Werte
erlaubt sind. Du kannst `RefCell<T>` trotz seiner Nachteile verwenden, um mehr
Funktionalität zu erhalten, als normale Referenzen bieten.

<!-- Old headings. Do not remove or links may break. -->

<a id="having-multiple-owners-of-mutable-data-by-combining-rc-t-and-ref-cell-t"></a>
<a id="allowing-multiple-owners-of-mutable-data-with-rct-and-refcellt"></a>

### Mehrere Owner veränderlicher Daten ermöglichen {#allowing-multiple-owners-of-mutable-data}

Häufig wird `RefCell<T>` in Kombination mit `Rc<T>` verwendet. Erinnere dich,
dass `Rc<T>` dir mehrere Owner für Daten erlaubt, aber nur unveränderlichen
Zugriff auf diese Daten gibt. Hast du ein `Rc<T>`, das eine `RefCell<T>`
enthält, kannst du einen Wert erhalten, der mehrere Owner haben kann _und_ den
du verändern kannst!

Erinnere dich zum Beispiel an das Cons-Listen-Beispiel in Listing 15-18, in dem
wir `Rc<T>` verwendet haben, damit sich mehrere Listen die Ownership einer
anderen Liste teilen können. Da `Rc<T>` nur unveränderliche Werte enthält,
können wir keinen der Werte in der Liste ändern, nachdem wir sie erzeugt haben.
Fügen wir `RefCell<T>` hinzu, um die Werte in den Listen ändern zu können.
Listing 15-24 zeigt, dass wir durch eine `RefCell<T>` in der Definition von
`Cons` den Wert verändern können, der in allen Listen gespeichert ist.

<Listing number="15-24" file-name="src/main.rs" caption="Mit `Rc<RefCell<i32>>` eine `List` erzeugen, die wir verändern können">

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-24/src/main.rs}}
```

</Listing>

Wir erzeugen einen Wert, der eine Instanz von `Rc<RefCell<i32>>` ist, und
speichern ihn in einer Variable namens `value`, damit wir später direkt darauf
zugreifen können. Dann erzeugen wir in `a` eine `List` mit einer
`Cons`-Variante, die `value` enthält. Wir müssen `value` klonen, damit sowohl
`a` als auch `value` die Ownership des inneren Werts `5` haben, statt die
Ownership von `value` an `a` zu übertragen oder `a` von `value` ausleihen zu
lassen.

Wir verpacken die Liste `a` in ein `Rc<T>`, damit beim Erzeugen der Listen `b`
und `c` beide auf `a` verweisen können, wie wir es in Listing 15-18 getan haben.

Nachdem wir die Listen in `a`, `b` und `c` erzeugt haben, wollen wir 10 zum Wert
in `value` addieren. Dazu rufen wir `borrow_mut` auf `value` auf, was das in
Kapitel 4 besprochene Feature der automatischen Dereferenzierung nutzt, um das
`Rc<T>` zum inneren `RefCell<T>`-Wert zu dereferenzieren. Die Methode
`borrow_mut` gibt einen Smart-Pointer `RefMut<T>` zurück, auf den wir den
Dereferenzierungsoperator anwenden, um den inneren Wert zu ändern.

Wenn wir `a`, `b` und `c` ausgeben, sehen wir, dass sie alle den veränderten
Wert `15` statt `5` haben:

```console
{{#include ../listings/ch15-smart-pointers/listing-15-24/output.txt}}
```

Diese Technik ist ziemlich raffiniert! Durch `RefCell<T>` haben wir einen nach
außen unveränderlichen `List`-Wert. Aber wir können die Methoden von
`RefCell<T>` verwenden, die Zugriff auf ihre innere Veränderlichkeit geben,
sodass wir unsere Daten verändern können, wenn wir es müssen. Die
Laufzeitprüfungen der Borrowing-Regeln schützen uns vor Data-Races, und manchmal
lohnt es sich, für diese Flexibilität in unseren Datenstrukturen etwas
Geschwindigkeit einzutauschen. Beachte, dass `RefCell<T>` nicht für Code mit
mehreren Threads funktioniert! `Mutex<T>` ist die threadsichere Version von
`RefCell<T>`, und `Mutex<T>` besprechen wir in Kapitel 16.

{{#quiz ../quizzes/ch15-05-interior-mutability.toml}}

[wheres-the---operator]: ch05-03-method-syntax.html#wheres-the---operator
