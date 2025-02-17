{
    'name': 'Repair Order',
    'version': '17.0.1.0',
    'author': 'Le Chinh Dai',
    'license': 'LGPL-3',
    'depends': ['base', 'repair', 'appointment', 'fleet', 'contacts', 'delivery','web'],
    'data': [
        'security/ir.model.access.csv',
        'views/res_partner_views.xml',
        'views/tab_calendar_event_views.xml',
        'views/repair_job_type_views.xml',
        
        # vehicle
        'views/vehicle_information_views.xml',

        # Pricelist
        'views/product_pricelist_views.xml',
        'views/tab_product_pricelist_views.xml',
        'views/tab_product_pricelist_item_views.xml',

        # Repair Order
        'views/repair_order_views.xml',
        'views/tab_repair_order_views.xml',
        'views/repair_order_smart_buttons_view.xml',

        # Sale Order
        'views/sale_order_views.xml',
        'views/tab_sale_order_views.xml',

        # LSC
        'views/lsc_button_views.xml',

        # Warranty
        'views/warranty_request_views.xml',

        'views/action_window.xml',
        'views/menus.xml',
    ],
   
    'installable': True,
    'application': True,
    'auto_install': False,
    'sequence': 1,  # Đưa Module lên đầu
}