# Academic Integrity Case Manager

This project is a Python desktop application for completing an Academic Integrity Case Report Form. It uses Tkinter to display a PDF-style form and Firebase Cloud Firestore to save the completed information online.

The form supports the five stages of the case process:

1. Faculty member information and alleged violation details.
2. Student review, comments, and signature.
3. Faculty follow-up when the form is returned or not returned within seven days.
4. Department Chair review.
5. Dean review.

The application also includes separate Faculty Member Comments and Student Comments areas.

## Project files

| File | Purpose |
|---|---|
| `academic_integrity_app.py` | Main Tkinter application and Firestore save logic. |
| `requirements.txt` | Python package dependency list. |
| `firebase-service-account.json` | Private Firebase Admin SDK credential. Never publish or share this file. |
| `Campus_Case_Report_Form_May_202047195.pdf` | Original PDF reference for the form design and wording. |
| `.gitignore` | Prevents credentials, databases, and Python cache files from being committed. |

The old `academic_integrity.db` SQLite database was removed because the application no longer uses SQLite. The generated `__pycache__` folder was also removed because Python recreates it automatically when needed.

## Requirements

- Python 3.9 or newer
- Tkinter, normally included with Python on Windows
- A Firebase project with Cloud Firestore enabled
- The Firebase Admin SDK private-key JSON file

## Firebase setup

1. Open the [Firebase Console](https://console.firebase.google.com/).
2. Create or select a Firebase project.
3. Open **Build → Firestore Database → Create database**.
4. Open **Project settings → Service accounts**.
5. Select **Firebase Admin SDK**.
6. Click **Generate new private key**.
7. Save the downloaded JSON file as `firebase-service-account.json` beside `academic_integrity_app.py`.

The current project already contains this file. Do not upload it to GitHub, email it, or include it in a public ZIP file. Anyone who obtains this credential can access the Firebase project with server-side permissions.

## Installation and running

Open PowerShell in the project folder and run:

```powershell
pip install -r requirements.txt
python academic_integrity_app.py
```

If the credential file is stored in another location, set its path first:

```powershell
$env:FIREBASE_CREDENTIALS = "C:\path\to\firebase-service-account.json"
python academic_integrity_app.py
```

In VS Code, use **Run Python File**. Do not select one line and use **Run Code**, because that can create a `tempCodeRunnerFile.py` containing only the selected line.

## How the application works

1. The program starts a Tkinter window.
2. It connects to Firebase using the service-account JSON file.
3. It creates a scrollable PDF-style form.
4. The user enters the case information.
5. The user clicks **Save Form**.
6. The app validates that a student name was entered.
7. The app creates an automatic Firestore document ID.
8. The complete form is saved in the Firebase `cases` collection.

Each Firestore document has this general structure:

```text
cases/{automatic-document-id}
  student_name
  student_number
  faculty_name
  form_data
    all fields from the form
  created_at
```

The `form_data` object contains every field, including text fields, checkboxes, Yes/No choices, signatures, and comments.

## Detailed line-by-line code explanation

Blank lines are only used to make the source easier to read. The following guide explains every functional line and line group in `academic_integrity_app.py`.

### Lines 1–13: imports, paths, and colors

- **Line 1** imports `os`, which lets the program read the optional `FIREBASE_CREDENTIALS` environment variable.
- **Line 2** imports Tkinter as `tk`, the standard Python GUI toolkit.
- **Line 3** imports `Path`, which provides safe Windows and cross-platform file paths.
- **Line 4** imports Tkinter message boxes and themed widgets.
- **Line 6** finds the folder containing the Python file.
- **Line 7** creates the default path for `firebase-service-account.json`.
- **Lines 9–13** define reusable colors for the university header, input fields, page background, normal text, and muted text.

### Lines 15–56: form field definitions

- **Line 15** documents that the dictionary keys become the names used in Firestore.
- **Line 16** starts `FIELD_GROUPS`, the master definition of the form fields.
- **Lines 17–30** define Page 1 fields for faculty information, student information, course details, violation description, sanction recommendation, confirmations, and faculty signature details.
- **Lines 31–42** define Page 2 fields for student review, student comments, student signature, student number, and the faculty follow-up step.
- **Lines 43–53** define Page 3 fields for Department Chair and Dean decisions, explanations, signatures, names, and dates.
- **Line 54** defines the Page 4 faculty comments field.
- **Line 55** defines the Page 5 student comments field.
- **Line 56** closes the field dictionary.
- The field type values have these meanings: `entry` creates a one-line input, `large` creates a multi-line text box, `check` creates a checkbox, `choice` creates Yes/No radio buttons, and `text` is treated as a normal one-line input.

### Lines 59–81: Firebase connection

- **Line 59** starts the `connect_firebase` function.
- **Line 60** documents that the function returns a Firestore client and the Firestore module.
- **Line 61** begins error handling for Firebase imports.
- **Lines 62–63** import the Firebase Admin SDK only when the application starts.
- **Lines 64–68** show a friendly installation message when `firebase-admin` is missing.
- **Lines 70–72** choose the credential path. The environment variable takes priority; otherwise the default file beside the app is used.
- **Line 73** checks whether the credential file exists.
- **Lines 74–78** raise a clear error if the credential file cannot be found.
- **Line 79** checks whether Firebase was already initialized.
- **Line 80** initializes Firebase with the private service-account certificate.
- **Line 81** creates and returns the Firestore client and module.

### Lines 84–94: application initialization

- **Line 84** starts the `CaseManager` class.
- **Line 85** describes the class as the PDF-style form controller.
- **Line 87** starts the class constructor.
- **Line 88** stores the Tkinter root window.
- **Line 89** sets the window title.
- **Line 90** sets the starting window size.
- **Line 91** sets the smallest allowed window size.
- **Line 92** connects to Firebase and stores the Firestore client and module.
- **Line 93** creates a dictionary that will store every input widget.
- **Line 94** calls the interface-building function.

### Lines 96–131: main scrollable interface

- **Lines 96–97** start and describe `build_interface`.
- **Line 98** sets the main window background to white.
- **Line 99** creates a Tkinter theme style object.
- **Lines 100–108** define fonts, colors, and sizes for normal labels, muted labels, section headings, subsection headings, and the Save button.
- **Line 110** creates the outer container.
- **Line 111** expands the outer container to fill the window.
- **Line 112** creates the canvas that holds the long form.
- **Line 113** creates the vertical scrollbar and connects it to the canvas.
- **Line 114** creates the form content frame with horizontal padding.
- **Lines 115–116** update the canvas scroll region whenever the form changes size.
- **Line 117** places the content frame inside the canvas.
- **Lines 118–119** make the content frame match the available canvas width.
- **Line 120** connects the canvas scrolling position to the scrollbar.
- **Lines 121–122** display the canvas and scrollbar.
- **Lines 124–131** build the header, introduction, five form sections, and bottom action bar in order.

### Lines 133–149: university header

- **Line 133** starts `build_header`.
- **Lines 134–136** create a fixed-height dark-blue header and prevent it from shrinking.
- **Lines 137–138** create and position the left header area.
- **Lines 139–143** display the university name, address, location, and email address.
- **Lines 144–145** create and position the right header area.
- **Lines 146–149** display the policy title and “Case Report Form” title.

### Lines 151–174: title and instructions

- **Line 151** starts `build_intro`.
- **Lines 152–153** display the main form title.
- **Line 154** displays the blue horizontal divider.
- **Lines 155–158** display the italic form description.
- **Line 159** displays the “Faculty Member instructions” heading.
- **Lines 160–166** store the five instructions in a list.
- **Line 167** loops through the instructions and generates numbers 1 through 5.
- **Line 168** creates one row for each instruction.
- **Line 169** makes the row fill the available width.
- **Lines 170–171** display the instruction number.
- **Lines 172–174** display the instruction sentence on the same row as its number.

### Lines 176–220: reusable layout helpers

- **Lines 176–177** define the section-heading helper.
- **Lines 179–180** define the smaller subsection-heading helper.
- **Lines 182–183** define the reusable form-field helper and its layout parameters.
- **Line 184** creates the field container.
- **Lines 185–189** choose grid layout for two-column rows or packed layout for full-width fields.
- **Lines 190–191** display the field label.
- **Lines 192–195** create a multi-line text area for `large` fields.
- **Lines 196–199** create a Boolean checkbox for `check` fields.
- **Lines 200–207** create Yes/No radio buttons for `choice` fields.
- **Lines 208–211** create a light-blue one-line entry field for normal fields.
- **Line 212** stores the widget and its type in `self.widgets`.
- **Line 213** returns the field frame.
- **Lines 215–220** create a two-column container and set the relative column widths.

### Lines 222–247: Step One

- **Line 222** starts the faculty section builder.
- **Line 223** displays the Step One heading.
- **Line 224** creates the two-column layout.
- **Lines 225–231** define the paired faculty, student, course, department, term, and assignment fields.
- **Lines 232–235** create each two-column row.
- **Line 236** creates the alleged-violation text area.
- **Line 237** displays the Page 5 reminder.
- **Line 238** creates the sanction recommendation text area.
- **Lines 239–240** display the checkbox instruction.
- **Lines 241–242** create the support-person and written-submission checkboxes.
- **Lines 243–246** create signature, name, and date fields.
- **Line 247** displays the Page 1 marker.

### Lines 249–272: Steps Two and Three

- **Lines 249–250** create the student section heading.
- **Lines 251–254** display the student policy explanation.
- **Lines 255–257** create student name and email fields.
- **Line 258** creates the Yes/No review field.
- **Line 259** creates the student comments area.
- **Lines 260–262** create student signature and student number fields.
- **Line 263** displays the Step Three heading.
- **Lines 264–265** display the seven-day instruction.
- **Lines 266–267** create the returned-form choice and proceeding checkbox.
- **Lines 268–271** create the Step Three faculty signature, name, and date fields.
- **Line 272** displays the Page 2 marker.

### Lines 274–296: Steps Four and Five

- **Line 274** starts the Department Chair and Dean builder.
- **Lines 275–278** display the Department Chair heading and instructions.
- **Lines 279–284** create the Department Chair decision, explanation, signature, name, and date fields.
- **Lines 286–289** display the Dean heading and instructions.
- **Lines 290–295** create the Dean decision, explanation, signature, name, and date fields.
- **Line 296** displays the Page 3 marker.

### Lines 298–311: comments and page markers

- **Lines 298–301** create the Faculty Member Comments section and Page 4 marker.
- **Lines 303–306** create the Student Comments section and Page 5 marker.
- **Line 308** starts the page-marker helper.
- **Lines 309–311** display the `F S D` footer text and page number.

### Lines 313–319: buttons and status

- **Line 313** starts the action-bar builder.
- **Lines 314–315** create the bottom action bar.
- **Line 316** creates the New / Clear button.
- **Line 317** creates the Save Form button.
- **Line 318** creates the status message variable.
- **Line 319** displays the current status message.

### Lines 321–347: reading and clearing form data

- **Line 321** starts `collect_form`.
- **Line 322** creates an empty dictionary.
- **Line 323** loops over every registered widget.
- **Lines 324–331** read text areas, checkboxes, radio buttons, and one-line entries using the correct Tkinter method.
- **Line 332** stores each value under its field name.
- **Line 333** returns all form data.
- **Line 335** starts `populate_form`.
- **Line 336** loops through every widget.
- **Line 337** gets the saved value or an empty value.
- **Lines 338–347** put values back into text areas, checkboxes, radio buttons, and entries.

### Lines 349–372: clearing and saving to Firestore

- **Lines 349–351** clear every input and update the status message.
- **Line 353** starts `save_record`.
- **Line 354** collects all entered values.
- **Lines 355–357** require either the faculty-side or student-side student name.
- **Line 358** begins Firebase save error handling.
- **Line 359** creates a new document reference in the `cases` collection.
- **Lines 360–366** save the student name, student number, faculty name, complete form data, and server timestamp.
- **Lines 367–370** display a useful error if Firestore saving fails.
- **Line 371** updates the status with the Firestore document ID.
- **Line 372** displays a success message.

### Lines 375–386: program entry point

- **Line 375** starts the `main` function.
- **Line 376** begins startup error handling.
- **Line 377** creates the Tkinter root window.
- **Line 378** creates the `CaseManager` application.
- **Lines 379–381** show a setup error and stop if Firebase or the GUI cannot start.
- **Line 382** starts Tkinter’s event loop so the window responds to user actions.
- **Lines 385–386** run `main()` only when this file is executed directly, not when it is imported by another Python file.

## Important security note

`firebase-service-account.json` is a private server credential. Keep it out of public repositories and public downloads. The `.gitignore` file excludes it, but still verify the file is not uploaded before sharing the project.
