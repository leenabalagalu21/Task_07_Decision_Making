# Appendices Index

This index helps stakeholders and reviewers locate supporting materials that back the main report.  
All appendices are organized by theme and cross-referenced to files in this repository.

---

## A. Data Lineage & Provenance
- **File:** `docs/data_provenance_scope.docx`  
- Contents: Source of data (Syracuse Women’s Lacrosse 2025 CSVs), collection process, privacy considerations, lineage of transformations.

---

## B. Code & Reproducibility
- **Files:** `code/step3_visualizations.py`, `code/step5_uncertainty.py`, `code/step6_sanity.py`, `code/step8_robustness.py`  
- **Environment:** `environment.yml`  
- **Run logs:** `results/logs/*.txt`  
- Purpose: Scripts and reproducibility notes for statistical validation, uncertainty quantification, sanity checks, and robustness analysis.

---

## C. LLM Prompts & Outputs
- **Files:**  
  - `prompts/prompts.docx` – full set of raw prompts used in LLM runs.  
  - `prompts/Task_6_Interview_script.docx` – transcript of interview task.  
  - `prompts/annotated_llm_outputs.md` – raw → edited → rationale (what was changed and why).  
- Purpose: Transparency in where LLM assistance was used and how outputs were verified or adjusted.

---

## D. Statistical Outputs
- **Tables:** `results/tables/` (e.g., `step5_ppg_ci_table.csv`, `step6_missingness.csv`, `step8_rank_stability.csv`).  
- **Figures:** `results/figures/` (e.g., `step3_top_scorers.png`, `step3_win_loss_trend.png`, `step5_ward_ppg_bootstrap.png`).  
- Purpose: Quantitative evidence underpinning claims in the stakeholder report.

---

## E. Ethical / Legal Checks
- **File:** integrated into `docs/Stakeholder_Report.docx` (Ethical/Legal Concerns section).  
- Notes on subgroup bias, fairness checks, and privacy safeguards.

---

## F. Workflow & Process Documentation
- **File:** `docs/workflow_document.docx`  
- Purpose: Full narrative of research workflow, including rationale for each step, validation decisions, and checkpoints.

---

## G. Final Reports
- **Stakeholder Report:** `docs/Stakeholder_Report.docx`  
- **Quick Start Guide for Reviewers:** `submission/quick_start.md`  

---

### How to Use
1. Start with `docs/Stakeholder_Report.docx` for decision summary.  
2. Consult `workflow_document.docx` for process transparency.  
3. Dive into appendices above for supporting data, code, and LLM audit trail.
