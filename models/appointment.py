from odoo import models, fields, api, _
from markupsafe import Markup
import requests
import re


class Appointment(models.Model):
    _name = 'appointment.model'
    _description = 'Appointments'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _inherits = {'res.partner': 'partner_id'}

    partner_id = fields.Many2one('res.partner',string = 'Assigned Agent', tracking = True)
    incoming_id = fields.Many2one('incoming.leads', string='Incoming Lead')
    appointment_date = fields.Datetime(string='Appointment Date')
    state = fields.Selection([('draft','Draft'),('confirmed','Confirmed'),('completed','Completed'),('cancelled','Cancelled')],string = 'State')
    insurance_provider = fields.Many2one('insurance.provider',string= 'Insurance Provider')
    doctor = fields.Many2one('doctor.model',string= 'Doctor')
    clinic = fields.Many2one('clinic.model',string= 'Clinic')
    reason_for_visit = fields.Text(string = 'Reason')

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

class Doctor(models.Model):
    _name = 'doctor.model'
    _description = 'Doctor'

    name =fields.Char(string='Doctor')
class Clinic(models.Model):
    _name = 'clinic.model'
    _description = 'Clinic'

    name =fields.Char(string='Clinic')
class InsuranceProvider(models.Model):
    _name = 'insurance.provider'
    _description = 'Insurance'

    name =fields.Char(string='Insurance Provider')
