# Criando a aplicação Flask para servir o modelo de machine learning treinado
# Importando as bibliotecas necessárias
from flask import Flask, request, jsonify
from pydantic import BaseModel, ValidationError
import pandas as pd
import pickle

app = Flask(__name__)

# Carregando o modelo treinado
pipeline_path = '../model_data/pipeline_obesidade.pkl'  # Caminho para o arquivo do pipeline treinado

with open(pipeline_path, 'rb') as f:
    pipeline = pickle.load(f)

# Criando classe de modelo de dados para validação de entrada usando Pydantic
class InputData(BaseModel):
    Gender: str
    Age: int
    Height: float
    Weight: float
    family_history: str
    FAVC: str
    FCVC: int
    NCP: int
    CAEC: str
    SMOKE: str
    CH2O: int
    SCC: str
    FAF: int
    TUE: int
    CALC: str
    MTRANS: str

# Criando a porta de entrada para a API
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Recebendo os dados de entrada em formato JSON
        input_data = InputData(**request.get_json())  # Valida os dados de entrada usando Pydantic

        # Convertendo os dados de entrada para um DataFrame do Pandas
        df_input = pd.DataFrame([input_data.model_dump()])  # Converte os dados validados para um DataFrame, preparando-os para a previsão usando o modelo de machine learning

        # Fazendo a previsão usando o modelo carregado
        prediction = pipeline.predict(df_input)

        # Retornando a previsão como resposta JSON
        return jsonify({
            "status": 200,
            "data": {"prediction": str(prediction[0])}
        }), 200
    
    except ValidationError as e:
        # Retornando erros de validação de entrada
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        print(f"\n--- ERRO INTERNO NA API ---")
        print(str(e))
        print("------------------------------------\n")
        return jsonify({"error": f"erro interno: {str(e)}"}), 500
    
if __name__ == '__main__':
    # Iniciando a aplicação Flask
    app.run(host='0.0.0.0', port=5000)