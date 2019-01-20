# Cryptography Website

Information Security Experiment Course 3 of Northeastern University

> Update: 2019.1.20 17:40

> Code Commit: 2018.9.26

> Editor: NEU - Amy Li

> Link: [Amy_Li's GitHub](https://github.com/AmyLi98)

> Cooperators: NEU - [LZY](https://github.com/WangHexie) & [MQY](https://github.com/OliviaCurry) & [JPH](https://github.com/Barrrrrry)

> Contact: hsrlhl@outlook.com

## 版权声明

版权所有，翻版必究。

Cryptography Website 代码及文档著作权归作者所有，任何形式的转载都请联系作者获得授权并注明出处。

### 使用说明

`usage:`    
   * python run.py \[webport\] \[socket_port\]   
   (Default port: \[5001\] \[8001\])
   
接下来是系统的简要操作说明：
由于我们的系统是基于web的，因此我们打包形成了run - Copy.vbs和run.vbs两个可执行文件。
这两个可执行文件在Cryptography文件夹下。
但是这两个的IP地址和端口号各不相同，正常运行时应双击run - Copy.vbs，运行后弹出系统主页，此时的IP地址为127.0.0.1:5001，端口号为8001。
在双机通信和双机加解密时,双机运行run.vbs，此时的IP地址为127.0.0.1:5002，端口号为8002。
一般情况下，双击两个.vbs文件是可以直接运行的，倘若由于系统或者配置的问题无法立即正常运行，可以通过cmd命令行或者powershell运行。

powershell/cmd中运行流程：

`usage:`   

1.cd到run.vbs所在的文件目录下   
2.执行命令：./small/python.exe run.py

### 实践环境
- 操作系统：Windows 10
- 开发环境：JetBrains PyCharm 2018.2 x64

### Cryptography Website系统基本功能架构图

![图1 Cryptography Website系统基本功能架构图](https://github.com/AmyLi98/Cryptography/blob/master/images/Cryptography%20Website.png)

Cryptography Website系统由四个模块构成：
**Home(主页)、Description(简介)、Cryptography Tool(密码学工具)、About Us(关于我们)。**

其中，Cryptography Tool部分是网站的核心部分，主要实现单机加解密和双机加解密实践的功能。

### Cryptography Website前端与后端交互的设计图

![图2 Cryptography Website前端与后端交互的设计图](https://github.com/AmyLi98/Cryptography/blob/master/images/%E5%89%8D%E5%90%8E%E7%AB%AF%E4%BA%A4%E4%BA%92.png)

python后端我们编写的密码学算法库将为单机加解密和双机加解密提供依赖，双机加解密的socket服务端将通过websocket接口每隔一段时间向web端发送HTTP请求，web端也每隔一段时间向socket服务端发送HTTP请求，由此两者建立链接，消息将每个很短一段时间从前端不断向后端发送，后端处理后的数据也不断向前端发送，使前端实时显示最新的数据，从而实现前端与后端的交互。

### 单机加解密和双机加解密功能的网页和系统设计
#### （1）Single Machine ——单机加解密
实现单机加解密功能的网页single_tool.html将Caesar、Keyword Cipher、Vigenere Cipher、Text-autokey Cipher、Playfair Cipher、Column Permutation Cipher、Double-Transposition Cipher、RC4、DES、RSA、MD5等11种密码和DH密钥交换集成在同一界面中，使用标签的方法实现不同加密算法之间的切换。

Encryption和Decryption均在页面显示，用户根据需要的不同进行不同的操作。页面的JavaScript代码应实现在用户点击Encrypt和Decrypt按钮时，监听文本输入框的变化并将发送载有更新的文本输入框内容的HTTP请求，后台socket实时监听并获取HTTP请求用来更新加解密算法的传入参数为文本输入框的内容。

在click事件监听器中，我采用的是XMLHttpRequest(XHR)，XHR是一个API对象，其中的方法可以用来在浏览器和服务器端传输数据，这个对象是浏览器的JavaScript环境提供的。从XHR获取数据的目的是为了持续修改一个加载过的页面。

#### （2）Dual machine encryption and decryption ——双机加解密

![图3 双机加解密系统设计图](https://github.com/AmyLi98/Cryptography/blob/master/images/%E5%8F%8C%E6%9C%BA%E5%8A%A0%E8%A7%A3%E5%AF%86.png)

实现双机加解密的网页double_cipher.html将通过某一用户输入的ip地址和端口号在两个用户之间建立连接，实现双机加解密，即一方加密后的密文除了在本地显示，同时在对方的解密端的密文框内显示，此时若对方已知正确的解密密钥，将实现原文的破译。

双机加解密的过程中需要实现每隔 300ms 调用一次监控待加密消息处的函数，以便实时进行加解密操作以及破译端实时获取加密端加密后的密文。

#### （3）Double machine communication ——双机通信

![图4 双机通信系统设计图](https://github.com/AmyLi98/Cryptography/blob/master/images/%E5%8F%8C%E6%9C%BA%E9%80%9A%E4%BF%A1.png)

实现双机通信的double_communication.html将通过用户输入的ip地址和端口号在两个网页（即用户）之间建立连接，实现双机通信，即即时聊天。

此时网页的JavaScript代码应使用socket在两者之间建立连接并实现发送一个chat命令，命令的内容是经过URI编码的message，在这里使用的加密方法是DES，然后另一方的web端实时监听本地的socket服务端，收到消息的第一时间，应实现解密，将消息转换成明文在本地的messages栏显示出来。

### 几个加解密算法
#### Autokey Plaintext
Autokey Cipher是多表替换密码，与维吉尼亚密码类似，但使用不同的方法生成密钥。通常来说它要比维吉尼亚密码更安全。自动密钥密码主要有两种，密文自动密钥密码（Autokey Ciphertext）和明文自动密钥密码（Autokey Plaintext）。由于两者基本原理类似，因此我选择实现Autokey Plaintext（又称Text-autokey）。

Text-autokey密码是将部分明文合并到密钥中的密码，它使用先前的明文消息文本来确定密钥流中的下一个元素。Autokey密码比使用固定密钥的多字母密码更安全，因为密钥不会在单个消息中重复。因此，与使用单个重复密钥的密码不同，诸如Kasiski检查或重合分析索引的密码分析方法将无法破译该密码加密的明文。如下例：

明文：THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG

关键词：CULTURE

自动生成密钥：CULTURE THE QUICK BROWN FOX JUMPS OVER THE

接下来的加密过程和维吉尼亚密码类似，从Vigenere密码的表格可得：

密文：VBP JOZGD IVEQV HYY AIICX CSNL FWW ZVDP WVK
#### RC4
>RSA 由 Ron Rivest设计，最初是一个专利密码产品。它是面向字节的流密码，密钥长度可变。它加解密使用相同的密钥，因此也属于对称加密算法。RC4 算法广泛应用于 SSL/TLS 协议和 WEP/WPA 协议。虽然RC4也是对称加密算法，但不同于DES的是，RC4不是对明文进行分组处理，而是字节流的方式依次加密明文中的每个字节，解密时也是依次对密文中的每个字节进行解密。

RC4算法包括初始化算法（KSA）和伪随机子密码生成算法（PRGA）两大部分。在初始化的过程中，密钥的主要功能是将S数组搅乱，i确保S数组的每个元素都得到处理，j保证S数组的搅乱是随机的。不同的S数组在经过伪随机子密码生成算法处理后，可以得到不同的子密钥序列，将S数组和明文进行XOR运算得到密文，解密过程也完全相同。

1. 密钥流：RC4算法的关键是依据明文和密钥生成相应的密钥流，密钥流的长度和明文的长度是相应的。
2. S数组：S[0],S[1].....S[255]，长度为256，S数组的每一位都是一个字节。算法执行的任何时候，S数组都包含0-255的8 bit数的排列组合，仅仅只是值的位置发生了变换。
3. 密钥K数组：长度为1-256字节。密钥的长度与明文长度、密钥流的长度没有必然关系。
4. KSA初始化算法
def KSA(key):
    :param key: 密钥
:return: S 数组
- KSA（Key Scheduling Algorithm）伪代码：
    for i from 0 to 255
        S[i] := i
    endfor
    j := 0
    for i from 0 to 255
        j := (j + S[i] + key[i mod keylength]) mod 256
        swap values of S[i] and S[j]
    endfor
5. PRGA伪随机子密码生成算法
def PRGA(S):
    :param S: S数组
:return: K数组
- PRGA（Psudo Random Generation Algorithm）伪代码：
    i := 0
    j := 0
    while GeneratingOutput:
        i := (i + 1) mod 256
        j := (j + S[i]) mod 256
        swap values of S[i] and S[j]
        K := S[(S[i] + S[j]) mod 256]
        output K
    endwhile

###  Cryptography网站系统的界面实现

由于我们组本次的工程实践项目采用网站的形式呈现系统，因此webpage界面的简洁性和用户友好度和体验度成为我们系统的一个重要的设计指标。同时，web端自身的特点导致我们在python后台与web页链接上存在诸多挑战。

本Cryptography网站系统的页面设计基于bootstrap，结合CSS、HTML5和JavaScript，实现网站系统的动态页面展示和功能的实现。
网站设计的创新点在于自行设计与定义基于CSS、HTML和jQuery等实现的各种动画效果，给予用户友好的视觉体验和效果，界面简洁，用户易于操作。

#### （1）real_index.html ——网站的主界面
1. 打开run - Copy.vbs，运行后弹出网站的主界面

![图5 real_index.html主屏幕图](https://github.com/AmyLi98/Cryptography/blob/master/images/real_index.html%E4%B8%BB%E5%B1%8F%E5%B9%95%E5%9B%BE.png)

2. 点击GitHub按钮，可以链接到我们组本次工程实践的GitHub项目网址；点击向下圆圈的按钮，可以进入网站所有密码的列举界面

![图6 real_index.html密码介绍模块(部分)](https://github.com/AmyLi98/Cryptography/blob/master/images/%E5%AF%86%E7%A0%81%E4%BB%8B%E7%BB%8D%E6%A8%A1%E5%9D%97(%E9%83%A8%E5%88%86).png)

3. 点击Start to use按钮，可以跳转到单机加解密和双机加解密实践介绍的块，点击Start按钮可以分别跳转到加解密工具的主页和双机加解密的主页

![图7 real_index.html的单机加解密start模块](https://github.com/AmyLi98/Cryptography/blob/master/images/%E5%8D%95%E6%9C%BA%E5%8A%A0%E8%A7%A3%E5%AF%86start%E6%A8%A1%E5%9D%97.png)

![图8 real_index.html的双机加解密start模块](https://github.com/AmyLi98/Cryptography/blob/master/images/%E5%8F%8C%E6%9C%BA%E5%8A%A0%E8%A7%A3%E5%AF%86start%E6%A8%A1%E5%9D%97.png)

4. 介绍网站的优越性模块

![图9 real_index.html的strength模块](https://github.com/AmyLi98/Cryptography/blob/master/images/strength%E6%A8%A1%E5%9D%97.png)

5. 介绍团队组成和分工的模块

![图10 real_index.html的team模块](https://github.com/AmyLi98/Cryptography/blob/master/images/team%E6%A8%A1%E5%9D%97.png)

#### （2）home_cryptography.html ——加解密工具的主页
1. 主页

![图11 home_cryptography.html加解密工具的主页](https://github.com/AmyLi98/Cryptography/blob/master/images/home_cryptography.html%E5%8A%A0%E8%A7%A3%E5%AF%86%E5%B7%A5%E5%85%B7%E7%9A%84%E4%B8%BB%E9%A1%B5.png)

2. 左侧导航栏处通过不同菜单的下拉栏，可以选择进入单机加解密或者双机加解密
 
![图12 home_cryptography.html左侧导航栏](https://github.com/AmyLi98/Cryptography/blob/master/images/%E5%B7%A6%E4%BE%A7%E5%AF%BC%E8%88%AA%E6%A0%8F.png)
 
#### （3）single_tool.html ——单机加解密功能页
1. 单机加解密网页的主界面
 
![图13 单机加解密网页的主界面](https://github.com/AmyLi98/Cryptography/blob/master/images/%E5%8D%95%E6%9C%BA%E5%8A%A0%E8%A7%A3%E5%AF%86%E7%BD%91%E9%A1%B5%E7%9A%84%E4%B8%BB%E7%95%8C%E9%9D%A2.png)

2. 点击“Column permutation Cipher”标签，输入明文和关键字，点击Encrypt按钮即可进行加密操作，将加密后的密文复制到右侧的解密端，可以进行解密操作
 
![图14 单机加解密实例界面](https://github.com/AmyLi98/Cryptography/blob/master/images/%E5%8D%95%E6%9C%BA%E5%8A%A0%E8%A7%A3%E5%AF%86%E5%AE%9E%E4%BE%8B%E7%95%8C%E9%9D%A2.png)
 
#### （4）double_cipher.html ——双机加解密密码功能页

双机加解密密码功能页的主界面和单机加解密主页类似，仅多了输入IP地址的输入框，但是在JavaScript代码实现上有所不同，因此所实现的功能也有所不同。

1. 先输入要连接的主机的IP地址，输入明文和密码等待加密

![图15 双机加解密中准备链接](https://github.com/AmyLi98/Cryptography/blob/master/images/%E5%8F%8C%E6%9C%BA%E5%8A%A0%E8%A7%A3%E5%AF%86%E4%B8%AD%E5%87%86%E5%A4%87%E9%93%BE%E6%8E%A5.png)

2. 点击Encrypt按钮进行加密操作，127.0.0.1:5001处显示出加密后的密文，打开127.0.0.1:5002，可以看到解密端的密文处自动显示出加密端加密后的密文
 
![图16 双机加解密中的加密端127.0.0.1:5001](https://github.com/AmyLi98/Cryptography/blob/master/images/%E5%8F%8C%E6%9C%BA%E5%8A%A0%E8%A7%A3%E5%AF%86%E4%B8%AD%E7%9A%84%E5%8A%A0%E5%AF%86%E7%AB%AF.png)
 
![图17 双机加解密中的解密端127.0.0.1:5002](https://github.com/AmyLi98/Cryptography/blob/master/images/%E5%8F%8C%E6%9C%BA%E5%8A%A0%E8%A7%A3%E5%AF%86%E4%B8%AD%E7%9A%84%E8%A7%A3%E5%AF%86%E7%AB%AF.png)

#### （5）double_communication.html ——双机通信功能页

1. 先输入要连接的主机的IP地址和端口号，点击submit进行链接
 
![图18 双机通信中链接主机](https://github.com/AmyLi98/Cryptography/blob/master/images/%E5%8F%8C%E6%9C%BA%E9%80%9A%E4%BF%A1%E4%B8%AD%E9%93%BE%E6%8E%A5%E4%B8%BB%E6%9C%BA.png)
 
 
2. 在消息输入框中输入要传递的文字类型的消息“hello”，点击send按钮，两客户端页面呈现不同的页面显示，可以看到8002端口的客户机页面上收到信息hello
 
![图19 双机通信中8001端口客户机发送hello消息](https://github.com/AmyLi98/Cryptography/blob/master/images/8001%E7%AB%AF%E5%8F%A3%E5%AE%A2%E6%88%B7%E6%9C%BA%E5%8F%91%E9%80%81hello%E6%B6%88%E6%81%AF.png)
 
![图20 双机通信中8002端口客户机接收hello消息](https://github.com/AmyLi98/Cryptography/blob/master/images/8002%E7%AB%AF%E5%8F%A3%E5%AE%A2%E6%88%B7%E6%9C%BA%E6%8E%A5%E6%94%B6hello%E6%B6%88%E6%81%AF.png)
 
 
2. 在8002端口的消息输入框中输入要传递的中文文字类型的消息“你好”，点击send按钮，两客户端页面呈现不同的页面显示，可以看到8001端口客户机页面上收到信息“你好”
 
![图21 双机通信中8002端口客户机发送“你好”消息](https://github.com/AmyLi98/Cryptography/blob/master/images/8002%E7%AB%AF%E5%8F%A3%E5%AE%A2%E6%88%B7%E6%9C%BA%E5%8F%91%E9%80%81%E2%80%9C%E4%BD%A0%E5%A5%BD%E2%80%9D%E6%B6%88%E6%81%AF.png)
 
![图22 双机通信中8001端口客户机接收“你好”消息](https://github.com/AmyLi98/Cryptography/blob/master/images/8001%E7%AB%AF%E5%8F%A3%E5%AE%A2%E6%88%B7%E6%9C%BA%E6%8E%A5%E6%94%B6%E2%80%9C%E4%BD%A0%E5%A5%BD%E2%80%9D%E6%B6%88%E6%81%AF.png)
 
 
3. 在8001端口的客户机页面处点击“选择文件”按钮，选择任一图片类型的文件进行上传，可以发现，发送端加密图片后发送给接收端，接收端解密发送来的图片信息后，并将图片显示出来
 
![图23 双机通信中8001端口客户机发送图片类型文件](https://github.com/AmyLi98/Cryptography/blob/master/images/8001%E7%AB%AF%E5%8F%A3%E5%AE%A2%E6%88%B7%E6%9C%BA%E5%8F%91%E9%80%81%E5%9B%BE%E7%89%87%E7%B1%BB%E5%9E%8B%E6%96%87%E4%BB%B6.png)
 
![图24 双机通信中8002端口客户机接收图片类型文件](https://github.com/AmyLi98/Cryptography/blob/master/images/8002%E7%AB%AF%E5%8F%A3%E5%AE%A2%E6%88%B7%E6%9C%BA%E6%8E%A5%E6%94%B6%E5%9B%BE%E7%89%87%E7%B1%BB%E5%9E%8B%E6%96%87%E4%BB%B6.png)
 
 
4. 在8001端口的客户机页面处点击“选择文件”按钮，选择任一其他类型的文件，如docx文件进行上传，可以发现，发送端加密二进制文件后发送给接收端，接收端解密发送来的文件信息后，并将文件及其链接显示出来，用户可以在网页查看文件内容，也可以下载到本地
 
![图25 双机通信中8002端口客户机接收到.docx文件](https://github.com/AmyLi98/Cryptography/blob/master/images/8002%E7%AB%AF%E5%8F%A3%E5%AE%A2%E6%88%B7%E6%9C%BA%E6%8E%A5%E6%94%B6%E5%88%B0.docx%E6%96%87%E4%BB%B6.png)
 
![图26 点击文件后下载文件](https://github.com/AmyLi98/Cryptography/blob/master/images/%E7%82%B9%E5%87%BB%E6%96%87%E4%BB%B6%E5%90%8E%E4%B8%8B%E8%BD%BD%E6%96%87%E4%BB%B6.png)
 
![图27 下载传送过来的文件到本地后可以正常打开查看编辑](https://github.com/AmyLi98/Cryptography/blob/master/images/%E4%B8%8B%E8%BD%BD%E6%96%87%E4%BB%B6.png)


#### （6）about_us.html ——关于我们的团队介绍页
1. 主界面
 
![图28 about_us主界面](https://github.com/AmyLi98/Cryptography/blob/master/images/about_us%E4%B8%BB%E7%95%8C%E9%9D%A2.png)
 
 
2. 点击个人介绍名片，通过动画特效，可以展开显示团队所有成员的信息
 
![图29 团队成员信息展示界面](https://github.com/AmyLi98/Cryptography/blob/master/images/%E5%9B%A2%E9%98%9F%E6%88%90%E5%91%98%E4%BF%A1%E6%81%AF%E5%B1%95%E7%A4%BA%E7%95%8C%E9%9D%A2.png)

