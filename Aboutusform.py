from wtforms import Form, StringField, SelectField, TextAreaField, validators

class AboutusForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    email = StringField('Email',[validators.Email(), validators.DataRequired()])
    remarks = TextAreaField('Message', [validators.DataRequired()],default='')
    replies = TextAreaField('Answer', [validators.DataRequired()],default='-')
    
class FAQ(Form):
    reply = TextAreaField('Message', [validators.DataRequired()],default='')