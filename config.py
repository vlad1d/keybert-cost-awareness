import os

# Database configuration
BASE_DIR = './database'
GITHUB_FILES = ['terraform-github.json', 'cloudformation-github.json']
STACKOVERFLOW_DIR = os.path.join(BASE_DIR, 'terraform-stackoverflow')

# KeyBERT configuration
MODEL_NAME = 'all-MiniLM-L6-v2'
TECHNICAL_WORDS = ['terraform', 'cloudformation', 'azure', 'google', 'aws']
ALLOW_TECHNICAL = True # set to False only when running unigrams

# All KeyBERT parameters that were used and presented as results in the research 
KEYBERT_PARAMS = {
   "default": { 
      "keyphrase_ngram_range": (1, 1),
      "top_n": 10
   },
   "unigrams0": {
      "keyphrase_ngram_range": (1, 1),
      "top_n": 10,
      "nr_candidates": 20,
      "use_mmr": True,
      "diversity": 0,
   },
   "unigrams0.3": {
      "keyphrase_ngram_range": (1, 1),
      "top_n": 10,
      "nr_candidates": 20,
      "use_mmr": True,
      "diversity": 0.3,
   },
   "bigrams0": {
      "keyphrase_ngram_range": (2, 2),
      "top_n": 10,
      "nr_candidates": 20,
      "use_mmr": True,
      "diversity": 0,
   },
   "bigrams0.3": {
      "keyphrase_ngram_range": (2, 2),
      "top_n": 10,
      "nr_candidates": 20,
      "use_mmr": True,
      "diversity": 0.3,
   },
   "trigrams0": {
      "keyphrase_ngram_range": (3, 3),
      "top_n": 10,
      "nr_candidates": 20,
      "use_mmr": True,
      "diversity": 0,
   },
   "trigrams0.3": {
      "keyphrase_ngram_range": (3, 3),
      "top_n": 10,
      "nr_candidates": 20,
      "use_mmr": True,
      "diversity": 0.3,
   },
   "upset": {
      "keyphrase_ngram_range": (2, 2),
      "top_n": 100,
   },
   "services": {
      "keyphrase_ngram_range": (2, 3),
      "top_n": 1000,
      "stop_words": "english"
   }
}

# Compound split rules for commonly-noticed terms in the results
COMPOUND_SPLIT_RULES = {
   'cloudbilling': 'cloud billing',
   'costcenter': 'cost center',
   'billingmetrics': 'billing metrics',
   'datacenter': 'data center',
   'estimatedcharges': 'estimated charges',
   'billingbudgets': 'billing budgets',
   'costmonitoring': 'cost monitoring',
   'billingmode': 'billing mode'
}