# Caderno de Exercícios Práticos: Nível 03 (Produção e Métricas)

**Material de Referência:** `03_GUIA_PRATICO_ROCKYOU.md`  
**Script Base:** `bruteforce_rockyou.py`  
**Alvo:** NexusBank Corporate (`/login` e `/admin/login`)  

---

## 🎯 Objetivo Desta Lista

Praticar automações de nível intermediário e avançado:
* Redirecionamento de ataques contra endpoints administrativos restritos.
* Implementação de logs de auditoria contínuos com marca temporal (*timestamp*).
* Captura de interrupção manual via teclado (`Ctrl + C`) com exibição de métricas parciais.
* Interpretação e análise dos registros no servidor do defensor (*Blue Team*).

---

## Exercício 3.1 — Ataque ao Painel Corporativo (`/admin/login`)

### Enunciado
No desafio final apresentado no slide da aula, o alvo do teste é a conta administrativa `admin` na rota corporativa `/admin/login`.  
Altere as configurações do script `bruteforce_rockyou.py` para executar o teste contra esse alvo específico.

### Tarefas
1. Altere a variável `URL_ALVO` para `"http://127.0.0.1:8002/admin/login"`.
2. Altere a variável `USUARIO_ALVO` para `"admin"`.
3. Garanta que a senha `admin123` esteja presente no arquivo `rockyou.txt`.
4. Execute o script e confira se o status 200 é atingido.

### Resolução Sugerida
```python
# Trecho de configuração no início do script:
URL_ALVO = "http://127.0.0.1:8002/admin/login"
USUARIO_ALVO = "admin"
ARQUIVO_WORDLIST = "rockyou.txt"
```

---

## Exercício 3.2 — Registro de Auditoria Contínuo com Data e Hora

### Enunciado
Em testes profissionais de segurança, cada requisição enviada deve ser documentada com horário exato em um arquivo de log para cruzamento de dados com a equipe defensiva (Blue Team).  
Modifique o script para que, a cada tentativa (certa ou errada), uma linha seja gravada no arquivo `auditoria.log` no formato:
`[HH:MM:SS] Usuario: ana | Senha: ... | Status: ...`

### Tarefas
1. Importe a classe `datetime` do módulo nativo: `from datetime import datetime`.
2. Dentro do laço, após obter o `resposta.status_code`, capture a hora atual com `datetime.now().strftime("%H:%M:%S")`.
3. Abra `auditoria.log` em modo de adição (`"a"`) e grave o registro.

### Resolução Sugerida
```python
from datetime import datetime
import requests

# Dentro do laço for, logo após receber a resposta:
agora = datetime.now().strftime("%H:%M:%S")
linha_log = f"[{agora}] Alvo: {USUARIO_ALVO} | Senha testada: '{senha}' | Status: {resposta.status_code}\n"

with open("auditoria.log", "a", encoding="utf-8") as arq_log:
    arq_log.write(linha_log)
```

---

## Exercício 3.3 — Interrupção Manual Segura (`Ctrl + C`)

### Enunciado
Como a wordlist `rockyou.txt` possui milhões de linhas, o analista frequentemente precisa interromper o teste manualmente pressionando `Ctrl + C` no terminal.  
Se o script não tratar isso, o Python encerra com o erro `KeyboardInterrupt` sem exibir o total de requisições disparadas até aquele momento.

Encapsule o laço principal em um bloco `try / except KeyboardInterrupt` para que, se o aluno interromper a execução, o relatório de métricas ainda seja calculado e exibido no terminal.

### Resolução Sugerida
```python
try:
    with open(ARQUIVO_WORDLIST, "r", encoding="latin-1", errors="ignore") as arquivo:
        for linha in arquivo:
            # ... lógica de requisição ...
            pass
except KeyboardInterrupt:
    print("\n\n[!] Teste interrompido manualmente pelo operador (Ctrl + C).")

# O script continua normalmente para o cálculo do tempo e exibição do relatório:
tempo_total = time.time() - tempo_inicio
print(f"Total de tentativas realizadas antes da interrupção: {tentativas}")
print(f"Tempo transcorrido: {tempo_total:.2f} segundos")
```

---

## Exercício 3.4 — Análise Forense do Lado Defensor (Blue Team)

### Enunciado
Toda requisição executada pelo seu script deixa um rastro nos logs do servidor NexusBank.

### Tarefas
1. Localize o arquivo de log gerado pela aplicação do laboratório (ou observe o terminal onde o backend do professor está rodando).
2. Verifique como as tentativas de login com status 401 vindas do mesmo IP se repetem em frações de segundo.
3. Responda em um pequeno parágrafo:  
   *Quais seriam duas medidas defensivas simples que o desenvolvedor do banco poderia configurar no servidor para neutralizar esse script de força bruta?*

### Resposta Sugerida para Discussão em Sala
1. **Rate Limiting / Bloqueio Temporário:** Bloquear temporariamente o endereço IP de origem ou a conta após 5 tentativas consecutivas com código 401.
2. **Segundo Fator de Autenticação (MFA / 2FA):** Mesmo que a senha seja descoberta via força bruta, o invasor não conseguiria autenticar sem o código temporário (OTP) enviado ao dispositivo do cliente.
3. **CAPTCHA:** Inserir desafio visual após a segunda tentativa errada para impedir disparos automatizados via script.
