from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

#設定資料庫位置/並建立app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'tlsyabrsdacvzb:0052cd379921a09ed41de5c9ef69a3c045b6de738c120fa6ec2f4291f57cf7e3@ec2-174-129-227-205.compute-1.amazonaws.com:5432/d8aekdhm679t9f'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

#設定app
manager = Manager(app)
manager.add_command('db', MigrateCommand)

#建立資料表欄位
class ItemInfo(db.Model):
    __tablename__ = 'ItemInfo'
    name = db.Column(db.String(20), primary_key=True)
    price = db.Column(db.Integer)
    stock = db.Column(db.Boolean)
    category = db.Column(db.String(5))

    def __init__(self
                 , name
                 , price
                 , stock
                 , category
                 ):
        self.name = name
        self.price = price
        self.stock = stock
        self.category = category


#if __name__ == '__main__':
#    manager.run()
