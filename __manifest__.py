# -*- coding: utf-8 -*-
{
    'name': 'NoveCare',
    'author': 'Super Team',
    'category': 'Crm, Products',
    'depends': ['base', 'mail', 'contacts', 'crm', 'website'],
    'web_icon': 'novecare,static/description/icon.png',
    'description': """Crm Automation Tools Responsible For Catching All Leads Come From Omni Channels """,
    'data': [
        'security/ir.model.access.csv',
        # 'security/security.xml',
        'views/incoming_leads_view.xml',
        'views/appointment_view.xml',
        'views/message_template_view.xml',
        'views/instagram_template.xml',
        'views/snapchat_template.xml',
        'views/tiktok_template.xml',
        'views/menus.xml',

    ],
    'demo': [
    ],
    'installable': True,
    'auto_install': False,
    'assets': {
        'web.assets_backend': [
            '/novecare_agent/static/src/scss/crm_leads.scss',
            '/novecare_agent/static/src/scss/appointment_styles.scss',
        ],
    },
}
