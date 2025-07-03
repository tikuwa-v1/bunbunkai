import re

quote_pairs = {'「': '」', '『': '』'}
opening_quotes = set(quote_pairs.keys())
closing_quotes = set(quote_pairs.values())

LISTING_PATTERN = re.compile(r'(?:「[^」]{1,5}」){2,}')

def split_text(text):
    result = []
    buffer = ''
    narration_buffer = ''
    stack = []
    i = 0

    while i < len(text):
        # 特定パターン処理：短い引用の連続（箇条書き）
        listing_match = LISTING_PATTERN.match(text, i)
        if listing_match:
            narration_buffer += listing_match.group()
            i += len(listing_match.group())
            continue

        char = text[i]
        prev_char = text[i - 1] if i > 0 else None

        if char in opening_quotes:
            # 直前が読点かつ後続が短い単語なら地の文に
            match = re.match(rf'{re.escape(char)}[^{quote_pairs[char]}]{{1,5}}{re.escape(quote_pairs[char])}', text[i:])
            if prev_char == '、' and match:
                # ex: 、『ふふ』
                narration_buffer += text[i:i+len(match.group())]
                i += len(match.group())
                continue

            # 通常のセリフ処理開始
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
