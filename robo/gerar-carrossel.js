// ROBO EDITOR NEXO - V3 (gerador de carrossel; caminho principal, sem Canva)
// Gera um carrossel de 4 telas (1080 x 1350 PNG) a partir de uma BASE e de uma PAUTA.
// Nao usa Canva nem internet para criar a arte (as fontes vem do Google Fonts se houver internet;
// sem internet, usa fontes do Windows).
//
// Como usar:  node gerar-carrossel.js            -> usa a proxima pauta nao usada e a base do dia
//             node gerar-carrossel.js preta       -> forca a base (branca, preta, viva, cinema)
//             node gerar-carrossel.js preta c1-dono  -> forca base e pauta
//
// Saida: pasta saida/AAAA-MM-DD_<pauta>/ com tela-1.png ... tela-4.png e legenda.txt
// A pauta usada e marcada em pautas.json ("usada": true) e anotada em log-editor.txt.

let chromium;
try { ({ chromium } = require('playwright-core')); } catch { ({ chromium } = require('playwright')); }
const fs = require('fs');
const path = require('path');

const PASTA = __dirname;
const LOG = path.join(PASTA, 'log-editor.txt');
function log(m) {
  const l = `[${new Date().toLocaleString('pt-BR')}] ${m}`;
  console.log(l);
  try { fs.appendFileSync(LOG, l + '\r\n', 'utf8'); } catch {}
}

// Bases: cores e fontes de cada visual
const BASES = {
  branca: { fundo: '#F0ECE4', texto: '#141416', destaque: '#B3261E', apoio: '#5D5C58', faixa: '#141416', faixaTexto: '#F0ECE4' },
  preta:  { fundo: '#0E0E10', texto: '#F4F2EE', destaque: '#D33A2C', apoio: '#9A9893', faixa: '#F4F2EE', faixaTexto: '#0E0E10' },
  viva:   { fundo: '#C8102E', texto: '#111111', destaque: '#FFFFFF', apoio: '#3A0A10', faixa: '#111111', faixaTexto: '#FFFFFF' },
  cinema: { fundo: 'radial-gradient(120% 90% at 75% 20%, #4A1410 0%, #1A0B0A 45%, #070707 100%)', texto: '#F3EDE4', destaque: '#E0483A', apoio: '#A89F95', faixa: '#E0483A', faixaTexto: '#0B0B0B' },
};
// Rodizio por dia da semana (0 = domingo)
const RODIZIO = ['preta', 'branca', 'preta', 'viva', 'branca', 'cinema', 'viva'];

function esc(s) { return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;'); }

function html(base, pauta, n) {
  const b = BASES[base];
  const total = 4;
  const fundo = b.fundo.startsWith('#') ? `background:${b.fundo};` : `background:${b.fundo};`;
  let corpo = '';
  if (n === 1) corpo = `<div class="frase g1">${esc(pauta.telas[0])}</div><div class="traco"></div>`;
  if (n === 2) corpo = `<div class="frase g2">${esc(pauta.telas[1])}</div>`;
  if (n === 3) corpo = `<div class="frase g3">${esc(pauta.telas[2])}</div><div class="impacto">${esc(pauta.impacto)}</div>`;
  if (n === 4) corpo = `
    <div class="frase final">“${esc(pauta.final)}”</div>
    <div class="linha"></div>
    <div class="nexo">NEXO</div>
    ${/tem um dono/i.test(pauta.final) ? '' : '<div class="tag">O sistema não tem lado. Ele tem um dono.</div>'}
    <div class="faixa">CAPÍTULO 1 GRÁTIS · LINK NA BIO</div>`;
  return `<!doctype html><html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Oswald:wght@400;600;700&family=Source+Serif+4:ital,opsz,wght@0,8..60,600;1,8..60,500&display=swap" rel="stylesheet">
<style>
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1350px}
body{${fundo}color:${b.texto};font-family:'Source Serif 4',Georgia,'Times New Roman',serif;position:relative;overflow:hidden}
.top,.bot{position:absolute;left:84px;right:84px;display:flex;justify-content:space-between;align-items:center;font-family:'Oswald','Arial Narrow',Arial,sans-serif;text-transform:uppercase;letter-spacing:.06em}
.top{top:70px;padding-bottom:22px;border-bottom:2px solid ${b.texto};font-size:28px}
.top b{font-weight:700;margin-right:14px}.top span{color:${b.apoio}}
.bot{bottom:70px;padding-top:22px;border-top:2px solid ${b.texto};font-size:26px;font-weight:600}
.bot .arr{color:${b.destaque}}
.miolo{position:absolute;left:84px;right:84px;top:200px;bottom:200px;display:flex;flex-direction:column;justify-content:center;gap:40px}
.frase{font-weight:600;line-height:1.14;letter-spacing:-.01em}
.g1{font-size:112px}.g2{font-size:96px}.g3{font-size:78px}
.final{font-size:68px;font-style:italic;font-weight:500}
.traco{width:130px;height:12px;background:${b.destaque}}
.impacto{overflow-wrap:normal;word-break:keep-all;font-family:'Oswald','Arial Narrow',Arial,sans-serif;font-weight:700;font-size:150px;line-height:1;color:${b.destaque};text-transform:uppercase}
.linha{height:2px;background:${b.texto}}
.nexo{font-family:'Oswald','Arial Narrow',Arial,sans-serif;font-weight:700;font-size:200px;line-height:.9}
.tag{font-size:40px;font-style:italic;color:${b.apoio}}
.faixa{background:${b.faixa};color:${b.faixaTexto};font-family:'Oswald','Arial Narrow',Arial,sans-serif;font-weight:600;font-size:40px;letter-spacing:.05em;text-align:center;padding:24px 0}
</style></head><body>
<div class="top"><div><b>NEXO</b><span>· CAPÍTULO ${esc(pauta.capitulo)}</span></div><div><span>${n}/${total}</span></div></div>
<div class="miolo">${corpo}</div>
<div class="bot"><div>PERES D'SOUZA</div><div class="arr">${n < total ? 'ARRASTA &gt;' : ''}</div></div>
<script>
// encolhe o texto que nao couber (palavras longas no destaque, frases longas)
window.fit = function () {
  const m = document.querySelector('.miolo');
  const W = m.clientWidth;
  for (const el of document.querySelectorAll('.impacto,.frase,.nexo')) {
    el.style.maxWidth = W + 'px';
    let t = parseFloat(getComputedStyle(el).fontSize);
    while (el.scrollWidth > W + 1 && t > 40) { t -= 4; el.style.fontSize = t + 'px'; }
  }
  for (const el of document.querySelectorAll('.frase,.impacto')) {
    let t = parseFloat(getComputedStyle(el).fontSize);
    while (m.scrollHeight > m.clientHeight + 1 && t > 40) { t -= 4; el.style.fontSize = t + 'px'; }
  }
};
fit();
</script>
</body></html>`;
}

(async () => {
  const [, , baseArg, pautaArg] = process.argv;
  const arqPautas = path.join(PASTA, 'pautas.json');
  const pautas = JSON.parse(fs.readFileSync(arqPautas, 'utf8'));
  // capitulo do mes: nov/2026 = cap. 1, dez/2026 = cap. 2, e assim por diante
  const ref = new Date(); const capMes = (ref.getFullYear() - 2026) * 12 + ref.getMonth() - 10 + 1;
  const pauta = pautaArg ? pautas.find((p) => p.id === pautaArg)
    : (pautas.find((p) => !p.usada && +p.capitulo === capMes) || pautas.find((p) => !p.usada));
  if (pauta && !pautaArg && +pauta.capitulo !== capMes) log(`AVISO: acabaram as pautas do capitulo ${capMes}; usando capitulo ${pauta.capitulo}.`);
  if (!pauta) { log('ESTOQUE VAZIO: nao ha pauta nao usada em pautas.json. Abasteca o estoque.'); return; }
  const base = BASES[baseArg] ? baseArg : RODIZIO[new Date().getDay()];

  const hoje = new Date().toISOString().slice(0, 10);
  const destino = path.join(PASTA, 'saida', `${hoje}_${pauta.id}`);
  fs.mkdirSync(destino, { recursive: true });

  const opcoes = { headless: true };
  if (process.env.ROBO_CHROME !== 'nao') opcoes.channel = 'chrome';
  let browser;
  try { browser = await chromium.launch(opcoes); }
  catch { delete opcoes.channel; browser = await chromium.launch(opcoes); }
  const page = await browser.newPage({ viewport: { width: 1080, height: 1350 } });

  for (let n = 1; n <= 4; n++) {
    await page.setContent(html(base, pauta, n), { waitUntil: 'networkidle', timeout: 20000 }).catch(() => {});
    await page.evaluate(() => document.fonts && document.fonts.ready).catch(() => {});
    await page.evaluate(() => window.fit && window.fit()).catch(() => {});
    await page.screenshot({ path: path.join(destino, `tela-${n}.png`) });
  }
  await browser.close();

  fs.writeFileSync(path.join(destino, 'legenda.txt'), pauta.legenda, 'utf8');
  fs.writeFileSync(path.join(destino, 'titulo-tiktok.txt'), pauta.tiktok || '', 'utf8');
  if (!pautaArg) { pauta.usada = true; pauta.usadaEm = hoje; fs.writeFileSync(arqPautas, JSON.stringify(pautas, null, 1), 'utf8'); }

  const restantes = pautas.filter((p) => !p.usada && +p.capitulo === capMes).length;
  log(`GERADO: ${pauta.id} na base ${base} -> ${destino} (pautas restantes do capitulo ${capMes}: ${restantes})`);
  if (restantes < 3) log('AVISO: estoque de pautas acabando. Peca ao Claude novas pautas.');
})().catch((e) => log('ERRO: ' + e.message));
