import os
import re
import fitz  # PyMuPDF
from tqdm import tqdm
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

# ----- Stopwords for Basic Text Cleaning -----
STOPWORDS = set([
    'the', 'and', 'is', 'in', 'to', 'a', 'of', 'for', 'on', 'with',
    'as', 'an', 'by', 'at', 'from', 'or', 'this', 'that', 'it', 'be',
    'are', 'was', 'were', 'have', 'has', 'had'
])

# ----- Clean Text Function -----
def clean_text_basic(text):
    text = text.lower()
    text = re.sub(r'[^a-z\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    words = text.split()
    words = [word for word in words if word not in STOPWORDS]
    return ' '.join(words)

# ----- Step 1 + Step 2: Extract and Clean Resumes -----
def extract_and_clean_resumes(folder_path):
    cleaned_resumes = []
    filenames = []

    for file in tqdm(os.listdir(folder_path)):
        if file.endswith('.pdf'):
            file_path = os.path.join(folder_path, file)
            doc = fitz.open(file_path)
            text = ""

            for page in doc:
                text += page.get_text()
            doc.close()

            cleaned = clean_text_basic(text)
            cleaned_resumes.append(cleaned)
            filenames.append(file)

    return cleaned_resumes, filenames

# ----- Step 3: TF-IDF Vectorizer -----
def vectorize_documents(documents):
    vectorizer = TfidfVectorizer(max_features=1000)
   
    vectors = vectorizer.fit_transform(documents)
    print(f"-------------{vectors}---------------------")
    return vectors, vectorizer

# ----- Step 4: Clustering -----
def cluster_with_job_description(tfidf_matrix, filenames, num_clusters=3):
    kmeans = KMeans(n_clusters=num_clusters, random_state=42)
    kmeans.fit(tfidf_matrix)
    labels = kmeans.labels_

    print("\n🔍 Clustering Results:\n")
    for i, file in enumerate(filenames):
        print(f"{file} => Cluster {labels[i]}")

    # Find the cluster of the job description (last entry)
    job_cluster = labels[-1]
    print(f"\n📌 Job Description is in Cluster {job_cluster}")
    print("📄 Resumes matching this cluster:")

    for i, file in enumerate(filenames[:-1]):
        if labels[i] == job_cluster:
            print(f"✅ {file}")

# ----- Main Pipeline -----
folder_path = "resume"
cleaned_resumes, resume_filenames = extract_and_clean_resumes(folder_path)

# Add Job Description here
job_description = """
We are looking for a Data Analyst with experience in Python, data visualization,
statistics, and report automation. Strong knowledge of Excel, SQL, and dashboards
using Power BI or Tableau is expected.
"""
cleaned_job_desc = clean_text_basic(job_description)

# Combine resumes + job description
all_documents = cleaned_resumes + [cleaned_job_desc]
all_filenames = resume_filenames + ["<Job Description>"]

# Vectorize
tfidf_matrix, vectorizer = vectorize_documents(all_documents)
print(f"\n✅ TF-IDF Matrix Shape: {tfidf_matrix.shape}")

# Cluster
cluster_with_job_description(tfidf_matrix, all_filenames, num_clusters=3)
