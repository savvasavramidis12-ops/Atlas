# TikTok-Kanal: Geldwissen (faceless, Deutsch)

Arbeitsanleitung für jedes neue Video. Ziel des Kanals: langfristig Geld verdienen.

## Nische und Format

- **Nische:** Privatfinanzen für Einsteiger in Deutschland (Sparen, ETF-Grundlagen, Zinseszins, Steuern im Alltag, Gehalt, Rente).
- **Sprache:** Deutsch. Preise in Euro, deutsche Zahlenschreibweise (24.000 €).
- **Format:** 1080×1920, 30 fps, **61–75 Sekunden** (über einer Minute bleiben), Sprecherstimme plus große Schrift. Kein Gesicht, keine Stockvideos.
- **Look:** gelber Grund `#ffd21f`, Schwarz `#121212`, Grün `#0b7a3e`, Rot-Orange `#e8452c`; Schrift Archivo Black und Inter. Text nur zwischen y=168 und y=1330.

## Aufbau jedes Videos

1. **Hook (0–4 s):** eine Frage oder überraschende Zahl, schon im ersten Bild sichtbar. Nie mit „Hallo" oder dem Kanalnamen beginnen.
2. **Aufbau:** ein konkretes Beispiel mit zwei Personen oder zwei Wegen und echten, nachgerechneten Zahlen.
3. **Köder:** die naheliegende, falsche Antwort anbieten und zum Kommentieren auffordern.
4. **Auflösung:** die Zahlen laufen sichtbar (Balken, Zähler), dann das Ergebnis.
5. **Warum:** ein Satz Erklärung.
6. **Schluss:** ein Merksatz, „Folge für mehr Geldwissen", Hinweis „Keine Anlageberatung".

## Regeln

- Jede Zahl wird im Skript berechnet, nie geschätzt. Annahmen (z. B. 7 % Rendite) stehen im Bild.
- Keine Empfehlung einzelner Aktien, Coins oder Anbieter. Keine Renditeversprechen.
- Jedes Video hat ein neues Thema und eine neue Hook; kein Thema aus `themen.md` zweimal.

## Herstellung

- Vorlage: `001-zinseszins-duell/` kopieren. `script.tsv` enthält die Sprechsätze (eine Zeile pro Satz), `build.py` erzeugt Tonspur, Szenen und Zeitplan aus den Satzlängen.
- Stimme: derzeit Piper „Thorsten" (einfache Qualität, nur Übergang). Eine bessere deutsche Stimme ist noch offen.
- Ablauf: Sätze vertonen → `python3 build.py <ordner-mit-ton> .` → `hyperframes check` → Standbilder ansehen → `hyperframes render --quality delivery`.
- Fertiges Video und Projekt nach `tiktok/NNN-kurzname/` committen und `themen.md` abhaken.
