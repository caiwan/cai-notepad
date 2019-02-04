# coding=utf-8

from app import components
from app.milestones.model import Milestone


class MilestoneService(components.Service):
    name = "milestones"
    model_class = Milestone

    pass


milestoneService = MilestoneService()


class Module(components.Module):
    name = "milestones"
    services = [milestoneService]
    models = [Milestone]
    components = []


module = Module()
