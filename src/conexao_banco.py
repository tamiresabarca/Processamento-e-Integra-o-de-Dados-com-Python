#-------------------------------------------
# Bibliotecas necessárias
#-------------------------------------------
from azure.identity import DefaultAzureCredential # Faz autenticação automática com a Azure (ex: identidade gerenciada, login local etc)
from azure.keyvault.secrets import SecretClient   # Cliente para acessar segredos (como senhas) no Azure Key Vault
from sqlalchemy import create_engine, text        # create_engine cria conexão com banco de dados / text permite comandos SQL seguros
import pandas as pd                               # Biblioteca para manipulação de dados em tabelas (DataFrames)
import urllib                                     # Usada para codificar strings de conexão (ex: substituir caracteres especiais por códigos URL)

#---------------------------------------------------
# Conexão com o banco usando Azure Key Vault
#---------------------------------------------------
def connect_to_database_schema(vault_url):
    """
    Conecta ao banco de dados SQL Server usando segredos do Key Vault.
    Retorna um SQLAlchemy engine.
    """
    credential = DefaultAzureCredential()
    client = SecretClient(vault_url=vault_url, credential=credential)

    # Recupera os segredos
    secret_database = client.get_secret("db-academy-database").value
    secret_server = client.get_secret("db-academy-server").value


    # Monta a connection string com urllib para encoding
     # Monta a connection string com urllib para encoding correto
    params = urllib.parse.quote_plus(
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={secret_server};"
        f"DATABASE={secret_database};"
        f"Authentication=ActiveDirectoryInteractive;"
        f"Encrypt=yes;"
        f"TrustServerCertificate=no;"
    )

    # Cria engine
    engine = create_engine(f"mssql+pyodbc:///?odbc_connect={params}")
    print("✅ Conexão com o banco de dados estabelecida.")
    return engine

 # Nome do schema e da tabela que serão criados no banco
schema_name = "tamires_abarca"
table_name = "clientes_limpos"

#---------------------------------------------------
# Criação de schema no banco, se não existir
#---------------------------------------------------
def create_schema(engine, schema_name):
    """
    Cria o schema no banco de dados, caso ainda não exista.
    """

    # Abre uma conexão com o banco de dados usando o engine fornecido
    with engine.connect() as conn:
        try:
            # Executa uma consulta para verificar se o schema já existe no banco
            result = conn.execute(text("""
                SELECT SCHEMA_NAME
                FROM INFORMATION_SCHEMA.SCHEMATA
                WHERE SCHEMA_NAME = :schema_name
            """), {"schema_name": schema_name})  # Usa parâmetro para evitar SQL injection

            # Se o schema não foi encontrado, cria um novo
            if not result.fetchone():  # Se não retornar nenhuma linha, o schema não existe
                conn.execute(text(f"CREATE SCHEMA {schema_name}"))  # Cria o schema no banco
                print(f"✅ Schema '{schema_name}' criado com sucesso.")  # Confirma criação
            else:
                print(f"ℹ️ Schema '{schema_name}' já existe.")  # Informa que já existe
        except Exception as e:
            print(f"❌ Erro ao criar o schema '{schema_name}': {e}")  # Mostra erro, se ocorrer
            raise  # Repassa o erro para possível tratamento externo


#---------------------------------------------------
# Upload de dados para o banco dentro do schema
#---------------------------------------------------
def upload_to_database_schema(df, engine, schema_name, table_name):
    """
    Envia os dados para o banco, criando a tabela no schema especificado.
    """
    try:
        # Envia o DataFrame para o banco de dados usando o método to_sql
        df.to_sql(
            name=table_name,          # Nome da tabela que será criada ou substituída
            con=engine,               # Conexão com o banco de dados (SQLAlchemy engine)
            schema=schema_name,       # Nome do schema onde a tabela será criada
            if_exists='replace',      # Substitui a tabela se ela já existir
            index=False               # Não envia o índice do DataFrame como coluna
        )
        # Mensagem de sucesso ao concluir o envio
        print(f"✅ Dados enviados com sucesso para '{schema_name}.{table_name}'.")
    except Exception as e:
        # Em caso de erro, imprime a mensagem com detalhes
        print(f"❌ Erro ao enviar os dados para '{schema_name}.{table_name}': {e}")
        raise  # Relança o erro para tratamento externo, se necessário
