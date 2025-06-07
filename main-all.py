from init import (
    extract_keywords, cleaned_all
)

profile = "upset" # ran with upset

# Apply KeyBERT to extract keywords
keywords = extract_keywords(profile=profile, text=cleaned_all)

# Print the keywords
print("\nExtracted keywords:")
for keyword, score in keywords:
    print(f"{keyword}: {score:.4f}")