import re
import tkinter as tk
from tkinter import messagebox, ttk

from app_config import LIGHT_BLUE, PAGE_BACKGROUND, TEXT


class RecordManagerMixin:
    """Search, display, modify, and delete Firestore case records."""

    def build_record_manager(self, parent):
        self.records_panel = tk.Frame(parent, bg=PAGE_BACKGROUND)
        self.section(self.records_panel, "Find Existing Records")
        ttk.Label(self.records_panel, text=("Enter a record ID, student name, student number, or faculty name to retrieve matching records.")).pack(anchor="w", pady=(0, 6))
        search_bar = tk.Frame(self.records_panel, bg=PAGE_BACKGROUND)
        search_bar.pack(fill="x", pady=(0, 8))
        self.search_entry = tk.Entry(search_bar, relief="solid", bd=1, bg=LIGHT_BLUE, fg=TEXT, font=("Arial", 10))
        self.search_entry.pack(side="left", fill="x", expand=True, ipady=4)
        self.search_entry.bind("<Return>", lambda _event: self.search_records())
        ttk.Button(search_bar, text="Search", command=self.search_records).pack(side="left", padx=(8, 0))
        ttk.Button(search_bar, text="Show All", command=self.show_all_records).pack(side="left", padx=(8, 0))

        columns = ("record_id", "student_name", "student_number", "faculty_name")
        self.records_tree = ttk.Treeview(self.records_panel, columns=columns, show="headings", height=6)
        headings = {"record_id": "Record ID", "student_name": "Student Name", "student_number": "Student Number", "faculty_name": "Faculty Name"}
        widths = {"record_id": 220, "student_name": 210, "student_number": 150, "faculty_name": 210}
        for column in columns:
            self.records_tree.heading(column, text=headings[column])
            self.records_tree.column(column, width=widths[column], anchor="w")
        self.records_tree.pack(fill="x", pady=(0, 8))
        self.records_tree.bind("<Double-1>", lambda _event: self.modify_selected_record())
        record_actions = tk.Frame(self.records_panel, bg=PAGE_BACKGROUND)
        record_actions.pack(fill="x", pady=(0, 8))
        ttk.Button(record_actions, text="Modify Selected", command=self.modify_selected_record).pack(side="left", padx=(0, 8))
        ttk.Button(record_actions, text="Delete Selected", command=self.delete_selected_record).pack(side="left")

    def toggle_record_manager(self):
        if self.records_panel.winfo_ismapped():
            self.records_panel.pack_forget()
            self.records_button.configure(text="Find / Manage Records")
        else:
            self.records_panel.pack(fill="x", pady=(10, 0))
            self.records_button.configure(text="Hide Records")

    def _read_records(self):
        records = []
        for snapshot in self.db.collection("cases").stream():
            record = snapshot.to_dict() or {}
            case_id = record.get("case_id")
            student_number = record.get("student_number") or record.get("form_data", {}).get("Student Number (Step 2)", "")
            if not case_id or not re.fullmatch(r"TRU-\d{4}(?:-\d+)?", str(case_id)):
                case_id = self._create_unique_case_id(student_number)
                self.db.collection("cases").document(snapshot.id).update({"case_id": case_id})
            records.append({"record_id": case_id, "document_id": snapshot.id, "student_name": record.get("student_name", ""), "student_number": record.get("student_number", ""), "faculty_name": record.get("faculty_name", ""), "form_data": record.get("form_data", {})})
        return records

    def _create_unique_case_id(self, student_number):
        """Create an ID from the last four digits, such as TRU-2418."""
        digits = re.sub(r"\D", "", str(student_number))
        base_id = f"TRU-{digits[-4:].zfill(4) if digits else '0000'}"
        existing_ids = set()
        for snapshot in self.db.collection("cases").stream():
            case_id = str((snapshot.to_dict() or {}).get("case_id", ""))
            existing_ids.add(case_id)
        if base_id not in existing_ids:
            return base_id
        suffix = 2
        while f"{base_id}-{suffix}" in existing_ids:
            suffix += 1
        return f"{base_id}-{suffix}"

    def _display_records(self, records):
        for item in self.records_tree.get_children():
            self.records_tree.delete(item)
        self.record_ids.clear()
        self.record_display_ids.clear()
        for record in records:
            item_id = self.records_tree.insert("", "end", values=(record["record_id"], record["student_name"], record["student_number"], record["faculty_name"]))
            self.record_ids[item_id] = record["document_id"]
            self.record_display_ids[item_id] = record["record_id"]
        self.status_var.set(f"Found {len(records)} record(s). Select one to modify or delete.")

    def search_records(self):
        query = self.search_entry.get().strip().casefold()
        if not query:
            messagebox.showwarning("Search value required", "Enter a record ID, student name, student number, or faculty name.")
            return
        try:
            records = self._read_records()
            matches = [record for record in records if any(query in str(record[field]).casefold() for field in ("record_id", "document_id", "student_name", "student_number", "faculty_name"))]
            self._display_records(matches)
        except Exception as error:
            self.status_var.set("Search failed.")
            messagebox.showerror("Firebase search failed", str(error))

    def show_all_records(self):
        try:
            self._display_records(self._read_records())
        except Exception as error:
            self.status_var.set("Record retrieval failed.")
            messagebox.showerror("Firebase retrieval failed", str(error))

    def _selected_record_id(self):
        selected = self.records_tree.selection()
        if not selected:
            messagebox.showwarning("No record selected", "Select a record first.")
            return None
        return self.record_ids.get(selected[0])

    def modify_selected_record(self):
        record_id = self._selected_record_id()
        if not record_id:
            return
        try:
            snapshot = self.db.collection("cases").document(record_id).get()
            if not snapshot.exists:
                messagebox.showerror("Record not found", "The selected record no longer exists.")
                return
            record = snapshot.to_dict() or {}
            self.current_record_id = record_id
            self.current_case_id = record.get("case_id", record_id)
            self.populate_form(record.get("form_data", {}))
            self.status_var.set(f"Editing record: {self.current_case_id}. Save Form to update it.")
        except Exception as error:
            messagebox.showerror("Firebase retrieval failed", str(error))

    def delete_selected_record(self):
        record_id = self._selected_record_id()
        if not record_id:
            return
        selected_item = self.records_tree.selection()[0]
        display_id = self.record_display_ids.get(selected_item, record_id)
        if not messagebox.askyesno("Delete record", f"Delete record {display_id}? This cannot be undone."):
            return
        try:
            self.db.collection("cases").document(record_id).delete()
            if self.current_record_id == record_id:
                self.current_record_id = None
                self.current_case_id = None
                self.clear_form()
            self.show_all_records()
            self.status_var.set(f"Deleted record: {display_id}")
        except Exception as error:
            self.status_var.set("Delete failed.")
            messagebox.showerror("Firebase delete failed", str(error))
