import requests
import random

# ---------------- CONFIG ----------------
IMAGE_PATH = "image (4).png"   # your image
GITHUB_TOKEN = ""  # <-- put your personal access token here

# 2-bit -> fruit mapping 
BIT_TO_FRUIT = {
    "00": "🍌",  # banana
    "01": "🍑",  # peach
    "10": "🍍",  # pineapple
    "11": "🥝",  # kiwi
}

# random separators
SEPARATORS = ["🍇", "🍉", "🥭", "🍋"]


# ---------------- ENCODING ----------------

def read_image_bytes(IMAGE_PATH):
    with open(IMAGE_PATH, "rb") as f:
        return f.read()


def bytes_to_fruit(data):
    """
    Each byte = 8 bits
    Split into 2-bit chunks
    Each 2 bits -> 1 emoji
    """
    output = []

    for byte in data:
        bits = f"{byte:08b}"  # e.g. 01101001

        # split into 2-bit chunks
        chunks = [bits[i:i+2] for i in range(0, 8, 2)]

        for chunk in chunks:
            output.append(BIT_TO_FRUIT[chunk])

            # randomly add separator (not always)
            if random.random() < 0.25:
                output.append(random.choice(SEPARATORS))

        # hard line separator for safety
        output.append("\n")

    return "".join(output)


# ---------------- GIST UPLOAD ----------------

def upload_to_gist(text):
    url = "https://api.github.com/gists"

    payload = {
        "description": "Fruit-Encoded Binary Storage",
        "public": False,
        "files": {
            "fruit_encoded.txt": {
                "content": text
            }
        }
    }

    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code != 201:
        raise Exception(f"Upload failed: {response.status_code}\n{response.text}")

    gist_data = response.json()
    return gist_data["files"]["fruit_encoded.txt"]["raw_url"]


# ---------------- RUN ----------------

if __name__ == "__main__":
    data = read_image_bytes(IMAGE_PATH)
    fruit_text = bytes_to_fruit(data)

    print("Preview:")
    print(fruit_text[:300])
    print("\nEncoded size (chars):", len(fruit_text))

    raw_url = upload_to_gist(fruit_text)
    print("\nRAW GIST URL:")
    print(raw_url)
