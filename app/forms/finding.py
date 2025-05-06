from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, SubmitField
from wtforms.validators import DataRequired


class FindingForm(FlaskForm):
    name = StringField('Bulgu Adı', validators=[DataRequired()])
    severity = SelectField('Önem Seviyesi', validators=[DataRequired()],
                          choices=[('Critical', 'Kritik'), 
                                   ('High', 'Yüksek'), 
                                   ('Medium', 'Orta'), 
                                   ('Low', 'Düşük')])
    description = TextAreaField('Açıklama')
    status = SelectField('Durum', validators=[DataRequired()],
                        choices=[('Open', 'Açık'), ('Closed', 'Kapalı')])
    submit = SubmitField('Kaydet') 