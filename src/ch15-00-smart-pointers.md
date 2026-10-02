# Smart-Pointer {#smart-pointers}

Ein Zeiger (_pointer_) ist ein allgemeines Konzept für eine Variable, die eine
Adresse im Speicher enthält. Diese Adresse verweist auf andere Daten oder
„zeigt“ auf sie. Die häufigste Art von Zeiger in Rust ist eine Referenz, die du
in Kapitel 4 kennengelernt hast. Referenzen werden durch das Symbol `&`
gekennzeichnet und leihen den Wert aus (_borrow_), auf den sie zeigen. Sie haben
außer dem Verweisen auf Daten keine besonderen Fähigkeiten und verursachen
keinen Mehraufwand.

_Smart-Pointer_ dagegen sind Datenstrukturen, die sich wie ein Zeiger verhalten,
aber zusätzliche Metadaten und Fähigkeiten haben. Das Konzept der Smart-Pointer
gibt es nicht nur in Rust: Smart-Pointer stammen aus C++ und existieren auch in
anderen Sprachen. Rust hat eine Reihe von Smart-Pointern in der
Standardbibliothek, die Funktionalität über die von Referenzen hinaus
bereitstellen. Um das allgemeine Konzept zu erkunden, sehen wir uns einige
verschiedene Beispiele für Smart-Pointer an, darunter einen Smart-Pointer-Typ
mit _Referenzzählung_ (_reference counting_). Mit diesem Zeiger können Daten
mehrere Owner haben, indem er die Zahl der Owner festhält und die Daten
aufräumt, wenn keine Owner mehr übrig sind.

In Rust mit seinem Konzept von Ownership und Borrowing gibt es einen weiteren
Unterschied zwischen Referenzen und Smart-Pointern: Während Referenzen Daten nur
ausleihen, _besitzen_ Smart-Pointer in vielen Fällen die Daten, auf die sie
zeigen.

Smart-Pointer werden normalerweise mit Structs implementiert. Anders als ein
gewöhnliches Struct implementieren Smart-Pointer die Traits `Deref` und `Drop`.
Der Trait `Deref` erlaubt einer Instanz des Smart-Pointer-Structs, sich wie eine
Referenz zu verhalten, sodass du deinen Code so schreiben kannst, dass er sowohl
mit Referenzen als auch mit Smart-Pointern funktioniert. Mit dem Trait `Drop`
kannst du den Code anpassen, der ausgeführt wird, wenn eine Instanz des
Smart-Pointers den Gültigkeitsbereich (_scope_) verlässt. In diesem Kapitel
besprechen wir beide Traits und zeigen, warum sie für Smart-Pointer wichtig
sind.

Da das Smart-Pointer-Pattern ein allgemeines Design-Pattern ist, das in Rust
häufig verwendet wird, behandelt dieses Kapitel nicht jeden existierenden
Smart-Pointer. Viele Bibliotheken haben ihre eigenen Smart-Pointer, und du
kannst sogar deine eigenen schreiben. Wir behandeln die gängigsten Smart-Pointer
der Standardbibliothek:

- `Box<T>`, um Werte auf dem Heap zu allozieren
- `Rc<T>`, ein Typ mit Referenzzählung, der mehrfache Ownership ermöglicht
- `Ref<T>` und `RefMut<T>`, auf die man über `RefCell<T>` zugreift, einen Typ,
  der die Borrowing-Regeln zur Laufzeit statt zur Kompilierzeit durchsetzt

Außerdem behandeln wir das Pattern der _inneren Veränderlichkeit_ (_interior
mutability_), bei dem ein unveränderlicher (_immutable_) Typ eine API zum
Verändern eines inneren Werts bereitstellt. Wir besprechen auch Referenzzyklen:
wie sie Speicherlecks verursachen können und wie man sie verhindert.

Legen wir los!
