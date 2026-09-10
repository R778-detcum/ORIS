class Playlist:
    def __init__(self):
        self.songs = []

    def add_song(self, name, duration):
        if not isinstance(name, str):
            print("Ошибка: название должно быть строкой")
            return
        if not isinstance(duration, (int, float)):
            print("Ошибка: длительность должна быть числом")
            return
        if duration <= 0:
            print("Ошибка: длительность должна быть больше нуля")
            return

        song = {"name": name, "duration": duration}
        self.songs.append(song)
        print("Песня добавлена")

    def remove_song(self, name):
        for song in self.songs:
            if song["name"] == name:
                self.songs.remove(song)
                print("Песня удалена")
                return
        print("Песни с таким названием нет")

    def total_duration(self):
        total = 0
        for song in self.songs:
            total += song["duration"]
        return total

    def __len__(self):
        return len(self.songs)

    def show(self):
        if len(self.songs) == 0:
            print("Плейлист пуст")
        else:
            for i in range(len(self.songs)):
                song = self.songs[i]
                print(i + 1, "-", song["name"], "-", song["duration"], "сек")


playlist = Playlist()

print("пустой плейлист ")
print("Количество:", len(playlist))
print("Длительность:", playlist.total_duration())
playlist.show()

print()
print("добавляем песни ")
playlist.add_song("Bohemian Rhapsody", 354)
playlist.add_song("Song 1", 200)
playlist.add_song("Song 2", 300)
print("Количество:", len(playlist))
print("Длительность:", playlist.total_duration())
playlist.show()

print()
print("удаляем существующую песню")
playlist.remove_song("Song 1")
print("Количество:", len(playlist))
print("Длительность:", playlist.total_duration())
playlist.show()

print()
print("удаляем несуществующую песню ")
playlist.remove_song("Какая-то песня")
print("Количество:", len(playlist))

print()
print("удаляем из плейлиста с несколькими песнями")
playlist.remove_song("Bohemian Rhapsody")
print("Количество:", len(playlist))
print("Длительность:", playlist.total_duration())
playlist.show()

print()
print("пробуем добавить неправильные данные")
playlist.add_song("Плохая", "две минуты")
playlist.add_song(12345, 100)
playlist.add_song("Ноль", 0)
print("Количество не изменилось:", len(playlist))
