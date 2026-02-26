# 🏥 Tech Challenge Fase 4 - Análise e Previsão de Obesidade

## 📌 Sobre o Projeto
Este projeto constitui a entrega da Fase 4 do Tech Challenge da Pós-Graduação em Data Analytics da FIAP. O objetivo principal é analisar dados relacionados à obesidade e estilos de vida, extraindo insights de negócios e saúde, além de construir e colocar em produção um modelo de Machine Learning capaz de prever o nível de obesidade de um paciente com base em suas características clínicas e comportamentais.

## 🚀 Links de Entrega (Cloud)
Para uma avaliação rápida e direta na nuvem, acesse os links abaixo:
* **Aplicação Web (Streamlit Cloud):** https://tech-challenge-fase4-c7zj4zryfz8v3qxfrzybqq.streamlit.app/
* **Dashboard Analítico (Power BI):** https://app.powerbi.com/view?r=eyJrIjoiOGI5NDFlODEtNWY1ZS00YjE0LTk1OTktODRmZmY4YThiNjI1IiwidCI6ImM5NjhjZDA5LTZlODgtNDVjZi1hMzliLWQwYmExMjdjZGNmYiJ9&pageName=bb942d4a492da90ee76e

---

## 🏗️ Arquitetura e Tecnologias Utilizadas
O projeto foi desenvolvido cobrindo todo o ciclo de vida dos dados: desde a exploração inicial e modelagem, até a construção de uma arquitetura de microsserviços (Docker) e deploy em nuvem (Cloud).

* **Linguagem:** Python 3.10+
* **Exploração de Dados (EDA):** Jupyter Notebook
* **Machine Learning:** `scikit-learn`, `pandas`, `numpy` (Modelo: Random Forest Classifier - Acurácia: 94.80%)
* **Backend / API:** Flask
* **Frontend:** Streamlit
* **Orquestração:** Docker & Docker Compose
* **Data Visualization:** Power BI

## 📂 Estrutura do Repositório
* `analise.ipynb`: Notebook Jupyter contendo a Análise Exploratória de Dados (EDA), o pré-processamento, a tradução da base e os testes iniciais de validação do modelo de Machine Learning.
* `/train`: Script de treinamento do modelo de Machine Learning (`train.py`), que gera o artefato `.pkl`.
* `/api`: API em Flask responsável por receber os dados via POST e retornar a predição.
* `/streamlit`: Interface interativa local configurada para consumir a API via container Docker.
* `/deploy_cloud`: Versão adaptada da aplicação Streamlit para deploy direto no Streamlit Community Cloud (consumindo o modelo localmente sem necessidade de containers).
* `docker-compose.yml`: Orquestrador dos microsserviços locais.
* `Obesity_Traduzido_PowerBI.csv`: Base de dados tratada e traduzida (gerada após o EDA).
* `Dashboard_Obesidade.pbix`: Painel gerencial construído no Power BI.

---

## ⚙️ Como Executar o Projeto Localmente (Docker)

Para avaliar a arquitetura de microsserviços, o projeto conta com scripts de automação que previnem condições de corrida (Race Conditions) e garantem que o modelo seja treinado antes de a API ser iniciada.

### Pré-requisitos
* Docker e Docker Compose instalados.
* Git bash ou PowerShell.

### Passo a Passo Automatizado (Recomendado)
Na raiz do projeto, execute o script correspondente ao seu sistema operacional:

**Para Windows (PowerShell):**
```powershell
.\start.ps1
```
*(Caso o Windows bloqueie a execução, rode `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` antes).*

**Para Linux / macOS (Bash):**
```bash
chmod +x start.sh
./start.sh
```

### Passo a Passo Manual (Caso prefira executar comando a comando)
1. **Treinamento do Modelo:**
   ```bash
   docker-compose run trainer
   ```
2. **Subir a API e a Interface:**
   ```bash
   docker-compose up --build api streamlit
   ```
3. Acesse a aplicação no navegador via: `http://localhost:8501`

---

## 📊 Visão Analítica (Power BI)
O painel foi estruturado para responder a grandes perguntas de negócios para a Diretoria Médica:
1. **Visão Executiva:** Distribuição demográfica e impacto genético (Histórico Familiar) nos níveis de obesidade.
2. **Hábitos e Comportamento:** A influência direta do sedentarismo, tempo de telas, consumo de calorias e lanches extrarefeições na taxa de risco do paciente.
3. **Análise de Profundidade (Tooltips):** Recursos de "dica de ferramenta" para detalhar o perfil nutricional sem poluir a visão principal.

---
*Projeto desenvolvido para o Tech Challenge da FIAP.*
