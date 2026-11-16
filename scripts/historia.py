import torch, torchaudio as ta, os
from chatterbox.mtl_tts import ChatterboxMultilingualTTS
torch.set_num_threads(os.cpu_count()); os.makedirs("vinheta",exist_ok=True)
T=["As Aventuras de Tatá e os Exploradores!","As Aventuras de Tatá... e os Exploradores!"]
m=ChatterboxMultilingualTTS.from_pretrained(device="cpu",t3_model="v3")
for k,t in enumerate(T):
    for take,sd in enumerate((5,77,123)):
        torch.manual_seed(sd)
        w=m.generate(t,language_id="pt",audio_prompt_path="saida/qwen/narrador.wav",exaggeration=0.75,cfg_weight=0.45,temperature=0.7)
        ta.save(f"vinheta/narr{k}_t{take}.wav",w,m.sr); print("ok",k,take,flush=True)
