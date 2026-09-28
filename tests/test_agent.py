import pytest

from unittest.mock import MagicMock, patch

from agent.customer_support import CustomerSupportAgent


@patch("agent.customer_support.OPENAI_API_KEY", "test-api-key")
@patch("agent.customer_support.OpenAI")
def test_loads_company_policies(mock_openai):
    """Verify that the agent loads the expected NovaStore company policies."""
    agent = CustomerSupportAgent()

    assert agent.company_policies["company_name"] == "NovaStore"

    policies = agent.company_policies["policies"]

    assert "shipping" in policies
    assert "returns" in policies
    assert "refunds" in policies
    assert "order_tracking" in policies
    assert "escalation" in policies

@patch("agent.customer_support.OPENAI_API_KEY", "test-api-key")
@patch("agent.customer_support.OpenAI")
def test_respond_returns_generated_text(mock_openai):
    """Verify that the agent returns the generated text from the LLM response."""
    mock_client = MagicMock()
    mock_openai.return_value = mock_client

    mock_response = MagicMock()
    mock_response.output_text = "Standard shipping takes 3-5 business days."

    mock_client.responses.create.return_value = mock_response

    agent = CustomerSupportAgent()

    result = agent.respond("How long does standard shipping take?")

    assert result == "Standard shipping takes 3-5 business days."

@patch("agent.customer_support.OPENAI_MODEL", "test-model")
@patch("agent.customer_support.OPENAI_API_KEY", "test-api-key")
@patch("agent.customer_support.OpenAI")
def test_respond_sends_correct_request(mock_openai):
    """Verify that the agent sends the expected model, input, and instructions to the LLM."""
    mock_client = MagicMock()
    mock_openai.return_value = mock_client

    mock_response = MagicMock()
    mock_response.output_text = "Test response"

    mock_client.responses.create.return_value = mock_response

    agent = CustomerSupportAgent()

    customer_message = "Can I return a product after 45 days?"

    agent.respond(customer_message)

    mock_client.responses.create.assert_called_once()

    call_kwargs = mock_client.responses.create.call_args.kwargs

    assert call_kwargs["model"] == "test-model"
    assert call_kwargs["input"] == customer_message
    assert "NovaStore" in call_kwargs["instructions"]
    assert "30 days" in call_kwargs["instructions"]

@patch("agent.customer_support.OPENAI_API_KEY", None)
def test_missing_api_key_raises_error():
    """Verify that agent initialization fails when the OpenAI API key is missing."""
    with pytest.raises(
        ValueError,
        match="OPENAI_API_KEY is not configured."
    ):
        CustomerSupportAgent()