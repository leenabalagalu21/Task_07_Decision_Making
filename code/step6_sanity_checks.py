# step6_sanity_checks.py
# Missingness, outliers (GPG), optional halftime accuracy if minute-level data exists

import pandas as pd, numpy as np, random
from scipy import stats
from pathlib import Path

PLAYERS_CSV = r"C:/Users/leena/Downloads/syracuse_lacrosse_2025_player_stats.csv"
OUTDIR = Path("results/step6"); OUTDIR.mkdir(parents=True, exist_ok=True)

np.random.seed(42); random.seed(42)

df = pd.read_csv(PLAYERS_CSV)

# standardize basics
rename_map = {'Games_Played':'Games','GP':'Games','PlayerName':'Player','player':'Player',
              'goal':'Goals','assists':'Assists','points':'Points'}
for k,v in rename_map.items():
    if k in df.columns and v not in df.columns: df = df.rename(columns={k:v})
if 'Assists' not in df.columns:
    if 'Points' in df.columns and 'Goals' in df.columns:
        df['Assists'] = pd.to_numeric(df['Points'],errors='coerce')-pd.to_numeric(df['Goals'],errors='coerce')
    else:
        df['Assists']=0
for c in ['Goals','Assists','Games','Points']:
    if c in df.columns: df[c] = pd.to_numeric(df[c], errors='coerce')

# 1) Missingness
miss = df.isna().sum().reset_index().rename(columns={'index':'column',0:'n_missing'})
miss.columns=['column','n_missing']
miss.to_csv(OUTDIR/"missingness.csv", index=False)

# 2) Outliers on Goals per Game
df['GPG'] = df['Goals'] / df['Games'].replace(0, np.nan)
q1,q3 = df['GPG'].quantile([0.25,0.75])
iqr = q3-q1; lower, upper = q1-1.5*iqr, q3+1.5*iqr
outliers = df[(df['GPG']<lower)|(df['GPG']>upper)]
outliers.to_csv(OUTDIR/"gpg_outliers.csv", index=False)

# 3) Optional halftime accuracy (requires Minute, ShotOnTarget, GameID)
if {'Minute','ShotOnTarget','GameID'}.issubset(df.columns):
    early = df[df['Minute']<=30].groupby('GameID')['ShotOnTarget'].mean()
    late  = df[df['Minute']>30].groupby('GameID')['ShotOnTarget'].mean()
    joined = pd.DataFrame({'early':early,'late':late}).dropna()
    if len(joined)>=3:
        t = stats.ttest_rel(joined['late'], joined['early'], nan_policy='omit')
        eff = (joined['late'].mean()-joined['early'].mean())/joined.stack().std(ddof=1)
        pd.DataFrame([{'ttest_p':t.pvalue, 'cohens_d':eff,
                       'mean_early':joined['early'].mean(),
                       'mean_late':joined['late'].mean()}]).to_csv(
            OUTDIR/"halftime_accuracy_test.csv", index=False)

print("Step 6 complete →", OUTDIR.resolve())
