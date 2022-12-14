from setuptools import setup, find_packages

__author__ = 'FRT Team'
setup(
    packages=find_packages(),
    install_requires=[
        'essentia==2.1b6.dev858',
        'numpy>=1.14.5',
        'matplotlib==3.6.2',
        'dtw==1.4.0',
        'pydub==0.25.1',
        'librosa==0.9.2',
        'llvmlite==0.39.1',
        'importlib-metadata==4.13.0',
        'numba==0.56.4',
        'urllib3==1.26.12',
        'chardet==3.0.4',
        'pytest==7.2.0'
    ]
)