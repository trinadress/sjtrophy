import sjtrophy
import inquirer
import pyfiglet
from os import system, name
from textwrap import wrap
from tabulate import tabulate


# EMPLOYEE SIDE APPLICATION
def sign_in(msg):
    system('clear')
    display_sj_trophy()
    display_message('LOGIN')
    display_message(msg)

    questions = [
        inquirer.Text('user_id',  message="USER ID".rjust(19)),
        inquirer.Text('password', message="PASSWORD".rjust(19))
    ]
    answers  = inquirer.prompt(questions)
    user_id  = answers['user_id']
    password = answers['password']
    employee = sjtrophy.verify_emp_login(user_id, password)


    if not employee:
        sign_in('No record of employee')
    elif sjtrophy.is_manager(user_id):
        manager_main_menu(None, user_id)
    else:
        associate_main_menu(None, user_id)


def manager_main_menu(msg, emp_id):
    system('clear')
    display_sj_trophy()
    display_message('MANAGER MENU')
    display_message(msg)

    sel_op    = 11*' ' + 'SELECT OPTION'
    new_o     = 12*' ' + 'NEW ORDER'
    view_ao   = 12*' ' + 'VIEW ACTIVE ORDERS'
    view_po   = 12*' ' + 'VIEW PAST ORDERS'
    mng_inv   = 12*' ' + 'MANAGE INVENTORY'
    mng_emp   = 12*' ' + 'MANAGE EMPLOYEES'
    back      = 12*' ' + 'BACK'
    questions = [
        inquirer.List('option',
                       message= sel_op,
                       choices=[new_o, view_ao, view_po, mng_inv, mng_emp, back])
    ]
    answers = inquirer.prompt(questions)

    if answers['option']   == new_o:
        new_order(None, emp_id)
    elif answers['option'] == view_ao:
        view_orders(None, "ACTIVE")
    elif answers['option'] == view_po:
        view_orders(None, "COMPLETE")
    elif answers['option'] == mng_inv:
        inventory(None, emp_id)
    elif answers['option'] == mng_emp:
        manage_employees(None)
    else:
        sign_in(None)

def associate_main_menu(msg, emp_id):
    system('clear')
    display_sj_trophy()
    display_message('ASSOCIATE MENU')
    display_message(msg)

    sel_op    = 11*' ' + 'SELECT OPTION'
    new_o     = 12*' ' + 'NEW ORDER'
    view_ao   = 12*' ' + 'VIEW ACTIVE ORDERS'
    view_po   = 12*' ' + 'VIEW PAST ORDERS'
    view_inv  = 12*' ' + 'VIEW INVENTORY'
    back      = 12*' ' + 'BACK'
    questions = [
        inquirer.List('option',
                       message= sel_op,
                       choices=[new_o, view_ao, view_po, view_inv, back])
    ]
    answers = inquirer.prompt(questions)

    if answers['option']   == new_o:
        new_order(None, emp_id)
    elif answers['option'] == view_ao:
        view_orders(None, 'ACTIVE')
    elif answers['option'] == view_po:
        view_orders(None, 'COMPLETE')
    elif answers['option'] == view_inv:
        inventory(None, emp_id)
    else:
        sign_in(None)

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ------------------------------------- MENU OPTIONS --------------------------------------------

def new_order(msg, emp_id):
    system('clear')
    display_sj_trophy()
    display_message('NEW ORDER')
    display_message(msg)

    new_cust = 11*' ' + "NEW CUSTOMER?"
    questions = [inquirer.Confirm('new_customer', message=new_cust, default=True)]
    answers = inquirer.prompt(questions)
    # insert to database return eid (highest eid)

    if answers['new_customer']:
        new_customer(msg)
        # cid = new_customer()
    else:
        cid = search_customer()
        if None == cid:
            cid = new_customer()

    itm_id    = 11*' ' + "ENTER ITEM ID"
    dsg_id    = 11*' ' + "ENTER DESIGN ID"
    no_itms   = 11*' ' + "ENTER NUMBER OF ITEMS FOR ENGRAVING"
    cust_dsg  = 11*' ' + "CUSTOM DESIGN?"
    questions = [
        inquirer.Text('item_id',   message=itm_id),
        inquirer.Confirm('design', message=cust_dsg, default=False)
    ]
    answers = inquirer.prompt(questions)
    # if answers['design']:
    #     # insert new design
    questions = [
        inquirer.Text('design_id',message=dsg_id),
        inquirer.Text('count',    message=no_itms)
    ]
    answers = inquirer.prompt(questions)
    # get prices of item and design to derive total cost
    # insert into customer_order set count, status item, design, customer, last_ud_by, total_cost
    msg = 'ORDER COMPLETE'
    if sjtrophy.is_manager(emp_id):
        manager_main_menu(msg, emp_id)
    else:
        associate_main_menu(msg, emp_id)



def view_orders(msg, status):
    system('clear')
    display_sj_trophy()
    stat_cond = "o_status = '{}'".format(status)
    if "ACTIVE" == status:
        display_message('ACTIVE ORDERS')
    else:
        display_message('PAST ORDERS')
    result = sjtrophy.select_table_where('customer_order', stat_cond)
    col = sjtrophy.retrieve_columns_from('customer_order')
    sjtrophy.display_results(result, col)
    display_message(msg)


    srt     = 12*' ' + "SORT RESULTS"
    edt     = 12*' ' + "EDIT AN ORDER"

    questions = [inquirer.List('option',
                               message="SELECT AN OPTION",
                               choices=[srt, edt]
                               )
                 ]
    answers = inquirer.prompt(questions)
    filt_res    = 11*' ' + "FILTER RESULTS"
    new         = 12*' ' + "NEWEST"
    old         = 12*' ' + "OLDEST"
    cnt         = 12*' ' + "ORDER COUNT"
    cust        = 12*' ' + "CUSTOMER"
    if srt == answers['option']:
        questions = [
            inquirer.Checkbox('sort_options',
                              message=filt_res,
                              choices=[new, old, cnt, cust],
                              default=[new]),
        ]
        answers = inquirer.prompt(questions)
        order_by = []
        if new in answers['sort_options']:
            order_by.append("date_created DESC")
        if old in answers['sort_options'] and 'Newest' not in answers['sort_options']:
            order_by.append("date_created ASC")
        if cnt in answers['sort_options']:
            order_by.append("count DESC")
        if cust in answers['sort_options']:
            order_by.append("customer")
        ord_list = ", ".join(order_by)
        sjtrophy.select_customer_order_filter(status, ord_list)






def manage_inventory(msg):
    system('clear')
    display_sj_trophy()
    display_message('INVENTORY MANAGEMENT')
    display_message(msg)


def manage_employees(msg):
    system('clear')
    display_sj_trophy()
    display_message('EMPLOYEE MANAGMENT')
    display_message(msg)

    # select all employees from the same branch
    questions = [inquirer.List('option',
                               message="SELECT AN OPTION",
                               choices=['Add an Employee', 'Remove an Employee',
                                        'Transfer an Employee']
                               )
                 ]
    answers = inquirer.prompt(questions)
    if 'Add an Employee' == answers['option']:
        questions = [
            inquirer.Text('e_name',   message="NAME"),
            inquirer.Text('e_addr',   message="ADDRESS"),
            inquirer.Text('e_num',    message="PHONE NUMBER"),
            inquirer.Text('e_temp_pw',message="TEMPORARY PASSWORD")
        ]
        answers = inquirer.prompt(questions)
        # insert employee with name, address, phone, temp_password, mgr(current_eid) and branch(current_branch)
        print("Employee Added")

    elif 'Remove an Employee' == answers['option']:
        questions = [
            inquirer.Text('eid',
                          message="Enter ID of Employee to Remove")
        ]
        answers = inquirer.prompt(questions)
        # Remove employee with eid
        print("Employee Removed")

    elif 'Transfer an Employee' == answers['option']:
        questions = [
            inquirer.Text('eid',
                          message="Enter ID of Employee to Transfer"),
            inquirer.Text('bid',
                          message="Enter Transferring Branch ID")
        ]
        answers = inquirer.prompt(questions)
        # update employee with eid set branch = bid
        print("Employee Transferred")


def inventory(msg, emp_id):
    system('clear')
    display_sj_trophy()
    display_message('INVENTORY')
    display_message(msg)

    sel_op    = 11*' ' + 'SELECT OPTION'
    fltr      = 12*' ' + 'FILTER'
    edit_inv  = 12*' ' + 'EDIT INVENTORY'
    back      = 12*' ' + 'BACK'
    fltr_by   = 11*' ' + 'FILTER BY'
    type      = 10*' ' + 'TYPE'
    cnt       = 10*' ' + 'COUNT'
    prc       = 10*' ' + 'PRICE'

    if sjtrophy.is_manager(emp_id):
        questions = [inquirer.List('option', message=sel_op, choices=[fltr, edit_inv, back])]
    else:
        questions = [inquirer.List('option', message=sel_op, choices=[fltr, back])]
    answers = inquirer.prompt(questions)

    if answers['option']   == fltr:
        questions = [inquirer.Checkbox('filter_options', message=fltr_by, choices=[type, cnt, prc])]
        answers   = inquirer.prompt(questions)
        filter = ()
        for op in answers['filter_options']:
            if op == type:
                filter += ('i_type',)
            if op == cnt:
                filter += ('count',)
            if op == prc:
                filter += ('i_price',)
        display_inventory(None, filter, emp_id)
    elif answers['option'] == edit_inv:
        edit_inventory(None)
    elif sjtrophy.is_manager(emp_id):
        manager_main_menu(None, emp_id)
    else:
        associate_main_menu(None, emp_id)


def edit_inventory(msg):
    system('clear')
    display_sj_trophy()
    display_message('INVENTORY')
    display_message(msg)


def display_inventory(msg, filter, emp_id):
    index          = 0
    invtry         = sjtrophy.sort_inventory(filter)
    invtry_divided = list_of_chunks(invtry[0], 10)
    length_of_id   = len(invtry_divided)
    sel_op         = 11*' ' + 'SELECT OPTION'
    next           = 12*' ' + 'NEXT'
    prev           = 12*' ' + 'PREV'
    back           = 12*' ' + 'BACK'
    dflt           = next

    while True:
        system('clear')
        display_sj_trophy()
        display_message('INVENTORY')
        display_message(msg)
        print(tabulate(invtry_divided[index], headers=invtry[1], tablefmt='fancy_grid'))
        print('PAGE {} OF {}'.format(index + 1, length_of_id))

        questions = [inquirer.List('option', message=sel_op, choices=[next, prev, back], default=dflt)]
        answers   = inquirer.prompt(questions)

        if answers['option']   == next:
            index = (index + 1) % length_of_id
            dflt = next
            continue
        elif answers['option'] == prev:
            index = (index - 1) % length_of_id
            dflt = prev
            continue
        else:
            break

    inventory(None, emp_id)

    # for chunk in tupls:
    #     print(tabulate(chunk, headers=invtry[1], tablefmt='fancy_grid') )

    #query inventory
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ---------------------------------------- HELPER -----------------------------------------------

def display_message(msg):
    if not msg: return
    width = 40
    border = '+-' + '-' * width + '-+'
    print(border.center(60))
    for line in wrap(msg, width):
        print('| {0:^{1}} |'.format(line, width).center(60))
    print(border.center(60))


def display_sj_trophy():
    border = '--------------------------------------------------------------'
    result = pyfiglet.figlet_format("SJ TROPHY", font = "big" )
    print(border)
    print(result)
    print(border)


def display_results(tuple_list, attr_list):
    print('\n' + tabulate(tuple_list, headers=attr_list, tablefmt='fancy_grid') +'\n' )


# Yield successive n-sized chunks from lst.
def divide_chunks(lst, n):
    # looping till length of lst
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def list_of_chunks(lst, chunk_size):
    return list(divide_chunks(lst, chunk_size))


def new_customer(msg):
    system('clear')
    display_sj_trophy()
    display_message('CUSTOMER SIGN UP')
    display_message(msg)

    questions = [
        inquirer.Text('name',    message="Full name"),
        inquirer.Text('address', message="Address"),
        inquirer.Text('number',  message="Phone number")
    ]
    answers = inquirer.prompt(questions)
    # insert to database return eid (highest eid)


def search_customer():
    questions = [
        inquirer.Text('cname',
                      message="Enter customer name")
    ]
    answers = inquirer.prompt(questions)

    # select from customer where cname = answers[cname]
    # return cid or null

sign_in(None)


