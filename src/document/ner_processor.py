"""
NER Processor - Named Entity Recognition for text extraction
"""
from typing import List, Dict, Any, Optional
from loguru import logger
import re


class NERProcessor:
    """Process text for Named Entity Recognition"""

    def __init__(self, use_spacy: bool = True):
        """
        Initialize NER processor

        Args:
            use_spacy: Whether to use spaCy for NER (requires spacy model installation)
        """
        self.use_spacy = use_spacy
        self.nlp = None

        if use_spacy:
            try:
                import spacy
                try:
                    self.nlp = spacy.load("en_core_web_sm")
                    logger.info("Loaded spaCy model: en_core_web_sm")
                except OSError:
                    logger.warning("spaCy model not found. Run: python -m spacy download en_core_web_sm")
                    self.use_spacy = False
            except ImportError:
                logger.warning("spaCy not installed. Using regex-based NER.")
                self.use_spacy = False

    def extract_entities(self, text: str) -> Dict[str, List[str]]:
        """
        Extract named entities from text

        Args:
            text: Input text

        Returns:
            Dictionary with entity types as keys and lists of entities as values
        """
        if self.use_spacy and self.nlp:
            return self._extract_with_spacy(text)
        else:
            return self._extract_with_regex(text)

    def _extract_with_spacy(self, text: str) -> Dict[str, List[str]]:
        """
        Extract entities using spaCy

        Args:
            text: Input text

        Returns:
            Dictionary of entities by type
        """
        doc = self.nlp(text)

        entities = {}
        for ent in doc.ents:
            entity_type = ent.label_
            entity_text = ent.text.strip()

            if entity_type not in entities:
                entities[entity_type] = []

            if entity_text not in entities[entity_type]:
                entities[entity_type].append(entity_text)

        logger.info(f"Extracted {sum(len(v) for v in entities.values())} entities using spaCy")
        return entities

    def _extract_with_regex(self, text: str) -> Dict[str, List[str]]:
        """
        Extract entities using regex patterns (fallback method)

        Args:
            text: Input text

        Returns:
            Dictionary of entities by type
        """
        entities = {
            "EMAIL": [],
            "PHONE": [],
            "URL": [],
            "DATE": [],
            "MONEY": [],
            "PERCENTAGE": []
        }

        # Email pattern
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        entities["EMAIL"] = list(set(re.findall(email_pattern, text)))

        # Phone pattern (US format)
        phone_pattern = r'\b(?:\+?1[-.]?)?\(?([0-9]{3})\)?[-.]?([0-9]{3})[-.]?([0-9]{4})\b'
        entities["PHONE"] = list(set(re.findall(phone_pattern, text)))
        entities["PHONE"] = ["-".join(match) if isinstance(match, tuple) else match for match in entities["PHONE"]]

        # URL pattern
        url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        entities["URL"] = list(set(re.findall(url_pattern, text)))

        # Date pattern (simple formats)
        date_pattern = r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b|\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{1,2},? \d{4}\b'
        entities["DATE"] = list(set(re.findall(date_pattern, text, re.IGNORECASE)))

        # Money pattern
        money_pattern = r'\$\s?\d+(?:,\d{3})*(?:\.\d{2})?'
        entities["MONEY"] = list(set(re.findall(money_pattern, text)))

        # Percentage pattern
        percentage_pattern = r'\b\d+(?:\.\d+)?%'
        entities["PERCENTAGE"] = list(set(re.findall(percentage_pattern, text)))

        # Remove empty lists
        entities = {k: v for k, v in entities.items() if v}

        logger.info(f"Extracted {sum(len(v) for v in entities.values())} entities using regex")
        return entities

    def extract_structured_data(self, text: str) -> Dict[str, Any]:
        """
        Extract structured data from text (entities + metadata)

        Args:
            text: Input text

        Returns:
            Dictionary with entities and metadata
        """
        entities = self.extract_entities(text)

        return {
            "entities": entities,
            "metadata": {
                "text_length": len(text),
                "word_count": len(text.split()),
                "entity_count": sum(len(v) for v in entities.values()),
                "entity_types": list(entities.keys())
            }
        }

    def highlight_entities(self, text: str, entity_type: Optional[str] = None) -> str:
        """
        Highlight entities in text with HTML markup

        Args:
            text: Input text
            entity_type: Optional specific entity type to highlight

        Returns:
            Text with HTML entity highlights
        """
        if not self.use_spacy or not self.nlp:
            return text

        doc = self.nlp(text)
        highlighted_text = text

        # Sort entities by position (reverse order to preserve indices)
        entities = sorted(doc.ents, key=lambda e: e.start_char, reverse=True)

        for ent in entities:
            if entity_type and ent.label_ != entity_type:
                continue

            # Add HTML markup
            highlighted = f'<mark data-entity="{ent.label_}">{ent.text}</mark>'
            highlighted_text = (
                highlighted_text[:ent.start_char] +
                highlighted +
                highlighted_text[ent.end_char:]
            )

        return highlighted_text

    def batch_process(self, texts: List[str]) -> List[Dict[str, Any]]:
        """
        Process multiple texts for NER

        Args:
            texts: List of text strings

        Returns:
            List of entity dictionaries
        """
        results = []

        for i, text in enumerate(texts):
            logger.info(f"Processing text {i + 1}/{len(texts)}")
            entities = self.extract_structured_data(text)
            results.append(entities)

        return results
