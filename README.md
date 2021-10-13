# Домашнее задание к 5 лекции

**Дедлайн: 18 октября, понедельник, 23:59**

_Это домашнее задание предполагает **кросс-проверку**: каждый студент будет проверять работы двух других студентов. По возможности менторы тоже могут дать свои комментарии к домашкам.
Вам на почту пришли инвайты в репозитории для 5-го домашнего задания, ссылку на репу нужно положить в оба тикета, авторами которых вы являетесь, подробнее в памятке тут. Обязательно выдайте доступ проверяющим._

## Условие


- Добавить ручку /v1/chats/search, которая в качестве обязательных аргументов принимает в запросе user_id и текст фразы, которую надо найти в сообщениях чатов. Поиск должен производиться только по тем чатам, где пользователь добавлен, а не по всем вообще.
- Возвращает ручка отнюдь не результат в виде ссылок на чаты и сообщения, где эта фраза есть, поскольку это может быть достаточно тяжеловесный процесс, а идентификатор таски, статус которой мы будем периодически опрашивать.
- Надо будет добавить вторую ручку /v1/chats/search/status/{task_id}, которая будет позволять получать статус. Возвращать 200 и статус таски, если она есть, и 404, если такой таски вообще не существует.
- Надо будет добавить и третью ручку, /v1/chats/search/{task_id}/messages которая позволяет получать результаты таски, со смещением и лимитом, которые указываются в запросе, наподобие того, как мы ищем сообщения в самом чате.
- (*) Возможно, стоит выводить сообщения с некоторой долей отклонения, например, по Левенштейну, воспользовавшись такой структурой, как BK-Tree.
- (*) Возможно, стоит сделать фоновый процесс, который будет зачищать отработавшие таски, поскольку иначе база будет пухнуть от информации поиска.
- (*) Также стоит установить таске таймаут, учитывая, что пользователь вряд ли будет ждать дольше 5 секунд, пока мессенджер что-то высветит, после чего таска должна прекратить работу, и вывести то, что уже нашла.

Описанные ручки представлены ниже в формате OpenAPI:

```yaml
openapi: "3.0.0"
info:
  version: 1.0.0
  title: Gentlemen Messenger API
servers:
  - url: http://localhost
paths:
  /v1/chats/search:
    post:
      description: "Запустить процесс поиска по истории сообщений для чатов, в которых есть данный пользователь"
      parameters:
        - in: query
          required: true
          name: user_id
          schema:
            type: string
          description: "Идентификатор пользователя"
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: "object"
              properties:
                message:
                  type: string
                  description: "текст сообщения, который надо найти в истории"
                  example: "Hello"
      responses:
        '201':
          $ref: '#/components/responses/GetHistoryResponse'
        '400':
          description: |
            * `bad-parameters` - неправильный формат входных параметров
        '404':
          description: |            
            * `user-not-found` - данный пользователь не найден
          
        default:
          $ref: '#/components/responses/DefaultErrorResponse'

  /v1/chats/search/status/{task_id}:
    get:
      description: "Получить статус таски на обработку"
      parameters:
        - in: path
          required: true
          name: task_id
          schema:
            type: string
      responses:
        '200':
          $ref:  "#/components/responses/GetTaskResponse"
        '400':
          description: |
            * `bad-parameters` - неправильный формат входных параметров
        '404':
          description: |            
            * `task-not-found` - задача на обработку не найдена
        default:
          $ref: '#/components/responses/DefaultErrorResponse'
   
  /v1/chats/search/{task_id}/messages:
    get:
      description: "получить список сообщений из чатов"
      parameters:
        - in: path
          required: true
          name: task_id
          schema:
            type: string
          example: "the-task-id"
        - in: query
          required: true
          name: limit
          schema:
            type: integer
            minimum: 1
            maximum: 1000
          description: "не больше стольки сообщений хотим получить в ответе"
          example: 10
        - in: query
          name: from
          schema:
            $ref: '#/components/schemas/Cursor'
          description: "указатель для сервера, обозначающий место, с которого стоит продолжить получение сообщений; если не указан, то сервер должен вернуть limit сообщений, начиная с самого последнего сообщения в истории"
      responses:
        '200':
          $ref: '#/components/responses/HistoryGetMessagesResponse'
        '400':
          description: |
            * `bad-parameters` - неправильный формат входных параметров
        '404':
          description: |
            * `task-not-found` - указанная задача не существует
        default:
          $ref: '#/components/responses/DefaultErrorResponse'

components:
  responses:
    DefaultErrorResponse:
      description: 'unexpected server error'
      content:
        application/json:
          schema:
            required:
              - message
            properties:
              message:
                type: string
                description: "error reason"

    GetHistoryResponse:
      description: "Задача создана успешно"
      content:
        application/json:
          schema:
            required:
              - task_id
            properties:
              task_id:
                type: string
                description: "Идентификатор созданной задачи"

    GetTaskResponse:
      description: "Получить статус задачи"
      content:
        application/json:
          schema:
            required:
              - status
            properties:
              status:
                type: string
                description: "Статус задачи. Может принимать значения SUCCESS|IN_PROCESS|WAITING|FAILED"

    HistoryGetMessagesResponse:
      description: 'action was completed successfully'
      content:
        application/json:
          schema:
            required:
              - messages
            properties:
              messages:
                type: array
                items:
                  $ref: '#/components/schemas/HistoryMessage'
              next:
                $ref: '#/components/schemas/Cursor'

  schemas:
    HistoryMessage:
      properties:
        text:
          type: string
        chat_id:
          type: string

    Cursor:
      required:
        - iterator
      properties:
        iterator:
          type: string
```

## Чек-лист

- Реализован указанные эндпойнты.
- Полученные фразы в поиске отсортированы по дате, т.е. сначала должны идти самые новые сообщения.
- Поставлена отсечка, по итогам таска должна хранить не более 100 сообщений.
- Приложение возвращает 400 в случае, если указана фраза в тексте не более 3 символов (т.е. по идее фронтенд потом не должен отсылать запросы, если в поле поиска больно короткое слово).
- (*) Через 5 минут после завершения таска и ее данные удаляются фоновым процессом.
- (*) Фразы с отклонением в 2-3 символа также находятся в истории сообщений.
