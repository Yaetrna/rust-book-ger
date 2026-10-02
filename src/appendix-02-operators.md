## Anhang B: Operatoren und Symbole {#appendix-b-operators-and-symbols}

Dieser Anhang enthält ein Glossar der Syntax von Rust, einschließlich der
Operatoren und anderer Symbole, die für sich allein oder im Zusammenhang mit
Pfaden, Generics, Trait-Bounds, Makros, Attributen, Kommentaren, Tupeln und
Klammern vorkommen.

### Operatoren {#operators}

Tabelle B-1 enthält die Operatoren in Rust, ein Beispiel dafür, wie der Operator
im Kontext aussieht, eine kurze Erklärung und die Angabe, ob dieser Operator
überladbar ist. Wenn ein Operator überladbar ist, ist der Trait angegeben, mit
dem dieser Operator überladen wird.

<span class="caption">Tabelle B-1: Operatoren</span>

| Operator                  | Beispiel                                                | Erklärung                                                                             | Überladbar?    |
| ------------------------- | ------------------------------------------------------- | ------------------------------------------------------------------------------------- | -------------- |
| `!`                       | `ident!(...)`, `ident!{...}`, `ident![...]`             | Makro-Expansion                                                                       |                |
| `!`                       | `!expr`                                                 | Bitweises oder logisches Komplement                                                   | `Not`          |
| `!=`                      | `expr != expr`                                          | Vergleich auf Ungleichheit                                                            | `PartialEq`    |
| `%`                       | `expr % expr`                                           | Arithmetischer Rest                                                                   | `Rem`          |
| `%=`                      | `var %= expr`                                           | Arithmetischer Rest und Zuweisung                                                     | `RemAssign`    |
| `&`                       | `&expr`, `&mut expr`                                    | Ausleihen (_borrow_)                                                                  |                |
| `&`                       | `&type`, `&mut type`, `&'a type`, `&'a mut type`        | Typ eines ausgeliehenen Zeigers                                                       |                |
| `&`                       | `expr & expr`                                           | Bitweises UND                                                                         | `BitAnd`       |
| `&=`                      | `var &= expr`                                           | Bitweises UND und Zuweisung                                                           | `BitAndAssign` |
| `&&`                      | `expr && expr`                                          | Logisches UND mit Kurzschlussauswertung                                               |                |
| `*`                       | `expr * expr`                                           | Arithmetische Multiplikation                                                          | `Mul`          |
| `*=`                      | `var *= expr`                                           | Arithmetische Multiplikation und Zuweisung                                            | `MulAssign`    |
| `*`                       | `*expr`                                                 | Dereferenzierung                                                                      | `Deref`        |
| `*`                       | `*const type`, `*mut type`                              | Raw-Pointer                                                                           |                |
| `+`                       | `trait + trait`, `'a + trait`                           | Zusammengesetzte Typeinschränkung                                                     |                |
| `+`                       | `expr + expr`                                           | Arithmetische Addition                                                                | `Add`          |
| `+=`                      | `var += expr`                                           | Arithmetische Addition und Zuweisung                                                  | `AddAssign`    |
| `,`                       | `expr, expr`                                            | Trennzeichen für Argumente und Elemente                                               |                |
| `-`                       | `- expr`                                                | Arithmetische Negation                                                                | `Neg`          |
| `-`                       | `expr - expr`                                           | Arithmetische Subtraktion                                                             | `Sub`          |
| `-=`                      | `var -= expr`                                           | Arithmetische Subtraktion und Zuweisung                                               | `SubAssign`    |
| `->`                      | `fn(...) -> type`, <code>&vert;...&vert; -> type</code> | Rückgabetyp von Funktionen und Closures                                               |                |
| `.`                       | `expr.ident`                                            | Feldzugriff                                                                           |                |
| `.`                       | `expr.ident(expr, ...)`                                 | Methodenaufruf                                                                        |                |
| `.`                       | `expr.0`, `expr.1` usw.                                 | Tupel-Indizierung                                                                     |                |
| `..`                      | `..`, `expr..`, `..expr`, `expr..expr`                  | Bereichsliteral, rechts exklusiv                                                      | `PartialOrd`   |
| `..=`                     | `..=expr`, `expr..=expr`                                | Bereichsliteral, rechts inklusiv                                                      | `PartialOrd`   |
| `..`                      | `..expr`                                                | Update-Syntax für Struct-Literale                                                     |                |
| `..`                      | `variant(x, ..)`, `struct_type { x, .. }`               | Pattern-Bindung „und der Rest“                                                        |                |
| `...`                     | `expr...expr`                                           | (Veraltet, stattdessen `..=` verwenden) In einem Pattern: inklusives Bereichs-Pattern |                |
| `/`                       | `expr / expr`                                           | Arithmetische Division                                                                | `Div`          |
| `/=`                      | `var /= expr`                                           | Arithmetische Division und Zuweisung                                                  | `DivAssign`    |
| `:`                       | `pat: type`, `ident: type`                              | Einschränkungen                                                                       |                |
| `:`                       | `ident: expr`                                           | Initialisierer für Struct-Felder                                                      |                |
| `:`                       | `'a: loop {...}`                                        | Schleifenlabel                                                                        |                |
| `;`                       | `expr;`                                                 | Endezeichen für Anweisungen und Elemente                                              |                |
| `;`                       | `[...; len]`                                            | Teil der Syntax für Arrays fester Größe                                               |                |
| `<<`                      | `expr << expr`                                          | Linksverschiebung                                                                     | `Shl`          |
| `<<=`                     | `var <<= expr`                                          | Linksverschiebung und Zuweisung                                                       | `ShlAssign`    |
| `<`                       | `expr < expr`                                           | Vergleich auf kleiner als                                                             | `PartialOrd`   |
| `<=`                      | `expr <= expr`                                          | Vergleich auf kleiner oder gleich                                                     | `PartialOrd`   |
| `=`                       | `var = expr`, `ident = type`                            | Zuweisung/Äquivalenz                                                                  |                |
| `==`                      | `expr == expr`                                          | Vergleich auf Gleichheit                                                              | `PartialEq`    |
| `=>`                      | `pat => expr`                                           | Teil der Syntax von Match-Armen                                                       |                |
| `>`                       | `expr > expr`                                           | Vergleich auf größer als                                                              | `PartialOrd`   |
| `>=`                      | `expr >= expr`                                          | Vergleich auf größer oder gleich                                                      | `PartialOrd`   |
| `>>`                      | `expr >> expr`                                          | Rechtsverschiebung                                                                    | `Shr`          |
| `>>=`                     | `var >>= expr`                                          | Rechtsverschiebung und Zuweisung                                                      | `ShrAssign`    |
| `@`                       | `ident @ pat`                                           | Pattern-Bindung                                                                       |                |
| `^`                       | `expr ^ expr`                                           | Bitweises exklusives ODER                                                             | `BitXor`       |
| `^=`                      | `var ^= expr`                                           | Bitweises exklusives ODER und Zuweisung                                               | `BitXorAssign` |
| <code>&vert;</code>       | <code>pat &vert; pat</code>                             | Pattern-Alternativen                                                                  |                |
| <code>&vert;</code>       | <code>expr &vert; expr</code>                           | Bitweises ODER                                                                        | `BitOr`        |
| <code>&vert;=</code>      | <code>var &vert;= expr</code>                           | Bitweises ODER und Zuweisung                                                          | `BitOrAssign`  |
| <code>&vert;&vert;</code> | <code>expr &vert;&vert; expr</code>                     | Logisches ODER mit Kurzschlussauswertung                                              |                |
| `?`                       | `expr?`                                                 | Fehlerweitergabe                                                                      |                |

### Symbole, die keine Operatoren sind {#non-operator-symbols}

Die folgenden Tabellen enthalten alle Symbole, die nicht als Operatoren
fungieren, sich also nicht wie ein Funktions- oder Methodenaufruf verhalten.

Tabelle B-2 zeigt Symbole, die für sich allein vorkommen und an einer Vielzahl
von Stellen gültig sind.

<span class="caption">Tabelle B-2: Eigenständige Syntax</span>

| Symbol                                                            | Erklärung                                                                        |
| ----------------------------------------------------------------- | -------------------------------------------------------------------------------- |
| `'ident`                                                          | Benannte Lifetime oder Schleifenlabel                                            |
| Ziffern, unmittelbar gefolgt von `u8`, `i32`, `f64`, `usize` usw. | Numerisches Literal eines bestimmten Typs                                        |
| `"..."`                                                           | String-Literal                                                                   |
| `r"..."`, `r#"..."#`, `r##"..."##` usw.                           | Rohes String-Literal; Escape-Zeichen werden nicht verarbeitet                    |
| `b"..."`                                                          | Byte-String-Literal; erzeugt ein Array von Bytes statt eines Strings             |
| `br"..."`, `br#"..."#`, `br##"..."##` usw.                        | Rohes Byte-String-Literal; Kombination aus rohem und Byte-String-Literal         |
| `'...'`                                                           | Zeichenliteral                                                                   |
| `b'...'`                                                          | ASCII-Byte-Literal                                                               |
| <code>&vert;...&vert; expr</code>                                 | Closure                                                                          |
| `!`                                                               | Immer leerer Bottom-Typ für divergierende Funktionen                             |
| `_`                                                               | „Ignorierte“ Pattern-Bindung; dient auch dazu, Ganzzahlliterale lesbar zu machen |

Tabelle B-3 zeigt Symbole, die im Zusammenhang mit einem Pfad durch die
Modulhierarchie zu einem Element vorkommen.

<span class="caption">Tabelle B-3: Syntax im Zusammenhang mit Pfaden</span>

| Symbol                                  | Erklärung                                                                                                              |
| --------------------------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| `ident::ident`                          | Namensraum-Pfad                                                                                                        |
| `::path`                                | Pfad relativ zur Crate-Root (also ein explizit absoluter Pfad)                                                         |
| `self::path`                            | Pfad relativ zum aktuellen Modul (also ein explizit relativer Pfad)                                                    |
| `super::path`                           | Pfad relativ zum Elternmodul des aktuellen Moduls                                                                      |
| `type::ident`, `<type as trait>::ident` | Assoziierte Konstanten, Funktionen und Typen                                                                           |
| `<type>::...`                           | Assoziiertes Element für einen Typ, der nicht direkt benannt werden kann (zum Beispiel `<&T>::...`, `<[T]>::...` usw.) |
| `trait::method(...)`                    | Einen Methodenaufruf eindeutig machen, indem der Trait genannt wird, der die Methode definiert                         |
| `type::method(...)`                     | Einen Methodenaufruf eindeutig machen, indem der Typ genannt wird, für den die Methode definiert ist                   |
| `<type as trait>::method(...)`          | Einen Methodenaufruf eindeutig machen, indem Trait und Typ genannt werden                                              |

Tabelle B-4 zeigt Symbole, die im Zusammenhang mit der Verwendung generischer
Typparameter vorkommen.

<span class="caption">Tabelle B-4: Generics</span>

| Symbol                         | Erklärung                                                                                                                                                                 |
| ------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `path<...>`                    | Gibt Parameter für einen generischen Typ in einem Typ an (zum Beispiel `Vec<u8>`)                                                                                         |
| `path::<...>`, `method::<...>` | Gibt Parameter für einen generischen Typ, eine generische Funktion oder Methode in einem Ausdruck an; oft als _Turbofish_ bezeichnet (zum Beispiel `"42".parse::<i32>()`) |
| `fn ident<...> ...`            | Generische Funktion definieren                                                                                                                                            |
| `struct ident<...> ...`        | Generisches Struct definieren                                                                                                                                             |
| `enum ident<...> ...`          | Generisches Enum definieren                                                                                                                                               |
| `impl<...> ...`                | Generische Implementierung definieren                                                                                                                                     |
| `for<...> type`                | Lifetime-Bounds höheren Rangs                                                                                                                                             |
| `type<ident=type>`             | Ein generischer Typ, bei dem ein oder mehrere assoziierte Typen bestimmte Zuweisungen haben (zum Beispiel `Iterator<Item=T>`)                                             |

Tabelle B-5 zeigt Symbole, die im Zusammenhang mit der Einschränkung generischer
Typparameter durch Trait-Bounds vorkommen.

<span class="caption">Tabelle B-5: Einschränkungen durch Trait-Bounds</span>

| Symbol                        | Erklärung                                                                                                                                                  |
| ----------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `T: U`                        | Generischer Parameter `T`, beschränkt auf Typen, die `U` implementieren                                                                                    |
| `T: 'a`                       | Generischer Typ `T` muss länger leben als die Lifetime `'a` (das heißt, der Typ kann transitiv keine Referenzen mit kürzeren Lifetimes als `'a` enthalten) |
| `T: 'static`                  | Generischer Typ `T` enthält keine ausgeliehenen Referenzen außer solchen mit `'static`                                                                     |
| `'b: 'a`                      | Generische Lifetime `'b` muss länger leben als die Lifetime `'a`                                                                                           |
| `T: ?Sized`                   | Erlaubt, dass ein generischer Typparameter ein Typ mit dynamischer Größe ist                                                                               |
| `'a + trait`, `trait + trait` | Zusammengesetzte Typeinschränkung                                                                                                                          |

Tabelle B-6 zeigt Symbole, die im Zusammenhang mit dem Aufrufen oder Definieren
von Makros und dem Angeben von Attributen für ein Element vorkommen.

<span class="caption">Tabelle B-6: Makros und Attribute</span>

| Symbol                                      | Erklärung          |
| ------------------------------------------- | ------------------ |
| `#[meta]`                                   | Äußeres Attribut   |
| `#![meta]`                                  | Inneres Attribut   |
| `$ident`                                    | Makro-Ersetzung    |
| `$ident:kind`                               | Makro-Metavariable |
| `$(...)...`                                 | Makro-Wiederholung |
| `ident!(...)`, `ident!{...}`, `ident![...]` | Makroaufruf        |

Tabelle B-7 zeigt Symbole, die Kommentare erzeugen.

<span class="caption">Tabelle B-7: Kommentare</span>

| Symbol     | Erklärung                               |
| ---------- | --------------------------------------- |
| `//`       | Zeilenkommentar                         |
| `//!`      | Innerer Dokumentationskommentar (Zeile) |
| `///`      | Äußerer Dokumentationskommentar (Zeile) |
| `/*...*/`  | Blockkommentar                          |
| `/*!...*/` | Innerer Dokumentationskommentar (Block) |
| `/**...*/` | Äußerer Dokumentationskommentar (Block) |

Tabelle B-8 zeigt die Kontexte, in denen runde Klammern verwendet werden.

<span class="caption">Tabelle B-8: Runde Klammern</span>

| Symbol            | Erklärung                                                                                                       |
| ----------------- | --------------------------------------------------------------------------------------------------------------- |
| `()`              | Leeres Tupel (auch Unit genannt), sowohl als Literal als auch als Typ                                           |
| `(expr)`          | Geklammerter Ausdruck                                                                                           |
| `(expr,)`         | Tupelausdruck mit einem Element                                                                                 |
| `(type,)`         | Tupeltyp mit einem Element                                                                                      |
| `(expr, ...)`     | Tupelausdruck                                                                                                   |
| `(type, ...)`     | Tupeltyp                                                                                                        |
| `expr(expr, ...)` | Funktionsaufruf-Ausdruck; wird auch zum Initialisieren von Tupel-`struct`s und Tupel-`enum`-Varianten verwendet |

Tabelle B-9 zeigt die Kontexte, in denen geschweifte Klammern verwendet werden.

<span class="caption">Tabelle B-9: Geschweifte Klammern</span>

| Kontext      | Erklärung      |
| ------------ | -------------- |
| `{...}`      | Blockausdruck  |
| `Type {...}` | Struct-Literal |

Tabelle B-10 zeigt die Kontexte, in denen eckige Klammern verwendet werden.

<span class="caption">Tabelle B-10: Eckige Klammern</span>

| Kontext                                            | Erklärung                                                                                                                    |
| -------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------- |
| `[...]`                                            | Array-Literal                                                                                                                |
| `[expr; len]`                                      | Array-Literal mit `len` Kopien von `expr`                                                                                    |
| `[type; len]`                                      | Array-Typ mit `len` Instanzen von `type`                                                                                     |
| `expr[expr]`                                       | Indizierung einer Collection; überladbar (`Index`, `IndexMut`)                                                               |
| `expr[..]`, `expr[a..]`, `expr[..b]`, `expr[a..b]` | Indizierung einer Collection, die sich als Slicing ausgibt, mit `Range`, `RangeFrom`, `RangeTo` oder `RangeFull` als „Index“ |
