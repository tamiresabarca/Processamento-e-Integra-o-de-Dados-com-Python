# Importa a biblioteca necessária para manipulação de dados
import pandas as pd

# Carrega diretamente o arquivo CSV — mas essa linha provavelmente está aqui só para testar (ver observação abaixo)
csv_path = pd.read_csv('C:/Projeto/data/dados_clientes_sujos_3000_v2.csv')  


#---------------------------------------------#
# Função para carregar dados de um arquivo CSV
#---------------------------------------------#
def load_data(csv_path):
    """Carrega os dados do arquivo CSV informado no caminho."""

    try:
        df = pd.read_csv(csv_path)  # Tenta carregar os dados a partir do caminho do arquivo
        print("✅ Dados carregados com sucesso.")
        return df  # Retorna o DataFrame carregado
    except Exception as e:
        # Caso ocorra algum erro (ex: arquivo não encontrado, erro de leitura, etc)
        print(f"❌ Erro ao carregar os dados: {e}")
        raise  # Levanta o erro novamente para interromper o fluxo, se necessário

#-----------------------------------------------------#
# Função para salvar os dados tratados em um novo CSV
#-----------------------------------------------------#
def save_cleaned_data(df, output_path):
    """Salva os dados tratados no caminho informado como CSV."""

    try:
        df.to_csv(output_path, index=False)  # Salva o DataFrame como CSV, sem o índice
        print(f"✅ Dados salvos com sucesso em '{output_path}'.")
    except Exception as e:
        # Caso ocorra algum erro durante a gravação (ex: permissão negada, caminho inválido, etc)
        print(f"❌ Erro ao salvar os dados: {e}")
        raise  # Levanta o erro novamente para depuração
