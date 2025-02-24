from find_citation import find_citing_sentences,find_content,find_citation_symbol,extract_text_with_fitz



if __name__ == '__main__':
    arxiv_pdf = './downloads/2311.03191.pdf'  # 替换为实际的 PDF 文件路径,如果是arxiv，可以使用download.py批量下载
    title = 'Metamath'            # 替换为你要查找的文章标题
    # 使用非标号格式查找，需要自行更换关键词，例如Metamath的引用通常是Yu et al.
    keywords = {'Yu et al.',
            'Yu et al., 2023','Yu et al.,2023','Yu et al.,\n2023','Yu et al.,\n 2023','Yu et al., \n2023', 'Yu et al., 2024','Yu et al.,2024','Yu et al.,\n2024','Yu et al.,\n 2024','Yu et al., \n2024',
            'Yu et al., (2023)','Yu et al.,(2023)','Yu et al.,\n(2023)','Yu et al.,\n (2023)','Yu et al., \n(2023)', 'Yu et al., (2024)','Yu et al.,(2024)','Yu et al.,\n(2024)','Yu et al.,\n (2024)','Yu et al., \n(2024)',
            'Yu et al. 2023','Yu et al.2023','Yu et al.\n2023','Yu et al.\n 2023','Yu et al. \n2023', 'Yu et al. 2024','Yu et al.2024','Yu et al.\n2024','Yu et al.\n 2024','Yu et al. \n2024',
            'Yu et al. (2023)','Yu et al.(2023)','Yu et al.\n(2023)','Yu et al.\n (2023)','Yu et al. \n(2023)', 'Yu et al. (2024)','Yu et al.(2024)','Yu et al.\n(2024)','Yu et al.\n (2024)','Yu et al. \n(2024)',             
            }
    text = extract_text_with_fitz(arxiv_pdf)
    content = find_content(text,keywords)
    symbol = find_citation_symbol(content,keywords)
    # 如果Yu et al. 这种方式没有找到，则进入标号匹配[34]模式
    if content == '未找到':
        title = 'Metamath' # 此处替换成自己文章中的关键字
        print(arxiv_pdf)
        sentences,symbol_number = find_citing_sentences(text, title)
        if sentences:
           print('标号模式找到原文')
           content = sentences[0] 
        if symbol_number:
            symbol = str(symbol_number)
        print(content)
        print(symbol)   

