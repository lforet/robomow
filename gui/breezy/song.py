"""
File: song.py
Author: Kenneth A. Lambert
"""

class Song(object):
    """Models a song."""

    def __init__(self, title, artist, price):
        """Sets up the model."""
        self.title = title
        self.artist = artist
        self.price = price

    def __str__(self):
        """Returns the string rep of the song."""
        return "Title:  " + self.title + "\n" + \
               "Artist: " + self.artist + "\n" + \
               "Price:  $%.2f\n" % self.price

def testSong():
    """Creates and prints a song."""
    song = Song("Let It Be", "The Beatles", 0.99)
    print(song)

import pickle

class SongDatabase(object):
    """Models a song database."""

    def __init__(self, fileName = ""):
        """Sets up the model.  Loads the model with songs if there
        is a file name"""
        self._items = {}
        self.fileName = fileName
        if fileName != "":
            try:
                file = open(fileName, "rb")
                while True:
                    song = pickle.load(file)
                    self[song.title] = song
            except Exception:
                file.close()

    def save(self, fileName = ""):
        """Saves the database to a file."""
        if fileName != "":
            self.fileName = fileName
        elif self.fileName == "": return
        file = open(self.fileName, "wb")
        for song in self._items.values():
            pickle.dump(song, file)
        file.close()

    def __getitem__(self, title):
        """Returns the cd with the given title, or None if
        the title does not exist."""
        return self._items.get(title, None)

    def __setitem__(self, title, song):
        """Adds or replaces the cd at the given title."""
        self._items[title] = song

    def pop(self, title):
        """Removes and returns the cd at the given title,
        or returns None if the title does not exist."""
        return self._items.pop(title, None)

    def getTitles(self):
        """Returns a sorted list of titles."""
        titles = list(self._items.keys())
        titles.sort()
        return titles

    def __str__(self):
        """Returns the string rep of the database."""
        return "\n".join(map(lambda title: str(self[title]),
                             self.getTitles()))

def testDatabase():
    """Creates a database, prints it, saves it,
    loads it, and prints it."""
    database = SongDatabase()
    song = Song("Let It Be", "The Beatles", 0.99)
    database[song.title] = song
    song = Song("Gimme Shelter", "The Rolling Stones", 01.29)
    database[song.title] = song
    song = Song("Kashmir", "Led Zepplin", 1.29)
    database[song.title] = song
    song = Song("Der Komissar", "Falco", 0.99)
    database[song.title] = song
    print(database)
    database.save("songs.dat")
    newdb = SongDatabase("songs.dat")
    print(newdb)
    
if __name__ == "__main__":
    testDatabase()

