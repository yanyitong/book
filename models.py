# coding:utf-8

from manage import *


# 管理员
class Admin(db.Model):
    __tablename__ = 'admin'
    admin_id = db.Column(db.String(32), primary_key=True, index=True)
    password = db.Column(db.String(32), nullable=False)
    admin_name = db.Column(db.String(32), nullable=False)
    gender = db.Column(db.String(5))
    phone = db.Column(db.String(32))
    note = db.Column(db.String(64))

    def __str__(self):
        return 'admin_id:%s, password:%s, admin_name:%s， gender:%s, phone:%s, note:%s' % (
            self.admin_id, self.password, self.admin_name, self.gender, self.phone, self.note)


# 读者
class Reader(db.Model):
    __tablename__ = 'reader'
    reader_id = db.Column(db.String(32), primary_key=True, index=True, default='sdfafdsf')
    reader_name = db.Column(db.String(32), nullable=False)
    password = db.Column(db.String(32), nullable=False)
    gender = db.Column(db.String(5))
    type = db.Column(db.String(32), default='student', nullable=False)
    balance = db.Column(db.String(32))
    chances = db.Column(db.String(32))
    phone = db.Column(db.String(32), nullable=False)

    def __str__(self):
        return ' reader_id:%s, reader_name:%s, password:%s, gender:%s, type:%s, balance:%s, chances:%s, phone:%s' % (
            self.reader_id, self.reader_name, self.password, self.gender, self.type, self.balance, self.chances,
            self.phone)


# 书本
class Book(db.Model):
    __tablename__ = 'book'
    ISBN = db.Column(db.String(64), primary_key=True, index=True)
    book_name = db.Column(db.String(32), nullable=False)
    author = db.Column(db.String(32))
    book_concern = db.Column(db.String(32))
    category = db.Column(db.String(32))
    location = db.Column(db.String(32))
    is_rent = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Double, default=0)
    sum = db.Column(db.BigInteger, default=0)
    now_amount = db.Column(db.BigInteger, default=0)
    origin = db.Column(db.String(255))
    qrcode = db.Column(db.String(255))
    img = db.Column(db.String(255))
    def __str__(self):
        return 'ISBN:%s, book_name:%s, author:%s, book_concern:%s, category:%s, location:%s, is_rent:%s, price:%s, sum:%s, now_amount:%s, origin:%s, qrcode:%s, img:%s' % (
            self.ISBN, self.book_name, self.author, self.book_concern, self.category, self.location, self.is_rent,
            self.price, self.sum, self.now_amount, self.origin, self.qrcode, self.img)


# 租借情况
class Borrow(db.Model):
    __tablename__ = 'borrow'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)
    ISBN = db.Column(db.String(32), nullable=False )
    book_name = db.Column(db.String(32), nullable=False)
    reader_id = db.Column(db.String(32), nullable=False, index=True)
    reader_name=db.Column(db.String(32), nullable=False)
    create_time = db.Column(db.Date, nullable=False)
    end_time = db.Column(db.Date, nullable=False)
    return_time = db.Column(db.Date)
    status = db.Column(db.String(255))
    forfeit = db.Column(db.String(255))

    def __str__(self):
        return 'id:%s, ISBN:%s, book_name:%s, reader_id:%s, reader_name：%s,create_time:%s, end_time:%s,return_time:%s, status:%s, forfeit:%s' % (
            self.id, self.ISBN, self.book_name, self.reader_id, self.reader_name, self.create_time,
            self.end_time, self.return_time, self.status, self.forfeit)


# 信息公示
class Information(db.Model):
    __tablename__ = 'information'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)
    user_id = db.Column(db.String(255), nullable=False)
    info = db.Column(db.String(255))
    type = db.Column(db.String(255), nullable=False)
    time = db.Column(db.Date, nullable=False)

    def __str__(self):
        return 'id:%s,user_id:%s  info:%s, type:%s, time:%s' % (
            self.id,self.user_id, self.info, self.type, self.time)