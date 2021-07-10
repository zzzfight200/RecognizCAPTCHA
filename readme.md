# 验证码自动识别

某邮箱登录的验证码识别程序，使用了python的selenium模块。一开始本打算使用pytesseract库，但最终使用了百度智能云API进行验证码识别。百度智能云的文字识别功能精确版，准且率大概不到50%，每月有200次的免费使用额度。有关pytesseract的代码没有删除，以后有时间再用起来。

代码经过一定修改，还没有验证，但主体没问题，可用

## Firefox浏览器驱动GeckoDriver安装方法

  python中常用selenium爬取动态渲染网页，这个过程之中需要安装浏览器驱动，以Firefox火狐浏览器安装驱动Geckodriver方法如下：
下载地址：https://github.com/mozilla/geckodriver/releases
将下载下来的GeckoDriver.exe放入python安装路径下的Scripts文件夹内
最后进入cmd控制台，输入geckodriver，如果出现版本信息和端口监听信息，则安装成功

## 后续

代码中RecognizCAPTCHA()函数为通过pytesseract识别，但参数没有设置好，以后再调试。

