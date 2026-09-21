# 6. Ferramentas prontas (visão geral)

Escrever o cliente HTTP na mão ensina o mecanismo. No mercado, pentesters e red teams também usam **ferramentas especializadas** quando o contrato de teste autoriza. Uma das mais citadas em cursos de segurança ofensiva é o **Hydra** (THC-Hydra): programa que testa autenticações em vários protocolos (HTTP, FTP, SSH, etc.), lendo usuários e senhas de arquivos.

## O que uma ferramenta dessas faz, em uma frase

Ela **automatiza** o mesmo fluxo do capítulo 5: tira candidato da wordlist, monta a requisição no formato certo daquele serviço, olha a resposta, tenta o próximo. A diferença é engenharia: paralelismo, dezenas de módulos, menos código para você manter.

## Quando faz sentido usar ferramenta pronta

- O escopo do teste **já está no contrato** e o alvo **sabe** que será testado.
- O protocolo não é um `POST` JSON simples — montar na mão seria lento e sujeito a erro.
- Você precisa padronizar o relatório (“usamos a ferramenta X na versão Y”).

## Quando faz sentido escrever na mão (e por isso esta aula existe)

- Para **aprender**: você vê o JSON, o 401, o timeout.
- Para API **muito específica** (campo com nome estranho, dois fatores no meio, CSRF token). A ferramenta genérica “não adivinha” o seu FastAPI.
- Para o **Blue Team** simular carga de forma controlada e validar o log — um script mínimo, no laboratório, já gera o padrão que o capítulo 8 descreve.

## O que esta apostila não traz

Não há linha de comando de ferramenta ofensiva aqui (nem “cole isto no Kali”). Comando copiado da apostila vira receita fora de contexto — inclusive contra alvo errado. Se a instituição autorizar demonstração, **o professor opera a ferramenta na frente da turma**, no IP do laboratório, e vocês observam o `acessos.log` subir.

## Relação com o Python da UC11

Python continua sendo a linguagem da disciplina: `requests` + arquivos cobrem o currículo. Ferramenta pronta é **cultura geral de segurança**, não substitui entender HTTP.

## Resumo do capítulo

Ferramenta pronta = o laço do capítulo 5, industrializado. Aprender na mão primeiro evita virar “operador de caixa-preta”. Uso só com autorização.

## Exercícios

1. Liste duas vantagens de uma ferramenta pronta e duas vantagens do script didático em `requests`.
2. Um colega quer “testar o Instagram da escola” com ferramenta de laboratório. O que você responde, com base no próximo capítulo?
3. Por que um `POST` JSON com nomes de campo `usuario` e `senha` pode exigir ajuste manual mesmo quando a ferramenta “tem módulo HTTP”?
4. Relacione: paralelizar 50 tentativas por segundo no laboratório ajuda o aluno a ver o quê nos logs? E qual o risco pedagógico (servidor cair, bagunçar a aula)?
