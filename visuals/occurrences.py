from collections import Counter
from upsetplot import UpSet, from_memberships
from matplotlib import pyplot as plt
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from init import cleaned_all_texts

phrases = [
   "dynamodb costs",
   "costs aws",
   "dynamodb pricing",
   "aws costs",
   "cheaper dynamodb",
   "cost aws",
   "expensive aws",
   "dynamodb cheap",
   "aws budgets",
   "budget aws",
   "aws cost",
   "dynamodb demand",
   "aws budget",
   "expensive dynamodb",
   "demand dynamodb",
   "cheapest aws",
   "dynamodb billing",
   "billing dynamodb",
   "expense aws",
   "aws valuable",
   "dynamodb pay",
   "aws dynamo",
   "dynamodb policy",
   "optimize aws",
   "cost cloud",
   "aws optimizing",
   "paying aws",
   "optinrequired aws",
   "infrastructure aws",
   "billing aws",
   "aws infrastructure",
   "price aws",
   "aws additional",
   "aws dynamodb",
   "dynamodb aws",
   "aws infrastructures",
   "dynamo demand",
   "managed dynamodb",
   "aws reduce",
   "aws billing",
   "cloud costs",
   "cheaper ec2",
   "increase aws",
   "dynamodb policies",
   "value aws",
   "minimize aws",
   "cheaper instances",
   "costs cloudwatch",
   "dynamodb usage",
   "dynamodb offers"
]

phrases_pairs = {tuple(sorted(phrase.lower().split())): phrase for phrase in phrases} # take all bigrams and put them in a set, sorted, to avoid duplicates
pairs = Counter() 

for text in cleaned_all_texts: # iterate over all texts in the dataset
   words = text.lower().split()
   bigrams = list(zip(words, words[1:])) # use zip to create a list of all adjacently paired words in the text

   for (word1, word2), _ in phrases_pairs.items(): # iterate over all pairs of words in the phrases
      for (w1, w2) in bigrams:
         if ((word1 in w1 and word2 in w2) or (word2 in w1 and word1 in w2)): # check if the pair of words is in the bigrams and matches partially
            pairs[(word1, word2)] += 1
     
nozero_pairs = {pair: count for pair, count in pairs.items() if count > 0} # filter out pairs that do not occur
data = from_memberships(nozero_pairs.keys(), data=list(nozero_pairs.values())) # create the data structure for the upset plot

# Make the images directory if it does not exist
if not os.path.exists("images"):
    os.makedirs("images")

# Now plot the data
fig = plt.figure(figsize=(16, 20))
upset = UpSet(
   data,
   sort_by='cardinality'
)
upset.plot(fig=fig)
upset.style_elements = {'marker_size': 10, 'line_width': 2}
plt.suptitle("UpSet Plot of KeyBERT Bigrams in Dataset")
plt.figtext(0.5, 0.91, "Shows co-occurrences of 50 KeyBERT bigram phrases + their frequency (partial match)", ha='center', fontsize=10)
plt.tight_layout()
plt.savefig("images/upset_plot_bigrams.pdf", bbox_inches='tight')
plt.show()

