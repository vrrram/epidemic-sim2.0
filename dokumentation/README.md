# Dokumentation - Epidemie-Simulationssystem

Vollständige IHK-Projektdokumentation für das 3. Lehrjahr

---

## 📁 Dokumentationsstruktur

```
dokumentation/
├── README.md                      # Diese Datei - Übersicht
├── PROJEKTDOKUMENTATION.md        # Hauptdokumentation (15+ Seiten)
└── BENUTZERHANDBUCH.md           # Anwenderhandbuch
```

---

## 📄 Enthaltene Dokumente

### 1. PROJEKTDOKUMENTATION.md (Hauptdokument)

**Umfang:** 15+ Seiten
**Zielgruppe:** IHK-Prüfer, Lehrkräfte, technische Betreuer

**Inhalt:**
- ✅ Projektauftrag und Projektziele
- ✅ Kundenwünsche und Anforderungsanalyse (10 funktionale, 3 nichtfunktionale Anforderungen)
- ✅ Auswahl und Begründung des Vorgehensmodells (Iteratives Prototyping)
- ✅ Projektphasen und Ablauf (6 Phasen mit Zeitplanung)
- ✅ Ressourcen- und Ablaufplanung mit Meilensteinen
- ✅ Kostenplanung (1.140 € Gesamtkosten)
- ✅ Risikoanalyse mit Gegenmaßnahmen
- ✅ Technische Planung:
  - Auswahl und Begründung der Programmiersprache (Python 3.10)
  - Auswahl und Begründung des Frameworks (PyQt5)
  - **Beschreibung und Begründung der 3 Verteilungsfunktionen:**
    1. Gleichverteilung (Uniform) für Positionen/Geschwindigkeiten
    2. Normalverteilung (Gaussian) für Infektionsanfälligkeit
    3. Exponentialverteilung (Exponential) für Genesungszeit
  - Architektur und Design (MVC-Pattern)
  - Planung der Benutzerschnittstelle (ISO 9241-110)
- ✅ Implementierung und Umsetzung (Kern-Algorithmen, Optimierungen, Clean Code)
- ✅ Testplanung und Qualitätssicherung (Unit-Tests, Integrationstests, Performance-Tests)
- ✅ **Anhang mit technischen Diagrammen:**
  - **SEIRD-Zustandsdiagramm** (Mermaid State Diagram)
  - **Klassendiagramm** (Mermaid Class Diagram)
  - **PAP: Hauptsimulationsschleife** (Mermaid Flowchart)
  - **PAP: Infektions-Check-Algorithmus** (Mermaid Flowchart)
  - **PAP: Quarantäne-Management** (Mermaid Flowchart)
- ✅ Zusammenfassung und Fazit
- ✅ Glossar mit Fachbegriffen

---

### 2. BENUTZERHANDBUCH.md

**Umfang:** 20+ Seiten
**Zielgruppe:** Endanwender, Lehrkräfte, Schüler

**Inhalt:**
- ✅ Einführung und Lernziele
- ✅ Installation (Python, Abhängigkeiten, Start)
- ✅ Schnellstart-Anleitung (2-Minuten-Tutorial)
- ✅ Benutzeroberfläche (3-Panel-Layout mit Screenshots)
- ✅ Parameter-Referenz (alle 15+ Parameter detailliert erklärt)
- ✅ Preset-Szenarien (15 vordefinierte Krankheiten)
- ✅ Tastaturkürzel (Space, R, F, Q, M, 1-9)
- ✅ FAQ (25+ häufig gestellte Fragen)
- ✅ Fehlerbehebung (Troubleshooting)

---

## 🎓 IHK-Anforderungen: Erfüllungsübersicht

| Anforderung | Status | Seite/Abschnitt |
|-------------|--------|-----------------|
| **Funktionale Anforderungen** |
| Zeitabhängige Simulation | ✅ Erfüllt | Kap. 2.1, 9.1 |
| 3 Zufallswerte mit versch. Verteilungen | ✅ Erfüllt | Kap. 8.3 (3 Seiten Detail) |
| Mindestens 7 Eingabeparameter | ✅ Erfüllt (15+) | Kap. 5 (Benutzerhandbuch) |
| Simulationsgeschwindigkeit 3+ Stufen | ✅ Erfüllt (4) | Kap. 2.1 |
| Visuelle Darstellung & Auswertung | ✅ Erfüllt | Kap. 4.4 |
| Animation zur Simulation | ✅ Erfüllt | Kap. 4.3 |
| Windows-Anwendung | ✅ Erfüllt | Kap. 2.1 |
| Auf Schulrechner ausführbar | ✅ Erfüllt | Kap. 2.3 |
| Start durch ausführbare Datei | ✅ Erfüllt | Kap. 2.3 |
| GUI | ✅ Erfüllt | Kap. 4, 8.5 |
| **Nichtfunktionale Anforderungen** |
| Clean Code Kriterien | ✅ Erfüllt | Kap. 9.3 |
| ISO 9241-110 Benutzeroberfläche | ✅ Erfüllt | Kap. 8.5 |
| Benutzerfreundliche Animation | ✅ Erfüllt | Kap. 9.2 |
| **Dokumentations-Anforderungen** |
| Umfang mind. 6 Seiten | ✅ Erfüllt (15+) | Gesamtes Dokument |
| Projektziele & Kundenwünsche | ✅ Erfüllt | Kap. 1, 2 |
| Vorgehensmodell (Auswahl & Begründung) | ✅ Erfüllt | Kap. 3 |
| Phasen des Vorgehensmodells | ✅ Erfüllt | Kap. 4 |
| Ressourcen- & Ablaufplanung | ✅ Erfüllt | Kap. 5 |
| Kostenplanung | ✅ Erfüllt | Kap. 6 |
| Risikoanalyse | ✅ Erfüllt | Kap. 7 |
| Verteilungsfunktionen (Beschr. & Begr.) | ✅ Erfüllt | Kap. 8.3 (3 Verteilungen) |
| Programmiersprache & Framework (Auswahl & Begr.) | ✅ Erfüllt | Kap. 8.1, 8.2 |
| Planung der Benutzerschnittstelle | ✅ Erfüllt | Kap. 8.5 |
| Planung des Testens | ✅ Erfüllt | Kap. 10 |
| Testprotokolle (mind. 2 Seiten Anhang) | ✅ Erfüllt | Kap. 10.6 |
| Kurze Beschreibung der Umsetzung | ✅ Erfüllt | Kap. 9 |
| Benutzerhandbuch digital | ✅ Erfüllt | BENUTZERHANDBUCH.md |

**Erfüllungsgrad: 100% aller Anforderungen**

---

## 📊 Enthaltene Diagramme (Mermaid-Syntax)

### 1. SEIRD-Zustandsdiagramm (State Diagram)

Zeigt die Zustandsübergänge im epidemiologischen Modell:
- **Susceptible** → Infected (bei Kontakt)
- **Infected** → Quarantine (bei Symptomen)
- **Infected** → Removed (Genesung)
- **Infected** → Dead (Mortalität)
- **Quarantine** → Removed/Dead

**Verwendung:** Erklärt das wissenschaftliche Modell hinter der Simulation

---

### 2. Klassendiagramm (Class Diagram)

Zeigt die Softwarearchitektur mit allen Hauptklassen:
- **EpidemicApp** (GUI-Controller)
- **EpidemicSimulation** (Simulationslogik)
- **Particle** (Einzelne Agenten)
- **SpatialGrid** (Optimierung)
- **SimulationCanvas** (Rendering)
- **SimParams** (Konfiguration)

**Verwendung:** Dokumentiert die Code-Struktur für technisches Verständnis

---

### 3. PAP: Hauptsimulationsschleife (Flowchart)

Programmablaufplan für die zentrale Update-Funktion:
1. Pause-Check
2. Physik-Update
3. Infektions-Check
4. Tag-Boundary → Update Infected
5. Quarantäne-Management
6. Statistik-Update

**Verwendung:** Zeigt den Ablauf jedes Simulations-Ticks

---

### 4. PAP: Infektions-Check-Algorithmus (Flowchart)

Detaillierter Ablauf der Infektionslogik:
1. Spatial Grid initialisieren
2. Für jeden Infizierten:
   - Hole nearby Susceptible
   - Berechne Distanz
   - Prüfe Infection Radius
   - Würfle Infektion (Probability × Susceptibility)

**Verwendung:** Dokumentiert die Kern-Algorithmus-Logik mit O(n) Komplexität

---

### 5. PAP: Quarantäne-Management (Flowchart)

Ablauf des Quarantäne-Systems:
1. Inkrementiere days_infected
2. Prüfe Genesungs-Bedingung (Exponentialverteilung!)
3. Würfle Mortalität
4. Prüfe Quarantäne-Kriterien
5. Verschiebe Partikel

**Verwendung:** Zeigt Interventionslogik und Verteilungsfunktion-Anwendung

---

## 🔍 Mermaid-Diagramme anzeigen

### Option 1: GitHub/GitLab (empfohlen)

Wenn die Dokumentation auf GitHub oder GitLab gehostet wird, werden Mermaid-Diagramme **automatisch gerendert**. Einfach die `.md`-Datei öffnen.

### Option 2: VS Code mit Extension

1. Installieren Sie VS Code: https://code.visualstudio.com/
2. Installieren Sie Extension: "Markdown Preview Mermaid Support"
3. Öffnen Sie `PROJEKTDOKUMENTATION.md`
4. Drücken Sie `Ctrl+Shift+V` für Vorschau

### Option 3: Online Mermaid Editor

1. Besuchen Sie https://mermaid.live/
2. Kopieren Sie ein Mermaid-Code-Block aus der Dokumentation
3. Fügen Sie ihn im Editor ein
4. Diagramm wird live gerendert
5. Export als PNG/SVG möglich

### Option 4: Markdown-Editor

Nutzen Sie einen dieser Editoren mit Mermaid-Support:
- **Typora** (Windows/Mac/Linux) - https://typora.io/
- **Mark Text** (Open Source) - https://marktext.app/
- **Obsidian** (mit Mermaid-Plugin) - https://obsidian.md/

---

## 📤 Export als PDF

### Methode 1: VS Code + Markdown PDF Extension

1. Installieren Sie Extension: "Markdown PDF"
2. Öffnen Sie `PROJEKTDOKUMENTATION.md`
3. Rechtsklick → "Markdown PDF: Export (pdf)"
4. PDF wird im gleichen Ordner erstellt

**⚠️ Hinweis:** Mermaid-Diagramme werden als Code-Blöcke exportiert (nicht gerendert)

### Methode 2: Pandoc + Mermaid Filter

```bash
# Installation
npm install -g mermaid-filter
pip install pandoc

# Konvertierung
pandoc PROJEKTDOKUMENTATION.md -o PROJEKTDOKUMENTATION.pdf --filter mermaid-filter
```

### Methode 3: GitHub Pages + Print to PDF

1. Pushen Sie Dokumentation zu GitHub
2. Aktivieren Sie GitHub Pages in Repository-Settings
3. Öffnen Sie die gerenderte Seite im Browser
4. `Ctrl+P` → "Als PDF speichern"

**✅ Empfohlen für professionelles Erscheinungsbild**

### Methode 4: Screenshot der Diagramme

1. Öffnen Sie https://mermaid.live/
2. Kopieren Sie Diagramm-Code
3. Export als PNG
4. Fügen Sie PNG in Word-Dokument ein
5. Exportieren Sie als PDF

---

## 📝 Wichtige Hinweise für die IHK-Abgabe

### ✅ Checkliste vor Abgabe

- [ ] Alle Dokumente auf Rechtschreibung geprüft
- [ ] Mermaid-Diagramme renderfähig (in VS Code getestet)
- [ ] Seitenzahlen korrekt (Projektdoku > 6 Seiten)
- [ ] Testprotokolle im Anhang vorhanden
- [ ] Benutzerhandbuch vollständig
- [ ] Deckblatt mit Namen, Datum, Klasse
- [ ] Inhaltsverzeichnis mit Seitenzahlen
- [ ] Glossar mit Fachbegriffen
- [ ] Quellenangaben (falls externe Quellen genutzt)

### 📋 Abgabeformate

**Digital (empfohlen):**
- ZIP-Archiv mit allen `.md`-Dateien
- Anleitung: "Dokumentation mit VS Code + Mermaid Extension öffnen"
- Alternativ: PDF-Export mit Screenshots der Diagramme

**Gedruckt:**
- PDF exportieren und ausdrucken
- Diagramme separat als Bilder ausdrucken und einkleben
- Oder: Diagramme in https://mermaid.live/ rendern und Screenshots drucken

### 🎯 Bewertungskriterien

**Dokumentation (LF 12):**
- Vollständigkeit aller geforderten Abschnitte
- Fachliche Korrektheit
- Strukturierte Gliederung
- Verständlichkeit

**Benutzerhandbuch (LF 10):**
- Zielgruppengerechte Sprache
- Schritt-für-Schritt-Anleitungen
- Troubleshooting-Sektion
- Vollständige Parameter-Referenz

**Testen + Clean Code (LF 11):**
- Testprotokolle mit klaren Ergebnissen
- Dokumentation der Clean-Code-Prinzipien
- Code-Beispiele mit Erklärung

---

## 🚀 Weitere Ressourcen

**Python-Dokumentation:**
- https://docs.python.org/3/

**PyQt5-Tutorial:**
- https://doc.qt.io/qtforpython/

**Epidemiologie-Grundlagen:**
- https://en.wikipedia.org/wiki/Compartmental_models_in_epidemiology

**Mermaid-Dokumentation:**
- https://mermaid-js.github.io/mermaid/

---

## 📞 Kontakt

**Bei Fragen zur Dokumentation:**
- Konsultieren Sie zuerst das Benutzerhandbuch (BENUTZERHANDBUCH.md)
- Prüfen Sie die FAQ-Sektion
- Kontaktieren Sie Ihre Lehrkraft

**Bei technischen Problemen:**
- Siehe Kapitel "Fehlerbehebung" im Benutzerhandbuch
- Prüfen Sie die README.md im Hauptverzeichnis

---

**Dokumentation erstellt:** Februar 2025
**Version:** 3.0
**Status:** Abgabebereit ✅
