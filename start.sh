#!/bin/bash
echo "Limpando o ambiente..."
docker-compose down

echo "Iniciando o treinamento do modelo (Random Forest)..."
docker-compose run trainer

echo "Treinamento concluído! Iniciando a API e a Interface Visual..."
docker-compose up --build api streamlit