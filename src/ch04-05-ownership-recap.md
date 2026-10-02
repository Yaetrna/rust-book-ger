## Rückblick auf Ownership {#ownership-recap}

Dieses Kapitel hat viele neue Konzepte eingeführt, etwa Ownership, Borrowing und Slices.
Wenn du mit Systemprogrammierung nicht vertraut bist, hat dieses Kapitel außerdem neue Konzepte wie Speicherallokation, Stack und Heap, Zeiger und undefiniertes Verhalten eingeführt. Bevor wir mit dem Rest von Rust weitermachen, halten wir kurz inne und atmen durch. Wir wiederholen und üben die zentralen Konzepte dieses Kapitels.

### Ownership im Vergleich zu Garbage-Collection {#ownership-versus-garbage-collection}

Um Ownership einzuordnen, sollten wir über **Garbage-Collection** sprechen.
Die meisten Programmiersprachen verwalten Speicher mit einem Garbage-Collector, etwa Python, JavaScript, Java und Go. Ein Garbage-Collector arbeitet zur Laufzeit neben dem laufenden Programm (zumindest ein Tracing-Collector). Der Collector durchsucht den Speicher nach Daten, die nicht mehr verwendet werden – das heißt, das laufende Programm kann diese Daten von keiner funktionslokalen Variable mehr erreichen. Dann gibt der Collector den ungenutzten Speicher zur späteren Verwendung frei.

Der wichtigste Vorteil eines Garbage-Collectors ist, dass er undefiniertes Verhalten (etwa die Verwendung freigegebenen Speichers) vermeidet, wie es in C oder C++ vorkommen kann. Garbage-Collection macht außerdem ein komplexes Typsystem zur Prüfung auf undefiniertes Verhalten überflüssig, wie es Rust hat. Garbage-Collection hat jedoch einige Nachteile. Ein offensichtlicher Nachteil ist die Performance, denn Garbage-Collection verursacht entweder häufigen kleinen Mehraufwand (bei Referenzzählung, wie in Python und Swift) oder seltenen großen Mehraufwand (beim Tracing, wie in allen anderen Sprachen mit Garbage-Collection).

Ein weiterer, weniger offensichtlicher Nachteil ist aber, dass **Garbage-Collection unvorhersehbar sein kann**. Um das zu veranschaulichen, nehmen wir an, wir implementieren einen Typ `Document`, der eine veränderliche (_mutable_) Liste von Wörtern darstellt. In einer Sprache mit Garbage-Collection wie Python könnten wir `Document` so implementieren:

```python
class Document:     
    def __init__(self, words: List[str]):
        """Create a new document"""
        self.words = words

    def add_word(self, word: str):
        """Add a word to the document"""
        self.words.append(word)
        
    def get_words(self) -> List[str]:  
        """Get a list of all the words in the document"""
        return self.words
```

Hier ist eine Möglichkeit, diese Klasse `Document` zu verwenden: Wir erzeugen ein Dokument `d`, kopieren es in ein neues Dokument `d2` und verändern dann `d2`.

```python
words = ["Hello"]
d = Document(words)

d2 = Document(d.get_words())
d2.add_word("world")
```

Betrachte zwei zentrale Fragen zu diesem Beispiel:

1. **Wann wird das Wort-Array freigegeben?**
   Dieses Programm hat drei Zeiger auf dasselbe Array erzeugt. Die Variablen `words`, `d` und `d2` enthalten alle einen Zeiger auf das auf dem Heap allozierte Wort-Array. Python gibt das Wort-Array deshalb erst frei, wenn alle drei Variablen ihren Gültigkeitsbereich (_scope_) verlassen haben. Allgemeiner gesagt ist es oft schwierig, allein durch Lesen des Quellcodes vorherzusagen, wo Daten von der Garbage-Collection eingesammelt werden.

2. **Was ist der Inhalt des Dokuments `d`?**
   Weil `d2` einen Zeiger auf dasselbe Wort-Array wie `d` enthält, verändert `d2.add_word("world")` auch das Dokument `d`. In diesem Beispiel sind die Wörter in `d` deshalb `["Hello", "world"]`. Das passiert, weil `d.get_words()` eine veränderliche Referenz auf das Wort-Array in `d` zurückgibt. Allgegenwärtige, implizite veränderliche Referenzen können leicht zu unvorhersehbaren Bugs führen, wenn Datenstrukturen ihr Innenleben nach außen geben können[^ownership-originally]. Hier ist es vermutlich nicht beabsichtigt, dass eine Änderung an `d2` auch `d` ändern kann.

Dieses Problem gibt es nicht nur in Python – ähnliches Verhalten kann dir in C#, Java, JavaScript und so weiter begegnen. Tatsächlich haben die meisten Programmiersprachen ein Konzept von Zeigern. Die Frage ist nur, wie die Sprache Zeiger für die Programmierenden sichtbar macht. Garbage-Collection macht es schwer zu erkennen, welche Variable auf welche Daten zeigt. Es war zum Beispiel nicht offensichtlich, dass `d.get_words()` einen Zeiger auf Daten innerhalb von `d` erzeugt.

Das Ownership-Modell von Rust stellt Zeiger dagegen in den Mittelpunkt. Das sehen wir, wenn wir den Typ `Document` in eine Rust-Datenstruktur übersetzen. Normalerweise würden wir ein `struct` verwenden, aber die haben wir noch nicht behandelt, also verwenden wir einfach einen Typalias:

```rust
type Document = Vec<String>;

fn new_document(words: Vec<String>) -> Document {
    words
}

fn add_word(this: &mut Document, word: String) {
    this.push(word);
}

fn get_words(this: &Document) -> &[String] {
    this.as_slice()
}
```

Diese Rust-API unterscheidet sich in einigen wesentlichen Punkten von der Python-API:

- Die Funktion `new_document` übernimmt die Ownership des Eingabevektors `words`. Das heißt, das `Document` _besitzt_ den Wortvektor. Der Wortvektor wird vorhersehbar freigegeben, wenn das `Document`, dem er gehört, seinen Gültigkeitsbereich verlässt.

- Die Funktion `add_word` verlangt eine veränderliche Referenz `&mut Document`, um ein Dokument verändern zu können. Sie übernimmt außerdem die Ownership der Eingabe `word`, sodass niemand sonst die einzelnen Wörter des Dokuments verändern kann.

- Die Funktion `get_words` gibt eine explizite unveränderliche (_immutable_) Referenz auf Strings innerhalb des Dokuments zurück. Die einzige Möglichkeit, aus diesem Wortvektor ein neues Dokument zu erzeugen, ist eine tiefe Kopie seines Inhalts, etwa so:

```rust,ignore
fn main() {
    let words = vec!["hello".to_string()];
    let d = new_document(words);

    // .to_vec() converts &[String] to Vec<String> by cloning each string
    let words_copy = get_words(&d).to_vec();
    let mut d2 = new_document(words_copy);
    add_word(&mut d2, "world".to_string());

    // The modification to `d2` does not affect `d`
    assert!(!get_words(&d).contains(&"world".into()));
}
```

Dieses Beispiel soll zeigen: Wenn Rust nicht deine erste Sprache ist, hast du bereits Erfahrung im Umgang mit Speicher und Zeigern! Rust macht diese Konzepte nur explizit. Das hat einen doppelten Vorteil: (1) Die Laufzeit-Performance verbessert sich, weil Garbage-Collection vermieden wird, und (2) die Vorhersehbarkeit verbessert sich, weil versehentliche „Lecks“ von Daten verhindert werden.

### Die Konzepte der Ownership {#the-concepts-of-ownership}

Wiederholen wir als Nächstes die Konzepte der Ownership. Diese Wiederholung fällt kurz aus – das Ziel ist, dich an die relevanten Konzepte zu erinnern. Wenn du merkst, dass du ein Konzept vergessen oder nicht verstanden hast, verweisen wir auf die passenden Kapitel, die du dir noch einmal ansehen kannst.

#### Ownership zur Laufzeit {#ownership-at-runtime}

Wir beginnen damit, zu wiederholen, wie Rust zur Laufzeit Speicher verwendet:

- Rust alloziert lokale Variablen in Stack-Frames, die beim Aufruf einer Funktion alloziert und am Ende des Aufrufs freigegeben werden.
- Lokale Variablen können entweder Daten (wie Zahlen, boolesche Werte, Tupel usw.) oder Zeiger enthalten.
- Zeiger können entweder über Boxen (Zeiger, die Daten auf dem Heap besitzen) oder über Referenzen (nicht-besitzende Zeiger) erzeugt werden.

Dieses Diagramm veranschaulicht, wie jedes Konzept zur Laufzeit aussieht:

```aquascope,interpreter,horizontal
fn main() {
  let mut a_num = 0;
  inner(&mut a_num);`[]`
}

fn inner(x: &mut i32) {
  let another_num = 1;
  let a_stack_ref = &another_num;

  let a_box = Box::new(2);  
  let a_box_stack_ref = &a_box;
  let a_box_heap_ref = &*a_box;`[]`

  *x += 5;
}
```

Sieh dir dieses Diagramm an und stell sicher, dass du jeden Teil verstehst. Du solltest zum Beispiel folgende Fragen beantworten können:

- Warum zeigt `a_box_stack_ref` auf den Stack, während `a_box_heap_ref` auf den Heap zeigt?
- Warum liegt der Wert `2` bei L2 nicht mehr auf dem Heap?
- Warum hat `a_num` bei L2 den Wert `5`?

Wenn du Boxen wiederholen willst, lies noch einmal [Kapitel 4.1][ch04-01]. Wenn du Referenzen wiederholen willst, lies noch einmal [Kapitel 4.2][ch04-02]. Wenn du Fallstudien mit Boxen und Referenzen sehen willst, lies noch einmal [Kapitel 4.3][ch04-03].

Slices sind eine besondere Art von Referenz, die auf eine zusammenhängende Folge von Daten im Speicher verweisen. Dieses Diagramm veranschaulicht, wie ein Slice auf eine Teilfolge der Zeichen eines Strings verweist:

```aquascope,interpreter
fn main() {
  let s = String::from("abcdefg");
  let s_slice = &s[2..5];`[]`
}
```

Wenn du Slices wiederholen willst, lies noch einmal [Kapitel 4.4][ch04-04].

#### Ownership zur Kompilierzeit {#ownership-at-compile-time}

Rust verfolgt für jede Variable die Berechtigungen @Perm{read} (Read, lesen), @Perm{write} (Write, schreiben) und @Perm{own} (Own, besitzen). Rust verlangt, dass eine Variable die passenden Berechtigungen für eine bestimmte Operation hat. Ein einfaches Beispiel: Wenn eine Variable nicht mit `let mut` deklariert ist, fehlt ihr die Berechtigung @Perm{write}, und sie kann nicht verändert werden:

```aquascope,permissions,stepper,boundaries,shouldFail
fn main() {
  let n = 0;
  n += 1;
}
```

Die Berechtigungen einer Variable können sich ändern, wenn sie **verschoben** (_moved_) oder **ausgeliehen** (_borrowed_) wird. Ein Move einer Variable mit einem nicht kopierbaren Typ (wie `Box<T>` oder `String`) erfordert die Berechtigungen @Perm{read}@Perm{own}, und der Move entzieht der Variable alle Berechtigungen. Diese Regel verhindert die Verwendung verschobener Variablen:

```aquascope,permissions,stepper,boundaries,shouldFail
fn main() {
  let s = String::from("Hello world");
  consume_a_string(s);
  println!("{s}"); // can't read `s` after moving it
}

fn consume_a_string(_s: String) {
  // om nom nom
}
```

Wenn du wiederholen willst, wie Moves funktionieren, lies noch einmal [Kapitel 4.1][ch04-01].

Eine Variable auszuleihen (also eine Referenz darauf zu erzeugen) entzieht ihr vorübergehend einige ihrer Berechtigungen. Ein unveränderlicher Borrow erzeugt eine unveränderliche Referenz und verhindert außerdem, dass die ausgeliehenen Daten verändert oder verschoben werden. Eine unveränderliche Referenz auszugeben, ist zum Beispiel in Ordnung:

```aquascope,permissions,stepper,boundaries
#fn main() {
let mut s = String::from("Hello");
let s_ref = &s;
println!("{s_ref}");
println!("{s}");
#}
```

Eine unveränderliche Referenz zu verändern, ist dagegen nicht in Ordnung:

```aquascope,permissions,stepper,boundaries,shouldFail
#fn main() {
let mut s = String::from("Hello");
let s_ref = &s;`(focus,paths:*s_ref)`
s_ref.push_str(" world");
println!("{s}");
#}
```

Die unveränderlich ausgeliehenen Daten zu verändern, ist ebenfalls nicht in Ordnung:

```aquascope,permissions,stepper,boundaries,shouldFail
#fn main() {
let mut s = String::from("Hello");`(focus)`
let s_ref = &s;`(focus,rxpaths:s$)`
s.push_str(" world");
println!("{s_ref}");
#}
```

Und Daten aus der Referenz herauszuverschieben, ist auch nicht in Ordnung:

```aquascope,permissions,stepper,boundaries,shouldFail
#fn main() {
let mut s = String::from("Hello");
let s_ref = &s;`(focus,paths:*s_ref)`
let s2 = *s_ref;
println!("{s}");
#}
```

Ein veränderlicher Borrow erzeugt eine veränderliche Referenz und verhindert, dass die ausgeliehenen Daten gelesen, geschrieben oder verschoben werden. Eine veränderliche Referenz zu verändern, ist zum Beispiel in Ordnung:

```aquascope,permissions,stepper,boundaries
#fn main() {
let mut s = String::from("Hello");
let s_ref = &mut s;
s_ref.push_str(" world");
println!("{s}");
#}
```

Auf die veränderlich ausgeliehenen Daten zuzugreifen, ist dagegen nicht in Ordnung:

```aquascope,permissions,stepper,boundaries,shouldFail
#fn main() {
let mut s = String::from("Hello");
let s_ref = &mut s;`(focus,rxpaths:s$)`
println!("{s}");
s_ref.push_str(" world");
#}
```

Wenn du Berechtigungen und Referenzen wiederholen willst, lies noch einmal [Kapitel 4.2][ch04-02].

#### Ownership zur Kompilierzeit und zur Laufzeit verbinden {#connecting-ownership-between-compile-time-and-runtime}

Die Berechtigungen von Rust sind darauf ausgelegt, undefiniertes Verhalten zu verhindern. Eine Art von undefiniertem Verhalten ist zum Beispiel ein **Use-after-free**, bei dem freigegebener Speicher gelesen oder beschrieben wird. Unveränderliche Borrows entziehen die Berechtigung @Perm{write}, um Use-after-free zu vermeiden, wie in diesem Fall:

```aquascope,interpreter,shouldFail,horizontal
#fn main() {
let mut v = vec![1, 2, 3];
let n = &v[0];`[]`
v.push(4);`[]`
println!("{n}");`[]`
#}
```

Eine andere Art von undefiniertem Verhalten ist ein **Double-Free**, bei dem Speicher zweimal freigegeben wird. Dereferenzierungen von Referenzen auf nicht kopierbare Daten haben nicht die Berechtigung @Perm{own}, um Double-Frees zu vermeiden, wie in diesem Fall:

```aquascope,interpreter,shouldFail,horizontal
#fn main() {
let v = vec![1, 2, 3];
let v_ref: &Vec<i32> = &v;
let v2 = *v_ref;`[]`
drop(v2);`[]`
drop(v);`[]`
#}
```

Wenn du undefiniertes Verhalten wiederholen willst, lies noch einmal [Kapitel 4.1][ch04-01] und [Kapitel 4.3][ch04-03].

### Der Rest der Ownership {#the-rest-of-ownership}

Wenn wir weitere Features wie Structs, Enums und Traits einführen, werden diese Features auf bestimmte Weise mit Ownership zusammenspielen. Dieses Kapitel liefert die grundlegende Basis, um dieses Zusammenspiel zu verstehen – die Konzepte Speicher, Zeiger, undefiniertes Verhalten und Berechtigungen werden uns helfen, in künftigen Kapiteln über die fortgeschritteneren Teile von Rust zu sprechen.

Und vergiss nicht, die Quiz zu machen, wenn du dein Verständnis überprüfen willst!

{{#quiz ../quizzes/ch04-05-ownership-recap.toml}}

[^ownership-originally]: Tatsächlich ging es bei der ursprünglichen Erfindung von Ownership-Typen gar nicht um Speichersicherheit. Es ging darum, in Java-ähnlichen Sprachen zu verhindern, dass veränderliche Referenzen auf das Innenleben von Datenstrukturen nach außen gelangen. Wenn du mehr über die Geschichte der Ownership-Typen erfahren willst, sieh dir den Artikel [„Ownership Types for Flexible Alias Protection“](https://dl.acm.org/doi/abs/10.1145/286936.286947) (Clarke et al. 1998) an.

[ch04-01]: ch04-01-what-is-ownership.html
[ch04-02]: ch04-02-references-and-borrowing.html
[ch04-03]: ch04-03-fixing-ownership-errors.html
[ch04-04]: ch04-04-slices.html
