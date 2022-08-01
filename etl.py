import petl as etl
import os
import pymysql
import pyodbc
import configparser
import time
from datetime import datetime

t = time.time()

# Read from config.ini
config = configparser.ConfigParser()
config.read('config.cfg')

# Get values from config.ini
csv_path = config.get('csv', 'file_path', fallback=r'C:\Users\john.delmundo\Desktop\dragonpay_orders\csv')

mysql_host = config.get('mysql', 'host')
mysql_user = config.get('mysql', 'user')
mysql_password = config.get('mysql', 'password')
mysql_db = config.get('mysql', 'database')
mysql_port = config.get('mysql', 'port')

mssql_driver = config.get('mssql', 'driver')
mssql_server = config.get('mssql', 'host')
mssql_user = config.get('mssql', 'user')
mssql_password = config.get('mssql', 'password')
mssql_db = config.get('mssql', 'database')

def row_count(table: etl.Table) -> int:
    """Returns the number of rows on a table"""
    return len(etl.dicts(table))

def start_etl() -> None:
    mssql_conn = pyodbc.connect('DRIVER={};SERVER={};DATABASE={};UID={};PWD={}'.format(mssql_driver, mssql_server, mssql_db, mssql_user, mssql_password))
    mssql_cursor = mssql_conn.cursor()
    create_table = """CREATE TABLE dbo.DragonPayPaidOrders (
                                RefDate DATETIME,
                                RefNo NVARCHAR(20),
                                MerchantId VARCHAR(20),
                                TxnId INT,
                                CCY VARCHAR(10),
                                Amount NVARCHAR(20),
                                Status VARCHAR(1),
                                Description NVARCHAR(20),
                                ProcId VARCHAR(10),
                                SettleDate DATETIME
                            )"""
    os.system('cls')
    print(f"[{datetime.now()}] Connecting to SQL Server " + '.' * 3 + ' done')

    print(f"[{datetime.now()}] Creating table 'dbo.DragonPayPaidOrders' if not exists " + '.' * 3 + ' done')


    try:
        mssql_cursor.execute(create_table)
        mssql_cursor.commit()
        print(f"[{datetime.now()}] Table 'dbo.DragonPayPaidOrders' successfully created " + '.' * 3)
    except:
        print(f"[{datetime.now()}] Table 'dbo.DragonPayPaidOrders' already exists " + '.' * 3)
        

    mssql_table = etl.fromdb(mssql_conn, query="select * from dbo.DragonPayPaidOrders")

    if not len(os.listdir(os.path.basename(csv_path))) == 0:
        for _ in os.listdir(os.path.basename(csv_path)):
            csv_table = etl.fromcsv(os.path.join(os.path.dirname(__file__), os.path.basename(csv_path), _))
            
            csv_table = etl.convert(csv_table, "TxnId", int)
            csv_table = etl.rename(csv_table, "Merchant", "MerchantId")
            csv_table = etl.rename(csv_table, "Proc", "ProcId")
            
            csv_table = etl.split(csv_table, "Amount", ",", ["Amount", "SplittedValue"])
            csv_table = etl.addfield(csv_table, "NewAmount", lambda col: col["Amount"] + col["SplittedValue"] if (col["SplittedValue"] != None) else col["Amount"])      

            new_csv_table = etl.cut(csv_table, "RefDate", "RefNo", "MerchantId", "TxnId", "CCY", "NewAmount", "Status", "Description", "ProcId", "SettleDate")
            
            new_csv_table = etl.rename(new_csv_table, "NewAmount", "Amount")
            new_csv_table = etl.convert(new_csv_table, "Amount", float)

            table = etl.antijoin(new_csv_table, mssql_table, key="TxnId")

            try:
                row = row_count(table)
                etl.appenddb(table, mssql_conn, 'DragonPayPaidOrders')
                print("[{dt}] Inserting {row_count} rows from '{filename}' to table '{table_name}' {periods} done".format(dt=datetime.now(), row_count=row, filename=_, periods='.' * 3, table_name='dbo.DragonPayPaidOrders'))
                # time.sleep(0.5)
            except Exception as e:
                print(e)

        elapsed = time.time() - t
        print(f"[{datetime.now()}] Time elapsed: {round(elapsed, 3)} seconds...")
    else:
        print("No files to read...")

    print()

    time.sleep(1)

    t2 = time.time()

    mysql_conn = pymysql.connect(host=mysql_host, user=mysql_user, password=mysql_password, database=mysql_db, port=int(mysql_port))

    create_table = """CREATE TABLE `dragon_pay_data` (
                        `Refdate` timestamp NULL DEFAULT NULL,
                        `Refno` varchar(255) NOT NULL,
                        `MerchantId` varchar(255) DEFAULT NULL,
                        `TxnId` double NOT NULL,
                        `Ccy` varchar(255) DEFAULT NULL,
                        `Amount` double DEFAULT NULL,
                        `Status` varchar(255) DEFAULT NULL,
                        `Description` varchar(255) DEFAULT NULL,
                        `ProcId` varchar(255) DEFAULT NULL,
                        `SettleDate` timestamp NULL DEFAULT NULL,
                        PRIMARY KEY (`Refno`,`TxnId`)
                        ) ENGINE=InnoDB DEFAULT CHARSET=utf8"""
                
    mysql_cursor = mysql_conn.cursor()

    try:
        print(f"[{datetime.now()}] Connecting to MySQL " + '.' * 3 + ' done')
        
        print(f"[{datetime.now()}] Creating table 'dragon_pay_data' if not exists " + '.' * 3 + ' done')
        mysql_cursor.execute(create_table)
        
        print(f"[{datetime.now()}] Table 'dragon_pay_data' created successfully " + '.' * 3)
        
    except:
        print(f"[{datetime.now()}] Table 'dragon_pay_data' already exists " + '.' * 3)
        

    mysql_table = etl.fromdb(mysql_conn, query="select * from dragon_pay_data;")

    mysql_conn.cursor().execute('SET SQL_MODE=ANSI_QUOTES')
    mysql_conn.cursor().execute('SET SQL_NOTES=0')

    if not len(os.listdir(os.path.basename(csv_path))) == 0:
        for _ in os.listdir(os.path.basename(csv_path)):
            csv_table = etl.fromcsv(os.path.join(os.path.dirname(__file__), os.path.basename(csv_path), _))
            
            csv_table = etl.convert(csv_table, "TxnId", float)
            csv_table = etl.rename(csv_table, "Merchant", "MerchantId")
            csv_table = etl.rename(csv_table, "Proc", "ProcId")
            
            csv_table = etl.split(csv_table, "Amount", ",", ["Amount", "SplittedValue"])
            csv_table = etl.addfield(csv_table, "NewAmount", lambda col: col["Amount"] + col["SplittedValue"] if (col["SplittedValue"] != None) else col["Amount"])      

            new_csv_table = etl.cut(csv_table, "RefDate", "RefNo", "MerchantId", "TxnId", "CCY", "NewAmount", "Status", "Description", "ProcId", "SettleDate")
            
            new_csv_table = etl.rename(new_csv_table, "NewAmount", "Amount")
            new_csv_table = etl.convert(new_csv_table, "Amount", float)

            table = etl.antijoin(new_csv_table, mysql_table, key="TxnId")

            table = etl.sub(table, "RefDate", " am", "")
            table = etl.sub(table, "RefDate", " pm", "")
            table = etl.convert(table, "RefDate", str)

            table = etl.sub(table, "SettleDate", " am", "")
            table = etl.sub(table, "SettleDate", " pm", "")
            table = etl.convert(table, "SettleDate", str)

            format = '%m/%d/%y %H:%M'

            table = etl.convert(table, ("RefDate", "SettleDate"), lambda d: datetime.strptime(d, format))

            # # print(etl.look(table))
            try:
                row = row_count(table)
                if row > 0:
                    etl.appenddb(table, mysql_conn, 'dragon_pay_data')
                    print("[{dt}] Inserting {row_count} rows from '{filename}' to table '{table_name}' {periods} done".format(dt=datetime.now(), row_count=row, filename=_, periods='.' * 3, table_name='dragon_pay_data'))
                    # time.sleep(0.5)
                else:
                    print("[{dt}] Inserting {row_count} rows from '{filename}' to table '{table_name}' {periods} done".format(dt=datetime.now(), row_count=row, filename=_, periods='.' * 3, table_name='dragon_pay_data'))
            except Exception as e:
                print(e)

        elapsed = time.time() - t2
        print(f"[{datetime.now()}] Time elapsed {round(elapsed, 3)} seconds...")
    else:
        print("No files to read...")

# query = "select * from dragon_pay_data"

# table = etl.fromdb(mysql_conn, query)
# table = etl.convert(table, "TxnId", int)
# table2 = etl.fromcsv(''.join([csv_path, '\\txnlist021722.csv']))
# table2 = etl.convert(table2, "TxnId", int)

# print(etl.look(table))
# print(etl.lookall(table2))

# print(etl.lookall(etl.antijoin(table2, table, key="TxnId")))

# table = etl.fromcsv(r'C:\Users\john.delmundo\Downloads\CNEBOOKSHOP-010122-072522-0726153542.csv')

# print(table)

# table = etl.fromcsv(r'C:\Users\john.delmundo\Downloads\CNEBOOKSHOP-010122-072522-0726153542.csv')

# table = etl.cut(table, "Refdate", "Refno", "MerchantId", "TxnId", "Ccy", "Amount", "Status", "Description", "ProcId", "SettleDate")
# etl.todb(table, mssql_conn, 'DragonPayPaidOrders')