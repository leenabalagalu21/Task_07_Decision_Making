# Task_07_Decision_Making

## 📌 Purpose
This repository contains the full workflow, code, documentation, and reports for **Task 7**, which required transforming an LLM-produced narrative into a **stakeholder-facing decision report** for Syracuse Women’s Lacrosse 2025. The focus was not only on performance insights but also on **ethics, reliability, transparency, and reproducibility**.

---

## 🏑 Stakeholder & Decision Context
- **Audience:** Syracuse Women’s Lacrosse coaching staff, athletic director, and performance analysts.  
- **Decision Need:** Identify actionable recommendations based on player stats, with explicit treatment of uncertainty and fairness.  
- **Risk Level:** Medium → Findings affect coaching strategy and player training focus, but do not involve high-stakes HR/legal actions.  

---

## 🔎 Data Provenance & Scope
- **Source:** Syracuse Women’s Lacrosse 2025 dataset (games & player stats).  
- **Collected by:** Athletic department staff.  
- **Privacy:** No personal identifiers beyond player names; compliant with FERPA.  
- **Limitations:** No demographic variables (so no subgroup fairness analysis); some missing values in shot/possession data.  

---

## 🛠️ Methods & Workflow
1. **Step 1–2:** Stakeholder context + provenance documentation.  
2. **Step 3:** Reproduced descriptive statistics & visualizations (top scorers, win/loss trends, goals vs. shots).  
3. **Step 4:** Captured LLM prompts, raw outputs, and edits (`appendices/annotated_llm_outputs.md`).  
4. **Step 5:** Quantified uncertainty using bootstrap confidence intervals.  
5. **Step 6:** Sanity checks — missingness, outliers, and effect size tests.  
6. **Step 7:** Bias & fairness review (not applicable due to dataset limits).  
7. **Step 8:** Robustness tests — top-N removal, normalization, seed variation.  
8. **Step 9:** Tiered recommendations (Operational, Investigatory, High-stakes).  

---

## 📊 Key Findings
- **Emma Muchnick** → Highest *total goals scored* (volume scorer).  
- **Emma Ward** → Highest *points per game efficiency* (PPG ~3.0–3.5).  
- Bootstrap CIs for Ward were stable across seeds: [2.9–3.5] and [3.1–3.8].  
- Win/loss trend revealed mid-season fatigue periods.  
- Robustness checks confirmed **recommendations hold under perturbations**.  

---

## Recommendations
- **Low-risk (Operational):** Continue leveraging Muchnick as the primary scorer.  
- **Medium-risk (Investigatory):** Monitor Ward’s efficiency and provide late-game endurance support.  
- **High-risk (Not applicable):** No personnel/legal interventions required.  

---

## Ethical & Legal Considerations
- All model-generated text is **labeled and annotated**.  
- Privacy maintained — no sensitive attributes.  
- Transparency ensured — all code, seeds, and outputs archived.  

---
## 🔄 Reproducibility
To reproduce this analysis:  
1. Clone the repo.
2. Run scripts in order:
- python code/step3_visualizations.py
- python code/step5_uncertainty.py
- python code/step6_sanity_checks.py
- python code/step8_robustness.py
3. Compare outputs in results/ with the report.

---

