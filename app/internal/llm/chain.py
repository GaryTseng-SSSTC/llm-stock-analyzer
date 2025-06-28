"""
LLM chain for stock trend analysis: embeds signal into prompt and queries LLM.
"""
from typing import Any, Dict
from pathlib import Path
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda, RunnableSerializable
from langchain_core.runnables.retry import RunnableRetry
from langchain_openai import AzureChatOpenAI
from langchain_core.output_parsers import JsonOutputParser
from app.configs.config import get_config
from app.services.analysis.stock_trend_pipeline import analyze_stock_trend_signal

config = get_config()

def get_llm_client() -> AzureChatOpenAI:
    """Return AzureChatOpenAI client for stock analysis."""
    return AzureChatOpenAI(
        azure_deployment=config.azure_openai.deployment,
        azure_endpoint=config.azure_openai.endpoint,
        api_version=config.azure_openai.api_version,
        api_key=config.azure_openai.subscription_key,
        temperature=config.llm.temperature,
        max_tokens=config.llm.max_tokens,
    )

def load_prompt_template(prompt_file: Path) -> PromptTemplate:
    """Load prompt template from file and return a PromptTemplate for stock analysis."""
    try:
        with open(prompt_file, "r", encoding="utf-8") as f:
            prompt_template_str = f.read().strip()
    except Exception as e:
        raise
    # Ensure prompt template contains {stock_id} and {signal_json} variables
    if "{stock_id}" not in prompt_template_str or "{signal_json}" not in prompt_template_str:
        prompt_template_str = (
            prompt_template_str
            + "\n\nStock: {stock_id}\n\nTechnical Indicators:\n```json\n{signal_json}\n```"
        )
    return PromptTemplate(
        input_variables=["stock_id", "signal_json"],
        template=prompt_template_str,
    )

def get_analysis_prompt_template() -> PromptTemplate:
    """Return stock analysis prompt template."""
    return load_prompt_template(config.llm.stock_analyzer_prompt_path)

def build_prompt_formatting_chain(prompt_template: PromptTemplate) -> RunnableLambda:
    """Format prompt for LLM with stock_id and signal_json."""
    import json
    def format_prompt_step(input_data: dict) -> str:
        formatted = prompt_template.format(
            stock_id=input_data["stock_id"],
            signal_json=json.dumps(input_data["signal"], ensure_ascii=False, indent=2),
        )
        return formatted
    return RunnableLambda(format_prompt_step)

def build_llm_call_chain(llm_client: Any) -> RunnableLambda:
    """Call LLM and return response text."""
    def call_llm_step(prompt: str) -> str:
        response = llm_client.invoke(prompt)
        response_text = response.content if hasattr(response, "content") else str(response)
        return response_text
    return RunnableLambda(call_llm_step)

def build_stock_signal_chain() -> RunnableLambda:
    """Chain to produce signal dict from stock_id."""
    def signal_step(stock_id: str) -> Dict[str, Any]:
        signal = analyze_stock_trend_signal(stock_id)
        return {"stock_id": stock_id, "signal": signal}
    return RunnableLambda(signal_step)

def build_json_output_parsing_chain() -> RunnableLambda:
    """Parse LLM response as JSON."""
    def parse_response_step(response_text: str) -> dict:
        parser = JsonOutputParser()
        return parser.parse(response_text)
    return RunnableLambda(parse_response_step)

def build_stock_analysis_chain(llm_client: Any, prompt_template: PromptTemplate) -> RunnableSerializable:
    """Full chain: stock_id → signal → prompt → LLM → JSON parse."""
    return (
        build_stock_signal_chain()
        | build_prompt_formatting_chain(prompt_template)
        | build_llm_call_chain(llm_client)
        | build_json_output_parsing_chain()
    )

def build_stock_analysis_chain_with_retry(llm_client: Any, prompt_template: PromptTemplate) -> RunnableSerializable:
    """Full chain with retry: stock_id → signal → prompt → LLM → JSON parse (with retry)."""
    base_chain = build_stock_analysis_chain(llm_client, prompt_template)
    return RunnableRetry(bound=base_chain, max_attempt_number=config.llm.retry)
