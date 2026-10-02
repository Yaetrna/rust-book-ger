## Organisation von Tests {#test-organization}

Wie am Anfang des Kapitels erwähnt, ist Testen eine komplexe Disziplin, und
verschiedene Leute verwenden unterschiedliche Begriffe und Organisationsformen.
Die Rust-Community unterscheidet bei Tests zwei Hauptkategorien: Unit-Tests und
Integrationstests. _Unit-Tests_ sind klein und fokussierter, testen jeweils ein
Modul isoliert und können private Schnittstellen testen. _Integrationstests_
liegen vollständig außerhalb deiner Bibliothek und verwenden deinen Code auf
dieselbe Weise wie jeder andere externe Code, also nur über die öffentliche
Schnittstelle, und prüfen dabei womöglich mehrere Module pro Test.

Beide Arten von Tests zu schreiben ist wichtig, um sicherzustellen, dass die
Teile deiner Bibliothek sowohl einzeln als auch zusammen das tun, was du
erwartest.

### Unit-Tests {#unit-tests}

Unit-Tests sollen jede Codeeinheit isoliert vom restlichen Code testen, um
schnell festzustellen, wo Code wie erwartet funktioniert und wo nicht.
Unit-Tests legst du im Verzeichnis _src_ in jede Datei mit dem Code, den sie
testen. Die Konvention ist, in jeder Datei ein Modul namens `tests` anzulegen,
das die Testfunktionen enthält, und das Modul mit `cfg(test)` zu annotieren.

#### Das Modul `tests` und `#[cfg(test)]` {#the-tests-module-and-cfgtest}

Die Annotation `#[cfg(test)]` am Modul `tests` weist Rust an, den Testcode nur
dann zu kompilieren und auszuführen, wenn du `cargo test` ausführst, nicht bei
`cargo
build`. Das spart Kompilierzeit, wenn du nur die Bibliothek bauen willst,
und spart Platz im resultierenden kompilierten Artefakt, weil die Tests nicht
enthalten sind. Du wirst sehen, dass Integrationstests die Annotation
`#[cfg(test)]` nicht brauchen, weil sie in einem anderen Verzeichnis liegen. Da
Unit-Tests aber in denselben Dateien wie der Code stehen, verwendest du
`#[cfg(test)]`, um anzugeben, dass sie nicht in das kompilierte Ergebnis
aufgenommen werden sollen.

Erinnere dich: Als wir im ersten Abschnitt dieses Kapitels das neue Projekt
`adder` erzeugt haben, hat Cargo diesen Code für uns erzeugt:

<span class="filename">Dateiname: src/lib.rs</span>

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/listing-11-01/src/lib.rs}}
```

Beim automatisch erzeugten Modul `tests` steht das Attribut `cfg` für
_Konfiguration_ (_configuration_) und teilt Rust mit, dass das folgende Element
nur bei einer bestimmten Konfigurationsoption aufgenommen werden soll. In diesem
Fall ist die Konfigurationsoption `test`, die Rust zum Kompilieren und Ausführen
von Tests bereitstellt. Durch das Attribut `cfg` kompiliert Cargo unseren
Testcode nur, wenn wir die Tests aktiv mit `cargo test` ausführen. Das gilt
neben den mit `#[test]` annotierten Funktionen auch für alle Hilfsfunktionen,
die in diesem Modul stehen.

<!-- Old headings. Do not remove or links may break. -->

<a id="testing-private-functions"></a>

#### Tests privater Funktionen {#private-function-tests}

In der Test-Community wird darüber diskutiert, ob private Funktionen direkt
getestet werden sollten oder nicht, und andere Sprachen machen es schwierig oder
unmöglich, private Funktionen zu testen. Unabhängig davon, welcher
Testphilosophie du folgst, erlauben dir die Sichtbarkeitsregeln von Rust,
private Funktionen zu testen. Betrachte den Code in Listing 11-12 mit der
privaten Funktion `internal_adder`.

<Listing number="11-12" file-name="src/lib.rs" caption="Eine private Funktion testen">

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/listing-11-12/src/lib.rs}}
```

</Listing>

Beachte, dass die Funktion `internal_adder` nicht als `pub` gekennzeichnet ist.
Tests sind einfach Rust-Code, und das Modul `tests` ist einfach ein weiteres
Modul. Wie wir in
[„Pfade, um auf ein Element im Modulbaum zu verweisen“][paths]<!-- ignore -->
besprochen haben, können Elemente in Kindmodulen die Elemente in ihren
Vorfahrenmodulen verwenden. In diesem Test bringen wir mit `use super::*` alle
Elemente, die zum Elternmodul des Moduls `tests` gehören, in den
Gültigkeitsbereich (_scope_), und dann kann der Test `internal_adder` aufrufen.
Wenn du der Meinung bist, dass private Funktionen nicht getestet werden sollten,
zwingt dich in Rust nichts dazu.

### Integrationstests {#integration-tests}

In Rust liegen Integrationstests vollständig außerhalb deiner Bibliothek. Sie
verwenden deine Bibliothek auf dieselbe Weise wie jeder andere Code, das heißt,
sie können nur Funktionen aufrufen, die Teil der öffentlichen API deiner
Bibliothek sind. Ihr Zweck ist zu testen, ob viele Teile deiner Bibliothek
korrekt zusammenarbeiten. Codeeinheiten, die für sich allein korrekt
funktionieren, können beim Zusammenspiel Probleme haben, daher ist auch die
Testabdeckung des zusammengefügten Codes wichtig. Um Integrationstests zu
erstellen, brauchst du zuerst ein Verzeichnis _tests_.

#### Das Verzeichnis _tests_ {#the-tests-directory}

Wir legen auf der obersten Ebene unseres Projektverzeichnisses neben _src_ ein
Verzeichnis _tests_ an. Cargo weiß, dass es in diesem Verzeichnis nach
Integrationstestdateien suchen muss. Wir können dann beliebig viele Testdateien
anlegen, und Cargo kompiliert jede der Dateien als eigenes Crate.

Erstellen wir einen Integrationstest. Lass den Code aus Listing 11-12 in der
Datei _src/lib.rs_, lege ein Verzeichnis _tests_ an und erstelle eine neue Datei
namens _tests/integration_test.rs_. Deine Verzeichnisstruktur sollte so
aussehen:

```text
adder
├── Cargo.lock
├── Cargo.toml
├── src
│   └── lib.rs
└── tests
    └── integration_test.rs
```

Gib den Code aus Listing 11-13 in die Datei _tests/integration_test.rs_ ein.

<Listing number="11-13" file-name="tests/integration_test.rs" caption="Ein Integrationstest für eine Funktion im Crate `adder`">

```rust,ignore
{{#rustdoc_include ../listings/ch11-writing-automated-tests/listing-11-13/tests/integration_test.rs}}
```

</Listing>

Jede Datei im Verzeichnis _tests_ ist ein separates Crate, daher müssen wir
unsere Bibliothek in den Gültigkeitsbereich jedes Test-Crates bringen. Deshalb
fügen wir am Anfang des Codes `use
adder::add_two;` hinzu, was wir in den
Unit-Tests nicht brauchten.

Wir müssen keinen Code in _tests/integration_test.rs_ mit `#[cfg(test)]`
annotieren. Cargo behandelt das Verzeichnis _tests_ besonders und kompiliert
Dateien in diesem Verzeichnis nur, wenn wir `cargo test` ausführen. Führe jetzt
`cargo test` aus:

```console
{{#include ../listings/ch11-writing-automated-tests/listing-11-13/output.txt}}
```

Die drei Abschnitte der Ausgabe umfassen die Unit-Tests, den Integrationstest
und die Dokumentationstests. Beachte: Schlägt ein Test in einem Abschnitt fehl,
werden die folgenden Abschnitte nicht ausgeführt. Schlägt zum Beispiel ein
Unit-Test fehl, gibt es keine Ausgabe für Integrations- und Dokumentationstests,
weil diese Tests nur ausgeführt werden, wenn alle Unit-Tests bestehen.

Der erste Abschnitt für die Unit-Tests ist derselbe, den wir bisher gesehen
haben: eine Zeile für jeden Unit-Test (einen namens `internal`, den wir in
Listing 11-12 hinzugefügt haben) und dann eine Zusammenfassungszeile für die
Unit-Tests.

Der Abschnitt für die Integrationstests beginnt mit der Zeile
`Running
tests/integration_test.rs`. Danach folgt eine Zeile für jede
Testfunktion in diesem Integrationstest und eine Zusammenfassungszeile für die
Ergebnisse des Integrationstests, direkt bevor der Abschnitt `Doc-tests adder`
beginnt.

Jede Integrationstestdatei hat ihren eigenen Abschnitt; fügen wir also weitere
Dateien im Verzeichnis _tests_ hinzu, gibt es mehr Abschnitte für
Integrationstests.

Wir können weiterhin eine bestimmte Integrationstestfunktion ausführen, indem
wir den Namen der Testfunktion als Argument an `cargo test` übergeben. Um alle
Tests in einer bestimmten Integrationstestdatei auszuführen, verwende das
Argument `--test` von `cargo test`, gefolgt vom Namen der Datei:

```console
{{#include ../listings/ch11-writing-automated-tests/output-only-05-single-integration/output.txt}}
```

Dieser Befehl führt nur die Tests in der Datei _tests/integration_test.rs_ aus.

#### Untermodule in Integrationstests {#submodules-in-integration-tests}

Wenn du weitere Integrationstests hinzufügst, möchtest du vielleicht mehr
Dateien im Verzeichnis _tests_ anlegen, um sie zu organisieren; du kannst die
Testfunktionen zum Beispiel nach der Funktionalität gruppieren, die sie testen.
Wie bereits erwähnt, wird jede Datei im Verzeichnis _tests_ als eigenes,
separates Crate kompiliert. Das ist nützlich, um getrennte Gültigkeitsbereiche
zu schaffen und genauer nachzuahmen, wie Endnutzer dein Crate verwenden werden.
Es bedeutet aber auch, dass sich Dateien im Verzeichnis _tests_ nicht so
verhalten wie Dateien in _src_, wie du in Kapitel 7 darüber gelernt hast, wie
man Code in Module und Dateien aufteilt.

Das unterschiedliche Verhalten von Dateien im Verzeichnis _tests_ fällt am
meisten auf, wenn du eine Reihe von Hilfsfunktionen hast, die du in mehreren
Integrationstestdateien verwenden willst, und versuchst, sie nach den Schritten
im Abschnitt
[„Module auf verschiedene Dateien aufteilen“][separating-modules-into-files]<!-- ignore -->
in Kapitel 7 in ein gemeinsames Modul auszulagern. Wenn wir zum Beispiel
_tests/common.rs_ anlegen und eine Funktion namens `setup` darin ablegen, können
wir `setup` Code hinzufügen, den wir aus mehreren Testfunktionen in mehreren
Testdateien aufrufen wollen:

<span class="filename">Dateiname: tests/common.rs</span>

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/no-listing-12-shared-test-code-problem/tests/common.rs}}
```

Wenn wir die Tests erneut ausführen, sehen wir in der Testausgabe einen neuen
Abschnitt für die Datei _common.rs_, obwohl diese Datei keine Testfunktionen
enthält und wir die Funktion `setup` nirgends aufgerufen haben:

```console
{{#include ../listings/ch11-writing-automated-tests/no-listing-12-shared-test-code-problem/output.txt}}
```

Dass `common` in den Testergebnissen mit `running 0 tests` erscheint, wollten
wir nicht. Wir wollten nur etwas Code mit den anderen Integrationstestdateien
teilen. Damit `common` nicht in der Testausgabe erscheint, legen wir statt
_tests/common.rs_ die Datei _tests/common/mod.rs_ an. Das Projektverzeichnis
sieht jetzt so aus:

```text
├── Cargo.lock
├── Cargo.toml
├── src
│   └── lib.rs
└── tests
    ├── common
    │   └── mod.rs
    └── integration_test.rs
```

Das ist die ältere Namenskonvention, die Rust ebenfalls versteht und die wir in
[„Alternative Dateipfade“][alt-paths]<!-- ignore --> in Kapitel 7 erwähnt haben.
Benennen wir die Datei so, behandelt Rust das Modul `common` nicht als
Integrationstestdatei. Wenn wir den Code der Funktion `setup` nach
_tests/common/mod.rs_ verschieben und die Datei _tests/common.rs_ löschen,
erscheint der Abschnitt in der Testausgabe nicht mehr. Dateien in
Unterverzeichnissen des Verzeichnisses _tests_ werden nicht als separate Crates
kompiliert und haben keine Abschnitte in der Testausgabe.

Nachdem wir _tests/common/mod.rs_ angelegt haben, können wir es aus jeder
Integrationstestdatei als Modul verwenden. Hier ist ein Beispiel, in dem die
Funktion `setup` aus dem Test `it_adds_two` in _tests/integration_test.rs_
aufgerufen wird:

<span class="filename">Dateiname: tests/integration_test.rs</span>

```rust,ignore
{{#rustdoc_include ../listings/ch11-writing-automated-tests/no-listing-13-fix-shared-test-code-problem/tests/integration_test.rs}}
```

Beachte, dass die Deklaration `mod common;` dieselbe ist wie die
Moduldeklaration, die wir in Listing 7-21 gezeigt haben. In der Testfunktion
können wir dann die Funktion `common::setup()` aufrufen.

#### Integrationstests für Binary-Crates {#integration-tests-for-binary-crates}

Ist unser Projekt ein Binary-Crate, das nur eine Datei _src/main.rs_ und keine
Datei _src/lib.rs_ enthält, können wir keine Integrationstests im Verzeichnis
_tests_ anlegen und in _src/main.rs_ definierte Funktionen mit einer
`use`-Anweisung in den Gültigkeitsbereich bringen. Nur Library-Crates stellen
Funktionen bereit, die andere Crates verwenden können; Binary-Crates sind dafür
gedacht, eigenständig ausgeführt zu werden.

Das ist einer der Gründe, warum Rust-Projekte, die eine Binärdatei
bereitstellen, eine schlichte Datei _src/main.rs_ haben, die Logik aufruft, die
in der Datei _src/lib.rs_ liegt. Mit dieser Struktur _können_ Integrationstests
das Library-Crate mit `use` testen, um die wichtige Funktionalität verfügbar zu
machen. Funktioniert die wichtige Funktionalität, funktioniert auch die kleine
Menge Code in der Datei _src/main.rs_, und diese kleine Menge Code muss nicht
getestet werden.

## Zusammenfassung {#summary}

Mit den Testfeatures von Rust kannst du festlegen, wie Code funktionieren soll,
und so sicherstellen, dass er auch bei Änderungen weiterhin wie erwartet
funktioniert. Unit-Tests prüfen verschiedene Teile einer Bibliothek einzeln und
können private Implementierungsdetails testen. Integrationstests prüfen, ob
viele Teile der Bibliothek korrekt zusammenarbeiten, und verwenden die
öffentliche API der Bibliothek, um den Code so zu testen, wie externer Code ihn
verwenden wird. Auch wenn das Typsystem und die Ownership-Regeln von Rust
helfen, einige Arten von Bugs zu verhindern, sind Tests weiterhin wichtig, um
Logikfehler zu verringern, die damit zu tun haben, wie sich dein Code verhalten
soll.

Kombinieren wir das Wissen aus diesem und den vorherigen Kapiteln und arbeiten
an einem Projekt!

{{#quiz ../quizzes/ch11-03-test-organization.toml}}

[paths]: ch07-03-paths-for-referring-to-an-item-in-the-module-tree.html
[separating-modules-into-files]: ch07-05-separating-modules-into-different-files.html
[alt-paths]: ch07-05-separating-modules-into-different-files.html#alternate-file-paths
