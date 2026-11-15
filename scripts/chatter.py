import torch, torchaudio as ta, os, sys, glob
sys.path.insert(0,os.path.dirname(__file__)); from falas import REFS
from chatterbox.mtl_tts import ChatterboxMultilingualTTS
from huggingface_hub import snapshot_download
torch.set_num_threads(os.cpu_count()); os.makedirs("saida3/chatterbox",exist_ok=True)
def run(m,tag):
    for n,(r1,r2,t) in REFS.items():
        for i,ref in enumerate([r1,r2],1):
            if not os.path.exists(ref): print("sem ref",ref); continue
            torch.manual_seed(5)
            try:
                w=m.generate(t,language_id="pt",audio_prompt_path=ref,exaggeration=0.55,cfg_weight=0.5,temperature=0.7)
                ta.save(f"saida3/chatterbox/{n}_ref{i}_{tag}.wav",w,m.sr); print("ok",n,i,tag,flush=True)
            except Exception as e: print("erro",n,i,tag,e,flush=True)
# 1) multilingual V3
try: m=ChatterboxMultilingualTTS.from_pretrained(device="cpu",t3_model="v3"); run(m,"v3")
except Exception as e: print("v3 falhou",e); m=ChatterboxMultilingualTTS.from_pretrained(device="cpu"); run(m,"v2")
# 2) finetune pt-br
try:
    d=snapshot_download("ResembleAI/Chatterbox-Multilingual-pt-br"); fs=os.listdir(d); print("ptbr arquivos:",fs,flush=True)
    if "ve.pt" in fs and "s3gen.pt" in fs:
        mp=ChatterboxMultilingualTTS.from_local(d,"cpu")
    else:
        from safetensors.torch import load_file
        st=[f for f in fs if f.endswith(".safetensors")]; print("t3:",st)
        sd=load_file(os.path.join(d,st[0])); sd={k.replace("t3.",""):v for k,v in sd.items()}
        print(m.t3.load_state_dict(sd,strict=False)); mp=m
    run(mp,"ptbr")
except Exception as e: print("ptbr falhou",repr(e),flush=True)
