
from odoo import models, fields



class FitnessTrainer(models.Model):
    _name = 'fitness.trainer'
    _description = 'Fitness Club Trainer'
    _parent_name = "supervisor_id"
    _parent_store = True
    _order = "parent_path, name"


    name = fields.Char(string="Trainer Name",required=True)
    supervisor_id = fields.Many2one('fitness.trainer',string='Supervisor',ondelete="set null",index=True)

    parent_path = fields.Char(index=True)

    expertise = fields.Selection([
        ('yoga','Yoga'),
        ('weightlifting','WeightLifting'),
        ('cardio','Cardio'),
        ('zumba','Zumba')
    ], string="Expertise", required=True )
    phone = fields.Char(string="Phone Number")
    email = fields.Char(string="Email")

    certification_ids = fields.Many2many(
        'fitness.certification', # Related model
        'trainer_certification_rel',   # Custom table name
        'trainer_ref_id',              # Custom column for fitness.trainer
        'certification_ref_id', # Custom column for fitness.certification
                 string="Certifications"
    )
