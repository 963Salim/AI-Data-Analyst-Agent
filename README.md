## English Version

AI Retail Data Analyst Agent is a local analytics web app for exploring a large Online Retail transaction dataset through natural-language questions.

The dataset contains more than 500,000 transaction rows from an online retail business, including information such as invoice numbers, products, quantities, prices, customers, countries, invoice dates, sales revenue and returns. This makes it suitable for typical business analytics tasks such as revenue analysis, product performance, customer analysis, monthly trends, return behavior, data-quality checks and advanced customer or basket analysis.

The project combines a FastAPI web interface, controlled analytics tools, a local Ollama LLM, pandas-based standard analyses, cached PySpark advanced analytics and a Power BI export pipeline. The goal is to show how business questions can be translated into safe, structured and reproducible data analysis workflows.

Instead of letting an LLM freely generate and execute code, the app follows a controlled agent architecture:

```text
User question
→ local Ollama LLM selects the best sub-agent
→ selected sub-agent chooses the correct analysis tool deterministically
→ tool registry validates and executes the tool
→ FastAPI returns structured results to the web app
```

This keeps the system flexible enough for natural-language interaction, while still making the actual data analysis transparent and controlled.

---

## Features

- Browser-based analytics interface built with FastAPI
- Natural-language questions for retail analytics
- Local Ollama LLM for sub-agent selection
- Deterministic sub-agent routing for tool selection
- Controlled pandas tools for standard analytics
- Cached PySpark tools for advanced analytics
- Tool registry for safe and validated tool execution
- KPI cards and table-based result views in the web app
- Power BI export script for reporting-ready tables
- Local-first setup without paid cloud APIs

---

## Example Questions

The app can answer questions such as:

```text
Give me a general summary.
Show sales by country.
Show the top 10 customers by revenue.
Which products generate the highest revenue?
How does monthly revenue develop?
Show monthly average order value.
Analyze returns.
Which products have the highest return rate?
Are there missing values?
Create an RFM customer segmentation.
Run a market basket analysis.
Compare countries by revenue, AOV and return rate.
Create an extended Spark data quality report.
```

---

## Architecture

The project uses a hybrid agent architecture.

The local LLM does not directly execute tools and does not generate Python code. It only chooses the most suitable sub-agent for the user question.

The selected sub-agent then applies deterministic routing logic to choose one of the available analysis tools. Finally, the tool registry validates the tool name and arguments before executing the corresponding Python function.

```text
User question
        |
        v
Local Ollama LLM Supervisor
        |
        v
Sub-Agent
        |
        v
Deterministic Tool Selection
        |
        v
Tool Registry
        |
        v
pandas Tool or cached PySpark Tool
        |
        v
Structured Result in Web App
```

This design reduces hallucinated tool calls and makes the system easier to debug, extend and explain.

---

## Sub-Agents

| Sub-Agent | Responsibility | Example Tools |
|---|---|---|
| `overview_agent` | General summaries and dataset overviews | `retail_summary`, `describe_dataset` |
| `sales_agent` | Revenue, product, customer and country analyses | `sales_by_country`, `top_products_by_revenue`, `top_customers_by_revenue` |
| `trend_agent` | Monthly and time-based analysis | `monthly_revenue_trend`, `monthly_orders_trend`, `monthly_average_order_value` |
| `returns_agent` | Returns, cancellations and return rates | `returns_analysis`, `return_rate_by_product`, `return_rate_by_country` |
| `data_quality_agent` | Missing values and dataset structure checks | `check_missing_values`, `describe_dataset` |
| `spark_agent` | Advanced analytics using cached PySpark results | `spark_customer_rfm_segmentation`, `spark_basket_product_pairs`, `spark_country_performance_scorecard` |

---

## Analytics Tools

### pandas Tools

The pandas layer is used for standard analytics tasks that should run quickly inside the web app.

Examples:

- Retail KPI summary
- Sales by country
- Top products by revenue
- Top customers by revenue
- Average order value by country
- Monthly revenue trend
- Monthly order trend
- Monthly average order value
- Returns analysis
- Return rates by product or country
- Missing value checks
- Dataset structure overview

### Cached PySpark Tools

The PySpark layer is used for heavier advanced analytics. To keep the web app responsive, Spark results are precomputed and stored as JSON cache files.

Examples:

- RFM customer segmentation
- Market basket product-pair analysis
- Monthly KPI dashboard
- Country performance scorecard
- Extended Spark data quality report

At runtime, the web app loads these cached results instead of starting expensive Spark jobs for every user question.

---

## Power BI Export

The project also includes a Power BI export script that creates reporting-ready CSV files.

The export pipeline generates tables such as:

```text
fact_sales.csv
dim_date.csv
dim_product.csv
dim_customer.csv
dim_country.csv
kpi_summary.csv
data_quality_summary.csv
```

These files can be used to build a Power BI dashboard with clean fact and dimension tables.

---

## Tech Stack

- Python
- FastAPI
- pandas
- PySpark
- Ollama
- Pydantic
- Uvicorn
- HTML/CSS/JavaScript
- Power BI export pipeline
- Git/GitHub

---

## Project Structure

```text
AI-Data-Analyst-Agent/
│
├── scripts/
│   ├── prepare_data.py
│   ├── inspect_dataset.py
│   ├── precompute_spark_cache.py
│   ├── precompute_basket_cache_fast.py
│   ├── test_spark_tools.py
│   └── export_powerbi_tables.py
│
├── src/
│   ├── agentic_system.py
│   ├── hybrid_agent.py
│   ├── local_llm_agent.py
│   ├── tool_registry.py
│   ├── tools.py
│   ├── cached_spark_tools.py
│   ├── spark_tools.py
│   ├── spark_session.py
│   │
│   └── subagents/
│       ├── __init__.py
│       ├── common.py
│       ├── overview_agent.py
│       ├── sales_agent.py
│       ├── trend_agent.py
│       ├── returns_agent.py
│       ├── data_quality_agent.py
│       └── spark_agent.py
│
├── main.py
├── webapp.py
├── requirements.txt
├── start_app.bat
└── README.md
```

---

## Data

The project is based on an Online Retail transaction dataset with more than 500,000 rows.

The raw dataset is not included in this repository because local data files can be large. To run the project locally, place the raw dataset here:

```text
Dataset/archive/online_retail.csv
```

Then run the preprocessing script:

```bash
python scripts/prepare_data.py
```

This creates the cleaned dataset:

```text
data/processed/retail_clean.csv
```

---

## Setup

Create and activate a virtual environment:

```bash
python -m venv .venv
```

On Windows:

```bash
.venv\Scripts\activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

Make sure Ollama is running locally and that the selected model is available.

Example:

```bash
ollama run llama3.2
```

---

## Run the Web App

Start the FastAPI app:

```bash
python -m uvicorn webapp:app --host 127.0.0.1 --port 8002
```

Then open:

```text
http://127.0.0.1:8002
```

The app can also be started on Windows with:

```text
start_app.bat
```

---

## Run from the Command Line

The project also includes a simple CLI entry point:

```bash
python main.py
```

You can then type questions directly into the terminal.

---

## Precompute Spark Cache

Advanced PySpark analyses can be precomputed with:

```bash
python scripts/precompute_spark_cache.py
```

For faster basket-analysis cache generation, use:

```bash
python scripts/precompute_basket_cache_fast.py
```

The generated cache files are stored in:

```text
data/cache/
```

These cache files are local generated artifacts and are not meant to be committed to GitHub.

---

## Export Power BI Tables

To generate the Power BI-ready CSV tables, run:

```bash
python scripts/export_powerbi_tables.py
```

The exported files are written to:

```text
exports/powerbi/
```

---

## API Usage

The app exposes a POST endpoint:

```text
POST /ask
```

Example request:

```json
{
  "question": "Show sales by country."
}
```

Example response:

```json
{
  "ok": true,
  "question": "Show sales by country.",
  "tool": "sales_by_country",
  "sub_agent": "sales_agent",
  "agent_mode": "hybrid_supervisor_keyword_subagents",
  "orchestrator_route": "sales_agent",
  "answer": "sales_agent selected the tool 'sales_by_country' and returned the corresponding analysis results.",
  "data": []
}
```

The automatic FastAPI documentation is available at:

```text
http://127.0.0.1:8002/docs
```

---

## Why This Project

This project demonstrates how natural-language analytics can be implemented in a controlled and explainable way.

The main idea is not to let an LLM freely generate analysis code. Instead, the LLM only helps with high-level routing, while the actual analysis is handled by predefined, tested and validated tools.

This makes the system more reliable, easier to extend and safer for analytical use cases.

The project combines several practical data skills:

- Data cleaning and feature engineering
- Backend development with FastAPI
- Agentic system design
- Local LLM integration with Ollama
- pandas-based analytics
- PySpark-based advanced analytics
- Cached analytics for faster web-app responses
- Power BI-ready data export
- GitHub-ready project structure

---

# AI Retail Data Analyst Agent

## Deutsche Version

AI Retail Data Analyst Agent ist eine lokale Analytics-Web-App zur Analyse eines großen Online-Retail-Transaktionsdatensatzes über natürlichsprachliche Fragen.

Der Datensatz umfasst mehr als 500.000 Transaktionszeilen eines Online-Retail-Geschäfts und enthält unter anderem Informationen zu Rechnungsnummern, Produkten, Mengen, Preisen, Kunden, Ländern, Rechnungsdaten, Umsätzen und Retouren. Dadurch eignet sich der Datensatz sehr gut für typische Business-Analytics-Aufgaben wie Umsatzanalysen, Produktperformance, Kundenanalysen, monatliche Trends, Retourenverhalten, Datenqualitätsprüfungen sowie fortgeschrittene Kunden- oder Warenkorbanalysen.

Das Projekt kombiniert eine FastAPI-Weboberfläche, kontrollierte Analysefunktionen, ein lokales Ollama-LLM, pandas-basierte Standardanalysen, gecachte PySpark-Analysen für fortgeschrittene Auswertungen sowie ein Power-BI-Exportskript. Ziel ist es zu zeigen, wie typische Business-Fragen sicher, strukturiert und reproduzierbar in Datenanalysen übersetzt werden können.

Statt ein LLM frei Code generieren und ausführen zu lassen, nutzt die App eine kontrollierte Agenten-Architektur:

```text
Nutzerfrage
→ lokales Ollama-LLM wählt den passenden Sub-Agent
→ ausgewählter Sub-Agent wählt deterministisch das passende Analyse-Tool
→ Tool Registry validiert und führt das Tool aus
→ FastAPI gibt strukturierte Ergebnisse an die Web-App zurück
```

Dadurch bleibt die Anwendung flexibel für natürlichsprachliche Eingaben, während die eigentliche Datenanalyse transparent und kontrolliert abläuft.

---

## Funktionen

- Browserbasierte Analytics-Oberfläche mit FastAPI
- Natürlichsprachliche Fragen für Retail Analytics
- Lokales Ollama-LLM zur Auswahl des passenden Sub-Agents
- Deterministisches Sub-Agent-Routing zur Tool-Auswahl
- Kontrollierte pandas-Tools für Standardanalysen
- Gecachte PySpark-Tools für fortgeschrittene Analysen
- Tool Registry für sichere und validierte Tool-Ausführung
- KPI-Karten und Tabellenansichten in der Web-App
- Power-BI-Exportskript für reportingfähige Tabellen
- Lokales Setup ohne kostenpflichtige Cloud-APIs

---

## Beispiel-Fragen

Die App kann unter anderem folgende Fragen beantworten:

```text
Give me a general summary.
Show sales by country.
Show the top 10 customers by revenue.
Which products generate the highest revenue?
How does monthly revenue develop?
Show monthly average order value.
Analyze returns.
Which products have the highest return rate?
Are there missing values?
Create an RFM customer segmentation.
Run a market basket analysis.
Compare countries by revenue, AOV and return rate.
Create an extended Spark data quality report.
```

---

## Architektur

Das Projekt verwendet eine hybride Agenten-Architektur.

Das lokale LLM führt keine Tools direkt aus und generiert keinen Python-Code. Es wählt nur den passendsten Sub-Agent für die Nutzerfrage aus.

Der ausgewählte Sub-Agent nutzt anschließend deterministische Routing-Logik, um eines der vorhandenen Analyse-Tools auszuwählen. Danach validiert die Tool Registry den Tool-Namen und die Argumente, bevor die passende Python-Funktion ausgeführt wird.

```text
Nutzerfrage
        |
        v
Lokaler Ollama-LLM-Supervisor
        |
        v
Sub-Agent
        |
        v
Deterministische Tool-Auswahl
        |
        v
Tool Registry
        |
        v
pandas-Tool oder gecachtes PySpark-Tool
        |
        v
Strukturiertes Ergebnis in der Web-App
```

Dieses Design reduziert halluzinierte Tool-Aufrufe und macht das System leichter testbar, erweiterbar und erklärbar.

---

## Sub-Agents

| Sub-Agent | Aufgabe | Beispiel-Tools |
|---|---|---|
| `overview_agent` | Allgemeine Zusammenfassungen und Datensatzüberblick | `retail_summary`, `describe_dataset` |
| `sales_agent` | Umsatz-, Produkt-, Kunden- und Länderanalysen | `sales_by_country`, `top_products_by_revenue`, `top_customers_by_revenue` |
| `trend_agent` | Monatliche und zeitbasierte Analysen | `monthly_revenue_trend`, `monthly_orders_trend`, `monthly_average_order_value` |
| `returns_agent` | Retouren, Stornos und Rückgabequoten | `returns_analysis`, `return_rate_by_product`, `return_rate_by_country` |
| `data_quality_agent` | Fehlende Werte und Datensatzstruktur | `check_missing_values`, `describe_dataset` |
| `spark_agent` | Fortgeschrittene Analysen mit gecachten PySpark-Ergebnissen | `spark_customer_rfm_segmentation`, `spark_basket_product_pairs`, `spark_country_performance_scorecard` |

---

## Analyse-Tools

### pandas-Tools

Die pandas-Schicht wird für Standardanalysen genutzt, die schnell direkt in der Web-App laufen sollen.

Beispiele:

- Retail-KPI-Zusammenfassung
- Umsatz nach Land
- Top-Produkte nach Umsatz
- Top-Kunden nach Umsatz
- Durchschnittlicher Bestellwert nach Land
- Monatliche Umsatzentwicklung
- Monatliche Bestellentwicklung
- Monatlicher durchschnittlicher Bestellwert
- Retourenanalyse
- Rückgabequoten nach Produkt oder Land
- Prüfung fehlender Werte
- Überblick über die Datensatzstruktur

### Gecachte PySpark-Tools

Die PySpark-Schicht wird für aufwendigere fortgeschrittene Analysen genutzt. Damit die Web-App schnell reagiert, werden Spark-Ergebnisse vorab berechnet und als JSON-Cache gespeichert.

Beispiele:

- RFM-Kundensegmentierung
- Market-Basket-Analyse für Produktpaare
- Monatliches KPI-Dashboard
- Länder-Performance-Scorecard
- Erweiterter Spark-Datenqualitätsbericht

Zur Laufzeit lädt die Web-App diese gecachten Ergebnisse, statt für jede Nutzerfrage neue Spark-Jobs zu starten.

---

## Power-BI-Export

Das Projekt enthält zusätzlich ein Power-BI-Exportskript, das reportingfähige CSV-Dateien erzeugt.

Die Export-Pipeline erstellt Tabellen wie:

```text
fact_sales.csv
dim_date.csv
dim_product.csv
dim_customer.csv
dim_country.csv
kpi_summary.csv
data_quality_summary.csv
```

Diese Dateien können genutzt werden, um ein Power-BI-Dashboard mit sauberen Fakt- und Dimensionstabellen aufzubauen.

---

## Tech Stack

- Python
- FastAPI
- pandas
- PySpark
- Ollama
- Pydantic
- Uvicorn
- HTML/CSS/JavaScript
- Power-BI-Export-Pipeline
- Git/GitHub

---

## Projektstruktur

```text
AI-Data-Analyst-Agent/
│
├── scripts/
│   ├── prepare_data.py
│   ├── inspect_dataset.py
│   ├── precompute_spark_cache.py
│   ├── precompute_basket_cache_fast.py
│   ├── test_spark_tools.py
│   └── export_powerbi_tables.py
│
├── src/
│   ├── agentic_system.py
│   ├── hybrid_agent.py
│   ├── local_llm_agent.py
│   ├── tool_registry.py
│   ├── tools.py
│   ├── cached_spark_tools.py
│   ├── spark_tools.py
│   ├── spark_session.py
│   │
│   └── subagents/
│       ├── __init__.py
│       ├── common.py
│       ├── overview_agent.py
│       ├── sales_agent.py
│       ├── trend_agent.py
│       ├── returns_agent.py
│       ├── data_quality_agent.py
│       └── spark_agent.py
│
├── main.py
├── webapp.py
├── requirements.txt
├── start_app.bat
└── README.md
```

---

## Daten

Das Projekt basiert auf einem Online-Retail-Transaktionsdatensatz mit mehr als 500.000 Zeilen.

Der Rohdatensatz ist nicht im Repository enthalten, da lokale Datendateien groß sein können. Um das Projekt lokal auszuführen, muss der Rohdatensatz hier abgelegt werden:

```text
Dataset/archive/online_retail.csv
```

Danach wird die Datenaufbereitung gestartet:

```bash
python scripts/prepare_data.py
```

Dadurch entsteht der bereinigte Datensatz:

```text
data/processed/retail_clean.csv
```

---

## Setup

Virtuelle Umgebung erstellen und aktivieren:

```bash
python -m venv .venv
```

Unter Windows:

```bash
.venv\Scripts\activate
```

Abhängigkeiten installieren:

```bash
pip install -r requirements.txt
```

Außerdem muss Ollama lokal laufen und das gewählte Modell verfügbar sein.

Beispiel:

```bash
ollama run llama3.2
```

---

## Web-App starten

FastAPI-App starten:

```bash
python -m uvicorn webapp:app --host 127.0.0.1 --port 8002
```

Danach im Browser öffnen:

```text
http://127.0.0.1:8002
```

Unter Windows kann die App alternativ gestartet werden mit:

```text
start_app.bat
```

---

## Nutzung über die Kommandozeile

Das Projekt enthält zusätzlich einen einfachen CLI-Einstieg:

```bash
python main.py
```

Danach können Fragen direkt im Terminal eingegeben werden.

---

## Spark-Cache vorberechnen

Fortgeschrittene PySpark-Analysen können vorab berechnet werden mit:

```bash
python scripts/precompute_spark_cache.py
```

Für eine schnellere Basket-Analyse-Cache-Erstellung kann alternativ ausgeführt werden:

```bash
python scripts/precompute_basket_cache_fast.py
```

Die erzeugten Cache-Dateien werden hier gespeichert:

```text
data/cache/
```

Diese Cache-Dateien sind lokal generierte Artefakte und sollen nicht nach GitHub committet werden.

---

## Power-BI-Tabellen exportieren

Um Power-BI-fähige CSV-Tabellen zu erzeugen, wird folgendes Skript ausgeführt:

```bash
python scripts/export_powerbi_tables.py
```

Die exportierten Dateien werden hier gespeichert:

```text
exports/powerbi/
```

---

## API-Nutzung

Die App stellt einen POST-Endpunkt bereit:

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
  "agent_mode": "hybrid_supervisor_keyword_subagents",
  "orchestrator_route": "sales_agent",
  "answer": "sales_agent selected the tool 'sales_by_country' and returned the corresponding analysis results.",
  "data": []
}
```

Die automatisch generierte FastAPI-Dokumentation ist verfügbar unter:

```text
http://127.0.0.1:8002/docs
```

---

## Warum dieses Projekt?

Dieses Projekt zeigt, wie natürlichsprachliche Analytics kontrolliert und nachvollziehbar umgesetzt werden können.

Der zentrale Gedanke ist nicht, dass ein LLM frei Analysecode generiert. Stattdessen unterstützt das LLM nur beim übergeordneten Routing, während die eigentliche Analyse durch definierte, testbare und validierte Tools durchgeführt wird.

Dadurch wird das System zuverlässiger, leichter erweiterbar und sicherer für analytische Anwendungsfälle.

Das Projekt verbindet mehrere praxisnahe Data-Skills:

- Datenbereinigung und Feature Engineering
- Backend-Entwicklung mit FastAPI
- Agentic-System-Design
- Lokale LLM-Integration mit Ollama
- pandas-basierte Analysen
- PySpark-basierte fortgeschrittene Analysen
- Gecachte Analysen für schnellere Web-App-Antworten
- Power-BI-fähiger Datenexport
- GitHub-fähige Projektstruktur
