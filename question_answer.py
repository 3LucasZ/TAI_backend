import anthropic


client = anthropic.Anthropic(
    api_key="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")


def chat(prompt, system_instructions=None, max_tokens=1000):
    kwargs = {
        "model": "claude-sonnet-4-5",
        "max_tokens": max_tokens,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    }

    # Add system instructions if provided
    if system_instructions:
        kwargs["system"] = system_instructions
    message = client.messages.create(**kwargs)

    # Return the text content
    return message.content[0].text


def valid_question(text):
    return True
    system = "You have to determine if the text is a question. " \
        "If it is a question return 1, if it isn't a question, return 0, " \
        "do not return anything else"
    response = chat(text, system_instructions=system)
    return response == '1'


def ask_professor(transcript, question):
    system = "You are a professor lecturing in class." \
        "You must answer questions your students have." \
        "You must sound like a professor but give a 1 sentence natural sounding answer without any latex or asterisks or weird symbols." \
        "You must answer questions based on a transcript of what you have said in the lecture in the past. " \
        # "Do not hallucinate; reference the past and include it's timestamp."
    prompt = f"Question: {question}, Transcript: {transcript}"
    response = chat(prompt, system_instructions=system)
    print(response)
    return response


def get_transcript(mock=False):
    filename = "transcript.txt"
    if mock:
        filename = "mock_transcript.txt"
    transcript = open(filename, "r")
    content = transcript.read()
    return content


def get_answer(question_text):
    transcript = get_transcript()
    return ask_professor(transcript, question_text)


if __name__ == "__main__":
    transcript = get_transcript(mock=True)
    ask_professor(transcript, "what are the dimensions of the sigma matrix?")
