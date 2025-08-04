# app/utils/compress.py
import pikepdf
import zipfile
import os

def compress_pdf(input_path):
    output_path = input_path.replace(".pdf", "_compressed.pdf")
    with pikepdf.open(input_path) as pdf:
        pdf.save(output_path, optimize_version=True)
    os.remove(input_path)
    return output_path

def compress_docx(input_path):
    output_path = input_path.replace(".docx", "_compressed.zip")
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(input_path, arcname=os.path.basename(input_path))
    os.remove(input_path)
    return output_path
