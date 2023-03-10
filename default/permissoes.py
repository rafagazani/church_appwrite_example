from appwrite.permission import Permission
from appwrite.role import Role
permission_default = [
    Permission.delete(Role.team('admin')),
    Permission.update(Role.team('admin')),
    Permission.read(Role.team('admin')),
    Permission.read(Role.users()),
    Permission.update(Role.users()),
]
apenas_admins = [
    Permission.delete(Role.team('admin')),
    Permission.update(Role.team('admin')),
    Permission.read(Role.team('admin')),
    Permission.create(Role.team('admin')),
]
admin_owner = [
    Permission.delete(Role.team('admin',role='owner')),
    Permission.update(Role.team('admin',role='owner')),
    Permission.read(Role.team('admin', role='owner')),
    Permission.write(Role.team('admin', role='owner')),
               Permission.read(Role.team('admin', role='owner'))]

leitura = [
    Permission.delete(Role.team('admin')),
    Permission.update(Role.team('admin')),
    Permission.read(Role.team('admin')),

    Permission.read(Role.users())
]

todos = [
        Permission.update(Role.users()),
        Permission.delete(Role.users()),
        Permission.read(Role.users())
         ]

role_team_admin =[Role.team('admin')]

role_team_admin_owner =[Role.team('admin', role='owner')]