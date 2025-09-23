def test_params_to_params_serializes_aliases(historicjoa_params_kwargs) -> None:
    """Validate Params.to_params uses USAJOBS aliases and formatting."""

    pass


def test_params_to_params_omits_none_fields() -> None:
    """Ensure Params.to_params excludes unset or None-valued fields."""

    pass


def test_item_model_parses_response_payload(historicjoa_response_payload) -> None:
    """Confirm Item model accepts serialized payload dictionaries."""

    pass


def test_response_next_token_returns_continuation(historicjoa_response_payload) -> None:
    """Check Response.next_token surfaces continuation tokens from paging metadata."""

    pass


def test_response_next_token_when_paging_missing() -> None:
    """Validate Response.next_token returns None when paging metadata is absent."""

    pass
