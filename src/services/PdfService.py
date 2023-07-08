import os
import urllib


class PdfService:

    @staticmethod
    def download_pdf(pdf_path: str):
        folder_path = "./downloads"
        if not os.path.exists(folder_path): os.mkdir(folder_path)

        folder_path = os.path.join(folder_path, pdf_path.split('/')[-2])
        if not os.path.exists(folder_path): os.mkdir(folder_path)
        file_save_path = os.path.join(folder_path, pdf_path.split('/')[-1])

        if os.path.exists(file_save_path):
            file_save_path = file_save_path

        urllib.request.urlretrieve(pdf_path, file_save_path)


