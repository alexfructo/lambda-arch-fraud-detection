# Business Case: Detecção de Fraudes em Cartões de Créditos

## **APRESENTAÇÃO**

Apresentamos esta proposta para implementação de uma Prova de Conceito para de Detecção de Fraudes em Transações com Cartões de Crédito.

Em um cenário onde a sofisticação dos crimes financeiros cresce exponencialmente, acreditamos que a tecnologia deve ser uma aliada estratégica na proteção do patrimônio institucional e de seus clientes.

Esta prova proposta representa o trabalho colaborativo de nossa equipe de estudantes do MBA de Engenharia de Dados, combinando estudos em engenharia de dados, ciência de dados, e do setor financeiro.

---

## **INTRODUÇÃO**

A transformação digital acelerou a adoção de serviços financeiros eletrônicos, mas, paralelamente, ampliou a superfície de ataque para atividades fraudulentas. As instituições financeiras globais reportam perdas anuais na casa de bilhões de dólares devido a fraudes, sem contar o dano irreparável à reputação e a perda de confiança dos clientes ([Juniper Agosto/2025](https://www.juniperresearch.com/press/fraud-to-cost-financial-institutions-58bn/), [TransUnion Outubro/2025](https://newsroom.transunion.com/h2-2025-global-fraud-report/)).

Sistemas tradicionais baseados em regras estáticas mostram-se cada vez mais insuficientes para lidar com a velocidade, volume e criatividade dos métodos fraudulentos atuais. A solução que propomos utiliza **Machine Learning (ML)** e **arquitetura de dados em tempo real** para criar um sistema de defesa proativo, adaptativo e inteligente.

---

## **CONTEXTO DE NEGÓCIO**

### **Desafios Atuais:**
*   **Falsos Positivos:** Regras rígidas geram um alto volume de alertas irrelevantes, sobrecarregando as equipes de análise e causando atrito para clientes legítimos.
*   **Tempo de Resposta:** A detecção *post-factum* permite que transações fraudulentas sejam concluídas, dificultando a recuperação dos valores.
*   **Fraudes Adaptativas:** Criminosos rapidamente identificam e burlam as regras de negócio predefinidas.
*   **Complexidade de Dados:** A incapacidade de correlacionar transações em tempo real com comportamentos históricos do cliente e fontes de dados externas limita a eficácia da detecção.

### **Oportunidades:**
*   **Redução de Perdas Financeiras:** Interceptar transações fraudulentas antes da sua conclusão.
*   **Melhoria da Experiência do Cliente:** Minimizar interrupções para transações legítimas, aumentando a satisfação e a fidelização.
*   **Preservação da Marca:** Reforçar a imagem de uma instituição segura e tecnologicamente avançada.
*   **Conformidade Regulatória:** Atender e exceder as exigências crescentes de órgãos reguladores.

---

## **PROPOSTA DE SOLUÇÃO**

Propomos a implementação de uma **Prova de Conceito de Detecção de Fraudes com Machine Learning em Tempo Real**.

**Principais Características:**

1.  **Modelagem Preditiva:** Uso de algoritmo de ML (Random Forest) treinado com dados históricos para pontuar o risco de cada transação instantaneamente.
2.  **Análise em Tempo Real:** Capacidade de analisar transações em milissegundos, permitindo a decisão de autorizar, negar ou solicitar autenticação adicional *antes* da finalização.
3.  **Aprendizado Contínuo:** O modelo é re-treinado periodicamente com novos dados, adaptando-se a padrões emergentes de fraude (conceito de *model drift*).
4.  **Painel Gerencial (Dashboard):** Visualização em tempo real de métricas de fraudes, eficácia do modelo e KPIs operacionais para apoio à decisão estratégica.

---

### **Arquitetura Atual**
```
[ Sistema Core Banking ] --> [ Filas de Transações ] --> [ Sistema Baseado em Regras ] --> [ Geração de Alertas ] --> [ Análise Manual por Backoffice ]
```
*   **Problemas:** Processamento por lotes (não real-time), dependência exclusiva de regras estáticas, alta taxa de falsos positivos, e resposta lenta.

### **Arquitetura Proposta **
```
                              |--> [ Modelo de ML em Tempo Real ] --> [ Sistema de Decisão ] --> [ Ação: Autorizar/Negar/Desafiar ]
[ Simulação de Core Banking ] --> [ Apache Kafka ]
                              |--> [ Data Lake (Armazenamento p/ Re-treino) ]

[ Simulação de Feedback do Analista ] --> [ Pipeline de Re-treino ] --> [ Serviço de Modelos ]
```
**Componentes da Arquitetura Proposta:**

1.  **Ingestão em Tempo Real (Apache Kafka):** Captura o fluxo de transações do core banking de forma resiliente e escalável.
2.  **Processamento de Stream (Spark Streaming):** Enriquece a transação com dados contextuais (histórico do cliente, blacklists, etc.) em milissegundos.
3.  **Serving do Modelo (MLflow):** Hospeda o modelo de ML treinado e disponibiliza uma API para pontuação de risco em baixa latência.
4.  **Sistema de Decisão:** Aplica a lógica de negócio com base no score de risco (ex: Score < 0.3: Autoriza; Score >= 0.3 e < 0.8: Desafia com 2FA; Score >= 0.8: Nega).
5.  **Data Lake (Amazon S3/Google Cloud Storage):** Armazena todas as transações e metadados para re-treino dos modelos.
6.  **Pipeline de Re-treino (Apache Airflow):** Orquestra jobs periódicos para re-treinar o modelo com novos dados, validar seu desempenho e promovê-lo para produção automaticamente.
7.  **Dashboard (Streamlit):** Apresenta os resultados e métricas para a equipe de operações e gestores.

---

## **RESULTADOS ESPERADOS**

### **Impacto Esperado:**

| Métrica | Situação Atual (Baseline) | Meta com a Solução | Impacto |
| :--- | :--- | :--- | :--- |
| **Fraudes Detectadas (Recall)** | ~40% (Estimado) | **> 85%** | **Redução de perdas financeiras em > 60%** |
| **Falsos Positivos** | Alto (> 90% dos alertas) | **< 15%** | **Melhoria significativa na CX e eficiência operacional** |
| **Tempo de Detecção** | Horas ou Dias | **Milissegundos** | **Prevenção proativa, antes da conclusão da fraude** |
| **Eficiência Operacional** | Análise manual intensiva | **Automação de > 70% das decisões** | **Equipe de análise focada em casos complexos** |

---

## PRÓXIMOS PASSOS

- Estender a solução para outros meios de pagamentos além dos cartões de créditos
- Implementar a solução utilizando dados reais de uma instituição financeira ou de meios de pagamentos 

---


Estamos confiantes de que esta solução não apenas resolverá um desafio crítico de negócio, mas também posicionará sua instituição na vanguarda da inovação e segurança no setor financeiro.

Atenciosamente,

## INTEGRANTES DO GRUPO 3
- Alex Fructo
- Luiz Fernando
- Marcos Kuniyoshi
- Priscila
- Yuri