# sj_trophy_shop
SJSU Database Systems Term Project

Data Requirements
- SJ Trophy Shop has multiple branches, each with a unique branch ID (bid). Each branch has multiple employees and may offer coupons. Each coupon has a unique coupon ID (coup_id), and an expiration date (exp_date), and a specified discount (discount).

- Each employee has a unique employee ID, (eid), and a name, phone number, and address on file (e_name, e_addr, e_num), respectively. Any employee can view or create an order, view inventory of items, and view or add a design.

- An order has a unique order number (ord_num) and consists of a specific required item, (sritem), count of the item, (count) design, (o_design) and order status (status).

- An item to be engraved is identified by a unique id (iid), may have more than one type(i_type). 
Design is also identified by a unique id (did).

- An employee is either a supervisor or a supervisee, the latter with only one supervisor. Supervisors may offer coupons at the store he or she works at to customers. A supervisee may update an order that he or she created. 

- A customer has a unique customer ID (cid), name (c_name), address, (c_addr) and phone number (c_num) on file after creating their first order. A customer may view the inventory of all items, and browse by different categories such as by type (i_type) and most popular (based on order count ord_count)

- A customer can write a review for an item, branch, or employee, specified by r_type. Each review has a unique id for a certain customer (rid), but may be duplicated among multiple customers.
