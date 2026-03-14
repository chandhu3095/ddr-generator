from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from groq import Groq
import os
import base64
import fitz  # PyMuPDF

app = Flask(__name__, static_folder='static')
CORS(app)

def extract_images_from_pdf(pdf_bytes):
    """Extract all images from a PDF and return as base64 list."""
    images = []
    try:
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        for page_num in range(len(doc)):
            page = doc[page_num]
            image_list = page.get_images(full=True)
            for img_index, img in enumerate(image_list):
                xref = img[0]
                base_image = doc.extract_image(xref)
                img_bytes = base_image["image"]
                img_ext = base_image["ext"]
                img_b64 = base64.b64encode(img_bytes).decode("utf-8")
                images.append({
                    "data": img_b64,
                    "ext": img_ext,
                    "page": page_num + 1,
                    "index": img_index + 1
                })
        doc.close()
    except Exception as e:
        print(f"Image extraction error: {e}")
    return images

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/extract-images', methods=['POST'])
def extract_images():
    """Extract images from uploaded thermal PDF."""
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    file = request.files['file']
    if not file.filename.endswith('.pdf'):
        return jsonify({'error': 'Please upload a PDF file'}), 400
    try:
        pdf_bytes = file.read()
        images = extract_images_from_pdf(pdf_bytes)
        return jsonify({'images': images, 'count': len(images)})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    inspection = data.get('inspection', '')
    thermal = data.get('thermal', '')
    client = data.get('client', 'Not Specified')
    address = data.get('address', 'Not Specified')
    date = data.get('date', '')
    ref = data.get('ref', 'DDR-001')
    images = data.get('images', [])  # base64 images from thermal PDF

    if not inspection and not thermal:
        return jsonify({'error': 'Please provide at least one document.'}), 400

    groq_key = os.environ.get("GROQ_API_KEY", "")
    if not groq_key:
        return jsonify({'error': 'GROQ_API_KEY not set in .env file.'}), 500

    prompt = f"""You are an expert waterproofing and structural diagnostics engineer. Read the provided inspection and thermal reports and generate a professional Detailed Diagnostic Report (DDR).

PROPERTY DETAILS:
- Client: {client}
- Address: {address}
- Date: {date}
- Reference: {ref}

INSPECTION REPORT:
---
{inspection or 'Not provided.'}
---

THERMAL REPORT:
---
{thermal or 'Not provided.'}
---

{"Thermal images have been extracted from the PDF and will be displayed inline in the report." if images else "No thermal images provided."}

Generate a complete DDR with EXACTLY these 7 sections. Use clear, client-friendly language. Do NOT invent facts. Write "Not Available" for missing info. Flag conflicts between documents.

For Section 2 (Area-wise Observations), after each area's findings, add a placeholder tag like:
[THERMAL_IMAGE:Hall] or [THERMAL_IMAGE:Bedroom] or [THERMAL_IMAGE:Kitchen] etc.
These tags will be replaced with actual thermal images in the final report.

## 1. PROPERTY ISSUE SUMMARY
Executive summary (3-5 sentences): overall condition, key problems, urgency level.

## 2. AREA-WISE OBSERVATIONS
For each area, combine visual + thermal findings:
### [Area Name]
- Visual findings
- Thermal findings (temperature differentials)
- Combined interpretation
[THERMAL_IMAGE:AreaName]

## 3. PROBABLE ROOT CAUSE
Root causes for each major issue. Be specific.

## 4. SEVERITY ASSESSMENT
Table with: Area | Issue | Severity | Reasoning
Severity: CRITICAL / HIGH / MODERATE / LOW

## 5. RECOMMENDED ACTIONS
- IMMEDIATE (within 1 week)
- SHORT-TERM (within 1 month)
- LONG-TERM (within 3-6 months)

## 6. ADDITIONAL NOTES
Other observations, precautions, client notes.

## 7. MISSING OR UNCLEAR INFORMATION
Gaps, conflicts, or Not Available items.

Be thorough, professional, and client-friendly."""

    try:
        client_groq = Groq(api_key=groq_key)
        chat = client_groq.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=4000
        )
        report_text = chat.choices[0].message.content
        return jsonify({'report': report_text, 'images': images})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("DDR Generator running at http://localhost:5000")
    app.run(debug=True, port=5000)