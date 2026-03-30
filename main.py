import pandas as pd
import json
from openai import OpenAI
import requests
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
json_url = str(os.getenv("WEB_DATABASE_URL"))
json_caminho_arquivo = "usuarios.json"
arquivo_com_ids = "SDW2023.csv"
openai_api_key = os.getenv("OPENAI_API_KEY")
news_icon_address = ""



def ler_json_da_internet(data_address: str) -> list[dict] | None:
    #carrega o arquivo json hospedado na url data_address
    #returna uma lista com os valores lidos ou None se ocorrer erro de leitura

    elementos = []
    try:
        response = requests.get(data_address)
        # Gere uma exceção para códigos de status inválidos. (4XX ou 5XX)
        response.raise_for_status()
        # Converte a resposta JSON em um objeto Python (geralmente um dicionário ou uma lista).
        elementos = response.json()

    #trata as exceções de obter a URL do arquivo e de decodificar o JSON obtido
    except requests.exceptions.RequestException as e:
        print(f"Erro ao obter o URL: {e}")
        return None
    except ValueError as e:
        print(f"Erro ao decodificar o JSON: {e}")
        return None
    
    #verifica se retornou o tipo esperado(lista ou dicionário)
    if( type(elementos) == type({}) or type(elementos) == type([]) ) :        
        # se retornou dicionário, converte para lista com um elemento        
        if type(elementos) == type({}):
            elementos = [elementos]
        return list(elementos)          
    else:    
        print("Resposta da requisição json retornou objeto diferente de dicionário ou lista de dicionários")
        return None
    
def ler_json_arquivo_local(caminho: str) -> list[dict] | None:
    #carrega o arquivo json localizado no caminho definido pela entrada
    #returna uma lista com os valores lidos ou None se ocorrer erro de leitura

    elementos = []
    try:
        # tenta abrir o arquivo e carregar os dados
        with open(caminho, 'r', encoding='utf-8') as f:
            elementos = json.load(f)

    #trata as exceções de arquivo não encontrado e falha ao decodificar o json
    except FileNotFoundError:
        print(f"Error: The file {caminho} was not found.")
        return None
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from the file {caminho}. Check for invalid syntax.")
        return None
    
    #verifica se retornou o tipo esperado(lista ou dicionário)
    if( type(elementos) == type({}) or type(elementos) == type([]) ) :
        # se retornou dicionário, converte para lista com um elemento
        if type(elementos) == type({}):
            elementos = [elementos]
        return list(elementos)          
    else:    
        print("Resposta da requisição json retornou objeto diferente de dicionário ou lista de dicionários")
        return None

def create_description(user:dict):
    response = client.responses.create(
    model="gpt-5.4",
    input=[
      {
          "role": "system",
          "content": "Você é um especialista em markting bancário."
      },
      {
          "role": "user",
          "content": f"Crie uma mensagem para {user['name']} sobre a importância dos investimentos (máximo de 100 caracteres)"
      }
     ]
    )
    return response.output_text


# tenta ler os arquivos com ids, se encontrar erro, atribui [] a ele
try:
    ids = pd.read_csv(arquivo_com_ids).iloc[ : , 0].to_list()
except:
    print("Erro ao ler o arquivo com ids")
    ids = []

# recupera a lista de usuários obtidas do arquivo json da web
usuarios1 = ler_json_da_internet(json_url)

# caso tenha havido falha na leitura, nenhum usuário foi retornado
if usuarios1 is None:
    usuarios1 = []


# recupera a lista de usuários obtidas do arquivo json local
usuarios2 = ler_json_arquivo_local(json_caminho_arquivo)

#caso tenha havido falha na leitura, nenhum usuário foi retornado
if usuarios2 is None:
    usuarios2 = []

# reune todos os usuários em uma só lista
todos_os_usuarios = usuarios1 + usuarios2

#atualiza o campo news dos usuários cuja id está em ids
for id in ids:
    #procura a id em todos os usuários
    for usuario in todos_os_usuarios:
        if(usuario["id"] == id):
            #prepara a nova entrada
            news_id = len(usuario["news"]) + 1
            description = create_description(usuario)
            # criar uma nova entrada no campo news do usário
            usuario["news"].append(
                {
                    "id": news_id, 
                    "icon": news_icon_address,
                    "description": description
                }
            )
            break


# Cria ou abre o arquivo usuarios_updated no modo escrita  ('w') 
# e json.dump() para guardar os dados atualizados dos clientes
# se o arquivo já existir, ele será sobrescrito

try:
    with open('usuarios_updated.json', 'w', encoding='utf-8') as json_file:
        # deve-se usar a opção ensure_ascii=False para garantir que todos 
        # os caracteres sejam exibidos corretamente no arquivo
        json.dump(todos_os_usuarios, json_file, indent=4, ensure_ascii=False)
except:
    print("Falha ao criar o arquivo json atualizado")
    exit()

print("Arquivo criado com sucesso")      

