import os
import sys
import pymysql
from impala.dbapi import connect

module = sys.argv[1]
tenantid = sys.argv[2]
tenantsid = sys.argv[3]

print(f'module: {module}')
print(f'tenantid：{tenantid}')
print(f'tenantsid：{tenantsid}')


impala_db = {
    'host': 'ddp-impala-jdbc.digiwincloud.com',
    'port': 21051,
    'user': 'tbb',
    'password': 'tbb123',
    'charset': 'utf8mb4',
    'database': 'tbb'
}

mysql_db = {
    'host': 'dap-mariadb.mariadb.database.azure.com',
    'port': 3306,
    'user': 'rootadmin@dap-mariadb',
    'password': 'dcms@123',
    'charset': 'utf8mb4',
    'database': 'tbb_saas_datacenter'
}

impala_sql = {
    'e10indicator': [
        '/opt/E10CN/tbb_temp_kongdata.sql',
        '/opt/E10CN/e10indicator_data.sql'
    ],
    'yfindicator': [
        '/opt/E10CN/tbb_temp_kongdata.sql'
    ],
    'cmdop': [
        '/opt/E10TW/tbb_temp_kongdata.sql',
        '/opt/E10TW/wf_iwc_data_tw.sql'
    ],
    'T100': [
        '/opt/E10TW/tbb_temp_kongdata.sql',
        '/opt/E10TW/t100_demo_data.sql'
    ],
    'TipTop': [
        '/opt/E10TW/tbb_temp_kongdata.sql',
        '/opt/E10TW/tiptop_demo_data.sql'
    ]    
}

mysql_sql = {
    'e10indicator': [
        '/opt/E10CN/tbb_temp_kong.sql',
        '/opt/E10CN/e10indicator.sql'
    ],
    'yfindicator': [
        '/opt/E10CN/tbb_temp_kong.sql',
        '/opt/E10CN/yfindicator.sql'
    ],
    'cmdop': [
        '/opt/E10TW/tbb_temp_kong.sql',
        '/opt/E10TW/wf_iwc_tw.sql'
    ],
    'T100': [
        '/opt/E10TW/tbb_temp_kong.sql',
        '/opt/E10TW/t100_demo.sql'
    ],
    'TipTop': [
        '/opt/E10TW/tbb_temp_kong.sql',
        '/opt/E10TW/tiptop_demo.sql'
    ]
}

def replace_placeholder_in_sql(sql_file, tenantid, tenantsid):
    with open(sql_file, 'r', encoding='utf-8') as file:
        sql_content = file.read()
        replaced_sql_content = sql_content.replace('TO_BE_REPLACE_tenantId', tenantid).replace('TO_BE_REPLACE_tenantSid', tenantsid)
        return replaced_sql_content

def write_tmp_sql_file(sql_content, sql_file):
    # 将替换后的 SQL 内容写入临时文件
    tmp_sql_file = sql_file + '_tmp'
    with open(tmp_sql_file, 'w', encoding='utf-8') as file:
        file.write(sql_content)
    return tmp_sql_file

def execute_sql_from_tmp_file(sql_file, cursor, tenantid, tenantsid):
    replaced_sql_content = replace_placeholder_in_sql(sql_file, tenantid, tenantsid)
    print(f"执行的 SQL 内容为：\n{replaced_sql_content}")  # 输出 SQL 内容
    tmp_sql_file = write_tmp_sql_file(replaced_sql_content, sql_file)
    try:
        with open(tmp_sql_file, 'r', encoding='utf-8') as file:
            sql_commands = file.read().split(';')
            for command in sql_commands:
                if command.strip():  # 检查命令是否为空
                    try:
                        print(f"正在执行 SQL 语句：{command}")
                        cursor.execute(command)
                        print(f"SQL 语句执行成功")
                    except Exception as e:
                        print(f"执行 SQL 语句时发生异常: {e}")
            # 添加 commit 操作，确保它与前面的代码是相匹配的
            cursor.execute("COMMIT")
            print("执行 commit 操作")
    except Exception as e:
        print(f"执行 SQL 语句时发生异常: {e}")
    finally:
        os.remove(tmp_sql_file)  # 执行完成后删除临时文件


# 修改 execute_sql_by_id 函数，调用 execute_sql_from_tmp_file
def execute_sql_by_id(module, db_info, sql_map, tenantid, tenantsid):
    try:
        if 'impala' in db_info:
            with connect(host=db_info['impala']['host'], port=db_info['impala']['port'],
                         user=db_info['impala']['user'], password=db_info['impala']['password'],
                         database=db_info['impala']['database']) as conn:
                with conn.cursor() as cursor:
                    cursor.execute('SHOW DATABASES')
                    databases = cursor.fetchall()
                    print('数据库连通性正常')

                    if module in sql_map:
                        sql_files = sql_map[module]
                        for file in sql_files:
                            execute_sql_from_tmp_file(file, cursor, tenantid, tenantsid)

                    print('执行完成')

        elif 'mysql' in db_info:  # 添加MySQL的检查
            conn = pymysql.connect(host=db_info['mysql']['host'], port=db_info['mysql']['port'],
                                  user=db_info['mysql']['user'], password=db_info['mysql']['password'],
                                  database=db_info['mysql']['database'], charset='utf8mb4')
            with conn.cursor() as cursor:
                print('数据库连通性正常')

                if module in sql_map:
                    sql_files = sql_map[module]
                    for file in sql_files:
                        execute_sql_from_tmp_file(file, cursor, tenantid, tenantsid)
                conn.commit()    

                print('执行完成')
    except Exception as e:
        print('数据库连接失败:', e)

# 添加执行 Impala 和 MySQL SQL 的代码

# 执行 Impala SQL
try:
    execute_sql_by_id(module, {'impala': impala_db}, impala_sql, tenantid, tenantsid)
except Exception as e:
    print('发生异常:', e)

# 执行 MySQL SQL
try:
    execute_sql_by_id(module, {'mysql': mysql_db}, mysql_sql, tenantid, tenantsid)
except Exception as e:
    print('发生异常:', e)
