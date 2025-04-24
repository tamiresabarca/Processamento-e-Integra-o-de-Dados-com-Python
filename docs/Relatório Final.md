
# Relatório Final - Processamento e Integração de Dados com Python

## Resumo Executivo
Este relatório apresenta um pipeline de dados desenvolvido em Python para tratar e integrar um conjunto de dados de clientes, originalmente em formato CSV, com destino a um banco de dados SQL Server hospedado na Azure. O processo envolveu a limpeza, padronização e exportação dos dados, com foco na segurança e reutilização do código.

## Data
Abril de 2025

## Objetivo
Este projeto tem como objetivo transformar dados brutos contidos em um arquivo CSV, limpando e padronizando essas informações para posterior carregamento seguro em um banco de dados SQL Server hospedado na Azure. O foco é garantir a qualidade, integridade e segurança dos dados ao longo de todo o processo.

## Tecnologias Utilizadas
- **Python** (Pandas, NumPy, Regex)
- **SQLAlchemy** + **pyodbc** (para conexão com SQL Server)
- **Azure Key Vault** + **Azure Identity** (para segurança)


## Etapas Realizadas

### 1. Análise Inicial dos Dados
- Leitura do arquivo CSV com dados de clientes
- Verificação de colunas com valores ausentes
- Identificação e contagem de duplicatas

### 2. Limpeza e Padronização dos Dados
- **Nomes**: Remoção de títulos (ex: "Sr.", "Dra."), padronização para capitalização correta e remoção de espaços extras;
- **E-mails**: Validação com expressões regulares e substituição por mensagens padrão nos casos inválidos;
- **Idade**: Conversão para tipo numérico (inteiro) e padronização de vazios e nulos;
- **Datas**: Normalização de formato, suportando entradas variadas e padronização de vazios e nulos;
- **Valores Monetários**: Remoção de símbolos, substituição de vírgulas por pontos, conversão para tipo float;
- **IDs de Produto**: Padronização para letras maiúsculas e remoção de espaços mantendo os valores como distintos com padronização de vazios e nulos;
- **Campo Ativo**: Conversão de valores como "sim", "1", "true" em `True`, e "não", "0" em `False` e padronização dos vazios e nulos;
- **Criação de `cliente_id`**: Geração de ID único para cada cliente com base em UUID;
- **Remoção de Duplicatas**: Aplicada com base nas colunas `nome_cliente`, `email`, `produto_id` e `valor_compra`.

### 3. Padronização de Dados
- Uniformização de nulos com `np.nan` para evitar erro de tipagem ao subir ao banco.


## 4. Carregamento de Dados

- Criação de **schema `tamires_abarca`** no SQL Server.
- Upload para a tabela `clientes_limpos` utilizando `to_sql()` do SQLAlchemy com `schema='tamires_abarca'`.

```python
df.to_sql(
    name=table_name,
    con=engine,
    schema=schema_name,
    if_exists='replace',
    index=False
)
```

- Conexão com o banco feita com string retirada do Azure Key Vault:
  - Nome do segredo: `conexao_SQL_azure`
  - Autenticação via `DefaultAzureCredential`

---
## Segurança

- Não há senhas ou strings de conexão expostas no código.
- Toda autenticação é feita via Azure Identity com acesso ao Key Vault.

---

### 5. Modularização do Código
O projeto foi estruturado em módulos Python organizados por responsabilidade (leitura de dados, tratamento e conexão com o banco), seguindo boas práticas de engenharia. Isso facilita a manutenção, testes e reutilização futura.

---

## Resultados
- Dados tratados e consistentes, prontos para análise ou uso em relatórios
- Minimização de erros comuns em sistemas baseados em entrada manual de dados
- Garantia de segurança no acesso a credenciais e manipulação de dados sensíveis
- Scripts prontos para reaproveitamento em novos datasets

---

## Aprendizados

- Modularização do código Python para reuso e organização.
- Boas práticas com Azure (Key Vault + SQL + Auth).
- Tratamento de dados com foco em integridade para bancos relacionais.
- Automatização de processos com pipeline em `main.py`.


**Autora**: Tamires Aline Silva Abarca  
**Projeto desenvolvido para**: Blue Academy - Desafio Individual
