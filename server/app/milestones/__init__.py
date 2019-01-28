from app.milestones.model import Milestone, TaggedMilestone


def init(app, api, models):
    # TBD
    models.extend([Milestone, TaggedMilestone])
