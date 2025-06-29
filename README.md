# llm-stock-analyzer

## Overview

A modern, maintainable API service for LLM-powered stock analysis, built with FastAPI, LangChain, Pydantic, and Python 3.12+. The service provides actionable trading suggestions using technical indicators and LLM reasoning, with a clean separation of business logic, prompt management, and API endpoints.

## Features

- **FastAPI** for async, production-grade API endpoints
- **LangChain** for LLM integration and prompt chaining
- **Pydantic v2** for robust request/response validation
- **YFinance** for global stock data
- **Shioaji (永豐金) API integration** for Taiwan market data (modular, see below)
- **Modular, testable service and analysis pipeline**
- **Versioned, documented prompt templates**
- **Structured logging and config management**
- **Comprehensive CI workflow (lint, type check, test)**

## Usage

1. **Start the API service:**

   ```sh
   uvicorn app.main:app --reload
   ```

2. **Health check:**

   ```sh
   curl http://localhost:8000/health
   ```

3. **Get LLM stock analysis:**

   ```sh
   curl -X POST "http://localhost:8000/api/v1/stock/llm-report" \
     -H "Content-Type: application/json" \
     -d '{"stock_id": "2330.TW"}'
   ```

   Response:

   ```json
   {"stock_id":"2330.TW","suggestion":"Long","reason":"The stock is in a strong uptrend with bullish MACD, consistent new highs, and confirmed momentum. Volume is stable and there are no overbought signals on RSI, suggesting the move is not exhausted. While there's no volume spike or breakout, the trend is well-supported and risk appears manageable. Consider a trailing stop to protect profits in case momentum fades."}
   ```

## Environment Setup (Recommended: uv)

1. **Create a virtual environment with uv:**

   ```sh
   uv venv
   ```

2. **Activate the virtual environment:**

   ```sh
   source .venv/bin/activate
   ```

3. **Sync and install all dependencies:**

   ```sh
   uv sync
   ```

## Project Structure

- `app/main.py` — FastAPI app entrypoint, config, logger
- `app/api/v1/endpoints.py` — API endpoints (LLM analysis, health)
- `app/configs/config.py` — Pydantic config, YAML loading
- `app/internal/analysis/indicators.py` — Technical indicator functions (MACD, RSI, OBV, etc.)
- `app/internal/llm/chain.py` — LLM chain, prompt formatting, output parsing (LangChain)
- `app/internal/shioaji/stock_data.py` — Shioaji (TW market) data logic (modular, not required for global)
- `app/internal/yfinance/stock_data.py` — YFinance (global market) data logic
- `app/services/analysis/stock_trend_pipeline.py` — Data pipeline, indicator enrichment
- `app/services/analysis/trend_analysis.py` — Trend signal generation
- `app/utils/logger.py` — Structured logging (Loguru)
- `app/assets/stock_analyzer_prompt.md` — Versioned, documented prompt template
- `tests/` — Pytest test cases for all modules and endpoints
- `.github/workflows/ci.yml` — CI workflow for lint, type check, and tests

## Continuous Integration

- Automated CI runs on every push and pull request via GitHub Actions.
- Checks: formatting, lint, type check (pyright), and all tests.
- See `.github/workflows/ci.yml` for details.

## TODO

- Integrate 永豐金 Shioaji API for Taiwan stock data (see `app/internal/shioaji/stock_data.py`)
- Further enhance test coverage and error handling as needed

## Contributing

- Follow PEP8 and Black formatting for all Python code.
- Use type hints and docstrings for all public functions/classes.
- Keep all business logic modular and testable.
- Do not hardcode secrets or credentials.
- See `.github/copilot-instructions.md` for detailed project and code style guidelines.

## Suggestions & Customization

This repository provides a basic, modular framework for LLM-powered stock analysis. You are encouraged to extend and adapt it for your own needs. Here are some ideas:

- **Prompt Optimization:**  
  The included prompt template is just a starting point. You can refine, expand, or version your prompts to improve LLM output quality and relevance for your use case.

- **LLM Output & Multi-Agent Integration:**  
  The current setup expects a single, structured JSON output. You can adjust the output format, add more fields, or even integrate this service as a component in a larger multi-agent system.

- **Richer Data Inputs:**  
  At present, only technical indicators are used as LLM input. For more comprehensive analysis, consider incorporating fundamental data, market sentiment, news, or institutional flows as additional features.

- **API Layer Flexibility:**  
  FastAPI is used here for demonstration and rapid prototyping. You are free to remove or replace it with another interface (e.g., CLI, batch, or event-driven), but be mindful of how you expose and manage the LLM and analysis pipeline.

Feel free to experiment, refactor, and build on this foundation to suit your own research or production needs!

## License

MIT
