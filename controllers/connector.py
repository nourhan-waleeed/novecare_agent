from odoo import fields
from odoo import http
from odoo.http import request
import requests
from datetime import datetime
import yaml
import re
import logging
_logger = logging.getLogger(__name__)

class WhatsappWoztell(http.Controller):

    def format_text(self, text):
        print('into formatting', text)
        text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
        text = text.replace('\n', '<br>')
        text = re.sub(r'\*\s+(.*?)(?:\n|$)', r'<li>\1</li>', text)
        text = re.sub(r'\#\#(.*?)\s', r'<h1>\1</h1>', text)
        print('foormatted', text)
        return text
    @http.route('/lead/generation', type='http', auth='public', methods=['GET', 'POST'], csrf=False)
    def handle_webhook(self, **kw):
        print('into controller')
        uid = request.session.authenticate('REAL_ESTATE', 'admin', 'admin')
        print('-------------------------------------------data--------------------------------------------')
        requested_data = request.httprequest.data
        data = yaml.safe_load(requested_data)
        print(data)
        token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOiJBUEkiLCJhcHAiOiI2NDU4YTRkZTlhMGU0YTU5ZDA3YzdlNjYiLCJhY2wiOlsiYXBpOmFkbWluIiwiYWNjb3VudDp1cGRhdGUiLCJhY3Rpb246Y3JlYXRlIiwiYWN0aW9uOmRlbGV0ZSIsImFjdGlvbjp1cGRhdGUiLCJhZ2VuZGE6Y3JlYXRlIiwiYWdlbmRhOmRlbGV0ZSIsImFnZW5kYTpyZWFkIiwiYWdlbmRhOnVwZGF0ZSIsImFwcDpsaW5rUGFydG5lciIsImFwcDpsaXN0TWFuYWdtZW50UmVxdWVzdCIsImFwcEluZm86Z2V0IiwiYXBwSW50ZWdyYXRpb246Y3JlYXRlIiwiYXBwSW50ZWdyYXRpb246ZGVsZXRlIiwid2hhdHNhcHA6Z2V0RmlsZSIsIndoYXRzYXBwTWVzc2FnZVRlbXBsYXRlczpjcmVhdGUiLCJ3aGF0c2FwcE1lc3NhZ2VUZW1wbGF0ZXM6ZGVsZXRlIiwid2hhdHNhcHBNZXNzYWdlVGVtcGxhdGVzOmdldCIsIndoYXRzYXBwTWVzc2FnZVRlbXBsYXRlczpsaXN0IiwidHJpZ2dlcjp1cGRhdGUiLCJ0cmlnZ2VyOmRlbGV0ZSIsInRyaWdnZXI6Y3JlYXRlIiwidHJlZTp1cGRhdGVUcmVlU2V0dGluZyIsInRyZWU6dXBkYXRlTm9kZXMiLCJ0cmVlOnVwZGF0ZUJhc2ljSW5mbyIsInRyZWU6cmVhZCIsInRyZWU6bGlzdCIsInRyZWU6aW1wb3J0IiwidHJlZTpnZXROb2RlcyIsInRyZWU6Z2V0VHJlZVNldHRpbmciLCJ0cmVlOmdldEJhc2ljSW5mbyIsInRyZWU6ZXhwb3J0IiwidHJlZTpkZWxldGUiLCJ0ZWFtTWVtYmVyOnVwZGF0ZSIsInRlYW1NZW1iZXI6bGlzdCIsInRlYW1NZW1iZXI6ZGVsZXRlIiwidGVhbU1lbWJlcjpjcmVhdGUiLCJyb2xlOmxpc3QiLCJyZXNwb25zZTp1cGRhdGUiLCJyZXNwb25zZTpkZWxldGUiLCJyZXNwb25zZTpjcmVhdGUiLCJub2RlOnVwZGF0ZSIsInByaW9yaXR5R3JvdXA6Y3JlYXRlIiwicHJpb3JpdHlHcm91cDpkZWxldGUiLCJwcmlvcml0eUdyb3VwOmdldCIsInByaW9yaXR5R3JvdXA6bGlzdCIsInByaW9yaXR5R3JvdXA6dXBkYXRlIiwicHVzaDpjcmVhdGUiLCJwdXNoOmRlbGV0ZSIsInB1c2g6Z2V0IiwicHVzaDpsaXN0IiwicHVzaDp1cGRhdGUiLCJub2RlOmRlbGV0ZSIsIm5vZGU6Y3JlYXRlIiwibWVtYmVyczptYW5hZ2VUYWdzIiwibWVtYmVyVGFnczpnZXQiLCJtZW1iZXJUYWdzOmRlbGV0ZSIsIm1lbWJlclRhZ3M6Y3JlYXRlIiwibWVtYmVyOndyaXRlIiwibWVtYmVyOnVwZGF0ZURldGFpbHMiLCJtZW1iZXI6cmVhZCIsIm1lZGlhTGlicmFyeTp1cGRhdGUiLCJtZW1iZXI6VG9nZ2xlTGl2ZUNoYXQiLCJtZW1iZXI6YWRtaW4iLCJtZW1iZXI6Y3JlYXRlIiwibWVtYmVyOmRlbGV0ZSIsIm1lbWJlcjpleHBvcnQiLCJtZW1iZXI6Z2V0Q29udmVyc2F0aW9uIiwibWVtYmVyOmdldERldGFpbHMiLCJtZW1iZXI6aW1wb3J0IiwibWVtYmVyOmxpc3QiLCJtZWRpYUxpYnJhcnk6bGlzdCIsIm1lZGlhTGlicmFyeTpnZXQiLCJtZWRpYUxpYnJhcnk6ZGVsZXRlIiwibWVkaWFMaWJyYXJ5OmNyZWF0ZSIsImxvZzpsaXN0IiwiaW50ZWdyYXRpb246dXBkYXRlIiwiaW50ZWdyYXRpb246bGlzdCIsImludGVncmF0aW9uOmdldCIsImludGVncmF0aW9uOmNyZWF0ZSIsImZpbGU6d2FHZXQiLCJmaWxlOmdldCIsImZpbGU6YWRtaW4iLCJkYXRhU291cmNlOnVwZGF0ZURvYyIsImRhdGFTb3VyY2U6dXBkYXRlRGF0YXNvdXJjZSIsImRhdGFTb3VyY2U6bGlzdERvY3MiLCJkYXRhU291cmNlOmxpc3REYXRhc291cmNlcyIsImRhdGFTb3VyY2U6aW1wb3J0RGF0YXNvdXJjZSIsImRhdGFTb3VyY2U6Z2V0RG9jIiwiZGF0YVNvdXJjZTpleHBvcnREYXRhc291cmNlIiwiZGF0YVNvdXJjZTpkZWxldGVEb2MiLCJkYXRhU291cmNlOmRlbGV0ZURhdGFzb3VyY2UiLCJkYXRhU291cmNlOmNyZWF0ZURvYyIsImRhdGFTb3VyY2U6Y3JlYXRlRGF0YXNvdXJjZSIsImRhc2hib2FyZDpsaXN0V2hhdHNhcHBBbmFseXRpY3MiLCJkYXNoYm9hcmQ6bGlzdFVzZXJzIiwiZGFzaGJvYXJkOmxpc3RUaWNrZXRpbmciLCJkYXNoYm9hcmQ6bGlzdE5scEFuYWx5dGljcyIsImRhc2hib2FyZDpsaXN0Q29tbWVudFJlcGx5IiwiZGFzaGJvYXJkOmxpc3RBc3NpZ25tZW50IiwiY2hhbm5lbDp1cGRhdGVUcmVlU2V0dGluZ3MiLCJjaGF0OmV4cG9ydCIsImNvbmRpdGlvbjpjcmVhdGUiLCJjb25kaXRpb246ZGVsZXRlIiwiY29uZGl0aW9uOnVwZGF0ZSIsImNvbnZlcnNhdGlvbjpyZWFkIiwiZGFzaGJvYXJkOmV4cG9ydEFuYWx5dGljcyIsImRhc2hib2FyZDpleHBvcnRVc2VycyIsImRhc2hib2FyZDpsaXN0QWdlbnRzIiwiZGFzaGJvYXJkOmxpc3RBbmFseXRpY3MiLCJjaGFubmVsOnVwZGF0ZVBsYXRmb3JtU2V0dGluZ3MiLCJjaGFubmVsOnVwZGF0ZVBsYXRmb3JtSW5mbyIsImNoYW5uZWw6dXBkYXRlTGl2ZUNoYXRTZXR0aW5ncyIsImNoYW5uZWw6dXBkYXRlRW52aXJvbm1lbnRJbmZvIiwiY2hhbm5lbDp1cGRhdGVEZXRhaWwiLCJjaGFubmVsOnVwZGF0ZUJyb2FkY2FzdEdyb3VwU2V0dGluZ3MiLCJjaGFubmVsOnVwZGF0ZUJhc2ljSW5mbyIsImNoYW5uZWw6dXBkYXRlQXZhaWxhYmlsaXRpZXMiLCJjaGFubmVsOmxpc3QiLCJjaGFubmVsOmdldFRyZWVTZXR0aW5ncyIsImNoYW5uZWw6Z2V0UGxhdGZvcm1TZXR0aW5ncyIsImNoYW5uZWw6Z2V0UGxhdGZvcm1JbmZvIiwiY2hhbm5lbDpnZXRMaXZlQ2hhdFNldHRpbmdzIiwiY2hhbm5lbDpkZWxldGVFbnZpcm9ubWVudCIsImNoYW5uZWw6Z2V0QXZhaWxhYmlsaXRpZXMiLCJjaGFubmVsOmdldEJhc2ljSW5mbyIsImNoYW5uZWw6Z2V0QnJvYWRjYXN0R3JvdXBTZXR0aW5ncyIsImNoYW5uZWw6Z2V0RGV0YWlscyIsImNoYW5uZWw6Z2V0RW52aXJvbm1lbnRJbmZvIiwiY2hhbm5lbDpjcmVhdGVDaGFubmVsIiwiY2hhbm5lbDpjcmVhdGVFbnZpcm9ubWVudCIsImNoYW5uZWw6ZGVsZXRlQ2hhbm5lbCIsImJvdGJ1aWxkZXI6cmVhZCIsImJvdGJ1aWxkZXI6bWFuYWdlIiwiYm90OnNlbmRSZXNwb25zZXMiLCJib3Q6cmVkaXJlY3RNZW1iZXJUb05vZGUiLCJib3Q6YWRtaW4iLCJhdWRpdFRyYWlsOmxpc3QiLCJiYWNrZ3JvdW5kVGFzazpnZXQiLCJiYWNrZ3JvdW5kVGFzazpsaXN0IiwiYmlsbGluZzpjcmVhdGVTdWJzY3JpcHRpb24iLCJiaWxsaW5nOmRlbGV0ZVN1YnNjcmlwdGlvbiIsImJpbGxpbmc6Z2V0U3Vic2NyaXB0aW9uIiwiYmlsbGluZzpsaXN0SW52b2ljZXMiLCJiaWxsaW5nOnVwZGF0ZVN1YnNjcmlwdGlvbiIsImF1ZGllbmNlOnVwZGF0ZSIsImF1ZGllbmNlOnJlYWQiLCJhdWRpZW5jZTpsaXN0IiwiYXVkaWVuY2U6Z2V0IiwiYXVkaWVuY2U6ZGVsZXRlIiwiYXVkaWVuY2U6Y3JlYXRlIiwiYXR0YWNobWVudElkOmxpc3QiLCJhcHBJbnRlZ3JhdGlvbjpnZXQiLCJhcHBJbnRlZ3JhdGlvbjpsaXN0IiwiYXBwSW50ZWdyYXRpb246dXBkYXRlIiwiYXBwU2V0dGluZ3M6Z2V0IiwiYXBwU2V0dGluZ3M6dXBkYXRlIiwiYXNzaWdubWVudDpsaXN0IiwiYXR0YWNobWVudElkOmNyZWF0ZSJdLCJqdGkiOiIwNDJiZDUxNC0zOTkyLTVmMmEtOTY2NS0wNGU4NTUwYzQ5MmQiLCJpc3MiOiI2NDU4YTRhZTNiZWIwMTAxMjcwOWI3ZjIiLCJpYXQiOjE2ODQwNjYxMDYyMzh9.Kip5h5leVtDojhakyroL2Rh9lzBt7QF-KCSuov9zhIo'
        woztell_url = "https://bot.api.woztell.com/sendResponses?accessToken=" + token
        channel_id = '645bf628d76ad166d9fae864'


        if data['type'] == 'TEXT':
            print('phone',data['from'][1:])
            lead = request.env['incoming.leads'].search([('lead_phone_no','=',data['from'][1:])],limit=1)
            if lead and not lead.takeover:

                url = "http://62.146.183.67:6565/ask"
                print('--------------------into ask ai')
                payload = {
                    "question": data['data']['text'],
                    "phone_number":data['from']
                }
                response = requests.post(url, json=payload)
                response.raise_for_status()

                answer = response.json().get('answer')
                print('answer', answer)

                if answer:
                    formatted_answer = self.format_text(answer)

                    to_woztell = {
                        "channelId": channel_id,
                        "recipientId": lead.lead_phone_no,
                        "response": [
                            {
                                "type": "TEXT",
                                "text": formatted_answer
                            }
                        ]
                    }
                    response = requests.post(woztell_url, json=to_woztell)
                    response.raise_for_status()
                    print('chat was found',lead)
                    lead.write({

                        'chat_history': [(0, 0, {
                            'lead': data['data']['text'],
                            'agent': formatted_answer,
                            'timestamp': fields.Datetime.now(),
                            "is_send_by_user": False

                        })]
                    })


