import fitz
import re
# from pdfminer.high_level import extract_text
import nltk

# 下载 NLTK 的 Punkt 分词器（用于句子分割），只需运行一次
nltk.download('punkt')
nltk.download('punkt_tab')

# 解析引用标记的函数，例如将 "[1,2-4]" 转换为数字集合 {1, 2, 3, 4}
def parse_citation(citation_str):
    citation_str = citation_str.strip('[]')  # 移除括号
    numbers = set()
    parts = citation_str.split(',')
    for part in parts:
        if '-' in part:
            start, end = map(int, part.split('-'))
            numbers.update(range(start, end + 1))
        else:
            numbers.add(int(part))
    return numbers

# 主函数：找到引用目标文章的句子
def find_citing_sentences(text, title):
    # 1. 提取 PDF 全文
    
    # 2. 将文本按行分割，找到参考文献部分
    lines = text.split('\n')
    ref_start = None
    for i, line in enumerate(lines):
        if re.search(r'\bReferences\b|\bBibliography\b', line, re.I):  # 忽略大小写
            ref_start = i
            break
    if ref_start is None:
        return [],[]
    ref_section = '\n'.join(lines[ref_start + 1:])  # 参考文献内容
    main_text = '\n'.join(lines[:ref_start])        # 正文内容
    
    # 3. 在参考文献中找到所有 [数字] 并解析
    ref_matches = list(re.finditer(r'\[\d+\]', ref_section))
    if not ref_matches:
        return [],[]

    references = {}
    for i in range(len(ref_matches)):
        start = ref_matches[i].end()
        end = ref_matches[i + 1].start() if i + 1 < len(ref_matches) else len(ref_section)
        ref_text = ref_section[start:end].strip()
        number = int(ref_matches[i].group()[1:-1])  # 提取数字，例如 [1] -> 1
        references[number] = ref_text
    
    # 4. 找到包含目标标题的参考文献编号
    target_numbers = [num for num, ref in references.items() if title in ref]
    print(target_numbers)
    if not target_numbers:
        return [],[]
    # 5. 将正文分割成句子
    main_text = main_text.replace('\n','')
    # —–
    main_text = main_text.replace('—','-')
    main_text = main_text.replace('–','-')

    sentences = nltk.sent_tokenize(main_text)
    
    # 6. 找到包含目标编号引用的句子
    citing_sentences = []
    for sentence in sentences:
        citations = re.findall(r'\[\d+(?:\s*[,-]\s*\d+)*\]', sentence)  # 匹配 [1], [1,2], [1-3] 等
        for citation in citations:
            cited_numbers = parse_citation(citation)
            if any(num in cited_numbers for num in target_numbers):
                citing_sentences.append(sentence)
                break  # 如果句子已匹配，无需检查其他引用
    
    return citing_sentences,target_numbers


# def extract_text_and_tables(pdf_path):
#     result = ''
#     with pdfplumber.open(pdf_path) as pdf:
#         for page in pdf.pages:
#             # 提取文本
#             text = page.extract_text()
#             result = result + text

#             # 提取表格
#             tables = page.extract_tables()
#             if tables:
#                 print("Page Tables:")
#                 for table in tables:
#                     for row in table:
#                         result = result + str(row)
#     return result


def extract_text_with_fitz(pdf_path):
    text = ""
    doc = fitz.open(pdf_path)
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text += page.get_text()
    doc.close()
    return text

def find_content(text,keywords):
    # text = text.replace('\n','')
    # text = text.replace('. (','**********!!!!!')
    # text = text.replace('. 202','**********~~~~~')

    # sentences = text.split('. ')
    sentences = nltk.sent_tokenize(text)
    shortest = '未找到'
    for s in sentences:
        # s = s.replace('**********!!!!!','. (')
        # s = s.replace('**********~~~~~','. 202')

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
    pdf_path = './downloads/2412.13488.pdf'
    pdf_text = extract_text_with_fitz(pdf_path)
    keywords = {
            'Yu et al., 2023','Yu et al.,2023','Yu et al.,\n2023','Yu et al.,\n 2023','Yu et al., \n2023', 'Yu et al., 2024','Yu et al.,2024','Yu et al.,\n2024','Yu et al.,\n 2024','Yu et al., \n2024',
            'Yu et al., (2023)','Yu et al.,(2023)','Yu et al.,\n(2023)','Yu et al.,\n (2023)','Yu et al., \n(2023)', 'Yu et al., (2024)','Yu et al.,(2024)','Yu et al.,\n(2024)','Yu et al.,\n (2024)','Yu et al., \n(2024)',
            'Yu et al. 2023','Yu et al.2023','Yu et al.\n2023','Yu et al.\n 2023','Yu et al. \n2023', 'Yu et al. 2024','Yu et al.2024','Yu et al.\n2024','Yu et al.\n 2024','Yu et al. \n2024',
            'Yu et al. (2023)','Yu et al.(2023)','Yu et al.\n(2023)','Yu et al.\n (2023)','Yu et al. \n(2023)', 'Yu et al. (2024)','Yu et al.(2024)','Yu et al.\n(2024)','Yu et al.\n (2024)','Yu et al. \n(2024)',             
            }
    sentence = find_content(pdf_text, keywords)

    if sentence == '未找到':
        nltk.download('punkt')
        nltk.download('punkt_tab')
        title = 'Metamath'
        sentences,symbol_number = find_citing_sentences(pdf_text, title)
        print(sentences,symbol_number)