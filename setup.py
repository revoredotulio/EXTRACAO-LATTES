from setuptools import setup, find_packages

setup(
    name='imip_lattes',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'numpy',
        'jupyter',
        'requests'
    ],
    author='Seu Nome',
    author_email='seuemail@example.com',
    description='Projeto de Extração de Informações do Currículo Lattes',
    url='https://github.com/revoredotulio/IMIP-LATTES',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
