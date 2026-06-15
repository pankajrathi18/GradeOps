"""Unit tests for plagiarism similarity filtering."""

from types import SimpleNamespace

import app.services.plagiarism_detector as plagiarism_module
from app.services.plagiarism_detector import PlagiarismDetector


class FakeEmbeddingModel:
    def __init__(self):
        self.encoded_texts: list[list[str]] = []

    def encode(self, texts, convert_to_tensor):
        assert convert_to_tensor is True
        self.encoded_texts.append(texts)
        return list(range(len(texts)))


def _detector(monkeypatch):
    monkeypatch.setattr(
        plagiarism_module,
        "get_settings",
        lambda: SimpleNamespace(
            plagiarism_similarity_threshold=0.9,
            embedding_model_id="unused-in-unit-tests",
        ),
    )
    return PlagiarismDetector()


def test_detect_flags_similar_answers_for_the_same_question(monkeypatch):
    detector = _detector(monkeypatch)
    model = FakeEmbeddingModel()
    monkeypatch.setattr(detector, "_get_model", lambda: model)
    monkeypatch.setattr(
        plagiarism_module.util,
        "cos_sim",
        lambda left, right: [[0.96 if {left, right} == {0, 1} else 0.2]],
    )

    flags = detector.detect(
        [
            {
                "student_id": "student-a",
                "answers": [
                    {"question_number": "q1", "extracted_text": "A sufficiently long answer text."}
                ],
            },
            {
                "student_id": "student-b",
                "answers": [
                    {"question_number": "Q1", "extracted_text": "Another sufficiently long answer."}
                ],
            },
        ]
    )

    assert len(flags) == 1
    assert flags[0].question == "Q1"
    assert flags[0].student_id_a == "student-a"
    assert flags[0].student_id_b == "student-b"
    assert flags[0].similarity == 0.96
    assert len(model.encoded_texts) == 1


def test_detect_ignores_short_answers_before_embedding(monkeypatch):
    detector = _detector(monkeypatch)
    model = FakeEmbeddingModel()
    monkeypatch.setattr(detector, "_get_model", lambda: model)

    flags = detector.detect(
        [
            {"student_id": "student-a", "answers": [{"question_number": "Q1", "extracted_text": "short"}]},
            {"student_id": "student-b", "answers": [{"question_number": "Q1", "extracted_text": "also short"}]},
        ]
    )

    assert flags == []
    assert model.encoded_texts == []
