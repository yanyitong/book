# encoding:utf-8

from models import db, Admin, Reader, Book, Borrow, Information
from sqlalchemy import and_, or_, not_


# 输出全表
def select_all(table_name):
    try:
        if table_name == Admin.__name__:
            result = Admin.query.all()
            return True, result
        elif table_name == Reader.__name__:
            result = Reader.query.all()
            return True, result
        elif table_name == Book.__name__:
            result = Book.query.all()
            return True, result
        elif table_name == Borrow.__name__:
            result = Borrow.query.all()
            return True, result
        elif table_name == Information.__name__:
            result = Information.query.all()
            return True, result
        else:
            return False, []
    except Exception as e:
        print(e)
        return False, []


# 根据单个值查询表
def select_one(table_name, key_name):
    try:
        if table_name == Admin.__name__:
            result = Admin.query.filter(Admin.admin_id == key_name).first()
            return True, result
        elif table_name == Reader.__name__:
            result = Reader.query.filter(Reader.reader_id == key_name).first()
            return True, result
        elif table_name == Book.__name__:
            result = Book.query.filter(Book.ISBN == key_name).first()
            return True, result
        elif table_name == Borrow.__name__:
            result = Borrow.query.filter(Borrow.reader_id == key_name).first()
            return True, result
        else:
            return False, []
    except Exception as e:
        print(e)
        return False, []

# 根据关键字查询表中的某个字段
# def select_value(table_name, key_name, value_name):
#     try:
#         if table_name == Admin.__name__:
#             result = Admim.query.filter(Admin.admin_id == key_name).first()
#             return True, result
#         elif table_name == Reader.__name__:
#             result = Reader.query.filter(Reader.reader_id == key_name).first()
#             return True, result
#         elif table_name == Book.__name__:
#             result = Book.query.filter(Book.ISBN == key_name).first()
#             return True, result
#         elif table_name == Borrow.__name__:
#             result = Borrow.query.filter(Borrow.reader_id == key_name).first()
#             return True, result
#         else:
#             return False, []
#     except Exception as e:
#         print(e)
#         return False, []


# 充值
def increase_balance(reader_id, balance):
    try:
        result = Reader.query.filter(Reader.reader_id == reader_id).update({'balance': Reader.balance + int(balance)})
        return True, result

    except Exception as e:
        print(e)
        return False, 0


# 修改单个值
def update_one(table_name, key_name, change_name, change_value):
    try:
        if table_name == Admin.__name__:
            result = Admin.query.filter(Admin.admin_id == key_name).update({change_name: change_value})
            return True, result
        elif table_name == Reader.__name__:
            result = Reader.query.filter(Reader.reader_id == key_name).update({change_name: change_value})
            return True, result
        elif table_name == Book.__name__:
            result = Book.query.filter(Book.ISBN == key_name).update({change_name: change_value})
            return True, result
        elif table_name == Borrow.__name__:
            result = Borrow.query.filter(Book.ISBN == key_name).update({change_name: change_value})
            return True, result
        elif table_name == Information.__name__:
            result = Information.query.filter(Information.id == key_name).update({change_name: change_value})
            return True, result
        else:
            return False, 0
    except Exception as e:
        print(e)
        return False, 0


# 插入管理员记录
def insert_admin(admin_id, password, admin_name, gender, phone, note):
    try:
        admin = Admin(admin_id=admin_id, password=password, admin_name=admin_name, gender=gender, phone=phone,
                      note=note)
        db.session.add(admin)
        db.session.commit()
        return True
    except Exception as e:
        print(e)
        return False


# 插入读者记录
def insert_reader(reader_id, reader_name, password, gender, type, balance, chances, phone):
    try:
        reader = Reader(reader_id=reader_id, reader_name=reader_name, password=password,  gender=gender,
                        type=type, balance=balance, chances=chances, phone=phone)
        db.session.add(reader)
        db.session.commit()
        return True
    except Exception as e:
        print(e)
        db.session.rollback()
        return False




# 插入租借记录
def insert_borrow(id,ISBN,book_name, reader_id, reader_name, create_time, end_time, return_time, status, forfeit):
    try:
        borrow = Borrow(id=id, ISBN=ISBN, book_name=book_name, reader_id=reader_id, reader_name=reader_name,
                        create_time=create_time, end_time=end_time, return_time=return_time, status=status,
                        forfeit=forfeit)
        db.session.add(borrow)
        db.session.commit()
        return True
    except Exception as e:
        print(e)
        return False


# 插入信息记录
def insert_info(id, info, type, time):
    try:
        info = Information(user_id=id, info=info, type=type, time=time)
        db.session.add(info)
        db.session.commit()
        return True
    except Exception as e:
        print(e)
        return False


# 删除管理员记录
def delete_admin(admin_id):
    try:
        admin = Admin.query.filter_by(admin_id=admin_id).first()
        db.session.delete(admin)
        db.session.commit()
        return True
    except Exception as e:
        print(e)
        return False


# 删除读者记录
def delete_reader(reader_id):
    try:
        reader = Reader.query.filter_by(reader_id=reader_id).first()
        db.session.delete(reader)
        db.session.commit()
        return True
    except Exception as e:
        print(e)
        return False



# 删除书本记录
def delete_book(ISBN):
    try:
        book = Book.query.filter_by(ISBN=ISBN).first()
        db.session.delete(book)
        db.session.commit()
        return True
    except Exception as e:
        print(e)
        return False



# 查询某个学生借阅记录
def show_see_Borrow_book(reader_id):
    try:
        Borrows = Borrow.query.filter(and_(Borrow.reader_id == reader_id)).all()
        return True, Borrows
    except Exception as e:
        print(e)
        return False, []


# 查询公告
def show_see_information():
    try:
        information = Information.query.filter_by(type=1).all()
        return True, information
    except Exception as e:
        print(e)
        return False, []

#查看聊天记录
def show_see_chat(reader_id):
    try:
        information1 = Information.query.filter_by(type=2,user_id=reader_id,).all()
        information2=Information.query.filter_by(type=3).all()
        return True, information1,information2
    except Exception as e:
        print(e)
        return False, []

# 查询所有的书本
def show_query_all_book(type_name, search_name):
    try:
        query = '%' + search_name + '%'
        if type_name == 'ISBN':
            result = Book.query.filter(Book.ISBN.like(query)).all()
            return True, result
        elif type_name == 'book_name':
            result = Book.query.filter(Book.book_name.like(query)).all()
            return True, result
        elif type_name == 'author':
            result = Book.query.filter(Book.author.like(query)).all()
            return True, result
        elif type_name == 'book_concern':
            result = Book.query.filter(Book.book_concern.like(query)).all()
            return True, result
        elif type_name == 'category':
            result = Book.query.filter(Book.category.like(query)).all()
            return True, result
        elif type_name == 'location':
            result = Book.query.filter(Book.location.like(query)).all()
            return True, result
        elif type_name == 'origin':
            result = Book.query.filter(Book.origin.like(query)).all()
            return True, result
        else:
            return False, []
    except Exception as e:
        print(e)
        return False, []


# 查询借阅的记录
def show_query_all_Borrow(type_name, search_name):
    try:
        query = '%' + search_name + '%'
        if type_name == 'ISBN':
            result = Borrow.query.filter(Borrow.ISBN.like(query)).all()
            return True, result
        elif type_name == 'book_name':
            result = Borrow.query.filter(Borrow.book_name.like(query)).all()
            return True, result
        elif type_name == 'reader_id':
            result = Borrow.query.filter(Borrow.reader_id.like(query)).all()
            return True, result
        elif type_name == 'reader_name':
            result = Borrow.query.filter(Borrow.reader_name.like(query)).all()
            return True, result
        else:
            return False, []
    except Exception as e:
        print(e)
        return False, []


# 写入注册的学生信息
#def show_register(reader_id, reader_name, password, gender, type, balance, chances,  phone):
#    result = insert_reader(reader_id,reader_name, password,  gender, type, balance, phone, chances,  phone)
#   return result


# 写入新书的信息
#def show_new_book(ISBN, book_name, author, book_concern, category, location, is_rent,price,sum,now_amount, origin):
#   result = insert_book(ISBN, book_name, author, book_concern, category, location, is_rent, price,sum,origin,False)
#  return result



# 图书馆图书借阅
def show_book_borrow(ISBN, book_name, reader_id, reader_name, create_time, end_time, status):
    try:
        db.session.begin(nested=True)
        borrow = Borrow(ISBN=ISBN, book_name=book_name, reader_id=reader_id, reader_name=reader_name,
                        create_time=create_time, end_time=end_time, status=status)
        number1 = Reader.query.filter(Reader.reader_id == reader_id).update({"chances": Reader.chances - 1})
        number2 = Book.query.filter(Book.ISBN == ISBN).update({"now_amount": Book.now_amount - 1})
        db.session.add(borrow)
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        print(e)
        return False


# 用户图书借阅
def show_book_borrow1(ISBN, book_name, reader_id, reader_name, create_time, end_time, status, origin):
    try:
        db.session.begin(nested=True)
        borrow = Borrow(ISBN=ISBN, book_name=book_name, reader_id=reader_id, reader_name=reader_name,
                        create_time=create_time, end_time=end_time, status=status)
        print(origin)
        print("插入成功")
        number1 = Reader.query.filter(Reader.reader_id == reader_id).update({"chances": Reader.chances - 1})
        print("设置次数成功")
        number2 = Book.query.filter(Book.ISBN == ISBN).update({"now_amount": Book.now_amount - 1})
        print("设置数量成功")
        number3 = Reader.query.filter(Reader.reader_id == reader_id).update({"balance": Reader.balance - 1})
        print("设置余额成功")
        number4 = Reader.query.filter(Reader.reader_id == str(origin)).update({"balance": Reader.balance + 1})
        print("转账成功")
        db.session.add(borrow)
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        print(e)
        return False


# 查询某学生借的某书是否还了
def select_Borrow_book(ISBN,reader_id):
    try:
        db.session.begin(subtransactions=True)
        result = Borrow.query.filter(and_(Borrow.ISBN == ISBN, Borrow.reader_id==reader_id,Borrow.status == True)).first()
        db.session.commit()
        if result is None:
            return False, []
        else:
            return True, result
    except Exception as e:
        db.session.rollback()
        print(e)
        return False, []


# 还书
def show_book_return(ISBN, reader_id, status, is_rent, book_number):
    try:
        db.session.begin(subtransactions=True)
        number1 = Reader.query.filter(Reader.reader_id == reader_id).update({"chances": Reader.chances+1})
        number2 = Book.query.filter(Book.ISBN == ISBN).update({"is_rent": is_rent})
        number3 = Borrow.query.filter(Borrow.ISBN == ISBN).update({"status": status})
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        print(e)
        return False


if __name__ == '__main__':
    pass

