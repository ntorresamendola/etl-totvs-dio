
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![ChatGPT](https://img.shields.io/badge/chatGPT-74aa9c?style=for-the-badge&logo=openai&logoColor=white)


# 📖 Sobre o Projeto

Este projeto foi desenvolvido para o bootcamp **"TOTVS - Fundamentos de Engenharia de Dados e Machine Learning"**, oferecido pela **DIO**. Trata-se de um projeto que visa demonstrar o pipeline ETL para dados, que são extraídos de um arquivo JSON hospedado na internet e de um arquivo JSON local(arquivo "usuarios.json"), ambos contendo dados bancários fictícios de usuários de banco.

Cada usuário contém o campo 'id', 'name', 'account', 'card', 'features' e 'news'. O objetivo é juntar os dados de todos os usários e atualizar o campo "news" de todos os usuário cujos id's estejam no arquivo "SDW2023.csv", adicionando uma nova entrada sobre investimentos, gerada usando a API do ChatGPT. Os outros usuários não devem ser modificados.

No final, é gerado um novo arquivo JSON localmente com os dados atualizados, chamado de "usuarios_updated.json"

# ⚙️Notas

Tanto o endereço do arquivo json online quanto a chave para a API da openai estão localizados em um arquivo ".env", que segue a estrutura do arquivo ".env.example." Renomear o arquivo ".env.example" para ".env" e inserir uma chave da openai válida para rodar o programa localmente.

Para instalar as dependências use o comando:

```
pip install -r requirements.txt
```

Para rodar o programa, basta baixar o repositório localmente e rodar o arquivo "main.py"