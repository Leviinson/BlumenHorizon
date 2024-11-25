# Настройка БД

## Установить базе данных кодировку для поддержки эмодзи

`ALTER DATABASE blumenhorizon CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;`

## По-надобности сделать это для каждой таблицы

`ALTER TABLE table_name CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;`

## Или для каждой колонки

`ALTER TABLE table_name MODIFY column_name VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;`
