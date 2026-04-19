from helm.benchmark.window_services.default_window_service import DefaultWindowService
from helm.common.tokenization_request import (
    DecodeRequest,
    DecodeRequestResult,
    TokenizationRequest,
    TokenizationRequestResult,
    TokenizationToken,
)


class _FakeTokenizerService:
    def tokenize(self, request: TokenizationRequest) -> TokenizationRequestResult:
        text = request.text
        if request.truncation:
            text = text[: request.max_length]
        tokens = [TokenizationToken(value=i) for i, _ in enumerate(text)]
        return TokenizationRequestResult(
            success=True,
            cached=False,
            text=text,
            tokens=tokens,
        )

    def decode(self, request: DecodeRequest) -> DecodeRequestResult:
        return DecodeRequestResult(
            success=True,
            cached=False,
            text="x" * len(request.tokens),
        )


def test_local_window_service_prefers_combined_budget_for_completion_requests():
    window_service = DefaultWindowService(
        service=_FakeTokenizerService(),
        tokenizer_name="huggingface/gpt2",
        max_sequence_length=2048,
        max_request_length=2048,
        max_sequence_and_generated_tokens_length=2040,
    )

    assert window_service.fits_within_context_window("x" * 2035, expected_completion_token_length=5)
    assert not window_service.fits_within_context_window("x" * 2036, expected_completion_token_length=5)

    truncated = window_service.truncate_from_right("x" * 3000, expected_completion_token_length=5)
    assert len(truncated) == 2035
