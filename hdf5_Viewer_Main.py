import napari
import h5py
import numpy as np
from tkinter import Tk
from tkinter import filedialog
from PyQt5.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QLineEdit

#----------------------------------------
# Napari Program to open and save hdf5 files
#----------------------------------------

viewer = napari.Viewer()

def hdf5_to_viewer(viewer):

    root = Tk()
    root.withdraw()

    path = filedialog.askopenfilename()

    f = h5py.File(path, "r")
              
    f_content = list(f.keys()) # content (first group) of file

    for content in f_content:

        if content == "Data":

            for img in f[content]:

                f_data = f[content][img]

                if np.sum(f_data) != 0:

                    viewer.add_image(f_data, name=img, colormap="viridis")
        
        elif content != "Data" and content != "Stats":

            f_data = f[content]
            
            viewer.add_image(f_data, name=content, colormap="viridis")
        
def save_all_imgs(viewer, name):

    root = Tk()
    root.withdraw()

    path = filedialog.askdirectory()

    hf_name = path + "/" + name + ".h5"

    hf = h5py.File(hf_name, "w")

    layer_list = viewer.layers

    for layer in layer_list:

        layer_name = layer.name

        hf.create_dataset(layer_name, data=layer.data)

    hf.close()

class H5ViewerWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Hdf5 Viewer Widget")
        
        layout = QVBoxLayout()
        label = QLabel("hdf5 Napari Viewer")
        open_button = QPushButton("Open File")
        text_box = QLineEdit("File_Name")
        save_button = QPushButton("Save to hdf5")

        widgets = [label, 
                   open_button,
                   text_box,
                   save_button]
        
        for w in widgets:
            layout.addWidget(w)
            
        widget = QWidget()
        widget.setLayout(layout)

        self.setCentralWidget(widget)
        
        open_button.clicked.connect(lambda: hdf5_to_viewer(viewer))
        save_button.clicked.connect(lambda: save_all_imgs(viewer=viewer, name=text_box.text()))

widget = H5ViewerWidget()

viewer.window.add_dock_widget(widget)

napari.run()

print("FINISHED")