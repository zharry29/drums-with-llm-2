def parse_response(text):
    """
    Extracts and returns the string between the first pair of @@@ markers.
    """
    start = text.find('@@@')
    if start == -1:
        return ""
    end = text.find('@@@', start + 3)
    if end == -1:
        return ""
    return text[start + 3:end].strip()

def parse_drum_notation(text):
    result = {}
    for line in text.strip().splitlines():
        if not line.strip() or ':' not in line:
            continue
        key, pattern = line.split(':', 1)
        key = key.strip()
        # Split by |, then split each part into a list of characters
        measures = [list(measure.strip()) for measure in pattern.strip().split('|')]
        result[key] = measures
    return result

# Example usage:
if __name__ == "__main__":
    notation = """
    K: O---|----|O---|----
    S: ----|S--o|----|O---
    H: x---|x---|x---|x---
    T: ----|----|-O--|---o
    C: O---|----|----|----
    R: ----|----|----|----
    """
    parsed = parse_drum_notation(notation)
    print(parsed)