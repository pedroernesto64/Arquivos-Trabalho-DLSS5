# Análise de Eficiência Energética e Desempenho do DLSS 4.5 com Pipeline Multi-Agente

Este repositório contém os dados, scripts e logs referentes à pesquisa acadêmica que avalia o impacto do algoritmo **DLSS 4.5** (incluindo *Frame Generation* até $4\times$, *Ray Reconstruction* e perfis de upscaling) na eficiência energética e no comportamento térmico de hardware, utilizando o jogo *Cyberpunk 2077* em uma GPU NVIDIA RTX 5060 e CPU Intel Core i5-12400F.

A análise descrita no artigo associado emprega uma arquitetura inovadora baseada em **múltiplos agentes de Grandes Modelos de Linguagem (LLMs)** para automatizar a formulação de hipóteses, o processamento computacional de dados e a validação de *insights*.

---

## 📂 Estrutura do Repositório

- **`Arquivos-Trabalho-DLSS5/`**: Diretório principal contendo os materiais complementares do projeto.
  - `dados.csv`: Conjunto de dados brutos coletados via NVIDIA FrameView durante os benchmarks.
  - `pipeline_runner.py`: Script Python responsável pela execução e processamento das consultas analíticas.
  - `High-Level-Generator.md` / `Low-Level-Generator.md`: Prompts e saídas associados à definição de hipóteses e métricas objetivas.
  - `Insight-Summarizer-And-Hallucination-Reflector.md`: Módulo de sumarização e reflexão iterativa para mitigação de alucinações nas LLMs.
  - `Log-Agente-[1-4].md`: Histórico e logs de execução dos agentes da pipeline.
  - `Resultados-Rodada-[1-3].md`: Dados processados e respostas obtidas nas diferentes rodadas de testes.
  - `Underlying-Hardware-And-Software.md`: Especificações técnicas do ambiente de teste.
- **Artigos Principais**:
  - `Análise-de-Eficiência-Energética-do-Algoritmo-de-Renderização-Neural-Guiada-por-3D-DLSS-4.5.pdf`: Artigo completo em português detalhando a metodologia e os resultados.
  - `An-LLM-Based-Approach-for-Insight-Generation-in-Data-Analysis.pdf`: Referência metodológica sobre a arquitetura de múltiplos agentes.

---

## ⚙️ Principais Conclusões do Estudo

1. **Eficiência do Frame Generation ($4\times$):** Elevou a eficiência energética para $1,66\text{ FPS/Watt}$ (um aumento de $175,5\%$ na fluidez) com um incremento marginal de apenas $4,8\%$ no consumo elétrico da GPU.
2. **Deslocamento de Gargalo:** Perfis de upscaling agressivos (como *Desempenho Ultra*) reduzem a carga da placa gráfica, mas transferem o gargalo e elevam o consumo térmico/elétrico da CPU em até $69,54\%$.
3. **Ponto de Equilíbrio Ideal:** A combinação entre a resolução nativa (DLAA) e o *Frame Generation $4\times$* (sem *Ray Reconstruction*) demonstrou ser a configuração mais vantajosa, equilibrando alta taxa de quadros e menor desgaste termelétrico global.
4. **Discrepâncias de FPS:** Constatou-se que a engine do jogo desconsidera quadros sintetizados por IA, enquanto o monitoramento externo (FrameView) contabiliza a taxa real, gerando discrepâncias proporcionais ao multiplicador de FG utilizado.

---

## 🚀 Como Executar o Pipeline de Análise

Certifique-se de ter o Python instalado e execute o script de automação para reprocessar as métricas a partir do conjunto de dados:

```bash
python Arquivos-Trabalho-DLSS5/pipeline_runner.py
```

---

## 👥 Autores (UNIFESP)
- Bernardo F. de Souza
- Lucas B. de Souza
- Pedro D. Pilchowski
- Sérgio G. Filho

*Instituto de Ciência e Tecnologia – Universidade Federal de São Paulo (UNIFESP)*
