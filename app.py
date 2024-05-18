import speech_recognition as sr
import pandas as pd
import difflib

import soundfile as sf

def convert_ogg_to_wav(input_file, output_file):
    data, samplerate = sf.read(input_file)
    sf.write(output_file, data, samplerate, format='WAV')

# Usage example
convert_ogg_to_wav("1/1.ogg", "1/1.wav")
# Функция для распознавания речи из аудиофайла
def recognize_audio(file_path):
    recognizer = sr.Recognizer()
    with sr.AudioFile(file_path) as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data, language="ru-RU")
            return text
        except sr.UnknownValueError:
            return "Распознавание не удалось"
        except sr.RequestError as e:
            return f"Ошибка запроса к сервису Google; {e}"

# Измененная функция для поиска наиболее похожего предложения в файле Excel
def find_similar_sentence(sentence, df):
    max_similarity = 0
    most_similar_sentence = ""
    sentence_row = 0
    for index, row in enumerate(df.itertuples(index=False), 1):
        excel_sentence = row[0]
        similarity = difflib.SequenceMatcher(None, sentence, excel_sentence).ratio()
        if similarity > max_similarity:
            max_similarity = similarity
            most_similar_sentence = excel_sentence
            sentence_row = index  # Сохраняем номер строки
    return most_similar_sentence, sentence_row, max_similarity

# Функция для выявления различий между двумя предложениями
def find_differences(sentence1, sentence2):
    s = difflib.ndiff(sentence1.split(), sentence2.split())
    return ' '.join(x[2:] for x in s if x.startswith('- ') or x.startswith('+ '))

# Основной код
if __name__ == "__main__":
    recognized_text = recognize_audio("1/1.wav")  # Распознавание текста из аудио
    print("Распознанный текст:", recognized_text)

    # Загрузка данных из Excel
    df = pd.read_excel("1/дефекты.xlsx", header=None)

    # Поиск наиболее похожего предложения, номера строки и процента схожести
    similar_sentence, sentence_row, similarity_percentage = find_similar_sentence(recognized_text, df)
    print(f"Наиболее похожее предложение из файла в строке {sentence_row}: {similar_sentence}")
    print(f"Процент схожести: {similarity_percentage*100:.2f}%")

    # Нахождение и вывод различий
    differences = find_differences(recognized_text, similar_sentence)
    print("Различия:", differences)