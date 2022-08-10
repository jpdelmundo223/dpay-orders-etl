# ETL Pipeline for DragonPay

## **Description**

An _ETL_ Pipeline created using Python and Selenium to automated the downloading of sales/transactions data (in .csv format) from their website [DragonPay](https://gw.dragonpay.ph/AdminWeb/LoginPage.aspx).

I used [_petl_](https://petl.readthedocs.io/en/stable/), a general purpose Python package for extracting, transforming and loading tables of data, for most of the tasks that involves transformations and loading of data from one place to another.

## **Purpose**

The purpose of this project is to automate the daily extraction, transformation, and loading of data that is coming from the vendors website, which helps to reduce time, effort, reducing manual errors, and giving you more time to focus with other things or tasks.

## **Technologies i used**

- Python 3.10
- Selenium 4.3.0
- MySQL
- SQL Server 2008 R2
- VS Code

## **Clone to your local**

```bash
> mkdir dragonpay_etl
> cd dragonpay_etl
> git clone https://github.com/jpdelmundo223/dpay-orders-etl.git
```

## **Enabling your virtual environment**

```bash
> cd dpay-orders-etl
> venv\Scripts\activate
```

## **Install requirements**

```python
> pip install requirements.txt
```
