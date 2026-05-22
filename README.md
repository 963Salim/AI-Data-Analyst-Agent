# AI Retail Data Analyst Agent

AI Retail Data Analyst Agent ist eine browserbasierte Analytics-Web-App zur Analyse eines Online-Retail-Datensatzes über natürlichsprachliche Nutzerfragen.

Die Anwendung ordnet Nutzerfragen kontrollierten Analysefunktionen zu und gibt die Ergebnisse als KPI-Karten, Tabellen oder strukturierte Zusammenfassungen zurück. Im Backend wird eine regelbasierte Sub-Agent-Architektur verwendet: Ein Orchestrator leitet die Nutzerfrage an spezialisierte Analyse-Agenten weiter.

Standardmäßig nutzt das Projekt pandas-basierte Analysefunktionen. Zusätzlich enthält das Projekt eine prototypische lokale PySpark-Erweiterung für ausgewählte KPI-Aggregationen, um eine skalierbare Alternative zur pandas-basierten Analysepipeline zu demonstrieren.

## Features

- Browserbasierte Analytics-Oberfläche mit FastAPI
- Analyse von über 500.000 Online-Retail-Transaktionen
- Natürlichsprachliche Nutzerfragen für typische Retail-Analysen
- Regelbasierte Sub-Agent-Architektur mit spezialisierten Analyse-Agenten
- Kontrollierte pandas-Analysefunktionen statt freier Code-Ausführung
- Prototypische lokale PySpark-Aggregationen als skalierbare Alternative für ausgewählte Analysen
- KPI-Karten für zentrale Retail-Kennzahlen
- Tabellarische Ergebnisse für Umsatz-, Produkt-, Länder-, Monats- und Retourenanalysen
- Datenpipeline zur Bereinigung und Anreicherung der Rohdaten

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

## Sub-Agent-Architektur

Das Projekt verwendet eine modulare regelbasierte Agent-Struktur:

```text
Nutzerfrage
→ Orchestrator Agent
→ spezialisierter Sub-Agent
→ kontrolliertes pandas-Analyse-Tool
→ strukturierte Ausgabe in der Web-App
```

### Verfügbare Sub-Agenten

| Sub-Agent | Aufgabe | Beispiel-Tools |
|---|---|---|
| Sales Agent | Umsatz-, Produkt- und Länderanalysen | `sales_by_country`, `top_products_by_revenue` |
| Trend Agent | Monatliche Umsatzentwicklung | `monthly_revenue_trend` |
| Returns Agent | Retouren, Stornos und negative Mengen | `returns_analysis` |
| Data Quality Agent | Fehlende Werte und Datensatzstruktur | `check_missing_values`, `describe_dataset` |
| Overview Agent | Allgemeine Retail-Zusammenfassung | `retail_summary` |

Diese Struktur macht den Analyseprozess transparent, kontrolliert und einfach erweiterbar.

## Tech Stack

- Python
- FastAPI
- pandas
- PySpark
- Pydantic
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

## Lokale PySpark-Erweiterung

Neben den standardmäßigen pandas-basierten Analysefunktionen enthält das Projekt eine prototypische PySpark-Erweiterung.

Die Spark-Ausführung erfolgt lokal über:

```text
master("local[*]")
```

Dadurch wird keine Cloud-Infrastruktur benötigt. Es werden weder Azure noch Databricks noch Hadoop verwendet.

Die PySpark-Erweiterung dient dazu, ausgewählte Aggregationen als skalierbare Alternative zur pandas-Pipeline umzusetzen. Aktuell wird beispielhaft die Länderanalyse mit PySpark nachgebaut:

```text
retail_clean.csv
→ PySpark DataFrame
→ Filterung gültiger Verkäufe
→ Aggregation nach Ländern
→ Umsatz, Menge und Anzahl der Bestellungen
→ strukturierte Ausgabe als list[dict]
```

Die Spark-Funktionen befinden sich in:

```text
src/spark_tools.py
```

Ein einfacher Vergleich zwischen pandas- und PySpark-Ergebnis kann ausgeführt werden mit:

```bash
python scripts/test_spark_tools.py
```

Die PySpark-Erweiterung ist als lokaler Prototyp gedacht und ergänzt die bestehende pandas-Pipeline, ohne diese zu ersetzen.

## Projektstruktur

```text
AI-Data-Analyst-Agent/
│
├── scripts/
│   ├── inspect_dataset.py
│   ├── prepare_data.py
│   ├── test_tools.py
│   └── test_spark_tools.py
│
├── src/
│   ├── agent.py
│   ├── tools.py
│   ├── spark_tools.py
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
5. Der Sub-Agent ruft eine kontrollierte pandas-Analysefunktion aus `src/tools.py` auf. Ergänzend enthält `src/spark_tools.py` prototypische PySpark-Versionen ausgewählter Aggregationen.
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

## Daten vorbereiten

Den Rohdatensatz unter folgendem Pfad ablegen:

```text
Dataset/archive/online_retail.csv
```

Dann ausführen:

```bash
python scripts/prepare_data.py
```

## Web-App starten

FastAPI-App starten:

```bash
python -m uvicorn webapp:app --host 127.0.0.1 --port 8001
```

Danach im Browser öffnen:

```text
http://127.0.0.1:8001
```

Unter Windows kann die App alternativ per Doppelklick gestartet werden:

```text
start_app.bat
```

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
http://127.0.0.1:8001/docs
```

## Beispiel-Analysen

### Sales by Country

Berechnet Umsatz, Menge und Anzahl der Bestellungen nach Ländern.

Für diese Analyse existiert zusätzlich eine prototypische PySpark-Implementierung, die dieselbe Aggregation lokal mit Spark DataFrames berechnet.

### Top Products by Revenue

Identifiziert die Produkte mit dem höchsten Umsatzbeitrag.

### Monthly Revenue Trend

Aggregiert Umsatz, Menge und Anzahl der Bestellungen nach Rechnungsmonat.

### Returns Analysis

Analysiert Retourenzeilen, Retourenquote, zurückgegebene Menge und Rückgabewert.

### Missing Values

Prüft, ob im bereinigten Datensatz noch fehlende Werte vorhanden sind.

## Ziel des Projekts

Das Projekt zeigt, wie natürlichsprachliche Nutzerfragen kontrolliert in strukturierte Datenanalysen übersetzt werden können.

Im Fokus stehen:

- Datenbereinigung und Feature Engineering mit pandas
- Entwicklung einer FastAPI-Web-App
- Aufbau kontrollierter Analysefunktionen
- Regelbasiertes Tool Routing
- Modulare Sub-Agent-Architektur
- Darstellung von Retail-KPIs und Analyseergebnissen in einer Web-Oberfläche
- Prototypische Erweiterung ausgewählter KPI-Aggregationen mit lokal ausgeführtem PySpark

Der Analyseprozess folgt dabei diesem Muster:

```text
Natürlichsprachliche Frage
→ regelbasierter Orchestrator
→ spezialisierter Sub-Agent
→ kontrolliertes Analyse-Tool
→ strukturiertes Ergebnis
```

## Hinweis

Dieses Projekt verwendet kein externes LLM und keine kostenpflichtige API. Die aktuelle Version basiert auf regelbasiertem Tool Routing und modularer Sub-Agent-Orchestrierung.

Die PySpark-Erweiterung wird lokal ausgeführt und benötigt keine Cloud-Infrastruktur. Sie dient als Prototyp, um ausgewählte pandas-Aggregationen zusätzlich mit Spark DataFrames umzusetzen.
