## Ownership-Fehler beheben {#fixing-ownership-errors}

Zu lernen, wie man einen Ownership-Fehler behebt, ist eine zentrale Fähigkeit in Rust. Wenn der Borrow-Checker deinen Code zurückweist, wie solltest du reagieren? In diesem Abschnitt besprechen wir mehrere Fallstudien zu häufigen Ownership-Fehlern. Jede Fallstudie stellt eine Funktion vor, die der Compiler zurückweist. Dann erklären wir, warum Rust die Funktion zurückweist, und zeigen mehrere Möglichkeiten, sie zu reparieren.

Ein wiederkehrendes Thema wird sein, zu verstehen, ob eine Funktion _tatsächlich_ sicher oder unsicher ist. Rust weist ein unsicheres Programm immer zurück[^safe-subset]. Manchmal weist Rust aber auch ein sicheres Programm zurück. Diese Fallstudien zeigen, wie du in beiden Situationen auf Fehler reagierst.

<!-- The last two sections have shown how a Rust program can be **unsafe** if it triggers undefined behavior. The ownership guarantee is that Rust will reject all unsafe programs. However, Rust will also reject *some* safe programs. Fixing an ownership error will depend on whether your program is *actually* safe or unsafe. -->

### Ein unsicheres Programm reparieren: Eine Referenz auf den Stack zurückgeben {#fixing-an-unsafe-program-returning-a-reference-to-the-stack}

In unserer ersten Fallstudie geht es darum, eine Referenz auf den Stack zurückzugeben, genau wie wir es im letzten Abschnitt in [„Daten müssen alle ihre Referenzen überleben“](ch04-02-references-and-borrowing.html#data-must-outlive-all-of-its-references) besprochen haben. Hier ist die Funktion, die wir uns angesehen haben:

```rust,ignore,does_not_compile
fn return_a_string() -> &String {
    let s = String::from("Hello world");
    &s
}
```

Wenn wir überlegen, wie wir diese Funktion reparieren, müssen wir fragen: **Warum ist dieses Programm unsicher?** Hier liegt das Problem bei der Lifetime der referenzierten Daten. Wenn du eine Referenz auf einen String herumreichen willst, musst du sicherstellen, dass der zugrunde liegende String lange genug lebt.

Je nach Situation gibt es vier Möglichkeiten, die Lifetime des Strings zu verlängern. Eine ist, die Ownership des Strings aus der Funktion heraus zu verschieben (_move_), indem man `&String` in `String` ändert:

```rust
fn return_a_string() -> String {
    let s = String::from("Hello world");
    s
}
```

Eine andere Möglichkeit ist, ein String-Literal zurückzugeben, das ewig lebt (angezeigt durch `'static`). Diese Lösung passt, wenn wir den String nie ändern wollen; dann ist eine Heap-Allokation unnötig:

```rust
fn return_a_string() -> &'static str {
    "Hello world"    
}
```

Eine weitere Möglichkeit ist, die Borrow-Prüfung mithilfe von Garbage-Collection auf die Laufzeit zu verschieben. Du kannst zum Beispiel einen [Zeiger mit Referenzzählung][rc] verwenden:

```rust
use std::rc::Rc;
fn return_a_string() -> Rc<String> {
    let s = Rc::new(String::from("Hello world"));
    Rc::clone(&s)
}
```

Referenzzählung besprechen wir genauer in Kapitel 15.4, [„`Rc<T>`, der Smart-Pointer mit Referenzzählung“](ch15-04-rc.html). Kurz gesagt klont `Rc::clone` nur einen Zeiger auf `s` und nicht die Daten selbst. Zur Laufzeit prüft das `Rc`, wann das letzte `Rc`, das auf die Daten zeigt, verworfen (_dropped_) wurde, und gibt die Daten dann frei.

Noch eine Möglichkeit ist, dass die aufrufende Stelle über eine veränderliche (_mutable_) Referenz einen „Platz“ bereitstellt, in den der String gelegt wird:

```rust
fn return_a_string(output: &mut String) {
    output.replace_range(.., "Hello world");
}
```

Bei dieser Strategie ist die aufrufende Stelle dafür verantwortlich, Platz für den String zu schaffen. Dieser Stil kann umständlich sein, aber er kann auch speichereffizienter sein, wenn die aufrufende Stelle genau steuern muss, wann Allokationen stattfinden.

Welche Strategie am besten passt, hängt von deiner Anwendung ab. Der entscheidende Gedanke ist aber, das eigentliche Problem hinter dem oberflächlichen Ownership-Fehler zu erkennen. Wie lange soll mein String leben? Wer soll dafür zuständig sein, ihn freizugeben? Sobald du diese Fragen klar beantworten kannst, musst du nur noch deine API entsprechend anpassen.

### Ein unsicheres Programm reparieren: Nicht genug Berechtigungen {#fixing-an-unsafe-program-not-enough-permissions}

Ein weiteres häufiges Problem ist der Versuch, schreibgeschützte Daten zu verändern oder Daten hinter einer Referenz zu verwerfen. Angenommen, wir versuchen, eine Funktion `stringify_name_with_title` zu schreiben. Diese Funktion soll aus einem Vektor von Namensbestandteilen den vollständigen Namen einer Person erzeugen, einschließlich eines zusätzlichen Titels.

```aquascope,permissions,stepper,boundaries,shouldFail
fn stringify_name_with_title(name: &Vec<String>) -> String {
    name.push(String::from("Esq."));`{}`
    let full = name.join(" ");
    full
}

// ideally: ["Ferris", "Jr."] => "Ferris Jr. Esq."
```

Dieses Programm wird vom Borrow-Checker zurückgewiesen, weil `name` eine unveränderliche (_immutable_) Referenz ist, `name.push(..)` aber die Berechtigung @Perm{write} benötigt. Dieses Programm ist unsicher, weil `push` andere Referenzen auf `name` außerhalb von `stringify_name_with_title` ungültig machen könnte, etwa so:

```aquascope,interpreter,shouldFail,horizontal
#fn stringify_name_with_title(name: &Vec<String>) -> String {
#    name.push(String::from("Esq."));
#    let full = name.join(" ");
#    full
#}
fn main() {
    let name = vec![String::from("Ferris")];
    let first = &name[0];`[]`
    stringify_name_with_title(&name);`[]`
    println!("{}", first);`[]`
}
```

In diesem Beispiel wird vor dem Aufruf von `stringify_name_with_title` eine Referenz `first` auf `name[0]` erzeugt. Die Funktion `name.push(..)` alloziert den Inhalt von `name` neu, was `first` ungültig macht, sodass das `println` freigegebenen Speicher liest.

Wie reparieren wir also diese API? Eine naheliegende Lösung ist, den Typ von `name` von `&Vec<String>` in `&mut Vec<String>` zu ändern:

```rust,ignore
fn stringify_name_with_title(name: &mut Vec<String>) -> String {
    name.push(String::from("Esq."));
    let full = name.join(" ");
    full
}
```

Das ist aber keine gute Lösung! **Funktionen sollten ihre Eingaben nicht verändern, wenn die aufrufende Stelle das nicht erwarten würde.** Wer `stringify_name_with_title` aufruft, erwartet vermutlich nicht, dass diese Funktion den eigenen Vektor verändert. Bei einer anderen Funktion wie `add_title_to_name` würde man vielleicht erwarten, dass sie ihre Eingabe verändert, aber nicht bei unserer Funktion.

Eine andere Option ist, die Ownership des Namens zu übernehmen, indem man `&Vec<String>` in `Vec<String>` ändert:

```rust,ignore
fn stringify_name_with_title(mut name: Vec<String>) -> String {
    name.push(String::from("Esq."));
    let full = name.join(" ");
    full
}
```

Aber auch das ist keine gute Lösung! **Es ist sehr selten, dass Rust-Funktionen die Ownership von Datenstrukturen übernehmen, die Heap-Daten besitzen, wie `Vec` und `String`.** Diese Version von `stringify_name_with_title` würde die Eingabe `name` unbrauchbar machen, was für die aufrufende Stelle sehr ärgerlich ist, wie wir am Anfang von [„Referenzen und Borrowing“](ch04-02-references-and-borrowing.html) besprochen haben.

Die Wahl von `&Vec` ist also eigentlich eine gute, die wir _nicht_ ändern wollen. Stattdessen können wir den Rumpf der Funktion ändern. Es gibt viele mögliche Lösungen, die sich darin unterscheiden, wie viel Speicher sie verbrauchen. Eine Möglichkeit ist, die Eingabe `name` zu klonen:

```rust,ignore
fn stringify_name_with_title(name: &Vec<String>) -> String {
    let mut name_clone = name.clone();
    name_clone.push(String::from("Esq."));
    let full = name_clone.join(" ");
    full
}
```

Indem wir `name` klonen, dürfen wir die lokale Kopie des Vektors verändern. Der Klon kopiert allerdings jeden String in der Eingabe. Unnötige Kopien können wir vermeiden, indem wir den Zusatz erst später anhängen:

```rust,ignore
fn stringify_name_with_title(name: &Vec<String>) -> String {
    let mut full = name.join(" ");
    full.push_str(" Esq.");
    full
}
```

Diese Lösung funktioniert, weil [`slice::join`] die Daten in `name` ohnehin in den String `full` kopiert.

Im Allgemeinen ist das Schreiben von Rust-Funktionen ein sorgfältiges Abwägen, um das _richtige_ Maß an Berechtigungen anzufordern. In diesem Beispiel ist es am idiomatischsten, für `name` nur die Read-Berechtigung zu erwarten.

{{#quiz ../quizzes/ch04-03-fixing-ownership-errors-sec1-idioms.toml}}

### Ein unsicheres Programm reparieren: Aliasing und Verändern einer Datenstruktur {#fixing-an-unsafe-program-aliasing-and-mutating-a-data-structure}

Eine weitere unsichere Operation ist die Verwendung einer Referenz auf Heap-Daten, die über einen anderen Alias freigegeben werden. Hier ist zum Beispiel eine Funktion, die eine Referenz auf den längsten String in einem Vektor holt und sie dann verwendet, während sie den Vektor verändert:

```aquascope,permissions,stepper,boundaries,shouldFail
fn add_big_strings(dst: &mut Vec<String>, src: &[String]) {`(focus,paths:*dst)`
    let largest: &String = 
      dst.iter().max_by_key(|s| s.len()).unwrap();`(focus,paths:*dst)`
    for s in src {
        if s.len() > largest.len() {
            dst.push(s.clone());`{}`
        }
    }
}
```

> _Hinweis:_ Dieses Beispiel verwendet [Iteratoren][iterators] und [Closures][closures], um knapp eine Referenz auf den längsten String zu finden. Wir besprechen diese Features in späteren Kapiteln; vorerst vermitteln wir hier nur ein intuitives Gefühl dafür, wie sie funktionieren.

Dieses Programm wird vom Borrow-Checker zurückgewiesen, weil `let largest = ..` die Berechtigungen @Perm{write} auf `dst` entzieht. `dst.push(..)` benötigt jedoch die Berechtigung @Perm{write}. Auch hier sollten wir fragen: **Warum ist dieses Programm unsicher?** Weil `dst.push(..)` den Inhalt von `dst` freigeben und damit die Referenz `largest` ungültig machen könnte.

Um das Programm zu reparieren, ist die entscheidende Erkenntnis, dass wir die Lifetime von `largest` so verkürzen müssen, dass sie sich nicht mit `dst.push(..)` überschneidet. Eine Möglichkeit ist, `largest` zu klonen:

```rust
fn add_big_strings(dst: &mut Vec<String>, src: &[String]) {
    let largest: String = dst.iter().max_by_key(|s| s.len()).unwrap().clone();
    for s in src {
        if s.len() > largest.len() {
            dst.push(s.clone());
        }
    }
}
```

Das kann allerdings die Performance beeinträchtigen, weil die String-Daten alloziert und kopiert werden müssen.

Eine andere Möglichkeit ist, zuerst alle Längenvergleiche durchzuführen und `dst` erst danach zu verändern:

```rust
fn add_big_strings(dst: &mut Vec<String>, src: &[String]) {
    let largest: &String = dst.iter().max_by_key(|s| s.len()).unwrap();
    let to_add: Vec<String> = 
        src.iter().filter(|s| s.len() > largest.len()).cloned().collect();
    dst.extend(to_add);
}
```

Auch das beeinträchtigt allerdings die Performance, weil der Vektor `to_add` alloziert werden muss.

Eine letzte Möglichkeit ist, die Länge von `largest` herauszukopieren, denn wir brauchen eigentlich nicht den Inhalt von `largest`, sondern nur seine Länge.
Diese Lösung ist wohl die idiomatischste und performanteste:

```rust
fn add_big_strings(dst: &mut Vec<String>, src: &[String]) {
    let largest_len: usize = dst.iter().max_by_key(|s| s.len()).unwrap().len();
    for s in src {
        if s.len() > largest_len {
            dst.push(s.clone());
        }
    }
}
```

All diesen Lösungen ist der entscheidende Gedanke gemeinsam: die Lifetime der Borrows auf `dst` so zu verkürzen, dass sie sich nicht mit einer Veränderung von `dst` überschneiden.

### Ein unsicheres Programm reparieren: Aus einer Collection kopieren oder verschieben {#fixing-an-unsafe-program-copying-vs-moving-out-of-a-collection}

Eine häufige Verwirrung beim Lernen von Rust entsteht, wenn man Daten aus einer Collection wie einem Vektor herauskopiert. Hier ist zum Beispiel ein sicheres Programm, das eine Zahl aus einem Vektor herauskopiert:

```aquascope,permissions,stepper,boundaries
#fn main() {
let v: Vec<i32> = vec![0, 1, 2];
let n_ref: &i32 = &v[0];`(focus,paths:*n_ref)`
let n: i32 = *n_ref;`{}`
#}
```

Die Dereferenzierung `*n_ref` erwartet nur die Berechtigung @Perm{read}, die der Pfad `*n_ref` hat. Was passiert aber, wenn wir den Typ der Elemente im Vektor von `i32` in `String` ändern? Dann stellt sich heraus, dass wir nicht mehr die nötigen Berechtigungen haben:

```aquascope,permissions,stepper,boundaries,shouldFail
#fn main() {
let v: Vec<String> = 
  vec![String::from("Hello world")];
let s_ref: &String = &v[0];`(focus,paths:*s_ref)`
let s: String = *s_ref;`[]``{}`
#}
```

Das erste Programm lässt sich kompilieren, das zweite nicht. Rust gibt folgende Fehlermeldung aus:

```text
error[E0507]: cannot move out of `*s_ref` which is behind a shared reference
 --> test.rs:4:9
  |
4 | let s = *s_ref;
  |         ^^^^^^
  |         |
  |         move occurs because `*s_ref` has type `String`, which does not implement the `Copy` trait
```

Das Problem ist, dass der Vektor `v` den String „Hello world“ besitzt. Wenn wir `s_ref` dereferenzieren, wird versucht, dem Vektor die Ownership des Strings wegzunehmen. Referenzen sind aber nicht-besitzende Zeiger – _über_ eine Referenz können wir keine Ownership übernehmen. Deshalb beschwert sich Rust, dass wir „cannot move out of \[...\] a shared reference“ (nicht aus einer geteilten Referenz herausverschieben können).

Aber warum ist das unsicher? Wir können das Problem veranschaulichen, indem wir das zurückgewiesene Programm simulieren:

```aquascope,interpreter,shouldFail,horizontal
#fn main() {
let v: Vec<String> = 
  vec![String::from("Hello world")];
let s_ref: &String = &v[0];`(focus,paths:*s_ref)`
let s: String = *s_ref;`[]``{}`

// These drops are normally implicit, but we've added them for clarity.
drop(s);`[]`
drop(v);`[]`
#}
```

Was hier passiert, ist ein **Double-Free**. Nach der Ausführung von `let s = *s_ref` glauben sowohl `v` als auch `s`, dass sie „Hello world“ besitzen. Nachdem `s` verworfen wurde, wird „Hello world“ freigegeben. Dann wird `v` verworfen, und undefiniertes Verhalten tritt auf, wenn der String ein zweites Mal freigegeben wird.

> _Hinweis:_ Nach der Ausführung von `s = *s_ref` müssen wir `v` oder `s` nicht einmal verwenden, um durch den Double-Free undefiniertes Verhalten zu verursachen. Sobald wir den String aus `s_ref` herausverschieben, tritt undefiniertes Verhalten auf, sobald die Elemente verworfen werden.

Dieses undefinierte Verhalten tritt jedoch nicht auf, wenn der Vektor `i32`-Elemente enthält. Der Unterschied ist, dass beim Kopieren eines `String` ein Zeiger auf Heap-Daten kopiert wird. Beim Kopieren eines `i32` nicht.
Fachlich ausgedrückt sagt Rust, dass der Typ `i32` den Trait `Copy` implementiert, `String` dagegen `Copy` nicht implementiert (Traits besprechen wir in einem späteren Kapitel).

Zusammengefasst: **Wenn ein Wert keine Heap-Daten besitzt, kann er ohne Move kopiert werden.** Zum Beispiel:

- Ein `i32` besitzt **keine** Heap-Daten, also **kann** er ohne Move kopiert werden.
- Ein `String` besitzt **sehr wohl** Heap-Daten, also **kann** er **nicht** ohne Move kopiert werden.
- Ein `&String` besitzt **keine** Heap-Daten, also **kann** er ohne Move kopiert werden.

> _Hinweis:_ Eine Ausnahme von dieser Regel sind veränderliche Referenzen. `&mut i32` ist zum Beispiel kein kopierbarer Typ. Wenn du also etwa Folgendes schreibst:
>
> ```rust,ignore
> let mut n = 0;
> let a = &mut n;
> let b = a;
> ```
>
> Dann kann `a` nicht mehr verwendet werden, nachdem es `b` zugewiesen wurde. Das verhindert, dass zwei veränderliche Referenzen auf dieselben Daten gleichzeitig verwendet werden.

Wenn wir also einen Vektor mit Typen haben, die nicht `Copy` sind, etwa `String`, wie greifen wir dann sicher auf ein Element des Vektors zu? Hier sind ein paar verschiedene Möglichkeiten, das sicher zu tun. Erstens kannst du darauf verzichten, die Ownership des Strings zu übernehmen, und einfach eine unveränderliche Referenz verwenden:

```rust,ignore
# fn main() {
let v: Vec<String> = vec![String::from("Hello world")];
let s_ref: &String = &v[0];
println!("{s_ref}!");
# }
```

Zweitens kannst du die Daten klonen, wenn du die Ownership des Strings bekommen und den Vektor unverändert lassen willst:

```rust,ignore
# fn main() {
let v: Vec<String> = vec![String::from("Hello world")];
let mut s: String = v[0].clone();
s.push('!');
println!("{s}");
# }
```

Schließlich kannst du eine Methode wie [`Vec::remove`] verwenden, um den String aus dem Vektor herauszuverschieben:

```rust,ignore
# fn main() {
let mut v: Vec<String> = vec![String::from("Hello world")];
let mut s: String = v.remove(0);
s.push('!');
println!("{s}");
assert!(v.len() == 0);
# }
```

### Ein sicheres Programm reparieren: Verschiedene Tupelfelder verändern {#fixing-a-safe-program-mutating-different-tuple-fields}

Die obigen Beispiele sind Fälle, in denen ein Programm unsicher ist. Rust kann aber auch sichere Programme zurückweisen. Ein häufiges Problem ist, dass Rust versucht, Berechtigungen feingranular zu verfolgen. Dabei kann Rust jedoch zwei verschiedene Places als denselben Place behandeln.

Sehen wir uns zuerst ein Beispiel für feingranulare Berechtigungsverfolgung an, das den Borrow-Checker besteht. Dieses Programm zeigt, wie du ein Feld eines Tupels ausleihen (_borrow_) und in ein anderes Feld desselben Tupels schreiben kannst:

```aquascope,permissions,stepper,boundaries
#fn main() {
let mut name = (
    String::from("Ferris"), 
    String::from("Rustacean")
);`(focus,paths:name)`
let first = &name.0;`(focus,paths:name)`
name.1.push_str(", Esq.");`{}`
println!("{first} {}", name.1);
#}
```

Die Anweisung `let first = &name.0` leiht `name.0` aus. Dieser Borrow entzieht `name.0` die Berechtigungen @Perm{write}@Perm{own}. Er entzieht auch `name` die Berechtigungen @Perm{write}@Perm{own}. (Man könnte `name` zum Beispiel nicht an eine Funktion übergeben, die einen Wert vom Typ `(String, String)` als Eingabe nimmt.) `name.1` behält aber die Berechtigung @Perm{write}, sodass `name.1.push_str(...)` eine gültige Operation ist.

Rust kann allerdings den Überblick darüber verlieren, welche Places genau ausgeliehen sind. Angenommen, wir lagern den Ausdruck `&name.0` in eine Funktion `get_first` aus. Beachte, wie Rust nach dem Aufruf von `get_first(&name)` jetzt die Berechtigung @Perm{write} auf `name.1` entzieht:

```aquascope,permissions,stepper,boundaries,shouldFail
fn get_first(name: &(String, String)) -> &String {
    &name.0
}

fn main() {
    let mut name = (
        String::from("Ferris"), 
        String::from("Rustacean")
    );
    let first = get_first(&name);`(focus,paths:name)`
    name.1.push_str(", Esq.");`{}`
    println!("{first} {}", name.1);
}
```

Jetzt können wir `name.1.push_str(..)` nicht mehr ausführen! Rust gibt diesen Fehler aus:

```text
error[E0502]: cannot borrow `name.1` as mutable because it is also borrowed as immutable
  --> test.rs:11:5
   |
10 |     let first = get_first(&name);
   |                           ----- immutable borrow occurs here
11 |     name.1.push_str(", Esq.");
   |     ^^^^^^^^^^^^^^^^^^^^^^^^^ mutable borrow occurs here
12 |     println!("{first} {}", name.1);
   |                ----- immutable borrow later used here
```

Das ist seltsam, denn das Programm war sicher, bevor wir es bearbeitet haben. Unsere Änderung verändert das Laufzeitverhalten nicht wesentlich. Warum spielt es also eine Rolle, dass wir `&name.0` in eine Funktion gesteckt haben?

Das Problem ist, dass Rust sich die Implementierung von `get_first` nicht ansieht, wenn es entscheidet, was `get_first(&name)` ausleihen soll. Rust betrachtet nur die Typsignatur, die lediglich sagt: „Irgendein `String` in der Eingabe wird ausgeliehen“. Rust entscheidet daher vorsichtshalber, dass sowohl `name.0` als auch `name.1` ausgeliehen werden, und entzieht beiden die Write- und Own-Berechtigungen.

Denk daran, der entscheidende Gedanke ist: **Das obige Programm ist sicher.** Es hat kein undefiniertes Verhalten! Eine künftige Version von Rust ist vielleicht schlau genug, es kompilieren zu lassen, aber heute wird es zurückgewiesen. Wie umgehen wir den Borrow-Checker also heute? Eine Möglichkeit ist, den Ausdruck `&name.0` wieder direkt einzusetzen, wie im ursprünglichen Programm. Eine andere Möglichkeit ist, die Borrow-Prüfung mit [Cells][cells] auf die Laufzeit zu verschieben; diese besprechen wir in späteren Kapiteln.

### Ein sicheres Programm reparieren: Verschiedene Array-Elemente verändern {#fixing-a-safe-program-mutating-different-array-elements}

Ein ähnliches Problem entsteht, wenn wir Elemente eines Arrays ausleihen. Beachte zum Beispiel, welche Places ausgeliehen werden, wenn wir eine veränderliche Referenz auf ein Array erzeugen:

```aquascope,permissions,stepper,boundaries
#fn main() {
let mut a = [0, 1, 2, 3];
let x = &mut a[1];`(focus,paths:a[_])`
*x += 1;`(focus,paths:a[_])`
println!("{a:?}");
#}
```

Der Borrow-Checker von Rust hat keine getrennten Places für `a[0]`, `a[1]` und so weiter. Er verwendet einen einzigen Place `a[_]`, der _alle_ Indizes von `a` darstellt. Rust macht das, weil es den Wert eines Index nicht immer bestimmen kann. Stell dir zum Beispiel ein komplexeres Szenario wie dieses vor:

```rust,ignore
let idx = a_complex_function();
let x = &mut a[idx];
```

Welchen Wert hat `idx`? Rust wird nicht raten, also nimmt es an, dass `idx` alles Mögliche sein könnte. Angenommen, wir versuchen zum Beispiel, aus einem Array-Index zu lesen, während wir in einen anderen schreiben:

```aquascope,permissions,boundaries,stepper,shouldFail
#fn main() {
let mut a = [0, 1, 2, 3];
let x = &mut a[1];`(focus,paths:a[_])`
let y = &a[2];`{}`
*x += *y;
#}
```

Rust weist dieses Programm jedoch zurück, weil `a` seine Read-Berechtigung an `x` abgegeben hat. Die Fehlermeldung des Compilers sagt dasselbe:

```text
error[E0502]: cannot borrow `a[_]` as immutable because it is also borrowed as mutable
 --> test.rs:4:9
  |
3 | let x = &mut a[1];
  |         --------- mutable borrow occurs here
4 | let y = &a[2];
  |         ^^^^^ immutable borrow occurs here
5 | *x += *y;
  | -------- mutable borrow later used here
```

<!-- However, Rust will reject this program because `a` gave its read permission to `x`. -->

Auch hier gilt: **Dieses Programm ist sicher.** Für Fälle wie diese bietet Rust oft eine Funktion in der Standardbibliothek, mit der sich der Borrow-Checker umgehen lässt. Wir könnten zum Beispiel [`slice::split_at_mut`][split_at_mut] verwenden:

```rust,ignore
# fn main() {
let mut a = [0, 1, 2, 3];
let (a_l, a_r) = a.split_at_mut(2);
let x = &mut a_l[1];
let y = &a_r[0];
*x += *y;
# }
```

Vielleicht fragst du dich: Wie ist `split_at_mut` denn implementiert? In manchen Rust-Bibliotheken, besonders bei Kerntypen wie `Vec` oder `slice`, findest du oft **`unsafe`-Blöcke**. `unsafe`-Blöcke erlauben die Verwendung von „rohen“ Zeigern (Raw-Pointern), deren Sicherheit der Borrow-Checker nicht prüft. Wir könnten zum Beispiel einen unsafe-Block verwenden, um unsere Aufgabe zu erledigen:

```rust,ignore
# fn main() {
let mut a = [0, 1, 2, 3];
let x = &mut a[1] as *mut i32;
let y = &a[2] as *const i32;
unsafe { *x += *y; } // DO NOT DO THIS unless you know what you're doing!
# }
```

Unsicherer Code ist manchmal nötig, um die Einschränkungen des Borrow-Checkers zu umgehen. Als allgemeine Strategie gilt: Wenn der Borrow-Checker ein Programm zurückweist, das du für tatsächlich sicher hältst, solltest du nach Funktionen der Standardbibliothek suchen (wie `split_at_mut`), die `unsafe`-Blöcke enthalten und dein Problem lösen. Unsicheren Code besprechen wir ausführlicher in [Kapitel 20][unsafe]. Vorerst solltest du nur wissen, dass Rust mit unsicherem Code bestimmte Patterns implementiert, die sonst unmöglich wären.

{{#quiz ../quizzes/ch04-03-fixing-ownership-errors-sec2-safety.toml}}

### Zusammenfassung {#summary}

Wenn du einen Ownership-Fehler behebst, solltest du dich fragen: Ist mein Programm tatsächlich unsicher? Wenn ja, musst du die eigentliche Ursache der Unsicherheit verstehen. Wenn nein, musst du die Einschränkungen des Borrow-Checkers verstehen, um sie zu umgehen.

[rc]: https://doc.rust-lang.org/std/rc/index.html
[cells]: https://doc.rust-lang.org/std/cell/index.html
[split_at_mut]: https://doc.rust-lang.org/std/primitive.slice.html#method.split_at_mut
[unsafe]: ch19-01-unsafe-rust.html
[`Vec::remove`]: https://doc.rust-lang.org/std/vec/struct.Vec.html#method.remove
[`slice::join`]: https://doc.rust-lang.org/std/primitive.slice.html#method.join
[iterators]: ch13-02-iterators.html
[closures]: ch13-01-closures.html

[^safe-subset]: Diese Garantie gilt für Programme, die in der „sicheren Teilmenge“ von Rust geschrieben sind. Wenn du `unsafe`-Code verwendest oder unsichere Komponenten aufrufst (etwa eine C-Bibliothek), musst du besonders sorgfältig sein, um undefiniertes Verhalten zu vermeiden.
