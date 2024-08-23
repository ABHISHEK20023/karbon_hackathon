from flask import Flask, request, render_template
import json
from model import probe_model_5l_profit

app = Flask(__name__)

@app.route('/', methods=['GET'])
def upload_page():
    return render_template('upload.html')

@app.route('/submit', methods=['POST'])
def submit():
    file = request.files['file']
    if file:
        try:
            content = file.read().decode('utf-8')
            data = json.loads(content)
            
            # Debugging print statements
            print("Received data:", data)
            
            if "financials" not in data["data"]:
                return "Invalid data format. Missing 'financials' key.", 400
            
            results = probe_model_5l_profit(data["data"])
            return render_template('results.html', results=results)
        except json.JSONDecodeError:
            return "Invalid JSON file.", 400
        except Exception as e:
            return str(e), 500
    return "No file uploaded.", 400

if __name__ == "__main__":
    app.run(debug=True)
