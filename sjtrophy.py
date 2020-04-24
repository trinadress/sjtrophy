import mysql.connector
import inquirer
#from texttable import Texttable
from tabulate import tabulate
from os import system, name

mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    passwd='',
    database='sjtrophy'
)

cursor = mydb.cursor()

#-------------------------- HELPER ---------------------------------------------
# Input: A list of strings
def attr_list(attributes):
    attr_str = ""
    for index, attr in enumerate(attributes):
        attr_str += str(attr)
        if index != len(attributes)-1:
            attr_str += ", "
    return attr_str


# Formats and prints table results
# Input: List of tuples (rows of table results), string list of attributes
def display_results(tuple_list, attr_list):
    print('\n' + tabulate(tuple_list, headers=attr_list, tablefmt='fancy_grid') +'\n' )


# Returns column names of a table
def retrieve_columns_from(table):
    sql     = "DESC {}".format(table)
    columns = []
    cursor.execute(sql)
    result = cursor.fetchall()
    for attr in result:
        columns.append(attr[0])
    return columns


def retrieve_key_from(table):
    sql = "SHOW KEYS FROM {} WHERE Key_name = 'PRIMARY'".format(table)
    cursor.execute(sql)
    result = cursor.fetchall()
    return(result[0][4])

#test
#retrieve_key_from('employee')
#------------------------- INSERT ----------------------------------------------

# def insert_coupon():


# def insert_employee():


# def insert_design():


# def insert_item():


# def insert_customer(name, addr, num):


# def insert_customer_order(count, item, design, cid, eid):
#     # derive total cost
#     sql_query = "INSERT INTO customer_order()"
#     cursor.execute(sql_query, id)
#
# def insert_review():


# def insert_item_request():


# def insert_coupon_offer():


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ---------------------------------------- UPDATE -----------------------------------------------




# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ---------------------------------------- DELETE -----------------------------------------------


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ---------------------------------------- SELECT -----------------------------------------------

def select_row_from(table, row_id):
    pri_key = retrieve_key_from(table)
    columns = retrieve_columns_from(table)
    sql     = "SELECT * FROM {} WHERE {} = %s".format(table, pri_key)
    cursor.execute(sql, (row_id,))
    return cursor.fetchone()
    # test print
    # display_results(result, columns)


def select_table(table):
    columns = retrieve_columns_from(table)
    sql     = "SELECT * from {}".format(table)
    cursor.execute(sql)
    return cursor.fetchall()
    # test print
    # display_results(result, columns)


def select_table_where(table, condition):
    columns = retrieve_columns_from(table)
    sql     = "SELECT * from {} WHERE {}".format(table, condition)
    cursor.execute(sql)
    return cursor.fetchall()
    # test print



def select_customer_order_filter(status, filter):
    pri_key = retrieve_key_from('customer_order')
    columns = retrieve_columns_from('customer_order')
    sql = "SELECT * FROM customer_order WHERE o_status = '{}' ORDER BY {}".format(status, filter)
    print(sql)
    cursor.execute(sql)
    results = cursor.fetchall()
    display_results(results, columns)


def gen_sel(table, *filter, **conditions):
    sql = "SELECT * FROM {}".format(table)
    if conditions != None:
        list = []
        for key in conditions:
            list.append(" {} = {}".format(key, conditions[key]))
        sql += "WHERE {}".format(", ".join(list))
    if filter != None:
        list = attr_list(filter)
        sql += "ORDER BY {}".format(list)


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ---------------------------------------- OTHER -----------------------------------------------

def verify_emp_login(emp_id, pw):
    emp = select_row_from('employee', emp_id)
    if not emp:
        print("EMPLOYEE DOES NOT EXIST")
        return False
    elif emp[4] != pw:
        print("INCORRECT PASSWORD")
        return False
    else:
        return True


def is_manager(emp_id):
    sql = "SELECT sup_id FROM employee WHERE e_id = %s"
    cursor.execute(sql, (emp_id,))
    result = cursor.fetchone()
    if not result[0]:
        return True
    return False


def sort_inventory(filter):
    if not filter:
        sql  = "SELECT * FROM item"
    else:
        attr = attr_list(filter)
        sql  = "SELECT * FROM item ORDER BY {}".format(attr)
    cols   = retrieve_columns_from('item')
    cursor.execute(sql)
    result = cursor.fetchall()

    return (result, cols)

# def filter_search(table, where, order_by)
#     if not where:
#     if not order_by:


cond = {'branch': '7'}
order = {'name'}
# select_customer_order_filter('COMPLETE', 'count DESC, total_cost DESC')

#test
# select_row_from('employee', 101)
# select_table('employee')
#select_from_table('employee', 'e_id', 'e_name', 'e_addr', 'e_num', 'e_pw', 'branch', 'sup_id')


