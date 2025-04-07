from odoo import models, fields, api, _
from markupsafe import Markup
import requests
import re
import json


class MessageTemplate(models.Model):
    _name = 'message.template'
    _description = 'Customized Messages'
    _rec_name = "template_name"

    name = fields.Selection([('message_template','Message Template'),('WHATSAPP_LIST','List Message'),('reply_button','Reply Button'),('img','Image')],string='Template Type')
    template_name = fields.Char(string='Template Name')

    #WHATSAPP_LIST
    header =fields.Text(string='Header')
    title =fields.Text(string='Title')
    button_title = fields.Text(string ='Button-Title')
    buttons = fields.One2many('buttons','msg_list',string = 'Buttons')
    computed_json =  fields.Html(sanitize=False)
    html_preview =  fields.Html(sanitize=False)
    section_title = fields.Text(string= 'Section Title')

    @api.onchange('name','header','title','button_title','buttons','section_title')
    def compute_templates(self):
        for rec in self:
            if rec.name == 'WHATSAPP_LIST':
                rec.whatsapp_list_template()
    def whatsapp_list_template(self):

        for rec in self:
            rows = []
            for button in rec.buttons:
                rows.append({
                    "title": button.title,
                    "payload":  button.title
                })
            whatsapp_list = {
                "type": rec.name,
                "body": {
                    "text": rec.title
                },
                "action": {
                    "button": rec.button_title,
                    "sections": [
                        {
                            "title": rec.section_title,
                            "rows":  rows
                        }
                    ]
                },
                "header": {
                    "type": "text",
                    "text": rec.header
                },
            }

            temp = json.dumps(whatsapp_list, ensure_ascii=False, indent=4)
            rec.computed_json = temp
            return None

    @api.onchange('computed_json')
    def generate_whatsapp_preview_html(self):
        for rec in self:
            if rec.name == 'WHATSAPP_LIST':

                rows_html = ""
                for button in rec.buttons:
                    rows_html += f"""
                <button class="option-button">{button.title}</button>
                    """

                style = """
<!DOCTYPE html>
<html dir="rtl">
<head>
<meta charset="UTF-8">
<style>
body {
  font-family: 'Segoe UI', Tahoma, Arial, sans-serif;
  background-color: #f0f1f2;
  margin: 0;
  padding: 10px;
}

.whatsapp-message {
  max-width: 280px;
  margin: 0 auto;
}

.header-section {
  background-color: #e1f5e9;
  border-radius: 7px 7px 0 0;
  padding: 12px 15px;
  border-bottom: 1px solid #d7eae0;
}

.header-text {
  color: #075e54;
  font-weight: bold;
  font-size: 14px;
}

.body-section {
  background-color: #e1f5e9;
  padding: 12px 15px;
  border-bottom: 1px solid #d7eae0;
}

.body-text {
  font-size: 14px;
}

.button-section {
  background-color: #e1f5e9;
  padding: 10px;
  text-align: center;
  border-bottom: 1px solid #d7eae0;
  border-radius: 0 0 7px 7px;
}

.action-button {
  color: #128c7e;
  font-weight: bold;
  font-size: 14px;
}

.section-header {
  background-color: #dcf8c6;
  padding: 10px 15px;
  margin-top: 8px;
  border-radius: 7px 7px 0 0;
  font-size: 13px;
  font-weight: 600;
  border-bottom: 1px solid #c5e9af;
}

.list-section {
  background-color: #dcf8c6;
  padding: 10px 15px;
  font-size: 13px;
  font-weight: 600;
  border-bottom: 1px solid #c5e9af;
}

.option-button {
  display: block;
  width: 100%;
  background-color: white;
  border: none;
  border-bottom: 1px solid #f0f0f0;
  padding: 12px 15px;
  text-align: right;
  font-size: 14px;
  font-family: inherit;
  cursor: pointer;
  outline: none;
}

.option-button:last-child {
  border-radius: 0 0 7px 7px;
}

.option-button:hover {
  background-color: #f8f8f8;
}
</style>
</head>
"""
                html_preview =f"""
<body>

<div class="whatsapp-message">
  <!-- First message box with header, body, and button -->
  <div class="header-section">
    <div class="header-text">{rec.header}</div>
  </div>
  <div class="body-section">
    <div class="body-text">{rec.title}</div>
  </div>
  <div class="button-section">
    <span class="action-button">{rec.button_title}</span>
  </div>

  <!-- Second message box with section headers and option buttons -->
  <div class="section-header">{rec.button_title}</div>
  <div class="list-section">{rec.section_title}</div>

{rows_html}
</div>

</body>
</html>

                        """

                rec.html_preview = style + html_preview


class ButtonList(models.Model):
    _name = 'buttons'
    _description = 'Buttons'

    msg_list = fields.Many2one('message.template')
    title = fields.Text(string ='Title')
