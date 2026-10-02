## Mit Umgebungsvariablen arbeiten {#working-with-environment-variables}

Wir verbessern die Binärdatei `minigrep`, indem wir ein zusätzliches Feature
hinzufügen: eine Option für eine Suche ohne Beachtung der Groß- und
Kleinschreibung, die der Benutzer über eine Umgebungsvariable einschalten kann.
Wir könnten dieses Feature zu einer Kommandozeilenoption machen und verlangen,
dass Benutzer sie jedes Mal angeben, wenn sie gelten soll. Machen wir es
stattdessen zu einer Umgebungsvariable, können unsere Benutzer die
Umgebungsvariable einmal setzen, und alle ihre Suchen in dieser Terminalsitzung
beachten Groß- und Kleinschreibung nicht.

<!-- Old headings. Do not remove or links may break. -->

<a id="writing-a-failing-test-for-the-case-insensitive-search-function"></a>

### Einen fehlschlagenden Test für die Suche ohne Groß-/Kleinschreibung schreiben {#writing-a-failing-test-for-case-insensitive-search}

Zuerst fügen wir der Bibliothek `minigrep` eine neue Funktion
`search_case_insensitive` hinzu, die aufgerufen wird, wenn die Umgebungsvariable
einen Wert hat. Wir folgen weiter dem TDD-Vorgehen, also ist der erste Schritt
wieder, einen fehlschlagenden Test zu schreiben. Wir fügen einen neuen Test für
die neue Funktion `search_case_insensitive` hinzu und benennen unseren alten
Test von `one_result` in `case_sensitive` um, um die Unterschiede zwischen den
beiden Tests zu verdeutlichen, wie in Listing 12-20 gezeigt.

<Listing number="12-20" file-name="src/lib.rs" caption="Einen neuen fehlschlagenden Test für die Funktion ohne Beachtung der Groß-/Kleinschreibung hinzufügen, die wir gleich hinzufügen">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-20/src/lib.rs:here}}
```

</Listing>

Beachte, dass wir auch `contents` des alten Tests bearbeitet haben. Wir haben
eine neue Zeile mit dem Text `"Duct tape."` mit großem _D_ hinzugefügt, die
nicht zur Suchanfrage `"duct"` passen sollte, wenn wir mit Beachtung der Groß-
und Kleinschreibung suchen. Den alten Test so zu ändern, hilft sicherzustellen,
dass wir die Suchfunktionalität mit Beachtung der Groß- und Kleinschreibung, die
wir bereits implementiert haben, nicht versehentlich kaputtmachen. Dieser Test
sollte jetzt bestehen und weiterhin bestehen, während wir an der Suche ohne
Beachtung der Groß- und Kleinschreibung arbeiten.

Der neue Test für die Suche _ohne_ Beachtung der Groß- und Kleinschreibung
verwendet `"rUsT"` als Suchanfrage. In der Funktion `search_case_insensitive`,
die wir gleich hinzufügen, sollte die Suchanfrage `"rUsT"` zur Zeile mit
`"Rust:"` mit großem _R_ passen und zur Zeile `"Trust me."`, obwohl sich bei
beiden die Groß- und Kleinschreibung von der Suchanfrage unterscheidet. Das ist
unser fehlschlagender Test, und er kompiliert nicht, weil wir die Funktion
`search_case_insensitive` noch nicht definiert haben. Füge ruhig eine
Gerüstimplementierung hinzu, die immer einen leeren Vektor zurückgibt, ähnlich
wie bei der Funktion `search` in Listing 12-16, um zu sehen, wie der Test
kompiliert und fehlschlägt.

### Die Funktion `search_case_insensitive` implementieren {#implementing-the-search_case_insensitive-function}

Die Funktion `search_case_insensitive`, gezeigt in Listing 12-21, ist fast
identisch mit der Funktion `search`. Der einzige Unterschied ist, dass wir
`query` und jede `line` in Kleinbuchstaben umwandeln, sodass die
Eingabeargumente, egal wie sie geschrieben sind, beim Prüfen, ob die Zeile die
Suchanfrage enthält, dieselbe Schreibweise haben.

<Listing number="12-21" file-name="src/lib.rs" caption="Die Funktion `search_case_insensitive` so definieren, dass sie Suchanfrage und Zeile vor dem Vergleich in Kleinbuchstaben umwandelt">

```rust,noplayground
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-21/src/lib.rs:here}}
```

</Listing>

Zuerst wandeln wir den String `query` in Kleinbuchstaben um und speichern ihn in
einer neuen Variable mit demselben Namen, die das ursprüngliche `query`
verschattet (_shadowing_). Der Aufruf von `to_lowercase` auf der Suchanfrage ist
nötig, damit wir die Suchanfrage, egal ob sie `"rust"`, `"RUST"`, `"Rust"` oder
`"rUsT"` lautet, so behandeln, als wäre sie `"rust"`, und die Groß- und
Kleinschreibung nicht beachten. `to_lowercase` kommt zwar mit grundlegendem
Unicode zurecht, ist aber nicht zu 100 Prozent genau. Würden wir eine echte
Anwendung schreiben, müssten wir hier etwas mehr Arbeit investieren, aber in
diesem Abschnitt geht es um Umgebungsvariablen, nicht um Unicode, also belassen
wir es dabei.

Beachte, dass `query` jetzt ein `String` und kein String-Slice ist, weil der
Aufruf von `to_lowercase` neue Daten erzeugt, statt auf vorhandene Daten zu
verweisen. Angenommen, die Suchanfrage lautet `"rUsT"`: Dieser String-Slice
enthält kein kleines `u` oder `t`, das wir verwenden könnten, also müssen wir
einen neuen `String` allozieren, der `"rust"` enthält. Wenn wir `query` jetzt
als Argument an die Methode `contains` übergeben, müssen wir ein Ampersand
hinzufügen, weil die Signatur von `contains` so definiert ist, dass sie einen
String-Slice nimmt.

Als Nächstes fügen wir für jede `line` einen Aufruf von `to_lowercase` hinzu, um
alle Zeichen in Kleinbuchstaben umzuwandeln. Nachdem wir `line` und `query` in
Kleinbuchstaben umgewandelt haben, finden wir Treffer unabhängig davon, wie die
Suchanfrage geschrieben ist.

Sehen wir nach, ob diese Implementierung die Tests besteht:

```console
{{#include ../listings/ch12-an-io-project/listing-12-21/output.txt}}
```

Großartig! Sie bestehen. Rufen wir jetzt die neue Funktion
`search_case_insensitive` aus der Funktion `run` auf. Zuerst fügen wir dem
Struct `Config` eine Konfigurationsoption hinzu, um zwischen der Suche mit und
ohne Beachtung der Groß- und Kleinschreibung umzuschalten. Das Hinzufügen dieses
Feldes führt zu Compilerfehlern, weil wir dieses Feld noch nirgends
initialisieren:

<span class="filename">Dateiname: src/main.rs</span>

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-22/src/main.rs:here}}
```

Wir haben das Feld `ignore_case` hinzugefügt, das einen Boolean enthält. Als
Nächstes muss die Funktion `run` den Wert des Feldes `ignore_case` prüfen und
damit entscheiden, ob sie die Funktion `search` oder die Funktion
`search_case_insensitive` aufruft, wie in Listing 12-22 gezeigt. Das kompiliert
immer noch nicht.

<Listing number="12-22" file-name="src/main.rs" caption="Je nach dem Wert in `config.ignore_case` entweder `search` oder `search_case_insensitive` aufrufen">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-22/src/main.rs:there}}
```

</Listing>

Schließlich müssen wir die Umgebungsvariable prüfen. Die Funktionen zum Arbeiten
mit Umgebungsvariablen befinden sich im Modul `env` der Standardbibliothek, das
am Anfang von _src/main.rs_ bereits im Gültigkeitsbereich (_scope_) ist. Wir
verwenden die Funktion `var` aus dem Modul `env`, um zu prüfen, ob für eine
Umgebungsvariable namens `IGNORE_CASE` ein Wert gesetzt wurde, wie in Listing
12-23 gezeigt.

<Listing number="12-23" file-name="src/main.rs" caption="Prüfen, ob eine Umgebungsvariable namens `IGNORE_CASE` einen Wert hat">

```rust,ignore,noplayground
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-23/src/main.rs:here}}
```

</Listing>

Hier legen wir eine neue Variable `ignore_case` an. Um ihren Wert zu setzen,
rufen wir die Funktion `env::var` auf und übergeben ihr den Namen der
Umgebungsvariable `IGNORE_CASE`. Die Funktion `env::var` gibt ein `Result`
zurück, das die erfolgreiche Variante `Ok` mit dem Wert der Umgebungsvariable
ist, wenn die Umgebungsvariable auf irgendeinen Wert gesetzt ist. Ist die
Umgebungsvariable nicht gesetzt, gibt sie die Variante `Err` zurück.

Wir verwenden die Methode `is_ok` auf dem `Result`, um zu prüfen, ob die
Umgebungsvariable gesetzt ist, was bedeutet, dass das Programm ohne Beachtung
der Groß- und Kleinschreibung suchen soll. Ist die Umgebungsvariable
`IGNORE_CASE` auf nichts gesetzt, gibt `is_ok` `false` zurück, und das Programm
sucht mit Beachtung der Groß- und Kleinschreibung. Uns interessiert nicht der
_Wert_ der Umgebungsvariable, sondern nur, ob sie gesetzt ist oder nicht, daher
prüfen wir `is_ok`, statt `unwrap`, `expect` oder eine der anderen Methoden zu
verwenden, die wir bei `Result` gesehen haben.

Wir übergeben den Wert in der Variable `ignore_case` an die `Config`-Instanz,
damit die Funktion `run` diesen Wert lesen und entscheiden kann, ob sie
`search_case_insensitive` oder `search` aufruft, wie wir es in Listing 12-22
implementiert haben.

Probieren wir es aus! Zuerst führen wir unser Programm ohne gesetzte
Umgebungsvariable und mit der Suchanfrage `to` aus, die zu jeder Zeile passen
sollte, die das Wort _to_ in Kleinbuchstaben enthält:

```console
{{#include ../listings/ch12-an-io-project/listing-12-23/output.txt}}
```

Sieht so aus, als würde das noch funktionieren! Führen wir das Programm jetzt
mit `IGNORE_CASE` auf `1` gesetzt, aber mit derselben Suchanfrage `to` aus:

```console
$ IGNORE_CASE=1 cargo run -- to poem.txt
```

Wenn du PowerShell verwendest, musst du die Umgebungsvariable setzen und das
Programm als separate Befehle ausführen:

```console
PS> $Env:IGNORE_CASE=1; cargo run -- to poem.txt
```

Dadurch bleibt `IGNORE_CASE` für den Rest deiner Shell-Sitzung gesetzt. Mit dem
Cmdlet `Remove-Item` lässt sich die Variable wieder entfernen:

```console
PS> Remove-Item Env:IGNORE_CASE
```

Wir sollten Zeilen erhalten, die _to_ enthalten und Großbuchstaben haben können:

<!-- manual-regeneration
cd listings/ch12-an-io-project/listing-12-23
IGNORE_CASE=1 cargo run -- to poem.txt
can't extract because of the environment variable
-->

```console
Are you nobody, too?
How dreary to be somebody!
To tell your name the livelong day
To an admiring bog!
```

Hervorragend, wir haben auch Zeilen mit _To_ erhalten! Unser Programm `minigrep`
kann jetzt ohne Beachtung der Groß- und Kleinschreibung suchen, gesteuert über
eine Umgebungsvariable. Jetzt weißt du, wie man Optionen handhabt, die entweder
über Kommandozeilenargumente oder über Umgebungsvariablen gesetzt werden.

Manche Programme erlauben für dieselbe Konfiguration Argumente _und_
Umgebungsvariablen. In diesen Fällen legen die Programme fest, dass das eine
oder das andere Vorrang hat. Versuch als weitere Übung für dich selbst, die
Beachtung der Groß- und Kleinschreibung entweder über ein Kommandozeilenargument
oder über eine Umgebungsvariable zu steuern. Entscheide, ob das
Kommandozeilenargument oder die Umgebungsvariable Vorrang haben soll, wenn das
Programm mit einem auf Beachtung und einem auf Nichtbeachtung der Groß- und
Kleinschreibung gesetzten Wert ausgeführt wird.

Das Modul `std::env` enthält viele weitere nützliche Features für den Umgang mit
Umgebungsvariablen: Sieh dir seine Dokumentation an, um zu erfahren, was
verfügbar ist.
