## Einen Single-Thread-Webserver bauen {#building-a-single-threaded-web-server}

Wir beginnen damit, einen Webserver mit nur einem Thread zum Laufen zu bringen.
Bevor wir anfangen, verschaffen wir uns einen kurzen Überblick über die
Protokolle, die beim Bau von Webservern eine Rolle spielen. Die Details dieser
Protokolle gehen über den Rahmen dieses Buches hinaus, aber ein kurzer Überblick
gibt dir die Informationen, die du brauchst.

Die beiden wichtigsten Protokolle bei Webservern sind das _Hypertext Transfer
Protocol_ _(HTTP)_ und das _Transmission Control Protocol_ _(TCP)_. Beide
Protokolle sind _Anfrage-Antwort_-Protokolle (_request-response_), das heißt,
ein _Client_ stellt Anfragen, und ein _Server_ lauscht auf die Anfragen und
liefert dem Client eine Antwort. Der Inhalt dieser Anfragen und Antworten wird
durch die Protokolle festgelegt.

TCP ist das Protokoll auf niedrigerer Ebene, das die Details beschreibt, wie
Informationen von einem Server zu einem anderen gelangen, aber nicht festlegt,
was diese Informationen sind. HTTP baut auf TCP auf, indem es den Inhalt der
Anfragen und Antworten definiert. Technisch ist es möglich, HTTP mit anderen
Protokollen zu verwenden, aber in den allermeisten Fällen sendet HTTP seine
Daten über TCP. Wir arbeiten mit den rohen Bytes von TCP- und HTTP-Anfragen und
-Antworten.

### Auf die TCP-Verbindung lauschen {#listening-to-the-tcp-connection}

Unser Webserver muss auf eine TCP-Verbindung lauschen, daher ist das der erste
Teil, an dem wir arbeiten. Die Standardbibliothek bietet das Modul `std::net`,
mit dem wir das tun können. Erstellen wir wie gewohnt ein neues Projekt:

```console
$ cargo new hello
     Created binary (application) `hello` project
$ cd hello
```

Gib zu Beginn den Code aus Listing 21-1 in _src/main.rs_ ein. Dieser Code
lauscht an der lokalen Adresse `127.0.0.1:7878` auf eingehende TCP-Streams. Wenn
er einen eingehenden Stream erhält, gibt er `Connection established!` aus.

<Listing number="21-1" file-name="src/main.rs" caption="Auf eingehende Streams lauschen und eine Nachricht ausgeben, wenn wir einen Stream erhalten">

```rust,no_run
{{#rustdoc_include ../listings/ch21-web-server/listing-21-01/src/main.rs}}
```

</Listing>

Mit `TcpListener` können wir an der Adresse `127.0.0.1:7878` auf
TCP-Verbindungen lauschen. In der Adresse ist der Teil vor dem Doppelpunkt eine
IP-Adresse, die deinen Computer darstellt (sie ist auf jedem Computer gleich und
steht nicht speziell für den Computer der Autoren), und `7878` ist der Port. Wir
haben diesen Port aus zwei Gründen gewählt: HTTP wird auf diesem Port
normalerweise nicht angenommen, sodass unser Server wahrscheinlich nicht mit
einem anderen Webserver in Konflikt gerät, der auf deinem Rechner laufen könnte,
und 7878 ist _rust_ auf einer Telefontastatur getippt.

Die Funktion `bind` funktioniert in diesem Szenario wie die Funktion `new`,
indem sie eine neue `TcpListener`-Instanz zurückgibt. Die Funktion heißt `bind`,
weil man im Netzwerkbereich das Verbinden mit einem Port, auf dem gelauscht
werden soll, als „Binden an einen Port“ (_binding to a port_) bezeichnet.

Die Funktion `bind` gibt ein `Result<T, E>` zurück, was anzeigt, dass das Binden
fehlschlagen kann, zum Beispiel wenn wir zwei Instanzen unseres Programms
ausführen und damit zwei Programme auf denselben Port lauschen würden. Weil wir
nur zu Lernzwecken einen einfachen Server schreiben, kümmern wir uns nicht um
die Behandlung solcher Fehler; stattdessen verwenden wir `unwrap`, um das
Programm anzuhalten, wenn Fehler auftreten.

Die Methode `incoming` von `TcpListener` gibt einen Iterator zurück, der uns
eine Folge von Streams liefert (genauer gesagt Streams vom Typ `TcpStream`). Ein
einzelner _Stream_ stellt eine offene Verbindung zwischen dem Client und dem
Server dar. _Verbindung_ (_connection_) ist die Bezeichnung für den gesamten
Anfrage-Antwort-Vorgang, bei dem sich ein Client mit dem Server verbindet, der
Server eine Antwort erzeugt und der Server die Verbindung schließt. Wir lesen
also aus dem `TcpStream`, um zu sehen, was der Client gesendet hat, und
schreiben dann unsere Antwort in den Stream, um Daten an den Client
zurückzusenden. Insgesamt verarbeitet diese `for`-Schleife jede Verbindung der
Reihe nach und erzeugt eine Reihe von Streams, die wir behandeln können.

Vorerst besteht unsere Behandlung des Streams darin, `unwrap` aufzurufen, um
unser Programm zu beenden, wenn der Stream Fehler hat; wenn es keine Fehler
gibt, gibt das Programm eine Nachricht aus. Im nächsten Listing fügen wir mehr
Funktionalität für den Erfolgsfall hinzu. Der Grund, warum wir von der Methode
`incoming` Fehler erhalten könnten, wenn sich ein Client mit dem Server
verbindet, ist, dass wir nicht tatsächlich über Verbindungen iterieren.
Stattdessen iterieren wir über _Verbindungsversuche_. Die Verbindung kann aus
einer Reihe von Gründen fehlschlagen, viele davon betriebssystemspezifisch. Zum
Beispiel haben viele Betriebssysteme eine Obergrenze für die Anzahl gleichzeitig
offener Verbindungen, die sie unterstützen können; neue Verbindungsversuche über
diese Anzahl hinaus erzeugen einen Fehler, bis einige der offenen Verbindungen
geschlossen werden.

Probieren wir diesen Code aus! Rufe im Terminal `cargo run` auf und lade dann
_127.0.0.1:7878_ in einem Webbrowser. Der Browser sollte eine Fehlermeldung wie
„Connection reset“ (Verbindung zurückgesetzt) anzeigen, weil der Server derzeit
keine Daten zurücksendet. Wenn du aber in dein Terminal schaust, solltest du
mehrere Nachrichten sehen, die ausgegeben wurden, als sich der Browser mit dem
Server verbunden hat!

```text
     Running `target/debug/hello`
Connection established!
Connection established!
Connection established!
```

Manchmal siehst du für eine Browseranfrage mehrere ausgegebene Nachrichten; der
Grund könnte sein, dass der Browser sowohl eine Anfrage für die Seite als auch
eine Anfrage für andere Ressourcen stellt, etwa das Symbol _favicon.ico_, das im
Browser-Tab erscheint.

Es könnte auch sein, dass der Browser mehrmals versucht, sich mit dem Server zu
verbinden, weil der Server mit keinen Daten antwortet. Wenn `stream` am Ende der
Schleife den Gültigkeitsbereich (_scope_) verlässt und verworfen (_dropped_)
wird, wird die Verbindung als Teil der `drop`-Implementierung geschlossen.
Browser gehen mit geschlossenen Verbindungen manchmal so um, dass sie es erneut
versuchen, weil das Problem vorübergehend sein könnte.

Browser öffnen manchmal auch mehrere Verbindungen zum Server, ohne Anfragen zu
senden, damit spätere Anfragen, falls sie _doch_ gesendet werden, schneller
erfolgen können. Wenn das passiert, sieht unser Server jede Verbindung,
unabhängig davon, ob über diese Verbindung Anfragen gesendet werden. Viele
Versionen von Chrome-basierten Browsern tun das zum Beispiel; du kannst diese
Optimierung abschalten, indem du den privaten Modus oder einen anderen Browser
verwendest.

Wichtig ist, dass wir erfolgreich ein Handle für eine TCP-Verbindung bekommen
haben!

Denk daran, das Programm mit <kbd>ctrl</kbd>-<kbd>C</kbd> zu beenden, wenn du
mit einer bestimmten Version des Codes fertig bist. Starte das Programm dann
nach jeder Reihe von Codeänderungen mit dem Befehl `cargo run` neu, um
sicherzustellen, dass du den neuesten Code ausführst.

### Die Anfrage lesen {#reading-the-request}

Implementieren wir die Funktionalität, um die Anfrage vom Browser zu lesen! Um
die Belange zu trennen, zuerst eine Verbindung zu bekommen und dann mit der
Verbindung etwas zu tun, beginnen wir eine neue Funktion zur Verarbeitung von
Verbindungen. In dieser neuen Funktion `handle_connection` lesen wir Daten aus
dem TCP-Stream und geben sie aus, damit wir sehen können, welche Daten der
Browser sendet. Ändere den Code so, dass er wie Listing 21-2 aussieht.

<Listing number="21-2" file-name="src/main.rs" caption="Aus dem `TcpStream` lesen und die Daten ausgeben">

```rust,no_run
{{#rustdoc_include ../listings/ch21-web-server/listing-21-02/src/main.rs}}
```

</Listing>

Wir bringen `std::io::BufReader` und `std::io::prelude` in den
Gültigkeitsbereich, um Zugriff auf Traits und Typen zu bekommen, mit denen wir
aus dem Stream lesen und in ihn schreiben können. In der `for`-Schleife in der
Funktion `main` geben wir jetzt keine Nachricht mehr aus, dass wir eine
Verbindung hergestellt haben, sondern rufen die neue Funktion
`handle_connection` auf und übergeben ihr den `stream`.

In der Funktion `handle_connection` erzeugen wir eine neue `BufReader`-Instanz,
die eine Referenz auf den `stream` umhüllt. Der `BufReader` fügt Pufferung
hinzu, indem er die Aufrufe der Methoden des Traits `std::io::Read` für uns
verwaltet.

Wir erzeugen eine Variable namens `http_request`, um die Zeilen der Anfrage zu
sammeln, die der Browser an unseren Server sendet. Dass wir diese Zeilen in
einem Vektor sammeln wollen, geben wir mit der Typannotation `Vec<_>` an.

`BufReader` implementiert den Trait `std::io::BufRead`, der die Methode `lines`
bereitstellt. Die Methode `lines` gibt einen Iterator über
`Result<String,
std::io::Error>` zurück, indem sie den Datenstrom jedes Mal
aufteilt, wenn sie ein Zeilenumbruch-Byte sieht. Um jeden `String` zu erhalten,
wenden wir `map` und `unwrap` auf jedes `Result` an. Das `Result` könnte ein
Fehler sein, wenn die Daten kein gültiges UTF-8 sind oder wenn beim Lesen aus
dem Stream ein Problem aufgetreten ist. Auch hier sollte ein Produktivprogramm
diese Fehler eleganter behandeln, aber wir entscheiden uns der Einfachheit
halber dafür, das Programm im Fehlerfall anzuhalten.

Der Browser signalisiert das Ende einer HTTP-Anfrage, indem er zwei
Zeilenumbruchzeichen hintereinander sendet. Um eine Anfrage aus dem Stream zu
erhalten, nehmen wir daher Zeilen, bis wir eine Zeile bekommen, die der leere
String ist. Sobald wir die Zeilen im Vektor gesammelt haben, geben wir sie mit
schöner Debug-Formatierung aus, damit wir uns die Anweisungen ansehen können,
die der Webbrowser an unseren Server sendet.

Probieren wir diesen Code aus! Starte das Programm und stelle erneut eine
Anfrage in einem Webbrowser. Beachte, dass wir im Browser weiterhin eine
Fehlerseite bekommen, die Ausgabe unseres Programms im Terminal jetzt aber
ungefähr so aussieht:

<!-- manual-regeneration
cd listings/ch21-web-server/listing-21-02
cargo run
make a request to 127.0.0.1:7878
Can't automate because the output depends on making requests
-->

```console
$ cargo run
   Compiling hello v0.1.0 (file:///projects/hello)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.42s
     Running `target/debug/hello`
Request: [
    "GET / HTTP/1.1",
    "Host: 127.0.0.1:7878",
    "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:99.0) Gecko/20100101 Firefox/99.0",
    "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language: en-US,en;q=0.5",
    "Accept-Encoding: gzip, deflate, br",
    "DNT: 1",
    "Connection: keep-alive",
    "Upgrade-Insecure-Requests: 1",
    "Sec-Fetch-Dest: document",
    "Sec-Fetch-Mode: navigate",
    "Sec-Fetch-Site: none",
    "Sec-Fetch-User: ?1",
    "Cache-Control: max-age=0",
]
```

Je nach Browser bekommst du vielleicht eine etwas andere Ausgabe. Jetzt, da wir
die Anfragedaten ausgeben, können wir sehen, warum wir für eine Browseranfrage
mehrere Verbindungen bekommen, indem wir uns den Pfad nach `GET` in der ersten
Zeile der Anfrage ansehen. Wenn die wiederholten Verbindungen alle _/_ anfragen,
wissen wir, dass der Browser wiederholt versucht, _/_ abzurufen, weil er von
unserem Programm keine Antwort bekommt.

Zerlegen wir diese Anfragedaten, um zu verstehen, was der Browser von unserem
Programm will.

<!-- Old headings. Do not remove or links may break. -->

<a id="a-closer-look-at-an-http-request"></a>
<a id="looking-closer-at-an-http-request"></a>

### Eine HTTP-Anfrage genauer betrachten {#looking-more-closely-at-an-http-request}

HTTP ist ein textbasiertes Protokoll, und eine Anfrage hat dieses Format:

```text
Method Request-URI HTTP-Version CRLF
headers CRLF
message-body
```

Die erste Zeile ist die _Anfragezeile_ (_request line_), die Informationen
darüber enthält, was der Client anfragt. Der erste Teil der Anfragezeile gibt
die verwendete Methode an, etwa `GET` oder `POST`, die beschreibt, wie der
Client diese Anfrage stellt. Unser Client hat eine `GET`-Anfrage verwendet, was
bedeutet, dass er nach Informationen fragt.

Der nächste Teil der Anfragezeile ist _/_, was den _Uniform Resource Identifier_
_(URI)_ angibt, den der Client anfragt: Ein URI ist fast, aber nicht ganz
dasselbe wie ein _Uniform Resource Locator_ _(URL)_. Der Unterschied zwischen
URIs und URLs ist für unsere Zwecke in diesem Kapitel nicht wichtig, aber die
HTTP-Spezifikation verwendet den Begriff _URI_, daher können wir hier gedanklich
einfach _URL_ für _URI_ einsetzen.

Der letzte Teil ist die HTTP-Version, die der Client verwendet, und dann endet
die Anfragezeile mit einer CRLF-Sequenz. (_CRLF_ steht für _carriage return_ und
_line feed_, also Wagenrücklauf und Zeilenvorschub – Begriffe aus der Zeit der
Schreibmaschinen!) Die CRLF-Sequenz kann auch als `\r\n` geschrieben werden,
wobei `\r` ein Wagenrücklauf und `\n` ein Zeilenvorschub ist. Die _CRLF-Sequenz_
trennt die Anfragezeile vom Rest der Anfragedaten. Beachte, dass wir bei der
Ausgabe von CRLF den Beginn einer neuen Zeile sehen und nicht `\r\n`.

Wenn wir uns die Daten der Anfragezeile ansehen, die wir bisher beim Ausführen
unseres Programms erhalten haben, sehen wir, dass `GET` die Methode, _/_ der
Anfrage-URI und `HTTP/1.1` die Version ist.

Nach der Anfragezeile sind die übrigen Zeilen ab `Host:` Header. `GET`-Anfragen
haben keinen Rumpf (_body_).

Versuche, eine Anfrage von einem anderen Browser zu stellen oder eine andere
Adresse anzufragen, etwa _127.0.0.1:7878/test_, um zu sehen, wie sich die
Anfragedaten ändern.

Jetzt, da wir wissen, was der Browser will, senden wir ein paar Daten zurück!

### Eine Antwort schreiben {#writing-a-response}

Wir implementieren nun, als Antwort auf eine Client-Anfrage Daten zu senden.
Antworten haben das folgende Format:

```text
HTTP-Version Status-Code Reason-Phrase CRLF
headers CRLF
message-body
```

Die erste Zeile ist eine _Statuszeile_ (_status line_), die die in der Antwort
verwendete HTTP-Version, einen numerischen Statuscode, der das Ergebnis der
Anfrage zusammenfasst, und eine Begründung (_reason phrase_) enthält, die den
Statuscode als Text beschreibt. Nach der CRLF-Sequenz folgen etwaige Header,
eine weitere CRLF-Sequenz und der Rumpf der Antwort.

Hier ist eine Beispielantwort, die HTTP-Version 1.1 verwendet und den Statuscode
200, die Begründung OK, keine Header und keinen Rumpf hat:

```text
HTTP/1.1 200 OK\r\n\r\n
```

Der Statuscode 200 ist die Standard-Erfolgsantwort. Der Text ist eine winzige
erfolgreiche HTTP-Antwort. Schreiben wir sie als Antwort auf eine erfolgreiche
Anfrage in den Stream! Entferne aus der Funktion `handle_connection` das
`println!`, das die Anfragedaten ausgegeben hat, und ersetze es durch den Code
in Listing 21-3.

<Listing number="21-3" file-name="src/main.rs" caption="Eine winzige erfolgreiche HTTP-Antwort in den Stream schreiben">

```rust,no_run
{{#rustdoc_include ../listings/ch21-web-server/listing-21-03/src/main.rs:here}}
```

</Listing>

Die erste neue Zeile definiert die Variable `response`, die die Daten der
Erfolgsnachricht enthält. Dann rufen wir `as_bytes` auf unserer `response` auf,
um die String-Daten in Bytes umzuwandeln. Die Methode `write_all` auf `stream`
nimmt ein `&[u8]` und sendet diese Bytes direkt über die Verbindung. Weil die
Operation `write_all` fehlschlagen könnte, verwenden wir wie zuvor `unwrap` für
jedes Fehlerergebnis. Auch hier würdest du in einer echten Anwendung eine
Fehlerbehandlung hinzufügen.

Führen wir mit diesen Änderungen unseren Code aus und stellen eine Anfrage. Wir
geben keine Daten mehr im Terminal aus, daher sehen wir außer der Ausgabe von
Cargo keine Ausgabe. Wenn du _127.0.0.1:7878_ in einem Webbrowser lädst,
solltest du statt eines Fehlers eine leere Seite bekommen. Du hast gerade von
Hand das Empfangen einer HTTP-Anfrage und das Senden einer Antwort programmiert!

### Echtes HTML zurückgeben {#returning-real-html}

Implementieren wir die Funktionalität, mehr als eine leere Seite zurückzugeben.
Erstelle die neue Datei _hello.html_ im Wurzelverzeichnis deines Projekts, nicht
im Verzeichnis _src_. Du kannst beliebiges HTML eingeben; Listing 21-4 zeigt
eine Möglichkeit.

<Listing number="21-4" file-name="hello.html" caption="Eine Beispiel-HTML-Datei, die in einer Antwort zurückgegeben wird">

```html
{{#include ../listings/ch21-web-server/listing-21-05/hello.html}}
```

</Listing>

Das ist ein minimales HTML5-Dokument mit einer Überschrift und etwas Text. Um es
vom Server zurückzugeben, wenn eine Anfrage eingeht, ändern wir
`handle_connection` wie in Listing 21-5 gezeigt, sodass die Funktion die
HTML-Datei liest, sie als Rumpf zur Antwort hinzufügt und sie sendet.

<Listing number="21-5" file-name="src/main.rs" caption="Den Inhalt von *hello.html* als Rumpf der Antwort senden">

```rust,no_run
{{#rustdoc_include ../listings/ch21-web-server/listing-21-05/src/main.rs:here}}
```

</Listing>

Wir haben `fs` zur `use`-Anweisung hinzugefügt, um das Dateisystem-Modul der
Standardbibliothek in den Gültigkeitsbereich zu bringen. Der Code zum Lesen des
Inhalts einer Datei in einen String sollte dir bekannt vorkommen; wir haben ihn
verwendet, als wir in Listing 12-4 den Inhalt einer Datei für unser I/O-Projekt
gelesen haben.

Als Nächstes verwenden wir `format!`, um den Inhalt der Datei als Rumpf der
Erfolgsantwort hinzuzufügen. Um eine gültige HTTP-Antwort sicherzustellen, fügen
wir den Header `Content-Length` hinzu, der auf die Größe unseres Antwortrumpfs
gesetzt wird – in diesem Fall die Größe von `hello.html`.

Führe diesen Code mit `cargo run` aus und lade _127.0.0.1:7878_ in deinem
Browser; du solltest dein HTML gerendert sehen!

Derzeit ignorieren wir die Anfragedaten in `http_request` und senden einfach
bedingungslos den Inhalt der HTML-Datei zurück. Das bedeutet, wenn du in deinem
Browser _127.0.0.1:7878/something-else_ anfragst, bekommst du trotzdem dieselbe
HTML-Antwort zurück. Im Moment ist unser Server sehr eingeschränkt und tut nicht
das, was die meisten Webserver tun. Wir wollen unsere Antworten je nach Anfrage
anpassen und die HTML-Datei nur bei einer wohlgeformten Anfrage an _/_
zurücksenden.

### Die Anfrage prüfen und gezielt antworten {#validating-the-request-and-selectively-responding}

Im Moment gibt unser Webserver das HTML in der Datei zurück, egal was der Client
angefragt hat. Fügen wir Funktionalität hinzu, um zu prüfen, ob der Browser _/_
anfragt, bevor wir die HTML-Datei zurückgeben, und einen Fehler zurückzugeben,
wenn der Browser etwas anderes anfragt. Dafür müssen wir `handle_connection` wie
in Listing 21-6 gezeigt ändern. Dieser neue Code vergleicht den Inhalt der
empfangenen Anfrage damit, wie eine Anfrage für _/_ aussieht, und fügt `if`- und
`else`-Blöcke hinzu, um Anfragen unterschiedlich zu behandeln.

<Listing number="21-6" file-name="src/main.rs" caption="Anfragen an */* anders behandeln als andere Anfragen">

```rust,no_run
{{#rustdoc_include ../listings/ch21-web-server/listing-21-06/src/main.rs:here}}
```

</Listing>

Wir sehen uns nur die erste Zeile der HTTP-Anfrage an. Statt die ganze Anfrage
in einen Vektor zu lesen, rufen wir daher `next` auf, um das erste Element aus
dem Iterator zu erhalten. Das erste `unwrap` kümmert sich um die `Option` und
hält das Programm an, wenn der Iterator keine Elemente hat. Das zweite `unwrap`
behandelt das `Result` und hat dieselbe Wirkung wie das `unwrap` im `map`, das
wir in Listing 21-2 hinzugefügt haben.

Als Nächstes prüfen wir, ob die `request_line` der Anfragezeile einer
GET-Anfrage an den Pfad _/_ entspricht. Wenn ja, gibt der `if`-Block den Inhalt
unserer HTML-Datei zurück.

Wenn die `request_line` _nicht_ der GET-Anfrage an den Pfad _/_ entspricht,
bedeutet das, dass wir eine andere Anfrage erhalten haben. Gleich fügen wir dem
`else`-Block Code hinzu, um auf alle anderen Anfragen zu antworten.

Führe diesen Code jetzt aus und frage _127.0.0.1:7878_ an; du solltest das HTML
aus _hello.html_ bekommen. Wenn du eine andere Anfrage stellst, etwa
_127.0.0.1:7878/something-else_, bekommst du einen Verbindungsfehler wie die,
die du beim Ausführen des Codes in Listing 21-1 und Listing 21-2 gesehen hast.

Fügen wir nun den Code aus Listing 21-7 zum `else`-Block hinzu, um eine Antwort
mit dem Statuscode 404 zurückzugeben, der signalisiert, dass der Inhalt für die
Anfrage nicht gefunden wurde. Außerdem geben wir etwas HTML für eine Seite
zurück, die im Browser gerendert wird und dem Endbenutzer die Antwort anzeigt.

<Listing number="21-7" file-name="src/main.rs" caption="Mit Statuscode 404 und einer Fehlerseite antworten, wenn etwas anderes als */* angefragt wurde">

```rust,no_run
{{#rustdoc_include ../listings/ch21-web-server/listing-21-07/src/main.rs:here}}
```

</Listing>

Hier hat unsere Antwort eine Statuszeile mit dem Statuscode 404 und der
Begründung `NOT FOUND`. Der Rumpf der Antwort ist das HTML in der Datei
_404.html_. Du musst für die Fehlerseite neben _hello.html_ eine Datei
_404.html_ erstellen; auch hier kannst du beliebiges HTML verwenden oder das
Beispiel-HTML aus Listing 21-8 nehmen.

<Listing number="21-8" file-name="404.html" caption="Beispielinhalt für die Seite, die mit jeder 404-Antwort zurückgesendet wird">

```html
{{#include ../listings/ch21-web-server/listing-21-07/404.html}}
```

</Listing>

Führe deinen Server mit diesen Änderungen erneut aus. Eine Anfrage an
_127.0.0.1:7878_ sollte den Inhalt von _hello.html_ zurückgeben, und jede andere
Anfrage, etwa _127.0.0.1:7878/foo_, sollte das Fehler-HTML aus _404.html_
zurückgeben.

<!-- Old headings. Do not remove or links may break. -->

<a id="a-touch-of-refactoring"></a>

### Refactoring {#refactoring}

Im Moment enthalten die `if`- und `else`-Blöcke viele Wiederholungen: Beide
lesen Dateien und schreiben den Inhalt der Dateien in den Stream. Die einzigen
Unterschiede sind die Statuszeile und der Dateiname. Machen wir den Code
prägnanter, indem wir diese Unterschiede in separate `if`- und `else`-Zeilen
auslagern, die die Werte der Statuszeile und des Dateinamens Variablen zuweisen;
diese Variablen können wir dann im Code zum Lesen der Datei und Schreiben der
Antwort bedingungslos verwenden. Listing 21-9 zeigt den resultierenden Code nach
dem Ersetzen der großen `if`- und `else`-Blöcke.

<Listing number="21-9" file-name="src/main.rs" caption="Die `if`- und `else`-Blöcke so umgestalten, dass sie nur den Code enthalten, der sich zwischen den beiden Fällen unterscheidet">

```rust,no_run
{{#rustdoc_include ../listings/ch21-web-server/listing-21-09/src/main.rs:here}}
```

</Listing>

Jetzt geben die `if`- und `else`-Blöcke nur die passenden Werte für die
Statuszeile und den Dateinamen in einem Tupel zurück; dann verwenden wir
Destrukturierung, um diese beiden Werte mit einem Pattern in der `let`-Anweisung
`status_line` und `filename` zuzuweisen, wie in Kapitel 19 besprochen.

Der zuvor duplizierte Code steht jetzt außerhalb der `if`- und `else`-Blöcke und
verwendet die Variablen `status_line` und `filename`. So ist der Unterschied
zwischen den beiden Fällen leichter zu erkennen, und wir haben nur eine Stelle,
an der wir den Code aktualisieren müssen, wenn wir ändern wollen, wie das Lesen
der Datei und das Schreiben der Antwort funktionieren. Das Verhalten des Codes
in Listing 21-9 ist dasselbe wie das in Listing 21-7.

Großartig! Wir haben jetzt einen einfachen Webserver in ungefähr 40 Zeilen
Rust-Code, der auf eine Anfrage mit einer Inhaltsseite und auf alle anderen
Anfragen mit einer 404-Antwort antwortet.

Derzeit läuft unser Server in einem einzigen Thread und kann daher immer nur
eine Anfrage gleichzeitig bedienen. Untersuchen wir, inwiefern das ein Problem
sein kann, indem wir einige langsame Anfragen simulieren. Dann beheben wir das,
damit unser Server mehrere Anfragen gleichzeitig verarbeiten kann.
