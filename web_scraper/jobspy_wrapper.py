from jobspy import scrape_jobs
import pandas as pd

def run_jobspy_scraper(resume_dict, user_filters):
    all_dfs = []
    locations = user_filters.get("location", ["Remote"])  # default to one if string

    # Normalize to list if single string
    if isinstance(locations, str):
        locations = [locations]

    for loc in locations:
        df = scrape_jobs(
            site_name=user_filters.get("site_name", ["indeed", "LinkedIn", "naukri"]),
            search_term=user_filters["search_term"],
            location=loc,
            results_wanted=user_filters.get("results_wanted", 30),
            country_indeed=user_filters.get("country_indeed", "India"),
            hours_old=user_filters.get("hours_old", 72),
            job_type=user_filters.get("job_type", None),
        )
        if not df.empty:
            all_dfs.append(df)

    if all_dfs:
        return pd.concat(all_dfs, ignore_index=True)
    else:
        return pd.DataFrame()
