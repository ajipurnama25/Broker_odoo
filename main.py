# This Python script is used to test the Odoo API

import xmlrpc.client
import auth_values
from datetime import datetime, timedelta

def create_partner(name):
    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(auth_values.url))

    id = models.execute_kw(auth_values.db,
                           auth_values.uid,
                           auth_values.password,
                           'res.partner',
                           'create',
                           [{'name': name}])

    print(id)

def create_purchase_order(vendor_name, pif):

    # Connect to the Odoo server
    common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(auth_values.url))
    uid = common.authenticate(auth_values.db, auth_values.username, auth_values.password, {})

    # Connect to the Odoo API
    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(auth_values.url))

    # Find vendor by name
    vendor_id = models.execute_kw(auth_values.db, auth_values.uid, auth_values.password,
                                  'res.partner', 'search', [[('name', '=', vendor_name)]], {'limit': 1})

    # Calculate order deadline (current date in system)
    order_deadline = datetime.now().strftime('%Y-%m-%d')

    # Calculate expected arrival (this Friday)
    today = datetime.today()
    days_until_friday = (4 - today.weekday()) % 7  # Number of days until Friday (0 = Monday, ..., 6 = Sunday)
    expected_arrival = (today + timedelta(days=days_until_friday)).strftime('%Y-%m-%d')

    # Find product by internal reference
    product_internal_ref = pif
    product_id = models.execute_kw(auth_values.db, auth_values.uid, auth_values.password,
                                   'product.product', 'search', [[('default_code', '=', product_internal_ref)]],
                                   {'limit': 1})

    if not product_id:
        print("Product with internal reference {} not found.".format(product_internal_ref))
        exit()

    product_refs = ["230036", "230037", "230062", "230075"]
    product_qty = [10000, 10000, 20000, 20000]
    #product_prices = [40000, 10000, 25000, 888]

    # Create Purchase Order Lines
    order_lines = []
    for i in range(0,len(product_refs)):
        product_id = models.execute_kw(auth_values.db, auth_values.uid, auth_values.password,
                                       'product.product', 'search', [[('default_code', '=', product_refs[i])]],
                                       {'limit': 1})

        if not product_id:
            print("Product with internal reference {} not found.".format(product_refs[i]))
            continue

        order_lines.append((0, 0, {
            'product_id': product_id[0],
            'product_qty': product_qty[i],  # Example quantity
            #'price_unit': product_prices[i],  # Example quantity
        }))


    # Create Purchase Order
    purchase_order_vals = {
        'partner_id': vendor_id[0],
        'partner_ref': 'MJK-SJ 30062023 SURIMI',
        'date_order': order_deadline,
        'date_planned': expected_arrival,
        'order_line': order_lines,
    }

    purchase_order_id = models.execute_kw(auth_values.db, auth_values.uid, auth_values.password,'purchase.order', 'create', [purchase_order_vals])

    models.execute_kw(auth_values.db, auth_values.uid, auth_values.password, 'purchase.order', 'write', [[purchase_order_id], {'state': "purchase"}])
    
    print("Purchase Order created with ID:", purchase_order_id)
print(order_lines)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # create_partner('test test test!!!')
    create_purchase_order("JAVA SEAFOOD, PT", "230036")


