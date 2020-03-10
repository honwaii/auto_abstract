from app.main.abstract_service import db
import pymysql
import pprint
from app.main.abstract_service import service


class TestClass:

    # 测试存储照片到硬盘
    def test_store_picture(self):
        service.store_picture()

    # 测试service.insert_model
    def test_insert_model(self):
        fp = open("../data_preprocessing/Step 1/output_picture/tsne_picture_output_5.png", 'rb')
        png = fp.read()
        fp.close()
        model = {
            "parameters": "yingyong",
            "input": "编程",
            "output": '[[1, 2, 3, 4], [5, 5, 5, 5]]',
            "picture": png
        }
        service.insert_model(model)

    # 测试service.insert_history
    def test_insert_history(self):
        histories = [
            {
                "title": "0000000000000000",
                "content": "ContentContentContentContentContentContent",
                "abstract": "AbstractAbstractAbstract",
                "model_id": 1
            },
            {
                "title": "111111111111111",
                "content": "ContentContentContentContentContentContent",
                "abstract": "AbstractAbstractAbstract",
                "model_id": 2
            },
            {
                "title": "2222222222222222",
                "content": "ContentContentContentContentContentContent",
                "abstract": "AbstractAbstractAbstract",
                "model_id": 3
            },
            {
                "title": "3333333333333333",
                "content": "abc--test",
                "abstract": "AbstractAbstractAbstract",
                "model_id": 4
            },
            {
                "title": "4444444444444444",
                "content": "ContentContentContentContentContentContent",
                "abstract": "AbstractAbstractAbstract",
                "model_id": 5
            }
        ]
        history = histories[3]
        ret = service.insert_history(history)
        print(ret)
        # assert(service.insert_history(history))

    # 测试service.select_history
    def test_select_history(self):
        history = {
            "title": "333",
            "content": "test"
        }
        histories = service.select_history(history)
        pprint.pprint(histories)