# Ownership verstehen {#understanding-ownership}

Ownership ist das einzigartigste Feature von Rust und hat tiefgreifende
Auswirkungen auf den Rest der Sprache. Es ermöglicht Rust, Garantien für
Speichersicherheit zu geben, ohne einen Garbage-Collector zu brauchen; deshalb
ist es wichtig zu verstehen, wie Ownership funktioniert. In diesem Kapitel
sprechen wir über Ownership und mehrere verwandte Features: Borrowing, Slices
und wie Rust Daten im Speicher anordnet.
