from bs4 import BeautifulSoup
import requests
import re
from selenium import webdriver
import time
browser = webdriver.Chrome()
def get_link_pw():
    i=1
    download_link=[]
    while i <= 13:
        html = 'https://www.sq688.com/search.php?key=%E5%BC%A0%E5%AD%A6%E5%8F%8B&page='
        html += str(i)
        i+=1
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
        }
        resp = requests.get(html, headers=headers)
        # resp.encoding = 'utf-8'
        soup = BeautifulSoup(resp.content, "lxml")
        for link in soup.find_all("a",class_='dw'):
            download_link.append(link.get('href'))
    with open('张学友音乐1.txt','w')as f:
        for i in download_link:
            start='https://www.sq688.com/'
            html =start + i
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
            }
            resp = requests.get(html, headers=headers)
            soup = BeautifulSoup(resp.content, "lxml")
            b=soup.find_all('p',class_='downurl')
            con=str(b[0].text)
            link=re.search(":(.*)[密提]",con).group(1)
            con=con.split()
            pw=con[-1][-4:]
            f.write(link+' '+pw)
            f.write('\n')


def batch_save_baidupan():
    def loginphont():
        browser.get("https://pan.baidu.com/")  # 打开链接
        browser.maximize_window()
        browser.find_element_by_id("TANGRAM__PSP_4__footerULoginBtn").click()
        browser.find_element_by_id("TANGRAM__PSP_4__userName").send_keys("用户名")
        browser.find_element_by_id("TANGRAM__PSP_4__password").send_keys("密码")
        browser.find_element_by_id("TANGRAM__PSP_4__submit").click()
        time.sleep(30)

    address_and_code = []
    for line in open('张学友音乐1.txt'):  # 循环读取百度地址和提取码
        line = line.split()
        address = line[0]  # 分离出百度盘地址
        code = line[1]  # 分割出提取码
        address_and_code.append([address,code])
    def add_to_source(address,code):
        browser.get(address)  # 打开链接
        if u"分享的文件已经被删除了" in browser.page_source:  # 如果文件被删除，跳过本次循环，重新一轮循环开始
            return
        else:
            browser.find_element_by_xpath('//*[@id="vxpqM1Gr"]').send_keys(code)  # 输入提取码
            time.sleep(2)
            browser.find_element_by_xpath("//span[contains(text(),'提取文件')]").click()
            time.sleep(3)
            browser.find_element_by_xpath("//span[contains(text(),'保存到网盘')]").click()
            time.sleep(1)
            browser.find_element_by_xpath("//span[contains(text(),'我的资源')]").click()
            time.sleep(1)
            browser.find_element_by_xpath("//span[contains(text(),'确定')]").click()
            time.sleep(3)
            
            
    def keep():
        for line in address_and_code:  # 循环读取百度地址和提取码
            try:
                add_to_source(line[0],line[1])
            except:
                with open ("not added.txt","a+") as f:
                    print(line[0],line[1])
                    f.write(line[0]+' '+line[1]+'\n')
    loginphont()
    keep()

batch_save_baidupan()
