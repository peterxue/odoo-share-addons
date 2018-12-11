# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


{
    'name': 'product debug replenish',
    'version': '12.0',
    'category': 'Warehouse',
    'sequence': 16,
    'license': 'AGPL-3',
    "author" : "liuaiqun",
    'website': 'http://blog.sina.com.cn/u/1406343191',
    'depends': ['mrp'],
    'description': u"产品补货路线分析",
    'summary': u"产品补货路线分析",
    'data': [
        'reports/report_replenish_debug.xml',
        'wizard/product_replenish_debug_views.xml',
        'views/product_template.xml',
    ],
    'application': True,
}
