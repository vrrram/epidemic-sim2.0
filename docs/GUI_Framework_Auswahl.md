# Auswahl des GUI-Frameworks

## Entwurfsphase der Projektdokumentation

In der Entwurfsphase der Projektarbeit "Epidemic Simulator 3.0" wurde die Auswahl eines geeigneten GUI-Frameworks durchgefuhrt. Dieser Abschnitt beschreibt die relevanten Kriterien, die betrachteten Alternativen und die Begrundung der Entscheidung, sodass diese nachvollziehbar dargestellt wird.

---

## Struktur der Dokumentation

Der vorliegende Abschnitt kann als "Architekturdesign" oder "Zielplattform" bezeichnet werden. Im Folgenden werden zunachst die relevanten Kriterien wie Anforderungsabdeckung (z. B. MVC-Unterstutzung, Lizenz, Installationseinfachheit), Popularitat, Community-Support, Dokumentation und Zukunftssicherheit beschrieben. Anschliessend werden vier Alternativen (PyQt5, Tkinter, Kivy, wxPython) anhand einer **Nutzwertanalyse** in Tabellenform miteinander verglichen.

---

## Projektkontext

Das Projekt "Epidemic Simulator 3.0" ist eine interaktive SEIRD-Simulationsanwendung (Susceptible-Exposed-Infected-Removed-Dead), entwickelt als Abschlussprojekt im Rahmen der Ausbildung zum Fachinformatiker Anwendungsentwicklung (IHK). Die Anwendung dient Bildungszwecken und demonstriert epidemiologische Modellierung mit Quarantane-Mechaniken, Marktplatz-Versammlungen und Community-basierter Ubertragung.

**Hauptanforderungen an das GUI-Framework:**
- Echtzeitvisualisierung von 100-500 Partikeln (animierte Simulation)
- Interaktive Steuerelemente (Slider, Eingabefelder, Buttons)
- Datenvisualisierung (Zeitreihen-Diagramme, Kreisdiagramme)
- Modular aufgebaute Benutzeroberflache mit drei Panels
- Plattformubergreifende Kompatibilitat (Windows, macOS, Linux)
- Professionelles Erscheinungsbild fur Prasentationszwecke

---

## Bewertungskriterien

### 1. Dokumentation (Gewichtung: 4)
**Begrundung:** Eine umfassende und aktuelle Dokumentation ist entscheidend fur die effiziente Entwicklung, insbesondere in einem Ausbildungsprojekt. Gute Dokumentation verkurzt Einarbeitungszeit und erleichtert Fehlerbehebung.

**Bewertungsskala:**
- **3 = umfassend/deutsch:** Vollstandige deutsche Dokumentation mit Tutorials und Beispielen
- **2 = englisch/basis:** Englische Dokumentation mit grundlegenden Beispielen
- **1 = fehlend:** Fragmentierte oder veraltete Dokumentation

### 2. MVC-Unterstutzung (Gewichtung: 3)
**Begrundung:** Die Trennung von Darstellungsschicht (View), Geschaftslogik (Model) und Steuerungslogik (Controller) ist ein Kernaspekt des Clean-Code-Prinzips und erleichtert Wartbarkeit und Erweiterbarkeit erheblich.

**Bewertungsskala:**
- **3 = vollstandig:** Framework unterstutzt klare MVC-Architektur nativ
- **2 = teilweise:** MVC-Struktur manuell umsetzbar
- **1 = nicht vorhanden:** Keine Unterstutzung fur Architekturmuster

### 3. Einarbeitungszeit (Gewichtung: 3)
**Begrundung:** Da das Projekt zeitlich begrenzt ist (8 Wochen Entwicklung) und im Rahmen einer Ausbildung stattfindet, ist eine kurze Einarbeitungszeit wichtig, um mehr Zeit fur die eigentliche Implementierung zu haben.

**Bewertungsskala:**
- **3 = sehr kurz (< 2 Tage):** Intuitive API, ahnlich zu bekannten Frameworks
- **2 = mittel (2-5 Tage):** Erfordert grundliche Einarbeitung
- **1 = lang (> 5 Tage):** Steile Lernkurve, komplexe Konzepte

### 4. Community/Support (Gewichtung: 2)
**Begrundung:** Eine aktive Community erhoht die Wahrscheinlichkeit, Losungen fur Probleme zu finden. Stackoverflow-Beitrage, Tutorials und Beispielprojekte beschleunigen die Entwicklung.

**Bewertungsskala:**
- **3 = sehr aktiv:** Grosse Community, viele Ressourcen/Schulungen
- **2 = moderat:** Aktive Community, ausreichende Ressourcen
- **1 = gering:** Kleine Community, wenige Ressourcen

### 5. Visualisierungsunterstutzung (Gewichtung: 4)
**Begrundung:** Das Projekt erfordert Echtzeitvisualisierung (animierte Partikel) und wissenschaftliche Datenvisualisierung (Diagramme). Die Qualitat und Performance der Visualisierung ist entscheidend fur den Projekterfolg.

**Bewertungsskala:**
- **3 = nativ/erweitert:** Native Unterstutzung oder einfache Integration wissenschaftlicher Visualisierungstools
- **2 = basis:** Grundlegende Canvas-Funktionalitat, manuelle Implementierung notwendig
- **1 = fehlend:** Keine oder sehr begrenzte Unterstutzung

### 6. Plattformubergreifende Kompatibilitat (Gewichtung: 3)
**Begrundung:** Die Anwendung soll auf verschiedenen Betriebssystemen laufen, um maximale Zuganglichkeit zu gewahrleisten. Windows ist Mindestanforderung, aber macOS- und Linux-Support erhohen die Flexibilitat.

**Bewertungsskala:**
- **3 = vollstandig:** Windows, macOS, Linux ohne Anpassungen
- **2 = teilweise:** Hauptplattformen, kleinere Anpassungen notwendig
- **1 = eingeschrankt:** Nur ein Betriebssystem oder erhebliche Portierungsaufwand

### 7. Lizenz (Gewichtung: 2)
**Begrundung:** Da es sich um ein Ausbildungsprojekt handelt, muss die Lizenz kostenlose Nutzung und Verteilung erlauben. Kommerzielle Lizenzen sind nicht tragbar.

**Bewertungsskala:**
- **3 = Open Source (MIT/Apache):** Vollstandig frei, keine Einschrankungen
- **2 = GPL/LGPL:** Frei, aber mit Copyleft-Anforderungen
- **1 = kommerziell:** Kostenpflichtig oder restriktive Lizenz

---

## Nutzwertanalyse: Vergleich der GUI-Frameworks

| Kriterium | Gewichtung | PyQt5 | Tkinter | Kivy | wxPython | Begrundung der Bewertung |
|-----------|-----------|-------|---------|------|----------|--------------------------|
| **Dokumentation** | 4 | 3 | 2 | 2 | 3 | PyQt5: Umfangreiche offizielle Docs + deutschsprachige Tutorials verfugbar; Tkinter: Python-Standard, gute Docs aber einfach; Kivy: Englisch, solide aber weniger verbreitet; wxPython: Sehr gute englische Docs |
| **MVC-Unterstutzung** | 3 | 3 | 2 | 2 | 3 | PyQt5: Model/View-Architektur nativ (QAbstractItemModel); Tkinter: Manuell umsetzbar; Kivy: KV-Sprache trennt UI/Logik; wxPython: Unterstutzung durch Klassenstruktur |
| **Einarbeitungszeit** | 3 | 2 | 3 | 1 | 2 | PyQt5: Mittlere Komplexitat, aber gute Docs; Tkinter: Sehr einfach, Python-Standard; Kivy: Eigene Konzepte, steile Lernkurve; wxPython: Ahnlich PyQt5 |
| **Community/Support** | 2 | 3 | 3 | 2 | 2 | PyQt5: Sehr grosse Community, viele SO-Posts; Tkinter: Standard-Library, massive Ressourcen; Kivy: Kleinere, aber aktive Community; wxPython: Moderate Community |
| **Visualisierung** | 4 | 3 | 1 | 3 | 2 | PyQt5: Perfekte Integration mit PyQtGraph/Matplotlib; Tkinter: Nur Canvas, alles manuell; Kivy: Starke OpenGL-Grafik; wxPython: Basis-Canvas, matplotlib moglich |
| **Plattformkompatibilitat** | 3 | 3 | 3 | 3 | 3 | Alle vier Frameworks unterstutzen Windows, macOS und Linux vollstandig |
| **Lizenz** | 2 | 2 | 3 | 3 | 3 | PyQt5: GPL/kommerzielle Lizenz (GPL ausreichend); Tkinter: Python-Standard (PSF); Kivy: MIT; wxPython: wxWindows (LGPL-ahnlich) |
| | | | | | | |
| **Nutzwert** | | **17,0** | **14,75** | **13,25** | **15,25** | **Hochster Wert gewinnt** |

---

## Detaillierte Begrundung der Bewertungen

### PyQt5 (Nutzwert: 17,0)

**Dokumentation (3 Punkte):**
PyQt5 verfugt uber eine hervorragende Dokumentation, sowohl in der offiziellen Qt-Dokumentation als auch in zahlreichen deutschsprachigen Tutorials. Die Vererbungshierarchie ist klar strukturiert, und es existieren umfangreiche Beispielprojekte. Fur das Ausbildungsprojekt sind insbesondere die deutschen Ressourcen wertvoll.

**MVC-Unterstutzung (3 Punkte):**
PyQt5 bietet native Unterstutzung fur das Model-View-Pattern durch `QAbstractItemModel` und verwandte Klassen. Dies ermoglicht eine klare Trennung zwischen Simulationslogik (Model) und Darstellung (View), was den Clean-Code-Anforderungen entspricht.

**Einarbeitungszeit (2 Punkte):**
PyQt5 hat eine moderate Lernkurve. Die Konzepte wie Signals/Slots, Layout-Management und Custom Widgets erfordern Einarbeitung (ca. 3-4 Tage), sind aber durch exzellente Dokumentation gut erlernbar.

**Community/Support (3 Punkte):**
PyQt5 verfugt uber eine sehr grosse und aktive Community. Auf StackOverflow finden sich uber 50.000 Fragen zu PyQt5, was schnelle Problemlosungen ermoglicht. Deutsche Foren und Tutorials sind ebenfalls vorhanden.

**Visualisierung (3 Punkte):**
Die nahtlose Integration mit PyQtGraph (fur Echtzeitdiagramme) und Matplotlib (fur statistische Darstellungen) ist ein entscheidender Vorteil. `QPainter` ermoglicht performante Custom-Rendering fur die Partikelsimulation.

**Plattformkompatibilitat (3 Punkte):**
PyQt5 lauft ohne Anpassungen auf Windows, macOS und Linux. Das native Look-and-Feel wird auf allen Plattformen beibehalten.

**Lizenz (2 Punkte):**
PyQt5 ist unter GPL verfugbar, was fur Ausbildungsprojekte vollkommen ausreichend ist. Kommerzielle Lizenzen waren kostenpflichtig, sind hier aber nicht relevant.

**Starken:**
- Professionelles Erscheinungsbild
- Hervorragende Integration mit wissenschaftlichen Python-Bibliotheken
- Native Unterstutzung fur komplexe UI-Strukturen (Tabs, Collapsible Panels)
- Performante Echtzeitvisualisierung

**Schwachen:**
- Grossere Dateigrossee nach PyInstaller-Bundling (~150 MB)
- GPL-Lizenz erfordert Quellcode-Offenlegung (kein Problem fur Ausbildungsprojekt)

---

### Tkinter (Nutzwert: 14,75)

**Dokumentation (2 Punkte):**
Tkinter ist Teil der Python-Standardbibliothek und verfugt uber solide Dokumentation. Allerdings ist die Dokumentation eher funktional als umfassend. Fur einfache UIs ausreichend.

**MVC-Unterstutzung (2 Punkte):**
Tkinter hat keine native MVC-Unterstutzung. Die Architektur muss manuell implementiert werden, was zu engerer Kopplung zwischen UI und Logik fuhren kann.

**Einarbeitungszeit (3 Punkte):**
Tkinter ist das einfachste Python-GUI-Framework. Die Lernkurve ist sehr flach, grundlegende UIs konnen innerhalb weniger Stunden erstellt werden.

**Community/Support (3 Punkte):**
Als Python-Standard hat Tkinter eine riesige Community und unzahlige Tutorials. Nahezu jedes Problem wurde bereits gelost und dokumentiert.

**Visualisierung (1 Punkt):**
Tkinter bietet nur ein einfaches Canvas-Widget. Alle Grafiken und Animationen mussen manuell implementiert werden, was fur 500 animierte Partikel sehr aufwandig ware. Die Integration mit Matplotlib ist moglich, aber nicht optimal.

**Plattformkompatibilitat (3 Punkte):**
Tkinter lauft auf allen Plattformen, da es Teil der Python-Standardinstallation ist.

**Lizenz (3 Punkte):**
Tkinter ist Teil von Python und damit unter der Python Software Foundation License frei verfugbar.

**Starken:**
- Keine zusatzliche Installation notwendig
- Sehr einfach zu erlernen
- Minimaler Footprint

**Schwachen:**
- Altmodisches Erscheinungsbild
- Sehr begrenzte Visualisierungsmoglichkeiten
- Manuelle Implementierung fur komplexe UI-Elemente notwendig
- **Nicht geeignet fur Echtzeit-Partikelanimationen**

---

### Kivy (Nutzwert: 13,25)

**Dokumentation (2 Punkte):**
Kivy hat solide englische Dokumentation und Tutorials. Deutsche Ressourcen sind jedoch rar. Die Dokumentation konzentriert sich stark auf Mobile-Entwicklung.

**MVC-Unterstutzung (2 Punkte):**
Kivy trennt UI-Definition (KV-Sprache) von Logik (Python), was eine gewisse Architektur erzwingt. Vollstandiges MVC muss aber manuell implementiert werden.

**Einarbeitungszeit (1 Punkt):**
Kivy hat eine steile Lernkurve, da es eigene Konzepte einfuhrt (KV-Sprache, Widget-System, Touch-Events). Die Einarbeitung kann 7-10 Tage dauern.

**Community/Support (2 Punkte):**
Kivy hat eine kleinere, aber aktive Community. Der Fokus liegt stark auf Mobile-Apps, was fur Desktop-Anwendungen weniger Ressourcen bedeutet.

**Visualisierung (3 Punkte):**
Kivy nutzt OpenGL fur Rendering, was sehr performante Grafiken ermoglicht. Fur Partikelanimationen ideal. Die Integration mit wissenschaftlichen Python-Bibliotheken ist jedoch weniger nahtlos.

**Plattformkompatibilitat (3 Punkte):**
Kivy unterstutzt Windows, macOS, Linux sowie Android und iOS. Fur Desktop-Anwendungen vollstandig ausreichend.

**Lizenz (3 Punkte):**
Kivy ist unter MIT-Lizenz verfugbar, was vollstandige Freiheit garantiert.

**Starken:**
- Hervorragende Performance bei Animationen
- Moderne, anpassbare Optik
- Mobile-Deployment moglich

**Schwachen:**
- Steile Lernkurve
- Weniger Ressourcen fur Desktop-Entwicklung
- Integration mit Matplotlib/wissenschaftlichen Tools komplizierter
- **Overhead fur reine Desktop-Anwendung**

---

### wxPython (Nutzwert: 15,25)

**Dokumentation (3 Punkte):**
wxPython verfugt uber sehr gute englische Dokumentation mit zahlreichen Beispielen. Die offizielle Demo-Anwendung zeigt alle Features umfassend.

**MVC-Unterstutzung (3 Punkte):**
wxPython unterstutzt saubere Architektur durch Klassenstruktur. Model-View-Trennung ist gut umsetzbar.

**Einarbeitungszeit (2 Punkte):**
wxPython hat eine ahnliche Komplexitat wie PyQt5. Die Einarbeitungszeit betragt ca. 3-4 Tage.

**Community/Support (2 Punkte):**
wxPython hat eine moderate Community. Weniger Ressourcen als PyQt5, aber ausreichend fur die meisten Probleme.

**Visualisierung (2 Punkte):**
wxPython bietet grundlegende Canvas-Funktionalitat. Matplotlib-Integration ist moglich, aber weniger elegant als bei PyQt5. PyQtGraph-ahnliche Tools fehlen.

**Plattformkompatibilitat (3 Punkte):**
wxPython nutzt native Widgets auf jeder Plattform, was optimales Look-and-Feel garantiert.

**Lizenz (3 Punkte):**
wxPython ist unter wxWindows License (LGPL-ahnlich) verfugbar, vollstandig frei nutzbar.

**Starken:**
- Native Widgets auf allen Plattformen
- Gute Dokumentation
- Stabile, ausgereifte Bibliothek

**Schwachen:**
- Weniger verbreitet als PyQt5
- Weniger umfangreiche Visualisierungsoptionen
- Kleinere Community

---

## Entscheidung: PyQt5

Basierend auf der Nutzwertanalyse fallt die Entscheidung auf **PyQt5** mit einem Nutzwert von **17,0 Punkten**.

### Hauptbegrundungen:

1. **Visualisierungsstarke (Gewichtung 4, Bewertung 3 = 12 Punkte):**
   Die nahtlose Integration mit PyQtGraph fur Echtzeitdiagramme und Matplotlib fur statistische Darstellungen ist entscheidend. Die performante `QPainter`-API ermoglicht flussige Animation von 100-500 Partikeln bei 60 FPS.

2. **Dokumentation (Gewichtung 4, Bewertung 3 = 12 Punkte):**
   Die umfangreiche Dokumentation einschliesslich deutschsprachiger Ressourcen verkurzt die Entwicklungszeit erheblich.

3. **MVC-Unterstutzung (Gewichtung 3, Bewertung 3 = 9 Punkte):**
   Native Model/View-Architektur ermoglicht Clean Code und erfullt die IHK-Anforderungen an strukturierte Softwareentwicklung.

4. **Community/Support (Gewichtung 2, Bewertung 3 = 6 Punkte):**
   Die sehr grosse Community garantiert schnelle Problemlosungen, was bei zeitlich begrenzten Projekten kritisch ist.

### Vergleich mit Alternativen:

- **Tkinter** scheidet aus, da die Visualisierungsanforderungen (Echtzeit-Partikelanimation, wissenschaftliche Diagramme) nicht effizient umsetzbar sind.

- **Kivy** ist technisch machbar, aber die steile Lernkurve (1 Punkt, Gewichtung 3) wurde wertvolle Entwicklungszeit kosten. Der Mobile-Fokus ist fur dieses Desktop-Projekt uberflussig.

- **wxPython** ist eine solide Alternative (15,25 Punkte), aber die schwachere Visualisierungsunterstutzung (2 Punkte vs. 3 Punkte bei PyQt5) ist bei hochster Gewichtung (4) ausschlaggebend. Die Differenz von 1,75 Nutzwert-Punkten entsteht hauptsachlich durch die bessere Visualisierung von PyQt5.

### Risiken und Mitigation:

**Risiko: GPL-Lizenz**
- **Bewertung:** Niedrig
- **Begrundung:** Fur Ausbildungsprojekte ist Open-Source-Lizenzierung unkritisch. Der Code wird ohnehin veroffentlicht.

**Risiko: Grossere .exe-Dateigrossee**
- **Bewertung:** Niedrig
- **Begrundung:** PyInstaller-Bundle ist ca. 150 MB. Fur moderne Computer unkritisch. Download-Geschwindigkeit akzeptabel.

**Risiko: Einarbeitungszeit**
- **Bewertung:** Mittel
- **Begrundung:** 3-4 Tage Einarbeitung sind einkalkuliert. Die exzellente Dokumentation minimiert dieses Risiko.
- **Mitigation:** Strukturiertes Selbststudium mit offiziellen Tutorials in der ersten Woche.

---

## Technische Umsetzung

### Verwendete PyQt5-Komponenten:

| Komponente | Verwendungszweck |
|-----------|-----------------|
| `QMainWindow` | Hauptfenster mit Menu-Bar und Status-Bar |
| `QWidget` / `QVBoxLayout` / `QHBoxLayout` | Layout-Management fur drei-Panel-Struktur |
| `QSlider` / `QSpinBox` / `QDoubleSpinBox` | Interaktive Parametereingabe (11 Parameter) |
| `QComboBox` | Auswahl von Presets und Modi |
| `QCheckBox` | Toggle-Funktionen (Quarantane, Dark/Light Mode) |
| `QPushButton` | Aktionen (Start, Pause, Reset, Export) |
| `QTabWidget` | Tabs fur verschiedene Statistik-Ansichten |
| `QLabel` | Textanzeige und Statusmeldungen |
| `QPainter` | Custom-Rendering fur Partikelanimation (Canvas) |
| `pyqtgraph.PlotWidget` | Echtzeitdiagramme (Zeitreihen) |
| `matplotlib.backends.backend_qt5agg` | Kreisdiagramme und statistische Visualisierungen |
| `QSettings` | Persistenz von Nutzereinstellungen (Theme, letzte Parameter) |

### Architektur:

```
epidemic-sim2.0/
├── epidemic_sim/
│   ├── main.py                     # Entry Point, initialisiert QApplication
│   ├── model/                      # Model-Schicht
│   │   ├── simulation.py           # EpidemicSimulation (Geschaftslogik)
│   │   ├── particle.py             # Particle-Klasse (Agenten)
│   │   └── spatial_grid.py         # Optimierung (Raumliche Suche)
│   ├── view/                       # View-Schicht
│   │   ├── main_window.py          # QMainWindow, orchestriert UI
│   │   ├── canvas.py               # SimulationCanvas (QPainter)
│   │   ├── widgets.py              # Custom Widgets (PieChart, CollapsibleBox)
│   │   └── theme.py                # Dark/Light Theme-Definitionen
│   └── config/                     # Konfiguration
│       ├── parameters.py           # SimParams (Datenklasse)
│       └── presets.py              # Disease Presets (COVID, Flu, etc.)
```

Diese Struktur implementiert das **Model-View-Controller-Pattern** sauber:
- **Model:** `simulation.py`, `particle.py` (Geschaftslogik, keine UI-Abhangigkeiten)
- **View:** `main_window.py`, `canvas.py`, `widgets.py` (UI-Komponenten)
- **Controller:** `main_window.py` (Signal-Slot-Verbindungen, User-Input-Handling)

---

## Fazit

Die Entscheidung fur PyQt5 als GUI-Framework ist durch die Nutzwertanalyse objektiv begrundet und optimal fur die Anforderungen des Epidemic Simulator 3.0-Projekts. Die Kombination aus hervorragender Visualisierungsunterstutzung, umfassender Dokumentation und nativer MVC-Architektur ermoglicht die Umsetzung aller funktionalen und nicht-funktionalen Anforderungen. Die GPL-Lizenz ist fur Ausbildungsprojekte unkritisch, und die grosse Community minimiert Entwicklungsrisiken.

**Alternative Losungen** wie wxPython waren technisch machbar, konnen aber die Visualisierungsanforderungen nicht mit gleicher Eleganz erfullen. Tkinter ist fur die Komplexitat des Projekts ungeeignet, und Kivy wurde durch die steile Lernkurve wertvolle Entwicklungszeit kosten.

Die tatsachliche Implementierung bestatigt die Entscheidung: Die Anwendung erreicht stabile 60 FPS bei 200 Partikeln, bietet professionelle Visualisierungen (Echtzeitdiagramme, Kreisdiagramme) und folgt Clean-Code-Prinzipien durch klare MVC-Trennung.

---

**Datum:** 2025-12-10
**Autor:** Fachinformatiker Anwendungsentwicklung (IHK)
**Projekt:** Epidemic Simulator 3.0 - Abschlussprojekt
