import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

class MovieLibrary:
    def __init__(self, root):
        self.root = root
        self.root.title("Movie Library")
        self.root.geometry("800x600")

        # Загрузка фильмов
        self.movies = self.load_movies()
        self.setup_ui()

    def setup_ui(self):
        # Поле ввода названия фильма
        ttk.Label(self.root, text="Название фильма:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.title_entry = ttk.Entry(self.root, width=40)
        self.title_entry.grid(row=0, column=1, padx=10, pady=5)

        # Поле выбора жанра
        ttk.Label(self.root, text="Жанр:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.genre_var = tk.StringVar()
        genres = ["Драма", "Комедия", "Боевик", "Фантастика", "Ужасы", "Мелодрама", "Детектив", "Анимация"]
        self.genre_combo = ttk.Combobox(self.root, textvariable=self.genre_var, values=genres, state="readonly")
        self.genre_combo.grid(row=1, column=1, padx=10, pady=5)

        # Поле ввода года выпуска
        ttk.Label(self.root, text="Год выпуска:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.year_entry = ttk.Entry(self.root)
        self.year_entry.grid(row=2, column=1, padx=10, pady=5)

        # Поле ввода рейтинга (0–10)
        ttk.Label(self.root, text="Рейтинг (0–10):").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.rating_entry = ttk.Entry(self.root)
        self.rating_entry.grid(row=3, column=1, padx=10, pady=5)

        # Кнопка добавления фильма
        self.add_btn = ttk.Button(self.root, text="Добавить фильм", command=self.add_movie)
        self.add_btn.grid(row=4, column=0, columnspan=2, pady=10)

        # Фильтры
        ttk.Label(self.root, text="Фильтр по жанру:").grid(row=5, column=0, padx=10, pady=5, sticky="w")
        self.filter_genre_var = tk.StringVar(value="Все")
        self.filter_genre_combo = ttk.Combobox(
            self.root,
            textvariable=self.filter_genre_var,
            values=["Все"] + genres
        )
        self.filter_genre_combo.grid(row=5, column=1, padx=10, pady=5)


        ttk.Label(self.root, text="Фильтр по году:").grid(row=6, column=0, padx=10, pady=5, sticky="w")
        self.filter_year_entry = ttk.Entry(self.root)
        self.filter_year_entry.grid(row=6, column=1, padx=10, pady=5)

        self.apply_filter_btn = ttk.Button(self.root, text="Применить фильтры", command=self.refresh_movies_table)
        self.apply_filter_btn.grid(row=7, column=0, columnspan=2, pady=5)

        # Таблица фильмов
        ttk.Label(self.root, text="Коллекция фильмов:").grid(row=8, column=0, columnspan=2, pady=10)
        columns = ("ID", "Название", "Жанр", "Год", "Рейтинг")
        self.movies_tree = ttk.Treeview(self.root, columns=columns, show="headings", height=12)

        for col in columns:
            self.movies_tree.heading(col, text=col)
            self.movies_tree.column(col, width=140)

        self.movies_tree.grid(row=9, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        # Заполнение таблицы
        self.refresh_movies_table()


    def load_movies(self):
        if os.path.exists("movies.json"):
            with open("movies.json", "r", encoding="utf-8") as f:
                return json.load(f)
        return []

    def save_movies(self):
        with open("movies.json", "w", encoding="utf-8") as f:
            json.dump(self.movies, f, ensure_ascii=False, indent=2)

    def add_movie(self):
        title = self.title_entry.get().strip()
        genre = self.genre_var.get()
        year_str = self.year_entry.get().strip()
        rating_str = self.rating_entry.get().strip()

        # Валидация полей
        if not title:
            messagebox.showerror("Ошибка", "Название фильма не может быть пустым")
            return
        if not genre:
            messagebox.showerror("Ошибка", "Выберите жанр")
            return

        # Валидация года выпуска
        try:
            year = int(year_str)
            if year < 1888 or year > 2030:  # 1888 — год первого фильма
                messagebox.showerror("Ошибка", "Год должен быть в диапазоне 1888–2030")
                return
        except ValueError:
            messagebox.showerror("Ошибка", "Год выпуска должен быть числом")
            return

        # Валидация рейтинга
        try:
            rating = float(rating_str)
            if rating < 0 or rating > 10:
                messagebox.showerror("Ошибка", "Рейтинг должен быть от 0 до 10")
                return
        except ValueError:
            messagebox.showerror("Ошибка", "Рейтинг должен быть числом")
            return

        # Добавление фильма
        movie = {
            "id": len(self.movies) + 1,
            "title": title,
            "genre": genre,
            "year": year,
            "rating": rating
        }
        self.movies.append(movie)
        self.save_movies()
        self.refresh_movies_table()

        # Очистка полей ввода
        self.title_entry.delete(0, tk.END)
        self.genre_var.set("")
        self.year_entry.delete(0, tk.END)
        self.rating_entry.delete(0, tk.END)

        messagebox.showinfo("Успех", "Фильм добавлен в коллекцию")

    def refresh_movies_table(self):
        # Очистка таблицы
        for item in self.movies_tree.get_children():
            self.movies_tree.delete(item)

        # Получение фильтров
        filter_genre = self.filter_genre_var.get()
        filter_year_str = self.filter_year_entry.get().strip()

        filtered_movies = self.movies


        # Фильтр по жанру
        if filter_genre != "Все":
            filtered_movies = [m for m in filtered_movies if m["genre"] == filter_genre]

        # Фильтр по году
        if filter_year_str:
            try:
                filter_year = int(filter_year_str)
                filtered_movies = [m for m in filtered_movies if m["year"] == filter_year]
            except ValueError:
                messagebox.showwarning("Предупреждение", "Некорректный год для фильтра")
                return

        # Заполнение таблицы отфильтрованными записями
        for movie in filtered_movies:
            self.movies_tree.insert("", "end", values=(
                movie["id"],
                movie["title"],
                movie["genre"],
                movie["year"],
                f"{movie['rating']:.1f}"
            ))

if __name__ == "__main__":
    root = tk.Tk()
    app = MovieLibrary(root)
    root.mainloop()
