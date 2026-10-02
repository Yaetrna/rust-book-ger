## Ownership-Inventur #1 {#ownership-inventory-1}

Die Ownership-Inventur ist eine Reihe von Quiz, die dein Verständnis von Ownership in praxisnahen Szenarien prüfen. Diese Szenarien sind von häufigen Fragen zu Rust auf StackOverflow inspiriert. Mit diesen Fragen kannst du testen, wie gut du Ownership bisher verstehst.

### Eine neue Technologie: die IDE im Browser {#a-new-technology-the-in-browser-ide}

In diesen Fragen geht es um Rust-Programme, die Funktionen verwenden, die du noch nicht kennst. Deshalb verwenden wir eine experimentelle Technologie, die IDE-Features im Browser unterstützt. Mit der IDE kannst du Informationen über unbekannte Funktionen und Typen abrufen. Probier im folgenden Programm zum Beispiel diese Aktionen aus:

- Bewege die Maus über `replace`, um seinen Typ und seine Beschreibung zu sehen.
- Bewege die Maus über `s2`, um seinen abgeleiteten Typ zu sehen.

---

<pre>
<code class="ide">
/// Turns a string into a far more exciting string
fn make_exciting(s: &str) -> String {
  let s2 = s.replace(".", "!");
  let s3 = s2.replace("?", "‽");
  s3
}
</code>
</pre>

---

Einige wichtige Einschränkungen dieser experimentellen Technologie:

**PLATTFORMKOMPATIBILITÄT:** Die IDE im Browser funktioniert nicht auf Touchscreens. Die IDE im Browser wurde nur mit Google Chrome 109 und Firefox 107 getestet. In älteren Safari-Versionen funktioniert sie möglicherweise nicht.

**SPEICHERVERBRAUCH:** Die IDE im Browser verwendet einen [WebAssembly](https://rustwasm.github.io/book/)-Build von [rust-analyzer](https://github.com/rust-lang/rust-analyzer), der ziemlich viel Speicher belegen kann. Jede Instanz der IDE scheint etwa ~300 MB zu belegen. (Hinweis: Uns haben auch einige Berichte über einen Speicherverbrauch von >10 GB erreicht.)

**SCROLLEN:** Die IDE im Browser „schluckt“ deinen Mauszeiger, wenn er beim Scrollen über den Editor fährt. Wenn du Probleme beim Scrollen der Seite hast, bewege den Mauszeiger auf die Bildlaufleiste ganz rechts.

**LADEZEITEN:** Die IDE kann bis zu 15 Sekunden brauchen, um ein neues Programm zu initialisieren. Während du mit dem Code im Editor arbeitest, zeigt sie „Loading...“ an.

### Das Quiz {#the-quiz}

{{#quiz ../quizzes/ch06-04-inventory.toml}}
