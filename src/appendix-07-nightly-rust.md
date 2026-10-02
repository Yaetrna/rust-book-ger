## Anhang G – Wie Rust entsteht und „Nightly Rust“ {#appendix-g---how-rust-is-made-and-nightly-rust}

In diesem Anhang geht es darum, wie Rust entsteht und wie sich das auf dich als
Rust-Entwickler auswirkt.

### Stabilität ohne Stillstand {#stability-without-stagnation}

Als Sprache legt Rust _sehr_ viel Wert auf die Stabilität deines Codes. Wir
wollen, dass Rust ein grundsolides Fundament ist, auf dem du aufbauen kannst,
und wenn sich ständig etwas ändern würde, wäre das unmöglich. Gleichzeitig
würden wir, wenn wir nicht mit neuen Features experimentieren könnten, wichtige
Mängel womöglich erst nach deren Release entdecken, wenn wir nichts mehr ändern
können.

Unsere Lösung für dieses Problem nennen wir „Stabilität ohne Stillstand“
(_stability without stagnation_), und unser Leitprinzip lautet: Du solltest nie
Angst davor haben müssen, auf eine neue Version von stabilem Rust zu
aktualisieren. Jedes Update sollte schmerzlos sein, dir aber auch neue Features,
weniger Bugs und schnellere Kompilierzeiten bringen.

### Tschu-tschu! Release-Kanäle und das Fahren mit den Zügen {#choo-choo-release-channels-and-riding-the-trains}

Die Entwicklung von Rust folgt einem _Zugfahrplan_. Das heißt, die gesamte
Entwicklung findet im Hauptbranch des Rust-Repositorys statt. Releases folgen
einem Software-Release-Zug-Modell, das unter anderem von Cisco IOS und anderen
Softwareprojekten verwendet wurde. Für Rust gibt es drei _Release-Kanäle_:

- Nightly
- Beta
- Stable

Die meisten Rust-Entwickler verwenden hauptsächlich den Stable-Kanal, aber wer
experimentelle neue Features ausprobieren möchte, kann Nightly oder Beta
verwenden.

Hier ist ein Beispiel dafür, wie der Entwicklungs- und Release-Prozess
funktioniert: Nehmen wir an, das Rust-Team arbeitet am Release von Rust 1.5.
Dieses Release ist im Dezember 2015 erschienen, liefert uns aber realistische
Versionsnummern. Ein neues Feature wird zu Rust hinzugefügt: Ein neuer Commit
landet im Hauptbranch. Jede Nacht wird eine neue Nightly-Version von Rust
erzeugt. Jeder Tag ist ein Release-Tag, und diese Releases werden von unserer
Release-Infrastruktur automatisch erstellt. Im Lauf der Zeit sehen unsere
Releases also so aus, einmal pro Nacht:

```text
nightly: * - - * - - *
```

Alle sechs Wochen ist es Zeit, ein neues Release vorzubereiten! Der Branch
`beta` des Rust-Repositorys zweigt vom Hauptbranch ab, den Nightly verwendet.
Jetzt gibt es zwei Releases:

```text
nightly: * - - * - - *
                     |
beta:                *
```

Die meisten Rust-Benutzer verwenden Beta-Releases nicht aktiv, testen aber in
ihrem CI-System gegen Beta, um Rust dabei zu helfen, mögliche Regressionen zu
entdecken. In der Zwischenzeit gibt es weiterhin jede Nacht ein Nightly-Release:

```text
nightly: * - - * - - * - - * - - *
                     |
beta:                *
```

Nehmen wir an, es wird eine Regression gefunden. Gut, dass wir etwas Zeit
hatten, das Beta-Release zu testen, bevor sich die Regression in ein stabiles
Release eingeschlichen hat! Die Korrektur wird auf den Hauptbranch angewendet,
sodass Nightly korrigiert ist, und dann wird die Korrektur in den Branch `beta`
zurückportiert und ein neues Beta-Release erzeugt:

```text
nightly: * - - * - - * - - * - - * - - *
                     |
beta:                * - - - - - - - - *
```

Sechs Wochen nachdem die erste Beta erstellt wurde, ist es Zeit für ein stabiles
Release! Der Branch `stable` wird aus dem Branch `beta` erzeugt:

```text
nightly: * - - * - - * - - * - - * - - * - * - *
                     |
beta:                * - - - - - - - - *
                                       |
stable:                                *
```

Hurra! Rust 1.5 ist fertig! Allerdings haben wir eine Sache vergessen: Weil die
sechs Wochen vorbei sind, brauchen wir auch eine neue Beta der _nächsten_
Version von Rust, 1.6. Nachdem also `stable` von `beta` abgezweigt ist, zweigt
die nächste Version von `beta` wieder von `nightly` ab:

```text
nightly: * - - * - - * - - * - - * - - * - * - *
                     |                         |
beta:                * - - - - - - - - *       *
                                       |
stable:                                *
```

Das nennt man das „Zugmodell“ (_train model_), weil alle sechs Wochen ein
Release „den Bahnhof verlässt“, aber noch eine Reise durch den Beta-Kanal
zurücklegen muss, bevor es als stabiles Release ankommt.

Rust veröffentlicht alle sechs Wochen ein Release, wie ein Uhrwerk. Wenn du das
Datum eines Rust-Releases kennst, kennst du auch das Datum des nächsten: sechs
Wochen später. Ein schöner Aspekt davon, dass Releases alle sechs Wochen geplant
sind, ist, dass der nächste Zug bald kommt. Wenn ein Feature ein bestimmtes
Release verpasst, musst du dir keine Sorgen machen: Das nächste kommt in kurzer
Zeit! Das hilft, den Druck zu verringern, möglicherweise unausgereifte Features
kurz vor dem Release-Termin noch hineinzuschmuggeln.

Dank dieses Prozesses kannst du dir immer den nächsten Build von Rust ansehen
und selbst überprüfen, dass sich leicht darauf aktualisieren lässt: Wenn ein
Beta-Release nicht wie erwartet funktioniert, kannst du das dem Team melden und
es beheben lassen, bevor das nächste stabile Release erscheint! Probleme in
einem Beta-Release sind relativ selten, aber `rustc` ist trotzdem eine Software,
und Bugs gibt es.

### Wartungszeit {#maintenance-time}

Das Rust-Projekt unterstützt die jeweils neueste stabile Version. Wenn eine neue
stabile Version veröffentlicht wird, erreicht die alte Version ihr Lebensende
(_end of life_, EOL). Das bedeutet, dass jede Version sechs Wochen lang
unterstützt wird.

### Instabile Features {#unstable-features}

Dieses Release-Modell hat noch einen Haken: instabile Features. Rust verwendet
eine Technik namens „Feature-Flags“, um festzulegen, welche Features in einem
bestimmten Release aktiviert sind. Wenn ein neues Feature aktiv entwickelt wird,
landet es im Hauptbranch und damit in Nightly, aber hinter einem _Feature-Flag_.
Wenn du als Benutzer das in Arbeit befindliche Feature ausprobieren möchtest,
kannst du das tun, musst aber ein Nightly-Release von Rust verwenden und deinen
Quellcode mit dem passenden Flag annotieren, um es zu aktivieren.

Wenn du ein Beta- oder Stable-Release von Rust verwendest, kannst du keine
Feature-Flags verwenden. Das ist der Schlüssel, der es uns ermöglicht, neue
Features praktisch zu nutzen, bevor wir sie für immer für stabil erklären. Wer
an vorderster Front dabei sein will, kann das tun, und wer eine grundsolide
Erfahrung möchte, kann bei Stable bleiben und weiß, dass sein Code nicht kaputt
geht. Stabilität ohne Stillstand.

Dieses Buch enthält nur Informationen über stabile Features, da sich Features in
Arbeit noch ändern und sich zwischen dem Zeitpunkt, zu dem dieses Buch
geschrieben wurde, und dem Zeitpunkt, zu dem sie in stabilen Builds aktiviert
werden, sicherlich unterscheiden. Die Dokumentation für Features, die es nur in
Nightly gibt, findest du online.

### Rustup und die Rolle von Rust Nightly {#rustup-and-the-role-of-rust-nightly}

Mit Rustup kannst du global oder pro Projekt leicht zwischen verschiedenen
Release-Kanälen von Rust wechseln. Standardmäßig hast du stabiles Rust
installiert. Um zum Beispiel Nightly zu installieren:

```console
$ rustup toolchain install nightly
```

Mit `rustup` kannst du auch alle _Toolchains_ (Releases von Rust und zugehörige
Komponenten) sehen, die du installiert hast. Hier ist ein Beispiel vom
Windows-Computer eines der Autoren:

```powershell
> rustup toolchain list
stable-x86_64-pc-windows-msvc (default)
beta-x86_64-pc-windows-msvc
nightly-x86_64-pc-windows-msvc
```

Wie du siehst, ist die Stable-Toolchain der Standard. Die meisten Rust-Benutzer
verwenden die meiste Zeit Stable. Vielleicht möchtest du die meiste Zeit Stable
verwenden, bei einem bestimmten Projekt aber Nightly, weil dir ein brandneues
Feature wichtig ist. Dazu kannst du im Verzeichnis dieses Projekts
`rustup override` verwenden, um die Nightly-Toolchain als diejenige festzulegen,
die `rustup` verwenden soll, wenn du dich in diesem Verzeichnis befindest:

```console
$ cd ~/projects/needs-nightly
$ rustup override set nightly
```

Jedes Mal, wenn du jetzt `rustc` oder `cargo` innerhalb von
_~/projects/needs-nightly_ aufrufst, stellt `rustup` sicher, dass du
Nightly-Rust statt deines standardmäßigen stabilen Rust verwendest. Das ist
praktisch, wenn du viele Rust-Projekte hast!

### Der RFC-Prozess und die Teams {#the-rfc-process-and-teams}

Wie erfährst du also von diesen neuen Features? Das Entwicklungsmodell von Rust
folgt einem _Request-for-Comments-Prozess (RFC-Prozess)_. Wenn du dir eine
Verbesserung in Rust wünschst, kannst du einen Vorschlag schreiben, einen
sogenannten RFC.

Jeder kann RFCs schreiben, um Rust zu verbessern, und die Vorschläge werden vom
Rust-Team geprüft und diskutiert, das aus vielen thematischen Unterteams
besteht. Eine vollständige Liste der Teams gibt es
[auf der Website von Rust](https://www.rust-lang.org/governance); sie umfasst
Teams für jeden Bereich des Projekts: Sprachdesign, Compiler-Implementierung,
Infrastruktur, Dokumentation und mehr. Das zuständige Team liest den Vorschlag
und die Kommentare, schreibt eigene Kommentare, und schließlich gibt es einen
Konsens, das Feature anzunehmen oder abzulehnen.

Wenn das Feature angenommen wird, wird im Rust-Repository ein Issue eröffnet,
und jemand kann es implementieren. Die Person, die es implementiert, ist
durchaus nicht unbedingt dieselbe Person, die das Feature ursprünglich
vorgeschlagen hat! Wenn die Implementierung fertig ist, landet sie hinter einem
Feature-Gate im Hauptbranch, wie wir im Abschnitt
[„Instabile Features“](#unstable-features)<!-- ignore --> besprochen haben.

Nach einiger Zeit, sobald Rust-Entwickler, die Nightly-Releases verwenden, das
neue Feature ausprobieren konnten, diskutieren Teammitglieder das Feature und
wie es sich in Nightly bewährt hat, und entscheiden, ob es in stabiles Rust
aufgenommen werden soll oder nicht. Wenn die Entscheidung positiv ausfällt, wird
das Feature-Gate entfernt, und das Feature gilt nun als stabil! Es fährt mit den
Zügen in ein neues stabiles Release von Rust.
