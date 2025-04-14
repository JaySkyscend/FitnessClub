{
    'name': 'Fitness Club ERP',
    'version':'1.0',
    'summary':'Manage Gym members, trainers , workouts efficiently',
    'author':'Jay Patel',
    'depends':['base'],
    'data':[
      'security/fitness_security.xml',
      'security/ir.model.access.csv',
      'views/fitness_member_views.xml',
      'views/fitness_trainer_view.xml',
      'views/fitness_session_views.xml',
      'views/fitness_equipment_views.xml',
      'views/fitness_certification_views.xml',
    ],
    'installable':True,
    'application':True,

}
