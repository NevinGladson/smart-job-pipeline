import os
import pandas as pd
from datetime import datetime

def save_as_csv(df, filename_base="ranked_jobs", applicant_name="default"):
    output_dir = "web_scraper/output"
    os.makedirs(output_dir, exist_ok=True)

    # === 1. Add Scraped Date column ===
    today = datetime.today().strftime("%Y-%m-%d")
    df.insert(0, "Scraped Date", today)

    # === 2. Build dynamic filename ===
    safe_name = applicant_name.lower().replace(" ", "_")
    filename = f"{filename_base}_{safe_name}.csv"
    file_path = os.path.join(output_dir, filename)

    # === 3. Append to top of existing file (like a stack) ===
    if os.path.exists(file_path):
        old_df = pd.read_csv(file_path)
        combined_df = pd.concat([df, old_df], ignore_index=True)
    else:
        combined_df = df

    # Save final file
    combined_df.to_csv(file_path, index=False)
    print(f"✅ Saved {len(df)} new jobs to {file_path}")
