import oci
import json
import time

# --- Seus Dados da Fila (Já preenchidos) ---

QUEUE_OCID = "ocid1.queue.oc1.phx.amaaaaaajedz4pyafk4tb33k3vxbqkoxubiiykxmkhxxl6bk5lwcwheet5dq"
QUEUE_ENDPOINT = "https://cell-1.queue.messaging.us-phoenix-1.oci.oraclecloud.com"
# ---------------------------------------------

# Tenta carregar as credenciais (lê o ~/.oci/config que criamos)
try:
    config = oci.config.from_file("~/.oci/config", "DEFAULT")
except Exception as e:
    print(f"--- ERRO CRÍTICO DE AUTENTICAÇÃO ---")
    print(f"Não foi possível ler o arquivo ~/.oci/config.")
    print(f"Verifique se o arquivo existe e se a linha 'key_file=' está correta.")
    print(f"Erro original: {e}")
    exit()

def criar_cliente_fila():
    """Cria e configura o cliente da OCI Queue"""
    # CORREÇÃO: O módulo é 'oci.queue'
    client = oci.queue.QueueClient(config)
    client.base_client.endpoint = QUEUE_ENDPOINT
    return client

def produtor_enviar_mensagem(email, mensagem):
    """Lógica do Produtor (Envia Mensagem)"""
    client = criar_cliente_fila()
    
    # 1. Monta o Payload JSON (formato do trabalho)
    payload = json.dumps({
        "email": email,
        "msg": mensagem
    })

    # 2. Define a entrada da mensagem
    # CORREÇÃO: O módulo é 'oci.queue.models'
    message_entry = oci.queue.models.PutMessagesDetailsEntry(content=payload)
    
    # 3. Monta a requisição
    # CORREÇÃO: O módulo é 'oci.queue.models'
    put_messages_details = oci.queue.models.PutMessagesDetails(
        messages=[message_entry]
    )

    try:
        response = client.put_messages(
            queue_id=QUEUE_OCID,
            put_messages_details=put_messages_details
        )
        print(f"\n[PRODUTOR] ✅ Sucesso! Mensagem enviada. ID: {response.data.messages[0].id}")
    except Exception as e:
        print(f"\n[PRODUTOR] ❌ ERRO ao enviar: {e}")

def consumidor_processar_mensagem():
    """Lógica do Consumidor (Recebe e Deleta/Devolve)"""
    client = criar_cliente_fila()
    
    try:
        get_messages_response = client.get_messages(
            queue_id=QUEUE_OCID,
            visibility_in_seconds=60 # Tempo de invisibilidade
        )
        
        messages = get_messages_response.data.messages
        if not messages:
            print("[CONSUMIDOR] Nenhuma mensagem na fila.")
            return

        for msg in messages:
            print("\n[CONSUMIDOR] Mensagem recebida.")
            
            # 1. Lê o JSON
            dados_email = json.loads(msg.content)
            receipt = msg.receipt # Recibo para deletar
            
            print(f"   E-mail para: {dados_email.get('email')}")
            
            # 2. SIMULA O PROCESSAMENTO (ex: enviar o email)
            # Para testar a falha, digite 'falha' no email
            if "falha" in dados_email.get("email", "").lower():
                print("   [PROCESSO] ❌ Falha simulada. Devolvendo para fila...")
                
                # UPDATE (Devolve para fila)
                # CORREÇÃO: O módulo é 'oci.queue.models'
                update_details = oci.queue.models.UpdateMessageDetails(
                    visibility_in_seconds=30 # Fica visível de novo em 30s
                )
                client.update_message(
                    queue_id=QUEUE_OCID,
                    message_receipt=receipt,
                    update_message_details=update_details
                )
                print("   [PROCESSO] Mensagem devolvida.")
            else:
                print("   [PROCESSO] ✅ Sucesso no envio simulado.")
                
                # DELETE (Deleta da fila)
                client.delete_message(
                    queue_id=QUEUE_OCID,
                    message_receipt=receipt
                )
                print("   [PROCESSO] Mensagem deletada.")

    except Exception as e:
        print(f"\n[CONSUMIDOR] ❌ ERRO ao processar: {e}")

# --- Menu Principal ---
def menu_principal():
    print("Conectando ao OCI...")
    # Testa a conexão inicial
    try:
        # CORREÇÃO: O cliente é 'oci.queue.QueueClient'
        client = oci.queue.QueueClient(config)
        client.base_client.endpoint = QUEUE_ENDPOINT
        client.get_stats(queue_id=QUEUE_OCID)
        print("Conexão com a Fila OCI bem-sucedida!")
    except Exception as e:
        print(f"--- FALHA NA CONEXÃO INICIAL ---")
        print(f"Verifique seu OCID, Endpoint e se o arquivo ~/.oci/config está correto.")
        print(f"Erro: {e}")
        return

    while True:
        print("\n--- Menu OCI Queue Python (Trabalho) ---")
        print("1. Enviar Mensagem (Produtor)")
        print("2. Processar Mensagem (Consumidor)")
        print("S. Sair")
        escolha = input("Escolha uma opção: ")

        if escolha == '1':
            email = input("Destinatário do e-mail: ")
            conteudo = input("Conteúdo da mensagem: ")
            produtor_enviar_mensagem(email, conteudo)
        
        elif escolha == '2':
            consumidor_processar_mensagem()
        
        elif escolha.upper() == 'S':
            break
        
        else:
            print("Opção inválida.")

# --- Ponto de Entrada ---
if __name__ == '__main__':
    menu_principal()