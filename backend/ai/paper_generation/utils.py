def calculate_total_marks(sections):

    total = 0

    for section in sections:

        total += (

            section.marks_per_question

            * section.number_of_questions

        )

    return total