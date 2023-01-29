from transformers import pipeline


sentences = [
    "We are very happy to show you the 🤗 Transformers library.",
    "This library sucks.",
    "One plus one equals two."
]

classifier = pipeline("sentiment-analysis")
result = classifier(sentences)
print(result)

zeroshot = pipeline("zero-shot-classification")
result = zeroshot("Bilibili is a good website", 
candidate_labels=["website", "game",'sport','music'])