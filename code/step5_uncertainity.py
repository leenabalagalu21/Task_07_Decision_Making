# step5_uncertainty.py
# Bootstrap CIs for key players' PPG + one histogram figure

import pandas as pd, numpy as np, random
import matplotlib.pyplot as plt
from pathlib import Path

PLAYERS_CSV = r"C:/Users/leena/Downloads/syracuse_lacrosse_2025_player_stats.csv"
OUTDIR = Path("results/step5"); OUTDIR.mkdir(parents=True, exist_ok=True)

np.random.seed(42); random.seed(42)

players = pd.read_csv(PLAYERS_CSV)
df = players.copy()

# standardize
rename_map = {'Games_Played':'Games','GP':'Games','PlayerName':'Player','player':'Player',
              'goal':'Goals','assists':'Assists','points':'Points'}
for k,v in rename_map.items():
    if k in df.columns and v not in df.columns: df = df.rename(columns={k:v})
for col in ['Player','Goals']:
    if col not in df.columns: raise ValueError(f"Missing column: {col}")
if 'Games' not in df.columns: raise ValueError("Need 'Games' in player CSV")
if 'Assists' not in df.columns:
    if 'Points' in df.columns:
        df['Assists'] = pd.to_numeric(df['Points'],errors='coerce')-pd.to_numeric(df['Goals'],errors='coerce')
    else:
        df['Assists']=0

for c in ['Goals','Assists','Games','Points']:
    if c in df.columns: df[c] = pd.to_numeric(df[c], errors='coerce')

# compute PPG
df['Points'] = df.get('Points', df['Goals'].fillna(0)+df['Assists'].fillna(0))
df['PPG'] = df['Points']/df['Games']

def bootstrap_ci(values, n_boot=10000, ci=95, seed=42):
    np.random.seed(seed)
    means = [np.mean(np.random.choice(values, size=len(values), replace=True)) for _ in range(n_boot)]
    lo, hi = np.percentile(means, [(100-ci)/2, 100-(100-ci)/2])
    return np.mean(means), float(lo), float(hi), np.array(means)

# pick featured players (Ward/Muchnick if present else top-2 PPG)
if {'Emma Ward','Emma Muchnick'}.issubset(set(df['Player'])):
    featured = df[df['Player'].isin(['Emma Ward','Emma Muchnick'])].copy()
else:
    featured = df.sort_values('PPG', ascending=False).head(2).copy()

rows=[]
hist_done=False
for _, r in featured.iterrows():
    ppg = (r['Goals']+r['Assists'])/r['Games']
    series = np.repeat(ppg, int(r['Games']) if pd.notna(r['Games']) else 1)
    mean_, lo, hi, boot = bootstrap_ci(series, 10000, 95, 42)
    rows.append({'Player': r['Player'], 'Mean_PPG': round(mean_,3), 'CI95_L': round(lo,3), 'CI95_U': round(hi,3)})

    # one example histogram
    if not hist_done:
        plt.figure()
        plt.hist(boot, bins=30, edgecolor='black')
        plt.axvline(lo, linestyle='--'); plt.axvline(hi, linestyle='--')
        plt.title(f"Bootstrap Distribution — {r['Player']} PPG")
        plt.xlabel("PPG"); plt.ylabel("Frequency")
        plt.tight_layout(); plt.savefig(OUTDIR/"fig_bootstrap_ppg_example.png", dpi=180); plt.close()
        hist_done=True

pd.DataFrame(rows).to_csv(OUTDIR/"ppg_ci_table.csv", index=False)
print("Step 5 complete →", OUTDIR.resolve())
