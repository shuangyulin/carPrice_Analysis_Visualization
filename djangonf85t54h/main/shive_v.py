import configparser
import re
import json
import os
import mysql.connector
from django.http import JsonResponse
from hdfs import InsecureClient
from pyhive import hive
import csv
from util.configread import config_read
from util.CustomJSONEncoder import CustomJsonEncoder
from util.codes import normal_code, system_error_code
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, date_format
import shutil
# 获取当前文件路径的根目录
parent_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

m_username = "Administrator"
hadoop_client = InsecureClient('http://localhost:9870')

dbtype, host, port, user, passwd, dbName, charset,hasHadoop = config_read(os.path.join(parent_directory,"config.ini"))

#将mysql里的相关表转成hive库里的表
def migrate_to_hive():

    mysql_conn = mysql.connector.connect(
        host=host,
        port=port,
        user=user,
        password=passwd,
        database=dbName
    )
    cursor = mysql_conn.cursor()

    hive_conn = hive.Connection(
        host='localhost',
        port=10000,
        username=m_username,
    )
    hive_cursor = hive_conn.cursor()
    #创建Hive数据库（如果不存在）
    hive_cursor.execute(f"CREATE DATABASE IF NOT EXISTS {dbName}")
    hive_cursor.execute(f"USE {dbName}")

    yonghu_table_path=f'/user/hive/warehouse/{dbName}.db/yonghu'
    #删除已有的hive表
    if hadoop_client.status(yonghu_table_path,strict=False):
        hadoop_client.delete(yonghu_table_path, recursive=True)
    # 在Hive中删除表
    yonghu_drop_table_query = f"""DROP TABLE yonghu"""
    hive_cursor.execute(yonghu_drop_table_query)
    cursor.execute("SELECT * FROM yonghu")
    yonghu_column_info = cursor.fetchall()
    #将数据写入 CSV 文件
    yonghu_path = os.path.join(parent_directory, "yonghu.csv")
    with open(yonghu_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        # 写入数据行
        for row in yonghu_column_info:
            writer.writerow(row)
    yonghu_spakr_clear(yonghu_path)
    cursor.execute("DESCRIBE yonghu")
    yonghu_column_info = cursor.fetchall()
    create_table_query = "CREATE TABLE IF NOT EXISTS yonghu ("
    for column, data_type, _, _, _, _ in yonghu_column_info:
        match = re.match(r'(\w+)(\(\d+\))?', data_type)
        mysql_type = match.group(1)
        hive_data_type = get_hive_type(mysql_type)
        create_table_query += f"{column} {hive_data_type}, "
    yonghu_create_table_query = create_table_query[:-2] + ") row format delimited fields terminated by ','"
    hive_cursor.execute(yonghu_create_table_query)
    # 上传映射文件
    yonghu_hdfs_csv_path = f'/user/hive/warehouse/{dbName}.db/yonghu'
    hadoop_client.upload(yonghu_hdfs_csv_path, yonghu_path)
    wodedinggou_table_path=f'/user/hive/warehouse/{dbName}.db/wodedinggou'
    #删除已有的hive表
    if hadoop_client.status(wodedinggou_table_path,strict=False):
        hadoop_client.delete(wodedinggou_table_path, recursive=True)
    # 在Hive中删除表
    wodedinggou_drop_table_query = f"""DROP TABLE wodedinggou"""
    hive_cursor.execute(wodedinggou_drop_table_query)
    cursor.execute("SELECT * FROM wodedinggou")
    wodedinggou_column_info = cursor.fetchall()
    #将数据写入 CSV 文件
    wodedinggou_path = os.path.join(parent_directory, "wodedinggou.csv")
    with open(wodedinggou_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        # 写入数据行
        for row in wodedinggou_column_info:
            writer.writerow(row)
    wodedinggou_spakr_clear(wodedinggou_path)
    cursor.execute("DESCRIBE wodedinggou")
    wodedinggou_column_info = cursor.fetchall()
    create_table_query = "CREATE TABLE IF NOT EXISTS wodedinggou ("
    for column, data_type, _, _, _, _ in wodedinggou_column_info:
        match = re.match(r'(\w+)(\(\d+\))?', data_type)
        mysql_type = match.group(1)
        hive_data_type = get_hive_type(mysql_type)
        create_table_query += f"{column} {hive_data_type}, "
    wodedinggou_create_table_query = create_table_query[:-2] + ") row format delimited fields terminated by ','"
    hive_cursor.execute(wodedinggou_create_table_query)
    # 上传映射文件
    wodedinggou_hdfs_csv_path = f'/user/hive/warehouse/{dbName}.db/wodedinggou'
    hadoop_client.upload(wodedinggou_hdfs_csv_path, wodedinggou_path)
    qichexinxi_table_path=f'/user/hive/warehouse/{dbName}.db/qichexinxi'
    #删除已有的hive表
    if hadoop_client.status(qichexinxi_table_path,strict=False):
        hadoop_client.delete(qichexinxi_table_path, recursive=True)
    # 在Hive中删除表
    qichexinxi_drop_table_query = f"""DROP TABLE qichexinxi"""
    hive_cursor.execute(qichexinxi_drop_table_query)
    cursor.execute("SELECT * FROM qichexinxi")
    qichexinxi_column_info = cursor.fetchall()
    #将数据写入 CSV 文件
    qichexinxi_path = os.path.join(parent_directory, "qichexinxi.csv")
    with open(qichexinxi_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        # 写入数据行
        for row in qichexinxi_column_info:
            writer.writerow(row)
    qichexinxi_spakr_clear(qichexinxi_path)
    cursor.execute("DESCRIBE qichexinxi")
    qichexinxi_column_info = cursor.fetchall()
    create_table_query = "CREATE TABLE IF NOT EXISTS qichexinxi ("
    for column, data_type, _, _, _, _ in qichexinxi_column_info:
        match = re.match(r'(\w+)(\(\d+\))?', data_type)
        mysql_type = match.group(1)
        hive_data_type = get_hive_type(mysql_type)
        create_table_query += f"{column} {hive_data_type}, "
    qichexinxi_create_table_query = create_table_query[:-2] + ") row format delimited fields terminated by ','"
    hive_cursor.execute(qichexinxi_create_table_query)
    # 上传映射文件
    qichexinxi_hdfs_csv_path = f'/user/hive/warehouse/{dbName}.db/qichexinxi'
    hadoop_client.upload(qichexinxi_hdfs_csv_path, qichexinxi_path)
    cursor.close()
    mysql_conn.close()
    hive_cursor.close()
    hive_conn.close()

#转换成hive的类型
def get_hive_type(mysql_type):
    type_mapping = {
        'INT': 'INT',
        'BIGINT': 'BIGINT',
        'FLOAT': 'FLOAT',
        'DOUBLE': 'DOUBLE',
        'DECIMAL': 'DECIMAL',
        'VARCHAR': 'STRING',
        'TEXT': 'STRING',
    }
    if isinstance(mysql_type, str):
        mysql_type = mysql_type.upper()
    return type_mapping.get(str(mysql_type), 'STRING')

#执行hive查询
def hive_query():
    # 连接到Hive服务器
    conn = hive.Connection(host='localhost', port=10000, username=m_username,database=dbName)
    # 创建一个游标对象
    cursor = conn.cursor()
    try:

        #定义Hive查询语句
        xingbie_query = "SELECT COUNT(*) AS total, xingbie FROM yonghu GROUP BY xingbie"
        # 执行Hive查询语句
        cursor.execute(xingbie_query)
        # 获取查询结果
        xingbie_results = cursor.fetchall()
        xingbie_json_list=[]
        for row in xingbie_results:
            xingbie_json_list.append({"xingbie":row[1],"total":row[0]})
        #将JSON数据写入文件
        with open(os.path.join(parent_directory, "yonghu_groupxingbie.json"), 'w', encoding='utf-8') as f:
            json.dump(xingbie_json_list, f, ensure_ascii=False, indent=4)


        #定义Hive查询语句
        qichemingcheng_query = "SELECT COUNT(*) AS total, qichemingcheng FROM wodedinggou GROUP BY qichemingcheng"
        # 执行Hive查询语句
        cursor.execute(qichemingcheng_query)
        # 获取查询结果
        qichemingcheng_results = cursor.fetchall()
        qichemingcheng_json_list=[]
        for row in qichemingcheng_results:
            qichemingcheng_json_list.append({"qichemingcheng":row[1],"total":row[0]})
        #将JSON数据写入文件
        with open(os.path.join(parent_directory, "wodedinggou_groupqichemingcheng.json"), 'w', encoding='utf-8') as f:
            json.dump(qichemingcheng_json_list, f, ensure_ascii=False, indent=4)


        #定义Hive查询语句
        tjtime_query = "SELECT COUNT(*) AS total, tjtime FROM qichexinxi GROUP BY tjtime"
        # 执行Hive查询语句
        cursor.execute(tjtime_query)
        # 获取查询结果
        tjtime_results = cursor.fetchall()
        tjtime_json_list=[]
        for row in tjtime_results:
            tjtime_json_list.append({"tjtime":row[1],"total":row[0]})
        #将JSON数据写入文件
        with open(os.path.join(parent_directory, "qichexinxi_grouptjtime.json"), 'w', encoding='utf-8') as f:
            json.dump(tjtime_json_list, f, ensure_ascii=False, indent=4)


        #定义Hive查询语句
        seriesname_query = "SELECT COUNT(*) AS total, seriesname FROM qichexinxi GROUP BY seriesname"
        # 执行Hive查询语句
        cursor.execute(seriesname_query)
        # 获取查询结果
        seriesname_results = cursor.fetchall()
        seriesname_json_list=[]
        for row in seriesname_results:
            seriesname_json_list.append({"seriesname":row[1],"total":row[0]})
        #将JSON数据写入文件
        with open(os.path.join(parent_directory, "qichexinxi_groupseriesname.json"), 'w', encoding='utf-8') as f:
            json.dump(seriesname_json_list, f, ensure_ascii=False, indent=4)

        where = ' WHERE 1 = 1 '
        seriesname_query = f'''SELECT `seriesname`, ROUND(SUM(`scorevalue`), 2) AS `total`
            FROM qichexinxi {where} GROUP BY `seriesname`'''
        #执行Hive查询语句
        cursor.execute(seriesname_query)
        # 获取查询结果
        seriesname_results = cursor.fetchall()
        seriesname_json_list=[]
        for row in seriesname_results:
            seriesname_json_list.append({"seriesname":row[0],"total":row[1]})
        #将JSON数据写入文件
        with open(os.path.join(parent_directory, "qichexinxi_valueseriesnamescorevalue.json"), 'w', encoding='utf-8') as f:
            json.dump(seriesname_json_list, f, ensure_ascii=False, indent=4)
        where = ' WHERE 1 = 1 '
        seriesname_query = f'''SELECT `seriesname`, ROUND(SUM(`salecount`), 2) AS `total`
            FROM qichexinxi {where} GROUP BY `seriesname`'''
        #执行Hive查询语句
        cursor.execute(seriesname_query)
        # 获取查询结果
        seriesname_results = cursor.fetchall()
        seriesname_json_list=[]
        for row in seriesname_results:
            seriesname_json_list.append({"seriesname":row[0],"total":row[1]})
        #将JSON数据写入文件
        with open(os.path.join(parent_directory, "qichexinxi_valueseriesnamesalecount.json"), 'w', encoding='utf-8') as f:
            json.dump(seriesname_json_list, f, ensure_ascii=False, indent=4)
        where = ' WHERE 1 = 1 '
        seriesname_query = f'''SELECT `seriesname`, ROUND(SUM(`minprice`), 2) AS `total`
            FROM qichexinxi {where} GROUP BY `seriesname`'''
        #执行Hive查询语句
        cursor.execute(seriesname_query)
        # 获取查询结果
        seriesname_results = cursor.fetchall()
        seriesname_json_list=[]
        for row in seriesname_results:
            seriesname_json_list.append({"seriesname":row[0],"total":row[1]})
        #将JSON数据写入文件
        with open(os.path.join(parent_directory, "qichexinxi_valueseriesnameminprice.json"), 'w', encoding='utf-8') as f:
            json.dump(seriesname_json_list, f, ensure_ascii=False, indent=4)
        pass
    except Exception as e:
         print(f"An error occurred: {e}")
    finally:
        # 关闭游标和连接
        cursor.close()
        conn.close()

#spark数据清洗和预处理
def yonghu_spakr_clear(csvpath):
    try:
        #创建Spark会话
        spark = SparkSession.builder.appName("djangonf85t54h").getOrCreate()
        df = spark.read.csv(csvpath, header=False, inferSchema=True)
        df = df.toDF(
            "id",
            "addtime",
            "yonghuzhanghao",
            "mima",
            "yonghuxingming",
            "touxiang",
            "shoujihao",
            "xingbie",
        )
        #显示原始数据
        df.show()
        #1.删除空值
        df_cleaned = df.dropna()
        #2.去除重复行
        df_cleaned = df_cleaned.dropDuplicates()
        df_cleaned = df_cleaned.withColumn("addtime", date_format(col("addtime"), 'yyyy-MM-dd HH:mm:ss'))
        #显示清洗后的数据
        df_cleaned.show()
        #保存清洗后的数据
        print(type(df_cleaned))
        output_path = 'yonghu_output_dir'  # 输出的目录
        df_cleaned.coalesce(1).write.csv(output_path, header=False, mode="overwrite")
        #手动移动生成的 CSV 文件到目标路径，并重命名
        for filename in os.listdir(output_path):
            if filename.startswith("part-") and filename.endswith(".csv"):
                shutil.move(os.path.join(output_path, filename), csvpath)
        #清理临时目录
        shutil.rmtree(output_path)
        #停止Spark会话
        spark.stop()
    except Exception as e:
        print("e:",e)
#spark数据清洗和预处理
def wodedinggou_spakr_clear(csvpath):
    try:
        #创建Spark会话
        spark = SparkSession.builder.appName("djangonf85t54h").getOrCreate()
        df = spark.read.csv(csvpath, header=False, inferSchema=True)
        df = df.toDF(
            "id",
            "addtime",
            "dingdanbianhao",
            "qichemingcheng",
            "qichetupian",
            "qichepinpai",
            "qicheleixing",
            "shoujia",
            "kucun",
            "shijijiage",
            "tianchuang",
            "zuowei",
            "qichepailiang",
            "shangshinianfen",
            "goumaishijian",
            "dingdanzhuangtai",
            "yonghuzhanghao",
            "yonghuxingming",
            "ispay",
        )
        #显示原始数据
        df.show()
        #1.删除空值
        df_cleaned = df.dropna()
        #2.去除重复行
        df_cleaned = df_cleaned.dropDuplicates()
        df_cleaned = df_cleaned.withColumn("addtime", date_format(col("addtime"), 'yyyy-MM-dd HH:mm:ss'))
        df_cleaned = df_cleaned.withColumn("goumaishijian", date_format(col("goumaishijian"), 'yyyy-MM-dd HH:mm:ss'))
        #显示清洗后的数据
        df_cleaned.show()
        #保存清洗后的数据
        print(type(df_cleaned))
        output_path = 'wodedinggou_output_dir'  # 输出的目录
        df_cleaned.coalesce(1).write.csv(output_path, header=False, mode="overwrite")
        #手动移动生成的 CSV 文件到目标路径，并重命名
        for filename in os.listdir(output_path):
            if filename.startswith("part-") and filename.endswith(".csv"):
                shutil.move(os.path.join(output_path, filename), csvpath)
        #清理临时目录
        shutil.rmtree(output_path)
        #停止Spark会话
        spark.stop()
    except Exception as e:
        print("e:",e)
#spark数据清洗和预处理
def qichexinxi_spakr_clear(csvpath):
    try:
        #创建Spark会话
        spark = SparkSession.builder.appName("djangonf85t54h").getOrCreate()
        df = spark.read.csv(csvpath, header=False, inferSchema=True)
        df = df.toDF(
            "id",
            "addtime",
            "detailurl",
            "tjtime",
            "seriesname",
            "imgurl",
            "scorevalue",
            "salecount",
            "ranknum",
            "minprice",
            "maxprice",
            "priceinfo",
            "brandid",
            "thumbsupnum",
            "crazilynum",
            "clicktime",
            "clicknum",
            "discussnum",
            "storeupnum",
        )
        #显示原始数据
        df.show()
        #1.删除空值
        df_cleaned = df.dropna()
        #2.去除重复行
        df_cleaned = df_cleaned.dropDuplicates()
        df_cleaned = df_cleaned.withColumn("addtime", date_format(col("addtime"), 'yyyy-MM-dd HH:mm:ss'))
        df_cleaned = df_cleaned.withColumn("clicktime", date_format(col("clicktime"), 'yyyy-MM-dd HH:mm:ss'))
        #显示清洗后的数据
        df_cleaned.show()
        #保存清洗后的数据
        print(type(df_cleaned))
        output_path = 'qichexinxi_output_dir'  # 输出的目录
        df_cleaned.coalesce(1).write.csv(output_path, header=False, mode="overwrite")
        #手动移动生成的 CSV 文件到目标路径，并重命名
        for filename in os.listdir(output_path):
            if filename.startswith("part-") and filename.endswith(".csv"):
                shutil.move(os.path.join(output_path, filename), csvpath)
        #清理临时目录
        shutil.rmtree(output_path)
        #停止Spark会话
        spark.stop()
    except Exception as e:
        print("e:",e)
    # hive分析
def shive_analyze(request):
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code, "msg": "成功", "data": {}}
        try:
            migrate_to_hive()
            hive_query()
            return JsonResponse(msg, encoder=CustomJsonEncoder)
        except Exception as e:
            msg['code'] = system_error_code
            msg['msg'] = f"发生错误：{e}"
            return JsonResponse(msg, encoder=CustomJsonEncoder)



