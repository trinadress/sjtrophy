import csv
import mysql.connector


mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="flaket44",
    database="sjtrophy"
)

cursor = mydb.cursor()

# # -----------------------------------------EMPLOYEE DATA-------------------------------------------------------------
csv_data = csv.reader(open('employee.csv', 'r'))
sql_script = "INSERT INTO employee(e_name, e_addr, e_num) VALUES (%s, %s, %s)"
for row in csv_data:
    cursor.execute(sql_script, row)

# -----------------------------------------BRANCH DATA---------------------------------------------------------------
sql_script = "INSERT INTO branch(mgr_id) VALUES (%s)"
for branch in range(10):
    id = (branch + 100,)
    cursor.execute(sql_script, id)
#
# # -----------------------------------------COUPON DATA---------------------------------------------------------------
# csv_data = csv.reader(open('coupon.csv', 'r'))
# sql_script = "INSERT INTO coupon(exp_date, discount, branch) VALUES (%s, %s, %s)"
# for row in csv_data:
#     cursor.execute(sql_script, row)
#
# # -----------------------------------------DESIGN DATA---------------------------------------------------------------
# csv_data = csv.reader(open('design.csv', 'r'))
# sql_script = "INSERT INTO design(d_size, d_font, d_text, d_price) VALUES (%s, %s, %s, %s)"
# for row in csv_data:
#     cursor.execute(sql_script, row)
#
# # -----------------------------------------ITEM DATA-----------------------------------------------------------------
# csv_data = csv.reader(open('item.csv', 'r'))
# sql_script = "INSERT INTO item(i_type, count, i_price) VALUES (%s, %s, %s)"
# for row in csv_data:
#     cursor.execute(sql_script, row)
#
# # -----------------------------------------CUSTOMER DATA-------------------------------------------------------------
# csv_data = csv.reader(open('customer.csv', 'r'))
# sql_script = "INSERT INTO customer(c_name, c_addr, c_num) VALUES (%s, %s, %s)"
# for row in csv_data:
#     cursor.execute(sql_script, row)
#
# # -----------------------------------------CUSTOMER ORDER DATA-------------------------------------------------------
# csv_data = csv.reader(open('customer_order.csv', 'r'))
# sql_script = "INSERT INTO customer_order(count, o_status, total_cost) VALUES (%s, %s, %s)"
# for row in csv_data:
#     cursor.execute(sql_script, row)
#
# # -------------------------------------------------------------------------------------------------------------------
# # -------------------------------------------FOREIGN KEYS------------------------------------------------------------
#
# sql_script = "UPDATE employee INNER JOIN branch on employee.e_id = branch.mgr_id SET branch = branch.b_id"
# cursor.execute(sql_script)
#
# sql_script = "UPDATE employee CROSS JOIN branch SET employee.branch = e_id % 10 + 1, employee.sup_id = branch.mgr_id " \
#              "WHERE branch.b_id = e_id % 10 + 1 AND employee.e_id != branch.mgr_id"
# cursor.execute(sql_script)
#
# sql_script = "UPDATE coupon CROSS JOIN branch SET coupon.branch = 20*RAND() % 10 + 1"
# cursor.execute(sql_script)

mydb.commit()
cursor.close()
print("done")
