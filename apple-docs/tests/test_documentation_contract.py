import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from apis.authority import SOURCE_AUTHORITY


class DocumentationContractTests(unittest.TestCase):
    def test_authority_order_labels_secondary_sources(self):
        self.assertEqual("primary", SOURCE_AUTHORITY[0]["authority"])
        self.assertEqual("secondary", SOURCE_AUTHORITY[4]["authority"])
        self.assertEqual("community", SOURCE_AUTHORITY[5]["authority"])

    def test_cache_documentation_matches_in_process_implementation(self):
        cache_doc = (ROOT / "references/cache.md").read_text(encoding="utf-8")
        evolution = (ROOT / "scripts/apis/swift_evolution.py").read_text(encoding="utf-8")
        hig = (ROOT / "scripts/apis/hig.py").read_text(encoding="utf-8")
        local_docs = (ROOT / "scripts/apis/local_xcode_docs.py").read_text(encoding="utf-8")
        self.assertIn("no persistent disk cache", cache_doc)
        self.assertIn("in memory", cache_doc)
        self.assertIn("_cache", evolution)
        self.assertIn("_topic_index_cache", hig)
        self.assertIn("_documents", local_docs)


if __name__ == "__main__":
    unittest.main()
