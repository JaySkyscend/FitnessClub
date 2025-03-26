

from odoo import models, fields

class FitnessMember(models.Model):
    _name = 'fitness.member'
    _description = 'Fitness Club Member'
    _order = "name asc"


    name = fields.Char(string="Member Name",required=True,placeholder="Enter Full Name")
    age = fields.Integer(string="Age", required=True)
    weight = fields.Float(string="Weight (kg)",digits=(6,3))
    trainer_id = fields.Many2one('fitness.trainer',string="Assigned Trainer",ondelete="restrict")
    session_ids = fields.One2many('fitness.session','member_id',string="Sessions")
    equipment_ids = fields.Many2many('fitness.equipment','fitness_member_equipment_rel','member_id','equipment_id',string="Used Equipment")
    is_active = fields.Boolean(string="Active",default=True)
    address = fields.Text(string="Address")
    health_details = fields.Html(string="Health Details",)
    join_date = fields.Date(string='Join Date',default=fields.Date.context_today,index=True)
    last_visit = fields.Datetime(string="Last Visit")
    membership_type = fields.Selection([
        ('bronze','Bronze'),
        ('silver','Silver'),
        ('gold','Gold'),
        ('platinum','Platinum')
    ], string="Membership Type", default='bronze' )

    state = fields.Selection([
        ('draft','Draft'),
        ('confirmed','Confirmed'),
        ('done','Done')
    ], string="Status",default='draft',tracking=True)

    email = fields.Char(string='Email')
    website = fields.Char(string="Website",widget="url")

    priority = fields.Selection([(str(num),str(num)) for num in range(0,5)], 'Priority')
    workout_time = fields.Float(string="Workout Time (HH:MM)",help="Example: 10:30, 15:45, 9:00")

    membership_code = fields.Char(string="Membership Code",size=4)
    password = fields.Char(string="Password",password=True)

    def activate(self):
        self.write({'state':'confirmed','active':True})

    def deactivate(self):
        self.write({'state':'draft','active':False})


    def action_save(self):
        return True

    def action_cancel(self):
        return {'type':'ir.actions.act_window_close'}