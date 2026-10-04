===== RODADA 1 =====

### Agente 2: Low-Level Generator (LL-G)
**Input Recebido:** 7 Perguntas Macro de Alto Nível ($h_1 \dots h_7$) lidas diretamente do arquivo `Log-Agente-1.md` (com as hipóteses atualizadas pelo usuário) + Esquema Detalhado das 16 Colunas de `dados.csv`.

**Decomposição em Subquestões Estatísticas Concretas ($s_{ij}$):**

---

#### 📌 Para $h_1$ (Escalabilidade de Eficiência com Multi Frame Generation):
* **Subquestão $s_{1.1}$:** Calcular a média de `Avg FPS (FrameView)`, consumo elétrico da GPU `GPU NV Power (Watts) (API)` e a eficiência energética derivativa `GPU_FPS_per_Watt` (`Avg FPS / GPU NV Power`) agrupando os dados por multiplicador de `Multi Frame Generation` (Não, 2x, 3x, 4x).
* **Subquestão $s_{1.2}$:** Sob o regime de Frame Generation 4x (`Multi Frame Generation` == '4x'), calcular a média de `Avg FPS (FrameView)`, `GPU NV Power (Watts) (API)` e `GPU_FPS_per_Watt` para cada nível de `Qualidade DLSS` (Desempenho Ultra, Desempenho, Balanceado, Qualidade, DLAA).
* **Subquestão $s_{1.3}$:** Calcular a variação percentual (%) na eficiência média (`GPU_FPS_per_Watt`) na transição de FG 2x para FG 3x e de FG 3x para FG 4x.

---

#### 📌 Para $h_2$ (Custo Elétrico e Térmico do Ray Reconstruction):
* **Subquestão $s_{2.1}$:** Calcular a média de `GPU NV Power (Watts) (API)`, `GPU0 Temp (C)` e `Avg FPS (FrameView)` agrupada por presença de Ray Reconstruction (`Ray reconstruction` == 'Sim' vs 'Não').
* **Subquestão $s_{2.2}$:** Calcular o coeficiente de correlação estatística de Pearson $r$ entre a temperatura da GPU (`GPU0 Temp (C)`) e o consumo de potência (`GPU NV Power (Watts) (API)`).
* **Subquestão $s_{2.3}$:** Obter os valores mínimo, máximo e o desvio padrão da temperatura da GPU (`GPU0 Temp (C)`) quando o Ray Reconstruction está ativado.

---

#### 📌 Para $h_3$ (Balanço de Carga e Consumo Global GPU vs CPU):
* **Subquestão $s_{3.1}$:** Calcular a razão média de potência `GPU_CPU_Power_Ratio` (`GPU NV Power / CPU Package Power`), a utilização média da GPU (`GPU0 Util%`) e da CPU (`CPU Util %`) nos modos extremos de DLSS (`DLAA` vs `Desempenho Ultra`).
* **Subquestão $s_{3.2}$:** Calcular a potência média individual da CPU (`CPU Package Power(Watts)`) e da GPU (`GPU NV Power (Watts) (API)`) para todos os perfis de `Qualidade DLSS`.

---

#### 📌 Para $h_4$ (Comportamento de Clocks da GPU sob Estresse Térmico/Energético):
* **Subquestão $s_{4.1}$:** Calcular a frequência média de clock do núcleo da GPU `GPU0Clk(MHz)` e da memória `GPU0MemClk(MHz)` agrupada por faixas de consumo da GPU (< 115W, 115W-125W, > 125W).
* **Subquestão $s_{4.2}$:** Calcular o coeficiente de correlação de Pearson $r$ entre a temperatura da GPU (`GPU0 Temp (C)`) e o clock do núcleo da GPU (`GPU0Clk(MHz)`).

---

#### 📌 Para $h_5$ (Configuração Otimizada para Eficiência Global do Sistema):
* **Subquestão $s_{5.1}$:** Filtrar todos os registros onde `Avg FPS (FrameView)` $\ge 60$ e identificar a linha de configuração que apresenta a menor potência total combinada do sistema `Total_Power_Watts` (`GPU NV Power + CPU Package Power`).
* **Subquestão $s_{5.2}$:** Para a configuração otimizada encontrada, extrair os valores exatos de `Qualidade DLSS`, `Multi Frame Generation`, `Ray reconstruction`, `Avg FPS (FrameView)`, `GPU NV Power`, `CPU Package Power`, `Total_Power_Watts` e a eficiência global `Total_FPS_per_Watt` (`Avg FPS / Total_Power_Watts`).

---

#### 📌 Para $h_6$ (Sensibilidade Térmica e Consumo da CPU com DLSS):
* **Subquestão $s_{6.1}$:** Calcular a média de `CPU Temp (C)`, `CPU Package Power(Watts)` e `CPU Util %` agrupando os registros por cada nível de `Qualidade DLSS`.
* **Subquestão $s_{6.2}$:** Calcular a variação percentual (%) na potência consumida pela CPU (`CPU Package Power(Watts)`) do modo de renderização nativa (DLAA) para o modo de maior reconstrução (Desempenho Ultra).

---

#### 📌 Para $h_7$ (Outliers entre as duas medidas de FPS: Cyberpunk QPS vs FrameView FPS):
* **Subquestão $s_{7.1}$:** Criar as métricas derivadas de discrepância `FPS_Delta = abs(Avg FPS (FrameView) - Avg QPS (CyberPunk))` e a razão `FPS_Ratio = Avg FPS (FrameView) / Avg QPS (CyberPunk)`. Identificar os 5 registros com maior discrepância (`FPS_Delta`).
* **Subquestão $s_{7.2}$:** Calcular a média de `FPS_Delta` e `FPS_Ratio` agrupando por multiplicador de `Multi Frame Generation` (Não, 2x, 3x, 4x) e por `Ray reconstruction` (Sim vs Não) para verificar se o algoritmo de manipulação de quadros (FG / Ray Reconstruction) é o fator causador da divergência.
* **Subquestão $s_{7.3}$:** Calcular o coeficiente de correlação de Pearson entre a discrepância de FPS (`FPS_Delta`) e as métricas de utilização/carga do sistema (`GPU0 Util%`, `CPU Util %`, `GPU NV Power`, `CPU Package Power`).
