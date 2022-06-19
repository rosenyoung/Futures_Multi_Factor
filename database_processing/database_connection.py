"""

Author: Rosenyoung
This module creates connection to different database
This module can also contain functions to query data. These functions can be added in later versions

Version 1.0 2022-06-17

"""

import pandas as pd
import os
import yaml

from sqlalchemy import create_engine
import pymysql


class DataBaseConn:
    def __init__(self, database_name):
        self.__database_username = "user"
        self.__database_password = "password"
        self.__database_ip = "ip"
        self.__database_port = 0000
        self.__database_name = database_name

        # Read config parameters from YAML
        self.__read_yaml()

        self.engine = create_engine('mysql+pymysql://{0}:{1}@{2}/{3}'.
                                    format(self.__database_username, self.__database_password,
                                           self.__database_ip, self.__database_name))

        self.conn = pymysql.connect(host=self.__database_ip,
                                    user=self.__database_username,
                                    password=self.__database_password,
                                    database=self.__database_name,
                                    port=self.__database_port,
                                    )

        print(f"Database {self.__database_name} connected!")

        self.cur = self.conn.cursor()

    def read_contract_list(self, length=5000):
        """
            Request list of current available contract
        """
        if self.__database_name == "test1":

            list_sql = f"""
                               SELECT
                                    * 
                                FROM `contract_list` 
                                WHERE IsAvailable = 1
                                ORDER BY `UpdDate` LIMIT {length} 
    
            """

            list_df = pd.read_sql_query(list_sql, self.engine)

            return list_df

        else:
            print("This function is only available when connecting to database test1!")

    def close_conn(self):
        self.conn.close()

    # Read database config from YAML
    def __read_yaml(self):
        filepath = os.path.join(os.getcwd(), 'database_config.yaml')  # The config.yaml should be under same path as py
        with open(filepath, 'r') as f:
            configs = yaml.load(f, Loader=yaml.FullLoader)  # Read yaml and return a dict
        # Find the config of current database
        for code in configs['database']:
            if configs['database'][code]['name'] == self.__database_name:
                self.__database_username = configs['database'][code]['username']
                self.__database_ip = configs['database'][code]['ip']
                self.__database_port = configs['database'][code]['port']
                self.__database_password = configs['database'][code]['password']





if __name__ == "__main__":
    database_conn = DataBaseConn("ibapi")
    list = database_conn.read_contract_list()
    print(list)
    # print(df.head(10))