import sys
import requests
from PySide6 import QtCore, QtWidgets, QtGui
import Data_Handler  # Importiere das Modul für Datenabruf

class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # Layout für die Widgets
        self.layout = QtWidgets.QVBoxLayout(self)

        # Eingabefeld für den GitHub-Benutzernamen
        self.username_input = QtWidgets.QLineEdit(self)
        self.username_input.setPlaceholderText("Gib den GitHub Benutzernamen ein")
        self.layout.addWidget(self.username_input)

        # Button zur Bestätigung des Benutzernamens
        self.confirm_button = QtWidgets.QPushButton("Benutzer bestätigen")
        self.layout.addWidget(self.confirm_button)

        # Label zur Anzeige des Benutzernamens und der öffentlichen Repositories
        self.user_info_label = QtWidgets.QLabel("", alignment=QtCore.Qt.AlignCenter)
        self.layout.addWidget(self.user_info_label)

        # Label für das Profilbild
        self.avatar_label = QtWidgets.QLabel("", alignment=QtCore.Qt.AlignCenter)
        self.layout.addWidget(self.avatar_label)

        # Verbindungen der Buttons zu ihren Funktionen
        self.confirm_button.clicked.connect(self.fetch_github_user_info)

        self.avatar_label.resize(50, 50)

    @QtCore.Slot()
    def fetch_github_user_info(self):
        """Holt Informationen über den angegebenen GitHub-Benutzer."""

        username = self.username_input.text().strip()  # Leerzeichen entfernen

        if username:
            user_info = Data_Handler.fetch_github_user_info(username)  # Aufruf der Funktion

            if user_info:
                login, public_repos, avatar_url = user_info

                # Anzeigen der Benutzerinformationen und des Profilbilds
                self.user_info_label.setText(f"Benutzername: {login}\nÖffentliche Repositories: {public_repos}")

                try:
                    # Setzen des Profilbildes als Pixmap im QLabel
                    response = requests.get(avatar_url)
                    response.raise_for_status()  # Überprüfen auf HTTP-Fehler

                    pixmap = QtGui.QPixmap()
                    pixmap.loadFromData(response.content)
  
                    if not pixmap.isNull():  # Überprüfen, ob das Pixmap erfolgreich geladen wurde
                        self.avatar_label.setPixmap(pixmap.scaled(400, 400, QtCore.Qt.KeepAspectRatio))
                    else:
                        print("Das Bild konnte nicht geladen werden.")
                        self.avatar_label.clear()  # Leeren bei Fehler

                except Exception as e:
                    print(f"Fehler beim Laden des Bildes: {e}")
                    self.avatar_label.clear()  # Leeren bei Fehler

            else:
                self.user_info_label.setText("Benutzer nicht gefunden.")
                self.avatar_label.clear()  # Leeren des Bildes bei Fehler

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    widget = MyWidget()
    widget.resize(800, 600)
    widget.setWindowTitle("GitHub Benutzerinfo")
    widget.show()
    sys.exit(app.exec())
    