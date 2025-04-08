# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import logging
import datetime

_logger = logging.getLogger(__name__)


class InstagramLeadController(http.Controller):
    @http.route('/instagram/lead', type='http', auth='public', website=True)
    def instagram_lead_form(self, **kw):
        return request.render('novecare_agent.instagram_lead_form')

    @http.route('/instagram/lead/submit', type='http', auth='public', website=True, methods=['POST'], csrf=False)
    def instagram_lead_submit(self, **post):
        lead_vals = {
            'lead_first_name': post.get('first_name'),
            'lead_last_name': post.get('last_name'),
            'lead_phone_no': post.get('phone'),
            'email': post.get('email'),
            'lead_gender': post.get('gender'),
            'lead_dob': post.get('dob') if post.get('dob') else False,
            'reason_for_visit': post.get('reason'),
            'source': 'Instagram',
            'lead_date': datetime.date.today(),
            'stages': 'lead',
            'preferred_contact_method': post.get('contact_method'),
        }



        lead = request.env['incoming.leads'].sudo().create(lead_vals)

        return request.render('novecare_agent.instagram_lead_confirmation', {
            'lead': lead
        })
class SnapChatLeadController(http.Controller):
    @http.route('/snapchat/lead', type='http', auth='public', website=True)
    def snapchat_lead_form(self, **kw):
        return request.render('novecare_agent.snapchat_lead_form')

    @http.route('/snapchat/lead/submit', type='http', auth='public', website=True, methods=['POST'], csrf=False)
    def instagram_lead_submit(self, **post):
        lead_vals = {
            'lead_first_name': post.get('first_name'),
            'lead_last_name': post.get('last_name'),
            'lead_phone_no': post.get('phone'),
            'email': post.get('email'),
            'lead_gender': post.get('gender'),
            'lead_dob': post.get('dob') if post.get('dob') else False,
            'reason_for_visit': post.get('reason'),
            'source': 'Snapchat',
            'lead_date': datetime.date.today(),
            'stages': 'lead',
            'preferred_contact_method': post.get('contact_method'),
        }



        lead = request.env['incoming.leads'].sudo().create(lead_vals)

        return request.render('novecare_agent.snapchat_lead_confirmation', {
            'lead': lead
        })
class TiktokLeadController(http.Controller):
    @http.route('/tiktok/lead', type='http', auth='public', website=True)
    def tiktok_lead_form(self, **kw):
        return request.render('novecare_agent.tiktok_lead_form')

    @http.route('/tiktok/lead/submit', type='http', auth='public', website=True, methods=['POST'], csrf=False)
    def tiktok_lead_submit(self, **post):
        lead_vals = {
            'lead_first_name': post.get('first_name'),
            'lead_last_name': post.get('last_name'),
            'lead_phone_no': post.get('phone'),
            'email': post.get('email'),
            'lead_gender': post.get('gender'),
            'lead_dob': post.get('dob') if post.get('dob') else False,
            'reason_for_visit': post.get('reason'),
            'source': 'Tiktok',
            'lead_date': datetime.date.today(),
            'stages': 'lead',
            'preferred_contact_method': post.get('contact_method'),
        }



        lead = request.env['incoming.leads'].sudo().create(lead_vals)

        return request.render('novecare_agent.tiktok_lead_confirmation', {
            'lead': lead
        })

