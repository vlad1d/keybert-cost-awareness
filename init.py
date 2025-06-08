
from keybert import KeyBERT

from config import (MODEL_NAME, KEYBERT_PARAMS)
from helper import (load_commit_issue_texts, load_stackoverflow_texts, clean_text)

# Initialize KeyBERT model
kw_model = KeyBERT(model=MODEL_NAME)

# Get raw texts
commit_issue_texts = load_commit_issue_texts()
stackoverflow_texts = load_stackoverflow_texts()

# Clean texts
cleaned_commit_issue_texts = [clean_text(text) for text in commit_issue_texts]
cleaned_commit_issues = ' '.join(cleaned_commit_issue_texts)

cleaned_stackoverflow_texts = [clean_text(text) for text in stackoverflow_texts]
cleaned_stackoverflow = ' '.join(cleaned_stackoverflow_texts)

# Combine all texts
cleaned_all_texts = cleaned_commit_issue_texts + cleaned_stackoverflow_texts
cleaned_all = ' '.join(cleaned_all_texts)
print(f"Total texts for keyword extraction: {len(cleaned_all_texts)}\n")

def extract_keywords(profile="default", text=None, vectorizer=None):
    """ Extract keywords using KeyBERT based on the specified profile. Defaults to 'default' profile. """
    
    config = KEYBERT_PARAMS[profile]
    corpus = text or cleaned_all # set to full text if nothing is provided
    
    return kw_model.extract_keywords( 
        corpus,
        keyphrase_ngram_range=config["keyphrase_ngram_range"],
        top_n=config["top_n"],
        **({"nr_candidates": config["nr_candidates"]} if config.get("nr_candidates") is not None else {}),
        use_maxsum=config.get("use_maxsum", False),
        use_mmr=config.get("use_mmr", False),
        diversity=config.get("diversity", None),
        **({"vectorizer": vectorizer} if vectorizer is not None else {})
    )

# Export all necessary functions and variables
__all__ = [
    "extract_keywords",
    "cleaned_commit_issue_texts", 
    "cleaned_commit_issues",
    "cleaned_stackoverflow_texts", 
    "cleaned_stackoverflow",
    "cleaned_all_texts", 
    "cleaned_all",
]