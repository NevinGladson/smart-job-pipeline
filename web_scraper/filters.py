import re

def filter_jobs(df, filters):
    if "location" in filters:
        locations = filters["location"]
    if isinstance(locations, str):
        pattern = locations
    else:
        pattern = "|".join(map(re.escape, locations))  # safely join list into regex
    df = df[df["location"].str.contains(pattern, case=False, na=False)]


    if "remote_only" in filters and filters["remote_only"]:
        df = df[df["is_remote"] == True]

    if "title_keywords" in filters:
        df = df[df["title"].str.contains("|".join(filters["title_keywords"]), case=False, na=False)]

    if "experience_keywords" in filters:
        keywords = filters["experience_keywords"]
        pattern = "|".join(keywords)
        df = df[df["description"].str.contains(pattern, case=False, na=False)]

    return df.reset_index(drop=True)
