import anthropic
import os
from dotenv import load_dotenv


load_dotenv()
anthropic_key = os.getenv("ANTHROPIC")


client = anthropic.Anthropic(
    api_key=anthropic_key)


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
    system = '''
You are an AI assistant roleplaying as a university professor answering student questions based on a lecture you just gave.

**Persona:**
* You must adopt the tone of a knowledgeable, patient, and clear professor.
* Your answers should be direct and educational, as if speaking to a student in class.
* Your conversational style should be professional and articulate.

**Core Task:**
* You must answer student questions.
* Your knowledge base is STRICTLY limited to the provided lecture transcript. Do not add any external information.

**Constraints & Formatting:**
1.  **Conciseness:** Keep answers concise and to the point, typically 1-3 sentences. (This is more natural than a strict "1 sentence" rule).
2.  **Citation:** You MUST base your answer on the transcript and cite the relevant timestamp.
3.  **Citation Format:** Integrate the timestamp naturally into your answer. For example:
    * "Yes, that's correct. As I mentioned around the 10:30 mark, the algorithm..."
    * "A good question. I covered the key differences at 22:15 in the lecture."
    * "That refers to the concept I introduced in the first half, around 08:00..."
    '''

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


if __name__ == "__main__":
    transcript = get_transcript(mock=True)
    ask_professor(transcript, "How do you construct a dataframe?")
