from pathlib import Path


APP_DIR = Path(__file__).resolve().parent
DEFAULT_CREDENTIALS_FILE = APP_DIR / "firebase-service-account.json"

BLUE = "#073f70"
LIGHT_BLUE = "#d9e4fb"
PAGE_BACKGROUND = "#ffffff"
TEXT = "#111111"
MUTED = "#505050"

# The dictionary keys are also the field names stored in Firestore.
FIELD_GROUPS = {
    "Page 1 - Faculty": [
        ("OSA use only", "text"), ("Student Name", "entry"),
        ("Student Number", "entry"), ("Student Email", "entry"),
        ("Faculty Member Name", "entry"), ("Faculty Date (yyyy-mm-dd)", "entry"),
        ("Course Name and Number", "entry"), ("Assignment Number or Exam", "entry"),
        ("Department", "entry"), ("Term or Semester", "entry"),
        ("Description of alleged violation", "large"),
        ("Recommendations for sanction", "large"),
        ("Student advised about support person", "check"),
        ("Student advised about written submission", "check"),
        ("Signature of Faculty Member", "entry"),
        ("Name of Faculty Member", "entry"),
        ("Faculty Signature Date (yyyy-mm-dd)", "entry"),
    ],
    "Page 2 - Student": [
        ("Student Name (typed or printed)", "entry"), ("My campus email", "entry"),
        ("Student reviewed information (Yes/No)", "choice"),
        ("Student Further Comments", "large"),
        ("Student Signature", "entry"), ("Student Number (Step 2)", "entry"),
        ("Student signed and returned this form", "choice"),
        ("Form not returned within 7 days; faculty is proceeding", "check"),
        ("Step 3 - Faculty Member Signature", "entry"),
        ("Step 3 - Faculty Member Name", "entry"),
        ("Step 3 - Faculty Date (yyyy-mm-dd)", "entry"),
    ],
    "Page 3 - Chair and Dean": [
        ("Department Chair agrees (Yes/No)", "choice"),
        ("Department Chair explanation if No", "large"),
        ("Department Chair Signature", "entry"), ("Department Chair Name", "entry"),
        ("Department Chair Date (yyyy-mm-dd)", "entry"),
        ("Dean agrees (Yes/No)", "choice"), ("Dean explanation if No", "large"),
        ("Dean Signature", "entry"), ("Dean Name", "entry"),
        ("Dean Date (yyyy-mm-dd)", "entry"),
    ],
    "Page 4 - Faculty Comments": [("Faculty Member Comments", "large")],
    "Page 5 - Student Comments": [("Student Comments", "large")],
}
