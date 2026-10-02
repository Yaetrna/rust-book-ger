## Referenzzyklen können Speicherlecks verursachen {#reference-cycles-can-leak-memory}

Die Garantien von Rust zur Speichersicherheit machen es schwierig, aber nicht
unmöglich, versehentlich Speicher zu erzeugen, der nie aufgeräumt wird (ein
sogenanntes _Speicherleck_). Speicherlecks vollständig zu verhindern, gehört
nicht zu den Garantien von Rust, das heißt, Speicherlecks sind in Rust
speichersicher. Dass Rust Speicherlecks zulässt, sehen wir an `Rc<T>` und
`RefCell<T>`: Es ist möglich, Referenzen zu erzeugen, bei denen Elemente in
einem Zyklus aufeinander verweisen. Das erzeugt Speicherlecks, weil der
Referenzzähler jedes Elements im Zyklus nie 0 erreicht und die Werte nie
verworfen (_dropped_) werden.

### Einen Referenzzyklus erzeugen {#creating-a-reference-cycle}

Sehen wir uns an, wie ein Referenzzyklus entstehen kann und wie man ihn
verhindert. Wir beginnen mit der Definition des Enums `List` und einer Methode
`tail` in Listing 15-25.

<Listing number="15-25" file-name="src/main.rs" caption="Eine Cons-Listen-Definition, die eine `RefCell<T>` enthält, damit wir ändern können, worauf eine `Cons`-Variante verweist">

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-25/src/main.rs:here}}
```

</Listing>

Wir verwenden eine weitere Variante der Definition von `List` aus Listing 15-5.
Das zweite Element der Variante `Cons` ist jetzt `RefCell<Rc<List>>`. Das heißt,
statt den `i32`-Wert ändern zu können wie in Listing 15-24, wollen wir den
`List`-Wert ändern, auf den eine `Cons`-Variante zeigt. Außerdem fügen wir eine
Methode `tail` hinzu, damit wir bequem auf das zweite Element zugreifen können,
wenn wir eine `Cons`-Variante haben.

In Listing 15-26 fügen wir eine Funktion `main` hinzu, die die Definitionen aus
Listing 15-25 verwendet. Dieser Code erzeugt eine Liste in `a` und eine Liste in
`b`, die auf die Liste in `a` zeigt. Dann ändert er die Liste in `a` so, dass
sie auf `b` zeigt, wodurch ein Referenzzyklus entsteht. Unterwegs gibt es
`println!`-Anweisungen, die zeigen, wie hoch die Referenzzähler an verschiedenen
Stellen dieses Vorgangs sind.

<Listing number="15-26" file-name="src/main.rs" caption="Einen Referenzzyklus aus zwei `List`-Werten erzeugen, die aufeinander zeigen">

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-26/src/main.rs:here}}
```

</Listing>

Wir erzeugen in der Variable `a` eine `Rc<List>`-Instanz, die einen `List`-Wert
mit der anfänglichen Liste `5, Nil` enthält. Dann erzeugen wir in der Variable
`b` eine `Rc<List>`-Instanz mit einem weiteren `List`-Wert, der den Wert `10`
enthält und auf die Liste in `a` zeigt.

Wir ändern `a` so, dass es statt auf `Nil` auf `b` zeigt, wodurch ein Zyklus
entsteht. Dazu verwenden wir die Methode `tail`, um eine Referenz auf die
`RefCell<Rc<List>>` in `a` zu erhalten, die wir in die Variable `link` legen.
Dann verwenden wir die Methode `borrow_mut` auf der `RefCell<Rc<List>>`, um den
Wert darin von einem `Rc<List>`, das einen `Nil`-Wert enthält, in das `Rc<List>`
in `b` zu ändern.

Wenn wir diesen Code ausführen und das letzte `println!` vorerst auskommentiert
lassen, erhalten wir diese Ausgabe:

```console
{{#include ../listings/ch15-smart-pointers/listing-15-26/output.txt}}
```

Der Referenzzähler der `Rc<List>`-Instanzen in `a` und `b` ist 2, nachdem wir
die Liste in `a` so geändert haben, dass sie auf `b` zeigt. Am Ende von `main`
verwirft Rust die Variable `b`, wodurch der Referenzzähler der
`Rc<List>`-Instanz von `b` von 2 auf 1 sinkt. Der Speicher, den `Rc<List>` auf
dem Heap hat, wird an dieser Stelle nicht verworfen, weil sein Referenzzähler 1
und nicht 0 ist. Dann verwirft Rust `a`, wodurch auch der Referenzzähler der
`Rc<List>`-Instanz von `a` von 2 auf 1 sinkt. Auch der Speicher dieser Instanz
kann nicht verworfen werden, weil die andere `Rc<List>`-Instanz noch darauf
verweist. Der für die Liste allozierte Speicher bleibt für immer unaufgeräumt.
Um diesen Referenzzyklus zu veranschaulichen, haben wir das Diagramm in
Abbildung 15-4 erstellt.

<img alt="Ein mit ‚a‘ beschriftetes Rechteck, das auf ein Rechteck mit der Ganzzahl 5 zeigt. Ein mit ‚b‘ beschriftetes Rechteck, das auf ein Rechteck mit der Ganzzahl 10 zeigt. Das Rechteck mit der 5 zeigt auf das Rechteck mit der 10, und das Rechteck mit der 10 zeigt zurück auf das Rechteck mit der 5, wodurch ein Zyklus entsteht." src="img/trpl15-04.svg" class="center" />

<span class="caption">Abbildung 15-4: Ein Referenzzyklus der Listen `a` und `b`,
die aufeinander zeigen</span>

Wenn du das letzte `println!` wieder einkommentierst und das Programm ausführst,
versucht Rust, diesen Zyklus auszugeben, wobei `a` auf `b` zeigt, das auf `a`
zeigt, und so weiter, bis der Stack überläuft.

Im Vergleich zu einem echten Programm sind die Folgen eines Referenzzyklus in
diesem Beispiel nicht sehr schlimm: Direkt nachdem wir den Referenzzyklus
erzeugt haben, endet das Programm. Würde aber ein komplexeres Programm viel
Speicher in einem Zyklus allozieren und ihn lange behalten, würde das Programm
mehr Speicher verbrauchen als nötig und könnte das System überlasten, sodass ihm
der verfügbare Speicher ausgeht.

Referenzzyklen entstehen nicht leicht, aber sie sind auch nicht unmöglich. Hast
du `RefCell<T>`-Werte, die `Rc<T>`-Werte enthalten, oder ähnliche verschachtelte
Kombinationen von Typen mit innerer Veränderlichkeit und Referenzzählung, musst
du sicherstellen, dass du keine Zyklen erzeugst; du kannst dich nicht darauf
verlassen, dass Rust sie abfängt. Ein Referenzzyklus wäre ein Logikfehler in
deinem Programm, den du mit automatisierten Tests, Code-Reviews und anderen
Praktiken der Softwareentwicklung minimieren solltest.

Eine weitere Lösung, um Referenzzyklen zu vermeiden, ist, deine Datenstrukturen
so umzuorganisieren, dass manche Referenzen Ownership ausdrücken und manche
nicht. Dadurch kannst du Zyklen haben, die aus einigen Ownership-Beziehungen und
einigen Nicht-Ownership-Beziehungen bestehen, und nur die Ownership-Beziehungen
beeinflussen, ob ein Wert verworfen werden kann. In Listing 15-25 sollen
`Cons`-Varianten ihre Liste immer besitzen, daher ist ein Umorganisieren der
Datenstruktur nicht möglich. Sehen wir uns ein Beispiel mit Graphen aus
Elternknoten und Kindknoten an, um zu sehen, wann Nicht-Ownership-Beziehungen
ein angemessener Weg sind, Referenzzyklen zu verhindern.

<!-- Old headings. Do not remove or links may break. -->

<a id="preventing-reference-cycles-turning-an-rct-into-a-weakt"></a>

### Referenzzyklen mit `Weak<T>` verhindern {#preventing-reference-cycles-using-weakt}

Bisher haben wir gezeigt, dass der Aufruf von `Rc::clone` den `strong_count`
einer `Rc<T>`-Instanz erhöht und eine `Rc<T>`-Instanz nur aufgeräumt wird, wenn
ihr `strong_count` 0 ist. Du kannst auch eine schwache Referenz (_weak
reference_) auf den Wert in einer `Rc<T>`-Instanz erzeugen, indem du
`Rc::downgrade` aufrufst und eine Referenz auf das `Rc<T>` übergibst. Mit
_starken Referenzen_ kannst du die Ownership einer `Rc<T>`-Instanz teilen.
_Schwache Referenzen_ drücken keine Ownership-Beziehung aus, und ihre Anzahl
beeinflusst nicht, wann eine `Rc<T>`-Instanz aufgeräumt wird. Sie verursachen
keinen Referenzzyklus, weil jeder Zyklus, an dem schwache Referenzen beteiligt
sind, durchbrochen wird, sobald der Zähler starker Referenzen der beteiligten
Werte 0 ist.

Wenn du `Rc::downgrade` aufrufst, erhältst du einen Smart-Pointer vom Typ
`Weak<T>`. Statt den `strong_count` in der `Rc<T>`-Instanz um 1 zu erhöhen,
erhöht der Aufruf von `Rc::downgrade` den `weak_count` um 1. Der Typ `Rc<T>`
verwendet `weak_count`, um festzuhalten, wie viele `Weak<T>`-Referenzen
existieren, ähnlich wie `strong_count`. Der Unterschied ist, dass `weak_count`
nicht 0 sein muss, damit die `Rc<T>`-Instanz aufgeräumt wird.

Da der Wert, auf den `Weak<T>` verweist, bereits verworfen worden sein könnte,
musst du, um irgendetwas mit dem Wert zu tun, auf den ein `Weak<T>` zeigt,
sicherstellen, dass der Wert noch existiert. Das tust du, indem du auf einer
`Weak<T>`-Instanz die Methode `upgrade` aufrufst, die eine `Option<Rc<T>>`
zurückgibt. Du erhältst das Ergebnis `Some`, wenn der `Rc<T>`-Wert noch nicht
verworfen wurde, und das Ergebnis `None`, wenn der `Rc<T>`-Wert verworfen wurde.
Da `upgrade` eine `Option<Rc<T>>` zurückgibt, stellt Rust sicher, dass der Fall
`Some` und der Fall `None` behandelt werden, und es gibt keinen ungültigen
Zeiger.

Als Beispiel erzeugen wir statt einer Liste, deren Elemente nur das nächste
Element kennen, einen Baum, dessen Elemente ihre Kindelemente _und_ ihre
Elternelemente kennen.

<!-- Old headings. Do not remove or links may break. -->

<a id="creating-a-tree-data-structure-a-node-with-child-nodes"></a>

#### Eine Baum-Datenstruktur erzeugen {#creating-a-tree-data-structure}

Zuerst bauen wir einen Baum mit Knoten, die ihre Kindknoten kennen. Wir erzeugen
ein Struct namens `Node`, das seinen eigenen `i32`-Wert sowie Referenzen auf
seine Kind-`Node`-Werte enthält:

<span class="filename">Dateiname: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-27/src/main.rs:here}}
```

Ein `Node` soll seine Kinder besitzen, und wir wollen diese Ownership mit
Variablen teilen, damit wir direkt auf jeden `Node` im Baum zugreifen können.
Dazu definieren wir die Elemente des `Vec<T>` als Werte vom Typ `Rc<Node>`.
Außerdem wollen wir ändern können, welche Knoten Kinder eines anderen Knotens
sind, daher haben wir in `children` eine `RefCell<T>` um den `Vec<Rc<Node>>`.

Als Nächstes verwenden wir unsere Struct-Definition und erzeugen eine
`Node`-Instanz namens `leaf` mit dem Wert `3` und ohne Kinder sowie eine weitere
Instanz namens `branch` mit dem Wert `5` und `leaf` als einem ihrer Kinder, wie
in Listing 15-27 gezeigt.

<Listing number="15-27" file-name="src/main.rs" caption="Einen Knoten `leaf` ohne Kinder und einen Knoten `branch` mit `leaf` als einem seiner Kinder erzeugen">

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-27/src/main.rs:there}}
```

</Listing>

Wir klonen das `Rc<Node>` in `leaf` und speichern es in `branch`, das heißt, der
`Node` in `leaf` hat jetzt zwei Owner: `leaf` und `branch`. Wir können über
`branch.children` von `branch` zu `leaf` gelangen, aber es gibt keinen Weg von
`leaf` zu `branch`. Der Grund ist, dass `leaf` keine Referenz auf `branch` hat
und nicht weiß, dass sie zusammengehören. `leaf` soll wissen, dass `branch` sein
Elternknoten ist. Darum kümmern wir uns als Nächstes.

#### Eine Referenz vom Kind auf sein Elternelement hinzufügen {#adding-a-reference-from-a-child-to-its-parent}

Damit der Kindknoten seinen Elternknoten kennt, müssen wir unserer
Struct-Definition `Node` ein Feld `parent` hinzufügen. Die Schwierigkeit besteht
darin, zu entscheiden, welchen Typ `parent` haben soll. Wir wissen, dass es kein
`Rc<T>` enthalten kann, weil das einen Referenzzyklus erzeugen würde, bei dem
`leaf.parent` auf `branch` und `branch.children` auf `leaf` zeigt, wodurch ihre
`strong_count`-Werte nie 0 würden.

Betrachtet man die Beziehungen anders herum, sollte ein Elternknoten seine
Kinder besitzen: Wird ein Elternknoten verworfen, sollten auch seine Kindknoten
verworfen werden. Ein Kind sollte sein Elternelement aber nicht besitzen:
Verwerfen wir einen Kindknoten, sollte das Elternelement weiterhin existieren.
Das ist ein Fall für schwache Referenzen!

Statt `Rc<T>` verwenden wir für den Typ von `parent` also `Weak<T>`, genauer
gesagt eine `RefCell<Weak<Node>>`. Jetzt sieht unsere Struct-Definition `Node`
so aus:

<span class="filename">Dateiname: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-28/src/main.rs:here}}
```

Ein Knoten kann auf seinen Elternknoten verweisen, besitzt ihn aber nicht. In
Listing 15-28 passen wir `main` so an, dass es diese neue Definition verwendet,
damit der Knoten `leaf` eine Möglichkeit hat, auf seinen Elternknoten `branch`
zu verweisen.

<Listing number="15-28" file-name="src/main.rs" caption="Ein Knoten `leaf` mit einer schwachen Referenz auf seinen Elternknoten `branch`">

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-28/src/main.rs:there}}
```

</Listing>

Das Erzeugen des Knotens `leaf` sieht ähnlich aus wie in Listing 15-27,
abgesehen vom Feld `parent`: `leaf` beginnt ohne Elternknoten, daher erzeugen
wir eine neue, leere `Weak<Node>`-Referenzinstanz.

Wenn wir an dieser Stelle versuchen, mit der Methode `upgrade` eine Referenz auf
den Elternknoten von `leaf` zu erhalten, bekommen wir einen `None`-Wert. Das
sehen wir in der Ausgabe der ersten `println!`-Anweisung:

```text
leaf parent = None
```

Wenn wir den Knoten `branch` erzeugen, hat auch er eine neue
`Weak<Node>`-Referenz im Feld `parent`, weil `branch` keinen Elternknoten hat.
`leaf` ist weiterhin eines der Kinder von `branch`. Sobald wir die
`Node`-Instanz in `branch` haben, können wir `leaf` so ändern, dass es eine
`Weak<Node>`-Referenz auf seinen Elternknoten erhält. Wir verwenden die Methode
`borrow_mut` auf der `RefCell<Weak<Node>>` im Feld `parent` von `leaf` und dann
die Funktion `Rc::downgrade`, um aus dem `Rc<Node>` in `branch` eine
`Weak<Node>`-Referenz auf `branch` zu erzeugen.

Wenn wir den Elternknoten von `leaf` erneut ausgeben, erhalten wir diesmal eine
`Some`-Variante mit `branch`: Jetzt kann `leaf` auf seinen Elternknoten
zugreifen! Wenn wir `leaf` ausgeben, vermeiden wir außerdem den Zyklus, der in
Listing 15-26 schließlich in einem Stack-Überlauf endete; die
`Weak<Node>`-Referenzen werden als `(Weak)` ausgegeben:

```text
leaf parent = Some(Node { value: 5, parent: RefCell { value: (Weak) },
children: RefCell { value: [Node { value: 3, parent: RefCell { value: (Weak) },
children: RefCell { value: [] } }] } })
```

Das Fehlen einer unendlichen Ausgabe zeigt, dass dieser Code keinen
Referenzzyklus erzeugt hat. Das können wir auch an den Werten erkennen, die wir
durch Aufruf von `Rc::strong_count` und `Rc::weak_count` erhalten.

#### Änderungen von `strong_count` und `weak_count` veranschaulichen {#visualizing-changes-to-strong_count-and-weak_count}

Sehen wir uns an, wie sich die Werte `strong_count` und `weak_count` der
`Rc<Node>`-Instanzen ändern, indem wir einen neuen inneren Gültigkeitsbereich
(_scope_) erzeugen und das Erzeugen von `branch` in diesen Gültigkeitsbereich
verschieben. So sehen wir, was passiert, wenn `branch` erzeugt und dann beim
Verlassen des Gültigkeitsbereichs verworfen wird. Die Änderungen sind in Listing
15-29 gezeigt.

<Listing number="15-29" file-name="src/main.rs" caption="`branch` in einem inneren Gültigkeitsbereich erzeugen und die Zähler starker und schwacher Referenzen untersuchen">

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-29/src/main.rs:here}}
```

</Listing>

Nachdem `leaf` erzeugt wurde, hat sein `Rc<Node>` einen starken Zähler von 1 und
einen schwachen Zähler von 0. Im inneren Gültigkeitsbereich erzeugen wir
`branch` und verknüpfen es mit `leaf`. Geben wir an dieser Stelle die Zähler
aus, hat das `Rc<Node>` in `branch` einen starken Zähler von 1 und einen
schwachen Zähler von 1 (für `leaf.parent`, das mit einem `Weak<Node>` auf
`branch` zeigt). Geben wir die Zähler in `leaf` aus, sehen wir, dass es einen
starken Zähler von 2 hat, weil `branch` jetzt einen Klon des `Rc<Node>` von
`leaf` in `branch.children` gespeichert hat, aber weiterhin einen schwachen
Zähler von 0.

Wenn der innere Gültigkeitsbereich endet, verlässt `branch` den
Gültigkeitsbereich, und der starke Zähler des `Rc<Node>` sinkt auf 0, also wird
sein `Node` verworfen. Der schwache Zähler von 1 durch `leaf.parent` spielt
keine Rolle dafür, ob `Node` verworfen wird, also haben wir keine Speicherlecks!

Versuchen wir nach dem Ende des Gültigkeitsbereichs, auf den Elternknoten von
`leaf` zuzugreifen, erhalten wir wieder `None`. Am Ende des Programms hat das
`Rc<Node>` in `leaf` einen starken Zähler von 1 und einen schwachen Zähler von
0, weil die Variable `leaf` jetzt wieder die einzige Referenz auf das `Rc<Node>`
ist.

Die gesamte Logik zum Verwalten der Zähler und zum Verwerfen von Werten ist in
`Rc<T>` und `Weak<T>` und ihre Implementierungen des Traits `Drop` eingebaut.
Indem du in der Definition von `Node` festlegst, dass die Beziehung von einem
Kind zu seinem Elternelement eine `Weak<T>`-Referenz sein soll, können
Elternknoten auf Kindknoten zeigen und umgekehrt, ohne einen Referenzzyklus und
Speicherlecks zu erzeugen.

## Zusammenfassung {#summary}

Dieses Kapitel hat behandelt, wie man mit Smart-Pointern andere Garantien und
Kompromisse erreicht als die, die Rust standardmäßig mit normalen Referenzen
bietet. Der Typ `Box<T>` hat eine bekannte Größe und zeigt auf Daten, die auf
dem Heap alloziert sind. Der Typ `Rc<T>` hält die Zahl der Referenzen auf Daten
auf dem Heap fest, sodass die Daten mehrere Owner haben können. Der Typ
`RefCell<T>` mit seiner inneren Veränderlichkeit gibt uns einen Typ, den wir
verwenden können, wenn wir einen unveränderlichen (_immutable_) Typ brauchen,
aber einen inneren Wert dieses Typs ändern müssen; außerdem setzt er die
Borrowing-Regeln zur Laufzeit statt zur Kompilierzeit durch.

Besprochen haben wir auch die Traits `Deref` und `Drop`, die einen Großteil der
Funktionalität von Smart-Pointern ermöglichen. Wir haben Referenzzyklen
untersucht, die Speicherlecks verursachen können, und wie man sie mit `Weak<T>`
verhindert.

Wenn dieses Kapitel dein Interesse geweckt hat und du deine eigenen
Smart-Pointer implementieren willst, findest du weitere nützliche Informationen
im [„Rustonomicon“][nomicon].

Als Nächstes sprechen wir über Nebenläufigkeit in Rust. Dabei lernst du sogar
einige neue Smart-Pointer kennen.

{{#quiz ../quizzes/ch15-06-reference-cycles.toml}}

[nomicon]: https://doc.rust-lang.org/nomicon/index.html
