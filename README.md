# Домашнее задание к 5 лекции

В рамках этого ДЗ необходимо реализовать поддержку поиска в приложении для пользователей, которые зарегистрированы.

## Условие


- Добавить  /v1/chats/search, которая в качестве обязательных аргументов принимает в запросе текст фразы, которую надо найти в сообщениях чатов. Поиск должен производиться только по тем чатам, где пользователь добавлен, а не по всем вообще. Ручке необходимо передавать session_id, чтобы она могла определить, о каком пользователе речь.
- Возвращает  отнюдь не результат в виде ссылок на чаты и сообщения, где эта фраза есть, поскольку это может быть достаточно тяжеловесный процесс, а идентификатор таски, статус которой мы будем периодически опрашивать.
- Надо будет добавить /v1/chats/search/status/{task_id}, которая будет позволять получать статус. Возвращать 200 и статус таски, если она есть, и 404, если такой таски вообще не существует. Hеобходимо передавать session_id, поскольку она не должна выдавать результаты запроса одного пользователя другому пользователю.
- Надо будет добавить и третью ручку, /v1/chats/search/{task_id}/messages которая позволяет получать результаты таски, со смещением и лимитом, которые указываются в запросе, наподобие того, как мы ищем сообщения в самом чате. Ручке необходимо передавать session_id, поскольку она не должна выдавать результаты запроса одного пользователя другому пользователю.
- (*) Возможно, стоит выводить сообщения с некоторой долей отклонения, например, по Левенштейну, воспользовавшись такой структурой, как BK-Tree.
- (*) Возможно, стоит сделать фоновый процесс, который будет зачищать отработавшие таски, поскольку иначе база будет пухнуть от информации поиска.
- (*) Также стоит установить таске таймаут, учитывая, что пользователь вряд ли будет ждать дольше 5 секунд, пока мессенджер что-то высветит, после чего таска должна прекратить работу, и вывести то, что уже нашла.

## Чек-лист

- Реализован указанные эндпойнты.
- Полученные фразы в поиске отсортированы по дате, т.е. сначала должны идти самые новые сообщения.
- Приложение возвращает 400 в случае, если указана фраза в тексте не более 3 символов (т.е. по идее фронтенд потом не должен отсылать запросы, если в поле поиска больно короткое слово).

