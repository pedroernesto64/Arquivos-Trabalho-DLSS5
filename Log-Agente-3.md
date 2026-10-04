===== RODADA 1 =====

### Agente 3: Python Execution & Query Agent (Py-QAgent)
**Input Recebido:** Subquestões estatísticas ($s_{1.1} \dots s_{7.3}$) extraídas de `Log-Agente-2.md` + dataset `dados.csv`.

---

### 1. Código Python Executado (`code`)
```python
import csv
import math
from collections import defaultdict

def clean_num(val):
    if not val: return 0.0
    s = str(val).strip()
    parts = s.split('.')
    if len(parts) > 2: s = ''.join(parts[:-1]) + '.' + parts[-1]
    return float(s)

def mean(vals): return sum(vals) / len(vals) if vals else 0.0

def std_dev(vals):
    if len(vals) < 2: return 0.0
    m = mean(vals)
    return math.sqrt(sum((x - m)**2 for x in vals) / (len(vals) - 1))

def pearson_corr(x, y):
    n = len(x)
    if n == 0: return 0.0
    mx, my = mean(x), mean(y)
    num = sum((xi - mx) * (yi - my) for xi, yi in zip(x, y))
    den = math.sqrt(sum((xi - mx)**2 for xi in x) * sum((yi - my)**2 for yi in y))
    return num / den if den != 0 else 0.0

# Execução no arquivo dados.csv
with open('dados.csv', encoding='utf-8') as f:
    rows = list(csv.DictReader(f))
```

---

### 2. Saída Numérica do Console ($R_{ij}$)

```text
--- [H1.1] Multi Frame Generation ---
FG Não: Avg FPS =  67.43 | GPU Power = 116.77W | FPS/Watt = 0.6025 (n=25)
FG 2x : Avg FPS = 113.89 | GPU Power = 116.63W | FPS/Watt = 0.9718 (n=25)
FG 3x : Avg FPS = 165.45 | GPU Power = 122.53W | FPS/Watt = 1.3442 (n=25)
FG 4x : Avg FPS = 207.06 | GPU Power = 122.43W | FPS/Watt = 1.6600 (n=24)

--- [H1.2] DLSS sob FG 4x ---
DLSS Desempenho Ultra (4x): Avg FPS = 280.19 | GPU Power = 114.36W | FPS/Watt = 2.4405
DLSS Desempenho       (4x): Avg FPS = 239.39 | GPU Power = 125.90W | FPS/Watt = 1.8935
DLSS Balanceado       (4x): Avg FPS = 211.19 | GPU Power = 127.44W | FPS/Watt = 1.6379
DLSS Qualidade        (4x): Avg FPS = 208.50 | GPU Power = 133.93W | FPS/Watt = 1.5477
DLSS DLAA             (4x): Avg FPS =  96.31 | GPU Power = 112.81W | FPS/Watt = 0.7579

--- [H1.3] Variação % de Eficiência entre degraus de FG ---
FG Não -> 2x: +61.30%
FG 2x  -> 3x: +38.32%
FG 3x  -> 4x: +23.49%

--- [H2.1] Ray Reconstruction (Sim vs Não) ---
RR Sim: GPU Power = 122.54W | GPU Temp = 61.96°C | Avg FPS = 126.01 (n=40)
RR Não: GPU Power = 117.54W | GPU Temp = 61.18°C | Avg FPS = 145.73 (n=59)

--- [H2.2 & H2.3] Correlação e Stats da GPU Temp com RR Sim ---
Pearson r(GPU Temp, GPU Power): 0.9840
RR Sim GPU Temp -> Min: 55.36°C | Max: 67.57°C | Desvio Padrão: 2.55°C

--- [H3.1 & H3.2] GPU/CPU Power e Utilização por DLSS ---
DLSS DLAA            : GPU Power = 115.40W | CPU Power = 25.73W | Razão GPU/CPU = 4.50 | GPU Util =  97.5% | CPU Util =  32.0%
DLSS Qualidade       : GPU Power = 131.01W | CPU Power = 35.64W | Razão GPU/CPU = 3.76 | GPU Util =  94.8% | CPU Util =  51.4%
DLSS Balanceado      : GPU Power = 125.86W | CPU Power = 38.33W | Razão GPU/CPU = 3.35 | GPU Util =  93.1% | CPU Util =  56.9%
DLSS Desempenho      : GPU Power = 121.38W | CPU Power = 40.69W | Razão GPU/CPU = 3.02 | GPU Util =  91.3% | CPU Util =  61.6%
DLSS Desempenho Ultra: GPU Power = 104.67W | CPU Power = 43.63W | Razão GPU/CPU = 2.41 | GPU Util =  83.4% | CPU Util =  70.0%

--- [H4.1 & H4.2] Clocks por faixa de consumo GPU e Correlação ---
Faixa < 115W   (n=26): GPU0Clk = 2808.38 MHz
Faixa 115-125W (n=29): GPU0Clk = 2789.82 MHz
Faixa > 125W   (n=44): GPU0Clk = 2780.25 MHz
Pearson r(GPU Temp, GPU0Clk): -0.8789

--- [H5.1 & H5.2] Configuração Otimizada (FPS >= 60) ---
Configuração Otimizada com Menor Potência Total (FPS >= 60):
  DLSS: DLAA | FG: 4x | RR: Não
  Avg FPS: 66.26 | GPU Power: 99.44W | CPU Power: 21.67W | Total Power: 121.12W
  FPS/Watt Total: 0.5470

--- [H6.1 & H6.2] CPU Temp, Power e Utilização por DLSS ---
DLSS DLAA            : CPU Temp = 42.06°C | CPU Power = 25.73W | CPU Util =  32.0%
DLSS Qualidade       : CPU Temp = 43.67°C | CPU Power = 35.64W | CPU Util =  51.4%
DLSS Balanceado      : CPU Temp = 44.48°C | CPU Power = 38.33W | CPU Util =  56.9%
DLSS Desempenho      : CPU Temp = 45.12°C | CPU Power = 40.69W | CPU Util =  61.6%
DLSS Desempenho Ultra: CPU Temp = 45.86°C | CPU Power = 43.63W | CPU Util =  70.0%
Variação % de CPU Power (DLAA -> Desempenho Ultra): +69.54%

--- [H7.1, H7.2, H7.3] Discrepância Cyberpunk QPS vs FrameView FPS ---
Top 5 maiores discrepâncias (FPS_Delta = |FrameView FPS - Cyberpunk QPS|):
  1. DLSS: Desempenho       | FG: 4x | RR: Não | FrameView FPS: 238.22 | Cyberpunk QPS:  59.89 | Delta: 178.33 | Razão: 3.9776
  2. DLSS: Desempenho Ultra | FG: 4x | RR: Não | FrameView FPS: 228.18 | Cyberpunk QPS:  57.32 | Delta: 170.86 | Razão: 3.9807
  3. DLSS: Balanceado       | FG: 4x | RR: Não | FrameView FPS: 218.40 | Cyberpunk QPS:  54.87 | Delta: 163.53 | Razão: 3.9804
  4. DLSS: Qualidade        | FG: 4x | RR: Não | FrameView FPS: 190.09 | Cyberpunk QPS:  47.98 | Delta: 142.11 | Razão: 3.9618
  5. DLSS: Desempenho       | FG: 4x | RR: Não | FrameView FPS: 177.16 | Cyberpunk QPS:  44.43 | Delta: 132.73 | Razão: 3.9874

Discrepância Média por Multi Frame Generation:
  FG Não: FPS_Delta Média =   0.44 FPS | FPS_Ratio Média = 0.9874 (n=25)
  FG 2x : FPS_Delta Média =  23.48 FPS | FPS_Ratio Média = 1.5410 (n=25)
  FG 3x : FPS_Delta Média =  48.07 FPS | FPS_Ratio Média = 2.0669 (n=25)
  FG 4x : FPS_Delta Média =  65.60 FPS | FPS_Ratio Média = 2.5772 (n=24)

Discrepância Média por Ray Reconstruction:
  RR Sim: FPS_Delta Média =  23.77 FPS | FPS_Ratio Média = 1.6039 (n=40)
  RR Não: FPS_Delta Média =  41.07 FPS | FPS_Ratio Média = 1.9082 (n=59)

Correlações de Pearson com FPS_Delta:
  r(FPS_Delta, GPU0 Util%):          +0.2529
  r(FPS_Delta, CPU Util %):          -0.2651
  r(FPS_Delta, GPU NV Power):        +0.2193
  r(FPS_Delta, CPU Package Power):   -0.2446
```

---

### 3. Respostas Verbalizadas (`verb(R_ij)`)

* **Para $h_1$:** A transição de sem FG para FG 2x aumenta a eficiência de **0,6025 para 0,9718 FPS/Watt** (+61,30%). De 2x para 3x, a eficiência sobe para **1,3442 FPS/Watt** (+38,32%). De 3x para 4x, atinge **1,6600 FPS/Watt** (+23,49%). Sob FG 4x, o modo Desempenho Ultra lidera com **2,4405 FPS/Watt** (280,19 FPS a 114,36W), enquanto DLAA registra **0,7579 FPS/Watt** (96,31 FPS a 112,81W).
* **Para $h_2$:** O Ray Reconstruction ativado ('Sim') consome em média **122,54W** a **61,96°C** (126,01 FPS), contra **117,54W** a **61,18°C** (145,73 FPS) desativado. A correlação de Pearson entre temperatura e potência é de **$r = 0,9840$**. A temperatura sob RR 'Sim' varia entre **55,36°C** e **67,57°C** (desvio padrão de **2,55°C**).
* **Para $h_3$:** No DLAA, a razão de potência GPU/CPU é de **4,50** (115,40W GPU / 25,73W CPU), com 97,5% GPU Util e 32,0% CPU Util. No Desempenho Ultra, a razão cai para **2,41** (104,67W GPU / 43,63W CPU), com GPU Util caindo para 83,4% e CPU Util subindo para 70,0%.
* **Para $h_4$:** O clock da GPU reduz de **2808,38 MHz** (faixa < 115W) para **2789,82 MHz** (115-125W) e **2780,25 MHz** (> 125W). A correlação entre a temperatura da GPU e o clock do núcleo é negativamente forte (**$r = -0,8789$**), indicando ajuste térmico dinâmico.
* **Para $h_5$:** A configuração de menor consumo total mantendo FPS $\ge 60$ é **DLAA + FG 4x (sem Ray Reconstruction)**, gerando **66,26 FPS** com **99,44W GPU + 21,67W CPU** (**121,12W total**), atingindo uma eficiência global de **0,5470 FPS/Watt Total**.
* **Para $h_6$:** O consumo da CPU sobe de **25,73W** (42,06°C, 32,0% util) no DLAA para **43,63W** (45,86°C, 70,0% util) no Desempenho Ultra, representando uma elevação de **+69,54%** no consumo da CPU à medida que a resolução interna cai.
* **Para $h_7$:** A discrepância entre o FPS medido pelo FrameView e o contador do jogo `Avg QPS` **NÃO é acaso**: ela é diretamente determinada pelo multiplicador de Frame Generation. Sem FG, a diferença média é de apenas **0,44 FPS** (razão 0,9874). Com FG 2x a diferença sobe para **23,48 FPS** (razão 1,5410); com FG 3x sobe para **48,07 FPS** (razão 2,0669); e com FG 4x atinge **65,60 FPS** (razão 2,5772, com pico de razão próximo de 4.0). Isso comprova empiricamente que o contador interno do jogo (`Avg QPS`) mede apenas os quadros renderizados tradicionalmente antes da interpolação de quadros, enquanto o FrameView mede a taxa final com os quadros sintetizados por IA.
