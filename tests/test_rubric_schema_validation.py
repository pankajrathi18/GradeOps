"""Unit tests for rubric schema input shapes."""

import pytest

from app.schemas.rubric import RubricSchema


def test_from_dict_accepts_a_list_of_rubric_items():
    schema = RubricSchema.from_dict(
        [
            {
                "question_number": "Q1",
                "max_marks": 3,
                "key_points": ["Defines momentum"],
            }
        ]
    )

    assert schema.title == "Exam Rubric"
    assert schema.items[0].question_number == "Q1"
    assert schema.items[0].max_marks == 3


def test_from_dict_rejects_an_unsupported_rubric_shape():
    with pytest.raises(ValueError, match="Invalid rubric structure"):
        RubricSchema.from_dict({"title": "Missing items"})
