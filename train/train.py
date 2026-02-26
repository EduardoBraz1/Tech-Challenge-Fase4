# Criando modelo de Machine Learning para classificação de obesidade usando tecnica de pipline e Random Forest e salvando o modelo treinado
# Importando as bibliotecas necessárias
import pandas as pd
import os
import pickle
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OrdinalEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score

# Carregando a base de dados
df = pd.read_csv('Obesity_Base_ML.csv')

# separando as variaveis peditoras (X) e a variável alvo (y)
X = df.drop('Obesity', axis=1) # Tirei a coluna 'Obesity' do DataFrame para criar o conjunto de variáveis preditoras (X)
y = df['Obesity'] # Atribui a coluna 'Obesity' do DataFrame à variável y, que representa a variável alvo ou rótulo para o modelo de machine learning.

# Descobrindo as colunas de texto de forma automatica
colunas_texto = X.select_dtypes(include=['object']).columns.tolist()

# Criando o pipeline de pré-processamento para as colunas de texto
preprocessor = ColumnTransformer(
    transformers=[
        ('tradutor_de_texto', OrdinalEncoder(), colunas_texto) # Aplica o OrdinalEncoder às colunas de texto identificadas, convertendo os valores categóricos em números inteiros.
    ],
    remainder='passthrough'  # Mantém as colunas numéricas sem alterações
)

# Criando o pipeline completo com o pré-processamento e o modelo de classificação
pipeline = Pipeline(steps=[
    ('preparacao_dados', preprocessor), # Aplica o pré-processamento definido anteriormente para preparar os dados para o modelo de machine learning.
    ('modelo_inteligencia', RandomForestClassifier(random_state=42)) # Adiciona o modelo de classificação Random Forest ao pipeline, configurando-o com um estado aleatório para garantir a reprodutibilidade dos resultados.
])

# Dividindo os dados em conjuntos de treino e teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42) # Divide os dados em conjuntos de treino e teste, reservando 20% dos dados para teste e configurando um estado aleatório para garantir a reprodutibilidade dos resultados.

# Definindo os hiperparâmetros para o GridSearchCV
param_grid = {
    'modelo_inteligencia__n_estimators': [50, 100, 200], # Define os valores para o número de árvores na floresta (n_estimators) a serem testados durante a busca em grade.
    'modelo_inteligencia__max_depth': [None, 10, 20], # Define os valores para a profundidade máxima das árvores (max_depth) a serem testados durante a busca em grade.
    'modelo_inteligencia__min_samples_split': [2, 5, 10], # Define os valores para o número mínimo de amostras necessárias para dividir um nó (min_samples_split) a serem testados durante a busca em grade.
}

# Configurando o GridSearchCV para encontrar os melhores hiperparâmetros
grid_search = GridSearchCV(
    estimator=pipeline, # Especifica o pipeline completo como o estimador a ser otimizado durante a busca em grade.
    param_grid=param_grid, # Fornece o dicionário de hiperparâmetros a serem testados durante a busca em grade.
    scoring='accuracy', # Define a métrica de avaliação a ser usada para comparar os modelos durante a busca em grade, neste caso, a acurácia.
    cv=3, # Define o número de folds para a validação cruzada durante a busca em grade, permitindo avaliar o desempenho do modelo em diferentes subconjuntos dos dados.
    verbose=2, # Configura o nível de verbosidade para exibir informações detalhadas sobre o progresso da busca em grade.
    n_jobs=-1 # Configura o número de jobs a serem executados em paralelo durante a busca em grade, utilizando todos os processadores disponíveis para acelerar o processo de otimização dos hiperparâmetros.
)

# Treinando o modelo usando o GridSearchCV para encontrar os melhores hiperparâmetros
print("Iniciando o treinamento do modelo com GridSearchCV...")
grid_search.fit(X_train, y_train) # Ajusta o modelo usando os dados de treino, realizando a busca em grade para encontrar os melhores hiperparâmetros.

# Exibindo os melhores hiperparâmetros encontrados
print("\nMelhores Hiperparâmetros Encontrados:")
print(grid_search.best_params_) # Exibe os melhores hiperparâmetros encontrados durante a busca em grade.

# Pegando o modelo vencedor do GridSearchCV
best_model = grid_search.best_estimator_ # Atribui o modelo com os melhores hiperparâmetros encontrado durante a busca em grade à variável best_model.

# Fazendo previsão e verificando a acurácia do modelo vencedor
previsoes = best_model.predict(X_test) # Usa o modelo vencedor para fazer previsões com os dados de teste.
acuracia = accuracy_score(y_test, previsoes) # Calcula a acurácia das previsões comparando-as com os rótulos reais dos dados de teste.

print(f"\nTreinamento concluido!")
print(f"Acurácia do modelo vencedor: {acuracia * 100:.2f}%") # Exibe a acurácia do modelo vencedor em porcentagem, formatada com duas casas decimais.
print("\nRelatório de Classificação:")
print(classification_report(y_test, previsoes)) # Exibe um relatório de classificação detalhado, incluindo métricas como precisão, recall e f1-score para cada classe, comparando as previsões do modelo com os rótulos reais dos dados de teste.

# Salvando o modelo treinado usando pickle
model_path = '../model_data/pipeline_obesidade.pkl' # Define o caminho onde o modelo treinado será salvo, utilizando a extensão .pkl para indicar que é um arquivo de modelo serializado com pickle.
os.makedirs(os.path.dirname(model_path), exist_ok=True) # Cria o diretório para salvar o modelo, se ele ainda não existir, garantindo que o caminho esteja disponível para armazenar o arquivo do modelo.

with open(model_path, 'wb') as f:
    pickle.dump(best_model, f) # Salva o modelo treinado no arquivo especificado usando pickle, permitindo que ele seja carregado posteriormente para fazer previsões ou análises adicionais.

print(f"Modelo salvo com sucesso em: {model_path}") # Exibe uma mensagem confirmando que o modelo foi salvo com sucesso, indicando o caminho onde o arquivo do modelo foi armazenado.