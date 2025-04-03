from odoo import models, fields, api, _



class IncomingLeads(models.Model):
    _name = 'incoming.leads'
    _description = 'Incoming Leads'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _inherits = {'res.partner': 'partner_id'}

    partner_id = fields.Many2one('res.partner',string = 'Assigned Agent', tracking = True)
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

    def whatsapp_view(self):
        # if clicked the chat interface will appear instead
        pass
    def original_lead_info(self):
        # if clicked the lead data will appear and its the default to how the data not the chat
        pass
    def action_book_appointment(self):
        # create an appointment
        pass
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
