from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

def rank_jobs(df, resume_dict, user_prefs):
    resume_text_parts = [
        " ".join(resume_dict.get("skills", [])),
        resume_dict.get("personal_profile", ""),
    ]

    experience_descriptions = [
        exp.get("description", "") for exp in resume_dict.get("experience", [])
        if isinstance(exp, dict)
    ]
    resume_text_parts.append(" ".join(experience_descriptions))

    resume_text = " ".join(resume_text_parts).strip()

    if not resume_text:
        print("⚠️ Warning: resume_text is empty. Resume score will be zero.")

    if not resume_text.strip():
        print("⚠️ Resume text is missing. Skipping TF-IDF matching.")
        df["resume_score"] = 0.0
        df["preference_score"] = 0
        df["total_score"] = 0
        return df


    
    df["title"] = df["title"].fillna("")
    df["description"] = df["description"].fillna("")
    
    combined = (df["title"] + " " + df["description"]).fillna("")
    tfidf = TfidfVectorizer().fit_transform([resume_text] + combined.tolist())
    similarities = cosine_similarity(tfidf[0:1], tfidf[1:]).flatten()
    df["resume_score"] = similarities


    if "preferences" in user_prefs:
        prefs = user_prefs["preferences"]
        pattern = "|".join(re.escape(pref) for pref in prefs)
        df["preference_score"] = df["description"].str.contains(
            pattern, case=False, na=False
        ).astype(int)
    else:
        df["preference_score"] = 0

    df["total_score"] = df["preference_score"] * 2 + df["resume_score"]
    return df.sort_values(by="total_score", ascending=False)

# The code given below has been tested on Google Colab and it works. However sentence transformer does take a decent amount of memory if you wish to run this
# on a local machine

# import numpy as np
# import re
# from sklearn.preprocessing import MinMaxScaler
# from sentence_transformers import SentenceTransformer, util
# from fuzzywuzzy import fuzz

# def rank_jobs(df, resume_dict, user_prefs):
#     # === Build resume_text from profile + responsibilities ===
#     profile = resume_dict.get("profile") or resume_dict.get("personal_profile") or ""
#     exp_blocks = resume_dict.get("experience", [])
    
#     responsibilities = []
#     for exp in exp_blocks:
#         if isinstance(exp, dict):
#             if "responsibilities" in exp:
#                 responsibilities.extend(exp["responsibilities"])
#             elif "description" in exp:
#                 responsibilities.append(exp["description"])

#     resume_text = (profile + "\n" + " ".join(responsibilities)).strip()

#     if not resume_text:
#         print("⚠️ Resume text is missing. Skipping ranking.")
#         df["resume_score"] = 0.0
#         df["preference_score"] = 0
#         df["total_score"] = 0
#         return df

#     # === Load transformer model ===
#     model = SentenceTransformer("all-MiniLM-L6-v2")
#     resume_embedding = model.encode(resume_text, convert_to_tensor=True)

#     # === Encode job descriptions ===
#     job_descriptions = df["description"].fillna("").tolist()
#     job_embeddings = model.encode(job_descriptions, convert_to_tensor=True)

#     # === Cosine similarity and normalization ===
#     similarities = util.cos_sim(resume_embedding, job_embeddings)[0].cpu().numpy()
#     scaler = MinMaxScaler(feature_range=(0, 7))
#     resume_scores = scaler.fit_transform(similarities.reshape(-1, 1)).flatten()

#     # === Preference scoring with fuzzy match ===
#     def score_preferences(row):
#         score = 0
#         prefs = user_prefs.get("preferences", [])
#         combined_text = " ".join([
#             str(row.get("title", "")),
#             str(row.get("description", "")),
#             str(row.get("company", "")),
#             str(row.get("location", "")),
#             str(row.get("job_type", ""))
#         ]).lower()

#         for pref in prefs:
#             if fuzz.partial_ratio(pref.lower(), combined_text) >= 80:
#                 score += 1
#                 break

#         if user_prefs.get("remote") and "remote" in combined_text:
#             score += 1

#         return score

#     preference_scores = df.apply(score_preferences, axis=1)

#     # === Final score ===
#     total_scores = resume_scores + preference_scores
#     total_scores = np.clip(total_scores, 1, 10)

#     df["resume_score"] = resume_scores.round(2)
#     df["preference_score"] = preference_scores
#     df["total_score"] = total_scores.round(1)

#     return df.sort_values(by="total_score", ascending=False).reset_index(drop=True)

