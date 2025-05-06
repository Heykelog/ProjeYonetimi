from app import db

class Setting(db.Model):
    __tablename__ = 'settings'

    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(100), nullable=False, unique=True)
    value = db.Column(db.Text, nullable=True)
    
    def __init__(self, key, value):
        self.key = key
        self.value = value
    
    @classmethod
    def get_setting(cls, key, default=None):
        setting = cls.query.filter_by(key=key).first()
        if setting:
            return setting.value
        return default
    
    @classmethod
    def set_setting(cls, key, value):
        setting = cls.query.filter_by(key=key).first()
        if setting:
            setting.value = value
        else:
            setting = cls(key, value)
            db.session.add(setting)
        db.session.commit()
        return setting 