python_classprojects

A curated collection of beginner-to-intermediate Python projects demonstrating skills in machine learning, computer vision, data analysis, and core programming.

Overview

This repository showcases practical implementations of:

Text classification using ML models
Image processing with OpenCV
Data cleaning and visualization
Core Python logic building

Each project is designed to be simple, runnable, and easy to understand.

Projects
Spam Email Detection (Machine Learning)
File: spam_email_detection_usingML.py
Models: Naive Bayes, Support Vector Machine
Technique: TF-IDF vectorization
Dataset: spam.csv
Output: Confusion Matrix and F1 Score comparison

Key Learning: Text preprocessing and model evaluation

Object Detection GUI (Computer Vision)
File: simple_Interactive_Object_Detection_GUI.py
Built using OpenCV + Tkinter
Features:
Shape detection (circle, triangle, polygon, etc.)
Color detection (HSV-based)
Image scaling and rotation controls
Includes desktop app packaging support

Key Learning: Image processing + GUI development

Online Voting System (Core Python)
File: Online_voting_system.py
Features:
Vote casting via CLI
Input validation
Winner calculation

Key Learning: Dictionaries, loops, and control flow

Employee Data Analysis
File: Employee_management_system.py
Dataset: employees.csv
Features:
Handling missing values
Removing duplicates
Correlation analysis
Box plot and heatmap visualization

Key Learning: Data preprocessing and visualization

Project Structure
python_classprojects/
├── spam_email_detection_usingML.py
├── simple_Interactive_Object_Detection_GUI.py
├── Online_voting_system.py
├── Employee_management_system.py
├── spam.csv
├── employees.csv
├── app_icon.ico
├── requirements.txt
└── README.md
Getting Started
1. Clone the Repository
git clone <your-repo-link>
cd python_classprojects
2. Install Dependencies
pip install -r requirements.txt
3. Run Projects
python filename.py

Example:

python spam_email_detection_usingML.py
Packaging the GUI Application

To convert the Object Detection GUI into a standalone desktop app:

pip install pyinstaller
pyinstaller --onefile --windowed --icon=app_icon.ico simple_Interactive_Object_Detection_GUI.py

Executable will be generated inside the dist/ folder.

Highlights
Multiple domains in one repo (ML + CV + Data + Core Python)
Beginner-friendly and modular code
Practical implementations with real datasets
Ready for extension into advanced projects
Future Improvements
Add GUI for Voting System
Improve ML model accuracy with advanced techniques
Integrate database support
Add real-time object detection
Notes
Ensure spam.csv and employees.csv are present in the root directory
GUI project requires a system with display support
Designed for learning and academic use
