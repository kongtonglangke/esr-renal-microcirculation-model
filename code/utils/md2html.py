# -*- coding: utf-8 -*-
"""Minimal Markdown -> styled standalone HTML converter for this project."""
import html
import re
import sys
from pathlib import Path

CSS = """
:root{--fg:#1a1a1a;--muted:#5a6672;--line:#e2e6ea;--bg:#ffffff;--accent:#0b6bcb;
--warn:#b3261e;--ok:#0f7b3f;--soft:#f6f8fa;--soft2:#eef4fb;}
*{box-sizing:border-box;}
body{margin:0;padding:48px 24px 96px;background:var(--bg);color:var(--fg);
font:16px/1.75 "Segoe UI","Microsoft YaHei",system-ui,-apple-system,sans-serif;}
main{max-width:980px;margin:0 auto;}
h1{font-size:30px;line-height:1.3;margin:0 0 22px;padding-bottom:14px;
border-bottom:3px solid var(--accent);font-weight:700;}
h2{font-size:22px;margin:44px 0 14px;padding-left:12px;border-left:5px solid var(--accent);
font-weight:700;}
h3{font-size:18px;margin:30px 0 10px;color:#12304f;font-weight:700;}
p{margin:12px 0;}
strong{font-weight:700;color:#0d2b4b;}
code{background:var(--soft);padding:2px 6px;border-radius:4px;
font-family:"Cascadia Mono",Consolas,monospace;font-size:.9em;color:#a3320b;}
blockquote{margin:18px 0;padding:14px 18px;background:var(--soft2);
border-left:5px solid var(--accent);border-radius:0 8px 8px 0;color:#233c55;}
blockquote p{margin:6px 0;}
table{width:100%;border-collapse:collapse;margin:18px 0;font-size:14.5px;
box-shadow:0 1px 3px rgba(0,0,0,.07);border-radius:8px;overflow:hidden;}
th{background:#12304f;color:#fff;padding:10px 12px;text-align:left;font-weight:600;
border:1px solid #12304f;white-space:nowrap;}
td{padding:9px 12px;border:1px solid var(--line);vertical-align:top;}
tbody tr:nth-child(even){background:var(--soft);}
tbody tr:hover{background:#e8f1fb;}
ul,ol{margin:12px 0;padding-left:26px;}
li{margin:5px 0;}
hr{border:0;border-top:1px solid var(--line);margin:36px 0;}
em{color:var(--muted);font-style:normal;font-size:.94em;}
.toc{background:var(--soft);border:1px solid var(--line);border-radius:10px;
padding:16px 22px;margin:24px 0;}
.toc a{color:var(--accent);text-decoration:none;}
.toc a:hover{text-decoration:underline;}
"""


def inline(t: str) -> str:
    t = html.escape(t, quote=False)
    t = re.sub(r"`([^`]+)`", r"<code>\1</code>", t)
    t = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"(?<!\*)\*([^*\n]+)\*(?!\*)", r"<em>\1</em>", t)
    return t


def slug(s: str) -> str:
    s = re.sub(r"[^\w\u4e00-\u9fff]+", "-", s).strip("-")
    return s.lower() or "sec"


def convert(md: str) -> str:
    lines = md.split("\n")
    out, i = [], 0
    headings = []
    while i < len(lines):
        ln = lines[i].rstrip()
        if not ln.strip():
            i += 1
            continue
        # table
        if ln.lstrip().startswith("|") and i + 1 < len(lines) and \
           re.match(r"^\s*\|[\s:|-]+\|\s*$", lines[i + 1]):
            hdr = [c.strip() for c in ln.strip().strip("|").split("|")]
            i += 2
            rows = []
            while i < len(lines) and lines[i].lstrip().startswith("|"):
                rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
                i += 1
            out.append("<table><thead><tr>" +
                       "".join(f"<th>{inline(h)}</th>" for h in hdr) +
                       "</tr></thead><tbody>" +
                       "".join("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>"
                               for r in rows) +
                       "</tbody></table>")
            continue
        # heading
        m = re.match(r"^(#{1,4})\s+(.*)$", ln)
        if m:
            lvl, txt = len(m.group(1)), m.group(2)
            sid = slug(txt)
            if lvl <= 3:
                headings.append((lvl, txt, sid))
            out.append(f'<h{lvl} id="{sid}">{inline(txt)}</h{lvl}>')
            i += 1
            continue
        # hr
        if re.match(r"^-{3,}$", ln.strip()):
            out.append("<hr>")
            i += 1
            continue
        # blockquote
        if ln.lstrip().startswith(">"):
            buf = []
            while i < len(lines) and lines[i].lstrip().startswith(">"):
                buf.append(lines[i].lstrip()[1:].strip())
                i += 1
            out.append("<blockquote>" + "".join(f"<p>{inline(b)}</p>" for b in buf if b) +
                       "</blockquote>")
            continue
        # lists
        if re.match(r"^\s*[-*]\s+", ln):
            buf = []
            while i < len(lines) and re.match(r"^\s*[-*]\s+", lines[i]):
                buf.append(re.sub(r"^\s*[-*]\s+", "", lines[i]))
                i += 1
            out.append("<ul>" + "".join(f"<li>{inline(b)}</li>" for b in buf) + "</ul>")
            continue
        if re.match(r"^\s*\d+\.\s+", ln):
            buf = []
            while i < len(lines) and re.match(r"^\s*\d+\.\s+", lines[i]):
                buf.append(re.sub(r"^\s*\d+\.\s+", "", lines[i]))
                i += 1
            out.append("<ol>" + "".join(f"<li>{inline(b)}</li>" for b in buf) + "</ol>")
            continue
        # paragraph
        buf = [ln]
        i += 1
        while i < len(lines) and lines[i].strip() and \
                not re.match(r"^(#{1,4}\s|\s*[-*]\s|\s*\d+\.\s|>|\||-{3,}$)", lines[i]):
            buf.append(lines[i].rstrip())
            i += 1
        out.append("<p>" + inline(" ".join(buf)) + "</p>")

    toc_items = [f'<a href="#{s}">{inline(t)}</a>' for lvl, t, s in headings if lvl == 2]
    toc = ""
    if toc_items:
        toc = ('<nav class="toc"><strong>目录</strong><ul>' +
               "".join(f"<li>{x}</li>" for x in toc_items) + "</ul></nav>")
    body = "\n".join(out)
    if toc:
        idx = body.find("<h2")
        body = body[:idx] + toc + body[idx:]
    return body


def main():
    src, dst = Path(sys.argv[1]), Path(sys.argv[2])
    md = src.read_text(encoding="utf-8")
    title = md.split("\n")[0].lstrip("# ").strip()
    doc = ("<!DOCTYPE html>\n<html lang=\"zh-CN\">\n<head>\n<meta charset=\"utf-8\">\n"
           "<meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">\n"
           f"<title>{html.escape(title)}</title>\n<style>{CSS}</style>\n</head>\n"
           f"<body><main>\n{convert(md)}\n</main></body>\n</html>\n")
    dst.write_text(doc, encoding="utf-8")
    print(f"OK -> {dst}  ({len(doc)} bytes)")


if __name__ == "__main__":
    main()
