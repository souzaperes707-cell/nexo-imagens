#!/usr/bin/env python3
"""Fase 8 — gera o estoque por função de 24/11 a 07/12/2026 (9h descoberta, 12h relacionamento em dias úteis, 19h conversão; sexta 19h = Sexta do NEXO).
Todas as citações são conferidas contra o texto do livro antes de renderizar."""
import json, os, re, subprocess, sys, glob
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = "https://raw.githubusercontent.com/souzaperes707-cell/nexo-imagens/main"
LIVRO = re.sub(r"\s+", " ", open("/tmp/miolo.txt").read())
TAGS_D = "#dilema #NEXO #suspense #thriller #reflexão"
TAGS_C = "#NEXO #thriller #suspense #livros #LiteraturaBrasileira #BookTok #Bookstagram"

T = [  # data, id, pergunta, (A, A_peq), (B, B_peq), palavras, argA, argB, contexto, cit1, cit2
 ("2026-11-24","dentro-fora","Você entenderia o sistema de dentro ou de fora?",("De dentro, você vê tudo.","Mas passa a fazer parte dele."),("De fora, você continua livre.","Mas nunca entende como ele funciona."),"Dentro ou fora?",
  "Só dá para mudar aquilo que se entende.","Quem entra não sai igual.","Num quarto sem janelas, uma voz fez essa pergunta a um homem.",
  "— A questão é: você quer entender de dentro ou de fora?","— E se eu disser que quero de fora? — Então essa conversa já teria terminado há muito tempo."),
 ("2026-11-25","aviso","Se alguém que você ama dissesse: “se eu demorar, não confia em ninguém”…",("Você obedeceria.","Ele sabia de algo que você não sabe."),("Você desconfiaria dele.","E se o aviso fosse a armadilha?"),"Obedecer ou desconfiar?",
  "Quem avisa sabe de algo.","Um aviso também pode ser uma isca.","Cláudio mandou esta mensagem a Helena. Ela respondeu com um emoji.",
  "“Se eu demorar, não confia em ninguém.”","Paranoia ou planejamento? A linha era fina para quem conhecia alguém de verdade. Ou achava que conhecia."),
 ("2026-11-26","limite","Qual o limite do que você faria para proteger alguém?",("Não existe limite.","Por quem eu amo, qualquer coisa."),("Existe, e eu sei qual é.","Algumas coisas eu não faria por ninguém."),"Com limite ou sem limite?",
  "Amor de verdade não negocia limite.","Quem não tem limite pode ser usado por qualquer um.","Preso numa sala sem janelas, ele ouvia perguntas sobre si mesmo.",
  "— Qual o limite do que você faria para proteger alguém?","— Porque um homem que sabe até onde vai é previsível — disse a voz. — E previsibilidade é a única coisa que nos interessa em você."),
 ("2026-11-27","alguem-ganhou","Quando todo mundo perde, alguém ganha?",("Sim. Sempre tem alguém.","Crise para uns é negócio para outros."),("Não. Às vezes é só azar.","Nem toda tragédia tem um dono."),"Alguém ganhou ou foi azar?",
  "Ninguém perde sozinho: o dinheiro vai para algum lugar.","Achar culpado para tudo também é uma forma de não entender.",None,None,None),
 ("2026-11-28","escolha","Você escolheu estar onde está… ou alguém escolheu por você?",("Eu escolhi.","Cada passo foi decisão minha."),("Escolheram por mim.","Só me deixaram achar que fui eu."),"Você escolheu ou escolheram por você?",
  None,None,"Maíra olhava a manifestação na praça. Algo ali não fechava.",
  "…aquilo não era espontâneo. Tinha uma estrutura por baixo.","Alguém havia decidido que aquelas pessoas estariam naquela praça naquele dia, acreditando que era uma escolha delas."),
 ("2026-11-29","falha","Quando algo dá errado para milhões de pessoas: foi falha ou foi feito?",("Foi falha.","Sistemas grandes quebram."),("Foi feito.","Ninguém erra tão bem por acaso."),"Falha ou feito?",
  None,None,"Um ano depois do Confisco, no Parque Municipal Rio Manso, algumas vozes ainda resistiam.",
  "— Isso não foi erro! Foi feito!","— Ou acha que alguém ganhou com isso?"),
 ("2026-11-30","aceitar","Você aceitaria algo errado só porque todo mundo aceitou?",("Não. Nunca.","O que é errado continua errado."),("Talvez. Cansa lutar sozinho.","Um dia a gente aprende a conviver."),"Aceitar ou resistir?",
  "Se ninguém resiste, nada muda.","Ninguém aguenta brigar todos os dias.","Um ano depois do dia em que o dinheiro das pessoas desapareceu.",
  "Um ano depois, ninguém gritava mais. Ninguém quebrava vidro. Ninguém dormia em fila na frente de banco.","As pessoas tinham aprendido a aceitar."),
 ("2026-12-01","prova","Se você tivesse a prova de que algo foi planejado… a quem entregaria?",("A todo mundo, agora.","Verdade escondida não serve para nada."),("A uma única pessoa de confiança.","Quem divulga cedo demais perde a prova."),"Todo mundo ou uma pessoa só?",
  "Quanto mais gente souber, mais difícil esconder.","Prova na mão errada vira arma contra você.","Sob tiros, Cláudio colocou um chip na mão de Rafael.",
  "— A prova de que o Confisco foi planejado.","Não foi falha de sistema. Foi o sistema funcionando exatamente como foi desenhado para funcionar."),
 ("2026-12-02","saber","Saber como uma manipulação funciona te protege dela?",("Protege.","Quem enxerga o truque não cai."),("Não protege.","Saber não é o mesmo que conseguir sair."),"Protege ou não protege?",
  "Conhecimento é a primeira defesa.","Entender a armadilha não abre a porta.","Ele reconhecia a técnica que estavam usando contra ele.",
  "Entender a técnica não a tornava menos eficaz. Era como saber o nome de uma doença enquanto ela avança.","O problema de reconhecer uma armadilha é que reconhecer não é o mesmo que ter escolha."),
 ("2026-12-03","dono","Um sistema precisa de um dono visível para funcionar?",("Precisa.","Sempre tem alguém no comando."),("Não precisa.","Ele funciona sozinho, com ou sem você."),"Tem dono ou funciona sozinho?",
  "Todo poder tem um rosto, mesmo escondido.","O mais perigoso é o que não precisa de rosto.","Na tela, um mapa que ele nunca tinha visto completo.",
  "Um circuito. Não um esquema: um circuito. Esquema tem começo e fim; circuito não tem nenhum dos dois.","— Não importa quem construiu. Importa que funciona."),
 ("2026-12-04","onze","Se alguém dissesse quem você é de verdade, quanto tempo você levaria para negar?",("Na hora.","Eu sei quem eu sou."),("Eu pensaria antes.","E se a pessoa estiver certa?"),"Na hora ou pensaria?",
  "Quem se conhece não hesita.","Hesitar é honestidade, não fraqueza.",None,None,None),
 ("2026-12-05","paciencia","O que é mais perigoso: quem tem pressa ou quem sabe esperar?",("Quem tem pressa.","Atropela tudo pelo caminho."),("Quem sabe esperar.","Ele nunca perde a hora certa."),"Pressa ou paciência?",
  None,None,"Maestro III sempre esperava.",
  "A certeza de que o tempo era um recurso que ele sempre teria em maior quantidade do que seus adversários.","Porque adversários têm pressa. Sistemas não."),
 ("2026-12-06","lado-certo","Ainda existe um lado certo a escolher?",("Existe.","Sempre existe o certo e o errado."),("Não existe mais.","Os dois lados servem ao mesmo dono."),"Existe ou não existe?",
  None,None,"Depois de semanas, a porta simplesmente se abriu. Ele saiu diferente.",
  "Alguma coisa tinha ficado para trás naquele quarto, e não era memória nem medo.","Era a versão de si mesmo que acreditava que existia um lado certo a escolher."),
 ("2026-12-07","reparar","Se alguém sumisse por semanas e voltasse, você repararia?",("Repararia.","Eu percebo quem está à minha volta."),("Talvez não.","A gente vive passando sem olhar."),"Repararia ou não?",
  "A gente sempre nota quem importa.","Na correria, ninguém vê ninguém.","Depois de semanas no escuro, ele pisou na calçada.",
  "Alguém passou por ele sem olhar, apressado, como se homens surgindo do nada em calçadas fossem parte normal da paisagem urbana.","Talvez fossem. Talvez ele nunca tivesse reparado antes."),
]

def confere(c):
    s = c.replace("“", "").replace("”", "").replace("…", "")
    for parte in re.split(r"\s—\s|^—\s", s):
        parte = parte.strip(" —")
        if parte and parte not in LIVRO:
            sys.exit(f"CITAÇÃO NÃO ENCONTRADA: {parte}")

for t in T:
    for c in (t[9], t[10]):
        if c: confere(c)
print("citações ok")

fila_d = sorted(glob.glob(os.path.join(RAIZ, "robo/musicas/back-in-back-3-*.m4a")))
fila_c = sorted(glob.glob(os.path.join(RAIZ, "robo/musicas/back-in-back-2-*.m4a"))) + sorted(glob.glob(os.path.join(RAIZ, "robo/musicas/raw-power-riff-*.m4a")))
est = json.load(open(os.path.join(RAIZ, "robo/estoque.json")))
datas = {t[0] for t in T}
est = [x for x in est if not (x["data"] in datas and x["tipo"] != "serie")]
novos = []
def gerar(spec, pasta, trecho=None):
    os.makedirs(pasta, exist_ok=True); sp = os.path.join(pasta, "spec.json"); json.dump(spec, open(sp, "w"), ensure_ascii=False, indent=1)
    cmd = ["python3", os.path.join(RAIZ, "robo/gerar-funcao.py"), sp, pasta] + ([trecho] if trecho else [])
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL)

for k, (data, pid, perg, A, B, palavras, argA, argB, ctx, c1, c2) in enumerate(T):
    base = f"fase8/{data}"; dow = __import__("datetime").date.fromisoformat(data).weekday()
    # 9h descoberta
    p = os.path.join(RAIZ, base, f"d-{pid}")
    gerar({"tipo":"video","funcao":"descoberta","rodape":"responda nos comentários","telas":[
        {"txt":perg,"dur":2.8},{"txt":A[0],"peq":A[1],"dur":2.4},{"txt":B[0],"peq":B[1],"dur":2.4},{"txt":palavras,"peq":"Uma palavra nos comentários.","dur":2.6}]}, p, fila_d[k % len(fila_d)])
    novos.append({"data":data,"hora":"09:00","tipo":"video","funcao":"descoberta","id":f"d-{pid}","video":f"{RAW}/{base}/d-{pid}/video.mp4",
        "legenda":f"{perg}\n\n{A[0]} {A[1]}\n{B[0]} {B[1]}\n\nResponda: {palavras}\n\n{TAGS_D}","tiktok":perg[:90],"trilha":os.path.basename(fila_d[k % len(fila_d)]),"formato":"Fase 8"})
    # 12h relacionamento (dias úteis)
    if argA and dow < 5:
        p = os.path.join(RAIZ, base, f"r-{pid}")
        fim = "Às 19h: a cena do livro em que essa pergunta aparece." if c1 else "Hoje, sexta, tem página nova do livro às 19h."
        gerar({"tipo":"carrossel","funcao":"relacionamento","rodape":"NEXO · uma pergunta por dia","telas":[
            {"txt":f"Hoje cedo a pergunta foi:","peq":perg},{"txt":argA,"peq":f"O argumento de quem responde: {A[0].rstrip('.')}"},
            {"txt":argB,"peq":f"O argumento de quem responde: {B[0].rstrip('.')}"},{"txt":"Qual pesa mais para você?","peq":f"Comente. {fim}"}]}, p)
        novos.append({"data":data,"hora":"12:00","tipo":"carrossel","funcao":"relacionamento","id":f"r-{pid}",
            "media":[f"{RAW}/{base}/r-{pid}/tela-{i}.jpg" for i in range(1,5)],
            "legenda":f"Os dois lados de uma pergunta: {perg}\n\nQual argumento pesa mais para você? Comente.\n\nNEXO, thriller político de Peres d'Souza.\n\n{TAGS_D}","tiktok":"Os dois lados da pergunta de hoje","formato":"Fase 8"})
    # 19h conversão (menos sexta)
    if c1 and dow != 4:
        p = os.path.join(RAIZ, base, f"c-{pid}"); tr = fila_c[k % len(fila_c)]
        gerar({"tipo":"video","funcao":"conversao","rodape":"NEXO · Peres d'Souza","telas":[
            {"txt":ctx,"dur":2.8},{"txt":c1,"citacao":True,"dur":3.2},{"txt":c2,"citacao":True,"dur":3.8},
            {"txt":"Leia o começo grátis.","peq":"E-book completo R$ 29,99 · link na bio","capa":True,"dur":3.0}]}, p, tr)
        novos.append({"data":data,"hora":"19:00","tipo":"video","funcao":"conversao","id":f"c-{pid}","video":f"{RAW}/{base}/c-{pid}/video.mp4",
            "legenda":f"{ctx}\n\nEssa cena está em NEXO, thriller político de Peres d'Souza. A pergunta de hoje cedo saiu daqui.\n\nLeia o começo grátis. Link na bio. E-book completo R$ 29,99.\n\n{TAGS_C}","tiktok":perg[:90],"trilha":os.path.basename(tr),"formato":"Fase 8"})
    print("ok", data)

est = sorted(est + novos, key=lambda x: (x["data"], x["hora"]))
json.dump(est, open(os.path.join(RAIZ, "robo/estoque.json"), "w"), ensure_ascii=False, indent=1)
print("estoque:", len(est), "itens; novos:", len(novos))
