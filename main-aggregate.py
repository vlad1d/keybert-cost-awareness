from collections import defaultdict
from init import (
    extract_keywords, cleaned_commit_issues, cleaned_stackoverflow_texts
)

profile = "default" # ran with trigrams0, trigrams0.3

# Apply KeyBERT on commits and issues
keywords = extract_keywords(profile=profile, text=cleaned_commit_issues)

# Print the keywords
print("Extracted keywords from commits and issues:")
for keyword, score in keywords:
    print(f"{keyword}: {score:.4f}")

# Apply KeyBERT on each Stack Overflow post individually
keyword_scores = defaultdict(list)

for cleaned_stackoverflow in cleaned_stackoverflow_texts:
    if cleaned_stackoverflow.strip():  # avoid empty strings
        keywords = extract_keywords(profile=profile, text=cleaned_stackoverflow)
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