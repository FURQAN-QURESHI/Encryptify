import streamlit as st

st.set_page_config(page_title="Encryptify", page_icon="🔒", layout="centered")

st.markdown("""
    <style>
        body {
            margin: 0;
            padding: 0;
        }
        .main { 
            background-color: #2E2E2E; 
            color: Blue;
            font-family: 'Arial', sans-serif;
            padding: 15px;
        }

         /* Center the button and set its width */
        .stButton {
            display: flex;
            justify-content: center;
            align-items: center;
        }

        .stButton>button {
            border-radius: 10px;
            background-color: #007BFF;
            color: white;
            font-weight: bold;
            width: 150px;  /* Set the width of the button */
            padding: 10px;
            margin: 0 auto;  /* Ensures the button is centered */
        }
        .stRadio>div>label, .stSelectbox>div>label {
            color: white;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
<div style='text-align: center; font-size: 40px; font-weight: bold; color: orange;'>
    Encryptify
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style="color:Yellow; font-size: 18px; margin-bottom: 0px;">
    Select Category:
</div>
""", unsafe_allow_html=True)

category = st.selectbox("", ["Substitution", "Transposition"], label_visibility="collapsed")
st.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)

# Add Encryption/Decryption mode selection
st.markdown("""
<div style="color:yellow; font-size: 18px; margin-bottom: 0px;">
    Choose Mode:
</div>
""", unsafe_allow_html=True)

mode = st.radio("", ["Encryption", "Decryption"], horizontal=True, label_visibility="collapsed")
st.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)

# Cipher functions - Encryption

def monoalphabetic_encrypt(plaintext, key):
    if len(key) != 26:
        return "Error: Key must be 26 characters (A-Z)"
    
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    cipher_text = ""
    
    for char in plaintext:
        if char.upper() in alphabet:
            idx = alphabet.find(char.upper())
            cipher_text += key[idx] if char.isupper() else key[idx].lower()
        else:
            cipher_text += char
    return cipher_text

def monoalphabetic_decrypt(ciphertext, key):
    if len(key) != 26:
        return "Error: Key must be 26 characters (A-Z)"
    
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    plain_text = ""
    
    # Track if we're at the start of a sentence
    is_start = True
    
    for char in ciphertext:
        if char.upper() in key.upper():
            idx = key.upper().find(char.upper())
            # Keep original case (rather than deriving from input case)
            if is_start:
                plain_text += alphabet[idx]  # Make first letter uppercase
                is_start = False
            else:
                plain_text += alphabet[idx] if char.isupper() else alphabet[idx].lower()
        else:
            plain_text += char
            # Reset sentence tracking after period, question mark, or exclamation mark
            if char in ['.', '!', '?']:
                is_start = True
    return plain_text

def polyalphabetic_encrypt(plaintext, key):
    if not key:
        return "Error: Key is required"
    
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    cipher_text = ""
    key = key.upper()
    key_idx = 0
    
    for char in plaintext:
        if char.upper() in alphabet:
            shift = alphabet.find(key[key_idx % len(key)])
            idx = alphabet.find(char.upper()) + shift
            cipher_text += alphabet[idx % 26] if char.isupper() else alphabet[idx % 26].lower()
            key_idx += 1
        else:
            cipher_text += char
    return cipher_text

def polyalphabetic_decrypt(ciphertext, key):
    if not key:
        return "Error: Key is required"
    
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    plain_text = ""
    key = key.upper()
    key_idx = 0
    
    for char in ciphertext:
        if char.upper() in alphabet:
            shift = alphabet.find(key[key_idx % len(key)])
            idx = alphabet.find(char.upper()) - shift
            plain_text += alphabet[idx % 26] if char.isupper() else alphabet[idx % 26].lower()
            key_idx += 1
        else:
            plain_text += char
    return plain_text

def generate_playfair_matrix(key):
    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"  # No J (replaced with I)
    key = key.upper().replace('J', 'I')
    
    # Remove spaces and punctuation from key
    key = ''.join(char for char in key if char.isalpha())
    
    # Remove duplicates while preserving order
    key = ''.join(dict.fromkeys(key))
    
    # Create matrix
    matrix = []
    used_chars = set()
    
    # First fill with key characters
    for char in key:
        if char not in used_chars and char in alphabet:
            matrix.append(char)
            used_chars.add(char)
    
    # Then fill with remaining alphabet characters
    for char in alphabet:
        if char not in used_chars:
            matrix.append(char)
            used_chars.add(char)
    
    # Convert to 5x5 matrix
    return [matrix[i*5:(i+1)*5] for i in range(5)]

def find_position(matrix, letter):
    letter = 'I' if letter == 'J' else letter
    for i, row in enumerate(matrix):
        if letter in row:
            return i, row.index(letter)
    return -1, -1  # Should not happen if matrix is properly formed

def playfair_encrypt(plaintext, key):
    if not key:
        return "Error: Key is required"
    
    matrix = generate_playfair_matrix(key)
    
    # Prepare plaintext - remove non-alphabetic chars, convert to uppercase, replace J with I
    cleaned_text = ''.join(char for char in plaintext if char.isalpha())
    cleaned_text = cleaned_text.upper().replace('J', 'I')
    
    # Split into digraphs
    i = 0
    digraphs = []
    while i < len(cleaned_text):
        if i == len(cleaned_text) - 1:
            # Last single character
            digraphs.append(cleaned_text[i] + 'X')
            break
        
        # Check if pair has same letters
        if cleaned_text[i] == cleaned_text[i+1]:
            digraphs.append(cleaned_text[i] + 'X')
            i += 1
        else:
            digraphs.append(cleaned_text[i] + cleaned_text[i+1])
            i += 2
    
    cipher_text = ""
    for digraph in digraphs:
        row1, col1 = find_position(matrix, digraph[0])
        row2, col2 = find_position(matrix, digraph[1])
        
        if row1 == row2:  # Same row
            cipher_text += matrix[row1][(col1+1)%5] + matrix[row2][(col2+1)%5]
        elif col1 == col2:  # Same column
            cipher_text += matrix[(row1+1)%5][col1] + matrix[(row2+1)%5][col2]
        else:  # Rectangle
            cipher_text += matrix[row1][col2] + matrix[row2][col1]
    
    return cipher_text

def playfair_decrypt(ciphertext, key):
    if not key:
        return "Error: Key is required"
    
    matrix = generate_playfair_matrix(key)
    
    # Prepare ciphertext - remove non-alphabetic chars, convert to uppercase
    cleaned_text = ''.join(char for char in ciphertext if char.isalpha())
    cleaned_text = cleaned_text.upper().replace('J', 'I')
    
    # Handle odd length (should not happen in properly encrypted text, but just in case)
    if len(cleaned_text) % 2 != 0:
        cleaned_text = cleaned_text[:-1]  # Remove last character
    
    # Split into digraphs
    digraphs = [cleaned_text[i:i+2] for i in range(0, len(cleaned_text), 2)]
    
    plain_text = ""
    for digraph in digraphs:
        if len(digraph) != 2:
            continue
            
        row1, col1 = find_position(matrix, digraph[0])
        row2, col2 = find_position(matrix, digraph[1])
        
        if row1 == row2:  # Same row
            plain_text += matrix[row1][(col1-1)%5] + matrix[row2][(col2-1)%5]
        elif col1 == col2:  # Same column
            plain_text += matrix[(row1-1)%5][col1] + matrix[(row2-1)%5][col2]
        else:  # Rectangle
            plain_text += matrix[row1][col2] + matrix[row2][col1]
    
    # Remove padding X's at the end or between identical letters
    result = ""
    i = 0
    while i < len(plain_text):
        # Add the current character
        result += plain_text[i]
        
        # Check if we're at the end or if the next character is 'X'
        if i+1 < len(plain_text):
            if plain_text[i+1] != 'X':
                result += plain_text[i+1]
            # Only add X if it's not a padding character (not at end and not between identical letters)
            elif i+2 < len(plain_text) and plain_text[i] != plain_text[i+2]:
                result += 'X'
        
        i += 2
    
    # Convert to more natural case (first letter capitalized, rest lowercase)
    if result:
        result = result[0] + result[1:].lower()
    
    return result

def vigenere_encrypt(plaintext, key):
    return polyalphabetic_encrypt(plaintext, key)

def vigenere_decrypt(ciphertext, key):
    return polyalphabetic_decrypt(ciphertext, key)

def rail_fence_encrypt(plaintext, key):
    if not key or key <= 1:
        return "Error: Key must be greater than 1"
    
    fence = [[] for _ in range(key)]
    rail = 0
    direction = 1
    
    for char in plaintext:
        fence[rail].append(char)
        rail += direction
        if rail == 0 or rail == key - 1:
            direction *= -1
    
    return ''.join([''.join(rail) for rail in fence])

def rail_fence_decrypt(ciphertext, key):
    if not key or key <= 1:
        return "Error: Key must be greater than 1"
    
    # Create empty fence with placeholder
    fence = [[''] * len(ciphertext) for _ in range(key)]
    
    # Mark positions in fence
    rail = 0
    direction = 1
    for i in range(len(ciphertext)):
        fence[rail][i] = '*'
        rail += direction
        if rail == 0 or rail == key - 1:
            direction *= -1
    
    # Fill fence with characters
    index = 0
    for i in range(key):
        for j in range(len(ciphertext)):
            if fence[i][j] == '*' and index < len(ciphertext):
                fence[i][j] = ciphertext[index]
                index += 1
    
    # Read off plaintext
    result = []
    rail = 0
    direction = 1
    for i in range(len(ciphertext)):
        result.append(fence[rail][i])
        rail += direction
        if rail == 0 or rail == key - 1:
            direction *= -1
    
    return ''.join(result)

def columnar_transposition_encrypt(plaintext, key):
    if not key:
        return "Error: Key is required"
    
    # Remove spaces from the key
    key = ''.join(key.split())
    
    # Keep the original plaintext with spaces
    cleaned_text = plaintext
    
    # Create columns based on key length
    columns = [''] * len(key)
    
    # Fill columns
    for i, char in enumerate(cleaned_text):
        columns[i % len(key)] += char
    
    return ''.join(columns)

def columnar_transposition_decrypt(ciphertext, key):
    if not key:
        return "Error: Key is required"
    
    # Remove spaces from the key
    key = ''.join(key.split())
    
    # Calculate dimensions
    key_length = len(key)
    text_length = len(ciphertext)
    
    # Number of rows needed
    full_columns = text_length // key_length
    partial_columns = text_length % key_length
    total_rows = full_columns + (1 if partial_columns > 0 else 0)
    
    # Create a matrix of the right size
    matrix = [['' for _ in range(key_length)] for _ in range(total_rows)]
    
    # Fill the matrix from the ciphertext
    pos = 0
    for col in range(key_length):
        # Determine how many cells to fill in this column
        col_height = full_columns + (1 if col < partial_columns else 0)
        for row in range(col_height):
            if pos < text_length:
                matrix[row][col] = ciphertext[pos]
                pos += 1
    
    # Read the plaintext row by row
    plaintext = ''
    for row in range(total_rows):
        for col in range(key_length):
            if matrix[row][col]:  # Check if cell contains a character
                plaintext += matrix[row][col]
    
    return plaintext

# Technique Selection
st.markdown("""
<div style="color:yellow; font-size: 18px; margin-bottom: 0px;">
    Choose Technique
</div>
""", unsafe_allow_html=True)

technique = st.radio(
    "",
    ["Monoalphabetic", "Polyalphabetic", "Playfair", "Vigenère"] if category == "Substitution" else ["Rail Fence", "Columnar Transposition"],
    horizontal=True,
    label_visibility="collapsed"
)

input_label = "Enter plain text here..." if mode == "Encryption" else "Enter cipher text here..."
st.markdown(f"""
<div style="color:yellow; font-size: 18px; margin-bottom: 0px;">
    {input_label}
</div>
""", unsafe_allow_html=True)

input_text = st.text_area("", height=150, label_visibility="collapsed")

st.markdown("""
<style>
/* Remove Streamlit default outer white container */
section[data-testid="stTextArea"] {
    background-color: transparent !important;
    box-shadow: none !important;
    padding: 0 !important;
    border: none !important;
}

/* Remove internal box white border */
section[data-testid="stTextArea"] > div:first-child {
    background-color: transparent !important;
    border: none !important;
    box-shadow: none !important;
    padding: 0 !important;
}

/* Style the real input field */
section[data-testid="stTextArea"] textarea {
    background-color: #2e2e2e !important;
    color: white !important;
    border: 2px white !important;
    border-radius: 10px !important;
    padding: 10px !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div style="color:yellow; font-size: 18px; margin-bottom: 0px;">
    Enter Cipher Key (if applicable)
</div>
""", unsafe_allow_html=True)

key = st.text_input("", "", label_visibility="collapsed")

button_text = "Encrypt" if mode == "Encryption" else "Decrypt"
result_label = "Encrypted text:" if mode == "Encryption" else "Decrypted text:"

if st.button(button_text):
    if input_text:
        result_text = ""
        
        if mode == "Encryption":
            if category == "Substitution":
                if technique == "Monoalphabetic":
                    result_text = monoalphabetic_encrypt(input_text, key)
                elif technique == "Polyalphabetic":
                    result_text = polyalphabetic_encrypt(input_text, key)
                elif technique == "Playfair":
                    result_text = playfair_encrypt(input_text, key)
                elif technique == "Vigenère":
                    result_text = vigenere_encrypt(input_text, key)
            else:  # Transposition
                if technique == "Rail Fence":
                    try:
                        result_text = rail_fence_encrypt(input_text, int(key) if key.isdigit() else 0)
                    except:
                        result_text = "Invalid Key! Enter a positive number."
                elif technique == "Columnar Transposition":
                    result_text = columnar_transposition_encrypt(input_text, key)
        else:  # Decryption
            if category == "Substitution":
                if technique == "Monoalphabetic":
                    result_text = monoalphabetic_decrypt(input_text, key)
                elif technique == "Polyalphabetic":
                    result_text = polyalphabetic_decrypt(input_text, key)
                elif technique == "Playfair":
                    result_text = playfair_decrypt(input_text, key)
                elif technique == "Vigenère":
                    result_text = vigenere_decrypt(input_text, key)
            else:  # Transposition
                if technique == "Rail Fence":
                    try:
                        result_text = rail_fence_decrypt(input_text, int(key) if key.isdigit() else 0)
                    except:
                        result_text = "Invalid Key! Enter a positive number."
                elif technique == "Columnar Transposition":
                    result_text = columnar_transposition_decrypt(input_text, key)

        st.markdown(f"""
        <div style="color:yellow; font-size: 18px; margin-bottom: 0px;">
            {result_label}
        </div>
        """, unsafe_allow_html=True)
        
        st.text_area("", value=result_text, height=150, label_visibility="collapsed")
    else:
        st.warning(f"Please enter text to {button_text.lower()}.")