# -*- coding: utf-8 -*-
from urllib.request import Request, urlopen, HTTPError, URLError
from bs4 import BeautifulSoup
import requests
import csv
import pandas as pd
import sqlite3

# URLs e tags de interesse
sites_e_tags = {
    "Festas e Shows": {
        "url": "https://www.sympla.com.br/eventos/show-musica-festa",
        "tags": ['h3.EventCardstyle__EventTitle-sc-1rkzctc-7', 'div.EventCardstyle__EventDate-sc-1rkzctc-6', 'div.EventCardstyle__EventLocation-sc-1rkzctc-8']
    },
    "Teatro e Espetáculos": {
        "url": "https://www.sympla.com.br/eventos/teatro-espetaculo",
        "tags": ['h3.EventCardstyle__EventTitle-sc-1rkzctc-7', 'div.EventCardstyle__EventDate-sc-1rkzctc-6', 'div.EventCardstyle__EventLocation-sc-1rkzctc-8']
    },
    "Passeios e Tours": {
        "url": "https://www.sympla.com.br/eventos/experiencias",
        "tags": ['h3.EventCardstyle__EventTitle-sc-1rkzctc-7', 'div.EventCardstyle__EventDate-sc-1rkzctc-6', 'div.EventCardstyle__EventLocation-sc-1rkzctc-8']
    }
}

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36"}

todos_os_eventos = []  # Lista para armazenar todos os eventos de todos os sites
id_evento = 1  # Contador de IDs

for nome_site, dados in sites_e_tags.items():
    url = dados['url']
    tags = dados['tags']

    req = Request(url, headers=headers)
    try:
        response = urlopen(req)
        html = response.read()
        soup = BeautifulSoup(html, 'html.parser')

        # Encontrando os cards dos eventos
        cards_eventos = soup.find_all('div', class_='EventCardstyle__EventCardContainer-sc-1rkzctc-0')

        for card in cards_eventos:
            nome = card.select_one(tags[0]).get_text(strip=True) if card.select_one(tags[0]) else "Nome não disponível"
            data = card.select_one(tags[1]).get_text(strip=True) if card.select_one(tags[1]) else "Data não disponível"
            local = card.select_one(tags[2]).get_text(strip=True) if card.select_one(tags[2]) else "Local não disponível"

            todos_os_eventos.append({
                'ID': id_evento,
                'Nome': nome,
                'Data': data,
                'Local': local,
                'Categoria': nome_site  # Adicionando a categoria
            })
            id_evento += 1

    except HTTPError as e:
        print(f"Erro HTTP em {nome_site}: {e.reason}")
    except URLError as e:
        print(f"Erro URL em {nome_site}: {e.reason}")

# Criando um DataFrame e salvando em CSV
df = pd.DataFrame(todos_os_eventos)
df.to_csv('todos_os_eventos.csv', index=False)

############################
##### Ajuste no DF: ######
############################
# Carregar o CSV (substitua pelo caminho do seu arquivo)
df = pd.read_csv('todos_os_eventos.csv')

# Dicionário para mapear meses abreviados
meses_abreviados = {'Jan': 1, 'Fev': 2, 'Mar': 3, 'Abr': 4, 'Mai': 5, 'Jun': 6,
                    'Jul': 7, 'Ago': 8, 'Set': 9, 'Out': 10, 'Nov': 11, 'Dez': 12}

# Função para extrair e formatar a data (corrigida)
def extrair_e_formatar_data(texto):
    try:
        _, data_hora = texto.split(', ')  # Ignorar o dia da semana
        data, _ = data_hora.split(' · ')    # Ignorar o horário
        dia, mes_abrev = data.split(' ')
        ano = '2024'  # Definir o ano (você pode ajustar isso)
        mes = meses_abreviados[mes_abrev]
        data_str = f'{dia}/{mes}/{ano}'
        return pd.to_datetime(data_str, format='%d/%m/%Y').strftime('%d/%m/%Y')
    except (ValueError, IndexError, KeyError):
        # Extrair dia e mês abreviado
        dia = texto[:2]
        mes_abrev = texto[3:6]

        # Verificar se são valores numéricos e alfabéticos válidos
        if not dia.isdigit() or not mes_abrev.isalpha():
            return None

        ano = '2024'  # Definir o ano (você pode ajustar isso)
        mes = meses_abreviados[mes_abrev.title()]  # Converter para título (ex: "Jun" -> "Jun")
        data_str = f'{dia}/{mes}/{ano}'
        return pd.to_datetime(data_str, format='%d/%m/%Y').strftime('%d/%m/%Y')
        # return None  # Retornar None para entradas inválidas

# Aplicar a função e criar a nova coluna
df['Data_formatada'] = df['Data'].astype(str).apply(extrair_e_formatar_data)

# Imprimir as colunas Data e Data_formatada para verificar o resultado
print(df[['Data', 'Data_formatada']])

# Renomear a coluna 'Data_formatada' para 'Data Formatada'
df = df.rename(columns={'Data_formatada': 'Data Formatada'})
df_corrigido = df.drop("Data", axis=1)
df_corrigido = df_corrigido.rename(columns={'Data Formatada': 'Data'})
df_corrigido.to_csv('todos_os_eventos.csv', index=False)


############################
##### BANCO DE DADOS: ######
############################

# Lendo o CSV com os dados dos eventos
df = pd.read_csv('todos_os_eventos.csv')

# Conectando ao banco de dados SQLite (criará um novo arquivo se não existir)
conn = sqlite3.connect('eventos.db')
conn = sqlite3.connect('dados_eventos.db')
cursor = conn.cursor()

# Criando as tabelas
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Eventos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        tipo TEXT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS DadosEventos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        evento_id INTEGER,
        data TEXT,
        localizacao TEXT,
        FOREIGN KEY(evento_id) REFERENCES Eventos(id)
    )
''')

# Inserindo os dados na tabela Eventos (sem duplicatas)
eventos_unicos = df[['Nome', 'Categoria']].drop_duplicates().rename(columns={'Categoria': 'tipo'})
eventos_unicos.to_sql('Eventos', conn, if_exists='append', index=False)

# Obtendo os IDs dos eventos inseridos
eventos_ids = pd.read_sql_query("SELECT id, nome FROM Eventos", conn)
eventos_ids = eventos_ids.set_index('nome').to_dict()['id']

# Adicionando a coluna evento_id ao DataFrame original
df['evento_id'] = df['Nome'].map(eventos_ids)

# Inserindo os dados na tabela DadosEventos
dados_eventos = df[['evento_id', 'Data', 'Local']].rename(columns={'Data': 'data', 'Local': 'localizacao'})
dados_eventos.to_sql('DadosEventos', conn, if_exists='append', index=False)

print("Dados inseridos com sucesso no banco de dados SQLite!")