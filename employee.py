import sjtrophy
import inquirer
import pyfiglet
from os import system, name
from textwrap import wrap
from tabulate import tabulate


# EMPLOYEE SIDE APPLICATION
def sign_in(msg):
    display_header(msg, 'LOGIN', 40)

    questions = [
        inquirer.Text('user_id',  message="USER ID".rjust(19)),
        inquirer.Text('password', message="PASSWORD".rjust(19))
    ]
    answers   = inquirer.prompt(questions)
    user_id   = answers['user_id']
    password  = answers['password']
    employee  = sjtrophy.verify_emp_login(user_id, password)
    branch_id = sjtrophy.select_row_from('employee', user_id)[0][5]

    if not employee:
        sign_in('No record of employee')
    elif sjtrophy.is_manager(user_id):
        manager_main_menu(None, user_id, branch_id)
    else:
        associate_main_menu(None, user_id, branch_id)


def manager_main_menu(msg, emp_id, branch_id):
    display_header(msg, 'MANAGER MENU', 40)

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
        inventory(None, emp_id, branch_id)
    elif answers['option'] == mng_emp:
        manage_employees(None, branch_id)
    else:
        sign_in(None)


def associate_main_menu(msg, emp_id, branch_id):
    display_header(msg, 'ASSOCIATE MENU', 40)

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
        inventory(None, emp_id, branch_id)
    else:
        sign_in(None)

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ------------------------------------- MENU OPTIONS --------------------------------------------

def new_order(msg, emp_id, branch_id):
    system('clear')
    display_sj_trophy()
    display_message('NEW ORDER', 40)
    display_message(msg, 40)

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
        manager_main_menu(msg, emp_id, branch_id)
    else:
        associate_main_menu(msg, emp_id, branch_id)



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
    display_message('INVENTORY MANAGEMENT', 40)
    display_message(msg, 40)


def manage_employees(msg, branch_id):
    system('clear')
    display_sj_trophy()
    dmsg = 'EMPLOYEE MANAGMENT'
    display_message(dmsg, 40)
    display_message(msg, 40)
    branch_emp = sjtrophy.filter_search('employee', ('branch', branch_id), None)
    display_paged_results(branch_emp, dmsg)
    opt         = 11*' ' + 'SELECT AN OPTION'
    add         = 12*' ' + 'ADD AN EMPLOYEE'
    rem         = 12*' ' + 'REMOVE AN EMPLOYEE'
    tfr         = 12*' ' + 'TRANSFER AN EMPLOYEE'

    questions = [inquirer.List('option',
                               message=opt,
                               choices=[add, rem, tfr]
                               )
                 ]
    answers = inquirer.prompt(questions)
    nme    = 12*' ' + 'NAME'
    addr   = 12*' ' + 'ADDRESS'
    phn    = 12*' ' + 'PHONE NUMBER'
    pw     = 12*' ' + 'TEMPORARY PASSWORD'
    rem_id = 12*' ' + 'ENTER ID OF EMPLOYEE TO REMOVE'
    tfr_id = 12*' ' + 'ENTER ID OF EMPLOYEE TO TRANSFER'
    b_id   = 12*' ' + 'ENTER BRANCH ID TO TRANSFER TO'


    if add == answers['option']:
        questions = [
            inquirer.Text('e_name',   message=nme),
            inquirer.Text('e_addr',   message=addr),
            inquirer.Text('e_num',    message=phn),
            inquirer.Text('e_temp_pw',message=pw)
        ]
        answers = inquirer.prompt(questions)
        print(answers)
        #sjtrophy.insert_into_table('employee')
        # insert employee with name, address, phone, temp_password, mgr(current_eid) and branch(current_branch)

    elif rem == answers['option']:
        questions = [
            inquirer.Text('eid',
                          message=rem_id)
        ]
        answers = inquirer.prompt(questions)
        # Remove employee with eid

    elif tfr == answers['option']:
        questions = [
            inquirer.Text('eid',
                          message=tfr_id),
            inquirer.Text('bid',
                          message=b_id)
        ]
        answers = inquirer.prompt(questions)
        # update employee with eid set branch = bid



def inventory(msg, emp_id, branch_id):
    sel_op     = 11*' ' + 'SELECT OPTION'
    sel_brnch  = 11*' ' + 'SELECT BRANCH'
    branch     = 12*' ' + 'BRANCH'
    fltr       = 12*' ' + 'FILTER'
    edit_inv   = 12*' ' + 'EDIT INVENTORY'
    back       = 12*' ' + 'BACK'
    fltr_by    = 11*' ' + 'FILTER BY'
    type       = 10*' ' + 'TYPE'
    cnt        = 10*' ' + 'COUNT'
    prc        = 10*' ' + 'PRICE'
    curr_brnch = branch_id
    branches   = []
    branch_map = {}
    fmt_brnch  = ''

    for index in range(1,11):
        fmt_brnch = 12*' ' + 'BRANCH {}'.format(index)
        branches.append(fmt_brnch)
        branch_map[fmt_brnch] = index
        #TO DO: add branch locations
    branches.append(back)

    while True:
        display_header(msg, 'INVENTORY', 40)

        if sjtrophy.is_manager(emp_id):
            questions = [inquirer.List('option', message=sel_op, choices=[branch, fltr, edit_inv, back])]
        else:
            questions = [inquirer.List('option', message=sel_op, choices=[branch, fltr, back])]
        answers = inquirer.prompt(questions)

        if answers['option']   == branch:
            questions  = [inquirer.List('sel_brnch', message=sel_brnch, choices=branches)]
            answers    = inquirer.prompt(questions)
            if answers['sel_brnch'] != back:
                curr_brnch = branch_map[answers['sel_brnch']]
                continue
            else:
                continue
        elif answers['option'] == fltr:
            questions  = [inquirer.Checkbox('filter_options', message=fltr_by, choices=[type, cnt, prc])]
            answers    = inquirer.prompt(questions)
            filter     = []
            for op in answers['filter_options']:
                if op == type:
                    filter.append('i_type')
                if op == cnt:
                    filter.append('count')
                if op == prc:
                    filter.append('i_price')
            where_condition = [('branch', curr_brnch)]
            filtered_table = sjtrophy.filter_search('item', where_condition, filter)
            display_paged_results(filtered_table, 'INVENTORY')
        elif answers['option'] == edit_inv:
            edit_inventory(None, emp_id, branch_id)
        elif sjtrophy.is_manager(emp_id):
            manager_main_menu(None, emp_id, branch_id)
        else:
            associate_main_menu(None, emp_id, branch_id)


def edit_inventory(msg, emp_id, branch_id):
    display_header(msg, 'INVENTORY', 40)

    sel_op    = 11*' ' + 'SELECT OPTION'
    upd_itm   = 12*' ' + 'UPDATE ITEM'
    add_itm   = 12*' ' + 'ADD ITEM'
    rmv_itm   = 12*' ' + 'REMOVE ITEM'
    back      = 12*' ' + 'BACK'
    questions = [inquirer.List('option', message=sel_op, choices=[upd_itm, add_itm, rmv_itm, back])]
    answers   = inquirer.prompt(questions)

    if answers['option']   == upd_itm:
        update_item(None, emp_id, branch_id)
    elif answers['option'] == add_itm:
        add_item(None, emp_id, branch_id)
    elif answers['option'] == rmv_itm:
        remove_item(None, emp_id, branch_id)
    else:
        inventory(msg, emp_id, branch_id)


def update_item(msg, emp_id, branch_id):

    while True:
        display_header(msg, 'INVENTORY', 40)

        sel_op    = 11*' ' + 'SELECT OPTION'
        press     = 11*' ' + 'PRESS'
        done      = 12*' ' + 'DONE'
        upd_price = 12*' ' + 'UPDATE PRICE'
        upd_count = 12*' ' + 'UPDATE COUNT'
        back      = 12*' ' + 'BACK'
        itmid     = 11*' ' + 'ENTER ITEM ID'
        new_price = 11*' ' + 'ENTER NEW PRICE'
        new_cnt   = 11*' ' + 'ENTER NEW COUNT'
        val_name  = ''
        attr_name = ''

        questions = [inquirer.List('option', message=sel_op, choices=[upd_price, upd_count, back])]
        answers   = inquirer.prompt(questions)

        if answers['option']   == upd_price:
            val_name  = new_price
            attr_name = 'i_price'
        elif answers['option'] == upd_count:
            val_name  = new_cnt
            attr_name = 'count'
        else:
            inventory(msg, emp_id, branch_id)

        questions = [inquirer.Text('itm_id',        message=itmid)]
        answers   = inquirer.prompt(questions)
        item_id   = answers['itm_id']
        display_row('item', item_id)

        questions = [inquirer.Text('update_value', message=val_name)]
        answers   = inquirer.prompt(questions)
        set_value = [(attr_name, answers['update_value'])]
        sjtrophy.update_row_values('item', set_value, item_id)
        display_row('item', item_id)

        questions = [inquirer.List('done', message=press, choices=[done])]
        answers   = inquirer.prompt(questions)

        if answers['done'] == done:
            continue


def add_item(msg, emp_id, branch_id):
    press     = 11*' ' + 'PRESS'
    done      = 12*' ' + 'DONE'
    type      = 11*' ' + 'ENTER TYPE'
    count     = 11*' ' + 'ENTER COUNT'
    price     = 11*' ' + 'ENTER PRICE'
    row_vals  = []
    questions = [inquirer.Text('type',  message=type),
                 inquirer.Text('count', message=count),
                 inquirer.Text('price', message=price)]
    answers   = inquirer.prompt(questions)

    row_vals = [answers['type'], answers['count'], answers['price'], branch_id]
    sjtrophy.insert_item(row_vals)

    questions = [inquirer.List('done', message=press, choices=[done])]
    answers   = inquirer.prompt(questions)

    if answers['done'] == done:
        return



def remove_item(msg, emp_id, branch_id):
    print("remove item")


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ---------------------------------------- HELPER -----------------------------------------------

def display_header(msg, header_name, header_size):
    system('clear')
    display_sj_trophy()
    display_message(header_name, header_size)
    display_message(msg, header_size)


def display_message(msg, width):
    if not msg: return
    print(format_str(msg, width))


def display_sj_trophy():
    border = '--------------------------------------------------------------'
    result = pyfiglet.figlet_format("SJ TROPHY", font = "big" )
    print(border)
    print(result)
    print(border)


def display_row(table, row_id):
    row = sjtrophy.select_row_from(table, row_id)
    sjtrophy.display_results(row[0], row[1])


def display_paged_results(results, message):
    index          = 0
    table_divided = list_of_chunks(results[0], 10)
    length_of_id   = len(table_divided)
    sel_op         = 11*' ' + 'SELECT OPTION'
    next           = 12*' ' + 'NEXT'
    prev           = 12*' ' + 'PREV'
    back           = 12*' ' + 'BACK'
    dflt           = next

    while True:
        display_header(None, message, 40)
        print(tabulate(table_divided[index], headers=results[1], tablefmt='fancy_grid'))
        print('PAGE {} OF {}'.format(index + 1, length_of_id))

        questions = [inquirer.List('option', message=sel_op, choices=[next, prev, back], default=dflt)]
        answers   = inquirer.prompt(questions)

        if answers['option']   == next:
            index = (index + 1) % length_of_id
            dflt  = next
            continue
        elif answers['option'] == prev:
            index = (index - 1) % length_of_id
            dflt  = prev
            continue
        else:
            break



def display_results(table, where, order_by, emp_id):
    index          = 0
    invtry         = sjtrophy.filter_search(table, where, order_by)
    invtry_divided = list_of_chunks(invtry[0], 10)
    length_of_id   = len(invtry_divided)
    sel_op         = 11*' ' + 'SELECT OPTION'
    next           = 12*' ' + 'NEXT'
    prev           = 12*' ' + 'PREV'
    back           = 12*' ' + 'BACK'
    dflt           = next

    while True:
        display_header(None, 'INVENTORY', 40)
        print(tabulate(invtry_divided[index], headers=invtry[1], tablefmt='fancy_grid'))
        print('PAGE {} OF {}'.format(index + 1, length_of_id))

        questions = [inquirer.List('option', message=sel_op, choices=[next, prev, back], default=dflt)]
        answers   = inquirer.prompt(questions)

        if answers['option']   == next:
            index = (index + 1) % length_of_id
            dflt  = next
            continue
        elif answers['option'] == prev:
            index = (index - 1) % length_of_id
            dflt  = prev
            continue
        else:
            break

# Yield successive n-sized chunks from lst.
def divide_chunks(lst, n):
    # looping till length of lst
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def format_str(msg, width):
    fmt_str  = ''
    border   = '+-' + '-' * width + '-+'
    border   = border.center(60)
    fmt_str += border
    fmt_str += '\n'
    for line in wrap(msg, width):
        fmt_str += '| {0:^{1}} |'.format(line, width).center(60)
        fmt_str += '\n'
    fmt_str += border
    return fmt_str


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
