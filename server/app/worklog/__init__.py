# coding=utf-8

from app import components
from app.worklog.model import Worklog, WorklogDurationCache


class WorklogService(components.Service):
    name = "worklog"
    model_class = Worklog
    settings = {
        "default_pomodoro_times": [
            [25, 5, 25, 5, 25, 15],
            [45, 15, 45, 15],
            [90, 15]
        ]
    }
    pass


worklogService = WorklogService()


class Module(components.Module):
    from app.worklog.controller import WorklogController, WorklogListController
    name = "worklog"
    services = [worklogService]
    models = [Worklog, WorklogDurationCache]
    controllers = [WorklogController, WorklogListController]


module = Module()
