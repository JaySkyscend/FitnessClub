
from odoo import fields,models,api



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

    # Computed fields ( not store in database)
    total_value = fields.Float(string="Total Value",compute="_compute_values",store=False)
    computed_value = fields.Float(string="Computed Value",compute="_compute_values",store=False)

    progress_percentage = fields.Integer(string="Completion %",compute="_compute_percentage",store=False)
    @api.depends('calories_burned','heart_rate_avg','distance_covered')
    def _compute_values(self):
        for record in self:
            record.total_value = (record.calories_burned or 0) + (record.heart_rate_avg or 0) + (record.distance_covered or 0)
            record.computed_value = (record.calories_burned or 0 ) + (record.distance_covered or 0 ) - (record.heart_rate_avg or 0)

    @api.depends('total_value','computed_value')
    def _compute_percentage(self):
        for record in self:
            if record.total_value:
                record.progress_percentage = int((record.computed_value / record.total_value) * 100)
            else:
                record.progress_percentage = 0
