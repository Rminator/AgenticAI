import os
import PyPDF2
import docx
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load spaCy NLP model
nlp = spacy.load("en_core_web_sm")

# Function to extract text from PDF
def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text() + "\n"
    return text

# Function to extract text from DOCX
def extract_text_from_docx(docx_path):
    doc = docx.Document(docx_path)
    return "\n".join([para.text for para in doc.paragraphs])

# Function to extract text from a file
def extract_text(file_path):
    if file_path.endswith(".pdf"):
        return extract_text_from_pdf(file_path)
    elif file_path.endswith(".docx"):
        return extract_text_from_docx(file_path)
    else:
        return None  # Skip unsupported files

# Preprocessing function: Clean text and remove stopwords
def preprocess_text(text):
    doc = nlp(text.lower())  # Convert to lowercase and process with spaCy
    tokens = [token.lemma_ for token in doc if not token.is_stop and token.is_alpha]  # Lemmatization & Stopwords removal
    return " ".join(tokens)

# Function to process resumes from a folder
def process_resumes(folder_path):
    processed_resumes = {}

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)

        if file_path.endswith((".pdf", ".docx")):
            print(f"Processing: {filename}")
            resume_text = extract_text(file_path)
            if resume_text:
                processed_resumes[filename] = preprocess_text(resume_text)

    return processed_resumes

# Function to rank resumes based on job description
def rank_resumes(job_description, resumes):
    vectorizer = TfidfVectorizer()
    texts = [job_description] + list(resumes.values())  # Combine job description with resumes
    tfidf_matrix = vectorizer.fit_transform(texts)
    
    scores = cosine_similarity(tfidf_matrix[0], tfidf_matrix[1:])[0]  # Compare job description with resumes
    ranked_resumes = sorted(zip(resumes.keys(), scores), key=lambda x: x[1], reverse=True)
    
    return ranked_resumes

# === Main Execution ===
resume_folder = "/Users/ngaonkar/Downloads/Resumes/"  # Change this to your folder path
job_desc = "Looking for a Data Engineer with SQL, AWS, Python, Databricks, and Lakehouse experience."

# Process resumes from the folder
processed_resumes = process_resumes(resume_folder)

# Rank resumes based on job description
ranked_results = rank_resumes(job_desc, processed_resumes)

# Print results
print("\n=== Ranked Resumes ===")
for i, (filename, score) in enumerate(ranked_results):
    print(f"Rank {i+1}: {filename} - Score: {score:.2f}")
