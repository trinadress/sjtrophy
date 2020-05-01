import employee
import csv
import random
import mysql.connector
import bcrypt



mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
    database="sjtrophy"
)

cursor = mydb.cursor()


# #-----------------------------------------EMPLOYEE DATA-------------------------------------------------------------
# csv_data = csv.reader(open('employee.csv'))
# sql_script = "INSERT INTO employee(e_name, e_addr, e_phone, e_pw) VALUES (%s, %s, %s, %s)"
# for row in csv_data:
#     row[3] = employee.encrypt_pw(row[3], employee.salt)
#     cursor.execute(sql_script, row)
#
# #-----------------------------------------BRANCH DATA---------------------------------------------------------------
# sql_script = "SELECT e_id FROM employee LIMIT 10"
# cursor.execute(sql_script)
# result = cursor.fetchall()
# sql_script = "INSERT INTO branch(mgr_id) VALUES (%s)"
# for eid in result:
#     cursor.execute(sql_script, eid)
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
# sql_script = "INSERT INTO item(i_type, count, i_price, branch) VALUES (%s, %s, %s, %s)"
# for row in csv_data:
#     cursor.execute(sql_script, row)
#
# # -----------------------------------------CUSTOMER DATA-------------------------------------------------------------
# csv_data = csv.reader(open('customer.csv', 'r'))
# sql_script = "INSERT INTO customer(c_name, c_addr, c_phone) VALUES (%s, %s, %s)"
# for row in csv_data:
#     cursor.execute(sql_script, row)
#
# # -----------------------------------------CUSTOMER ORDER DATA-------------------------------------------------------
# csv_data = csv.reader(open('customer_order.csv', 'r'))
# sql_script = "INSERT INTO customer_order(count, o_status, branch, total_cost) VALUES (%s, %s, %s, %s)"
# for row in csv_data:
#     cursor.execute(sql_script, row)
#
# for o in range(10000, 10099):
#     i = random.randint(1, 51)
#     d = random.randint(0, 50)
#     c = random.randint(1000, 1049)
#     l = random.randint(100, 149)
#     sql = "UPDATE customer_order SET item_id = {}, design_id = {}, " \
#           "customer = {}, last_ud_by = {} WHERE ord_num = {}".format(i, d, c, l, o)
#     cursor.execute(sql)
#
# #-------------------------------------------------------------------------------------------------------------------
# #-------------------------------------------FOREIGN KEYS------------------------------------------------------------
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
#
mydb.commit()
cursor.close()
print("done")
