

def read_text(path):
    """
    Read the text from a file.
    """
    # Open the file
    with open(path, "r", encoding='utf-8') as file:
        # Read the text
        text = file.read()

    return text


def extract_references(text):
    lines = text.split("\n")

    found_references = False

    markers = [
        "reference",
        "bibliography",
        "word count",
    ]
    
    # Find index of line that contains ["References", "REFERENCES", "Bibliography", "BIBLIOGRAPHY" etc]
    for index, line in enumerate(lines):
        
        # if line containes any of the markers
        if any(marker in line.strip().lower() for marker in markers) and len(line.strip()) < 20:
            found_references = True
            break
    
    if not found_references:
        return ""
    else:
        references = lines[index:]

        # join the lines with "\n"
        return "\n".join(references)

def save_references(references, fname):
    """
    Save the references to a file.
    """
    # Open the file
    with open(fname, "w", encoding='utf-8') as file:
        # Write the references
        file.write(references)
    

if __name__ == "__main__":
    fname = "test.txt"
    text = read_text(fname)
    references = extract_references(text)

    reference_fname = fname.split(".")[0] + "_references.txt"
    save_references(references, reference_fname)

    print("References saved to", reference_fname)