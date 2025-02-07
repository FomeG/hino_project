# -*- coding: utf-8 -*-
{
    'name': "z_banggia",

    'summary': "Short (1 phrase/line) summary of the module's purpose",

    'description': """
Long description of module's purpose
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': [
        'base',
        'nhom3_odoo_project',
        'product',
        ],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/product_pricelist_views.xml',
        
        'views/product_pricelist_item_views.xml', 
        
        # 'views/tab_apdungxe.xml',
        # 'views/tab_apdungkm.xml',
        # 'views/tab_apdungdaily.xml',
        # 'views/tab_khachhang.xml',
        
        
        'views/menu.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    
    'installable': True,
    'application': True,
    'auto_install': False,
    'sequence': 1,  # Số càng thấp, module càng được ưu tiên hiển thị
    
}

