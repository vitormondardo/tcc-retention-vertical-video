# 📱 A Influência da Retenção de Tela Vertical no Comportamento de Consumo

> Trabalho de Conclusão de Curso — Bacharelado em Sistemas de Informação

<div align="center">
  <a href="https://python.org">
    <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"/>
  </a>
  <a href="https://jupyter.org">
    <img src="https://img.shields.io/badge/Jupyter-F37626?style=for-the-badge&logo=jupyter&logoColor=white" alt="Jupyter"/>
  </a>
  <a href="https://scikit-learn.org">
    <img src="https://img.shields.io/badge/scikit_learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white" alt="scikit-learn"/>
  </a>
  <br>
  <img src="https://img.shields.io/badge/Status-Em_Desenvolvimento-FFD700?style=for-the-badge&logoColor=black" alt="Status"/>
  <img src="https://img.shields.io/badge/Licença-Acadêmica-lightgrey?style=for-the-badge" alt="Licença"/>
</div>
---

## 📋 Sobre o Projeto

Este trabalho investiga **como a retenção de atenção em vídeos verticais influencia o comportamento de consumo dos usuários** em plataformas digitais como TikTok e YouTube Shorts.

A pesquisa aplica técnicas de **Ciência de Dados, Análise de Dados e Machine Learning** para identificar quais métricas de retenção — como tempo médio assistido, taxa de conclusão e percentual assistido — possuem maior correlação com engajamento e comportamento de consumo, contribuindo com evidências empíricas para o campo do marketing digital.

### ❓ Questão de Pesquisa

> *Como a retenção de atenção em conteúdos em tela vertical influencia o comportamento de consumo dos usuários em plataformas digitais?*

---

## 🎯 Objetivos

**Geral:** Analisar a influência da retenção de atenção em vídeos verticais sobre o comportamento de consumo dos usuários em plataformas digitais.

**Específicos:**
- a) Revisar a literatura sobre atenção, retenção de tela e comportamento de consumo em plataformas;
- b) Identificar os principais fatores que influenciam a retenção de atenção em vídeos curtos verticais;
- c) Coletar e organizar dados sobre métricas de retenção e comportamento de engajamento;
- d) Aplicar técnicas de análise de dados e aprendizado de máquina para verificar correlações entre retenção e comportamento de consumo.

---

## 🗂️ Estrutura do Repositório

```
tcc-retencao-video-vertical/
│
├── README.md                                         # Este arquivo
│
├── TCCII_pipeline_retencao_video_vertical.ipynb      # Pipeline principal de análise
│
├── data/
│   ├── TikTokData_1.xlsx                             # Dataset real — canal TikTok (Zawacki, 2021–2022)
│   ├── TikTokData_Video_Uploads.csv                  # Dados de uploads do TikTok
│   ├── youtube_shorts_tiktok_trends_2025.csv         # Dataset público de tendências (48k+ registros)
│   └── DATA_DICTIONARY_1.csv                         # Dicionário de dados (58 variáveis)
│
├── docs/
│   ├── TCC_Vitor_Hugo_M_Silveira.pdf                 # Trabalho escrito completo
│   └── MVP_TCC_I.pdf                                 # Projeto Mínimo Viável (TCC I)
│
├── dashboards/
│   ├── dashboard_1_tiktok_real_1.png                 # Análise do canal TikTok real
│   ├── dashboard_2_comparative_1.png                 # Análise comparativa (Zawacki aprofundado)
│   ├── dashboard_3_insights_1.png                    # TikTok vs YouTube Shorts
│   ├── dashboard_4_ml_1.png                          # Modelos de Machine Learning
│   ├── dashboard_1_modelos_cenarios.png              # Comparativo modelos × cenários
│   ├── dashboard_2_zawacki_aprofundado.png           # Análise aprofundada Zawacki
│   ├── dashboard_3_tiktok_vs_youtube.png             # Comparativo de plataformas
│   └── dashboard_4_importancias_comparativas.png     # Importância de features
│
└── references/
    ├── vertical_video_a_review_of_the_literature_on_communication.pdf
    ├── shortform_video_content_SVC_engagement_and_marketing_capabilities.pdf
    ├── Algorithmic_Personalization_in_Social_Media_Marketing.pdf
    ├── This_Way_Up__The_Effectiveness_of_Mobile_Vertical_Video_Marketing.pdf
    ├── Driving_Factors_and_Moderating_Effects_Behind_Citizen_Engagement.pdf
    ├── the_attention_span_economy.pdf
    ├── the_economics_of_attention.pdf
    └── influence_of_social_media_on_consumer_behavior.pdf
```

---

## ⚡ Quick Start

### Pré-requisitos

- Python 3.10+
- JupyterLab
- VirtualBox (ambiente de execução isolado — opcional, mas recomendado)

### Instalação

```bash
# 1. Clone o repositório
git clone https://github.com/vitormondardo/tcc-retencao-video-vertical.git
cd tcc-retencao-video-vertical

# 2. Crie um ambiente virtual
python -m venv venv
source venv/bin/activate        # Linux/Mac
venv\Scripts\activate           # Windows

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Abra o notebook principal
jupyter notebook TCCII_pipeline_retencao_video_vertical.ipynb
```

### `requirements.txt`

```
pandas>=2.0
numpy>=1.24
scikit-learn>=1.3
matplotlib>=3.7
seaborn>=0.12
scipy>=1.11
jupyterlab>=4.0
openpyxl>=3.1
```

---

## 🔬 Metodologia

A pesquisa é **quantitativa, exploratória e descritiva**, combinando análise documental com modelagem preditiva.

### Datasets Utilizados

| Dataset | Fonte | Registros | Descrição |
|---|---|---|---|
| TikTokData_Video_Uploads.csv | Emily Zawacki (Kaggle/Figshare) | 48 vídeos | Métricas reais de canal de Geologia (2021–2022) |
| youtube_shorts_tiktok_trends_2025.csv | Público | 48.079 linhas | Tendências TikTok e YouTube Shorts, 58 variáveis |

### Métricas Analisadas

| Métrica | Unidade | Definição |
|---|---|---|
| `duration` | Segundos | Duração total do vídeo |
| `avg_watch_time` | Segundos | Tempo médio de visualização |
| `avg_pct_watched` | % | Percentual médio assistido |
| `completion_rate` | % | Taxa de conclusão do vídeo |
| `views` | Unidades | Total de visualizações |
| `likes / shares / comments` | Unidades | Métricas de engajamento |
| `engagement_rate` | % | Taxa geral de engajamento |

### Pipeline de Análise

```
Coleta de Dados → Limpeza (Pandas/NumPy) → EDA → Análise Estatística
       ↓
Modelagem ML → Validação Cruzada (LOOCV / 5-fold CV) → Insights → Dashboards
```

---

## 🤖 Modelos de Machine Learning

Quatro modelos foram selecionados e comparados via **Cross-Validation (LOOCV para n < 100)**:

| Modelo | Justificativa | CV R² (Dataset A) |
|---|---|---|
| Regressão Linear | Baseline parcimonioso | 0.209 |
| Ridge Regression | Reduz instabilidade por multicolinearidade | — |
| **Random Forest** | **Melhor desempenho — captura não-linearidades** | **0.287** |
| Gradient Boosting | Ensemble sequencial para padrões hierárquicos | 0.064 |

### Importância de Features (Random Forest)

```
avg_watch_time   ████████████████████████████  55.3%
avg_pct_watched  █████████████                 27.0%
duration         ████████                      17.6%
```

> O tempo médio assistido é o preditor mais relevante de engajamento — mais do que a duração do vídeo em si.

---

## 📊 Principais Resultados

- **Vídeos curtos (< 30s)** apresentam maior retenção média: **63.2%**
- **Vídeos de 30–60s** são os mais frequentes e equilibrados: **44.5%** de retenção
- **Duração ótima** identificada pelo Random Forest: **~53 segundos → 11.5% ER Likes**
- Correlação negativa entre duração e retenção (r = -0.41): vídeos mais longos retêm menos
- Correlação positiva entre duração e engajamento por likes (r = 0.34): vídeos mais longos geram mais likes entre quem assiste
- Clustering K-Means (k=3) segmentou vídeos em: **Virais**, **Desempenho Médio** e **Baixo Alcance**

---

## 📁 Dashboards

| Dashboard | Conteúdo |
|---|---|
| `dashboard_1` | Análise do canal TikTok real (Zawacki) — correlações e distribuições |
| `dashboard_2` | Análise aprofundada — Zawacki com múltiplos cenários |
| `dashboard_3` | TikTok vs YouTube Shorts — comparativo de plataformas |
| `dashboard_4` | Modelos de ML — Real vs Previsto, RMSE, importância de features |

---

## 🛠️ Tecnologias e Ferramentas

| Categoria | Tecnologia |
|---|---|
| Linguagem | Python 3.10+ |
| Análise de Dados | Pandas, NumPy, SciPy |
| Machine Learning | Scikit-learn (RF, GB, Ridge, LinearRegression, KMeans) |
| Visualização | Matplotlib, Seaborn |
| Ambiente | Jupyter Notebook, VirtualBox |
| Dados | Kaggle, Figshare, API TikTok |
| Versionamento | Git, GitHub |

---

## 📚 Referências Principais

- ZAWACKI, E. *TikTok Channel Analytics Dataset*, Figshare, 2021–2022.
- CRESWELL, J. W. *Research Design*. 4. ed. Sage, 2014.
- GIL, A. C. *Métodos e Técnicas de Pesquisa Social*. 7. ed. Atlas, 2019.
- HAIR, J. et al. *Multivariate Data Analysis*. 7. ed. Pearson, 2010.
- BREIMAN, L. Random Forests. *Machine Learning*, v. 45, p. 5–32, 2001.
- FRIEDMAN, J. Greedy function approximation: a gradient boosting machine. *Annals of Statistics*, v. 29, n. 5, p. 1189–1232, 2001.

---

## 👤 Autor

**Vitor Hugo M. Silveira**
Bacharelando em Sistemas de Informação
TCC II — 2025/2026

---

## 📄 Licença

Este projeto é de natureza acadêmica. Os dados do dataset Zawacki são de uso público disponibilizados no Kaggle/Figshare. Os demais datasets públicos seguem suas respectivas licenças de origem.

---

*Elaborado com Python, Jupyter Notebook e dedicação. Orientado para contribuição acadêmica, científica e profissional na área de Ciência de Dados e Marketing Digital.*
