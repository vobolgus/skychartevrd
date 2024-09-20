# Используем официальный образ Python
FROM python:3.11-slim

# Устанавливаем LaTeX и зависимости
RUN apt-get update && apt-get install -y \
    texlive-latex-base \
    texlive-latex-recommended \
    texlive-latex-extra \
    texlive-fonts-recommended \
    texlive-fonts-extra \
    texlive-lang-cyrillic \
    latexmk

# Устанавливаем необходимые Python-зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Устанавливаем рабочую директорию
WORKDIR /usr/src/app

# Копируем все файлы проекта в контейнер
COPY . .

# Команда для запуска бота
CMD ["python", "bot.py"]
