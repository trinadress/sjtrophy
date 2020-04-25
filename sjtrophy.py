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

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ---------------------------------------- HELPER -----------------------------------------------

def display_results(tuples, attr_list):
    tuple_list = []
    if not isinstance(tuples, list):
        tuple_list.append(tuples)
    print('\n' + tabulate(tuple_list, headers=attr_list, tablefmt='fancy_grid') +'\n' )


# Returns column names of a table
def retrieve_column_names(table):
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

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ---------------------------------------- INSERT -----------------------------------------------

def insert_into_table(table, attributes, values):
    attr = ", ".join(attributes)
    val = ", ".join(values)
    sql = "INSERT INTO {}({}) VALUES({})".format(table, attr, val)
    cursor.execute(sql)

def insert_coupon(values):
    values = ", ".join(values)
    sql = "INSERT INTO coupon(exp_date, discount, branch) VALUES ({})".format(values)
    cursor.execute(sql)
    mydb.commit()


def insert_employee(values):
    values = ", ".join(values)
    sql = "INSERT INTO employee(e_name, e_addr, e_phone, e_pw) VALUES ({})".format(values)
    cursor.execute(sql)
    mydb.commit()


def insert_design(values):
    values = ", ".join(values)
    sql = "INSERT INTO design(d_size, d_font, d_text, d_price) VALUES ({})".format(values)
    cursor.execute(sql)
    mydb.commit()


def insert_item(values):
    #values = ", ".join(values)
    sql = "INSERT INTO item(i_type, count, i_price, branch) VALUES (%s, %s, %s, %s)"
    cursor.execute(sql, values)
    mydb.commit()


def insert_customer(values):
    values = ", ".join(values)
    sql = "INSERT INTO customer(c_name, c_addr, c_phone) VALUES ({})".format(values)
    cursor.execute(sql)
    mydb.commit()


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

def update_row_values(table, set_values, row_id):
    pri_key = retrieve_key_from(table)
    sql     = 'UPDATE {}'.format(table)
    sql    += create_sql_clause('SET', set_values)
    sql    += create_sql_clause('WHERE', [(pri_key, row_id)])
    cursor.execute(sql)
    mydb.commit()


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ---------------------------------------- DELETE -----------------------------------------------


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ---------------------------------------- SELECT -----------------------------------------------

def select_row_from(table, row_id):
    pri_key   = retrieve_key_from(table)
    col_names = retrieve_column_names(table)
    sql       = "SELECT * FROM {} WHERE {} = %s".format(table, pri_key)
    cursor.execute(sql, (row_id,))
    return (cursor.fetchone(), col_names)


def select_table(table):
    columns = retrieve_column_names(table)
    sql     = "SELECT * from {}".format(table)
    cursor.execute(sql)
    return cursor.fetchall()
    # test print
    # display_results(result, columns)


def select_table_where(table, condition):
    columns = retrieve_column_names(table)
    sql     = "SELECT * from {} WHERE {}".format(table, condition)
    cursor.execute(sql)
    return cursor.fetchall()


def select_customer_order_filter(status, filter):
    pri_key = retrieve_key_from('customer_order')
    columns = retrieve_column_names('customer_order')
    sql = "SELECT * FROM customer_order WHERE o_status = '{}' ORDER BY {}".format(status, filter)
    print(sql)
    cursor.execute(sql)
    results = cursor.fetchall()
    display_results(results, columns)



# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ---------------------------------------- OTHER -----------------------------------------------

def verify_emp_login(emp_id, pw):
    emp = select_row_from('employee', emp_id)
    if not emp:
        print("EMPLOYEE DOES NOT EXIST")
        return False
    elif emp[0][4] != pw:
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
        attr = ", ".join(filter)
        sql  = "SELECT * FROM item ORDER BY {}".format(attr)
    cols   = retrieve_column_names('item')


# def filter_search(table, where, *order_by):
#     sql = 'SELECT * FROM {}'.format(table)
#     if where:
#         where_list = []
#         for where_cond in where:
#             where_list.append("{} = {}".format(where_cond, where[where_cond]))
#             sql += ' WHERE {}'.format(", ".join(where_list))
#     if order_by:
#         sql += ' ORDER BY {}'.format(', '.join(order_by))
#     cols = retrieve_column_names(table)
#     print(sql)
#     cursor.execute(sql)
#     result = cursor.fetchall()
#
#     return (result, cols)

def filter_search(table, where, order_by):
    sql = 'SELECT * FROM {}'.format(table)
    if where:
        sql += create_sql_clause('WHERE', where)
    if order_by:
        sql += ' ORDER BY {}'.format(', '.join(order_by))
    cols   = retrieve_column_names(table)
    cursor.execute(sql)
    result = cursor.fetchall()
    return (result, cols)




#select_customer_order_filter('COMPLETE', 'count DESC, total_cost DESC')

#test
# select_row_from('employee', 101)
# select_table('employee')
#select_from_table('employee', 'e_id', 'e_name', 'e_addr', 'e_num', 'e_pw', 'branch', 'sup_id')

def create_sql_clause(clause_name, vars_and_vals):
    my_list   = []
    clause = ''
    v_and_v = []
    v_temp = vars_and_vals
    if not type(v_temp) is list:
        v_temp = v_and_v
        v_and_v.append(vars_and_vals)
    for pair in v_temp:
        my_list.append("{} = {}".format(pair[0], pair[1]))
        clause += ' {} {}'.format(clause_name, ", ".join(my_list))
    return clause

