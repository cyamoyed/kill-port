from setuptools import setup, find_packages

setup(
    name="kill-port",
    version="1.0.0",
    description="端口进程杀死工具 - 用于快速查找并杀死占用指定端口的进程",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="cyam",
    author_email="980713832@qq.com",
    url="https://github.com/cyamoyed/kill-port",
    packages=find_packages(),
    py_modules=["main", "cli", "gui"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS :: MacOS X",
    ],
    python_requires=">=3.7",
    install_requires=[
        "PyQt5>=5.15.0",
    ],
    entry_points={
        "console_scripts": [
            "kill-port=main:main",
        ],
    },
)
