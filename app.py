from flask import Flask, render_template, request

app = Flask(__name__)

# Functions for Playfair Cipher (as defined earlier)
def generate_key_matrix(key):
    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
    key = key.upper().replace("J", "I")
    key = ''.join(sorted(set(key), key=key.index))
    matrix = []
    
    for char in key:
        if char not in matrix:
            matrix.append(char)
    
    for char in alphabet:
        if char not in matrix:
            matrix.append(char)
    
    return [matrix[i:i+5] for i in range(0, 25, 5)]

def preprocess_text(text, mode):
    text = text.upper().replace("J", "I")
    text = ''.join([char for char in text if char.isalpha()])
    
    if mode == "encrypt":
        digraphs = []
        i = 0
        while i < len(text):
            if i + 1 == len(text):
                digraphs.append(text[i] + 'X')
                break
            if text[i] == text[i + 1]:
                digraphs.append(text[i] + 'X')
                i += 1
            else:
                digraphs.append(text[i] + text[i + 1])
                i += 2
        return digraphs
    else:
        return [text[i:i+2] for i in range(0, len(text), 2)]

def find_position(matrix, char):
    for i, row in enumerate(matrix):
        if char in row:
            return i, row.index(char)
    return None

def encrypt_digraph(digraph, matrix):
    row1, col1 = find_position(matrix, digraph[0])
    row2, col2 = find_position(matrix, digraph[1])
    
    if row1 == row2:
        return matrix[row1][(col1 + 1) % 5] + matrix[row2][(col2 + 1) % 5]
    elif col1 == col2:
        return matrix[(row1 + 1) % 5][col1] + matrix[(row2 + 1) % 5][col2]
    else:
        return matrix[row1][col2] + matrix[row2][col1]

def decrypt_digraph(digraph, matrix):
    row1, col1 = find_position(matrix, digraph[0])
    row2, col2 = find_position(matrix, digraph[1])
    
    if row1 == row2:
        return matrix[row1][(col1 - 1) % 5] + matrix[row2][(col2 - 1) % 5]
    elif col1 == col2:
        return matrix[(row1 - 1) % 5][col1] + matrix[(row2 - 1) % 5][col2]
    else:
        return matrix[row1][col2] + matrix[row2][col1]

def playfair_cipher(key, text, mode):
    matrix = generate_key_matrix(key)
    digraphs = preprocess_text(text, mode)
    
    result_text = ""
    
    if mode == "encrypt":
        for digraph in digraphs:
            result_text += encrypt_digraph(digraph, matrix)
    elif mode == "decrypt":
        for digraph in digraphs:
            result_text += decrypt_digraph(digraph, matrix)
    
    return result_text

# Flask route
@app.route('/', methods=['GET', 'POST'])
def home():
    result = ""
    mode = None
    if request.method == 'POST':
        mode = request.form['mode']
        key = request.form['key']
        text = request.form['text']
        
        if key and text:
            result = playfair_cipher(key, text, mode)
        else:
            result = "Please enter both key and text."
        
    return render_template('index.html', result=result, mode=mode)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
