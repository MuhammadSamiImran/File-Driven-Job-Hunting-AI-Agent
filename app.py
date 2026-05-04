import os
import csv
from datetime import datetime

# --- CONFIGURATION ---
JOB_DIR = "input_jobs"
RESUME_DIR = "input_resumes"
KB_DIR = "input_kb"
OUTPUT_DIR = "outputs"
TRACKER_DIR = "tracker"

# Agent's knowledge base of skills to look for
KEYWORDS = [
    "python", "machine learning", "data preprocessing", "github", "git",
    "api", "prompt engineering", "sql", "communication", "problem solving",
    "oop", "database", "jupyter", "pandas", "numpy", "deep learning",
    "html", "css", "flask", "streamlit", "scikit-learn", "pytorch", "tensorflow"
]

def ensure_folders():
    """Step 1: Prepare the Environment"""
    for folder in [JOB_DIR, RESUME_DIR, KB_DIR, OUTPUT_DIR, TRACKER_DIR]:
        os.makedirs(folder, exist_ok=True)

def read_text_files(folder):
    """Step 2: Perception - The agent reads its environment"""
    combined_text = ""
    file_count = 0
    if not os.path.exists(folder):
        return "", 0
    
    for filename in os.listdir(folder):
        if filename.lower().endswith(".txt"):
            path = os.path.join(folder, filename)
            with open(path, "r", encoding="utf-8") as file:
                combined_text += f"\n\n--- FILE: {filename} ---\n"
                combined_text += file.read()
                file_count += 1
    return combined_text, file_count

def save_text(path, content):
    """Step 3: Action - The agent writes its findings"""
    with open(path, "w", encoding="utf-8") as file:
        file.write(content)

def extract_keywords(text):
    """Reasoning: Identifying key AI/Dev terms in text"""
    text_lower = text.lower()
    found = [kw for kw in KEYWORDS if kw in text_lower]
    return list(set(found)) # Remove duplicates

def compare_skills(job_skills, resume_skills):
    """Reasoning: Calculating the match score"""
    matched = [skill for skill in job_skills if skill in resume_skills]
    missing = [skill for skill in job_skills if skill not in resume_skills]
    score = 0 if not job_skills else round((len(matched) / len(job_skills)) * 100, 2)
    return matched, missing, score

# --- GENERATION FUNCTIONS (The 'Actions') ---

def generate_job_analysis(job_skills):
    report = "Job Analysis Report\n===================\n\n"
    report += "Primary Skills/Keywords found in your Job Posters:\n"
    for skill in job_skills:
        report += f" [x] {skill}\n"
    return report

def generate_skill_gap_report(score, matched, missing):
    report = "Skill Gap Report\n================\n\n"
    report += f"Current Match Score: {score}%\n\n"
    report += "Matched Skills:\n" + "".join([f"- {s}\n" for s in matched])
    report += "\nMissing Skills (Gaps):\n" + "".join([f"- {s}\n" for s in missing])
    return report

def generate_resume_suggestions(job_skills, missing):
    output = "Tailored Resume Suggestions\n===========================\n\n"
    output += "1. Skill Integration:\n"
    for skill in job_skills:
        output += f"- Highlight your experience with '{skill}' more prominently.\n"
    
    if missing:
        output += "\n2. Critical Gaps to Address:\n"
        for skill in missing:
            output += f"- URGENT: Mention projects or certifications related to {skill}.\n"
    return output

def generate_interview_questions(job_skills, kb_text):
    questions = "Interview Preparation Questions\n==============================\n\n"
    questions += "Technical Drills (from JDs):\n"
    for skill in job_skills:
        questions += f"- Can you explain a complex project where you used {skill}?\n"
    
    questions += "\nContextual Questions (from your KB notes):\n"
    kb_lines = [line.strip("- ") for line in kb_text.splitlines() if len(line.strip()) > 10]
    for line in kb_lines[:5]: # Use top 5 relevant notes
        questions += f"- Based on your notes: 'How would you apply {line[:50]}...' in this role?\n"
    return questions

def create_or_update_tracker():
    """Memory: Maintaining the application history"""
    path = os.path.join(TRACKER_DIR, "applications.csv")
    if not os.path.exists(path):
        with open(path, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["application_id", "company", "role", "source", "status", "applied_date", "interview_date", "follow_up_date", "next_action", "notes"])
            # Default starter row
            writer.writerow(["APP-001", "Example AI Corp", "AI Intern", "LinkedIn", "Not Applied", "2026-05-04", "", "2026-05-10", "Apply after tailoring", "Initial target"])
    return path

def generate_reminders():
    """Reasoning: Checking state and notifying user"""
    tracker_path = os.path.join(TRACKER_DIR, "applications.csv")
    reminders = "System Reminders & Alerts\n=========================\n\n"
    
    if not os.path.exists(tracker_path): return "No applications tracked yet."

    with open(tracker_path, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            status = row['status'].lower()
            if status == "interview scheduled":
                reminders += f"URGENT: Interview for {row['role']} at {row['company']} on {row['interview_date']}!\n"
            elif status == "not applied":
                reminders += f"ACTION: You haven't applied to {row['company']} yet. Finish tailoring!\n"
    return reminders

def run_agent():
    """The Agent Loop: Orchestrating the workflow"""
    print("--- CareerPrep Agent Starting ---")
    ensure_folders()

    # 1. PERCEIVE
    job_text, jc = read_text_files(JOB_DIR)
    resume_text, rc = read_text_files(RESUME_DIR)
    kb_text, kc = read_text_files(KB_DIR)

    if jc == 0 or rc == 0:
        print("Error: Please add .txt files to input_jobs and input_resumes.")
        return

    # 2. REASON
    js = extract_keywords(job_text)
    rs = extract_keywords(resume_text)
    matched, missing, score = compare_skills(js, rs)

    # 3. ACT (Generate Content)
    analysis = generate_job_analysis(js)
    gap = generate_skill_gap_report(score, matched, missing)
    suggs = generate_resume_suggestions(js, missing)
    iq = generate_interview_questions(js, kb_text)
    
    create_or_update_tracker()
    reminders = generate_reminders()

    # 4. MEMORY (Save results)
    save_text(os.path.join(OUTPUT_DIR, "job_analysis_report.txt"), analysis)
    save_text(os.path.join(OUTPUT_DIR, "skill_gap_report.txt"), gap)
    save_text(os.path.join(OUTPUT_DIR, "tailored_resume_suggestions.txt"), suggs)
    save_text(os.path.join(OUTPUT_DIR, "interview_questions.txt"), iq)
    save_text(os.path.join(TRACKER_DIR, "reminders.txt"), reminders)

    # Final summary report
    full_report = f"FINAL AGENT REPORT - {datetime.now()}\n\n{analysis}\n{gap}\n{reminders}"
    save_text(os.path.join(OUTPUT_DIR, "final_agent_report.txt"), full_report)

    print(f"Success! Agent analyzed {jc} job(s). Match Score: {score}%. Check 'outputs/' folder.")

if __name__ == "__main__":
    run_agent()