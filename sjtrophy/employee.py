#import sjtrophy
import inquirer
from os import system, name


# EMPLOYEE SIDE APPLICATION
def sign_in():
    system('clear')
    display_border_title('Employee Log In')

    questions = [
        inquirer.Text('username', message="Username".rjust(19)),
        inquirer.Text('password', message="Password".rjust(19))
    ]
    answers  = inquirer.prompt(questions)
    username = answers['username']
    password = answers['password']


def mgr_main_menu():
    system('clear')
    display_border_title('MANAGER MENU')

    questions = [
        inquirer.List('option',
                       message= 11*' ' + 'SELECT OPTION',
                       choices=[12*' ' + 'New Order',
                                12*' ' + 'View active orders',
                                12*' ' + 'View past orders',
                                12*' ' + 'Manage Inventory',
                                12*' ' + 'Manage Employees'])
    ]
    answers = inquirer.prompt(questions)
    print(answers)


def new_customer():
    print('Please Enter Customer Information')
    questions = [
        inquirer.Text('name',
                      message="Full name"),
        inquirer.Text('address',
                      message="Address"),
        inquirer.Text('number',
                      message="Phone number")
    ]
    answers = inquirer.prompt(questions)
    print(answers)
    # save to database


def new_order():
    system('clear')
    questions = [inquirer.Confirm('new_customer',
                               message="Is this a new customer?", default=True
                               )
                 ]
    answers = inquirer.prompt(questions)
    print(answers)
    if answers['new_customer']:
        new_customer()
    else:
        questions = [
             inquirer.Text('cname',
                          message="Enter customer name")
            ]
        answers = inquirer.prompt(questions)
        print(answers)
        # create new customer if id is invalid


#---------------------------------Helper Methods------------------------------------

def display_border_title(title):
    border = '------------------------------'
    print('\n{}'.format(border.center(60)))
    print('\n{}\n'.format(title.center(60)))
    print(border.center(60))

sign_in()
mgr_main_menu()
new_order()





# def view_active_orders():

# def view_past_orders():

# def manage_inventory():

# def manage_empl_info():
