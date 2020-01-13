class Form(object):

    fields = []

    def __init__(self, form, Class, instance=None):
        self.form = form
        self.instance = instance
        self.Class = Class
        self.errors = None
        self.data = None

    def load_data(self):
        self.data = {}
        for field in self.fields:
            self.data[field] = self.form.get(field)

    def save(self):
        self.load_data()
        model = self.Class(**self.data)
        return model

    def is_valid(self):
        self.errors = {}
        for field in self.fields:
            value = self.form.get(field)
            if value is "" or value is None:
                self.errors[field] = "Você deve inserir um valor para <strong>%s</strong> no formulário" % field
            self.data[field] = value
        if self.errors:
            return False
        return True

def required_field(form, required):
    result = {'error': None, 'data': None}
    data = {}
    message = {}
    for field in required:
        value = form.get(field)
        if value is "" or value is None:
            message[field] = "Você deve inserir um valor para <strong>%s</strong> no formulário" % field
        data[field] = value
    result['data'] = data
    result['error'] = message
    return result