import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'resume_dict')))

import json
import argparse
from jobspy_wrapper import run_jobspy_scraper
from filters import filter_jobs
from ranker import rank_jobs
from storage.save_output import save_as_csv
from obtaining_res_dict import load_or_generate_resume_dict

CONFIG_DIR = "web_scraper/config"

def load_json(path, fallback={}):
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    else:
        print(f"⚠️ {path} not found. Using defaults.")
        return fallback

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run job scraper pipeline")
    parser.add_argument("--resume_file", required=True)
    args = parser.parse_args()

    resume_dict = load_or_generate_resume_dict(args.resume_file)

    filters = load_json(os.path.join(CONFIG_DIR, "filters.json"))
    prefs = load_json(os.path.join(CONFIG_DIR, "user_prefs.json"))

    raw_df = run_jobspy_scraper(resume_dict, filters)
    print(f"📊 Retrieved {len(raw_df)} jobs from scraping.")

    filtered_df = filter_jobs(raw_df, filters)
    print(f"🔍 {len(filtered_df)} jobs remain after filtering.")

    ranked_df = rank_jobs(filtered_df, resume_dict, prefs)

    applicant_name = resume_dict.get("name", "default")  
    save_as_csv(ranked_df, applicant_name=applicant_name)


    required_cols = ['title', 'company', 'location', 'total_score', 'job_url']
    missing = [col for col in required_cols if col not in ranked_df.columns]
    if missing:
        print(f"⚠️ Missing columns in ranked output: {missing}")
    else:
        print("\n--- Top 5 Ranked Jobs ---")
        print(ranked_df[required_cols].head())
