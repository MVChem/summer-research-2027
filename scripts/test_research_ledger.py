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

    def test_adjacent_migrations_preserve_identity_and_discovery(self):
        adjacent = json.loads((ledger.LEDGER.parent / "adjacent_leads.json").read_text())
        ledger.validate_adjacent(adjacent, self.full)

    def test_adjacent_cannot_duplicate_main(self):
        row = self.full["candidates"][0]
        adjacent = {"candidates": [{"fullName": row["name"], "aliases": [], "homepage": row["homepage"], "includeInPrimaryRanking": False}]}
        with self.assertRaises(AssertionError):
            ledger.validate_adjacent(adjacent, self.full)

    def test_migration_cannot_change_discovery(self):
        row = self.full["candidates"][0]
        adjacent = {"candidates": [], "migratedRecords": [{"mainId": row["id"], "name": row["name"], "discoveredAt": "2020-01-01T00:00:00Z", "migrationVerifiedAt": row["verifiedAt"]}]}
        with self.assertRaises(AssertionError):
            ledger.validate_adjacent(adjacent, self.full)

    def test_migration_requires_existing_target(self):
        adjacent = {"candidates": [], "migratedRecords": [{"mainId": "missing-identity"}]}
        with self.assertRaises(AssertionError):
            ledger.validate_adjacent(adjacent, self.full)

    def test_appointment_timing_reaches_index_and_ranking(self):
        data = copy.deepcopy(self.full)
        row = data["candidates"][0]
        row["appointmentTimingStatus"] = "Incoming 2027; exact month unknown"
        row["appointmentTimingLabel"] = "2027待入职；夏季主办权限未定"
        summary = ledger.compact_index(data, self.paths)["candidates"][0]
        self.assertEqual(summary["appointmentTimingStatus"], row["appointmentTimingStatus"])
        self.assertIn(row["appointmentTimingLabel"], ledger.render_compact(data))

    def test_appointment_timing_requires_visible_label(self):
        data = copy.deepcopy(self.full)
        row = data["candidates"][0]
        row["appointmentTimingStatus"] = "Incoming 2027"
        row.pop("appointmentTimingLabel", None)
        with self.assertRaises(AssertionError):
            ledger.validate(data)

    def test_inquiry_view_excludes_unknown_and_precedent_only(self):
        data = copy.deepcopy(self.full)
        row = data["candidates"][0]
        row["scores"]["shortVisit"] = 0
        row["shortVisit"]["status"] = "precedent-only"
        row.pop("remoteInquiryEvidence", None)
        self.assertNotIn(row["id"], {r["id"] for r in ledger.inquiry_rows(data)})

    def test_inquiry_view_keeps_remote_separate(self):
        data = copy.deepcopy(self.full)
        row = data["candidates"][0]
        row["scores"]["shortVisit"] = 0
        row["shortVisit"]["status"] = "remote-only-inquiry"
        rendered = ledger.render_inquiries(data, {"schemaVersion": 1, "notes": {}})
        remote_section = rendered.split("## 仅远程入口", 1)[1]
        self.assertIn(row["name"], remote_section)
        self.assertNotIn(row["name"], rendered.split("## 仅远程入口", 1)[0])

    def test_inquiry_view_orders_fit_first(self):
        rows = ledger.inquiry_rows(self.full)
        self.assertEqual([r["scores"]["fit"] for r in rows], sorted((r["scores"]["fit"] for r in rows), reverse=True))

    def test_zero_score_generic_inquiry_is_separate_without_rescoring(self):
        data = copy.deepcopy(self.full)
        row = data["candidates"][0]
        row["scores"]["shortVisit"] = 0
        row["shortVisit"]["status"] = "unknown"
        row.pop("remoteInquiryEvidence", None)
        notes = {"schemaVersion": 1, "notes": {row["id"]: {"note": "Generic intern inquiry; external eligibility unknown", "category": "generic-intern-eligibility-unconfirmed", "inclusionRationale": "Primary homepage explicitly invites intern inquiries", "sourceIds": [row["sources"][0]["id"]]}}}
        ledger.validate_inquiry_notes(notes, data)
        rendered = ledger.render_inquiries(data, notes)
        self.assertIn(row["name"], rendered.split("## 一般 intern 入口", 1)[1].split("## 仅远程入口", 1)[0])
        self.assertNotIn(row["name"], rendered.split("## 一般 intern 入口", 1)[0])
        self.assertEqual(row["scores"]["shortVisit"], 0)

    def test_inquiry_annotations_require_source_references(self):
        row = ledger.inquiry_rows(self.full)[0]
        notes = {"schemaVersion": 1, "notes": {row["id"]: {"note": "A limitation", "sourceIds": ["missing"]}}}
        with self.assertRaises(AssertionError):
            ledger.validate_inquiry_notes(notes, self.full)

    def test_inquiry_view_keeps_record_dates_and_scores(self):
        original = copy.deepcopy(self.full)
        notes = json.loads((ledger.LEDGER.parent / "visitor_inquiry_notes.json").read_text())
        ledger.validate_inquiry_notes(notes, self.full)
        self.assertIn("一般 intern 入口", ledger.render_inquiries(self.full, notes))
        self.assertEqual(original, self.full)

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

    def test_unverified_physical_evidence_is_visible(self):
        data = copy.deepcopy(self.full)
        row = data["candidates"][0]
        row["physicalEvidence"]["status"] = "unverified"
        row["scores"]["physical"] = 0
        summary = ledger.compact_index(data, self.paths)["candidates"][0]
        self.assertEqual(summary["physicalEvidenceStatus"], "unverified")
        self.assertEqual(summary["physicalEvidenceLabel"], "真机待核实")
        self.assertIn("**真机待核实**", ledger.render_compact(data))
        self.assertEqual(row["scores"]["physical"], 0)

    def test_simulation_only_label_is_explicit(self):
        row = copy.deepcopy(self.full["candidates"][0])
        row["physicalEvidence"]["status"] = "simulation-only"
        row["scores"]["physical"] = 0
        self.assertEqual(ledger.physical_evidence_label(row), "仅仿真；真机待核实")

    def test_weak_historical_evidence_is_not_promoted(self):
        row = copy.deepcopy(self.full["candidates"][0])
        row["physicalEvidence"]["status"] = "historical-or-indirect"
        row["scores"]["physical"] = 10
        self.assertEqual(ledger.physical_evidence_label(row), "弱/历史真机线索")
        self.assertEqual(row["scores"]["physical"], 10)

    def test_embedded_perception_does_not_imply_actuation(self):
        row = copy.deepcopy(self.full["candidates"][0])
        row["physicalEvidence"]["status"] = "embedded-perception-only; actuation-unverified"
        row["scores"]["physical"] = 10
        self.assertEqual(ledger.physical_evidence_label(row), "仅嵌入式感知；机器人执行未核")
        self.assertEqual(row["scores"]["physical"], 10)

    def test_verified_hardware_has_no_backup_label(self):
        row = copy.deepcopy(self.full["candidates"][0])
        row["physicalEvidence"]["status"] = "public-hardware-evidence"
        row["scores"]["physical"] = 25
        self.assertIsNone(ledger.physical_evidence_label(row))

    def test_simulation_cannot_receive_physical_points(self):
        data = copy.deepcopy(self.full)
        row = data["candidates"][0]
        row["physicalEvidence"]["status"] = "simulation-only"
        row["scores"]["physical"] = 10
        with self.assertRaises(AssertionError):
            ledger.validate(data)

    def test_explicit_visitor_backup_tier_is_preserved(self):
        data = copy.deepcopy(self.full)
        row = data["candidates"][0]
        row["candidateTier"] = "Robotics-AI visitor backup; current learned hardware unverified"
        row["physicalEvidence"]["status"] = "AI相关 · 真机待核实"
        row["scores"]["physical"] = 12
        summary = ledger.compact_index(data, self.paths)["candidates"][0]
        self.assertEqual(summary["candidateTier"], row["candidateTier"])
        self.assertEqual(summary["physicalEvidenceLabel"], "AI相关 · 真机待核实（弱/历史线索）")
        self.assertIn("AI相关 · 真机待核实（弱/历史线索）", ledger.render_compact(data))
        self.assertEqual(row["scores"]["physical"], 12)


    def test_priority_overlay_preserves_all_records_and_scores(self):
        notes = ledger.priority_notes()
        ledger.validate_priority_notes(notes, self.full)
        before = copy.deepcopy(self.full)
        rows = ledger.ranked_rows(self.full)
        self.assertEqual({r['id'] for r in rows}, {r['id'] for r in self.full['candidates']})
        self.assertEqual(self.full, before)

    def test_unknown_ap_start_is_not_recent(self):
        row = copy.deepcopy(self.full['candidates'][0])
        row['title'] = 'Assistant Professor'
        self.assertEqual(ledger.priority_tier(row, {'appointments':{}, 'constraints':[]}), 3)

    def test_explicit_closed_route_overrides_new_ap_status(self):
        row = copy.deepcopy(self.full['candidates'][0]); row['title'] = 'Assistant Professor'
        notes = {'appointments':{row['id']:{'appointmentStart':{'year':2026,'status':'current'}}},
                 'constraints':[{'candidateId':row['id'],'kind':'no-summer-interns'}]}
        self.assertEqual(ledger.priority_tier(row, notes), 7)

    def test_preference_is_not_minimum_or_closure(self):
        row = next(r for r in self.full['candidates'] if r['id'] == 'dhruv-shah')
        self.assertEqual(ledger.priority_tier(row, ledger.priority_notes()), 5)
        self.assertEqual(row['scores']['shortVisit'], 10)
        text = ledger.render_contact_constraints(ledger.priority_notes())
        self.assertIn('时长偏好或常态，不是硬性禁令', text)

    def test_incoming_year_without_month_is_not_before_summer(self):
        row = copy.deepcopy(self.full['candidates'][0]); row['title'] = 'Incoming Assistant Professor'
        notes = {'appointments':{row['id']:{'appointmentStart':{'year':2027,'status':'incoming'}}}, 'constraints':[]}
        self.assertEqual(ledger.priority_tier(row, notes), 2)
        notes['appointments'][row['id']]['appointmentStart']['month'] = 1
        self.assertEqual(ledger.priority_tier(row, notes), 1)

    def test_priority_notes_reject_unknown_identity(self):
        notes = copy.deepcopy(ledger.priority_notes())
        notes['appointments']['not-a-record'] = next(iter(notes['appointments'].values()))
        with self.assertRaises(AssertionError): ledger.validate_priority_notes(notes, self.full)


    def test_appointment_sources_cannot_dangle(self):
        notes = copy.deepcopy(ledger.priority_notes())
        entry = notes['appointments']['tom-silver']
        entry['appointmentStart']['sourceIds'] = ['missing']
        with self.assertRaises(AssertionError): ledger.validate_priority_notes(notes, self.full)


    def test_restriction_catalogue_is_not_a_candidate_count(self):
        notes = ledger.priority_notes()
        ledger.validate_priority_notes(notes, self.full)
        text = ledger.render_contact_constraints(notes)
        self.assertIn('Simon B. Stepputtis', text)
        self.assertIn('限制目录；未计入新增排名', text)
        self.assertNotIn('simon-b-stepputtis', {r['id'] for r in self.full['candidates']})


    def test_recent_move_is_not_first_career_ap_tier(self):
        row = copy.deepcopy(self.full['candidates'][0]); row['title'] = 'Assistant Professor'
        notes = {'appointments':{row['id']:{'appointmentStart':{'year':2024,'status':'current','appointmentType':'institution-move'}}}, 'constraints':[]}
        self.assertEqual(ledger.priority_tier(row, notes), 3)

    def test_conflicting_date_range_retains_bounds(self):
        notes = copy.deepcopy(ledger.priority_notes())
        start = notes['appointments']['tom-silver']['appointmentStart']
        start.update({'year':2025,'endYear':2026,'precision':'range'})
        ledger.validate_priority_notes(notes, self.full)
        start['endYear'] = 2024
        with self.assertRaises(AssertionError): ledger.validate_priority_notes(notes, self.full)


if __name__ == "__main__":
    unittest.main()
