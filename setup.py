from setuptools import setup
from setuptools import find_packages

install_requires = [
    "petl==1.7.10",
    "PyMySQL==1.0.2",
    "pyodbc==4.0.34",
    "selenium==4.3.0",
]

setup(
    name="ETL Pipeline for DragonPay",
    version="1.0",
    description="A simple ETL pipeline that is used to extract information from DragonPay vendor website.",
    author="John Paul Del Mundo",
    author_email="jpdelmundo223@gmail.com",
    maintainer="John Paul Del Mundo",
    packages=find_packages(include=['csv', 'chromedriver']),
    url="https://github.com/jpdelmundo223/dpay-orders-etl",
    install_requires=install_requires,
    keywords=["etl", "dragonpay"]
)