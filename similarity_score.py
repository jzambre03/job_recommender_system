from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
import nltk

# Download necessary NLTK data
nltk.download("punkt")

def preprocess_text_for_doc2vec(text):
    """
    Preprocess text by tokenizing into sentences and words (for Doc2Vec).
    """
    sentences = nltk.sent_tokenize(text.lower())
    return [nltk.word_tokenize(sentence) for sentence in sentences]

def preprocess_text_for_tfidf(text):
    """
    Preprocess text by lowercasing and removing extra spaces (for TF-IDF).
    """
    return " ".join(text.lower().split())

def calculate_similarity_tfidf(resume, job_description):
    """
    Calculate similarity using TF-IDF and cosine similarity.
    Args:
        resume (str): Text of the resume.
        job_description (str): Text of the job description.
    Returns:
        float: Similarity score between 0 and 1.
    """
    if not resume or not job_description:
        return 0.0  # Handle empty inputs

    resume = preprocess_text_for_tfidf(resume)
    job_description = preprocess_text_for_tfidf(job_description)
    
    documents = [resume, job_description]
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform(documents)
    similarity_score = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
    return similarity_score

def calculate_similarity_doc2vec(resume, job_description):
    """
    Calculate similarity using Doc2Vec and cosine similarity.
    Args:
        resume (str): Text of the resume.
        job_description (str): Text of the job description.
    Returns:
        float: Similarity score between 0 and 1.
    """
    if not resume or not job_description:
        return 0.0  # Handle empty inputs

    # Preprocess the text
    resume_sentences = preprocess_text_for_doc2vec(resume)
    job_sentences = preprocess_text_for_doc2vec(job_description)

    # Combine sentences for training
    documents = [
        TaggedDocument(words=sentence, tags=[str(i)])
        for i, sentence in enumerate(resume_sentences + job_sentences)
    ]

    # Train a simple Doc2Vec model
    model = Doc2Vec(
        documents,
        vector_size=50,
        window=2,
        min_count=1,
        workers=4,
        epochs=50,  # Fewer epochs for faster training
        seed=42  # Fixed seed for reproducibility
    )

    # Infer vectors for the texts
    resume_vector = model.infer_vector([word for sentence in resume_sentences for word in sentence])
    job_vector = model.infer_vector([word for sentence in job_sentences for word in sentence])

    # Calculate cosine similarity
    similarity_score = cosine_similarity([resume_vector], [job_vector])[0][0]
    return similarity_score