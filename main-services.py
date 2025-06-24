import re
import json
from sklearn.feature_extraction.text import CountVectorizer
from collections import defaultdict
from init import (extract_keywords, cleaned_all_texts, cleaned_all)


profile = "services" # ran with services

def fuzzy_match(phrase, text):
   """ Use a window matching approach with fuzzywuzzy to find if a phrase is present in the text. """
   words = phrase.lower().split()
   pattern = r"(?i)" + r".{0,10}".join([re.escape(word) for word in words])
   return re.search(pattern, text.lower())

   
    
with open("database/services.json", "r") as file:
   services = json.load(file)

# Get the service names or codes from the services JSON
map_to_service = {}
for service in services["Services"]:
   name = service["ServiceName"].lower().strip()
   code = service["ServiceCode"].lower().strip()
   cleaned_name = re.sub(r"^(amazon|aws)\s+", "", name)
   cleaned_code = re.sub(r"^(amazon|aws)\s+", "", code)
   
   # Map all aliases to the cleaned name
   # This covers more terms when trying to identify the service
   for alias in {name, code, cleaned_name, cleaned_code}:
      map_to_service[alias] = cleaned_name 

# Use CountVectorizer to extract n-grams from the cleaned texts based on the service names
# First, extract bigrams and trigrams from the texts
vectorizer = CountVectorizer(ngram_range=(2,3), stop_words='english')
X = vectorizer.fit_transform(cleaned_all_texts)
ngrams = vectorizer.get_feature_names_out()

# Create a mapping of n-grams to services
# That is, for each n-gram, find whether it belongs to any service
map_to_phrase = defaultdict(set)
for ngram in ngrams:
   for term, service in map_to_service.items():
      if term in ngram:
         map_to_phrase[service].add(ngram)

# Put the results through KeyBERT to get the most relevant phrases
keywords = extract_keywords(profile=profile, text=cleaned_all, vectorizer=vectorizer)

# Rank the services based on the keywords extracted by appending the keywords and their scores
ranked_services = defaultdict(set)
for keyword, score in keywords:
   tokens = re.findall(r"\b\w+\b", keyword.lower())
   
   for alias, service in map_to_service.items():
      if ' ' not in alias and alias in tokens: # if the alias is a single word and it is in the keyword
         ranked_services[service].add((keyword, score))
         
      elif ' ' in alias:
         pattern = r'\b' + re.escape(alias) + r'\b' # match the alias as a whole word
         if re.search(pattern, keyword.lower()):
            ranked_services[service].add((keyword, score))
         
# Print the services and their keywords
for service, phrases in ranked_services.items():
   # Sort phrases by score in descending order
   sorted_phrases = sorted(phrases, key=lambda x: x[1], reverse=True)
   
   print(f"\n--- {service.upper()} ---")
   for phrase, score in sorted_phrases[:10]: # limit only to top 10 phrases
      print(f"{phrase}: {score:.4f}")
      
      for text in cleaned_all_texts:
         # Use fuzzy matching to find the phrase in the text
         match = fuzzy_match(phrase, text)
         if match:
            # Split the text around the match to show context
            start,end = match.span()
            actual_start = max (0, start - 200) # capture 100 characters before the match
            actual_end = min(len(text), end + 200) # capture 100 characters after
            
            # Print the context of the match
            actual = text[actual_start:actual_end]
            if actual_start > 0:
               actual = "[...]" + actual
            if actual_end < len(text):
               actual = actual + "[...]"
            # print(f"[...] {actual} [...]\n")
            print(f"{actual}\n-")
            
      print("\n")