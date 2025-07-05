📚 Python Backend Projects Collection
This repository contains multiple Python backend projects demonstrating different functionalities using Flask, machine learning, audio processing, GUI development, and database management.

📂 Project Files
1. whisper_try.py - 🎤 Voice-Based Interview Evaluation
Description:
A Flask-based backend that:

Generates interview questions and answers using the Mistral API.

Records audio answers from the microphone.

Transcribes the recorded audio using OpenAI's Whisper model.

Evaluates the correctness of the answer using the Mistral API.

How to Run:

bash
Copy
Edit
python whisper_try.py
Endpoints:

POST /generate_qa → Generate interview questions and answers based on candidate description.

GET /transcribe → Record and transcribe user’s spoken answer.

POST /evaluate_answer → Evaluate transcribed answer for correctness.

2. tools.py - 🛠️ Tool Shop Product Management (GUI)
# Product Manager App

A simple desktop application built with Python, SQLite, and TTKBootstrap that allows users to manage inventory in a tool shop. It supports product addition, viewing, billing, stock adjustment, and deletion.

## Features
- Add new products with name, category, price, and quantity
- View all products in a tabular view
- Generate bills by adding products to a cart and calculating total
- Adjust existing product stock
- Delete products by name

## Technologies Used
- Python 3.x
- Tkinter (GUI)
- ttkbootstrap (UI styling)
- SQLite (Database)

## Customization
- Change themes by replacing the theme in `ttk.Style("superhero")`
- Update background color from `self.configure(bg="#726f6f")`

3. traintest.py - 🤖 Scikit-Learn Practice
Description:
This file is used for practicing machine learning concepts using the scikit-learn library.

Helps in learning dataset handling, model training, prediction, and evaluation.

Suitable for practicing classification, vectorization, and model workflows.

How to Run:

bash
Copy
Edit
python traintest.py
⚙️ Requirements
Python 3.x

Flask

scikit-learn

Mistral API

whisper

sounddevice

python-dotenv

sqlite3

tkinter

🚀 Setup Instructions
Clone the repository:

bash
Copy
Edit
git clone https://github.com/yourusername/your-repo-name.git
cd your-repo-name
Install dependencies:

bash
Copy
Edit
pip install flask mistralai sounddevice whisper scikit-learn python-dotenv
Run the required .py file using:

bash
Copy
Edit
python filename.py
💡 Notes
Make sure to configure your Mistral API key in a .env file:

ini
Copy
Edit
MISTRAL_API_KEY=your_api_key_here
The tools.py file will automatically create a tools_shop.db SQLite database for storing product data.

👨‍💻 Author
Thariq Ahamed ks
Backend Developer | Python Enthusiast
