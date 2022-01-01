# chromosome

# 1. 功能介绍

给朋友写的用于标注染色体中DNA位置的画图软件

![01-software](02-images/01-software.png)

![02-DNA](02-images/02-DNA.png)

# 2. 安装与使用

## 1. 直接使用

windows : 运行chromosome.exe

ubuntu: 

```bash
./dist/main
```

## 2. 编译使用

1. Dependencies：

   ```bash
   pip install -r requirements.txt
   ```

   opencv-python == 3.4.2.16
   pyqt5 == 5.15.6
   numpy == 1.19.5

   pyinstaller

2. Run

   ```python
   python chromosome.py
   ```

3. packing

   ```bash
   pyinstaller -F chromosome.py
   ```

   [pyinstaller教程](https://zhangguixin.top/2022/01/01/程序设计/pyinstaller使用/)



