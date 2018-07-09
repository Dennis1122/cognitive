from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.pdfpage import PDFPage
from pdfminer.layout import LAParams
from StringIO import StringIO

def read_pdf(path, pages=None):
    if not pages:
        pagenums = set()
    else:
        pagenums = set(pages)
    manager = PDFResourceManager()
    fd=open(path, 'rb')
    text = list()
    for page in PDFPage.get_pages(fd, pagenums):
        output = StringIO()
        converter = TextConverter(manager, output, laparams=LAParams())
        interpreter = PDFPageInterpreter(manager, converter)
        interpreter.process_page(page)
        text.append(output.getvalue())
        converter.close()
        output.close
    fd.close()
    converter.close()
    return text
    
    