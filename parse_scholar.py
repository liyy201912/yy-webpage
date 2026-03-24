#!/usr/bin/env python3
"""Parse Yanyu Li's Google Scholar publications from JSON API response."""

import json
import re
import sys
from html import unescape
from urllib.request import urlopen, Request

def fetch_publications(cstart=0, pagesize=100):
    url = (
        "https://scholar.google.com/citations?user=XUj8koUAAAAJ&hl=en"
        f"&sortby=pubdate&cstart={cstart}&pagesize={pagesize}&json=1"
    )
    req = Request(url, headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"})
    with urlopen(req) as resp:
        data = json.load(resp)
    return data.get("B", "")

def parse_html(html_str):
    """Extract publication entries from the HTML table rows."""
    from html.parser import HTMLParser

    class ScholarParser(HTMLParser):
        def __init__(self):
            super().__init__()
            self.pubs = []
            self.current = {}
            self.in_title = False
            self.in_authors = False
            self.in_venue = False
            self.in_citations = False
            self.in_year = False
            self.gray_count = 0
            self.last_tag = None

        def handle_starttag(self, tag, attrs):
            attrs_d = dict(attrs)
            if tag == "tr" and "gsc_a_tr" in attrs_d.get("class", ""):
                self.current = {}
                self.gray_count = 0
            elif tag == "a" and "gsc_a_at" in attrs_d.get("class", ""):
                self.in_title = True
            elif tag == "a" and "gsc_a_ac" in attrs_d.get("class", ""):
                self.in_citations = True
                cite_href = attrs_d.get("href", "")
                if cite_href and "cites=" in cite_href:
                    # Extract citation count from link text if available
                    pass
            elif tag == "span" and "gsc_a_h" in attrs_d.get("class", ""):
                self.in_year = True
            self.last_tag = tag

        def handle_endtag(self, tag):
            if tag == "tr" and self.current:
                if self.current.get("title"):
                    self.pubs.append(self.current)
                self.current = {}
            elif tag == "a":
                self.in_title = False
                self.in_citations = False
            elif tag == "span":
                self.in_year = False
            elif tag == "div" and "gs_gray" in str(self.last_tag):
                pass

        def handle_data(self, data):
            data = data.strip()
            if not data:
                return
            if self.in_title:
                # Clean title - remove SVG/math artifacts
                clean = re.sub(r"E<svg[^>]*>.*?</svg>", "E²", data)
                clean = re.sub(r"&amp;", "&", clean)
                if clean and not clean.startswith("<"):
                    self.current["title"] = self.current.get("title", "") + unescape(clean)
            elif self.in_year:
                self.current["year"] = data
            elif self.in_citations and data.isdigit():
                self.current["citations"] = int(data)
            elif "gs_gray" in str(self.last_tag):
                # First gs_gray = authors, second = venue
                if "authors" not in self.current:
                    self.current["authors"] = unescape(data)
                elif "venue" not in self.current:
                    # Venue may contain year in span - extract venue part
                    venue = re.sub(r",\s*\d{4}\s*$", "", data)
                    self.current["venue"] = unescape(venue)
                else:
                    pass

    # Simpler regex-based extraction
    pubs = []
    row_pattern = re.compile(
        r'<tr class="gsc_a_tr">.*?<a[^>]*class="gsc_a_at"[^>]*>([^<]*(?:<[^>]+>[^<]*)*)</a>'
        r'.*?<div class="gs_gray">([^<]+)</div>'
        r'.*?<div class="gs_gray">([^<]+)(?:<[^>]+>)?([^<]*)</div>'
        r'.*?class="gsc_a_ac[^"]*"[^>]*>([^<]*)</a>'
        r'.*?<span class="gsc_a_h[^"]*"[^>]*>([^<]*)</span>',
        re.DOTALL
    )

    # Split by tr and parse each row
    rows = re.findall(r'<tr class="gsc_a_tr">(.*?)</tr>', html_str, re.DOTALL)
    for row in rows:
        pub = {}
        # Title - content between > and </a> for gsc_a_at link (non-greedy)
        m = re.search(r'<a[^>]*class="gsc_a_at"[^>]*>((?:(?!</a>).)*?)</a>', row, re.DOTALL)
        if m:
            title = m.group(1)
            title = re.sub(r'E<svg[^>]*>.*?</svg>', 'E²', title)
            title = unescape(re.sub(r'&amp;', '&', title))
            pub["title"] = title.strip()
        # Authors (first gs_gray div - only text, no nested tags)
        m = re.search(r'<div class="gs_gray">([^<]+)</div>', row)
        if m:
            pub["authors"] = unescape(m.group(1).strip())
        # Venue - second gs_gray div (strip span with year)
        gray_divs = re.findall(r'<div class="gs_gray">(.*?)</div>', row, re.DOTALL)
        if len(gray_divs) >= 2:
            venue = gray_divs[1]
            venue = re.sub(r'<span[^>]*>.*?</span>', '', venue)
            venue = re.sub(r',\s*\d{4}\s*$', '', venue.strip())
            venue = re.sub(r'\s+', ' ', venue)
            pub["venue"] = unescape(venue.strip()) if venue.strip() else "N/A"
        else:
            pub["venue"] = "N/A"
        # Citations
        m = re.search(r'class="gsc_a_ac[^"]*"[^>]*>([^<]*)</a>', row)
        if m:
            c = m.group(1).strip()
            pub["citations"] = int(c) if c.isdigit() else 0
        else:
            pub["citations"] = 0
        # Year
        m = re.search(r'<span class="gsc_a_h[^"]*"[^>]*>([^<]*)</span>', row)
        if m:
            pub["year"] = m.group(1).strip()
        else:
            pub["year"] = ""

        if pub.get("title"):
            pubs.append(pub)

    return pubs

def main():
    import os
    # Use saved file if available (avoids SSL issues)
    json_path = "/Users/yli16/.cursor/projects/Users-yli16-yy-webpage/agent-tools/03552cac-7615-4a18-85c1-68764605ec49.txt"
    if os.path.exists(json_path):
        with open(json_path) as f:
            data = json.load(f)
        html = data.get("B", "")
    else:
        html = fetch_publications(0, 100)
    pubs = parse_html(html)

    # Sort: 2024-2026 first, then 2022-2023, then others
    def sort_key(p):
        y = p.get("year", "")
        try:
            yi = int(y) if y else 0
        except ValueError:
            yi = 0
        if 2024 <= yi <= 2026:
            return (0, -yi)
        elif 2022 <= yi <= 2023:
            return (1, -yi)
        else:
            return (2, -yi)

    pubs.sort(key=sort_key)

    print("# Yanyu Li - Recent Publications (Google Scholar)")
    print("# Sorted by: 2024-2026 first, then 2022-2023, then others")
    print("# Profile: https://scholar.google.com/citations?user=XUj8koUAAAAJ")
    print()

    for i, p in enumerate(pubs[:40], 1):
        print(f"## {i}. {p.get('title', 'N/A')}")
        print(f"   **Authors:** {p.get('authors', 'N/A')}")
        print(f"   **Venue/Journal:** {p.get('venue', 'N/A')}")
        print(f"   **Year:** {p.get('year', 'N/A')}")
        print(f"   **Citations:** {p.get('citations', 0)}")
        print()

if __name__ == "__main__":
    main()
