"""Unit tests for AI-provider response parsing."""

from app.services.ai_provider import AIProvider


def test_parse_json_extracts_and_clamps_grade_values():
    provider = AIProvider.__new__(AIProvider)

    result = provider._parse_json(
        'Model response: {"marks_awarded": 8, "confidence": "0.9", '
        '"justification": "Correct derivation."} End.',
        max_marks=5,
    )

    assert result == {
        "marks_awarded": 5,
        "confidence": 0.9,
        "justification": "Correct derivation.",
    }


def test_parse_json_returns_none_for_invalid_or_missing_json():
    provider = AIProvider.__new__(AIProvider)

    assert provider._parse_json("The answer is probably correct.", max_marks=4) is None
    assert provider._parse_json("{not valid json}", max_marks=4) is None
