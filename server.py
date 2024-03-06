import os
import json
from flask import Flask, render_template, request, jsonify
import parser

app = Flask(__name__, template_folder='templates')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/parse', methods=['POST'])
def parse():
    try:
        if "file_path" not in request.files:
            return jsonify({
                "error": "no file included in the request"
            }), 400

        file = request.files["file_path"]

        if file.filename == "":
            return jsonify({
                "error": "no selected file"
            }), 400

        upload_folder = os.path.join(os.getcwd(), 'uploads')
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)
        file_path = os.path.join(upload_folder, file.filename)
        file.save(file_path)

        bencoded_file, bencoded_file_size = parser.read_bencoded_file(file_path)
        parsed_bencoded_file, _ = parser.parse_bencoded(bencoded_file, 0)
        parsed_bencoded_file = parser.convert_bytes_to_strings(parsed_bencoded_file)
        jason = json.dumps(parsed_bencoded_file, indent=4)
        jason_response = jsonify(json.loads(jason))
        return jason_response
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)


"""
        # Print the form data
        print(request.form)
        print(request.data)

        for file_key in request.files:
            file = request.files[file_key]
            print(f"Uploaded File: {file.filename}, Content Type: {file.content_type}, Size: {len(file.read())} bytes")

        file_path = request.form['file_path']
        print(f'File path: {file_path}', fuck)
"""