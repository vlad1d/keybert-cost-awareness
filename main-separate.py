from init import (
    extract_keywords, cleaned_commit_issues, cleaned_stackoverflow
)

profile = "default" # ran with unigrams0, unigrams0.3, bigrams0, bigrams0.3

# Apply KeyBERT on commits and issues
keywords = extract_keywords(profile=profile, text=cleaned_commit_issues)

# Print the keywords
print("Extracted keywords from commits and issues:")
for keyword, score in keywords:
    print(f"{keyword}: {score:.4f}")

# Apply KeyBERT on Stack Overflow posts
keywords = extract_keywords(profile=profile, text=cleaned_stackoverflow)

# Print the keywords
print("\nExtracted keywords from Stack Overflow posts:")
for keyword, score in keywords:
    print(f"{keyword}: {score:.4f}")