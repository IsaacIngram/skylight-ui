from PyQt6 import uic

from PyQt6.QtWidgets import QWidget, QApplication
from switch_widget import SwitchWidget, Position
from svg_button_widget import SvgButtonWidget
from svg_slider import SvgSlider
from dim_screen import DimScreen
from settings_screen import SettingsScreen
import model

class ControlWidget(QWidget):

    skylight_obj: model.Skylight
    dim_screen: DimScreen
    settings_screen: SettingsScreen
    blackout_switch_widget: SwitchWidget
    filter_switch_widget: SwitchWidget
    blackout_slider: SvgSlider
    filter_slider: SvgSlider

    def __init__(self, skylight_obj: model.Skylight, dim_screen: DimScreen, settings_screen: SettingsScreen, *args, **kwargs):
        """
        Create a new control widget

        Params:
        skylight_obj (Skylight): Skylight object
        dim_screen (DimScreen): Dim screen
        settings_screen (SettingsScreen): Settings screen
        """
        super().__init__(*args, **kwargs)

        # Load ui
        uic.loadUi('control_widget.ui', self)
        
        # Set local variables
        self.skylight_obj = skylight_obj
        self.dim_screen = dim_screen
        self.settings_screen = settings_screen

        # Create switches
        self.blackout_switch_widget = SwitchWidget(Position.CLOSED, self.blackoutSwitch, self)
        self.filter_switch_widget = SwitchWidget(Position.CLOSED, self.filterSwitch, self)
        self.blackout_switch_widget.clicked.connect(self.blackout_switch_callback)
        self.filter_switch_widget.clicked.connect(self.filter_switch_callback)

        # Create buttons
        self.dim_button = SvgButtonWidget('images/dim-icon.svg', self.dimButton, 50, 50, self)
        self.settings_button = SvgButtonWidget('images/settings-icon.svg', self.settingsButton, 100, 100, self)
        self.dim_button.clicked.connect(self.dim_screen_callback)
        self.settings_button.clicked.connect(self.settings_screen_callback)

        # Create sliders
        self.blackout_slider = SvgSlider(self.blackoutSlider, value_update_callback=self.blackout_slider_callback, parent=self)
        self.filter_slider = SvgSlider(self.filterSlider, value_update_callback=self.filter_slider_callback, parent=self)

        # Hide connection indicator
        self.connectionIndicator.hide()

        self.show()

    def blackout_switch_callback(self):
        """
        Callback function for when the blackout switch is clicked
        """
        if self.blackout_switch_widget.checkbox.isChecked():
            # Uncheck
            self.blackout_switch_widget.checkbox.setChecked(False)
            self.blackout_slider.set_value(0)
        else:
            # Check
            self.blackout_switch_widget.checkbox.setChecked(True)
            self.blackout_slider.set_value(100)


    def filter_switch_callback(self):
        """
        Callback function for when the filter switch is clicked
        """
        if self.filter_switch_widget.checkbox.isChecked():
            # Uncheck
            self.filter_switch_widget.checkbox.setChecked(False)
            self.filter_slider.set_value(0)
        else:
            # Check
            self.filter_switch_widget.checkbox.setChecked(True)
            self.filter_slider.set_value(100)


    def dim_screen_callback(self):
        self.dim_screen.set_screen_dim()

    def show_connection_indicator(self):
        """
        Show the not connected indicator
        """
        self.connectionIndicator.show()

    def hide_connection_indicator(self):
        """
        Hide the not connected indicator
        """
        self.connectionIndicator.hide()

    def settings_screen_callback(self):
        self.settings_screen.switch_to()

    def blackout_slider_callback(self, new_value: int):
        """
        Callback function for when the slider value is updated
        """
        if new_value == 0:
            self.blackout_switch_widget.set_closed()
        elif new_value == 100:
            self.blackout_switch_widget.set_open()
        else:
            self.blackout_switch_widget.disable()

    def filter_slider_callback(self, new_value: int):
        """
        Callback function for when the slider value is updated
        """
        if new_value == 0:
            self.filter_switch_widget.set_closed()
        elif new_value == 100:
            self.filter_switch_widget.set_open()
        else:
            self.filter_switch_widget.disable()

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    w = ControlWidget(0)
    w.show()
    sys.exit(app.exec())