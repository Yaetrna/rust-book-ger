## Referenzen und Borrowing {#references-and-borrowing}

Ownership, Boxen und Moves bilden eine Grundlage, um sicher mit dem Heap zu programmieren. APIs, die nur mit Moves arbeiten, können allerdings umständlich zu benutzen sein. Angenommen, du möchtest zum Beispiel ein paar Strings zweimal lesen:

```aquascope,interpreter,shouldFail,horizontal
fn main() {
    let m1 = String::from("Hello");
    let m2 = String::from("world");
    greet(m1, m2);`[]`
    let s = format!("{} {}", m1, m2);`[]` // Error: m1 and m2 are moved
}

fn greet(g1: String, g2: String) {
    println!("{} {}!", g1, g2);`[]`
}
```

In diesem Beispiel verschiebt (_moves_) der Aufruf von `greet` die Daten aus `m1` und `m2` in die Parameter von `greet`. Beide Strings werden am Ende von `greet` verworfen (_dropped_) und können deshalb in `main` nicht mehr verwendet werden. Würden wir sie trotzdem lesen, wie in der Operation `format!(..)`, wäre das undefiniertes Verhalten. Der Rust-Compiler weist dieses Programm deshalb mit demselben Fehler zurück, den wir im letzten Abschnitt gesehen haben:

```text
error[E0382]: borrow of moved value: `m1`
 --> test.rs:5:30
 (...rest of the error...)
```

Dieses Move-Verhalten ist äußerst unpraktisch. Programme müssen einen String oft mehr als einmal verwenden. Eine alternative Version von `greet` könnte die Ownership der Strings zurückgeben, etwa so:

```aquascope,interpreter,horizontal
fn main() {
    let m1 = String::from("Hello");
    let m2 = String::from("world");`[]`
    let (m1_again, m2_again) = greet(m1, m2);
    let s = format!("{} {}", m1_again, m2_again);`[]`
}

fn greet(g1: String, g2: String) -> (String, String) {
    println!("{} {}!", g1, g2);
    (g1, g2)
}
```

Dieser Programmierstil ist allerdings recht langatmig. Mit Referenzen bietet Rust eine knappe Möglichkeit, Daten ohne Moves zu lesen und zu schreiben.

### Referenzen sind nicht-besitzende Zeiger {#references-are-non-owning-pointers}

Eine **Referenz** ist eine Art Zeiger. Hier ist ein Beispiel für eine Referenz, mit der wir unser `greet`-Programm bequemer schreiben können:

```aquascope,interpreter,horizontal
fn main() {
    let m1 = String::from("Hello");
    let m2 = String::from("world");`[]`
    greet(&m1, &m2);`[]` // note the ampersands
    let s = format!("{} {}", m1, m2);
}

fn greet(g1: &String, g2: &String) { // note the ampersands
    `[]`println!("{} {}!", g1, g2);
}
```

Der Ausdruck `&m1` verwendet den Ampersand-Operator, um `m1` „auszuleihen“ (_borrow_), also eine Referenz darauf zu erzeugen. Der Typ des `greet`-Parameters `g1` wird zu `&String` geändert, was „eine Referenz auf einen `String`“ bedeutet.

<!-- At runtime, the references look like this:

<img src="img/experiment/ch04-02-stack1.jpg" class="center" width="350" /> -->

Beachte bei L2, dass es von `g1` bis zum String „Hello“ zwei Schritte sind. `g1` ist eine Referenz, die auf `m1` auf dem Stack zeigt, und `m1` ist ein String mit einer Box, die auf „Hello“ auf dem Heap zeigt.

Während `m1` die Heap-Daten „Hello“ besitzt, besitzt `g1` _weder_ `m1` noch „Hello“. Nachdem `greet` beendet ist und das Programm L3 erreicht, wurden deshalb keine Heap-Daten freigegeben. Nur der Stack-Frame von `greet` verschwindet. Das passt zu unserem _Prinzip der Box-Freigabe_. Weil `g1` „Hello“ nicht besessen hat, hat Rust „Hello“ nicht im Namen von `g1` freigegeben.

Referenzen sind **nicht-besitzende Zeiger**, weil sie die Daten, auf die sie zeigen, nicht besitzen.

### Das Dereferenzieren eines Zeigers greift auf seine Daten zu {#dereferencing-a-pointer-accesses-its-data}

Die bisherigen Beispiele mit Boxen und Strings haben nicht gezeigt, wie Rust einem Zeiger zu seinen Daten „folgt“. So hat etwa das Makro `println!` auf rätselhafte Weise sowohl mit Strings vom Typ `String` funktioniert, die ihre Daten besitzen, als auch mit String-Referenzen vom Typ `&String`. Der zugrunde liegende Mechanismus ist der **Dereferenzierungsoperator**, der mit einem Sternchen (`*`) geschrieben wird. Hier ist zum Beispiel ein Programm, das Dereferenzierungen auf verschiedene Arten verwendet:

```aquascope,interpreter
# fn main() {
let mut x: Box<i32> = Box::new(1);
let a: i32 = *x;         // *x reads the heap value, so a = 1
*x += 1;                 // *x on the left-side modifies the heap value,
                         //     so x points to the value 2

let r1: &Box<i32> = &x;  // r1 points to x on the stack
let b: i32 = **r1;       // two dereferences get us to the heap value

let r2: &i32 = &*x;      // r2 points to the heap value directly
let c: i32 = *r2;`[]`    // so only one dereference is needed to read it
# }
```

Beachte den Unterschied zwischen `r1`, das auf `x` auf dem Stack zeigt, und `r2`, das auf den Heap-Wert `2` zeigt.

Beim Lesen von Rust-Code wirst du den Dereferenzierungsoperator vermutlich nicht sehr oft sehen. Rust fügt Dereferenzierungen und Referenzen in bestimmten Fällen implizit ein, etwa wenn du eine Methode mit dem Punktoperator aufrufst. Dieses Programm zeigt zum Beispiel zwei gleichwertige Arten, die Funktionen [`i32::abs`](https://doc.rust-lang.org/std/primitive.i32.html#method.abs) (Absolutwert) und [`str::len`](https://doc.rust-lang.org/std/primitive.str.html#method.len) (Länge eines Strings) aufzurufen:

```rust,ignore
# fn main()  {
let x: Box<i32> = Box::new(-1);
let x_abs1 = i32::abs(*x); // explicit dereference
let x_abs2 = x.abs();      // implicit dereference
assert_eq!(x_abs1, x_abs2);

let r: &Box<i32> = &x;
let r_abs1 = i32::abs(**r); // explicit dereference (twice)
let r_abs2 = r.abs();       // implicit dereference (twice)
assert_eq!(r_abs1, r_abs2);

let s = String::from("Hello");
let s_len1 = str::len(&s); // explicit reference
let s_len2 = s.len();      // implicit reference
assert_eq!(s_len1, s_len2);
# }
```

Dieses Beispiel zeigt implizite Umwandlungen auf drei Arten:

1. Die Funktion `i32::abs` erwartet eine Eingabe vom Typ `i32`. Um `abs` mit einer `Box<i32>` aufzurufen, kannst du die Box explizit dereferenzieren, etwa mit `i32::abs(*x)`. Du kannst die Box aber auch implizit dereferenzieren, indem du die Syntax für Methodenaufrufe verwendest, etwa `x.abs()`. Die Punktsyntax ist syntaktischer Zucker für die Syntax von Funktionsaufrufen.

2. Diese implizite Umwandlung funktioniert über mehrere Zeigerebenen hinweg. Rufst du `abs` zum Beispiel auf einer Referenz auf eine Box `r: &Box<i32>` auf, fügt Rust zwei Dereferenzierungen ein.

3. Diese Umwandlung funktioniert auch in die umgekehrte Richtung. Die Funktion `str::len` erwartet eine Referenz `&str`. Wenn du `len` auf einem `String` aufrufst, der seine Daten besitzt, fügt Rust einen einzelnen Borrow-Operator ein. (Tatsächlich findet sogar noch eine weitere Umwandlung von `String` zu `str` statt!)

Auf Methodenaufrufe und implizite Umwandlungen gehen wir in späteren Kapiteln genauer ein. Wichtig ist vorerst nur, dass diese Umwandlungen bei Methodenaufrufen und einigen Makros wie `println` stattfinden. Wir wollen die ganze „Magie“ von Rust entzaubern, damit du ein klares mentales Modell davon bekommst, wie Rust funktioniert.

{{#quiz ../quizzes/ch04-02-references-sec1-basics.toml}}

### Rust vermeidet gleichzeitiges Aliasing und Verändern {#rust-avoids-simultaneous-aliasing-and-mutation}

Zeiger sind ein mächtiges und gefährliches Feature, weil sie **Aliasing** ermöglichen. Aliasing bedeutet, über verschiedene Variablen auf dieselben Daten zuzugreifen. Für sich genommen ist Aliasing harmlos. Kombiniert mit **Veränderung** (_mutation_) haben wir aber ein Rezept für eine Katastrophe. Eine Variable kann einer anderen auf viele Arten „den Boden unter den Füßen wegziehen“, zum Beispiel:

- Indem sie die gemeinsam genutzten Daten freigibt, sodass die andere Variable auf freigegebenen Speicher zeigt.
- Indem sie die gemeinsam genutzten Daten verändert und so Laufzeiteigenschaften ungültig macht, auf die sich die andere Variable verlässt.
- Indem sie die gemeinsam genutzten Daten _nebenläufig_ verändert und so ein Data-Race verursacht, das für die andere Variable zu nichtdeterministischem Verhalten führt.

Als durchgehendes Beispiel betrachten wir Programme, die die Datenstruktur Vektor verwenden, also [`Vec`]. Anders als Arrays, die eine feste Länge haben, haben Vektoren eine variable Länge, weil sie ihre Elemente auf dem Heap speichern. [`Vec::push`] fügt zum Beispiel ein Element am Ende eines Vektors hinzu, etwa so:

```aquascope,interpreter,horizontal
#fn main() {
let mut v: Vec<i32> = vec![1, 2, 3];`[]`
v.push(4);`[]`
#}
```

Das Makro `vec!` erzeugt einen Vektor mit den Elementen zwischen den eckigen Klammern. Der Vektor `v` hat den Typ `Vec<i32>`. Die Syntax `<i32>` bedeutet, dass die Elemente des Vektors den Typ `i32` haben.

Ein wichtiges Implementierungsdetail ist, dass `v` auf dem Heap ein Array mit einer bestimmten _Kapazität_ alloziert. Wir können einen Blick in das Innere von `Vec` werfen und uns dieses Detail selbst ansehen:

```aquascope,interpreter,horizontal,concreteTypes
#fn main() {
let mut v: Vec<i32> = vec![1, 2, 3];`[]`
#}
```

> _Hinweis:_ Klicke auf das Fernglas-Symbol oben rechts im Diagramm, um in jedem Laufzeitdiagramm diese Detailansicht ein- und auszuschalten.

Beachte, dass der Vektor eine Länge (`len`) von 3 und eine Kapazität (`cap`) von 3 hat. Der Vektor ist also voll. Wenn wir ein `push` ausführen, muss der Vektor deshalb eine neue Allokation mit größerer Kapazität anlegen, alle Elemente dorthin kopieren und das ursprüngliche Array auf dem Heap freigeben. Im Diagramm oben liegt das Array `1 2 3 4` an einer (möglicherweise) anderen Speicherstelle als das ursprüngliche Array `1 2 3`.

Um den Bogen zurück zur Speichersicherheit zu schlagen, bringen wir nun Referenzen ins Spiel. Angenommen, wir erzeugen eine Referenz auf die Heap-Daten eines Vektors. Dann kann ein Push diese Referenz ungültig machen, wie unten simuliert:

```aquascope,interpreter,shouldFail,horizontal
#fn main() {
let mut v: Vec<i32> = vec![1, 2, 3];
let num: &i32 = &v[2];`[]`
v.push(4);`[]`
println!("Third element is {}", *num);`[]`
#}
```

Anfangs zeigt `v` auf ein Array mit 3 Elementen auf dem Heap. Dann wird `num` als Referenz auf das dritte Element erzeugt, wie bei L1 zu sehen. Die Operation `v.push(4)` ändert jedoch die Größe von `v`. Dabei wird das bisherige Array freigegeben und ein neues, größeres Array alloziert. `num` zeigt danach auf ungültigen Speicher. Bei L3 liest die Dereferenzierung `*num` deshalb ungültigen Speicher, was zu undefiniertem Verhalten führt.

Abstrakter formuliert besteht das Problem darin, dass der Vektor `v` sowohl einen Alias hat (die Referenz `num`) als auch verändert wird (durch die Operation `v.push(4)`). Um solche Probleme zu vermeiden, folgt Rust deshalb einem grundlegenden Prinzip:

> **Prinzip der Zeigersicherheit** (_Pointer Safety Principle_): Daten sollten niemals gleichzeitig einen Alias haben und verändert werden.

Daten dürfen einen Alias haben. Daten dürfen verändert werden. Aber Daten dürfen nicht _gleichzeitig_ einen Alias haben _und_ verändert werden. Bei Boxen (besitzenden Zeigern) setzt Rust dieses Prinzip zum Beispiel durch, indem es Aliasing verbietet. Wird eine Box von einer Variable einer anderen zugewiesen, wird die Ownership verschoben und die vorherige Variable ungültig. Auf Daten, die einen Owner haben, kann man nur über diesen Owner zugreifen – Aliasse gibt es nicht.

Weil Referenzen jedoch nicht-besitzende Zeiger sind, brauchen sie andere Regeln als Boxen, um das _Prinzip der Zeigersicherheit_ einzuhalten. Referenzen sind ja gerade dafür gedacht, vorübergehend Aliasse zu erzeugen. Im restlichen Abschnitt erklären wir die Grundlagen, wie Rust mit dem **Borrow-Checker** die Sicherheit von Referenzen gewährleistet.

### Referenzen ändern Berechtigungen auf Places {#references-change-permissions-on-places}

Die Kernidee des Borrow-Checkers ist, dass Variablen drei Arten von **Berechtigungen** auf ihre Daten haben:

- **Read** (@Perm{read}, lesen): Die Daten können an eine andere Stelle kopiert werden.
- **Write** (@Perm{write}, schreiben): Die Daten können verändert werden.
- **Own** (@Perm{own}, besitzen): Die Daten können verschoben oder verworfen werden.

Diese Berechtigungen existieren nicht zur Laufzeit, sondern nur im Compiler. Sie beschreiben, wie der Compiler über dein Programm „denkt“, bevor es ausgeführt wird.

Standardmäßig hat eine Variable die Berechtigungen Read und Own (@Perm{read}@Perm{own}) auf ihre Daten. Ist eine Variable mit `let mut` annotiert, hat sie zusätzlich die Write-Berechtigung (@Perm{write}). Die entscheidende Idee ist,
dass **Referenzen diese Berechtigungen vorübergehend entziehen können.**

Um diese Idee zu veranschaulichen, sehen wir uns die Berechtigungen in einer Variante des obigen Programms an, die tatsächlich sicher ist. Das `push` steht jetzt hinter dem `println!`. Die Berechtigungen in diesem Programm werden mit einer neuen Art von Diagramm dargestellt. Das Diagramm zeigt für jede Zeile, wie sich die Berechtigungen ändern.

```aquascope,permissions,stepper
#fn main() {
let mut v: Vec<i32> = vec![1, 2, 3];
let num: &i32 = &v[2];
println!("Third element is {}", *num);
v.push(4);
#}
```

Gehen wir die Zeilen einzeln durch:

1. Nach `let mut v = (...)` ist die Variable `v` initialisiert (angezeigt durch <i class="fa fa-arrow-turn-up"></i>). Sie erhält die Berechtigungen @Perm[gained]{read}@Perm[gained]{write}@Perm[gained]{own} (das Pluszeichen zeigt einen Gewinn an).
2. Nach `let num = &v[2]` wurden die Daten in `v` von `num` **ausgeliehen** (angezeigt durch <i class="fa fa-arrow-right"></i>). Dabei passieren drei Dinge:
   - Der Borrow entzieht `v` die Berechtigungen @Perm[lost]{write}@Perm[lost]{own} (der Schrägstrich zeigt einen Verlust an). `v` kann weder beschrieben noch besessen, aber weiterhin gelesen werden.
   - Die Variable `num` hat die Berechtigungen @Perm{read}@Perm{own} erhalten. `num` ist nicht beschreibbar (die fehlende Berechtigung @Perm{write} wird als Strich <span class="perm write">‒</span> dargestellt), weil es nicht mit `let mut` gekennzeichnet wurde.
   - Der **Place** `*num` hat die Berechtigung @Perm{read} erhalten.
3. Nach `println!(...)` ist `num` nicht mehr in Gebrauch, also ist `v` nicht mehr ausgeliehen. Deshalb gilt:
   - `v` erhält seine Berechtigungen @Perm{write}@Perm{own} zurück (angezeigt durch <i class="fa fa-rotate-left"></i>).
   - `num` und `*num` haben alle ihre Berechtigungen verloren (angezeigt durch <i class="fa fa-arrow-turn-down"></i>).
4. Nach `v.push(4)` ist `v` nicht mehr in Gebrauch und verliert alle seine Berechtigungen.

Sehen wir uns als Nächstes ein paar Feinheiten des Diagramms an. Erstens: Warum siehst du sowohl `num` als auch `*num`? Weil der Zugriff auf Daten über eine Referenz nicht dasselbe ist wie das Verändern der Referenz selbst. Angenommen, wir deklarieren zum Beispiel eine Referenz auf eine Zahl mit `let mut`:

```aquascope,permissions,stepper
#fn main() {
let x = 0;
let mut x_ref = &x;
# println!("{x_ref} {x}");
#}
```

Beachte, dass `x_ref` die Berechtigung @Perm{write} hat, `*x_ref` aber nicht. Das heißt, wir können der Variable `x_ref` eine andere Referenz zuweisen (z. B. `x_ref = &y`), aber wir können die Daten, auf die sie zeigt, nicht verändern (z. B. `*x_ref += 1`).

Allgemeiner gesagt sind Berechtigungen auf **Places** definiert und nicht nur auf Variablen. Ein Place ist alles, was du auf die linke Seite einer Zuweisung schreiben kannst. Zu den Places gehören:

- Variablen, wie `a`.
- Dereferenzierungen von Places, wie `*a`.
- Array-Zugriffe auf Places, wie `a[0]`.
- Felder von Places, wie `a.0` bei Tupeln oder `a.field` bei Structs (mehr dazu im nächsten Kapitel).
- Beliebige Kombinationen davon, wie `*((*a)[0].1)`.

Zweitens: Warum verlieren Places ihre Berechtigungen, wenn sie nicht mehr verwendet werden? Weil sich manche Berechtigungen gegenseitig ausschließen. Wenn du `num = &v[2]` schreibst, kann `v` nicht verändert oder verworfen werden, solange `num` in Gebrauch ist. Das heißt aber nicht, dass es ungültig wäre, `num` noch einmal zu verwenden. Fügen wir dem obigen Programm zum Beispiel ein weiteres `println!` hinzu, verliert `num` seine Berechtigungen einfach eine Zeile später:

```aquascope,permissions,stepper
#fn main() {
let mut v: Vec<i32> = vec![1, 2, 3];
let num: &i32 = &v[2];
println!("Third element is {}", *num);
println!("Again, the third element is {}", *num);
v.push(4);
#}
```

Problematisch wird es erst, wenn du versuchst, `num` _nach_ dem Verändern von `v` noch einmal zu verwenden. Sehen wir uns das genauer an.

### Der Borrow-Checker findet Berechtigungsverletzungen {#the-borrow-checker-finds-permission-violations}

Erinnere dich an das _Prinzip der Zeigersicherheit_: Daten sollten nicht gleichzeitig einen Alias haben und verändert werden. Diese Berechtigungen sollen sicherstellen, dass Daten nicht verändert werden können, solange sie einen Alias haben. Wenn du eine Referenz auf Daten erzeugst (sie also „ausleihst“), sind diese Daten vorübergehend schreibgeschützt, bis die Referenz nicht mehr in Gebrauch ist.

Rust verwendet diese Berechtigungen in seinem **Borrow-Checker**. Der Borrow-Checker sucht nach potenziell unsicheren Operationen mit Referenzen. Kehren wir zu dem unsicheren Programm von vorhin zurück, in dem `push` eine Referenz ungültig macht. Diesmal ergänzen wir das Berechtigungsdiagramm um einen weiteren Aspekt:

```aquascope,permissions,boundaries,stepper,shouldFail
#fn main() {
let mut v: Vec<i32> = vec![1, 2, 3];
let num: &i32 = &v[2];`{}`
v.push(4);`{}`
println!("Third element is {}", *num);
#}
```

Immer wenn ein Place verwendet wird, erwartet Rust je nach Operation bestimmte Berechtigungen für diesen Place. Der Borrow `&v[2]` setzt zum Beispiel voraus, dass `v` lesbar ist. Deshalb wird die Berechtigung @Perm{read} zwischen der Operation `&` und dem Place `v` angezeigt. Der Buchstabe ist ausgefüllt, weil `v` in dieser Zeile die Read-Berechtigung hat.

Die verändernde Operation `v.push(4)` setzt dagegen voraus, dass `v` lesbar und beschreibbar ist. Es werden sowohl @Perm{read} als auch @Perm{write} angezeigt. `v` hat jedoch keine Write-Berechtigung (es ist von `num` ausgeliehen). Deshalb ist der Buchstabe @Perm[missing]{write} hohl: Die Write-Berechtigung wird _erwartet_, aber `v` hat sie nicht.

Wenn du versuchst, dieses Programm zu kompilieren, gibt der Rust-Compiler folgenden Fehler aus:

```text
error[E0502]: cannot borrow `v` as mutable because it is also borrowed as immutable
 --> test.rs:4:1
  |
3 | let num: &i32 = &v[2];
  |                  - immutable borrow occurs here
4 | v.push(4);
  | ^^^^^^^^^ mutable borrow occurs here
5 | println!("Third element is {}", *num);
  |                                 ---- immutable borrow later used here
```

Die Fehlermeldung erklärt, dass `v` nicht verändert werden kann, solange die Referenz `num` in Gebrauch ist. Das ist der oberflächliche Grund – das eigentliche Problem ist, dass `num` durch `push` ungültig werden könnte. Rust erkennt diese mögliche Verletzung der Speichersicherheit.

### Veränderliche Referenzen bieten exklusiven, nicht-besitzenden Zugriff auf Daten {#mutable-references-provide-unique-and-non-owning-access-to-data}

Die Referenzen, die wir bisher gesehen haben, sind schreibgeschützte **unveränderliche Referenzen** (_immutable references_), auch **geteilte Referenzen** (_shared references_) genannt. Unveränderliche Referenzen erlauben Aliasing, verbieten aber Veränderungen. Es ist jedoch auch nützlich, vorübergehend schreibenden Zugriff auf Daten zu gewähren, ohne sie zu verschieben.

Der Mechanismus dafür sind **veränderliche Referenzen** (_mutable references_), auch **exklusive Referenzen** (_unique references_) genannt. Hier ist ein einfaches Beispiel für eine veränderliche Referenz mit den zugehörigen Änderungen der Berechtigungen:

```aquascope,permissions,stepper,boundaries
#fn main() {
let mut v: Vec<i32> = vec![1, 2, 3];
let num: &mut i32 = &mut v[2];
*num += 1;
println!("Third element is {}", *num);
println!("Vector is now {:?}", v);
#}
```

<blockquote><div style="margin-block-start: 1em; margin-block-end: 1em"><i>Hinweis:</i> Wenn die erwarteten Berechtigungen für ein Beispiel nicht unbedingt relevant sind, kürzen wir sie mit Punkten ab, etwa so: <div class="permission-stack stack-size-2"><div class="perm read"><div class="small">•</div><div class="big">R</div></div><div class="perm write"><div class="small">•</div><div class="big">W</div></div></div>. Bewege die Maus über die Kreise (oder tippe auf einem Touchscreen darauf), um die zugehörigen Berechtigungsbuchstaben zu sehen.</div></blockquote>

Eine veränderliche Referenz wird mit dem Operator `&mut` erzeugt. Der Typ von `num` wird als `&mut i32` geschrieben. Im Vergleich zu unveränderlichen Referenzen siehst du zwei wichtige Unterschiede bei den Berechtigungen:

1. Als `num` eine unveränderliche Referenz war, hatte `v` noch die Berechtigung @Perm{read}. Jetzt, da `num` eine veränderliche Referenz ist, hat `v` _alle_ Berechtigungen verloren, solange `num` in Gebrauch ist.
2. Als `num` eine unveränderliche Referenz war, hatte der Place `*num` nur die Berechtigung @Perm{read}. Jetzt, da `num` eine veränderliche Referenz ist, hat `*num` zusätzlich die Berechtigung @Perm{write} erhalten.

Die erste Beobachtung ist es, die veränderliche Referenzen _sicher_ macht. Veränderliche Referenzen erlauben Veränderungen, verhindern aber Aliasing. Der ausgeliehene Place `v` wird vorübergehend unbrauchbar und ist damit faktisch kein Alias.

Die zweite Beobachtung ist es, die veränderliche Referenzen _nützlich_ macht. `v[2]` kann über `*num` verändert werden. `*num += 1` verändert zum Beispiel `v[2]`. Beachte, dass `*num` die Berechtigung @Perm{write} hat, `num` aber nicht. `num` bezeichnet die veränderliche Referenz selbst, d. h., man kann `num` keine _andere_ veränderliche Referenz zuweisen.

Veränderliche Referenzen können auch vorübergehend zu schreibgeschützten Referenzen „herabgestuft“ werden. Zum Beispiel:

```aquascope,permissions,stepper,boundaries
#fn main() {
let mut v: Vec<i32> = vec![1, 2, 3];
let num: &mut i32 = &mut v[2];`(focus,paths:*num)`
let num2: &i32 = &*num;`(focus,paths:*num)`
println!("{} {}", *num, *num2);
#}
```

> _Hinweis:_ Wenn Änderungen der Berechtigungen für ein Beispiel nicht relevant sind, blenden wir sie aus. Ausgeblendete Schritte kannst du mit einem Klick auf „»“ anzeigen, ausgeblendete Berechtigungen innerhalb eines Schritts mit einem Klick auf „● ● ●“.

In diesem Programm entzieht der Borrow `&*num` dem Place `*num` die Berechtigung @Perm{write}, aber _nicht_ die Berechtigung @Perm{read}, sodass `println!(..)` sowohl `*num` als auch `*num2` lesen kann.

### Berechtigungen werden am Ende der Lifetime einer Referenz zurückgegeben {#permissions-are-returned-at-the-end-of-a-references-lifetime}

Wir haben oben gesagt, dass eine Referenz Berechtigungen ändert, solange sie „in Gebrauch“ ist. Die Formulierung „in Gebrauch“ beschreibt die **Lifetime** einer Referenz, also den Codebereich von ihrer Geburt (wo die Referenz erzeugt wird) bis zu ihrem Tod (der letzten Verwendung bzw. den letzten Verwendungen der Referenz).

In diesem Programm beginnt die Lifetime von `y` zum Beispiel mit `let y = &x` und endet mit `let z = *y`:

```aquascope,permissions,stepper,boundaries
#fn main() {
let mut x = 1;
let y = &x;`(focus,paths:x)`
let z = *y;`(focus,paths:x)`
x += z;
#}
```

Die Berechtigung @Perm{write} auf `x` geht an `x` zurück, nachdem die Lifetime von `y` geendet hat, wie wir es schon gesehen haben.

In den bisherigen Beispielen war eine Lifetime ein zusammenhängender Codebereich. Sobald Kontrollfluss ins Spiel kommt, ist das jedoch nicht unbedingt der Fall. Hier ist zum Beispiel eine Funktion, die das erste Zeichen in einem Vektor aus ASCII-Zeichen in einen Großbuchstaben umwandelt:

```aquascope,permissions,stepper,boundaries
fn ascii_capitalize(v: &mut Vec<char>) {
    let c = &v[0];`(focus,paths:*v)`
    if c.is_ascii_lowercase() {
        let up = c.to_ascii_uppercase();`(focus,paths:*v)`
        v[0] = up;
    } else {`(focus,paths:*v)`
        println!("Already capitalized: {:?}", v);
    }
}
```

Die Variable `c` hat in jedem Zweig der if-Anweisung eine andere Lifetime. Im then-Block wird `c` im Ausdruck `c.to_ascii_uppercase()` verwendet. Deshalb erhält `*v` die Berechtigung @Perm{write} erst nach dieser Zeile zurück.

Im else-Block wird `c` dagegen nicht verwendet. `*v` erhält die Berechtigung @Perm{write} sofort beim Betreten des else-Blocks zurück.

{{#quiz ../quizzes/ch04-02-references-sec2-perms.toml}}

### Daten müssen alle ihre Referenzen überleben {#data-must-outlive-all-of-its-references}

Als Teil des _Prinzips der Zeigersicherheit_ stellt der Borrow-Checker sicher, dass **Daten jede Referenz auf sie überleben müssen.** Rust setzt das auf zwei Arten durch. Die erste betrifft Referenzen, die innerhalb des Gültigkeitsbereichs (_scope_) einer einzelnen Funktion erzeugt und verworfen werden. Angenommen, wir versuchen zum Beispiel, einen String zu verwerfen, während wir noch eine Referenz darauf halten:

```aquascope,permissions,stepper,boundaries,shouldFail
#fn main() {
let s = String::from("Hello world");
let s_ref = &s;`(focus,rxpaths:s$)`
drop(s);`{}`
println!("{}", s_ref);
#}
```

Um solche Fehler zu erkennen, verwendet Rust die Berechtigungen, die wir bereits besprochen haben. Der Borrow `&s` entzieht `s` die Berechtigung @Perm{own}. `drop` erwartet jedoch die Berechtigung @Perm{own}, was zu einem Konflikt bei den Berechtigungen führt.

Entscheidend ist, dass Rust in diesem Beispiel weiß, wie lange `s_ref` lebt. Rust braucht aber einen anderen Mechanismus, um die Regel durchzusetzen, wenn es nicht weiß, wie lange eine Referenz lebt. Genauer gesagt: wenn Referenzen entweder Eingaben oder Ausgaben einer Funktion sind. Hier ist zum Beispiel eine sichere Funktion, die eine Referenz auf das erste Element eines Vektors zurückgibt:

```aquascope,permissions,boundaries,showFlows
fn first(strings: &Vec<String>) -> &String {
    let s_ref = &strings[0];
    s_ref`{}`
}
```

Dieser Codeausschnitt führt eine neue Art von Berechtigung ein, die Flow-Berechtigung @Perm{flow} („fließen“). Die Berechtigung @Perm{flow} wird immer dann erwartet, wenn ein Ausdruck eine Eingabereferenz verwendet (wie `&strings[0]`) oder eine Ausgabereferenz zurückgibt (wie `return s_ref`).

Anders als die Berechtigungen @Perm{read}@Perm{write}@Perm{own} ändert sich @Perm{flow} im Rumpf einer Funktion nicht. Eine Referenz hat die Berechtigung @Perm{flow}, wenn sie in einem bestimmten Ausdruck verwendet werden darf (also dorthin _fließen_ darf). Angenommen, wir ändern `first` zum Beispiel in eine neue Funktion `first_or`, die einen Parameter `default` hat:

```aquascope,permissions,boundaries,showFlows,shouldFail
fn first_or<'a, 'b, 'c>(strings: &'a Vec<String>, default: &'b String) -> &'c String {
    if strings.len() > 0 {
        &strings[0]`{}`
    } else {
        default`{}`
    }
}
```

Diese Funktion lässt sich nicht mehr kompilieren, weil den Ausdrücken `&strings[0]` und `default` die nötige Berechtigung @Perm{flow} fehlt, um zurückgegeben zu werden. Aber warum? Rust meldet folgenden Fehler:

```text
error[E0106]: missing lifetime specifier
 --> test.rs:1:57
  |
1 | fn first_or(strings: &Vec<String>, default: &String) -> &String {
  |                      ------------           -------     ^ expected named lifetime parameter
  |
  = help: this function's return type contains a borrowed value, but the signature does not say whether it is borrowed from `strings` or `default`
```

Die Meldung „missing lifetime specifier“ (fehlende Lifetime-Angabe) ist etwas rätselhaft, aber die Hilfemeldung liefert nützlichen Kontext. Wenn Rust _nur_ die Funktionssignatur betrachtet, weiß es nicht, ob die Ausgabe `&String` eine Referenz auf `strings` oder auf `default` ist. Um zu verstehen, warum das wichtig ist, nehmen wir an, wir würden `first_or` so verwenden:

```rust,ignore
fn main() {
    let strings = vec![];
    let default = String::from("default");
    let s = first_or(&strings, &default);
    drop(default);
    println!("{}", s);
}
```

Dieses Programm ist unsicher, wenn `first_or` zulässt, dass `default` in den Rückgabewert _fließt_. Wie im vorherigen Beispiel könnte `drop` die Referenz `s` ungültig machen. Rust würde dieses Programm nur dann kompilieren lassen, wenn es _sicher_ wüsste, dass `default` nicht in den Rückgabewert fließen kann.

Um festzulegen, ob `default` zurückgegeben werden darf, bietet Rust einen Mechanismus namens _Lifetime-Parameter_. Diesen Mechanismus erklären wir später in Kapitel 10.3, [„Referenzen mit Lifetimes validieren“](ch10-03-lifetime-syntax.html). Vorerst genügt es zu wissen, dass (1) Eingabe- und Ausgabereferenzen anders behandelt werden als Referenzen innerhalb eines Funktionsrumpfs und (2) Rust einen anderen Mechanismus, nämlich die Berechtigung @Perm{flow}, verwendet, um die Sicherheit dieser Referenzen zu prüfen.

Um die Berechtigung @Perm{flow} in einem anderen Zusammenhang zu sehen, nehmen wir an, du versuchst, eine Referenz auf eine Variable auf dem Stack zurückzugeben, etwa so:

```aquascope,permissions,boundaries,showFlows,shouldFail
fn return_a_string() -> &String {
    let s = String::from("Hello world");
    let s_ref = &s;
    s_ref`{}`
}
```

Dieses Programm ist unsicher, weil die Referenz `&s` ungültig wird, sobald `return_a_string` zurückkehrt. Rust weist dieses Programm mit einem ähnlichen Fehler `missing lifetime specifier` zurück. Jetzt verstehst du, was dieser Fehler bedeutet: Für `s_ref` fehlen die passenden Flow-Berechtigungen.

{{#quiz ../quizzes/ch04-02-references-sec3-safety.toml}}

### Zusammenfassung {#summary}

Referenzen ermöglichen es, Daten zu lesen und zu schreiben, ohne ihre Ownership zu verbrauchen. Referenzen werden mit Borrows (`&` und `&mut`) erzeugt und mit Dereferenzierungen (`*`) verwendet, oft implizit.

Referenzen lassen sich allerdings leicht falsch verwenden. Der Borrow-Checker von Rust setzt ein System von Berechtigungen durch, das sicherstellt, dass Referenzen sicher verwendet werden:

- Alle Variablen können ihre Daten lesen, besitzen und (optional) schreiben.
- Das Erzeugen einer Referenz überträgt Berechtigungen vom ausgeliehenen Place auf die Referenz.
- Die Berechtigungen werden zurückgegeben, sobald die Lifetime der Referenz geendet hat.
- Daten müssen alle Referenzen überleben, die auf sie zeigen.

In diesem Abschnitt hattest du vermutlich das Gefühl, dass wir mehr darüber gesprochen haben, was Rust _nicht_ kann, als darüber, was Rust _kann_. Das ist Absicht! Eine der zentralen Stärken von Rust ist, dass du Zeiger ohne Garbage-Collection verwenden kannst und dabei trotzdem undefiniertes Verhalten vermeidest. Wenn du diese Sicherheitsregeln jetzt verstehst, ersparst du dir später Frust mit dem Compiler.

[`String::push_str`]: https://doc.rust-lang.org/std/string/struct.String.html#method.push_str
[`Vec`]: https://doc.rust-lang.org/std/vec/struct.Vec.html
[`Vec::push`]: https://doc.rust-lang.org/std/vec/struct.Vec.html#method.push
