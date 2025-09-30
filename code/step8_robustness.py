# step8_robustness.py
# Robustness & Sensitivity: remove top-N, per-possession normalization, seed/CI-width

import pandas as pd, numpy as np, random
from scipy.stats import pearsonr, spearmanr
from pathlib import Path

PLAYERS_CSV = r"C:/Users/leena/Downloads/syracuse_lacrosse_2025_player_stats.csv"
OUTDIR = Path("results/step8"); OUTDIR.mkdir(parents=True, exist_ok=True)

np.random.seed(42); random.seed(42)

df = pd.read_csv(PLAYERS_CSV)

# -------------------------
# Standardize column names
# -------------------------
rename_map = {
    'Games_Played': 'Games', 'GP': 'Games',
    'PlayerName': 'Player', 'player': 'Player',
    'goal': 'Goals', 'assists': 'Assists',
    'shots': 'Shots', 'points': 'Points'
}
for k, v in rename_map.items():
    if k in df.columns and v not in df.columns:
        df = df.rename(columns={k: v})

# If Assists missing but Points exist: Assists = Points - Goals (best effort)
if 'Assists' not in df.columns:
    if {'Points', 'Goals'}.issubset(df.columns):
        df['Assists'] = pd.to_numeric(df['Points'], errors='coerce') - pd.to_numeric(df['Goals'], errors='coerce')
    else:
        df['Assists'] = 0

# Coerce types
for c in ['Goals', 'Assists', 'Games', 'Shots', 'Possessions', 'Points']:
    if c in df.columns:
        df[c] = pd.to_numeric(df[c], errors='coerce')

# Remove any accidental duplicate column labels
df = df.loc[:, ~df.columns.duplicated()].copy()

# -------------------------
# Helpers
# -------------------------
def leaders_table(d: pd.DataFrame) -> pd.DataFrame:
    t = d.copy()
    t['PPG'] = (t['Goals'] + t['Assists']) / t['Games']
    return t.sort_values('PPG', ascending=False)[['Player', 'PPG']]

def corr_shots_goals(d: pd.DataFrame):
    if 'Shots' not in d.columns:
        return None, None
    r, p = pearsonr(d['Shots'], d['Goals'])
    return float(r), float(p)

def remove_top_n(d: pd.DataFrame, n: int = 1) -> pd.DataFrame:
    key = 'Shots' if 'Shots' in d.columns else 'Goals'
    top = d.sort_values(key, ascending=False).head(n)['Player']
    return d[~d['Player'].isin(top)].copy()

def add_rates(d: pd.DataFrame) -> pd.DataFrame:
    t = d.copy()
    if 'Possessions' in t.columns:
        t['Goals_rate'] = t['Goals'] / t['Possessions']
        t['Assists_rate'] = t['Assists'] / t['Possessions']
    else:
        # fall back to per-game rates if we don't have possessions
        t['Goals_rate'] = t['Goals'] / t['Games']
        t['Assists_rate'] = t['Assists'] / t['Games']
    return t

# -------------------------
# Baseline
# -------------------------
leaders_table(df).to_csv(OUTDIR / "baseline_leaders.csv", index=False)
r0, p0 = corr_shots_goals(df)
pd.DataFrame([{'scenario': 'baseline', 'r': r0, 'p': p0}]).to_csv(OUTDIR / "corr_baseline.csv", index=False)

# -------------------------
# Remove top-1, top-2
# -------------------------
for n in [1, 2]:
    dfn = remove_top_n(df, n)
    rn, pn = corr_shots_goals(dfn)
    leaders_table(dfn).to_csv(OUTDIR / f"leaders_remove_top{n}.csv", index=False)
    pd.DataFrame([{'scenario': f'remove_top{n}', 'r': rn, 'p': pn}]).to_csv(OUTDIR / f"corr_remove_top{n}.csv", index=False)

# -------------------------
# Per-possession normalization & rank stability (SAFE VERSION)
# -------------------------
rated = add_rates(df)

# Baseline ranking (per-game)
rank_base_list = leaders_table(df)['Player'].tolist()

# Build a clean rate-based frame with ONLY rate columns (avoid duplicate labels)
if {'Goals_rate', 'Assists_rate'}.issubset(rated.columns):
    rate_df = rated[['Player', 'Games', 'Goals_rate', 'Assists_rate']].copy()
    rate_df = rate_df.rename(columns={'Goals_rate': 'Goals', 'Assists_rate': 'Assists'})
else:
    # Fallback to original per-game columns if possessions not available
    needed = {'Player', 'Games', 'Goals', 'Assists'}
    if not needed.issubset(df.columns):
        raise ValueError(f"Missing required columns for rate ranking: {needed - set(df.columns)}")
    rate_df = df[['Player', 'Games', 'Goals', 'Assists']].copy()

# Ensure no duplicate column labels remain
rate_df = rate_df.loc[:, ~rate_df.columns.duplicated()].reset_index(drop=True)

# Rate-based ranking
rank_rate_list = leaders_table(rate_df)['Player'].tolist()

# Spearman rank correlation between baseline and rate-based rankings
mapped = [rank_rate_list.index(p) for p in rank_base_list if p in rank_rate_list]
rho = spearmanr(range(len(mapped)), mapped).correlation if len(mapped) > 1 else np.nan
pd.DataFrame([{'metric': 'rank_spearman_rho', 'rho': rho}]).to_csv(OUTDIR / "rank_stability.csv", index=False)

# -------------------------
# Seed sensitivity for CI width (first leader)
# -------------------------
def ci_width_for_player(name: str, seed: int = 42, n_boot: int = 5000):
    if name not in df['Player'].values:
        return None
    w = df[df['Player'] == name].iloc[0]
    ppg = (w['Goals'] + w['Assists']) / w['Games']
    series = np.repeat(ppg, int(w['Games']) if pd.notna(w['Games']) else 1)
    np.random.seed(seed)
    means = [np.mean(np.random.choice(series, size=len(series), replace=True)) for _ in range(n_boot)]
    return float(np.percentile(means, 97.5) - np.percentile(means, 2.5))

lead_name = leaders_table(df).iloc[0]['Player']
rows = []
for seed in [11, 42, 20250929]:
    for n_boot in [2000, 10000]:
        rows.append({
            'player': lead_name,
            'seed': seed,
            'n_boot': n_boot,
            'ci_width': ci_width_for_player(lead_name, seed, n_boot)
        })
pd.DataFrame(rows).to_csv(OUTDIR / "ci_width_sensitivity.csv", index=False)

print("Step 8 complete →", OUTDIR.resolve())
