# 8. Do lado da defesa (Blue Team)

Até aqui o olhar foi: como um cliente HTTP se comporta. Agora vire o tabuleiro. O **Blue Team** (defesa) não precisa “adivinhar a senha”. Ele precisa **perceber o padrão** no log e reagir: alertar, bloquear IP, obrigar troca de senha, ligar rate limiting.

O laboratório já registra cada tentativa: usuário, sucesso/falha, IP, horário — no SQLite e em `data/acessos.log`.

## O que um log de login deveria ter

No mínimo:

| Campo | Por quê |
|---|---|
| Data e hora (timestamp) | Ver rajada em poucos segundos |
| Usuário tentado | Mesma conta? Várias contas? |
| Sucesso ou falha | Maré de falhas é o sinal clássico |
| IP de origem | Mesma origem repetida |
| (Opcional) User-Agent / rota | Login comum vs `/admin/login` |

Sem isso, o defensor discute no escuro.

## O padrão de dicionário / brute force

Não é inteligência artificial. É conta de padaria:

- **Muitas falhas seguidas**
- **Mesmo IP** (ou um pequeno conjunto)
- **Pouco tempo** (dezenas ou centenas por minuto)
- Muitas vezes **o mesmo usuário** (`admin`, `ana`) enquanto a wordlist gira

Um ser humano digitando erra duas, três vezes. Não erra 400 vezes em um minuto com precisão de máquina.

## Trecho de log de exemplo (didático)

Imagine `data/acessos.log` assim (horários inventados):

```text
2026-09-21 14:02:01 UTC | usuario=ana | sucesso=False | ip=192.168.0.55
2026-09-21 14:02:01 UTC | usuario=ana | sucesso=False | ip=192.168.0.55
2026-09-21 14:02:02 UTC | usuario=ana | sucesso=False | ip=192.168.0.55
2026-09-21 14:02:02 UTC | usuario=ana | sucesso=False | ip=192.168.0.55
2026-09-21 14:02:03 UTC | usuario=ana | sucesso=False | ip=192.168.0.55
2026-09-21 14:02:03 UTC | usuario=ana | sucesso=True  | ip=192.168.0.55
```

Leitura de defensor:

1. Mesmo usuário, mesmo IP, falhas empilhadas no mesmo segundo — **automação**.
2. A última linha `sucesso=True` é o pior momento: o dicionário **acertou**. Daí em diante o atacante já está “dentro” no sentido da API de login.
3. Ação tardia ainda serve: invalidar sessão, resetar senha, bloquear o IP `192.168.0.55` na rede da sala.

Um login honesto da Ana, da casa dela, pareceria: um ou dois `False` espaçados, depois um `True`, IP residencial estável, horário humano.

## O que o laboratório ainda **não** faz (aula futura)

Detectar sozinho, alertar no painel, banir IP, exigir captcha, guardar hash. O raciocínio desta aula é só: **se o log existe, o padrão é visível**. Sem log, a defesa é cega — e o atacante agradece.

## Rate limiting e bloqueio, em uma frase

- **Rate limiting**: “este IP só pode tentar N logins por minuto.”
- **Bloqueio de conta**: “esta conta, após N falhas, dorme 15 minutos.”
- **Hash**: mesmo com vazamento do banco, a senha não está legível; wordlist ainda pode ser testada *offline*, mas o `/login` deixa de ser o atalho fácil.

Nada disso está ligado no alvo didático. Por isso o log enche rápido se alguém repetir POST.

## Resumo do capítulo

Log bom transforma brute force em gráfico óbvio. Procure rajada de falhas, mesmo IP, mesmo usuário, relógio apertado. A resposta defensiva (bloquear, alertar) é o próximo nível da disciplina.

## Exercícios

1. No trecho de exemplo, em que segundo o defensor já deveria suspeitar, **antes** do `sucesso=True`?
2. Abra (com o professor) o `data/acessos.log` real do laboratório depois de alguns logins manuais. Diferença visual para o trecho “rajada”?
3. Por que registrar o **IP** importa mais do que registrar só “falhou”?
4. Proponha, em três bullets, uma regra simples de alerta (“se acontecer X, avise Y”). Não precisa codificar.
