# AI Retail Data Analyst Agent

AI Retail Data Analyst Agent ist eine browserbasierte Analytics-Web-App zur Analyse eines Online-Retail-Datensatzes über natürlichsprachliche Nutzerfragen.

Die Anwendung übersetzt typische Business-Fragen in kontrollierte Analysefunktionen und gibt die Ergebnisse als KPI-Karten, Tabellen oder strukturierte Zusammenfassungen zurück. Im Backend arbeitet eine regelbasierte Sub-Agent-Architektur: Ein Orchestrator analysiert die Nutzerfrage und leitet sie an einen spezialisierten Analyse-Agenten weiter.

Das Projekt nutzt eine pandas-basierte Analysepipeline. Es führt keinen frei generierten Code aus und verwendet in der aktuellen Version kein externes LLM.

## Features

- Browserbasierte Analytics-Oberfläche mit FastAPI
- Analyse eines Online-Retail-Datensatzes mit über 500.000 Transaktionen
- Natürlichsprachliche Fragen für typische Retail-Analysen
- Regelbasierter Orchestrator mit spezialisierten Sub-Agenten
- Kontrollierte pandas-Analysefunktionen statt freier Code-Ausführung
- KPI-Karten für zentrale Retail-Kennzahlen
- Tabellenansichten für Umsatz-, Produkt-, Länder-, Monats- und Retourenanalysen
- Datenpipeline zur Bereinigung und Anreicherung der Rohdaten
- REST-API über den `/ask`-Endpoint
- Einfache lokale Ausführung über Browser, API oder CLI

## Beispiel-Fragen

Die Anwendung kann unter anderem folgende Fragen beantworten:

```text
Show sales by country.
Which products generate the highest revenue?
How does monthly revenue develop?
Analyze returns.
Are there missing values?
Give me a general summary.
```

## Architektur

Das Projekt verwendet eine modulare, regelbasierte Agent-Struktur:

```text
Nutzerfrage
→ Orchestrator Agent
→ spezialisierter Sub-Agent
→ kontrolliertes pandas-Analyse-Tool
→ strukturierte Ausgabe in der Web-App
```

Der Vorteil dieser Architektur ist, dass die Analysewege transparent, kontrollierbar und erweiterbar bleiben. Jede Nutzerfrage wird nicht frei ausgeführt, sondern gezielt einer vorhandenen Analysefunktion zugeordnet.

## Verfügbare Sub-Agenten

| Sub-Agent | Aufgabe | Beispiel-Tools |
|---|---|---|
| Sales Agent | Umsatz-, Produkt- und Länderanalysen | `sales_by_country`, `top_products_by_revenue` |
| Trend Agent | Monatliche Umsatzentwicklung | `monthly_revenue_trend` |
| Returns Agent | Retouren, Stornos und negative Mengen | `returns_analysis` |
| Data Quality Agent | Fehlende Werte und Datensatzstruktur | `check_missing_values`, `describe_dataset` |
| Overview Agent | Allgemeine Retail-Zusammenfassung | `retail_summary` |

## Tech Stack

- Python
- FastAPI
- pandas
- Pydantic
- Uvicorn
- HTML/CSS
- JavaScript
- Git/GitHub

## Datensatz

Das Projekt basiert auf einem Online-Retail-Transaktionsdatensatz mit mehr als 500.000 Zeilen.

Der Rohdatensatz ist nicht im Repository enthalten, da größere lokale Datendateien nicht versioniert werden sollen. Um das Projekt lokal auszuführen, muss der Datensatz unter folgendem Pfad abgelegt werden:

```text
Dataset/archive/online_retail.csv
```

Anschließend wird die Datenaufbereitung ausgeführt:

```bash
python scripts/prepare_data.py
```

Dadurch entsteht der bereinigte Datensatz:

```text
data/processed/retail_clean.csv
```

## Datenaufbereitung

Die Datei `scripts/prepare_data.py` bereitet den Rohdatensatz für die Analyse vor.

Dabei werden unter anderem folgende Schritte durchgeführt:

- Einlesen des Rohdatensatzes
- Vereinheitlichung der Spaltennamen
- Umwandlung von Rechnungsdaten in Datumsformate
- Behandlung fehlender Customer IDs
- Entfernung ungültiger Produktbeschreibungen
- Erstellung neuer Analysevariablen

Erstellte Features:

```text
revenue
is_return
invoice_month
invoice_date
is_valid_sale
```

Diese Variablen werden später für Umsatz-, Produkt-, Länder-, Monats- und Retourenanalysen verwendet.

## Projektstruktur

```text
AI-Data-Analyst-Agent/
│
├── scripts/
│   ├── inspect_dataset.py
│   ├── prepare_data.py
│   └── test_tools.py
│
├── src/
│   ├── agent.py
│   ├── tools.py
│   └── subagents/
│       ├── __init__.py
│       ├── common.py
│       ├── sales_agent.py
│       ├── trend_agent.py
│       ├── returns_agent.py
│       ├── data_quality_agent.py
│       └── overview_agent.py
│
├── main.py
├── webapp.py
├── start_app.bat
├── requirements.txt
└── README.md
```

## Funktionsweise

1. Der Nutzer gibt eine natürlichsprachliche Frage in der Web-App ein.
2. Das FastAPI-Backend empfängt die Anfrage über den `/ask`-Endpoint.
3. Der Orchestrator in `src/agent.py` analysiert die Frage regelbasiert.
4. Die Frage wird an einen passenden Sub-Agenten weitergeleitet.
5. Der Sub-Agent ruft eine kontrollierte pandas-Analysefunktion aus `src/tools.py` auf.
6. Das Ergebnis wird an die Web-App zurückgegeben und als Tabelle oder Zusammenfassung angezeigt.

Beispiel:

```text
Frage:
Show sales by country.

Routing:
Orchestrator → Sales Agent → sales_by_country

Ausgabe:
Umsatz, Menge und Anzahl der Bestellungen nach Ländern.
```

## Installation

Repository klonen und in das Projektverzeichnis wechseln:

```bash
git clone <repository-url>
cd AI-Data-Analyst-Agent
```

Virtuelle Umgebung erstellen und aktivieren:

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

macOS/Linux:

```bash
source .venv/bin/activate
```

Abhängigkeiten installieren:

```bash
pip install -r requirements.txt
```

## Daten vorbereiten

Den Rohdatensatz unter folgendem Pfad ablegen:

```text
Dataset/archive/online_retail.csv
```

Dann die Datenpipeline ausführen:

```bash
python scripts/prepare_data.py
```

## Web-App starten

FastAPI-App lokal starten:

```bash
python -m uvicorn webapp:app --host 127.0.0.1 --port 8002
```

Danach im Browser öffnen:

```text
http://127.0.0.1:8002
```

Unter Windows kann die App alternativ per Doppelklick gestartet werden:

```text
start_app.bat
```

## CLI-Nutzung

Neben der Web-App kann der Agent auch über die Kommandozeile ausgeführt werden:

```bash
python main.py
```

Danach können Fragen direkt im Terminal eingegeben werden. Mit `exit` oder `quit` wird das Programm beendet.

## API-Nutzung

Die Anwendung stellt einen POST-Endpoint bereit:

```text
POST /ask
```

Beispiel-Request:

```json
{
  "question": "Show sales by country."
}
```

Beispiel-Response:

```json
{
  "ok": true,
  "question": "Show sales by country.",
  "tool": "sales_by_country",
  "sub_agent": "sales_agent",
  "agent_mode": "rule_based_subagent_orchestration",
  "orchestrator_route": "sales_agent",
  "answer": "The Sales Agent analyzed revenue, quantity and orders by country.",
  "data": []
}
```

Die automatisch generierte FastAPI-Dokumentation ist verfügbar unter:

```text
http://127.0.0.1:8002/docs
```

## Beispiel-Analysen

### Sales by Country

Berechnet Umsatz, verkaufte Menge und Anzahl der Bestellungen nach Ländern.

### Top Products by Revenue

Identifiziert die Produkte mit dem höchsten Umsatzbeitrag.

### Monthly Revenue Trend

Aggregiert Umsatz, Menge und Anzahl der Bestellungen nach Rechnungsmonat.

### Returns Analysis

Analysiert Retourenzeilen, Retourenquote, zurückgegebene Menge und Rückgabewert.

### Missing Values

Prüft, ob im bereinigten Datensatz noch fehlende Werte vorhanden sind.

### Retail Summary

Gibt eine kompakte Übersicht über zentrale Kennzahlen des bereinigten Datensatzes zurück.

## Ziel des Projekts

Das Projekt zeigt, wie natürlichsprachliche Nutzerfragen kontrolliert in strukturierte Datenanalysen übersetzt werden können.

Im Fokus stehen:

- Datenbereinigung und Feature Engineering mit pandas
- Entwicklung einer FastAPI-Web-App
- Aufbau kontrollierter Analysefunktionen
- Regelbasiertes Tool Routing
- Modulare Sub-Agent-Architektur
- Darstellung von Retail-KPIs und Analyseergebnissen in einer Web-Oberfläche
- Bereitstellung einer einfachen API für analytische Nutzerfragen

Der Analyseprozess folgt dabei diesem Muster:

```text
Natürlichsprachliche Frage
→ regelbasierter Orchestrator
→ spezialisierter Sub-Agent
→ kontrolliertes Analyse-Tool
→ strukturiertes Ergebnis
```

## Hinweise

Dieses Projekt verwendet in der aktuellen Version kein externes LLM und keine kostenpflichtige API. Die Analyse basiert auf regelbasiertem Tool Routing und modularer Sub-Agent-Orchestrierung.

Lokale Datendateien, vorbereitete CSV-Dateien, virtuelle Umgebungen und Umgebungsvariablen sollten nicht versioniert werden.
