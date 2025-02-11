import sys
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *

#Visual Practice rev0.1 Guillaume Sahuc fev/2025

class ZoomableGraphicsView(QGraphicsView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setRenderHint(QPainter.Antialiasing)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.AnchorUnderMouse)
        self.setDragMode(QGraphicsView.ScrollHandDrag)  
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

    def wheelEvent(self, event):
        zoom_factor = 1.05
        if event.angleDelta().y() > 0:
            self.scale(zoom_factor, zoom_factor)
        else:
            self.scale(1 / zoom_factor, 1 / zoom_factor)

class NoteTextItem(QGraphicsTextItem):
    def __init__(self, x, y, note, *args, **kwargs):
        super().__init__(note, *args, **kwargs)
        self.setDefaultTextColor(QColor("black"))
        font = QFont("Courier New")
        font.setPointSize(10)
        font.setBold(True)
        self.setFont(font)
        self.setZValue(1000.0)
        self.setPos(x - 11, y + 30)

class NoteItem(QGraphicsEllipseItem):
    def __init__(self, x, y, note, is_first_note=False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setRect(QRectF(x - 10 , y + 30, 20, 20))
        self.setBrush(QBrush(QColor("#FAEBD7")))

        pen = QPen()
        if is_first_note:
            pen.setWidth(3)
            pen.setColor(QColor("#7EC0EE"))
        self.setPen(pen)

        text_item = NoteTextItem(x, y, note)
        text_item.setParentItem(self)

class FretLabelItem(QGraphicsTextItem):
    def __init__(self, x, y, label, *args, **kwargs):
        super().__init__(label, *args, **kwargs)
        self.setDefaultTextColor(QColor("white"))
        font = QFont()
        font.setPointSize(10)
        font.setBold(True)
        self.setFont(font)
        self.setZValue(1000.0)
        self.setPos(x - 8, y + 10)

class NeckItem(QGraphicsItem):
    def __init__(self, frets, strings, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.frets = frets
        self.strings = strings

    def boundingRect(self) -> QRectF:
        return QRectF(0, 0, (self.frets + 1) * 50, self.strings * 30)

    def paint(self, painter: QPainter, option, widget=None):
        pen = QPen(QColor("#EEDFCC"))  # Définir la couleur du stylo pour les lignes
        painter.setPen(pen)
        for fret in range(self.frets + 1):
            for string in range(self.strings):
                x = fret * 50
                y = string * 30
                painter.drawRect(x + 25, y + 40, 50, 30)

class GuitarNeck:
    def __init__(self, scene, x_offset, y_offset, num_strings, note_pattern=None):
        self.note_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        self.string_tunings = ['E', 'B', 'G', 'D', 'A', 'E', 'B', 'F#', 'C#', 'G#'][:num_strings]  # Réglages pour un maximum de 10 cordes

        self.frets = 12
        self.strings = num_strings
        self.fret_labels = [0, 3, 5, 7, 9, 12, 15, 17, 19, 21, 24]
        self.note_pattern = note_pattern if note_pattern is not None else self.note_names
        self.scene = scene
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.create_neck()
        self.create_fret_labels()
        self.create_notes()

    def create_neck(self):
        self.neck_item = NeckItem(self.frets - 1, self.strings - 1)
        self.neck_item.setPos(self.x_offset, self.y_offset)
        self.scene.addItem(self.neck_item)

    def create_fret_labels(self):
        for label in self.fret_labels:
            if label <= self.frets:
                x = label * 50 + self.x_offset
                y = self.y_offset
                fret_label_item = FretLabelItem(x, y, str(label))
                self.scene.addItem(fret_label_item)

    def get_note_for_position(self, string, fret):
        open_string_note = self.note_names.index(self.string_tunings[string])
        note_index = (open_string_note + fret) % len(self.note_names)
        return self.note_names[note_index]

    def create_notes(self):
        for string in range(self.strings):
            for fret in range(self.frets + 1):
                note = self.get_note_for_position(string, fret)
                is_first_note = (note == self.note_pattern[0])
                if note in self.note_pattern:
                    x = fret * 50 + self.x_offset
                    y = string * 30 + self.y_offset
                    self.add_note_item(x, y, note, is_first_note)

    def add_note_item(self, x, y, note, is_first_note=False):
        note_item = NoteItem(x, y, note, is_first_note)
        self.scene.addItem(note_item)

def main():
    app = QApplication(sys.argv)

    scene = QGraphicsScene()
    scene.setSceneRect(-100, -100, 3200, 1200)  # Définir la taille de la scène

    num_strings = 7  # Définir le nombre de cordes souhaité, entre 6 et 10
    note_pattern = ['C', 'E', 'G']  # Exemple de modèle de notes
    num_columns = 3  # Nombre de colonnes

    cycle_of_fifths = ['C', 'G', 'D', 'A', 'E', 'B', 'F#', 'C#', 'G#', 'D#', 'A#', 'F']

    for i in range(12):
        x_offset = (i % num_columns) * 700
        y_offset = (i // num_columns) * 250
        # Calculer le nouveau pattern pour les quintes
        current_pattern = [(cycle_of_fifths[(cycle_of_fifths.index(note) + i) % 12]) for note in note_pattern]
        GuitarNeck(scene, x_offset, y_offset, num_strings, current_pattern)

    view = ZoomableGraphicsView(scene)
    view.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
