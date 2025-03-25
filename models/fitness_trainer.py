
from odoo import models, fields

class FitnessTrainer(models.Model):
    _name = 'fitness.trainer'
    _description = 'Fitness Club Trainer'


    name = fields.Char(string="Trainer Name",required=True)
    expertise = fields.Selection([
        ('yoga','Yoga'),
        ('weightlifting','WeightLifting'),
        ('cardio','Cardio'),
        ('zumba','Zumba')
    ], string="Expertise", required=True )
    phone = fields.Char(string="Phone Number")
    email = fields.Char(string="Email")

