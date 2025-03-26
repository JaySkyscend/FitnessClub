

from odoo import models, fields , api

class FitnessMember(models.Model):
    _name = 'fitness.member'
    _description = 'Fitness Club Member'
    _order = "sequence, name asc"


    name = fields.Char(string="Member Name",required=True,placeholder="Enter Full Name")
    image = fields.Binary(string="Profile Picture")
    related_record = fields.Reference(
        selection=[('fitness.trainer','Trainer'),
                   ('res.partner','Customer')],
        string="Related Record"
    )
    age = fields.Integer(string="Age", required=True)
    weight = fields.Float(string="Weight (kg)",digits=(6,3))
    performance_score = fields.Float(string="Performance Score")
    amount = fields.Monetary(string="Membership Fee",currency_field="currency_id")
    currency_id = fields.Many2one('res.currency',string="Currency",default=lambda self: self.env.ref('base.CAD').id)
    trainer_id = fields.Many2one('fitness.trainer',string="Assigned Trainer",ondelete="restrict",index=True)
    session_ids = fields.One2many('fitness.session','member_id',string="Sessions")

    # Float fields to store the total values from all one2many records
    total_session_value = fields.Float(string="Total Session Value",compute="_compute_totals",store=True)
    total_computed_value = fields.Float(string="Total Computed Value",compute="_compute_totals",store=True)

    final_score = fields.Integer(string="Final Score",compute="_compute_final_score",store=True)

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

    workout_duration = fields.Integer(string="Workout Duration (Minutes)")
 #   document = fields.Binary(string="Upload File")

    # to add file in database
    document = fields.Binary(string="Upload File",attachment=True)
    document_name = fields.Char(string="File Name")


    email = fields.Char(string='Email')
    website = fields.Char(string="Website",widget="url")

    priority = fields.Selection([(str(num),str(num)) for num in range(0,5)], 'Priority')
    workout_time = fields.Float(string="Workout Time (HH:MM)",help="Example: 10:30, 15:45, 9:00")

    membership_code = fields.Char(string="Membership Code",size=4)
    password = fields.Char(string="Password",password=True)



    state = fields.Selection([
        ('draft','Draft'),
        ('pending','Pending Approval'),
        ('active','Active'),
        ('suspend','Suspend'),
        ('closed','Closed')
    ], default = 'draft')

    sequence = fields.Integer('Sequence')

    parent_id = fields.Many2one('fitness.member','Gym Leader')

    child_ids = fields.One2many('fitness.member','parent_id','Gym Members')

    parent_path = fields.Char('Parent Path',index=True)

    def activate(self):
        self.write({'state':'confirmed','active':True})

    def deactivate(self):
        self.write({'state':'draft','active':False})


    def action_save(self):
        return True

    def action_cancel(self):
        return {'type':'ir.actions.act_window_close'}

    @api.depends('session_ids.total_value','session_ids.computed_value')
    def _compute_totals(self):
        for record in self:
            record.total_session_value = sum(record.session_ids.mapped('total_value'))
            record.total_computed_value = sum(record.session_ids.mapped('computed_value'))

    @api.depends('total_session_value','total_computed_value')
    def _compute_final_score(self):
        for record in self:
            record.final_score = int(record.total_session_value - record.total_computed_value)
