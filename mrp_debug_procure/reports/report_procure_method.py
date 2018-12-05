# -*- coding: utf-8 -*-

from odoo import api, models, _
import logging

_logger = logging.getLogger(__name__)

class ReportProcureMethod(models.AbstractModel):
    _name = 'report.mrp_debug_procure.report_procure_method'
    _description = 'debug mrp pruduction procure method'

    def get_mto_route(self):
        try:
            mto_route = self.env['stock.warehouse']._find_global_route('stock.route_warehouse0_mto', _('Make To Order'))
        except:
            mto_route = False
            
        return mto_route
        
    def get_rules_and_methods(self, move,mto_route):
        product = move.product_id
        routes = product.route_ids + product.route_from_categ_ids + move.warehouse_id.route_ids
         
        all_rule = self.env['stock.rule'].search([('route_id', 'in', [x.id for x in routes]),
                                                    ('action', '!=', 'push')])
        first_rule = self.env['stock.rule'].search([('route_id', 'in', [x.id for x in routes]),
                                                      ('location_src_id', '=', move.location_id.id),
                                                      ('location_id', '=', move.location_dest_id.id), 
                                                      ('action', '!=', 'push')], limit=1)
                                                      
        method= [ { 'id':1,  'usage':'NO',  'desc':u'因可用的规则为mto，故选mto'},
                  { 'id':2,  'usage':'NO',  'desc':u'因存在mto_route故选mto'},
                  { 'id':3,  'usage':'Yes', 'desc':u'不改变(默认值为mts)'},
                 ]
                  
        if first_rule and (first_rule.procure_method == 'make_to_order'):
            res[0]['select']='Yes';
        elif not first_rule:
            if mto_route and mto_route.id in [x.id for x in routes]:
                res[1]['select']='Yes';

        return {
            'all_rules': all_rule,
            'first_rule': first_rule,
            'methods': method,
        }
                
    
    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['stock.move'].browse(docids)
        return {
            'doc_ids': docs.ids,
            'doc_model': 'stock.move',
            'data': data,
            'docs': docs,
            'get_mto_route': self.get_mto_route,
            'get_rules_and_methods': self.get_rules_and_methods,
        }
        

#class CouponReport(models.AbstractModel):
#    _name = 'report.sale_coupon.report_coupon'
#    _description = 'Sales Coupon Report'
#
#    @api.model
#    def _get_report_values(self, docids, data=None):
#        docs = self.env['sale.coupon'].browse(docids)
#        return {
#            'doc_ids': docs.ids,
#            'doc_model': 'sale.coupon',
#            'data': data,
#            'docs': docs,
#        }
