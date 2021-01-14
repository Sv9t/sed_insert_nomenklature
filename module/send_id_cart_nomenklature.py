import requests
import logging
import traceback
import time
from ctypes import c_ulong, windll


def send_id_cart_nomenklature(succesfully, var_func, errMessage, *args):
    """
    Отправляем ID страниц на проставление номенклатур
    list_attr, driver, linkAddr, idnomenklature, pathIdJur, yearStart, yearEnd, userIn, passIn, page_arch_end
    args[1]=ip
    """
    logger = logging.getLogger()
    list_attr, driver, linkAddr, idnomenklature, pathIdJur, yearStart, yearEnd, userIn, passIn, page_arch_end = args[0]
    try:
        ## Подключаем сессию и формируем запрос
        s = requests.Session()
        data = {'username': userIn,
                'password': passIn,
                'do': 'login'}

        url = f'http://{args[1]}:8080/portal/login'
        # Регистрируемся и получаем статус аутентификации
        r = s.post(url, data=data, stream=True, timeout=5.05)
        windll.Kernel32.SetConsoleTextAttribute(
            windll.Kernel32.GetStdHandle(c_ulong(0xfffffff5)), 2)
        print(f'Статус аутентификации: {r.status_code}')
        windll.Kernel32.SetConsoleTextAttribute(
            windll.Kernel32.GetStdHandle(c_ulong(0xfffffff5)), 15)
        ## Читаем наш созданный txt
        with open(pathIdJur) as e:
            # считаем постранично начиная со страницы 1
            for string in enumerate(e, start=1):
                stringListIdCart = string[1].rstrip('\n')
                print(
                    f'[{list_attr}]: Отправляем ID {stringListIdCart} на проставление номенклатуры "{idnomenklature}" Страница: {string[0]} из {page_arch_end}')
                logger.info(
                    f'[{list_attr}]: Отправляем ID {stringListIdCart} на проставление номенклатуры "{idnomenklature}" Страница: {string[0]} из {page_arch_end}')
                ## Отправляем с помощью get-запроса и сохранением cookies запросы
                send_get = f'http://{args[1]}:8080/portal/auth/portal/dbmi/delo/{linkAddr}/CardListWindow?action=1&MI_ACTION_FIELD=MI_GROUP_INDEX_ACTION&INDEX={idnomenklature}&DOCS_GROUP={stringListIdCart}'
                response = s.get(send_get, stream=True, timeout=5.05)
                windll.Kernel32.SetConsoleTextAttribute(
                    windll.Kernel32.GetStdHandle(c_ulong(0xfffffff5)), 14)
                print(f'Статус ответа GET: {response.status_code}')
                windll.Kernel32.SetConsoleTextAttribute(
                    windll.Kernel32.GetStdHandle(c_ulong(0xfffffff5)), 15)
                time.sleep(5)
    except Exception as e:
        print(f'[{list_attr}]: Ошибка в send_id_cart_nomenklature() ERR:{e.args}')
        logger.error(
            f'[{list_attr}]: Ошибка в send_id_cart_nomenklature() ERR:{e.args} TRACE:{traceback.format_exc()}')
        errMsg = errMessage(driver)
        print(f'[{list_attr}]: {errMsg}')

        fails = f'Неуспешно, {list_attr} send_id_cart_nomenklature() ERR: {errMsg}'
        succesfully(fails, var_func, logger)  # Пишем в get.txt о неуспехе
    else:
        print(f'[{list_attr}]: Перехожу к следующему журналу')
        logger.info(f'[{list_attr}]: Перехожу к следующему журналу')
        succes = f'Успешно, {list_attr} Код номенклатуры:{idnomenklature} Года: {yearStart}-{yearEnd}'
        # ЗАписываем в get.txt что успешно
        succesfully(succes, var_func, logger)
