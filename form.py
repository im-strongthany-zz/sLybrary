from wtforms import Form, StringField, SelectField

class BookSearchForm(Form):
    opts = [('Title','Title')]
    select = SelectField('Search for books:', choices=opts)
    search = StringField('')