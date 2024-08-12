#!/bin/bash

error_exit() {
    echo "Ошибка: $1"
    exit 1
}


PLATFORM=$(uname -s) || error_exit "Не удалось определить платформу."
echo "Платформа: $PLATFORM"

# Установка Python
case $PLATFORM in
    Linux)
        echo "Платформа Linux обнаружена"
        
        # Проверка наличия wget
        if ! command -v wget &> /dev/null
        then
            echo "wget не найден. Устанавливаем wget..."
            sudo apt-get update || error_exit "Не удалось обновить списки пакетов."
            sudo apt-get install -y wget || error_exit "Не удалось установить wget."
        fi
        
        # Загрузка и установка Python
        PYTHON_VERSION="3.12.3"
        wget https://www.python.org/ftp/python/$PYTHON_VERSION/Python-$PYTHON_VERSION.tgz || error_exit "Не удалось загрузить Python."
        tar -xzf Python-$PYTHON_VERSION.tgz || error_exit "Не удалось распаковать архив Python."
        cd Python-$PYTHON_VERSION || error_exit "Не удалось перейти в каталог Python."
        ./configure --enable-optimizations || error_exit "Ошибка конфигурации Python."
        sudo make altinstall || error_exit "Ошибка установки Python."
        ;;
    
    Darwin)
        echo "Платформа macOS обнаружена"
        
        # Проверка наличия Homebrew
        if ! command -v brew &> /dev/null
        then
            echo "Homebrew не найден. Устанавливаем Homebrew..."
            /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)" || error_exit "Не удалось установить Homebrew."
        fi
        
        # Установка Python через Homebrew
        brew update || error_exit "Не удалось обновить Homebrew."
        brew install python || error_exit "Не удалось установить Python через Homebrew."
        ;;
    
    *)
        error_exit "Платформа $PLATFORM не поддерживается этим скриптом."
        ;;
esac

# Установка pip
if command -v python3 &> /dev/null
then
    echo "Устанавливаем pip..."
    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py || error_exit "Не удалось загрузить get-pip.py."
    python3 get-pip.py || error_exit "Не удалось установить pip."
else
    error_exit "Python не был установлен."
fi

# Установка библиотек из requirements.txt
if [ -f "requirements.txt" ]; then
    echo "Установка библиотек из requirements.txt..."
    pip3 install -r requirements.txt || error_exit "Не удалось установить библиотеки из requirements.txt."
else
    echo "Файл requirements.txt не найден, пропускаем установку зависимостей."
fi

# Проверка установки Python и pip
if command -v python3 &> /dev/null && command -v pip3 &> /dev/null
then
    echo "Python и pip успешно установлены!"
    python3 --version
    pip3 --version
else
    error_exit "Ошибка: Python или pip не были установлены."
fi



SERVICE_FILE="/etc/systemd/system/"

if [ -f "main.py" ]; then
    read -p "Хотите создать службу для запуска Gaia Faker? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        sudo bash -c "cat > $SERVICE_FILE" <<EOL
[Unit]
Description=Gaia testing tool
After=network.target

[Service]
User=$(whoami)
WorkingDirectory=$(pwd)
ExecStart=$(which python3) $(pwd)/main.py
Restart=always

[Install]
WantedBy=multi-user.target
EOL

        # Перезагрузка systemd и активация службы
        sudo systemctl daemon-reload || error_exit "Не удалось перезагрузить systemd."
        sudo systemctl enable gaiafaker.service || error_exit "Не удалось включить службу."
        sudo systemctl start gaiafaker.service || error_exit "Не удалось запустить службу."

        echo "Служба запущена!"

    else
        echo "Служба не создана."
    fi
else
    echo "Файл main.py не найден, пропускаем создание службы."
fi
