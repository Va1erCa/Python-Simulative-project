# ETL-пайплайн для обучающей платформы
**by Va1erCa [Va1errCa] (Жидков Валерий)**

Задача построения подсистемы сбора/обработки/размещение на локальном Postgres-сервере информации об учебном процессе студентов он-лайн университета.

## Модули/файлы проекта: ##
* `data_processor.py` - основной модуль приложения
* `get_data.py` - получение данных с сетевого ресурса по api
* `put_data.py` - сохранение данных в БД Postgres (на локальный сервер)
* `google_sheets.py` - подготовка отчета со статистикой обучения в Google-таблице 
* `email_notifications.py` - рассылка почтовых уведомлений по протоколу SMTP
* `logger.py` - работа с инфраструктурой логирования и собственный класс-регистратор
* `exceptions.py` - собственные исключения приложения
* `app_types.py` - общие типы приложения
* `config.py` - константы / настройки  
* `requirements.txt` - перечень требуемых библиотек
* `.env` - файл с переменными окружения ( \<client> , \<client_key> )

  
### requirements.txt ###
* cформирован с помощью команды:
    * ```pipreqs --force``` (утилита ```pipreqs``` устанавливается командой ```pip install pipreqs```)
* развертывание библиотек командой:
    * ```pip install -r requirements.txt ```

## Описание ##
Приложение реализует механизм получения данных с помощью API сетевого ресурса (itresume.ru), обработку и размещение в локальную базу данных (Postgres). 
После успешного пополнения базы, расчитываются некоторые стат.показатели учебного процесса за обработанную дату, отчет формируется в эл.таблице Google Sheets.
После чего, производится рассылка почтовых уведомлений всем заинтересованным лицам. Указанные операции сопровождаются логированием. 

В начале работы приложение запрашивает у пользователя дату, за которую будет производится обработка.
Далее обработка осуществляется автоматически и состоит из этапов:
0. Подготовка инфраструктуры логирования, проверка папки хранения логов на допустимое заполнение, очистка в случае необходимости, создание экземпляра собственного регистратора(логера);  
1. Опрос сетевого ресурса по api, сбор данных за выбранную дату, входной контроль идентификации пользователя;
2. Инициализация соединения с базой данных на лкальном сервере, подготовка таблицы в случае необходимости;
3. Запись данных в базу, с контролем полноты заполнения полей;
4. Подготовка отчета в эл.таблице Google Sheets для заинтересованных лиц;  
5. Оповещение заинтересованных лиц о произведенной обработке по эл.почте
   
Все этапы логируются. 

Для успешной работы приложения должен быть развернут PostgreSQL-сервер на локальной машине. В котором необходимо завести базу с именем и параметрами указанными в константе `SERVER_CONNECTION_PARAMS` файла `config.py`.

В процессе чтения осуществляется входной контроль данных: к записи в базу не допускаются строки где идентификатор пользователя либо не задан либо не содержит ровно 32 символа (котрольная длина идентификатора указана в константе `LENGTH_OF_USER_ID_FIELD` в `cobfig.py`).  

Создание таблицы в БД для сохранения результатов обработки производится автоматически. Необходимость полной очистки таблицы в начале очередного сеанса работы приложения задается константой `DB_MAIN_TABLE_OPEN_RESET = True`. При записи данных в таблицу БД производится контроль заполнения полей.     

В модуле `config.py` сохранены некоторые настройки приложения. Например, флаг тестового режима `TEST_APP_MODE` (если он равен `True`, обрабатываются данные только за первый час выбранной пользователем даты), флаг глубины хранения логов (по умолчанию - 3 файла), путь к папке хранения логов (по умолчанию - `.logs`) и т.д. 

В приложении присутствует языковая поддержка, т.е. возможность представить взаимодействие с пользователем и логирование на русском (`CURR_LANG = RUSSIAN`) либо на английском (`CURR_LANG = ENGLISH`) языках (константа находится в `config.py`).
