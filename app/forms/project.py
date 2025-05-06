from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, FloatField, BooleanField, DateField, SubmitField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, NumberRange, Optional


class ProjectForm(FlaskForm):
    name = StringField('Proje Adı', validators=[DataRequired()])
    manager = StringField('Proje Yöneticisi', validators=[DataRequired()])
    pentest_date = DateField('Pentest Tarihi', validators=[Optional()], format='%Y-%m-%d')
    project_type = SelectField('Proje Türü', validators=[DataRequired()],
                              choices=[('Proje', 'Proje'), ('Küçük Talep', 'Küçük Talep')])
    mandays = FloatField('Adam-Gün', validators=[
        DataRequired(),
        NumberRange(min=0, message='Adam-gün değeri pozitif bir sayı olmalıdır')
    ])
    extra_mandays = FloatField('Ek Adam-Gün', validators=[
        Optional(),
        NumberRange(min=0, message='Ek adam-gün değeri pozitif bir sayı olmalıdır')
    ], default=0)
    extra_mandays_reason = TextAreaField('Ek Adam-Gün Nedeni', validators=[Optional()])
    company_id = SelectField('Şirket', validators=[DataRequired()], coerce=int)
    completed = BooleanField('Tamamlandı')
    tags = StringField('Etiketler', validators=[Optional()], description='Virgülle ayırarak birden fazla etiket girebilirsiniz (ör: Mobil Şube, Internet Şube)')
    is_backlog = BooleanField('Backlog Projesi', default=False)
    priority = IntegerField('Öncelik', validators=[Optional(), NumberRange(min=0, max=10)], default=0, description='0-10 arası, 10 en yüksek öncelik')
    submit = SubmitField('Kaydet') 