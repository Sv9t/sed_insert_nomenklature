import logging
import traceback
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


def check_list_attr(list_attr2, logger):
    """ Проверяем первую переменнуюи присваеваем ей часть ссылки """

    if list_attr2 == 'Входящие':
        list_attr2 = "income-ready-for-delo"
        return list_attr2
    elif list_attr2 == 'Исходящие':
        list_attr2 = "outcome-ready-for-delo"
        return list_attr2
    elif list_attr2 == 'Внутренние':
        list_attr2 = "internal-ready-for_delo"
        return list_attr2
    else:
        print(f'Ошибка в синтаксисе в переменной: {list_attr2}. Проверь!')
        logger.error(
            f'Ошибка в синтаксисе в переменной: {list_attr2}. Проверь!')
        raise ValueError


def hundred_cart(succesfully, var_func, errMessage, *args):
    """
    Открываем страницу К списанию Входящие
    args[0]=log_in_attrlist,args[1]=ip,args[2]=jurnal_view
    """

    logger = logging.getLogger()
    list_attr, driver, yearStart, yearEnd, list_attr2, idnomenklature, userIn, passIn = args[0]
    try:
        # Проверяем первую переменную
        list_attr2 = check_list_attr(list_attr2, logger)

        driver.get(
            f'http://{args[1]}:8080/portal/auth/portal/dbmi/delo/{list_attr2}')
        driver.wait = WebDriverWait(driver, 1020).until(
            EC.presence_of_element_located((By.ID, "BODY_BLOCK_SearchBlockDescription")))  # Ждем 17мин на появление формы поиска attr_43524541544544_choiceDatePeriod
        ## Ставим период дат
        print(f'[{list_attr}]: Ставим период дат')
        logger.info(
            f'[{list_attr}]: Ставим период дат')
        driver.find_element_by_id(
            "attr_43524541544544_choiceDatePeriod").click()
        ## Ставим Дата регистрации
        print(f'[{list_attr}]: Ставим Дата регистрации')
        logger.info(
            f'[{list_attr}]: Ставим Дата регистрации')
        fromDate = '01.01.{}'.format(yearStart)
        toDate = '31.12.{}'.format(yearEnd)
        driver.find_element_by_xpath(
            '//input[@id="attr_4a42525f524547445f44415445524547_fromDate"]'
        ).send_keys(fromDate)

        driver.find_element_by_xpath(
            '//input[@id="attr_4a42525f524547445f44415445524547_toDate"]'
        ).send_keys(toDate)
        ## Ставим журнал регистраци
        if args[2].lower() == 'да':
            print(f'[{list_attr}]: Ставим журнал регистрации')
            logger.info(
                f'[{list_attr}]:Ставим журнал регистрации')
            driver.find_element_by_xpath(
                '//input[@id="attr_4a42525f524547445f5245474a4f55524e_select"]'
            ).send_keys(list_attr)
            driver.wait = WebDriverWait(driver, 1020).until(
                EC.presence_of_element_located(
                    (By.ID, "attr_4a42525f524547445f5245474a4f55524e_select_popup")))  # Ждем 17мин на появление
            driver.find_element_by_id(
                "attr_4a42525f524547445f5245474a4f55524e_select_popup0").click()
        ## Нажимаем поиск portlet-content-center
        driver.find_element_by_xpath(
            '//span[@id="dijit_form_Button_0_label"]').click()
        driver.wait = WebDriverWait(driver, 1020).until(
            EC.element_to_be_clickable(
                (By.CLASS_NAME, "portlet-content-center")))
    except ValueError:
        print('Ошибка в синтаксисе первой переменной ERR:ValueError')
        logger.info('Ошибка в синтаксисе первой переменной ERR: ValueError')
        print(f'[{list_attr}]: Перехожу к следующему журналу')
        logger.info(f'[{list_attr}]: Перехожу к следующему журналу')
        fails = f'Неуспешно, Ошибка в первой переменной ERR:ValueError. {list_attr} Года: {yearStart}-{yearEnd}'
        succesfully(fails, var_func, logger)  # Пишем в get.txt о неуспехе
    except TimeoutException as e:
        print(
            f'[{list_attr}]: Ошибка в hundred_cart():TimeoutException Не дождался страницу ERR: {e.args}')
        logger.error(
            f'[{list_attr}]: Ошибка в hundred_cart():TimeoutException Не дождался страницу ERR:{e.args} TRACE:{traceback.format_exc()}')

        fails = f'Неуспешно, {list_attr} hundred_cart() TimeoutException Не дождался страницу '
        succesfully(fails, var_func, logger)  # Пишем в get.txt о неуспехе
    except Exception as e:
        print(
            f'[{list_attr}]: Ошибка в hundred_cart() Общая ошибка ERR:{e.args}')
        logger.error(
            f'[{list_attr}]: Ошибка в hundred_cart() Общая ошибка ERR:{e.args} TRACE:{traceback.format_exc()}')
        errMsg = errMessage(driver)
        print(f'[{list_attr}]: {errMsg}')

        fails = f'Неуспешно, {list_attr} hundred_cart() ERR: {errMsg}'
        succesfully(fails, var_func, logger)  # Пишем в get.txt о неуспехе
    else:
        hundred_cart = [list_attr, driver, yearStart, yearEnd,
                        list_attr2, idnomenklature, userIn, passIn]
        return hundred_cart
    finally:
        pass
