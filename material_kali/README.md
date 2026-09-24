# Laboratório Complementar: Kali Linux na Prática (Wireshark, Burp e Hydra)

Bem-vindo ao complemento de **ferramentas de Kali** para os módulos `material_bruteforce/` e `material_blackhat/`.

Cada ferramenta tem uma pasta própria, e dentro dela **duas frentes**: `BRUTEFORCE` (NexusBank `/login`) e `C2` (GitHub `bhtprojan`).

> ⚠️ **Aviso de Responsabilidade e Ética Profissional**
> Use apenas em laboratório, contra alvos próprios (`127.0.0.1`, VM de aula, repo privado).
> Interceptar tráfego de terceiros sem autorização é ilegal (**Marco Civil, Art. 154-A**).
> No Wireshark/Burp você verá **senhas de teste em texto claro** — por isso usamos apenas `123456`, `senha123` e tokens falsos de aula.

---

## 🗺️ Mapa de Navegação

| Ferramenta | Pasta | Guia Bruteforce | Exercícios Bruteforce | Guia C2 (GitHub) | Exercícios C2 | Apoio |
| :---: | :--- | :--- | :--- | :--- | :--- | :--- |
| **Wireshark** | `01_wireshark/` | `01_GUIA_PRATICO_WIRESHARK_BRUTEFORCE.md` | `01_EXERCICIOS_WIRESHARK_BRUTEFORCE.md` | `02_GUIA_PRATICO_WIRESHARK_C2.md` | `02_EXERCICIOS_WIRESHARK_C2.md` | `filtros.txt`, `tshark_comandos.sh` |
| **Burp Suite** | `02_burp/` | `01_GUIA_PRATICO_BURP_BRUTEFORCE.md` | `01_EXERCICIOS_BURP_BRUTEFORCE.md` | `02_GUIA_PRATICO_BURP_C2.md` | `02_EXERCICIOS_BURP_C2.md` | `burp_proxy_config.py` |
| **Hydra vs Python** | `03_hydra_vs_python/` | `01_GUIA_PRATICO_HYDRA_BRUTEFORCE.md` | `01_EXERCICIOS_HYDRA_BRUTEFORCE.md` | `02_GUIA_PRATICO_HYDRA_C2_LIMITES.md` | `02_EXERCICIOS_HYDRA_C2.md` | `comandos_hydra.sh`, `comparar_tempo.py` |

---

## 🧭 Quando usar cada uma?

```text
[Python script] --gera--> [HTTP POST /login] --capturado por--> [Wireshark: vê tudo no fio]
                                              --interceptado por--> [Burp: pausa, edita e reenvia]
[Hydra] --faz o mesmo ataque, sem código--> compare velocidade e flexibilidade com Python
[C2 GitHub: HTTPS api.github.com] --Wireshark vê só TLS--> [Burp com CA vê JSON/base64 dentro]
```

* **Wireshark:** prova que o script Python realmente envia `{"usuario":"ana","senha":"..."}` e recebe `401/200`. Ideal para aula de protocolo.
* **Burp:** prova que dá para fazer o mesmo ataque sem programar (Repeater/Intruder) e para editar na mão.
* **Hydra:** prova que ferramenta pronta é mais rápida de lançar, mas Python é mais flexível (JSON, 2 arquivos, métricas, relatório CSV).

---

## ⚙️ Pré-requisitos (Kali)

```bash
sudo apt update && sudo apt install -y wireshark hydra tshark
# Burp Suite Community já vem no Kali. Rode: burpsuite &
# Python:
pip install requests urllib3
```

* **Loopback no Windows:** Wireshark não enxerga `127.0.0.1` sem adaptador Npcap. Soluções de aula:
  1. Rode o servidor em `0.0.0.0` e acesse pelo IP da LAN (`http://192.168.x.x:8002/login`), ou
  2. Rode tudo dentro do Kali (`python3 -m uvicorn ...`) e capture em `lo`, ou
  3. Instale Npcap com suporte a loopback e capture na interface `Adapter for loopback traffic capture`.
* **Hora sincronizada:** Wireshark/Burp e Python na mesma hora facilitam correlacionar `auditoria.log` com pacotes.

---

## 🐳 Docker Local por Aluno (padrão de sala)

Cada aluno sobe o laboratório na própria máquina — não há servidor central:

```bash
cd banco_web
docker compose up --build
# em outro terminal:
curl http://127.0.0.1:8002/api/saude
```

* A API publica `8002:8002` e escuta em `0.0.0.0:8002`, então `http://127.0.0.1:8002/login` funciona em cada máquina isolada.
* Todos os exercícios (bruteforce, Burp via `proxies`, Hydra contra `:8002`, Wireshark) foram feitos para esse alvo local.

## 🔓 Por que HTTP Mostra Tudo (e HTTPS Não)

O NexusBank é **HTTP puro, sem TLS** — decisão didática. No Follow TCP Stream o aluno vê:

* Pedido: `{"usuario": "ana", "senha": "123456"}` em texto claro.
* Resposta `200`: `{"ok": true, "papel": "cliente", "token": "YW5hOm...="}` + cookie `nb_session` sem `HttpOnly/Secure`.
* Token = `base64(usuario:papel:data)`, previsível e sem assinatura — dá para decodificar no próprio Burp Decoder.

No C2 GitHub (`https://api.github.com`) é o oposto: Wireshark só vê SNI, IP, hora e tamanho. O contraste HTTP × HTTPS virou exercício Blue Team nos guias.

## 👥 Sala Cheia na Mesma Rede: um Aluno Vê o Outro?

**Não, cada um só vê o próprio tráfego.** Motivos:

1. Rede chaveada (switch/Wi-Fi com client isolation): unicast de A↔A não vai para B. O Wireshark em modo promíscuo só soma broadcasts/multicast (mDNS, ARP), não o `POST /login` do colega.
2. Tráfego local nem sai da máquina: `127.0.0.1` fica no loopback; até o acesso ao próprio IP da LAN (`192.168.x.x → 192.168.x.x:8002`) é resolvido internamente, sem ir para o fio.
3. Docker bridge (`172.x`) é namespace isolado por host.

> Regra de sala: cada um captura na própria interface (`lo` ou seu `eth0/Wi-Fi`) com filtro `tcp.port == 8002 && ip.addr == <seu-IP>`. Se aparecer IP de colega, é broadcast — ignore ou use `ip.src == <seu-IP>` para focar. Não façam ARP spoofing um no outro: cai no Art. 154-A.

---

## 📁 Estrutura

```text
material_kali/
├── README.md
├── 01_wireshark/
│   ├── README.md
│   ├── 01_GUIA_PRATICO_WIRESHARK_BRUTEFORCE.md
│   ├── 01_EXERCICIOS_WIRESHARK_BRUTEFORCE.md
│   ├── 02_GUIA_PRATICO_WIRESHARK_C2.md
│   ├── 02_EXERCICIOS_WIRESHARK_C2.md
│   ├── filtros.txt
│   └── tshark_comandos.sh
├── 02_burp/
│   ├── README.md
│   ├── 01_GUIA_PRATICO_BURP_BRUTEFORCE.md
│   ├── 01_EXERCICIOS_BURP_BRUTEFORCE.md
│   ├── 02_GUIA_PRATICO_BURP_C2.md
│   ├── 02_EXERCICIOS_BURP_C2.md
│   └── burp_proxy_config.py
└── 03_hydra_vs_python/
    ├── README.md
    ├── 01_GUIA_PRATICO_HYDRA_BRUTEFORCE.md
    ├── 01_EXERCICIOS_HYDRA_BRUTEFORCE.md
    ├── 02_GUIA_PRATICO_HYDRA_C2_LIMITES.md
    ├── 02_EXERCICIOS_HYDRA_C2.md
    ├── comandos_hydra.sh
    └── comparar_tempo.py
```
