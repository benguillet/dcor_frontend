change_perms= [{'title':'Add/Change Users', 'description':'This allows users to add users to the hipercic system.'},
               {'title':'Add/Change Group', 'description':'This allows users to add groups to the hipercic system.'},
              ]
delete_perms= [{'title':'Delete Users', 'description':'Users are able to remove other users from the system.'},
               {'title':'Delete Groups', 'description':'Users are able to remove groups from the system.'},
              ]
other_perms= [{'title':'run cluster job', 'description':'text about running cluster jobs'},
             ]             

def all_perms():
    perms=change_perms+delete_perms+other_perms
    return perms



