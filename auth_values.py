# url = 'http://192.168.0.21:8069'
# db = 'erp_odoo_dev'
# username = 'admin'
# uid = 2
# password = 'ifCZ@@2020'

import xmlrpc.client

# Informasi koneksi
url = 'http://192.168.0.21:8069'
db = 'erp_odoo_dev'
username = 'admin'
uid = 2
password = 'ifCZ@@2020'

# Buat koneksi XML-RPC
common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
uid = common.authenticate(db, username, password, {})

if uid:
    print("Koneksi berhasil! UID pengguna:", uid)
else:
    print("Gagal mengautentikasi.")
