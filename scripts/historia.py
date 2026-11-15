import torch, torchaudio as ta, os
from chatterbox.mtl_tts import ChatterboxMultilingualTTS
torch.set_num_threads(os.cpu_count()); os.makedirs("historia",exist_ok=True)
REF={"narradora":"saida/qwen/narrador.wav","tata":"saida3/chatterbox/jardel_ref2_v3.wav","jardel":"saida3/chatterbox/jardel_ref1_v3.wav",
"juju":"saida/qwen/juju.wav","nayara":"saida/qwen/nayara.wav","lari":"saida/qwen/lari.wav","arthur":"saida/chatterbox/arthur.wav","mike":"saida/chatterbox/mike.wav"}
L=[("narradora","Era uma manhã de sol, e a turma da Tatá chegou correndo ao parquinho."),
("tata","Olha, gente! Ganhei um baldinho novo!"),
("narradora","O Mike trouxe o seu dinossauro preferido. Mas, quando a Lari quis segurar..."),
("lari","Dino! Quero!"),
("mike","Não! É meu! Ninguém mexe!"),
("narradora","A Lari ficou tristinha. E a turma ficou em silêncio."),
("jardel","Mike... brincar sozinho é bem menos divertido, né?"),
("tata","Toma, Lari. Pode brincar com o meu baldinho!"),
("narradora","O Mike viu o sorriso da Lari... e pensou um pouquinho."),
("mike","Lari... quer brincar com o dino comigo?"),
("lari","Oba!"),
("arthur","Vamos construir um castelo pro dino!"),
("juju","Eu faço a torre!"),
("nayara","Juntos é mais divertido!"),
("narradora","Naquele dia, a turma aprendeu que emprestar é um jeito de dizer: eu me importo com você."),
("narradora","Amigo de verdade divide, cuida e brinca junto. Como Jesus ensinou: amem-se uns aos outros. João, capítulo quinze, versículo doze.")]
m=ChatterboxMultilingualTTS.from_pretrained(device="cpu",t3_model="v3")
for i,(who,t) in enumerate(L):
    for take,sd in enumerate((5,77)):
        torch.manual_seed(sd)
        ex=0.5 if who=="narradora" else 0.6
        w=m.generate(t,language_id="pt",audio_prompt_path=REF[who],exaggeration=ex,cfg_weight=0.5,temperature=0.7)
        ta.save(f"historia/{i:02d}_{who}_t{take}.wav",w,m.sr); print("ok",i,who,take,flush=True)
