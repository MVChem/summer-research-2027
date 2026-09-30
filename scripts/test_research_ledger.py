"""Standard-library regression checks for the additive, sharded research ledger."""
import copy
import json
import unittest

import research_ledger as ledger


class ResearchLedgerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.index = json.loads(ledger.LEDGER.read_text())
        cls.full, cls.paths, cls.batches = ledger.load_shards(cls.index)

    def test_full_records_and_compact_index_agree(self):
        ledger.validate(self.full)
        self.assertEqual(ledger.compact_index(self.full, self.paths), self.index)
        self.assertEqual(len(self.full["candidates"]), sum(map(len, self.batches.values())))

    def test_duplicate_identity_rejected(self):
        data = copy.deepcopy(self.full)
        duplicate = copy.deepcopy(data["candidates"][0])
        duplicate["id"] += "-duplicate"
        data["candidates"].append(duplicate)
        with self.assertRaises(AssertionError):
            ledger.validate(data)

    def test_unknown_opportunity_cannot_score(self):
        data = copy.deepcopy(self.full)
        data["candidates"][0]["shortVisit"]["status"] = "unknown"
        data["candidates"][0]["scores"]["shortVisit"] = 1
        with self.assertRaises(AssertionError):
            ledger.validate(data)

    def test_future_discovery_rejected(self):
        data = copy.deepcopy(self.full)
        data["candidates"][0]["discoveredAt"] = "2999-01-01T00:00:00Z"
        with self.assertRaises(AssertionError):
            ledger.validate(data)

    def test_unknown_source_reference_rejected(self):
        data = copy.deepcopy(self.full)
        data["candidates"][0]["physicalEvidence"]["sourceIds"].append("missing-source")
        with self.assertRaises(AssertionError):
            ledger.validate(data)

    def test_every_summary_links_to_its_full_record(self):
        full_by_id = {row["id"]: row for row in self.full["candidates"]}
        for summary in self.index["candidates"]:
            row = full_by_id[summary["id"]]
            self.assertEqual(summary["discoveredAt"], row["discoveredAt"])
            self.assertEqual(summary["verifiedAt"], row["verifiedAt"])
            path, anchor = summary["detailPage"].split("#")
            text = (ledger.LEDGER.parent / path).read_text()
            self.assertIn(f'<a id="{anchor}"></a>', text)
            self.assertIn(row["name"], text)
            self.assertTrue((ledger.LEDGER.parent / summary["recordFile"]).is_file())


if __name__ == "__main__":
    unittest.main()
