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

predefined_keywords = {"bill", "cheap", "cost", "efficient", "expens", "pay" }
proposed_keywords = {"budget"}
other_keywords = {"provision", "demand", "optimiz", "reduce", "tun", "minim"}

# Count matches
predefined_counts = count_matches(predefined_keywords, cleaned_all)
proposed_counts = count_matches(proposed_keywords, cleaned_all)
other_counts = count_matches(other_keywords, cleaned_all)

# Configure the plot
keys = list(predefined_counts.keys()) + list(proposed_counts.keys()) + list(other_counts.keys())
vals = list(predefined_counts.values()) + list(proposed_counts.values()) + list(other_counts.values())
colours = ['goldenrod'] * len(predefined_counts) + ['green'] * len(proposed_counts) + ['red'] * len(other_counts)

# Add a legend
legend = [
    Patch(facecolor='goldenrod', label='Predefined Keywords'),
    Patch(facecolor='green', label='Proposed Keywords'),
    Patch(facecolor='red', label='Other Frequent Keywords')
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
plt.savefig("images/keyword_frequencies.png", dpi=300, bbox_inches='tight')
plt.show()
