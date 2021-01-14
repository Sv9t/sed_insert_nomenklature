import time
import os
from ctypes import c_ulong, windll
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def errMessage(driver):
    """ Ждем сообщение об ошибке 1020 сек. и возвращаем его """

    driver.wait = WebDriverWait(driver, 1020).until(
        EC.presence_of_element_located(
            (By.XPATH, '//table[@class="err_msg"]')))
    time.sleep(1)
    return driver.find_element_by_class_name("err_msg").text


def succesfully(*args):
    """
    Записываем сообщение об успехе или не успехе
    args[0]=fails,args[1]=var_func,args[2]=logger
    """
    with open(args[1].pathGet, 'a') as lines:
        lines.write(f'{args[0]}\n')
    args[2].info(f'Записал что {args[0]}')


def func_list_tread(*args):
    """
    Function return generated list for pool treads
    args[0]=list_attr,args[1]=var_func,args[2]=succesfully
    """
    list_tread = []
    for i in args[0]:
        list_tread.append([args[2], args[1], i])
    return list_tread


def moving_all(pathDirReport, pathJur, pathLog, pathGet, pathDirTxt):
    """ Копируем get.txt, log.txt, jurnal.txt в папку report """
    from shutil import copy2
    from distutils.file_util import move_file

    timeDir = time.strftime("%d.%m.%Y_%H-%M-%S", time.localtime())
    # Создаем полное имя папки
    nameDir = f'Проставление_номенклатуры_{timeDir}'
    pathMakeDir = os.path.join(pathDirReport, nameDir)
    os.mkdir(pathMakeDir)
    for i in [pathJur, pathLog, pathGet]:
        copy2(i, pathMakeDir)   # Копируем во вновь созданную папку
    for file_txt in os.listdir(pathDirTxt):    # Проходим по папке txt
        # Создаем абсолютные пути для каждого файла
        path_file_txt = os.path.join(pathDirTxt, file_txt)
        # Перекидываем файлы txt с ошибками в новую папку
        move_file(path_file_txt, pathMakeDir)
    windll.Kernel32.SetConsoleTextAttribute(
        windll.Kernel32.GetStdHandle(c_ulong(0xfffffff5)), 2)
    print(f'\nСкопировал все *.txt в {nameDir}')
