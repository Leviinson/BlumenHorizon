# Документация по установке и инициализации

## Установка

1. **Обновление cтандартных пакетов:**
   Перед началом установки рекомендуется обновить все пакеты на вашей системе, чтобы убедиться, что у вас установлены последние версии.

   ```bash
   sudo apt update -y && sudo apt upgrade -y
   ```

2. **Установка необходимых пакетов:**

    ```bash
    sudo apt install -y htop tree wget nginx mysql-server neovim zsh python3-dev default-libmysqlclient-dev build-essential pkg-config

    # Oh My Zsh (можете добавить свою конфигурацию в ~/.zshrc config. файл)
    sh -c "$(wget https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh -O -)"

    # Redis
    sudo apt-get install lsb-release curl gpg
    curl -fsSL https://packages.redis.io/gpg | sudo gpg --dearmor -o /usr/share/keyrings/redis-archive-keyring.gpg
    sudo chmod 644 /usr/share/keyrings/redis-archive-keyring.gpg
    echo "deb [signed-by=/usr/share/keyrings/redis-archive-keyring.gpg] https://packages.redis.io/deb $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/redis.list
    sudo apt-get update
    sudo apt-get install redis

    # Check healthness
    redis-cli -c ping

    # Poetry
    curl -sSL https://install.python-poetry.org | python3 -
    echo 'export PATH="/root/.local/bin:$PATH"' >> ~/.zshrc
    source ~/.zshrc
    poetry config virtualenvs.in-project true
    ```

3. **Создание рабочей директории и инициализация в неё исходного кода проекта:**

    ```bash
    mkdir /var/www/blumenhorizon/
    cd /var/www/blumenhorizon/

    git init .
    git config --global init.defaultBranch main
    ```

    Запросите у наставника Ваш Fine-grained PAT-token, чтобы иметь возможность запуллить код проекта на Ваш VPS.
    Для следующих разрешений будет доступ чтения/записи: Commit statuses, Contents.
    Для Metadata только чтение.

    ```bash
    git remote add origin https://(вставить сюда выданный PAT TOKEN без скобочек)>@github.com/Leviinson/BlumenHorizon.git
    git pull origin main
    poetry shell
    poetry install --only main
    ```

    Запросите у Вашего наставника .env файл и поместите его содержимое в .env в /var/www/blumenhorizon/.env

## Настройка БД

### Установить базе данных кодировку для поддержки эмодзи

`ALTER DATABASE blumenhorizon CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;`

### По-надобности сделать это для каждой таблицы

`ALTER TABLE table_name CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;`

### Или для каждой колонки

`ALTER TABLE table_name MODIFY column_name VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;`
