import os
import subprocess
import shutil

# Функция для компиляции LaTeX файла в PDF
def compile_latex_to_pdf(tex_filename, output_directory, pdf_destination):
    try:
        # Проверяем, существует ли папка для выходных файлов, и создаём её, если она не существует
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)

        if not os.path.exists(pdf_destination):
            os.makedirs(pdf_destination)
        # Вызываем pdflatex для компиляции .tex файла в PDF
        with open(os.devnull, 'w') as FNULL:
            # Компилируем LaTeX файл, указывая папку для выходных файлов, подавляя вывод
            print(f"Компиляция {tex_filename}...")
            subprocess.run(["pdflatex",f"-output-directory={output_directory}", tex_filename],
                stdout=FNULL, stderr=FNULL, check=True)
            # Определяем базовое имя файла (без расширения)
            base_filename = os.path.splitext(os.path.basename(tex_filename))[0]
            pdf_filename = base_filename + ".pdf"

            # Полный путь к PDF-файлу в папке output
            pdf_filepath = os.path.join(output_directory, pdf_filename)

            # Проверяем, существует ли PDF файл и перемещаем его в папку назначения
            if os.path.exists(pdf_filepath):
                destination_filepath = os.path.join(pdf_destination, pdf_filename)
                shutil.move(pdf_filepath, destination_filepath)
                print(f"PDF файл перемещён в {destination_filepath}")
            else:
                print(f"PDF файл {pdf_filename} не найден в папке {output_directory}")
        print(f"Успешно скомпилирован файл: {tex_filename}")
    except subprocess.CalledProcessError:
        print(f"Ошибка при компиляции {tex_filename}")