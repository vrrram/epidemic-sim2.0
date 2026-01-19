# Streamlit Experiment - NICHT TEIL DES HAUPTPROJEKTS

## WICHTIGER HINWEIS

Die Datei `epidemic_sim_streamlit.py` ist ein **experimenteller Proof-of-Concept** zur Demonstration von Code-Komplexitatsunterschieden zwischen PyQt5 und Streamlit.

**DIES IST NICHT DAS HAUPTPROJEKT.**

## Hauptprojekt: PyQt5-Implementation

Das tatsachliche Epidemic Simulator 3.0-Projekt verwendet **PyQt5** und befindet sich in:

```
epidemic_sim/
├── main.py              # Hauptprogramm
├── model/               # SEIRD-Simulationslogik
├── view/                # PyQt5 GUI (2355 Zeilen)
└── config/              # Parameter und Presets
```

## Warum Streamlit NICHT verwendet wird

Das Streamlit-Experiment zeigt zwar weniger Code (~300 Zeilen), **fehlen aber kritische Features**:

| Feature | PyQt5 (Hauptprojekt) | Streamlit (Experiment) |
|---------|---------------------|------------------------|
| Echtzeit-Partikelanimation (60 FPS) | ✅ | ❌ |
| Offline-Desktop-Anwendung | ✅ | ❌ (Web-basiert) |
| Quarantane-Zonen-Visualisierung | ✅ | ❌ |
| Community-Modus (9-Tile-Grid) | ✅ | ❌ |
| PyQtGraph Echtzeitdiagramme | ✅ | ❌ |
| Dark/Light Theme-System | ✅ | ⚠️ (Eingeschrankt) |
| Keyboard-Shortcuts | ✅ | ❌ |

## Zweck des Experiments

Das Streamlit-Experiment dient ausschließlich zur **technischen Dokumentation** und demonstriert:

1. Wie viel weniger Code deklarative Frameworks fur **einfache** Dashboards benotigen
2. Warum Streamlit fur **dieses spezifische Projekt ungeeignet** ist
3. Trade-offs zwischen Code-Komplexitat und Feature-Vollstandigkeit

## Dokumentation

Detaillierte technische Analyse in:
- `docs/GUI_Framework_Auswahl.md` - Nutzwertanalyse (PyQt5 gewinnt mit 17,0 Punkten)
- `docs/Alternative_Frameworks_Analysis.md` - Warum Alternativen NICHT funktionieren

## Fazit

**PyQt5 ist die einzige technisch geeignete Losung** fur Epidemic Simulator 3.0.

Streamlit kann keine Echtzeit-Partikelanimation und ist web-basiert (kein Offline-Desktop).
Das Experiment zeigt interessante Code-Reduktionen, aber **diese Features fehlen**.

---

**Das Streamlit-Experiment ist ein Vergleichsobjekt, NICHT die Produktionsversion.**
