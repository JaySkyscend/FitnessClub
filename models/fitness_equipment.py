from odoo import fields,models

class FitnessEquipment(models.Model):
    _name = 'fitness.equipment'
    _description = 'Fitness Equipment'

    name = fields.Char(string="Equipment Name",required=True)
    equipment_type = fields.Selection([
        ('cardio','Cardio Machine'),
        ('strength','Strength Machine'),
        ('flexibility','Flexibility Equipment'),
        ('free_weights','Free Weights')
    ], string="Equipment Type",required = True)
    purchase_date = fields.Date(string="Purchase Date")
    maintenance_date =fields.Date(string="Last Maintenance Date")
     
