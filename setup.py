from setuptools import setup

setup(
    name='QR Code Generator Y7X',
    version='1.0',
    description='A stylish and customizable QR Code Generator & Reader',
    author='Yugank (Y7X)',
    install_requires=[
        'customtkinter',
        'qrcode',
        'pillow',
        'opencv-python',
        'numpy',
        'pyperclip'
    ],
    python_requires='>=3.9',
)
