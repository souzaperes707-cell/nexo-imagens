# Manual do Robô NEXO — Equipe Alpha (V1 · 15/11/2026)

Este manual é para quem for continuar o robô: o próprio Peres, uma conversa nova com o Claude, outra IA ou um programador. Ele explica o que cada peça faz, onde está e como consertar.

## 1. Para que serve

Divulgar e vender o e-book **NEXO** (thriller político de Peres d'Souza, Vol. II da trilogia A Ordem) na Hotmart, por R$ 29,99.

- **Meta:** R$ 5.000 em 90 dias a partir de 03/11/2026; nenhuma semana sem venda.
- **Caminho de venda:** a pessoa vê o post, lê o Capítulo 1 grátis e compra.
- **Capítulo 1 grátis (PDF público):** https://drive.google.com/file/d/1mEdsd-aOyYgqHxVKRedYquEkGWr5DwnN/view?usp=sharing
- **Compra (Hotmart):** https://hotmart.com/pt-br/marketplace/produtos/nexo-o-sistema-nao-tem-lado-ele-tem-um-dono/A108140607I

## 2. Onde está cada peça (tudo em contas do Peres)

| Peça | Onde | Observação |
|---|---|---|
| Código do robô, imagens, vídeos e trechos de música | GitHub `souzaperes707-cell/nexo-imagens` (público) | Só material de post e arquivos do robô; nada pessoal |
| Turnos automáticos | Tarefas agendadas na conta Claude do Peres | Modelo Sonnet, para não gerar custo extra |
| Regras e registros diários | Google Drive, pasta "Equipe Alpha — Registros" (id `1XfzG9PnZ0p63cQuDFUXJHVwh0-qYnZRs`) | Regras: "Equipe Alpha — REGRAS DE AUTONOMIA V1" |
| Livro completo | Google Drive, NEXO.pdf (id `1xZTcUlLDkAiLupcycdhDgNNKoj39xjRv`) | Fonte das pautas; nunca inventar trecho |
| Carrossel diário | Metricool, marca "NEXO LIVRO OFICIAL" (blogId 7598023), plano grátis | 20 publicações por mês; Instagram `ponto_utyl`, TikTok `@nexolivros`, YouTube |
| Vídeo diário | Buffer, conta nexolivrooficial, plano grátis | Canal TikTok `nexolivros` (id `6af922c3ece6dfde5fcbe3dd`); até 3 canais, 10 posts na fila por canal |
| Músicas inteiras | Com o Peres | No GitHub só ficam trechos de 15 s |
| Robô antigo (reserva) | PC do Peres: `Desktop\memoria alfa\robo-nexo\editor\` (V3.1) | Usa um pautas.json próprio; não usar ao mesmo tempo que a nuvem |

## 3. O dia do robô (horário de Campo Grande)

| Hora | Turno | O que faz |
|---|---|---|
| 06h27 | **Manhã** (Publicador + Fiscal + Estrategista) | Gera carrosséis dos próximos 3 dias sem post, agenda no Metricool às 11h, revisa legendas e mantém pelo menos 10 pautas livres |
| 11h | Metricool publica | Carrossel de 4 telas no Instagram e no TikTok |
| 17h43 | **Tarde** (Atendimento + Divulgação + Analista) | Responde leitores por e-mail, manda até 10 e-mails a resenhistas e analisa as métricas |
| 19h (Brasília) | Buffer publica | Vídeo vertical com música do Peres no TikTok (e Instagram/YouTube quando conectados) |
| 21h13 | **Vigia da Noite** | Confere o que saiu, corrige falhas, garante o carrossel de amanhã e agenda o vídeo de amanhã no Buffer |

Também existe a tarefa "Resumo diário de e-mails NEXO e bancos" (05h57 de Brasília), que só lê o Gmail e resume respostas.

Cada turno grava um arquivo novo nos Registros do Drive (`AAAA-MM-DD manha.md`, `tarde.md`, `noite (vigia).md`). Só manda e-mail de alerta ao Peres se houver problema que não conseguiu resolver.

## 4. Arquivos do robô (`robo/`)

| Arquivo | Função | Uso |
|---|---|---|
| `pautas.json` | Estoque de pautas (telas, destaque, frase final do livro, legenda, título do TikTok, `usada`) | Editado pelo Estrategista |
| `gerar-carrossel.js` | Desenha as 4 telas (1080×1350) com Playwright/Chromium; ajusta texto que não cabe (`fit()`) | Chamado pelo preparar-post |
| `preparar-post.py` | Escolhe a próxima pauta livre do capítulo do mês, gera as telas em JPG e marca como usada | `python3 robo/preparar-post.py AAAA-MM-DD [id]` |
| `gerar-video.py` (V2) | Transforma as 4 telas em vídeo 9:16 de 14,2 s com zoom e transições; põe um trecho de música do Peres | `python3 robo/gerar-video.py AAAA-MM/<id> [trecho.m4a ou estilo]` |
| `musicas/` | 45 trechos de 15 s (Raw Power Riff 15, Ação 13, Back in Back 2: 4, Back in Back 3: 13) | Rodízio diário intercalando as músicas |
| `trilhas.py` | Trilhas compostas por código (suspense, ação, tensão, mistério) | Só reserva, se faltar trecho de música |

**Regras das pautas:** capítulo muda por mês (nov/2026 = Cap. 1, dez/2026 = Cap. 2…). A primeira tela é uma cena concreta. A frase final é citação idêntica ao livro. Legenda termina com "Leia o Capítulo 1 grátis. Link na bio."

**Rodízio de fundo do carrossel (segunda a domingo):** branca, preta, viva, branca, cinema, viva, preta.

**Links públicos:** `https://raw.githubusercontent.com/souzaperes707-cell/nexo-imagens/main/AAAA-MM/<id>/tela-N.jpg` e `.../video.mp4`. O Metricool e o Buffer leem esses links.

**Commits:** `git -c user.name="Equipe Alpha" -c user.email="equipe-alpha@users.noreply.github.com" commit -m "..."` e `git -c push.negotiate=true push`.

## 5. Regras que nunca mudam sem o Peres

- Nunca citar Grupo Pereira, Comper, Fort ou terceiros.
- Nunca inventar venda, número, trecho, resenha ou urgência.
- Não gastar dinheiro, não mudar preço, não publicar na Amazon, não abrir afiliados sem o OK do Peres.
- Chaves e senhas: só o Peres cria e guarda (GitHub Secrets). Nunca colar em conversa.
- E-mails de divulgação do NEXO são autônomos (autorizado em 02/11/2026); qualquer outro e-mail precisa de rascunho e OK.
- Mudanças no robô: explicar antes e esperar o VAI. Toda versão nova ganha número (V1, V2…) e um mini cérebro.

## 6. Como consertar

| Sintoma | Causa provável | O que fazer |
|---|---|---|
| Post não saiu no Instagram/TikTok | Conta desconectada no Metricool ou Buffer | Peres reconecta a conta no site da ferramenta |
| Metricool recusa a imagem | Link não é do GitHub raw ou ainda não propagou | Esperar 1 min e conferir com `curl` (precisa dar 200) |
| TikTok recusa a imagem | Formato PNG | Usar JPG (já é o padrão) |
| Texto cortado na tela | Frase longa | Descartar a pauta (`"obs":"descartada"`) e gerar outra |
| Cota do Metricool acabou | Plano grátis: 20/mês | Fim de semana fica só com o vídeo do Buffer |
| Vídeo sem música | Pasta `robo/musicas` vazia | O robô usa as trilhas de código sozinho |
| Mudança deu errado | — | Voltar para a versão salva anterior (seção 7) |

## 7. Versões

| Versão salva no GitHub (branch) | Data | O que é |
|---|---|---|
| `versao/publicador-v1` | 14/11/2026 | Publicador na Nuvem V1: carrossel gerado na nuvem e agendado no Metricool |
| `versao/video-v1` | 15/11/2026 | Vídeo V1: vídeo diário com trilhas compostas por código |
| `versao/video-v2` | 15/11/2026 | Vídeo V2: trechos das músicas do Peres em rodízio (45 trechos) + este manual |

Cada versão fica salva num ramo (branch) próprio, que não muda mais. O robô roda sempre no ramo `main`.
Para ver uma versão: no GitHub, clique no seletor de branch (onde está escrito `main`) e escolha a versão. Para voltar: peça ao Claude "volte o robô para a versão versao/X".
A cada versão nova, criar o ramo `versao/<nome>-vN` apontando para o commit dela.

## 8. Pendências (15/11/2026)

- Conectar Instagram e YouTube no Buffer (Peres, uma vez) para o vídeo das 19h sair nos três.
- Tornar a conta do TikTok comercial para o link da bio ficar clicável.
- Turno da manhã ainda agenda o carrossel sem a música automática do TikTok (o Vigia já usa).
- Testar o link "Continue lendo" no fim do PDF do Capítulo 1.
- WhatsApp Business com resposta automática (Capítulo 1 + Hotmart), quando o Peres quiser.
