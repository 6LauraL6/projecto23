from flask import Flask, render_template, request, jsonify,redirect, url_for
import pandas as pd
import matplotlib.pyplot as plt

app = Flask(__name__, static_url_path='/static')

# Cargar los datos del archivo CSV
data = pd.read_csv('data/heart-attack-prediction.csv')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data')
def data_page():
    return render_template('data.html')

@app.route('/api/data', methods=['GET'])
def get_all_data():
    return jsonify(data.to_dict(orient='records'))

@app.route('/api/data/<column>/<value>', methods=['GET'])
def get_data_by_filter(column, value):
    filtered_data = data[data[column] == value]
    return jsonify(filtered_data.to_dict(orient='records'))

@app.route('/api/data', methods=['POST'])
def create_data():
    new_data = request.get_json()
    data = data.append(new_data, ignore_index=True)
    return jsonify({'message': 'Datos creados exitosamente'})

@app.route('/api/data/<int:patient_id>', methods=['PUT'])
def update_data(patient_id):
    updated_data = request.get_json()
    global data
    data.loc[data['Patient ID'] == patient_id] = updated_data
    return jsonify({'message': 'Datos actualizados exitosamente'})
    

@app.route('/api/data/<int:patient_id>', methods=['DELETE'])
def delete_data(patient_id):
    global data
    data = data[data['Patient ID'] != patient_id]
    return jsonify({'message': 'Datos eliminados exitosamente'})

@app.route('/data/country_rank')
def country_rank():
    country_counts = data['Country'].value_counts().head(5)
    plt.bar(country_counts.index, country_counts.values, color="#287e1d")
    plt.xlabel('País')
    plt.ylabel('Número de Pacientes')
    plt.title('Ránking de Países con Más Pacientes')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('static/country_rank.png')

    return render_template('data.html', country_rank=True)

@app.route('/api/services_page', methods=['GET'])
def get_api_services():
    services = [
        {
            'name': 'Obtener todos los datos',
            'url': '/api/data',
            'description': 'Obtener todos los datos del dataset.'
        },
        {
            'name': 'Filtrar datos por columna y valor',
            'url': '/api/data/<column>/<value>',
            'description': 'Obtener datos filtrados por columna y valor.'
        }
        # Agrega más servicios si es necesario
    ]

    if request.headers.get('accept') == 'application/json':
        return jsonify(services)
    else:
        return render_template('api_services.html', services=services)

@app.route('/data/distribution')
def data_distribution():
    data = pd.read_csv('data/heart-attack-prediction.csv')
    
    plt.figure(figsize=(12, 10))

    # Gráfico 1 - Distribución de Edad
    plt.hist(data['Age'], bins=20, color='skyblue')
    plt.title('Distribución de Edad')
    plt.xlabel('Edad')
    plt.ylabel('Frecuencia')
    plt.savefig('static/age_distribution.png')
    plt.close()

    # Gráfico 2 - Distribución de Presión Arterial
    plt.figure(figsize=(12, 10))
    plt.hist(data['Blood Pressure'], bins=20, color='salmon')
    plt.title('Distribución de Presión Arterial en Reposo')
    plt.xlabel('Presión Arterial en Reposo')
    plt.ylabel('Frecuencia')
    plt.savefig('static/blood_pressure_distribution.png')
    plt.close()

    # Gráfico 3 - Distribución de Colesterol
    plt.figure(figsize=(12, 10))
    plt.hist(data['Cholesterol'], bins=20, color='lightgreen')
    plt.title('Distribución de Colesterol')
    plt.xlabel('Colesterol')
    plt.ylabel('Frecuencia')
    plt.savefig('static/cholesterol_distribution.png')
    plt.close()

    return render_template('data_distribution.html')



if __name__ == '__main__':
    app.run(debug=True)
