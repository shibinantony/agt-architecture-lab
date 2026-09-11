"""Check the optional source-example guard without importing upstream AGT."""

import importlib.util
import json
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock, patch


EXAMPLE_PATH = Path(__file__).resolve().parents[1] / "examples" / "upstream-agt" / "run.py"
SPEC = importlib.util.spec_from_file_location("upstream_agt_example", EXAMPLE_PATH)
example = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(example)


class UpstreamProvenanceTests(unittest.TestCase):
    def archive(self):
        return {"url": example.EXPECTED_SOURCE_URL, "subdirectory": example.EXPECTED_SUBDIRECTORY, "archive_info": {}}

    def verify(self, provenance, package_version="5.0.0", crypto_version="50.0.1", raw=False):
        metadata = provenance if raw else json.dumps(provenance)
        installed = SimpleNamespace(version=package_version, read_text=Mock(return_value=metadata))
        with patch.object(example, "distribution", return_value=installed), patch.object(example, "version", return_value=crypto_version):
            return example.verify_installation()

    def test_accepts_exact_archive_and_exact_git_revision(self):
        self.assertEqual(self.verify(self.archive()), "5.0.0")
        git = {"url": example.EXPECTED_REPOSITORY_URL + ".git", "subdirectory": example.EXPECTED_SUBDIRECTORY, "vcs_info": {"vcs": "git", "commit_id": example.EXPECTED_SOURCE_COMMIT}}
        self.assertEqual(self.verify(git), "5.0.0")

    def test_rejects_pypi_wheel_and_malformed_source_metadata(self):
        for value in (None, "", "invalid json", "null", "[]"):
            with self.subTest(metadata=value), self.assertRaises(RuntimeError):
                self.verify(value, raw=True)

    def test_rejects_wrong_repository_commit_or_package_directory(self):
        for update in ({"url": "https://untrusted.example/" + example.EXPECTED_SOURCE_COMMIT + ".zip"}, {"url": example.EXPECTED_REPOSITORY_URL + "/archive/main.zip"}, {"subdirectory": "wrong-package"}, {"url": example.EXPECTED_REPOSITORY_URL, "vcs_info": {"vcs": "git", "commit_id": "0" * 40}}):
            with self.subTest(update=update), self.assertRaises(RuntimeError):
                self.verify({**self.archive(), **update})

    def test_rejects_other_package_versions_even_with_expected_source_metadata(self):
        with self.assertRaises(RuntimeError):
            self.verify(self.archive(), package_version="4.1.0")

    def test_rejects_unreviewed_crypto_version(self):
        with self.assertRaises(RuntimeError):
            self.verify(self.archive(), crypto_version="48.0.1")


if __name__ == "__main__":
    unittest.main()
