
from bs4 import BeautifulSoup
from pdfminer.high_level import extract_text
from io import BytesIO

def parse_html(content: bytes) -> str:
    soup = BeautifulSoup(content, "lxml")
    # Keep visible text; real impl would keep structure & headings
    return soup.get_text(separator="\n")

def parse_pdf(content: bytes) -> str:
    return extract_text(BytesIO(content))
