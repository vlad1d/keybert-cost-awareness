import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import re

# Useful functions
def count_matches(keywords, unigrams):
    """
    Counts the number of partial matches for each keyword in a list of unigrams.
    """
    result = {}
    for keyword in keywords:
        cnt = 0 
        for unigram in unigrams:
            if keyword in unigram:
                cnt += 1
        if cnt > 0:
            result[keyword] = cnt
    return result

# A list of extracted KeyBERT keywords from the previous step
output = [
    # Unigrams
    "dynamodb", "elasticloadbalancing", "costs", "billing", "pricing", "cloudtrail",
    "cloud", "cost", "cloudwatch", "costing", "cloudbasedsensorcentral", 
    "provisioning", "availability", "ec2instances", "swapping",

    # Bigrams
    "dynamodb costs", "costs aws", "dynamodb pricing", "aws costs", "cheaper dynamodb",
    "expensive aws", "dynamodb cheap", "aws budgets", "aws cost", "dynamodb demand",
    "aws optimizing", "aws reduce", "cheaper terraform", "aws customizations",
    "budget cloudtrail", "cloudwatch tuning", "aws elasticloadbalancing", "reduces cost",

    # Trigrams
    "costs enabling dynamodb", "cost change dynamodb", "aws cost management",
    "minimize aws costs", "dynamodb cheap terraform", "cheaper dynamodb enable",
    "dynamo db cost", "make dynamodb cheap", "cost default dynamodb",
    "dynamodb billing demand", "increasing billl aws", "allow cheaper instances",
    "cloudformation newer cheaper", "cost lambda infrastructure",
    "experimental cloudwatch billing"
]

original_keywords = {"bill", "cheap", "cost", "efficient", "expens", "pay" }
new_keywords = {"cloud", "provision", "budget", "demand", "optimiz", "reduce", "tune", "minim"}

# Extract all unigrams as individual words
unigrams = []
for word in output:
    tokens = re.findall(r'\b\w+\b', word.lower())
    unigrams.extend(tokens)

# Count matches
original_counts = count_matches(original_keywords, unigrams)
new_counts = count_matches(new_keywords, unigrams)

# Configure the plot
keys = list(original_counts.keys()) + list(new_counts.keys())
vals = list(original_counts.values()) + list(new_counts.values())
colours = ['green'] * len(original_counts) + ['red'] * len(new_counts)

# Add a legend
legend = [
    Patch(facecolor='green', label='Predefined Keywords'),
    Patch(facecolor='red', label='Proposed Keywords')
]

# Create the plot
plt.figure(figsize=(10, 6))
plt.bar(keys, vals, color=colours)
plt.title("Keyword Frequencies: Predefined vs. Proposed")
plt.xlabel("Keywords")
plt.ylabel("Frequency")
plt.legend(handles=legend)
plt.grid(axis='y')
plt.show()
