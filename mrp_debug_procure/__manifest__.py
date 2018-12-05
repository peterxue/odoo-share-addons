# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


{
    'name': 'mrp debug procure',
    'version': '12.0',
    'category': 'Manufacturing',
    'sequence': 16,
    'license': 'AGPL-3',
    "author" : "liuaiqun",
    'website': 'http://blog.sina.com.cn/u/1406343191',
    'depends': ['mrp'],
    'description': u"显示生产单中，原材料补货方法（mto/mts）的计算方式",
    'summary': u"显示生产单中，原材料补货方法（mto/mts）的计算方式",
    'data': [

        'reports/report_procure_method.xml',
        'views/mrp_production.xml',
    ],
    'application': True,
}
