# Main script to run Watson agents for medical diagnostics with metadata extraction and report generation
import os
import json
from dotenv import dotenv_values
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, EntitiesOptions, KeywordsOptions
from concurrent.futures import ThreadPoolExecutor, as_completed
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet

# === Function to summarize keywords ===
def summarize_keywords(response_json):
    keywords = response_json.get("keywords", [])
    top_keywords = sorted(
        [kw for kw in keywords if kw["text"].lower() not in ["keywords", "analysis of the medical report"]],
        key=lambda k: k["relevance"],
        reverse=True
    )[:5]
    summary = "Based on the analysis of the medical report, the following clinical indicators are most relevant:\n\n"
    for kw in top_keywords:
        summary += f"- {kw['text']} (relevance score: {round(kw['relevance'], 2)})\n"
    summary += "\nThese keywords suggest a combination of physiological and psychological components that should be reviewed by a multidisciplinary medical team."
    return summary

# === Function to extract patient info from the report ===
def extract_patient_info(text):
    info = {}
    lines = text.splitlines()
    for line in lines:
        if ":" in line:
            key, value = line.split(":", 1)
            info[key.strip()] = value.strip()
        if line.strip().lower() == "chief complaint:":
            break
    return info

# === Load IBM Watson credentials from .env ===
env_path = r"your env file path"
creds = dotenv_values(env_path)
os.environ["IBM_WATSON_API_KEY"] = creds.get("IBM_WATSON_API_KEY", "")
os.environ["IBM_WATSON_URL"] = creds.get("IBM_WATSON_URL", "")
IBM_API_KEY = os.environ["IBM_WATSON_API_KEY"]
IBM_URL = os.environ["IBM_WATSON_URL"]
if not IBM_API_KEY or not IBM_URL:
    raise ValueError("❌ API key or URL is missing. Check your .env file and variable names.")

# === Watson Agent Classes ===
class WatsonBaseAgent:
    def __init__(self, medical_report):
        authenticator = IAMAuthenticator(IBM_API_KEY)
        self.nlu = NaturalLanguageUnderstandingV1(
            version='2022-04-07',
            authenticator=authenticator
        )
        self.nlu.set_service_url(IBM_URL)
        self.medical_report = medical_report

    def run(self):
        response = self.nlu.analyze(
            text=self.medical_report,
            features=Features(
                entities=EntitiesOptions(),
                keywords=KeywordsOptions()
            )
        ).get_result()
        return summarize_keywords(response)

class Cardiologist(WatsonBaseAgent): pass
class Psychologist(WatsonBaseAgent): pass
class Pulmonologist(WatsonBaseAgent): pass
class WatsonAgent(WatsonBaseAgent): pass

class MultidisciplinaryTeam(WatsonBaseAgent):
    def __init__(self, cardiologist_report, psychologist_report, pulmonologist_report):
        combined_report = (
            f"Cardiologist Summary:\n{cardiologist_report}\n\n"
            f"Psychologist Summary:\n{psychologist_report}\n\n"
            f"Pulmonologist Summary:\n{pulmonologist_report}\n"
        )
        super().__init__(combined_report)

# === Read the medical report ===
medical_report_path = r"your report file path"
with open(medical_report_path, "r", encoding="utf-8") as file:
    medical_report = file.read()

patient_info = extract_patient_info(medical_report)

# === Run Watson agents concurrently ===
agents = {
    "Cardiologist": Cardiologist(medical_report),
    "Psychologist": Psychologist(medical_report),
    "Pulmonologist": Pulmonologist(medical_report),
    "Watson": WatsonAgent(medical_report),
}
def get_response(agent_name, agent):
    response = agent.run()
    return agent_name, response

responses = {}
with ThreadPoolExecutor() as executor:
    futures = {executor.submit(get_response, name, agent): name for name, agent in agents.items()}
    for future in as_completed(futures):
        agent_name, response = future.result()
        responses[agent_name] = response

# === Final Diagnosis ===
team_agent = MultidisciplinaryTeam(
    cardiologist_report=responses["Cardiologist"],
    psychologist_report=responses["Psychologist"],
    pulmonologist_report=responses["Pulmonologist"]
)
final_diagnosis = team_agent.run()
patient_header = (
    f"Patient Name: {patient_info.get('Name', 'N/A')}\n"
    f"Patient ID: {patient_info.get('Patient ID', 'N/A')}\n"
    f"Age: {patient_info.get('Age', 'N/A')}\n"
    f"Gender: {patient_info.get('Gender', 'N/A')}\n"
    f"Date of Report: {patient_info.get('Date of Report', 'N/A')}\n"
)
final_diagnosis_text = f"{patient_header}\n\n### Final Diagnosis Report\n\n{final_diagnosis}"

# === Save TXT file ===
txt_output_path = "results/final_diagnosis_summary.txt"
os.makedirs(os.path.dirname(txt_output_path), exist_ok=True)
with open(txt_output_path, "w", encoding="utf-8") as txt_file:
    txt_file.write(final_diagnosis_text)

# === Save PDF file ===
pdf_output_path = "results/final_diagnosis_summary.pdf"
doc = SimpleDocTemplate(pdf_output_path, pagesize=A4)
styles = getSampleStyleSheet()
story = [Paragraph("Final Diagnosis Report", styles["Title"]), Spacer(1, 12)]

for field in ["Name", "Patient ID", "Age", "Gender", "Date of Report"]:
    story.append(Paragraph(f"{field}: {patient_info.get(field, 'N/A')}", styles["Normal"]))
story.append(Spacer(1, 12))

for line in final_diagnosis.strip().split('\n'):
    if line.strip():
        story.append(Paragraph(line.strip(), styles["Normal"]))
        story.append(Spacer(1, 6))

doc.build(story)
print(f"✅ Diagnosis saved to {pdf_output_path}")
print("\n📋 Diagnosis Summary:\n")
print(final_diagnosis_text)

