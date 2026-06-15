"""Additional unit tests for OCR text utility edge cases."""

from app.services.text_utils import extract_marks_from_block, merge_answers_by_question


def test_extract_marks_sums_compound_marking_scheme():
    text = "Q4. Solve the equation [2+3 Marks]\nShow all working."

    assert extract_marks_from_block(text) == 5


def test_merge_answers_keeps_longest_valid_answer_for_each_rubric_question():
    answers = [
        {
            "question_number": "q1",
            "extracted_text": "A short but valid response about Newton's laws.",
            "ocr_confidence": 0.9,
        },
        {
            "question_number": "1",
            "extracted_text": "A longer valid response explaining that net force equals mass times acceleration.",
            "ocr_confidence": 0.5,
        },
        {
            "question_number": "Q2",
            "extracted_text": "This answer is outside the selected rubric.",
            "ocr_confidence": 0.9,
        },
    ]

    merged = merge_answers_by_question(answers, rubric_questions=["Q1"])

    assert len(merged) == 1
    assert merged[0]["question_number"] == "Q1"
    assert merged[0]["extracted_text"].startswith("A longer valid response")
    assert merged[0]["is_blank"] is False
