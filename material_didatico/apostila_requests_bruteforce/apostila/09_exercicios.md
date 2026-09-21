# 9. Exercícios consolidados

Lista única para revisão e para o professor aplicar como lista da semana. **Sem gabarito.** Os enunciados repetem os de cada capítulo, agrupados.

## Capítulo 1 — HTTP

1. Escreva com suas palavras a diferença entre **cliente** e **servidor**. Dê um exemplo que não seja o navegador.
2. O laboratório expõe `POST /login`. Explique por que um `GET /login` provavelmente não faria sentido para enviar senha.
3. Relacione status: senha errada vs senha certa no FastAPI do laboratório.
4. Monte no papel o JSON de um `POST /admin/login`.

## Capítulo 2 — `requests`

1. Instale `requests` e faça `GET https://httpbin.org/get`. Imprima o `status_code`.
2. Com o laboratório ligado, `GET http://127.0.0.1:8002/contas` e conte as contas.
3. Dois `POST /login` (erro e acerto, se o seed estiver liberado). Anote os status.
4. Servidor desligado: o erro é `401` ou `RequestException`? Explique.

## Capítulo 3 — Arquivos

1. `nomes.txt` com cinco nomes; programa imprime em maiúsculas.
2. O que acontece se o log for aberto com `"w"` no segundo dia?
3. Anexe em `aula.log` um horário (`datetime`); rode duas vezes.
4. Linha em branco na wordlist: efeito sem `continue`.

## Capítulo 4 — Wordlists

1. Dez senhas fracas inventadas (nunca as suas reais) e justificativa.
2. Senha de 4 dígitos (`0-9`): quantas combinações no pior caso?
3. Wordlist de 20 linhas vs brute force pura de 8 caracteres: quem acha `admin123` antes, em geral?
4. Seed removido: wordlist genérica ou brute force de 12 caracteres? Por quê?

## Capítulo 5 — Fluxo do ataque (conceitos)

1. Passo A (um `POST`) no laboratório; anote status de senha errada.
2. Wordlist de 8 linhas; Passo B conta linhas úteis.
3. Fluxograma do pseudocódigo.
4. Duas defesas no servidor que quebram ou denunciam o fluxo.

## Capítulo 6 — Ferramentas prontas

1. Duas vantagens da ferramenta pronta e duas do script didático.
2. Colega quer testar rede de terceiros: resposta ética.
3. Por que JSON com campos `usuario`/`senha` pode exigir ajuste mesmo com “módulo HTTP”.
4. Paralelizar 50 tentativas/s: o que o log mostra e qual o risco na aula.

## Capítulo 7 — Ética e lei

1. Parágrafo para familiar: Wi-Fi do vizinho não é lição de casa.
2. IP errado na sala: o que fazer imediatamente.
3. Número da lei do Marco Civil e do art. 154-A — sem inventar inciso.
4. Tutorial de “invadir câmera” vs autorização.

## Capítulo 8 — Blue Team

1. No log de exemplo, quando suspeitar **antes** do sucesso.
2. Comparar log real do laboratório (logins manuais) com a rajada.
3. Por que o campo IP importa.
4. Três bullets de uma regra de alerta, sem código.

## Desafio integrador (opcional)

Com o laboratório **autorizado** e ligado, faça **três** logins manuais pela interface ou pelo Swagger (`/docs`). Depois abra `data/acessos.log` e escreva um parágrafo: dá para distinguir humano de script só por esse arquivo? O que faltaria no log para ter certeza?
