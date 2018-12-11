# -*- coding: utf-8 -*-

from odoo import api, models, _
from odoo.osv import expression

import logging

_logger = logging.getLogger(__name__)

class ReportReplenishDebug(models.AbstractModel):
    _name = 'report.product_debug_replenish.report_replenish_debug'
    _description = 'debug product replenish'
    
    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['product.replenish.debug'].browse(docids)
        
        
        return {
            'doc_ids': docs.ids,
            'doc_model': 'product.replenish.debug',
            'data': data,
            'docs': docs,
            'prepare_run_values':self._prepare_run_values,
            'get_rule': self.get_rule,
            'get_all_routes_and_rule': self.get_all_routes_and_rule,
        }
        
    def _prepare_run_values(self, wizard_record):
        values = {
            'warehouse_id': wizard_record.warehouse_id,
            'route_ids': wizard_record.route_ids,
            'date_planned': wizard_record.date_planned,
            'priority':1,
        }
        return values
        
        
    @ api.model
    def _search_rule(self, route_ids, product_id, warehouse_id, domain):
        
        search_rule_log={"input_route_ids":route_ids.ids,
                    "input_product_id":product_id,
                    "input_warehouse_id": warehouse_id,
                    "input_domain": domain,
                    "input_warehouse_name": warehouse_id.name,
                    "input_product_name": product_id.name,
                    }
        running_flag=""
        
        if warehouse_id:
            domain = expression.AND([['|', ('warehouse_id', '=', warehouse_id.id), ('warehouse_id', '=', False)], domain])
        Rule = self.env['stock.rule']
        res = self.env['stock.rule']
        search_domain=""
        if route_ids:
            #res = Rule.search(expression.AND([[('route_id', 'in', route_ids.ids)], domain]), order='route_sequence, sequence', limit=1)
            search_domain =    expression.AND([[('route_id', 'in', route_ids.ids)], domain])
            res=Rule.search(search_domain, order='route_sequence, sequence', limit=1)
            running_flag= u"按指定路线"
        if not res:
            product_routes = product_id.route_ids | product_id.categ_id.total_route_ids
            if product_routes:
                #res = Rule.search(expression.AND([[('route_id', 'in', product_routes.ids)], domain]), order='route_sequence, sequence', limit=1)
                search_domain =    expression.AND([[('route_id', 'in', product_routes.ids)], domain])
                res=Rule.search(search_domain, order='route_sequence, sequence', limit=1)
                running_flag= u"按产品"
        if not res and warehouse_id:
            warehouse_routes = warehouse_id.route_ids
            if warehouse_routes:
                #res = Rule.search(expression.AND([[('route_id', 'in', warehouse_routes.ids)], domain]), order='route_sequence, sequence', limit=1)
                search_domain =    expression.AND([[('route_id', 'in', product_routes.ids)], domain])
                res=Rule.search(search_domain, order='route_sequence, sequence', limit=1)
                running_flag= u"按仓库"
                
        search_rule_log["running_flag"]=running_flag
        search_rule_log["search_domain"]=search_domain
        search_rule_log["result"]=res
        _logger.info(search_rule_log)
        
        return res,search_rule_log
        
        
        
    def get_rule(self, wizard_record, values):
        product_id =  wizard_record.product_id
        location = wizard_record.location_id
        my_rule = False
        my_logs=[]
        iter_num=0
        while (not my_rule) and location:
            iter_num +=1
            my_rule,my_log = self._search_rule(values.get('route_ids', False), product_id, values.get('warehouse_id', False), [('location_id', '=', location.id), ('action', '!=', 'push')])
            my_log["location"]=location.id
            my_log["location_name"]=location.name 
            my_log["iter_num"]=iter_num
            my_logs.append(my_log)
            location = location.location_id
        return { 'rule':my_rule, 'logs': my_logs}
                  
        
    def get_all_routes_and_rule(self, wizard_record):
        product_id =  wizard_record.product_id
        warehouse_id = wizard_record.warehouse_id
                
        domain =[('action', '!=', 'push')]
        domain = expression.AND([['|', ('warehouse_id', '=', warehouse_id.id), ('warehouse_id', '=', False)], domain])
        
        input_routes    = wizard_record.route_ids
        product_routes = product_id.route_ids | product_id.categ_id.total_route_ids
        warehouse_routes = wizard_record.warehouse_id.route_ids
        
        res=[]
        
        if input_routes:
            search_domain = expression.AND([[('route_id', 'in', input_routes.ids)],domain])
            search_result = self.env['stock.rule'].search(search_domain, order='route_sequence, sequence')
            res.append({'section':'按指定路线', 'rules':search_result, 'domain':search_domain, 'routes':input_routes})
        else:
            res.append({'section':'按指定路线', 'rules':[], 'domain':"", 'routes':[]})
            
        if product_routes:
            search_domain = expression.AND([[('route_id', 'in', product_routes.ids)], domain])
            search_result = self.env['stock.rule'].search(search_domain, order='route_sequence, sequence')
            res.append({'section':'按产品', 'rules':search_result, 'domain':search_domain, 'routes':product_routes})
        else:
            res.append({'section':'按产品', 'rules':[], 'domain':"", 'routes':[]})
            
        if warehouse_routes:
            search_domain = expression.AND([[('route_id', 'in', warehouse_routes.ids)], domain])
            search_result = self.env['stock.rule'].search(search_domain, order='route_sequence, sequence')
            res.append({'section':'按仓库', 'rules':search_result, 'domain':search_domain, 'routes':warehouse_routes})
        else:
            res.append({'section':'按仓库', 'rules':[], 'domain':"", 'routes':[]})
            
        return res
   