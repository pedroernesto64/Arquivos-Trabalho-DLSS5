**$h_1$ (Escalabilidade de Eficiência com Multi Frame Generation):** Como o aumento progressivo do multiplicador de Multi Frame Generation (Sem FG, 2x, 3x e 4x) afeta a eficiência energética da GPU RTX 5060 em termos de FPS por Watt (`Avg FPS / GPU NV Power`) nos diferentes perfis de Qualidade DLSS?

#### Insight $h_1$ (Escalabilidade de Eficiência com Multi Frame Generation):
> O multiplicador de Multi Frame Generation 4x impulsiona a eficiência energética da RTX 5060 de 0,6025 FPS/Watt (sem FG) para 1,6600 FPS/Watt (+175,5%), com um aumento de consumo na GPU de apenas 4,8%. Combinado ao perfil DLSS Desempenho Ultra, o sistema atinge seu ápice absoluto de eficiência com 2,4405 FPS/Watt (280,19 FPS sob 114,36W). Isso comprova que a interpolação de quadros maximiza a fluidez sem inflacionar o envelope térmico ou elétrico do chip.



=======================================================================================



**$h_2$ (Custo Elétrico e Térmico do Ray Reconstruction):** Qual é o impacto adicional em consumo elétrico (`GPU NV Power`) e elevação térmica (`GPU0 Temp`) provocado pela ativação do Ray Reconstruction em comparação aos cenários em que apenas o Ray Tracing convencional está ativo?

#### Insight $h_2$ (Custo Elétrico e Térmico do Ray Reconstruction):
> A ativação do Ray Reconstruction eleva o consumo médio da GPU em 5,00W (de 117,54W para 122,54W) e a temperatura média em apenas 0,78°C (de 61,18°C para 61,96°C), apresentando uma correlação linear quase perfeita ($r = 0,9840$) entre potência e temperatura. No entanto, a funcionalidade acarreta uma redução média de 19,72 FPS no desempenho geral. Assim, o recurso exige avaliação de custo-benefício caso a prioridade seja a taxa de quadros máxima.



=======================================================================================



**$h_3$ (Balanço de Carga e Consumo Global GPU vs CPU):** De que maneira a alternância entre os modos DLSS de maior qualidade (como DLAA) e de maior desempenho (como Desempenho Ultra) altera a distribuição de consumo elétrico (`GPU NV Power` vs `CPU Package Power`) e os percentuais de utilização entre a RTX 5060 e a CPU i5-12400F?

#### Insight $h_3$ (Balanço de Carga e Consumo Global GPU vs CPU):
> A transição do DLSS DLAA para o modo Desempenho Ultra reduz o uso da GPU de 97,5% para 83,4% e desloca o gargalo para o i5-12400F, cuja utilização sobe de 32,0% para 70,0%. Consequentemente, a razão de potência GPU/CPU cai de 4,50 (115,40W GPU / 25,73W CPU) para 2,41 (104,67W GPU / 43,63W CPU). Esse comportamento evidencia que resoluções internas mais baixas sobrecarregam o processador, alterando a matriz energética do sistema.



=======================================================================================



**$h_4$ (Comportamento de Clocks da GPU sob Estresse Térmico/Energético):** Como a variação na taxa de consumo energético (`GPU NV Power`) e na temperatura da GPU (`GPU0 Temp`) afeta a estabilidade da frequência de clock do núcleo da GPU (`GPU0Clk`) e da memória (`GPU0MemClk`)?

#### Insight $h_4$ (Comportamento de Clocks da GPU sob Estresse Térmico/Energético):
> O clock do núcleo da RTX 5060 sofre uma diminuição gradual de 2808,38 MHz (sob consumo < 115W) para 2780,25 MHz (sob consumo > 125W) à medida que o consumo elétrico e a temperatura aumentam. Existe uma forte correlação negativa ($r = -0,8789$) entre a temperatura da GPU e a frequência do núcleo. Esse mecanismo reflete a atuação direta da gestão térmica dinâmica da GPU para conter o superaquecimento em cargas elevadas.



=======================================================================================



**$h_5$ (Configuração Otimizada para Eficiência Global do Sistema):** Qual combinação específica de parâmetros (Qualidade DLSS + Frame Generation + Ray Reconstruction) minimiza a potência total combinada do sistema (`GPU NV Power + CPU Package Power`) mantendo uma taxa de quadros fluida (ex: $\text{FPS} \ge 60$)?

#### Insight $h_5$ (Configuração Otimizada para Eficiência Global do Sistema):
> Para obter uma taxa fluida com o menor consumo elétrico combinado do sistema ($\text{FPS} \ge 60$), a combinação DLAA com FG 4x (sem Ray Reconstruction) revelou-se a mais econômica. Essa configuração entrega 66,26 FPS exigindo apenas 121,12W de potência total (99,44W na GPU e 21,67W na CPU). Trata-se da solução ideal para operar o conjunto RTX 5060 e i5-12400F com máxima eficiência energética global (0,5470 FPS/Watt Total).



=======================================================================================



**$h_6$ (Sensibilidade Térmica e Consumo da CPU com DLSS):** Em que medida a alteração da resolução interna de renderização proporcionada pelo DLSS impacta a temperatura de operação (`CPU Temp`) e a potência consumida (`CPU Package Power`) da CPU Intel Core i5-12400F durante o jogo?

#### Insight $h_6$ (Sensibilidade Térmica e Consumo da CPU com DLSS):
> A diminuição da resolução interna provocada pelos perfis mais agressivos de DLSS eleva progressivamente a temperatura e o consumo da CPU i5-12400F. O consumo da CPU escala de 25,73W (42,06°C) no DLAA até 43,63W (45,86°C) no Desempenho Ultra, representando um aumento de +69,54% no consumo do processador. Esse incremento térmico/elétrico confirma que a economia de potência na GPU em DLSS agressivo é parcialmente anulada pela maior exigência sobre a CPU.



=======================================================================================



**$h_7$ (Outliers entre as duas medidas de FPS):** Em alguns momentos há uma discrepância grande entre o FPS medido diretamente pelo jogo (`Avg QPS (CyberPunk)`) e o FPS medido pelo Frameview (`Avg FPS (FrameView)`). Essa discrepância tem relação com outras métricas, ou é mero acaso?

#### Insight $h_7$ (Discrepância nos Top 15 Outliers entre Cyberpunk QPS e FrameView FPS):
> A análise dos 15 registros de maior discrepância entre o FPS do jogo (`Avg QPS`) e o FrameView revela que 100% dos maiores outliers ocorrem exclusivamente sob FG 4x (66,7%) e FG 3x (33,3%), com um delta médio de 125,45 FPS e razão média de 3,4936. O caso limite foi registrado no DLSS Balanceado + FG 4x (sem RR), no qual o FrameView marcou 125,09 FPS enquanto a engine do jogo reportou apenas 30,96 QPS (razão de 4,0403). Isso comprova categoricamente que o contador interno do jogo desconsidera os quadros sintetizados por IA, os quais são capturados integralmente pelo medidor externo FrameView.