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
EXCLUDED = {"tianyizhou", "deviparikh"}
BASELINE_ALIASES = {"jasonjanghochoi", "yangruiboding", "robinding", "kiantebrantley", "tomaslozanoperez"}


def name_key(value):
    value = unicodedata.normalize("NFKD", value).casefold()
    return "".join(c for c in value if c.isalnum())


def url_key(value):
    url = urlsplit(value)
    assert url.scheme in {"http", "https"} and url.netloc, f"Invalid URL: {value}"
    assert not url.username and not url.password, "Credentials must not appear in URLs"
    return (url.netloc.removeprefix("www.") + url.path.rstrip("/")).casefold()


def timestamp(value):
    assert re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", value), f"Not UTC ISO 8601: {value}"
    result = datetime.fromisoformat(value.replace("Z", "+00:00"))
    assert result <= datetime.now(timezone.utc), f"Future research timestamp: {value}"
    return result


def validate(data):
    assert data["schemaVersion"] == 1
    assert data["rubricVersion"] == "fit40-physical25-shortVisit20-freshness15-v1"
    baseline = json.loads((ROOT / data["baseline"]["path"]).read_text())
    canonical = json.dumps(baseline, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode()
    assert hashlib.sha256(canonical).hexdigest() == data["baseline"]["canonicalJsonSha256"], "Original 200 changed"
    old = baseline["contacts"]
    assert len(old) == data["baseline"]["count"] == 200
    names = {name_key(row["name"]) for row in old} | BASELINE_ALIASES | EXCLUDED
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
        for field in ("physicalEvidence", "shortVisit"):
            evidence = row[field]
            assert {"status", "summary", "sourceIds"} <= evidence.keys()
            assert evidence["summary"] and set(evidence["sourceIds"]) <= source_ids
        assert set(row["scores"]) == set(CAPS) == set(row["scoreReasons"])
        for field, cap in CAPS.items():
            score = row["scores"][field]
            assert isinstance(score, int) and not isinstance(score, bool) and 0 <= score <= cap
            assert isinstance(row["scoreReasons"][field], str) and row["scoreReasons"][field].strip()
        if row["shortVisit"]["status"] in {"unknown", "incompatible", "degree-only", "long-term-only"}:
            assert row["scores"]["shortVisit"] == 0, "Unknown/incompatible short-visit opportunity must score 0"


def cell(value):
    return str(value).replace("|", "\\|").replace("\n", " ")


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


def main():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--write", action="store_true")
    group.add_argument("--check", action="store_true")
    args = parser.parse_args()
    data = json.loads(LEDGER.read_text())
    validate(data)
    expected = render(data)
    if args.write:
        RANKED.write_text(expected)
    else:
        assert RANKED.read_text() == expected, "Ranked view stale; run --write"
    print(f"Research ledger valid: {len(data['candidates'])} new candidates; original 200 preserved")


if __name__ == "__main__":
    main()
