
#Подключение библиотек
import matplotlib.pyplot as plt
import pandas as pd
import csv

#Функция конвертирования типа данных str в int для дальнейшей работы с CSV файлом
def convert_str_num_to_int(data: pd.DataFrame, col_names: list) -> pd.DataFrame:
    new_df = data.copy()
    for col in col_names:
        new_df[col] = new_df[col].str.replace("K", "000")
        new_df[col] = new_df[col].map(lambda x: int(float(x) * 1000) if '.' in x else int(x))
    return new_df
#Функция удаление не нужный столбцов по их названию. Нужно для дальнейшей работы с CSV файлом
def drop_columns(data: pd.DataFrame, cols_to_drop: list = None, idx_to_drop: list = None) -> pd.DataFrame:
    new_data = data.copy()
    if cols_to_drop is not None:
        new_data = new_data.drop(columns=cols_to_drop, errors='ignore')
    if idx_to_drop is not None:
        new_data = new_data.drop(index=idx_to_drop)
    return new_data

#Чтение исходного CSV файла и удаление не нужных столбцов
data = pd.read_csv('games.csv')
cols_names = ["Times Listed", "Summary" , "Reviews" , "Backlogs", "Wishlist", "Team", "Unnamed: 0" ]
data = drop_columns(data, cols_to_drop=cols_names)
#Конвертирование нужный столбцов из str в int
numerical_cols = ["Plays", "Playing", "Number of Reviews"]
data = convert_str_num_to_int(data, numerical_cols)
#Удаляем квадратные скобки и ковычки. Создаем новый DF с бинарными столбцами. Дальше считаем сумму того или иного жанра
data["Genres"] = data["Genres"].str.replace(r'[\[\]\'\"]', "", regex=True)
genres = data["Genres"].str.get_dummies(",")
popularity = genres.sum().sort_values(ascending=False)

#Создаем новый dataset с двумя столбцами Genre и Popularity ( фильтруем и удаляем дубликаты)
dataset = pd.DataFrame({"Genre": popularity.index, "Popularity": popularity.values})
dataset["Genre"] = dataset["Genre"].astype("category")
dataset['Genre'] = dataset['Genre'].drop_duplicates()
dataset = dataset[dataset['Popularity'] >= 90]

#Построение графика, засчет dataset
dataset.plot.bar(x='Genre', y='Popularity')
plt.xlabel('Genre')
plt.ylabel('Popularity')
plt.show()

# СSV файл в котором хранятся жанры и их популярность
output_file = 'popularity.csv'
dataset.to_csv(output_file, index=False)
# CSV файл, в котором хранится очищенный исходный CSV файл
output_file = 'New_game_info.csv'
data.to_csv(output_file, index=False)

