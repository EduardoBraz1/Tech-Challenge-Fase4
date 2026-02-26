# Escolha do sistema operacional base
FROM python:3.9-slim

# Definir o diretório de trabalho dentro do container
WORKDIR /app

# Copiar os arquivos de requisitos para o container
COPY requirements.txt .

# Instalar as dependências
RUN pip install -r requirements.txt

# Copiar o código da aplicação para o container
COPY . .

# Executar o script de treinamento
CMD ["python", "app.py"]