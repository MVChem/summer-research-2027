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

    def test_qualified_unknown_opportunity_cannot_score(self):
        data = copy.deepcopy(self.full)
        data["candidates"][0]["shortVisit"]["status"] = "unknown · future host unconfirmed"
        data["candidates"][0]["scores"]["shortVisit"] = 1
        with self.assertRaises(AssertionError):
            ledger.validate(data)

    def test_baseline_addenda_are_later_observations(self):
        addenda = json.loads((ledger.LEDGER.parent / "baseline_addenda.json").read_text())
        ledger.validate_addenda(addenda, self.index["baseline"])

    def test_baseline_addenda_cannot_backfill_discovery(self):
        addenda = json.loads((ledger.LEDGER.parent / "baseline_addenda.json").read_text())
        addenda["events"][0]["discoveredAt"] = addenda["events"][0]["observedAt"]
        with self.assertRaises(AssertionError):
            ledger.validate_addenda(addenda, self.index["baseline"])

    def test_baseline_addenda_require_known_identity(self):
        addenda = json.loads((ledger.LEDGER.parent / "baseline_addenda.json").read_text())
        addenda["events"][0]["baselineId"] = 999999
        with self.assertRaises(AssertionError):
            ledger.validate_addenda(addenda, self.index["baseline"])

    def test_baseline_addenda_cannot_claim_modified_records(self):
        addenda = json.loads((ledger.LEDGER.parent / "baseline_addenda.json").read_text())
        addenda["originalRecordsModified"] = True
        with self.assertRaises(AssertionError):
            ledger.validate_addenda(addenda, self.index["baseline"])

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

    def test_existing_policy_references_resolve(self):
        ledger.validate_policy_references(self.full)

    def test_unknown_policy_anchor_rejected(self):
        data = copy.deepcopy(self.full)
        data["candidates"][0]["unknowns"].append("[Policy](../eligibility_notes.md#missing-test-policy)")
        with self.assertRaises(AssertionError):
            ledger.validate_policy_references(data)

    def test_future_retrieval_attempt_rejected(self):
        data = copy.deepcopy(self.full)
        row = data["candidates"][0]
        row["verificationAttempts"] = [{"attemptedAt": "2999-01-01T00:00:00Z", "sourceIds": [row["sources"][0]["id"]], "outcome": "live-retrieval-failed"}]
        with self.assertRaises(AssertionError):
            ledger.validate(data)

    def test_retrieval_attempt_cannot_claim_verification(self):
        data = copy.deepcopy(self.full)
        row = data["candidates"][0]
        row["verificationAttempts"] = [{"attemptedAt": row["verifiedAt"], "verifiedAt": row["verifiedAt"], "sourceIds": [row["sources"][0]["id"]], "outcome": "live-retrieval-failed"}]
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
