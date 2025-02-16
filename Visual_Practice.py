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
    def __init__(self, scene, x_offset, y_offset, num_strings, num_frets, note_pattern=None):
        self.note_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        self.string_tunings = ['E', 'B', 'G', 'D', 'A', 'E', 'B', 'F#', 'C#', 'G#'][:num_strings]  # Réglages pour un maximum de 10 cordes

        self.frets = num_frets
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

class Pattern:
    def __init__(self, name, notes):
        self.name = name
        self.notes = notes

    def __repr__(self):
        return f"Pattern(name={self.name}, notes={self.notes})"



def main():
    app = QApplication(sys.argv)
    
    #initialisation de plusieurs patterns
    patterns = [
        Pattern("Major arpeggio", ['C', 'E', 'G']),
        Pattern("Minor arpeggio", ['A', 'C', 'E']),
        Pattern("Pentatonic Major Scale", ['C', 'D', 'E', 'G', 'A']),
        Pattern("Pentatonic Minor Scale", ['A', 'C', 'D', 'E', 'G']),
        Pattern("Blues Major Scale", ['G', 'A', 'A#', 'B', 'D', 'E']),
        Pattern("Blues Minor Scale", ['F', 'G#', 'A#', 'B', 'C', 'D#']),
        Pattern("Major Scale", ['C', 'D', 'E', 'F', 'G', 'A', 'B']),
        Pattern("Minor Scale", ['A', 'B', 'C', 'D', 'E', 'F', 'G']),
        Pattern("Byzantine Scale", ['C', 'C#', 'E', 'F', 'G', 'G#', 'B']),
]

    scene = QGraphicsScene()
    scene.setSceneRect(-100, -100, 6000, 2000)  # Définir la taille de la scène

    num_strings = 7  # Définir le nombre de cordes souhaité, entre 6 et 10
    num_columns = 3  # Nombre de colonnes
    num_frets = 12   # Nombre de frettes

    cycle_of_fifths = ['C', 'G', 'D', 'A', 'E', 'B', 'F#', 'C#', 'G#', 'D#', 'A#', 'F']

    # Ajoute l'image en arrière-plan
    pixmap = QPixmap("guitar.png")  # Remplace par le chemin de ton image
    # Agrandir l'image par 2
    scaled_pixmap = pixmap.scaled(pixmap.width() * 2, pixmap.height() * 2)
    scene.image_item = QGraphicsPixmapItem(scaled_pixmap)
    scene.image_item.setPos(0, 0)  # Positionne l'image à (700, 0)
    opacity_effect = QGraphicsOpacityEffect()
    opacity_effect.setOpacity(0.3)  # X% de transparence
    scene.image_item.setGraphicsEffect(opacity_effect)
    scene.addItem(scene.image_item)
    

    # Ajoute le texte
    scene.text_item = QGraphicsTextItem("Visual Practice : ")
    font = QFont("Engraved MT", 20)
    scene.text_item.setFont(font)
    scene.text_item.setDefaultTextColor(Qt.white)

    # Créer un QComboBox et ajouter les noms des patterns
    combo_box = QComboBox()
    #combo_box.setFixedSize(300, 35)  # Définir la taille du QComboBox (largeur x hauteur)
    # Définir une nouvelle police et l'appliquer au QComboBox
    font = QFont()
    font.setPointSize(20)
    combo_box.setFont(font)
    for pattern in patterns:
        combo_box.addItem(pattern.name)


    # Positionne le texte centré en haut
    text_rect = scene.text_item.boundingRect()
    text_x = 300
    scene.text_item.setPos(text_x, -50)
    scene.addItem(scene.text_item)
    
    # Intégrer le QComboBox dans la scène en utilisant un QGraphicsProxyWidget
    proxy = QGraphicsProxyWidget()
    proxy.setWidget(combo_box)
    combo_x = 500
    proxy.setPos(combo_x, -50)
    scene.addItem(proxy)
    
    def clear_scene():
        for item in scene.items():
            if isinstance(item, (NeckItem, NoteItem, NoteTextItem, FretLabelItem)):
                scene.removeItem(item)


    def update_scene():
        # Effacer tous les éléments de la scène
        clear_scene()


        # Récupérer le pattern sélectionné
        selected_pattern_name = combo_box.currentText()
        selected_pattern = next((pattern for pattern in patterns if pattern.name == selected_pattern_name), None)

        if selected_pattern:
            for i in range(12):
                x_offset = (i % num_columns) * 62.5 * num_frets
                y_offset = (i // num_columns) * 250
                # Calculer le nouveau pattern pour les quintes
                current_pattern = [(cycle_of_fifths[(cycle_of_fifths.index(note) + i) % 12]) for note in selected_pattern.notes]
                GuitarNeck(scene, x_offset, y_offset, num_strings, num_frets, current_pattern)
                


    # Connecter le signal currentIndexChanged du QComboBox à la méthode update_scene
    combo_box.currentIndexChanged.connect(update_scene)
    
    # Initialiser la scène avec le premier pattern
    update_scene()
    view = ZoomableGraphicsView(scene)
    view.scale(1 / 1.4, 1 / 1.4)
    view.centerOn(0, 0)
    view.showMaximized()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
