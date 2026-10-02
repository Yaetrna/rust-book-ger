## Methoden {#methods}

Methoden ähneln Funktionen: Wir deklarieren sie mit dem Schlüsselwort `fn` und
einem Namen, sie können Parameter und einen Rückgabewert haben, und sie
enthalten Code, der ausgeführt wird, wenn die Methode irgendwo anders aufgerufen
wird. Anders als Funktionen werden Methoden im Kontext eines Structs definiert
(oder eines Enums oder eines Trait-Objekts, die wir in
[Kapitel 6][enums]<!-- ignore --> bzw.
[Kapitel 18][trait-objects]<!-- ignore --> behandeln), und ihr erster Parameter
ist immer `self`, das die Instanz des Structs darstellt, auf der die Methode
aufgerufen wird.

<!-- Old headings. Do not remove or links may break. -->

<a id="defining-methods"></a>

### Methodensyntax {#method-syntax}

Ändern wir die Funktion `area`, die eine `Rectangle`-Instanz als Parameter hat,
und machen wir stattdessen eine Methode `area` daraus, die auf dem Struct
`Rectangle` definiert ist, wie in Listing 5-13 gezeigt.

<Listing number="5-13" file-name="src/main.rs" caption="Eine Methode `area` auf dem Struct `Rectangle` definieren">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-13/src/main.rs}}
```

</Listing>

Um die Funktion im Kontext von `Rectangle` zu definieren, beginnen wir einen
`impl`-Block (für _implementation_, Implementierung) für `Rectangle`. Alles
innerhalb dieses `impl`-Blocks gehört zum Typ `Rectangle`. Dann verschieben wir
die Funktion `area` in die geschweiften Klammern von `impl` und ändern den
ersten (und in diesem Fall einzigen) Parameter in der Signatur und überall im
Rumpf zu `self`. In `main`, wo wir die Funktion `area` aufgerufen und `rect1`
als Argument übergeben haben, können wir stattdessen die _Methodensyntax_
verwenden, um die Methode `area` auf unserer `Rectangle`-Instanz aufzurufen. Die
Methodensyntax folgt auf eine Instanz: Wir fügen einen Punkt hinzu, gefolgt vom
Methodennamen, runden Klammern und etwaigen Argumenten.

In der Signatur von `area` verwenden wir `&self` statt `rectangle: &Rectangle`.
`&self` ist eigentlich die Kurzform von `self: &Self`. Innerhalb eines
`impl`-Blocks ist der Typ `Self` ein Alias für den Typ, für den der `impl`-Block
gilt. Methoden müssen als ersten Parameter einen Parameter namens `self` vom Typ
`Self` haben, daher lässt Rust dich das an der ersten Parameterstelle mit dem
bloßen Namen `self` abkürzen. Beachte, dass wir weiterhin das `&` vor der
Kurzform `self` brauchen, um anzuzeigen, dass diese Methode die `Self`-Instanz
ausleiht (_borrow_), genau wie wir es bei `rectangle: &Rectangle` getan haben.
Methoden können die Ownership von `self` übernehmen, `self` unveränderlich
(_immutable_) ausleihen, wie wir es hier getan haben, oder `self` veränderlich
(_mutable_) ausleihen, genau wie bei jedem anderen Parameter.

Wir haben hier `&self` aus demselben Grund gewählt, aus dem wir in der
Funktionsversion `&Rectangle` verwendet haben: Wir wollen keine Ownership
übernehmen, und wir wollen die Daten im Struct nur lesen, nicht schreiben.
Wollten wir als Teil dessen, was die Methode tut, die Instanz ändern, auf der
wir die Methode aufgerufen haben, würden wir `&mut self` als ersten Parameter
verwenden. Eine Methode, die mit bloßem `self` als erstem Parameter die
Ownership der Instanz übernimmt, ist selten; diese Technik wird normalerweise
verwendet, wenn die Methode `self` in etwas anderes umwandelt und du verhindern
willst, dass die aufrufende Stelle die ursprüngliche Instanz nach der Umwandlung
noch verwendet.

Der Hauptgrund, Methoden statt Funktionen zu verwenden, ist – neben der
Methodensyntax und dem Vorteil, den Typ von `self` nicht in jeder
Methodensignatur wiederholen zu müssen – die Organisation. Wir haben alles, was
wir mit einer Instanz eines Typs tun können, in einen einzigen `impl`-Block
gesteckt, statt künftige Nutzerinnen und Nutzer unseres Codes an verschiedenen
Stellen der von uns bereitgestellten Bibliothek nach den Fähigkeiten von
`Rectangle` suchen zu lassen.

Beachte, dass wir einer Methode denselben Namen wie einem der Felder des Structs
geben können. Wir können zum Beispiel auf `Rectangle` eine Methode definieren,
die ebenfalls `width` heißt:

<Listing file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/no-listing-06-method-field-interaction/src/main.rs:here}}
```

</Listing>

Hier lassen wir die Methode `width` `true` zurückgeben, wenn der Wert im Feld
`width` der Instanz größer als `0` ist, und `false`, wenn der Wert `0` ist:
Innerhalb einer gleichnamigen Methode können wir ein Feld für beliebige Zwecke
verwenden. Wenn wir in `main` auf `rect1.width` runde Klammern folgen lassen,
weiß Rust, dass wir die Methode `width` meinen. Wenn wir keine runden Klammern
verwenden, weiß Rust, dass wir das Feld `width` meinen.

Oft, aber nicht immer, soll eine Methode, der wir denselben Namen wie einem Feld
geben, nur den Wert des Felds zurückgeben und sonst nichts tun. Solche Methoden
heißen _Getter_, und Rust implementiert sie nicht automatisch für Felder von
Structs, wie es manche anderen Sprachen tun. Getter sind nützlich, weil du das
Feld privat, die Methode aber öffentlich machen und so als Teil der öffentlichen
API des Typs schreibgeschützten Zugriff auf dieses Feld ermöglichen kannst. Was
öffentlich und privat bedeuten und wie man ein Feld oder eine Methode als
öffentlich oder privat kennzeichnet, besprechen wir in
[Kapitel 7][public]<!-- ignore -->.

### Methoden mit mehr Parametern {#methods-with-more-parameters}

Üben wir den Umgang mit Methoden, indem wir eine zweite Methode auf dem Struct
`Rectangle` implementieren. Diesmal soll eine Instanz von `Rectangle` eine
andere `Rectangle`-Instanz nehmen und `true` zurückgeben, wenn das zweite
`Rectangle` vollständig in `self` (das erste `Rectangle`) passt; andernfalls
soll sie `false` zurückgeben. Sobald wir die Methode `can_hold` definiert haben,
wollen wir also das in Listing 5-14 gezeigte Programm schreiben können.

<Listing number="5-14" file-name="src/main.rs" caption="Die noch nicht geschriebene Methode `can_hold` verwenden">

```rust,ignore
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-14/src/main.rs}}
```

</Listing>

Die erwartete Ausgabe sähe wie folgt aus, weil beide Abmessungen von `rect2`
kleiner sind als die Abmessungen von `rect1`, `rect3` aber breiter ist als
`rect1`:

```text
Can rect1 hold rect2? true
Can rect1 hold rect3? false
```

Wir wissen, dass wir eine Methode definieren wollen, also steht sie im Block
`impl Rectangle`. Die Methode heißt `can_hold` und nimmt als Parameter einen
unveränderlichen Borrow eines anderen `Rectangle`. Welchen Typ der Parameter
hat, erkennen wir am Code, der die Methode aufruft: `rect1.can_hold(&rect2)`
übergibt `&rect2`, einen unveränderlichen Borrow von `rect2`, einer Instanz von
`Rectangle`. Das ist sinnvoll, weil wir `rect2` nur lesen müssen (statt zu
schreiben, wofür wir einen veränderlichen Borrow bräuchten) und weil `main` die
Ownership von `rect2` behalten soll, damit wir es nach dem Aufruf der Methode
`can_hold` weiterverwenden können. Der Rückgabewert von `can_hold` ist ein
boolescher Wert, und die Implementierung prüft, ob Breite und Höhe von `self`
jeweils größer sind als Breite und Höhe des anderen `Rectangle`. Fügen wir die
neue Methode `can_hold` dem `impl`-Block aus Listing 5-13 hinzu, wie in Listing
5-15 gezeigt.

<Listing number="5-15" file-name="src/main.rs" caption="Die Methode `can_hold` auf `Rectangle` implementieren, die eine andere `Rectangle`-Instanz als Parameter nimmt">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-15/src/main.rs:here}}
```

</Listing>

Wenn wir diesen Code mit der Funktion `main` aus Listing 5-14 ausführen,
bekommen wir die gewünschte Ausgabe. Methoden können mehrere Parameter haben,
die wir der Signatur nach dem Parameter `self` hinzufügen, und diese Parameter
funktionieren genau wie Parameter in Funktionen.

### Assoziierte Funktionen {#associated-functions}

Alle Funktionen, die innerhalb eines `impl`-Blocks definiert sind, heißen
_assoziierte Funktionen_, weil sie dem Typ zugeordnet sind, der nach dem `impl`
genannt wird. Wir können assoziierte Funktionen definieren, die `self` nicht als
ersten Parameter haben (und daher keine Methoden sind), weil sie keine Instanz
des Typs brauchen, um zu arbeiten. Eine solche Funktion haben wir bereits
verwendet: die Funktion `String::from`, die auf dem Typ `String` definiert ist.

Assoziierte Funktionen, die keine Methoden sind, werden oft für Konstruktoren
verwendet, die eine neue Instanz des Structs zurückgeben. Diese heißen oft
`new`, aber `new` ist kein besonderer Name und nicht in die Sprache eingebaut.
Wir könnten zum Beispiel eine assoziierte Funktion namens `square`
bereitstellen, die einen einzigen Parameter für die Abmessung hat und ihn sowohl
als Breite als auch als Höhe verwendet. So lässt sich ein quadratisches
`Rectangle` leichter erzeugen, ohne denselben Wert zweimal angeben zu müssen:

<span class="filename">Dateiname: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/no-listing-03-associated-functions/src/main.rs:here}}
```

Die Schlüsselwörter `Self` im Rückgabetyp und im Rumpf der Funktion sind Aliasse
für den Typ, der nach dem Schlüsselwort `impl` steht, in diesem Fall
`Rectangle`.

Um diese assoziierte Funktion aufzurufen, verwenden wir die Syntax `::` mit dem
Namen des Structs; `let sq = Rectangle::square(3);` ist ein Beispiel. Diese
Funktion liegt im Namensraum des Structs: Die Syntax `::` wird sowohl für
assoziierte Funktionen als auch für Namensräume verwendet, die durch Module
erzeugt werden. Module besprechen wir in [Kapitel 7][modules]<!-- ignore -->.

### Mehrere `impl`-Blöcke {#multiple-impl-blocks}

Jedes Struct darf mehrere `impl`-Blöcke haben. Listing 5-15 entspricht zum
Beispiel dem Code in Listing 5-16, in dem jede Methode in ihrem eigenen
`impl`-Block steht.

<Listing number="5-16" caption="Listing 5-15 mit mehreren `impl`-Blöcken umgeschrieben">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-16/src/main.rs:here}}
```

</Listing>

Hier gibt es keinen Grund, diese Methoden auf mehrere `impl`-Blöcke aufzuteilen,
aber die Syntax ist gültig. Einen Fall, in dem mehrere `impl`-Blöcke nützlich
sind, sehen wir in Kapitel 10, wo wir generische Typen und Traits besprechen.

### Methodenaufrufe sind syntaktischer Zucker für Funktionsaufrufe {#method-calls-are-syntactic-sugar-for-function-calls}

Mit den bisher besprochenen Konzepten können wir jetzt sehen, wie
Methodenaufrufe syntaktischer Zucker für Funktionsaufrufe sind. Angenommen, wir
haben ein Rechteck-Struct mit einer Methode `area` und einer Methode
`set_width`:

```rust,ignore
# struct Rectangle {
#     width: u32,
#     height: u32,
# }
# 
impl Rectangle {
    fn area(&self) -> u32 {
        self.width * self.height
    }

    fn set_width(&mut self, width: u32) {
        self.width = width;
    }
}
```

Und angenommen, wir haben ein Rechteck `r`. Dann sind die Methodenaufrufe
`r.area()` und `r.set_width(2)` gleichbedeutend mit Folgendem:

```rust
# struct Rectangle {
#     width: u32,
#     height: u32,
# }
# 
# impl Rectangle {
#     fn area(&self) -> u32 {
#        self.width * self.height
#      }
# 
#     fn set_width(&mut self, width: u32) {
#         self.width = width;
#     }
# }
# 
# fn main() {
let mut r = Rectangle { 
    width: 1,
    height: 2
};
let area1 = r.area();
let area2 = Rectangle::area(&r);
assert_eq!(area1, area2);

r.set_width(2);
Rectangle::set_width(&mut r, 2);
# }
```

Der Methodenaufruf `r.area()` wird zu `Rectangle::area(&r)`. Der Funktionsname
ist die assoziierte Funktion `Rectangle::area`. Das Funktionsargument ist der
Parameter `&self`. Rust fügt den Borrow-Operator `&` automatisch ein.

> _Hinweis:_ Wenn du C oder C++ kennst, bist du zwei verschiedene Syntaxformen
> für Methodenaufrufe gewohnt: `r.area()` und `r->area()`. Rust hat keine
> Entsprechung zum Pfeiloperator `->`. Wenn du den Punktoperator verwendest,
> referenziert und dereferenziert Rust den Empfänger der Methode automatisch.

Der Methodenaufruf `r.set_width(2)` wird entsprechend zu
`Rectangle::set_width(&mut r, 2)`. Diese Methode erwartet `&mut self`, also ist
das erste Argument ein veränderlicher Borrow `&mut r`. Das zweite Argument ist
genau dasselbe, die Zahl 2.

Wie wir in Kapitel 4.2
[„Das Dereferenzieren eines Zeigers greift auf seine Daten zu“](ch04-02-references-and-borrowing.html#dereferencing-a-pointer-accesses-its-data)
beschrieben haben, fügt Rust so viele Referenzen und Dereferenzierungen ein, wie
nötig sind, damit die Typen für den Parameter `self` zusammenpassen. Hier sind
zum Beispiel zwei gleichwertige Aufrufe von `area` für eine veränderliche
Referenz auf ein Rechteck in einer Box:

```rust
# struct Rectangle {
#     width: u32,
#     height: u32,
# }
# 
# impl Rectangle {
#     fn area(&self) -> u32 {
#        self.width * self.height
#      }
# 
#     fn set_width(&mut self, width: u32) {
#         self.width = width;
#     }
# }
# fn main() {
let r = &mut Box::new(Rectangle { 
    width: 1,
    height: 2
});
let area1 = r.area();
let area2 = Rectangle::area(&**r);
assert_eq!(area1, area2);
# }
```

Rust fügt zwei Dereferenzierungen hinzu (eine für die veränderliche Referenz,
eine für die Box) und dann einen unveränderlichen Borrow, weil `area`
`&Rectangle` erwartet. Beachte, dass auch hier eine veränderliche Referenz zu
einer geteilten Referenz „herabgestuft“ wird, wie wir es in
[Kapitel 4.2](ch04-02-references-and-borrowing.html#mutable-references-provide-unique-and-non-owning-access-to-data)
besprochen haben. Umgekehrt dürftest du `set_width` nicht auf einem Wert vom Typ
`&Rectangle` oder `&Box<Rectangle>` aufrufen.

{{#quiz ../quizzes/ch05-03-method-syntax-sec1.toml}}

### Methoden und Ownership {#methods-and-ownership}

Wie in Kapitel 4.2
[„Referenzen und Borrowing“](ch04-02-references-and-borrowing.html) besprochen,
müssen Methoden auf Structs aufgerufen werden, die die nötigen Berechtigungen
haben. Als durchgehendes Beispiel verwenden wir diese drei Methoden, die
`&self`, `&mut self` bzw. `self` nehmen.

```rust,ignore
impl Rectangle {    
    fn area(&self) -> u32 {
        self.width * self.height
    }

    fn set_width(&mut self, width: u32) {
        self.width = width;
    }

    fn max(self, other: Rectangle) -> Rectangle {
        Rectangle { 
            width: self.width.max(other.width),
            height: self.height.max(other.height),
        }
    }
}
```

#### Lesen und Schreiben mit `&self` und `&mut self` {#reads-and-writes-with-self-and-mut-self}

Wenn wir mit `let rect = Rectangle { ... }` ein Rechteck erzeugen, das seine
Daten besitzt, hat `rect` die Berechtigungen @Perm{read} und @Perm{own}. Mit
diesen Berechtigungen dürfen die Methoden `area` und `max` aufgerufen werden:

```aquascope,permissions,boundaries,stepper
#struct Rectangle {
#    width: u32,
#    height: u32,
#}
#impl Rectangle {    
#  fn area(&self) -> u32 {
#    self.width * self.height
#  }
#
#  fn set_width(&mut self, width: u32) {
#    self.width = width;
#  }
#
#  fn max(self, other: Self) -> Self {
#    let w = self.width.max(other.width);
#    let h = self.height.max(other.height);
#    Rectangle { 
#      width: w,
#      height: h
#    }
#  }
#}
#fn main() {
let rect = Rectangle {
    width: 0,
    height: 0
};`(focus,rxpaths:^rect$)`
println!("{}", rect.area());`{}`

let other_rect = Rectangle { width: 1, height: 1 };
let max_rect = rect.max(other_rect);`{}`
#}
```

Wenn wir jedoch versuchen, `set_width` aufzurufen, fehlt uns die Berechtigung
@Perm{write}:

```aquascope,permissions,boundaries,shouldFail
#struct Rectangle {
#    width: u32,
#    height: u32,
#}
#impl Rectangle {    
#  fn area(&self) -> u32 {
#    self.width * self.height
#  }
#
#  fn set_width(&mut self, width: u32) {
#    self.width = width;
#  }
#
#  fn max(self, other: Self) -> Self {
#    let w = self.width.max(other.width);
#    let h = self.height.max(other.height);
#    Rectangle { 
#      width: w,
#      height: h
#    }
#  }
#}
#fn main() {
let rect = Rectangle {
    width: 0,
    height: 0
};
rect.set_width(0);`{}`
#}
```

Rust weist dieses Programm mit dem entsprechenden Fehler zurück:

```text
error[E0596]: cannot borrow `rect` as mutable, as it is not declared as mutable
  --> test.rs:28:1
   |
24 | let rect = Rectangle {
   |     ---- help: consider changing this to be mutable: `mut rect`
...
28 | rect.set_width(0);
   | ^^^^^^^^^^^^^^^^^ cannot borrow as mutable
```

Einen ähnlichen Fehler bekommen wir, wenn wir versuchen, `set_width` auf einer
unveränderlichen Referenz auf ein `Rectangle` aufzurufen, selbst wenn das
zugrunde liegende Rechteck veränderlich ist:

```aquascope,permissions,boundaries,stepper,shouldFail
#struct Rectangle {
#    width: u32,
#    height: u32,
#}
#impl Rectangle {    
#  fn area(&self) -> u32 {
#    self.width * self.height
#  }
#
#  fn set_width(&mut self, width: u32) {
#    self.width = width;
#  }
#
#  fn max(self, other: Self) -> Self {
#    let w = self.width.max(other.width);
#    let h = self.height.max(other.height);
#    Rectangle { 
#      width: w,
#      height: h
#    }
#  }
#}
#fn main() {
// Added the mut keyword to the let-binding
let mut rect = Rectangle {
    width: 0,
    height: 0
};`(focus,rxpaths:^rect$)`
rect.set_width(1);`{}`     // this is now ok

let rect_ref = &rect;`(focus,rxpaths:^\*rect_ref$)`
rect_ref.set_width(2);`{}` // but this is still not ok
#}
```

#### Moves mit `self` {#moves-with-self}

Der Aufruf einer Methode, die `self` erwartet, verschiebt (_moves_) das
Eingabe-Struct (es sei denn, das Struct implementiert `Copy`). Wir können ein
`Rectangle` zum Beispiel nicht mehr verwenden, nachdem wir es an `max` übergeben
haben:

```aquascope,permissions,boundaries,stepper,shouldFail
#struct Rectangle {
#    width: u32,
#    height: u32,
#}
#impl Rectangle {    
#  fn area(&self) -> u32 {
#    self.width * self.height
#  }
#
#  fn set_width(&mut self, width: u32) {
#    self.width = width;
#  }
#
#  fn max(self, other: Self) -> Self {
#    let w = self.width.max(other.width);
#    let h = self.height.max(other.height);
#    Rectangle { 
#      width: w,
#      height: h
#    }
#  }
#}
#fn main() {
let rect = Rectangle {
    width: 0,
    height: 0
};`(focus,rxpaths:^rect$)`
let other_rect = Rectangle { 
    width: 1, 
    height: 1 
};
let max_rect = rect.max(other_rect);`(focus,rxpaths:^rect$)`
println!("{}", rect.area());`{}`
#}
```

Sobald wir `rect.max(..)` aufrufen, verschieben wir `rect` und verlieren damit
alle Berechtigungen darauf. Der Versuch, dieses Programm zu kompilieren, ergibt
folgenden Fehler:

```text
error[E0382]: borrow of moved value: `rect`
  --> test.rs:33:16
   |
24 | let rect = Rectangle {
   |     ---- move occurs because `rect` has type `Rectangle`, which does not implement the `Copy` trait
...
32 | let max_rect = rect.max(other_rect);
   |                     --------------- `rect` moved due to this method call
33 | println!("{}", rect.area());
   |                ^^^^^^^^^^^ value borrowed here after move
```

Eine ähnliche Situation entsteht, wenn wir versuchen, eine `self`-Methode auf
einer Referenz aufzurufen. Angenommen, wir wollen eine Methode `set_to_max`
schreiben, die `self` das Ergebnis von `self.max(..)` zuweist:

```aquascope,permissions,boundaries,stepper,shouldFail
#struct Rectangle {
#    width: u32,
#    height: u32,
#}
impl Rectangle {    
#  fn area(&self) -> u32 {
#    self.width * self.height
#  }
#
#  fn set_width(&mut self, width: u32) {
#    self.width = width;
#  }
#
#  fn max(self, other: Self) -> Self {
#    let w = self.width.max(other.width);
#    let h = self.height.max(other.height);
#    Rectangle { 
#      width: w,
#      height: h
#    }
#  }
    fn set_to_max(&mut self, other: Rectangle) {`(focus,rxpaths:^\*self$)`
        *self = self.max(other);`{}`
    }
}
```

Dann sehen wir, dass `self` in der Operation `self.max(..)` die Berechtigungen
@Perm{own} fehlen. Rust weist dieses Programm daher mit folgendem Fehler zurück:

```text
error[E0507]: cannot move out of `*self` which is behind a mutable reference
  --> test.rs:23:17
   |
23 |         *self = self.max(other);
   |                 ^^^^^----------
   |                 |    |
   |                 |    `*self` moved due to this method call
   |                 move occurs because `*self` has type `Rectangle`, which does not implement the `Copy` trait
   |
```

Das ist dieselbe Art von Fehler, die wir in Kapitel 4.3
[„Aus einer Collection kopieren oder verschieben“](ch04-03-fixing-ownership-errors.html#fixing-an-unsafe-program-copying-vs-moving-out-of-a-collection)
besprochen haben.

#### Gute Moves und schlechte Moves {#good-moves-and-bad-moves}

Vielleicht fragst du dich: Warum spielt es eine Rolle, ob wir aus `*self`
herausverschieben? Tatsächlich ist es im Fall von `Rectangle` sogar sicher, aus
`*self` herauszuverschieben, auch wenn Rust es dich nicht tun lässt. Wenn wir
zum Beispiel ein Programm simulieren, das das zurückgewiesene `set_to_max`
aufruft, siehst du, dass nichts Unsicheres passiert:

```aquascope,interpreter,shouldFail,horizontal
#struct Rectangle {
#    width: u32,
#    height: u32,
#}
impl Rectangle {    
#  fn max(self, other: Self) -> Self {
#    let w = self.width.max(other.width);
#    let h = self.height.max(other.height);
#    Rectangle { 
#      width: w,
#      height: h
#    }
#  }
    fn set_to_max(&mut self, other: Rectangle) {
        let max = self.max(other);`[]`
        *self = max;
    }
}

fn main() {
    let mut rect = Rectangle { width: 0, height: 1 };
    let other_rect = Rectangle { width: 1, height: 0 };`[]`
    rect.set_to_max(other_rect);`[]`
}
```

Es ist sicher, aus `*self` herauszuverschieben, weil `Rectangle` keine
Heap-Daten besitzt. Tatsächlich können wir Rust dazu bringen, `set_to_max` zu
kompilieren, indem wir der Definition von `Rectangle` einfach
`#[derive(Copy, Clone)]` hinzufügen:

```aquascope,permissions,boundaries,stepper
\#[derive(Copy, Clone)]
struct Rectangle {
    width: u32,
    height: u32,
}

impl Rectangle {    
#  fn max(self, other: Self) -> Self {
#    let w = self.width.max(other.width);
#    let h = self.height.max(other.height);
#    Rectangle { 
#      width: w,
#      height: h
#    }
#  }
    fn set_to_max(&mut self, other: Rectangle) {`(focus,rxpaths:^\*self$)`
        *self = self.max(other);`{}`
    }
}
```

Beachte, dass `self.max(other)` anders als vorher die Berechtigung @Perm{own}
weder auf `*self` noch auf `other` benötigt. Denk daran, dass `self.max(other)`
zu `Rectangle::max(*self, other)` aufgelöst wird. Die Dereferenzierung `*self`
erfordert keine Ownership über `*self`, wenn `Rectangle` kopierbar ist.

Vielleicht fragst du dich: Warum leitet Rust `Copy` für `Rectangle` nicht
automatisch ab? Rust leitet `Copy` nicht automatisch ab, damit APIs bei
Änderungen stabil bleiben. Stell dir vor, die Autorin des Typs `Rectangle`
beschließt, ein Feld `name: String` hinzuzufügen. Dann würde der Compiler
plötzlich jeden Client-Code zurückweisen, der sich darauf verlässt, dass
`Rectangle` `Copy` ist. Um dieses Problem zu vermeiden, müssen API-Autorinnen
und -Autoren `#[derive(Copy)]` explizit hinzufügen, um anzuzeigen, dass sie
erwarten, dass ihr Struct immer `Copy` ist.

Um das Problem besser zu verstehen, führen wir eine Simulation durch.
Angenommen, wir fügen `Rectangle` das Feld `name: String` hinzu. Was würde
passieren, wenn Rust `set_to_max` kompilieren ließe?

```aquascope,interpreter,shouldFail,horizontal
struct Rectangle {
    width: u32,
    height: u32,
    name: String,
}

impl Rectangle {    
#  fn max(self, other: Self) -> Self {
#    let w = self.width.max(other.width);
#    let h = self.height.max(other.height);
#    Rectangle { 
#      width: w,
#      height: h,
#      name: String::from("max")
#    }
#  }
    fn set_to_max(&mut self, other: Rectangle) {
        `[]`let max = self.max(other);`[]`
        drop(*self);`[]` // This is usually implicit,
                         // but added here for clarity.
        *self = max;
    }
}

fn main() {
    let mut r1 = Rectangle { 
        width: 9, 
        height: 9, 
        name: String::from("r1") 
    };
    let r2 = Rectangle {
        width: 16,
        height: 16,
        name: String::from("r2")
    };
    r1.set_to_max(r2);
}
```

In diesem Programm rufen wir `set_to_max` mit zwei Rechtecken `r1` und `r2` auf.
`self` ist eine veränderliche Referenz auf `r1`, und `other` ist ein Move von
`r2`. Nach dem Aufruf von `self.max(other)` übernimmt die Methode `max` die
Ownership beider Rechtecke. Wenn `max` zurückkehrt, gibt Rust beide Strings „r1“
und „r2“ auf dem Heap frei. Beachte das Problem: An der Stelle L2 soll `*self`
lesbar und beschreibbar sein. `(*self).name` (eigentlich `r1.name`) wurde jedoch
freigegeben.

Wenn wir also `*self = max` ausführen, tritt undefiniertes Verhalten auf. Wenn
wir `*self` überschreiben, verwirft (_drops_) Rust implizit die Daten, die
vorher in `*self` waren. Um dieses Verhalten explizit zu machen, haben wir
`drop(*self)` hinzugefügt. Nach dem Aufruf von `drop(*self)` versucht Rust,
`(*self).name` ein zweites Mal freizugeben. Das ist ein Double-Free und damit
undefiniertes Verhalten.

Merk dir also: Wenn du einen Fehler wie „cannot move out of `*self`“ siehst,
liegt das meist daran, dass du versuchst, eine `self`-Methode auf einer Referenz
wie `&self` oder `&mut self` aufzurufen. Rust schützt dich vor einem
Double-Free.

## Zusammenfassung {#summary}

Mit Structs kannst du eigene Typen erstellen, die für deinen Anwendungsbereich
sinnvoll sind. Mit Structs hältst du zusammengehörige Datenstücke beieinander
und benennst jedes Stück, um deinen Code klar zu machen. In `impl`-Blöcken
kannst du Funktionen definieren, die zu deinem Typ gehören, und Methoden sind
eine Art assoziierter Funktion, mit der du das Verhalten von Instanzen deiner
Structs festlegst.

Structs sind aber nicht die einzige Möglichkeit, eigene Typen zu erstellen:
Wenden wir uns dem Enum-Feature von Rust zu, um deinem Werkzeugkasten ein
weiteres Werkzeug hinzuzufügen.

{{#quiz ../quizzes/ch05-03-method-syntax-sec2.toml}}

[enums]: ch06-00-enums.html
[trait-objects]: ch18-02-trait-objects.md
[public]: ch07-03-paths-for-referring-to-an-item-in-the-module-tree.html#exposing-paths-with-the-pub-keyword
[modules]: ch07-02-defining-modules-to-control-scope-and-privacy.html
