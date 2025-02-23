import pdfplumber
import fitz

def extract_text_and_tables(pdf_path):
    result = ''
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            # 提取文本
            text = page.extract_text()
            result = result + text

            # 提取表格
            tables = page.extract_tables()
            if tables:
                print("Page Tables:")
                for table in tables:
                    for row in table:
                        result = result + str(row)
    return result


def extract_text_with_fitz(pdf_path):
    text = ""
    doc = fitz.open(pdf_path)
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text += page.get_text()
    doc.close()
    return text

def find_content(text,keywords):
    text = text.replace('. (','**********!!!!!')
    text = text.replace('. 202','**********~~~~~')

    sentences = text.split('. ')
    shortest = '未找到'
    for s in sentences:
        s = s.replace('**********!!!!!','. (')
        s = s.replace('**********~~~~~','. 202')

        if any(keyword in s for keyword in keywords):
            if shortest=='未找到' or len(s) < len(shortest):
                shortest = s
    shortest = shortest.replace('-\n','')
    print(shortest)
    return shortest

def find_citation_symbol(sentence, keywords):
    for key in keywords:
        if key in sentence:
            return key
    return '未找到'

if __name__ == "__main__":
    pdf_path = 'downloads/2502.11476.pdf'
    pdf_text = extract_text_with_fitz(pdf_path)
    pdf_text = pdf_text.replace('\n','')

    # find_content(pdf_text, keywords)