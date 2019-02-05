# coding=utf-8

from app import components
from app.notes.attachments.model import NoteAttachment


class AttachmentService(components.Service):
    name = "attachment"
    model_class = NoteAttachment
    pass


attachmentService = AttachmentService()


class Module(components.Module):
    name = "attachment"
    services = [attachmentService]
    models = [NoteAttachment]
    controllers = []


module = Module()
