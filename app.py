from flask import Flask, jsonify, request
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Функция для получения данных METAR в формате JSON
def get_weather_data(airport_code, data_format):
    base_url = f"http://metartaf.ru/{airport_code}.{data_format}"
    response = requests.get(base_url)

    if response.status_code == 200:
        if data_format == 'json':
            return response.json()
        elif data_format == 'xml':
            return response.content  # для XML-ответа
    else:
        return None

# Эндпоинт для получения данных в формате JSON
@app.route('/weather/json/<airport_code>', methods=['GET'])
def get_weather_json(airport_code):
    data = get_weather_data(airport_code, 'json')
    if data:
        return jsonify(data)
    else:
        return jsonify({"error": "Data not found"}), 404

# Эндпоинт для получения данных в формате XML
@app.route('/weather/xml/<airport_code>', methods=['GET'])
def get_weather_xml(airport_code):
    data = get_weather_data(airport_code, 'xml')
    if data:
        return app.response_class(data, mimetype='application/xml')
    else:
        return jsonify({"error": "Data not found"}), 404


# @app.route('/task2.html',methods=['POST','GET'])
# def get_metar():
#     if requests.method == 'POST':
#         user = request.form['icao']
#         return redirect
    




if __name__ == '__main__':
    app.run(debug=True) 