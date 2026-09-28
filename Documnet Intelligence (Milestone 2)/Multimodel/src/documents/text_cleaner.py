import re
 
 
class TextCleaner:
 
    @staticmethod
    def clean_text(text):
 
        if not text:
            return ""
 
        lines = text.splitlines()
 
        cleaned_lines = []
 
        for line in lines:
 
            cleaned_line = re.sub(
                r'[ \t]+',
                ' ',
                line
            )
 
            cleaned_line = "".join(
                ch for ch in cleaned_line
                if ch.isprintable()
            )
 
            cleaned_line = cleaned_line.strip()
 
            if cleaned_line:
                cleaned_lines.append(cleaned_line)
 
        return "\n".join(cleaned_lines)

