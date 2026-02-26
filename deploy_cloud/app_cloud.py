# Streamlit para visualizar os dados de obesidade e prever a obesidade na nuvem (Cloud version)
# Importando as bibliotecas necessárias
import streamlit as st
import pandas as pd
import pickle

# Configurando a pagina
st.set_page_config(page_title="Diagnóstico de Obesidade", page_icon="🏥", layout="centered")

# ------------ Carregando o modelo diretamente ------------
@st.cache_resource
def load_model():
    with open("pipeline_obesidade.pkl", 'rb') as f:
        return pickle.load(f)

pipeline = load_model()
# -------------------------------------------------------

st.title("🏥 Sistema Preditivo de Obesidade")
st.write("Preencha os dados clínicos do paciente para prever o nível de obesidade.")

# Criando os campos de entrada
st.header("Dados do Paciente")

col1, col2 = st.columns(2) # Dividindo a tela em duas colunas para organizar os campos de entrada

with col1:
    gender = st.selectbox("Gênero", options=["Male", "Female"], format_func=lambda x: "Masculino" if x == "Male" else "Feminino") # Campo de seleção para o gênero do paciente, com opções "Masculino" e "Feminino"
    age = st.number_input("Idade", min_value=14, max_value=100, value=25, step=1) # Campo de entrada numérica para a idade do paciente, com um intervalo de 14 a 100 anos e um valor padrão de 25 anos
    height = st.number_input("Altura (metros)", min_value=1.00, max_value=2.50, value=1.70, step=0.01) # Campo de entrada numérica para a altura do paciente em metros, com um intervalo de 1.00 a 2.50 metros e um valor padrão de 1.70 metros
    weight = st.number_input("Peso (kg)", min_value=30.0, max_value=200.0, value=70.0, step=0.1) # Campo de entrada numérica para o peso do paciente em kg, com um intervalo de 30.0 a 200.0 kg e um valor padrão de 70.0 kg
    family_history = st.selectbox("Histórico Familiar de Sobrepeso?", options=["yes", "no"], format_func=lambda x: "Sim" if x == "yes" else "Não") # Campo de seleção para indicar se o paciente tem histórico familiar de sobrepeso, com opções "Sim" e "Não"
    favc = st.selectbox("Consome alimentos de alta caloria?", options=["yes", "no"], format_func=lambda x: "Sim" if x == "yes" else "Não") # Campo de seleção para indicar se o paciente consome alimentos de alta caloria, com opções "Sim" e "Não"
    fcvc = st.selectbox("Frequência de vegetais consumidos por dia?", options=[1, 2, 3], format_func=lambda x: "1 - raramente" if x == 1 else ("2 - às vezes" if x == 2 else "3 - sempre")) # Campo de seleção para indicar a frequência de consumo de vegetais por dia, com opções "1 - raramente", "2 - às vezes" e "3 - sempre"
    ncp = st.selectbox("Número de refeições principais", options=[1, 2, 3, 4], format_func=lambda x: f"{x} refeições principais") # Campo de seleção para indicar o número de refeições principais do paciente, com opções de 1 a 4 refeições principais

with col2:
    caec = st.selectbox("Consome alimentos entre as refeições?", options=["no", "Sometimes", "Frequently", "Always"], format_func=lambda x: {"no": "Não", "Sometimes": "Às vezes", "Frequently": "Frequentemente", "Always": "Sempre"}[x]) # Campo de seleção para indicar a frequência de consumo de alimentos entre as refeições, com opções "Não", "Às vezes", "Frequentemente" e "Sempre"
    smoke = st.selectbox("Fuma?", options=["yes", "no"], format_func=lambda x: "Sim" if x == "yes" else "Não") # Campo de seleção para indicar se o paciente fuma, com opções "Sim" e "Não"
    ch2o = st.selectbox("Consumo diário de água", options=[1, 2, 3], format_func=lambda x: {1: "< 1 Litro", 2: "1 a 2 Litros", 3: "> 2 Litros"}[x]) # Campo de seleção para indicar o consumo diário de água do paciente, com opções "< 1 Litro", "1 a 2 Litros" e "> 2 Litros"
    scc = st.selectbox("Monitora ingestão calórica?", options=["yes", "no"], format_func=lambda x: "Sim" if x == "yes" else "Não") # Campo de seleção para indicar se o paciente monitora a ingestão calórica, com opções "Sim" e "Não"
    faf = st.selectbox("Atividade física (dias por semana)", options=[0, 1, 2, 3], format_func=lambda x: {0: "Nenhuma", 1: "1 a 2 dias", 2: "3 a 4 dias", 3: "5 ou mais dias"}[x]) # Campo de seleção para indicar a frequência de atividade física do paciente por semana, com opções "Nenhuma", "1 a 2 dias", "3 a 4 dias" e "5 ou mais dias"
    tue = st.selectbox("Tempo de telas", options=[0, 1, 2], format_func=lambda x: {0: "0 a 2h/dia", 1: "3 a 5h/dia", 2: "> 5h/dia"}[x]) # Campo de seleção para indicar o tempo diário de telas do paciente, com opções "0 a 2h/dia", "3 a 5h/dia" e "> 5h/dia"
    calc = st.selectbox("Consumo de álcool", options=["no", "Sometimes", "Frequently", "Always"], format_func=lambda x: {"no": "Não bebe", "Sometimes": "Às vezes", "Frequently": "Frequentemente", "Always": "Sempre"}[x]) # Campo de seleção para indicar a frequência de consumo de álcool do paciente, com opções "Não", "Às vezes", "Frequentemente" e "Sempre"
    mtrans = st.selectbox("Meio de transporte principal", options=["Automobile", "Motorbike", "Bike", "Public_Transportation", "Walking"], format_func=lambda x: {"Automobile": "Carro", "Motorbike": "Moto", "Bike": "Bicicleta", "Public_Transportation": "Transporte Público", "Walking": "A pé"}[x]) # Campo de seleção para indicar o meio de transporte principal do paciente, com opções "Automóvel", "Motocicleta", "Bicicleta", "Transporte Público" e "Caminhada"

st.markdown("---") # Linha horizontal para separar os campos de entrada da seção de previsão

# Criando o botão de previsão
if st.button("Realizar Previsão", type="primary", width="stretch"): # Botão para realizar a previsão, com estilo primário e largura total do contêiner
    
    # Preparando os dados de entrada para a API
    input_data = {
        "Gender": gender,
        "Age": age,
        "Height": height,
        "Weight": weight,
        "family_history": family_history,
        "FAVC": favc,
        "FCVC":fcvc,
        "NCP": ncp,
        "CAEC": caec,
        "SMOKE": smoke,
        "CH2O": ch2o,
        "SCC": scc,
        "FAF": faf,
        "TUE": tue,
        "CALC": calc,
        "MTRANS": mtrans
    }

    # Enviando os dados para a API e obtendo a previsão
    try:
        # Convertendo os dados de entrada em um DataFrame para o pipeline
        input_df = pd.DataFrame([input_data])
        
        # Realizando a previsão usando o pipeline carregado
        diagnostico = pipeline.predict(input_df)[0]

        # Traduzindo o resultado da previsão para uma mensagem mais amigável
        traducao = {
            "Insufficient_Weight": "Abaixo do Peso",
            "Normal_Weight": "Peso Normal",
            "Overweight_Level_I": "Sobrepeso Nível I",
            "Overweight_Level_II": "Sobrepeso Nível II",
            "Obesity_Type_I": "Obesidade Tipo I",
            "Obesity_Type_II": "Obesidade Tipo II",
            "Obesity_Type_III": "Obesidade Tipo III"
        }

        st.success(f"**Diagnóstico Preditivo:** {traducao.get(diagnostico, diagnostico)}") # Exibindo o resultado da previsão em uma mensagem de sucesso, traduzida para uma forma mais amigável
        st.balloons() # Exibindo balões de celebração para tornar a experiência mais divertida

    except Exception as e:
        st.error(f"Erro ao realizar a predição. Detalhes: {str(e)}") # Exibindo uma mensagem de erro caso ocorra algum problema durante a predição, mostrando os detalhes do erro para ajudar na resolução