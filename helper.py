""" Helper functions for data loading and text processing. """

import re
import os
import json
from config import (ALLOW_TECHNICAL, TECHNICAL_WORDS, COMPOUND_SPLIT_RULES, BASE_DIR, GITHUB_FILES, STACKOVERFLOW_DIR)

def clean_text(text, blocked=TECHNICAL_WORDS):
    """
    Cleans the text by:
    - replacing underscores with spaces
    - splitting up commonly identified compound words
    - removing unwanted tokens
    """

    # Replace underscores with spaces
    text = text.lower()
    text = text.replace('_', ' ') 

    # Split up commonly identified compound words
    for compound, split in COMPOUND_SPLIT_RULES.items():
        text = text.replace(compound, split)

    # Remove unwanted tokens
    if ALLOW_TECHNICAL:
        return text
    
    tokens = re.findall(r'\b\w+\b', text)
    filtered_tokens = [token for token in tokens if not any(word in token for word in blocked)]
    return ' '.join(filtered_tokens)

def get_text_from_so(post):
    """ Extracts the text from a Stack Overflow post. Uses BeautifulSoup to parse HTML content. """
      
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

def load_commit_issue_texts():
    """ Loads commit and issue texts from JSON files, filtering out unrelated records. """
    
    commit_issue_texts = []
    
    # Process each file in the GITHUB_FILES list
    for file in GITHUB_FILES:
        path = os.path.join(BASE_DIR, file)
        with open(path, 'r') as f:
            data = json.load(f)
        
        for record in data:
            # Remove records that are marked as 'unrelated'
            if "unrelated" not in record.get('codes', []):
                type = record.get('type')
                content = record.get('content', {})

                # Extract the text based on the type of record
                # Strip whitespace and handle empty cases too 
                if type == 'commit':
                    text = (content.get('message') or '').strip() 
                elif type == 'issue': 
                    title = (content.get('title') or '').strip() 
                    body = (content.get('body') or '').strip()
                    text = (title + ' ' + body).strip()
                else:
                    text = ''

                # Append to the list
                if text:
                    commit_issue_texts.append(text)

    # Print for debugging then return
    print(f"Loaded {len(commit_issue_texts)} commits and issues from {len(GITHUB_FILES)} files.")
    return commit_issue_texts

def load_stackoverflow_texts():
    """ Loads Stack Overflow posts from JSON files, extracting the text content. """
    
    # Get all JSON files in the Stack Overflow directory
    stackoverflow_files = [f for f in os.listdir(STACKOVERFLOW_DIR) if f.endswith('.json')]
    stackoverflow_texts = []
    
    for file in stackoverflow_files:
        # Load each file and extract the text using a helper function
        path = os.path.join(STACKOVERFLOW_DIR, file)
        with open(path, 'r') as f:
            data = json.load(f)

        text = get_text_from_so(data)
        
        # Clean the text and append it to the list if it's not empty
        if text:
            stackoverflow_texts.append(text)

    # Print for debugging then return
    print(f"Loaded {len(stackoverflow_texts)} Stack Overflow posts from {len(stackoverflow_files)} files.")
    return stackoverflow_texts
