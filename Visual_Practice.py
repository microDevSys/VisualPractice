import sys
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *

#Visual Practice rev0.6 © Guillaume Sahuc 2025/07
#https://github.com/microDevSys/VisualPractice
#https://creativecommons.org/licenses/by-nc-nd/4.0/deed.en

#just a tools to practice, if you want to support my work : paypal.me/VisualPractice

# Constants
NOTE_FONT_SIZE = 10
FRET_FONT_SIZE = 10
CHORD_LABEL_FONT_SIZE = 18
#YOU CAN CHOOSE COLOR HERE = http://guillaume.sahuc.free.fr/couleur.html
NECK_COLOR = "#EEDFCC"
FIRST_NOTE="#7EC0EE"
NOTE_COLOR = "#FAEBD7"
FRET_LABELS = [0, 3, 5, 7, 9, 12, 15, 17, 19, 21, 24]
STRING_TUNINGS = ['E', 'B', 'G', 'D', 'A', 'E', 'B', 'F#', 'C#', 'G#']

# Liste des notes avec dièses et bémols
notes_sharp = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
notes_flat = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]

# Dictionnaire des notes enharmoniques
enharmonic_notes = {
    "Cb": "B",  # Do bémol est équivalent à Si
    "Fb": "E",  # Fa bémol est équivalent à Mi
    "B#": "C",  # Si dièse est équivalent à Do
    "E#": "F"  # Mi dièse est équivalent à Fa
}

enharmonic_tunings_notes = {
    "F#": "Gb",  # Fa dièse est équivalent à Sol bémol
    "C#": "Db",  # Do dièse est équivalent à Ré bémol
    "G#": "Ab" # Sol dièse est équivalent à La bémol
}

enharmonic_accidentals_notes = {
    "Eb" : "D#",
    "Ab" : "G#", 
    "Db" : "C#",
    "Gb" : "F#",
    "Cb" : "B",
    "Fb" : "E"
}

# Schéma des intervalles pour différents types de gammes
SCALE_TYPES = {
    "major": [2, 2, 1, 2, 2, 2, 1],  # Gamme majeure (Ionien)
    "minor": [2, 1, 2, 2, 1, 2, 2],  # Gamme mineure naturelle (Éolien)
    "minor_harmonic": [2, 1, 2, 2, 1, 3, 1],  # Gamme mineure harmonique
    "minor_melodic_asc": [2, 1, 2, 2, 2, 2, 1],  # Gamme mineure mélodique ascendante
    "minor_melodic_desc": [2, 1, 2, 2, 1, 2, 2],  # Gamme mineure mélodique descendante (identique à naturelle)
    "pentatonic_major": [2, 2, 3, 2, 3],  # Gamme pentatonique majeure
    "pentatonic_minor": [3, 2, 2, 3, 2],  # Gamme pentatonique mineure
    "blues_major": [2, 1, 1, 3, 2, 3],  # Gamme blues majeure
    "blues_minor": [3, 2, 1, 1, 3, 2],  # Gamme blues mineure
    "byzantine": [1, 3, 1, 2, 1, 3, 1],  # Gamme byzantine
    # Modes diatoniques
    "ionian": [2, 2, 1, 2, 2, 2, 1],  # Mode Ionien (identique à la gamme majeure)
    "dorian": [2, 1, 2, 2, 2, 1, 2],  # Mode Dorien
    "phrygian": [1, 2, 2, 2, 1, 2, 2],  # Mode Phrygien
    "lydian": [2, 2, 2, 1, 2, 2, 1],  # Mode Lydien
    "mixolydian": [2, 2, 1, 2, 2, 1, 2],  # Mode Mixolydien
    "aeolian": [2, 1, 2, 2, 1, 2, 2],  # Mode Éolien (identique à la gamme mineure naturelle)
    "locrian": [1, 2, 2, 1, 2, 2, 2]  # Mode Locrien
}

CHORDS_INTERVALS = {
    "major": [0, 4, 7],          # Fondamentale, Tierce Majeure, Quinte Juste
    "minor": [0, 3, 7],          # Fondamentale, Tierce Mineure, Quinte Juste
    "diminished": [0, 3, 6],     # Fondamentale, Tierce Mineure, Quinte Diminuée
    "augmented": [0, 4, 8],      # Fondamentale, Tierce Majeure, Quinte Augmentée
    "sus2": [0, 2, 7],           # Fondamentale, Seconde Majeure, Quinte Juste
    "sus4": [0, 5, 7],           # Fondamentale, Quarte Juste, Quinte Juste
    "dominant7": [0, 4, 7, 10],  # Fondamentale, Tierce Majeure, Quinte Juste, Septième Mineure
    "maj7": [0, 4, 7, 11],       # Fondamentale, Tierce Majeure, Quinte Juste, Septième Majeure
    "m7": [0, 3, 7, 10],    # Fondamentale, Tierce Mineure, Quinte Juste, Septième Mineure
    "mMaj7": [0, 3, 7, 11], # Fondamentale, Tierce Mineure, Quinte Juste, Septième Majeure
    "half_dim7": [0, 3, 6, 10],  # Fondamentale, Tierce Mineure, Quinte Diminuée, Septième Mineure
    "dim7": [0, 3, 6, 9],        # Fondamentale, Tierce Mineure, Quinte Diminuée, Septième Diminuée
    "7sus4": [0, 5, 7, 10]       # Fondamentale, Quarte Juste, Quinte Juste, Septième Mineure
}


# Dictionnaire des armures pour les gammes majeures et mineures
key_signatures = {
    "C": {"use_sharps": True, "accidentals": []},
    "G": {"use_sharps": True, "accidentals": ["F#"]},
    "D": {"use_sharps": True, "accidentals": ["F#", "C#"]},
    "A": {"use_sharps": True, "accidentals": ["F#", "C#", "G#"]},
    "E": {"use_sharps": True, "accidentals": ["F#", "C#", "G#", "D#"]},
    "B": {"use_sharps": True, "accidentals": ["F#", "C#", "G#", "D#", "A#"]},
    "F#": {"use_sharps": True, "accidentals": ["F#", "C#", "G#", "D#", "A#", "E#"]},
    "Cb": {"use_sharps": False, "accidentals": ["Bb", "Eb", "Ab", "Db", "Gb", "Cb", "Fb"]},
    "Gb": {"use_sharps": False, "accidentals": ["Bb", "Eb", "Ab", "Db", "Gb", "Cb"]},
    "Db": {"use_sharps": False, "accidentals": ["Bb", "Eb", "Ab", "Db", "Gb"]},
    "Ab": {"use_sharps": False, "accidentals": ["Bb", "Eb", "Ab", "Db"]},
    "Eb": {"use_sharps": False, "accidentals": ["Bb", "Eb", "Ab"]},
    "Bb": {"use_sharps": False, "accidentals": ["Bb", "Eb"]},
    "F": {"use_sharps": False, "accidentals": ["Bb"]}
}

key_signatures_minor = {
    "A minor": {"use_sharps": True, "accidentals": []},
    "E minor": {"use_sharps": True, "accidentals": ["F#"]},
    "B minor": {"use_sharps": True, "accidentals": ["F#", "C#"]},
    "F# minor": {"use_sharps": True, "accidentals": ["F#", "C#", "G#"]},
    "C# minor": {"use_sharps": True, "accidentals": ["F#", "C#", "G#", "D#"]},
    "G# minor": {"use_sharps": True, "accidentals": ["F#", "C#", "G#", "D#", "A#"]},
    "D# minor": {"use_sharps": True, "accidentals": ["F#", "C#", "G#", "D#", "A#", "E#"]},
    "Ab minor": {"use_sharps": False, "accidentals": ["Bb", "Eb", "Ab", "Db", "Gb", "Cb", "Fb"]},
    "Eb minor": {"use_sharps": False, "accidentals": ["Bb", "Eb", "Ab", "Db", "Gb", "Cb"]},
    "Bb minor": {"use_sharps": False, "accidentals": ["Bb", "Eb", "Ab", "Db", "Gb"]},
    "F minor": {"use_sharps": False, "accidentals": ["Bb", "Eb", "Ab", "Db"]},
    "C minor": {"use_sharps": False, "accidentals": ["Bb", "Eb", "Ab"]},
    "G minor": {"use_sharps": False, "accidentals": ["Bb", "Eb"]},
    "D minor": {"use_sharps": False, "accidentals": ["Bb"]}
}

# Ordre des tonalités dans le cycle des quintes
cycle_of_fifths_major = [
    "C", "G", "D", "A", "E", "B", "F#", # Dièses
     "Db", "Ab" , "Eb", "Bb", "F"  # Bémols
]

cycle_of_fifths_minor = [
    "A minor", "E minor", "B minor", "F# minor", "C# minor", "G# minor",  # Dièses
    "Eb minor", "Bb minor", "F minor",  "C minor",  "G minor", "D minor",     # Bémols
]

def get_note_by_interval(root_note, interval, use_sharps=True):
    # Vérifie si la note de départ est enharmonique
    if root_note in enharmonic_notes:
        root_note = enharmonic_notes[root_note]
    
    notes = notes_sharp if use_sharps else notes_flat
    if notes == notes_flat and  "#" in root_note:
        root_note = enharmonic_tunings_notes[root_note]
    if notes == notes_sharp and  "b" in root_note:
        root_note = enharmonic_accidentals_notes[root_note]

    # Trouve l'index de la note de départ
    start_index = notes.index(root_note)
    
    # Calcule l'index de la note résultante
    result_index = (start_index + interval) % len(notes)
    # Retourne la note correspondante
    return notes[result_index]

def get_notes_by_mode(root, mode):
    """
    Génère une liste de notes à partir d'une note de départ et d'un mode musical.
    
    :param root: La note de départ (ex: "C", "D#", "Gb").
    :param mode: Le mode musical (ex: "major", "minor", "dorian", etc.).
    :return: Une liste de notes correspondant au mode.
    """
    if mode not in SCALE_TYPES:
        raise ValueError(f"Mode inconnu : {mode}")
    
    # Vérifie si la note de départ est enharmonique
    if root in enharmonic_notes:
        root = enharmonic_notes[root]
    
    # Détermine si on utilise les dièses ou les bémols
    key_info = get_key_signature(root)
    use_sharps = key_info["use_sharps"]
    
    # Récupère les intervalles du mode
    intervals = SCALE_TYPES[mode]
    
    # Génère la gamme
    notes = generate_scale(root, intervals, use_sharps)
    
    return notes

def generate_scale(start_note, intervals, use_sharps=True):
    """Génère une gamme à partir d'une note de départ et d'un schéma d'intervalles."""
    if start_note in enharmonic_notes:
        start_note = enharmonic_notes[start_note]
    
    notes = notes_sharp if use_sharps else notes_flat
    scale = []

    start_index = notes.index(start_note)
    
    for step in intervals:
        scale.append(notes[start_index % len(notes)])
        start_index += step
    
    return scale

def get_key_signature(tonality):
    """Récupère les informations sur l'armure d'une tonalité."""
    return key_signatures.get(tonality, key_signatures_minor.get(tonality, {"use_sharps": True, "accidentals": []}))

def generate_scales_in_cycle(scale_type, is_minor=False):
    """
    Génère toutes les gammes dans l'ordre du cycle des quintes.
    """
    if scale_type not in SCALE_TYPES:
        raise ValueError(f"Type de gamme inconnu : {scale_type}")
    
    cycle = cycle_of_fifths_minor if is_minor else cycle_of_fifths_major
    all_scales = {}
    
    for tonality in cycle:
        key_info = get_key_signature(tonality)
        use_sharps = key_info["use_sharps"]
        scale = generate_scale(tonality.split()[0], SCALE_TYPES[scale_type], use_sharps)
        all_scales[tonality] = scale
    
    return all_scales


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
        font.setPointSize(NOTE_FONT_SIZE)
        font.setBold(True)
        self.setFont(font)
        self.setZValue(50)
        self.setPos(x - 11, y + 30)

class NoteItem(QGraphicsEllipseItem):
    def __init__(self, x, y, note, is_first_note=False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setRect(QRectF(x - 10 , y + 30, 20, 20))
        self.setBrush(QBrush(QColor(NOTE_COLOR)))

        pen = QPen()
        if is_first_note:
            pen.setWidth(3)
            pen.setColor(QColor(FIRST_NOTE))
        self.setPen(pen)

        text_item = NoteTextItem(x, y, note)
        text_item.setParentItem(self)

class ChordLabelItem(QGraphicsTextItem):
    def __init__(self, x, y, label, *args, **kwargs):
        super().__init__(label, *args, **kwargs)
        self.setDefaultTextColor(QColor("white"))
        font = QFont()
        font.setPointSize(CHORD_LABEL_FONT_SIZE)
        font.setBold(True)
        self.setFont(font)
        self.setZValue(50)
        self.setPos(x, y)

class FretLabelItem(QGraphicsTextItem):
    def __init__(self, x, y, label, *args, **kwargs):
        super().__init__(label, *args, **kwargs)
        self.setDefaultTextColor(QColor("white"))
        font = QFont()
        font.setPointSize(FRET_FONT_SIZE)
        font.setBold(True)
        self.setFont(font)
        self.setZValue(50)
        self.setPos(x - 8, y + 10)

class NeckItem(QGraphicsItem):
    def __init__(self, frets, strings, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.frets = frets
        self.strings = strings

    def boundingRect(self) -> QRectF:
        return QRectF(0, 0, (self.frets + 1) * 50, self.strings * 30)

    def paint(self, painter: QPainter, option, widget=None):
        pen = QPen(QColor(NECK_COLOR))  # Définir la couleur du stylo pour les lignes
        painter.setPen(pen)
        for fret in range(self.frets + 1):
            for string in range(self.strings):
                x = fret * 50
                y = string * 30
                painter.drawRect(x + 25, y + 40, 50, 30)

class GuitarNeck:
    def __init__(self, scene, x_offset, y_offset, num_strings, num_frets, note_pattern=None):
        self.frets = num_frets
        self.strings = num_strings
        # Accordage spécial pour 4 ou 5 cordes
        if num_strings == 5:
            self.string_tunings = STRING_TUNINGS[1:-4] #['B', 'G', 'D', 'A', 'E']
        elif num_strings == 4:
            self.string_tunings = STRING_TUNINGS[2:-4] #['G', 'D', 'A', 'E']
        else:
            self.string_tunings = STRING_TUNINGS[:num_strings]
        self.note_pattern = note_pattern if note_pattern is not None else notes_sharp 
        self.scene = scene
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.chord_type = ""
        self.create_neck()
        self.create_fret_labels()
        #self.create_notes()

    def create_neck(self):
        self.neck_item = NeckItem(self.frets - 1, self.strings - 1)
        self.neck_item.setPos(self.x_offset, self.y_offset)
        self.scene.addItem(self.neck_item)

    def create_fret_labels(self):
        for label in FRET_LABELS:
            if label <= self.frets:
                x = label * 50 + self.x_offset
                y = self.y_offset
                fret_label_item = FretLabelItem(x, y, str(label))
                self.scene.addItem(fret_label_item)

    def create_root_label(self,label_text):
        label_x = self.x_offset - 20  # Adjust as needed
        label_y = self.y_offset - 20  # Adjust as needed
        root_label_item = ChordLabelItem(label_x, label_y, label_text)
        self.scene.addItem(root_label_item)

    def get_note_for_position(self, string, fret, use_sharps):
        root_note = self.string_tunings[string]
        interval = fret
        return get_note_by_interval(root_note, interval, use_sharps)

    def create_notes(self,use_sharps):
        for string in range(self.strings):
            for fret in range(self.frets + 1):
                note = self.get_note_for_position(string, fret,use_sharps)
                is_first_note = (note == self.note_pattern[0])
                if note in self.note_pattern:
                    x = fret * 50 + self.x_offset
                    y = string * 30 + self.y_offset
                    self.add_note_item(x, y, note, is_first_note)

    def add_note_item(self, x, y, note, is_first_note=False):
        note_item = NoteItem(x, y, note, is_first_note)
        self.scene.addItem(note_item)

    def generate_chord_notes(self, root, chord_type):
        chord_notes = []
        # Vérifier si l'accord est mineur et ajuster la tonalité
        if chord_type == "minor":
            key_info = get_key_signature(f"{root} {chord_type}")
        else:
            key_info = get_key_signature(root)
        use_sharps = key_info["use_sharps"]
        for interval in CHORDS_INTERVALS[chord_type]:
            chord_note = get_note_by_interval(root, interval,use_sharps)
            chord_notes.append(chord_note)
        self.note_pattern = chord_notes
        self.create_notes(use_sharps)
        # Create and add the chord label
        label_text = f"{root} {chord_type}"
        self.create_root_label(label_text)

def main():
    app = QApplication(sys.argv)
    
    dark_palette = QPalette()
    dark_palette.setColor(QPalette.Window, Qt.black)  # Fond noir
    dark_palette.setColor(QPalette.WindowText, Qt.white)  # Texte blanc
    dark_palette.setColor(QPalette.Base, Qt.darkGray)  # Fond des widgets
    dark_palette.setColor(QPalette.AlternateBase, Qt.darkGray)
    dark_palette.setColor(QPalette.ToolTipBase, Qt.white)
    dark_palette.setColor(QPalette.ToolTipText, Qt.white)
    dark_palette.setColor(QPalette.Text, Qt.white)
    dark_palette.setColor(QPalette.Button, Qt.darkGray)
    dark_palette.setColor(QPalette.ButtonText, Qt.white)
    dark_palette.setColor(QPalette.Highlight, Qt.blue)
    dark_palette.setColor(QPalette.HighlightedText, Qt.black)
    # Appliquer la palette
    app.setPalette(dark_palette)
    
    Chords_scales = {
        "C Major": [("C", "major"), ("D", "minor"), ("E", "minor"), ("F", "major"),
                    ("G", "major"), ("A", "minor"), ("B", "diminished")],
        "G Major": [("G", "major"), ("A", "minor"), ("B", "minor"), ("C", "major"),
                    ("D", "major"), ("E", "minor"), ("F#", "diminished")],
        "D Major": [("D", "major"), ("E", "minor"), ("F#", "minor"), ("G", "major"),
                    ("A", "major"), ("B", "minor"), ("C#", "diminished")],
        "A Major": [("A", "major"), ("B", "minor"), ("C#", "minor"), ("D", "major"),
                    ("E", "major"), ("F#", "minor"), ("G#", "diminished")],
        "E Major": [("E", "major"), ("F#", "minor"), ("G#", "minor"), ("A", "major"),
                    ("B", "major"), ("C#", "minor"), ("D#", "diminished")],
        "B Major": [("B", "major"), ("C#", "minor"), ("D#", "minor"), ("E", "major"),
                    ("F#", "major"), ("G#", "minor"), ("A#", "diminished")],
        "F# Major": [("F#", "major"), ("G#", "minor"), ("A#", "minor"), ("B", "major"),
                     ("C#", "major"), ("D#", "minor"), ("E#", "diminished")],
        "C# Major": [("C#", "major"), ("D#", "minor"), ("E#", "minor"), ("F#", "major"),
                     ("G#", "major"), ("A#", "minor"), ("B#", "diminished")],
        "Ab Major": [("Ab", "major"), ("Bb", "minor"), ("C", "minor"), ("Db", "major"),
                     ("Eb", "major"), ("F", "minor"), ("G", "diminished")],
        "Eb Major": [("Eb", "major"), ("F", "minor"), ("G", "minor"), ("Ab", "major"),
                     ("Bb", "major"), ("C", "minor"), ("D", "diminished")],
        "Bb Major": [("Bb", "major"), ("C", "minor"), ("D", "minor"), ("Eb", "major"),
                     ("F", "major"), ("G", "minor"), ("A", "diminished")],
        "F Major": [("F", "major"), ("G", "minor"), ("A", "minor"), ("Bb", "major"),
                    ("C", "major"), ("D", "minor"), ("E", "diminished")],
                    

        "A Minor": [("A", "minor"), ("B", "diminished"), ("C", "major"), ("D", "minor"),
                    ("E", "minor"), ("F", "major"), ("G", "major")],
        "E Minor": [("E", "minor"), ("F#", "diminished"), ("G", "major"), ("A", "minor"),
                    ("B", "minor"), ("C", "major"), ("D", "major")],
        "B Minor": [("B", "minor"), ("C#", "diminished"), ("D", "major"), ("E", "minor"),
                    ("F#", "minor"), ("G", "major"), ("A", "major")],
        "F# Minor": [("F#", "minor"), ("G#", "diminished"), ("A", "major"), ("B", "minor"),
                     ("C#", "minor"), ("D", "major"), ("E", "major")],
        "C# Minor": [("C#", "minor"), ("D#", "diminished"), ("E", "major"), ("F#", "minor"),
                     ("G#", "minor"), ("A", "major"), ("B", "major")],
        "G# Minor": [("G#", "minor"), ("A#", "diminished"), ("B", "major"), ("C#", "minor"),
                     ("D#", "minor"), ("E", "major"), ("F#", "major")],
        "D# Minor": [("D#", "minor"), ("E#", "diminished"), ("F#", "major"), ("G#", "minor"),
                     ("A#", "minor"), ("B", "major"), ("C#", "major")],
        "A# Minor": [("A#", "minor"), ("B#", "diminished"), ("C#", "major"), ("D#", "minor"),
                     ("E#", "minor"), ("F#", "major"), ("G#", "major")],
        "F Minor": [("F", "minor"), ("G", "diminished"), ("Ab", "major"), ("Bb", "minor"),
                    ("C", "minor"), ("Db", "major"), ("Eb", "major")],
        "C Minor": [("C", "minor"), ("D", "diminished"), ("Eb", "major"), ("F", "minor"),
                    ("G", "minor"), ("Ab", "major"), ("Bb", "major")],                   
        "G Minor": [("G", "minor"), ("A", "diminished"), ("Bb", "major"), ("C", "minor"),
                    ("D", "minor"), ("Eb", "major"), ("F", "major")],                    
        "D Minor": [("D", "minor"), ("E", "diminished"), ("F", "major"), ("G", "minor"),
                    ("A", "minor"), ("Bb", "major"), ("C", "major")]

}
    scene = QGraphicsScene()
    scene.setSceneRect(-100, -100, 6000, 3000)  # Définir la taille de la scène

    # Ajoute l'image en arrière-plan
    pixmap = QPixmap("guitar.png")  # Remplace par le chemin de ton image
    # Agrandir l'image par 2
    scaled_pixmap = pixmap.scaled(pixmap.width() * 2, pixmap.height() * 2)
    scene.image_item = QGraphicsPixmapItem(scaled_pixmap)
    scene.image_item.setPos(0, 0)  # Positionne l'image
    opacity_effect = QGraphicsOpacityEffect()
    opacity_effect.setOpacity(0.3)  # X% de transparence
    scene.image_item.setGraphicsEffect(opacity_effect)
    scene.addItem(scene.image_item)
    
    # Ajoute le texte
    scene.text_item = QGraphicsTextItem("Visual Practice : ")
    font = QFont("Engraved MT", 18)
    font.setBold(True)
    scene.text_item.setFont(font)
    scene.text_item.setDefaultTextColor(QColor(255, 165, 0))

    # Créer un QComboBox et ajouter les noms des patterns
    combo_box = QComboBox()
    combo_box.setMaxVisibleItems(30)
    # Définir une nouvelle police et l'appliquer au QComboBox
    combo_box.setFont(font)
    combo_box.setPalette(dark_palette)

    # Remplacer la vue interne par un QListView pour accéder aux barres de défilement
    view = QListView()
    combo_box.setView(view)

    # Élargir la scrollbar verticale
    scrollbar = view.verticalScrollBar()
    scrollbar.setFixedWidth(35)  # largeur en px
    scrollbar.setStyleSheet("""
    QScrollBar:vertical {
        background: #333;
        width: 35px;
        margin: 0px;
    }
    QScrollBar::handle:vertical {
        background: #777;
        min-height: 20px;
    }
    """)
    
    # Élargir la liste déroulante
    view.setMinimumWidth(450)  # largeur de la fenêtre déroulante en px
    
    #ajout des éléments
    for mode_name in SCALE_TYPES.keys():
        combo_box.addItem(mode_name)
        
    for chords_name in CHORDS_INTERVALS.keys():
        combo_box.addItem(f"All Chords -{chords_name}")
    
    scale_names = list(Chords_scales.keys())
    for scale in scale_names:
        combo_box.addItem(f"Chords in Scale ({scale})")

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
    proxy.setZValue(100)
    scene.addItem(proxy)
    
    text_item = QGraphicsTextItem("Strings : ")
    text_item.setFont(font)
    text_item.setDefaultTextColor(QColor(255, 165, 0))  # Orange
    text_item.setPos(1080, -50)  # Position du texte
    # Ajout à la scène
    scene.addItem(text_item)
    
    string_combo_box = QComboBox()
    string_combo_box.setFont(font)
    string_combo_box.setPalette(dark_palette)
    for i in range(4, 11):
        string_combo_box.addItem(str(i), i)
    string_combo_box.setCurrentText("7")
    proxy2 = QGraphicsProxyWidget()
    proxy2.setWidget(string_combo_box)
    proxy2.setPos(1200, -50)
    proxy2.setZValue(100)
    scene.addItem(proxy2)

    text_item = QGraphicsTextItem("Columns : ")
    text_item.setFont(font)
    text_item.setDefaultTextColor(QColor(255, 165, 0))  # Orange
    text_item.setPos(1320, -50)  # Position du texte
    # Ajout à la scène
    scene.addItem(text_item)
    
    columns_combo_box = QComboBox()
    columns_combo_box.setFont(font)
    columns_combo_box.setPalette(dark_palette)
    for i in range(2, 7):
        columns_combo_box.addItem(str(i), i)
    columns_combo_box.setCurrentText("3")
    proxy3 = QGraphicsProxyWidget()
    proxy3.setWidget(columns_combo_box)
    proxy3.setPos(1450, -50)
    proxy3.setZValue(100)
    scene.addItem(proxy3)
    
    text_item = QGraphicsTextItem("Frets : ")
    text_item.setFont(font)
    text_item.setDefaultTextColor(QColor(255, 165, 0))  # Orange
    text_item.setPos(1520, -50)  # Position du texte
    # Ajout à la scène
    scene.addItem(text_item)
    
    frets_combo_box = QComboBox()
    frets_combo_box.setFont(font)
    frets_combo_box.setPalette(dark_palette)
    frets_combo_box.setMaxVisibleItems(15)
    for i in range(12, 25):
        frets_combo_box.addItem(str(i), i)
    frets_combo_box.setCurrentText("12")
    proxy4 = QGraphicsProxyWidget()
    proxy4.setWidget(frets_combo_box)
    proxy4.setPos(1620, -50)
    proxy4.setZValue(100)
    scene.addItem(proxy4)
    
    
    def clear_scene():
        for item in scene.items():
            if isinstance(item, (NeckItem, NoteItem, NoteTextItem, FretLabelItem, ChordLabelItem)):
                scene.removeItem(item)

    def update_scene():
        num_strings = string_combo_box.currentData()  # Sélection du nombre de cordes
        num_columns = columns_combo_box.currentData() # Sélection du nombre de colonnes
        num_frets = frets_combo_box.currentData()     # Sélection du nombre de frets
        # Effacer tous les éléments de la scène
        clear_scene()

        # Récupérer le pattern sélectionné
        selected_pattern_name = combo_box.currentText()
    
        # Vérifier si on a sélectionné une gamme diatonique
        if "Chords in Scale" in selected_pattern_name:
            key = selected_pattern_name.split("(")[-1].strip(")")
            if key in Chords_scales:
                scale = Chords_scales[key]
                for i, (root, chord_type) in enumerate(scale):
                    # Calculer les offsets
                    x_offset = (i % num_columns) * 62.5 * num_frets
                    y_offset = (i // num_columns) * 42 * num_strings
                    # Mettre à jour le manche avec les notes de la gamme
                    guitar_neck = GuitarNeck(scene, x_offset, y_offset, num_strings, num_frets)
                    guitar_neck.generate_chord_notes(root,chord_type)

                for i in range(7,12): #keep blank guitar neck
                    x_offset = (i % num_columns) * 62.5 * num_frets
                    y_offset = (i // num_columns) * 42 * num_strings
                    guitar_neck = GuitarNeck(scene, x_offset, y_offset, num_strings, num_frets)
        #---------------------------------------------------------------------------------------
        elif "All Chords -" in selected_pattern_name:
            pattern = selected_pattern_name.split("-")[-1]
            if pattern.__contains__("minor"):
                cycle = cycle_of_fifths_minor 
            else: 
                cycle = cycle_of_fifths_major
            i = 0
            for tonality in cycle:
                x_offset = (i % num_columns) * 62.5 * num_frets
                y_offset = (i // num_columns) * 42 * num_strings
                key_info = get_key_signature(tonality)
                use_sharps = key_info["use_sharps"]
                guitar_neck = GuitarNeck(scene, x_offset, y_offset, num_strings, num_frets)
                guitar_neck.generate_chord_notes(tonality.split()[0],pattern)
                i += 1
        #---------------------------------------------------------------------------------------
        else:
            if selected_pattern_name.__contains__("minor"):
                Scales = generate_scales_in_cycle(selected_pattern_name,is_minor=True)
            else:
                Scales = generate_scales_in_cycle(selected_pattern_name)
            i = 0
            for tonality,scale in Scales.items():
                x_offset = (i % num_columns) * 62.5 * num_frets
                y_offset = (i // num_columns) * 42 * num_strings
                key_info = get_key_signature(tonality)
                use_sharps = key_info["use_sharps"]
                guitar_neck = GuitarNeck(scene, x_offset, y_offset, num_strings, num_frets, scale)
                guitar_neck.create_root_label(f"{tonality.split()[0]} {selected_pattern_name}")
                guitar_neck.create_notes(use_sharps)
                i += 1
        view.resetTransform()
        view.scale(1 / 1.4, 1 / 1.4)
        view.centerOn(0, 0)

    # Connecter le signal currentIndexChanged du QComboBox à la méthode update_scene
    combo_box.currentIndexChanged.connect(update_scene)
    string_combo_box.currentTextChanged.connect(update_scene)
    columns_combo_box.currentTextChanged.connect(update_scene)
    frets_combo_box.currentTextChanged.connect(update_scene)
    view = ZoomableGraphicsView(scene)
    view.scale(1 / 1.4, 1 / 1.4)
    view.centerOn(0, 0)
    # Initialiser la scène avec le premier pattern
    update_scene()
    view.showMaximized()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()