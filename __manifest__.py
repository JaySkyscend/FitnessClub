{
    'name': 'Fitness Club ERP',
    'version':'1.0',
    'summary':'Manage Gym members, trainers , workouts, and payments efficiently',
    'author':'Jay Patel',
    'depends':['base'],
    'data':[
      'security/fitness_security.xml',
      'security/ir.model.access.csv',
      'views/fitness_member_views.xml',

    ],
    'installable':True,
    'application':True,

}
