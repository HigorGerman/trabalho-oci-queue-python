# Produtor/Consumidor com OCI Queue em Python

Este projeto é uma reimplementação em Python de um exemplo de Produtor/Consumidor para o serviço OCI Queue (Oracle Cloud Infrastructure).

Foi desenvolvido como atividade acadêmica, com o objetivo de recriar a lógica de um exemplo original (feito em Node.js com chamadas de API REST manuais), aplicando melhores práticas de programação em uma nova linguagem.

## 🎯 Objetivo do Trabalho e Melhorias Aplicadas

Conforme solicitado, o foco deste projeto foi aplicar melhorias sobre o exemplo original:

* **1. Aplicação de Boas Práticas (Uso do SDK Oficial):**
    A principal melhoria foi substituir as chamadas manuais de API REST e a assinatura complexa de requisições (`ociHttpRequest.js`) pelo **SDK oficial da OCI para Python** (`import oci`). Isso torna o código mais limpo, seguro, profissional e fácil de manter.

* **2. Organização e Clareza do Código:**
    O script é modularizado em funções claras que separam as responsabilidades:
    * `criar_cliente_fila()`: Cuida da conexão e autenticação.
    * `produtor_enviar_mensagem()`: Toda a lógica de envio (PutMessage).
    * `consumidor_processar_mensagem()`: Toda a lógica de recebimento (GetMessage), sucesso (DeleteMessage) e falha (UpdateMessage).
    * `menu_principal()`: Controla a interação com o usuário.

* **3. Comentários Explicativos:**
    O código inclui comentários (`#`) e docstrings (`"""..."""`) explicando o propósito de cada função e a lógica de negócios (como o tratamento de falhas e a exclusão de mensagens).

## ✨ Funcionalidades

O script `app_fila.py` fornece um menu interativo de console para simular um sistema de filas:

* **Produtor (Opção 1):** Envia uma mensagem em formato JSON (`{"email": "...", "msg": "..."}`) para a fila principal da OCI.
* **Consumidor (Opção 2):**
    * Busca mensagens da fila (fica invisível para outros consumidores).
    * Simula o processamento da mensagem.
    * **Em caso de Sucesso:** Deleta a mensagem da fila (chamada `DeleteMessage`).
    * **Em caso de Falha (Simulada):** Devolve a mensagem à fila com um novo timeout (chamada `UpdateMessage`), permitindo que ela seja processada novamente ou, eventualmente, enviada para a DLQ.

## 📋 Pré-requisitos

* Python 3.9+
* Uma conta na Oracle Cloud Infrastructure (OCI).
* Uma Fila Principal e uma Fila de Mensagens Mortas (DLQ) configuradas na OCI.

## ⚙️ Configuração Local

Este projeto não armazena chaves de segurança no código. Ele utiliza o método de autenticação padrão do SDK da OCI.

### 1. Instalar Dependências

O SDK da OCI é necessário (a opção `[full]` garante que o módulo `queue` seja instalado):

```bash
python3 -m pip install "oci[full]"
