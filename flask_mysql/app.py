from flask import Flask, render_template, request
import json

from pyecharts.charts import Bar

from flask_mysql import db
from jinja2 import Markup

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/hello')
def hello_world2():
    data = 'hello data'
    return render_template("hello.html", data=data)


@app.route("/user/<username>", methods=["GET", "POST"])
def get_user(username):
    return "hello %s" % username


# http://127.0.0.1:5000/data?a=a1&b=b1
@app.route('/data', methods=["POST", "GET"])
def test_data():
    # print(request.args)
    # print(request.args.get("a"), request.args.get("b"))
    # print(request.headers)
    # print(request.headers.get("User-Agent"))
    # print(request.data)
    # import json
    # print(json.loads(request.data))
    # print(request.cookies)
    # print(request.cookies.get("token"))
    print(request.form)
    print(request.form.get("username"), request.form.get("password"))
    return 'success'


@app.route("/use_template")
def use_template():
    datas = [(1, "name1"), (2, "name2"), (3, "name3")]
    title = "学生信息"
    return render_template("use_template.html", datas=datas, title=title)


def read_pvuv_data():
    """
    read pv uv data
    :return: list, ele:(pdate, pv, uv)

    """
    data = []
    with open("./data/pvuv.txt") as fin:
        is_first_line = True

        for line in fin:
            if is_first_line:
                is_first_line = False
                continue
            line = line[:-1]
            pdate, pv, uv = line.split("\t")
            data.append((pdate, pv, uv))
    # return html
    return data


@app.route("/pvuv")
def pvuv():
    # read file
    data = read_pvuv_data()
    # return html
    return render_template("pvuv.html", data=data)


@app.route("/getjson")
def getjson():
    # read file
    data = read_pvuv_data()
    # return html
    return json.dumps(data)


@app.route("/show_add_user")
def show_add_user():
    return render_template("show_add_user.html")


@app.route("/do_add_user", methods=["POST"])
def do_add_user():
    print(request.form)
    name = request.form.get("name")
    sex = request.form.get("sex")
    age = request.form.get("age")
    email = request.form.get("email")
    sql = f"""
    insert
    into
    user(name, sex, age, email)
    values('{name}', '{sex}', {age}, '{email}')
    """
    print(sql)

    db.insert_or_update_data(sql)
    return "success"


@app.route("/show_users")
def show_users():
    sql = "select id, name from user"
    data = db.query_data(sql)
    return render_template("show_users.html", data = data)


@app.route("/show_user/<user_id>")
def show_user(user_id):
    sql = "select * from user where id=" + user_id
    data = db.query_data(sql)
    user = data[0]
    return render_template("show_user.html", user=user)


@app.route("/show_echarts")
def show_echarts():
    xdata = ["衬衫","羊毛衫","雪纺衫","裤子","高跟鞋","袜子"]
    ydata = [5, 20, 36, 10, 10, 20]
    return render_template("show_echarts.html", xdata=Markup(json.dumps(xdata)), ydata=Markup(json.dumps(ydata)))


@app.route("/show_pyecharts")
def show_pyecharts():
    bar = (
        Bar()
            .add_xaxis(["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"])
            .add_yaxis("商家A", [5, 20, 36, 10, 75, 90])
    )
    return render_template("show_pyecharts.html", bar_options=bar.dump_options())


if __name__ == '__main__':
    app.run()
