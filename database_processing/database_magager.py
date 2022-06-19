"""
Author: Rosenyoung
This module manages tables of high frequency data
This module can manage tables of all available contracts, and can delete tables of contacts that are overtime.

Version 1.0 2022-06-18

"""

import json
import pandas as pd
import numpy as np
import os
from database_connection import DataBaseConn
import datetime

class DatabaseManager:
    def __init__(self):
        # Database connection
        database_conn = DataBaseConn("test1") # Change database name here
        self.__engine = database_conn.engine
        self.__data_conn = database_conn.conn
        self.__cur = database_conn.cur

        # Get current date
        self.__current_date = datetime.date.today()

        # Current contract list in database
        self.__current_contract_list = list(database_conn.read_contract_list(length=5000)["ContractId"])

        # Requested contract list from CTP
        self.__requested_contract_list =[]
        self.__filename = "instruments" # You can adjust the filename here


    def del_contract_list(self, period = 60):
        """
        This function is used to delete high frequency contract data on a time-rolling basis
        Delete all high frequency tables created before 60 days
        """
        overtime_list_sql = f"""
        SELECT
            ContractId 
        FROM
            contract_list 
        WHERE
            IsAvailable = 1 
            AND UpdDate < date_add('{self.__current_date}', interval -{period} day)
        """

        overtime_list_df = pd.read_sql_query(overtime_list_sql, self.__engine)
        overtime_list = list(overtime_list_df["ContractId"])

        for code in overtime_list:
            # Drop this table
            table_name = "high_freq_" + code
            delete_sql = f"""
            DROP TABLE IF EXISTS `{table_name}`;
            """

            # Update `contract_list`. Turn `Isavailable` to 0
            upd_sql = f"""
            UPDATE contract_list 
            SET IsAvailable = 0 
            WHERE
                ContractId = '{code}'
            """


            print(delete_sql)
            print(upd_sql)

            try:
                self.__cur.execute(delete_sql)
                self.__cur.execute(upd_sql)
                self.__data_conn.commit()
            except Exception as err:
                print(f"Error occurs in mysql: {err}")

        print(f"High frequency data before {period} days has been deleted!")

    def upd_contract_list(self):
        """
        Update the contract list according to the daily requested contract information from CTP
        This function get today's available contract ID from json file, and check whether these contract IDs are recorded
        in the table 'contract_list' in database.
        If not, this function will create a new table of this contract ID, and update this ID into `contract_list`
        """
        # Read current available contracts from CTP json file
        filepath = os.path.join(os.getcwd(), f'{self.__filename}.json')
        with open(filepath, 'r') as f:
            configs = json.load(f)  # Read json and return a list of dict
            for item in configs:
                self.__requested_contract_list.append(item["InstrumentID"])
        print(self.__requested_contract_list)
        print(self.__current_contract_list)
        print(len(self.__requested_contract_list))

        available_status = 1 # Set the `Isavailable` to 1


        # Create new tables if a contract in today's list requested from CTP is not in current `contract_list`.
        for code in self.__requested_contract_list:
            if code not in self.__current_contract_list:
                database_name = "high_freq_" + code
                create_table_sql = f"""
                CREATE TABLE `{database_name}`  (
                  `ContractId` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
                  `TimeIndex` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
                  `LastPrice` decimal(10, 2) NULL DEFAULT 0.00,
                  `Volume` int(10) UNSIGNED ZEROFILL NULL DEFAULT NULL COMMENT 'Cumulative volume dealed',
                  `CumulTurnover` bigint(20) UNSIGNED ZEROFILL NULL DEFAULT NULL COMMENT 'Cumulative turnover money value',
                  `OpenInt` int(10) UNSIGNED ZEROFILL NULL DEFAULT NULL,
                  `BidPrice_1` decimal(10, 2) NULL DEFAULT 0.00,
                  `BidPrice_2` decimal(10, 2) NULL DEFAULT 0.00,
                  `BidPrice_3` decimal(10, 2) NULL DEFAULT 0.00,
                  `BidPrice_4` decimal(10, 2) NULL DEFAULT 0.00,
                  `BidPrice_5` decimal(10, 2) NULL DEFAULT 0.00,
                  `AskPrice_1` decimal(10, 2) NULL DEFAULT 0.00,
                  `AskPrice_2` decimal(10, 2) NULL DEFAULT 0.00,
                  `AskPrice_3` decimal(10, 2) NULL DEFAULT 0.00,
                  `AskPrice_4` decimal(10, 2) NULL DEFAULT 0.00,
                  `AskPrice_5` decimal(10, 2) NULL DEFAULT 0.00,
                  `BidVolume_1` int(8) UNSIGNED ZEROFILL NULL DEFAULT NULL,
                  `BidVolume_2` int(8) UNSIGNED ZEROFILL NULL DEFAULT NULL,
                  `BidVolume_3` int(8) UNSIGNED ZEROFILL NULL DEFAULT NULL,
                  `BidVolume_4` int(8) UNSIGNED ZEROFILL NULL DEFAULT NULL,
                  `BidVolume_5` int(8) UNSIGNED ZEROFILL NULL DEFAULT NULL,
                  `AskVolume_1` int(8) UNSIGNED ZEROFILL NULL DEFAULT NULL,
                  `AskVolume_2` int(8) UNSIGNED ZEROFILL NULL DEFAULT NULL,
                  `AskVolume_3` int(8) UNSIGNED ZEROFILL NULL DEFAULT NULL,
                  `AskVolume_4` int(8) UNSIGNED ZEROFILL NULL DEFAULT NULL,
                  `AskVolume_5` int(8) UNSIGNED ZEROFILL NULL DEFAULT NULL,
                  PRIMARY KEY (`ContractId`, `TimeIndex`) USING BTREE
                ) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;
                """

                # Update contract_list
                upd_contract_list_sql = f"""
                INSERT INTO contract_list (`ContractId`, `UpdDate`, `IsAvailable`)
                    VALUES ('{code}', '{self.__current_date}', {available_status})
                """
                try:
                    self.__cur.execute(create_table_sql)
                    self.__cur.execute(upd_contract_list_sql)
                    self.__data_conn.commit()
                except Exception as err:
                    print(f"Error occurs in mysql: {err}")

        print("Contract list has been updated!")



if __name__ == "__main__":
    database_mng = DatabaseManager()
    database_mng.upd_contract_list()
    database_mng.del_contract_list()