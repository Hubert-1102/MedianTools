from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time




def nips(papers):
    driver = webdriver.Edge()
    for paper in papers:
        try:
            driver.get(paper.url) 
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.XPATH,'/html/body/div[2]/div/p[2]/i'))
            )
            author_container = driver.find_element(By.XPATH,'/html/body/div[2]/div/p[2]/i')
            author_name = author_container.text
            print(author_name)
            paper.authors=author_name.split(',')
        except:
            print('error!!!!!!!!!!!       '+paper.url,paper.title)
    driver.quit()
#  <span _ngcontent-ng-c1131135293="">Caiguang Zhang</span>

def ieee(papers):
    driver = webdriver.Edge()
    for paper in papers:
        try:
            driver.get(paper.url) 
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR,'span[_ngcontent-ng-c1131135293=""]'))
            )
            author_containers = driver.find_elements(By.CSS_SELECTOR,'span[_ngcontent-ng-c1131135293=""]')
            seen = set()
            for author_container in author_containers:
                author_name = author_container.text.replace(';','').strip()
                if author_name not in seen and len(author_name)>1:
                    seen.add(author_name)
                    paper.authors.append(author_name)
            print(paper.authors)
        except:
            print('error!!!!!!!!!!!       '+paper.url,paper.title)
    driver.quit()


def openreview(papers):
    driver = webdriver.Edge()
    for paper in papers:
        try:
            driver.get(paper.url) 
            WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'a[data-toggle="tooltip"][data-placement="top"]'))
        )
            elements = driver.find_elements(By.CSS_SELECTOR, 'a[data-toggle="tooltip"][data-placement="top"]')
            authors = []
            for element in elements:
                if 'CC BY 4.0' in element.text:
                    continue
                authors.append(element.text)
            print(authors)
            paper.authors = authors
        except:
            print('error!!!!!!!!!!!       '+paper.url,paper.title)
        time.sleep(5)

def springer(papers):
    # <a data-test="author-name" data-track="click" data-track-action="open author" data-track-label="link"
    driver = webdriver.Edge()
    for paper in papers:
        try:
            driver.get(paper.url) 
            WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'a[data-test="author-name"][data-track="click"][data-track-action="open author"][data-track-label="link"]'))
        )
            elements = driver.find_elements(By.CSS_SELECTOR, 'a[data-test="author-name"][data-track="click"][data-track-action="open author"][data-track-label="link"]')
            authors = []
            for element in elements:
                authors.append(element.text)
            print(authors)
            paper.authors = authors
        except:
            print('error!!!!!!!!!!!       '+paper.url,paper.title)

def acm(papers):
    """
    此方法有问题
    暂时不用
    
    """
    # 'span[property="familyName"]'
    driver = webdriver.Edge()
    for paper in papers:
        try:
            driver.get(paper.url) 
            WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'span[property="familyName"]'))
        )
            WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'span[property="givenName"]'))
        )
            elements_familyName = driver.find_elements(By.CSS_SELECTOR, 'span[property="familyName"]')
            elements_givenName = driver.find_elements(By.CSS_SELECTOR, 'span[property="givenName"]')

            authors = []
            for index,element in enumerate(elements_familyName):
                # if index % 2 ==0 :
                    # continue
                authors.append(f'{elements_givenName[index].text} {element.text}')


            print(authors)
            paper.authors = authors
        except:
            print('error!!!!!!!!!!!       '+paper.url,paper.title)
def arxiv(papers):
    driver = webdriver.Edge()
    for paper in papers:
        driver.get(paper.url)
        WebDriverWait(driver, 15).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "authors"))
                )
        # 定位所有 class 为 author 的容器
        author_containers = driver.find_elements(By.CLASS_NAME, 'authors')
        
        # 存储作者名称的列表
        author_names = []

        for container in author_containers:
            a_tags = container.find_elements(By.TAG_NAME, 'a')

            for a_tag in a_tags:
                name = a_tag.text.strip()  
                if name:  
                    author_names.append(name)

        for name in author_names:
            paper.authors.append(name)
        print(paper.authors)

    # 关闭浏览器
    driver.quit()

def acl(papers):
    driver = webdriver.Edge()
    for paper in papers:
        driver.get(paper.url)
        WebDriverWait(driver, 15).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "lead"))
                )
        author_containers = driver.find_elements(By.CLASS_NAME, 'lead')
        
        author_names = []

        for container in author_containers:
            a_tags = container.find_elements(By.TAG_NAME, 'a')

            for a_tag in a_tags:
                name = a_tag.text.strip()  
                if name:  
                    author_names.append(name)

        for name in author_names:
            paper.authors.append(name)
        print(paper.authors)
    # 关闭浏览器
    driver.quit()



def get_title_url_year(url_scholar):
    driver = webdriver.Edge()
    driver.get(url_scholar)

    results = []
    page_number = 1

    try:
        while True:
            print(f"正在抓取第 {page_number} 页...")
            
            # 等待内容加载
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CLASS_NAME, "gs_rt"))
            )

            # 抓取当前页数据
            articles = driver.find_elements(By.CLASS_NAME, "gs_rt")[1:]
            year_info = driver.find_elements(By.CLASS_NAME, "gs_a")
            print(len(articles), len(year_info))
            for index,article in enumerate(articles):
                try:
                    link = article.find_element(By.TAG_NAME, "a")
                    title = link.text.strip()
                    url = link.get_attribute("href").strip()
                    year = year_info[index].text.strip()
                    if title and url:
                        results.append({"title": title, "url": url, "year": year.split(',')[-1]})
                except Exception as e:
                    print(f"条目抓取失败: {str(e)}")
                    continue

            # 尝试翻页
            try:
                # <b style="display:block;margin-left:53px">下一頁</b>
                WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'b[style="display:block;margin-left:53px"]'))
            )
                next_button = driver.find_element(
                    By.CSS_SELECTOR, 'b[style="display:block;margin-left:53px"]'
                )
                
                # 滚动到下一页按钮
                driver.execute_script("arguments[0].scrollIntoView();", next_button)
                time.sleep(1)
                
                # 高亮显示按钮（调试用）
                driver.execute_script("arguments[0].style.border='3px solid red';", next_button)
                
                next_button.click()
                page_number += 1
                
                # 等待新页面加载
                WebDriverWait(driver, 15).until(
                    EC.staleness_of(articles[0])  # 等待旧元素失效
                )
                time.sleep(3)  # 额外缓冲时间
                
            except NoSuchElementException:
                print("已到达最后一页")
                break
            except TimeoutException:
                print("页面加载超时，尝试重试...")
                # 可以添加重试逻辑
                break

    finally:
        driver.quit()

    # 去重处理
    seen = set()
    unique_results = []
    for item in results:
        identifier = item["url"]
        if identifier not in seen:
            seen.add(identifier)
            unique_results.append(item)

    # 输出统计信息
    print(f"\n共抓取 {len(unique_results)} 篇唯一文章：")
    for idx, item in enumerate(unique_results[:3], 1):  # 显示前3条作为示例
        print(f"{idx}. {item['title']}")
        print(f"   {item['url']}")
        print(f"   {item['year']}")


    # 保存到文件
    import csv
    with open('data/all_articles.csv', 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=['title', 'url', 'year'])
        writer.writeheader()
        writer.writerows(unique_results)
