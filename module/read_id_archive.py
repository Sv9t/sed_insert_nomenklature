import os
import time
import logging
import traceback
from ctypes import c_ulong, windll
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def read_id_archive(succesfully, var_func, errMessage, *args):
    """
    Переходим непосредственно к чтению ID карточек
    list_attr, page, driver, linkAddr, yearStart, yearEnd, idnomenklature, userIn, passIn
    args[1]=ip
    args[2]=pathDirTxt
    """

    logger = logging.getLogger()
    list_attr, page, driver, yearStart, yearEnd, linkAddr, idnomenklature, userIn, passIn = args[0]
    try:
        # print(pathDirTxt)
        ## Проверяем переменную linkAddr, если она "outcome-ready-for-delo"
        ## то это Исходящие и значит, что проходов listTrCount = 6
        if linkAddr == "outcome-ready-for-delo":
            listIterTrCount = 6
        else:
            listIterTrCount = 7

        pageExit = 0  # Переменная для выхода из цикла, 0 - продолжаем, 1 - выход
        timeTxt = time.strftime("%d.%m.%Y_%H-%M-%S", time.localtime())
        pathIdJur = os.path.join(
            args[2], f'{list_attr}_{idnomenklature}_{yearStart}-{yearEnd}_{timeTxt}.txt')
        # print(pathIdJur)
        with open(pathIdJur, 'w'):
            pass
        print(f'[{list_attr}]: Cоздал TXT: {pathIdJur}')
        logger.error(f'[{list_attr}]: Cоздал TXT: {pathIdJur}')
        # time.sleep(5)
        for page_arch in page:
            # print(f'page_arch: {page_arch}')

            if page_arch == 1:   # Если первая страница
                pass
            else:
                ## Переходим на следующую страницу
                print(
                    f'[{list_attr}]: Переходим на следующую страницу - {page_arch}')
                logger.info(
                    f'[{list_attr}]: Переходим на следующую страницу - {page_arch}')
                driver.get(
                    f'http://{args[1]}:8080/portal/auth/portal/dbmi/delo/{linkAddr}/CardListWindow?MI_INTERNAL_REQUEST_FLAG_FIELD=true&action=e&page={page_arch}')
                driver.wait = WebDriverWait(driver, 1020).until(
                    EC.element_to_be_clickable(
                        (By.CLASS_NAME, "portlet-content-center")))  # Ждем 17мин на появление формы страницы
            # time.sleep(5)
            print(f'[{list_attr}]: Читаю id карточек')
            logger.info(f'[{list_attr}]: Читаю id карточек')
            tableId = driver.find_elements_by_xpath(
                '//table[contains(@id, "dataItem")]/tbody/tr')
            # for t in tableId:
            #     print(f'tableId: {t.text}')
            tableTrTd = driver.find_elements_by_xpath(
                '//table[contains(@id, "dataItem")]/tbody/tr/td')
            # for t in tableTrTd:
            #     print(f'tableTrTd: {t.text}')
            ## Содаем список listTr c id карточек на странице
            listTr = []
            listTrCount = 0
            for tr in tableTrTd:
                # print(f'listTrCount: {listTrCount}, tr: {tr.text}')
                # Когда счетчик равен 7 (или 6), то проход уже идет 8 раз (или 7)
                if listTrCount == listIterTrCount:
                    # Если 8 (или 7) столбец пустой, без номенклатуры
                    if tr.text == '':
                        pass
                    else:
                        listTr.append(tr.text)   # Если столбец с номенклатурой
                    listTrCount = 0
                else:
                    # Счетчик 8 (или 7) столбца карточки в поиске
                    listTrCount += 1
            # print(f'listTr: {listTr}')
            ## Считаем сколько надо id вычесть со страницы
            ## Записываем полученные id в TXT
            listIdCart = []
            with open(pathIdJur, 'a') as lineid:
                for ii in tableId:
                    listIdCart.append(ii.get_attribute('id'))
                ## Если есть карточки с уже заполненной номенклатурой
                ## то удаляем с конца кол-во id с номенклатурой len(listTr)
                if 20 > len(listTr) > 0:
                    windll.Kernel32.SetConsoleTextAttribute(
                        windll.Kernel32.GetStdHandle(c_ulong(0xfffffff5)), 6)
                    print(
                        f'[{list_attr}]: Карточек с номенклатурой еще {len(listTr)}')
                    windll.Kernel32.SetConsoleTextAttribute(
                        windll.Kernel32.GetStdHandle(c_ulong(0xfffffff5)), 15)
                    logger.info(
                        f'[{list_attr}]: Карточек с номенклатурой еще {len(listTr)}')
                    listIdCart = listIdCart[:-(len(listTr))]
                    # Присваеваем переменной pageExit 1, означающей,
                    # что дальше карточки только с номенклатурой, можно выходить
                    # из цикла for page_arch in page
                    pageExit = 1
                    # Присваевам переменную page_arch_end самой последней странице
                    page_arch_end = page_arch
                elif len(listTr) == 20:
                    windll.Kernel32.SetConsoleTextAttribute(
                        windll.Kernel32.GetStdHandle(c_ulong(0xfffffff5)), 6)
                    print(
                        f'[{list_attr}]: Карточек с номенклатурой уже {len(listTr)}')
                    windll.Kernel32.SetConsoleTextAttribute(
                        windll.Kernel32.GetStdHandle(c_ulong(0xfffffff5)), 15)
                    logger.info(
                        f'[{list_attr}]: Карточек с номенклатурой уже {len(listTr)}')
                    # Присваевам переменную page_arch_end самой последней странице
                    page_arch_end = page_arch
                    # Запиывать ID этой страницы не нужно, выходим
                    break
                else:
                    print(
                        f'[{list_attr}]: Карточек с номенклатурой {len(listTr)}')
                    logger.info(
                        f'[{list_attr}]: Карточек с номенклатурой {len(listTr)}')
                    listIdCart = listIdCart[:]
                ## Создаем из списка строку с нижним подчеркиванием
                listIdCart = '_'.join(listIdCart)
                ## Пишем эту строку и ставим перенос строки
                lineid.write(f'{listIdCart}\n')

            print(
                f'[{list_attr}]: Записал ID страницы - {page_arch}')
            logger.info(
                f'[{list_attr}]: Записал ID страницы - {page_arch}')
            logger.info(
                f'[{list_attr}]: Сформированная строка с ID страниц - {listIdCart}')
            # print(f'pageExit: {pageExit}')
            if pageExit == 1:
                break   # Выйти из цикла for, тк след.страница уже с индексом номенклатуры
            else:
                pass
    except Exception as e:
        print(f'[{list_attr}]: Ошибка в read_id_archive() Общая ошибка ERR:{e.args}')
        logger.error(
            f'[{list_attr}]: Ошибка в read_id_archive() Общая ошибка ERR:{e.args} TRACE: {traceback.format_exc()}')
        errMsg = errMessage(driver)
        print(f'[{list_attr}]: {errMsg}')

        fails = f'Неуспешно, {list_attr} read_id_archive() ERR: {errMsg}'
        succesfully(fails, var_func, logger)  # Пишем в get.txt о неуспехе
    else:
        send_id_cart_nomenklature = [list_attr, driver, linkAddr, idnomenklature, pathIdJur, yearStart, yearEnd, userIn, passIn, page_arch_end]
        return send_id_cart_nomenklature
