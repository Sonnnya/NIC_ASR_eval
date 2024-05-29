import jiwer
import os

# Путь к папкам с текстами и предсказаниями
test_folder = 'test' # папка с оригинальными текстами
predict_folder = 'model_predict' # папка с предсказаниями модели

# Кодировка файлов как параметр
def read_file(file_path, encoding='windows-1251'):
    with open(file_path, 'r', encoding=encoding) as file:
        return file.read().strip()

# Собираем все тексты из папки test_folder
test_texts = {}
if os.path.exists(test_folder) and os.path.isdir(test_folder):
    for filename in os.listdir(test_folder):
        if filename.endswith('.txt'):
            file_path = os.path.join(test_folder, filename)
            try:
                text = read_file(file_path, encoding='windows-1251')
            except UnicodeDecodeError:
                print("Кодировка файлов не windows-1251, попытка попробовать Unicode...")
                text = read_file(file_path, ncoding='utf-8')
            if text:
                test_texts[filename] = text

# Собираем все предсказания из папки predict_folder
predict_texts = {}
if os.path.exists(predict_folder) and os.path.isdir(predict_folder):
    for filename in os.listdir(predict_folder):
        if filename.endswith('.txt'):
            file_path = os.path.join(predict_folder, filename)
            try:
                text = read_file(file_path, encoding='windows-1251')
            except UnicodeDecodeError:
                print("Кодировка файлов не windows-1251, попытка попробовать Unicode...")
                text = read_file(file_path, ncoding='utf-8')
            if text:
                predict_texts[filename] = text

error_rates = []
for test_filename, test_text in test_texts.items():
    # Имена файлов в папках должны совпадать 
    # или можно организовать по-другому.
    predict_filename = test_filename  
    if predict_filename in predict_texts:
        predict_text = predict_texts[predict_filename]
        if test_text and predict_text:
            wer = jiwer.wer(test_text, predict_text)
            error_rates.append(wer)

if error_rates:
    mean_wer = sum(error_rates) / len(error_rates)
    print(f"Средний WER: {mean_wer:.4f}")
else:
    print("Нет данных для расчета WER.")
