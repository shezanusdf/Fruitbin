import requests

raw_url = "https://gist.githubusercontent.com/shezanusdf/17c7c883ed4299798ec17c7302cc6404/raw/e234338a5fc481338b20592769b2247ef5a2d0fb/fruit_encoded.txt" # GIST URL GOES HERE

FRUIT_TO_BITS = {
    "🍌": "00",
    "🍑": "01",
    "🍍": "10",
    "🥝": "11",
}


def fetch_encoded_text(raw_url):
    response = requests.get(raw_url)
    encoded_text = response.text        
    return encoded_text
    
def extract_bitstream(encoded_text):
    bits = []
    
    for char in encoded_text:
        if char in FRUIT_TO_BITS:
            bits.append(FRUIT_TO_BITS[char])
    return "".join(bits)


bitstream = extract_bitstream(fetch_encoded_text(raw_url))

def bitstream_to_bytes(bitstream):
    byte_array = bytearray()

    for i in range(0, len(bitstream), 8):
        byte_bits = bitstream[i:i+8]
        byte_value = int(byte_bits, 2)
        byte_array.append(byte_value)

    return bytes(byte_array)

with open("decoded.png", "wb") as f:
    f.write(bitstream_to_bytes(bitstream))


