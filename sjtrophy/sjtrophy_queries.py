import mysql.connector
import inquirer
from os import system, name

mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    passwd='flaket44',
    database='sjtrophy'
)

cursor = mydb.cursor()




# INSERTING OBJECTS

def insert_branch():
def insert_coupon():
def insert_employee():
def insert_design():
def insert_item();
def insert_customer(name, addr, num):
def insert_customer_order(count, item, design, cid, eid):
    # derive total cost
    sql_query = "INSERT INTO customer_order()"
    cursor.execute(sql_query, id)

def insert_review():
def insert_item_request():
def insert_coupon_offer():


# RETRIEVING DATA

def get_branch_mgr():
def get_mgr_branch():

def get_item_price():
def get_item_type():
def get_item_count():
def get_item():

def get_design_size():
def get_design_font():
def get_design_text():
def get_design_price():
def get_design():


def search_customer_by_name(name):
    sql_query = "SELECT * FROM customer WHERE c_name = %s"
    cursor.execute(sql_query, name)
    results = cursor.fetchmany(size=10)
    return results

def search_customer_by_id(id):
    sql_query = "SELECT * FROM customer WHERE c_id = %s"
    cursor.execute(sql_query, id)
    results = cursor.fetchmany(size=10)
    return results
