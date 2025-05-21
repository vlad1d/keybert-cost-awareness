import os
import re
import json
from keybert import KeyBERT
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS

# Database configuration
base = './database'
github_files = ['terraform-github.json', 'cloudformation-github.json']
stackoverflow_folder = os.path.join(base, 'terraform-stackoverflow')

# KeyBERT configuration
model = 'all-MiniLM-L6-v2'
technical_words = ['terraform', 'cloudformation', 'azure', 'google', 'aws',
                   #  'dynamo', 'elastic', 'cloudwatch', 'costexplorer'
]

# KeyBERT parameters
KeyBERT_PARAMS = dict (
    keyphrase_ngram_range = (1, 1),
    top_n = 10,
    nr_candidates = 20,
    use_maxsum = False,
    use_mmr = False
)

# Split rules for commonly identified compound words
compound_split_rules = {
    'cloudbilling': 'cloud billing',
    'costcenter': 'cost center',
    'billingmetrics': 'billing metrics',
    'datacenter': 'data center',
    'estimatedcharges': 'estimated charges',
    'billingbudgets': 'billing budgets',
    'costmonitoring': 'cost monitoring',
    'billingmode': 'billing mode'
}

# Initialize KeyBERT model with custom stop words
kw_model = KeyBERT(model=model)

# Useful functions
def clean_text(text, blocked=technical_words):
    """
    Cleans the text by:
    - replacing underscores with spaces
    - splitting up commonly identified compound words
    - removing unwanted tokens
    """

    # replace underscores with spaces
    text = text.lower()
    text = text.replace('_', ' ') 

    # split up commonly identified compound words
    for compound, split in compound_split_rules.items():
        text = text.replace(compound, split)

    # remove unwanted tokens
    tokens = re.findall(r'\b\w+\b', text)
    filtered_tokens = [token for token in tokens if not any(word in token for word in blocked)]
    return ' '.join(filtered_tokens)

def get_text_from_so(post):
    """
    Extracts the text from a Stack Overflow post.
    """
    from bs4 import BeautifulSoup

    # Extract the body of the post
    body_html = post.get('Body', '')
    body = BeautifulSoup(body_html, 'html.parser').get_text(separator=' ', strip =True)

    # Extract the title of the post
    title = (post.get('Title') or '').strip()

    # Extract the comments of the post
    comments_html = post.get('comments', [])
    comments = ' '.join([comment.get('Text', '').strip() for comment in comments_html if comment.get('Text')])

    # Combine the title, body, and comments
    text = f"{title} {body} {comments}".strip()
    return text

# Load the commits and issues from the JSON files, ensure filtering out unrelated records
commit_issue_texts = []
for file in github_files:
    path = os.path.join(base, file)
    with open(path, 'r') as f:
       data = json.load(f)
    
    for record in data:
        if "unrelated" not in record.get('codes', []):
            type = record.get('type')
            content = record.get('content', {})

            if type == 'commit':
                text = (content.get('message') or '').strip() 
            elif type == 'issue': 
                title = (content.get('title') or '').strip() 
                body = (content.get('body') or '').strip()
                text = (title + ' ' + body).strip()
            else:
                text = ''

            if text:
                commit_issue_texts.append(text)

print(f"Loaded {len(commit_issue_texts)} commits and issues from {len(github_files)} files.")

# Load Stack Overflow posts from JSON files
stackoverflow_files = [f for f in os.listdir(stackoverflow_folder) if f.endswith('.json')]
stackoverflow_texts = []
for file in stackoverflow_files:
    path = os.path.join(stackoverflow_folder, file)
    with open(path, 'r') as f:
        data = json.load(f)

    text = get_text_from_so(data)
    if text:
        stackoverflow_texts.append(text)

print(f"Loaded {len(stackoverflow_texts)} Stack Overflow posts from {len(stackoverflow_files)} files.")

# Clean texts
cleaned_commit_issue_texts = [clean_text(text) for text in commit_issue_texts]
cleaned_commit_issues = ' '.join(cleaned_commit_issue_texts)

cleaned_stackoverflow_texts = [clean_text(text) for text in stackoverflow_texts]
cleaned_stackoverflow = ' '.join(cleaned_stackoverflow_texts)

# Combine all texts
cleaned_all_texts = cleaned_commit_issue_texts + cleaned_stackoverflow_texts
cleaned_all = ' '.join(cleaned_all_texts)
print(f"Total texts for keyword extraction: {len(cleaned_all_texts)}\n")