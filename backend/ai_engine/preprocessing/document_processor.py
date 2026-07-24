"""Text extraction boundary for every upload format accepted by the API."""
import csv, json, re, shutil, subprocess, tempfile, zipfile
from html import unescape
from pathlib import Path
from xml.etree import ElementTree as ET

class DocumentExtractionError(ValueError):
    """A user-correctable upload/extraction problem (returned as HTTP 422)."""

class DocumentProcessor:
    supported_extensions = {".pdf", ".doc", ".docx", ".ppt", ".pptx", ".txt", ".md", ".rtf", ".csv", ".xls", ".xlsx", ".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff", ".html", ".htm", ".xml", ".json", ".odt", ".odp", ".ods", ".epub"}
    def process(self, file_path):
        path, extension = Path(file_path), Path(file_path).suffix.lower()
        if extension not in self.supported_extensions:
            raise DocumentExtractionError(f"Unsupported file type '{extension or 'without an extension'}'.")
        if not path.exists():
            raise DocumentExtractionError("Uploaded file could not be found after saving.")
        try:
            pages = self._extract(path, extension)
        except DocumentExtractionError: raise
        except Exception as exc: raise DocumentExtractionError(f"Could not read '{path.name}': {exc}") from exc
        pages = [{"page_number": i + 1, "text": self._normalise(p.get("text", ""))} for i, p in enumerate(pages)]
        pages = [p for p in pages if p["text"]]
        text = "\n\n".join(p["text"] for p in pages)
        if not text: raise DocumentExtractionError("No readable text was found. Upload a text-based file or a clear, searchable scan.")
        return {"text": text, "pages": pages, "filename": path.name, "file_type": extension}
    def _extract(self, path, extension):
        if extension == ".pdf": return self._pdf(path)
        if extension == ".docx":
            from backend.ai_engine.preprocessing.docx_parser import DOCXParser
            return [{"text": p["text"]} for p in DOCXParser().extract(str(path))["page_data"]]
        if extension == ".pptx":
            from backend.ai_engine.preprocessing.ppt_parser import PPTParser
            return [{"text": p["text"]} for p in PPTParser().extract(str(path))["page_data"]]
        if extension in {".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff"}:
            from backend.ai_engine.preprocessing.ocr_parser import OCRParser
            return [{"text": p["text"]} for p in OCRParser().extract(str(path))["page_data"]]
        if extension in {".xlsx", ".xls"}: return self._spreadsheet(path)
        if extension in {".odt", ".odp", ".ods"}: return self._open_document(path)
        if extension == ".epub": return self._epub(path)
        if extension in {".doc", ".ppt"}: return self._convert_legacy_office(path)
        return [{"text": self._plain_text(path, extension)}]
    @staticmethod
    def _normalise(text): return re.sub(r"\n{3,}", "\n\n", str(text or "").replace("\x00", "")).strip()
    def _pdf(self, path):
        try: import pdfplumber
        except ImportError as exc: raise DocumentExtractionError("PDF support is not installed. Install backend requirements first.") from exc
        pages = []
        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                text = page.extract_text() or ""
                if not text.strip():
                    try:
                        from backend.ai_engine.preprocessing.ocr_parser import OCRParser
                        image = page.to_image(resolution=250).original
                        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as handle: image.save(handle.name); temp_name = handle.name
                        try: text = OCRParser().extract(temp_name)["text"]
                        finally: Path(temp_name).unlink(missing_ok=True)
                    except Exception as exc: raise DocumentExtractionError("This PDF is a scan and OCR could not read it. Upload a searchable PDF or clearer scan.") from exc
                pages.append({"text": text})
        return pages
    @staticmethod
    def _plain_text(path, extension):
        raw = path.read_text(encoding="utf-8", errors="replace")
        if extension == ".json":
            try: return json.dumps(json.loads(raw), indent=2, ensure_ascii=False)
            except json.JSONDecodeError: return raw
        if extension == ".csv": return "\n".join(" | ".join(row) for row in csv.reader(raw.splitlines()))
        if extension in {".html", ".htm"}: return unescape(re.sub(r"<[^>]+>", " ", raw))
        if extension == ".xml":
            try: return " ".join(ET.fromstring(raw).itertext())
            except ET.ParseError: return re.sub(r"<[^>]+>", " ", raw)
        if extension == ".rtf":
            return re.sub(r"\\[a-z]+-?\d* ?|[{}]", "", raw.replace(r"\par", "\n"))
        return raw
    @staticmethod
    def _xml_text(blob):
        root = ET.fromstring(blob)
        return "\n".join(" ".join(e.itertext()).strip() for e in root.iter() if e.tag.endswith("}p"))
    def _open_document(self, path):
        try:
            with zipfile.ZipFile(path) as archive: return [{"text": self._xml_text(archive.read("content.xml"))}]
        except (KeyError, zipfile.BadZipFile, ET.ParseError) as exc: raise DocumentExtractionError("The OpenDocument file is invalid or contains no readable content.") from exc
    def _epub(self, path):
        try:
            with zipfile.ZipFile(path) as archive:
                return [{"text": unescape(re.sub(r"<[^>]+>", " ", archive.read(name).decode("utf-8", "replace")))} for name in archive.namelist() if name.lower().endswith((".xhtml", ".html", ".htm"))]
        except zipfile.BadZipFile as exc: raise DocumentExtractionError("The EPUB file is invalid.") from exc
    @staticmethod
    def _spreadsheet(path):
        try:
            import pandas as pd
            sheets = pd.read_excel(path, sheet_name=None, header=None)
            return [{"text": f"Sheet: {name}\n" + frame.fillna("").astype(str).to_csv(index=False, header=False)} for name, frame in sheets.items()]
        except ImportError as exc: raise DocumentExtractionError("Spreadsheet support is not installed. Install pandas and openpyxl.") from exc
        except Exception as exc: raise DocumentExtractionError("Could not read spreadsheet. For legacy .xls files, install xlrd or upload .xlsx.") from exc
    def _convert_legacy_office(self, path):
        soffice = shutil.which("soffice") or shutil.which("libreoffice")
        if not soffice: raise DocumentExtractionError(f"Legacy '{path.suffix}' files require LibreOffice conversion. Please upload .docx or .pptx instead.")
        with tempfile.TemporaryDirectory() as output_dir:
            result = subprocess.run([soffice, "--headless", "--convert-to", "pdf", "--outdir", output_dir, str(path)], capture_output=True, text=True, timeout=90)
            converted = Path(output_dir) / f"{path.stem}.pdf"
            if result.returncode or not converted.exists(): raise DocumentExtractionError(f"Could not convert legacy Office file: {result.stderr.strip()}")
            return self._pdf(converted)
