def uniq(lines):
    return [lines[i] for i in range(len(lines)) if i == 0 or lines[i] != lines[i - 1]]

def head(lines, n=10):
    return lines[:n]

def wc(lines):
    return {
        "lines": len(lines),
        "words": sum(len(line.split()) for line in lines),
        "characters": sum(len(line) for line in lines),
    }
