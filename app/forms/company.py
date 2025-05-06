from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SubmitField
from wtforms.validators import DataRequired, NumberRange


class CompanyForm(FlaskForm):
    name = StringField('Şirket Adı', validators=[DataRequired()])
    total_mandays = FloatField('Toplam Adam-Gün', validators=[
        DataRequired(),
        NumberRange(min=0, message='Adam-gün değeri pozitif bir sayı olmalıdır')
    ])
    submit = SubmitField('Kaydet') 