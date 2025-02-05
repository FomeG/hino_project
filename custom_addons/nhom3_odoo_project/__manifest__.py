{
    'name': 'Lệnh sửa chữa',
    'version': '17.0.1.0',
    'author': 'Le Chinh Dai',
    'license': 'LGPL-3',
    'depends': ['base', 'repair', 'appointment', 'fleet', 'contacts'],
    'data': [
        'security/ir.model.access.csv',
        'views/repair_quotations.xml',
        # 'views/repair_order_view.xml',
        # 'views/repair_order_vehicle_views.xml',
        'views/tab_repair_history_views.xml',
        'views/tab_service_info_worklist_service_views.xml',
        'views/tab_promotions_program_views.xml',
        'views/tab_sale_order.xml',
        'views/vehicle_views.xml',
        'views/view.xml',
        'views/quotations_list_view.xml',
        'views/smart_buttons_view.xml',
        'views/tab_customer_vehicle_info_view.xml',
        'views/menus.xml',
    ],
    'installable': True,
    'application': True,
}