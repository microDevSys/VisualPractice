import sys
import os
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *

#Visual Practice rev0.8 © Guillaume Sahuc 2026/01
#https://github.com/microDevSys/VisualPractice
#https://creativecommons.org/licenses/by-nc-nd/4.0/deed.en

#just a tools to practice, if you want to support my work : paypal.me/VisualPractice

# Constants
NOTE_FONT_SIZE = 10
FRET_FONT_SIZE = 10
CHORD_LABEL_FONT_SIZE = 18
#YOU CAN CHOOSE COLOR HERE = http://guillaume.sahuc.free.fr/couleur.html
NECK_COLOR = "#EEDFCC"
NOTE_COLOR = "#FAEBD7"
# Couleurs pour chaque degré (7 couleurs pour les 7 degrés d'une gamme)
DEGREE_COLORS = [
    "#00AAFF",  # 1er degré (tonique) - bleu
    "#8B8B00",  # 2ème degré - or
    "#4DD24D",  # 3ème degré - vert
    "#FFA500",  # 4ème degré - orange
    "#FF0000",  # 5ème degré - rouge
    "#B139ED",  # 6ème degré - violet
    "#A9A0A0"   # 7ème degré - gris
]
FIRST_NOTE= DEGREE_COLORS[0]  # Couleur du 1er degré (tonique)
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
    "major": [0, 4, 7],          # Fondamentale (I), Tierce Majeure (III), Quinte Juste (V)
    "minor": [0, 3, 7],          # Fondamentale (I), Tierce Mineure (bIII), Quinte Juste (V)
    "diminished": [0, 3, 6],     # Fondamentale (I), Tierce Mineure (bIII), Quinte Diminuée (b5)
    "augmented": [0, 4, 8],      # Fondamentale (I), Tierce Majeure (III), Quinte Augmentée (#5)
    "sus2": [0, 2, 7],           # Fondamentale (I), Seconde Majeure (II), Quinte Juste (V)
    "sus4": [0, 5, 7],           # Fondamentale (I), Quarte Juste (IV), Quinte Juste (V)
    "dominant7": [0, 4, 7, 10],  # Fondamentale (I), Tierce Majeure (III), Quinte Juste (V), Septième Mineure (bVII)
    "maj7": [0, 4, 7, 11],       # Fondamentale (I), Tierce Majeure (III), Quinte Juste (V), Septième Majeure (VII)
    "m7": [0, 3, 7, 10],    # Fondamentale (I), Tierce Mineure (bIII), Quinte Juste (V), Septième Mineure (bVII)
    "mMaj7": [0, 3, 7, 11], # Fondamentale (I), Tierce Mineure (bIII), Quinte Juste (V), Septième Majeure (VII)
    "half_dim7": [0, 3, 6, 10],  # Fondamentale (I), Tierce Mineure (bIII), Quinte Diminuée (b5), Septième Mineure (bVII)
    "dim7": [0, 3, 6, 9],        # Fondamentale (I), Tierce Mineure (bIII), Quinte Diminuée (b5), Septième Diminuée (bb7)
    "7sus4": [0, 5, 7, 10]       # Fondamentale (I), Quarte Juste (IV), Quinte Juste (V), Septième Mineure (bVII)
}

# Mapping intervalle chromatique -> index de degré pour la couleur
INTERVAL_TO_DEGREE = {
    0: 0,   # Fondamentale -> I 
    2: 1,   # Seconde Majeure -> II 
    3: 2,   # Tierce Mineure -> bIII 
    4: 2,   # Tierce Majeure -> III 
    5: 3,   # Quarte Juste -> IV 
    6: 4,   # Quinte Diminuée -> b5 
    7: 4,   # Quinte Juste -> V 
    8: 4,   # Quinte Augmentée -> #5 
    9: 6,   # Septième Diminuée -> bb7 
    10: 6,  # Septième Mineure -> bVII 
    11: 6   # Septième Majeure -> VII 
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

def create_styled_combo_box(font, palette, items=None, current_text=None):
    """Helper function to create a styled combo box with common settings."""
    combo = QComboBox()
    combo.setFont(font)
    combo.setPalette(palette)
    if items:
        for item in items:
            if isinstance(item, tuple):
                combo.addItem(str(item[0]), item[1])
            else:
                combo.addItem(item)
    if current_text:
        combo.setCurrentText(current_text)
    return combo

class SpaceComboBox(QComboBox):
    """QComboBox qui avance/recul de façon circulaire avec Haut, Bas ou Espace."""
    def keyPressEvent(self, event):
        count = self.count()
        if not count:
            return

        if event.key() == Qt.Key_Up:
            # recule et boucle au dernier si on est au premier
            self.setCurrentIndex((self.currentIndex() - 1) % count)

        elif event.key() in (Qt.Key_Down, Qt.Key_Space):
            # avance et boucle au premier si on est au dernier
            self.setCurrentIndex((self.currentIndex() + 1) % count)

            # éviter le comportement par défaut sur espace (validation du bouton par ex.)
            if event.key() == Qt.Key_Space:
                return

        else:
            super().keyPressEvent(event)

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
    def __init__(self, x, y, note, is_first_note=False, degree_index=None, show_all_colors=True, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setRect(QRectF(x - 10 , y + 30, 20, 20))
        self.setBrush(QBrush(QColor(NOTE_COLOR)))

        pen = QPen()
        if show_all_colors:
            # Mode toutes les couleurs
            if degree_index is not None and 0 <= degree_index < len(DEGREE_COLORS):
                pen.setWidth(3)
                pen.setColor(QColor(DEGREE_COLORS[degree_index]))
        else:
            # Mode uniquement 1er degré
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
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setRenderHint(QPainter.TextAntialiasing, True)
        painter.setRenderHint(QPainter.SmoothPixmapTransform, True)
        pen = QPen(QColor(NECK_COLOR))  # Définir la couleur du stylo pour les lignes
        pen.setCosmetic(True)  # Épaisseur constante indépendante du zoom
        painter.setPen(pen)
        for fret in range(self.frets + 1):
            for string in range(self.strings):
                x = fret * 50
                y = string * 30
                painter.drawRect(x + 25, y + 40, 50, 30)

class GuitarNeck:
    def __init__(self, scene, x_offset, y_offset, num_strings, num_frets, note_pattern=None, show_all_colors=True):
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
        self.show_all_colors = show_all_colors
        self.note_degrees = {}  # Dictionnaire pour stocker les degrés des notes dans les accords
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
                # Trouver l'index du degré dans le pattern
                degree_index = None
                if note in self.note_pattern:
                    # Si c'est un accord (on a des degrés spécifiques), utiliser le mapping
                    if self.note_degrees:
                        degree_index = self.note_degrees.get(note, None)
                    else:
                        # Sinon, utiliser l'index dans le pattern (gammes)
                        degree_index = self.note_pattern.index(note)
                if note in self.note_pattern:
                    x = fret * 50 + self.x_offset
                    y = string * 30 + self.y_offset
                    self.add_note_item(x, y, note, is_first_note, degree_index)

    def add_note_item(self, x, y, note, is_first_note=False, degree_index=None):
        note_item = NoteItem(x, y, note, is_first_note, degree_index, self.show_all_colors)
        self.scene.addItem(note_item)

    def generate_chord_notes(self, root, chord_type):
        chord_notes = []
        self.note_degrees = {}  # Réinitialiser le dictionnaire des degrés
        # Vérifier si l'accord est mineur et ajuster la tonalité
        if chord_type == "minor":
            key_info = get_key_signature(f"{root} {chord_type}")
        else:
            key_info = get_key_signature(root)
        use_sharps = key_info["use_sharps"]
        for interval in CHORDS_INTERVALS[chord_type]:
            chord_note = get_note_by_interval(root, interval,use_sharps)
            chord_notes.append(chord_note)
            # Mapper la note à son degré pour la couleur
            degree_index = INTERVAL_TO_DEGREE.get(interval, 0)
            self.note_degrees[chord_note] = degree_index
        self.note_pattern = chord_notes
        self.create_notes(use_sharps)
        # Create and add the chord label
        label_text = f"{root} {chord_type}"
        self.create_root_label(label_text)

def main():
    # Optimisation pour High DPI et compatibilité multiplateforme
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    
    app = QApplication(sys.argv)
    
    dark_palette = QPalette()
    dark_palette.setColor(QPalette.Window, Qt.black)  # Fond noir
    dark_palette.setColor(QPalette.WindowText, Qt.white)  # Texte blanc
    dark_palette.setColor(QPalette.Base, Qt.black)  # Fond des widgets
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

    # Ajoute l'image en arrière-plan (avec vérification d'existence)
    image_path = "guitar.png"
    if os.path.exists(image_path):
        pixmap = QPixmap(image_path)
        if not pixmap.isNull():
            # Agrandir l'image par 2
            scaled_pixmap = pixmap.scaled(pixmap.width() * 2, pixmap.height() * 2, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            scene.image_item = QGraphicsPixmapItem(scaled_pixmap)
            scene.image_item.setPos(0, 0)  # Positionne l'image
            opacity_effect = QGraphicsOpacityEffect()
            opacity_effect.setOpacity(0.3)  # X% de transparence
            scene.image_item.setGraphicsEffect(opacity_effect)
            scene.addItem(scene.image_item)
    else:
        scene.image_item = None  # Pas d'image de fond
    
    # Ajoute le texte
    scene.text_item = QGraphicsTextItem("Visual Practice : ")
    font = QFont("Engraved MT", 18)
    font.setBold(True)
    scene.text_item.setFont(font)
    scene.text_item.setDefaultTextColor(QColor(255, 165, 0))

    # Créer un QComboBox et ajouter les noms des patterns
    combo_box = SpaceComboBox()
    combo_box.setMaxVisibleItems(30)
    combo_box.setFont(font)
    combo_box.setPalette(dark_palette)  
    combo_box.setFocusPolicy(Qt.StrongFocus)  # important pour recevoir la barre d’espace


    # Remplacer la vue interne par un QListView pour accéder aux barres de défilement
    view = QListView()
    combo_box.setView(view)

    # Élargir la scrollbar verticale
    scrollbar = view.verticalScrollBar()
    scrollbar.setFixedWidth(35)  # largeur en px
    
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

    # =============================================================================
    # POSITIONS DES ÉLÉMENTS DE L'INTERFACE - Modifier ici pour ajuster la disposition
    # =============================================================================
    pos_visual_practice_x = 300
    pos_visual_practice_y = -50
    
    pos_combo_box_x = 500
    pos_combo_box_y = -50
    
    pos_strings_label_x = 1080
    pos_strings_label_y = -50
    pos_strings_combo_x = 1200
    pos_strings_combo_y = -50
    
    pos_columns_label_x = 1320
    pos_columns_label_y = -50
    pos_columns_combo_x = 1450
    pos_columns_combo_y = -50
    
    pos_frets_label_x = 1520
    pos_frets_label_y = -50
    pos_frets_combo_x = 1620
    pos_frets_combo_y = -50
    
    pos_legend_title_x = 0
    pos_legend_title_y = -100
    pos_legend_start_x = 300
    pos_legend_start_y = -90
    pos_legend_spacing = 70
    
    pos_checkbox_x = 0
    pos_checkbox_y = -50
    # =============================================================================

    # Positionne le texte centré en haut
    scene.text_item.setPos(pos_visual_practice_x, pos_visual_practice_y)
    scene.addItem(scene.text_item)
    
    # Intégrer le QComboBox dans la scène en utilisant un QGraphicsProxyWidget
    proxy = QGraphicsProxyWidget()
    proxy.setWidget(combo_box)
    proxy.setPos(pos_combo_box_x, pos_combo_box_y)
    proxy.setZValue(100)
    scene.addItem(proxy)
    
    text_strings = QGraphicsTextItem("Strings : ")
    text_strings.setFont(font)
    text_strings.setDefaultTextColor(QColor(255, 165, 0))
    text_strings.setPos(pos_strings_label_x, pos_strings_label_y)
    scene.addItem(text_strings)
    
    string_combo_box = create_styled_combo_box(font, dark_palette, [(i, i) for i in range(4, 11)], "7")
    proxy2 = QGraphicsProxyWidget()
    proxy2.setWidget(string_combo_box)
    proxy2.setPos(pos_strings_combo_x, pos_strings_combo_y)
    proxy2.setZValue(100)
    scene.addItem(proxy2)

    text_columns = QGraphicsTextItem("Columns : ")
    text_columns.setFont(font)
    text_columns.setDefaultTextColor(QColor(255, 165, 0))
    text_columns.setPos(pos_columns_label_x, pos_columns_label_y)
    scene.addItem(text_columns)
    
    columns_combo_box = create_styled_combo_box(font, dark_palette, [(i, i) for i in range(2, 7)], "3")
    proxy3 = QGraphicsProxyWidget()
    proxy3.setWidget(columns_combo_box)
    proxy3.setPos(pos_columns_combo_x, pos_columns_combo_y)
    proxy3.setZValue(100)
    scene.addItem(proxy3)
    
    text_frets = QGraphicsTextItem("Frets : ")
    text_frets.setFont(font)
    text_frets.setDefaultTextColor(QColor(255, 165, 0))
    text_frets.setPos(pos_frets_label_x, pos_frets_label_y)
    scene.addItem(text_frets)
    
    frets_combo_box = create_styled_combo_box(font, dark_palette, [(i, i) for i in range(12, 25)], "12")
    frets_combo_box.setMaxVisibleItems(15)
    proxy4 = QGraphicsProxyWidget()
    proxy4.setWidget(frets_combo_box)
    proxy4.setPos(pos_frets_combo_x, pos_frets_combo_y)
    proxy4.setZValue(100)
    scene.addItem(proxy4)
    
    # Légende des degrés
    legend_title = QGraphicsTextItem("Degrees Legend:")
    legend_title.setFont(font)
    legend_title.setDefaultTextColor(QColor(255, 165, 0))
    legend_title.setPos(pos_legend_title_x, pos_legend_title_y)
    scene.addItem(legend_title)
    
    degree_names = ["I", "II", "III", "IV", "V", "VI", "VII"]
    for i in range(7):
        # Créer un cercle coloré pour chaque degré
        degree_circle = QGraphicsEllipseItem(0, 0, 20, 20)
        degree_circle.setBrush(QBrush(QColor(NOTE_COLOR)))
        degree_pen = QPen()
        degree_pen.setWidth(3)
        degree_pen.setColor(QColor(DEGREE_COLORS[i]))
        degree_circle.setPen(degree_pen)
        degree_circle.setPos(pos_legend_start_x + (i * pos_legend_spacing), pos_legend_start_y)
        scene.addItem(degree_circle)
        
        # Ajouter le texte du degré
        degree_text = QGraphicsTextItem(degree_names[i])
        degree_font = QFont("Courier New")
        degree_font.setPointSize(NOTE_FONT_SIZE)
        degree_font.setBold(True)
        degree_text.setFont(degree_font)
        degree_text.setDefaultTextColor(QColor(255, 165, 0))
        degree_text.setPos(pos_legend_start_x + 20 + (i * pos_legend_spacing), pos_legend_start_y + 5)
        scene.addItem(degree_text)
    
    # Checkbox pour activer/désactiver toutes les couleurs
    color_checkbox = QCheckBox("All Degrees Colors")
    color_checkbox.setChecked(False)
    color_checkbox.setFont(font)
    checkbox_palette = QPalette()
    checkbox_palette.setColor(QPalette.WindowText, QColor(255, 165, 0))
    color_checkbox.setPalette(checkbox_palette)
    proxy_checkbox = QGraphicsProxyWidget()
    proxy_checkbox.setWidget(color_checkbox)
    proxy_checkbox.setPos(pos_checkbox_x, pos_checkbox_y)
    proxy_checkbox.setZValue(100)
    scene.addItem(proxy_checkbox)
    
    
    def clear_scene():
        # More efficient: filter and remove in one pass
        for item in [i for i in scene.items() if isinstance(i, (NeckItem, NoteItem, NoteTextItem, FretLabelItem, ChordLabelItem))]:
            scene.removeItem(item)

    def update_scene():
        num_strings = string_combo_box.currentData()
        num_columns = columns_combo_box.currentData()
        num_frets = frets_combo_box.currentData()
        show_all_colors = color_checkbox.isChecked()
        
        # Cache frequently used multipliers
        x_multiplier = 62.5 * num_frets
        y_multiplier = 42 * num_strings
        
        clear_scene()
        selected_pattern_name = combo_box.currentText()
    
        # Vérifier si on a sélectionné une gamme diatonique
        if "Chords in Scale" in selected_pattern_name:
            key = selected_pattern_name.split("(")[-1].strip(")")
            if key in Chords_scales:
                scale = Chords_scales[key]
                for i, (root, chord_type) in enumerate(scale):
                    x_offset = (i % num_columns) * x_multiplier
                    y_offset = (i // num_columns) * y_multiplier
                    guitar_neck = GuitarNeck(scene, x_offset, y_offset, num_strings, num_frets, show_all_colors=show_all_colors)
                    guitar_neck.generate_chord_notes(root, chord_type)

                for i in range(7, 12):  # keep blank guitar neck
                    x_offset = (i % num_columns) * x_multiplier
                    y_offset = (i // num_columns) * y_multiplier
                    guitar_neck = GuitarNeck(scene, x_offset, y_offset, num_strings, num_frets, show_all_colors=show_all_colors)
        #---------------------------------------------------------------------------------------
        elif "All Chords -" in selected_pattern_name:
            pattern = selected_pattern_name.split("-")[-1]
            cycle = cycle_of_fifths_minor if "minor" in pattern else cycle_of_fifths_major
            for i, tonality in enumerate(cycle):
                x_offset = (i % num_columns) * x_multiplier
                y_offset = (i // num_columns) * y_multiplier
                guitar_neck = GuitarNeck(scene, x_offset, y_offset, num_strings, num_frets, show_all_colors=show_all_colors)
                guitar_neck.generate_chord_notes(tonality.split()[0], pattern)
        #---------------------------------------------------------------------------------------
        else:
            Scales = generate_scales_in_cycle(selected_pattern_name, is_minor="minor" in selected_pattern_name)
            for i, (tonality, scale) in enumerate(Scales.items()):
                x_offset = (i % num_columns) * x_multiplier
                y_offset = (i // num_columns) * y_multiplier
                key_info = get_key_signature(tonality)
                use_sharps = key_info["use_sharps"]
                guitar_neck = GuitarNeck(scene, x_offset, y_offset, num_strings, num_frets, scale, show_all_colors=show_all_colors)
                guitar_neck.create_root_label(f"{tonality.split()[0]} {selected_pattern_name}")
                guitar_neck.create_notes(use_sharps)
        view.resetTransform()
        view.scale(1 / 1.4, 1 / 1.4)
        view.centerOn(0, 0)
        combo_box.setFocus()

    # Connecter le signal currentIndexChanged du QComboBox à la méthode update_scene
    combo_box.currentIndexChanged.connect(update_scene)
    string_combo_box.currentTextChanged.connect(update_scene)
    columns_combo_box.currentTextChanged.connect(update_scene)
    frets_combo_box.currentTextChanged.connect(update_scene)
    color_checkbox.stateChanged.connect(update_scene)
    view = ZoomableGraphicsView(scene)
    view.scale(1 / 1.4, 1 / 1.4)
    view.centerOn(0, 0)
    # Initialiser la scène avec le premier pattern
    update_scene()
    view.showMaximized()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()