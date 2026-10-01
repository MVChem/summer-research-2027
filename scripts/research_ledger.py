#!/usr/bin/env python3
"""Validate the additive research ledger and render its deterministic ranked view."""
import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
import re
import unicodedata
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "data/research/mentor_candidates.json"
RANKED = ROOT / "data/research/ranked_candidates.md"
CAPS = {"fit": 40, "physical": 25, "shortVisit": 20, "freshness": 15}
BASELINE_ALIASES = {"jasonjanghochoi", "yangruiboding", "robinding", "kiantebrantley", "tomaslozanoperez"}


def name_key(value):
    value = unicodedata.normalize("NFKD", value).casefold()
    return "".join(c for c in value if c.isalnum())


def url_key(value):
    url = urlsplit(value)
    assert url.scheme in {"http", "https"} and url.netloc, f"Invalid URL: {value}"
    assert not url.username and not url.password, "Credentials must not appear in URLs"
    return (url.netloc.removeprefix("www.") + url.path.rstrip("/")).casefold()



def identity_review_warnings(data):
    """Flag first/last-name matches for review; never merge identities automatically."""
    baseline = json.loads((ROOT / data["baseline"]["path"]).read_text())["contacts"]
    groups = {}
    for scope, rows in (("baseline", baseline), ("new", data["candidates"])):
        for row in rows:
            entity = (scope, str(row["id"]), row["name"])
            for name in (row["name"], *row.get("aliases", [])):
                folded = "".join(c for c in unicodedata.normalize("NFKD", name).casefold() if not unicodedata.combining(c))
                parts = re.findall(r"[^\W\d_]+", folded)
                if len(parts) >= 2:
                    groups.setdefault((parts[0], parts[-1]), set()).add(entity)
    return [
        {"nameKey": " ".join(key), "identities": sorted(entities)}
        for key, entities in sorted(groups.items())
        if len(entities) > 1 and any(entity[0] == "new" for entity in entities)
    ]


def timestamp(value):
    assert re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", value), f"Not UTC ISO 8601: {value}"
    result = datetime.fromisoformat(value.replace("Z", "+00:00"))
    assert result <= datetime.now(timezone.utc), f"Future research timestamp: {value}"
    return result


def validate(data):
    assert data["schemaVersion"] in {1, 2}
    assert data["rubricVersion"] == "fit40-physical25-shortVisit20-freshness15-v1"
    baseline = json.loads((ROOT / data["baseline"]["path"]).read_text())
    canonical = json.dumps(baseline, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode()
    assert hashlib.sha256(canonical).hexdigest() == data["baseline"]["canonicalJsonSha256"], "Original 200 changed"
    old = baseline["contacts"]
    assert len(old) == data["baseline"]["count"] == 200
    names = {name_key(row["name"]) for row in old} | BASELINE_ALIASES
    urls = {url_key(row["homepage"]) for row in old if row.get("homepage")}
    ids = set()
    required = {"id", "name", "aliases", "school", "homepage", "title", "batch", "discoveredAt", "verifiedAt", "researchAreas", "fitReason", "physicalEvidence", "shortVisit", "scores", "scoreReasons", "sources", "unknowns"}
    for row in data["candidates"]:
        assert required <= row.keys(), f"Missing fields for {row.get('name')}"
        assert row["id"] not in ids and re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", row["id"])
        ids.add(row["id"])
        keys = {name_key(n) for n in [row["name"], *row["aliases"]]}
        assert not keys & names, f"Duplicate or excluded identity: {row['name']}"
        names.update(keys)
        homepage = url_key(row["homepage"])
        assert homepage not in urls, f"Duplicate homepage: {row['name']}"
        urls.add(homepage)
        assert timestamp(row["discoveredAt"]) <= timestamp(row["verifiedAt"])
        if "discoveryTimestampNote" in row:
            assert isinstance(row["discoveryTimestampNote"], str) and row["discoveryTimestampNote"].strip(), "Discovery timestamp note must be nonempty text"
        if "candidateTier" in row:
            assert isinstance(row["candidateTier"], str) and row["candidateTier"].strip(), "Candidate tier must be nonempty text"
        if "appointmentTimingStatus" in row:
            assert isinstance(row["appointmentTimingStatus"], str) and row["appointmentTimingStatus"].strip(), "Appointment timing must be nonempty text"
            assert isinstance(row.get("appointmentTimingLabel"), str) and row["appointmentTimingLabel"].strip(), "Appointment timing requires a visible label"
        assert row["sources"] and row["unknowns"] and row["researchAreas"]
        source_ids = set()
        for source in row["sources"]:
            assert {"id", "label", "url", "summary", "verifiedAt"} <= source.keys()
            assert source["id"] not in source_ids and source["summary"]
            source_ids.add(source["id"])
            url_key(source["url"])
            assert timestamp(source["verifiedAt"]) <= timestamp(row["verifiedAt"])
        remote = row.get("remoteInquiryEvidence")
        if remote is not None:
            assert {"status", "summary", "sourceIds", "verifiedAt"} <= remote.keys()
            assert remote["status"] and remote["summary"]
            assert remote["sourceIds"] and set(remote["sourceIds"]) <= source_ids
            assert timestamp(remote["verifiedAt"]) <= timestamp(row["verifiedAt"])
        for attempt in row.get("verificationAttempts", []):
            assert {"attemptedAt", "sourceIds", "outcome"} <= attempt.keys()
            assert timestamp(row["discoveredAt"]) <= timestamp(attempt["attemptedAt"])
            assert attempt["sourceIds"] and set(attempt["sourceIds"]) <= source_ids
            assert isinstance(attempt["outcome"], str) and attempt["outcome"].strip()
            assert "verifiedAt" not in attempt, "A retrieval attempt is not a successful verification timestamp"
        for field in ("physicalEvidence", "shortVisit"):
            evidence = row[field]
            assert {"status", "summary", "sourceIds"} <= evidence.keys()
            assert evidence["summary"] and set(evidence["sourceIds"]) <= source_ids
        assert set(row["scores"]) == set(CAPS) == set(row["scoreReasons"])
        for field, cap in CAPS.items():
            score = row["scores"][field]
            assert isinstance(score, int) and not isinstance(score, bool) and 0 <= score <= cap
            assert isinstance(row["scoreReasons"][field], str) and row["scoreReasons"][field].strip()
        if row["physicalEvidence"]["status"] in {"simulation-only", "unverified", "no-verified-robot-deployment", "real-world-data-only; no robot deployment"}:
            assert row["scores"]["physical"] == 0, "Unverified or simulation-only robot evidence must score 0"
        status = row["shortVisit"]["status"].split(" · ", 1)[0]
        if status in {"unknown", "incompatible", "degree-only", "long-term-only", "precedent-only", "remote-only-inquiry", "stale-2022-inquiry; current route unverified"}:
            assert row["scores"]["shortVisit"] == 0, "Unknown/incompatible short-visit opportunity must score 0"



def validate_adjacent(adjacent, data):
    """Keep active adjacent leads disjoint and preserve discovery during migration."""
    baseline = json.loads((ROOT / data["baseline"]["path"]).read_text())["contacts"]
    main = {row["id"]: row for row in data["candidates"]}
    names = {name_key(n) for row in [*baseline, *main.values()] for n in [row["name"], *row.get("aliases", [])]}
    urls = {url_key(row["homepage"]) for row in [*baseline, *main.values()] if row.get("homepage")}
    for row in adjacent["candidates"]:
        keys = {name_key(n) for n in [row["fullName"], *row.get("aliases", [])]}
        assert not keys & names, "Adjacent lead duplicates an active identity"
        assert url_key(row["homepage"]) not in urls, "Adjacent lead duplicates an active homepage"
        assert row["includeInPrimaryRanking"] is False
        names.update(keys)
        urls.add(url_key(row["homepage"]))
    seen = set()
    for migration in adjacent.get("migratedRecords", []):
        target = migration["mainId"]
        assert target in main and target not in seen, "Unknown or duplicate migration target"
        seen.add(target)
        assert migration["discoveredAt"] == main[target]["discoveredAt"], "Migration changed discovery time"
        assert name_key(migration["name"]) in {name_key(n) for n in [main[target]["name"], *main[target]["aliases"]]}
        assert timestamp(migration["discoveredAt"]) <= timestamp(migration["migrationVerifiedAt"])


def validate_policy_references(data):
    """Ensure relative policy citations from detail pages reach explicit anchors."""
    policy = (ROOT / "data/research/eligibility_notes.md").read_text()
    anchors = set(re.findall(r'<a id="([^"]+)"', policy))
    for row in data["candidates"]:
        encoded = json.dumps(row, ensure_ascii=False)
        for anchor in re.findall(r"\]\(\.\./eligibility_notes\.md#([a-z0-9-]+)\)", encoded):
            assert anchor in anchors, f"Missing policy anchor {anchor}: {row['name']}"


def validate_addenda(addenda, baseline_meta):
    """Later observations must never become backfilled baseline discovery dates."""
    baseline = json.loads((ROOT / baseline_meta["path"]).read_text())["contacts"]
    by_id = {row["id"]: row for row in baseline}
    assert addenda["baselineCommit"] == baseline_meta["commit"]
    assert addenda["originalRecordsModified"] is False
    seen = set()
    for event in addenda["events"]:
        assert event["baselineId"] in by_id, "Unknown baseline identity"
        assert name_key(event["name"]) == name_key(by_id[event["baselineId"]]["name"])
        assert "discoveredAt" not in event, "Do not backfill baseline discovery dates"
        assert event["eventType"] == "later-public-source-verification-not-discovery"
        timestamp(event["observedAt"])
        identity = (event["baselineId"], event["observedAt"])
        assert identity not in seen, "Duplicate baseline observation"
        seen.add(identity)
        assert event["finding"] and event["sources"]
        for source in event["sources"]:
            url_key(source["url"])
            assert source["evidence"] and source["retrieval"]


def cell(value):
    return str(value).replace("|", "\\|").replace("\n", " ")


PRIORITY_LABELS = {
    0: "近期已到岗 AP（2024起）", 1: "暑期前明确拟到岗 AP", 2: "拟到岗/职级时点待核 AP",
    3: "其他 AP；入职年待核或较早", 4: "其他教师与研究导师", 5: "较长访问偏好；降低首联优先级",
    6: "明确至少三个月；降低首联优先级", 7: "当前明确暂停相关访问/暑期入口",
}


def priority_notes():
    path = LEDGER.parent / "priority_notes.json"
    return json.loads(path.read_text()) if path.exists() else {"appointments": {}, "constraints": []}


def is_assistant_professor(row):
    return bool(re.search(r"\bassistant professor\b", row["title"].split(";")[0], re.I))


def priority_tier(row, notes):
    constraints = [x for x in notes.get("constraints", []) if x.get("candidateId") == row["id"]]
    if any(x["kind"] in {"no-summer-interns", "no-visitors"} for x in constraints):
        return 7
    if any(x["kind"] == "minimum-duration" and x.get("months", 0) >= 3 for x in constraints):
        return 6
    if any(x["kind"] == "duration-preference" and x.get("months", 0) >= 3 for x in constraints):
        return 5
    if not is_assistant_professor(row):
        return 4
    start = notes.get("appointments", {}).get(row["id"], {}).get("appointmentStart", {})
    if start.get("status") == "current" and start.get("year", 0) >= 2024:
        return 0
    if start.get("status") == "incoming":
        year, month = start.get("year"), start.get("month")
        if year and (year < 2027 or (year == 2027 and month and month < 6)):
            return 1
        return 2
    if re.search(r"incoming|adjunct", row["title"], re.I):
        return 2
    return 3


def priority_key(row, notes):
    return (priority_tier(row, notes), -row["scores"]["fit"], -row["scores"]["physical"],
            -sum(row["scores"].values()), row["discoveredAt"], row["name"])


def ranked_rows(data):
    notes = priority_notes()
    if not notes.get("appointments"):
        return sorted(data["candidates"], key=lambda r: (-sum(r["scores"].values()), -r["scores"]["fit"], -r["scores"]["physical"], r["discoveredAt"], r["name"]))
    return sorted(data["candidates"], key=lambda row: priority_key(row, notes))


def validate_priority_notes(notes, data):
    assert notes["schemaVersion"] == 1
    rows = {row["id"]: row for row in data["candidates"]}
    baseline = {row["id"]: row for row in json.loads((ROOT / data["baseline"]["path"]).read_text())["contacts"]}
    for identity, entry in notes["appointments"].items():
        assert identity in rows and is_assistant_professor(rows[identity]), "Unknown or non-AP priority identity"
        assert entry["display"] and entry["sources"]
        for source in entry["sources"]:
            url_key(source["url"]); timestamp(source["observedAt"]); assert source["evidence"]
        source_ids = {source["id"] for source in entry["sources"]}
        assert len(source_ids) == len(entry["sources"]), "Duplicate appointment source ID"
        start = entry.get("appointmentStart", {})
        if start:
            assert start["sourceIds"] and set(start["sourceIds"]) <= source_ids, "Dangling appointment source reference"
            assert start["status"] in {"current", "incoming", "unresolved"}
            assert start["precision"] in {"year", "month", "day", "academic-year", "unknown"}
            if start["precision"] not in {"unknown"}:
                assert isinstance(start["year"], int) and 1900 <= start["year"] <= 2100
            if start["precision"] in {"month", "day"}: assert 1 <= start["month"] <= 12
            if start["precision"] == "day": assert 1 <= start["day"] <= 31
    seen = set()
    for entry in notes["constraints"]:
        assert entry["key"] not in seen; seen.add(entry["key"])
        assert entry["kind"] in {"minimum-duration", "duration-preference", "no-summer-interns", "no-visitors", "local-students-only", "capacity-or-role"}
        assert entry["scope"] and entry["summary"] and entry["sources"]
        assert sum(key in entry for key in ("candidateId", "baselineId", "catalogueIdentity")) == 1
        if "catalogueIdentity" in entry:
            target = entry["catalogueIdentity"]
            assert target["title"] and target["institution"]
            url_key(target["homepage"])
            assert name_key(entry["name"]) not in {name_key(r["name"]) for r in [*rows.values(), *baseline.values()]}, "Restriction-only identity already has a main record"
        else:
            target = rows[entry["candidateId"]] if "candidateId" in entry else baseline[entry["baselineId"]]
        assert name_key(entry["name"]) == name_key(target["name"])
        timestamp(entry["observedAt"])
        for source in entry["sources"]: url_key(source["url"]); assert source["evidence"]
        assert "discoveredAt" not in entry


def render_ap_priority(data, notes):
    rows = [r for r in ranked_rows(data) if is_assistant_professor(r)]
    lines = ["# 新进 Assistant Professor 优先看", "", "[全部候选：最新偏好排序](ranked_candidates.md) · [明确限制与暑期关闭](contact_constraints.md) · [访问问询入口](visitor_inquiries.md) · [评分说明](README.md)", "",
             f"当前新增记录中有 **{len(rows)} 位**以公开准确职级列出的 AP；这里只核实了一部分入职日期，日期未知不等于资历较老。", "",
             "约八周是初步参考，未说明时长不会被排除。先看近期已到岗 AP，再看暑期前有明确任职日期的 AP；其他 AP 仍保留。明确至少三个月及较长访问偏好降序，硬性最短时长与偏好分开；明确不接收暑期/访客优先标记。", "",
             "工作排序暂以 **2024年起**作为约近两三年的范围，并单列2027暑期前已公告入职者；这是可调整的整理约定，不是年龄判断、用户硬性年限或接收概率。各层内部先按研究匹配，再按真机证据及原总分。原四项分数和发现时间均未改写。", ""]
    for tier, label in PRIORITY_LABELS.items():
        subset = [r for r in rows if priority_tier(r, notes) == tier]
        if not subset: continue
        lines += [f"## {label}（{len(subset)}）", "", "| 导师 / 学校 | 准确任职与入职证据 | 原分数：匹配/真机/访问/新鲜 | 访问与时点提醒 |", "|---|---|---|---|"]
        for r in subset:
            entry = notes["appointments"].get(r["id"], {})
            sources = " ".join(f"[核查来源{i+1}]({x['url']})" for i,x in enumerate(entry.get("sources", [])))
            start = entry.get("display", "任职起始时间尚未单独核实")
            restrictions = [x["summary"] for x in notes["constraints"] if x.get("candidateId") == r["id"]]
            warning = "；".join(restrictions) or entry.get("caveat", "")
            evidence = physical_evidence_label(r)
            if evidence: warning += ("；" if warning else "") + evidence
            if not warning: warning = "时长、2027容量、经费与主办批准另核"
            scores = "/".join(str(r["scores"][k]) for k in CAPS)
            lines.append(f"| [{cell(r['name'])}](batches/{r['batch']}.md#{r['id']}) · {cell(r['school'])} | {cell(r['title'])}；**{cell(start)}** {sources} | {sum(r['scores'].values())}（{scores}） | **{cell(warning)}**；{cell(r['shortVisit']['status'])} |")
        lines.append("")
    lines += ["## 日期核查口径", "", "职级与研究来源见逐人详情；新的入职时间核查单独记录于 priority_notes.json，不把本次排序修改伪装成全套来源重查。日精度仅用于来源明确给出日的情况；新闻发布日期不自动等于入职日。", ""]
    for identity, entry in notes["appointments"].items():
        row = next(r for r in data["candidates"] if r["id"] == identity)
        for src in entry["sources"]:
            lines.append(f"- {cell(row['name'])}：[来源]({src['url']}) · {src['evidence']}（核查 {src['observedAt']}）")
    return "\n".join(lines) + "\n"


def render_contact_constraints(notes):
    labels = [("no-summer-interns", "明确不接收暑期实习"), ("no-visitors", "当前明确暂停相关访客入口"),
              ("minimum-duration", "明确最短时长"), ("duration-preference", "时长偏好或常态，不是硬性禁令"),
              ("local-students-only", "明确仅面向本校的研究入口"), ("capacity-or-role", "容量或任职提醒")]
    lines = ["# 访问与暑期限制 · 单独核对", "", "[新进 AP 优先看](ap_priority.md) · [全部候选](ranked_candidates.md) · [旧名单后续观察](baseline_addenda.md)", "",
             "这里只写已读取的明确限制，按对应人群和项目解释。未列出不代表开放；关闭学位招生不等于关闭访客。未注明时长也不代表可接受任何长度。约八周仅作初步参考，明确至少三个月或长期偏好会降低首联优先级。", "",
             "以下是来源观察时点的状态，不把未注明适用年份的措辞断言为永久禁令或专门的2027决定。旧200条只增加后续观察，不改原记录、不补造发现时间。", ""]
    for kind, heading in labels:
        entries = [x for x in notes["constraints"] if x["kind"] == kind]
        if not entries: continue
        lines += ["## " + heading, ""]
        for x in entries:
            origin = "原名单 #" + str(x["baselineId"]) if "baselineId" in x else ("限制目录；未计入新增排名" if "catalogueIdentity" in x else "新增候选")
            sources = " · ".join(f"[来源{i+1}]({s['url']})" for i,s in enumerate(x["sources"]))
            lines += [f"### {x['name']}（{origin}）", ""]
            if "catalogueIdentity" in x:
                identity = x["catalogueIdentity"]
                lines += [f"- 公开任职：{identity['title']} · {identity['institution']} · [主页]({identity['homepage']})"]
            lines += [f"- 适用范围：{x['scope']}", f"- **{x['summary']}**", f"- 核查：{x['observedAt']} · {sources}", ""]
    return "\n".join(lines) + "\n"


def render(data):
    rows = sorted(data["candidates"], key=lambda r: (-sum(r["scores"].values()), -r["scores"]["fit"], -r["scores"]["physical"], r["discoveredAt"], r["name"]))
    lines = ["# 新发现导师候选 · 排序", "", "[字段与评分说明](README.md) · [结构化记录](mentor_candidates.json)", "", f"新增 **{len(rows)} 位**；原有 200 位保持不变。时间均为 UTC。", "", "总分 = 研究匹配 40 + 真机证据 25 + 短访证据 20 + 信息新鲜度 15。分数是筛选优先级，不是录取概率；没有联系导师或发送邮件。", "", "| 排序 | 导师 / 学校 | 总分 | 匹配 / 真机 / 短访 / 新鲜 | 首次发现 UTC | 最后核查 UTC |", "|---:|---|---:|---|---|---|"]
    for index, row in enumerate(rows, 1):
        scores = " / ".join(str(row["scores"][key]) for key in CAPS)
        lines.append(f"| {index} | [{cell(row['name'])}]({row['homepage']}) · {cell(row['school'])} | {sum(row['scores'].values())} | {scores} | {row['discoveredAt']} | {row['verifiedAt']} |")
    if not rows:
        lines += ["", "等待首批完成来源核实的新增候选。"]
    for index, row in enumerate(rows, 1):
        lines += ["", f"## {index}. {row['name']} · {row['school']}", "", f"- 稳定键：`{row['id']}`；批次：{row['batch']}", f"- 任职：{row['title']}", f"- 方向：{'；'.join(row['researchAreas'])}", f"- 匹配理由：{row['fitReason']}", f"- 真机证据（{row['physicalEvidence']['status']}）：{row['physicalEvidence']['summary']}", f"- 短访证据（{row['shortVisit']['status']}）：{row['shortVisit']['summary']}", f"- 首次发现：{row['discoveredAt']}；最后核查：{row['verifiedAt']}", "- 评分依据："]
        for key in CAPS:
            lines.append(f"  - {key} {row['scores'][key]}/{CAPS[key]}：{row['scoreReasons'][key]}")
        lines.append("- 未确认事项：" + "；".join(row["unknowns"]))
        lines.append("- 来源：")
        for source in row["sources"]:
            lines.append(f"  - [{source['label']}]({source['url']})：{source['summary']}（核查 {source['verifiedAt']}）")
    return "\n".join(lines) + "\n"


def physical_evidence_label(row):
    """Expose limited evidence without re-scoring or inventing hardware access."""
    status = row["physicalEvidence"]["status"]
    if status == "embedded-perception-only; actuation-unverified":
        return "仅嵌入式感知；机器人执行未核"
    if status == "robot-collected-data; online-learned-deployment-unverified":
        return "机器人采集数据；在线学习部署未核实"
    if status == "AI相关 · 真机待核实":
        return status + ("（弱/历史线索）" if row["scores"]["physical"] else "")
    if row["scores"]["physical"] == 0:
        return "仅仿真；真机待核实" if status == "simulation-only" else "真机待核实"
    if row["scores"]["physical"] <= 12:
        return "弱/历史真机线索"
    if status != "public-hardware-evidence":
        return "受限真机证据：" + status
    return None


def compact_index(data, record_files):
    keys = ("id", "name", "aliases", "school", "title", "homepage", "batch", "discoveredAt", "verifiedAt", "scores", "researchAreas")
    rows = []
    for row in data["candidates"]:
        summary = {key: row[key] for key in keys}
        if row.get("discoveryTimestampNote"):
            summary["discoveryTimestampNote"] = row["discoveryTimestampNote"]
        if row.get("candidateTier"):
            summary["candidateTier"] = row["candidateTier"]
        if row.get("appointmentTimingStatus"):
            summary["appointmentTimingStatus"] = row["appointmentTimingStatus"]
            summary["appointmentTimingLabel"] = row["appointmentTimingLabel"]
        evidence_label = physical_evidence_label(row)
        if evidence_label:
            summary["physicalEvidenceStatus"] = row["physicalEvidence"]["status"]
            summary["physicalEvidenceLabel"] = evidence_label
        summary["shortVisitStatus"] = row["shortVisit"]["status"]
        summary["recordFile"] = f"batches/{row['batch']}.json"
        summary["detailPage"] = f"batches/{row['batch']}.md#{row['id']}"
        rows.append(summary)
    return {"schemaVersion": 2, "baseline": data["baseline"], "rubricVersion": data["rubricVersion"], "recordFiles": record_files, "candidates": rows}


def render_compact(data):
    lines = ["# 新发现导师候选 · 排序", "", "[新进 AP 优先看](ap_priority.md) · [明确限制与暑期关闭](contact_constraints.md) · [字段与评分说明](README.md) · [结构化索引](mentor_candidates.json) · [机构访问规则](eligibility_notes.md)", "", f"新增 **{len(data['candidates'])} 位**；原有 200 位保持不变。所有时间为 UTC。点击导师姓名查看完整证据、来源、评分理由和未确认事项。", "", "排序已按2026-10-01的新偏好调整：先看经核实近期入职的 AP；其他 AP、教授和明确长期条件分别排序。2024起是可调整的近两三年工作范围；约八周不再是硬筛选。各层先按研究匹配，再看真机及原总分。原总分 = 匹配40 + 真机25 + 短访20 + 新鲜度15，保留作证据对照，不是接收概率；未改原评分或发现时间。", "", "| 排序 | 导师 / 学校（完整资料） | 总分（四项） | 访问证据状态 | 首次发现 UTC | 最后核查 UTC |", "|---:|---|---|---|---|---|"]
    for index, row in enumerate(ranked_rows(data), 1):
        scores = "/".join(str(row["scores"][key]) for key in CAPS)
        detail = f"batches/{row['batch']}.md#{row['id']}"
        discovery = row["discoveredAt"] + (" †" if row.get("discoveryTimestampNote") else "")
        evidence_label = physical_evidence_label(row)
        evidence_note = f" · **{PRIORITY_LABELS[priority_tier(row, priority_notes())]}**"
        evidence_note += f" · **{cell(evidence_label)}**" if evidence_label else ""
        if row.get("appointmentTimingLabel"):
            evidence_note += f" · **{cell(row['appointmentTimingLabel'])}**"
        lines.append(f"| {index} | [{cell(row['name'])}]({detail}) · {cell(row['school'])}{evidence_note} | {sum(row['scores'].values())} ({scores}) | {cell(row['shortVisit']['status'])} | {discovery} | {row['verifiedAt']} |")
    if any(row.get("discoveryTimestampNote") for row in data["candidates"]):
        lines += ["", "† 时间口径例外：此条使用首次可精确保留的来源观察/核查记录时间，不能断言为最早遇到该线索的时刻。未重建更早时间；原值保持不变，具体限制见详情和索引的 discoveryTimestampNote。"]
    return "\n".join(lines) + "\n"


def render_batch(batch, rows):
    lines = [f"# 检索批次 {batch}", "", "[返回完整排序](../ranked_candidates.md) · [本批完整 JSON](" + batch + ".json) · [评分与字段](../README.md)", "", f"本批 **{len(rows)} 位**。首次发现时间保持不变；资料修正通过独立提交保留历史。分数是研究筛选优先级，不是接收概率。", ""]
    for row in sorted(rows, key=lambda r: (r["discoveredAt"], r["id"])):
        lines += [f'<a id="{row["id"]}"></a>', "", f"## {row['name']} · {row['school']}", "", f"- 稳定键：`{row['id']}`；[导师主页]({row['homepage']})", f"- 任职：{row['title']}", f"- 方向：{'；'.join(row['researchAreas'])}", f"- 匹配理由：{row['fitReason']}", f"- 真机证据（{row['physicalEvidence']['status']}）：{row['physicalEvidence']['summary']}", f"- 短访证据（{row['shortVisit']['status']}）：{row['shortVisit']['summary']}", f"- 首次发现：{row['discoveredAt']}；最后核查：{row['verifiedAt']}", f"- 当前总分：{sum(row['scores'].values())}/100；评分依据："]
        for key in CAPS:
            lines.append(f"  - {key} {row['scores'][key]}/{CAPS[key]}：{row['scoreReasons'][key]}")
        lines.append("- 未确认事项：" + "；".join(row["unknowns"]))
        lines.append("- 来源：")
        for source in row["sources"]:
            retrieval = f"；读取方式 {source['retrieval']}" if source.get("retrieval") else ""
            lines.append(f"  - [{source['label']}]({source['url']})：{source['summary']}（核查 {source['verifiedAt']}{retrieval}）")
        lines += [""]
    return "\n".join(lines) + "\n"


def inquiry_rows(data, notes=None):
    """Select evidence-bearing inquiries; never promote precedent-only rows."""
    generic_ids = {identity for identity, note in (notes or {}).get("notes", {}).items() if note.get("category") == "generic-intern-eligibility-unconfirmed"}
    rows = [r for r in data["candidates"] if r["scores"]["shortVisit"] > 0 or r["shortVisit"]["status"].startswith("remote-only-inquiry") or r.get("remoteInquiryEvidence") or r["id"] in generic_ids]
    return sorted(rows, key=lambda r: (-r["scores"]["fit"], -r["scores"]["physical"], -r["scores"]["shortVisit"], -r["scores"]["freshness"], r["discoveredAt"], r["name"]))


def validate_inquiry_notes(notes, data):
    by_id = {r["id"]: r for r in inquiry_rows(data, notes)}
    assert notes["schemaVersion"] == 1
    for identity, note in notes["notes"].items():
        assert identity in by_id, "Inquiry note must refer to a current inquiry row"
        assert isinstance(note["note"], str) and note["note"].strip()
        assert note["sourceIds"] and set(note["sourceIds"]) <= {s["id"] for s in by_id[identity]["sources"]}, "Inquiry note references unknown sources"
        assert note.get("category") in {None, "generic-intern-eligibility-unconfirmed"}
        if by_id[identity]["scores"]["shortVisit"] == 0 and note.get("category"):
            assert isinstance(note.get("inclusionRationale"), str) and note["inclusionRationale"].strip(), "Zero-score generic inquiries need a source-backed inclusion rationale"


def render_inquiries(data, notes):
    rows = inquiry_rows(data, notes)
    groups = {"onsite": [], "generic": [], "remote": []}
    for row in rows:
        if row["shortVisit"]["status"].startswith("remote-only-inquiry"):
            category = "remote"
        elif notes["notes"].get(row["id"], {}).get("category"):
            category = "generic"
        else:
            category = "onsite"
        groups[category].append(row)
    lines = ["# 明确访问问询入口 · 实用筛选", "", "[全部候选与总分排序](ranked_candidates.md) · [原始索引](mentor_candidates.json) · [机构规则](eligibility_notes.md) · [原200位后续补充](baseline_addenda.md)", "", f"从现有记录筛出 **{len(rows)} 条**有来源支持的访问/实习问询线索。这里只是联系入口，**没有已确认的2027约八周接收承诺**。没有发送邮件或提交表单。", "", "本页按研究匹配分优先，其次真机、短访、新鲜度及发现时间；不把一般询问、学校制度或个人自费能力当成已获资格。所有人的主办类别、八周安排、2027容量、经费和设备访问都需确认。具体奖学金要求、无资助、时间不匹配、任职时点及证据限制优先看下列加粗提示，再读完整资料。", ""]
    titles = {"onsite": "访问/短期研究问询线索（现场安排仍须确认）", "generic": "一般 intern 入口（外校硕士适用性未明确）", "remote": "仅远程入口（现场短访分为0）"}
    for category in ("onsite", "generic", "remote"):
        lines += [f"## {titles[category]} · {len(groups[category])} 条", "", "| 导师 / 机构 | 匹配 / 真机 / 短访 | 已知限制与证据状态 | 直接来源 / 机构规则 | 记录核查 UTC |", "|---|---|---|---|---|"]
        for row in groups[category]:
            note = notes["notes"].get(row["id"], {})
            status = note.get("note", row["shortVisit"]["status"])
            if status == "inquiry-only":
                status = "公开问询入口；详细资格与期限未定"
            evidence = physical_evidence_label(row)
            if evidence:
                status += "；" + evidence
            source_ids = note.get("sourceIds", row["shortVisit"]["sourceIds"])
            sources = {s["id"]: s for s in row["sources"]}
            links = " ".join(f"[{sid}]({sources[sid]['url']})" for sid in source_ids)
            anchors = sorted(set(re.findall(r"\]\(\.\./eligibility_notes\.md#([a-z0-9-]+)\)", json.dumps(row, ensure_ascii=False))))
            links += " " + " ".join(f"[规则](eligibility_notes.md#{a})" for a in anchors)
            detail = f"batches/{row['batch']}.md#{row['id']}"
            scores = "/".join(str(row["scores"][k]) for k in ("fit", "physical", "shortVisit"))
            lines.append(f"| [{cell(row['name'])}]({detail}) · {cell(row['school'])} | {scores} | **{cell(status)}** | {links.strip()} | {row['verifiedAt']} |")
        lines.append("")
    lines += ["本页只重组已经发布的证据，不新增核查时间，也不改变首次发现时间或分数。仅历史访客、本校学位岗位、一般机构资格且无导师询问入口的记录不会自动列入。精确来源核查时间、读取限制和首次时间请查看逐人详情；机构政策可能采用较早的独立核查。", ""]
    return "\n".join(lines)


def load_shards(index):
    files = sorted((ROOT / "data/research/batches").glob("*.json"))
    assert files, "No detailed batch records"
    data = {key: value for key, value in index.items() if key != "candidates"}
    data["candidates"] = []
    paths = []
    batches = {}
    for file in files:
        rows = json.loads(file.read_text())
        assert isinstance(rows, list) and rows, f"Empty or invalid batch: {file}"
        assert all(row["batch"] == file.stem for row in rows), f"Batch name mismatch: {file}"
        data["candidates"].extend(rows)
        batches[file.stem] = rows
        paths.append("batches/" + file.name)
    return data, paths, batches


def main():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--write", action="store_true")
    group.add_argument("--check", action="store_true")
    args = parser.parse_args()
    data = json.loads(LEDGER.read_text())
    addenda_path = LEDGER.parent / "baseline_addenda.json"
    if addenda_path.exists():
        validate_addenda(json.loads(addenda_path.read_text()), data["baseline"])
    if data["schemaVersion"] == 1:
        validate(data)
        outputs = {RANKED: render(data)}
    else:
        full, record_files, batches = load_shards(data)
        validate(full)
        validate_policy_references(full)
        expected_index = compact_index(full, record_files)
        outputs = {LEDGER: json.dumps(expected_index, ensure_ascii=False, indent=2) + "\n", RANKED: render_compact(full)}
        outputs.update({ROOT / f"data/research/batches/{batch}.md": render_batch(batch, rows) for batch, rows in batches.items()})
        data = full
    adjacent_path = LEDGER.parent / "adjacent_leads.json"
    if adjacent_path.exists():
        validate_adjacent(json.loads(adjacent_path.read_text()), data)
    inquiry_notes_path = LEDGER.parent / "visitor_inquiry_notes.json"
    if inquiry_notes_path.exists():
        inquiry_notes = json.loads(inquiry_notes_path.read_text())
        validate_inquiry_notes(inquiry_notes, data)
        outputs[LEDGER.parent / "visitor_inquiries.md"] = render_inquiries(data, inquiry_notes)
    priority_path = LEDGER.parent / "priority_notes.json"
    if priority_path.exists():
        notes = json.loads(priority_path.read_text())
        validate_priority_notes(notes, data)
        outputs[LEDGER.parent / "ap_priority.md"] = render_ap_priority(data, notes)
        outputs[LEDGER.parent / "contact_constraints.md"] = render_contact_constraints(notes)
    for path, expected in outputs.items():
        if args.write:
            path.write_text(expected)
        else:
            assert path.read_text() == expected, f"Generated file stale: {path}; run --write"
    for warning in identity_review_warnings(data):
        print("Manual identity review (not an automatic duplicate): " + json.dumps(warning, ensure_ascii=False))
    print(f"Research ledger valid: {len(data['candidates'])} new candidates; original 200 preserved")


if __name__ == "__main__":
    main()
