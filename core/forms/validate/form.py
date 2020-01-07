def required_field(form, requiride):

    messages = {}
    for field in requiride:
        value = form.get(field)
        if value is "" or value is None:
            messages[field] = "Você deve inserir um valor para <strong>%s</strong> no formulário" % field
    return messages