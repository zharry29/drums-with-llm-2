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
    """
    parsed = parse_drum_notation(notation)
    print(parsed)