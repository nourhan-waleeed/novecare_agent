from odoo import models, fields, api, _
from markupsafe import Markup
import requests
import re
import json



class ChatDashboard(models.Model):
    _name = 'chat.dashboard'
    _description = 'Chats Dashboard'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name =fields.Char(default = "Chats Dashboard")
    contacts = fields.Many2one('incoming.leads',string= 'Contacts')
    chats = fields.Html(sanitize=False,related ='contacts.html_chat')

    contacts_sidebar = fields.Html(compute="compute_contacts_sidebar", sanitize=False)
    box = fields.Html(sanitize=False)

    def call_send_message(self):
        self.contacts.send_remote_message(self.box)
        self.box = False
    #
    # def compute_contacts_sidebar(self):
    #     for record in self:
    #         html_content = '<div class="contacts-container">'
    #
    #         contacts = self.env['incoming.leads'].search([])
    #
    #         for contact in contacts:
    #             html_content += f'''
    #             <div class="contact-card" onclick="getChat({contact.id})">
    #                 <div><strong>{contact.lead_first_name or 'Unnamed Contact'}</strong></div>
    #                 <div>{contact.lead_phone_no or ''}</div>
    #                 <div>{contact.email or ''}</div>
    #             </div>
    #             '''
    #
    #         html_content += '</div>'
    #
    #         record.contacts_sidebar = Markup(html_content)

    def compute_contacts_sidebar(self):
        for record in self:
            html_content = '<div class="contacts-container">'

            contacts = self.env['incoming.leads'].search([])

            html_content += '''
            <style>
                .contacts-container {
                    padding: 10px 0;
                }
                .contact-card {
                    position: relative;
                    display: flex;
                    padding: 14px;
                    margin-bottom: 14px;
                    border-radius: 8px;
                    background-color: white;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.05);
                    border-left: 3px solid #005a4f;
                    transition: transform 0.2s ease, box-shadow 0.2s ease;
                }
                .contact-card:hover {
                    transform: translateY(-2px);
                    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
                }
                .contact-info {
                    flex-grow: 1;
                    padding-right: 35px;
                }
                .contact-name {
                    font-weight: 600;
                    font-size: 16px;
                    color: #333;
                    margin-bottom: 7px;
                }
                .contact-detail {
                    font-size: 14px;
                    color: #666;
                    margin-bottom: 5px;
                    display: flex;
                    align-items: center;
                }
                .contact-detail i {
                    width: 18px;
                    margin-right: 8px;
                    text-align: center;
                    color: #005a4f;
                }
                .contact-stage {
                    display: inline-block;
                    padding: 3px 10px;
                    border-radius: 12px;
                    background-color: #E0F0EF;
                    color: #005a4f;
                    font-size: 13px;
                    font-weight: 500;
                    margin-top: 6px;
                }
                .contact-partner {
                    font-style: italic;
                    color: #777;
                    font-size: 13px;
                    margin-top: 6px;
                    border-top: 1px dashed #e0e0e0;
                    padding-top: 6px;
                }
                .open-record {
                    position: absolute;
                    right: 12px;
                    top: 50%;
                    transform: translateY(-50%);
                    cursor: pointer;
                    color: #005a4f;
                    font-size: 18px;
                    width: 28px;
                    height: 28px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    border-radius: 50%;
                    background-color: #E0F0EF;
                }
                .open-record:hover {
                    background-color: #005a4f;
                    color: white;
                }
                /* Prevent the arrow click from triggering the parent's onclick */
                .open-record {
                    z-index: 10;
                }
            </style>
            '''

            for contact in contacts:
                contact_url = f"/web#id={contact.id}&model=incoming.leads&view_type=form"

                partner_info = ""
                if contact.partner_id and contact.partner_id.name:
                    partner_info = f'''
                    <div class="contact-partner">
                        <i class="fa fa-building-o"></i> {contact.partner_id.name}
                    </div>
                    '''

                html_content += f'''
                <div class="contact-card" onclick="getChat({contact.id})">
                    <div class="contact-info">
                        <div class="contact-name">{contact.name or 'Unnamed Contact'}</div>
                        <div class="contact-detail"><i class="fa fa-phone"></i> {contact.lead_phone_no or 'No phone'}</div>
                        <div class="contact-detail"><i class="fa fa-envelope"></i> {contact.email or 'No email'}</div>
                        <div class="contact-stage">{contact.stages}</div>
                        {partner_info}
                    </div>
                    <div class="open-record" onclick="event.stopPropagation(); window.open('{contact_url}', '_blank');">
                        <i class="fa fa-external-link"></i>
                    </div>
                </div>
                '''

            html_content += '</div>'

            record.contacts_sidebar = Markup(html_content)
    @api.model
    def get_chat(self,contact_id,recordId):
        contact_ref = self.env['incoming.leads'].browse(int(contact_id))
        record_ref = self.browse(int(recordId))
        print('contact_id',contact_id)
        print('contact_ref',contact_ref)
        search = self.env['incoming.leads'].search([('id','=',contact_ref.id)])
        print('searchh',search)

        record_ref.contacts = contact_ref



    @api.model
    def create(self, vals):
        if self.search_count([]) >= 1:
            return self.search([], limit=1)
        return super(ChatDashboard, self).create(vals)
