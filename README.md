# llm-stock-analyzer

## Overview

A modern, maintainable API service for LLM-powered stock analysis, built with FastAPI, LangChain, Pydantic, and Python 3.12+. The service provides actionable trading suggestions using technical indicators and LLM reasoning, with a clean separation of business logic, prompt management, and API endpoints.

## Features

- **FastAPI** for async, production-grade API endpoints
- **LangChain** for LLM integration and prompt chaining
- **Pydantic v2** for robust request/response validation
- **YFinance** for global stock data
- **(TODO) Shioaji (永豐金) API integration** for Taiwan market data
- **Modular, testable service and analysis pipeline**
- **Versioned, documented prompt templates**
- **Structured logging and config management**

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

## Project Structure

- `app/main.py` — FastAPI app entrypoint, config, logger
- `app/api/v1/endpoints.py` — API endpoints (LLM analysis, health)
- `app/services/analysis/` — Stock analysis pipeline, technical indicator logic
- `app/internal/llm/chain.py` — LLM chain, prompt formatting, output parsing
- `app/assets/stock_analyzer_prompt.md` — Versioned, documented prompt template
- `app/utils/logger.py` — Structured logging
- `app/configs/config.py` — Pydantic config, YAML loading
- `tests/` — Pytest/unittest test cases

## TODO

- Integrate 永豐金 Shioaji API for Taiwan stock data (currently placeholder, see `app/internal/shioaji/stock_data.py`)
- Add more automated tests and CI
- Expand prompt templates and multi-language support

## License

MIT
