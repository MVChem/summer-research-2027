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

    def test_remote_only_invitation_cannot_score_as_onsite(self):
        data = copy.deepcopy(self.full)
        row = data["candidates"][0]
        row["shortVisit"]["status"] = "remote-only-inquiry · in-person route unverified"
        row["scores"]["shortVisit"] = 5
        with self.assertRaises(AssertionError):
            ledger.validate(data)

    def test_remote_inquiry_requires_known_source(self):
        data = copy.deepcopy(self.full)
        row = data["candidates"][0]
        row["remoteInquiryEvidence"] = {"status": "explicit-inquiry", "summary": "Remote research inquiry only", "sourceIds": ["missing-source"], "verifiedAt": row["verifiedAt"]}
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

    def test_middle_initial_match_warns_without_merging(self):
        data = copy.deepcopy(self.full)
        original = next(r for r in data["candidates"] if r["name"] == "Mark W. Mueller")
        variant = copy.deepcopy(original)
        variant.update(id="test-mark-mueller", name="Mark Mueller", aliases=[])
        data["candidates"].append(variant)
        before_count = len(data["candidates"])
        warnings = ledger.identity_review_warnings(data)
        self.assertTrue(any(w["nameKey"] == "mark mueller" for w in warnings))
        self.assertEqual(len(data["candidates"]), before_count)

    def test_alias_variants_of_one_identity_do_not_warn(self):
        data = copy.deepcopy(self.full)
        row = data["candidates"][0]
        data["candidates"] = [row]
        row["name"] = "Zebulon Q. Testname"
        row["aliases"] = ["Zebulon Testname", "Zebulon Q Testname"]
        self.assertEqual(ledger.identity_review_warnings(data), [])

    def test_shared_surname_alone_does_not_warn(self):
        data = copy.deepcopy(self.full)
        first = copy.deepcopy(data["candidates"][0])
        second = copy.deepcopy(first)
        first.update(id="test-one", name="Zebulon Testname", aliases=[])
        second.update(id="test-two", name="Zephyra Testname", aliases=[])
        data["candidates"] = [first, second]
        self.assertEqual(ledger.identity_review_warnings(data), [])

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

    def test_timestamp_qualification_survives_compact_index(self):
        data = copy.deepcopy(self.full)
        row = data["candidates"][0]
        row["discoveryTimestampNote"] = "First preserved source observation; earlier exact time unavailable."
        summary = ledger.compact_index(data, self.paths)["candidates"][0]
        self.assertEqual(summary["discoveryTimestampNote"], row["discoveryTimestampNote"])
        self.assertEqual(summary["discoveredAt"], row["discoveredAt"])

    def test_ranked_view_marks_qualified_timestamp_without_changing_it(self):
        data = copy.deepcopy(self.full)
        row = data["candidates"][0]
        row["discoveryTimestampNote"] = "First preserved source observation."
        text = ledger.render_compact(data)
        self.assertIn(row["discoveredAt"] + " †", text)
        self.assertIn("† 时间口径例外", text)

    def test_unqualified_timestamp_has_no_marker(self):
        data = copy.deepcopy(self.full)
        for row in data["candidates"]:
            row.pop("discoveryTimestampNote", None)
        self.assertNotIn("†", ledger.render_compact(data))
        self.assertTrue(all("discoveryTimestampNote" not in row for row in ledger.compact_index(data, self.paths)["candidates"]))

    def test_empty_timestamp_qualification_rejected(self):
        data = copy.deepcopy(self.full)
        data["candidates"][0]["discoveryTimestampNote"] = " "
        with self.assertRaises(AssertionError):
            ledger.validate(data)


if __name__ == "__main__":
    unittest.main()
