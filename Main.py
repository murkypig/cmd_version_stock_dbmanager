import sqlite3
import sys
import prettytable as pt
import pandas as pd
import xlsxwriter
import datetime
import DBmanager



now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print(type(now.encode('UTF-8')))
print(type(eval(str("1234.xlsx".encode('UTF-8')))))

dbase = sqlite3.connect('Data.db')
cursor = dbase.cursor()


dbase.execute('''CREATE TABLE IF NOT EXISTS Stock_records(
	ID INT AUTO_INCREMENT PRIMARY KEY ,
	inventory_id TEXT NOT NULL,
	Stock_ship_num INT NOT NULL,
	date_time TEXT NOT NULL)''')
def insert_record(inventory_id,Stock_ship_num,date_time):
	dbase.execute('''INSERT INTO Stock_records(inventory_id,Stock_ship_num,date_time)
		VALUES(?,?,?)''',(inventory_id,Stock_ship_num,date_time))
	dbase.commit()



def export_Data():
	data = cursor.execute(''' SELECT * FROM Stock_records ''')
	dict = {}
	index = []
	col_1 =[]
	col_2 =[]
	col_3 =[]
	i = 1
	for record in data:
		#row = [str(record[1]),str(record[2]),str(record[3])]
		index.append(record[0])
		col_1.append(record[1])
		col_2.append(record[2])
		col_3.append(record[3])
		df4 = pd.DataFrame({'inventory_id':col_1,'Stock_ship_num':col_2,'date_time':col_3},index=index)
		#tb.add_row(row)
	#print(df4)
	#data_name = str('Data'+ datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+'.xlsx')
	data_name = str("Data").encode('UTF-8')+str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")).encode('UTF-8')+str("xlsx").encode('UTF-8')
#----------------
#problem
	##datatoexcel = pd.ExcelWriter(data_name,engine = 'xlsxwriter')
	datatoexcel = pd.ExcelWriter("abcd.xlsx",engine = 'xlsxwriter')
	df4.to_excel(datatoexcel, sheet_name = 'Sheet1')

	datatoexcel.save()


def read_Data():
	data = cursor.execute(''' SELECT * FROM Stock_records ''')
	tb = pt.PrettyTable()
	tb.field_names = (["inventory_id","Stock_ship_num","date_time"])

	
	tb.align["inventory_id"] = "l"
	tb.padding_width = 1
	
	for record in data:
		row = [str(record[1]),str(record[2]),str(record[3])]
		tb.add_row(row)
	print(tb)
#read_Data()



def check_Data(inventory_id):
		#from math import *
	data = cursor.execute(''' SELECT * FROM Stock_records WHERE inventory_id =	inventory_id''')
	#dbase.commit()
	#print(data)
	record_inv = 0
	for record in data:
		#print ('ID : '+str(record[0]))
		if record[1]==inventory_id:
			record_inv =  record_inv + int(record[2])
		#print ('inventory_id : '+str(record[1]))
		#print ('Stock_ship_num : '+str(record[2]))
		#print ('date_time : '+str(record[3])+'\n')
	#print(record_inv)
	return record_inv

print(' 1. 輸入庫存'+'\n','2. 提取庫存'+'\n','3. 查看當前存貨'+'\n', '4. 匯出 excel'+'\n', '5. 離開系統')


key = 1

while key:
	fun_sel = input("選擇功能:")
	while (fun_sel):
		if fun_sel == "1":
			inventory_id = input('物品ID:')
			stock_ship_num = int(input('輸入庫存:'))
			date_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
			insert_record(inventory_id,stock_ship_num,date_time)
			print('輸入完畢')
			break
		if fun_sel == "2":
			inventory_id = input('物品ID:')
			stock_ship_num = int(input('提取庫存:'))
			if check_Data(inventory_id) >= stock_ship_num:
				date_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
				stock_ship_num = 0 -  stock_ship_num
				insert_record(inventory_id,stock_ship_num,date_time)
				print('提取完畢')
				break
			else:
				print("庫存不足抱歉")
				break
		if fun_sel == "3":
			#inventory_id = input('物品ID:')
			check_stock = input("是否要看存貨資料:[y/n]")
			if check_stock=="y" or check_stock == "Y":
				read_Data()
				break
			else:
				break

		if fun_sel == "4":
			#inventory_id = input('物品ID:')
			export_stock = input("是否要匯出存貨資料:[y/n]")
			if export_stock=="y" or export_stock == "Y":
				export_Data()
				break
			else:
				break
		if fun_sel == "5":
			print('離開系統')
			sys.exit(0)
		else:
			print('輸入錯誤，請重新輸入')
			break