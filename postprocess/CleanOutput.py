import re


def cleanAnswer(text):
    # Remove bold markers
    text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)

    # Remove bullet markers
    text = re.sub(r"^\s*\*\s+", "- ", text, flags=re.MULTILINE)

    # Convert multiple newlines to single blank line
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()
