import mysql.connector
import inquirer
#from texttable import Texttable
from tabulate import tabulate
from os import system, name
import bcrypt
import logging

logging.basicConfig(filename='employee.log', level=logging.DEBUG)

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
    logging.debug('Display Results')
    if not isinstance(tuples, list):
        tuple_list = []
        tuple_list.append(tuples)
        tuples = tuple_list
    print('\n' + tabulate(tuples, headers=attr_list, tablefmt='fancy_grid') +'\n' )


# Returns column names of a table
def retrieve_column_names(table):
    logging.debug('Retrieve column names')
    sql     = "DESC {}".format(table)
    columns = []
    cursor.execute(sql)
    result = cursor.fetchall()
    for attr in result:
        columns.append(attr[0])
    return columns


def retrieve_key_from(table):
    logging.debug('Retrieve key from table')
    sql = "SHOW KEYS FROM {} WHERE Key_name = 'PRIMARY'".format(table)
    cursor.execute(sql)
    result = cursor.fetchall()
    return(result[0][4])

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ---------------------------------------- INSERT -----------------------------------------------

def insert_into_table(table, attributes, values):
    logging.debug('Insert into table')
    attr = ", ".join(attributes)
    s    = []
    for _ in values:
        s.append('%s')
    s = ", ".join(s)
    sql = "INSERT INTO {}({}) VALUES({})".format(table, attr, s)
    cursor.execute(sql, values)
    mydb.commit()


def insert_coupon(values):
    sql = "INSERT INTO coupon(exp_date, discount, branch) VALUES (%s, %s, %s)"
    cursor.execute(sql, values)
    mydb.commit()


def insert_employee(values):
    sql = "INSERT INTO employee(e_name, e_addr, e_phone, e_pw) VALUES (%s, %s, %s, %s)"
    cursor.execute(sql, values)
    mydb.commit()


def insert_design(values):
    sql = "INSERT INTO design(d_size, d_font, d_text, d_price) VALUES (%s, %s, %s, %s)"
    cursor.execute(sql, values)
    mydb.commit()


def insert_item(values):
    sql = "INSERT INTO item(i_type, count, i_price, branch) VALUES (%s, %s, %s, %s)"
    cursor.execute(sql, values)
    mydb.commit()


def insert_customer(values):
    sql = "INSERT INTO customer(c_name, c_addr, c_phone) VALUES (%s, %s, %s)"
    cursor.execute(sql, values)
    mydb.commit()


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ---------------------------------------- UPDATE -----------------------------------------------


def update_row_values(table, set_values, row_id):
    logging.debug('Update row values')
    pri_key = retrieve_key_from(table)
    sql     = 'UPDATE {}'.format(table)
    sql    += create_sql_clause('SET', set_values)
    sql    += create_sql_clause('WHERE', [(pri_key, row_id)])
    print(sql)
    cursor.execute(sql)
    mydb.commit()


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ---------------------------------------- DELETE -----------------------------------------------


def delete_rows(table, where_condition):
    logging.debug('Delete rows')
    where = create_sql_clause('WHERE', where_condition)
    sql = "DELETE FROM {} {}".format(table, where)
    print(sql)
    cursor.execute(sql)
    mydb.commit()


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ---------------------------------------- SELECT -----------------------------------------------

def select_row_from(table, row_id):
    logging.debug('Select row')
    pri_key   = retrieve_key_from(table)
    col_names = retrieve_column_names(table)
    sql       = "SELECT * FROM {} WHERE {} = %s".format(table, pri_key)
    cursor.execute(sql, (row_id,))
    return (cursor.fetchone(), col_names)


def select_table(table):
    logging.debug('Select table')
    col_names = retrieve_column_names(table)
    sql       = "SELECT * from {}".format(table)
    cursor.execute(sql)
    return (cursor.fetchall(), col_names)


def select_table_where(table, condition):
    logging.debug('Select table with condition')
    col_names = retrieve_column_names(table)
    sql       = "SELECT * from {} WHERE {}".format(table, condition)
    cursor.execute(sql)
    return (cursor.fetchall(), col_names)


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ---------------------------------------- OTHER -----------------------------------------------


def verify_emp_login(emp_id, pw):
    logging.warning('Verifying employee login')
    emp = select_row_from('employee', emp_id)
    if not emp[0]:
        return (False, 'NO RECORD OF EMPLOYEE')
    elif not bcrypt.checkpw(pw.encode('utf8'), emp[0][4].encode('utf-8')):
        return (False, 'INVALID PASSWORD')
    else:
        return (True, None)


def is_manager(emp_id):
    logging.warning('Verifying manager')
    sql = "SELECT sup_id FROM employee WHERE e_id = %s"
    cursor.execute(sql, (emp_id,))
    result = cursor.fetchone()
    if not result[0]:
        return True
    return False


def sort_inventory(filter):
    logging.debug('Sorting inventory')
    if not filter:
        sql  = "SELECT * FROM item"
    else:
        attr = ", ".join(filter)
        sql  = "SELECT * FROM item ORDER BY {}".format(attr)
    cols   = retrieve_column_names('item')


def filter_search(table, where, order_by):
    logging.debug('Filter search')
    sql = 'SELECT * FROM {}'.format(table)
    if where:
        sql += create_sql_clause('WHERE', where)
    if order_by:
        sql += ' ORDER BY {}'.format(', '.join(order_by))
    cols = retrieve_column_names(table)
    cursor.execute(sql)
    return (cursor.fetchall(), cols)


def create_sql_clause(clause_name, vars_and_vals):
    logging.debug('Creating SQL clause')
    my_list   = []
    clause = ''
    v_and_v = []
    v_temp = vars_and_vals
    if not type(v_temp) is list:
        v_temp = v_and_v
        v_and_v.append(vars_and_vals)
    for pair in v_temp:
        if isinstance(pair[1], str):
            my_list.append("{} = \'{}\'".format(pair[0], pair[1]))
        else:
            my_list.append("{} = {}".format(pair[0], pair[1]))
        clause += ' {} {}'.format(clause_name, ", ".join(my_list))
    return clause


def get_max(table, value):
    logging.debug('Getting maximum value')
    sql = "SELECT MAX({}) FROM {}".format(value, table)
    cursor.execute(sql)
    return cursor.fetchall()