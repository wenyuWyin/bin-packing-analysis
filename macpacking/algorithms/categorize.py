def normalize(w: int, capacity: int) -> int:
    # Categorized every item's weight in the input stream
    ratio = w / capacity
    if w > (1 / 2) * ratio:
        return 0
    elif w > (2 / 5) * ratio:
        return 1
    elif w > (1 / 3) * ratio:
        return 2
    else:
        return 3
