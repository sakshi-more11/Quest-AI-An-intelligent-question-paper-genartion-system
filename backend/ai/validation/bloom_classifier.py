"""
Bloom Taxonomy Classification
Using Fine-tuned BERT Model
"""


import torch

from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification
)



# ---------------------------------------
# Model Configuration
# ---------------------------------------

MODEL_PATH = (
    "backend/ai/models/bloom_bert"
)



# ---------------------------------------
# Bloom Labels
# ---------------------------------------

BLOOM_LABELS = {

    0:"BT1 - Remember",

    1:"BT2 - Understand",

    2:"BT3 - Apply",

    3:"BT4 - Analyze",

    4:"BT5 - Evaluate",

    5:"BT6 - Create"

}



# ---------------------------------------
# Load Model
# ---------------------------------------

tokenizer = AutoTokenizer.from_pretrained(
    MODEL_PATH
)


model = AutoModelForSequenceClassification.from_pretrained(
    MODEL_PATH
)


model.eval()



# ---------------------------------------
# Prediction Function
# ---------------------------------------

def predict_bloom(question:str):


    inputs = tokenizer(

        question,

        return_tensors="pt",

        truncation=True,

        padding=True,

        max_length=256

    )


    with torch.no_grad():


        outputs = model(**inputs)



    logits = outputs.logits


    probabilities = torch.softmax(
        logits,
        dim=1
    )


    confidence, prediction = torch.max(
        probabilities,
        dim=1
    )



    bloom_level = BLOOM_LABELS[
        prediction.item()
    ]



    return {


        "question":question,


        "bloom_level":bloom_level,


        "confidence":round(
            confidence.item(),
            3
        )

    }