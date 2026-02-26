# Limpa containeres antigas
Whrite-Host "Limpando o ambiente..." -ForegroundColor Yellow
docker-compose down

# Treina o modelo
Whirite-Host "Inciando o treinamento do movelo (Random Forest)..." -ForegroundColor Cyan
docker-compose run trainer

# Inicia API e Streamlit
Write-Host "Treinamento concluído! Inciando a API e o Streamlit..." -ForegroundColor Green
docker-compose up --build api streamlit