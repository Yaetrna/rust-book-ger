## Was ist Ownership? {#what-is-ownership}

Ownership ist eine Disziplin, die die **Sicherheit** von Rust-Programmen gewährleistet. Um Ownership zu verstehen, müssen wir zunächst verstehen, was ein Rust-Programm sicher (oder unsicher) macht.

### Sicherheit ist die Abwesenheit von undefiniertem Verhalten {#safety-is-the-absence-of-undefined-behavior}

Fangen wir mit einem Beispiel an. Dieses Programm lässt sich sicher ausführen:

```rust
fn read(y: bool) {
    if y {
        println!("y is true!");
    }
}

fn main() {
    let x = true;
    read(x);
}
```

Wir können dieses Programm unsicher machen, indem wir den Aufruf von `read` vor die Definition von `x` verschieben:

```rust,ignore,does_not_compile
fn read(y: bool) {
    if y {
        println!("y is true!");
    }
}

fn main() {
    read(x); // oh no! x isn't defined!
    let x = true;
}
```

> _Hinweis_: In diesem Kapitel verwenden wir viele Codebeispiele, die sich nicht kompilieren lassen. Achte auf die Fragezeichen-Krabbe, wenn du nicht sicher bist, ob sich ein Programm kompilieren lassen sollte oder nicht.

Dieses zweite Programm ist unsicher, weil `read(x)` erwartet, dass `x` einen Wert vom Typ `bool` hat, `x` aber noch keinen Wert hat.

Wird ein Programm wie dieses von einem Interpreter ausgeführt, würde das Lesen von `x` vor seiner Definition eine Exception auslösen, etwa einen [`NameError`] in Python oder einen [`ReferenceError`] in JavaScript. Exceptions haben aber ihren Preis. Jedes Mal, wenn ein interpretiertes Programm eine Variable liest, muss der Interpreter prüfen, ob diese Variable definiert ist.

Das Ziel von Rust ist es, Programme zu effizienten Binärdateien zu kompilieren, die so wenige Laufzeitprüfungen wie möglich brauchen. Deshalb prüft Rust nicht zur _Laufzeit_, ob eine Variable vor ihrer Verwendung definiert ist. Stattdessen prüft Rust das zur _Kompilierzeit_. Wenn du versuchst, das unsichere Programm zu kompilieren, bekommst du diesen Fehler:

```text
error[E0425]: cannot find value `x` in this scope
 --> src/main.rs:8:10
  |
8 |     read(x); // oh no! x isn't defined!
  |          ^ not found in this scope
```

Vermutlich hast du das Gefühl, dass es gut ist, wenn Rust sicherstellt, dass Variablen vor ihrer Verwendung definiert sind. Aber warum? Um die Regel zu begründen, müssen wir fragen: **Was würde passieren, wenn Rust ein abgelehntes Programm kompilieren ließe?**

Sehen wir uns zunächst an, wie das sichere Programm kompiliert und ausgeführt wird. Auf einem Computer mit einem Prozessor der [x86](https://en.wikipedia.org/wiki/X86)-Architektur erzeugt Rust für die Funktion `main` im sicheren Programm folgenden Assemblercode ([den vollständigen Assemblercode findest du hier](https://rust.godbolt.org/z/xnT1fzsqv)):

```x86asm
main:
    ; ...
    mov     edi, 1
    call    read
    ; ...
```

> _Hinweis_: Wenn du dich mit Assemblercode nicht auskennst, ist das kein Problem! Dieser Abschnitt enthält nur ein paar Assembler-Beispiele, um dir zu zeigen, wie Rust unter der Haube tatsächlich funktioniert. Im Allgemeinen musst du kein Assembler können, um Rust zu verstehen.

Dieser Assemblercode wird:

- Die Zahl 1, die `true` darstellt, in ein „Register“ (eine Art Assembler-Variable) namens `edi` kopieren.
- Die Funktion `read` aufrufen, die erwartet, dass ihr erstes Argument `y` im Register `edi` steht.

Dürfte die unsichere Funktion kompiliert werden, sähe ihr Assemblercode vielleicht so aus:

```x86asm
main:
    ; ...
    call    read
    mov     edi, 1    ; mov is after call
    ; ...
```

Dieses Programm ist unsicher, weil `read` erwartet, dass `edi` ein boolescher Wert ist, also entweder die Zahl `0` oder `1`. Aber `edi` könnte alles Mögliche sein: `2`, `100`, `0x1337BEEF`. Sobald `read` sein Argument `y` für irgendetwas verwenden will, verursacht es sofort _**UNDEFINIERTES VERHALTEN!**_

Rust legt nicht fest, was passiert, wenn du `if y { .. }` ausführst, während `y` weder `true` noch `false` ist. Dieses _Verhalten_, also das, was nach dem Ausführen der Anweisung passiert, ist _undefiniert_. Irgendetwas wird passieren, zum Beispiel:

- Der Code läuft ohne Absturz, und niemand bemerkt ein Problem.
- Der Code stürzt sofort ab, wegen eines [Segmentation Fault](https://en.wikipedia.org/wiki/Segmentation_fault) oder eines anderen Betriebssystemfehlers.
- Der Code läuft ohne Absturz, bis ein Angreifer genau die richtige Eingabe erzeugt, um deine Produktionsdatenbank zu löschen, deine Backups zu überschreiben und dir dein Pausenbrot zu klauen.

**Ein grundlegendes Ziel von Rust ist es, sicherzustellen, dass deine Programme nie undefiniertes Verhalten haben.** Das ist mit „Sicherheit“ gemeint. Undefiniertes Verhalten ist besonders gefährlich für Low-Level-Programme mit direktem Zugriff auf den Speicher. Etwa [70 % der gemeldeten Sicherheitslücken](https://msrc.microsoft.com/blog/2019/07/a-proactive-approach-to-more-secure-code/) in Low-Level-Systemen werden durch Speicherkorruption verursacht, eine Form von undefiniertem Verhalten.

Ein zweites Ziel von Rust ist es, undefiniertes Verhalten zur _Kompilierzeit_ statt zur _Laufzeit_ zu verhindern. Dieses Ziel hat zwei Beweggründe:

1. Fehler zur Kompilierzeit zu erkennen bedeutet, diese Fehler in der Produktion zu vermeiden, was die Zuverlässigkeit deiner Software verbessert.
2. Fehler zur Kompilierzeit zu erkennen bedeutet, weniger Laufzeitprüfungen für diese Fehler zu brauchen, was die Performance deiner Software verbessert.

Rust kann nicht alle Fehler verhindern. Wenn eine Anwendung einen öffentlichen, nicht authentifizierten Endpunkt `/delete-production-database` anbietet, braucht ein Angreifer keine verdächtige if-Anweisung, um die Datenbank zu löschen. Trotzdem machen die Schutzmechanismen von Rust Programme wahrscheinlich sicherer als eine Sprache mit weniger Schutzmechanismen, wie z. B. [das Android-Team von Google](https://security.googleblog.com/2022/12/memory-safe-languages-in-android-13.html) festgestellt hat.

### Ownership als Disziplin für Speichersicherheit {#ownership-as-a-discipline-for-memory-safety}

Da Sicherheit die Abwesenheit von undefiniertem Verhalten ist und Ownership mit Sicherheit zu tun hat, müssen wir Ownership anhand der Formen undefinierten Verhaltens verstehen, die es verhindert. Die Rust-Referenz führt eine lange Liste von [„Behavior considered undefined“](https://doc.rust-lang.org/reference/behavior-considered-undefined.html) (als undefiniert geltendes Verhalten). Vorerst konzentrieren wir uns auf eine Kategorie: Operationen auf dem Speicher.

Der Speicher ist der Ort, an dem Daten während der Ausführung eines Programms abgelegt werden. Es gibt viele Arten, über Speicher nachzudenken:

- Wenn du mit Systemprogrammierung nicht vertraut bist, denkst du vielleicht auf hoher Ebene an Speicher, etwa: „Speicher ist der Arbeitsspeicher in meinem Computer“ oder „Speicher ist das, was ausgeht, wenn ich zu viele Daten lade“.
- Wenn du mit Systemprogrammierung vertraut bist, denkst du vielleicht auf niedriger Ebene an Speicher, etwa: „Speicher ist ein Array von Bytes“ oder „Speicher sind die Zeiger, die ich von `malloc` zurückbekomme“.

Beide Speichermodelle sind _gültig_, aber sie sind keine _nützlichen_ Denkweisen dafür, wie Rust funktioniert. Das High-Level-Modell ist zu abstrakt, um zu erklären, wie Rust funktioniert. Du musst zum Beispiel das Konzept eines Zeigers verstehen. Das Low-Level-Modell ist zu konkret, um zu erklären, wie Rust funktioniert. Rust erlaubt dir zum Beispiel nicht, Speicher als Array von Bytes zu interpretieren.

Rust bietet eine bestimmte Art, über Speicher nachzudenken. Ownership ist eine Disziplin, um Speicher innerhalb dieser Denkweise sicher zu verwenden. Der Rest dieses Kapitels erklärt das Speichermodell von Rust.

### Variablen leben auf dem Stack {#variables-live-in-the-stack}

Hier ist ein Programm wie das aus Abschnitt 3.3, das eine Zahl `n` definiert und eine Funktion `plus_one` mit `n` aufruft. Unter dem Programm siehst du eine neue Art von Diagramm. Dieses Diagramm veranschaulicht den Inhalt des Speichers während der Ausführung des Programms an den drei markierten Stellen.

```aquascope,interpreter,horizontal
fn main() {
    let n = 5;`[]`
    let y = plus_one(n);`[]`
    println!("The value of y is: {y}");
}

fn plus_one(x: i32) -> i32 {
    `[]`x + 1
}
```

Variablen leben in **Frames**. Ein Frame ist eine Zuordnung von Variablen zu Werten innerhalb eines einzelnen Gültigkeitsbereichs (_scope_), etwa einer Funktion. Zum Beispiel:

- Der Frame von `main` enthält an der Stelle L1 `n = 5`.
- Der Frame von `plus_one` enthält bei L2 `x = 5`.
- Der Frame von `main` enthält an der Stelle L3 `n = 5; y = 6`.

Frames sind in einem **Stack** der gerade aufgerufenen Funktionen organisiert. Bei L2 liegt zum Beispiel der Frame von `main` über dem Frame der aufgerufenen Funktion `plus_one`. Nachdem eine Funktion zurückgekehrt ist, gibt Rust den Frame der Funktion frei. (Freigeben nennt man auch **Freeing** oder **Dropping**, auf Deutsch _verwerfen_; wir verwenden diese Begriffe gleichbedeutend.) Diese Folge von Frames heißt Stack (Stapel), weil der zuletzt hinzugefügte Frame immer der nächste ist, der freigegeben wird.

> _Hinweis:_ Dieses Speichermodell beschreibt nicht vollständig, wie Rust tatsächlich funktioniert! Wie wir vorhin beim Assemblercode gesehen haben, legt der Rust-Compiler `n` oder `x` vielleicht in ein Register statt in einen Stack-Frame. Diese Unterscheidung ist aber ein Implementierungsdetail. Sie sollte dein Verständnis von Sicherheit in Rust nicht verändern, daher können wir uns auf den einfacheren Fall von Variablen konzentrieren, die nur in Frames liegen.

Wenn ein Ausdruck eine Variable liest, wird der Wert der Variable aus ihrem Platz im Stack-Frame kopiert. Führen wir zum Beispiel dieses Programm aus:

```aquascope,interpreter,horizontal
#fn main() {
let a = 5;`[]`
let mut b = a;`[]`
b += 1;`[]`
#}
```

Der Wert von `a` wird in `b` kopiert, und `a` bleibt unverändert, auch nachdem `b` geändert wurde.

### Boxen leben auf dem Heap {#boxes-live-in-the-heap}

Das Kopieren von Daten kann allerdings viel Speicher belegen. Hier ist zum Beispiel ein leicht abgewandeltes Programm. Dieses Programm kopiert ein Array mit 1 Million Elementen:

```aquascope,interpreter
#fn main() {
let a = [0; 1_000_000];`[]`
let b = a;`[]`
#}
```

Beachte, dass der Frame von `main` durch das Kopieren von `a` in `b` 2 Millionen Elemente enthält.

Um den Zugriff auf Daten weiterzugeben, ohne sie zu kopieren, verwendet Rust **Zeiger**. Ein Zeiger ist ein Wert, der eine Stelle im Speicher beschreibt. Den Wert, auf den ein Zeiger zeigt, nennt man seinen **Pointee** (das Ziel des Zeigers). Eine gängige Art, einen Zeiger zu erzeugen, ist es, Speicher auf dem **Heap** zu allozieren. Der Heap ist ein separater Speicherbereich, in dem Daten unbegrenzt lange leben können. Heap-Daten sind nicht an einen bestimmten Stack-Frame gebunden. Rust bietet ein Konstrukt namens [`Box`](https://doc.rust-lang.org/std/boxed/index.html), um Daten auf den Heap zu legen. Wir können das Array mit einer Million Elementen zum Beispiel so in `Box::new` einpacken:

```aquascope,interpreter
#fn main() {
let a = Box::new([0; 1_000_000]);`[]`
let b = a;`[]`
#}
```

Beachte, dass es jetzt immer nur ein einziges Array gleichzeitig gibt. Bei L1 ist der Wert von `a` ein Zeiger (dargestellt als Punkt mit Pfeil) auf das Array im Heap. Die Anweisung `let b = a` kopiert den Zeiger aus `a` nach `b`, die Daten, auf die er zeigt, werden aber nicht kopiert. Beachte, dass `a` jetzt ausgegraut ist, weil es _verschoben_ (_moved_) wurde – was das bedeutet, sehen wir gleich.

{{#quiz ../quizzes/ch04-01-ownership-sec1-stackheap.toml}}

### Rust erlaubt keine manuelle Speicherverwaltung {#rust-does-not-permit-manual-memory-management}

Speicherverwaltung ist der Vorgang, Speicher zu allozieren und freizugeben. Anders gesagt ist es der Vorgang, ungenutzten Speicher zu finden und diesen Speicher später zurückzugeben, wenn er nicht mehr verwendet wird. Stack-Frames werden von Rust automatisch verwaltet. Wenn eine Funktion aufgerufen wird, alloziert Rust einen Stack-Frame für die aufgerufene Funktion. Wenn der Aufruf endet, gibt Rust den Stack-Frame frei.

Wie wir oben gesehen haben, werden Heap-Daten beim Aufruf von `Box::new(..)` alloziert. Aber wann werden Heap-Daten freigegeben? Stell dir vor, Rust hätte eine Funktion `free()`, die eine Heap-Allokation freigibt. Stell dir vor, Rust würde Programmierern erlauben, `free` aufzurufen, wann immer sie wollen. Diese Art „manueller“ Speicherverwaltung führt leicht zu Bugs. Wir könnten zum Beispiel einen Zeiger auf freigegebenen Speicher lesen:

```aquascope,interpreter,shouldFail
#fn free<T>(_t: T) {}
#fn main() {
let b = Box::new([0; 100]);`[]`
free(b);`[]`
assert!(b[0] == 0);`[]`
#}
```

> _Hinweis:_ Vielleicht fragst du dich, wie wir dieses Rust-Programm ausführen, obwohl es sich nicht kompilieren lässt. Wir verwenden [spezielle Werkzeuge](https://github.com/cognitive-engineering-lab/aquascope), um Rust zu Lernzwecken so zu simulieren, als wäre der Borrow-Checker abgeschaltet. So können wir „Was wäre, wenn“-Fragen beantworten, etwa: Was wäre, wenn Rust dieses unsichere Programm kompilieren ließe?

Hier allozieren wir ein Array auf dem Heap. Dann rufen wir `free(b)` auf, was den Heap-Speicher von `b` freigibt. Der Wert von `b` ist deshalb ein Zeiger auf ungültigen Speicher, den wir mit dem Symbol „⦻“ darstellen. Bisher ist noch kein undefiniertes Verhalten aufgetreten! Bei L2 ist das Programm noch sicher. Ein ungültiger Zeiger ist nicht zwangsläufig ein Problem.

Das undefinierte Verhalten tritt auf, wenn wir versuchen, den Zeiger zu _verwenden_, indem wir `b[0]` lesen. Das wäre ein Versuch, auf ungültigen Speicher zuzugreifen, der das Programm abstürzen lassen könnte. Oder schlimmer: Es könnte nicht abstürzen und beliebige Daten zurückgeben. Deshalb ist dieses Programm **unsicher**.

Rust erlaubt Programmen nicht, Speicher manuell freizugeben. Diese Regel vermeidet die oben gezeigten Arten von undefiniertem Verhalten.

### Der Owner einer Box verwaltet ihre Freigabe {#a-boxs-owner-manages-deallocation}

Stattdessen gibt Rust den Heap-Speicher einer Box _automatisch_ frei. Hier ist eine _fast_ korrekte Beschreibung der Regel, nach der Rust Boxen freigibt:

> **Prinzip der Box-Freigabe (fast korrekt)** (_Box deallocation principle_): Wenn eine Variable an eine Box gebunden ist, gibt Rust beim Freigeben des Frames der Variable auch den Heap-Speicher der Box frei.

Verfolgen wir zum Beispiel ein Programm, das eine Box alloziert und freigibt:

```aquascope,interpreter,horizontal
fn main() {
    let a_num = 4;`[]`
    make_and_drop();`[]`
}

fn make_and_drop() {
    let a_box = Box::new(5);`[]`
}
```

Bei L1, vor dem Aufruf von `make_and_drop`, besteht der Zustand des Speichers nur aus dem Stack-Frame von `main`. Bei L2, während des Aufrufs von `make_and_drop`, zeigt `a_box` auf `5` auf dem Heap. Sobald `make_and_drop` fertig ist, gibt Rust seinen Stack-Frame frei. `make_and_drop` enthält die Variable `a_box`, also gibt Rust auch die Heap-Daten in `a_box` frei. Bei L3 ist der Heap deshalb leer.

Der Heap-Speicher der Box wurde erfolgreich verwaltet. Aber was, wenn wir dieses System missbrauchen? Zurück zu unserem früheren Beispiel: Was passiert, wenn wir zwei Variablen an eine Box binden?

```rust,ignore
# fn main() {
let a = Box::new([0; 1_000_000]);
let b = a;
# }
```

Das Array in der Box ist jetzt sowohl an `a` als auch an `b` gebunden. Nach unserem „fast korrekten“ Prinzip würde Rust versuchen, den Heap-Speicher der Box _zweimal_ freizugeben, einmal für jede Variable. Auch das ist undefiniertes Verhalten!

Um diese Situation zu vermeiden, kommen wir endlich zu Ownership. Wenn `a` an `Box::new([0; 1_000_000])` gebunden wird, sagen wir, dass `a` die Box **besitzt** (_owns_). Die Anweisung `let b = a` **verschiebt** (_moves_) die Ownership der Box von `a` nach `b`. Mit diesen Begriffen lässt sich die Regel, nach der Rust Boxen freigibt, genauer so beschreiben:

> **Prinzip der Box-Freigabe (vollständig korrekt):** Wenn eine Variable eine Box besitzt, gibt Rust beim Freigeben des Frames der Variable auch den Heap-Speicher der Box frei.

Im obigen Beispiel besitzt `b` das Array in der Box. Wenn der Gültigkeitsbereich endet, gibt Rust die Box deshalb nur einmal frei, und zwar für `b`, nicht für `a`.

### Collections verwenden Boxen {#collections-use-boxes}

Boxen werden von Rust-Datenstrukturen[^boxed-data-structures] wie [`Vec`](https://doc.rust-lang.org/std/vec/struct.Vec.html), [`String`](https://doc.rust-lang.org/std/string/struct.String.html) und [`HashMap`](https://doc.rust-lang.org/std/collections/struct.HashMap.html) verwendet, um eine variable Anzahl von Elementen aufzunehmen. Hier ist zum Beispiel ein Programm, das einen String erzeugt, verschiebt und verändert:

```aquascope,interpreter,horizontal
fn main() {
    let first = String::from("Ferris");`[]`
    let full = add_suffix(first);`[]`
    println!("{full}");
}

fn add_suffix(mut name: String) -> String {
    `[]`name.push_str(" Jr.");`[]`
    name
}
```

Dieses Programm ist etwas aufwendiger, also verfolge jeden Schritt genau:

1. Bei L1 wurde der String „Ferris“ auf dem Heap alloziert. Er gehört `first`.
2. Bei L2 wurde die Funktion `add_suffix(first)` aufgerufen. Dadurch wird die Ownership des Strings von `first` nach `name` verschoben. Die String-Daten werden nicht kopiert, wohl aber der Zeiger auf die Daten.
3. Bei L3 vergrößert die Funktion `name.push_str(" Jr.")` die Heap-Allokation des Strings. Dabei passieren drei Dinge. Erstens erzeugt sie eine neue, größere Allokation. Zweitens schreibt sie „Ferris Jr.“ in die neue Allokation. Drittens gibt sie den ursprünglichen Heap-Speicher frei. `first` zeigt jetzt auf freigegebenen Speicher.
4. Bei L4 ist der Frame von `add_suffix` verschwunden. Diese Funktion hat `name` zurückgegeben und damit die Ownership des Strings an `full` übertragen.

### Variablen können nach einem Move nicht mehr verwendet werden {#variables-cannot-be-used-after-being-moved}

Das String-Programm hilft, ein zentrales Sicherheitsprinzip der Ownership zu veranschaulichen. Stell dir vor, `first` würde in `main` nach dem Aufruf von `add_suffix` verwendet. Wir können ein solches Programm simulieren und uns das daraus entstehende undefinierte Verhalten ansehen:

```aquascope,interpreter,shouldFail
fn main() {
    let first = String::from("Ferris");
    let full = add_suffix(first);
    println!("{full}, originally {first}");`[]` // first is now used here
}

fn add_suffix(mut name: String) -> String {
    name.push_str(" Jr.");
    name
}
```

Nach dem Aufruf von `add_suffix` zeigt `first` auf freigegebenen Speicher. `first` in `println!` zu lesen, wäre daher eine Verletzung der Speichersicherheit (undefiniertes Verhalten). Denk daran: Dass `first` auf freigegebenen Speicher zeigt, ist kein Problem. Das Problem ist, dass wir versucht haben, `first` zu _verwenden_, nachdem es ungültig geworden ist.

Zum Glück weigert sich Rust, dieses Programm zu kompilieren, und gibt folgenden Fehler aus:

```text
error[E0382]: borrow of moved value: `first`
 --> test.rs:4:35
  |
2 |     let first = String::from("Ferris");
  |         ----- move occurs because `first` has type `String`, which does not implement the `Copy` trait
3 |     let full = add_suffix(first);
  |                           ----- value moved here
4 |     println!("{full}, originally {first}"); // first is now used here
  |                                   ^^^^^ value borrowed here after move
```

Gehen wir die Schritte dieses Fehlers durch. Rust sagt, dass `first` verschoben wird, als wir in Zeile 3 `add_suffix(first)` aufgerufen haben. Der Fehler stellt klar, dass `first` verschoben wird, weil es den Typ `String` hat, der `Copy` nicht implementiert. Wir besprechen `Copy` bald – kurz gesagt würdest du diesen Fehler nicht bekommen, wenn du statt `String` einen `i32` verwenden würdest. Schließlich sagt der Fehler, dass wir `first` nach dem Move verwenden (es wird „ausgeliehen“, _borrowed_, was wir im nächsten Abschnitt besprechen).

Wenn du also eine Variable verschiebst, hindert Rust dich daran, diese Variable später zu verwenden. Allgemeiner gesagt setzt der Compiler dieses Prinzip durch:

> **Prinzip der verschobenen Heap-Daten** (_Moved heap data principle_): Wenn eine Variable `x` die Ownership von Heap-Daten an eine andere Variable `y` verschiebt, kann `x` nach dem Move nicht mehr verwendet werden.

Jetzt solltest du allmählich den Zusammenhang zwischen Ownership, Moves und Sicherheit erkennen. Das Verschieben der Ownership von Heap-Daten vermeidet undefiniertes Verhalten durch das Lesen freigegebenen Speichers.

### Klonen vermeidet Moves {#cloning-avoids-moves}

Eine Möglichkeit, das Verschieben von Daten zu vermeiden, ist, sie mit der Methode `.clone()` zu _klonen_. Wir können das Sicherheitsproblem im vorherigen Programm zum Beispiel mit einem Klon beheben:

```aquascope,interpreter
fn main() {
    let first = String::from("Ferris");
    let first_clone = first.clone();`[]`
    let full = add_suffix(first_clone);`[]`
    println!("{full}, originally {first}");
}

fn add_suffix(mut name: String) -> String {
    name.push_str(" Jr.");
    name
}
```

Beachte, dass `first_clone` bei L1 nicht „flach“ den Zeiger in `first` kopiert hat, sondern die String-Daten „tief“ in eine neue Heap-Allokation kopiert hat. Während `first_clone` bei L2 von `add_suffix` verschoben und ungültig gemacht wurde, ist die ursprüngliche Variable `first` deshalb unverändert. `first` kann gefahrlos weiterverwendet werden.

{{#quiz ../quizzes/ch04-01-ownership-sec2-moves.toml}}

### Zusammenfassung {#summary}

Ownership ist in erster Linie eine Disziplin der Heap-Verwaltung:[^pointer-management]

- Alle Heap-Daten müssen genau einer Variable gehören.
- Rust gibt Heap-Daten frei, sobald ihr Owner seinen Gültigkeitsbereich verlässt.
- Ownership kann durch Moves übertragen werden, die bei Zuweisungen und Funktionsaufrufen stattfinden.
- Auf Heap-Daten kann nur über ihren aktuellen Owner zugegriffen werden, nicht über einen früheren Owner.

Wir haben nicht nur betont, _wie_ die Schutzmechanismen von Rust funktionieren, sondern auch, _warum_ sie undefiniertes Verhalten vermeiden. Wenn du vom Rust-Compiler eine Fehlermeldung bekommst, ist es leicht, frustriert zu sein, wenn du nicht verstehst, warum Rust sich beschwert. Diese konzeptionellen Grundlagen sollten dir helfen, die Fehlermeldungen von Rust zu deuten. Sie sollten dir außerdem helfen, APIs zu entwerfen, die besser zu Rust passen.

[^boxed-data-structures]: Diese Datenstrukturen verwenden nicht wörtlich den Typ `Box`. `String` ist zum Beispiel mit `Vec` implementiert, und `Vec` mit [`RawVec`](https://doc.rust-lang.org/nomicon/vec/vec-raw.html) statt mit `Box`. Typen wie `RawVec` sind aber trotzdem boxähnlich: Sie besitzen Speicher auf dem Heap.

[^pointer-management]: In einem anderen Sinn ist Ownership eine Disziplin der _Zeiger_-Verwaltung. Wir haben aber noch nicht beschrieben, wie man Zeiger auf etwas anderes als den Heap erzeugt. Dazu kommen wir im nächsten Abschnitt.

[`NameError`]: https://docs.python.org/3/library/exceptions.html#NameError
[`ReferenceError`]: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/ReferenceError
