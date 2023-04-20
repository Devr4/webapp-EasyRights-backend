import shutil
from uuid import uuid4
from PyPDF2 import PdfFileMerger
from fillpdf import fillpdfs
from fpdf import FPDF
from config import *
import os

def create_note(note: str, main_pdf_path: str):
    if note:
        fpdf = FPDF()
        fpdf.add_page()
        fpdf.set_font("Arial", size=30)
        fpdf.set_text_color(255, 0, 0)
        fpdf.cell(w=0, h=10, txt="Note", border=0, align="C", ln=1)
        fpdf.cell(w=0, h=10, txt="", border=0, align="C", ln=1)
        fpdf.set_font("Arial", "", size=12)
        fpdf.set_text_color(0, 0, 0)
        fpdf.multi_cell(0, 10, "\n" + note + "\n", align="C", border=1)
        fpdf.output(main_pdf_path + "2")
        pdf_merger = PdfFileMerger()
        pdf_merger.append(main_pdf_path)
        pdf_merger.append(main_pdf_path + "2")
        file_name = str(uuid4()) + ".pdf"
        save_path = os.path.join(os.getcwd(), "static_download", file_name)
        with open(save_path, 'wb') as output:
            pdf_merger.write(output)
        pdf_merger.close()
        try:
            os.unlink(main_pdf_path + "2")
        except Exception as e:
            print(f"can't delete file {main_pdf_path}2: {e}")
        try:
            os.unlink(main_pdf_path)

        except Exception as e:
            print(f"can't delete file {main_pdf_path}: {e}")
        return file_name
    dest = shutil.move(main_pdf_path, os.path.join(os.getcwd(), "static_download"))
    return os.path.basename(dest)


def create_pdf(data: list[dict]):
    if data:
        data_dict = {}
        file_name = str(uuid4()) + ".pdf"
        path_to_file = os.path.join(os.getcwd(), "web_app", "tmp", file_name)
        for d in data[:-1]:
            data_dict.update(d["answer"])
        modulo_path = os.path.join(os.getcwd(), "web_app", "static", "modulo.pdf")
        fillpdfs.write_fillable_pdf(modulo_path, path_to_file, data_dict)
        file_name2 = str(uuid4()) + ".pdf"
        path_to_file2 = os.path.join(os.getcwd(), "web_app", "tmp", file_name2)
        fillpdfs.flatten_pdf(path_to_file, path_to_file2)
        try:
            os.unlink(path_to_file)
        except Exception:
            print(f"can't delete file {path_to_file}")
        print(f"File created: {file_name2}")
        return create_note(data[-1]["answer"]["Note"], path_to_file2)
