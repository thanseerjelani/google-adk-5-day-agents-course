"""
Day 2 - Task 2A: Custom Function Tools
Currency Converter with Fee Calculation

Demonstrates:
- Function tools with best practices
- Dictionary returns with status
- Type hints and docstrings
- Error handling
"""

def get_fee_for_payment_method(method: str) -> dict:
    """Looks up transaction fee percentage for a payment method.
    
    Args:
        method: Payment method name (e.g., "platinum credit card")
    
    Returns:
        {"status": "success", "fee_percentage": 0.02} or
        {"status": "error", "error_message": "..."}
    """
    fee_database = {
        "platinum credit card": 0.02,
        "gold debit card": 0.035,
        "bank transfer": 0.01,
    }
    
    fee = fee_database.get(method.lower())
    if fee is not None:
        return {"status": "success", "fee_percentage": fee}
    return {"status": "error", "error_message": f"Payment method '{method}' not found"}


def get_exchange_rate(base_currency: str, target_currency: str) -> dict:
    """Gets exchange rate between two currencies.
    
    Args:
        base_currency: ISO 4217 code (e.g., "USD")
        target_currency: ISO 4217 code (e.g., "EUR")
    
    Returns:
        {"status": "success", "rate": 0.93} or
        {"status": "error", "error_message": "..."}
    """
    rate_database = {
        "usd": {"eur": 0.93, "jpy": 157.50, "inr": 83.58}
    }
    
    rate = rate_database.get(base_currency.lower(), {}).get(target_currency.lower())
    if rate:
        return {"status": "success", "rate": rate}
    return {"status": "error", "error_message": f"Unsupported pair: {base_currency}/{target_currency}"}


# Create agent with custom tools
from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini

currency_agent = LlmAgent(
    name="currency_agent",
    model=Gemini(model="gemini-2.5-flash-lite"),
    instruction="""You are a currency conversion assistant.
    
    For conversion requests:
    1. Use get_fee_for_payment_method() for transaction fees
    2. Use get_exchange_rate() for conversion rates
    3. Check "status" field in responses
    4. Calculate final amount and provide breakdown
    """,
    tools=[get_fee_for_payment_method, get_exchange_rate]
)

# Key Learnings:
# - Function tools need clear docstrings (LLM reads them)
# - Always return dict with "status" field
# - Type hints enable ADK to generate schemas
# - Error handling via structured responses