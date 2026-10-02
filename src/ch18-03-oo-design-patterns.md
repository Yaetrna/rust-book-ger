## Ein objektorientiertes Design-Pattern implementieren {#implementing-an-object-oriented-design-pattern}

Das _State-Pattern_ ist ein objektorientiertes Design-Pattern. Der Kern dieses
Patterns besteht darin, dass wir eine Menge von Zuständen definieren, die ein
Wert intern haben kann. Die Zustände werden durch eine Menge von
_Zustandsobjekten_ dargestellt, und das Verhalten des Werts ändert sich je nach
seinem Zustand. Wir arbeiten ein Beispiel mit einem Struct für einen Blogbeitrag
durch, das ein Feld für seinen Zustand hat, der ein Zustandsobjekt aus der Menge
„Entwurf“, „Review“ oder „veröffentlicht“ sein wird.

Die Zustandsobjekte teilen sich Funktionalität: In Rust verwenden wir natürlich
Structs und Traits statt Objekten und Vererbung. Jedes Zustandsobjekt ist für
sein eigenes Verhalten verantwortlich und dafür, festzulegen, wann es in einen
anderen Zustand übergehen soll. Der Wert, der ein Zustandsobjekt enthält, weiß
nichts über das unterschiedliche Verhalten der Zustände oder darüber, wann
zwischen Zuständen gewechselt wird.

Der Vorteil des State-Patterns besteht darin, dass wir, wenn sich die
geschäftlichen Anforderungen an das Programm ändern, weder den Code des Werts,
der den Zustand enthält, noch den Code, der den Wert verwendet, ändern müssen.
Wir müssen nur den Code innerhalb eines der Zustandsobjekte aktualisieren, um
seine Regeln zu ändern oder vielleicht weitere Zustandsobjekte hinzuzufügen.

Zuerst implementieren wir das State-Pattern auf eine eher traditionelle
objektorientierte Weise. Dann verwenden wir einen Ansatz, der in Rust etwas
natürlicher ist. Legen wir los und implementieren wir schrittweise einen
Arbeitsablauf für Blogbeiträge mit dem State-Pattern.

Die fertige Funktionalität wird so aussehen:

1. Ein Blogbeitrag beginnt als leerer Entwurf.
1. Wenn der Entwurf fertig ist, wird ein Review des Beitrags angefordert.
1. Wenn der Beitrag genehmigt ist, wird er veröffentlicht.
1. Nur veröffentlichte Blogbeiträge geben Inhalt zum Ausgeben zurück, damit
   nicht genehmigte Beiträge nicht versehentlich veröffentlicht werden können.

Alle anderen Änderungsversuche an einem Beitrag sollen keine Wirkung haben. Wenn
wir zum Beispiel versuchen, einen Entwurf zu genehmigen, bevor wir ein Review
angefordert haben, soll der Beitrag ein unveröffentlichter Entwurf bleiben.

<!-- Old headings. Do not remove or links may break. -->

<a id="a-traditional-object-oriented-attempt"></a>

### Ein Versuch im traditionellen objektorientierten Stil {#attempting-traditional-object-oriented-style}

Es gibt unendlich viele Möglichkeiten, Code zu strukturieren, um dasselbe
Problem zu lösen, jede mit anderen Vor- und Nachteilen. Die Implementierung in
diesem Abschnitt folgt eher einem traditionellen objektorientierten Stil, den
man zwar in Rust schreiben kann, der aber einige Stärken von Rust nicht nutzt.
Später zeigen wir eine andere Lösung, die zwar weiterhin das objektorientierte
Design-Pattern verwendet, aber so strukturiert ist, dass sie Programmierern mit
objektorientierter Erfahrung vielleicht weniger vertraut vorkommt. Wir
vergleichen die beiden Lösungen, um die Vor- und Nachteile zu erleben, die es
mit sich bringt, Rust-Code anders zu entwerfen als Code in anderen Sprachen.

Listing 18-11 zeigt diesen Arbeitsablauf in Codeform: Es ist ein Beispiel für
die Verwendung der API, die wir in einem Library-Crate namens `blog`
implementieren werden. Das kompiliert noch nicht, weil wir den Crate `blog` noch
nicht implementiert haben.

<Listing number="18-11" file-name="src/main.rs" caption="Code, der das gewünschte Verhalten unseres Crates `blog` demonstriert">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch18-oop/listing-18-11/src/main.rs:all}}
```

</Listing>

Wir wollen es dem Benutzer ermöglichen, mit `Post::new` einen neuen Entwurf
eines Blogbeitrags zu erstellen. Wir wollen ermöglichen, dass dem Blogbeitrag
Text hinzugefügt wird. Wenn wir versuchen, den Inhalt des Beitrags sofort, also
vor der Genehmigung, abzurufen, sollten wir keinen Text bekommen, weil der
Beitrag noch ein Entwurf ist. Zu Demonstrationszwecken haben wir `assert_eq!` in
den Code eingefügt. Ein ausgezeichneter Unit-Test dafür wäre, zuzusichern, dass
ein Entwurf eines Blogbeitrags von der Methode `content` einen leeren String
zurückgibt, aber wir werden für dieses Beispiel keine Tests schreiben.

Als Nächstes wollen wir ermöglichen, ein Review des Beitrags anzufordern, und
wir wollen, dass `content` während des Wartens auf das Review einen leeren
String zurückgibt. Wenn der Beitrag genehmigt wird, soll er veröffentlicht
werden, das heißt, der Text des Beitrags wird zurückgegeben, wenn `content`
aufgerufen wird.

Beachte, dass der einzige Typ aus dem Crate, mit dem wir interagieren, der Typ
`Post` ist. Dieser Typ verwendet das State-Pattern und enthält einen Wert, der
eines von drei Zustandsobjekten ist, die die verschiedenen Zustände darstellen,
in denen sich ein Beitrag befinden kann – Entwurf, Review oder veröffentlicht.
Der Wechsel von einem Zustand in einen anderen wird intern innerhalb des Typs
`Post` verwaltet. Die Zustände ändern sich als Reaktion auf die Methoden, die
die Benutzer unserer Bibliothek auf der `Post`-Instanz aufrufen, aber sie müssen
die Zustandsänderungen nicht direkt verwalten. Außerdem können Benutzer bei den
Zuständen keinen Fehler machen, etwa einen Beitrag veröffentlichen, bevor er
überprüft wurde.

<!-- Old headings. Do not remove or links may break. -->

<a id="defining-post-and-creating-a-new-instance-in-the-draft-state"></a>

#### `Post` definieren und eine neue Instanz erzeugen {#defining-post-and-creating-a-new-instance}

Beginnen wir mit der Implementierung der Bibliothek! Wir wissen, dass wir ein
öffentliches Struct `Post` brauchen, das Inhalt enthält, also beginnen wir mit
der Definition des Structs und einer zugehörigen öffentlichen Funktion `new`, um
eine Instanz von `Post` zu erzeugen, wie in Listing 18-12 gezeigt. Außerdem
erstellen wir einen privaten Trait `State`, der das Verhalten definiert, das
alle Zustandsobjekte für einen `Post` haben müssen.

Dann enthält `Post` in einem privaten Feld namens `state` ein Trait-Objekt
`Box<dyn State>` innerhalb einer `Option<T>`, um das Zustandsobjekt aufzunehmen.
Warum die `Option<T>` nötig ist, wirst du gleich sehen.

<Listing number="18-12" file-name="src/lib.rs" caption="Definition eines Structs `Post` und einer Funktion `new`, die eine neue `Post`-Instanz erzeugt, eines Traits `State` und eines Structs `Draft`">

```rust,noplayground
{{#rustdoc_include ../listings/ch18-oop/listing-18-12/src/lib.rs}}
```

</Listing>

Der Trait `State` definiert das Verhalten, das verschiedene Zustände eines
Beitrags gemeinsam haben. Die Zustandsobjekte sind `Draft`, `PendingReview` und
`Published`, und sie alle werden den Trait `State` implementieren. Vorerst hat
der Trait keine Methoden, und wir beginnen damit, nur den Zustand `Draft` zu
definieren, weil das der Zustand ist, in dem ein Beitrag beginnen soll.

Wenn wir einen neuen `Post` erzeugen, setzen wir sein Feld `state` auf einen
`Some`-Wert, der eine `Box` enthält. Diese `Box` zeigt auf eine neue Instanz des
Structs `Draft`. Das stellt sicher, dass jede neue Instanz von `Post`, die wir
erzeugen, als Entwurf beginnt. Weil das Feld `state` von `Post` privat ist, gibt
es keine Möglichkeit, einen `Post` in einem anderen Zustand zu erzeugen! In der
Funktion `Post::new` setzen wir das Feld `content` auf einen neuen, leeren
`String`.

#### Den Text des Beitragsinhalts speichern {#storing-the-text-of-the-post-content}

In Listing 18-11 haben wir gesehen, dass wir eine Methode namens `add_text`
aufrufen und ihr einen `&str` übergeben können wollen, der dann als Textinhalt
des Blogbeitrags hinzugefügt wird. Wir implementieren das als Methode, statt das
Feld `content` als `pub` offenzulegen, damit wir später eine Methode
implementieren können, die steuert, wie die Daten des Felds `content` gelesen
werden. Die Methode `add_text` ist ziemlich einfach, also fügen wir die
Implementierung in Listing 18-13 zum Block `impl
Post` hinzu.

<Listing number="18-13" file-name="src/lib.rs" caption="Die Methode `add_text` implementieren, um dem `content` eines Beitrags Text hinzuzufügen">

```rust,noplayground
{{#rustdoc_include ../listings/ch18-oop/listing-18-13/src/lib.rs:here}}
```

</Listing>

Die Methode `add_text` nimmt eine veränderliche (_mutable_) Referenz auf `self`,
weil wir die `Post`-Instanz ändern, auf der wir `add_text` aufrufen. Dann rufen
wir `push_str` auf dem `String` in `content` auf und übergeben das Argument
`text`, um es zum gespeicherten `content` hinzuzufügen. Dieses Verhalten hängt
nicht vom Zustand ab, in dem sich der Beitrag befindet, und ist daher nicht Teil
des State-Patterns. Die Methode `add_text` interagiert überhaupt nicht mit dem
Feld `state`, gehört aber zu dem Verhalten, das wir unterstützen wollen.

<!-- Old headings. Do not remove or links may break. -->

<a id="ensuring-the-content-of-a-draft-post-is-empty"></a>

#### Sicherstellen, dass der Inhalt eines Entwurfs leer ist {#ensuring-that-the-content-of-a-draft-post-is-empty}

Auch nachdem wir `add_text` aufgerufen und unserem Beitrag Inhalt hinzugefügt
haben, soll die Methode `content` weiterhin einen leeren String-Slice
zurückgeben, weil sich der Beitrag noch im Entwurfszustand befindet, wie das
erste `assert_eq!` in Listing 18-11 zeigt. Implementieren wir die Methode
`content` vorerst mit dem Einfachsten, was diese Anforderung erfüllt: immer
einen leeren String-Slice zurückgeben. Das ändern wir später, sobald wir die
Möglichkeit implementieren, den Zustand eines Beitrags zu ändern, damit er
veröffentlicht werden kann. Bisher können sich Beiträge nur im Entwurfszustand
befinden, daher sollte der Inhalt des Beitrags immer leer sein. Listing 18-14
zeigt diese Platzhalter-Implementierung.

<Listing number="18-14" file-name="src/lib.rs" caption="Eine Platzhalter-Implementierung der Methode `content` für `Post` hinzufügen, die immer einen leeren String-Slice zurückgibt">

```rust,noplayground
{{#rustdoc_include ../listings/ch18-oop/listing-18-14/src/lib.rs:here}}
```

</Listing>

Mit dieser hinzugefügten Methode `content` funktioniert in Listing 18-11 alles
bis einschließlich des ersten `assert_eq!` wie beabsichtigt.

<!-- Old headings. Do not remove or links may break. -->

<a id="requesting-a-review-of-the-post-changes-its-state"></a>
<a id="requesting-a-review-changes-the-posts-state"></a>

#### Ein Review anfordern, was den Zustand des Beitrags ändert {#requesting-a-review-which-changes-the-posts-state}

Als Nächstes müssen wir Funktionalität hinzufügen, um ein Review eines Beitrags
anzufordern, was seinen Zustand von `Draft` auf `PendingReview` ändern soll.
Listing 18-15 zeigt diesen Code.

<Listing number="18-15" file-name="src/lib.rs" caption="Methoden `request_review` für `Post` und den Trait `State` implementieren">

```rust,noplayground
{{#rustdoc_include ../listings/ch18-oop/listing-18-15/src/lib.rs:here}}
```

</Listing>

Wir geben `Post` eine öffentliche Methode namens `request_review`, die eine
veränderliche Referenz auf `self` nimmt. Dann rufen wir eine interne Methode
`request_review` auf dem aktuellen Zustand von `Post` auf, und diese zweite
Methode `request_review` verbraucht den aktuellen Zustand und gibt einen neuen
Zustand zurück.

Wir fügen die Methode `request_review` zum Trait `State` hinzu; alle Typen, die
den Trait implementieren, müssen jetzt die Methode `request_review`
implementieren. Beachte, dass der erste Parameter der Methode nicht `self`,
`&self` oder `&mut self` ist, sondern `self: Box<Self>`. Diese Syntax bedeutet,
dass die Methode nur gültig ist, wenn sie auf einer `Box` aufgerufen wird, die
den Typ enthält. Diese Syntax übernimmt die Ownership an `Box<Self>` und macht
den alten Zustand ungültig, sodass sich der Zustandswert des `Post` in einen
neuen Zustand verwandeln kann.

Um den alten Zustand zu verbrauchen, muss die Methode `request_review` die
Ownership am Zustandswert übernehmen. Hier kommt die `Option` im Feld `state`
von `Post` ins Spiel: Wir rufen die Methode `take` auf, um den `Some`-Wert aus
dem Feld `state` herauszunehmen und an seiner Stelle ein `None` zu hinterlassen,
weil Rust keine unbesetzten Felder in Structs zulässt. So können wir den Wert
`state` aus `Post` herausverschieben (_move_), statt ihn auszuleihen
(_borrowing_). Dann setzen wir den `state`-Wert des Beitrags auf das Ergebnis
dieser Operation.

Wir müssen `state` vorübergehend auf `None` setzen, statt es direkt mit Code wie
`self.state = self.state.request_review();` zu setzen, um die Ownership am Wert
`state` zu bekommen. Das stellt sicher, dass `Post` den alten `state`-Wert nicht
mehr verwenden kann, nachdem wir ihn in einen neuen Zustand verwandelt haben.

Die Methode `request_review` von `Draft` gibt eine neue, in eine Box gelegte
Instanz eines neuen Structs `PendingReview` zurück, das den Zustand darstellt,
in dem ein Beitrag auf ein Review wartet. Das Struct `PendingReview`
implementiert ebenfalls die Methode `request_review`, führt aber keine
Verwandlung durch. Stattdessen gibt es sich selbst zurück, denn wenn wir für
einen Beitrag, der sich bereits im Zustand `PendingReview` befindet, ein Review
anfordern, soll er im Zustand `PendingReview` bleiben.

Jetzt sehen wir allmählich die Vorteile des State-Patterns: Die Methode
`request_review` von `Post` ist unabhängig von ihrem `state`-Wert dieselbe.
Jeder Zustand ist für seine eigenen Regeln verantwortlich.

Wir lassen die Methode `content` von `Post` unverändert, sodass sie einen leeren
String-Slice zurückgibt. Wir können jetzt einen `Post` sowohl im Zustand
`PendingReview` als auch im Zustand `Draft` haben, wollen aber im Zustand
`PendingReview` dasselbe Verhalten. Listing 18-11 funktioniert jetzt bis zum
zweiten Aufruf von `assert_eq!`!

<!-- Old headings. Do not remove or links may break. -->

<a id="adding-the-approve-method-that-changes-the-behavior-of-content"></a>
<a id="adding-approve-to-change-the-behavior-of-content"></a>

#### `approve` hinzufügen, um das Verhalten von `content` zu ändern {#adding-approve-to-change-contents-behavior}

Die Methode `approve` ähnelt der Methode `request_review`: Sie setzt `state` auf
den Wert, den der aktuelle Zustand laut eigener Aussage haben soll, wenn dieser
Zustand genehmigt wird, wie in Listing 18-16 gezeigt.

<Listing number="18-16" file-name="src/lib.rs" caption="Die Methode `approve` für `Post` und den Trait `State` implementieren">

```rust,noplayground
{{#rustdoc_include ../listings/ch18-oop/listing-18-16/src/lib.rs:here}}
```

</Listing>

Wir fügen die Methode `approve` zum Trait `State` hinzu und fügen ein neues
Struct hinzu, das `State` implementiert: den Zustand `Published`.

Ähnlich wie `request_review` bei `PendingReview` funktioniert, hat der Aufruf
der Methode `approve` auf einem `Draft` keine Wirkung, weil `approve` `self`
zurückgibt. Wenn wir `approve` auf `PendingReview` aufrufen, gibt es eine neue,
in eine Box gelegte Instanz des Structs `Published` zurück. Das Struct
`Published` implementiert den Trait `State` und gibt sowohl bei der Methode
`request_review` als auch bei der Methode `approve` sich selbst zurück, weil der
Beitrag in diesen Fällen im Zustand `Published` bleiben soll.

Jetzt müssen wir die Methode `content` von `Post` aktualisieren. Der von
`content` zurückgegebene Wert soll vom aktuellen Zustand des `Post` abhängen,
also lassen wir den `Post` an eine Methode `content` delegieren, die für seinen
`state` definiert ist, wie in Listing 18-17 gezeigt.

<Listing number="18-17" file-name="src/lib.rs" caption="Die Methode `content` von `Post` so aktualisieren, dass sie an eine Methode `content` von `State` delegiert">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch18-oop/listing-18-17/src/lib.rs:here}}
```

</Listing>

Weil das Ziel darin besteht, all diese Regeln innerhalb der Structs zu halten,
die `State` implementieren, rufen wir eine Methode `content` auf dem Wert in
`state` auf und übergeben die Beitragsinstanz (also `self`) als Argument. Dann
geben wir den Wert zurück, den die Methode `content` auf dem `state`-Wert
liefert.

Wir rufen die Methode `as_ref` auf der `Option` auf, weil wir eine Referenz auf
den Wert innerhalb der `Option` wollen statt der Ownership am Wert. Weil `state`
eine `Option<Box<dyn State>>` ist, wird beim Aufruf von `as_ref` eine
`Option<&Box<dyn
State>>` zurückgegeben. Würden wir `as_ref` nicht aufrufen,
bekämen wir einen Fehler, weil wir `state` nicht aus dem ausgeliehenen `&self`
des Funktionsparameters herausverschieben können.

Dann rufen wir die Methode `unwrap` auf, von der wir wissen, dass sie nie einen
Panic auslöst, weil wir wissen, dass die Methoden von `Post` sicherstellen, dass
`state` immer einen `Some`-Wert enthält, wenn diese Methoden fertig sind. Das
ist einer der Fälle, über die wir im Abschnitt
[„Wenn du mehr Informationen hast als
der Compiler“][more-info-than-rustc]<!-- ignore --> in Kapitel 9 gesprochen
haben, in denen wir wissen, dass ein `None`-Wert nie möglich ist, obwohl der
Compiler das nicht verstehen kann.

Wenn wir an diesem Punkt `content` auf der `&Box<dyn State>` aufrufen, greift
die Deref-Coercion für `&` und `Box`, sodass die Methode `content` letztlich auf
dem Typ aufgerufen wird, der den Trait `State` implementiert. Das bedeutet, dass
wir `content` zur Definition des Traits `State` hinzufügen müssen, und dort
bringen wir die Logik dafür unter, welcher Inhalt je nach Zustand zurückgegeben
wird, wie in Listing 18-18 gezeigt.

<Listing number="18-18" file-name="src/lib.rs" caption="Die Methode `content` zum Trait `State` hinzufügen">

```rust,noplayground
{{#rustdoc_include ../listings/ch18-oop/listing-18-18/src/lib.rs:here}}
```

</Listing>

Wir fügen eine Standardimplementierung für die Methode `content` hinzu, die
einen leeren String-Slice zurückgibt. Dadurch müssen wir `content` für die
Structs `Draft` und `PendingReview` nicht implementieren. Das Struct `Published`
überschreibt die Methode `content` und gibt den Wert in `post.content` zurück.
Es ist zwar bequem, dass die Methode `content` von `State` den Inhalt des `Post`
bestimmt, aber dadurch verschwimmen die Grenzen zwischen der Verantwortung von
`State` und der von `Post`.

Beachte, dass wir für diese Methode Lifetime-Annotationen brauchen, wie wir in
Kapitel 10 besprochen haben. Wir nehmen eine Referenz auf einen `post` als
Argument und geben eine Referenz auf einen Teil dieses `post` zurück, daher
hängt die Lifetime der zurückgegebenen Referenz mit der Lifetime des Arguments
`post` zusammen.

Und wir sind fertig – Listing 18-11 funktioniert jetzt vollständig! Wir haben
das State-Pattern mit den Regeln für den Arbeitsablauf von Blogbeiträgen
implementiert. Die Logik, die zu den Regeln gehört, befindet sich in den
Zustandsobjekten, statt über ganz `Post` verstreut zu sein.

> ### Warum kein Enum? {#why-not-an-enum}
>
> Vielleicht hast du dich gefragt, warum wir kein Enum mit den verschiedenen
> möglichen Zuständen eines Beitrags als Varianten verwendet haben. Das ist
> sicherlich eine mögliche Lösung; probiere sie aus und vergleiche die
> Endergebnisse, um zu sehen, was dir lieber ist! Ein Nachteil eines Enums ist,
> dass an jeder Stelle, die den Wert des Enums prüft, ein `match`-Ausdruck oder
> etwas Ähnliches nötig ist, um jede mögliche Variante zu behandeln. Das könnte
> sich mehr wiederholen als diese Lösung mit Trait-Objekten.

<!-- Old headings. Do not remove or links may break. -->

<a id="trade-offs-of-the-state-pattern"></a>

#### Das State-Pattern bewerten {#evaluating-the-state-pattern}

Wir haben gezeigt, dass Rust in der Lage ist, das objektorientierte
State-Pattern zu implementieren, um die verschiedenen Arten von Verhalten zu
kapseln, die ein Beitrag in jedem Zustand haben soll. Die Methoden von `Post`
wissen nichts über die verschiedenen Verhaltensweisen. Durch die Art, wie wir
den Code organisiert haben, müssen wir nur an einer einzigen Stelle nachsehen,
um zu wissen, wie sich ein veröffentlichter Beitrag verhalten kann: in der
Implementierung des Traits `State` für das Struct `Published`.

Würden wir eine alternative Implementierung erstellen, die das State-Pattern
nicht verwendet, würden wir stattdessen vielleicht `match`-Ausdrücke in den
Methoden von `Post` oder sogar im Code von `main` verwenden, die den Zustand des
Beitrags prüfen und an diesen Stellen das Verhalten ändern. Dann müssten wir an
mehreren Stellen nachsehen, um alle Auswirkungen davon zu verstehen, dass sich
ein Beitrag im veröffentlichten Zustand befindet.

Mit dem State-Pattern brauchen die Methoden von `Post` und die Stellen, an denen
wir `Post` verwenden, keine `match`-Ausdrücke, und um einen neuen Zustand
hinzuzufügen, müssten wir nur ein neues Struct hinzufügen und die Trait-Methoden
für dieses eine Struct an einer einzigen Stelle implementieren.

Die Implementierung mit dem State-Pattern lässt sich leicht um weitere
Funktionalität erweitern. Um zu sehen, wie einfach die Wartung von Code ist, der
das State-Pattern verwendet, probiere einige dieser Vorschläge aus:

- Füge eine Methode `reject` hinzu, die den Zustand des Beitrags von
  `PendingReview` zurück auf `Draft` ändert.
- Verlange zwei Aufrufe von `approve`, bevor der Zustand auf `Published`
  geändert werden kann.
- Erlaube Benutzern, Textinhalt nur hinzuzufügen, wenn sich ein Beitrag im
  Zustand `Draft` befindet. Tipp: Mach das Zustandsobjekt dafür verantwortlich,
  was sich am Inhalt ändern darf, aber nicht dafür, den `Post` zu verändern.

Ein Nachteil des State-Patterns ist, dass einige der Zustände miteinander
gekoppelt sind, weil die Zustände die Übergänge zwischen den Zuständen
implementieren. Wenn wir zwischen `PendingReview` und `Published` einen weiteren
Zustand wie `Scheduled` hinzufügen, müssten wir den Code in `PendingReview`
ändern, damit er stattdessen zu `Scheduled` übergeht. Es wäre weniger Arbeit,
wenn sich `PendingReview` beim Hinzufügen eines neuen Zustands nicht ändern
müsste, aber das würde bedeuten, zu einem anderen Design-Pattern zu wechseln.

Ein weiterer Nachteil ist, dass wir einige Logik dupliziert haben. Um einen Teil
der Duplizierung zu beseitigen, könnten wir versuchen, für die Methoden
`request_review` und `approve` im Trait `State` Standardimplementierungen zu
erstellen, die `self` zurückgeben. Das würde jedoch nicht funktionieren: Wenn
`State` als Trait-Objekt verwendet wird, weiß der Trait nicht, was das konkrete
`self` genau sein wird, daher ist der Rückgabetyp zur Kompilierzeit nicht
bekannt. (Das ist eine der zuvor erwähnten Regeln zur dyn-Kompatibilität.)

Weitere Duplizierung sind die ähnlichen Implementierungen der Methoden
`request_review` und `approve` von `Post`. Beide Methoden verwenden
`Option::take` mit dem Feld `state` von `Post`, und wenn `state` ein `Some` ist,
delegieren sie an die Implementierung derselben Methode des umhüllten Werts und
setzen den neuen Wert des Felds `state` auf das Ergebnis. Hätten wir viele
Methoden auf `Post`, die diesem Schema folgen, könnten wir in Betracht ziehen,
ein Makro zu definieren, um die Wiederholung zu beseitigen (siehe den Abschnitt
[„Makros“][macros]<!-- ignore --> in Kapitel 20).

Indem wir das State-Pattern genau so implementieren, wie es für
objektorientierte Sprachen definiert ist, nutzen wir die Stärken von Rust nicht
so vollständig, wie wir könnten. Sehen wir uns einige Änderungen am Crate `blog`
an, mit denen sich ungültige Zustände und Übergänge in Kompilierzeitfehler
verwandeln lassen.

### Zustände und Verhalten als Typen kodieren {#encoding-states-and-behavior-as-types}

Wir zeigen dir, wie man das State-Pattern neu denken kann, um andere Vor- und
Nachteile zu erhalten. Statt die Zustände und Übergänge vollständig zu kapseln,
sodass externer Code nichts von ihnen weiß, kodieren wir die Zustände in
verschiedene Typen. Folglich verhindert das Typprüfungssystem von Rust Versuche,
Entwürfe dort zu verwenden, wo nur veröffentlichte Beiträge erlaubt sind, indem
es einen Compilerfehler ausgibt.

Betrachten wir den ersten Teil von `main` in Listing 18-11:

<Listing file-name="src/main.rs">

```rust,ignore
{{#rustdoc_include ../listings/ch18-oop/listing-18-11/src/main.rs:here}}
```

</Listing>

Wir ermöglichen weiterhin, mit `Post::new` neue Beiträge im Entwurfszustand zu
erstellen und dem Inhalt des Beitrags Text hinzuzufügen. Aber statt eine Methode
`content` für einen Entwurf zu haben, die einen leeren String zurückgibt, sorgen
wir dafür, dass Entwürfe die Methode `content` überhaupt nicht haben. Wenn wir
dann versuchen, den Inhalt eines Entwurfs abzurufen, bekommen wir einen
Compilerfehler, der uns sagt, dass die Methode nicht existiert. Dadurch ist es
für uns unmöglich, versehentlich den Inhalt eines Entwurfs im Produktivbetrieb
anzuzeigen, weil dieser Code nicht einmal kompiliert. Listing 18-19 zeigt die
Definition eines Structs `Post` und eines Structs `DraftPost` sowie die Methoden
beider.

<Listing number="18-19" file-name="src/lib.rs" caption="Ein `Post` mit einer Methode `content` und ein `DraftPost` ohne Methode `content`">

```rust,noplayground
{{#rustdoc_include ../listings/ch18-oop/listing-18-19/src/lib.rs}}
```

</Listing>

Sowohl das Struct `Post` als auch das Struct `DraftPost` haben ein privates Feld
`content`, das den Text des Blogbeitrags speichert. Die Structs haben kein Feld
`state` mehr, weil wir die Kodierung des Zustands in die Typen der Structs
verlagern. Das Struct `Post` stellt einen veröffentlichten Beitrag dar und hat
eine Methode `content`, die den `content` zurückgibt.

Wir haben weiterhin eine Funktion `Post::new`, aber statt einer Instanz von
`Post` gibt sie eine Instanz von `DraftPost` zurück. Weil `content` privat ist
und es keine Funktionen gibt, die `Post` zurückgeben, ist es momentan nicht
möglich, eine Instanz von `Post` zu erzeugen.

Das Struct `DraftPost` hat eine Methode `add_text`, sodass wir wie bisher Text
zu `content` hinzufügen können, aber beachte, dass für `DraftPost` keine Methode
`content` definiert ist! Das Programm stellt jetzt also sicher, dass alle
Beiträge als Entwürfe beginnen und der Inhalt von Entwürfen nicht zur Anzeige
verfügbar ist. Jeder Versuch, diese Einschränkungen zu umgehen, führt zu einem
Compilerfehler.

<!-- Old headings. Do not remove or links may break. -->

<a id="implementing-transitions-as-transformations-into-different-types"></a>

Wie bekommen wir also einen veröffentlichten Beitrag? Wir wollen die Regel
durchsetzen, dass ein Entwurf überprüft und genehmigt werden muss, bevor er
veröffentlicht werden kann. Ein Beitrag im Zustand „Review ausstehend“ soll
weiterhin keinen Inhalt anzeigen. Implementieren wir diese Einschränkungen,
indem wir ein weiteres Struct `PendingReviewPost` hinzufügen, die Methode
`request_review` für `DraftPost` so definieren, dass sie einen
`PendingReviewPost` zurückgibt, und eine Methode `approve` für
`PendingReviewPost` definieren, die einen `Post` zurückgibt, wie in Listing
18-20 gezeigt.

<Listing number="18-20" file-name="src/lib.rs" caption="Ein `PendingReviewPost`, der durch Aufruf von `request_review` auf `DraftPost` erzeugt wird, und eine Methode `approve`, die einen `PendingReviewPost` in einen veröffentlichten `Post` verwandelt">

```rust,noplayground
{{#rustdoc_include ../listings/ch18-oop/listing-18-20/src/lib.rs:here}}
```

</Listing>

Die Methoden `request_review` und `approve` übernehmen die Ownership an `self`,
verbrauchen damit die Instanzen von `DraftPost` und `PendingReviewPost` und
verwandeln sie in einen `PendingReviewPost` bzw. einen veröffentlichten `Post`.
Auf diese Weise bleiben keine `DraftPost`-Instanzen übrig, nachdem wir
`request_review` auf ihnen aufgerufen haben, und so weiter. Für das Struct
`PendingReviewPost` ist keine Methode `content` definiert, daher führt der
Versuch, seinen Inhalt zu lesen, zu einem Compilerfehler, genau wie bei
`DraftPost`. Weil die einzige Möglichkeit, eine veröffentlichte `Post`-Instanz
zu bekommen, für die eine Methode `content` definiert ist, darin besteht, die
Methode `approve` auf einem `PendingReviewPost` aufzurufen, und die einzige
Möglichkeit, einen `PendingReviewPost` zu bekommen, darin besteht, die Methode
`request_review` auf einem `DraftPost` aufzurufen, haben wir den Arbeitsablauf
für Blogbeiträge jetzt im Typsystem kodiert.

Wir müssen aber auch einige kleine Änderungen an `main` vornehmen. Die Methoden
`request_review` und `approve` geben neue Instanzen zurück, statt das Struct zu
verändern, auf dem sie aufgerufen werden, daher müssen wir weitere
`let post =`-Zuweisungen mit Shadowing hinzufügen, um die zurückgegebenen
Instanzen zu speichern. Außerdem können wir die Zusicherungen, dass der Inhalt
von Entwürfen und Beiträgen mit ausstehendem Review leere Strings sind, nicht
mehr haben, und wir brauchen sie auch nicht: Code, der versucht, den Inhalt von
Beiträgen in diesen Zuständen zu verwenden, können wir nicht mehr kompilieren.
Der aktualisierte Code in `main` ist in Listing 18-21 zu sehen.

<Listing number="18-21" file-name="src/main.rs" caption="Änderungen an `main`, um die neue Implementierung des Arbeitsablaufs für Blogbeiträge zu verwenden">

```rust,ignore
{{#rustdoc_include ../listings/ch18-oop/listing-18-21/src/main.rs}}
```

</Listing>

Die Änderungen, die wir an `main` vornehmen mussten, um `post` neu zuzuweisen,
bedeuten, dass diese Implementierung nicht mehr ganz dem objektorientierten
State-Pattern folgt: Die Verwandlungen zwischen den Zuständen sind nicht mehr
vollständig innerhalb der Implementierung von `Post` gekapselt. Unser Gewinn ist
jedoch, dass ungültige Zustände jetzt dank des Typsystems und der Typprüfung zur
Kompilierzeit unmöglich sind! Das stellt sicher, dass bestimmte Bugs, etwa die
Anzeige des Inhalts eines unveröffentlichten Beitrags, entdeckt werden, bevor
sie in den Produktivbetrieb gelangen.

Probiere die zu Beginn dieses Abschnitts vorgeschlagenen Aufgaben mit dem Crate
`blog` in dem Stand aus, den er nach Listing 18-21 hat, um zu sehen, was du vom
Design dieser Version des Codes hältst. Beachte, dass manche Aufgaben in diesem
Design vielleicht schon erledigt sind.

Wir haben gesehen, dass Rust zwar objektorientierte Design-Patterns
implementieren kann, in Rust aber auch andere Patterns zur Verfügung stehen,
etwa das Kodieren von Zuständen im Typsystem. Diese Patterns haben andere Vor-
und Nachteile. Auch wenn dir objektorientierte Patterns sehr vertraut sein
mögen, kann es Vorteile bringen, das Problem neu zu durchdenken, um die Features
von Rust zu nutzen, etwa das Verhindern mancher Bugs zur Kompilierzeit.
Objektorientierte Patterns sind in Rust nicht immer die beste Lösung, weil Rust
bestimmte Features wie Ownership hat, die objektorientierte Sprachen nicht
haben.

## Zusammenfassung {#summary}

Unabhängig davon, ob du Rust nach der Lektüre dieses Kapitels für eine
objektorientierte Sprache hältst, weißt du jetzt, dass du Trait-Objekte
verwenden kannst, um in Rust einige objektorientierte Features zu bekommen.
Dynamischer Dispatch kann deinem Code etwas Flexibilität verleihen, im Tausch
gegen ein wenig Laufzeit-Performance. Du kannst diese Flexibilität nutzen, um
objektorientierte Patterns zu implementieren, die die Wartbarkeit deines Codes
verbessern können. Rust hat außerdem weitere Features wie Ownership, die
objektorientierte Sprachen nicht haben. Ein objektorientiertes Pattern ist nicht
immer der beste Weg, die Stärken von Rust zu nutzen, aber es ist eine verfügbare
Option.

Als Nächstes sehen wir uns Patterns an, die ein weiteres Feature von Rust sind,
das viel Flexibilität ermöglicht. Wir haben sie im Lauf des Buches kurz
betrachtet, aber ihre vollen Möglichkeiten noch nicht gesehen. Los geht’s!

{{#quiz ../quizzes/ch17-03-oo-design-patterns.toml}}

[more-info-than-rustc]: ch09-03-to-panic-or-not-to-panic.html#cases-in-which-you-have-more-information-than-the-compiler
[macros]: ch20-05-macros.html#macros
