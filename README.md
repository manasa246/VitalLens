# VitalLens 🩺

### Transforming Blood Reports into Actionable Insights

VitalLens is an AI-powered healthcare application that analyzes blood test reports and generates easy-to-understand health insights along with personalized Indian diet recommendations.

## Features

* Upload blood reports in TXT or PDF format
* Extract and analyze blood test parameters
* Classify results as High, Low, or Normal
* Generate simplified health summaries
* Provide personalized Indian diet recommendations
* Download analysis results

## Tech Stack

* Python
* Streamlit
* Google Gemini 2.5 Flash
* LangChain
* PyPDF
* UV

## Installation

```bash
git clone https://github.com/manasa246/VitalLens.git
cd VitalLens
uv sync
```

Create a `.env` file:

```env
GOOGLE_API_KEY=your_google_api_key
```

Run the application:

```bash
uv run streamlit run app.py
```

## How It Works

1. Upload or paste a blood report.
2. AI extracts and analyzes blood test values.
3. Results are classified as High, Low, or Normal.
4. A health summary and diet recommendations are generated.
