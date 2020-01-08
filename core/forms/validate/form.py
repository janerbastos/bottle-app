class Form(object):

    def __init__(self, form, Class, instance=None):
        self.form = form
        self.instance = instance
        self.Class = Class

    def load_data(self, fields):
        data = {}
        for field in fields:
            data[field] = self.form.get(field)
        return data

    def save(self, fields):
        data = self.load_data(fields)
        print(data)
        model = self.Class(**data)
        return model

    def is_valid(self):
        pass


def required_field(form, requiride):
    messages = {}
    for field in requiride:
        value = form.get(field)
        if value is "" or value is None:
            messages[field] = "Você deve inserir um valor para <strong>%s</strong> no formulário" % field
    return messages