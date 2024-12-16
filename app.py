from flask import Flask, request, jsonify, render_template
import json
from datetime import datetime

app = Flask(__name__)

def load_data():
    with open('data.json', 'r') as file:
        return json.load(file)
def save_data(data):
    with open('data.json', 'w') as file:
        json.dump(data, file, indent=2)

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/book', methods=['GET'])
def register():
    data = load_data()
    return jsonify(data), 200

#EndSession
@app.route('/reset', methods=['GET'])
def reset():
    data = load_data()
    for entry in data:
        entry["REMARKS"] = ""
        entry["LOG IN TIME"] = ""
        entry["DATE"] = ""
    save_data(data)
    return jsonify({"message": "All values reset successfully."}), 200

#Process
@app.route('/attendance', methods=['GET'])
def handle():
    data=load_data()
    uid = request.args.get('uid')
    roll_number = request.args.get('rollno')

    if not uid or not roll_number:
        return jsonify({"error": "Missing uid or roll_number parameter"}), 400

    user = next((item for item in data if item["ROLL NO."] == roll_number), None)

    if not user:
        return jsonify({"message": "Not registered"}), 404

    if user["UID"] != uid:
        user["REMARKS"] = "tampered"
        with open('data.json', 'w') as file:
            json.dump(data, file, indent=2)
        return jsonify({"message": "ID not matched"}), 403

    user["REMARKS"] = "Present"
    user["LOG IN TIME"] = datetime.now().strftime("%H:%M")
    user["DATE"] = datetime.now().strftime("%Y-%m-%d")


    save_data(data)
    return jsonify({"message": "Marked"}), 200

#midwork
@app.route('/markabsent', methods=['GET'])
def mark_absent():
    data = load_data()
    current_time = datetime.now().strftime("%H:%M")
    current_date = datetime.now().strftime("%Y-%m-%d")

    for entry in data:
        if not entry.get("REMARKS"):
            entry["REMARKS"] = "Absent"
            entry["LOG IN TIME"] = current_time
            entry["DATE"] = current_date

    save_data(data)
    return jsonify({"message": "Access time ended"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=80)
    