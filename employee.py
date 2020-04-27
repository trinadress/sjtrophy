import sjtrophy
import inquirer
import pyfiglet
import bcrypt
from os import system, name
from textwrap import wrap
from tabulate import tabulate
import logging

logging.basicConfig(filename='employee.log', level=logging.DEBUG)

salt = bcrypt.gensalt()

# EMPLOYEE SIDE APPLICATION
def sign_in(msg):
    logging.info('Signing in')
    display_header(msg, 'LOGIN', 40)

    usrid     = 11*' ' + 'USER ID'
    psswd     = 11*' ' + 'PASSWORD'
    questions = [
        inquirer.Text('user_id',  message=usrid),
        inquirer.Text('password', message=psswd)
    ]
    answers   = inquirer.prompt(questions)
    user_id   = answers['user_id']
    password  = answers['password']
    employee  = sjtrophy.verify_emp_login(user_id, password)

    logging.info('Sign in successful')
    if not employee[0]:
        sign_in(employee[1])
    branch_id = sjtrophy.select_row_from('employee', user_id)[0][5]

    if sjtrophy.is_manager(user_id):
        manager_main_menu(None, user_id, branch_id)
    associate_main_menu(None, user_id, branch_id)


def manager_main_menu(msg, emp_id, branch_id):
    logging.info('Manager logged in')
    display_header(msg, 'MANAGER MENU', 40)

    sel_op    = 11*' ' + 'SELECT OPTION'
    new_o     = 12*' ' + 'NEW ORDER'
    view_o    = 12*' ' + 'VIEW ORDERS'
    mng_inv   = 12*' ' + 'MANAGE INVENTORY'
    mng_emp   = 12*' ' + 'MANAGE EMPLOYEES'
    log_o     = 12*' ' + 'LOG OUT'
    questions = [inquirer.List('option', message= sel_op, choices=[new_o, view_o, mng_inv, mng_emp, log_o])]
    answers   = inquirer.prompt(questions)['option']
    logging.debug('Selected option')

    if answers   == new_o:
        new_order(None, emp_id, branch_id)
    elif answers == view_o:
        view_orders(None, emp_id, branch_id)
    elif answers == mng_inv:
        inventory(None, emp_id, branch_id)
    elif answers == mng_emp:
        manage_employees(None, emp_id, branch_id)
    else:
        sign_in(None)


def associate_main_menu(msg, emp_id, branch_id):
    display_header(msg, 'ASSOCIATE MENU', 40)

    sel_op    = 11*' ' + 'SELECT OPTION'
    new_o     = 12*' ' + 'NEW ORDER'
    view_o    = 12*' ' + 'VIEW ORDERS'
    view_inv  = 12*' ' + 'VIEW INVENTORY'
    log_o     = 12*' ' + 'LOG OUT'
    questions = [inquirer.List('option', message= sel_op, choices=[new_o, view_o, view_inv, log_o])]
    answers   = inquirer.prompt(questions)['option']

    if answers   == new_o:
        new_order(None, emp_id)
    elif answers == view_o:
        view_orders(None, emp_id, branch_id)
    elif answers == view_inv:
        inventory(None, emp_id, branch_id)
    else:
        sign_in(None)

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ------------------------------------- MENU OPTIONS --------------------------------------------

def new_order(msg, emp_id, branch_id):
    logging.info('Creating new order')
    display_header(msg, 'NEW ORDER', 40)

    new_cust = 11*' ' + "NEW CUSTOMER?"
    questions = [inquirer.Confirm('new_customer', message=new_cust, default=True)]
    answers = inquirer.prompt(questions)
    # insert to database return eid (highest eid)

    if answers['new_customer']:
        new_customer(msg)
        # cid = new_customer()
    else:
        c = sjtrophy.search_customer()
        if None == c:
            cid = new_customer()

    itm_id    = 11*' ' + "ENTER ITEM ID"
    dsg_id    = 11*' ' + "ENTER DESIGN ID"
    no_itms   = 11*' ' + "ENTER NUMBER OF ITEMS FOR ENGRAVING"
    cust_dsg  = 11*' ' + "CUSTOM DESIGN?"
    msg       = 'ORDER COMPLETE'
    questions = [inquirer.Text('item_id',   message=itm_id),
                 inquirer.Confirm('design', message=cust_dsg, default=False)]
    answers   = inquirer.prompt(questions)
    if answers['design']:
        # insert new design
    else:
    questions = [inquirer.Text('design_id',message=dsg_id),
                 inquirer.Text('count',    message=no_itms)]
    answers   = inquirer.prompt(questions)
    # get prices of item and design to derive total cost
    # insert into customer_order set count, status item, design, customer, last_ud_by, total_cost


    if sjtrophy.is_manager(emp_id):
        manager_main_menu(msg, emp_id, branch_id)
    else:
        associate_main_menu(msg, emp_id, branch_id)


def view_orders(msg, emp_id, branch_id):
    logging.info('Viewing Orders')
    sel_op    = 11*' ' + "SELECT OPTION"
    fltr      = 12*' ' + "FILTER"
    edt       = 12*' ' + "EDIT ORDER"
    back      = 12*' ' + "BACK"
    filt_res  = 11*' ' + "FILTER BY"
    new       = 12*' ' + "NEWEST"
    old       = 12*' ' + "OLDEST"
    cnt       = 12*' ' + "ORDER COUNT"
    cust      = 12*' ' + "CUSTOMER"
    actv      = 12*' ' + "ACTIVE"
    cmpltd    = 12*' ' + "COMPLETED"

    while True:
        display_header(msg, 'ORDERS', 40)

        questions = [inquirer.List('option', message=sel_op, choices=[fltr, edt, back])]
        answers   = inquirer.prompt(questions)['option']

        if fltr == answers:
            logging.info('Filtering results')
            questions = [inquirer.Checkbox('sort_options', message=filt_res, choices=[new, old, cnt, cust, actv, cmpltd], default=[new])]
            answers   = inquirer.prompt(questions)['sort_options']
            order_by  = []
            if new in answers:
                order_by.append("date_created DESC")
            if old in answers and 'Newest' not in answers:
                order_by.append("date_created ASC")
            if cnt in answers:
                order_by.append("count DESC")
            if cust in answers:
                order_by.append("customer")
            if (actv in answers and cmpltd in answers) or (actv not in answers and cmpltd not in answers):
                stat_cond = None
            elif actv in answers:
                stat_cond = [('o_status', 'ACTIVE')]
            else:
                stat_cond = [('o_status', 'COMPLETE')]

            result = sjtrophy.filter_search('customer_order', stat_cond, order_by)
            display_paged_results(result, 'CUSTOMER ORDERS')

        elif edt == answers:
            logging.info('Editing orders')
            print("TO DO: EDIT ORDER")

        elif sjtrophy.is_manager(emp_id):
            logging.info('Returning to main menu')
            manager_main_menu(msg, emp_id, branch_id)
        else:
            logging.info('Returning to main menu')
            associate_main_menu(msg, emp_id, branch_id)


# TODO: Error checking
def manage_employees(msg, emp_id, branch_id):
    logging.info('Managing employees')
    display_header(msg, 'EMPLOYEE MANAGEMENT', 40)
    opt    = 11*' ' + 'SELECT OPTION'
    view   = 12*' ' + 'VIEW EMPLOYEES'
    add    = 12*' ' + 'ADD AN EMPLOYEE'
    rem    = 12*' ' + 'REMOVE AN EMPLOYEE'
    tfr    = 12*' ' + 'TRANSFER AN EMPLOYEE'
    back   = 12*' ' + 'BACK'
    nme    = 12*' ' + 'NAME'
    addr   = 12*' ' + 'ADDRESS'
    phn    = 12*' ' + 'PHONE NUMBER'
    pw     = 12*' ' + 'TEMPORARY PASSWORD'
    rem_id = 12*' ' + 'ENTER ID OF EMPLOYEE TO REMOVE'
    tfr_id = 12*' ' + 'ENTER ID OF EMPLOYEE TO TRANSFER'
    b_id   = 12*' ' + 'ENTER BRANCH ID TO TRANSFER TO'

    questions = [inquirer.List('option', message=opt, choices=[view, add, rem, tfr, back])]
    answers = inquirer.prompt(questions)

    # View Employees
    if view == answers['option']:
        logging.info('Viewing employees')
        branch_emp = sjtrophy.filter_search('employee', ('branch', branch_id), None)
        display_paged_results(branch_emp, None)
        manage_employees(None, emp_id, branch_id)

    # Add an Employee
    if add == answers['option']:
        logging.info('Adding an employee')
        attr = []
        val  = []
        questions = [
            inquirer.Text('e_name',   message=nme),
            inquirer.Text('e_addr',   message=addr),
            inquirer.Text('e_phone',  message=phn),
            inquirer.Text('e_pw',     message=pw)
        ]
        answers = inquirer.prompt(questions)

        answers.update([('branch', branch_id), ('sup_id', emp_id)])
        answers['e_pw'] = encrypt_pw(answers['e_pw'], salt)
        ans             = separate_key_value(answers)
        attr            = ans[0]
        val             = ans[1]
        sjtrophy.insert_into_table('employee', attr, val)

    # Remove an Employee
    elif rem == answers['option']:
        logging.info('Removing an employee')
        questions = [inquirer.Text('eid', message=rem_id)]
        answers   = inquirer.prompt(questions)
        sjtrophy.delete_rows('employee', [('e_id', answers['eid'])])
    # Transfer an Employee
    elif tfr == answers['option']:
        logging.info('Transferring an employee')
        questions = [inquirer.Text('e_id', message=tfr_id),
                     inquirer.Text('branch',message=b_id)]
        answers   = inquirer.prompt(questions)
        sjtrophy.update_row_values('employee', [('branch', answers['branch'])], answers['e_id'])
    # Return to main menu
    else:
        logging.info('Returning to main menu')
        manager_main_menu(None, emp_id, branch_id)

    manage_employees(None, emp_id, branch_id)


def inventory(msg, emp_id, branch_id):
    logging.info('Managing inventory')
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
        #TODO: ADD BRANCH LOCATIONS
    branches.append(back)

    while True:
        display_header(msg, 'INVENTORY', 40)

        if sjtrophy.is_manager(emp_id):
            questions = [inquirer.List('option', message=sel_op, choices=[branch, fltr, edit_inv, back])]
        else:
            questions = [inquirer.List('option', message=sel_op, choices=[branch, fltr, back])]
        answers = inquirer.prompt(questions)['option']

        if answers  == branch:
            logging.info('Selecting a branch')
            questions      = [inquirer.List('sel_brnch', message=sel_brnch, choices=branches)]
            branch_answers = inquirer.prompt(questions)['sel_brnch']
            if branch_answers == back:
                continue
            curr_brnch = branch_map[branch_answers]

        elif answers == fltr:
            logging.info('Filter')
            questions      = [inquirer.Checkbox('filter_options', message=fltr_by, choices=[type, cnt, prc])]
            filter_choices = inquirer.prompt(questions)['filter_options']
            filter     = []
            if type in filter_choices:
                filter.append('i_type')
            if cnt in filter_choices:
                filter.append('count')
            if prc in filter_choices:
                filter.append('i_price')
            where_condition   = [('branch', curr_brnch)]
            filtered_results  = sjtrophy.filter_search('item', where_condition, filter)
            display_paged_results(filtered_results, 'INVENTORY')

        elif answers == edit_inv:
            logging.info('Edit inventory')
            edit_inventory(None, emp_id, branch_id)

        elif sjtrophy.is_manager(emp_id):
            manager_main_menu(None, emp_id, branch_id)

        else:
            associate_main_menu(None, emp_id, branch_id)


def edit_inventory(msg, emp_id, branch_id):
    logging.info('Editing inventory')
    display_header(msg, 'INVENTORY', 40)

    sel_op    = 11*' ' + 'SELECT OPTION'
    upd_itm   = 12*' ' + 'UPDATE ITEM'
    add_itm   = 12*' ' + 'ADD ITEM'
    rmv_itm   = 12*' ' + 'REMOVE ITEM'
    back      = 12*' ' + 'BACK'
    questions = [inquirer.List('option', message=sel_op, choices=[upd_itm, add_itm, rmv_itm, back])]
    answers   = inquirer.prompt(questions)['option']

    if answers   == upd_itm:
        update_item(None, emp_id, branch_id)
    elif answers == add_itm:
        add_item(None, emp_id, branch_id)
    elif answers == rmv_itm:
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
        answers   = inquirer.prompt(questions)['option']

        if answers   == upd_price:
            val_name  = new_price
            attr_name = 'i_price'
        elif answers == upd_count:
            val_name  = new_cnt
            attr_name = 'count'
        else:
            edit_inventory(msg, emp_id, branch_id)

        questions = [inquirer.Text('itm_id', message=itmid)]
        item_id   = inquirer.prompt(questions)['itm_id']
        display_row('item', item_id)

        questions = [inquirer.Text('update_value', message=val_name)]
        answers   = inquirer.prompt(questions)['update_value']
        set_value = [(attr_name, answers)]
        sjtrophy.update_row_values('item', set_value, item_id)
        display_row('item', item_id)

        questions = [inquirer.List('done', message=press, choices=[done])]
        answer    = inquirer.prompt(questions)['done']

        if answers == done:
            continue


def add_item(msg, emp_id, branch_id):
    press     = 11*' ' + 'PRESS'
    done      = 12*' ' + 'DONE'
    type      = 11*' ' + 'ENTER TYPE'
    count     = 11*' ' + 'ENTER COUNT'
    price     = 11*' ' + 'ENTER PRICE'

    questions = [inquirer.Text('type',  message=type),
                 inquirer.Text('count', message=count),
                 inquirer.Text('price', message=price)]
    answers   = inquirer.prompt(questions)

    row_vals  = [answers['type'], answers['count'], answers['price'], branch_id]
    sjtrophy.insert_item(row_vals)

    questions = [inquirer.List('done', message=press, choices=[done])]
    answers   = inquirer.prompt(questions)

    if answers['done'] == done:
        return


def remove_item(msg, emp_id, branch_id):
    c_item     = 11*' ' + 'CHOOSE ITEM'
    press      = 11*' ' + 'PRESS'
    done       = 12*' ' + 'DONE'
    delete     = 11*' ' + 'DELETE?'
    where_cond = "branch = {}".format(branch_id)
    items      = sjtrophy.select_table_where('item', where_cond)[0]
    item_types = []
    fmt_items  = []
    dict       = {}

    for item in items:
        item_types.append((item[0],item[1]))
    for item in item_types:
        fmt_items.append(12*' ' + '{} {}'.format(item[0], item[1].upper()))
    for index, item in enumerate(fmt_items):
        dict[item] = item_types[index]

    questions  = [inquirer.List('types', message=c_item, choices=fmt_items)]
    choice     = inquirer.prompt(questions)['types']
    where_cond = "i_id = {} and i_type = \"{}\"".format(dict[choice][0], dict[choice][1])
    result     = sjtrophy.select_table_where('item', where_cond)
    sjtrophy.display_results(result[0][0], result[1])

    questions  = [inquirer.Confirm('delete', message=delete)]
    del_yes    = inquirer.prompt(questions)['delete']
    if del_yes:
        sjtrophy.delete_rows('item', where_cond)

    questions  = [inquirer.List('done', message=press, choices=[done])]
    answer     = inquirer.prompt(questions)['done']
    if answer == done:
        return


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
    table_divided  = list_of_chunks(results[0], 10)
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
        answers   = inquirer.prompt(questions)['option']

        if answers   == next:
            index = (index + 1) % length_of_id
            dflt  = next
        elif answers == prev:
            index = (index - 1) % length_of_id
            dflt  = prev
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
    name = 11 * ' ' + 'ENTER CUSTOMER NAME'
    questions = [inquirer.Text('cname', message=name)]
    answers = inquirer.prompt(questions)
    where_clause = "c_name = '{}' ".format(answers['cname'])
    print(where_clause)
    return sjtrophy.select_table_where('customer', where_clause)


def new_design():
    size  = 11*' ' + 'ENTER DESIGN SIZE'
    font  = 11*' ' + 'ENTER DESIGN FONT'
    text  = 11*' ' + 'ENTER DESIGN TEXT'
    price = 11*' ' + 'ENTER PRICE'
    questions = [inquirer.Text('size', message=size),
                 inquirer.Text('font', message=font),
                 inquirer.Text('text', message=text),
                 inquirer.Text('price', message=price)]
    answers = inquirer.prompt(questions)
    values = [answers['size'], answers['font'], answers['text'], answers['price']]
    sjtrophy.insert_design(values)



def encrypt_pw(pw, salt):
    return bcrypt.hashpw(pw, salt)


def separate_key_value(dict):
    keys = []
    vals = []
    for key in dict:
        keys.append(key)
        vals.append(dict[key])
    return (keys, vals)


sign_in(None)
