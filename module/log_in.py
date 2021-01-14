from ctypes import c_ulong, windll
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementNotVisibleException, TimeoutException
import logging
import traceback


def log_in(succesfully, var_func, *args):
    """
    Пытаемся залогиниться
    args[2]=list_attr, args[0]=ip, args[1]=hidden_browser
    """
    logger = logging.getLogger()

    a = args[2].split(';')   # Делим строку по разделителю ';'
    list_attr2 = a[0]   # переменная вкладки Входящие, Исходящие, Внутренние
    list_attr = a[1]  # переменная журнала
    yearStart = a[2]   # переменная начала года
    yearEnd = a[3]   # переменная конца года
    userIn = a[4]   # переменная логин
    passIn = a[5]   # переменная пароль
    idnomenklature = a[6]   # id карточки номенклатуры

    windll.Kernel32.SetConsoleTextAttribute(
        windll.Kernel32.GetStdHandle(c_ulong(0xfffffff5)), 3)
    print(f'\n{"*"*70}\nБеру журнал: {list_attr} {yearStart}-{yearEnd}\n{"*"*70}')
    windll.Kernel32.SetConsoleTextAttribute(
        windll.Kernel32.GetStdHandle(c_ulong(0xfffffff5)), 15)
    logger.info(
        f'\n{"*"*70}\nБеру журнал: {list_attr} {yearStart}-{yearEnd}\n{"*"*70}')

    try:
        url_to = f'http://{args[0]}:8080/portal/login'
        print(f'[{list_attr}]: Открываю страницу {url_to}')

        profile = Options()
        if args[1] == 'true':
            profile.headless = True 
        else:
            profile.headless = False
        
        driver = Firefox(options=profile, executable_path='geckodriver.exe')  # Присваеваем переменную driver для запуска браузера
        driver.wait = WebDriverWait(driver, 30)

        driver.get(url_to)  # Открываем страницу входа в СЭД
        driver.wait = WebDriverWait(driver, 1020).until(
            EC.presence_of_element_located((By.NAME, "MILoginForm")))  # Ждем 17мин на появление формы входа
        driver.find_element_by_name("username").send_keys(userIn)  # Вводим логин
        driver.find_element_by_name("password").send_keys(passIn)  # Вводим пароль
        driver.find_element_by_class_name("loginbutton").click()  # Жмем кнопку войти

        ### WAIT LOGIN ###
        driver.wait = WebDriverWait(driver, 1020).until(EC.presence_of_element_located(
            (By.ID, "sizer")))   # Ждем 17мин до загрузки страницы СЭДа
        print(f'[{list_attr}]: Залогинился')
        logger.info(f'[{list_attr}]: Залогинился')
    except ElementNotVisibleException as e:
        print(f'[{list_attr}]:Ошибка в log_in:ElementNotVisibleException Не дождался формы ERR:{e.args}')
        logger.error(
            f'[{list_attr}]: Ошибка в log_in:ElementNotVisibleException Не дождался формы ERR:{e.args} TRACE:{traceback.format_exc()}')
        fails = f'Неуспешно, {list_attr} Ошибка в log_in:ElementNotVisibleException Не дождался формы ERR:{e.args}'
        succesfully(fails, var_func, logger)  # Пишем в get.txt о неуспехе
    except TimeoutException as e:
        print(
            f'[{list_attr}]: Ошибка в log_in:TimeoutException Не дождался страницу ERR: {e.args}')
        logger.error(
            f'[{list_attr}]: Ошибка в log_in:TimeoutException Не дождался страницу ERR:{e.args} TRACE:{traceback.format_exc()}')

        fails = f'Неуспешно, {list_attr} log_in:TimeoutException Не дождался страницу '
        succesfully(fails, var_func, logger)  # Пишем в get.txt о неуспехе
    except Exception as e:
        print(f'[{list_attr}]: Общая ошибка в log_in() ERR:{e.args}')
        logger.error(
            f'[{list_attr}]: Общая ошибка в log_in() ERR:{e.args} TRACE:{traceback.format_exc()}')
        fails = f'Неуспешно, {list_attr} Общая ошибка в log_in() ERR: {e.args}'
        succesfully(fails, var_func, logger)  # Пишем в get.txt о неуспехе
    else:
        log_in_attrlist = [list_attr, driver, yearStart, yearEnd, list_attr2, idnomenklature, userIn, passIn]
        return log_in_attrlist
    # finally:
    #     driver.quit()
