import re
import base64  # Added this line
from langdetect import detect

def detect_mood(text):
    # Simple mood detection based on keywords
    text = text.lower()
    if re.search(r'happy|mazaa|fun', text):
        return "happy"
    elif re.search(r'sad|dukh|stress', text):
        return "sad"
    else:
        return "neutral"

def process_image(file):
    b = file.getvalue()
    mime = "image/png" if file.name.lower().endswith(".png") else "image/jpeg"
    return base64.b64encode(b).decode("utf-8"), mime

def remove_emojis(text):
    emoji_pattern = re.compile(
        "["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags
        u"\U00002500-\U00002BEF"  # chinese symbols
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        "]+", flags=re.UNICODE
    )
    return emoji_pattern.sub(r'', text)

def js_escape(text):
    return text.replace('"', '\\"').replace("\n", "\\n")