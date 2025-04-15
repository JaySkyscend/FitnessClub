from email.policy import default

from PIL.ImageChops import difference, offset
from systemd.login import sessions

from odoo import models, fields , api , Command



class FitnessMember(models.Model):
    _name = 'fitness.member'
    _description = 'Fitness Club Member'
    _order = "sequence, name asc"
    _parent_store = True
    _parent_name = "parent_id"


    name = fields.Char(string="Member Name",required=True,placeholder="Enter Full Name" ,domain="[('name','like=','N%')]" )
    image = fields.Binary(string="Profile Picture")
    related_record = fields.Reference(
        selection=[('fitness.trainer','Trainer'),
                   ('res.partner','Customer')],
        string="Related Record"
    )
    age = fields.Integer(string="Age", required=True)
    weight = fields.Float(string="Weight (kg)",digits=(6,3))
    active = fields.Boolean(string="Active", default=True)
    performance_score = fields.Float(string="Performance Score")
    amount = fields.Monetary(string="Membership Fee",currency_field="currency_id")
    currency_id = fields.Many2one('res.currency',string="Currency",default=lambda self: self.env.ref('base.CAD').id , required = "amount")
    trainer_id = fields.Many2one('fitness.trainer',string="Assigned Trainer",ondelete="restrict",index=True)
  #  domain = "[('name','like','S%')]

    is_leader = fields.Boolean(string="IS Leader")


    session_count = fields.Integer(string="Session Count",compute="_compute_session_count")

    session_ids = fields.One2many('fitness.session','member_id',string="Sessions")

    # Float fields to store the total values from all One2many records
    total_session_value = fields.Float(string="Total Session Value",compute="_compute_totals",store=True)
    total_computed_value = fields.Float(string="Total Computed Value",compute="_compute_totals",store=True)

    final_score = fields.Integer(string="Final Score",compute="_compute_final_score",store=True)

    equipment_ids = fields.Many2many('fitness.equipment','fitness_member_equipment_rel','member_id','equipment_id',string="Used Equipment",domain=[('equipment_type','=','strength')])
    address = fields.Text(string="Address")
    health_details = fields.Html(string="Health Details",)
    join_date = fields.Date(string='Join Date',default=fields.Date.today(),index=True)
    last_visit = fields.Datetime(string="Last Visit")
    membership_type = fields.Selection([
        ('bronze','Bronze'),
        ('silver','Silver'),
        ('gold','Gold'),
        ('platinum','Platinum')
    ], string="Membership Type", default='bronze' )

    workout_duration = fields.Integer(string="Workout Duration (Minutes)")


    #document = fields.Binary(string="Upload File")

    # to add file in database
    document = fields.Binary(string="Upload File",attachment=True)
    document_name = fields.Char(string="File Name")


    email = fields.Char(string='Email')
    website = fields.Char(string="Website",widget="url")

    priority = fields.Selection([(str(num),str(num)) for num in range(0,5)], 'Priority')
    workout_time = fields.Float(string="Workout Time (HH:MM)",help="Example: 10:30, 15:45, 9:00")

    membership_code = fields.Char(string="Membership Code",size=4)
    password = fields.Char(string="Password",password=True,copy=False)



    state = fields.Selection([
        ('draft','Draft'),
        ('pending','Pending Approval'),
        ('active','Active'),
        ('suspend','Suspend'),
        ('closed','Closed')
    ], default = 'draft')

    sequence = fields.Integer('Sequence')

    parent_id = fields.Many2one('fitness.member','Gym Leader',index=True,ondelete="set null")

    child_ids = fields.One2many('fitness.member','parent_id','Gym Members')

    parent_path = fields.Char('Parent Path',index=True)

    def activate(self):
        existing_members = self.exists()
        if existing_members:
            existing_members.write({'state':'active','active':True})


    def deactivate(self):
        self.write({'state':'draft','active':False})


    # def action_save(self):
    #     return True
    #
    # def action_cancel(self):
    #     return {'type':'ir.actions.act_window_close'}


    def action_set_pending(self):
        self.write({'state':'pending'})

    def action_approve(self):
        self.write({'state':'active'})

    # def action_suspend(self):
    #     self.write({'state':'suspend'})

    def action_suspend(self):
        self.write({'state':'suspend'})

    def action_close(self):
        self.write({'state':'closed'})



    @api.depends('session_ids.total_value','session_ids.computed_value')
    def _compute_totals(self):
        print("Environment",self.env)
        for record in self:
            record.total_session_value = sum(record.session_ids.mapped('total_value'))
            record.total_computed_value = sum(record.session_ids.mapped('computed_value'))

    @api.depends('total_session_value','total_computed_value')
    def _compute_final_score(self):
        for record in self:
            record.final_score = int(record.total_session_value - record.total_computed_value)


    @api.model
    def print_environment_info(self,*args,**kwargs):
            print("\n========Environment Info=======")
            print(self.env)
            cr = self.env.cr
            print("Cursor",cr)
            cr.execute("select name , age from fitness_member")
            record = cr.fetchone()
            print("Fetch one Record",record)
            records = cr.fetchall()
            print("Fetch all records",records)
            cr.execute("select name from fitness_trainer")
            desc = [d.name for d in cr.description]
            dict_record = dict(zip(desc, cr.fetchone()))
            print("Print Dictionary",dict_record)
            cr.execute("select name from fitness_trainer")
            dict_records = [dict(zip(desc,row)) for row in cr.fetchall()]
            print("fetch all Records in list of dictionary",dict_records)

            cr.execute("Update fitness_trainer set name='Vipul Dubey' where id=1")
            print("Updated Records")

            cr.execute("delete from fitness_member where id = 1")
            print("Delete Record")

            user = self.env.user
            print("User",user)

            current_company = self.env.company
            print("Current_company",current_company)

            selected_companies = self.env.companies
            print("Selected Companies",selected_companies)

            lang = self.env.lang
            print("Language",lang)

            context = self.env.context
            print("Context",context)

            # user_id = fields.Many2one('res.users',default=lambda self: self.env.user)
            # print("User Id", user_id)


            partner_obj = self.env['res.partner']
            print("Another Model Object",partner_obj)

            models = list(self.env.registry.models)
            print("Models",models)

            objects = list(self.env.registry.models.values())
            print("Objects",objects)

            models_and_objects = [(name,obj) for name, obj in self.env.registry.models.items()]
            print("Models and Object",models_and_objects)


            view = self.env.ref('base.view_partner_form')
            print("View",view)

            action = self.env.ref('base.action_partner_form')
            print("Action",action)

            menu = self.env.ref('FitnessClubERP.menu_fitness_members')
            print("Menu",menu)

            group = self.env.ref('base.group_user')
            print("Group Name:",group.name)

            access_rule = self.env.ref('FitnessClubERP.access_fitness_user')
            print("Access Rule Name:",access_rule.name)

            admin_user = self.env.ref('base.user_admin')
            print("Admin User:",admin_user.name)


            base_company = self.env.ref('base.main_company')
            print("Company Name:",base_company)


            # what is self
            # self refers to the current recordset on which a method is being executed.
            # it's like this in other programming languages.


            blank_rs = self.env['res.partner']
            print("Blank recordset",blank_rs)


            members = self.env['fitness.member'].search([])
            for rec in members:
                rec.ensure_one()
                print("Iterate single Recordset")
                print("Name:",rec.name)
                break


            print("Fetch Normal Field from recordset")
            for member in members:
                print("Name:",member.name)
                print("Age:",member.age)


            print("Fetch Relational Field from recordset")
            print("Trainer_id",members.trainer_id)

            print("Multile record recordset")
            equipment_names = members.mapped('equipment_ids').mapped('name')
            print("Equipments:",equipment_names)

            print("Ensure_one():",member.ensure_one().name)
            print("Ensure_one() for multiple record raise single ton error")

            mtdt = member.get_metadata()
            print("Metadata:",mtdt)

            mtdt_multiple = members.get_metadata()
            print("Metadata for multiple",mtdt_multiple)



            def is_adult(member):
                return member.age < 30
            adult = members.filtered(is_adult)
            print("Adult",adult)

            # with lambda function
            adult_members = members.filtered(lambda m: m.age < 30)
            print("Adult members:",adult_members)

            not_adult_member = members.filtered(lambda m:  not m.age < 30)
            print("Not Adult Member:",not_adult_member)

            gold_members = self.env['fitness.member'].search([]).filtered(lambda m:  m.membership_type == 'gold')
            print("Gold Member",gold_members)

            not_adult_member_and_gold_member = self.env['fitness.member'].search([]).filtered(lambda m: m.membership_type == 'gold' and  not m.age < 30)
            print("Not adult and gold member",not_adult_member_and_gold_member)

            member_names = members.mapped("name")
            print("Multiple record in list",member_names)

            # with lambda
            member_names_with_lambda = list(map(lambda m: m.name, members))
            print("Member names with lambda",member_names_with_lambda)

            # Get the values of multiple fields from multiple record
            # recordset for all the records in a list.
            members_info = [(m.name , m.age) for m in members]
            print("Members Info",members_info)


            results = [m.weight + m.performance_score for m in members]
            print("Result", results)

            sort_record_by_name = members.sorted('name')
            print("Sorted record by name",sort_record_by_name)

            sort_name_by_lambda = members.sorted(lambda rec : rec.name)
            print("Sort name by lambda",sort_name_by_lambda)

            sort_name_desc = members.sorted(lambda rec : rec.name, reverse=True)
            print("Sort by desending",sort_name_desc)

            # check whether a recordset containing a record is inside another recordset ot not.
            jay_rec = self.filtered(lambda rec: rec.name == 'Akash Gupta')
            print("Jay",jay_rec.name)

            res1 = jay_rec in self
            print("Checking not in self",res1)

            all_members = self.env['fitness.member'].search([])
            some_members = all_members.filtered(lambda m : m.age < 30)

            res = some_members > all_members
            print("Some member is subset of all member",res)

            res1 = all_members > some_members
            print("All member is superset of some member",res1)

            senior_members = self.env['fitness.member'].search([('age', '>', 40)])
            union = gold_members | senior_members
            for m in union:
                print("Union Member",m.name)

            blank_recordset = member.browse([])

            young_member = member.search([('age', '<', 30)])
            union_recordset = blank_recordset  | young_member | gold_members
            print("Union recordset",union_recordset)

            intersection_recordset = gold_members & senior_members
            print("Intersection recordset",intersection_recordset)

            difference_recordset = gold_members - intersection_recordset
            print("Difference recordset",difference_recordset)



            # print("User:",self.env.user)
            # print("User Id",self.env.uid)
            # print("Context:",self.env.context)
            # print("Current Company:",self.env.company.name)
            # print("All Companies:",self.env.companies.mapped('name'))
            # print("Cursor (cr):",self.env.cr)
            # print("Registry:",self.env.registry)
            # # alt = self.env.ref('fitness.action_fitness_member')
            # # print("Reference",alt)
            # mdls = self.env.values()
            # print("Model",mdls)
            # mdls_n_objs = list(self.env.items())
            # print("Items",mdls_n_objs)
            # print("member",FitnessMember)
            # # member = self.env['fitness.member'].search([]).exists()
            # # if member:
            # #     print("Existing member:",member)
            # # else:
            # #     print("No valid members found.")
            # # member = self.browse([1]).exists()
            # # print(member.ensure_one().name)
            # # mtdt = self.get_metadata()
            # # print("Metadata",mtdt)
            # members = self.env['fitness.member'].search([])
            # first_three = members[:3]
            # print("First Three",first_three)
            # last_one = members[-1]
            # print("Last one",last_one)
            # adult_members = members.filtered(lambda m: m.age < 30)
            #
            # for member in adult_members:
            #     print(member.name,member.age)
            # gold_members = self.env['fitness.member'].search([]).filtered(lambda m: not m.membership_type == 'gold')
            # print("Gold Member",gold_members)
            # member_name = self.env['fitness.member'].search([]).mapped(lambda rec:(rec.id ,rec.name))
            # print("Mapped",member_name)
            # session_total = member.session_ids.mapped('total_value')
            # print(session_total)
            # sorted_records = self.env['fitness.member'].search([]).sorted(key=lambda r:r.name , reverse=True)
            # print("Sorted records",sorted_records)
            # sorted_by_session_count = members.sorted(key=lambda m: len(m.session_ids))
            # print("Count",sorted_by_session_count)
            # all_member = self.env['fitness.member'].search([])
            # active_member = all_member.filtered(lambda m:m.active)
            #
            # if active_member <= all_member:
            #     print("Active member are a subset of all members.")
            #
            # member1 = self.env['fitness.member'].browse(1)
            # print("Browse Member",member1)
            # data = member1.read(['name','age'])
            # print("Data from read",data)

            # senior_members = self.env['fitness.member'].search(['age', '>', 40])
            # print("Senior Members:",senior_members.mapped('name'))

            # combined = gold_members | senior_members
            # for m in combined:
            #     print(m.name)


    def action_create_member(self):
        self.env['fitness.member'].create({
            'name':'Virendra Gandhi',
            'age': 35,
            'weight' : 75.8,
            'active' : True,
            'performance_score': 10,
            'amount' : 15000,
            'currency_id': self.env.ref('base.CAD').id,
            'trainer_id':3,
            'address':'Shahibaug, Ahmedabad',
            'health_details':'<p>Sugar Problem</p>',
            'join_date':fields.Date.today(),
            'last_visit':fields.Datetime.now(),
            'membership_type':'silver',
            'workout_duration':120,
            'session_ids': [
                ( 0, 0, {
                    'name': 'Strength Exercise',
                    'duration':2.0,
                    'calories_burned':750,
                    'heart_rate_avg':120,
                    'distance_covered':5.0,
                    'notes':'Focus on upper body',
                }),
                ( Command.create({
                   'name':'Cardio Blast',
                    'duration':1.0,
                    'calories_burned':400,
                    'heart_rate_avg': 110,
                    'distance_covered':3.0,
                    'notes':'high-intensity interval session',
                }))
            ],
            # 'equipment_ids':[
            #     (4,6),
            #     (4,7),
            #     Command.link(3),
            # ]

             'equipment_ids':[(6,0,[1,2,3,4,5,6])]
            #'equipment_ids': Command.set([3, 6, 7]),
        })



        """Create new fitness.equipment records from member model"""
        equipment_obj = self.env['fitness.equipment']
        equipment_vals_lst = [
            {
                'name': 'Shoulder Machine',
                'equipment_type': 'strength',
            },
            {
                'name': 'Leg machine',
                'equipment_type': 'strength'
            },
        ]
        new_equipment = equipment_obj.create(equipment_vals_lst)
        print("New Equipment",new_equipment)


    def action_update_member(self):

       self.write({
            'name': 'Grisha Pandit',
            'age': 30,

        })

       # equipmemt_obj = self.env['fitness.equipment'].search([
       #     ('name','in',['Shoulder Machine','Leg Machine'])
       # ])

       equipment_obj = self.env['fitness.equipment'].search([('name','in',['Shoulder Machine','Leg Machine'])])

       for equipment in equipment_obj:

           equipment.new_rec = 'Cardio' if equipment.name == 'Shoulder Machine' else 'Strength'

          # equipment_update = equipment.write()
           print("Record Created",equipment_obj)




    def action_update_session(self):
        self.ensure_one()

        updates = [
            (1, 4, {
                'name':'Updated HIIT Session',
                'duration':2.0,
            }),
            Command.update(7,{
                'name':'Updated Strength Session',
                'duration':1.3,

            }),
            (0,0, {
                 'name':'Zumba Session',
                 'duration':1.5,
                 'notes':'Flexibility workout'
            }),
            Command.create({
                'name':'Meditation Session',
                'duration':0.5,
                'notes':'Calm and focused breathing',
            }),
        ]

        self.write({
            'session_ids': updates
        })






    def action_delete_member_session(self):

        #  Update the O2M field and delete an existing record
        # making sure it is deleted from the comodel’s table as
        # well.(Use both no and Command operation)

        if self and self.session_ids:
            session_to_delete = self.session_ids[:1]
            self.write({
                'session_ids': [(2, session_to_delete.id, 0)]
            })
            print(f"Deleted session with ID {session_to_delete.id} for {self.name}")
        else:
            print("No sessions found or member not available.")





    def action_unlink_sessions(self):

        """  Update the O2M field and delete an existing record
  making sure it is not deleted from the comodel’s table
  as well.(Use both no and Command operation)  """



        if self :


            new_session_data = {
                'name':'New Session',
                'duration': 45
            }

            unlink_commands = [(3, session.id, 0) for session in self.session_ids]

            update_command = unlink_commands + [(0 ,0 , new_session_data)]

            self.write({
                'session_ids': update_command
            })
            print(f"Unlinked {len(unlink_commands)} sessions and added a new one for {self.name} (sessions still exist in DB)")
        else:
            print("No sessions found or member doesn't exist.")



    def action_add_existing_equipment(self):

        """ Update the O2M field and link an existing record from
the comodel.(Use both no and Command operation) """


        self.ensure_one()
        #
        # operations = [
        #     (4,11),
        #     Command.link(11),
        # ]
        #
        # self.write({
        #     'session_ids': operations
        # })


        """" Update M2M field to link a value keeping existing
values as it is in the M2M field. """

        # equipment_id = 7
        #
        # self.write({
        #     'equipment_ids':[
        #         (4, equipment_id)
        #     ]
        #         })

        """" Update M2M field to remove existing values and add
new values. """


        new_equipment_ids = [7,4]

        self.write({
            'equipment_ids': [
                #(6 , 0, new_equipment_ids),
                 Command.set(new_equipment_ids)
            ]
        })





    def action_remove_all_equipment(self):

        """ Remove all the records from the O2M field.(Use both
          no and Command operation)  """

        self.ensure_one()

        # self.write({
        #     'session_ids':  [
        #         # (5,0,0),
        #         Command.clear()
        #     ]
        # })


        """ Update M2M field to remove all values.  """

        self.write({'equipment_ids':[(5,0,0)]})
        print(f"All equipment removed for {self.name}")




    def action_replace_all_equipment(self):
           # self.ensure_one()
           #
           # new_sessions = self.env['fitness.session'].search([('name','in',['Zumba Session','Meditation Session'])])
           #
           # self.write({
           #     'session_ids': [
           #         # (6,0, new_sessions.ids)
           #          Command.set(new_sessions.ids)
           #     ]
           # })

            # self.write({
            #     'equipment_ids': [(6, 0,[1,2,3,4])]  # ✅ Use .ids
            # })
            # print(f"Replaced all equipment for {self.name}")
            #


          """  Update a compute field using inverse in the field’s
          definition. """

          for member in self:
             # for record in self:
                if member.id == 11:
                    sessions.total_session_value = 100


 #  def copy_read(self):

     #  """ Duplicate a Record of the Current Model """
        #  new_rec = self.copy()
       # print("New Rec",new_rec)


       # """ Duplicate Multiple Records of the Current Model """
       # duplicates = self.copy_data()
       # for vals in duplicates:
       # self.env['fitness.member'].create(vals)

   #    """  Duplicate a Record and Copy its O2M Field Too """
       # duplicate = self.copy({
       #     'session_ids': [( 0 ,0, {
       #         'name': session.name,
       #         'duration': session.duration,
       #         'notes': session.notes,
       #     }) for session in self.session_ids]
       # })

     #  """ Duplicate a Record But Prevent Certain Fields from Being Copied """

    # def copy_read(self, default=None):
    #     default = dict(default or {})
    #     default['age'] = 0
    #     default['trainer_id'] = False
    #     return super().copy(default)


    def copy_read(self):
        for rec in self:
            # default = {
            #      'name': rec.name + ('Copy')
            #    }
            # new_rec = rec.copy(default=default)

            default = {
                'name': 'New Duplicate Name',
                'age': self.age + 1,

            }
            new_rec = rec.copy(default=default)
            print("New Rec",new_rec)

    def delete_record(self):
        self.unlink()
        res_8 = self.browse([8,32])
        res_8.unlink()
        equipment_obj = self.env['fitness.equipment'].browse(4)
        equipment_obj.unlink()
        print("Delete Equipment",equipment_obj)


    def search_record(self):
        all_records = self.search([])
        print("All records",all_records)
        age_records = self.search([('age', '>', 25)])
        print("Age Greate than 25",age_records)
        cardio_trainer = self.env['fitness.trainer'].search([('expertise','=','Cardio')])
        print("Another model",cardio_trainer.name)
        skip_initial = self.search([], offset=3)
        print("Skip initial",skip_initial)
        five_members = self.search([],limit=5)
        print("Five member",five_members)
        sorted_by_name = self.search([], order='name')
        print("Sorted by name",sorted_by_name)
        sorted_by_date_desc = self.search([], order='join_date desc')
        print("Sorted by reverse date", sorted_by_date_desc)
        records = self.search([('age','>=',25)],
                               offset=2,
                                limit=5,
                                 order='name desc')
        print("Records by all parameter",records)

        # age_less_records = self.search([('age', '<', 25)])
        # print("Age less than 25",age_less_records)
        # display_3_records = self.search([],limit=3)
        # print("Display 3",display_3_records)
        #
        #
        # all_cond_recs = self.search([],offset=2,limit=3,order='name')
        # print("All condition",all_cond_recs)
        # count = self.search_count([('age','>',25)])
        # print("Count Age > 25",{count})
        # search_count_1 = self.search_count([])
        # print(search_count_1)
        # search_read_records = self.search_read(domain=[('age','<', 25)],fields=['name','active','trainer_id'])
        # print("Search read records",search_read_records)
        # offset_recs = self.search_read(fields=['name','active','trainer_id'],offset=5)
        # print("Offset",offset_recs)
        # read_group_record = self.read_group(domain=[('age', '<', 25)],fields=['session_ids'],groupby=['trainer_id'],lazy=True)
        # print("Read Group Records",read_group_record)


    @api.depends('session_ids')
    def _compute_session_count(self):
        for rec in self:
            rec.session_count = len(rec.session_ids)

    def action_view_session(self):
        self.ensure_one()
        return {
            'type':'ir.actions.act_window',
            'name':'Session',
            'view_mode':'list,form',
            'res_model':'member.session',
            'domain':[('member_id','=',self.id)],
            'contex':{'default_member_id':self.id}
        }


    def browse_record(self):
        member1 = self.env['fitness.member']
        print("Browse Member",member1.browse(1))
        many_member = self.env['fitness.member'].browse([4,5,6])
        print("Many Member",many_member)

        trainer_obj = self.env['fitness.trainer']
        trainer_1 = trainer_obj.browse(1).name
        print("Trainer1",trainer_1)
        trainer_many = trainer_obj.browse([2,3,4])
        print("trainer many",trainer_many)


        all_fields = member1.browse(11).read()[0]
        print("All fields",all_fields)

        specific_field = member1.browse(11).read(['name'])
        print("Specific field",specific_field)

        date_field = member1.browse(11).read(['join_date','last_visit','trainer_id','equipment_ids','session_ids','related_record'])
        print("Date & many field",date_field)

        read_another = trainer_obj.browse(1).read(['name'])
        print("Another model",read_another)

        records = self.env['fitness.member'].browse([11, 33, 29])  # Example record IDs
        data = records.read(['trainer_id'])

        for record in data:
            print("Trainer ID:", record['trainer_id'])

