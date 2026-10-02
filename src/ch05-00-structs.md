# Zusammengehörige Daten mit Structs strukturieren {#using-structs-to-structure-related-data}

Ein _Struct_ (von engl. _structure_) ist ein benutzerdefinierter Datentyp, mit
dem du mehrere zusammengehörige Werte, die eine sinnvolle Gruppe bilden,
zusammenpacken und benennen kannst. Wenn du eine objektorientierte Sprache
kennst: Ein Struct ist wie die Datenattribute eines Objekts. In diesem Kapitel
vergleichen wir Tupel mit Structs, um auf dem aufzubauen, was du bereits weißt,
und zeigen, wann Structs die bessere Wahl sind, um Daten zu gruppieren.

Wir zeigen, wie man Structs definiert und instanziiert. Wir besprechen, wie man
assoziierte Funktionen definiert, insbesondere die Art assoziierter Funktionen,
die man _Methoden_ nennt, um das Verhalten festzulegen, das zu einem Struct-Typ
gehört. Structs und Enums (die wir in Kapitel 6 besprechen) sind die Bausteine,
mit denen du neue Typen für den Anwendungsbereich deines Programms erstellst, um
die Typprüfung von Rust zur Kompilierzeit voll auszunutzen.
