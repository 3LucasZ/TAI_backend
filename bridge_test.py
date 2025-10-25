import requests
import sys
import json

# --- Configuration
BASE_URL = "http://127.0.0.1:8000"
# ---


def main():
    print("--- FastAPI Test Client ---")
    print(f"Targeting server at: {BASE_URL}")
    print("Enter an endpoint path to POST to.")
    print("Valid paths: /setCollapsedTrue, /setCollapsedFalse, /chat/user/, /chat/bot/")
    print("Type 'q' to stop.")

    while True:
        try:
            path = input("\nEnter path> ").strip()
            if not path:
                continue

            # Handle exit
            if path == 'q':
                break

            # Handle endpoints
            full_url = f"{BASE_URL}{path}"
            if path == "/setCollapsedTrue":
                # no body
                response = requests.post(full_url)
                print(f"POST to {path} | Status: {response.status_code}")
                print(f"Response: {response.text}")
            elif path == "/setCollapsedFalse":
                # no body
                response = requests.post(full_url)
                print(f"POST to {path} | Status: {response.status_code}")
                print(f"Response: {response.text}")
            elif path == "/chat/user/" or path == "/chat/bot/":
                # require a JSON body: {"text": "..."}
                message_text = input("  Enter message text> ").strip()
                payload = {"text": message_text}
                # Send request with JSON payload
                response = requests.post(full_url, json=payload)
                print(
                    f"POST to {path} with {json.dumps(payload)} | Status: {response.status_code}")
                print(f"Response: {response.text}")

            else:
                # Handle unknown paths
                print(f"Error: Unknown path '{path}'.")
                print(
                    "Valid paths are: /setCollapsedTrue, /setCollapsedFalse, /chat/user/, /chat/bot/")

        except requests.exceptions.ConnectionError:
            print(f"\n--- !! Connection Error !! ---")
            print(f"Could not connect to {BASE_URL}.")
            print("Please make sure your FastAPI server is running.")
            print("---------------------------------\n")

        except KeyboardInterrupt:
            # Allow clean exit with Ctrl+C
            print("\nExiting test client. Goodbye!")
            sys.exit(0)

        except Exception as e:
            print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    # Check if 'requests' library is installed
    try:
        import requests
    except ImportError:
        print("Error: The 'requests' library is not installed.")
        print("Please install it by running: pip install requests")
        sys.exit(1)

    main()
