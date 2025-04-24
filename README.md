# Projeto: Processamento e Integração de Dados com Python

## Descrição

Este projeto realiza a extração, tratamento e carregamento de dados em um banco de dados SQL Server hospedado no Azure. O objetivo é transformar dados brutos contidos em um arquivo CSV, limpá-los, padronizá-los e armazená-los em uma tabela no banco para análise e uso futuro.
A autenticação e o acesso aos dados sensíveis são realizados de forma segura via integração com o Azure Key Vault.

---

## Tecnologias e Bibliotecas

- Python 3.13.2
- Pandas
- NumPy
- SQLAlchemy
- pyodbc
- re (expressões regulares)
- azure-identity
- azure-keyvault-secrets
- UUID
- Logging
---

## Estrutura de Pastas

```
├── data/                      # Arquivos CSV de entrada e saída
├── docs/                      # Relatório final (PDF ou .md)
├── src/                       # Código-fonte do projeto
│   ├── acesso_CSV.py          # Funções para carregar e salvar arquivos CSV
│   ├── conexao_banco.py       # Conexão com banco de dados via Azure Key Vault
│   ├── main.py                # Script principal com execução do pipeline completo
│   └── tratar_CSV.py          # Funções de limpeza e padronização dos dados
├── requirements.txt           # Lista de bibliotecas utilizadas
└── README.md                  # Este arquivo

```

---

## Como Executar

1. Clone este repositório (ou baixe como zip)
2. Instale as dependências com:

```
pip install -r requirements.txt
```

3. Execute o script principal (em `src/`) via terminal ou IDE (como VS Code):

```
python src/main.py

```

### O que o script faz:
1. Lê um arquivo CSV contendo dados de clientes
2. Remove duplicatas baseados em chegagem de multiplos campos como `nome_cliente`, `email` e `produto_id`
3. Padroniza formatos (emails, datas, moedas, etc.)
4. Gera identificadores únicos (UUIDs)
5. Salva um arquivo CSV com a limpeza realizada
6. Padroniza valores nulos para compatibilidade com SQL
7. Cria um schema `tamires_abarca`
8. Sobe os dados tratados para a tabela `clientes_limpos` no SQL Server
---

## Configurações Sensíveis

A string de conexão está armazenada com o nome de segredo no Azure Key Vault (ex: `conexao_SQL_azure`).

A aplicação usa `DefaultAzureCredential` para autenticar automaticamente com a conta logada no ambiente.

---

## Funcionalidades

- **Leitura de dados**: Carrega os dados de um arquivo CSV com registros de clientes.

- **Tratamento dos dados**:
  - **Nomes**: Remove títulos como "Sr.", "Dra." e corrige a capitalização.
  - **E-mails**: Valida formatos e trata e-mails ausentes ou inválidos.
  - **Idades**: Converte valores numéricos e trata valores faltantes ou incorretos evidenciando os nulos.
  - **Datas**: Detecta e converte diferentes formatos de data e evidencia datas nulas.
  - **Valores monetários**: Converte valores como "R$ 1.200,00" para float.
  - **IDs de produto**: Padroniza como distintos e evidencia nulos em IDs.
  - **Status ativo**: Converte para booleano os valores "sim", "não", "1", "0" e evidencia nulos.
  - **ID do cliente**: Gera identificadores únicos para cada cliente com base em UUID.
  - **Remoção de duplicatas**: Remove linhas repetidas considerando nome, e-mail, ID do produto e valor da compra.

- **Exportação**: Salva os dados tratados em um novo arquivo CSV.

- **Integração com o Azure**:
  - Conexão segura com o banco via **Azure Key Vault** (sem expor senhas).
  - Envio dos dados limpos para uma tabela no SQL Server dentro do schema `tamires_abarca`.

---

## Autor

Tamires Aline Silva Abarca  
Projeto desenvolvido para a Blue Academy - Desafio Individual