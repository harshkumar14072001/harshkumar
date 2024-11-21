from .constants import BOT_WELCOME_MESSAGE, PYTHON_QUESTION_LIST


def generate_bot_responses(message, session):
    bot_responses = []

    current_question_id = session.get("current_question_id")
    if not current_question_id:
        bot_responses.append(BOT_WELCOME_MESSAGE)

    success, error = record_current_answer(message, current_question_id, session)

    if not success:
        return [error]

    next_question, next_question_id = get_next_question(current_question_id)

    if next_question:
        bot_responses.append(next_question)
    else:
        final_response = generate_final_response(session)
        bot_responses.append(final_response)

    session["current_question_id"] = next_question_id
    session.save()

    return bot_responses


def record_current_answer(answer, current_question_id, session):
    '''
    Validates and stores the answer for the current question in the session.
    '''
    if not current_question_id:  # if no current question is available ,then  nothing to record
        return False, "No question to answer."

    # aasuming it is empty
    if not answer.strip():  # If the answer is empty
        return False, "Answer cannot be empty."

    # Store the answer in the session if it is not empty
    # if answers not in session then make a dict of it and with current question id add it 
    if "answers" not in session:
        session["answers"] = {}

    session["answers"][current_question_id] = answer
    session.save()

    return True, ""


def get_next_question(current_question_id):
    '''
    Fetches the next question from the PYTHON_QUESTION_LIST based on the current_question_id.
    '''
    # Ensure `PYTHON_QUESTION_LIST` is defined a list of questions
    try:
        question_list = PYTHON_QUESTION_LIST
    except NameError:
        return None, None  # If the list is not defined

    # If there is no current_question_id, start from the beginning
    if current_question_id is None:
        return question_list[0], 0

    # Get the next question based on the current index
    next_question_id = current_question_id + 1

    if next_question_id < len(question_list):  # Check if it is within bounds or not of PYTHON QUESTION LIST
        return question_list[next_question_id], next_question_id
    else:
        return None, None  # No more questions


def generate_final_response(session):
    '''
    Creates a final result message including a score based on the answers
    by the user for questions in the PYTHON_QUESTION_LIST.
    '''
    answers = session.get("answers", {})
    total_questions = len(PYTHON_QUESTION_LIST)
    answered_questions = len(answers)

    # Calculate a dummy score (you can enhance this logic based on actual scoring criteria)
    score = f"{answered_questions}/{total_questions}"

    response = "quiz Completed!\n"
    response += f"You answered {answered_questions} out of {total_questions} questions.\n"
    response += f"Your score: {score}\n"

    # Optional: Add answers and feedback to the result
    response += "Answers:\n"
    for question_id, answer in answers.items():
        question = PYTHON_QUESTION_LIST[question_id]
        response += f"Q: {question}\nA: {answer}\n"

    return response
