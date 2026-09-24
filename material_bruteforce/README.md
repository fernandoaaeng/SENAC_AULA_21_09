# Laboratório Prático: Automação de Autenticação e Força Bruta

Bem-vindo ao material prático do módulo de **Requisições HTTP, Manipulação de Arquivos e Testes de Autenticação com Python**.

Este ambiente foi estruturado em **três níveis progressivos**. Cada nível é composto por:
1. **Guia Prático (`.md`)**: Explicação teórica, funcionamento do protocolo, análise linha a linha do código e procedimento de execução no terminal. *(Formatado especialmente para leitura ou exportação direta em PDF)*.
2. **Script Executável (`.py`)**: O código pronto para uso, limpo e comentado.
3. **Caderno de Exercícios (`.md`)**: Desafios práticos com enunciado, tarefas e resolução comentada para fixação pós-leitura.

---

## 🗺️ Mapa de Navegação e Arquivos

Consulte a tabela abaixo para localizar o material de cada etapa:

| Nível / Etapa | Guia Prático (Teoria e Código) | Script Python (.py) | Caderno de Exercícios | Arquivos de Entrada | Foco do Aprendizado |
| :---: | :--- | :--- | :--- | :--- | :--- |
| **01** | `01_GUIA_PRATICO_INICIANTE.md` | `bruteforce_simples.py` | `01_EXERCICIOS_INICIANTE.md` | `senhas.txt` | **Base Fundamental:** Modelo Cliente-Servidor, métodos HTTP, status codes (`200` vs `401`), leitura com `with open`, `strip()` e interrupção com `break`. |
| **02** | `02_GUIA_PRATICO_USUARIOS_E_SENHAS.md` | `bruteforce_multi_usuarios.py` | `02_EXERCICIOS_USUARIOS_E_SENHAS.md` | `usuarios.txt`<br>`senhas.txt` | **Múltiplos Alvos:** Laços aninhados (loop dentro de loop), leitura de dois arquivos com `.splitlines()`, controle de acesso e erro 403. |
| **03** | `03_GUIA_PRATICO_ROCKYOU.md` | `bruteforce_rockyou.py` | `03_EXERCICIOS_ROCKYOU.md` | `rockyou.txt` | **Cenário Real / Produção:** Leitura em streaming de arquivos gigantescos, codificação `latin-1`, tolerância a falhas de rede (`try/except`) e cálculo de velocidade (req/s). |

---

## 🖨️ Dica: Como Salvar os Guias como PDF

Os arquivos Markdown (`.md`) foram diagramados com tabelas compactas, blocos de código com numeração de linha e espaçamentos planejados para impressão ou conversão em PDF:

* **No VS Code:** Instale a extensão **Markdown PDF** ou **Markdown Preview Enhanced**, clique com o botão direito no arquivo `.md` e escolha `Markdown PDF: Export (pdf)`.
* **No Navegador:** Abra o arquivo `.md` renderizado no GitHub/VS Code, pressione `Ctrl + P` (Imprimir) e selecione a opção **Salvar como PDF**.

---

## ⚙️ Pré-requisitos de Execução

Antes de rodar os scripts, instale a biblioteca `requests` no terminal do seu computador:

```bash
pip install requests
```

Para executar qualquer um dos códigos, abra o terminal nesta pasta:
```bash
cd material_bruteforce

# Executar Nível 01:
python bruteforce_simples.py

# Executar Nível 02:
python bruteforce_multi_usuarios.py

# Executar Nível 03:
python bruteforce_rockyou.py
```

---

## 📁 Estrutura Organizada dos Arquivos

```text
material_bruteforce/
│
├── README.md                                <- Este índice geral
│
├── 01_GUIA_PRATICO_INICIANTE.md             <- Teoria HTTP completa + Explicação linha a linha
├── 01_EXERCICIOS_INICIANTE.md               <- 4 exercícios com resolução sobre o script simples
├── bruteforce_simples.py                    <- Script Python de 18 linhas
│
├── 02_GUIA_PRATICO_USUARIOS_E_SENHAS.md     <- Lógica de múltiplos usuários + Linha a linha
├── 02_EXERCICIOS_USUARIOS_E_SENHAS.md       <- Exercícios de laços aninhados, CSV e rota admin
├── bruteforce_multi_usuarios.py             <- Script com dois arquivos de entrada
│
├── 03_GUIA_PRATICO_ROCKYOU.md               <- Streaming, latin-1, métricas e try/except
├── 03_EXERCICIOS_ROCKYOU.md                 <- Exercícios de auditoria em log, Ctrl+C e Blue Team
├── bruteforce_rockyou.py                    <- Script avançado completo com relatórios
│
├── usuarios.txt                             <- Arquivo de dados (usuários de teste)
└── senhas.txt                               <- Arquivo de dados (senhas de teste)
```
