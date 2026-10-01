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
        assert row["sources"] and row["unknowns"] and row["researchAreas"]
        source_ids = set()
        for source in row["sources"]:
            assert {"id", "label", "url", "summary", "verifiedAt"} <= source.keys()
            assert source["id"] not in source_ids and source["summary"]
            source_ids.add(source["id"])
            url_key(source["url"])
            assert timestamp(source["verifiedAt"]) <= timestamp(row["verifiedAt"])
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
        status = row["shortVisit"]["status"].split(" · ", 1)[0]
        if status in {"unknown", "incompatible", "degree-only", "long-term-only", "precedent-only", "stale-2022-inquiry; current route unverified"}:
            assert row["scores"]["shortVisit"] == 0, "Unknown/incompatible short-visit opportunity must score 0"



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


def ranked_rows(data):
    return sorted(data["candidates"], key=lambda r: (-sum(r["scores"].values()), -r["scores"]["fit"], -r["scores"]["physical"], r["discoveredAt"], r["name"]))


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


def compact_index(data, record_files):
    keys = ("id", "name", "aliases", "school", "title", "homepage", "batch", "discoveredAt", "verifiedAt", "scores", "researchAreas")
    rows = []
    for row in data["candidates"]:
        summary = {key: row[key] for key in keys}
        summary["shortVisitStatus"] = row["shortVisit"]["status"]
        summary["recordFile"] = f"batches/{row['batch']}.json"
        summary["detailPage"] = f"batches/{row['batch']}.md#{row['id']}"
        rows.append(summary)
    return {"schemaVersion": 2, "baseline": data["baseline"], "rubricVersion": data["rubricVersion"], "recordFiles": record_files, "candidates": rows}


def render_compact(data):
    lines = ["# 新发现导师候选 · 排序", "", "[字段与评分说明](README.md) · [结构化索引](mentor_candidates.json) · [机构访问规则](eligibility_notes.md)", "", f"新增 **{len(data['candidates'])} 位**；原有 200 位保持不变。所有时间为 UTC。点击导师姓名查看完整证据、来源、评分理由和未确认事项。", "", "总分 = 匹配 40 + 真机 25 + 短访 20 + 新鲜度 15。括号内为四项分数。研究优先级不是录取概率；没有联系导师或发送邮件。学校路径、一般询问入口与导师实际接收是不同事项。", "", "| 排序 | 导师 / 学校（完整资料） | 总分（四项） | 访问证据状态 | 首次发现 UTC | 最后核查 UTC |", "|---:|---|---|---|---|---|"]
    for index, row in enumerate(ranked_rows(data), 1):
        scores = "/".join(str(row["scores"][key]) for key in CAPS)
        detail = f"batches/{row['batch']}.md#{row['id']}"
        lines.append(f"| {index} | [{cell(row['name'])}]({detail}) · {cell(row['school'])} | {sum(row['scores'].values())} ({scores}) | {cell(row['shortVisit']['status'])} | {row['discoveredAt']} | {row['verifiedAt']} |")
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
