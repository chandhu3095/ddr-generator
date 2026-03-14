# 🏗 DDR Generator — AI Diagnostic Report System

An AI-powered system that converts **site inspection reports and thermal imaging reports into a structured Detailed Diagnostic Report (DDR)**.

The application reads inspection observations, thermal data, and extracted thermal images, then uses a **Large Language Model (LLM)** to generate a **professional, client-ready diagnostic report**.

---

# 🚀 Features

* Upload **Inspection Report** (text / document)
* Upload **Thermal Report**
* Upload **Thermal PDF** to automatically extract thermal images
* AI merges inspection + thermal findings
* Generates a structured **Detailed Diagnostic Report (DDR)**
* Provides **area-wise observations, root cause analysis, severity assessment, and repair recommendations**
* Supports **thermal image embedding inside the report**
* Export report as **PDF or copy text**

---

# 🧠 AI Workflow

The system follows this pipeline:

Inspection Report
↓
Thermal Report
↓
Thermal Images PDF (optional)
↓
Image Extraction (PyMuPDF)
↓
Flask Backend API
↓
Groq LLM (LLaMA-3)
↓
Structured DDR Report

---

# 🖥 System Architecture

# Frontend (HTML / JS)↓Flask Backend API↓Groq LLM (LLaMA-3.1)↓DDR Report Generation

---

# 📂 Project Structure

```
DDR-Generator
│
├── static/
│   └── index.html          # Frontend UI
│
├── app.py                  # Flask backend server
├── requirements.txt        # Python dependencies
├── .gitignore
├── README.md
│
├── sample_insoection.md    # Sample inspection report
└── sample_thermal_report.md # Sample thermal report
```

---

# ⚙️ Installation

### 1️⃣ Clone the repository

```
git clone https://github.com/chandhu3095/ddr-generator.git
cd ddr-generator
```

---

### 2️⃣ Install dependencies

```
pip install -r requirements.txt
```

---

### 3️⃣ Add Groq API Key

Create a `.env` file in the project root:

```
GROQ_API_KEY=your_groq_api_key_here
```

Get your API key from:
https://console.groq.com

---

### 4️⃣ Run the server

```
python app.py
```

Server starts at:

```
http://localhost:5000
```

---

# 📊 DDR Report Structure

The AI generates a structured report containing:

1. Property Issue Summary
2. Area-wise Observations
3. Probable Root Cause
4. Severity Assessment
5. Recommended Actions
6. Additional Notes
7. Missing or Unclear Information

The report is designed to be **client-friendly and suitable for professional building diagnostics**.

---

# 🖼 Thermal Image Extraction

Thermal images are extracted from uploaded PDF files using **PyMuPDF**.

Extracted images are:

* converted to Base64
* sent to frontend
* embedded into DDR report sections

This allows visual support for thermal findings.

---

# 📌 Example Use Case

Property inspection identifies:

* wall dampness
* ceiling seepage
* tile joint gaps

Thermal imaging detects:

* temperature anomalies
* moisture zones

The AI combines both inputs to determine:

* root cause of leakage
* severity level
* recommended repair actions

---

# 🛠 Technologies Used

### Frontend

* HTML
* CSS
* JavaScript

### Backend

* Python
* Flask
* Flask-CORS

### AI

* Groq API
* LLaMA 3.1 Model

### Document Processing

* PyMuPDF (fitz)

---

# 🎥 Demo

The system allows users to:

1️⃣ Upload inspection report
2️⃣ Upload thermal report
3️⃣ Extract thermal images from PDF
4️⃣ Generate AI diagnostic report

---

# 📈 Future Improvements

* Automatic PDF text extraction
* Smart image-to-area matching
* Support for multiple property reports
* Export report as structured PDF document
* Integration with building inspection platforms

---

# 👨‍💻 Author

**Chandhu**

AI / Data Science Graduate
Passionate about building AI-powered automation tools.

GitHub:
https://github.com/chandhu3095

---

# 📜 License

This project is for educational and demonstration purposes.
