import os
os.environ['ETS_TOOLKIT'] = 'qt4'

from pyface.qt import QtGui, QtCore
from traits.api import HasTraits, Instance, on_trait_change
from traitsui.api import View, Item
from mayavi.core.ui.api import MayaviScene, MlabSceneModel, SceneEditor
from mayavi import mlab
import numpy as np

class Visualization(HasTraits):
    scene = Instance(MlabSceneModel, ())

    @on_trait_change('scene.activated')
    def update_plot(self):
        r = 1
        theta_values = np.array([np.pi / 4, np.pi / 4, 3 * np.pi / 4, 3 * np.pi / 4])
        phi_values = np.array([0, np.pi / 2, np.pi / 2, 0])

        points_r = np.array([r, r, r, r])
        points_theta = theta_values
        points_phi = phi_values

        mlab.clf(figure=self.scene.mayavi_scene)
        mlab.points3d(points_r, points_theta, points_phi, scale_mode='none', scale_factor=0.1)

        for i in range(4):
            lines_r = np.array([points_r[i], points_r[(i + 1) % 4]])
            lines_theta = np.array([points_theta[i], points_theta[(i + 1) % 4]])
            lines_phi = np.array([points_phi[i], points_phi[(i + 1) % 4]])
            mlab.plot3d(lines_r, lines_theta, lines_phi, tube_radius=0.01)

        # Create table widget
        self.table = QtGui.QTableWidget()
        self.table.setColumnCount(3)
        self.table.setRowCount(4)
        self.table.setHorizontalHeaderLabels(['r', 'theta', 'phi'])
        self.table.setVerticalHeaderLabels(['A', 'B', 'C', 'D'])

        # Fill table with data
        for i in range(4):
            self.table.setItem(i, 0, QtGui.QTableWidgetItem(str(points_r[i])))
            self.table.setItem(i, 1, QtGui.QTableWidgetItem(str(points_theta[i])))
            self.table.setItem(i, 2, QtGui.QTableWidgetItem(str(points_phi[i])))

    view = View(Item('scene', editor=SceneEditor(scene_class=MayaviScene),
                     height=250, width=300, show_label=False),
                resizable=True)    

class MayaviQWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        layout = QtGui.QVBoxLayout(self)
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(0)
        self.visualization = Visualization()

        self.ui = self.visualization.edit_traits(parent=self,
                                                 kind='subpanel').control
        layout.addWidget(self.ui)
        layout.addWidget(self.visualization.table) # Add table widget
        self.ui.setParent(self)

if __name__ == "__main__":
    app = QtGui.QApplication.instance()
    if app is None:
        app = QtGui.QApplication([])
    container = QtGui.QWidget()
    container.setWindowTitle("Embedding Mayavi in a PyQt4 Application")
    layout = QtGui.QGridLayout(container)

    mayavi_widget = MayaviQWidget(container)
    layout.addWidget(mayavi_widget, 0, 0, 2, 2)

    table_widget = mayavi_widget.visualization.table # Get the table widget from the MayaviQWidget
    layout.addWidget(table_widget, 2, 0, 1, 2) # Add the table widget to the layout

    container.setLayout(layout)

    main_window = QtGui.QMainWindow()
    main_window.setCentralWidget(container)
    main_window.show()

    app.exec_()