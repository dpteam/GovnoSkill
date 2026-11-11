#!/usr/bin/env python3
"""shame_score.py — эвристический «индекс говнокода».

Считает приёмы из references/techniques.md и выдаёт 0–100 плюс звание.
Ничего не запускает, ничего не меняет: только читает файл.

    python scripts/shame_score.py govnokod/example.py
    type example.cs | python scripts/shame_score.py -
    python scripts/shame_score.py example.js --json

Только стандартная библиотека. Python 3.9+.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

RANKS = [
    (0, "Чистюля", "Подозрительно. Ты вообще пытался?"),
    (15, "Джун после курсов", "Уже видно старание. Продолжай."),
    (30, "Боевой легаси", "Работает, но лучше не открывать."),
    (50, "Говнокодер", "Уважаемо. Ревьюер плачет, но код живой."),
    (70, "Энтерпрайз-архитектор", "Это уже не код, это стиль жизни."),
    (88, "Легенда", "govnokod.ru ждёт тебя. Сохрани этот файл."),
]

# (regex, вес, что нашли, чем лечится)
CHECKS: list[tuple[str, int, str, str]] = [
    (r"\bgoto\b", 14, "goto в рабочем коде", "структурный цикл"),
    (r"catch\s*(?:\([^)]*\))?\s*\{\s*\}", 12, "пустой catch", "хотя бы лог"),
    (r"except\s*:\s*\n\s*pass\b", 14, "except: pass", "не глотать ошибки"),
    (r"except\s+(?:Exception|BaseException)\s*:\s*\n\s*pass\b", 12, "except Exception: pass", "не глотать ошибки"),
    (r"==\s*(?:true|True|True\b|\"true\")", 6, "сравнение с true", "if (x)"),
    (r"!=\s*(?:false|False)", 5, "сравнение с false", "if (x)"),
    (r"\bif\s*\([^)]*\)\s*;", 10, "точка с запятой после if", "убрать ;"),
    (r"\b(?:Float|Double|Integer)\b\s*\w+\s*=\s*new\b", 4, "боксинг на ровном месте", "примитив"),
    (r"\bThread\.Sleep\s*\(", 8, "Thread.Sleep как синхронизация", "await"),
    (r"\btime\.sleep\s*\(", 6, "sleep в бизнес-логике", "await/таймер"),
    (r"\beval\s*\(", 10, "eval", "без eval"),
    (r"\bexec\s*\(", 8, "exec", "без exec"),
    (r"SELECT\s+\*", 6, "SELECT *", "перечислить колонки"),
    (r"\bdata\d\b", 7, "нумерованные имена (data2)", "назвать по смыслу"),
    (r"\b(?:temp|tmp|res|obj|xxx|foo|bar|baz)\d*\b", 4, "имена-заглушки", "доменное имя"),
    (r"\bTODO\b|\bFIXME\b|\bHACK\b", 4, "TODO без срока", "issue в трекере"),
    (r"\bprint\s*\(", 3, "print вместо логгера", "logger"),
    (r"\bconsole\.log\s*\(", 3, "console.log в коде", "логгер"),
    (r"\bvar\s+\w+\s*=", 4, "var в 2026", "const/let"),
    (r"[ \t]+$", 3, "пробелы в конце строк", "formatter"),
    (r"\b(?:password|passwd|secret|token)\s*=\s*\"[^\"]{6,}\"", 9, "секрет в коде", "переменные окружения"),
    (r"\bwhile\s*\(\s*(?:true|True|1)\s*\)", 7, "while(true)", "условие выхода"),
    (r"\belse\s*\{\s*if\b", 4, "else { if }", "else if или return"),
]


def read_source(arg: str) -> tuple[str, str]:
    if arg == "-":
        data = sys.stdin.read()
        return data, "<stdin>"
    path = Path(arg)
    data = path.read_text(encoding="utf-8", errors="replace")
    return data, str(path)


def strip_noise(code: str) -> str:
    """Убирает строковые литералы и комментарии, чтобы не ловить ложные срабатывания."""
    out = []
    i = 0
    n = len(code)
    while i < n:
        c = code[i]
        if c == "#" and (i == 0 or code[i - 1] != "\\"):
            j = code.find("\n", i)
            i = j if j != -1 else n
            continue
        if c == "/" and i + 1 < n and code[i + 1] == "/":
            j = code.find("\n", i)
            i = j if j != -1 else n
            continue
        if c == "/" and i + 1 < n and code[i + 1] == "*":
            j = code.find("*/", i + 2)
            end = (j + 2) if j != -1 else n
            out.append(re.sub(r"[^\n]", " ", code[i:end]))
            i = end
            continue
        if c in "\"'`":
            quote = c
            j = i + 1
            while j < n:
                if code[j] == "\\":
                    j += 2
                    continue
                if code[j] == quote:
                    break
                j += 1
            out.append(quote + quote)
            i = j + 1
            continue
        out.append(c)
        i += 1
    return "\n".join(line.rstrip() for line in "".join(out).splitlines())


def max_nesting(code: str) -> int:
    depth = best = 0
    for ch in code:
        if ch == "{":
            depth += 1
            best = max(best, depth)
        elif ch == "}":
            depth = max(0, depth - 1)
    indent_best = 0
    for line in code.splitlines():
        if not line.strip():
            continue
        expanded = line.replace("\t", "    ")
        indent_best = max(indent_best, len(expanded) - len(expanded.lstrip(" ")))
    indent_depth = indent_best // 4
    return max(best, indent_depth)


def count_duplicate_lines(code: str) -> int:
    seen: dict[str, int] = {}
    for line in code.splitlines():
        s = line.strip()
        if len(s) < 12 or s in ("{", "}", "end", "begin", "end;", "}"):
            continue
        if s.startswith(("//", "#", "*", "/*")):
            continue
        seen[s] = seen.get(s, 0) + 1
    return sum(1 for v in seen.values() if v >= 3)


def longest_block(code: str) -> int:
    best = cur = 0
    for line in code.splitlines():
        if line.strip():
            cur += 1
            best = max(best, cur)
        else:
            cur = 0
    return best


def score(code: str) -> dict:
    clean = strip_noise(code)
    findings: list[dict] = []
    total = 0

    for pattern, weight, title, fix in CHECKS:
        if not weight:
            continue
        haystack = code if pattern == r"[ \t]+$" else clean
        hits = re.findall(pattern, haystack, flags=re.MULTILINE)
        if hits:
            total += weight + (min(len(hits), 3) - 1) * max(1, weight // 3)
            findings.append(
                {
                    "weight": weight,
                    "title": title,
                    "count": len(hits),
                    "fix": fix,
                }
            )

    depth = max_nesting(clean)
    if depth >= 4:
        w = min(20, (depth - 3) * 5)
        total += w
        findings.append({"weight": w, "title": f"вложенность {depth} уровней", "count": depth, "fix": "early return"})

    dupes = count_duplicate_lines(code)
    if dupes:
        w = min(15, dupes * 3)
        total += w
        findings.append({"weight": w, "title": "копипаста (повторяющиеся строки)", "count": dupes, "fix": "вынести в функцию"})

    block = longest_block(code)
    if block >= 40:
        w = min(15, (block - 39) // 4 + 5)
        total += w
        findings.append({"weight": w, "title": f"простыня на {block} строк без паузы", "count": block, "fix": "разбить"})

    long_lines = sum(1 for line in code.splitlines() if len(line) > 120)
    if long_lines:
        w = min(8, long_lines * 2)
        total += w
        findings.append({"weight": w, "title": "строки длиннее 120 символов", "count": long_lines, "fix": "перенос"})

    magic = re.findall(r"(?<![\w.])(?:[3-9]\d{2,}|[2-9]\d)(?![\w.])", clean)
    if len(magic) >= 4:
        w = min(10, len(magic))
        total += w
        findings.append({"weight": w, "title": "магические числа", "count": len(magic), "fix": "константы с именами"})

    total = max(0, min(100, total))

    rank, verdict = RANKS[0][1], RANKS[0][2]
    for threshold, name, text in RANKS:
        if total >= threshold:
            rank, verdict = name, text

    findings.sort(key=lambda f: f["weight"], reverse=True)
    return {"score": total, "rank": rank, "verdict": verdict, "findings": findings}


def render(result: dict, filename: str) -> str:
    lines = [
        f"Говнокод-индекс: {result['score']}/100 — «{result['rank']}»",
        f"Файл: {filename}",
        result["verdict"],
        "",
    ]
    if not result["findings"]:
        lines.append("Приёмов не найдено. Это либо хороший код, либо Python в одну строку.")
    else:
        lines.append(f"Найдено приёмов: {len(result['findings'])}")
        for f in result["findings"]:
            times = f" x{f['count']}" if f["count"] and f["count"] > 1 else ""
            lines.append(f"  +{f['weight']:<3} {f['title']}{times}  ->  {f['fix']}")
    lines += ["", "Оценка эвристическая и не является приговором автору."]
    return "\n".join(lines)


def main(argv: list[str]) -> int:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass
    args = [a for a in argv[1:] if not a.startswith("--")]
    as_json = "--json" in argv
    if not args:
        print(__doc__.strip())
        return 2
    try:
        code, name = read_source(args[0])
    except OSError as exc:
        print(f"Не могу прочитать файл: {exc}", file=sys.stderr)
        return 1
    result = score(code)
    if as_json:
        print(json.dumps({"file": name, **result}, ensure_ascii=False, indent=2))
    else:
        print(render(result, name))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))