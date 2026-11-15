import torch, soundfile as sf, os, sys
sys.path.insert(0,os.path.dirname(__file__)); from falas import P
from qwen_tts import Qwen3TTSModel
torch.set_num_threads(os.cpu_count())
m=Qwen3TTSModel.from_pretrained("Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign",device_map="cpu",dtype=torch.float32)
os.makedirs("saida/qwen",exist_ok=True)
for n,(d,t) in P.items():
    torch.manual_seed(7)
    for lang in ("Portuguese","Auto"):
        try:
            w,sr=m.generate_voice_design(text=t,language=lang,instruct=d); break
        except Exception as e: print("erro",n,lang,e)
    sf.write(f"saida/qwen/{n}.wav",w[0],sr); print("ok",n,flush=True)
