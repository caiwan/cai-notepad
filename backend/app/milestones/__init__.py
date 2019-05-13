# coding=utf-8

from app import components
from app.milestones.model import Milestone, TaggedMilestone


class MilestoneService(components.Service):
    name = "milestones"
    model_class = Milestone
    pass


milestoneService = MilestoneService()


class Module(components.Module):
    from app.milestones.controller import MilestoneController, MilestoneListController
    name = "milestones"
    services = [milestoneService]
    models = [Milestone, TaggedMilestone]
    components = [MilestoneController, MilestoneListController]


module = Module()
