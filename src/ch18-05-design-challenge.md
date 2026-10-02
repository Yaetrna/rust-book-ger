# Abwägungen beim Design {#design-trade-offs}

In diesem Abschnitt geht es um **Abwägungen beim Design** (_design trade-offs_) in Rust. Um Rust wirkungsvoll einzusetzen, reicht es nicht, nur zu wissen, wie Rust funktioniert. Du musst entscheiden, welche der vielen Werkzeuge von Rust für eine bestimmte Aufgabe geeignet sind. In diesem Abschnitt stellen wir dir eine Reihe von Quiz, die dein Verständnis von Abwägungen beim Design in Rust prüfen. Nach jedem Quiz erklären wir ausführlich unsere Begründung für jede Frage.

Hier ist ein Beispiel dafür, wie eine Frage aussehen wird. Sie beginnt mit der Beschreibung einer Software-Fallstudie mit einer Reihe möglicher Designs:

> **Kontext:** Du entwirfst eine Anwendung mit einer globalen Konfiguration, die z. B. Kommandozeilen-Flags enthält.
>
> **Funktionalität:** Die Anwendung muss unveränderliche (_immutable_) Referenzen auf diese Konfiguration in der gesamten Anwendung weitergeben.
>
> **Designs:** Unten stehen mehrere vorgeschlagene Designs, um die Funktionalität zu implementieren.
>
> ```rust,ignore
> use std::rc::Rc;
> use std::sync::Arc;
>
> struct Config { 
>     flags: Flags,
>     // .. more fields ..
> }
> 
> // Option 1: use a reference
> struct ConfigRef<'a>(&'a Config);
> 
> // Option 2: use a reference-counted pointer
> struct ConfigRef(Rc<Config>);
> 
> // Option 3: use an atomic reference-counted pointer
> struct ConfigRef(Arc<Config>);
> ```

Wenn man nur den Kontext und die zentrale Funktionalität betrachtet, kommen alle drei Designs infrage.
Wir brauchen mehr Informationen über die Ziele des Systems, um zu entscheiden, welche am sinnvollsten sind.
Daher stellen wir eine neue Anforderung:

> Wähle jede Design-Option aus, die die folgende Anforderung erfüllt:
>
> **Anforderung:** Die Referenz auf die Konfiguration muss zwischen mehreren Threads geteilt werden können.
>
> **Antwort:**
>
> <input type="checkbox" checked disabled> Option 1 <br>
> <input type="checkbox" disabled> Option 2 <br>
> <input type="checkbox" checked disabled> Option 3 <br>

Formal ausgedrückt bedeutet das, dass `ConfigRef` [`Send`] und [`Sync`] implementiert.
Unter der Annahme `Config: Send + Sync` erfüllen sowohl `&Config` als auch `Arc<Config>` diese Anforderung,
[`Rc`] aber nicht (weil nicht-atomare Zeiger mit Referenzzählung nicht threadsicher sind). Option 2 erfüllt die Anforderung also nicht, Option 3 dagegen schon.

Wir könnten auch versucht sein zu folgern, dass Option 1 die Anforderung nicht erfüllt, weil Funktionen wie [`thread::spawn`] verlangen, dass alle in einen Thread verschobenen (_moved_) Daten nur Referenzen mit einer `'static`-Lifetime enthalten dürfen. Das schließt Option 1 jedoch aus zwei Gründen nicht aus:

1. Die `Config` könnte als globale statische Variable gespeichert werden (z. B. mit [`OnceLock`]), sodass man Referenzen vom Typ `&'static Config` konstruieren könnte.
2. Nicht alle Nebenläufigkeitsmechanismen erfordern `'static`-Lifetimes, zum Beispiel [`thread::scope`].

Daher schließt die Anforderung in der angegebenen Form nur Typen aus, die nicht [`Send`] sind, und wir betrachten die Optionen 1 und 3 als richtige Antworten.

[`thread::spawn`]: https://doc.rust-lang.org/std/thread/fn.spawn.html
[`Send`]: https://doc.rust-lang.org/std/marker/trait.Send.html
[`Sync`]: https://doc.rust-lang.org/std/marker/trait.Sync.html
[`Rc`]: https://doc.rust-lang.org/std/rc/struct.Rc.html
[`OnceLock`]: https://doc.rust-lang.org/std/sync/struct.OnceLock.html
[`thread::scope`]: https://doc.rust-lang.org/std/thread/fn.scope.html

<hr>

Jetzt bist du mit den Fragen unten an der Reihe! Jeder Abschnitt enthält ein Quiz, das sich auf ein einzelnes Szenario konzentriert. Bearbeite das Quiz und lies nach jedem Quiz unbedingt die Erläuterungen zu den Antworten.

<!-- These questions are both experimental and opinionated &mdash; please leave us feedback via the bug button 🐞 if you disagree with our answers. -->

Zu jedem Quiz haben wir außerdem Links zu beliebten Rust-Crates angegeben, die als Inspiration für das Quiz gedient haben.

## Referenzen {#references}

_Inspiration:_ [Bevy-Assets][Bevy assets], [Petgraph-Knotenindizes][Petgraph node indices], [Cargo-Units][Cargo units]

{{#quiz ../quizzes/ch17-05-design-challenge-references.toml}}

[Bevy assets]: https://docs.rs/bevy/0.11.2/bevy/asset/struct.Assets.html
[Petgraph node indices]: https://docs.rs/petgraph/0.6.4/petgraph/graph/struct.NodeIndex.html
[Cargo units]: https://docs.rs/cargo/0.73.1/cargo/core/compiler/struct.Unit.html

## Trait-Bäume {#trait-trees}

_Inspiration:_ [Yew-Komponenten][Yew components], [Druid-Widgets][Druid widgets]

{{#quiz ../quizzes/ch17-05-design-challenge-trait-trees.toml}}

[Yew components]: https://docs.rs/yew/0.20.0/yew/html/trait.Component.html
[Druid widgets]: https://docs.rs/druid/0.8.3/druid/trait.Widget.html

## Dispatch {#dispatch}

_Inspiration:_ [Bevy-Systeme][Bevy systems], [Diesel-Queries][Diesel queries], [Axum-Handler][Axum handlers]

{{#quiz ../quizzes/ch17-05-design-challenge-dispatch.toml}}

[Bevy systems]: https://docs.rs/bevy_ecs/0.11.2/bevy_ecs/system/trait.IntoSystem.html
[Diesel queries]: https://docs.diesel.rs/2.1.x/diesel/query_dsl/trait.BelongingToDsl.html
[Axum handlers]: https://docs.rs/axum/0.6.20/axum/handler/trait.Handler.html

## Zwischendarstellungen {#intermediates}

_Inspiration:_ [Serde] und [miniserde]

{{#quiz ../quizzes/ch17-05-design-challenge-intermediates.toml}}

[Serde]: https://docs.rs/serde/1.0.188/serde/trait.Serialize.html
[miniserde]: https://docs.rs/miniserde/0.1.34/miniserde/trait.Serialize.html
