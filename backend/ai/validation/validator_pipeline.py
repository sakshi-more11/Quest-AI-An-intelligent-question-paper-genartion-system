"""
Complete Question Validation Pipeline

Pipeline:
Question
 |
 |-- Bloom Classification
 |
 |-- Difficulty Prediction
 |
 |-- Duplicate Detection
 |
Validated Question
"""


from backend.ai.validation.bloom_classifier import (
    predict_bloom
)


from backend.ai.validation.difficulty_classifier import (
    predict_difficulty
)


from backend.ai.validation.duplicate_detector import (
    check_duplicate
)



def validate_question(
        question,
        existing_questions
):


    # -----------------------------
    # Bloom Classification
    # -----------------------------

    bloom_result = predict_bloom(
        question
    )


    # -----------------------------
    # Difficulty Prediction
    # -----------------------------

    difficulty_result = predict_difficulty(
        question
    )


    # -----------------------------
    # Duplicate Detection
    # -----------------------------

    duplicate_result = check_duplicate(

        question,

        existing_questions

    )



    # -----------------------------
    # Final Validation Result
    # -----------------------------


    is_valid = not duplicate_result["duplicate"]



    return {


        "question": question,


        "bloom_level":
            bloom_result["bloom_level"],



        "bloom_confidence":
            bloom_result["confidence"],



        "difficulty":
            difficulty_result["difficulty"],



        "difficulty_confidence":
            difficulty_result["confidence"],



        "duplicate":
            duplicate_result["duplicate"],



        "similarity":
            duplicate_result["similarity"],



        "matched_question":
            duplicate_result["matched_question"],



        "validated":
            is_valid

    }