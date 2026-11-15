import torch, torchaudio as ta, os
from chatterbox.mtl_tts import ChatterboxMultilingualTTS
torch.set_num_threads(os.cpu_count()); os.makedirs("historia",exist_ok=True)
REF={"juju":"saida/qwen/juju.wav"}
FIX=[(12,"juju","Eu faço a tôrre!"),(12,"juju","Eu vou fazer a tôrre do castelo!")]
m=ChatterboxMultilingualTTS.from_pretrained(device="cpu",t3_model="v3")
for k,(i,who,t) in enumerate(FIX):
    for take,sd in enumerate((5,77,123)):
        torch.manual_seed(sd)
        w=m.generate(t,language_id="pt",audio_prompt_path=REF[who],exaggeration=0.6,cfg_weight=0.5,temperature=0.7)
        ta.save(f"historia/{i:02d}_{who}_fix{k}_t{take}.wav",w,m.sr); print("ok",k,take,flush=True)
