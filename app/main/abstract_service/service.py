# 业务逻辑层
import sys
sys.path
from app.main.abstract_service import db
import time

# 插入model
def insert_model(model):
    # 系统现在时间
    time_now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    model["timestamp"] = time_now

    sql = """
            insert
            into
            auto_abstract_model(parameters, input, output, picture, timestamp)
            values(%s, %s, %s, %s, %s)
            """
    insert_model_tuple = (model["parameters"], model["input"], model["output"], model["picture"], model["timestamp"])
    print(sql)
    ret=db.insert_with_param(sql, insert_model_tuple)
    return ret



# 根据id查询model
def select_model(model_id):
    sql = "select * from auto_abstract_model where model_id = " + str(model_id)
    print(sql)
    model = db.query_data(sql)[0]
    return model


# 插入历史
def insert_history(history):
    # 系统现在时间
    time_now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    sql = """
            insert
            into
            auto_abstract_history(title, content, abstract, model_id, timestamp)
            values(%s, %s, %s, %s, %s)
    """
    insert_history_tuple = (history["title"], history["content"], history["abstract"], history["model_id"], time_now)
    print(sql)
    ret = db.insert_with_param(sql, insert_history_tuple)
    return ret


# TODO 按查询参数模糊查询所有历史
# def select_history(history):
#     sql = "select * from auto_abstract_history where title like %s and content like %s " \
#           "and abstract like %s and model_id = %s and timestamp = %s"
#
#     title_like = "%" + history["title"] + "%"
#     content_like = "%" + history["content"] + "%"
#     abstract_like = "%%"
#     model_id = "%%"
#     timestamp = "%%"
#     # abstract_like = "%" + history["abstract"] + "%"
#     # model_id = history["model_id"]
#     # timestamp = history["timestamp"]
#     select_history_tuple = {title_like, content_like, abstract_like, model_id, timestamp}
#     histories = db.query_data_with_param(sql, select_history_tuple)
#     return histories

def select_history():
    sql = "select * from auto_abstract_history"
    histories = db.query_data(sql)
    return histories

# 从数据库查出二进制数据写到硬盘./picture
def store_picture():
    sql = """
        select input, picture from auto_abstract_model
        """
    data = db.query_data(sql)
    for datum in data:
        filename = datum["input"]
        pic = datum["picture"]
        print(type(pic))
        fw = open('./picture/' + filename + '.png', 'wb')
        fw.write(pic)
        fw.close
    print(len(data))
    print(data)


if __name__ == '__main__':
    histories = select_history()
    print(histories)