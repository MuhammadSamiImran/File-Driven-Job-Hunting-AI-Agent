# Job-Hunting Agent

An automated AI agent help students to streamline the job application process.

## How it Works
Using the **GAME Framework**:
- **Goal**: Automate JD analysis and resume tailoring.
- **Actions**: Reads folder inputs, matches keywords, generates interview prep.
- **Memory**: Tracks applications via CSV and saves persistent reminders.
- **Environment**: File-based system.

## Setup
1. Place job descriptions in `input_jobs/`.
2. Place your resume (txt) in `input_resumes/`.
3. Place course notes/interview tips in `input_kb/`.
4. Run: `python app.py`.
5. Check `outputs/` for your tailored reports.
