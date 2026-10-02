# Fehlerbehandlung {#error-handling}

Fehler gehören in der Software einfach dazu, daher hat Rust eine Reihe von
Features für Situationen, in denen etwas schiefgeht. In vielen Fällen verlangt
Rust von dir, die Möglichkeit eines Fehlers anzuerkennen und etwas zu
unternehmen, bevor dein Code kompiliert. Diese Anforderung macht dein Programm
robuster, weil sie sicherstellt, dass du Fehler entdeckst und angemessen
behandelst, bevor du deinen Code in Produktion bringst!

Rust teilt Fehler in zwei große Kategorien ein: behebbare und nicht behebbare
Fehler. Bei einem _behebbaren Fehler_ (_recoverable error_), etwa einem Fehler
_Datei nicht gefunden_, wollen wir das Problem höchstwahrscheinlich nur melden
und die Operation erneut versuchen. _Nicht behebbare Fehler_ (_unrecoverable
errors_) sind immer Symptome von Bugs, etwa der Versuch, auf eine Stelle hinter
dem Ende eines Arrays zuzugreifen, daher wollen wir das Programm sofort beenden.

Die meisten Sprachen unterscheiden nicht zwischen diesen beiden Arten von
Fehlern und behandeln beide gleich, mit Mechanismen wie Exceptions. Rust hat
keine Exceptions. Stattdessen gibt es den Typ `Result<T, E>` für behebbare
Fehler und das Makro `panic!`, das die Ausführung stoppt, wenn das Programm auf
einen nicht behebbaren Fehler stößt. Dieses Kapitel behandelt zuerst den Aufruf
von `panic!` und geht dann auf die Rückgabe von `Result<T, E>`-Werten ein.
Außerdem sehen wir uns an, was man bedenken sollte, wenn man entscheidet, ob man
versucht, einen Fehler zu beheben, oder die Ausführung stoppt.
