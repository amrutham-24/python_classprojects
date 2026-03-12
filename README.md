# python_classprojects
Packaging Instructions – Object Detection GUI

**Project File:** `simple_Interactive_Object_Detection_GUI.py`

## 1. Prepare the Application Icon

1. Generate or download an icon for the application.
2. Convert the image to **`.ico` format** (recommended size: 256×256).
3. Save the icon in the **same folder** as the Python file.
   Example:

   ```
   simple_Interactive_Object_Detection_GUI.py
   app_icon.ico
   ```

## 2. Install Packaging Tool

Install PyInstaller using pip:

```
pip install pyinstaller
```

## 3. Create the Desktop Application

Open terminal/command prompt in the project folder and run:

```
pyinstaller --onefile --windowed --icon=app_icon.ico simple_Interactive_Object_Detection_GUI.py
```

### Flags Used

* `--onefile` → Creates a single executable file
* `--windowed` → Prevents the terminal window from opening
* `--icon` → Sets the application icon

## 4. Locate the Executable

After packaging completes:

* Navigate to the **`dist`** folder created by PyInstaller.
* The executable file will be located there.

Example:

```
dist/
   simple_Interactive_Object_Detection_GUI.exe
```

## 5. Run the Application

Double-click the `.exe` file to launch the Object Detection GUI as a desktop application.









The Online Voting System is a simple Python program that allows users to vote for predefined candidates.
It demonstrates the use of lists, dictionaries, loops, and conditional statements.
***************
Features
-Displays a list of candidates
-Accepts votes from users
-Handles invalid inputs
-Counts votes for each candidate
-Announces the winner
-Voting stops when stop is entered
****************
*How to Run*
-USING NOTEPAD
Save the file as voting_system.py
Open Command Prompt
Go to the folder where the file is saved:
  cd path\to\folder
Run the program:
  python voting_system.py
-USING VSCODE
Open VS Code
Create voting_system.py
Paste the code and save
Open terminal and run:
  python voting_system.py
***********************

#Future Improvements
-Handle tie between candidates
-Add user authentication
-Add GUI interface(Eg. Tkinter,PyQt etc.)
-Store votes in a database




