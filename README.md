# Latex论文翻译工具
主要针对英文翻译为中文，可以保留latex中的公式、特殊命令与引用（包括文献引用和标签引用）。【目前只支持百度翻译】

## 安装使用
### 下载本项目
```
git clone https://github.com/waitwaitforget/LatexPaperTranslation.git
cd LatexPaperTranslation
pip install -r requirements.txt # 安装依赖库
```
### 注册百度翻译开发者账号
这一步需要自行Google或者百度，比较简单。

主要是拿到百度翻译API的使用权限，注册以后需要提供appid和secretkey，在本项目SETTINGS.py文件中设置好。

### 运行本项目
```
python run.py
```
下面你可以打开浏览器，输入[http://localhost:5000](http://localhost:5000)。

把你的英文latex文本输入到左边的输入框，然后点击translate按钮可以在右边得到翻译后的文本。
**注意** 

多段翻译需要在段之间加一个空行

## 使用规则
目前项目里只针对latex行内公式、`\**{}`这种格式的字符串、\ref{}、\cite{}支持。
如果需要额外的支持，可以自行修改lib/translator.py文件，添加新的规则。

## 示例
下面是我测试的一段结果。
![image](https://raw.githubusercontent.com/waitwaitforget/LatexPaperTranslation/master/img/demo.png)
## 说明
本工具是个人写博士毕业论文期间辅助使用的，比较简陋。如果使用过程中有什么问题，可以提issue。
