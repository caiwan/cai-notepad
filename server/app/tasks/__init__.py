import sys

from flask import request
import components

import mongoengine


## -- model

class Task(components.BaseModel):
    title = mongoengine.StringField(max_length=512)
    completed = mongoengine.BooleanField(default=False)    
    pass


# --- controllers

class TaskListController(components.Controller):
    path = "/tasks/"

    def get(self):
        tasks_json = [task.to_mongo() for task in Task.objects(is_deleted=False)]
        return(tasks_json, 200) 

    def post(self):
        task_json = request.json
        if '_id' in task_json:
            del task_json['_id']

        task = components.BaseModel.update_document(Task(), task_json)
        task.save()
        
        return (task.to_mongo(), 201)

    pass

class TaskController(components.Controller):
    path = "/tasks/<string:task_id>/"

    def get(self,task_id):
        try: 
            task = Task.objects.get(_id=mongoengine.fields.ObjectId(task_id), is_deleted=False)
            return (task.to_mongo(), 200)

        except Task.DoesNotExist as e:
            return({"error" : [str(e)]}, 404)
        except e:
            return({"error" : [str(e)]}, 500)

        return ('', 204)

    def put(self,task_id):
        task_json = request.json
        if '_id' in task_json:
            del task_json['_id']
        try: 
            task = Task.objects.get(_id=mongoengine.fields.ObjectId(task_id), is_deleted=False)
            components.BaseModel.update_document(task, task_json)
            # TODO: update modification date here 
            task.save()
            return (task.to_mongo(), 200)
        except Task.DoesNotExist as e:
            return({"error" : str(e)}, 404)
        except :
            return({
                "error" : [str(err) for err in sys.exc_info()]
            }, 500)
        return ('', 204)

    def delete(self,task_id):
        try: 
            task = Task.objects.get(_id=mongoengine.fields.ObjectId(task_id), is_deleted=False)
            task.is_deleted = True
            task.save()
        except Task.DoesNotExist as e:
            return({"error" : [str(e)]}, 404)
        except e:
            return({"error" : [str(e)]}, 500)

        return ('', 204)

    pass


def init(app, api, model_target):
    components.register_controllers(api, [TaskController, TaskListController])
