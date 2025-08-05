# smart-job-pipeline

# JobRanker: AI-Powered Resume-Aware Job Scraper

This project automates job scraping, filtering, and personalized ranking based on a user's resume and preferences. It leverages NLP and transformer models to match job listings to applicant profiles with high relevance.

---

## 🔍 Features

- ✅ Parse resume (PDF/DOCX) and convert to structured JSON
- ✅ Scrape job listings from major job boards using [JobSpy](https://github.com/cullenwatson/JobSpy)
- ✅ Filter jobs by location, title, experience, and preferences
- ✅ Rank jobs using SentenceTransformer (semantic resume-to-job similarity)
- ✅ Fuzzy match user preferences (e.g., “remote”, “valuation”)
- ✅ CSV output with timestamping and applicant-specific filenames
- ✅ Modular pipeline: scraping, filtering, ranking, exporting

---

## 🚀 Technologies Used

- Python
- [pdfplumber](https://github.com/jsvine/pdfplumber), `python-docx` – for resume parsing
- [OpenAI GPT-4o](https://platform.openai.com/docs/models/gpt-4o) – for resume structuring
- [JobSpy](https://github.com/cullenwatson/JobSpy) – for scraping jobs
- `sentence-transformers` – for semantic similarity
- `fuzzywuzzy` – for preference keyword matching
- Pandas, Sklearn, NumPy – for data processing

---

## 📁 Folder Structure
├── resume_dict/
│ └── obtaining_res_dict.py # Extract structured info from resume
├── web_scraper/
│ ├── main_scraper.py # Orchestrates full pipeline
│ ├── config/
│ │ ├── filters.json
│ │ └── user_prefs.json
│ ├── ranker.py # Job ranking logic
│ ├── filters.py # Job filtering logic
│ └── storage/
│ └── save_output.py # Saves to applicant-specific CSV



---

## 📦 How to Run

1. Clone the repo
2. Create a `.env` file and set your OpenAI API key
3. Place your resume (PDF/DOCX) in the root folder
4. Run:

```bash
python web_scraper/main_scraper.py --resume_file Resume.pdf
```
The ouput will be stored in 

web_scraper/output/ranked_jobs_<applicant_name>.csv

👤 Multi-User Support

  - Each resume gets its own output file

  - Scraped date column tracks job freshness

  - Ideal for teams or applicants applying in parallel


💡 Use Cases

  - Resume-to-job scoring tool for applicants

  - Backend pipeline for job boards or career platforms

  - Educational project to demonstrate data engineering + NLP skills


⚠️ Things to Watch Out For

  - OpenAI API usage may incur cost

  - JobSpy is occasionally blocked (e.g. Glassdoor); prefer Indeed

  - Transformer model requires a minimum of 1GB RAM

  - resume_dict must be parsed successfully for ranking to work


📄 License

 MIT License

✨ Acknowledgements

  - JobSpy

  - Sentence-Transformers

  - OpenAI
