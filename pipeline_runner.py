import csv
import math
from collections import defaultdict

def clean_num(val):
    if not val:
        return 0.0
    s = str(val).strip()
    parts = s.split('.')
    if len(parts) > 2:
        s = ''.join(parts[:-1]) + '.' + parts[-1]
    return float(s)

def mean(vals):
    return sum(vals) / len(vals) if vals else 0.0

def std_dev(vals):
    if len(vals) < 2: return 0.0
    m = mean(vals)
    var = sum((x - m)**2 for x in vals) / (len(vals) - 1)
    return math.sqrt(var)

def pearson_corr(x, y):
    n = len(x)
    if n == 0: return 0.0
    mx, my = mean(x), mean(y)
    num = sum((xi - mx) * (yi - my) for xi, yi in zip(x, y))
    den = math.sqrt(sum((xi - mx)**2 for xi in x) * sum((yi - my)**2 for yi in y))
    return num / den if den != 0 else 0.0

def run_agent_3():
    with open('dados.csv', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    parsed = []
    for r in rows:
        qps = clean_num(r['Avg QPS (CyberPunk)'])
        fps = clean_num(r['Avg FPS (FrameView)'])
        gpu_power = clean_num(r['GPU NV Power (Watts) (API)'])
        cpu_power = clean_num(r['CPU Package Power(Watts)'])
        gpu_temp = clean_num(r['GPU0 Temp (C)'])
        cpu_temp = clean_num(r['CPU Temp (C)'])
        gpu_util = clean_num(r['GPU0 Util%'])
        cpu_util = clean_num(r['CPU Util %'])
        gpu_clk = clean_num(r['GPU0Clk(MHz)'])
        cpu_clk = clean_num(r['CPUClk(MHz)'])
        
        fps_per_watt = fps / gpu_power if gpu_power > 0 else 0.0
        total_power = gpu_power + cpu_power
        total_fps_per_watt = fps / total_power if total_power > 0 else 0.0
        gpu_cpu_ratio = gpu_power / cpu_power if cpu_power > 0 else 0.0

        fps_delta = abs(fps - qps)
        fps_ratio = fps / qps if qps > 0 else 0.0

        item = {
            'dlss': r['Qualidade DLSS'],
            'fg': r['Multi Frame Generation'],
            'rr': r['Ray reconstruction'],
            'tracing': r['Tracing'],
            'qps': qps,
            'fps': fps,
            'gpu_power': gpu_power,
            'cpu_power': cpu_power,
            'gpu_temp': gpu_temp,
            'cpu_temp': cpu_temp,
            'gpu_util': gpu_util,
            'cpu_util': cpu_util,
            'gpu_clk': gpu_clk,
            'cpu_clk': cpu_clk,
            'fps_per_watt': fps_per_watt,
            'total_power': total_power,
            'total_fps_per_watt': total_fps_per_watt,
            'gpu_cpu_ratio': gpu_cpu_ratio,
            'fps_delta': fps_delta,
            'fps_ratio': fps_ratio
        }
        parsed.append(item)

    print("=================== OUTPUT DO AGENTE 3 (Py-QAgent) ===================")

    # H1
    print("\n--- [H1.1] Multi Frame Generation ---")
    fg_groups = defaultdict(list)
    for p in parsed: fg_groups[p['fg']].append(p)
    for fg_k in ['Não', '2x', '3x', '4x']:
        grp = fg_groups[fg_k]
        print(f"FG {fg_k:3s}: Avg FPS = {mean([x['fps'] for x in grp]):6.2f} | GPU Power = {mean([x['gpu_power'] for x in grp]):6.2f}W | FPS/Watt = {mean([x['fps_per_watt'] for x in grp]):.4f} (n={len(grp)})")

    print("\n--- [H1.2] DLSS sob FG 4x ---")
    fg4 = [p for p in parsed if p['fg'] == '4x']
    dlss_g = defaultdict(list)
    for p in fg4: dlss_g[p['dlss']].append(p)
    for dlss_k in ['Desempenho Ultra', 'Desempenho', 'Balanceado', 'Qualidade', 'DLAA']:
        grp = dlss_g[dlss_k]
        print(f"DLSS {dlss_k:16s} (4x): Avg FPS = {mean([x['fps'] for x in grp]):6.2f} | GPU Power = {mean([x['gpu_power'] for x in grp]):6.2f}W | FPS/Watt = {mean([x['fps_per_watt'] for x in grp]):.4f}")

    print("\n--- [H1.3] Variação % de Eficiência entre degraus de FG ---")
    eff_non = mean([x['fps_per_watt'] for x in fg_groups['Não']])
    eff_2x = mean([x['fps_per_watt'] for x in fg_groups['2x']])
    eff_3x = mean([x['fps_per_watt'] for x in fg_groups['3x']])
    eff_4x = mean([x['fps_per_watt'] for x in fg_groups['4x']])
    print(f"FG Não -> 2x: {((eff_2x - eff_non)/eff_non)*100:+.2f}%")
    print(f"FG 2x  -> 3x: {((eff_3x - eff_2x)/eff_2x)*100:+.2f}%")
    print(f"FG 3x  -> 4x: {((eff_4x - eff_3x)/eff_3x)*100:+.2f}%")

    # H2
    print("\n--- [H2.1] Ray Reconstruction (Sim vs Não) ---")
    rr_g = defaultdict(list)
    for p in parsed: rr_g[p['rr']].append(p)
    for rr_k in ['Sim', 'Não']:
        grp = rr_g[rr_k]
        print(f"RR {rr_k:3s}: GPU Power = {mean([x['gpu_power'] for x in grp]):6.2f}W | GPU Temp = {mean([x['gpu_temp'] for x in grp]):5.2f}°C | Avg FPS = {mean([x['fps'] for x in grp]):6.2f} (n={len(grp)})")

    print("\n--- [H2.2 & H2.3] Correlação e Stats da GPU Temp com RR Sim ---")
    r_temp_pow = pearson_corr([p['gpu_temp'] for p in parsed], [p['gpu_power'] for p in parsed])
    rr_sim_temps = [p['gpu_temp'] for p in rr_g['Sim']]
    print(f"Pearson r(GPU Temp, GPU Power): {r_temp_pow:.4f}")
    print(f"RR Sim GPU Temp -> Min: {min(rr_sim_temps):.2f}°C | Max: {max(rr_sim_temps):.2f}°C | Desvio Padrão: {std_dev(rr_sim_temps):.2f}°C")

    # H3
    print("\n--- [H3.1 & H3.2] GPU/CPU Power e Utilização por DLSS ---")
    dlss_all_g = defaultdict(list)
    for p in parsed: dlss_all_g[p['dlss']].append(p)
    for dlss_k in ['DLAA', 'Qualidade', 'Balanceado', 'Desempenho', 'Desempenho Ultra']:
        grp = dlss_all_g[dlss_k]
        r_pow = mean([x['gpu_cpu_ratio'] for x in grp])
        gp = mean([x['gpu_power'] for x in grp])
        cp = mean([x['cpu_power'] for x in grp])
        gu = mean([x['gpu_util'] for x in grp])
        cu = mean([x['cpu_util'] for x in grp])
        print(f"DLSS {dlss_k:16s}: GPU Power = {gp:6.2f}W | CPU Power = {cp:5.2f}W | Razão GPU/CPU = {r_pow:4.2f} | GPU Util = {gu:5.1f}% | CPU Util = {cu:5.1f}%")

    # H4
    print("\n--- [H4.1 & H4.2] Clocks por faixa de consumo GPU e Correlação ---")
    b1 = [p for p in parsed if p['gpu_power'] < 115.0]
    b2 = [p for p in parsed if 115.0 <= p['gpu_power'] <= 125.0]
    b3 = [p for p in parsed if p['gpu_power'] > 125.0]
    print(f"Faixa < 115W   (n={len(b1):2d}): GPU0Clk = {mean([x['gpu_clk'] for x in b1]):.2f} MHz | MemClk = {mean([x['gpu_mem_clk'] if 'gpu_mem_clk' in x else x['gpu_clk'] for x in b1]):.2f} MHz")
    print(f"Faixa 115-125W (n={len(b2):2d}): GPU0Clk = {mean([x['gpu_clk'] for x in b2]):.2f} MHz")
    print(f"Faixa > 125W   (n={len(b3):2d}): GPU0Clk = {mean([x['gpu_clk'] for x in b3]):.2f} MHz")
    r_temp_clk = pearson_corr([p['gpu_temp'] for p in parsed], [p['gpu_clk'] for p in parsed])
    print(f"Pearson r(GPU Temp, GPU0Clk): {r_temp_clk:.4f}")

    # H5
    print("\n--- [H5.1 & H5.2] Configuração Otimizada (FPS >= 60) ---")
    valid_60 = [p for p in parsed if p['fps'] >= 60.0]
    valid_sorted = sorted(valid_60, key=lambda x: x['total_power'])
    opt = valid_sorted[0]
    print(f"Configuração Otimizada com Menor Potência Total (FPS >= 60):")
    print(f"  DLSS: {opt['dlss']} | FG: {opt['fg']} | RR: {opt['rr']}")
    print(f"  Avg FPS: {opt['fps']:.2f} | GPU Power: {opt['gpu_power']:.2f}W | CPU Power: {opt['cpu_power']:.2f}W | Total Power: {opt['total_power']:.2f}W")
    print(f"  FPS/Watt Total: {opt['total_fps_per_watt']:.4f}")

    # H6
    print("\n--- [H6.1 & H6.2] CPU Temp, Power e Utilização por DLSS ---")
    dlaa_cp = mean([x['cpu_power'] for x in dlss_all_g['DLAA']])
    du_cp = mean([x['cpu_power'] for x in dlss_all_g['Desempenho Ultra']])
    diff_cp_pct = ((du_cp - dlaa_cp) / dlaa_cp) * 100.0
    for dlss_k in ['DLAA', 'Qualidade', 'Balanceado', 'Desempenho', 'Desempenho Ultra']:
        grp = dlss_all_g[dlss_k]
        print(f"DLSS {dlss_k:16s}: CPU Temp = {mean([x['cpu_temp'] for x in grp]):5.2f}°C | CPU Power = {mean([x['cpu_power'] for x in grp]):5.2f}W | CPU Util = {mean([x['cpu_util'] for x in grp]):5.1f}%")
    print(f"Variação % de CPU Power (DLAA -> Desempenho Ultra): {diff_cp_pct:+.2f}%")

    # H7 (Discrepância QPS vs FPS)
    print("\n--- [H7.1, H7.2, H7.3] Discrepância Cyberpunk QPS vs FrameView FPS ---")
    sorted_by_delta = sorted(parsed, key=lambda x: x['fps_delta'], reverse=True)
    print("Top 5 maiores discrepâncias (FPS_Delta = |FrameView FPS - Cyberpunk QPS|):")
    for i, p in enumerate(sorted_by_delta[:5], 1):
        print(f"  {i}. DLSS: {p['dlss']:16s} | FG: {p['fg']:2s} | RR: {p['rr']:3s} | FrameView FPS: {p['fps']:6.2f} | Cyberpunk QPS: {p['qps']:6.2f} | Delta: {p['fps_delta']:6.2f} | Razão: {p['fps_ratio']:.4f}")

    print("\nDiscrepância Média por Multi Frame Generation:")
    for fg_k in ['Não', '2x', '3x', '4x']:
        grp = fg_groups[fg_k]
        m_delta = mean([x['fps_delta'] for x in grp])
        m_ratio = mean([x['fps_ratio'] for x in grp])
        print(f"  FG {fg_k:3s}: FPS_Delta Média = {m_delta:6.2f} FPS | FPS_Ratio Média = {m_ratio:.4f} (n={len(grp)})")

    print("\nDiscrepância Média por Ray Reconstruction:")
    for rr_k in ['Sim', 'Não']:
        grp = rr_g[rr_k]
        m_delta = mean([x['fps_delta'] for x in grp])
        m_ratio = mean([x['fps_ratio'] for x in grp])
        print(f"  RR {rr_k:3s}: FPS_Delta Média = {m_delta:6.2f} FPS | FPS_Ratio Média = {m_ratio:.4f} (n={len(grp)})")

    r_delta_gpu_util = pearson_corr([p['fps_delta'] for p in parsed], [p['gpu_util'] for p in parsed])
    r_delta_cpu_util = pearson_corr([p['fps_delta'] for p in parsed], [p['cpu_util'] for p in parsed])
    r_delta_gpu_power = pearson_corr([p['fps_delta'] for p in parsed], [p['gpu_power'] for p in parsed])
    r_delta_cpu_power = pearson_corr([p['fps_delta'] for p in parsed], [p['cpu_power'] for p in parsed])

    print("\nCorrelações de Pearson com FPS_Delta:")
    print(f"  r(FPS_Delta, GPU0 Util%):          {r_delta_gpu_util:+.4f}")
    print(f"  r(FPS_Delta, CPU Util %):          {r_delta_cpu_util:+.4f}")
    print(f"  r(FPS_Delta, GPU NV Power):        {r_delta_gpu_power:+.4f}")
    print(f"  r(FPS_Delta, CPU Package Power):   {r_delta_cpu_power:+.4f}")

if __name__ == '__main__':
    run_agent_3()
