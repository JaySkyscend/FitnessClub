from odoo import models, fields

class FitnessCertification(models.Model):
    _name = 'fitness.certification'
    _description = 'Trainer Certification'


    name = fields.Char(string="Certification Name",required=True)
    authority = fields.Char(string="Issued By")
    validity =fields.Char(string="Validity (years)")
    color_index = fields.Integer('Color')

