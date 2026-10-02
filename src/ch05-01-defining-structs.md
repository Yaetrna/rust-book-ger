## Structs definieren und instanziieren {#defining-and-instantiating-structs}

Structs ähneln Tupeln, die wir im Abschnitt
[„Der Tupeltyp“][tuples]<!-- ignore --> besprochen haben, denn beide enthalten
mehrere zusammengehörige Werte. Wie bei Tupeln können die Bestandteile eines
Structs unterschiedliche Typen haben. Anders als bei Tupeln benennst du in einem
Struct jedes Datenstück, sodass klar ist, was die Werte bedeuten. Durch diese
Namen sind Structs flexibler als Tupel: Du musst dich nicht auf die Reihenfolge
der Daten verlassen, um die Werte einer Instanz anzugeben oder auf sie
zuzugreifen.

Um ein Struct zu definieren, schreiben wir das Schlüsselwort `struct` und
benennen das gesamte Struct. Der Name eines Structs sollte beschreiben, welche
Bedeutung die zusammengefassten Datenstücke haben. Dann definieren wir in
geschweiften Klammern die Namen und Typen der Datenstücke, die wir _Felder_
(_fields_) nennen. Listing 5-1 zeigt zum Beispiel ein Struct, das Informationen
über ein Benutzerkonto speichert.

<Listing number="5-1" file-name="src/main.rs" caption="Eine Definition des Structs `User`">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-01/src/main.rs:here}}
```

</Listing>

Um ein Struct nach seiner Definition zu verwenden, erzeugen wir eine _Instanz_
dieses Structs, indem wir für jedes Feld konkrete Werte angeben. Wir erzeugen
eine Instanz, indem wir den Namen des Structs angeben und dann geschweifte
Klammern mit Paaren der Form _`key:
value`_ hinzufügen, wobei die Schlüssel die
Namen der Felder sind und die Werte die Daten, die wir in diesen Feldern
speichern wollen. Wir müssen die Felder nicht in derselben Reihenfolge angeben,
in der wir sie im Struct deklariert haben. Anders gesagt ist die
Struct-Definition wie eine allgemeine Vorlage für den Typ, und Instanzen füllen
diese Vorlage mit bestimmten Daten, um Werte des Typs zu erzeugen. Wir können
zum Beispiel einen bestimmten Benutzer deklarieren, wie in Listing 5-2 gezeigt.

```aquascope,interpreter
#struct User {
#    active: bool,
#    username: String,
#    email: String,
#    sign_in_count: u64,
#}
fn main() {
    let user1 = User {
        email: String::from("someone@example.com"),
        username: String::from("someusername123"),
        active: true,
        sign_in_count: 1,
    };`[]`
}
```

Um einen bestimmten Wert aus einem Struct zu bekommen, verwenden wir die
Punktnotation. Um zum Beispiel auf die E-Mail-Adresse dieses Benutzers
zuzugreifen, verwenden wir `user1.email`. Wenn die Instanz veränderlich
(_mutable_) ist, können wir einen Wert ändern, indem wir die Punktnotation
verwenden und einem bestimmten Feld etwas zuweisen. Listing 5-3 zeigt, wie man
den Wert im Feld `email` einer veränderlichen `User`-Instanz ändert.

```aquascope,interpreter
#struct User {
#    active: bool,
#    username: String,
#    email: String,
#    sign_in_count: u64,
#}
fn main() {
    let mut user1 = User {
        email: String::from("someone@example.com"),
        username: String::from("someusername123"),
        active: true,
        sign_in_count: 1,
    };`[]`

    user1.email = String::from("anotheremail@example.com");`[]`
}
```

Beachte, dass die gesamte Instanz veränderlich sein muss; Rust erlaubt nicht,
nur bestimmte Felder als veränderlich zu kennzeichnen. Wie bei jedem Ausdruck
können wir als letzten Ausdruck im Funktionsrumpf eine neue Instanz des Structs
erzeugen, um diese neue Instanz implizit zurückzugeben.

Listing 5-4 zeigt eine Funktion `build_user`, die eine `User`-Instanz mit der
angegebenen E-Mail-Adresse und dem angegebenen Benutzernamen zurückgibt. Das
Feld `active` erhält den Wert `true` und `sign_in_count` den Wert `1`.

<Listing number="5-4" file-name="src/main.rs" caption="Eine Funktion `build_user`, die eine E-Mail-Adresse und einen Benutzernamen nimmt und eine `User`-Instanz zurückgibt">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-04/src/main.rs:here}}
```

</Listing>

Es ist sinnvoll, die Funktionsparameter genauso zu nennen wie die Felder des
Structs, aber die Feldnamen und Variablen `email` und `username` wiederholen zu
müssen, ist etwas mühsam. Hätte das Struct mehr Felder, wäre das Wiederholen
jedes Namens noch lästiger. Zum Glück gibt es eine praktische Kurzschreibweise!

<!-- Old headings. Do not remove or links may break. -->

<a id="using-the-field-init-shorthand-when-variables-and-fields-have-the-same-name"></a>

### Die Kurzschreibweise für die Feldinitialisierung verwenden {#using-the-field-init-shorthand}

Weil die Parameternamen und die Feldnamen des Structs in Listing 5-4 genau
gleich sind, können wir mit der Syntax der _Kurzschreibweise für die
Feldinitialisierung_ (_field init shorthand_) `build_user` so umschreiben, dass
sich die Funktion genau gleich verhält, aber `username` und `email` nicht
wiederholt, wie in Listing 5-5 gezeigt.

<Listing number="5-5" file-name="src/main.rs" caption="Eine Funktion `build_user`, die die Kurzschreibweise für die Feldinitialisierung verwendet, weil die Parameter `username` und `email` genauso heißen wie die Felder des Structs">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-05/src/main.rs:here}}
```

</Listing>

Hier erzeugen wir eine neue Instanz des Structs `User`, das ein Feld namens
`email` hat. Wir wollen den Wert des Felds `email` auf den Wert des Parameters
`email` der Funktion `build_user` setzen. Weil das Feld `email` und der
Parameter `email` denselben Namen haben, müssen wir nur `email` statt
`email: email` schreiben.

<!-- Old headings. Do not remove or links may break. -->

<a id="creating-instances-from-other-instances-with-struct-update-syntax"></a>

### Instanzen mit der Struct-Update-Syntax erzeugen {#creating-instances-with-struct-update-syntax}

Oft ist es nützlich, eine neue Instanz eines Structs zu erzeugen, die die
meisten Werte einer anderen Instanz desselben Typs übernimmt, einige davon aber
ändert. Das kannst du mit der Struct-Update-Syntax erreichen.

Zunächst zeigen wir in Listing 5-6, wie man auf die übliche Weise, ohne die
Update-Syntax, eine neue `User`-Instanz in `user2` erzeugt. Wir setzen einen
neuen Wert für `email`, verwenden ansonsten aber dieselben Werte aus `user1`,
das wir in Listing 5-2 erzeugt haben.

```aquascope,interpreter
#struct User {
#    active: bool,
#    username: String,
#    email: String,
#    sign_in_count: u64,
#}
fn main() {
#   let user1 = User {
#      email: String::from("someone@example.com"),
#      username: String::from("someusername123"),
#      active: true,
#      sign_in_count: 1,
#   };
    // --snip--

    let user2 = User {
        active: user1.active,
        username: user1.username,
        email: String::from("another@example.com"),
        sign_in_count: user1.sign_in_count,
    };`[]`
}
```

<span class="caption">Listing 5-6: Eine neue `User`-Instanz erzeugen, die alle
Werte außer einem aus `user1` verwendet</span>

Mit der Struct-Update-Syntax erreichen wir dasselbe mit weniger Code, wie in
Listing 5-7 gezeigt. Die Syntax `..` gibt an, dass die übrigen, nicht explizit
gesetzten Felder denselben Wert haben sollen wie die Felder der angegebenen
Instanz.

<Listing number="5-7" file-name="src/main.rs" caption="Die Struct-Update-Syntax verwenden, um einen neuen Wert für `email` einer `User`-Instanz zu setzen, die übrigen Werte aber aus `user1` zu übernehmen">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-07/src/main.rs:here}}
```

</Listing>

Der Code in Listing 5-7 erzeugt ebenfalls eine Instanz in `user2`, die einen
anderen Wert für `email` hat, aber dieselben Werte für die Felder `username`,
`active` und `sign_in_count` aus `user1`. Das `..user1` muss am Ende stehen, um
anzugeben, dass alle übrigen Felder ihre Werte aus den entsprechenden Feldern in
`user1` bekommen sollen; wir können aber für beliebig viele Felder in beliebiger
Reihenfolge Werte angeben, unabhängig von der Reihenfolge der Felder in der
Definition des Structs.

Beachte, dass die Struct-Update-Syntax `=` wie eine Zuweisung verwendet; das
liegt daran, dass sie die Daten verschiebt (_move_), so wie wir es im Abschnitt
[„Was ist Ownership?“][move]<!-- ignore --> gesehen haben. In diesem Beispiel
ist `user1` nach dem Erzeugen von `user2` teilweise ungültig, weil der `String`
im Feld `username` von `user1` nach `user2` verschoben wurde. Hätten wir `user2`
sowohl für `email` als auch für `username` neue `String`-Werte gegeben und damit
nur die Werte `active` und `sign_in_count` aus `user1` verwendet, wäre `user1`
nach dem Erzeugen von `user2` weiterhin vollständig gültig. Die Typen von
`active` und `sign_in_count` sind Typen, die den Trait `Copy` implementieren,
daher gilt das Verhalten, das wir im Abschnitt
[„Aus einer Collection kopieren oder verschieben“][copy]<!-- ignore -->
besprochen haben.

<!-- Old headings. Do not remove or links may break. -->

<a id="using-tuple-structs-without-named-fields-to-create-different-types"></a>

### Verschiedene Typen mit Tupel-Structs erzeugen {#creating-different-types-with-tuple-structs}

Rust unterstützt auch Structs, die Tupeln ähneln, sogenannte _Tupel-Structs_
(_tuple structs_). Tupel-Structs haben die zusätzliche Bedeutung, die der Name
des Structs mitbringt, aber ihren Feldern sind keine Namen zugeordnet; sie haben
nur die Typen der Felder. Tupel-Structs sind nützlich, wenn du dem ganzen Tupel
einen Namen geben und es zu einem anderen Typ als andere Tupel machen willst und
wenn es umständlich oder überflüssig wäre, jedes Feld wie in einem normalen
Struct zu benennen.

Um ein Tupel-Struct zu definieren, beginnst du mit dem Schlüsselwort `struct`
und dem Namen des Structs, gefolgt von den Typen im Tupel. Hier definieren und
verwenden wir zum Beispiel zwei Tupel-Structs namens `Color` und `Point`:

<Listing file-name="src/main.rs">

```aquascope,interpreter
struct Color(i32, i32, i32);
struct Point(i32, i32, i32);

fn main() {
    let black = Color(0, 0, 0);
    let origin = Point(0, 0, 0);`[]`
}
```

</Listing>

Beachte, dass die Werte `black` und `origin` unterschiedliche Typen haben, weil
sie Instanzen verschiedener Tupel-Structs sind. Jedes Struct, das du definierst,
ist ein eigener Typ, auch wenn die Felder innerhalb des Structs dieselben Typen
haben. Eine Funktion, die einen Parameter vom Typ `Color` nimmt, kann zum
Beispiel kein `Point` als Argument nehmen, obwohl beide Typen aus drei
`i32`-Werten bestehen. Ansonsten ähneln Instanzen von Tupel-Structs Tupeln: Du
kannst sie in ihre einzelnen Bestandteile destrukturieren, und du kannst mit
einem `.` gefolgt vom Index auf einen einzelnen Wert zugreifen. Anders als bei
Tupeln musst du bei Tupel-Structs beim Destrukturieren den Typ des Structs
angeben. Wir würden zum Beispiel `let Point(x, y, z) = origin;` schreiben, um
die Werte im Punkt `origin` in Variablen namens `x`, `y` und `z` zu
destrukturieren.

<!-- Old headings. Do not remove or links may break. -->

<a id="unit-like-structs-without-any-fields"></a>

### Unit-artige Structs definieren {#defining-unit-like-structs}

Du kannst auch Structs definieren, die gar keine Felder haben! Sie heißen
_Unit-artige Structs_ (_unit-like structs_), weil sie sich ähnlich wie `()`
verhalten, der Unit-Typ, den wir im Abschnitt
[„Der Tupeltyp“][tuples]<!-- ignore --> erwähnt haben. Unit-artige Structs
können nützlich sein, wenn du einen Trait für einen Typ implementieren musst,
aber keine Daten hast, die du im Typ selbst speichern willst. Traits besprechen
wir in Kapitel 10. Hier ist ein Beispiel für die Deklaration und Instanziierung
eines Unit-Structs namens `AlwaysEqual`:

```aquascope,interpreter
struct AlwaysEqual;

fn main() {
    let subject = AlwaysEqual;`[]`
}
```

Um `AlwaysEqual` zu definieren, verwenden wir das Schlüsselwort `struct`, den
gewünschten Namen und dann ein Semikolon. Geschweifte oder runde Klammern sind
nicht nötig! Eine Instanz von `AlwaysEqual` in der Variable `subject` bekommen
wir dann auf ähnliche Weise: mit dem definierten Namen, ohne geschweifte oder
runde Klammern. Stell dir vor, wir implementieren später für diesen Typ ein
Verhalten, bei dem jede Instanz von `AlwaysEqual` immer gleich jeder Instanz
jedes anderen Typs ist, vielleicht um für Testzwecke ein bekanntes Ergebnis zu
haben. Für dieses Verhalten bräuchten wir keinerlei Daten! In Kapitel 10 siehst
du, wie man Traits definiert und für beliebige Typen implementiert, auch für
Unit-artige Structs.

> ### Ownership von Struct-Daten {#ownership-of-struct-data}
>
> In der Definition des Structs `User` in Listing 5-1 haben wir den Typ
> `String`, der seine Daten besitzt, statt des String-Slice-Typs `&str`
> verwendet. Das ist eine bewusste Entscheidung, denn wir wollen, dass jede
> Instanz dieses Structs alle ihre Daten besitzt und dass diese Daten so lange
> gültig sind, wie das gesamte Struct gültig ist.
>
> Structs können auch Referenzen auf Daten speichern, die etwas anderem gehören,
> aber dafür braucht man _Lifetimes_, ein Feature von Rust, das wir in Kapitel
> 10 besprechen. Lifetimes stellen sicher, dass die von einem Struct
> referenzierten Daten so lange gültig sind wie das Struct. Angenommen, du
> versuchst, eine Referenz in einem Struct zu speichern, ohne Lifetimes
> anzugeben, etwa wie folgt in _src/main.rs_; das funktioniert nicht:
>
> <Listing file-name="src/main.rs">
>
> <!-- CAN'T EXTRACT SEE https://github.com/rust-lang/mdBook/issues/1127 -->
>
> ```rust,ignore,does_not_compile
> struct User {
>     active: bool,
>     username: &str,
>     email: &str,
>     sign_in_count: u64,
> }
>
> fn main() {
>     let user1 = User {
>         active: true,
>         username: "someusername123",
>         email: "someone@example.com",
>         sign_in_count: 1,
>     };
> }
> ```
>
> </Listing>
>
> Der Compiler beschwert sich, dass er Lifetime-Angaben braucht:
>
> ```console
> $ cargo run
>    Compiling structs v0.1.0 (file:///projects/structs)
> error[E0106]: missing lifetime specifier
>  --> src/main.rs:3:15
>   |
> 3 |     username: &str,
>   |               ^ expected named lifetime parameter
>   |
> help: consider introducing a named lifetime parameter
>   |
> 1 ~ struct User<'a> {
> 2 |     active: bool,
> 3 ~     username: &'a str,
>   |
>
> error[E0106]: missing lifetime specifier
>  --> src/main.rs:4:12
>   |
> 4 |     email: &str,
>   |            ^ expected named lifetime parameter
>   |
> help: consider introducing a named lifetime parameter
>   |
> 1 ~ struct User<'a> {
> 2 |     active: bool,
> 3 |     username: &str,
> 4 ~     email: &'a str,
>   |
>
> For more information about this error, try `rustc --explain E0106`.
> error: could not compile `structs` (bin "structs") due to 2 previous errors
> ```
>
> In Kapitel 10 besprechen wir, wie du diese Fehler behebst, damit du Referenzen
> in Structs speichern kannst; vorerst beheben wir solche Fehler, indem wir
> Typen wie `String`, die ihre Daten besitzen, statt Referenzen wie `&str`
> verwenden.

### Felder eines Structs ausleihen {#borrowing-fields-of-a-struct}

Ähnlich wie in unserer Besprechung in
[„Verschiedene Tupelfelder verändern“][differentfields] verfolgt der
Borrow-Checker von Rust Ownership-Berechtigungen sowohl auf der Ebene des
Structs als auch auf der Ebene der Felder. Wenn wir zum Beispiel ein Feld `x`
eines `Point`-Structs ausleihen (_borrow_), verlieren sowohl `p` als auch `p.x`
vorübergehend ihre Berechtigungen (`p.y` aber nicht):

```aquascope,permissions,stepper,boundaries
#fn main() {
struct Point { x: i32, y: i32 }

let mut p = Point { x: 0, y: 0 };`(focus,paths:p)`
let x = &mut p.x;`(focus,paths:p)`
*x += 1;`(focus,paths:p)`
println!("{}, {}", p.x, p.y);
#}
```

Wenn wir also versuchen, `p` zu verwenden, während `p.x` veränderlich
ausgeliehen ist, etwa so:

```aquascope,permissions,stepper,boundaries,shouldFail
struct Point { x: i32, y: i32 }

fn print_point(p: &Point) {
    println!("{}, {}", p.x, p.y);
}

fn main() {
    let mut p = Point { x: 0, y: 0 };`(focus,paths:p)`
    let x = &mut p.x;`(focus,paths:p)`
    print_point(&p);`{}`
    *x += 1;`(focus,paths:p)`
}
```

Dann weist der Compiler unser Programm mit folgendem Fehler zurück:

```text
error[E0502]: cannot borrow `p` as immutable because it is also borrowed as mutable
  --> test.rs:10:17
   |
9  |     let x = &mut p.x;
   |             -------- mutable borrow occurs here
10 |     print_point(&p);
   |                 ^^ immutable borrow occurs here
11 |     *x += 1;
   |     ------- mutable borrow later used here
```

Allgemeiner gesagt: Wenn du auf einen Ownership-Fehler stößt, an dem ein Struct
beteiligt ist, solltest du überlegen, welche Felder deines Structs mit welchen
Berechtigungen ausgeliehen werden sollen. Denk aber an die Einschränkungen des
Borrow-Checkers, denn Rust nimmt manchmal an, dass mehr Felder ausgeliehen sind,
als es tatsächlich der Fall ist.

{{#quiz ../quizzes/ch05-01-structs.toml}}

<!-- manual-regeneration
for the error above
after running update-rustc.sh:
pbcopy < listings/ch05-using-structs-to-structure-related-data/no-listing-02-reference-in-struct/output.txt
paste above
add `> ` before every line -->

[tuples]: ch03-02-data-types.html#the-tuple-type
[move]: ch04-01-what-is-ownership.html
[copy]: ch04-03-fixing-ownership-errors.html#fixing-an-unsafe-program-copying-vs-moving-out-of-a-collection
[differentfields]: ch04-03-fixing-ownership-errors.html#fixing-a-safe-program-mutating-different-tuple-fields
