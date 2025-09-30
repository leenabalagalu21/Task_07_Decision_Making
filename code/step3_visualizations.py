# step3_visualizations.py
# Visuals for Syracuse Women's Lacrosse 2025 (Top scorers, W/L trend, Goals vs Shots, PPG>=5)

import pandas as pd, numpy as np, random
import matplotlib.pyplot as plt
from pathlib import Path

# ---------- config ----------
GAMES_CSV   = r"C:/Users/leena/Downloads/syracuse_lacrosse_2025_cleaned.csv"
PLAYERS_CSV = r"C:/Users/leena/Downloads/syracuse_lacrosse_2025_player_stats.csv"
OUTDIR = Path("results/step3"); OUTDIR.mkdir(parents=True, exist_ok=True)

# reproducibility
np.random.seed(42); random.seed(42)

# ---------- load ----------
games = pd.read_csv(GAMES_CSV)
players = pd.read_csv(PLAYERS_CSV)

# ---------- standardize players df ----------
df = players.copy()
rename_map = {
    'Games_Played':'Games','GP':'Games','PlayerName':'Player','player':'Player',
    'goal':'Goals','assists':'Assists','shots':'Shots','points':'Points'
}
for k,v in rename_map.items():
    if k in df.columns and v not in df.columns: df = df.rename(columns={k:v})

# required
for col in ['Player','Goals']:
    if col not in df.columns: raise ValueError(f"Missing column: {col}")
if 'Games' not in df.columns: raise ValueError("Need 'Games' or 'Games_Played' in players CSV")

# derive
if 'Assists' not in df.columns:
    if 'Points' in df.columns: df['Assists'] = pd.to_numeric(df['Points'],errors='coerce')-pd.to_numeric(df['Goals'],errors='coerce')
    else: df['Assists'] = 0
for c in ['Goals','Assists','Games','Shots','Points']:
    if c in df.columns: df[c] = pd.to_numeric(df[c], errors='coerce')

# ---------- 1) Top scorers ----------
top = df.sort_values('Goals', ascending=False).head(10)
plt.figure(figsize=(10,6))
plt.bar(top['Player'], top['Goals'])
plt.xticks(rotation=45, ha='right'); plt.ylabel("Goals"); plt.xlabel("Player")
plt.title("Top 10 Goal Scorers - Syracuse WLax 2025")
plt.tight_layout(); plt.savefig(OUTDIR/"fig_top_scorers.png", dpi=180); plt.close()

# ---------- 2) Win/Loss trend (robust date parsing) ----------
# Clean + parse Date robustly, then sort by date for a sensible plot
if 'Date' in games.columns:
    # (Optional) strip stray text and keep only the date-like token
    # Example patterns: 03/07/2025, 2025-03-07, 3-7-25
    games['Date'] = games['Date'].astype(str).str.extract(
        r'(\d{1,4}[/-]\d{1,2}[/-]\d{1,4})'
    ).squeeze()

    def parse_date_safe(s: pd.Series) -> pd.Series:
        # Try common formats first; fall back to dateutil
        fmts = ['%m/%d/%Y', '%m/%d/%y', '%Y-%m-%d', '%m-%d-%Y', '%m-%d-%y']
        out = pd.to_datetime(s, format=fmts[0], errors='coerce')
        for f in fmts[1:]:
            mask = out.isna()
            if mask.any():
                out.loc[mask] = pd.to_datetime(s.loc[mask], format=f, errors='coerce')
        # final fallback (handles oddballs)
        mask = out.isna()
        if mask.any():
            out.loc[mask] = pd.to_datetime(s.loc[mask], errors='coerce')
        return out

    games['Date_parsed'] = parse_date_safe(games['Date'])
    # If everything failed, fall back to index order
    if games['Date_parsed'].isna().all():
        games = games.reset_index().rename(columns={'index': 'GameIdx'})
        games['Date_parsed'] = range(1, len(games) + 1)
else:
    games = games.reset_index().rename(columns={'index': 'GameIdx'})
    games['Date_parsed'] = range(1, len(games) + 1)

# Map result to 1/0
if 'Result' not in games.columns:
    raise ValueError("Games CSV needs a 'Result' column with W/L values.")
games['Game_Result'] = games['Result'].astype(str).str.upper().str.startswith('W').astype(int)

# Sort by date for a clean left→right season timeline
games = games.sort_values('Date_parsed')

plt.figure(figsize=(12, 5))
plt.plot(games['Date_parsed'], games['Game_Result'], marker='o', linestyle='-')
plt.yticks([0, 1], ["Loss", "Win"])
plt.title("Win/Loss Trend Over Season")
plt.xlabel("Game (date order)")
plt.ylabel("Result")
plt.grid(True)
plt.tight_layout()
plt.savefig(OUTDIR / "fig_win_loss_trend.png", dpi=180)
plt.close()

# ---------- 3) Goals vs Shots (if available) ----------
if 'Shots' in df.columns:
    plt.figure(figsize=(8,6))
    plt.scatter(df['Shots'], df['Goals'], alpha=0.75)
    for _,r in df.iterrows():
        plt.annotate(str(r['Player']), (r.get('Shots',0), r.get('Goals',0)), fontsize=7, alpha=0.7)
    plt.xlabel("Shots"); plt.ylabel("Goals"); plt.grid(True)
    plt.title("Goals vs Shots — Player Performance")
    plt.tight_layout(); plt.savefig(OUTDIR/"fig_goals_vs_shots.png", dpi=180); plt.close()

# ---------- 4) PPG (>=5 GP) ----------
df['Points'] = df.get('Points', df['Goals'].fillna(0)+df['Assists'].fillna(0))
df['PPG'] = df['Points']/df['Games']
eligible = df[df['Games']>=5].sort_values('PPG', ascending=False)

plt.figure(figsize=(10,6))
plt.bar(eligible['Player'], eligible['PPG'])
plt.xticks(rotation=45, ha='right'); plt.ylabel("Points per Game"); plt.xlabel("Player")
plt.title("PPG (≥5 GP) — Syracuse WLax 2025")
plt.tight_layout(); plt.savefig(OUTDIR/"fig_ppg_ge5.png", dpi=180); plt.close()

print("Step 3 complete →", OUTDIR.resolve())
