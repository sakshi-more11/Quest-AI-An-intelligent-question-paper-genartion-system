"""
Difficulty Level Classification
Using Fine-tuned BERT Model
"""


import torch


from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification
)



# ---------------------------------------
# Model Path
# ---------------------------------------

MODEL_PATH = (
    "backend/ai/models/difficulty_bert"
)



# ---------------------------------------
# Difficulty Labels
# ---------------------------------------

DIFFICULTY_LABELS = {

    0: "Easy",

    1: "Medium",

    2: "Hard"

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

def predict_difficulty(question:str):


    inputs = tokenizer(

        question,

        return_tensors="pt",

        truncation=True,

        padding=True,

        max_length=256

    )



    with torch.no_grad():

        outputs = model(
            **inputs
        )



    logits = outputs.logits



    probabilities = torch.softmax(
        logits,
        dim=1
    )



    confidence, prediction = torch.max(
        probabilities,
        dim=1
    )



    difficulty = DIFFICULTY_LABELS[
        prediction.item()
    ]



    return {


        "question": question,


        "difficulty": difficulty,


        "confidence": round(
            confidence.item(),
            3
        )

    }