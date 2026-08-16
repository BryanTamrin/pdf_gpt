import sys
from pypdf import PdfReader
from pathlib import Path

def main():
    # check input
    if len(sys.argv) != 2:
        sys.exit("valid syntax = python main.py [filename]")
    if not sys.argv[1].endswith(".pdf"):
        sys.exit("file is not a pdf")
    if not Path(sys.argv[1]).exists():
        sys.exit(f"{sys.argv[1]} does not exist")
    
    # read file
    reader = PdfReader(sys.argv[1])
    extracted_text = []
    for page in reader.pages:
        text = (page.extract_text())
        extracted_text.append(text)
    text = "\n".join(extracted_text)
    print(text)

    
if __name__ == "__main__":
    main()