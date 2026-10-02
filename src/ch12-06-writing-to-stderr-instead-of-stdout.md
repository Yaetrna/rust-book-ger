<!-- Old headings. Do not remove or links may break. -->

<a id="writing-error-messages-to-standard-error-instead-of-standard-output"></a>

## Fehler auf die Standardfehlerausgabe umleiten {#redirecting-errors-to-standard-error}

Im Moment schreiben wir unsere gesamte Ausgabe mit dem Makro `println!` ins
Terminal. In den meisten Terminals gibt es zwei Arten von Ausgabe: die
_Standardausgabe_ (`stdout`) für allgemeine Informationen und die
_Standardfehlerausgabe_ (`stderr`) für Fehlermeldungen. Durch diese
Unterscheidung können Benutzer die erfolgreiche Ausgabe eines Programms in eine
Datei umleiten und Fehlermeldungen trotzdem auf dem Bildschirm ausgeben lassen.

Das Makro `println!` kann nur auf die Standardausgabe schreiben, also müssen wir
etwas anderes verwenden, um auf die Standardfehlerausgabe zu schreiben.

### Prüfen, wohin Fehler geschrieben werden {#checking-where-errors-are-written}

Sehen wir uns zuerst an, wie der von `minigrep` ausgegebene Inhalt derzeit auf
die Standardausgabe geschrieben wird, einschließlich aller Fehlermeldungen, die
wir stattdessen auf die Standardfehlerausgabe schreiben wollen. Dazu leiten wir
den Standardausgabestrom in eine Datei um und verursachen absichtlich einen
Fehler. Den Standardfehlerstrom leiten wir nicht um, daher wird jeder Inhalt,
der an die Standardfehlerausgabe gesendet wird, weiterhin auf dem Bildschirm
angezeigt.

Von Kommandozeilenprogrammen wird erwartet, dass sie Fehlermeldungen an den
Standardfehlerstrom senden, damit wir Fehlermeldungen auch dann auf dem
Bildschirm sehen, wenn wir den Standardausgabestrom in eine Datei umleiten.
Unser Programm verhält sich derzeit nicht so: Wir werden gleich sehen, dass es
die Ausgabe der Fehlermeldung stattdessen in einer Datei speichert!

Um dieses Verhalten zu zeigen, führen wir das Programm mit `>` und dem Dateipfad
_output.txt_ aus, in den wir den Standardausgabestrom umleiten wollen. Wir
übergeben keine Argumente, was einen Fehler verursachen sollte:

```console
$ cargo run > output.txt
```

Die Syntax `>` weist die Shell an, den Inhalt der Standardausgabe statt auf den
Bildschirm in _output.txt_ zu schreiben. Wir haben die erwartete Fehlermeldung
nicht auf dem Bildschirm gesehen, also muss sie in der Datei gelandet sein. Das
steht in _output.txt_:

```text
Problem parsing arguments: not enough arguments
```

Ja, unsere Fehlermeldung wird auf die Standardausgabe geschrieben. Es ist viel
nützlicher, Fehlermeldungen wie diese auf die Standardfehlerausgabe zu
schreiben, damit nur Daten aus einem erfolgreichen Lauf in der Datei landen. Das
ändern wir.

### Fehler auf die Standardfehlerausgabe schreiben {#printing-errors-to-standard-error}

Mit dem Code in Listing 12-24 ändern wir, wie Fehlermeldungen ausgegeben werden.
Dank des Refactorings, das wir früher in diesem Kapitel vorgenommen haben, steht
der gesamte Code, der Fehlermeldungen ausgibt, in einer Funktion, `main`. Die
Standardbibliothek stellt das Makro `eprintln!` bereit, das auf den
Standardfehlerstrom schreibt. Ändern wir also die beiden Stellen, an denen wir
`println!` zur Ausgabe von Fehlern aufgerufen haben, so, dass sie stattdessen
`eprintln!` verwenden.

<Listing number="12-24" file-name="src/main.rs" caption="Fehlermeldungen mit `eprintln!` auf die Standardfehlerausgabe statt auf die Standardausgabe schreiben">

```rust,ignore
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-24/src/main.rs:here}}
```

</Listing>

Führen wir das Programm jetzt erneut auf dieselbe Weise aus, ohne Argumente und
mit Umleitung der Standardausgabe durch `>`:

```console
$ cargo run > output.txt
Problem parsing arguments: not enough arguments
```

Jetzt sehen wir den Fehler auf dem Bildschirm, und _output.txt_ enthält nichts,
was das Verhalten ist, das wir von Kommandozeilenprogrammen erwarten.

Führen wir das Programm erneut mit Argumenten aus, die keinen Fehler
verursachen, leiten die Standardausgabe aber weiterhin in eine Datei um, etwa
so:

```console
$ cargo run -- to poem.txt > output.txt
```

Wir sehen keine Ausgabe im Terminal, und _output.txt_ enthält unsere Ergebnisse:

<span class="filename">Dateiname: output.txt</span>

```text
Are you nobody, too?
How dreary to be somebody!
```

Das zeigt, dass wir jetzt wie vorgesehen die Standardausgabe für erfolgreiche
Ausgaben und die Standardfehlerausgabe für Fehlerausgaben verwenden.

## Zusammenfassung {#summary}

Dieses Kapitel hat einige der wichtigsten Konzepte wiederholt, die du bisher
gelernt hast, und gezeigt, wie man in Rust gängige I/O-Operationen durchführt.
Mit Kommandozeilenargumenten, Dateien, Umgebungsvariablen und dem Makro
`eprintln!` zum Ausgeben von Fehlern bist du jetzt darauf vorbereitet,
Kommandozeilenanwendungen zu schreiben. Zusammen mit den Konzepten aus den
vorherigen Kapiteln wird dein Code gut organisiert sein, Daten effektiv in den
passenden Datenstrukturen speichern, Fehler sauber behandeln und gut getestet
sein.

Als Nächstes erkunden wir einige Features von Rust, die von funktionalen
Sprachen beeinflusst wurden: Closures und Iteratoren.
