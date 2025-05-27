from collections import Counter
from upsetplot import UpSet, from_memberships
from matplotlib import pyplot as plt

phrases = [
   "dynamodb costs", "dynamodb pricing", "cheaper dynamodb", "cost cloud",
   "dynamodb demand", "dynamodb cheap", "billing dynamodb", "demand dynamodb",
   "dynamodb billing", "expensive dynamodb", "billing cloud", "cloud billing",
   "cloud costs", "dynamodb pay", "cloud cheaper", "budget cloudtrail",
   "dynamodb policy", "cheaper instances", "managed dynamodb", "costs cloudwatch",
   "cheaper billing", "dynamodb offers", "billing cloudwatch", "dynamo demand",
   "data billing", "payment dynamodb", "instance pricing", "instances cheaper",
   "dynamo db", "reduced cost", "dynamodb policies", "instances costs",
   "costs billing", "plan dynamodb", "reduces cost", "cost reductions",
   "cost billing", "reducing cost", "reduce cost", "cost reduction",
   "cloudwatch billing", "reduced costs", "cost reducing", "value dynamodb",
   "instances cost", "spending cloud", "cheaper ec2", "reduces costs",
   "depends dynamodb", "cost reduce", "expensive instances", "costs reduced",
   "cheaper instance", "dynamodb provided", "costs reduce", "advance dynamodb",
   "data cheaper", "io pricing", "cloud solutions", "value cloudwatch",
   "specification dynamodb", "new dynamodb", "instance costs", "instances expensive",
   "costs reducing", "fine dynamodb", "dynamodb advance", "dynamodb support",
   "reduce costs", "dynamo backend", "cost reduced", "dynamodb usage",
   "costs change", "ec2 pricing", "dynamodb use", "lower costs",
   "billing costs", "cloudwatch costs", "target dynamodb", "selection dynamodb",
   "instance cost", "cost server", "dynamo resource", "true dynamodb",
   "cost monitoring", "cost change", "decrease costs", "tracking costs",
   "cost tracking", "cloud compute", "costs feature", "dynamodb service",
   "capacity billing", "pricing support", "change pricing", "dynamodb scalable",
   "backend dynamo", "cloud charges", "elastic cloud", "amazon dynamodbv2"
]

original_keywords = {"bill", "cheap", "cost", "efficient", "expens", "pay" }

# filter the phrases to only include those that contain the original keywords
filtered_phrases = [phrase for phrase in phrases if any(keyword in phrase for keyword in original_keywords)]

memberships = [] # create a list of tuples to use for the upset plot
# basically pairs the words "formally" to keep track of which words are in the same phrase

for phrase in filtered_phrases:
   word1, word2 = phrase.lower().split()
   sorted_pair = tuple(sorted([word1, word2]))
   memberships.append(sorted_pair)
   
memberships_counts = Counter(memberships) # use counter to count the occurrences of each pair

data = from_memberships(memberships_counts.keys(), data=list(memberships_counts.values())) # create the data structure for the upset plot

# now plot the data
fig = plt.figure(figsize=(16, 20))
upset = UpSet(
   data,
   sort_by='cardinality'
)
upset.plot(fig=fig)
upset.style_elements = {'marker_size': 10, 'line_width': 2}
plt.suptitle("UpSet Plot of Co-occurrences in KeyBERT Phrases")
plt.figtext(0.5, 0.91, "Shows co-occurrences of keywords in 100 KeyBERT bigram phrases.", ha='center', fontsize=10)
plt.tight_layout()
plt.show()

