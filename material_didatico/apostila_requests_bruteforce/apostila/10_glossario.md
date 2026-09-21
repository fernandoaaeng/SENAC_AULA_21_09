# 10. Glossário

Termos desta apostila, em linguagem de curso técnico — não de manual jurídico.

**API**  
Conjunto de rotas que um programa oferece para outro programa (não só para o navegador). O FastAPI do banco é uma API HTTP.

**Blue Team**  
Equipe (ou mentalidade) de **defesa**: logs, alerta, contenção, correção.

**Brute force (força bruta)**  
Testar muitas combinações até acertar. No rigor, “pura” = todas as combinações de caracteres. No dia a dia da aula, muita gente chama de brute force também o ataque de **dicionário**.

**Cliente**  
Quem inicia a requisição: navegador, `requests`, aplicativo móvel.

**Corpo (body)**  
Dados enviados ou recebidos além dos cabeçalhos. Em APIs modernas, costuma ser JSON.

**CSV**  
Arquivo de texto com colunas separadas por vírgula. Útil para abrir log no planilha.

**Dicionário (ataque de)**  
Testar senhas de uma **wordlist**, não o alfabeto inteiro.

**Endpoint / rota**  
Caminho da API, como `/login` ou `/admin/logs`.

**Hash**  
Função que transforma senha em um valor de tamanho fixo, **sem** caminho fácil de volta. Senha não deveria ser guardada em texto puro. O laboratório guarda em texto puro **de propósito**.

**HTTP**  
Protocolo da web: métodos, status, cabeçalhos, corpo.

**Hydra**  
Exemplo conhecido de programa que automatiza testes de senha em vários protocolos. Só com autorização.

**IP**  
Número que identifica (de forma aproximada) a origem na rede. No log, agrupa tentativas da mesma máquina.

**JSON**  
Formato de texto com chaves e valores (`{"usuario": "ana"}`). `response.json()` no Python vira `dict` ou `list`.

**Log**  
Registro histórico de eventos. Append (`"a"`) no arquivo; ou tabela no SQLite.

**Rate limiting**  
Teto de requisições por tempo (por IP ou por conta). Freio contra dicionário online.

**Red Team**  
Mentalidade de ataque (teste autorizado), o “time vermelho”.

**Requisição**  
O pedido HTTP completo (método + URL + cabeçalhos + corpo).

**`requests`**  
Biblioteca Python de cliente HTTP.

**Servidor**  
Quem recebe a requisição e responde. Ex.: Uvicorn + FastAPI na porta 8002.

**Status code**  
Número da resposta: `200` ok, `401` não autenticado, `404` não achou, `500` o servidor quebrou.

**Timeout**  
Tempo máximo de espera pela rede. Evita programa preso.

**Wordlist**  
Arquivo com candidatos (senhas, usuários, caminhos), um por linha.
