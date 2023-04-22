import os
from ..helpers.get_netloc import get_netloc
import urllib.request
import re
import PyPDF2
import hashlib

class DocumentParser:
    def __init__(self) -> None:
        pass

    def process(self, url):
        name = hashlib.sha256(url.encode()).hexdigest()[:4]
        path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "documents",
            f"{name}.pdf"
        )
        os.makedirs(
            os.path.dirname(path),
            exist_ok=True
        )
        if not os.path.isfile(path):
            urllib.request.urlretrieve(
                url, 
                path
            )
        PDFFile = open(path,'rb')
        PDF = PyPDF2.PdfReader(PDFFile)
        pages = len(PDF.pages)
        key = '/Annots'
        uri = '/URI'
        ank = '/A'

        links = []
        for page in range(pages):
            pageSliced = PDF.pages[page]
            pageObject = pageSliced.get_object()
            if key in pageObject.keys():
                ann = pageObject[key]
                for a in ann:
                    u = a.get_object()
                    if uri in u[ank].keys():
                        links.append(u[ank][uri])

        os.system("pdftotext {} {}".format(
                path, path.replace(".pdf", ".txt")
            )
        )
        with open(path.replace(".pdf", ".txt"), "r") as file:
            results = re.findall(r"\w+://\w+\.\w+\.\w+/?[\w\.\?=#]*", file.read().replace("\n", ""))
            for i in results:
                if i not in links:
                    links.append(i)
        return {
            "text": None,
            "title": None,
            "netloc": get_netloc(url),
            "links": links
        }

    
if __name__ == "__main__":
    print(DocumentParser().process("https://arxiv.org/pdf/2103.09113.pdf"))
#    print(DocumentParser().process("https://raw.githubusercontent.com/msuiche/porosity/master/defcon2017/dc25-msuiche-Porosity-Decompiling-Ethereum-Smart-Contracts-wp.pdf"))
