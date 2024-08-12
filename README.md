## Projeto de Web Scraping Sympla e Dashboard no Looker Studio

### Descrição

Este projeto consiste em coletar dados de eventos do site da Sympla utilizando web scraping e criar um dashboard interativo no Looker Studio para visualizar e analisar os dados coletados.

### Etapas do Projeto

1. **Web Scraping:**
   - Utilizando a linguagem Python e a biblioteca BeautifulSoup, o script `web_scraping_sympla.ipynb` extrai informações como nome, data, local e categoria de eventos das páginas de categorias do Sympla.
   - Os dados são armazenados em um banco de dados SQLite (`eventos.db`) para facilitar a consulta e análise.

2. **Banco de Dados SQLite:**
   - O banco de dados `eventos.db` contém duas tabelas:
      - `Eventos`: Armazena informações únicas sobre cada evento (ID, nome, tipo).
      - `DadosEventos`: Armazena detalhes de cada evento (ID, ID do evento, data, localização).

3. **Consultas SQL:**
   - O script `consultas_sql.ipynb` executa diversas consultas SQL no banco de dados para extrair informações relevantes sobre os eventos.
   - As consultas incluem:
      - Listar todos os eventos com detalhes.
      - Listar os eventos mais próximos de iniciar.
      - Listar eventos em um local específico, exemplo Rio De Janeiro.

4. **Dashboard no Looker Studio:**
   - Os dados do banco de dados SQLite são conectados ao Looker Studio, ou arquivo csv ou xlsx através do drive.
   - Um dashboard interativo é criado para visualizar os dados de forma clara e intuitiva.
   - O dashboard inclui gráficos, tabelas e filtros para explorar os dados por diferentes categorias, datas e locais.

### Como Usar

1. **Execute o Web Scraping:**
   - Certifique-se de ter as bibliotecas `requests`, `BeautifulSoup4` e `pandas` instaladas (`pip install requests beautifulsoup4 pandas`).
   - Execute o script `web_scraping_sympla.py` para coletar os dados e armazená-los no banco de dados.

2. **Conecte ao Looker Studio:**
   - No Looker Studio, crie uma nova fonte de dados e conecte-a ao arquivo `eventos.db`, `todos_os_eventos_sympla.csv` ou `todos_os_eventos_sympla.xlsx`.
   - Crie um novo relatório e utilize os dados para construir seu dashboard.

### Link para o Dashboard

[Dashboard](https://lookerstudio.google.com/reporting/09d014a5-a245-431c-8751-2a8b11b36deb)


### Imagens do Dashboard

#### Capa:
<p align="center">
  <img alt="portifolio" src="https://github.com/LLR798/web_scraping_and_analysis_sympla_eventos/blob/main/imagens/capa.png?raw=true" width="100%">
</p>

#### Eventos:
<p align="center">
  <img alt="portifolio" src="https://github.com/LLR798/web_scraping_and_analysis_sympla_eventos/blob/main/imagens/eventos.png?raw=true" width="100%">
</p>

#### Cronograma:
<p align="center">
  <img alt="portifolio" src="https://github.com/LLR798/web_scraping_and_analysis_sympla_eventos/blob/main/imagens/cronograma.png?raw=true" width="100%">
</p>

### Considerações Finais

- Este projeto é um exemplo de como combinar web scraping com visualização de dados para obter insights sobre eventos.
