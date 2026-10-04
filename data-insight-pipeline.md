# Especificação da Arquitetura Multi-Agente para Análise de Dados (CSV / Pandas)
## Estudo: Eficiência Energética e Desempenho de GPU com DLSS 5 em Cyberpunk 2077

Esta especificação adapta a arquitetura do artigo *"An LLM-Based Approach for Insight Generation in Data Analysis"* (Sánchez Pérez et al., 2025) para operar **diretamente sobre arquivos CSV via scripts Python/Pandas** (sem passar por bancos SQL), garantindo que **100% dos cálculos numéricos sejam executados deterministicamente por scripts**, prevenindo alucinações matemáticas da LLM.

---

## 1. Visão Geral da Arquitetura Adaptada

```
+-----------------------------------------------------------------------------------+
| 1. HYPOTHESIS GENERATOR                                                           |
|    +-------------------------+         +----------------------------------+       |
|    | High-Level Generator    | ------> | Low-Level Generator              |       |
|    | (HL-G Agent)            | $h_i$   | (LL-G Agent)                     |       |
|    | Prompt macro/exploratório|         | Decompõe $h_i$ em subquestões    |       |
|    +-------------------------+         | estatísticas ($s_{ij}$)          |       |
|                                        +----------------------------------+       |
+---------------------------------------------------------|-------------------------+
                                                          | $s_{ij}$
                                                          v
+-----------------------------------------------------------------------------------+
| 2. PANDAS EXECUTION AGENT (Py-QAgent - Substitui Text-to-SQL)                     |
|    +------------------------------------------------------------------------+     |
|    | a. Geração de Script Python / Pandas a partir de $s_{ij}$               |     |
|    | b. Execução em Sandbox e Extração de Tabelas/Resultados ($R_{ij}$)      |     |
|    | c. Verbalização dos Resultados (`verb(R_{ij})`)                        |     |
|    | d. Validação de Relevância e Respondação ($score_a \ge 0.7$)            |     |
|    +------------------------------------------------------------------------+     |
+---------------------------------------------------------|-------------------------+
                                                          | `verb(R_{ij})`
                                                          v
+-----------------------------------------------------------------------------------+
| 3. SUMMARIZER & REFLECTION MODULE                                                 |
|    +------------------------------------------------------------------------+     |
|    | a. Síntese do Insight (Máx 3 frases, orientado a ações/decisões)       |     |
|    | b. Hallucination Detector & Reflexion Loop (Verificação estrita das    |     |
|    |    afirmações contra o output numérico real $R_{ij}$)                  |     |
|    +------------------------------------------------------------------------+     |
+-----------------------------------------------------------------------------------+
```

---

## 2. Adaptações Principais em Relação ao Artigo Original

1. **Substituição de Text-to-SQL por Python/Pandas Agent (Py-QAgent):**
   - Como os dados estão em uma planilha CSV de 100x16 células, o custo e overhead de subir um banco SQLite/Postgres são desnecessários.
   - O Py-QAgent gera scripts `.py` focados em Pandas para manipulação da tabela.

2. **Garantia de Cálculo via Script (Zero Math pela LLM):**
   - A LLM nunca faz somas, médias, divisões (ex: FPS/Watt), correlações ou percentuais na "cabeça".
   - O script Python lê o CSV, trata as colunas, calcula os indicadores (ex: `eficiencia_energetica = df['Avg FPS (FrameView)'] / df['GPU NV Power (Watts) (API)']`), e imprime o resultado exato formatado.

3. **Tratamento de Dados Locais (Parsing Numérico):**
   - O dataset `dados.csv` contém números formatados no padrão europeu/brasileiro com pontos em milhares ou decimais (ex: `2.808.441` ou `107.092`).
   - O Py-QAgent obrigatoriamente inclui uma etapa padronizada de *cleaning/parsing* no script Python antes de realizar qualquer agregação.

---

## 3. Descrição do Dataset (Dinfo & Dschema)

### `short(Dinfo)` (Usado pelo HL-G Agent)
> Base de dados de benchmarking de GPU executando o jogo Cyberpunk 2077 com tecnologia DLSS 5. Contém 100 medições cobrindo variações de qualidade DLSS (Desempenho Ultra a DLAA), Multi Frame Generation (2x, 3x, 4x), Ray Reconstruction e Ray Tracing, avaliando impacto em FPS, consumo energético da GPU/CPU (Watts), utilitário %, frequências de clock e temperaturas (C).

### `Dschema` Completo (Usado pelo LL-G, Py-QAgent e Summarizer)
- `Qualidade DLSS`: Categoria (Desempenho Ultra, Desempenho, Balanceado, Qualidade, DLAA)
- `Multi Frame Generation`: Categoria (2x, 3x, 4x)
- `Ray reconstruction`: Booleano/Texto (Sim, Não)
- `Tracing`: Texto (Ray tracing)
- `Avg QPS (CyberPunk)`: Numérico (Média de Quadros por Segundo reportado pelo jogo)
- `TimeStamp`: Data/Hora da medição
- `Avg FPS (FrameView)`: Numérico (Média de Quadros por Segundo medido via FrameView)
- `GPU0Clk(MHz)`: Numérico (Clock da GPU em MHz)
- `GPU0MemClk(MHz)`: Numérico (Clock da Memória da GPU em MHz)
- `GPU0 Util%`: Numérico (Percentual de uso da GPU)
- `GPU0 Temp (C)`: Numérico (Temperatura da GPU em °C)
- `GPU NV Power (Watts) (API)`: Numérico (Consumo elétrico da GPU em Watts)
- `CPUClk(MHz)`: Numérico (Clock da CPU em MHz)
- `CPU Util %`: Numérico (Percentual de uso da CPU)
- `CPU Temp (C)`: Numérico (Temperatura da CPU em °C)
- `CPU Package Power(Watts)`: Numérico (Consumo elétrico da CPU em Watts)

---

## 4. Script Modelo de Execução Automática (Pipeline Python)

Para rodar a arquitetura na prática no ambiente do projeto, fornecemos o script base que orquestra a chamada das LLMs e executa os códigos Pandas gerados:

```python
import pandas as pd
import numpy as np
import io

def parse_cyberpunk_csv(file_path):
    """
    Lê e limpa o dataset dados.csv garantindo tipos de dados corretos.
    """
    df = pd.read_csv(file_path)
    
    # Tratamento de colunas numéricas com formato pt-BR / europeu se necessário
    num_cols = [
        'Avg QPS (CyberPunk)', 'Avg FPS (FrameView)', 'GPU0Clk(MHz)',
        'GPU0MemClk(MHz)', 'GPU0 Util%', 'GPU0 Temp (C)',
        'GPU NV Power (Watts) (API)', 'CPUClk(MHz)', 'CPU Util %',
        'CPU Temp (C)', 'CPU Package Power(Watts)'
    ]
    
    for col in num_cols:
        if col in df.columns:
            # Converte para string e ajusta pontuação se necessário
            df[col] = df[col].astype(str).str.replace('.', '', regex=False).str.replace(',', '.', regex=False)
            # Para valores float com casas decimais mantidas adequadamente:
            df[col] = pd.to_numeric(df[col], errors='coerce')
            
    # Criação de Métricas Derivadas Padrão
    df['GPU_FPS_per_Watt'] = df['Avg FPS (FrameView)'] / df['GPU NV Power (Watts) (API)']
    df['Total_System_Power_Watts'] = df['GPU NV Power (Watts) (API)'] + df['CPU Package Power(Watts)']
    df['Total_FPS_per_Watt'] = df['Avg FPS (FrameView)'] / df['Total_System_Power_Watts']
    
    return df

# Exemplo de execução segura de script gerado pelo Py-QAgent
def execute_generated_py_code(code_str, df):
    local_vars = {'df': df, 'pd': pd, 'np': np}
    stdout_capture = io.StringIO()
    import sys
    sys_stdout_orig = sys.stdout
    sys.stdout = stdout_capture
    try:
        exec(code_str, {}, local_vars)
        output = stdout_capture.getvalue()
    except Exception as e:
        output = f"Erro na execução do script: {str(e)}"
    finally:
        sys.stdout = sys_stdout_orig
    return output
```

---

## 5. Resumo das Vantagens da Otimização CSV vs. SQL

1. **Latência Reduzida:** Acesso instantâneo em memória via Pandas, sem overhead de conexão com banco de dados.
2. **Confiabilidade Matemática Absoluta:** Como o Py-QAgent gera o script Pandas que calcula médias, razões e deltas, elimina-se o erro de "LLM Math".
3. **Auditabilidade Completa:** Cada insight gerado possui como rastreabilidade o script `.py` exato e o `execution_output` impresso do console.
