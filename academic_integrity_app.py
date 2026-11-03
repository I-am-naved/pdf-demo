import tkinter as tk
from tkinter import messagebox

from firebase_service import connect_firebase
from form_view import FormViewMixin
from record_manager import RecordManagerMixin


class CaseManager(RecordManagerMixin, FormViewMixin):
    """Main controller for the academic integrity case manager."""

    def __init__(self, root):
        self.root = root
        self.root.title("Academic Integrity Case Manager")
        self.root.geometry("1180x760")
        self.root.minsize(920, 600)
        self.db, self.firestore = connect_firebase()
        self.widgets = {}
        self.current_record_id = None
        self.current_case_id = None
        self.search_entry = None
        self.records_tree = None
        self.records_panel = None
        self.record_ids = {}
        self.record_display_ids = {}
        self.build_interface()

    def save_record(self):
        """Create a new Firestore record or update the selected record."""
        data = self.collect_form()
        if not data.get("Student Name") and not data.get("Student Name (typed or printed)"):
            messagebox.showwarning("Missing information", "Enter the student name before saving.")
            return
        student_number = data.get("Student Number") or data.get("Student Number (Step 2)")
        if not student_number or len("".join(character for character in str(student_number) if character.isdigit())) < 4:
            messagebox.showwarning("Missing student number", "Enter a student number containing at least four digits.")
            return
        try:
            record = {
                "student_name": data.get("Student Name") or data.get("Student Name (typed or printed)", ""),
                "student_number": student_number,
                "faculty_name": data.get("Faculty Member Name") or data.get("Name of Faculty Member", ""),
                "form_data": data,
            }
            if self.current_record_id:
                document = self.db.collection("cases").document(self.current_record_id)
                document.update(record)
                display_id = self.current_case_id or document.id
                self.status_var.set(f"Updated in Firebase: {display_id}")
                messagebox.showinfo("Updated", "The selected case was updated in Firebase.")
            else:
                case_id = self._create_unique_case_id(student_number)
                document = self.db.collection("cases").document(case_id)
                record["case_id"] = case_id
                record["created_at"] = self.firestore.SERVER_TIMESTAMP
                document.set(record)
                self.status_var.set(f"Saved to Firebase: {case_id}")
                messagebox.showinfo("Saved", "The case information was saved to Firebase.")
        except Exception as error:
            self.status_var.set("Save failed.")
            messagebox.showerror("Firebase save failed", str(error))


def main():
    try:
        root = tk.Tk()
        CaseManager(root)
    except Exception as error:
        messagebox.showerror("Application setup failed", str(error))
        return
    root.mainloop()


if __name__ == "__main__":
    main()
