"""
PDF Extractor - Extract text, tables, and metadata from PDF files
"""
import pdfplumber
import fitz  # PyMuPDF
from typing import List, Dict, Any, Optional
import pandas as pd
from loguru import logger
from pathlib import Path


class PDFExtractor:
    """Extract data from PDF documents"""

    def __init__(self):
        """Initialize PDF extractor"""
        logger.info("Initialized PDFExtractor")

    def extract_text(self, pdf_path: str, page_numbers: Optional[List[int]] = None) -> str:
        """
        Extract text from PDF

        Args:
            pdf_path: Path to PDF file
            page_numbers: Optional list of page numbers (0-indexed), or None for all pages

        Returns:
            Extracted text as string
        """
        try:
            text_content = []

            with pdfplumber.open(pdf_path) as pdf:
                pages = page_numbers if page_numbers else range(len(pdf.pages))

                for page_num in pages:
                    if page_num < len(pdf.pages):
                        page = pdf.pages[page_num]
                        text = page.extract_text()
                        if text:
                            text_content.append(f"--- Page {page_num + 1} ---\n{text}")

            full_text = "\n\n".join(text_content)
            logger.info(f"Extracted text from {len(text_content)} pages of {pdf_path}")
            return full_text

        except Exception as e:
            logger.error(f"Failed to extract text from PDF: {e}")
            raise

    def extract_tables(self, pdf_path: str, page_numbers: Optional[List[int]] = None) -> List[pd.DataFrame]:
        """
        Extract tables from PDF

        Args:
            pdf_path: Path to PDF file
            page_numbers: Optional list of page numbers, or None for all pages

        Returns:
            List of DataFrames, one per table found
        """
        try:
            all_tables = []

            with pdfplumber.open(pdf_path) as pdf:
                pages = page_numbers if page_numbers else range(len(pdf.pages))

                for page_num in pages:
                    if page_num < len(pdf.pages):
                        page = pdf.pages[page_num]
                        tables = page.extract_tables()

                        for table in tables:
                            if table and len(table) > 0:
                                # Convert to DataFrame
                                df = pd.DataFrame(table[1:], columns=table[0])
                                df.attrs['page'] = page_num + 1
                                all_tables.append(df)

            logger.info(f"Extracted {len(all_tables)} tables from {pdf_path}")
            return all_tables

        except Exception as e:
            logger.error(f"Failed to extract tables from PDF: {e}")
            raise

    def extract_metadata(self, pdf_path: str) -> Dict[str, Any]:
        """
        Extract metadata from PDF

        Args:
            pdf_path: Path to PDF file

        Returns:
            Dictionary with metadata
        """
        try:
            doc = fitz.open(pdf_path)

            metadata = {
                "page_count": len(doc),
                "file_path": pdf_path,
                "file_size_mb": Path(pdf_path).stat().st_size / (1024 * 1024),
                "pdf_version": doc.metadata.get("format", ""),
                "title": doc.metadata.get("title", ""),
                "author": doc.metadata.get("author", ""),
                "subject": doc.metadata.get("subject", ""),
                "creator": doc.metadata.get("creator", ""),
                "producer": doc.metadata.get("producer", ""),
                "creation_date": doc.metadata.get("creationDate", ""),
                "modification_date": doc.metadata.get("modDate", ""),
            }

            doc.close()

            logger.info(f"Extracted metadata from {pdf_path}")
            return metadata

        except Exception as e:
            logger.error(f"Failed to extract metadata from PDF: {e}")
            raise

    def extract_all(self, pdf_path: str) -> Dict[str, Any]:
        """
        Extract everything from PDF: text, tables, and metadata

        Args:
            pdf_path: Path to PDF file

        Returns:
            Dictionary with all extracted data
        """
        try:
            logger.info(f"Extracting all data from {pdf_path}")

            result = {
                "metadata": self.extract_metadata(pdf_path),
                "text": self.extract_text(pdf_path),
                "tables": self.extract_tables(pdf_path)
            }

            return result

        except Exception as e:
            logger.error(f"Failed to extract data from PDF: {e}")
            raise

    def search_text(self, pdf_path: str, search_term: str, case_sensitive: bool = False) -> List[Dict[str, Any]]:
        """
        Search for text in PDF and return matches with page numbers

        Args:
            pdf_path: Path to PDF file
            search_term: Text to search for
            case_sensitive: Whether search should be case sensitive

        Returns:
            List of matches with page numbers and context
        """
        try:
            matches = []

            with pdfplumber.open(pdf_path) as pdf:
                for page_num, page in enumerate(pdf.pages):
                    text = page.extract_text()
                    if not text:
                        continue

                    # Perform search
                    search_text = text if case_sensitive else text.lower()
                    search_pattern = search_term if case_sensitive else search_term.lower()

                    if search_pattern in search_text:
                        # Find all occurrences
                        lines = text.split('\n')
                        for line_num, line in enumerate(lines):
                            check_line = line if case_sensitive else line.lower()
                            if search_pattern in check_line:
                                matches.append({
                                    "page": page_num + 1,
                                    "line": line_num + 1,
                                    "context": line.strip()
                                })

            logger.info(f"Found {len(matches)} matches for '{search_term}' in {pdf_path}")
            return matches

        except Exception as e:
            logger.error(f"Failed to search PDF: {e}")
            raise

    def extract_images(self, pdf_path: str, output_dir: str = "data/extracted_images") -> List[str]:
        """
        Extract images from PDF

        Args:
            pdf_path: Path to PDF file
            output_dir: Directory to save extracted images

        Returns:
            List of paths to extracted images
        """
        try:
            import os
            os.makedirs(output_dir, exist_ok=True)

            doc = fitz.open(pdf_path)
            image_paths = []

            for page_num in range(len(doc)):
                page = doc[page_num]
                image_list = page.get_images()

                for img_index, img in enumerate(image_list):
                    xref = img[0]
                    base_image = doc.extract_image(xref)
                    image_bytes = base_image["image"]
                    image_ext = base_image["ext"]

                    image_filename = f"page{page_num + 1}_img{img_index + 1}.{image_ext}"
                    image_path = os.path.join(output_dir, image_filename)

                    with open(image_path, "wb") as img_file:
                        img_file.write(image_bytes)

                    image_paths.append(image_path)

            doc.close()

            logger.info(f"Extracted {len(image_paths)} images from {pdf_path}")
            return image_paths

        except Exception as e:
            logger.error(f"Failed to extract images from PDF: {e}")
            raise
