{
    'name': 'Repair Order',
    'version': '17.0.1.0',
    'author': 'Le Chinh Dai',
    'license': 'LGPL-3',
    'depends': ['base', 'repair', 'appointment', 'fleet', 'contacts', 'delivery'],
    'data': [
        'security/ir.model.access.csv',
        'views/repair_sale_orer_form.xml',
        'views/lsc.xml',
        'views/bg_hoadondt_view.xml',
        'views/repair_quotations.xml',
        # 'views/repair_order_view.xml',
        # 'views/repair_order_vehicle_views.xml',
        'views/tab_repair_history_views.xml',
        'views/tab_service_info_worklist_service_views.xml',
        'views/tab_promotions_program_views.xml',
        'views/tab_sale_order.xml',
        'views/vehicle_views.xml',
        'views/view.xml',
        'views/repair_order_list_view.xml',
        'views/repair_order_smart_buttons_view.xml',
        'views/appointment_smart_buttons_view.xml',
        'views/tab_customer_vehicle_info_view.xml',

        
        #region BẢNG GIÁ
        'views/product_pricelist_views.xml',
        'views/product_pricelist_item_views.xml', 
        #endregion
        
        
        'views/tad_order_detail.xml',
        'views/tab_customer_signature.xml',
        'views/tab_other_info.xml',
        'views/menus.xml',
    ],
    
    'installable': True,
    'application': True,
    'auto_install': False,
    'sequence': 1,  # Đưa Module lên đầu
}