import sys
from pyart.interface.mantidipythonwidget import MantidIPythonWidget  # noqa: F401
import os
from qtpy.QtWidgets import QDialog, QApplication  # type: ignore
from qtpy.uic import loadUi as load_ui  # type: ignore

# from pyvdrive.interface.gui import ui_LaunchManager
import pyart.interface.LiveDataView
# import pyart.interface.PeakPickWindow as PeakPickWindow
# import pyart.interface.ExperimentRecordView as ev

#  Script used to start the VDrive reduction GUI from MantidPlot


class LauncherManager(QDialog):
    """
    Launcher manager
    """
    def __init__(self, load_ui=False):
        """

        """
        super(LauncherManager, self).__init__(None)

        # set up UI: it is tricky
        script_dir = os.path.dirname(__file__)
        dir_names = os.listdir('{}/..'.format(script_dir))
        print(f'dir names: {dir_names}')
        lib_dir = None
        for dir_name in dir_names:
            if dir_name.startswith('lib'):
                lib_dir = dir_name
        if lib_dir is None:
            ui_dir = os.path.join(script_dir, '../pyvdrive/interface/gui')
        else:
            ui_dir = os.path.join(script_dir, '../{}/pyvdrive/interface/gui'.format(lib_dir))
        ui_path = os.path.join(ui_dir, 'LaunchManager.ui')


        if load_ui:
            self.ui = load_ui(ui_path, baseinstance=self)

            # init widgets
            self.ui.checkBox_keepOpen.setChecked(True)

            # define event handlers
            self.ui.pushButton_quit.clicked.connect(self.do_exit)
            self.ui.pushButton_vdrivePlot.clicked.connect(self.do_launch_vdrive)
            self.ui.pushButton_choppingHelper.clicked.connect(self.do_launch_chopper)
            self.ui.pushButton_peakProcessing.clicked.connect(self.do_launch_peak_picker)
            self.ui.pushButton_reducedDataViewer.clicked.connect(self.do_launch_viewer)
            self.ui.pushButton_terminal.clicked.connect(self.do_launch_terminal)

        # initialize main window (may not be shown though)
        # self._mainReducerWindow = VdriveMainWindow()  # the main ui class in this file is called MainWindow

        self._myPeakPickerWindow = None
        self._myLogPickerWindow = None

        return

    def do_exit(self):
        """
        exit the application
        :return:
        """
        self.close()

        return

    def do_launch_chopper(self):
        """
        launch the log picker window
        :return:
        """
        self._mainReducerWindow.do_launch_log_picker_window()

        if not self.ui.checkBox_keepOpen.isChecked():
            self.close()

        return

    def do_launch_live_view(self, auto_start):
        """ launch live view
        :param auto_start: flag to start the live view automatically
        :return:
        """
        live_view = pyart.interface.LiveDataView.VulcanLiveDataView(None, None)

        live_view.show()
        # start live
        live_view.do_start_live()

        return live_view

    def do_launch_peak_picker(self):
        """
        launch peak picker window
        :return:
        """

        self._myPeakPickerWindow = PeakPickWindow.PeakPickerWindow(self._mainReducerWindow,
                                                                   self._mainReducerWindow.get_controller())
        # self._myPeakPickerWindow.set_controller(self._mainReducerWindow.get_controller())
        self._myPeakPickerWindow.show()

        if not self.ui.checkBox_keepOpen.isChecked():
            self.close()

        return

    def do_launch_terminal(self):
        """

        :return:
        """
        self._mainReducerWindow.menu_workspaces_view()

        if not self.ui.checkBox_keepOpen.isChecked():
            self.close()

        return

    def do_launch_vdrive(self):
        """
        launch the main VDrivePlot window
        :return:
        """
        self._mainReducerWindow.show()

        if not self.ui.checkBox_keepOpen.isChecked():
            self.close()

        return

    def do_launch_record_view(self):
        """launch the experimental record viewer
        :return:
        """

        viewer = ev.VulcanExperimentRecordView(self)
        viewer.show()

        return

    def do_launch_viewer(self):
        """
        launch reduced data view
        :return:
        """
        self._mainReducerWindow.do_launch_reduced_data_viewer()

        if not self.ui.checkBox_keepOpen.isChecked():
            self.close()

        return


# END-DEFINITION (class)


# Main application
def lava_app():
    if QApplication.instance():
        _app = QApplication.instance()
    else:
        _app = QApplication(sys.argv)
    return _app


# get arguments
args = sys.argv
if len(args) == 2:
    option = args[1]
else:
    option = '-t'
if isinstance(option, str):
    option = option.lower()
else:
    print('Lava option must be a string.  Execute "lava --help" for help')
    sys.exit(-1)

app = lava_app()

launcher = LauncherManager(False)
# launcher.show()

if option in ['-h', '--help']:
    print('Options:')
    print('  -t: launch IPython terminal')
    print('  -c: launch chopping/slicing interface')
    print('  --view (-v): launch reduced data view interface')
    print('  --peak (-p): launch peak processing interface')
    print('  --main (-m): launch main PyVDrive GUI control panel')
    print('  --live (-l): launch live data view interface in auto mode')
    print('  --live-prof: launch live data view interface in professional mode')
    print('  --record: launch experimental record manager')
    sys.exit(1)

auto_start = False
launcher.do_launch_live_view(auto_start)
launcher.close()


app.exec_()
