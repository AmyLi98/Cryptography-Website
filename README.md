# Cryptography
CryptographyExperimentCourse3 of Northeastern University
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
