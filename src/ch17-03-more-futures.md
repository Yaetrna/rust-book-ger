<!-- Old headings. Do not remove or links may break. -->

<a id="yielding"></a>

### Die Kontrolle an die Runtime abgeben {#yielding-control-to-the-runtime}

Erinnere dich aus dem Abschnitt
[„Unser erstes asynchrones Programm“][async-program]<!-- ignore -->, dass Rust
einer Runtime an jedem Await-Punkt die Gelegenheit gibt, den Task zu pausieren
und zu einem anderen zu wechseln, wenn das abgewartete Future nicht bereit ist.
Umgekehrt gilt das auch: Rust pausiert async-Blöcke _nur_ an einem Await-Punkt
und gibt nur dort die Kontrolle an eine Runtime zurück. Alles zwischen
Await-Punkten ist synchron.

Das bedeutet: Wenn du in einem async-Block ohne Await-Punkt viel Arbeit
erledigst, blockiert dieses Future alle anderen Futures daran, voranzukommen.
Manchmal hört man dafür, dass ein Future andere Futures _aushungert_
(_starving_). In manchen Fällen ist das vielleicht kein großes Problem. Wenn du
aber eine aufwendige Einrichtung oder langwierige Arbeit erledigst oder ein
Future hast, das eine bestimmte Aufgabe unbegrenzt weiter ausführt, musst du dir
überlegen, wann und wo du die Kontrolle an die Runtime zurückgibst.

Simulieren wir eine langwierige Operation, um das Problem des Aushungerns zu
veranschaulichen, und erkunden dann, wie man es löst. Listing 17-14 führt eine
Funktion `slow` ein.

<Listing number="17-14" caption="Mit `thread::sleep` langsame Operationen simulieren" file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-14/src/main.rs:slow}}
```

</Listing>

Dieser Code verwendet `std::thread::sleep` statt `trpl::sleep`, sodass ein
Aufruf von `slow` den aktuellen Thread für einige Millisekunden blockiert. Wir
können `slow` als Platzhalter für Operationen aus der Praxis verwenden, die
sowohl langwierig als auch blockierend sind.

In Listing 17-15 verwenden wir `slow`, um in einem Paar von Futures diese Art
von CPU-gebundener Arbeit nachzuahmen.

<Listing number="17-15" caption="Die Funktion `slow` aufrufen, um langsame Operationen zu simulieren" file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-15/src/main.rs:slow-futures}}
```

</Listing>

Jedes Future gibt die Kontrolle erst _nach_ einer Reihe langsamer Operationen an
die Runtime zurück. Wenn du diesen Code ausführst, siehst du diese Ausgabe:

<!-- manual-regeneration
cd listings/ch17-async-await/listing-17-15/
cargo run
copy just the output
-->

```text
'a' started.
'a' ran for 30ms
'a' ran for 10ms
'a' ran for 20ms
'b' started.
'b' ran for 75ms
'b' ran for 10ms
'b' ran for 15ms
'b' ran for 350ms
'a' finished.
```

Wie bei Listing 17-5, wo wir mit `trpl::select` Futures beim Abrufen zweier URLs
gegeneinander antreten ließen, endet `select` weiterhin, sobald `a` fertig ist.
Zwischen den Aufrufen von `slow` in den beiden Futures gibt es aber keine
Verschränkung. Das Future `a` erledigt seine gesamte Arbeit, bis der Aufruf
`trpl::sleep` abgewartet wird, dann erledigt das Future `b` seine gesamte
Arbeit, bis sein eigener Aufruf `trpl::sleep` abgewartet wird, und schließlich
wird das Future `a` fertig. Damit beide Futures zwischen ihren langsamen
Aufgaben vorankommen können, brauchen wir Await-Punkte, an denen wir die
Kontrolle an die Runtime zurückgeben können. Wir brauchen also etwas, das wir
abwarten können!

Diese Art von Übergabe sehen wir bereits in Listing 17-15: Würden wir das
`trpl::sleep` am Ende des Futures `a` entfernen, würde es fertig werden, ohne
dass das Future `b` _überhaupt_ läuft. Versuchen wir, die Funktion `trpl::sleep`
als Ausgangspunkt zu verwenden, damit sich Operationen beim Vorankommen
abwechseln können, wie in Listing 17-16 gezeigt.

<Listing number="17-16" caption="Mit `trpl::sleep` Operationen beim Vorankommen abwechseln lassen" file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-16/src/main.rs:here}}
```

</Listing>

Wir haben zwischen den einzelnen Aufrufen von `slow` Aufrufe von `trpl::sleep`
mit Await-Punkten hinzugefügt. Jetzt ist die Arbeit der beiden Futures
verschränkt:

<!-- manual-regeneration
cd listings/ch17-async-await/listing-17-16
cargo run
copy just the output
-->

```text
'a' started.
'a' ran for 30ms
'b' started.
'b' ran for 75ms
'a' ran for 10ms
'b' ran for 10ms
'a' ran for 20ms
'b' ran for 15ms
'a' finished.
```

Das Future `a` läuft immer noch eine Weile, bevor es die Kontrolle an `b`
abgibt, weil es `slow` aufruft, bevor es überhaupt `trpl::sleep` aufruft, aber
danach wechseln sich die Futures jedes Mal ab, wenn eines von ihnen auf einen
Await-Punkt trifft. In diesem Fall haben wir das nach jedem Aufruf von `slow`
getan, aber wir könnten die Arbeit auf jede Weise aufteilen, die für uns am
sinnvollsten ist.

Eigentlich wollen wir hier aber nicht _schlafen_: Wir wollen so schnell wie
möglich vorankommen. Wir müssen nur die Kontrolle an die Runtime zurückgeben.
Das können wir direkt tun, mit der Funktion `trpl::yield_now`. In Listing 17-17
ersetzen wir all diese Aufrufe von `trpl::sleep` durch `trpl::yield_now`.

<Listing number="17-17" caption="Mit `yield_now` Operationen beim Vorankommen abwechseln lassen" file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-17/src/main.rs:yields}}
```

</Listing>

Dieser Code drückt die eigentliche Absicht deutlicher aus und kann erheblich
schneller sein als `sleep`, weil Timer wie der, den `sleep` verwendet, oft in
ihrer Feinheit begrenzt sind. Die Version von `sleep`, die wir verwenden,
schläft zum Beispiel immer mindestens eine Millisekunde, selbst wenn wir ihr
eine `Duration` von einer Nanosekunde übergeben. Noch einmal: Moderne Computer
sind _schnell_: Sie können in einer Millisekunde viel erledigen!

Das bedeutet, dass Async selbst für rechengebundene Aufgaben nützlich sein kann,
je nachdem, was dein Programm sonst noch tut, weil es ein nützliches Werkzeug
bietet, um die Beziehungen zwischen verschiedenen Teilen des Programms zu
strukturieren (allerdings auf Kosten des Mehraufwands für den asynchronen
Zustandsautomaten). Das ist eine Form von _kooperativem Multitasking_
(_cooperative multitasking_), bei dem jedes Future selbst bestimmen kann, wann
es die Kontrolle über Await-Punkte abgibt. Jedes Future trägt daher auch die
Verantwortung, nicht zu lange zu blockieren. In manchen auf Rust basierenden
eingebetteten Betriebssystemen ist das die _einzige_ Art von Multitasking!

In echtem Code wirst du natürlich normalerweise nicht in jeder einzelnen Zeile
Funktionsaufrufe mit Await-Punkten abwechseln. Die Kontrolle auf diese Weise
abzugeben, ist zwar relativ billig, aber nicht kostenlos. In vielen Fällen kann
der Versuch, eine rechengebundene Aufgabe aufzuteilen, sie erheblich
verlangsamen, daher ist es für die _Gesamt_-Performance manchmal besser, eine
Operation kurz blockieren zu lassen. Miss immer, wo die tatsächlichen
Performance-Engpässe deines Codes liegen. Die zugrunde liegende Dynamik solltest
du aber im Hinterkopf behalten, wenn du _tatsächlich_ siehst, dass viel Arbeit
seriell geschieht, von der du erwartet hast, dass sie nebenläufig geschieht!

### Eigene asynchrone Abstraktionen bauen {#building-our-own-async-abstractions}

Wir können Futures auch zusammensetzen, um neue Schemata zu schaffen. Wir können
zum Beispiel eine Funktion `timeout` aus asynchronen Bausteinen bauen, die wir
bereits haben. Wenn wir fertig sind, ist das Ergebnis ein weiterer Baustein, mit
dem wir noch mehr asynchrone Abstraktionen schaffen könnten.

Listing 17-18 zeigt, wie dieses `timeout` mit einem langsamen Future
funktionieren soll.

<Listing number="17-18" caption="Unser gedachtes `timeout` verwenden, um eine langsame Operation mit einem Zeitlimit auszuführen" file-name="src/main.rs">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch17-async-await/listing-17-18/src/main.rs:here}}
```

</Listing>

Implementieren wir das! Denken wir zuerst über die API für `timeout` nach:

- Es muss selbst eine async-Funktion sein, damit wir es abwarten können.
- Sein erster Parameter sollte ein Future sein, das ausgeführt werden soll. Wir
  können es generisch machen, damit es mit jedem Future funktioniert.
- Sein zweiter Parameter ist die maximale Wartezeit. Verwenden wir eine
  `Duration`, lässt sie sich leicht an `trpl::sleep` weitergeben.
- Es sollte ein `Result` zurückgeben. Wird das Future erfolgreich fertig, ist
  das `Result` `Ok` mit dem Wert, den das Future erzeugt hat. Läuft das
  Zeitlimit zuerst ab, ist das `Result` `Err` mit der Dauer, die das Zeitlimit
  gewartet hat.

Listing 17-19 zeigt diese Deklaration.

<!-- This is not tested because it intentionally does not compile. -->

<Listing number="17-19" caption="Die Signatur von `timeout` definieren" file-name="src/main.rs">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch17-async-await/listing-17-19/src/main.rs:declaration}}
```

</Listing>

Das erfüllt unsere Ziele für die Typen. Denken wir jetzt über das nötige
_Verhalten_ nach: Wir wollen das übergebene Future gegen die Dauer antreten
lassen. Mit `trpl::sleep` können wir aus der Dauer ein Timer-Future machen und
mit `trpl::select` diesen Timer zusammen mit dem Future ausführen, das der
Aufrufer übergibt.

In Listing 17-20 implementieren wir `timeout`, indem wir per Pattern-Matching
das Ergebnis des Abwartens von `trpl::select` prüfen.

<Listing number="17-20" caption="`timeout` mit `select` und `sleep` definieren" file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-20/src/main.rs:implementation}}
```

</Listing>

Die Implementierung von `trpl::select` ist nicht fair: Sie pollt die Argumente
immer in der Reihenfolge, in der sie übergeben werden (andere Implementierungen
von `select` wählen zufällig, welches Argument zuerst gepollt wird). Daher
übergeben wir `future_to_try` zuerst an `select`, damit es eine Chance hat,
fertig zu werden, selbst wenn `max_time` eine sehr kurze Dauer ist. Wird
`future_to_try` zuerst fertig, gibt `select` `Left` mit der Ausgabe von
`future_to_try` zurück. Wird `timer` zuerst fertig, gibt `select` `Right` mit
der Ausgabe `()` des Timers zurück.

Ist `future_to_try` erfolgreich und erhalten wir ein `Left(output)`, geben wir
`Ok(output)` zurück. Läuft stattdessen der Timer ab und erhalten wir ein
`Right(())`, ignorieren wir das `()` mit `_` und geben stattdessen
`Err(max_time)` zurück.

Damit haben wir ein funktionierendes `timeout`, das aus zwei anderen asynchronen
Hilfsfunktionen gebaut ist. Wenn wir unseren Code ausführen, gibt er nach Ablauf
des Zeitlimits den Fehlerfall aus:

```text
Failed after 2 seconds
```

Da sich Futures mit anderen Futures zusammensetzen lassen, kannst du aus
kleineren asynchronen Bausteinen wirklich leistungsfähige Werkzeuge bauen. Mit
demselben Ansatz kannst du zum Beispiel Zeitlimits mit Wiederholungsversuchen
kombinieren und diese wiederum bei Operationen wie Netzwerkaufrufen (etwa denen
in Listing 17-5) einsetzen.

In der Praxis arbeitest du meist direkt mit `async` und `await` und in zweiter
Linie mit Funktionen wie `select` und Makros wie dem Makro `join!`, um zu
steuern, wie die äußersten Futures ausgeführt werden.

Wir haben jetzt mehrere Möglichkeiten gesehen, mit mehreren Futures gleichzeitig
zu arbeiten. Als Nächstes sehen wir uns an, wie wir mit _Streams_ mit mehreren
Futures arbeiten können, die im Laufe der Zeit nacheinander eintreffen.

{{#quiz ../quizzes/async-03-more-futures.toml}}

[async-program]: ch17-01-futures-and-syntax.html#our-first-async-program
