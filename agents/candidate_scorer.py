from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def score(job_desc, candidate_profile):
    v = TfidfVectorizer().fit_transform([job_desc, candidate_profile])
    return int(cosine_similarity(v[0:1], v[1:2])[0][0] * 100)

if __name__ == "__main__":
    print(f"Скоринг: {score('Python developer React', 'Senior Python engineer, 5 years React')}")
