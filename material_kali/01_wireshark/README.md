# 01 — Wireshark: Vendo o Brute Force no Fio

**Foco:** `material_bruteforce/` (`/login` na porta `8002`)
**Ferramenta:** Wireshark / `tshark` (qualquer SO, ideal no Kali)
**Apoio:** `filtros.txt`, `tshark_comandos.sh`

> Use apenas contra seu laboratório (`127.0.0.1` ou IP da VM de aula).

## O que você vai ver

Mesmo com script rodando "na própria máquina", os pacotes passam pela pilha TCP e são capturáveis — só precisa da interface certa (ver README raiz sobre loopback no Windows).
