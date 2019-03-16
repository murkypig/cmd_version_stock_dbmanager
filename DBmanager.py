import sqlite3
import sys
import prettytable as pt
import pandas as pd
import xlsxwriter
import datetime




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