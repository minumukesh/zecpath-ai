import json

from src.hr_screening_dataset.dataset_builder import (
    CATEGORIES,
    ROLE_PROFILES,
    build_dataset,
    validate_dataset,
)


class TestHRScreeningDataset:

    def setup_method(self):

        self.dataset = build_dataset()


    def test_multiple_roles_present(self):

        assert len(self.dataset["roles"]) >= 4

        assert set(self.dataset["roles"]) == set(
            ROLE_PROFILES.keys()
        )


    def test_all_categories_present_for_each_role(self):

        for role in self.dataset["roles"]:

            role_categories = {
                item["category"]
                for item in self.dataset["questions"]
                if item["role"] == role
            }

            assert role_categories == set(CATEGORIES)


    def test_question_metadata(self):

        for item in self.dataset["questions"]:

            assert item["expected_answer_type"]

            assert isinstance(
                item["mandatory"],
                bool,
            )

            assert 1 <= item["scoring_importance"] <= 5

            assert item["template_id"]


    def test_multilingual_future_ready_fields(self):

        assert (
            self.dataset["language_strategy"]
            ["supported_languages"]
            == ["en", "ml", "hi"]
        )

        for item in self.dataset["questions"]:

            assert item["language"] == "en"

            assert set(
                item["supported_languages"]
            ) == {"en", "ml", "hi"}

            assert "ml" in item["translations"]

            assert "hi" in item["translations"]


    def test_dataset_validation(self):

        assert validate_dataset(
            self.dataset
        ) == []


    def test_question_count(self):

        assert (
            self.dataset["question_count"]
            == len(self.dataset["roles"])
            * len(CATEGORIES)
        )
