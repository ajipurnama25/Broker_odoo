from paho import mqtt
import paho.mqtt.client as paho
import paho.mqtt.subscribe as subscribe
import ssl
import json
import xmlrpc.client
import auth_values

def process_message(client, userdata, message):
    # Parsing JSON payload
    order_data = json.loads(message.payload)

    # Connect to the Odoo API
    common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(auth_values.url))
    uid = common.authenticate(auth_values.db, auth_values.username, auth_values.password, {})

    # Create a connection to the models
    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(auth_values.url))

    # Create purchase order
    order_lines = []
    for line in order_data['order_line']:
        order_lines.append((0, 0, {
            'product_id': line[2]['product_id'],
            'product_qty': line[2]['product_qty'],
            # Add other fields as needed
        }))
    purchase_order_vals = {
        'partner_id': order_data['partner_id'],
        'partner_ref': order_data['partner_ref'],
        'date_order': order_data['date_order'],
        'date_planned': order_data['date_planned'],
        'order_line': order_lines,
        # Add other fields as needed
    }
    # print(order_data)
    
    # sending data to odoo
    purchase_order_id = models.execute_kw(auth_values.db, uid, auth_values.password, 'purchase.order', 'create', [purchase_order_vals])
    models.execute_kw(auth_values.db, uid, auth_values.password, 'purchase.order', 'write', [[purchase_order_id], {'state': "purchase"}])

    print("Purchase Order created with ID:", purchase_order_id)

    # SSL/TLS settings
    sslSettings = ssl.SSLContext(ssl.PROTOCOL_TLS)

    # MQTT authentication
    auth = {'username': 'admin', 'password': 'Admin12345'}

    # Subscribe to MQTT topic
    subscribe.callback(process_message, '#', hostname='0ef562581d144a8da051382a90237387.s1.eu.hivemq.cloud', port=8883, auth=auth, tls=sslSettings, protocol=paho.MQTTv31)

    # Loop to keep the script running and handle callbacks
    paho.Client().loop_forever()
