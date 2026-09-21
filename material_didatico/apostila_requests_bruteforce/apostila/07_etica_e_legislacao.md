# 7. Ética e legislação

Ferramenta de segurança não é brinquedo de rede aberta. No Brasil, invadir ou tentar invadir sistema alheio **sem autorização** pode ser crime, mesmo “só para treinar”, mesmo “não peguei dado nenhum”, mesmo “a senha era 123456”.

Esta seção é séria de propósito.

## Autorização é o interruptor

Pergunta única antes de qualquer teste:

> Eu tenho permissão **por escrito ou inequívoca da aula** para testar **este** alvo?

No SENAC, o alvo combinado é a instância do laboratório (`banco_web_aula_21_09` na máquina do professor ou no Docker da sala). Fora disso: site da escola, Wi-Fi do shopping, painel da prefeitura, Instagram, e-mail do colega — **não**.

“Rede aberta” não é convite. “Não tinha senha forte” não é convite. “É só um login” não é convite.

## Marco Civil da Internet (Lei nº 12.965/2014)

É a lei que organiza direitos e deveres no uso da internet no Brasil. Entre outros pontos, trata de **privacidade**, **registros de conexão** e responsabilidades. Para esta aula, o recado prático é: a rede não é terra sem lei. Tráfego, logs e dados de terceiros têm proteção jurídica. Você não “experimenta” em cima da vida digital alheia.

Não use o Marco Civil como desculpa genérica para tudo — leia o texto oficial se for aprofundar. O que importa na UC11: **há lei específica para internet**, e ela não abona ataque didático improvisado.

## Artigo 154-A do Código Penal

Incluído pela Lei nº 12.737/2012 (conhecida na imprensa como Lei Carolina Dieckmann), o art. 154-A trata de **invasão de dispositivo informático**: invadir dispositivo alheio, conectado ou não à rede, mediante violação indevida de mecanismo de segurança, com o fim de obter, adulterar ou destruir dados ou instalar vulnerabilidades.

Penas e agravantes estão no próprio Código; o professor não precisa transformar a aula em concurso de Defensoria. O que o aluno técnico precisa gravar:

- **Dispositivo alheio** inclui servidor, celular, computador, painel web.
- **Mecanismo de segurança** inclui senha de login. Furá-la sem autorização não é “exercício de `requests`”.
- Tentativa e contexto (prejuízo, dados pessoais) pesam na esfera penal e também na **disciplinar da escola** e na **civil**.

Esta apostila **não** é parecer jurídico. Em caso real, advogado. Em caso de aula, **só o laboratório**.

## Regras de ouro da UC11

1. Só o IP / a URL que o professor escrever no quadro.
2. Sem VPN “para esconder” o teste da escola — se precisa esconder, já está errado.
3. Sem publicar wordlist+alvo+horário em grupo de mensagem como troféu.
4. Relatório da aula descreve o **laboratório**, não dados de pessoas reais.

## Resumo do capítulo

Autorização define se você é aluno em laboratório ou autor de crime. Marco Civil (Lei 12.965/2014) e art. 154-A do Código Penal existem. Treine no alvo combinado.

## Exercícios

1. Redija um parágrafo (cinco linhas) explicando a um familiar por que “testar a senha do Wi-Fi do vizinho” não é trabalho de casa da UC11.
2. O laboratório está no IP `192.168.10.20` e você ataca, sem querer, `192.168.10.21`. O que você faz nos 10 segundos seguintes?
3. Cite a lei do Marco Civil e o artigo do Código Penal vistos na aula, com o número correto — sem inventar inciso.
4. Um tutorial na internet ensina a “invadir câmera de segurança”. Relacione com autorização e com o art. 154-A.
