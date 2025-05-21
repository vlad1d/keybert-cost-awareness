from init import (
    kw_model, KeyBERT_PARAMS,
    cleaned_all
)

# Apply KeyBERT to extract keywords
keywords = kw_model.extract_keywords(
    cleaned_all,
    **KeyBERT_PARAMS
)

# Print the keywords
print("\nExtracted keywords:")
for keyword, score in keywords:
    print(f"{keyword}: {score:.4f}")