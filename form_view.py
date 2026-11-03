import tkinter as tk
from tkinter import ttk

from app_config import BLUE, LIGHT_BLUE, MUTED, PAGE_BACKGROUND, TEXT


class FormViewMixin:
    """Build and manage the academic integrity report form."""

    def build_interface(self):
        self.root.configure(bg=PAGE_BACKGROUND)
        style = ttk.Style(self.root)
        style.configure("Form.TLabel", background=PAGE_BACKGROUND, foreground=TEXT, font=("Arial", 10))
        style.configure("Muted.TLabel", background=PAGE_BACKGROUND, foreground=MUTED, font=("Arial", 10))
        style.configure("Section.TLabel", background=PAGE_BACKGROUND, foreground=BLUE, font=("Arial", 15, "bold"))
        style.configure("Subsection.TLabel", background=PAGE_BACKGROUND, foreground=BLUE, font=("Arial", 12, "bold"))
        style.configure("Save.TButton", font=("Arial", 10, "bold"))

        outer = tk.Frame(self.root, bg=PAGE_BACKGROUND)
        outer.pack(fill="both", expand=True)
        canvas = tk.Canvas(outer, bg=PAGE_BACKGROUND, highlightthickness=0)
        scrollbar = ttk.Scrollbar(outer, orient="vertical", command=canvas.yview)
        content = tk.Frame(canvas, bg=PAGE_BACKGROUND, padx=70, pady=0)
        content.bind("<Configure>", lambda _event: canvas.configure(scrollregion=canvas.bbox("all")))
        window_id = canvas.create_window((0, 0), window=content, anchor="nw")
        canvas.bind("<Configure>", lambda event: canvas.itemconfigure(window_id, width=event.width))
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.build_header(content)
        self.build_intro(content)
        self.build_step_one(content)
        self.build_step_two(content)
        self.build_step_three(content)
        self.build_step_four(content)
        self.build_step_five(content)
        self.build_action_bar(content)
        self.build_record_manager(content)

    def build_header(self, parent):
        header = tk.Frame(parent, bg=BLUE, height=150)
        header.pack(fill="x")
        header.pack_propagate(False)
        left = tk.Frame(header, bg=BLUE)
        left.pack(side="left")
        tk.Label(left, text="Thompson Rivers University", bg=BLUE, fg="white", font=("Arial", 18, "bold"), anchor="w").pack(anchor="w")
        for line in ("123 Campus Way", "Kamloops, BC  A1A 1A1", "integrity@campus.edu"):
            tk.Label(left, text=line, bg=BLUE, fg="white", font=("Arial", 10), anchor="w").pack(anchor="w")
        right = tk.Frame(header, bg=BLUE)
        right.pack(side="right", pady=34)
        tk.Label(right, text="ACADEMIC INTEGRITY POLICY", bg=BLUE, fg="white", font=("Arial", 14, "bold")).pack(anchor="e")
        tk.Label(right, text="Case Report Form", bg=BLUE, fg="white", font=("Arial", 11, "bold")).pack(anchor="e", pady=(4, 0))

    def build_intro(self, parent):
        tk.Label(parent, text="Case Report Form: On Campus Course", bg=PAGE_BACKGROUND, fg=TEXT, font=("Arial", 22, "bold")).pack(pady=(15, 6))
        tk.Frame(parent, bg=BLUE, height=4).pack(fill="x", pady=(0, 10))
        tk.Label(parent, text=("This form can be completed as a printed copy, or electronically. Include only one student and one assignment or exam per form."), bg=PAGE_BACKGROUND, fg=TEXT, font=("Arial", 10, "italic"), wraplength=1000, justify="left").pack(anchor="w", pady=(0, 14))
        self.section(parent, "Faculty Member instructions")
        instructions = [
            "Fill out the fields below. Use multiple forms if more than one student is involved.",
            "Provide comments and evidence. Submissions without evidence will not be accepted.",
            "Sign the printed copy, or type your name in the signature row if submitting digitally.",
            "Save as studentlastname_coursenumber_month_year.pdf.",
            "Send the form and evidence to the student, or meet in person for the next step.",
        ]
        for number, text in enumerate(instructions, 1):
            row = tk.Frame(parent, bg=PAGE_BACKGROUND)
            row.pack(fill="x", pady=(0, 6))
            tk.Label(row, text=f"{number}.", bg=PAGE_BACKGROUND, fg=TEXT, font=("Arial", 10), width=3, anchor="w").pack(side="left")
            tk.Label(row, text=text, bg=PAGE_BACKGROUND, fg=TEXT, font=("Arial", 10), anchor="w", justify="left").pack(side="left", padx=(4, 0))

    def section(self, parent, text):
        ttk.Label(parent, text=text, style="Section.TLabel").pack(anchor="w", pady=(12, 8))

    def subsection(self, parent, text):
        ttk.Label(parent, text=text, style="Subsection.TLabel").pack(anchor="w", pady=(12, 6))

    def field(self, parent, name, kind="entry", column=0, row=0, colspan=1, grid_mode=False):
        frame = tk.Frame(parent, bg=PAGE_BACKGROUND)
        if grid_mode:
            frame.grid(row=row, column=column, columnspan=colspan, sticky="ew", padx=(0 if column == 0 else 18, 0), pady=(0, 8))
        else:
            frame.pack(fill="x", pady=(0, 8))
        tk.Label(frame, text=name, bg=PAGE_BACKGROUND, fg=TEXT, font=("Arial", 10), anchor="w").pack(anchor="w")
        if kind == "large":
            widget = tk.Text(frame, height=5, wrap="word", relief="solid", bd=1, bg=LIGHT_BLUE, fg=TEXT, font=("Arial", 10))
            widget.pack(fill="both", expand=True, pady=(3, 0))
        elif kind == "check":
            widget = tk.BooleanVar()
            ttk.Checkbutton(frame, text="Completed", variable=widget).pack(anchor="w", pady=4)
        elif kind == "choice":
            widget = tk.StringVar(value="")
            choices = tk.Frame(frame, bg=PAGE_BACKGROUND)
            choices.pack(anchor="w", pady=3)
            ttk.Radiobutton(choices, text="Yes", value="Yes", variable=widget).pack(side="left", padx=(0, 15))
            ttk.Radiobutton(choices, text="No", value="No", variable=widget).pack(side="left")
        else:
            widget = tk.Entry(frame, relief="solid", bd=1, bg=LIGHT_BLUE, fg=TEXT, font=("Arial", 10))
            widget.pack(fill="x", pady=(3, 0), ipady=4)
        self.widgets[name] = (widget, kind)
        return frame

    def two_column_frame(self, parent):
        frame = tk.Frame(parent, bg=PAGE_BACKGROUND)
        frame.pack(fill="x")
        frame.columnconfigure(0, weight=3)
        frame.columnconfigure(1, weight=2)
        return frame

    def build_step_one(self, parent):
        self.section(parent, "Step One — To be completed by Faculty Member")
        grid = self.two_column_frame(parent)
        rows = [
            (("Faculty Member Name", "entry"), ("Faculty Date (yyyy-mm-dd)", "entry")),
            (("Student Name", "entry"), ("Student Number", "entry")),
            (("Student Email", "entry"), ("Term or Semester", "entry")),
            (("Course Name and Number", "entry"), ("Assignment Number or Exam", "entry")),
            (("Department", "entry"), None),
        ]
        for row, (left, right) in enumerate(rows):
            self.field(grid, *left, column=0, row=row, grid_mode=True)
            if right:
                self.field(grid, *right, column=1, row=row, grid_mode=True)
        self.field(parent, "Description of alleged violation", "large")
        ttk.Label(parent, text="(Use Page 5 if you need more room.)", style="Muted.TLabel").pack(anchor="w")
        self.field(parent, "Recommendations for sanction", "large")
        ttk.Label(parent, text="When contacting the student, ensure they are advised of the following (check when completed):", style="Form.TLabel", wraplength=1000).pack(anchor="w", pady=(2, 6))
        self.field(parent, "Student advised about support person", "check")
        self.field(parent, "Student advised about written submission", "check")
        grid = self.two_column_frame(parent)
        self.field(grid, "Signature of Faculty Member", "entry", column=0, row=0, grid_mode=True)
        self.field(grid, "Name of Faculty Member", "entry", column=1, row=0, grid_mode=True)
        self.field(parent, "Faculty Signature Date (yyyy-mm-dd)", "entry")
        self.page_marker(parent, "PAGE 1 of 5")

    def build_step_two(self, parent):
        self.section(parent, "Step Two — To be completed by Student within 7 days")
        ttk.Label(parent, text=("I have been made aware of the Academic Integrity Policy, as well as the alleged violation. I understand I may make a written submission and that a confidential record of this matter will be held by Student Affairs."), style="Form.TLabel", wraplength=1000, justify="left").pack(anchor="w", pady=(0, 8))
        grid = self.two_column_frame(parent)
        self.field(grid, "Student Name (typed or printed)", "entry", column=0, row=0, grid_mode=True)
        self.field(grid, "My campus email", "entry", column=1, row=0, grid_mode=True)
        self.field(parent, "Student reviewed information (Yes/No)", "choice")
        self.field(parent, "Student Further Comments", "large")
        grid = self.two_column_frame(parent)
        self.field(grid, "Student Signature", "entry", column=0, row=0, grid_mode=True)
        self.field(grid, "Student Number (Step 2)", "entry", column=1, row=0, grid_mode=True)
        self.subsection(parent, "Step Three — To be completed by Faculty Member")
        ttk.Label(parent, text="If the student returned a signed form, continue. If not returned within 7 days, proceed anyway.", style="Form.TLabel", wraplength=1000).pack(anchor="w", pady=(0, 6))
        self.field(parent, "Student signed and returned this form", "choice")
        self.field(parent, "Form not returned within 7 days; faculty is proceeding", "check")
        grid = self.two_column_frame(parent)
        self.field(grid, "Step 3 - Faculty Member Signature", "entry", column=0, row=0, grid_mode=True)
        self.field(grid, "Step 3 - Faculty Member Name", "entry", column=1, row=0, grid_mode=True)
        self.field(parent, "Step 3 - Faculty Date (yyyy-mm-dd)", "entry")
        self.page_marker(parent, "PAGE 2 of 5")

    def build_step_three(self, parent):
        self.section(parent, "Step Four — To be completed by the Department Chair")
        ttk.Label(parent, text=("All alleged breaches shall be reviewed by the Department Chair. Confirm signatures, ensure evidence is attached, then forward to the Dean within 7 days."), style="Form.TLabel", wraplength=1000, justify="left").pack(anchor="w", pady=(0, 8))
        self.field(parent, "Department Chair agrees (Yes/No)", "choice")
        self.field(parent, "Department Chair explanation if No", "large")
        grid = self.two_column_frame(parent)
        self.field(grid, "Department Chair Signature", "entry", column=0, row=0, grid_mode=True)
        self.field(grid, "Department Chair Name", "entry", column=1, row=0, grid_mode=True)
        self.field(parent, "Department Chair Date (yyyy-mm-dd)", "entry")
        self.section(parent, "Step Five — To be completed by the Dean")
        ttk.Label(parent, text=("Cases that reach the Academic Integrity Committee must be forwarded from the Dean (or designate). Confirm all signatures and attached evidence, then submit one PDF."), style="Form.TLabel", wraplength=1000, justify="left").pack(anchor="w", pady=(0, 8))
        self.field(parent, "Dean agrees (Yes/No)", "choice")
        self.field(parent, "Dean explanation if No", "large")
        grid = self.two_column_frame(parent)
        self.field(grid, "Dean Signature", "entry", column=0, row=0, grid_mode=True)
        self.field(grid, "Dean Name", "entry", column=1, row=0, grid_mode=True)
        self.field(parent, "Dean Date (yyyy-mm-dd)", "entry")
        self.page_marker(parent, "PAGE 3 of 5")

    def build_step_four(self, parent):
        self.section(parent, "Faculty Member Comments")
        self.field(parent, "Faculty Member Comments", "large")
        self.page_marker(parent, "PAGE 4 of 5")

    def build_step_five(self, parent):
        self.section(parent, "Student Comments")
        self.field(parent, "Student Comments", "large")
        self.page_marker(parent, "PAGE 5 of 5")

    def page_marker(self, parent, text):
        tk.Label(parent, text=f"F  S  D                                      {text}", bg=PAGE_BACKGROUND, fg=MUTED, font=("Arial", 9, "bold")).pack(anchor="e", pady=(6, 10))

    def build_action_bar(self, parent):
        bar = tk.Frame(parent, bg=PAGE_BACKGROUND, pady=12)
        bar.pack(fill="x")
        ttk.Button(bar, text="New / Clear", command=self.clear_form).pack(side="left", padx=(0, 8))
        ttk.Button(bar, text="Save Form", command=self.save_record, style="Save.TButton").pack(side="left")
        self.records_button = ttk.Button(bar, text="Find / Manage Records", command=self.toggle_record_manager)
        self.records_button.pack(side="left", padx=(8, 0))
        self.status_var = tk.StringVar(value="Ready.")
        ttk.Label(bar, textvariable=self.status_var, style="Muted.TLabel").pack(side="right")

    def collect_form(self):
        data = {}
        for field, (widget, kind) in self.widgets.items():
            if kind == "large":
                value = widget.get("1.0", "end-1c").strip()
            elif kind == "check":
                value = bool(widget.get())
            elif kind == "choice":
                value = widget.get()
            else:
                value = widget.get().strip()
            data[field] = value
        return data

    def populate_form(self, data):
        for field, (widget, kind) in self.widgets.items():
            value = data.get(field, "")
            if kind == "large":
                widget.delete("1.0", "end")
                widget.insert("1.0", value or "")
            elif kind == "check":
                widget.set(bool(value))
            elif kind == "choice":
                widget.set(value or "")
            else:
                widget.delete(0, "end")
                widget.insert(0, value or "")

    def clear_form(self):
        self.current_record_id = None
        self.current_case_id = None
        self.populate_form({})
        self.status_var.set("New record. Complete the form and save.")
