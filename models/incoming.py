from odoo import models, fields, api, _
from markupsafe import Markup
import requests
import re
import json
class IncomingLeads(models.Model):
    _name = 'incoming.leads'
    _description = 'Incoming Leads'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    partner_id = fields.Many2one('res.users',string = 'Call Center Agent', tracking = True)
    stages = fields.Selection([('lead','Lead'),('patient','Patient'),('won','Closed Won')],string = 'Stages',tracking = True)
    lead_status = fields.Selection([('expected_patient','Expected Patient'),('need_2nd_call','Need Second Call'),('need_3rd_call','Need Third Call'),
                                    ('closed_lost','Closed Lost'),('book_appointment','Book Appointment'),('confirmed','Confirmed')
                                    ,('consultation','Consultation'),('procedure','Procedure')
                                    ,('rescheduled','Rescheduled'),('no_show','No Show'),('show','Show')
                                    ],string='Status',tracking = True)
    patient_status = fields.Selection([('confirmed','Confirmed'),('rescheduled_appointment','Rescheduled Appointment')
                                        ,('no_show','No Show'),('show','Show')
                                       ],string='Status',tracking = True)
    won_status = fields.Selection([('consultation','Consultation'),('procedure','Procedure')],string='Status',tracking = True)
    reason = fields.Text(string = 'Reason')
    segment = fields.Many2one('segments.model',string = 'Segment')
    source = fields.Selection([('Instagram','Instagram'),('Tiktok','Tiktok'),('Snapchat','Snapchat'),('Facebook','Facebook'),('Whatsapp','Whatsapp')],
                              string ='Source')
    lead_date = fields.Date(string = 'Lead Date')
    reason_for_visit = fields.Text(string = 'Reason for Visit')

    # lead personal info
    lead_first_name = fields.Char(string = 'First Name')
    lead_last_name = fields.Char(string = 'Last Name')
    lead_gender = fields.Selection([('Male','Male'),('Female','Female')],string = 'Gender')
    lead_dob = fields.Date(string = 'Date of Birth')

    # lead contact info
    lead_phone_no = fields.Char(string = 'Phone Number')
    email = fields.Char(string = 'Email')
    preferred_contact_method = fields.Selection([('whatsapp','Whatsapp'),('phone','Phone Call'),('email','Email')]
                                                ,string = 'Preferred Contact Method')
    wp_show = fields.Boolean(string='Show Whatsapp',default=False)
    use_temp = fields.Boolean(string='Use Message Template',default=False)
    template = fields.Many2one('message.template')
    json_msg = fields.Html(related ='template.computed_json')
    html_preview = fields.Html(related ='template.html_preview')

    def whatsapp_view(self):
        for rec in self:
            if not rec.wp_show:
                rec.wp_show = True

    def original_lead_info(self):
        for rec in self:
            if rec.wp_show:
                rec.wp_show = False

    def action_book_appointment(self):
        return {
            'name': 'Appointment',
            'type': 'ir.actions.act_window',
            'res_model': 'appointment.model',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_incoming_id': self.id,
                'default_partner_id': self.partner_id.id,
                'default_lead_first_name': self.lead_first_name,
                'default_lead_last_name': self.lead_last_name,
                'default_lead_gender': self.lead_gender,
                'default_lead_dob': self.lead_dob,
                'default_lead_phone_no': self.lead_phone_no,
                'default_email': self.email,
                'default_reason_for_visit': self.reason,
                'default_appointment_date': fields.Datetime.now(),
                'default_state': 'draft',
        },
        }


    # chating
    chat_history = fields.One2many('chat.history','incoming', string ='Chat')
    box = fields.Html(string='Message Box')
    html_chat = fields.Html(string='Chat Display', compute='chat_interface', sanitize=False)


    def send_message(self):
        for rec in self:
            print('sending message')
            token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOiJBUEkiLCJhcHAiOiI2NDU4YTRkZTlhMGU0YTU5ZDA3YzdlNjYiLCJhY2wiOlsiYXBpOmFkbWluIiwiYWNjb3VudDp1cGRhdGUiLCJhY3Rpb246Y3JlYXRlIiwiYWN0aW9uOmRlbGV0ZSIsImFjdGlvbjp1cGRhdGUiLCJhZ2VuZGE6Y3JlYXRlIiwiYWdlbmRhOmRlbGV0ZSIsImFnZW5kYTpyZWFkIiwiYWdlbmRhOnVwZGF0ZSIsImFwcDpsaW5rUGFydG5lciIsImFwcDpsaXN0TWFuYWdtZW50UmVxdWVzdCIsImFwcEluZm86Z2V0IiwiYXBwSW50ZWdyYXRpb246Y3JlYXRlIiwiYXBwSW50ZWdyYXRpb246ZGVsZXRlIiwid2hhdHNhcHA6Z2V0RmlsZSIsIndoYXRzYXBwTWVzc2FnZVRlbXBsYXRlczpjcmVhdGUiLCJ3aGF0c2FwcE1lc3NhZ2VUZW1wbGF0ZXM6ZGVsZXRlIiwid2hhdHNhcHBNZXNzYWdlVGVtcGxhdGVzOmdldCIsIndoYXRzYXBwTWVzc2FnZVRlbXBsYXRlczpsaXN0IiwidHJpZ2dlcjp1cGRhdGUiLCJ0cmlnZ2VyOmRlbGV0ZSIsInRyaWdnZXI6Y3JlYXRlIiwidHJlZTp1cGRhdGVUcmVlU2V0dGluZyIsInRyZWU6dXBkYXRlTm9kZXMiLCJ0cmVlOnVwZGF0ZUJhc2ljSW5mbyIsInRyZWU6cmVhZCIsInRyZWU6bGlzdCIsInRyZWU6aW1wb3J0IiwidHJlZTpnZXROb2RlcyIsInRyZWU6Z2V0VHJlZVNldHRpbmciLCJ0cmVlOmdldEJhc2ljSW5mbyIsInRyZWU6ZXhwb3J0IiwidHJlZTpkZWxldGUiLCJ0ZWFtTWVtYmVyOnVwZGF0ZSIsInRlYW1NZW1iZXI6bGlzdCIsInRlYW1NZW1iZXI6ZGVsZXRlIiwidGVhbU1lbWJlcjpjcmVhdGUiLCJyb2xlOmxpc3QiLCJyZXNwb25zZTp1cGRhdGUiLCJyZXNwb25zZTpkZWxldGUiLCJyZXNwb25zZTpjcmVhdGUiLCJub2RlOnVwZGF0ZSIsInByaW9yaXR5R3JvdXA6Y3JlYXRlIiwicHJpb3JpdHlHcm91cDpkZWxldGUiLCJwcmlvcml0eUdyb3VwOmdldCIsInByaW9yaXR5R3JvdXA6bGlzdCIsInByaW9yaXR5R3JvdXA6dXBkYXRlIiwicHVzaDpjcmVhdGUiLCJwdXNoOmRlbGV0ZSIsInB1c2g6Z2V0IiwicHVzaDpsaXN0IiwicHVzaDp1cGRhdGUiLCJub2RlOmRlbGV0ZSIsIm5vZGU6Y3JlYXRlIiwibWVtYmVyczptYW5hZ2VUYWdzIiwibWVtYmVyVGFnczpnZXQiLCJtZW1iZXJUYWdzOmRlbGV0ZSIsIm1lbWJlclRhZ3M6Y3JlYXRlIiwibWVtYmVyOndyaXRlIiwibWVtYmVyOnVwZGF0ZURldGFpbHMiLCJtZW1iZXI6cmVhZCIsIm1lZGlhTGlicmFyeTp1cGRhdGUiLCJtZW1iZXI6VG9nZ2xlTGl2ZUNoYXQiLCJtZW1iZXI6YWRtaW4iLCJtZW1iZXI6Y3JlYXRlIiwibWVtYmVyOmRlbGV0ZSIsIm1lbWJlcjpleHBvcnQiLCJtZW1iZXI6Z2V0Q29udmVyc2F0aW9uIiwibWVtYmVyOmdldERldGFpbHMiLCJtZW1iZXI6aW1wb3J0IiwibWVtYmVyOmxpc3QiLCJtZWRpYUxpYnJhcnk6bGlzdCIsIm1lZGlhTGlicmFyeTpnZXQiLCJtZWRpYUxpYnJhcnk6ZGVsZXRlIiwibWVkaWFMaWJyYXJ5OmNyZWF0ZSIsImxvZzpsaXN0IiwiaW50ZWdyYXRpb246dXBkYXRlIiwiaW50ZWdyYXRpb246bGlzdCIsImludGVncmF0aW9uOmdldCIsImludGVncmF0aW9uOmNyZWF0ZSIsImZpbGU6d2FHZXQiLCJmaWxlOmdldCIsImZpbGU6YWRtaW4iLCJkYXRhU291cmNlOnVwZGF0ZURvYyIsImRhdGFTb3VyY2U6dXBkYXRlRGF0YXNvdXJjZSIsImRhdGFTb3VyY2U6bGlzdERvY3MiLCJkYXRhU291cmNlOmxpc3REYXRhc291cmNlcyIsImRhdGFTb3VyY2U6aW1wb3J0RGF0YXNvdXJjZSIsImRhdGFTb3VyY2U6Z2V0RG9jIiwiZGF0YVNvdXJjZTpleHBvcnREYXRhc291cmNlIiwiZGF0YVNvdXJjZTpkZWxldGVEb2MiLCJkYXRhU291cmNlOmRlbGV0ZURhdGFzb3VyY2UiLCJkYXRhU291cmNlOmNyZWF0ZURvYyIsImRhdGFTb3VyY2U6Y3JlYXRlRGF0YXNvdXJjZSIsImRhc2hib2FyZDpsaXN0V2hhdHNhcHBBbmFseXRpY3MiLCJkYXNoYm9hcmQ6bGlzdFVzZXJzIiwiZGFzaGJvYXJkOmxpc3RUaWNrZXRpbmciLCJkYXNoYm9hcmQ6bGlzdE5scEFuYWx5dGljcyIsImRhc2hib2FyZDpsaXN0Q29tbWVudFJlcGx5IiwiZGFzaGJvYXJkOmxpc3RBc3NpZ25tZW50IiwiY2hhbm5lbDp1cGRhdGVUcmVlU2V0dGluZ3MiLCJjaGF0OmV4cG9ydCIsImNvbmRpdGlvbjpjcmVhdGUiLCJjb25kaXRpb246ZGVsZXRlIiwiY29uZGl0aW9uOnVwZGF0ZSIsImNvbnZlcnNhdGlvbjpyZWFkIiwiZGFzaGJvYXJkOmV4cG9ydEFuYWx5dGljcyIsImRhc2hib2FyZDpleHBvcnRVc2VycyIsImRhc2hib2FyZDpsaXN0QWdlbnRzIiwiZGFzaGJvYXJkOmxpc3RBbmFseXRpY3MiLCJjaGFubmVsOnVwZGF0ZVBsYXRmb3JtU2V0dGluZ3MiLCJjaGFubmVsOnVwZGF0ZVBsYXRmb3JtSW5mbyIsImNoYW5uZWw6dXBkYXRlTGl2ZUNoYXRTZXR0aW5ncyIsImNoYW5uZWw6dXBkYXRlRW52aXJvbm1lbnRJbmZvIiwiY2hhbm5lbDp1cGRhdGVEZXRhaWwiLCJjaGFubmVsOnVwZGF0ZUJyb2FkY2FzdEdyb3VwU2V0dGluZ3MiLCJjaGFubmVsOnVwZGF0ZUJhc2ljSW5mbyIsImNoYW5uZWw6dXBkYXRlQXZhaWxhYmlsaXRpZXMiLCJjaGFubmVsOmxpc3QiLCJjaGFubmVsOmdldFRyZWVTZXR0aW5ncyIsImNoYW5uZWw6Z2V0UGxhdGZvcm1TZXR0aW5ncyIsImNoYW5uZWw6Z2V0UGxhdGZvcm1JbmZvIiwiY2hhbm5lbDpnZXRMaXZlQ2hhdFNldHRpbmdzIiwiY2hhbm5lbDpkZWxldGVFbnZpcm9ubWVudCIsImNoYW5uZWw6Z2V0QXZhaWxhYmlsaXRpZXMiLCJjaGFubmVsOmdldEJhc2ljSW5mbyIsImNoYW5uZWw6Z2V0QnJvYWRjYXN0R3JvdXBTZXR0aW5ncyIsImNoYW5uZWw6Z2V0RGV0YWlscyIsImNoYW5uZWw6Z2V0RW52aXJvbm1lbnRJbmZvIiwiY2hhbm5lbDpjcmVhdGVDaGFubmVsIiwiY2hhbm5lbDpjcmVhdGVFbnZpcm9ubWVudCIsImNoYW5uZWw6ZGVsZXRlQ2hhbm5lbCIsImJvdGJ1aWxkZXI6cmVhZCIsImJvdGJ1aWxkZXI6bWFuYWdlIiwiYm90OnNlbmRSZXNwb25zZXMiLCJib3Q6cmVkaXJlY3RNZW1iZXJUb05vZGUiLCJib3Q6YWRtaW4iLCJhdWRpdFRyYWlsOmxpc3QiLCJiYWNrZ3JvdW5kVGFzazpnZXQiLCJiYWNrZ3JvdW5kVGFzazpsaXN0IiwiYmlsbGluZzpjcmVhdGVTdWJzY3JpcHRpb24iLCJiaWxsaW5nOmRlbGV0ZVN1YnNjcmlwdGlvbiIsImJpbGxpbmc6Z2V0U3Vic2NyaXB0aW9uIiwiYmlsbGluZzpsaXN0SW52b2ljZXMiLCJiaWxsaW5nOnVwZGF0ZVN1YnNjcmlwdGlvbiIsImF1ZGllbmNlOnVwZGF0ZSIsImF1ZGllbmNlOnJlYWQiLCJhdWRpZW5jZTpsaXN0IiwiYXVkaWVuY2U6Z2V0IiwiYXVkaWVuY2U6ZGVsZXRlIiwiYXVkaWVuY2U6Y3JlYXRlIiwiYXR0YWNobWVudElkOmxpc3QiLCJhcHBJbnRlZ3JhdGlvbjpnZXQiLCJhcHBJbnRlZ3JhdGlvbjpsaXN0IiwiYXBwSW50ZWdyYXRpb246dXBkYXRlIiwiYXBwU2V0dGluZ3M6Z2V0IiwiYXBwU2V0dGluZ3M6dXBkYXRlIiwiYXNzaWdubWVudDpsaXN0IiwiYXR0YWNobWVudElkOmNyZWF0ZSJdLCJqdGkiOiIwNDJiZDUxNC0zOTkyLTVmMmEtOTY2NS0wNGU4NTUwYzQ5MmQiLCJpc3MiOiI2NDU4YTRhZTNiZWIwMTAxMjcwOWI3ZjIiLCJpYXQiOjE2ODQwNjYxMDYyMzh9.Kip5h5leVtDojhakyroL2Rh9lzBt7QF-KCSuov9zhIo'
            url = "https://bot.api.woztell.com/sendResponses?accessToken=" + token
            channel_id = '645bf628d76ad166d9fae864'
            if rec.box:
                print('the message to send',rec.box)
                clean_message = rec.box
                if isinstance(clean_message, str):
                    # Strip outer <p> tags if they exist
                    clean_message = re.sub(r'^<p>(.*?)</p>$', r'\1', clean_message)
                    # Also handle multiple paragraphs by replacing inner <p> tags with line breaks
                    clean_message = re.sub(r'</p>\s*<p>', '\n', clean_message)
                    # Remove any remaining <p> or </p> tags
                    clean_message = re.sub(r'</?p>', '', clean_message)
                    print('clean message:', clean_message)
                    phone = f"2{rec.lead_phone_no}"
                response = {
                    "channelId": channel_id,
                    "recipientId": phone,
                    "response": [
                        {
                            "type": "TEXT",
                            "text": clean_message
                        }
                    ]
                }
                requests.post(url, json=response)
                rec.write({

                    'chat_history': [(0, 0, {
                        'agent': rec.box,
                        'timestamp': fields.Datetime.now(),
                        "is_send_by_user": True
                    })]
                })
            if rec.json_msg:
                template_json = json.loads(rec.json_msg)

                phone = f"2{rec.lead_phone_no}"
                response_data = {
                    "channelId": channel_id,
                    "recipientId": phone,
                    "response": [template_json]
                }


                requests.post(url, json=response_data)
                rec.write({

                    'chat_history': [(0, 0, {
                        'agent': rec.html_preview,
                        'timestamp': fields.Datetime.now(),
                        "is_send_by_user": True
                    })]
                })
            rec.box =False
            rec.template =False


    @api.depends('chat_history')
    def chat_interface(self):
        for record in self:
            html = [f'''
                <div class="chat-interface">
                    <div class="chat-header">
                        <div class="header-avatar">
                            <img src="/novecare_agent/static/src/img/avatar.png" alt="Assistant"/>
                        </div>
                        <div class="header-info">
                            <h3>{record.lead_first_name} {record.lead_last_name}</h3>
                            <span class="status">Online</span>
                        </div>
                    </div>
                    <div class="chat-messages" id="chat-messages">
            ''']
            for msg in record.chat_history:
                if msg.lead:
                    html.append(f'''
                        <div class="message-wrapper user-message">
                            <div class="message">
                                <div class="message-content">{msg.lead}</div>
                                <div class="message-meta">
                                    <span class="time">{msg.create_date.strftime('%I:%M %p')}</span>
                                    <span class="status">✓</span>
                                </div>
                            </div>
                        </div>
                    ''')
                if msg.agent:
                    if msg.is_send_by_user:
                        html.append(f'''
                            <div class="message-wrapper assistant-message">
                                <div class="avatar">
                                    <img src="/novecare_agent/static/src/img/avatar.png" alt="Assistant"/>
                                </div>
                                <div class="message">
                                    <div class="wp-message-agent-name">{record.partner_id.name}</div>
                                    <div class="message-content">{msg.agent}</div>
                                    <div class="message-meta">
                                        <span class="time">{msg.create_date.strftime('%I:%M %p')}</span>
                                    </div>
                                </div>
                            </div>
                        ''')
                    else:
                        html.append(f'''
                            <div class="message-wrapper assistant-message">
                                <div class="avatar">
                                    <img src="/booking/static/src/img/bot-avatar.png" alt="Assistant"/>
                                </div>
                                <div class="message">
                                    <div class="wp-message-agent-name">Bot</div>
                                    <div class="message-content">{msg.agent}</div>
                                    <div class="message-meta">
                                        <span class="time">{msg.create_date.strftime('%I:%M %p')}</span>
                                    </div>
                                </div>
                            </div>
                        ''')

            record.html_chat = Markup(''.join(html))

class Appointment(models.Model):
    _name = 'appointment.model'
    _description = 'Appointments'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    # lead personal info
    lead_first_name = fields.Char(string = 'First Name')
    lead_last_name = fields.Char(string = 'Last Name')
    lead_gender = fields.Selection([('Male','Male'),('Female','Female')],string = 'Gender')
    lead_dob = fields.Date(string = 'Date of Birth')

    # lead contact info
    lead_phone_no = fields.Char(string = 'Phone Number')
    email = fields.Char(string = 'Email')

    # EVALUATION
    smoker = fields.Boolean(string="Smoker", track_visibility="true")
    alcoholic = fields.Boolean(string="Alcoholic", track_visibility="true")

    primary_diagnosis = fields.Many2many('eval.primary.diagnosis.model', track_visibility="true")
    secondary_diagnosis = fields.Many2many('eval.secondary.diagnosis.model', track_visibility="true")

    chronic_condition = fields.Many2many('eval.chronic.conditions.model', track_visibility="true")
    allergies = fields.Many2many('eval.allergies.model', track_visibility="true")
    medications = fields.Many2many('eval.medication.model', track_visibility="true")
    family_history = fields.Many2many('eval.family.history.model', track_visibility="true")

    #######vital signs
    temp = fields.Char(string="Temperature", track_visibility="true")
    pulse = fields.Char(string="Pulse", track_visibility="true")
    bp = fields.Char(string="Blood Pressure", track_visibility="true")
    p_height = fields.Float(string="Height", track_visibility="true")
    p_weight = fields.Float(string="Weight", track_visibility="true")
    p_bmi = fields.Float(string="BMI", track_visibility="true")
    height = fields.Char(string="Height", track_visibility="true")
    weight = fields.Char(string="Weight", track_visibility="true")
    bmi = fields.Char(string="BMI", track_visibility="true")



class Segments(models.Model):
        _name = 'segments.model'
        _description = 'Lead Segments'

        name = fields.Char(string ='Segment')


class ChatHistory(models.Model):
    _name = "chat.history"

    lead = fields.Html(string= 'Lead',sanitize=False)
    agent = fields.Html(string= 'Agent',sanitize=False)

    incoming = fields.Many2one('incoming.leads')
    is_send_by_user = fields.Boolean(string = 'sent by user',default=False)
    timestamp = fields.Datetime(string='Timestamp', default=fields.Datetime.now, readonly=True)

    @api.model
    def create(self, vals):
        result = super(ChatHistory, self).create(vals)

        return result

# evaluation sheet models

class PrimaryDiagnosis(models.Model):
    _name = 'eval.primary.diagnosis.model'
    name = fields.Char(string="Primary Diagnosis")


class SecondaryDiagnosis(models.Model):
    _name = 'eval.secondary.diagnosis.model'
    name = fields.Char(string="Secondary Diagnosis")


class ChronicConditions(models.Model):
    _name = 'eval.chronic.conditions.model'
    name = fields.Char(string="Chronic Conditions")


class Allergies(models.Model):
    _name = 'eval.allergies.model'
    name = fields.Char(string="Allergies")


class Medications(models.Model):
    _name = 'eval.medication.model'
    name = fields.Char(string="Medications")


class FamilyHistory(models.Model):
    _name = 'eval.family.history.model'
    name = fields.Char(string="Family History")
