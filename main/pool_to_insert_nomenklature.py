#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""  
******************************************************************************
***************     Скрипт проставления номенклатуры по http        **********
******************************************************************************
"""
import re
import os
import base64
import logging
import traceback
import httpimport
import configparser
import multiprocessing
from ctypes import c_ulong, windll
from mod_control import control_version, control_hhtpimport, VariableUrlGitLab

httpimport.INSECURE = True
logger = logging.getLogger()
logger.setLevel(logging.INFO)
log_format = '%(asctime)s: %(message)s'
logging.basicConfig(format=log_format,
                    filename=os.path.join(
                        os.path.abspath(os.curdir), 'log.txt'),
                    datefmt='%Y-%m-%d %H:%M:%S')

url = f"http://{base64.b64decode(VariableUrlGitLab.HOST).decode()}"
with httpimport.remote_repo(["verify_txt", "log_in", "hundred_cart", "check_element_in_list", "read_id_archive", "send_id_cart_nomenklature", "utils"], url):
    from verify_txt import verify
    from log_in import log_in
    from hundred_cart import hundred_cart
    from check_element_in_list import check_element_in_list
    from read_id_archive import read_id_archive
    from send_id_cart_nomenklature import send_id_cart_nomenklature
    from utils import errMessage, succesfully, func_list_tread, moving_all


class Variable:
    """
    List of all variables
    """

    ###  Настройки из .ini  ###
    path = os.path.abspath(os.curdir)
    pathSet = os.path.join(path, 'settings.ini')
    config = configparser.ConfigParser()
    config.read(pathSet)

    Attribute = config['Attribute']
    process = Attribute['process']
    hidden_browser = Attribute['hidden_browser']

    UserCustom = config['UserCustom']
    ip = UserCustom['ip']
    jurnal_view = UserCustom['jurnal_view']
    path_report = UserCustom['path_report']
    path_txt = UserCustom['path_txt']

    ###  Создание путей  ###
    pathLog = os.path.join(path, 'log.txt')
    pathGet = os.path.join(path, 'get.txt')
    pathDirReport = os.path.join(path, path_report)
    pathDirTxt = os.path.join(path, path_txt)
    pathJur = os.path.join(path, 'jurnal.txt')


def main(*args):
    """
    Main fuction with run other functions
    succesfully, var_func, list_attr
    """
    succesfully, var_func, list_attr = args[0]
    #list_attr, driver, yearStart, yearEnd, list_attr2, idnomenklature, userIn, passIn
    log_in_attrlist = log_in(succesfully, var_func,
        var_func.ip, var_func.hidden_browser, list_attr)
    #Attributes DRIVER
    driver = log_in_attrlist[1]
    #list_attr, driver, yearStart, yearEnd, list_attr2, idnomenklature, userIn, passIn
    hundred_cart_attrlist = hundred_cart(
        succesfully, var_func, errMessage, log_in_attrlist, var_func.ip, var_func.jurnal_view)
    #list_attr, page, driver, yearStart, yearEnd, list_attr2, idnomenklature, userIn, passIn
    check_element_in_list_attrlist = check_element_in_list(
        succesfully, var_func, errMessage, hundred_cart_attrlist, var_func.ip, var_func.pathDirTxt)
    if len(check_element_in_list_attrlist) == 9:
        #list_attr, driver, linkAddr, idnomenklature, pathIdJur, yearStart, yearEnd, userIn, passIn, page_arch_end
        read_id_archive_attrlist = read_id_archive(
            succesfully, var_func, errMessage, check_element_in_list_attrlist, var_func.ip, var_func.pathDirTxt)
        #GET function
        send_id_cart_nomenklature(succesfully, var_func, errMessage, read_id_archive_attrlist, var_func.ip)
    #Close DRIVER
    driver.quit()


if __name__ == '__main__':
    """
    Run main function Main() with attributes 'list_attr'
    """
    var_func = Variable()
    control_hhtpimport(var_func.path)
    if control_version() is True:
        # Стираем логи
        verify(var_func.pathLog, var_func.pathGet)
        # Читаем список журналов
        list_attr = open(var_func.pathJur).read().splitlines()   
        logger.info(f'Прочитал список из журнала: {list_attr}')
        # Возвращаем сгененированный список
        list_tread = func_list_tread(list_attr, var_func, succesfully)
        try:
            proc = int(var_func.process)
            pool = multiprocessing.Pool(processes=proc)
            pool.map(main, list_tread)
        except Exception as e:
            print(f'Произошла общая ошибка ERR:{e.args}')
            logger.info(
                f'Произошла общая ошибка ERR:{e.args} TRACE:{traceback.format_exc()}')
            pool.terminate()
        finally:
            pool.close()
            pool.join()

        #MOVE finction
        moving_all(var_func.pathDirReport, var_func.pathJur,
                var_func.pathLog, var_func.pathGet, var_func.pathDirTxt)
        print('Я все выполнил!')
    else:
        windll.Kernel32.SetConsoleTextAttribute(
            windll.Kernel32.GetStdHandle(c_ulong(0xfffffff5)), 4)
        print('-' * 50)
        windll.Kernel32.SetConsoleTextAttribute(
            windll.Kernel32.GetStdHandle(c_ulong(0xfffffff5)), 14)
        print('\nВнимание! Обновите версию скрипта и замените все файлы.\n')
        windll.Kernel32.SetConsoleTextAttribute(
            windll.Kernel32.GetStdHandle(c_ulong(0xfffffff5)), 4)
        logger.info('Внимание! Обновите версию скрипта.')

    windll.Kernel32.SetConsoleTextAttribute(
        windll.Kernel32.GetStdHandle(c_ulong(0xfffffff5)), 4)
    print('-' * 50)

    windll.Kernel32.SetConsoleTextAttribute(
        windll.Kernel32.GetStdHandle(c_ulong(0xfffffff5)), 12)
    input('\nНажмите ЕНТЕР на клаве для выхода\n')
