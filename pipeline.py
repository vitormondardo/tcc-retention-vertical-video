# [Código] Leitura do Dataset A (Zawacki) com encoding='utf-8-sig'
# O encoding utf-8-sig remove o BOM e evita erros silenciosos em nomes de colunas.

DATASET_A_PATH = BASE_DIR / 'TikTokData_Video_Uploads.csv'
if not DATASET_A_PATH.exists():
    raise FileNotFoundError(f'Dataset A não encontrado em: {DATASET_A_PATH}')

df_zawacki_raw = pd.read_csv(DATASET_A_PATH, encoding='utf-8-sig')

print('Dataset A - Zawacki carregado.')
print(f'Shape bruto: {df_zawacki_raw.shape}')
display(df_zawacki_raw.head())

# [Código] Leitura do Dataset B (Público)
# O dicionário é carregado junto para documentar a origem das variáveis usadas.

DATASET_B_PATH = BASE_DIR / 'youtube_shorts_tiktok_trends_2025.csv'
DICTIONARY_CANDIDATES = [BASE_DIR / 'DATA_DICTIONARY__1_.csv', BASE_DIR / 'DATA_DICTIONARY (1).csv', BASE_DIR / 'DATA_DICTIONARY.csv']
DATA_DICTIONARY_PATH = next((p for p in DICTIONARY_CANDIDATES if p.exists()), None)

if not DATASET_B_PATH.exists():
    raise FileNotFoundError(f'Dataset B não encontrado em: {DATASET_B_PATH}')
if DATA_DICTIONARY_PATH is None:
    raise FileNotFoundError('Dicionário de dados não encontrado. Nomes esperados: DATA_DICTIONARY__1_.csv, DATA_DICTIONARY (1).csv ou DATA_DICTIONARY.csv')

df_public_raw = pd.read_csv(DATASET_B_PATH)
df_dictionary = pd.read_csv(DATA_DICTIONARY_PATH)

print('Dataset B - Público carregado.')
print(f'Shape bruto: {df_public_raw.shape}')
print(f'Dicionário oficial: {DATA_DICTIONARY_PATH.name}, shape: {df_dictionary.shape}')
display(df_public_raw.head())
display(df_dictionary.head(12))

# [Código] Verificação inicial (shape, head, tipos)
# Esta célula registra evidências de schema antes de qualquer transformação.

print('Dataset A - shape e tipos')
print(df_zawacki_raw.shape)
display(df_zawacki_raw.dtypes.to_frame('dtype').T)

display(df_zawacki_raw.head(3))

print()
print('Dataset B - shape e tipos')
print(df_public_raw.shape)
display(df_public_raw.dtypes.to_frame('dtype').T)

display(df_public_raw.head(3))

print()
print('Plataformas no Dataset B')
display(df_public_raw['platform'].value_counts(dropna=False).to_frame('n'))

print()
print('Colunas usadas no estudo segundo o DATA_DICTIONARY oficial')
cols_interesse = ['platform', 'duration_sec', 'views', 'likes', 'comments', 'shares', 'saves', 'engagement_rate', 'avg_watch_time_sec', 'completion_rate', 'category', 'creator_tier', 'traffic_source', 'publish_dayofweek']
display(df_dictionary[df_dictionary['column'].isin(cols_interesse)])

# Limpeza e Transformação (ETL)
# [Código] Limpeza Dataset A (renomeação, conversão numérica, dropna)
# A limpeza preserva apenas variáveis analíticas necessárias e evita coerções implícitas.

rename_zawacki = {
    'Duration (s)': 'duration',
    'Views': 'views',
    'Likes': 'likes',
    'Comments': 'comments',
    'Shares': 'shares',
    'Average Watch Time (s)': 'avg_watch_time',
    'Avg. % Watched': 'avg_pct_watched',
    '% Watched Full Video': 'pct_full_video',
    'ER Likes (%)': 'er_likes',
    'ER Comments (%)': 'er_comments',
    'ER Shares (%)': 'er_shares',
    'Video Topic': 'video_topic',
    'Date Published': 'date_published',
}

df_zawacki = df_zawacki_raw.copy()
df_zawacki.columns = [c.strip() for c in df_zawacki.columns]
df_zawacki = df_zawacki.rename(columns=rename_zawacki)

required_zawacki = ['duration', 'views', 'likes', 'comments', 'shares', 'avg_watch_time', 'avg_pct_watched', 'pct_full_video', 'er_likes']
missing_zawacki = [c for c in required_zawacki if c not in df_zawacki.columns]
if missing_zawacki:
    raise KeyError(f'Colunas ausentes no Dataset A após renomeação: {missing_zawacki}')

for col in required_zawacki:
    df_zawacki[col] = pd.to_numeric(df_zawacki[col], errors='coerce')

n_before = len(df_zawacki)
df_zawacki = df_zawacki.dropna(subset=required_zawacki).copy()
df_zawacki = df_zawacki[
    (df_zawacki['duration'] > 0) &
    (df_zawacki['views'] > 0) &
    (df_zawacki['avg_watch_time'] >= 0) &
    (df_zawacki['avg_pct_watched'].between(0, 200)) &
    (df_zawacki['er_likes'] >= 0)
].copy()

print('Dataset A limpo.')
print(f'Linhas antes: {n_before} | depois: {len(df_zawacki)} | removidas: {n_before - len(df_zawacki)}')
display(df_zawacki[required_zawacki].describe().T)


# [Código] Limpeza Dataset B (filtro de outliers, dropna, separação por plataforma)
# As definições de engagement_rate e completion_rate seguem o DATA_DICTIONARY oficial.

numeric_public = ['duration_sec', 'views', 'likes', 'comments', 'shares', 'saves', 'engagement_rate', 'avg_watch_time_sec', 'completion_rate']
required_public = ['platform'] + numeric_public

df_public = df_public_raw.copy()
df_public.columns = [c.strip() for c in df_public.columns]

missing_public = [c for c in required_public if c not in df_public.columns]
if missing_public:
    raise KeyError(f'Colunas ausentes no Dataset B: {missing_public}')

for col in numeric_public:
    df_public[col] = pd.to_numeric(df_public[col], errors='coerce')

df_public['platform'] = df_public['platform'].astype(str).str.strip()

# Recalcula métricas oficiais para auditar consistência e preencher eventuais nulos.
engagement_calc = (df_public['likes'] + df_public['comments'] + df_public['shares'] + df_public['saves']) / df_public['views'].replace(0, np.nan)
completion_calc = df_public['avg_watch_time_sec'] / df_public['duration_sec'].replace(0, np.nan)

diff_engagement = (df_public['engagement_rate'] - engagement_calc).abs().max(skipna=True)
diff_completion = (df_public['completion_rate'] - completion_calc).abs().max(skipna=True)

print(f'Diferença máxima engagement_rate oficial vs recalculado: {diff_engagement:.8f}')
print(f'Diferença máxima completion_rate oficial vs recalculado: {diff_completion:.8f}')

df_public['engagement_rate'] = df_public['engagement_rate'].fillna(engagement_calc)
df_public['completion_rate'] = df_public['completion_rate'].fillna(completion_calc)

n_before = len(df_public)
df_public_clean = df_public.dropna(subset=required_public).copy()
df_public_clean = df_public_clean[
    (df_public_clean['views'] > 0) &
    (df_public_clean['duration_sec'] > 0) &
    (df_public_clean['avg_watch_time_sec'] >= 0) &
    (df_public_clean['engagement_rate'].between(0, 1)) &
    (df_public_clean['completion_rate'].between(0, 1)) &
    (df_public_clean['platform'].isin(['TikTok', 'YouTube']))
].copy()

# Amostra fixa para acelerar ML, preservando o dataset completo para EDA.
df_public_ml = df_public_clean.sample(n=min(15000, len(df_public_clean)), random_state=RANDOM_STATE).copy()

df_tiktok_full = df_public_clean[df_public_clean['platform'] == 'TikTok'].copy()
df_youtube_full = df_public_clean[df_public_clean['platform'] == 'YouTube'].copy()
df_tiktok_ml = df_public_ml[df_public_ml['platform'] == 'TikTok'].copy()
df_youtube_ml = df_public_ml[df_public_ml['platform'] == 'YouTube'].copy()

print('Dataset B limpo.')
print(f'Linhas antes: {n_before} | depois: {len(df_public_clean)} | removidas: {n_before - len(df_public_clean)}')
print(f'Amostra para ML: {len(df_public_ml)} linhas')
print(f'TikTok full: {len(df_tiktok_full)} | YouTube full: {len(df_youtube_full)}')
print(f'TikTok ML: {len(df_tiktok_ml)} | YouTube ML: {len(df_youtube_ml)}')
display(df_public_clean.groupby('platform')[numeric_public].agg(['count', 'mean', 'median']).round(4))

#_______________________________________________________________________________________________________________
# Feature Engeneering (FE)

# Features derivadas Zawacki (engagement_total, retention_score, log_views, duration_category)
# As features derivadas tornam explícitas as dimensões de consumo: alcance, retenção e engajamento.

DURATION_BINS = [0, 15, 60, 300]
DURATION_LABELS = ['Muito curto (≤15s)', 'Curto-Médio (16-60s)', 'Longo (>60s)']

df_zawacki['engagement_total'] = df_zawacki[['likes', 'comments', 'shares']].sum(axis=1)
df_zawacki['retention_score'] = df_zawacki['avg_pct_watched'] / 100
# log1p reduz assimetria de views sem perder vídeos com baixa audiência.
df_zawacki['log_views'] = np.log1p(df_zawacki['views'])
df_zawacki['duration_category'] = pd.cut(
    df_zawacki['duration'],
    bins=DURATION_BINS,
    labels=DURATION_LABELS,
    include_lowest=True,
    right=True
)

print('Features derivadas do Dataset A criadas.')
print('Distribuição por categoria de duração:')
display(df_zawacki['duration_category'].value_counts(dropna=False).to_frame('n'))
display(df_zawacki[['duration', 'avg_watch_time', 'avg_pct_watched', 'retention_score', 'engagement_total', 'er_likes', 'log_views', 'duration_category']].head())

# Features derivadas Dataset Público (log_views, duration_category)
# A mesma categorização de duração é aplicada para permitir comparação entre datasets.

def adicionar_features_publicas(df):
    df = df.copy()
    df['engagement_total_calc'] = df[['likes', 'comments', 'shares', 'saves']].sum(axis=1)
    df['log_views'] = np.log1p(df['views'])
    df['duration_category'] = pd.cut(
        df['duration_sec'],
        bins=DURATION_BINS,
        labels=DURATION_LABELS,
        include_lowest=True,
        right=True
    )
    return df

df_public_clean = adicionar_features_publicas(df_public_clean)
df_public_ml = adicionar_features_publicas(df_public_ml)
df_tiktok_full = df_public_clean[df_public_clean['platform'] == 'TikTok'].copy()
df_youtube_full = df_public_clean[df_public_clean['platform'] == 'YouTube'].copy()
df_tiktok_ml = df_public_ml[df_public_ml['platform'] == 'TikTok'].copy()
df_youtube_ml = df_public_ml[df_public_ml['platform'] == 'YouTube'].copy()

print('Features derivadas do Dataset B criadas.')
print('Distribuição por plataforma e categoria de duração:')
display(pd.crosstab(df_public_clean['platform'], df_public_clean['duration_category'], margins=True))

fora_recorte = df_public_clean['duration_category'].isna().sum()
if fora_recorte > 0:
    print(f'Atenção: {fora_recorte} vídeos ficaram fora do recorte 0-300s e foram mantidos com categoria nula para auditoria.')


# Análise exploratória (EDA) - Estatísticas descritivas e insights iniciais
# Estatísticas descritivas Zawacki

cols_desc_z = ['duration', 'views', 'likes', 'comments', 'shares', 'avg_watch_time', 'avg_pct_watched', 'pct_full_video', 'er_likes', 'engagement_total']

desc_zawacki = df_zawacki[cols_desc_z].describe().T.round(4)
print('Estatísticas descritivas - Dataset A')
display(desc_zawacki)

retencao_por_categoria_z = (
    df_zawacki.groupby('duration_category', observed=False)
    .agg(
        n=('duration', 'size'),
        duracao_media=('duration', 'mean'),
        retencao_media_pct=('avg_pct_watched', 'mean'),
        watch_time_medio=('avg_watch_time', 'mean'),
        er_likes_medio=('er_likes', 'mean')
    )
    .round(4)
)

print('Insight 6 - Retenção média por categoria de duração no Dataset A')
display(retencao_por_categoria_z)

# Estatísticas descritivas TikTok vs YouTube no Dataset B

platform_stats = (
    df_public_clean.groupby('platform')
    .agg(
        n=('platform', 'size'),
        duracao_media=('duration_sec', 'mean'),
        duracao_mediana=('duration_sec', 'median'),
        views_mediana=('views', 'median'),
        engagement_rate_medio=('engagement_rate', 'mean'),
        completion_rate_medio=('completion_rate', 'mean'),
        watch_time_medio=('avg_watch_time_sec', 'mean')
    )
    .round(5)
)

print('Estatísticas descritivas por plataforma - Dataset B')
display(platform_stats)

engagement_por_plataforma = df_public_clean.groupby('platform')['engagement_rate'].mean().round(6)
completion_engagement_por_plataforma = df_public_clean.groupby('platform')[['completion_rate', 'engagement_rate']].mean().round(6)

print('Insight 7 - Engagement rate médio por plataforma')
for plataforma, valor in engagement_por_plataforma.items():
    print(f'{plataforma}: engagement_rate médio = {valor:.6f}')

print()
print('Insight 8 - Completion rate x Engagement rate por plataforma')
display(completion_engagement_por_plataforma)