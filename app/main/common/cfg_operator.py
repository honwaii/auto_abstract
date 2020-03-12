#!/usr/bin/python
# -*- coding: utf-8 -*-
from configparser import ConfigParser

path = "../../configuration.cfg"


class Configuration:
    configs = None

    def __init__(self, path):
        super().__init__()
        self.path = path
        self.configs = ConfigParser()
        self.configs.read(path, encoding='utf-8')

    def get_all_configs(self):
        """
        :return: 所有的配置的列表，[(配置名，配置的值)]
        """
        cp = self.configs
        # 得到所有的section，以列表的形式返回
        section = cp.sections()[0]
        # 得到该section的所有键值对
        return cp.items(section)

    def get_config(self, config_name: str):
        section = self.configs.sections()[0]
        return self.configs.get(section, config_name)


configuration = Configuration(path)
