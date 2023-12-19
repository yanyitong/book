# encoding:utf-8

from flask import Flask, request, render_template
from manage import *
from servers import app_server, information_server
from pay import AliPay
import json
import datetime
import time
import utils

import requests
import hashlib
import pymysql
import logging
import datetime



@app.route('/', methods=['GET'])
def index():
    response = request.cookies.get('WTF')
    page = app_server.cookie_checking_all(response, 'student/StudentIndex.html', 'teacher/TeacherIndex.html',
                                          'Index.html')
    return render_template(page)


@app.route('/student')
def student():
    response = request.cookies.get('WTF')
    page = app_server.cookie_checking_reader(response, 'student/StudentIndex.html', 'Index.html')
    return render_template(page)


@app.route('/StuPasChange')
def stu_pas_change():
    response = request.cookies.get('WTF')
    page = app_server.cookie_checking_reader(response, 'student/StuPasChange.html', 'Index.html')
    return render_template(page)

@app.route('/StuAbout')
def stu_about():
    response = request.cookies.get('WTF')
    page = app_server.cookie_checking_reader(response, 'student/StuAbout.html', 'Index.html')
    return render_template(page)

@app.route('/StuInformation')
def stu_information():
    response = request.cookies.get('WTF')
    page = app_server.cookie_checking_reader(response, 'student/StuInformation.html', 'Index.html')
    return render_template(page)

@app.route('/StuRentQuery')
def stu_rent_query():
    response = request.cookies.get('WTF')
    page = app_server.cookie_checking_reader(response, 'student/StuRentQuery.html', 'Index.html')
    return render_template(page)


@app.route('/StuBookQuery')
def stu_book_query():
    response = request.cookies.get('WTF')
    page = app_server.cookie_checking_reader(response, 'student/StuBookQuery.html', 'Index.html')
    return render_template(page)

@app.route('/StuBookDetails')
def stu_details_query():
    response = request.cookies.get('WTF')
    ISBN = request.args.get("ISBN")
    type = request.args.get("type")
    page = app_server.cookie_checking_reader(response, 'student/StuBookDetails.html', 'Index.html')
    return render_template(page, ISBN=ISBN, type=type)

@app.route('/StuSeeBookQuery')
def stu_see_book_query():
    response = request.cookies.get('WTF')
    page = app_server.cookie_checking_reader(response, 'student/StuSeeBookQuery.html', 'Index.html')
    return render_template(page)

@app.route('/contact')
def stu_concat():
    response = request.cookies.get('WTF')
    page = app_server.cookie_checking_reader(response, 'student/contact.html', 'Index.html')
    return render_template(page)


# 注册
@app.route('/signup', methods=['POST'])
def student_signup():
    id = request.values.get('userid')
    password = request.values.get('password')
    name = request.values.get('name')
    typename = request.values.get('typename')
    gender = request.values.get('gender')
    phone = request.values.get('phone')

    insert = app_server.check_signup(id, name, password, typename, gender, phone)
    return insert


# 学生端登录检查
@app.route('/studentLogin', methods=['POST'])
def student_login():
    student_id = request.values.get('studentid')
    student_password = request.values.get('studentpassword')

    query = app_server.login_checking(student_id, student_password, 'reader')

    if query == 'error' or query == 'none':
        return 'error'
    else:
        student_id = query[0]
        student_name = query[1]
        student_password = query[2]
        result = [student_id, student_name, student_password]
        return json.dumps(result)



# 学生修改密码
@app.route('/PostStuChangePas', methods=['POST'])
def post_stu_change_pas():
    studentId = request.values.get('studentId')
    OldPassword = request.values.get('OldPassword')
    NewPassword = request.values.get('NewPassword')
    print(studentId+OldPassword+NewPassword);
    try:
        is_student = app_server.login_checking(studentId, OldPassword, "student")
        # 如果原密码正确，那就修改密码
        if is_student == 'error':
            return 'error'
        elif is_student == 'none':
            return 'none'
        else:
            changepas = information_server.password_change(studentId, NewPassword, "student")
            if changepas == 'correct':
                return 'correct'
            elif changepas == 'error':
                return 'error'
    except Exception as e:
        print(e)
        return 'error'


# 查询学生看过的书籍
@app.route('/PostStuSeeBookQuery', methods=['POST'])
def post_stu_see_book_query():
    student_id = request.values.get('studentId')
    try:
        rents = information_server.show_see_book(student_id)
        list_rent = []
        for i in rents:
            map_rent = {"ISBN": i.ISBN, "book_name": i.book_name, "reader_id": i.reader_id,
                        "reader_name": i.reader_name,
                        "create_time": i.create_time, "end_time": i.end_time, "status": i.status}
            list_rent.append(map_rent)

        return json.dumps({"id": list_rent}, cls=information_server.DateEncoding)
    except Exception as e:
        print(e)
        return 'error'


# 查询读者个人信息
@app.route('/postStuInformation', methods=['POST'])
def post_information():
    student_id = request.values.get('studentId')
    try:
        i = information_server.show_Information(student_id)
        map_rent = {"reader_id": i.reader_id, "reader_name": i.reader_name, "gender": i.gender,
                        "password": i.password,
                        "type": i.type, "balance": i.balance, "chances": i.chances, "phone": i.phone }
        return json.dumps({"id": map_rent}, cls=information_server.DateEncoding)

    except Exception as e:
        print(e)
        return 'error'


# 更新个人信息
@app.route('/updateInformation', methods=['POST'])
def updata_information():
    user_id = request.values.get('user_id')
    user_name = request.values.get('user_name')
    gender = request.values.get('gender')
    phone = request.values.get('phone')
    try:
        i = information_server.update_information(user_id, user_name, gender, phone)
        return json.dumps(i)

    except Exception as e:
        print(e)
        return 'error'


# 查看正在借阅的书籍
@app.route('/postStuRentQuery', methods=['POST'])
def post_stu_rent_query():
    student_id = request.values.get('studentId')
    try:
        rents = information_server.show_rent_book(student_id)
        list_rent = []
        for i in rents:
            result, rents = information_server.find_detail(i.ISBN)
            map_rent = {"ISBN": rents.ISBN, "book_name": rents.book_name, "author": rents.author,
                        "book_concern": rents.book_concern,
                        "category": rents.category, "location": rents.location, "price": rents.price,
                        "qrcode": rents.qrcode, "img": rents.img, "now_amount": rents.now_amount,
                        "origin": rents.origin, "status": i.status}
            list_rent.append(map_rent)
        return json.dumps({"id": list_rent}, cls=information_server.DateEncoding)
    except Exception as e:
        print(e)
        return 'error'


# 书目查询
@app.route('/PostStuBookQuery', methods=['POST'])
def post_stu_book_query():
    type_name = request.values.get('typeName')
    search_name = request.values.get('searchName')
    try:
        rents = information_server.all_book_query(type_name, search_name)
        list_rent = []
        for i in rents:
            if i.is_rent:
                is_rent = '不可借'
            else:
                is_rent = '可借'

            map_rent = {"ISBN": i.ISBN, "book_name": i.book_name, "author": i.author, "book_concern": i.book_concern,
                        "category": i.category, "location": i.location, "is_rent": is_rent, "price": i.price, "qrcode": i.qrcode, "img": i.img}
            list_rent.append(map_rent)

        return json.dumps({"id": list_rent}, cls=information_server.DateEncoding)
    except Exception as e:
        print(e)
        return 'error'

@app.route('/displaybooks', methods=['POST'])
def post_stu_like_query():
        studentId = request.values.get('studentId')
        try:
            rents1, rents2 = information_server.search_like_book(studentId)
            result =[]
            for book, score in rents1[:8]:
                flag, bokk = utils.select_one('Book', book)
                path = bokk.img
                sub=(book, rents2[book]["author"],rents2[book]["book_concern"],rents2[book]["book_name"], score, path)
                result.append(sub)
            return result
        except Exception as e:
            print(e)
            return 'error'


# 管理员前端跳转部分
@app.route('/admin')
def teacher():
    response = request.cookies.get('WTF')
    page = app_server.cookie_checking_teacher(response, 'teacher/TeacherIndex.html', 'Index.html')
    return render_template(page)


@app.route('/AdmPasChange')
def adm_pas_change():
    response = request.cookies.get('WTF')
    page = app_server.cookie_checking_teacher(response, 'teacher/AdmPasChange.html', 'Index.html')
    return render_template(page)


@app.route('/LibraryCard')
def library_card():
    response = request.cookies.get('WTF')
    page = app_server.cookie_checking_teacher(response, 'teacher/LibraryCard.html', 'Index.html')
    return render_template(page)


@app.route('/BookBorrow')
def book_borrow():
    response = request.cookies.get('WTF')
    page = app_server.cookie_checking_teacher(response, 'teacher/BookBorrow.html', 'Index.html')
    return render_template(page)


@app.route('/BookReturn')
def book_return():
    response = request.cookies.get('WTF')
    page = app_server.cookie_checking_teacher(response, 'teacher/BookReturn.html', 'Index.html')
    return render_template(page)


@app.route('/BorrowInformation')
def borrow_information():
    response = request.cookies.get('WTF')
    page = app_server.cookie_checking_teacher(response, 'teacher/BorrowInformation.html', 'Index.html')
    return render_template(page)


@app.route('/NewBook')
def new_book():
    response = request.cookies.get('WTF')
    page = app_server.cookie_checking_teacher(response, 'teacher/NewBook.html', 'Index.html')
    return render_template(page)


@app.route('/BookInformation')
def book_information():
    response = request.cookies.get('WTF')
    page = app_server.cookie_checking_teacher(response, 'teacher/BookInformation.html', 'Index.html')
    return render_template(page)


# 管理员登录检查
@app.route('/adminLogin', methods=['POST'])
def teacher_login():
    teacher_id = request.values.get('teacherid')
    teacher_password = request.values.get('teacherpassword')
    query = app_server.login_checking(teacher_id, teacher_password, 'admin')
    print(query)

    if query == 'error' or query == 'none':
        return 'error'
    else:
        teacher_id = query[0]
        teacher_name = query[1]
        teacher_password = query[2]
        result = [teacher_id, teacher_name, teacher_password]

        return json.dumps(result)


# 教师修改密码
@app.route('/PostAdmPasChange', methods=['POST'])
def post_adm_pas_change():
    teacherId = request.values.get('teacherid')
    OldPassword = request.values.get('OldPassword')
    NewPassword = request.values.get('NewPassword')
    try:
        is_student = app_server.login_checking(teacherId, OldPassword, "admin")
        # 如果原密码正确，那就修改密码
        if is_student == 'error':
            return 'error'
        elif is_student == 'none':
            return 'none'
        else:
            changepas = information_server.password_change(teacherId, NewPassword, "admin")
            if changepas == 'correct':
                return 'correct'
            elif changepas == 'error':
                return 'error'
    except Exception as e:
        print(e)
        return 'error'


# 办理借书证
@app.route('/PostLibraryCard', methods=['POST'])
def post_library_card():
    student_id = request.values.get("studentId")
    student_name = request.values.get("studentName")
    college = request.values.get("college")
    major = request.values.get("major")
    phone = request.values.get("phone")
    note = request.values.get("note")
    gender = request.values.get("gender")
    password = request.values.get("password")
    try:
        result = information_server.register(student_id, password, student_name, gender, college, major, phone, note)
        return json.dumps({"id": result})
    except Exception as e:
        print(e)
        return 'error'


# 查询正在借阅的书籍
@app.route('/PostBookBorrow1', methods=['POST'])
def post_book_borrow1():
    student_id = request.values.get('studentId')
    try:
        rents = information_server.show_rent_book(student_id)
        list_rent = []
        for i in rents:
            map_rent = {"ISBN": i.ISBN, "book_name": i.book_name, "student_id": i.student_id,
                        "student_name": i.student_name,
                        "begin_date": i.begin_date, "end_date": i.end_date}
            list_rent.append(map_rent)

        return json.dumps({"id": list_rent}, cls=information_server.DateEncoding)
    except Exception as e:
        print(e)
        return 'error'


# 借书操作
@app.route('/PostBookBorrow2', methods=['POST'])
def post_book_borrow2():
    ISBN = request.values.get('ISBN')
    student_id = request.values.get('studentId')
    try:
        result = information_server.book_borrow(ISBN, student_id)
        return json.dumps({"id": result})
    except Exception as e:
        print(e)
        return 'error'


# 查询正在借阅的书籍
@app.route('/PostBookReturn1', methods=['POST'])
def post_book_return1():
    student_id = request.values.get('studentId')
    try:
        rents = information_server.show_rent_book(student_id)
        list_rent = []
        for i in rents:
            map_rent = {"ISBN": i.ISBN, "book_name": i.book_name, "student_id": i.student_id,
                        "student_name": i.student_name,
                        "begin_date": i.begin_date, "end_date": i.end_date}
            list_rent.append(map_rent)

        return json.dumps({"id": list_rent}, cls=information_server.DateEncoding)
    except Exception as e:
        print(e)
        return 'error'


# 还书操作
@app.route('/PostBookReturn2', methods=['POST'])
def post_book_return2():
    ISBN = request.values.get('ISBN')
    student_id = request.values.get('studentId')
    try:
        result = information_server.book_return(ISBN, student_id)
        return json.dumps({"id": result})
    except Exception as e:
        print(e)
        return 'error'


# 管理员端查询借阅信息
@app.route('/PostBorrowInformation', methods=['POST'])
def post_borrow_information():
    type_name = request.values.get('borrowTypeName')
    search_name = request.values.get('borrowSearchName')
    try:
        rents = information_server.all_rent_query(type_name, search_name)
        list_rent = []
        for i in rents:
            # if i.status:
            #     i.status = '已归还'
            # else:
            #     i.status = '借出'
            map_rent = {"ISBN": i.ISBN, "book_name": i.book_name, "student_id": i.reader_id,
                        "student_name": i.reader_name,
                        "begin_date": i.create_time, "end_date": i.end_time, "is_return": i.status}
            list_rent.append(map_rent)

        return json.dumps({"id": list_rent}, cls=information_server.DateEncoding)
    except Exception as e:
        print(e)
        return 'error'


# 新书录入
@app.route('/PostNewBook', methods=['POST'])
def post_new_book():
    ISBN = request.values.get("ISBN")
    book_name = request.values.get("bookName")
    author = request.values.get("author")
    book_concern = request.values.get("bookConcern")
    category = request.values.get("category")
    location = request.values.get("location")
    is_ret = 1
    price = 20
    sum = 30
    now_amount = 30
    origin = 0
    try:
        result = information_server.new_book(ISBN, book_name, author, book_concern, category, location, is_ret, price,
                                             sum, now_amount, origin)
        return json.dumps({"id": result})
    except Exception as e:
        print(e)
        return 'error'

# 消息发送
@app.route('/sendMessage', methods=['POST'])
def post_message():
    studentId = request.values.get("studentId")
    message = request.values.get("message")
    try:
        result = information_server.send_message(studentId, message)
        return json.dumps({"id": result})
    except Exception as e:
        print(e)
        return 'error'

# 查阅借书详情
@app.route('/PostBookReturn1/detail', methods=['POST'])
def stu_rent_detail():
    ISBN = request.values.get('ISBN')
    print(ISBN)
    try:
        result, rents = information_server.find_detail(ISBN)
        map_rent={"ISBN": rents.ISBN, "book_name": rents.book_name, "author": rents.author,
                        "book_concern" : rents.book_concern,
                        "category": rents.category, "location": rents.location, "price": rents.price, "qrcode":rents.qrcode , "img": rents.img, "now_amount": rents.now_amount, "origin": rents.origin}
        return json.dumps({"id": map_rent})
    except Exception as e:
        print(e)
        return 'error'

# 管理员端查询图书信息
@app.route('/PostBookInformation', methods=['POST'])
def post_book_information():
    type_name = request.values.get('bookTypeName')
    search_name = request.values.get('bookSearchName')
    try:
        rents = information_server.all_book_query(type_name, search_name)
        list_rent = []
        for i in rents:
            if i.is_rent:
                is_rent = '不可借'
            else:
                is_rent = '可借'
            map_rent = {"ISBN": i.ISBN, "book_name": i.book_name, "author": i.author, "book_concern": i.book_concern,
                        "category": i.category, "location": i.location, "is_rent": is_rent}
            list_rent.append(map_rent)

        return json.dumps({"id": list_rent})
    except Exception as e:
        print(e)
        return 'error'


@app.route('/pay', methods=['POST'])
def pay():
    a = str(request.cookies.get('WTF')).replace('%5B%22', '').replace('%20%22', '').replace('%22%5D', '').replace('%22', '').split(',')
    reader_id = str(a[0])
    order_id = reader_id + str(datetime.datetime.now().strftime("%Y%m%d%H%M%S"))
    print(order_id)
    order_amount = request.form['order_amount']
    print(order_amount)
    # 沙箱环境地址：https://openhome.alipay.com/platform/appDaily.htm?tab=info
    app_id = "2021000122678915"  # APPID （沙箱应用）

    # 支付完成后，支付偷偷向这里地址发送一个post请求，识别公网IP,如果是 192.168.20.13局域网IP ,支付宝找不到，def page2() 接收不到这个请求
    notify_url = "http://127.0.0.1:3326/callback"

    # 支付完成后，跳转的地址。
    return_url = "http://localhost:3326/StuInformation"

    merchant_private_key_path = "D:/pythonexample/reader_knowledge-master/keys/private_key.txt"  # 应用私钥
    alipay_public_key_path = "D:/pythonexample/reader_knowledge-master/keys/public_key.txt"  # 支付宝公钥

    alipay = AliPay(
        appid=app_id,
        app_notify_url=notify_url,
        return_url=return_url,
        app_private_key_path=merchant_private_key_path,
        alipay_public_key_path=alipay_public_key_path,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥
        debug=True,  # 默认False,
    )
    #print(alipay)
    res = alipay.direct_pay(subject='充值',  # 商品描述
                            out_trade_no=order_id,  # 用户购买的商品订单号
                            total_amount = order_amount)  # 交易金额

    utils.increase_balance(reader_id,order_amount)

    pay_url = f"https://openapi.alipaydev.com/gateway.do?{res}"

    return redirect(pay_url)    # 访问是跳转到pay_url页面

#聊天
@app.route('/chat', methods=['POST'])
def chat():
    user_id = request.values.get('studentId')
    try:
        result, informations1,informations2 = information_server.chat_with_admin(user_id)
        list_chat = []
        for i in informations1:
            map_chat = {"info": i.info, "time": i.time, "type": i.type}
            list_chat.append(map_chat)
        for i in informations2:
            map_chat = {"info": i.info, "time": i.time, "type": i.type}
            list_chat.append(map_chat)
        print("sldalkd")
        print(list_chat)
        return json.dumps({"id":list_chat})
    except Exception as e:
        print(e)
        return 'error'
#发送消息
@app.route('/sendMessage_1', methods=['POST'])
def chat1():
    studentId = request.values.get("studentId")
    message = request.values.get("message")
    try:
        result = information_server.send_message1(studentId, message)
        return json.dumps({"id": result})
    except Exception as e:
        print(e)
        return 'error'
# 公告栏
@app.route('/notices', methods=['GET'])
def get_notices():
    try:
        rents = information_server.show_Information2()
        list_rent = []
        for i in rents:
            str1 = str(i.info)
            title, content = str1.split(",")
            map_rent = {"title": title, "content": content, "date": i.time}
            list_rent.append(map_rent)
        return json.dumps({"id": list_rent}, cls=information_server.DateEncoding)
    except Exception as e:
        print(e)
        return 'error'


if __name__ == '__main__':
    app.run(debug=True, port="3326")
