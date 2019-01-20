# Cryptography Website

Information Security Experiment Course 3 of Northeastern University

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

Cryptography Website系统由四个模块构成：
**Home(主页)、Description(简介)、Cryptography Tool(密码学工具)、About Us(关于我们)。**

其中，Cryptography Tool部分是网站的核心部分，主要实现单机加解密和双机加解密实践的功能。

### Cryptography Website前端与后端交互的设计图

python后端我们编写的密码学算法库将为单机加解密和双机加解密提供依赖，双机加解密的socket服务端将通过websocket接口每隔一段时间向web端发送HTTP请求，web端也每隔一段时间向socket服务端发送HTTP请求，由此两者建立链接，消息将每个很短一段时间从前端不断向后端发送，后端处理后的数据也不断向前端发送，使前端实时显示最新的数据，从而实现前端与后端的交互。

### 单机加解密和双机加解密功能的网页和系统设计
#### （1）Single Machine ——单机加解密
实现单机加解密功能的网页single_tool.html将Caesar、Keyword Cipher、Vigenere Cipher、Text-autokey Cipher、Playfair Cipher、Column Permutation Cipher、Double-Transposition Cipher、RC4、DES、RSA、MD5等11种密码和DH密钥交换集成在同一界面中，使用标签的方法实现不同加密算法之间的切换。

Encryption和Decryption均在页面显示，用户根据需要的不同进行不同的操作。页面的JavaScript代码应实现在用户点击Encrypt和Decrypt按钮时，监听文本输入框的变化并将发送载有更新的文本输入框内容的HTTP请求，后台socket实时监听并获取HTTP请求用来更新加解密算法的传入参数为文本输入框的内容。

在click事件监听器中，我采用的是XMLHttpRequest(XHR)，XHR是一个API对象，其中的方法可以用来在浏览器和服务器端传输数据，这个对象是浏览器的JavaScript环境提供的。从XHR获取数据的目的是为了持续修改一个加载过的页面。

#### （2）Dual machine encryption and decryption ——双机加解密

实现双机加解密的网页double_cipher.html将通过某一用户输入的ip地址和端口号在两个用户之间建立连接，实现双机加解密，即一方加密后的密文除了在本地显示，同时在对方的解密端的密文框内显示，此时若对方已知正确的解密密钥，将实现原文的破译。

双机加解密的过程中需要实现每隔 300ms 调用一次监控待加密消息处的函数，以便实时进行加解密操作以及破译端实时获取加密端加密后的密文。

#### （3）Double machine communication ——双机通信

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



