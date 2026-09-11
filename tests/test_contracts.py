"""Validate both decision examples against the actual published JSON schema."""

import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker


ROOT = Path(__file__).resolve().parents[1]


class ContractTests(unittest.TestCase):
    def test_all_decision_examples_satisfy_schema_and_date_formats(self):
        schema = json.loads(
            (ROOT / "framework/schemas/governance-decision-contract.schema.json")
            .read_text(encoding="utf-8")
        )
        Draft202012Validator.check_schema(schema)
        validator = Draft202012Validator(schema, format_checker=FormatChecker())
        examples = list((ROOT / "framework/templates").glob("*.example.json"))
        self.assertGreaterEqual(len(examples), 2)
        for path in examples:
            with self.subTest(example=path.name):
                validator.validate(json.loads(path.read_text(encoding="utf-8")))


if __name__ == "__main__":
    unittest.main()
