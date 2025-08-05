import os
import json
import hashlib
import argparse
import pdfplumber
import docx
import ast
from openai import OpenAI
from dotenv import load_dotenv

# Load API key
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)

CACHE_DIR = "resume_dict/cache"
os.makedirs(CACHE_DIR, exist_ok=True)

def hash_file(file_path):
    with open(file_path, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()

def extract_text_from_pdf(file_path):
    with pdfplumber.open(file_path) as pdf:
        return "\n".join(page.extract_text() for page in pdf.pages if page.extract_text())

def extract_text_from_docx(file_path):
    doc = docx.Document(file_path)
    return "\n".join([para.text for para in doc.paragraphs if para.text.strip()])

def convert_to_dict(text):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an assistant that extracts structured resume data as a JSON dictionary."},
            {"role": "user", "content": "Extract name, contact, education, experience, skills, certifications, and a short personal profile from the resume text below. Return a valid JSON dictionary. Text:\n\n" + text}
        ],
        temperature=0.3,
    )
    return response.choices[0].message.content.strip()

def clean_raw_response(raw_response):
    """Remove triple-backtick markdown formatting if present"""
    if raw_response.startswith("```"):
        raw_response = raw_response.strip("`").strip()
        if raw_response.startswith("json"):
            raw_response = raw_response[4:].strip()
    return raw_response

def load_or_generate_resume_dict(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    file_hash = hash_file(file_path)
    cache_path = os.path.join(CACHE_DIR, f"{file_hash}.json")

    if os.path.exists(cache_path):
        print(f"✅ Loaded cached resume dictionary from {cache_path}")
        with open(cache_path, "r") as f:
            return json.load(f)

    print("⏳ Extracting text and calling OpenAI API...")
    if ext == ".pdf":
        text = extract_text_from_pdf(file_path)
    elif ext == ".docx":
        text = extract_text_from_docx(file_path)
    else:
        raise ValueError("Unsupported file type. Only PDF and DOCX are supported.")

    raw_response = convert_to_dict(text)
    print("\n🧪 RAW OpenAI RESPONSE:\n", raw_response[:500])

    raw_response = clean_raw_response(raw_response)

    try:
        resume_dict = json.loads(raw_response)
    except json.JSONDecodeError:
        try:
            resume_dict = ast.literal_eval(raw_response)
        except Exception:
            print("⚠️ Still failed to parse. Saving raw.")
            resume_dict = {"raw_response": raw_response}

    with open(cache_path, "w") as f:
        json.dump(resume_dict, f, indent=2)

    print(f"✅ Resume dictionary saved to {cache_path}")

    if "raw_response" in resume_dict:
        print("⚠️ Warning: Resume dictionary could not be structured. Some features will be disabled.")

    return resume_dict

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Extract structured resume data.')
    parser.add_argument('--resume_file', required=True)
    args = parser.parse_args()

    resume_data = load_or_generate_resume_dict(args.resume_file)
    print("\n--- Resume Dictionary ---")
    print(json.dumps(resume_data, indent=2))
