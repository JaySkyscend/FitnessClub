


from odoo import fields,models



class FitnessSession(models.Model):
    _name = 'fitness.session'
    _description = 'Fitness Session'

    name = fields.Char(string="Session Name",required=True)
    date = fields.Date(string="Session Date",default=fields.Date.context_today,required=True)
    duration = fields.Float(string="Duration (Hours)", help="Duration in hours, eg.,1.5 for 1 hour 30 minutes")
    member_id = fields.Many2one('fitness.member',string="Member",ondelete="cascade")
    trainer_id = fields.Many2one('fitness.trainer',string="Trainer")
    notes = fields.Text(string="Notes")

    related_record = fields.Reference(
        selection=[
            ('fitness.trainer', 'Trainer'),
            ('fitness.member', 'Member'),
            ('res.partner', 'Customer')
        ],
        string="Related Record"
    )

    # three manually entered float fields
    calories_burned = fields.Float(string="Calories Burned",help="Total Calories burn during session")
    heart_rate_avg = fields.Float(string="Average Heart Rate", help="Average heart rate during session")
    distance_covered = fields.Float(string="Distance covered (km)",help="Distance covered in kilometers.")
