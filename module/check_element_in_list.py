import logging
import re
import time
import traceback
from ctypes import c_ulong, windll
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC


def check_element_in_list(succesfully, var_func, errMessage, *args):
    """ 
    Проверяем пустой ли выведен список или нет
    list_attr, driver, yearStart, yearEnd, list_attr2, idnomenklature, userIn, passIn
    """

    logger = logging.getLogger()
    list_attr, driver, yearStart, yearEnd, list_attr2, idnomenklature, userIn, passIn = args[0]
    try:
        ## ЧИТАЕМ ТЕКСТ НАЙДЕНЫ ЛИ ДОКУМЕНТЫ
        textSearch = driver.find_elements_by_xpath(
            '//div[@class="icHeader"]')
        listTextSearch = []
        for i in textSearch:
            # print('i', i.text)
            listTextSearch.append(i.text)
        if len(listTextSearch) == 2:
            textSearchStr = ''.join(listTextSearch[1])
            # print('textSearch', textSearchStr)
            ## Если кол-во букв больше 0 и элемент показан
            windll.Kernel32.SetConsoleTextAttribute(
                windll.Kernel32.GetStdHandle(c_ulong(0xfffffff5)), 6)
            print(f'[{list_attr}]: {textSearchStr}')
            windll.Kernel32.SetConsoleTextAttribute(
                windll.Kernel32.GetStdHandle(c_ulong(0xfffffff5)), 15)
            logger.info(f'[{list_attr}]: {textSearchStr}')

            print(f'[{list_attr}]: Перехожу к следующему журналу')
            logger.info(f'[{list_attr}]: Перехожу к следующему журналу')
            
            succes = f'Успешно, {textSearchStr} - {list_attr} Года: {yearStart}-{yearEnd}'
            # Записываем в get.txt что успешно
            succesfully(succes, var_func, logger)
            return ['Next']
        else:
            ## Нажимаем на Индекс номенклатуры
            print(f'[{list_attr}]: Нажимаем на Индекс номенклатуры')
            logger.info(
                f'[{list_attr}]: Нажимаем на Индекс номенклатуры')
            driver.find_element_by_link_text("Индекс номенклатуры").click()
            driver.wait = WebDriverWait(driver, 1020).until(
                EC.element_to_be_clickable(
                    (By.CLASS_NAME, "portlet-content-center")))
            # time.sleep(5)
            ## Нажимаем на Индекс номенклатуры 2
            print(f'[{list_attr}]: Нажимаем на Индекс номенклатуры 2')
            logger.info(
                f'[{list_attr}]: Нажимаем на Индекс номенклатуры 2')
            driver.find_element_by_link_text("Индекс номенклатуры").click()
            driver.wait = WebDriverWait(driver, 1020).until(
                EC.element_to_be_clickable(
                    (By.CLASS_NAME, "portlet-content-center")))
            # time.sleep(5)
            # Считаем кол-во страниц pagebanner
            pagebanner = driver.find_element_by_xpath(
                '//div[@class="pagebanner"]').text
            countDoc = re.findall('\d+', pagebanner)
            print(countDoc)
            if countDoc[0] == '1000':   # ['1000', '1', '20']
                driver.find_element_by_xpath(
                    '//span[@class="resDocCounter"]').click()   # Нажимаем на 1000+
                time.sleep(5)
                pagebanner = driver.find_element_by_xpath(
                    '//div[@class="pagebanner"]').text
                countDoc = re.findall('\d+', pagebanner)   # берем только числа
                print(countDoc[0])

                # Высчитываем, если при делении на 20стр не остается остатка, то просто делим
                # если есть остаток то прибавляем 1 страницу
                if int(countDoc[0]) % 20 == 0:
                    c = int(countDoc[0]) // 20
                else:
                    c = int(countDoc[0]) // 20 + 1

                print(c)
                page = []
                for i in range(1, c + 1):
                    page.append(i)
                # Список страниц с шагом 1
                windll.Kernel32.SetConsoleTextAttribute(
                    windll.Kernel32.GetStdHandle(c_ulong(0xfffffff5)), 6)
                print(f'[{list_attr}]: Всего страниц: {page[-1]}')
                logger.info(f'[{list_attr}]: Всего страниц: {page[-1]}')
                windll.Kernel32.SetConsoleTextAttribute(
                    windll.Kernel32.GetStdHandle(c_ulong(0xfffffff5)), 15)

            else:
                print('ne 1000')
                # Высчитываем, если при делении на 20стр не остается остатка, то просто делим
                # если есть остаток то прибавляем 1 страницу
                if int(countDoc[0]) % 20 == 0:
                    c = int(countDoc[0]) // 20
                else:
                    c = int(countDoc[0]) // 20 + 1

                print(c)
                if c == 1:   # Если меньше 20 карточек значит 1 страница
                    page = [1]
                else:
                    page = []
                    for i in range(1, c + 1):
                        page.append(i)
                print(f'[{list_attr}]: Всего страниц: {page[-1]}')
                logger.info(f'[{list_attr}]: Всего страниц: {page[-1]}')

            ## Вывел список для списания
            print(f'[{list_attr}]: Вывел список для чтения')
            logger.info(f'[{list_attr}]: Вывел список для чтения')
            time.sleep(1)

            read_id_archive = [
                list_attr, page, driver, yearStart, yearEnd, list_attr2, idnomenklature, userIn, passIn]
            return read_id_archive
    except TimeoutException as e:
        print(
            f'[{list_attr}]: Ошибка в check_element_in_list():TimeoutException Не дождался страницу ERR: {e.args}')
        logger.error(
            f'[{list_attr}]: Ошибка в check_element_in_list():TimeoutException Не дождался страницу ERR:{e.args} TRACE:{traceback.format_exc()}')

        fails = f'Неуспешно, {list_attr} check_element_in_list() TimeoutException Не дождался страницу '
        succesfully(fails, var_func, logger)  # Пишем в get.txt о неуспехе
    except Exception as e:
        print(
            f'[{list_attr}]: Ошибка в check_element_in_list() Общая ошибка ERR:{e.args}')
        logger.error(
            f'[{list_attr}]: Ошибка в check_element_in_list() Общая ошибка ERR:{e.args} TRACE:{traceback.format_exc()}')
        errMsg = errMessage(driver)
        print(f'[{list_attr}]: {errMsg}')

        fails = f'Неуспешно, {list_attr} check_element_in_list() ERR: {errMsg}'
        succesfully(fails, var_func, logger)  # Пишем в get.txt о неуспехе
    finally:
        pass
