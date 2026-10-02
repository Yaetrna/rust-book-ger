## Kommentare {#comments}

Alle Programmiererinnen und Programmierer bemühen sich, ihren Code leicht verständlich zu machen, aber manchmal ist eine zusätzliche Erklärung angebracht. In solchen Fällen hinterlassen sie in ihrem Quellcode _Kommentare_, die der Compiler ignoriert, die für Menschen, die den Quellcode lesen, aber nützlich sein können.

Hier ist ein einfacher Kommentar:

```rust
// hello, world
```

In Rust beginnt ein Kommentar im idiomatischen Kommentarstil mit zwei Schrägstrichen und reicht bis zum Ende der Zeile. Für Kommentare, die über eine einzelne Zeile hinausgehen, musst du in jede Zeile `//` schreiben, etwa so:

```rust
// So we're doing something complicated here, long enough that we need
// multiple lines of comments to do it! Whew! Hopefully, this comment will
// explain what's going on.
```

Oder du verwendest die Syntax für mehrzeilige Kommentare mit `/*` und `*/`:

```rust
/* So we’re doing something complicated here, long enough that we need
   multiple lines of comments to do it! Whew! Hopefully, this comment will
   explain what’s going on. */
```

Kommentare können auch am Ende von Zeilen stehen, die Code enthalten:

<span class="filename">Dateiname: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-24-comments-end-of-line/src/main.rs}}
```

Häufiger wirst du sie aber in diesem Format sehen, mit dem Kommentar in einer eigenen Zeile über dem Code, den er erläutert:

<span class="filename">Dateiname: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-25-comments-above-line/src/main.rs}}
```

Rust kennt außerdem eine weitere Art von Kommentaren, die Dokumentationskommentare, die wir im Abschnitt [„Ein Crate auf Crates.io veröffentlichen“][publishing]<!-- ignore --> in Kapitel 14 besprechen.

[publishing]: ch14-02-publishing-to-crates-io.html
