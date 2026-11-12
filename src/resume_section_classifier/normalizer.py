import re


def normalize_text(text):
    """
    Clean and normalize resume text while preserving line structure.
    """

    # Normalize different line-ending formats
    text = text.replace("\r\n", "\n")
    text = text.replace("\r", "\n")

    # Convert tabs to spaces
    text = text.replace("\t", " ")

    # Normalize common bullet characters
    text = text.replace("•", "-")
    text = text.replace("▪", "-")
    text = text.replace("●", "-")

    # Remove excessive spaces
    text = re.sub(r"[ ]{2,}", " ", text)

    # Remove excessive blank lines
    text = re.sub(r"\n[ ]*\n[ ]*\n+", "\n\n", text)

    return text.strip()


def normalize_heading(line):
    """
    Normalize a possible resume section heading.
    """

    line = line.strip()

    # Remove common heading/bullet characters
    line = re.sub(r"^[#>*\-•▪●\s]+", "", line)

    # Remove trailing punctuation
    line = re.sub(r"[:\-–—]+$", "", line)

    # Normalize spaces
    line = re.sub(r"\s+", " ", line).strip()

    # Convert to lowercase
    return line.lower()
