from flask import Flask, request, send_file, make_response, send_from_directory, Response, jsonify
from pypdf import PdfMerger
from io import BytesIO
import  base64


app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello, World!'
    
@app.route('/health_check')
def check():
    return {"status":"Application is running"}
    
@app.route('/merge_pdfs', methods=['POST'])
def merge_pdfs():
    # Check if files were sent in the request
    print("MERGE INVOKED")
    if 'files' not in request.files:
        return "No files provided", 400
    try:
        pdf_files = request.files.getlist('files')
    except Exception as e:
        pdf_files = None
        print(e)
        return f"Error with input file or with the input ingestion.\n{e}", 400
    try:
        if pdf_files!=None:
            merger = PdfMerger()
            for pdf in pdf_files:
                merger.append(pdf)
            merged_pdf_buffer = BytesIO()
            merger.write(merged_pdf_buffer)
            merged_pdf_buffer.seek(0)
            buffer_base64 = base64.b64encode(merged_pdf_buffer.getvalue()).decode('utf-8')
        
            response_data = {
                "buffer": buffer_base64,
                "status": "Success"
            }
            print("Res data")
            print(response_data)
            return jsonify(response_data)
    except Exception as e:
        print(e)
        return f"Error during the conversion.\n{e}", 400
        
@app.route('/test_convertor')
def test():
    # Instantiate the PdfMerger object
    merger = PdfMerger()
    
    # Append the PDF file to the merger
    merger.append("TOEFL_2840801238061083.pdf")
    
    # Create a BytesIO buffer to hold the merged PDF
    merged_pdf_buffer = BytesIO()
    
    # Write the merged PDF content to the buffer
    merger.write(merged_pdf_buffer)
    
    # Seek to the beginning of the buffer
    merged_pdf_buffer.seek(0)
    
    # Prepare the response data
    buffer_base64 = base64.b64encode(merged_pdf_buffer.getvalue()).decode('utf-8')
        
    response_data = {
            "buffer": buffer_base64,
            "status": "Success"
    }
    print("Res data")
    print(response_data)
    
    # Return the response data
    return jsonify(response_data)
    

# def lambda_handler(event, context):
#     return awsgi.response(app, event, context, base64_content_types={"image/png"})