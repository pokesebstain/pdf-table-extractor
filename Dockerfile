# 使用Windows Server Core基础镜像
FROM mcr.microsoft.com/windows/servercore:ltsc2019

# 安装Python
RUN powershell -Command \
    Invoke-WebRequest -Uri https://www.python.org/ftp/python/3.9.0/python-3.9.0-amd64.exe -OutFile python-3.9.0-amd64.exe ; \
    Start-Process python-3.9.0-amd64.exe -ArgumentList '/quiet InstallAllUsers=1 PrependPath=1' -Wait ; \
    Remove-Item python-3.9.0-amd64.exe

# 安装Java
RUN powershell -Command \
    Invoke-WebRequest -Uri https://download.oracle.com/java/17/latest/jdk-17_windows-x64_bin.exe -OutFile jdk-17.exe ; \
    Start-Process jdk-17.exe -ArgumentList '/s' -Wait ; \
    Remove-Item jdk-17.exe

# 设置工作目录
WORKDIR /app

# 复制应用文件
COPY . .

# 安装依赖
RUN pip install flask tabula-py pandas openpyxl pillow pystray pyinstaller

# 运行打包命令
CMD ["pyinstaller", "pdf_extractor.spec"] 