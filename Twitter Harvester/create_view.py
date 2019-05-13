import couchdb
import os
import re


# Create a view in couchDB, returning a dictionary with the properties of the view
def create_view (db, design_name, map_file_name, reduce_name):

    func_dir = os.path.dirname(os.path.realpath(__file__))+"/map_functions/"
    view_name = re.sub('.js', '', map_file_name)

    # Reads the map function from the directory
    map_func = open(func_dir+map_file_name, 'r').read()

    # Reduce function
    if reduce_name == None:
        # Design Doc
        design_doc = {
            '_id': '_design/'+design_name,
            'views': {
                view_name: {
                    'map': map_func
                }
            }
        }
    else:
        if reduce_name in "_count _sum _stats":
            reduce_func = reduce_name
        else:
            reduce_func = open(reduce_name+'.js','r').read()
        # Design Doc
        design_doc = {
            '_id': '_design/'+design_name,
            'views': {
                view_name: {
                    'map': map_func,
                    'reduce': reduce_func
                }
            }
        }

    try:
        db.save(design_doc)
    except couchdb.http.ResourceConflict:
        design = db["_design/"+design_name]
        db.delete(design)
        db.save(design_doc)


#sever_instance = couchdb.Server('http://127.0.0.1:5984/')
#create_view(sever_instance, 'something', 'name1111ss.js', None)