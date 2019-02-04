# coding=utf-8

from app import components
from app.sync.model import NoteSync, TaskSync
from app.notes.model import Note
from app.tasks.model import Task


class SyncService(components.Service):

    def __init__(self, name, model, target, *args, **kwargs):
        self.name = name
        self.model_class = model
        self.target_class = target
        return super().__init__(*args, **kwargs)

    pass


noteSyncService = SyncService("noteSync", NoteSync, Note)
taskSyncService = SyncService("taskSync", TaskSync, Task)


class Module(components.Module):
    name = "sync"
    services = [noteSyncService, taskSyncService]
    models = [NoteSync, TaskSync]
    components = []


module = Module()
