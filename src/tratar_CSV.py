#-------------------------------------------
# Bibliotecas necessárias
#-------------------------------------------
import pandas as pd # Biblioteca para manipulação de dados em formato de tabelas (DataFrames)
import re           # Biblioteca para trabalhar com expressões regulares (útil para limpeza de texto)
import numpy as np  # Biblioteca para operações numéricas e tratamento de valores nulos
import uuid         # Biblioteca para gerar identificadores únicos universais (UUID)

#-------------------------#
# 1. Limpeza de Nomes
#-------------------------#
def clean_names(df):
    try:
        def limpar_nome(nome): #Função auxiliar que será aplicada a cada nome individualmente
            if pd.isna(nome):  # Verifica se o valor é nulo (NaN), e se for, retorna como está
                return nome
            nome = nome.strip() # Remove espaços em branco do início e fim
            if '.' in nome:     # Se houver ponto (.), como em "Sr. João", separa o nome
                nome = nome.split('.', 1)[1]  # Remove a parte antes do ponto (ex: "Sr.")
            nome = nome.lower()               # Converte o nome para letras minúsculas
            nome = re.sub(r'\s+', ' ', nome).strip() # Remove espaços duplicados e limpa início/fim
            if re.fullmatch(r'[a-zA-Z]\.?', nome):  # Se o nome for só uma letra (como "A."), considera inválido
                return ''
            return nome.title() # Coloca a primeira letra de cada palavra em maiúscula (formato título)

        df['nome_cliente'] = df['nome_cliente'].apply(limpar_nome)  # Aplica a função `limpar_nome` na coluna 'nome_cliente' do DataFrame
        print("✅ Nomes limpos e padronizados.") # Mensagem de sucesso
    except Exception as e:
        print(f"❌ Erro ao limpar nomes: {e}") # Em caso de erro, exibe a mensagem

#-------------------------#
# 2. Validação de E-mails
#-------------------------#
def clean_emails(df): # Valida e trata os e-mails no DataFrame
    try:
        regex_email = r'^[\w\.-]+@[\w\.-]+\.\w+$' # Expressão regular para verificar se o e-mail tem um formato válido (ex: nome@dominio.com)

        def tratar_email(email):  # Função auxiliar que será aplicada a cada e-mail individualmente
            if pd.isna(email) or email.strip() == "":      # Verifica se o valor é nulo ou está em branco
                return 'E-mail inválido ou não cadastrado' # Retorna mensagem padrão para valores ausentes
            elif not re.match(regex_email, email):         # Se não combinar com o padrão da regex
                return f'E-mail "{email}" inválido'        # Retorna uma mensagem específica com o valor original
            return email                                   # Se for válido, retorna o e-mail original

        df['email'] = df['email'].apply(tratar_email)      # Aplica a função `tratar_email` na coluna 'email' do DataFrame
        print("✅ E-mails validados e tratados.")         # Mensagem de sucesso
    except Exception as e:
        print(f"❌ Erro ao validar e-mails: {e}")         # Em caso de erro, exibe a mensagem

#-------------------------#
# 3. Limpeza de Idades
#-------------------------#

# Limpa e padroniza a coluna de idades
def clean_age(df):
    try:
        # Função auxiliar que trata cada valor de idade individualmente
        def ajustar_idade(valor):
            if pd.isna(valor) or str(valor).strip() == "":  # Verifica se o valor está ausente ou é uma string vazia
                return np.nan                               # Retorna NaN (valor nulo do NumPy)
            try:
                return int(float(valor))                    # Converte o valor para float e depois para inteiro
            except (ValueError, TypeError):                 # Captura erros de conversão (ex: texto inválido)
                return np.nan                               # Retorna NaN em caso de erro

        # Aplica a função `ajustar_idade` na coluna 'idade' e converte a coluna para o tipo inteiro que aceita nulos (Int64)
        df['idade'] = df['idade'].apply(ajustar_idade).astype('Int64')

        print("✅ Idades limpas e padronizadas.")            # Mensagem de sucesso
    except Exception as e:
        print(f"❌ Erro ao limpar idades: {e}")              # Em caso de erro, exibe a mensagem

#-------------------------#
# 4. Formatação de Datas
#-------------------------#

# Converte e padroniza as datas no DataFrame
def clean_dates(df):
    try:
        # Identifica as colunas do DataFrame que contêm a palavra 'data' no nome (ignorando maiúsculas/minúsculas)
        colunas_data = [col for col in df.columns if 'data' in col.lower()]
        
        # Lista de formatos possíveis para datas a serem reconhecidas
        formatos_possiveis = ['%d/%m/%Y', '%Y/%m/%d', '%m/%d/%Y', 
                              '%d-%m-%Y', '%Y-%m-%d', '%m-%d-%Y']

        # Função auxiliar que tenta converter um valor para data
        def converter_data(valor):
            if pd.isna(valor) or str(valor).strip() == "":  # Verifica se o valor é nulo ou uma string vazia
                return pd.NaT                             # Retorna um valor nulo de data (pd.NaT)
            # Tenta converter o valor para data em cada um dos formatos possíveis
            for formato in formatos_possiveis:
                try:
                    return pd.to_datetime(valor, format=formato, errors='raise')  # Converte para data
                except (ValueError, TypeError):  # Captura erros caso o formato não seja compatível
                    continue  # Continua tentando os próximos formatos
            return pd.NaT  # Retorna NaT (Not a Time) se nenhum formato for compatível

        # Aplica a função `converter_data` em todas as colunas que contêm 'data' no nome
        for col in colunas_data:
            df[col] = df[col].apply(converter_data)

        print("✅ Datas convertidas.")  # Mensagem de sucesso
    except Exception as e:
        print(f"❌ Erro ao converter datas: {e}")  # Mensagem de erro caso ocorra uma exceção


#-------------------------#
# 5. Conversão de Moeda
#-------------------------#

# Converte valores monetários para formato numérico (float)
def clean_currency(df):
    try:
        # Função auxiliar que limpa e converte o valor monetário
        def limpar_moeda(valor):
            if pd.isnull(valor):  # Verifica se o valor é nulo
                return np.nan  # Retorna um valor nulo (np.nan) se o valor for nulo
            # Remove qualquer caractere que não seja número ou vírgula (ex: R$, espaços, etc.)
            valor_limpo = re.sub(r'[^\d,]', '', str(valor))
            # Substitui a vírgula (,) por ponto (.) para que seja compatível com o formato float
            valor_limpo = valor_limpo.replace(',', '.')
            # Converte a string limpa para um número decimal (float)
            return float(valor_limpo)

        # Aplica a função `limpar_moeda` na coluna 'valor_compra' do DataFrame
        df['valor_compra'] = df['valor_compra'].apply(limpar_moeda)

        print("✅ Valores monetários convertidos.")  # Mensagem de sucesso
    except Exception as e:
        print(f"❌ Erro ao converter moeda: {e}")  # Mensagem de erro caso ocorra uma exceção


#-------------------------#
# 6. Padronização de IDs
#-------------------------#

# Padroniza os IDs de produtos (tornando-os em maiúsculo e tratando valores nulos)
def clean_product_ids(df):
    try:
        # Função auxiliar que realiza a padronização do valor do ID
        def padronizar_id(valor):
            if pd.isna(valor) or str(valor).strip() == "":  # Verifica se o valor é nulo ou está vazio
                return np.nan  # Retorna um valor nulo (np.nan) se o valor for nulo ou vazio
            return str(valor).strip().upper()  # Remove espaços antes e depois do valor, e transforma em maiúsculo

        # Aplica a função `padronizar_id` na coluna 'produto_id' do DataFrame
        df['produto_id'] = df['produto_id'].apply(padronizar_id)

        print("✅ IDs de produtos padronizados.")  # Mensagem de sucesso indicando que a padronização foi realizada
    except Exception as e:
        print(f"❌ Erro ao padronizar produto_id: {e}")  # Em caso de erro, exibe uma mensagem indicando a falha


#-------------------------#
# 7. Padroniza valor 'ativo'
#-------------------------#

# Padroniza o status de "ativo" (converte para valores booleanos ou nulos)
def clean_active_status(df):
    try:
        # Função auxiliar que padroniza o valor do status de ativo
        def padronizar_ativo(valor):
            if pd.isna(valor) or str(valor).strip() == "":  # Verifica se o valor é nulo ou está vazio
                return np.nan  # Retorna um valor nulo (np.nan) se o valor for nulo ou vazio

            # Define os valores que serão considerados como "True" e "False"
            valores_true = {"1", "sim", "true", "yes"}
            valores_false = {"0", "não", "no", "false"}

            valor_str = str(valor).strip().lower()  # Converte o valor para uma string minúscula e remove espaços

            # Verifica se o valor está entre os valores de "True" e retorna True
            if valor_str in valores_true:
                return True
            # Verifica se o valor está entre os valores de "False" e retorna False
            elif valor_str in valores_false:
                return False
            return np.nan  # Retorna np.nan se o valor não for um valor válido para "True" ou "False"

        # Aplica a função `padronizar_ativo` na coluna 'ativo' do DataFrame
        df['ativo'] = df['ativo'].apply(padronizar_ativo)

        print("✅ Status 'ativo' padronizado.")  # Mensagem de sucesso indicando que a padronização foi realizada
    except Exception as e:
        print(f"❌ Erro ao padronizar status 'ativo': {e}")  # Em caso de erro, exibe uma mensagem indicando a falha


#-------------------------#
# 8. Geração de ID Cliente
#-------------------------#

# Função que gera um identificador único para cada cliente, utilizando UUID
def padronizar_cliente_id(df):
    """
    Gera IDs únicos para os clientes na coluna 'cliente_id' usando UUID.
    Garante que os valores sejam únicos no DataFrame e estão prontos para subir ao SQL Server.
    """
    try:
        # Verifica se o DataFrame foi fornecido e se não está vazio
        if df is None or df.empty:
            raise ValueError("DataFrame está vazio ou não foi fornecido.")  # Levanta um erro caso o DataFrame esteja vazio

        # Geração de UUIDs únicos para cada cliente
        cliente_ids = [str(uuid.uuid4()) for _ in range(len(df))]  # Cria uma lista de UUIDs convertidos para string

        # Verifica se há duplicatas nos UUIDs gerados (é improvável, mas é uma verificação de segurança)
        if len(cliente_ids) != len(set(cliente_ids)):
            raise ValueError("Colisão de UUIDs detectada. Refaça a geração.")  # Levanta um erro caso haja duplicatas

        # Adiciona a coluna 'cliente_id' ao DataFrame com os UUIDs gerados
        df['cliente_id'] = cliente_ids

        print("✅ 'cliente_id' gerado com UUIDs únicos e seguros.")  # Mensagem de sucesso indicando que a geração foi bem-sucedida

    except Exception as e:
        print(f"❌ Erro ao gerar cliente_id: {e}")  # Em caso de erro, exibe uma mensagem indicando a falha


#-------------------------#
# 9. Remoção de Duplicatas
#-------------------------#

# Função que identifica e remove duplicatas no DataFrame, com base em múltiplas colunas.
def remove_duplicates(df):
    try:
        # Identificar duplicatas com base nas colunas 'nome_cliente', 'email', 'produto_id' e 'valor_compra'.
        # O parâmetro keep=False faz com que todas as duplicatas sejam marcadas, não apenas a última ou a primeira.
        duplicatas = df[df.duplicated(subset=['nome_cliente', 'email', 'produto_id', 'valor_compra'], keep=False)]
        
        # Verifica se existem duplicatas no DataFrame
        if not duplicatas.empty:
            print("⚠️ Linhas duplicadas encontradas:")  # Mensagem de alerta caso existam duplicatas
            print(duplicatas)  # Exibe as duplicatas encontradas no DataFrame
        else:
            print("✅ Nenhuma duplicata encontrada.")  # Mensagem de sucesso caso não haja duplicatas

        # Remove as duplicatas, mantendo apenas a primeira ocorrência em cada conjunto de duplicados
        df = df.drop_duplicates(subset=['nome_cliente', 'email', 'produto_id', 'valor_compra'], keep='first')

        print("✅ Duplicatas removidas.")  # Mensagem de sucesso indicando que as duplicatas foram removidas
        return df  # Retorna o DataFrame após a remoção das duplicatas

    except Exception as e:
        print(f"❌ Erro ao remover duplicatas: {e}")  # Em caso de erro, exibe uma mensagem indicando o que ocorreu
        return df  # Retorna o DataFrame original em caso de erro

#-------------------------#
# 10. Padronizar Nulos para SQL
#-------------------------#

# Função que padroniza os valores nulos de acordo com os tipos de dados para garantir compatibilidade com o SQL.
def padronizar_nulos_para_sql(df):
    try:
        # Itera sobre cada coluna do DataFrame
        for col in df.columns:
            # Verifica se a coluna é do tipo datetime (data e hora)
            if pd.api.types.is_datetime64_any_dtype(df[col]):
                # Para valores nulos na coluna de data, substitui por None (valor nulo compatível com SQL)
                df[col] = df[col].where(df[col].notna(), None)
            
            # Verifica se a coluna é do tipo inteiro ou ponto flutuante (numérico)
            elif pd.api.types.is_integer_dtype(df[col]) or pd.api.types.is_float_dtype(df[col]):
                # Se a coluna for numérica, mantém o valor como está (não altera os nulos)
                df[col] = df[col]
            
            # Verifica se a coluna é do tipo booleano
            elif pd.api.types.is_bool_dtype(df[col]):
                # Para valores booleanos, mantém os valores nulos como estão
                df[col] = df[col]
            
            # Para qualquer outro tipo de dado (como strings, objetos, etc.)
            else:
                # Para valores nulos em outras colunas, substitui por None
                df[col] = df[col].where(df[col].notna(), None)

        # Mensagem de sucesso indicando que os nulos foram padronizados
        print("✅ Nulos padronizados para envio ao SQL.")
        
        # Retorna o DataFrame após a padronização dos nulos
        return df

    except Exception as e:
        # Em caso de erro, exibe uma mensagem de erro
        print(f"❌ Erro ao padronizar nulos para SQL: {e}")
        
        # Retorna o DataFrame original em caso de erro
        return df

