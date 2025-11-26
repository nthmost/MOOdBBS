"""Zipcode validation service."""

import re
from typing import Optional, Tuple


class ZipcodeValidator:
    """Validate postal codes for various countries."""

    # US zipcode patterns
    US_ZIP5 = re.compile(r'^\d{5}$')
    US_ZIP9 = re.compile(r'^\d{5}-\d{4}$')

    # Canadian postal code (A1A 1A1)
    CA_POSTAL = re.compile(r'^[A-Z]\d[A-Z]\s?\d[A-Z]\d$', re.IGNORECASE)

    # UK postal code (simplified - covers most formats)
    UK_POSTAL = re.compile(r'^[A-Z]{1,2}\d{1,2}[A-Z]?\s?\d[A-Z]{2}$', re.IGNORECASE)

    def validate(self, zipcode: str) -> Tuple[bool, Optional[str]]:
        """Validate a zipcode/postal code.

        Args:
            zipcode: The zipcode to validate

        Returns:
            Tuple of (is_valid, error_message)
        """
        if not zipcode or not zipcode.strip():
            return False, "Zipcode cannot be empty"

        zipcode = zipcode.strip()

        # Try US formats first (most common)
        if self.US_ZIP5.match(zipcode):
            return True, None
        if self.US_ZIP9.match(zipcode):
            return True, None

        # Try Canadian
        if self.CA_POSTAL.match(zipcode):
            return True, None

        # Try UK
        if self.UK_POSTAL.match(zipcode):
            return True, None

        # If it's 5+ digits, might be another country's numeric postal code
        if re.match(r'^\d{4,6}$', zipcode):
            return True, None  # Accept 4-6 digit codes (many countries)

        # If it has letters and numbers and is 3-10 chars, probably valid
        if re.match(r'^[A-Z0-9\s-]{3,10}$', zipcode, re.IGNORECASE):
            return True, None

        return False, "Invalid zipcode format. Examples: 94118 (US), A1A 1A1 (CA), SW1A 1AA (UK)"

    def normalize(self, zipcode: str) -> str:
        """Normalize a zipcode to standard format.

        Args:
            zipcode: The zipcode to normalize

        Returns:
            Normalized zipcode
        """
        zipcode = zipcode.strip().upper()

        # Normalize Canadian postal codes (add space if missing)
        if self.CA_POSTAL.match(zipcode.replace(' ', '')):
            if ' ' not in zipcode and len(zipcode) == 6:
                return f"{zipcode[:3]} {zipcode[3:]}"

        return zipcode
