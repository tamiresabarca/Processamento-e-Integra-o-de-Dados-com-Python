#----------------------------
# Importação de módulos locais
#----------------------------
# Para manipulação de dados em DataFrame
import pandas as pd

# Funções para carregar e salvar dados CSV
from acesso_CSV import load_data, save_cleaned_data

# Funções de tratamento dos dados (limpeza, formatação, etc.)
from tratar_CSV import (
    clean_names, clean_emails, clean_age, clean_dates, clean_currency,
    clean_product_ids, clean_active_status, padronizar_cliente_id , remove_duplicates, padronizar_nulos_para_sql
)

# Funções para conexão com banco, criação de schema e upload de dados
from conexao_banco import connect_to_database_schema, create_schema, upload_to_database_schema

#----------------------------
# Execução principal do script
#----------------------------


# Esse bloco só será executado se o script for rodado diretamente (e não importado)
if __name__ == "__main__":

    #----------------------------
    # Configurações do projeto
    #----------------------------

    # Caminho do arquivo CSV com os dados brutos
    csv_path = 'C:/Projeto/data/dados_clientes_sujos_3000_v2.csv'

    # URL do Azure Key Vault (onde estão armazenadas as credenciais do banco)
    vault_url = "https://kv-academy-01.vault.azure.net/"

    # Nome do schema e da tabela que serão criados no banco
    schema_name = "tamires_abarca"
    table_name = "clientes_limpos"

    # Caminho onde os dados tratados serão salvos localmente
    output_path = 'C:/Projeto/data/clientes_limpos.csv'

    #----------------------------
    # 1. Carregamento dos dados
    #----------------------------
    df = load_data(csv_path)

    #----------------------------
    # 2. Limpeza e tratamento dos dados
    #----------------------------

    clean_names(df)             # Remove sujeiras dos nomes e padroniza
    clean_emails(df)            # Valida e limpa os e-mails
    clean_age(df)               # Converte idade para inteiro ou marca como ausente
    clean_dates(df)             # Padroniza o formato das datas
    clean_currency(df)          # Converte valores monetários em float
    clean_product_ids(df)       # Corrige IDs de produtos
    clean_active_status(df)     # Converte status ativo para booleano
    remove_duplicates(df)       # Remove registros duplicados
    padronizar_cliente_id(df)   # Padroniza cliente_id
    padronizar_nulos_para_sql(df) #Padroniza nulos para o SQL


    # 2.1 Visualização das 50 primeiras linhas após limpeza
    pd.set_option('display.max_columns', None)  # Mostra todas as colunas
    pd.set_option('display.width', None)        # Evita quebra de linha na impressão
    print("\n📋 Primeiras 50 linhas do DataFrame limpo:") #Imprime as primeiras 50 linhas do DF
    print(df.head(50))

    #----------------------------
    # 3. Salva os dados limpos localmente
    #----------------------------
    save_cleaned_data(df, output_path)

    #----------------------------
    # 4. Conecta ao banco de dados
    #----------------------------
    engine = connect_to_database_schema(vault_url)

    #----------------------------
    # 5. Cria o schema no banco (caso ainda não exista)
    #----------------------------
    create_schema(engine, schema_name)

    #----------------------------
    # 6. Envia os dados para o banco (tabela no schema definido)
    #----------------------------
    upload_to_database_schema(df, engine, schema_name, table_name)
