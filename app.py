from flask import Flask, render_template, request, url_for, redirect, jsonify, session, make_response, g
from datetime import timedelta
from web_sqlite import *
import os

web = Flask(__name__)
web.secret_key = os.urandom(24)
database = My_sqlite("student.db")


@web.route('/')
def hello_world():
    if g.Turntable:
        return redirect(url_for("backstage"))
    else:
        return redirect(url_for("login"))


@web.before_request
def before_request():
    user_id = session.get("uname")
    if user_id:
        g.Turntable = True
    else:
        if 'uname' in request.cookies:
            uname = request.cookies.get('uname')
            session['uname'] = uname
            g.Turntable = True
        else:
            g.Turntable = False


@web.errorhandler(404)
def error_date(error):
    return render_template("404.html"), 404


@web.route("/register", methods=["GET", "POST"])  # 注册
def register():
    if request.method == "GET":
        return render_template("register.html")
    else:
        user = request.form.get("user")
        paw = request.form.get("password")
        if intoAdmin(database, user, paw):
            return redirect(url_for("login"))
        else:
            return render_template("register.html", msg=f"已经存在学号为:{user}的用户了")


@web.route("/login", methods=["GET", "POST"])  # 登录
def login():
    if request.method == "GET":
        if g.Turntable:
            return redirect(url_for("backstage"))
        else:
            return make_response(render_template("login.html"))
    else:
        if g.Turntable:
            return redirect(url_for("backstage"))
        else:
            user = request.form.get("user")
            paw = request.form.get("password")
            if loGin(database, user):
                if selPassword(database, user, paw):
                    response = redirect(url_for("backstage"))
                    session['uname'] = user
                    session.permanent = True
                    web.permanent_session_lifetime = timedelta(hours=24)
                    response.set_cookie("uname", user, 3600)
                    return response
                else:
                    return render_template("login.html", msg="密码错误")
            else:
                return f"不存在学号为'{user}'的用户"


@web.route("/backstage", methods=["GET", "POST"])
def backstage():
    if g.Turntable:
        return render_template("backstage.html", date_List=getStudentInfo(database))
    else:
        return redirect(url_for("login"))


@web.route("/modifyStu/<no>", methods=["GET", "POST"])
def modifyStu(no):
    if stuinMysql(database, no):
        if request.method == "GET":
            if g.Turntable:
                return render_template("modifyStu.html", data=getOneStudent(database, no)[0])
            else:
                return redirect(url_for("login"))
        else:
            no = request.form.get("No")
            name = request.form.get("Name")
            sex = request.form.get("Sex")
            upDataStudent(database, no, name, sex)
            return redirect(url_for("backstage"))
    else:
        return render_template("404.html"), 404


@web.route("/getStu", methods=["POST"])
def getStu():
    no = request.form.get("No")
    name = request.form.get("Name")
    sex = request.form.get("Sex")
    if not stuinMysql(database, no):
        intoStudentInfo(database, no, name, sex)
        return jsonify({"code": 200}), 200
    else:
        return jsonify({"code": 404}), 200


@web.route("/delStu", methods=["POST"])
def delStu():
    no = request.form.get("No")
    if delStudent(database, no):
        return jsonify({"code": 200}), 200
    else:
        return jsonify({"code": 404}), 200


@web.route("/logout")
def logout():
    session.clear()
    response = redirect(url_for("login"))
    response.delete_cookie("uname")
    return response


if __name__ == '__main__':
    web.run(host='0.0.0.0', port=5555)
    web.debug = True
