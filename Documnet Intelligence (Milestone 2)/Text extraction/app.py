from src.documents.loader import extract_text_from_pdf
 
 
# PDF file path
file_path = "data/documents/safety_manual.pdf"
 
 
# Extract text from PDF
text = extract_text_from_pdf(file_path)
 
 
# Display extracted text
print(text)
 
 
# Display total characters
print("Total characters:", len(text))