# Benutzerhandbuch: Epidemie-Simulationssystem

**Version:** 3.0
**Datum:** Februar 2025
**Zielgruppe:** Lehrkräfte, Schüler, Bildungseinrichtungen

---

## Inhaltsverzeichnis

1. [Einführung](#1-einführung)
2. [Installation](#2-installation)
3. [Schnellstart](#3-schnellstart)
4. [Benutzeroberfläche](#4-benutzeroberfläche)
5. [Parameter-Referenz](#5-parameter-referenz)
6. [Preset-Szenarien](#6-preset-szenarien)
7. [Tastaturkürzel](#7-tastaturkürzel)
8. [Häufig gestellte Fragen (FAQ)](#8-häufig-gestellte-fragen-faq)
9. [Fehlerbehebung](#9-fehlerbehebung)

---

## 1. Einführung

### 1.1 Was ist die Epidemie-Simulation?

Die Epidemie-Simulation ist ein Bildungswerkzeug zur Visualisierung der Ausbreitung von Infektionskrankheiten. Sie basiert auf dem wissenschaftlichen SEIRD-Modell (Susceptible-Exposed-Infected-Recovered-Dead) und ermöglicht es, verschiedene Interventionsmaßnahmen wie Quarantäne, Social Distancing und räumliche Isolation zu untersuchen.

### 1.2 Lernziele

- Verständnis epidemiologischer Grundkonzepte (R0, Herdenimmunität, Infektionsketten)
- Visualisierung des Einflusses von Interventionsmaßnahmen
- Vergleich verschiedener Krankheitsszenarien (COVID-19, Grippe, Masern, etc.)
- Experimentieren mit Parametern zur Hypothesentestung

### 1.3 Systemanforderungen

**Minimum:**
- Windows 10 oder höher (Windows 11 empfohlen)
- Python 3.8+
- 4 GB RAM
- Intel Core i3 oder äquivalent
- 100 MB freier Festplattenspeicher

**Empfohlen:**
- Windows 11
- Python 3.10+
- 8 GB RAM
- Intel Core i5 oder besser
- Dedizierte Grafikkarte (optional, verbessert Rendering)

---

## 2. Installation

### 2.1 Python installieren

1. Besuchen Sie [python.org/downloads](https://python.org/downloads)
2. Laden Sie Python 3.10 oder höher herunter
3. Führen Sie den Installer aus
4. ⚠️ **Wichtig:** Aktivieren Sie "Add Python to PATH"

### 2.2 Abhängigkeiten installieren

Öffnen Sie eine Kommandozeile (cmd) und führen Sie aus:

```bash
cd epidemic-sim2.0
pip install -r requirements.txt
```

**Enthaltene Bibliotheken:**
- PyQt5: GUI-Framework
- PyQtGraph: Echtzeit-Graphen
- NumPy: Numerische Berechnungen
- Matplotlib: Tortendiagramme

### 2.3 Simulation starten

**Methode 1: Python-Skript**
```bash
python epidemic_sim/main.py
```

**Methode 2: Modul-Start**
```bash
python -m epidemic_sim.main
```

**Methode 3: Ausführbare Datei (optional)**
Falls eine `.exe`-Datei bereitgestellt wurde, einfach doppelklicken.

---

## 3. Schnellstart

### 3.1 Ihre erste Simulation (2 Minuten)

1. **Starten Sie die Anwendung**
   ```bash
   python epidemic_sim/main.py
   ```

2. **Wählen Sie ein Preset**
   - Klicken Sie auf das Dropdown-Menü "PRESETS" (linkes Panel)
   - Wählen Sie "COVID-19 (Original Strain)"

3. **Starten Sie die Simulation**
   - Die Simulation startet automatisch
   - Beobachten Sie die Partikel im zentralen Canvas

4. **Experimentieren Sie**
   - Drücken Sie `SPACE` zum Pausieren
   - Drücken Sie `2` für 2x Geschwindigkeit
   - Drücken Sie `Q` zum Aktivieren der Quarantäne

5. **Analysieren Sie die Ergebnisse**
   - Beobachten Sie den "TIME SERIES" Graph (rechtes Panel)
   - Wechseln Sie zum "PIE CHART" Tab

### 3.2 Wichtigste Bedienelemente

| Element | Funktion | Tastatur |
|---------|----------|----------|
| **PAUSE/RESUME** | Simulation anhalten/fortsetzen | `SPACE` |
| **RESET** | Simulation neu starten | `R` |
| **Speed Buttons** | Geschwindigkeit anpassen (0.5x - 5x) | - |
| **Preset Dropdown** | Vordefinierte Szenarien laden | `1`-`9` |
| **Quarantine Checkbox** | Quarantäne aktivieren/deaktivieren | `Q` |

---

## 4. Benutzeroberfläche

### 4.1 Layout-Übersicht

```
┌───────────────────────────────────────────────────────────────┐
│  EPIDEMIE SIMULATOR v3.0                                       │
├──────────────┬────────────────────────────┬───────────────────┤
│              │                            │                   │
│  Parameter   │      Simulation Canvas     │  Steuerung &      │
│  (links)     │      (zentriert)           │  Statistik        │
│              │                            │  (rechts)         │
│              │                            │                   │
│  • Disease   │   [Partikel-Animation]     │  • PAUSE/RESET    │
│  • Population│                            │  • Speed Control  │
│  • Intervent.│   Blau = Susceptible       │  • Statistics     │
│  • Presets   │   Rot  = Infected          │  • Graphs         │
│              │   Grau = Removed           │  • Pie Chart      │
│              │   Dunkelrot = Dead         │                   │
│              │                            │                   │
└──────────────┴────────────────────────────┴───────────────────┘
```

### 4.2 Linkes Panel: Parameter-Steuerung

**Collapsible Boxes (ausklappbar):**

1. **DISEASE PARAMETERS** (Krankheitsparameter)
   - Infection Radius: Ansteckungsreichweite
   - Infection Probability: Übertragungswahrscheinlichkeit
   - Infection Duration: Krankheitsdauer in Tagen
   - Mortality Rate: Sterblichkeitsrate
   - Initial Infected %: Startinfektionen (Patient Zero)

2. **POPULATION PARAMETERS** (Bevölkerungsparameter)
   - Population Size: Anzahl Partikel (50-1000)
   - Social Distancing Strength: Abstandskraft
   - Social Distance Compliance: Befolgungs-Rate

3. **INTERVENTION PARAMETERS** (Interventionsparameter)
   - Social Distance Range: Reichweite der Distanzierung

4. **COMMUNITY PARAMETERS** (nur im Community-Modus)
   - Particles Per Community: Bevölkerung pro Gemeinde
   - Travel Probability: Reisewahrscheinlichkeit
   - Initially Infected Communities: Anzahl infizierter Gemeinden

5. **QUARANTINE PARAMETERS** (nur wenn Quarantäne aktiv)
   - Quarantine After: Tage bis zur Isolation
   - Quarantine Start Day: Tag des Quarantäne-Beginns
   - Quarantine Duration: Dauer der Isolation
   - Asymptomatic Rate: Anteil symptomfreier Fälle

6. **MARKETPLACE PARAMETERS** (nur wenn Marketplace aktiv)
   - Marketplace Interval: Tage zwischen Events
   - Marketplace Duration: Dauer des Events
   - Marketplace Attendance: Teilnahmequote

7. **PRESETS**
   - Dropdown-Menü mit vordefinierten Szenarien

**💡 Tipp:** Bewegen Sie die Maus über einen Parameter, um eine detaillierte Beschreibung (Tooltip) zu sehen!

### 4.3 Zentraler Canvas: Simulation

**Visuelle Kodierung:**

| Farbe | Zustand | Bedeutung |
|-------|---------|-----------|
| 🔵 Blau (Cyan) | Susceptible | Anfällig, kann infiziert werden |
| 🔴 Rot | Infected | Aktuell infiziert, ansteckend |
| ⚫ Grau | Removed | Genesen, immun |
| 🟤 Dunkelrot | Dead | Verstorben (bei Mortalität > 0) |

**Modi:**

1. **Simple Mode (Standard)**
   - Alle Partikel in einem gemeinsamen Raum
   - Quarantäne-Zone: Untere linke Ecke (gestrichelte Linie)

2. **Communities Mode**
   - 9 separate Gemeinden in 3×3 Gitter
   - Gelegentlicher Reiseverkehr zwischen Gemeinden
   - Quarantäne-Zone: Unteres linkes Tile

**Interaktion:**
- **Klicken:** Keine direkte Interaktion mit Partikeln
- **Zoom:** Nicht implementiert (feste Ansicht)
- **Pan:** Nicht implementiert (feste Ansicht)

### 4.4 Rechtes Panel: Steuerung & Analyse

**Steuerbuttons:**
- **PAUSE/RESUME:** Simulation anhalten/fortsetzen
- **RESET:** Neustart mit aktuellen Parametern
- **FULL:** Vollbildmodus (blendet rechtes Panel aus)

**Speed Control:**
- 0.5x: Zeitlupe (für detaillierte Beobachtung)
- 1x: Normale Geschwindigkeit (Standard)
- 2x: Doppelte Geschwindigkeit
- 5x: Fünffache Geschwindigkeit (für lange Simulationen)

**Statistics:**
```
DAY: 042
S: 125 (62.5%) | I:  15 ( 7.5%)
R:  55 (27.5%) | D:   5 ( 2.5%)
```
- **S:** Susceptible (anfällig)
- **I:** Infected (infiziert)
- **R:** Removed (genesen)
- **D:** Dead (verstorben)

**Visualizations:**

1. **TIME SERIES Tab**
   - X-Achse: Tage
   - Y-Achse: Prozent der Population
   - Linien: Blau (S), Rot (I), Grau (R), Dunkelrot (D)
   - Zeigt Epidemie-Verlauf über Zeit

2. **PIE CHART Tab**
   - Momentaufnahme der aktuellen Verteilung
   - Zeigt Anteile aller Zustände
   - Unterscheidet symptomatische/asymptomatische Infektionen

**Simulation Mode:**
- **SIMPLE:** Einzelner Raum
- **COMMUNITIES:** 9 getrennte Gemeinden

**Interventions:**
- **Quarantine Zone:** Checkbox zum Aktivieren
- **Marketplace Gatherings:** Checkbox für Events

**Visualizations:**
- **Show Infection Radius:** Zeigt rote Kreise um Infizierte

---

## 5. Parameter-Referenz

### 5.1 Krankheitsparameter (Disease Parameters)

#### Infection Radius (Ansteckungsreichweite)

**Bereich:** 0.01 - 0.40
**Standard:** 0.15
**Einheit:** Simulationseinheiten

**Beschreibung:**
Definiert den Radius, innerhalb dessen eine Infektion übertragen werden kann. Größere Werte simulieren luftübertragene Krankheiten (z.B. Masern), kleinere Werte Kontaktinfektionen (z.B. Ebola).

**Beispiele:**
- **0.10:** Ebola (direkter Kontakt)
- **0.15:** COVID-19, Grippe (Tröpfcheninfektion)
- **0.30:** Masern (Aerosole, Raumluft)

**💡 Tipp:** Kombinieren Sie mit Infection Probability für realistische Szenarien.

---

#### Infection Probability (Übertragungswahrscheinlichkeit)

**Bereich:** 0.00 - 1.00 (0% - 100%)
**Standard:** 0.15
**Einheit:** Wahrscheinlichkeit pro Kontakt

**Beschreibung:**
Wahrscheinlichkeit, dass eine anfällige Person bei Kontakt mit einer infizierten Person angesteckt wird. Wird durch individuelle Anfälligkeit (Normalverteilung) modifiziert.

**Formel:**
```
Effektive Wahrscheinlichkeit = Infection Probability × Individual Susceptibility
```

**Beispiele:**
- **0.01:** Niedrig ansteckend (R0 < 2)
- **0.15:** Mittel ansteckend (R0 = 2-5)
- **0.50:** Hoch ansteckend (R0 > 10)

**Wichtig:** Dieser Wert wird pro Zeitschritt angewendet (24 Schritte/Tag). Daher ergeben kleine Werte realistisches Verhalten.

---

#### Infection Duration (Krankheitsdauer)

**Bereich:** 1 - 100 Tage
**Standard:** 25 Tage
**Einheit:** Simulationstage

**Beschreibung:**
Durchschnittliche Dauer, die ein Partikel infiziert bleibt. Die tatsächliche Dauer variiert durch Exponentialverteilung (Recovery Time Modifier).

**Formel:**
```
Tatsächliche Dauer = Infection Duration × Recovery Time Modifier
```
- Recovery Time Modifier ~ Exp(1.0), geclippt auf [0.5, 3.0]
- Beispiel: Modifier = 1.5 → 25 × 1.5 = 37.5 Tage

**Beispiele:**
- **7 Tage:** Erkältung, kurze Grippe
- **14 Tage:** COVID-19 (typischer Verlauf)
- **30 Tage:** Lange Erkrankungen

---

#### Mortality Rate (Sterblichkeitsrate)

**Bereich:** 0.00 - 1.00 (0% - 100%)
**Standard:** 0.00
**Einheit:** Case Fatality Rate (CFR)

**Beschreibung:**
Wahrscheinlichkeit, dass ein infizierter Partikel stirbt statt zu genesen. Verstorbene Partikel werden aus der Simulation entfernt.

**Beispiele:**
- **0.00:** Keine Todesfälle (SIR-Modell)
- **0.01:** 1% (Saisonale Grippe)
- **0.02:** 2% (COVID-19 Original)
- **0.10:** 10% (SARS)
- **0.50:** 50% (Ebola)

**⚠️ Hinweis:** Hohe Mortalität reduziert die Population, was die Ausbreitung selbst-limitiert ("Burn-out").

---

#### Fraction Infected Init (Initiale Infektionsrate)

**Bereich:** 0.000 - 0.050 (0% - 5%)
**Standard:** 0.01 (1%)
**Einheit:** Prozent der Population

**Beschreibung:**
Anteil der Population, der zu Beginn infiziert ist (Patient Zero). Beeinflusst die Geschwindigkeit des initialen Ausbruchs.

**Beispiele:**
- **0.005 (0.5%):** Einzelner Patient Zero
- **0.01 (1%):** Wenige initiale Fälle
- **0.02 (2%):** Mehrere gleichzeitige Ausbrüche

**💡 Tipp:** Niedrige Werte (< 1%) zeigen die Entwicklung der Epidemie-Kurve am besten.

---

### 5.2 Bevölkerungsparameter (Population Parameters)

#### Population Size (Populationsgröße)

**Bereich:** 50 - 2000 Partikel
**Standard:** 200
**Einheit:** Anzahl Partikel

**Beschreibung:**
Gesamtzahl der simulierten Individuen. Höhere Werte ergeben realistischere Statistiken, benötigen aber mehr Rechenleistung.

**Performance:**
- **50-200:** 60 FPS, schnell, gut für Tests
- **200-500:** 30-60 FPS, ausgeglichen
- **500-1000:** 20-30 FPS, hohe Präzision
- **1000-2000:** 10-20 FPS, maximale Details

**⚠️ Hinweis:** Änderungen erfordern RESET (Button "Apply" klicken).

---

#### Social Distancing Strength (Abstandsstärke)

**Bereich:** 0.0 - 2.0
**Standard:** 0.0 (deaktiviert)
**Einheit:** Repulsionskraft

**Beschreibung:**
Stärke der abstoßenden Kraft zwischen Partikeln. Simuliert Social Distancing-Maßnahmen.

**Werte:**
- **0.0:** Keine Distanzierung (normales Verhalten)
- **0.5:** Schwache Distanzierung (persönlicher Raum)
- **1.0:** Mittlere Distanzierung (aktives Vermeiden)
- **1.5:** Starke Distanzierung (Lockdown-ähnlich)

**Effekt:** Reduziert Kontaktrate → Verlangsamt Ausbreitung

---

#### Social Distance Compliance (Befolgungs-Rate)

**Bereich:** 0.0 - 1.0 (0% - 100%)
**Standard:** 1.0 (100%)
**Einheit:** Anteil der Population

**Beschreibung:**
Prozentsatz der Population, die Social Distancing befolgt. Simuliert realistisches Compliance-Verhalten.

**Werte:**
- **0.3 (30%):** Niedrige Compliance (viele Verweigerer)
- **0.7 (70%):** Mittlere Compliance (realistisch)
- **0.9 (90%):** Hohe Compliance (disziplinierte Gesellschaft)
- **1.0 (100%):** Perfekte Compliance (unrealistisch)

**💡 Tipp:** Kombinieren Sie mit Distancing Strength: z.B. Strength=1.0, Compliance=0.7 für realistische Szenarien.

---

### 5.3 Interventionsparameter (Intervention Parameters)

#### Social Distance Range (Abstandsreichweite)

**Bereich:** 1 - 10 Gitterzellen
**Standard:** 2
**Einheit:** Anzahl Gitterzellen

**Beschreibung:**
Bestimmt, wie weit Partikel nach Nachbarn suchen, um Abstand zu halten. Höhere Werte = größere Awareness.

**Werte:**
- **1:** Nur direkte Nachbarn
- **2:** Mittlere Reichweite (Standard)
- **5:** Weitreichendes Vermeideverhalten

**⚠️ Hinweis:** Höhere Werte erhöhen Rechenlast!

---

#### Quarantine After (Quarantäne nach)

**Bereich:** 1 - 20 Tage
**Standard:** 5 Tage
**Einheit:** Tage

**Beschreibung:**
Anzahl Tage nach Infektion, nach denen symptomatische Partikel in Quarantäne verschoben werden.

**Interpretation:**
- **1-3 Tage:** Sehr frühe Erkennung (unrealistisch)
- **5-7 Tage:** Realistische Symptom-Onset-Zeit
- **10+ Tage:** Verzögerte Erkennung

**Wichtig:** Nur symptomatische Fälle werden quarantiniert! (Siehe Asymptomatic Rate)

---

#### Quarantine Start Day (Quarantäne-Startag)

**Bereich:** 0 - 30 Tage
**Standard:** 10 Tage
**Einheit:** Simulationstag

**Beschreibung:**
Tag, an dem die Quarantäne-Politik beginnt. Simuliert verzögerte staatliche Reaktion.

**Szenarien:**
- **0:** Sofortige Quarantäne von Tag 1
- **10:** Reaktive Maßnahme (nach Ausbruchserkennung)
- **20:** Späte Intervention (Epidemie bereits fortgeschritten)

---

#### Quarantine Duration (Quarantäne-Dauer)

**Bereich:** 0 - 50 Tage (0 = unbegrenzt)
**Standard:** 14 Tage
**Einheit:** Tage

**Beschreibung:**
Dauer, die Partikel in Quarantäne bleiben. Bei 0 bleiben sie bis zur Genesung.

**Werte:**
- **0:** Bis Genesung (perfekte Compliance)
- **7:** Kurze Isolation
- **14:** Standard (2 Wochen)
- **21+:** Längere Isolation

---

#### Asymptomatic Rate (Asymptomatische Rate)

**Bereich:** 0.0 - 0.5 (0% - 50%)
**Standard:** 0.20 (20%)
**Einheit:** Anteil Infizierter

**Beschreibung:**
Prozentsatz der Infizierten, die keine Symptome zeigen. Diese werden NICHT quarantiniert und verbreiten die Krankheit unerkannt.

**Beispiele:**
- **0.0:** Alle zeigen Symptome (ideal für Eindämmung)
- **0.20:** 20% asymptomatisch (Grippe)
- **0.35:** 35% asymptomatisch (COVID-19)
- **0.50:** 50% asymptomatisch (Superspreader-Risiko)

**⚠️ Kritisch:** Hohe asymptomatische Raten erschweren Eindämmung massiv!

---

### 5.4 Community-Parameter (nur Community-Modus)

#### Particles Per Community (Partikel pro Gemeinde)

**Bereich:** 20 - 200
**Standard:** 60
**Einheit:** Partikel

**Beschreibung:**
Bevölkerungsgröße jeder der 9 Gemeinden. Gesamtpopulation = 9 × Wert.

**Beispiel:** 60 → Gesamtpopulation = 540

---

#### Travel Probability (Reisewahrscheinlichkeit)

**Bereich:** 0.0 - 1.0 (0% - 100%)
**Standard:** 0.02 (2%)
**Einheit:** Tägliche Wahrscheinlichkeit pro Partikel

**Beschreibung:**
Wahrscheinlichkeit, dass ein Partikel täglich in eine andere Gemeinde reist. Simuliert geografische Ausbreitung.

**Werte:**
- **0.01 (1%):** Seltenes Reisen (starke Isolation)
- **0.05 (5%):** Häufiges Reisen (schwache Isolation)
- **0.20 (20%):** Sehr häufiges Reisen (praktisch keine Isolation)

---

#### Initially Infected Communities (Initial infizierte Gemeinden)

**Bereich:** 1 - 9
**Standard:** 2
**Einheit:** Anzahl Gemeinden

**Beschreibung:**
Anzahl der Gemeinden, die zu Beginn infizierte Partikel enthalten.

**Szenarien:**
- **1:** Single-Point-Outbreak (z.B. Wuhan, COVID-19)
- **3:** Multiple gleichzeitige Ausbrüche
- **9:** Pandemie von Anfang an

---

### 5.5 Marketplace-Parameter (nur wenn Marketplace aktiv)

#### Marketplace Interval (Marktplatz-Intervall)

**Bereich:** 1 - 30 Tage
**Standard:** 7 Tage
**Einheit:** Tage zwischen Events

**Beschreibung:**
Tage zwischen Marktplatz-Events (Massenansammlungen). Simuliert Festivals, Gottesdienste, Konzerte.

**Werte:**
- **1:** Täglicher Markt (hohe Kontaktrate)
- **7:** Wöchentlich (realistisch)
- **14+:** Selten (geringer Einfluss)

---

#### Marketplace Duration (Marktplatz-Dauer)

**Bereich:** 1 - 10 Zeitschritte
**Standard:** 2
**Einheit:** Zeitschritte (nicht Tage!)

**Beschreibung:**
Dauer, die Partikel am Marktplatz verweilen. 24 Zeitschritte = 1 Tag.

**Werte:**
- **1-2:** Kurzer Besuch (Einkaufen)
- **3-5:** Längerer Aufenthalt (Restaurant, Kino)
- **10:** Sehr lange (mehrstündiges Event)

---

#### Marketplace Attendance (Marktplatz-Teilnahme)

**Bereich:** 0.1 - 1.0 (10% - 100%)
**Standard:** 0.3 (30%)
**Einheit:** Anteil der Population

**Beschreibung:**
Prozentsatz der Population, die am Event teilnimmt.

**Werte:**
- **0.1 (10%):** Kleine Veranstaltung
- **0.3 (30%):** Mittlere Veranstaltung
- **0.7 (70%):** Große Massenveranstaltung (Superspreader-Potenzial!)

---

## 6. Preset-Szenarien

Die Simulation enthält 15 vordefinierte Szenarien basierend auf realen Krankheiten und Bildungsszenarien.

### 6.1 Echte Krankheiten

| Preset | R0 | CFR | Beschreibung |
|--------|----|----|--------------|
| **COVID-19 (Original Strain)** | 2.5-3.0 | 1.5% | Original-Variante, Wuhan 2019 |
| **COVID-19 (Delta Variant)** | 5-6 | 0.8% | Delta-Variante, 2021, hochansteckend |
| **COVID-19 (Omicron Variant)** | 7-10 | 0.2% | Omicron-Variante, 2021, sehr ansteckend, mild |
| **Spanish Flu (1918)** | 1.8-2.0 | 5% | Spanische Grippe, verheerende Pandemie |
| **Measles** | 12-18 | 0.2% | Masern, eine der ansteckendsten Krankheiten |
| **Ebola (2014 Outbreak)** | 1.5-2.5 | 50% | Ebola-Ausbruch 2014, sehr tödlich |
| **Influenza (Seasonal)** | 1.3-1.8 | 0.1% | Saisonale Grippe |
| **Common Cold (Rhinovirus)** | 2-3 | 0% | Erkältung, nicht tödlich |
| **SARS (2003)** | 2-3 | 10% | SARS-Ausbruch 2003 |
| **MERS (Coronavirus)** | 0.6-0.9 | 35% | MERS, hohe Letalität, niedrige Übertragung |

**💡 Tipp:** Verwenden Sie Tastenkürzel `1`-`9` für schnellen Zugriff!

### 6.2 Bildungsszenarien

| Preset | Zweck |
|--------|-------|
| **Baseline Epidemic** | Generische Epidemie für Grundlagen-Unterricht |
| **Slow Burn** | Langsame Ausbreitung, lange Dauer |
| **Fast Outbreak** | Schneller Ausbruch, hohes R0 |
| **Social Distancing (Weak)** | Demonstration schwacher Intervention |
| **Social Distancing (Strong)** | Demonstration starker Intervention |

### 6.3 Verwendung von Presets

1. **Preset auswählen:**
   - Öffnen Sie das "PRESETS" Dropdown (linkes Panel)
   - Klicken Sie auf gewünschtes Preset
   - Simulation wird automatisch zurückgesetzt

2. **Parameter anzeigen:**
   - Nach dem Laden zeigen Slider die Preset-Werte
   - Tooltip zeigt Details beim Hover

3. **Preset anpassen:**
   - Ändern Sie beliebige Parameter nach dem Laden
   - Preset dient als Ausgangspunkt

4. **Vergleich durchführen:**
   - Laden Sie Preset A → Beobachten Sie 100 Tage → Screenshot
   - RESET → Laden Sie Preset B → Beobachten Sie 100 Tage → Screenshot
   - Vergleichen Sie Graphen

**Beispiel-Unterrichtsstunde:**
```
1. Laden: "COVID-19 (Original Strain)"
   → Beobachten: Natürlicher Verlauf ohne Intervention

2. RESET → Aktivieren: Quarantine (Q drücken)
   → Beobachten: Effekt der Quarantäne

3. RESET → Aktivieren: Social Distancing (Strength=1.0, Compliance=0.8)
   → Beobachten: Effekt von Abstandsregeln

4. Vergleichen: Welche Intervention ist effektiver?
```

---

## 7. Tastaturkürzel

### 7.1 Hauptsteuerung

| Taste | Funktion | Beschreibung |
|-------|----------|--------------|
| `SPACE` | Pause/Resume | Simulation anhalten/fortsetzen |
| `R` | Reset | Simulation mit aktuellen Parametern neu starten |
| `F` | Fullscreen | Rechtes Panel ausblenden für größere Ansicht |
| `ESC` | Fullscreen Exit | Zurück zur normalen Ansicht |

### 7.2 Interventionen

| Taste | Funktion | Beschreibung |
|-------|----------|--------------|
| `Q` | Toggle Quarantine | Quarantäne aktivieren/deaktivieren |
| `M` | Toggle Marketplace | Marktplatz-Events aktivieren/deaktivieren |

### 7.3 Presets (Schnellzugriff)

| Taste | Preset | Krankheit |
|-------|--------|-----------|
| `1` | COVID-19 (Original) | Original-Stamm |
| `2` | COVID-19 (Delta) | Delta-Variante |
| `3` | COVID-19 (Omicron) | Omicron-Variante |
| `4` | Spanish Flu | Spanische Grippe 1918 |
| `5` | Measles | Masern |
| `6` | Ebola | Ebola 2014 |
| `7` | Influenza | Saisonale Grippe |
| `8` | Common Cold | Erkältung |
| `9` | SARS | SARS 2003 |

### 7.4 Erweiterte Shortcuts

| Taste | Funktion | Beschreibung |
|-------|----------|--------------|
| `Ctrl+T` | Toggle Tooltips | Tooltips ein-/ausschalten (weniger Ablenkung) |
| `+` | Font Size Increase | Schriftgröße erhöhen (Barrierefreiheit) |
| `-` | Font Size Decrease | Schriftgröße verringern |

**💡 Tipp für Präsentationen:**
1. Drücken Sie `F` für Fullscreen
2. Drücken Sie `Ctrl+T` zum Ausblenden von Tooltips
3. Verwenden Sie `1`-`9` für schnellen Szenario-Wechsel

---

## 8. Häufig gestellte Fragen (FAQ)

### 8.1 Allgemeine Fragen

**Q: Warum gibt es keine Infektionen, obwohl ich hohe Parameter eingestellt habe?**

A: Überprüfen Sie:
- Ist die Simulation pausiert? (Drücken Sie `SPACE`)
- Ist mindestens 1 Partikel initial infiziert? (Fraction Infected Init > 0)
- Ist Infection Probability > 0?
- Sind Partikel nah genug beieinander? (Verkleinern Sie Social Distancing)

**Q: Warum sind die Graphen "leer" oder zeigen keine Daten?**

A: Die Graphen aktualisieren sich täglich. Warten Sie, bis mindestens 2-3 Tage vergangen sind. Erhöhen Sie die Geschwindigkeit auf 5x mit dem entsprechenden Button.

**Q: Kann ich meine eigenen Presets speichern?**

A: In dieser Version nicht direkt über die GUI. Sie können jedoch die Datei `epidemic_sim/config/presets.py` manuell editieren und neue Einträge hinzufügen.

**Q: Wie exportiere ich die Simulationsdaten?**

A: Export-Funktion ist in dieser Version nicht implementiert. Sie können Screenshots machen:
- Windows: `Windows + Shift + S` (Snipping Tool)
- Oder: Print Screen Taste

---

### 8.2 Performance-Fragen

**Q: Die Simulation läuft sehr langsam. Was kann ich tun?**

A: Performance-Optimierungen:
1. **Reduzieren Sie die Population:** 200 Partikel statt 1000
2. **Deaktivieren Sie Infection Radius Display:** Checkbox "Show Infection Radius" ausschalten
3. **Reduzieren Sie Geschwindigkeit:** Nutzen Sie 0.5x oder 1x statt 5x
4. **Communities-Modus deaktivieren:** Simple Mode ist schneller
5. **Schließen Sie andere Programme:** Freier RAM und CPU

**Q: Wie viele Partikel sind "optimal"?**

A:
- **Unterricht/Demo:** 200-300 Partikel (60 FPS, flüssig)
- **Experimente:** 500 Partikel (30 FPS, guter Kompromiss)
- **Forschung:** 1000 Partikel (20 FPS, hohe Präzision)

**Q: Warum "ruckelt" die Animation bei 1000 Partikeln?**

A: Das ist normal. Die Simulation verwendet adaptives Frame-Skipping:
- <200 Partikel: 60 FPS (jeder Frame)
- 200-500: 30 FPS (jeder 2. Frame)
- >500: 20 FPS (jeder 3. Frame)

Dies erhält die Simulationsgeschwindigkeit bei reduzierter Rendering-Last.

---

### 8.3 Wissenschaftliche Fragen

**Q: Was bedeutet R0 (Basisreproduktionszahl)?**

A: R0 ist die durchschnittliche Anzahl von Menschen, die eine infizierte Person ansteckt (ohne Interventionen).
- R0 < 1: Epidemie stirbt aus
- R0 = 1: Endemisches Gleichgewicht
- R0 > 1: Epidemie breitet sich aus

In dieser Simulation wird R0 durch folgende Parameter beeinflusst:
- Infection Radius (größer → mehr Kontakte → höheres R0)
- Infection Probability (höher → mehr Übertragungen → höheres R0)
- Infection Duration (länger → mehr Gelegenheiten → höheres R0)

**Q: Warum ist die Sterblichkeitsrate (CFR) nicht gleich der Mortalitätsrate im Preset?**

A: CFR (Case Fatality Rate) ist der Anteil der Infizierten, die sterben. In der Simulation:
- **Mortality Rate Parameter:** Wahrscheinlichkeit des Todes am Ende der Infektion
- **Beobachtete CFR:** Kann niedriger sein, wenn Interventionen die Infektionszahl reduzieren

**Q: Wie realistisch sind die Simulationen?**

A: Die Simulation ist ein **vereinfachtes Modell**:

**Realistische Aspekte:**
- SEIRD-Modell (epidemiologisch fundiert)
- Drei Verteilungsfunktionen (biologische Variation)
- Räumliche Dynamik (geografische Ausbreitung)
- Interventionseffekte (Quarantäne, Distanzierung)

**Vereinfachungen:**
- Homogene Mischung (keine Altersgruppen, Vorerkrankungen)
- Konstante Parameter (keine zeitliche Variation)
- 2D-Raum (vereinfachte Topologie)
- Keine Demografie (keine Geburten/natürliche Todesfälle)

**Fazit:** Geeignet für **qualitative** Einsichten, nicht für **quantitative** Vorhersagen.

---

### 8.4 Technische Fragen

**Q: Kann ich die Simulation auf Mac/Linux nutzen?**

A: Ja! Die Simulation ist in Python geschrieben und plattformunabhängig:
1. Installieren Sie Python 3.8+ für Ihr System
2. Installieren Sie Abhängigkeiten: `pip install -r requirements.txt`
3. Starten Sie: `python epidemic_sim/main.py`

**Q: Wie erstelle ich eine .exe-Datei?**

A: Verwenden Sie PyInstaller:
```bash
pip install pyinstaller
pyinstaller --onefile --windowed epidemic_sim/main.py
```
Die .exe befindet sich dann in `dist/main.exe`.

**Q: Warum funktioniert die Simulation nicht auf meinem Schulrechner?**

A: Häufige Ursachen:
1. **Python nicht installiert:** Laden Sie Python 3.8+ herunter
2. **Fehlende Bibliotheken:** Führen Sie `pip install -r requirements.txt` aus
3. **Administratorrechte:** Manche Schulrechner blockieren Python-Ausführung
4. **Antivirus:** Kann Python-Skripte fälschlicherweise blockieren

**Lösung:** Erstellen Sie eine .exe-Datei (siehe oben) oder kontaktieren Sie den IT-Support.

---

## 9. Fehlerbehebung

### 9.1 Häufige Fehler

#### Fehler: "ModuleNotFoundError: No module named 'PyQt5'"

**Ursache:** PyQt5 nicht installiert

**Lösung:**
```bash
pip install PyQt5
```

Oder alle Abhängigkeiten auf einmal:
```bash
pip install -r requirements.txt
```

---

#### Fehler: "Application failed to start because no Qt platform plugin could be initialized"

**Ursache:** PyQt5 nicht korrekt installiert oder fehlende Systemabhängigkeiten

**Lösung:**
```bash
# Deinstallieren und neu installieren
pip uninstall PyQt5
pip install PyQt5

# Unter Linux: Installieren Sie zusätzliche Abhängigkeiten
sudo apt-get install python3-pyqt5 libqt5widgets5
```

---

#### Fehler: "Simulation friert ein" oder "No response"

**Ursache:** Zu viele Partikel oder Endlosschleife

**Lösung:**
1. Drücken Sie `Ctrl+C` im Terminal, um Programm zu beenden
2. Starten Sie neu mit weniger Partikeln (z.B. 200)
3. Aktualisieren Sie auf die neueste Version

---

#### Fehler: "Quarantine-Zone ist leer" trotz aktivierter Quarantäne

**Ursache:** Quarantäne-Bedingungen nicht erfüllt

**Überprüfen Sie:**
- Ist "Quarantine After" < aktuelle Tage der Infizierten?
- Ist "Quarantine Start Day" <= aktueller Simulationstag?
- Ist "Asymptomatic Rate" < 100%? (100% = niemand zeigt Symptome)
- Gibt es überhaupt Infizierte?

---

### 9.2 Leistungsprobleme

#### Problem: FPS zu niedrig

**Lösungen:**
1. Reduzieren Sie Population Size auf 200-300
2. Deaktivieren Sie "Show Infection Radius"
3. Wechseln Sie von Communities zu Simple Mode
4. Schließen Sie andere Anwendungen
5. Aktualisieren Sie Grafiktreiber

---

#### Problem: Verzögerte UI-Reaktion

**Lösungen:**
1. Pausieren Sie Simulation beim Anpassen von Parametern
2. Reduzieren Sie Simulationsgeschwindigkeit auf 1x
3. Verwenden Sie Presets statt manuelle Parameteranpassung

---

### 9.3 Visuelle Probleme

#### Problem: Canvas ist schwarz/leer

**Ursachen & Lösungen:**
1. **Keine Partikel erstellt:** Drücken Sie RESET (`R`)
2. **Falsche Farben:** Überprüfen Sie Theme-Einstellungen
3. **Grafiktreiber-Problem:** Aktualisieren Sie Treiber
4. **High-DPI-Display:** Windows-Skalierung kann Probleme verursachen
   - Rechtsklick auf python.exe → Eigenschaften → Kompatibilität
   - "Skalierung bei hohen DPI-Einstellungen überschreiben" aktivieren

---

#### Problem: Schrift zu klein/zu groß

**Lösung:**
- Drücken Sie `+` zum Vergrößern
- Drücken Sie `-` zum Verkleinern
- Einstellung wird automatisch gespeichert

---

### 9.4 Kontakt & Support

**Für technische Probleme:**
- Prüfen Sie zuerst dieses Handbuch und die FAQ
- Konsultieren Sie die README.md im Projektverzeichnis
- Erstellen Sie ein Issue auf GitHub (falls verfügbar)

**Für Bildungsfragen:**
- Kontaktieren Sie Ihre Lehrkraft
- Nutzen Sie die Tooltip-Funktion in der Anwendung (Maus über Parameter)

---

## Anhang: Schnellreferenz

### Parameter-Empfehlungen für Szenarien

| Szenario | Infection Radius | Prob. Infection | Duration | Mortality | Quarantine | Social Dist. |
|----------|------------------|-----------------|----------|-----------|------------|--------------|
| Keine Intervention | 0.15 | 0.15 | 25 | 0.02 | ❌ | ❌ |
| Nur Quarantäne | 0.15 | 0.15 | 25 | 0.02 | ✅ (Day 10) | ❌ |
| Nur Social Distancing | 0.15 | 0.15 | 25 | 0.02 | ❌ | ✅ (Str: 1.0) |
| Kombiniert | 0.15 | 0.15 | 25 | 0.02 | ✅ (Day 10) | ✅ (Str: 1.0) |
| Superspreader-Event | 0.15 | 0.15 | 25 | 0.02 | ❌ | ❌ + Marketplace ✅ |

---

### Tastaturkürzel (Schnellzugriff)

```
STEUERUNG:              INTERVENTIONEN:        PRESETS:
Space = Pause/Resume    Q = Quarantine         1 = COVID-19 (Orig)
R     = Reset           M = Marketplace        2 = COVID-19 (Delta)
F     = Fullscreen                             3 = COVID-19 (Omicron)
                                               4 = Spanish Flu
                                               5 = Measles
                                               6 = Ebola
                                               7 = Influenza
                                               8 = Common Cold
                                               9 = SARS
```

---

**Ende des Benutzerhandbuchs**
**Version:** 3.0
**Letzte Aktualisierung:** Februar 2025
