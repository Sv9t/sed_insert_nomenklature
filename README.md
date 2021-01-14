# Данный скрипт поможет вам массово проставить номенклатуру в документообороте, в документах, находящихся во вкладке «К списанию» и подвкладках «Входящие», «Внутренние», «Исходящие».

Необходимо:
- ПК с windows, версии windows 7 или старше;
- Установленный браузер Firefox ESR, версии не выже 68esr;
- Установленные python (версия не ниже 3.8) и менеджер пакетов pip;
- логин\пароль отдельного пользователя, под которым будем проставлять номенклатуру;
- код карточки номенклатуры, которую необходимо проставить в документах;
- Название(я) журнала(ов), для разграничения вывода документов по конкретному журналу. Это необходимо, если вы хотите для каждого журнала прописать свою отдельную номенклатуру.

Скрипт состоит из двух частей, это каталог "module", который необходимо разместить в репозитории GitLab, и второй, это все остальное (кроме файла "base64_decode_encode.py"), которое необходимо отправить пользователям, а также разместить в репозитории GitLab для проверки версии скрипта.

первая часть:
1.1 Каталог "module" необходимо разместить в репозитории GitLab.

1.2 Скопировать путь до каталога в GitLab формата "gitlab.local/group/python_production/insert_nomeklature/raw/master/module".

1.3 С помощью скрипта "base64_decode_encode.py" необходимо скопированный путь декодировать и вставить в локальный файл "mod_control.py" в переменную "HOST"

Вторая часть:
2.1 В репозитории GitLab разместить отдельно source скрипта, а именно все остальное, исключая каталог "module"

2.2 По аналогии с п. 1.3 выполнить тоже самое для пути до файла "mod_control.py" в каталоге "main" и вставить кодированную ссылку в локальный файл "mod_control.py" в переменную "VERSION_HOST", для проверки версии скрипта у пользователей.

2.3 В локальном файле "mod_control.py" в переменной "VERSION_LOCAL" прописана версия скрипта для пользователей, елси она не будет совпадать с версией, прописанной в файле "mod_control.py" из п. 2.2, то скрипт выдаст уведомление об обновлении.

Установка:
3.1 Запускаем «install_env.bat», автоматически установится виртуальное окружение и необходимые зависимости (для установки окружения необходим интернет). По итогу выполнения скрипта, в вашем каталоге должна появиться папка «env_gitlab». Файлы «install_env.bat» и «requirements.txt» можно удалить, они нам не нужны.

3.2 Настройка "settings.ini":

- "ip = ХХ.XX.ХХ.XХ" - строка, где вместо XX надо надо вписать свой адрес сервера документооборота, где вы хотите проставить номенклатуру (например, ip = 192.168.1.1);
- "jurnal_view = нет" - если стоит нет, журнал при поиске документов учитываться не будет, но журнал в jurnal.txt должен быть обязательно!;
- "path_report = report" - Папка, куда будут складываться ваши отчеты проставления номенклатуры, с указанием даты выполнения; (Не рекомендуется менять)
- "path_txt = txt" - Папка,куда складываются временные txt файлы; (Не рекомендуется менять)
далее настройки для опытных:
- "process = 1" отвечает за количество процессов, выполняющихся одновременно. Один процесс соответствует одному ядру процессора ПК, на котором запускается скрипт. Если у вас строк в «jurnal.txt» 10, а ядер на ПК 4, то для ускорения обработки документов можно запустить одновременно 4 процесса. Как только закончится один из проходов (строк), скрипт приступит к следующему проходу (строке), но всегда будут активны одновременно 4 процесса.
- "hidden_browser = true" - отвечает за показ работы скрипта в браузере, true скрывает браузеры, false показывает. (Рекомендуется оставить true, так как показ браузера это дополнительная нагрузка на ядро процессора)

3.3 Настройка "jurnal.txt":

- "Исходящие" - означает какую вкладку в документообороте открывать скрипту. Может принимать значения: Исходящие, Входящие, Внутренние. ВАЖНО! Прописывать имя вкладки именно с большой буквы, без синтаксических ошибок.
- "Номенклатура 2014-2019 Исходящие" - означает журнал, по которому будет происходить выборка писем. Данный пункт может учитываться или нет (настраивается в settings.ini). Если журнал при поиске документов будет учитываться, то журнал должен называться один в один как журнал в документообороте. Если не будет, можно назвать как хотите для понимания что это за «проход», то есть из названия журнала »Номенклатура 2014-2019 Исходящие» будет понятно, что это проход скрипта за «2014-2019» года во вкладке «Исходящие». Так же название журнала пишется в логах!
- "2014" - год, с которого начинать искать документы скрипт (по умолчанию начинает искать с 01 января)
- "2019" - год, до которого заканчивает искать документы скрипт (по умолчанию до 31 декабря)
- "admin" - логин пользователя, под которым будем проставлять номенклатуру
- "123456" - пароль пользователя
- "12345678" - код карточки номенклатуры, которую надо проставить в документы.

Каждая отдельная строка это один проход скрипта, если вам необходимо проставить номенклатуру сначала в исходящих, потом во входящих, то каждый такой проход необходимо писать в отдельной строке.

4.1 Для запуска скрипта запустите файл "run.bat" (для работы скрипта интернет не нужен). После завершения работы скрипт сформирует папку со всеми необходимыми файлами в папке "report"