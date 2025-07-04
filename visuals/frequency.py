"""
This script visualizes the frequency of predefined and proposed keywords in the whole dataset.
"""

import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import re
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from init import cleaned_all

# Useful functions
def count_matches(keywords, text):
    """
    Counts the number of occurrences of each keyword in the text.
    """
    result = {keyword: 0 for keyword in keywords}
    tokens = re.findall(r'\b\w+\b', text.lower()) # Extract words from text
    
    for token in tokens:
        for keyword in keywords:
            if keyword in token:
                result[keyword] += 1
    
    return {keyword: count for keyword, count in result.items() if count > 0}

original_keywords = {"bill", "cheap", "cost", "efficient", "expens", "pay" }
new_keywords = {"provision", "budget", "demand", "optimiz", "reduce", "tun", "minim"}

# Count matches
original_counts = count_matches(original_keywords, cleaned_all)
new_counts = count_matches(new_keywords, cleaned_all)

# Configure the plot
keys = list(original_counts.keys()) + list(new_counts.keys())
vals = list(original_counts.values()) + list(new_counts.values())
colours = ['green'] * len(original_counts) + ['red'] * len(new_counts)

# Add a legend
legend = [
    Patch(facecolor='green', label='Predefined Keywords'),
    Patch(facecolor='red', label='Proposed Keywords')
]

# Make the images directory if it does not exist
if not os.path.exists("images"):
    os.makedirs("images")
 
# Create the plot
plt.figure(figsize=(10, 6))
plt.bar(keys, vals, color=colours)
plt.title("Keyword Frequencies: Predefined vs. Frequent")
plt.xlabel("Keywords")
plt.ylabel("Frequency")
plt.legend(handles=legend)
plt.grid(axis='y')
plt.savefig("images/keyword_frequencies.pdf", bbox_inches='tight')
plt.show()
