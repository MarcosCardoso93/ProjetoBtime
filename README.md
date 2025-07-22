# 🚗 Projeto Btime – Web Scraping de Tabela FIPE

Este projeto tem como objetivo realizar a extração de dados da **Tabela FIPE**, utilizando **web scraping** e **consumo de API**.

---

## 📦 Conteúdo do Projeto

- `Scrappyfipe.py` – Script para scraping via site da FIPE.
- `ApiFipe.py` – Script para coleta de dados via API da FIPE.
- `listaFipe.csv` – Planilha com códigos de veículos da FIPE.
- `RetornoConsultaApi.csv` – Resultado da consulta via API.
- `RetornoConsultaSite.csv` – Resultado da consulta via scraping.
- `requirements.txt` – Lista de bibliotecas necessárias para executar os scripts.
- `msedgedriver.exe` – Driver do Microsoft Edge (versão mais recente no momento da criação).

---

## ⚙️ Requisitos

- **Python 3.10+** (recomendado)
- **Microsoft Edge** instalado
- Conexão com a internet

> 🔄 O driver `msedgedriver.exe` é compatível com a versão atual do Edge. Caso o navegador seja atualizado, pode ser necessário substituir o driver.

---

## 🧪 Como usar

1. Instale as dependências:
   ```bash
   pip install -r requirements.txt
