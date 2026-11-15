import torch, torchaudio as ta, os, sys
sys.path.insert(0,os.path.dirname(__file__)); from falas import P
from chatterbox.mtl_tts import ChatterboxMultilingualTTS
torch.set_num_threads(os.cpu_count())
m=ChatterboxMultilingualTTS.from_pretrained(device="cpu")
os.makedirs("saida2/chatterbox",exist_ok=True)
for n,(d,t,sd) in P.items():
    if not n.startswith('jardel'): continue
    torch.manual_seed(sd)
    ref=f"saida2/qwen/{n}.wav"
    try:
        w=m.generate(t,language_id="pt",audio_prompt_path=ref if os.path.exists(ref) else None,exaggeration=0.6,cfg_weight=0.4)
        ta.save(f"saida2/chatterbox/{n}.wav",w,m.sr); print("ok",n,flush=True)
    except Exception as e: print("erro",n,e)
