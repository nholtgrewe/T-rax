import sys
import os
from wx.lib.pubsub import Publisher as pub
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import SIGNAL
import numpy as np

from views.T_Rax_MainView import TRaxMainView
from T_Rax_QTROISelectorController import TRaxROIController
from T_Rax_QTROISelectorSingleController import TRaxROIControllerSingle
from convert_ui_files import convert_ui_files
from T_Rax_Data import TraxData
from T_Rax_RubyData import TraxRubyData
from epics import caput, PV



class TRaxMainController(object):
    def __init__(self):
        self.main_view = TRaxMainView()
        
        self.create_signals()
        self.create_sub_controller()
        self.load_parameter()
        self.temperature_btn_click()
        self.main_view.show()

    def create_sub_controller(self):
        self.temperature_controller = TRaxTemperatureController(self,self.main_view)
        self.ruby_controller = TRaxRubyController(self, self.main_view)
        
    def load_parameter(self):
       try:
            fid = open('parameters.txt', 'r')
            self.temperature_controller._exp_working_dir = ':'.join(fid.readline().split(':')[1::])[1:-1]
            self.temperature_controller._calib_working_dir = ':'.join(fid.readline().split(':')[1::])[1:-1]
            self.ruby_controller._exp_working_dir = ':'.join(fid.readline().split(':')[1::])[1:-1]
            fid.close()
       except IOError:
            self.temperature_controller._exp_working_dir = os.getcwd()
            self.temperature_controller._calib_working_dir = os.getcwd(),
            self.ruby_controller._exp_working_dir = os.getcwd()

    def create_signals(self):
        self.create_navigation_signals()
        self.create_axes_listener()
        self.create_error_listener()
        self.main_view.closeEvent = self.closeEvent  

    def create_navigation_signals(self):
        self.main_view.connect(self.main_view.ruby_btn, SIGNAL('clicked()'), self.ruby_btn_click)
        self.main_view.connect(self.main_view.raman_btn, SIGNAL('clicked()'), self.raman_btn_click)
        self.main_view.connect(self.main_view.diamond_btn, SIGNAL('clicked()'), self.diamond_btn_click)
        self.main_view.connect(self.main_view.temperature_btn, SIGNAL('clicked()'), self.temperature_btn_click)
        self.main_view.main_frame.resizeEvent = self.main_view.resize_graphs

    def create_axes_listener(self):
        self.main_view.graph_1axes.canvas.mpl_connect('motion_notify_event', self.on_mouse_move_in_graph)
        self.main_view.temperature_control_graph.canvas.mpl_connect('motion_notify_event', self.on_mouse_move_in_graph)

    def create_error_listener(self):
        pub.subscribe(self.interpolation_error, "INTERPOLATION RANGE ERROR")

    def connect_click_function(self, emitter, function):
        self.main_view.connect(emitter, SIGNAL('clicked()'), function)

    def temperature_btn_click(self):
        self.main_view.navigate_to('temperature_btn')
        self.mode = "temperature"

    def ruby_btn_click(self):
        self.main_view.navigate_to('ruby_btn')
        self.mode = "ruby"

    def diamond_btn_click(self):
        self.main_view.navigate_to('diamond_btn')
        self.mode = "diamond"

    def raman_btn_click(self):
        self.main_view.update_navigation_bar('rgba(21, 134, 31, 255)', 'raman_btn')
        self.main_view.hide_control_widgets()

    def on_mouse_move_in_graph(self, event):
        x_coord, y_coord = event.xdata, event.ydata
        if x_coord <> None:
           self.main_view.status_coord_lbl.setText('x: %(x).3F y: %(y).3F' \
                              % {'x':x_coord, 'y':y_coord})
        else:
           self.main_view.status_coord_lbl.setText('')


    def interpolation_error(self, event):
        error_message=QtGui.QMessageBox.warning(None, 'Interpolation Error',
                                                'Etalon spectrum file has not the right range. Please select either standard temperature or load another etalon file.',
                                                QtGui.QMessageBox.Ok, QtGui.QMessageBox.NoButton)

    def save_directories(self):
        fid = open('parameters.txt', 'w')
        output_str = \
            'Temperature Working directory: ' + self.temperature_controller._exp_working_dir + '\n' + \
            'Temperature Calibration directory: ' + self.temperature_controller._calib_working_dir +'\n'+\
            'Ruby Working directory: ' + self.ruby_controller._exp_working_dir
        fid.write(output_str)
        fid.close()

    def closeEvent(self, event):
        self.save_directories()
        try:
            self.temperature_controller.roi_controller.view.close()
        except:
            pass
        try:
            self.ruby_controller.roi_controller.view.close()
        except:
            pass
        self.main_view.close()
        event.accept()
'''

********************************************************************************************************
'''     

class TRaxTemperatureController():
    def __init__(self, parent, main_view):
        self.parent = parent
        self.data = TraxData()
        self.main_view = main_view
        self.create_signals()
        self.load_exp_data('D:\Programming\VS Projects\T-Rax\T-Rax\sample files\IR files\lamp_6p5A.SPE')
        
        pub.sendMessage("EXP DATA CHANGED", self)
        pub.sendMessage("ROI CHANGED")

    def create_signals(self):
        self.create_exp_file_signals()
        self.create_roi_view_signals()

        self.create_temperature_pub_listeners()
        self.create_calibration_signals()
        self.create_temperature_control_signals()
        self.create_auto_process_signal()

        self.main_view.temperature_control_widget.epics_connection_cb.clicked.connect(self.epics_connection_cb_clicked)
        self.epics_is_connected=False

    def create_temperature_pub_listeners(self):
        pub.subscribe(self.data_changed, "EXP DATA CHANGED")
        pub.subscribe(self.roi_changed, "ROI CHANGED")
    
    def create_calibration_signals(self):
        self.connect_click_function(self.main_view.temperature_control_widget.load_ds_calib_data_btn,
                                    self.load_ds_calib_data)
        self.connect_click_function(self.main_view.temperature_control_widget.load_us_calib_data_btn,
                                    self.load_us_calib_data)
        self.main_view.temperature_control_widget.ds_temperature_rb.toggled.connect(self.ds_temperature_rb_clicked)
        self.main_view.temperature_control_widget.us_temperature_rb.toggled.connect(self.us_temperature_rb_clicked)
        self.main_view.temperature_control_widget.ds_etalon_rb.toggled.connect(self.ds_etalon_rb_clicked)
        self.main_view.temperature_control_widget.us_etalon_rb.toggled.connect(self.us_etalon_rb_clicked)
        self.connect_click_function(self.main_view.temperature_control_widget.ds_etalon_btn,self.ds_etalon_btn_clicked)
        self.connect_click_function(self.main_view.temperature_control_widget.us_etalon_btn,self.us_etalon_btn_clicked)
        self.main_view.temperature_control_widget.ds_temperature_txt.editingFinished.connect(self.ds_temperature_changed)
        self.main_view.temperature_control_widget.us_temperature_txt.editingFinished.connect(self.us_temperature_changed)

    def create_temperature_control_signals(self):
        self.main_view.temperature_control_widget.fit_from_txt.editingFinished.connect(self.fit_txt_changed)
        self.main_view.temperature_control_widget.fit_to_txt.editingFinished.connect(self.fit_txt_changed)

    def create_auto_process_signal(self):
        self.main_view.temperature_control_widget.auto_process_cb.clicked.connect(self.auto_process_cb_click)
        self.autoprocess_timer = QtCore.QTimer(self.main_view)
        self.autoprocess_timer.setInterval(100)
        self.main_view.connect(self.autoprocess_timer,QtCore.SIGNAL('timeout()'), self.check_files)
    
    def create_exp_file_signals(self):
        self.connect_click_function(self.main_view.temperature_control_widget.load_exp_data_btn, self.load_exp_data)        
        self.connect_click_function(self.main_view.temperature_control_widget.load_next_exp_data_btn, self.load_next_exp_data)        
        self.connect_click_function(self.main_view.temperature_control_widget.load_previous_exp_data_btn, self.load_previous_exp_data)

    def create_roi_view_signals(self):
        self.connect_click_function(self.main_view.temperature_control_widget.roi_setup_btn, self.load_roi_view)
    
    def connect_click_function(self, emitter, function):
        self.main_view.connect(emitter, SIGNAL('clicked()'), function)

    def load_exp_data(self, filename=None):
        if filename is None:
            filename = str(QtGui.QFileDialog.getOpenFileName(self.main_view, caption="Load Experiment SPE", 
                                          directory = self._exp_working_dir))

        if filename is not '':
            self._exp_working_dir = '/'.join(str(filename).replace('\\','/').split('/')[0:-1])+'/'
            self._files_before = dict([(f, None) for f in os.listdir(self._exp_working_dir)]) #reset for the autoprocessing
            self.data.load_exp_data(filename)

    def load_next_exp_data(self):
        self.data.load_next_exp_file()

    def load_previous_exp_data(self):
        self.data.load_previous_exp_file()

    def load_roi_view(self):
        try:
            self.roi_controller.show()
        except AttributeError:
            self.roi_controller = TRaxROIController(self.data, parent=self.main_view)
            self.roi_controller.show()

    def data_changed(self, event):
        self.main_view.temperature_control_graph.update_graph(self.data.get_ds_spectrum(), self.data.get_us_spectrum(),
                                                self.data.get_ds_roi_max(), self.data.get_us_roi_max(),
                                                self.data.get_ds_calib_file_name(), self.data.get_us_calib_file_name())
        self.main_view.set_temperature_filename(self.data.get_exp_file_name().replace('\\','/').split('/')[-1])
        print self.data.get_exp_file_name()
        self.main_view.set_temperature_foldername('/'.join(self.data.get_exp_file_name().replace('\\','/').split('/')[-3:-1]))
        self.main_view.set_calib_filenames(self.data.get_ds_calib_file_name().replace('\\','/').split('/')[-1],
                                           self.data.get_us_calib_file_name().replace('\\','/').split('/')[-1])
        self.main_view.temperature_control_widget.ds_etalon_lbl.setText(self.data.get_ds_calib_etalon_file_name().replace('\\','/').split('/')[-1])
        self.main_view.temperature_control_widget.us_etalon_lbl.setText(self.data.get_us_calib_etalon_file_name().replace('\\','/').split('/')[-1])
        self.main_view.set_fit_limits(self.data.get_x_roi_limits())
        self.update_pv_names()

    def roi_changed(self, event):
        self.data.calc_spectra()
        self.main_view.temperature_control_graph.update_graph(self.data.get_ds_spectrum(), self.data.get_us_spectrum(),
                                                self.data.get_ds_roi_max(), self.data.get_us_roi_max(),
                                                self.data.get_ds_calib_file_name(), self.data.get_us_calib_file_name())
        self.main_view.set_fit_limits(self.data.get_x_roi_limits())
        self.update_pv_names()

    def update_pv_names(self):
        if self.epics_is_connected:
            #self.pv_us_temperature.put(self.data.get_us_temp())
            #self.pv_ds_temperature.put(self.data.get_ds_temp())
            #self.pv_us_int.put(self.data.get_us_roi_max())
            #self.pv_ds_int.put(self.data.get_ds_roi_max())
            caput('13IDD:us_las_temp.VAL', self.data.get_us_temp())
            caput('13IDD:ds_las_temp.VAL', self.data.get_ds_temp())

            caput('13IDD:up_t_int', str(self.data.get_us_roi_max()))
            caput('13IDD:dn_t_int', str(self.data.get_ds_roi_max()))
    
    def load_ds_calib_data(self, filename=None):
        if filename is None:
            filename = str(QtGui.QFileDialog.getOpenFileName(self.main_view, caption="Load Downstream calibration SPE", 
                                          directory = self._calib_working_dir))
        
        if filename is not '':
            self._calib_working_dir = '/'.join(str(filename).replace('\\','/').split('/')[0:-1]) + '/'
            self.data.load_ds_calib_data(filename)

    def load_us_calib_data(self, filename=None):
        if filename is None:
            filename = str(QtGui.QFileDialog.getOpenFileName(self.main_view, caption="Load Upstream calibration SPE", 
                                          directory = self._calib_working_dir))
        
        if filename is not '':
            self._calib_working_dir = '/'.join(str(filename).replace('\\','/').split('/')[0:-1]) + '/'
            self.data.load_us_calib_data(filename)

    def ds_temperature_rb_clicked(self):
        self.data.set_ds_calib_modus(0)

    def us_temperature_rb_clicked(self):
        self.data.set_us_calib_modus(0)

    def ds_etalon_rb_clicked(self):
        self.data.set_ds_calib_modus(1)
    
    def us_etalon_rb_clicked(self):
        self.data.set_us_calib_modus(1)

    def ds_etalon_btn_clicked(self, filename=None):
        if filename is None:
            filename = str(QtGui.QFileDialog.getOpenFileName(self.main_view, caption="Load Downstream Etalaon Spectrum", 
                                          directory = self._calib_working_dir))
        
        if filename is not '':
            self.data.load_ds_calib_etalon(filename)

    def us_etalon_btn_clicked(self, filename=None):
        if filename is None:
            filename = str(QtGui.QFileDialog.getOpenFileName(self.main_view, caption="Load Upstream Etalaon Spectrum", 
                                          directory = self._calib_working_dir))
        
        if filename is not '':
            self.data.load_us_calib_etalon(filename)

    def ds_temperature_changed(self):
        self.data.set_ds_calib_temp(np.double(self.main_view.temperature_control_widget.ds_temperature_txt.text()))
    
    def us_temperature_changed(self):
        self.data.set_us_calib_temp(np.double(self.main_view.temperature_control_widget.us_temperature_txt.text()))
    
    def fit_txt_changed(self):
        limits = self.main_view.temperature_control_widget.get_fit_limits()
        self.data.set_x_roi_limits_to(limits)

    
    def auto_process_cb_click(self):
        if self.main_view.temperature_control_widget.auto_process_cb.isChecked():
            self._files_before = dict([(f, None) for f in os.listdir(self._exp_working_dir)])
            self.autoprocess_timer.start()
        else:
            self.autoprocess_timer.stop()

    def check_files(self):
        print self._exp_working_dir
        self._files_now = dict([(f,None) for f in os.listdir(self._exp_working_dir)])
        self._files_added = [f for f in self._files_now if not f in self._files_before]
        self._files_removed = [f for f in self._files_before if not f in self._files_now]
        if len(self._files_added) > 0:
            new_file_str = self._files_added[-1]
            if self.file_is_spe(new_file_str) and not self.file_is_raw(new_file_str):
                path = self._exp_working_dir + '\\' + new_file_str
                self.data.load_exp_data(path)
            self._files_before = self._files_now
            
    def file_is_spe(self, filename):
        return filename.endswith('.SPE') or filename.endswith('.spe')
    
    def file_is_raw(self, filename):
        try:
            #checks if file contains "-raw" string at the end
            return filename.split('-')[-1].split('.')[0] == 'raw'
        except:
            return false        
        
    def epics_connection_cb_clicked(self):
        if self.main_view.temperature_control_widget.epics_connection_cb.isChecked():
            self.pv_us_temperature=PV('13IDD:us_las_temp.VAL')
            self.pv_ds_temperature=PV('13IDD:ds_las_temp.VAL')
            self.pv_us_int = PV('13IDD:up_t_int')
            self.pv_ds_int = PV('13IDD:dn_t_int')
            self.epics_is_connected=True
            self.update_pv_names()
        else:
            self.epics_is_connected=False

class TRaxRubyController():
    def __init__(self, parent, main_view):
        self.parent = parent
        self.data = TraxRubyData()
        
        self.main_view = main_view
        self.create_signals()
        
        pub.sendMessage("EXP RUBY DATA CHANGED", self)

    def create_signals(self):
        self.create_exp_file_signals()
        self.create_roi_view_signals()
        self.create_temperature_pub_listeners()
        self.create_auto_process_signal()
        self.create_pressure_signals()
        self.create_axes_click_signal()

    def create_temperature_pub_listeners(self):
        pub.subscribe(self.data_changed, "EXP RUBY DATA CHANGED")
        pub.subscribe(self.roi_changed, "RUBY ROI CHANGED")
        pub.subscribe(self.ruby_pos_changed, "RUBY POS CHANGED")

    def create_auto_process_signal(self):
        self.main_view.ruby_control_widget.auto_process_cb.clicked.connect(self.auto_process_cb_click)
        self.autoprocess_timer = QtCore.QTimer(self.main_view)
        self.autoprocess_timer.setInterval(100)
        self.main_view.connect(self.autoprocess_timer,QtCore.SIGNAL('timeout()'), self.check_files)
    
    def create_exp_file_signals(self):
        self.connect_click_function(self.main_view.ruby_control_widget.load_exp_data_btn, self.load_ruby_data)        
        self.connect_click_function(self.main_view.ruby_control_widget.load_next_exp_data_btn, self.load_next_exp_data)        
        self.connect_click_function(self.main_view.ruby_control_widget.load_previous_exp_data_btn, self.load_previous_exp_data)

    def create_roi_view_signals(self):
        self.connect_click_function(self.main_view.ruby_control_widget.roi_setup_btn, self.load_roi_view)

    def create_axes_click_signal(self):
        self.pos_update_timer = QtCore.QTimer(self.main_view)
        self.pos_update_timer.setInterval(5)
        self.main_view.connect(self.pos_update_timer, QtCore.SIGNAL('timeout()'),self.update_ruby_mouse_move_pos)
        self.main_view.graph_1axes.canvas.mpl_connect('button_press_event', self.axes_click)
        self.main_view.graph_1axes.canvas.mpl_connect('button_release_event', self.axes_release)
        self.main_view.graph_1axes.canvas.mpl_connect('motion_notify_event', self.axes_move)
        self.main_view.graph_1axes.canvas.mpl_connect('scroll_event', self.axes_mouse_scroll)

    def create_pressure_signals(self):
        self.main_view.ruby_control_widget.reference_pos_txt.editingFinished.connect(self.reference_txt_changed)
        self.main_view.ruby_control_widget.temperature_txt.editingFinished.connect(self.temperature_txt_changed)
        self.main_view.ruby_control_widget.conditions_cb.currentIndexChanged.connect(self.condition_cb_changed)
        self.connect_click_function(self.main_view.ruby_control_widget.fit_ruby_btn,self.fit_ruby_btn_click)
    
    def connect_click_function(self, emitter, function):
        self.main_view.connect(emitter, SIGNAL('clicked()'), function)

    def load_ruby_data(self, filename=None):
        if filename is None:
            filename = str(QtGui.QFileDialog.getOpenFileName(self.main_view, caption="Load Experiment SPE", 
                                          directory = self._exp_working_dir))

        if filename is not '':
            self._exp_working_dir = '/'.join(str(filename).replace('\\','/').split('/')[0:-1])+'/'
            self._files_before = dict([(f, None) for f in os.listdir(self._exp_working_dir)]) #reset for the autoprocessing
            self.data.load_ruby_data(filename)

    def load_next_exp_data(self):
        self.data.load_next_ruby_file()

    def load_previous_exp_data(self):
        self.data.load_previous_ruby_file()

    def load_roi_view(self):
        try:
            self.roi_controller.show()
        except AttributeError:
            self.roi_controller = TRaxROIControllerSingle(self.data, parent=self.main_view)
            self.roi_controller.show()

    def data_changed(self, event):
        self.main_view.graph_1axes.update_graph(self.data.get_spectrum(), self.data.click_pos, self.data.get_fitted_spectrum())
        self.main_view.set_ruby_filename(self.data.get_exp_file_name().replace('\\','/').split('/')[-1])
        self.main_view.set_ruby_foldername('/'.join(self.data.get_exp_file_name().replace('\\','/').split('/')[-3:-1]))

    def roi_changed(self, event):
        self.main_view.graph_1axes.update_graph(self.data.get_spectrum(), self.data.click_pos, self.data.get_fitted_spectrum())
        self.main_view.set_ruby_filename(self.data.get_exp_file_name().replace('\\','/').split('/')[-1])
        self.main_view.set_ruby_foldername('/'.join(self.data.get_exp_file_name().replace('\\','/').split('/')[-3:-1]))

    def ruby_pos_changed(self, event):
        self.main_view.graph_1axes.update_graph(self.data.get_spectrum(), self.data.click_pos, self.data.get_fitted_spectrum())

    def axes_click(self,event):
        if event.button==1:
            self._axes_mouse_x=event.xdata
            self.pos_update_timer.start()
        else:
            self.data.set_x_roi_limits_to(self.data.get_x_limits())
            pub.sendMessage("RUBY ROI CHANGED")

    def axes_move(self,event):
        self._axes_mouse_x=event.xdata

    def axes_release(self,event):
        self.pos_update_timer.stop()
    
    def update_ruby_mouse_move_pos(self):
        x_coord=self._axes_mouse_x
        if x_coord is not None:
            self.update_ruby_pos(x_coord)

    def update_ruby_pos(self,x_coord):
        self.data.set_click_pos(x_coord)
        self.main_view.ruby_control_widget.measured_pos_lbl.setText('%.2f'%x_coord)
        self.main_view.ruby_control_widget.pressure_lbl.setText('%.1f'%self.data.get_pressure())

    def axes_mouse_scroll(self,event):
        curr_xlim = self.main_view.graph_1axes.axes.get_xlim()
        base_scale=1.5
        if event.button == 'up':
            #zoom in
            scale_factor = 1/base_scale
        elif event.button == 'down':
            #zoom out
            scale_factor = base_scale
        else:
            scale_factor = 1
            print event.button

        new_width = (curr_xlim[1]-curr_xlim[0])*scale_factor

        relx = (curr_xlim[1]-event.xdata)/(curr_xlim[1]-curr_xlim[0])
        new_xlim=([event.xdata-new_width*(1-relx), event.xdata+new_width*(relx)])
        self.main_view.graph_1axes.axes.set_xlim(new_xlim)
        self.data.set_x_roi_limits_to(new_xlim)
        pub.sendMessage("RUBY ROI CHANGED")
        self.main_view.graph_1axes.redraw_figure()


    def reference_txt_changed(self):
        self.data.set_ruby_reference_pos(np.double(self.main_view.ruby_control_widget.reference_pos_txt.text()))
        self.main_view.ruby_control_widget.pressure_lbl.setText('%.1f'%self.data.get_pressure())

    def temperature_txt_changed(self):
        self.data.set_temperature(np.double(self.main_view.ruby_control_widget.temperature_txt.text()))
        self.main_view.ruby_control_widget.pressure_lbl.setText('%.1f'%self.data.get_pressure())

    def condition_cb_changed(self):
        ind=self.main_view.ruby_control_widget.conditions_cb.currentIndex()
        if ind==0:
            self.data.set_ruby_condition('hydrostatic')
        elif ind==1:
            self.data.set_ruby_condition('non-hydrostatic')
        self.main_view.ruby_control_widget.pressure_lbl.setText('%.1f'%self.data.get_pressure())

    def fit_ruby_btn_click(self):
        self.data.fit_spectrum()
        self.main_view.ruby_control_widget.measured_pos_lbl.setText('%.2f'%self.data.click_pos)
        self.main_view.ruby_control_widget.pressure_lbl.setText('%.1f'%self.data.get_pressure())
            
    def auto_process_cb_click(self):
        if self.main_view.ruby_control_widget.auto_process_cb.isChecked():
            self._files_before = dict([(f, None) for f in os.listdir(self._exp_working_dir)])
            self.autoprocess_timer.start()
        else:
            self.autoprocess_timer.stop()

    def check_files(self):
        self._files_now = dict([(f,None) for f in os.listdir(self._exp_working_dir)])
        self._files_added = [f for f in self._files_now if not f in self._files_before]
        self._files_removed = [f for f in self._files_before if not f in self._files_now]
        if len(self._files_added) > 0:
            new_file_str = self._files_added[-1]
            if self.file_is_spe(new_file_str) and not self.file_is_raw(new_file_str):
                path = self._exp_working_dir + '\\' + new_file_str
                self.data.load_ruby_data(path)
            self._files_before = self._files_now
            
    def file_is_spe(self, filename):
        return filename.endswith('.SPE') or filename.endswith('.spe')
    
    def file_is_raw(self, filename):
        try:
            #checks if file contains "-raw" string at the end
            return filename.split('-')[-1].split('.')[0] == 'raw'
        except:
            return false

    

if __name__ == "__main__":
    #convert_ui_files()
    app = QtGui.QApplication(sys.argv)
    controller = TRaxMainController()
    controller.main_view.show()
    app.exec_()