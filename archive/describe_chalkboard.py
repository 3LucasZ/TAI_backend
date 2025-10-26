import os
import base64
from reka import Reka
from reka.errors import RekaError

# --- Configuration ---

# 1. SET YOUR API KEY
# Best practice is to set this as an environment variable.
# On Mac/Linux: export REKA_API_KEY='your-key-here'
# On Windows: set REKA_API_KEY='your-key-here'
# The script will read it from the environment.
#
# !! FALLBACK (Not Recommended for Production) !!
# If you don't set an environment variable, uncomment the next line
# and paste your key directly.
# REKA_API_KEY = "YOUR_API_KEY_HERE"

# --- End Configuration ---


def get_api_key():
    """Fetches the Reka API key."""
    api_key = os.getenv("REKA_API_KEY")

    # Check if the fallback is being used
    if not api_key:
        try:
            # Check if the user hardcoded the key above
            if 'REKA_API_KEY' in locals() or 'REKA_API_KEY' in globals():
                api_key = REKA_API_KEY
        except NameError:
            pass  # Variable wasn't defined, which is fine

    if not api_key or api_key == "YOUR_API_KEY_HERE":
        print("Error: REKA_API_KEY is not set.")
        print("Please set the REKA_API_KEY environment variable or")
        print("hardcode it in the REKA_API_KEY variable in the script.")
        return None
    return api_key


def encode_image_to_base64(image_path):
    """Encodes a local image file to a base64 string."""
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    except FileNotFoundError:
        print(f"Error: Image file not found at {image_path}")
        return None
    except Exception as e:
        print(f"Error encoding image: {e}")
        return None


def ask_question_about_image(image_content, content_type, question, model_name="reka-flash"):
    """
    Sends a question about an image to the Reka API.

    :param image_content: The image data (either a URL or a base64 string).
    :param content_type: "url" or "base64".
    :param question: The text question to ask about the image.
    :param model_name: The Reka model to use (e.g., 'reka-flash', 'reka-core').
    """
    api_key = get_api_key()
    if not api_key:
        return

    try:
        # 1. Initialize the Reka client
        client = Reka(api_key=api_key)

        # 2. Determine the image content type for the API
        if content_type == "url":
            image_payload = image_content
        elif content_type == "base64":
            # For base64, Reka expects a data URI prefix
            # We'll guess the mime type, but common ones are image/jpeg or image/png
            # You might need to adjust this if you know the exact type.
            image_payload = f"data:image/jpeg;base64,{image_content}"
        else:
            print("Error: Invalid content_type. Must be 'url' or 'base64'.")
            return

        print(f"Asking Reka (model: {model_name})...")
        print(f"Question: {question}\n")

        # 3. Call the multimodal endpoint
        response = client.chat.multimodal(
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "content": image_payload
                        },
                        {
                            "type": "text",
                            "content": question
                        }
                    ]
                }
            ],
            model=model_name
        )

        # 4. Print the response
        print("--- Reka's Answer ---")
        print(response.text)

        # Uncomment the line below to see the full, raw response object
        # print("\n--- Full Response Object ---\n", response)

    except RekaError as e:
        print(f"A Reka API error occurred: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# --- --- --- --- --- --- ---
# --- RUN THE SCRIPT HERE ---
# --- --- --- --- --- --- ---


if __name__ == "__main__":

    # --- --- --- --- --- --- --- --- --- --- ---
    # OPTION 1: Use an Image from a URL
    # --- --- --- --- --- --- --- --- --- --- ---

    # === EDIT THESE VALUES ===
    image_from_url = "https://storage.googleapis.com/reka-website-assets/flying_car.jpeg"
    question_for_url = "What is unusual about this image?"
    # =========================

    ask_question_about_image(
        image_content=image_from_url,
        content_type="url",
        question=question_for_url,
        model_name="reka-flash"  # You can also try 'reka-core' for the most powerful model
    )

    # --- --- --- --- --- --- --- --- --- --- ---
    # OPTION 2: Use a Local Image File
    # --- --- --- --- --- --- --- --- --- --- ---

    # To use this, comment out the "OPTION 1" block above
    # and uncomment the block below.

    """
    # === EDIT THESE VALUES ===
    local_image_path = "path/to/your/local_image.png" # e.g., "C:/Users/YourName/Desktop/photo.jpg"
    question_for_local = "Describe the main object in this photo."
    # =========================

    # Encode the local image to base64
    base64_image = encode_image_to_base64(local_image_path)
    
    if base64_image:
        ask_question_about_image(
            image_content=base64_image,
            content_type="base64",
            question=question_for_local,
            model_name="reka-flash"
        )
    """
