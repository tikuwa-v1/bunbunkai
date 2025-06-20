# splitter.py
import re

quote_pairs = {'「': '」', '『': '』'}
opening_quotes = set(quote_pairs.keys())
closing_quotes = set(quote_pairs.values())

def split_text(text):
    result = []
    buffer = ''
    narration_buffer = ''
    stack = []
    i = 0

    while i < len(text):
        char = text[i]

        if char in opening_quotes:
            if narration_buffer.strip():
                result.append("[地の文] " + narration_buffer.strip())
                narration_buffer = ''
            buffer += char
            stack.append(quote_pairs[char])

        elif char in closing_quotes:
            buffer += char
            if stack and char == stack[-1]:
                stack.pop()
            if not stack:
                result.append("[セリフ] 不明：" + buffer.strip())
                buffer = ''
        else:
            if stack:
                buffer += char
            else:
                narration_buffer += char

        i += 1

    if narration_buffer.strip():
        result.append("[地の文] " + narration_buffer.strip())

    return "\n".join(result)
