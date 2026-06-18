from typing import Any

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from src.agentic_system import run_agent
from src.tools import retail_summary


app = FastAPI(title="AI Retail Data Analyst Agent")


class QuestionRequest(BaseModel):
    question: str


@app.get("/", response_class=HTMLResponse)
def home():
    summary = retail_summary()

    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>AI Retail Data Analyst Agent</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <style>
        :root {{
            --bg: #0b1120;
            --panel: #111827;
            --panel-light: #172033;
            --border: #263244;
            --text: #f8fafc;
            --muted: #94a3b8;
            --accent: #2563eb;
            --accent-hover: #1d4ed8;
            --table-bg: #020617;
            --table-head: #1e293b;
            --success: #22c55e;
            --spark: #f97316;
        }}

        * {{
            box-sizing: border-box;
        }}

        body {{
            margin: 0;
            font-family: Inter, Arial, sans-serif;
            background: linear-gradient(135deg, #020617 0%, #0f172a 45%, #111827 100%);
            color: var(--text);
        }}

        .page {{
            max-width: 1180px;
            margin: 0 auto;
            padding: 40px 24px 64px;
        }}

        .hero {{
            border: 1px solid var(--border);
            background: rgba(17, 24, 39, 0.88);
            border-radius: 22px;
            padding: 34px;
            box-shadow: 0 24px 70px rgba(0, 0, 0, 0.28);
            margin-bottom: 24px;
        }}

        .eyebrow {{
            color: #93c5fd;
            font-size: 14px;
            font-weight: 700;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            margin-bottom: 12px;
        }}

        h1 {{
            margin: 0;
            font-size: 38px;
            line-height: 1.15;
            letter-spacing: -0.03em;
        }}

        .subtitle {{
            margin-top: 16px;
            color: #cbd5e1;
            max-width: 900px;
            font-size: 17px;
            line-height: 1.65;
        }}

        .examples {{
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin-top: 24px;
        }}

        .example-btn {{
            background: #172033;
            color: #e5e7eb;
            border: 1px solid #334155;
            border-radius: 999px;
            padding: 9px 14px;
            cursor: pointer;
            font-weight: 600;
        }}

        .example-btn:hover {{
            background: #23314a;
        }}

        .pandas-btn {{
            border-color: #60a5fa;
            color: #bfdbfe;
            background: #1e293b;
        }}

        .spark-btn {{
            border-color: #fb923c;
            color: #fed7aa;
            background: #24160d;
        }}

        .kpi-grid {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 16px;
            margin-bottom: 24px;
        }}

        .kpi {{
            border: 1px solid var(--border);
            background: rgba(17, 24, 39, 0.92);
            border-radius: 18px;
            padding: 20px;
        }}

        .kpi-label {{
            color: var(--muted);
            font-size: 13px;
            margin-bottom: 8px;
        }}

        .kpi-value {{
            font-size: 24px;
            font-weight: 800;
            letter-spacing: -0.02em;
        }}

        .card {{
            border: 1px solid var(--border);
            background: rgba(17, 24, 39, 0.94);
            border-radius: 20px;
            padding: 24px;
            margin-bottom: 24px;
        }}

        .input-row {{
            display: grid;
            grid-template-columns: 1fr 150px;
            gap: 14px;
        }}

        input {{
            width: 100%;
            padding: 16px 18px;
            border-radius: 14px;
            border: 1px solid #334155;
            background: #020617;
            color: #f8fafc;
            font-size: 16px;
            outline: none;
        }}

        input:focus {{
            border-color: #60a5fa;
            box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.22);
        }}

        button.primary {{
            padding: 16px 18px;
            border-radius: 14px;
            border: none;
            background: var(--accent);
            color: white;
            font-weight: 800;
            cursor: pointer;
            font-size: 15px;
        }}

        button.primary:hover {{
            background: var(--accent-hover);
        }}

        .loading {{
            color: #93c5fd;
            margin-top: 16px;
            font-weight: 600;
        }}

        .question-guide {{
            display: none;
        }}

        .question-guide-header {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            gap: 16px;
            margin-bottom: 18px;
            flex-wrap: wrap;
        }}

        .question-guide-title {{
            margin: 0;
            font-size: 22px;
            letter-spacing: -0.02em;
        }}

        .question-guide-subtitle {{
            margin-top: 8px;
            color: var(--muted);
            line-height: 1.5;
            max-width: 850px;
        }}

        .guide-badge {{
            display: inline-block;
            margin-bottom: 10px;
            padding: 6px 10px;
            border-radius: 999px;
            font-size: 12px;
            font-weight: 800;
            letter-spacing: 0.06em;
            text-transform: uppercase;
        }}

        .guide-badge.pandas {{
            color: #bfdbfe;
            border: 1px solid #60a5fa;
            background: rgba(37, 99, 235, 0.15);
        }}

        .guide-badge.spark {{
            color: #fed7aa;
            border: 1px solid #fb923c;
            background: rgba(249, 115, 22, 0.12);
        }}

        .close-btn {{
            background: #172033;
            color: #e5e7eb;
            border: 1px solid #334155;
            border-radius: 10px;
            padding: 8px 12px;
            cursor: pointer;
            font-weight: 700;
        }}

        .close-btn:hover {{
            background: #23314a;
        }}

        .question-list {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 12px;
        }}

        .question-item {{
            text-align: left;
            background: #020617;
            color: #e5e7eb;
            border: 1px solid #334155;
            border-radius: 12px;
            padding: 13px 14px;
            cursor: pointer;
            line-height: 1.4;
            font-size: 14px;
        }}

        .question-item:hover {{
            border-color: #60a5fa;
            background: #0f172a;
        }}

        .question-item.spark:hover {{
            border-color: #fb923c;
        }}

        .result-header {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            gap: 16px;
            margin-bottom: 18px;
            flex-wrap: wrap;
        }}

        .tool {{
            display: inline-block;
            background: #0f172a;
            border: 1px solid #334155;
            color: #93c5fd;
            padding: 7px 10px;
            border-radius: 10px;
            font-family: Consolas, monospace;
            font-size: 13px;
            margin-top: 6px;
        }}

        .answer {{
            color: #e5e7eb;
            line-height: 1.6;
            margin: 0;
        }}

        .table-wrap {{
            width: 100%;
            overflow-x: auto;
            border-radius: 14px;
            border: 1px solid var(--border);
            margin-top: 16px;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            background: var(--table-bg);
            min-width: 720px;
        }}

        th, td {{
            padding: 13px 16px;
            border-bottom: 1px solid #1f2937;
            text-align: left;
            font-size: 14px;
            white-space: nowrap;
        }}

        th {{
            background: var(--table-head);
            color: #f8fafc;
            font-weight: 800;
        }}

        td {{
            color: #e5e7eb;
        }}

        tr:hover td {{
            background: rgba(30, 41, 59, 0.55);
        }}

        .error {{
            color: #fecaca;
            background: #7f1d1d;
            border: 1px solid #991b1b;
            padding: 14px;
            border-radius: 12px;
        }}

        .empty {{
            color: var(--muted);
            padding: 12px 0;
        }}

        pre {{
            white-space: pre-wrap;
            color: #e5e7eb;
            background: #020617;
            border: 1px solid #334155;
            border-radius: 12px;
            padding: 14px;
            overflow-x: auto;
        }}

        @media (max-width: 850px) {{
            .kpi-grid {{
                grid-template-columns: repeat(2, 1fr);
            }}

            .input-row {{
                grid-template-columns: 1fr;
            }}

            .question-list {{
                grid-template-columns: 1fr;
            }}

            h1 {{
                font-size: 30px;
            }}
        }}

        @media (max-width: 520px) {{
            .kpi-grid {{
                grid-template-columns: 1fr;
            }}

            .page {{
                padding: 24px 14px;
            }}

            .hero, .card {{
                padding: 20px;
            }}
        }}
    </style>
</head>

<body>
    <main class="page">
        <section class="hero">
            <div class="eyebrow">Retail Data Analytics</div>
            <h1>AI Retail Data Analyst Agent</h1>
            <p class="subtitle">
                A browser-based analytics assistant for the Online Retail dataset.
                The application maps natural-language questions to controlled analysis tools
                and returns structured business insights as tables or summaries.
            </p>

            <div class="examples">
                <button class="example-btn" onclick="setQuestion('Which products generate the highest revenue?')">Top products</button>
                <button class="example-btn" onclick="setQuestion('Show sales by country.')">Sales by country</button>
                <button class="example-btn" onclick="setQuestion('How does monthly revenue develop?')">Monthly revenue</button>
                <button class="example-btn" onclick="setQuestion('Are there missing values?')">Missing values</button>
                <button class="example-btn" onclick="setQuestion('Analyze returns.')">Returns</button>

                <button class="example-btn pandas-btn" onclick="showQuestionGuide('pandas')">Pandas questions</button>
                <button class="example-btn spark-btn" onclick="showQuestionGuide('spark')">PySpark questions</button>
            </div>
        </section>

        <section class="kpi-grid">
            <div class="kpi">
                <div class="kpi-label">Rows analyzed</div>
                <div class="kpi-value">{summary["rows"]:,}</div>
            </div>
            <div class="kpi">
                <div class="kpi-label">Total revenue</div>
                <div class="kpi-value">£{summary["total_revenue"]:,.0f}</div>
            </div>
            <div class="kpi">
                <div class="kpi-label">Unique orders</div>
                <div class="kpi-value">{summary["unique_orders"]:,}</div>
            </div>
            <div class="kpi">
                <div class="kpi-label">Countries</div>
                <div class="kpi-value">{summary["countries"]}</div>
            </div>
        </section>

        <section class="card">
            <div class="input-row">
                <input id="questionInput" type="text" value="Show sales by country." placeholder="Ask a question about the retail dataset...">
                <button class="primary" onclick="askAgent()">Ask Agent</button>
            </div>
            <div id="loading" class="loading" style="display:none;">Analyzing request...</div>
        </section>

        <section id="questionGuide" class="card question-guide"></section>

        <section id="result" class="card" style="display:none;"></section>
    </main>

    <script>
        const questionExamples = {{
            pandas: {{
                title: "Possible Pandas Questions",
                badge: "Pandas tools",
                badgeClass: "pandas",
                subtitle: "These questions use the standard pandas-based tools for direct web-app analytics.",
                questions: [
                    "Give me a general summary.",
                    "Show sales by country.",
                    "Show the top 10 countries by revenue.",
                    "Which products generate the highest revenue?",
                    "Show the top 20 products by revenue.",
                    "How does monthly revenue develop?",
                    "Show monthly revenue trend.",
                    "Analyze returns.",
                    "Are there missing values?",
                    "Show the dataset structure.",
                    "Which columns are in the dataset?",
                    "Describe the dataset.",
                    "Show the top 10 customers by revenue.",
                    "Show average order value by country.",
                    "Show monthly order development.",
                    "Show monthly average order value.",
                    "Which products have the highest return rate?",
                    "Show return rate by country."
                ]
            }},
            spark: {{
                title: "Possible PySpark Questions",
                badge: "PySpark tools",
                badgeClass: "spark",
                subtitle: "These questions use the PySpark-based advanced analytics layer for customer segmentation, basket analysis, KPI dashboards, scorecards and data-quality reports.",
                questions: [
                    "Show customer segments with Spark.",
                    "Create an RFM customer segmentation.",
                    "Show the top 20 customer segments with Spark.",
                    "Which customers are Champions based on RFM?",
                    "Which products are often bought together?",
                    "Run a market basket analysis.",
                    "Show product pairs that are often bought together.",
                    "Create a monthly KPI dashboard.",
                    "Show an advanced monthly KPI overview with Spark.",
                    "Compare countries with a scorecard.",
                    "Create a country performance scorecard.",
                    "Compare countries by revenue, AOV and return rate.",
                    "Run a full data quality report.",
                    "Create an extended Spark data quality report.",
                    "Run a Spark validation report."
                ]
            }}
        }};

        function setQuestion(text) {{
            document.getElementById("questionInput").value = text;
        }}

        function showQuestionGuide(type) {{
            const guide = questionExamples[type];
            const guideDiv = document.getElementById("questionGuide");

            if (!guide) {{
                return;
            }}

            let html = `
                <div class="question-guide-header">
                    <div>
                        <span class="guide-badge ${{guide.badgeClass}}">${{guide.badge}}</span>
                        <h2 class="question-guide-title">${{guide.title}}</h2>
                        <p class="question-guide-subtitle">${{guide.subtitle}}</p>
                    </div>
                    <button class="close-btn" onclick="hideQuestionGuide()">Close</button>
                </div>
                <div class="question-list">
            `;

            guide.questions.forEach(question => {{
                const buttonClass = guide.badgeClass === "spark"
                    ? "question-item spark"
                    : "question-item";

                html += `
                    <button class="${{buttonClass}}" data-question="${{escapeHtml(question)}}">
                        ${{escapeHtml(question)}}
                    </button>
                `;
            }});

            html += "</div>";

            guideDiv.innerHTML = html;
            guideDiv.style.display = "block";

            guideDiv.querySelectorAll(".question-item").forEach(button => {{
                button.addEventListener("click", () => {{
                    setQuestion(button.dataset.question);
                    document.getElementById("questionInput").focus();
                }});
            }});

            guideDiv.scrollIntoView({{ behavior: "smooth", block: "start" }});
        }}

        function hideQuestionGuide() {{
            const guideDiv = document.getElementById("questionGuide");
            guideDiv.style.display = "none";
        }}

        function escapeHtml(text) {{
            return String(text)
                .replaceAll("&", "&amp;")
                .replaceAll("<", "&lt;")
                .replaceAll(">", "&gt;")
                .replaceAll('"', "&quot;")
                .replaceAll("'", "&#039;");
        }}

        async function askAgent() {{
            const question = document.getElementById("questionInput").value.trim();
            const resultDiv = document.getElementById("result");
            const loadingDiv = document.getElementById("loading");

            if (!question) {{
                resultDiv.style.display = "block";
                resultDiv.innerHTML = '<div class="error">Please enter a question.</div>';
                return;
            }}

            loadingDiv.style.display = "block";
            resultDiv.style.display = "none";

            try {{
                const response = await fetch("/ask", {{
                    method: "POST",
                    headers: {{ "Content-Type": "application/json" }},
                    body: JSON.stringify({{ question }})
                }});

                const result = await response.json();

                loadingDiv.style.display = "none";
                resultDiv.style.display = "block";

                if (!result.ok) {{
                    resultDiv.innerHTML = `<div class="error">${{escapeHtml(result.error)}}</div>`;
                    return;
                }}

                resultDiv.innerHTML = renderResult(result);
                resultDiv.scrollIntoView({{ behavior: "smooth", block: "start" }});

            }} catch (error) {{
                loadingDiv.style.display = "none";
                resultDiv.style.display = "block";
                resultDiv.innerHTML = `<div class="error">Request failed: ${{escapeHtml(error)}}</div>`;
            }}
        }}

        function formatColumnName(name) {{
            return String(name)
                .replaceAll("_", " ")
                .replace(/\\b\\w/g, char => char.toUpperCase());
        }}

        function formatValue(value) {{
            if (value === null || value === undefined) {{
                return "";
            }}

            if (typeof value === "number") {{
                return Number.isInteger(value)
                    ? value.toLocaleString()
                    : value.toLocaleString(undefined, {{ maximumFractionDigits: 2 }});
            }}

            return escapeHtml(value);
        }}

        function renderResult(result) {{
            let html = `
                <div class="result-header">
                    <div>
                        <div><strong>Sub-agent</strong></div>
                        <span class="tool">${{escapeHtml(result.sub_agent || "unknown")}}</span>
                    </div>
                    <div>
                        <div><strong>Tool used</strong></div>
                        <span class="tool">${{escapeHtml(result.tool || "unknown")}}</span>
                    </div>
                </div>
                <p class="answer"><strong>Answer:</strong> ${{escapeHtml(result.answer || "")}}</p>
            `;

            html += renderData(result.data);
            return html;
        }}

        function renderData(data) {{
            if (Array.isArray(data)) {{
                if (data.length === 0) {{
                    return '<p class="empty">No records found.</p>';
                }}

                const columns = Object.keys(data[0]);
                let table = '<div class="table-wrap"><table><thead><tr>';

                columns.forEach(col => {{
                    table += `<th>${{escapeHtml(formatColumnName(col))}}</th>`;
                }});

                table += '</tr></thead><tbody>';

                data.forEach(row => {{
                    table += '<tr>';
                    columns.forEach(col => {{
                        table += `<td>${{formatValue(row[col])}}</td>`;
                    }});
                    table += '</tr>';
                }});

                table += '</tbody></table></div>';
                return table;
            }}

            if (typeof data === "object" && data !== null) {{
                let table = '<div class="table-wrap"><table><thead><tr><th>Metric</th><th>Value</th></tr></thead><tbody>';

                Object.entries(data).forEach(([key, value]) => {{
                    table += `<tr><td>${{escapeHtml(formatColumnName(key))}}</td><td>${{formatValue(value)}}</td></tr>`;
                }});

                table += '</tbody></table></div>';
                return table;
            }}

            return `<pre>${{escapeHtml(JSON.stringify(data, null, 2))}}</pre>`;
        }}

        document.getElementById("questionInput").addEventListener("keydown", function(event) {{
            if (event.key === "Enter") {{
                askAgent();
            }}
        }});
    </script>
</body>
</html>
    """


@app.post("/ask")
def ask_agent(request: QuestionRequest) -> dict[str, Any]:
    try:
        result = run_agent(request.question)

        return {
            "ok": True,
            "question": request.question,
            "tool": result["tool"],
            "sub_agent": result.get("sub_agent"),
            "agent_mode": result.get("agent_mode"),
            "orchestrator_route": result.get("orchestrator_route"),
            "answer": result["answer"],
            "data": result["data"],
        }

    except Exception as exc:
        return {
            "ok": False,
            "error": str(exc),
        }