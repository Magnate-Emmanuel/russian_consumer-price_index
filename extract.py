import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('seaborn-whitegrid')

def extract_data():
    connection = sqlite3.connect('Prices.db')
    cursor = connection.cursor()
    extract_table = '''SELECT Product_name,
    Index_2010 - 100 AS I2010, Index_2011 - 100 AS I2011, Index_2012 - 100 AS I2012,
    Index_2013 - 100 AS I2013, Index_2014 - 100 AS I2014, Index_2015 - 100 AS I2015,
    Index_2016 - 100 AS I2016, Index_2017 - 100 AS I2017, Index_2018 - 100 AS I2018,
    Index_2019 - 100 AS I2019, Index_2020 - 100 AS I2020, Index_2021 - 100 AS I2021
    FROM Prices
    WHERE Product_name IN
    (SELECT Product_name FROM Prices
    WHERE LENGTH(Product_code) = 8)
    AND I2010 IS NOT -100
    AND I2021 IS NOT -100;'''
    result_table = cursor.execute(extract_table)
    rows = result_table.fetchall()
    connection.commit()
    connection.close()
    df = pd.DataFrame(rows)

    return df


df = extract_data()

#print(df.loc[:,1:13])
year = range(2010, 2022)
for i in range(0, 4):
    s = list(df.loc[i, 1:13]) #присвоение наименований продукта
    plt.title(df[0][i])
    plt.xlabel('Год', fontsize=12)
    plt.ylabel('Прирост цены в %', fontsize=12)
    plt.plot(year, s)
    plt.savefig(str(df[0][i])+'.pdf')
    plt.clf()

print("INFO: Go to file directory to view reports")