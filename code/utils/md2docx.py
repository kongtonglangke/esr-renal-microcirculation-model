#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
md2docx.py -- faithful Markdown -> Word (.docx) converter for the CHM submission.

Deliberately a FORMAT CONVERSION, not a regeneration: the manuscript text and
every number are passed through unchanged, because the numbers have been
verified against the model output and a generative re-write would put that at
risk.

Formatting follows the Sage/CHM author instructions:
  * wide margins, double spacing throughout
  * every page numbered
  * headings on their own line, not indented
  * SI units are handled in the source text
"""
import re
import sys
from pathlib import Path

from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

BASE_FONT = "Times New Roman"
MONO_FONT = "Consolas"
BODY_SIZE = Pt(12)


# --------------------------------------------------------------------------
def _set_page(doc):
    for s in doc.sections:
        s.top_margin = Cm(2.54); s.bottom_margin = Cm(2.54)
        s.left_margin = Cm(2.54); s.right_margin = Cm(2.54)
        s.page_width = Cm(21.0); s.page_height = Cm(29.7)


def _add_page_number(doc):
    for s in doc.sections:
        p = s.footer.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run()
        for instr in ("begin", "PAGE", "end"):
            el = OxmlElement("w:fldChar") if instr in ("begin", "end") else OxmlElement("w:instrText")
            if instr in ("begin", "end"):
                el.set(qn("w:fldCharType"), instr)
            else:
                el.set(qn("xml:space"), "preserve"); el.text = " PAGE "
            run._r.append(el)
        run.font.name = BASE_FONT; run.font.size = Pt(10)


def _style_base(doc):
    st = doc.styles["Normal"]
    st.font.name = BASE_FONT; st.font.size = BODY_SIZE
    st.element.rPr.rFonts.set(qn("w:eastAsia"), BASE_FONT)
    pf = st.paragraph_format
    pf.line_spacing_rule = WD_LINE_SPACING.DOUBLE
    pf.space_after = Pt(0)
    for name, size, before, after in (("Heading 1", 14, 12, 6), ("Heading 2", 12, 10, 4),
                                      ("Heading 3", 12, 8, 4), ("Heading 4", 12, 6, 2)):
        h = doc.styles[name]
        h.font.name = BASE_FONT; h.font.size = Pt(size); h.font.bold = True
        h.font.color.rgb = RGBColor(0, 0, 0)
        h.paragraph_format.space_before = Pt(before)
        h.paragraph_format.space_after = Pt(after)
        h.paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE
        h.paragraph_format.keep_with_next = True


INLINE = re.compile(r"(\*\*.+?\*\*|\*[^*]+?\*|`[^`]+?`|\^[0-9]+|_[^_]+_)")


def _runs(par, text):
    """inline **bold**, *italic*, `code`."""
    for tok in INLINE.split(text):
        if not tok:
            continue
        if tok.startswith("**") and tok.endswith("**") and len(tok) > 4:
            r = par.add_run(tok[2:-2]); r.bold = True
        elif tok.startswith("`") and tok.endswith("`") and len(tok) > 2:
            r = par.add_run(tok[1:-1]); r.font.name = MONO_FONT; r.font.size = Pt(10.5)
        elif tok.startswith("*") and tok.endswith("*") and len(tok) > 2:
            r = par.add_run(tok[1:-1]); r.italic = True
        else:
            par.add_run(tok)
        for r in par.runs:
            if r.font.name is None:
                r.font.name = BASE_FONT


def _add_table(doc, rows):
    ncol = max(len(r) for r in rows)
    t = doc.add_table(rows=0, cols=ncol)
    t.style = "Table Grid"
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, row in enumerate(rows):
        cells = t.add_row().cells
        for j in range(ncol):
            txt = row[j] if j < len(row) else ""
            p = cells[j].paragraphs[0]
            p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE
            p.paragraph_format.space_after = Pt(0)
            _runs(p, txt)
            for r in p.runs:
                r.font.size = Pt(10)
                if i == 0:
                    r.bold = True
    doc.add_paragraph()


def _split_row(line):
    line = line.strip()
    if line.startswith("|"):
        line = line[1:]
    if line.endswith("|"):
        line = line[:-1]
    return [c.strip() for c in line.split("|")]


def convert(md_path: Path, docx_path: Path):
    lines = md_path.read_text(encoding="utf-8").split("\n")
    doc = Document()
    _set_page(doc); _style_base(doc); _add_page_number(doc)

    i, n = 0, len(lines)
    while i < n:
        ln = lines[i]
        s = ln.strip()

        # ---- table block ----
        if s.startswith("|") and i + 1 < n and set(lines[i + 1].strip()) <= set("|-: "):
            rows = [_split_row(lines[i])]
            i += 2
            while i < n and lines[i].strip().startswith("|"):
                rows.append(_split_row(lines[i])); i += 1
            _add_table(doc, rows)
            continue

        # ---- indented code / equation block ----
        if ln.startswith("    ") and s:
            block = []
            while i < n and (lines[i].startswith("    ") or not lines[i].strip()):
                if lines[i].strip():
                    block.append(lines[i][4:])
                i += 1
            for b in block:
                p = doc.add_paragraph()
                p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE
                p.paragraph_format.space_after = Pt(0)
                p.paragraph_format.left_indent = Cm(0.75)
                r = p.add_run(b); r.font.name = MONO_FONT; r.font.size = Pt(10.5)
            doc.add_paragraph()
            continue

        # ---- headings ----
        m = re.match(r"^(#{1,6})\s+(.*)$", s)
        if m:
            lvl = min(len(m.group(1)), 4)
            p = doc.add_heading(level=lvl)
            _runs(p, m.group(2))
            for r in p.runs:
                r.bold = True
            i += 1
            continue

        # ---- horizontal rule ----
        if re.fullmatch(r"-{3,}", s):
            i += 1
            continue

        # ---- block quote ----
        if s.startswith(">"):
            p = doc.add_paragraph()
            p.paragraph_format.left_indent = Cm(0.8)
            _runs(p, s.lstrip("> ").strip())
            for r in p.runs:
                r.italic = True
            i += 1
            continue

        # ---- blank ----
        if not s:
            i += 1
            continue

        # ---- ordinary paragraph (join soft-wrapped lines) ----
        buf = [s]
        i += 1
        while i < n and lines[i].strip() and not re.match(r"^(#{1,6}\s|\||>\s|-\s|\*\s|\d+\.\s)", lines[i].strip()) \
                and not lines[i].startswith("    ") and not re.fullmatch(r"-{3,}", lines[i].strip()):
            buf.append(lines[i].strip()); i += 1
        p = doc.add_paragraph()
        _runs(p, " ".join(buf))

    docx_path.parent.mkdir(parents=True, exist_ok=True)
    doc.save(docx_path)
    print("OK ->", docx_path.name)


if __name__ == "__main__":
    src, dst = Path(sys.argv[1]), Path(sys.argv[2])
    convert(src, dst)
