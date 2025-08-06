
# AI Agents for Medical Diagnostics  
A multidisciplinary AI assistant for analyzing patient case reports using IBM Watson NLU

---

## Overview

This project is a Python-based system designed to simulate the diagnostic approach of a **multidisciplinary medical team**. It uses **IBM Watson's Natural Language Understanding (NLU)** API to analyze structured patient case reports and extract the most relevant clinical indicators.

The system features virtual agents (Cardiologist, Psychologist, Pulmonologist, Watson Agent) that read and analyze reports in parallel. Their outputs are synthesized into a clear, human-readable **diagnosis summary**, which is exported in both `.txt` and `.pdf` formats.

---

## Features

- ✅ **Real IBM Watson API integration**  
- ✅ **Multithreaded analysis** by specialist agents  
- ✅ Extracts and filters top clinical keywords  
- ✅ Adds patient metadata (name, age, gender, date, etc.)  
- ✅ Exports formatted summary reports in both **text** and **PDF**  
- ✅ Fully customizable for other medical specializations

---

## AI Agents

| Agent         | Focus                                                                                   |
|---------------|------------------------------------------------------------------------------------------|
| **Cardiologist**  | Analyzes cardiovascular symptoms, e.g., chest pain, palpitations                     |
| **Psychologist**  | Detects stress/anxiety-driven conditions such as panic disorder                      |
| **Pulmonologist** | Identifies respiratory conditions like asthma, wheezing, breathlessness              |
| **Watson Agent**  | General keyword/phrase extraction using IBM Watson NLU                               |
| **Multidisciplinary Team** | Combines all agents’ results into a single final diagnosis                  |

---

## Repository Structure

```
.
├── Medical Reports/         # Sample structured case reports
├── Results/                 # Output files (PDFs and summaries)
├── ibm-credentials.env      # IBM Watson API credentials (not uploaded)
├── Main_With_Metadata.py    # Main script with agent logic and export
├── README.md                # Project documentation
```

---

##  Output Example

- `results/final_diagnosis_summary.txt`  
- `results/final_diagnosis_summary.pdf`

Includes:
- Patient Metadata (name, age, ID, date)  
- Top 5 clinical keywords (ranked by relevance)  
- A concise AI-generated summary

---

##  How to Run

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Add your IBM Watson credentials**  
   Create a file named `ibm-credentials.env` with:
   ```
   IBM_WATSON_API_KEY=your_api_key_here
   IBM_WATSON_URL=https://api.your-region.natural-language-understanding.watson.cloud.ibm.com/instances/your_instance_id
   ```

3. **Run the script**
   ```bash
   python Main_With_Metadata.py
   ```

---

## Notes on AI Capabilities

This project uses IBM Watson NLU, which specializes in extracting key phrases and entities from unstructured text. It does **not** diagnose conditions directly.

However, **larger AI models** such as:
- **GPT-4** (with medical prompting or fine-tuning)
- **MedPaLM 2** (by Google)
- **ClinicalBERT**, **BioGPT**, etc.

...can often generate **accurate diagnoses**, simulate clinical reasoning, and even suggest treatments when given the same report. These models may be integrated in future upgrades.

---

## Future Enhancements

- Add agents for other specialties (Neurology, Endocrinology, etc.)  
- Add diagnosis inference based on keywords  
- Web dashboard (Streamlit) for uploading and reviewing reports  
- RAG-based integration with LLMs for clinical explanations  
- Smart ICD-10 code prediction

---

## Dev Notes & Precautions
Before running the project, please make sure the following conditions are met to avoid common errors:

1.  Environment File (.env)
Ensure the .env file is named ibm-credentials.env.

It must be located in the root directory of the project.

Use this structure (no quotes around values!):
IBM_WATSON_API_KEY=your_api_key_here
IBM_WATSON_URL=https://your_instance_url_here


2. Medical Report File
Place your medical report (in .txt format) inside the Medical Reports/ folder.

The filename must match the one referenced in the script, or update the path in:

medical_report_path = "Medical Reports/your_report.txt"


3. Required Folders
Make sure there is a results/ folder to save output files.

If not, the script will auto-create it, but it's good practice to include it.

4. Install Dependencies
Use the following command to install required packages:

pip install -r requirements.txt

5. Avoid Common Errors

    
Issue	                                                 Solution
- .env not                                             - found Double-check path and file extension. Use .env, not .txt.
- API Key missing	                                     - Make sure values are set correctly inside .env.
- Encoding errors on Windows	                         - Ensure report files are saved in UTF-8 encoding.
- PDF not generating	                                  - Make sure reportlab is installed.
- Wrong paths	                                        - Use raw strings (r"...") for Windows paths in Python scripts.


## Acknowledgments

- [IBM Watson NLU](https://www.ibm.com/cloud/watson-natural-language-understanding)  
- Inspired by real-world diagnostic workflows in multidisciplinary hospitals

---
