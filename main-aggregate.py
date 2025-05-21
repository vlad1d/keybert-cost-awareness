from collections import defaultdict
from init import (
    kw_model, KeyBERT_PARAMS,
    cleaned_commit_issues, cleaned_stackoverflow_texts
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

# Apply KeyBERT on each Stack Overflow post individually
keyword_scores = defaultdict(list)

for cleaned_stackoverflow in cleaned_stackoverflow_texts:
    if cleaned_stackoverflow.strip():  # avoid empty strings
        keywords = kw_model.extract_keywords(cleaned_stackoverflow, **KeyBERT_PARAMS)
        for kw, score in keywords:
            keyword_scores[kw].append(score)

# Compute average scores per keyword
avg_scores = {kw: sum(scores) / len(scores) for kw, scores in keyword_scores.items()}

# Sort by average score and take top 10
top_keywords = sorted(avg_scores.items(), key=lambda x: x[1], reverse=True)[:10]

# Print the aggregated top keywords
print("\nExtracted aggregated keywords from Stack Overflow posts:")
for keyword, avg_score in top_keywords:
    print(f"{keyword}: {avg_score:.4f}")