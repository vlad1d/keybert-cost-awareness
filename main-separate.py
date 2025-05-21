from init import (
    kw_model, KeyBERT_PARAMS,
    cleaned_commit_issues, cleaned_stackoverflow
)

# Apply KeyBERT on commits and issues
keywords = kw_model.extract_keywords(
    cleaned_commit_issues,
    **KeyBERT_PARAMS
)

# Print the keywords
print("Extracted keywords from commits and issues:")
for keyword, score in keywords:
    print(f"{keyword}: {score:.4f}")

# Apply KeyBERT on Stack Overflow posts
keywords = kw_model.extract_keywords(
    cleaned_stackoverflow,
    **KeyBERT_PARAMS
)

# Print the keywords
print("\nExtracted keywords from Stack Overflow posts:")
for keyword, score in keywords:
    print(f"{keyword}: {score:.4f}")