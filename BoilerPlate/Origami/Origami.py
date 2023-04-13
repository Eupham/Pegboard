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
        # Define the square in spherical coordinates
        r = 1
        theta_values = np.array([np.pi / 4, np.pi / 4, 3 * np.pi / 4, 3 * np.pi / 4])
        phi_values = np.array([0, np.pi / 2, np.pi / 2, 0])

        points_r = np.array([r, r, r, r])
        points_theta = theta_values
        points_phi = phi_values

        # Clear the existing plot and replot the square and the points
        mlab.clf(figure=self.scene.mayavi_scene)

        # Plot the square
        square_r = np.array([r, r, r, r, r])
        square_theta = np.array([np.pi / 4, 3 * np.pi / 4, 3 * np.pi / 4, np.pi / 4, np.pi / 4])
        square_phi = np.array([0, 0, np.pi / 2, np.pi / 2, 0])
        mlab.plot3d(square_r, square_theta, square_phi, tube_radius=0.01)

        # Plot the points
        mlab.points3d(points_r, points_theta, points_phi, scale_mode='none', scale_factor=0.1)
        
        # Add an event listener for mouse clicks on the Mayavi scene
        picker = self.scene.mayavi_scene.on_mouse_pick(self.handle_pick)

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

    def handle_pick(self, picker):
        # Get the coordinates of the picked point in spherical coordinates
        r, theta, phi = picker.pick_position

        # Define the four corners of the square in spherical coordinates
        r0 = 1
        theta_values = np.array([np.pi / 4, np.pi / 4, 3 * np.pi / 4, 3 * np.pi / 4])
        phi_values = np.array([0, np.pi / 2, np.pi / 2, 0])

        # Check if the point is inside the four corners of the square
        if phi >= phi_values.min() and phi <= phi_values.max() and theta >= theta_values.min() and theta <= theta_values.max():
            # Project the point onto the slope defined by the four corners
            A = np.vstack([np.ones(3), np.cos(np.pi/4)*np.array([1,1,0]), np.array([0,np.sin(np.pi/4),np.sin(np.pi/4)])])
            b = np.array([r0, r0*np.cos(theta), r0*np.sin(theta)*np.sin(phi)])
            x_hat = np.linalg.solve(A, b)
            r_new = np.linalg.norm(x_hat)
            theta_new = np.arccos(x_hat[1] / r_new)
            phi_new = np.arcsin(x_hat[2] / r_new / np.sin(theta_new))

            # Add the picked point to the plot
            mlab.points3d(r_new, theta_new, phi_new, color=(1, 0, 0), scale_factor=0.1)


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
