# -*- coding: utf-8 -*-
#__license__ = 'MIT'
import sys
import time
import win32com.client
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QComboBox, QMessageBox
from PyQt5 import QtWidgets,QtGui
#from PyQt5.QtGui import QIntValidator,QDoubleValidator,QFont
from PyQt5.QtCore import QRegExp
from PyQt5.QtCore import QTimer, QDateTime
from fpdf import FPDF

import windowui_english
import pyansys
import datetime
from pyansys import examples
import numpy as np
import matplotlib.pyplot as plt
import pylab
import os
import screenshots
#import sys
from PIL import Image
import giscnn
from pyansys import examples
import pyvista as pv
import vtk
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
import mph
from MPhmain import mph
import reportlab
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Image,Table, TableStyle
from reportlab.lib.enums import TA_CENTER,TA_LEFT,TA_JUSTIFY
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch

import fpdf
import tabtohorzion
SwFileName = ""
swfile_format = 0
client = mph.start()

import logging
logging.basicConfig(filename='myProgramLog.txt', level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

logger.info("软件运行正常")
logger.debug("软件无报错")
logger.info("工作正常")

# class childWindow(QDialog):
#     def __init__(self):
#         QDialog.__init__(self)
#         self.child=zc.Ui_MainWindow()
#         self.child.setupUi(self)




class MainCode(QMainWindow,windowui_english.Ui_MainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        windowui_english.Ui_MainWindow.__init__(self)
        #w = self.tab1
        #w.addTab(QtWidgets.QWidget(), "tab1")
        #w.addTab(QtWidgets.QWidget(), "tab2")
        #w.addTab(QtWidgets.QWidget(), "tab3")
        #w.show()
        self.setupUi(self)
        self.timer = QTimer()#show current time
        self.timer.timeout.connect(self.showTime)
        self.timer.start(1000)
        # self.tabWidget.setTabBar(tabtohorzion.TabBar(self))
        # self.tabWidget.setTabPosition(QtWidgets.QTabWidget.West)
        # self.tabWidget.addTab(QtWidgets.QWidget(), "标准模型")
        # self.tabWidget.addTab(QtWidgets.QWidget(), "缺陷诊断")
        # self.tabWidget.addTab(QtWidgets.QWidget(), "缺陷分析")
        #self.tab2.setTabBar(tabtohorzion.TabBar(self))
        #self.tab3.setTabBar(tabtohorzion.TabBar(self))
        ################title setting###########################
        self.actiontitlenewfile.triggered.connect(self.titlenewfile)  # 触发事件动作为"新建"
        #self.actiontitlesavefile_.triggered.connect(self.titlesavefile)  # 触发事件动作为"保存"
        self.actiontitleinput.triggered.connect(self.titleinput)  # 触发事件动作为"导入"
        self.actiontitleoutput.triggered.connect(self.titleoutput)  # 触发事件动作为"导出"
        self.actiontitleexit.triggered.connect(self.windowexit)  # 触发事件动作为"关闭窗口"
        self.actiontitlelist.triggered.connect(self.titlelist)  # 触发事件动作为"输入环境变量列表"
        #self.actiontitlecompute.triggered.connect(self.titlecompute)  # 触发事件动作为"计算"
        self.actiontitlejietu.triggered.connect(self.titlejietu)  # 触发事件动作为"截图"
        self.actiontitleprocess.triggered.connect(self.titleprocess)  # 触发事件动作为"后处理"
        self.actiontitlereviewin.triggered.connect(self.titlereviewin)  # 触发事件动作为"缺陷模块预览和导入"
        self.actiontitlereviewpdf.triggered.connect(self.titlereviewpdf)  # 触发事件动作为"仿真分析报告预览"
        self.actionbtitleuserbook.triggered.connect(self.titleuserbook)  # 触发事件动作为"软件使用说明"
        self.actiontitlebanquan.triggered.connect(self.titlebanquan)  # 触发事件动作为"版权信息"

#########################################model simulation page#######################

        self.save_solidworks_file.clicked.connect(self.on_save)#打开solidworks模型
        self.open_solidworks_file.clicked.connect(self.on_open)#保存solidworks模型
        self.open_ansys_file.clicked.connect(self.open_ansys)#打开ansys模型
        self.save_ansys_file.clicked.connect(self.save_ansys)#保存ansys模型
        self.saveas_xt_and_showin_ansys.clicked.connect(self.saveas_xt_and_showin_ansys_function)#另存为x_t格式并导进ANSYS
        self.calculate_ansys.clicked.connect(self.calcuate_ansys_prcoess)
        self.model_ansys_show_click.clicked.connect(self.ansys_show)
        self.modul_soli_show_click.clicked.connect(self.modul_solid_show)
        self.assembly_soli_show_click.clicked.connect(self.assembly_solid_show)
        #self.model_soli_show_click.clicked.connect(self.solidworks_show)
        self.openworkbench.clicked.connect(self.openworkbenchprocess)
        self.playout_3D.clicked.connect(self.playout_3D_show)  # 打开仿真结果3D模型
        self.mesh_ansys.clicked.connect(self.mesh_process)
        self.upload_model.clicked.connect(self.upload_model_process)
        self.load_simu_model.clicked.connect(self.load_simulation_model)

        self.init_model_device_type()
        self.init_model_device_company()
        self.init_model_device_modelNumber()
        self.init_modul_device_No()
        self.init_assembly_device_No()
        self.init_model_fault_type()
        self.init_simu_model_device_number()
        self.init_model_workvoltage_unit()
        self.init_model_workcurrent_unit()
        self.init_model_environmenttemp_unit()
        self.init_model_environpressure_unit()
        #self.init_model_physicsfield_type()
        #self.init_model_fault_set()
        self.init_model_number_input()

        # self.vtkWidget = QVTKRenderWindowInteractor(self.centralwidget)  # 提供平台独立的响应鼠标、键盘和时钟事件的交互机制
        # self.verticalLayout_ansys_show.addWidget(self.vtkWidget)
        # self.ren = vtk.vtkRenderer()  # 负责管理场景的渲染过程
        # self.ren.SetBackground(1.0, 1.0, 1.0)  # 设置页面底部颜色值
        # self.ren.SetBackground2(0.1, 0.2, 0.4)  # 设置页面顶部颜色值
        # self.ren.SetGradientBackground(1)  # 开启渐变色背景设置
        #
        # self.vtkWidget.GetRenderWindow().AddRenderer(self.ren)
        # self.iren = self.vtkWidget.GetRenderWindow().GetInteractor()
        # # 交互器样式的一种，该样式下，用户是通过控制相机对物体作旋转、放大、缩小等操作
        # style = vtk.vtkInteractorStyleTrackballCamera()
        # self.iren.SetInteractorStyle(style)
        self.model_device_type.activated.connect(self.on_model_device_type_Activate)
        #client = mph.start()





###################################fault diagnosis page####################
        self.init_diagnosis_fault_type()
        self.diagnosis_fault_type.activated.connect(self.on_diagnosis_fault_type_Activate)
        self.open_fault_file.clicked.connect(self.open_fault_data)
        #self.upload_fault_data.clicked.connect(self.upload_fault)
        self.init_diagnosis_device_type()
        self.init_diagnosis_device_company()
        self.init_diagnosis_device_modelNumber()

################################fault analysis page#######################################
        self.init_analysis_device_type()
        self.init_analysis_device_company()
        self.init_analysis_device_modelNumber()
        self.init_analysis_fault_type()
        self.init_analysis_workvoltage_unit_a()
        self.init_analysis_workvoltage_unit_b()
        self.init_analysis_workvoltage_unit_c()
        self.init_analysis_workcurrent_unit_a()
        self.init_analysis_workcurrent_unit_b()
        self.init_analysis_workcurrent_unit_c()
        self.init_analysis_workgamma_unit_a()
        self.init_analysis_workgamma_unit_b()
        self.init_analysis_workgamma_unit_c()
        self.init_analysis_environmenttemp_unit()
        self.init_analysis_environpressure_unit()
        #self.init_analysis_physicsfield_type()
        #self.init_analysis_fault_set()
        #self.init_analysis_number_input()

        #self.analysis_calculate1.clicked.connect(self.analysis_calculate_1)  # 打开solidworks模型
        self.playout_3D_fault.clicked.connect(self.playout_3D_show_fault)  # 打开仿真结果3D模型
        self.mesh_ansys_fault.clicked.connect(self.mesh_process_fault)
        #self.upload_model_fault.clicked.connect(self.upload_model_process_fault)
        self.load_simu_model_fault.clicked.connect(self.load_simulation_model_fault)
        self.calculate_ansys_fault.clicked.connect(self.calcuate_ansys_prcoess_fault)
        self.model_ansys_show_click_fault.clicked.connect(self.ansys_show_fault)




########################################################################
    def showTime(self):
        time = QDateTime.currentDateTime()
        timeDisplay = time.toString("yyyy-MM-dd hh:mm:ss dddd")
        self.timeshow.setText(timeDisplay)
######################title setting##########################

    def titlenewfile(self):
        print("newfile")
        FileName_fault, filetype = QFileDialog.getSaveFileName(self, '保存文件', r'./', 'All Files(*);;TXT (*.txt)')

    def titlesavefile(self):
        print("savefile")
        FileName_fault, filetype = QFileDialog.getSaveFileName(self, '保存文件', r'./', 'All Files(*);;TXT (*.txt)')

    def titleinput(self):
        print("input")
        FileName_fault, filetype = QFileDialog.getOpenFileName(self, '打开文件', r'./', 'All Files(*);;TXT (*.txt)')

    def titleoutput(self):
        print("newfile")
        FileName_fault, filetype = QFileDialog.getSaveFileName(self, '保存文件', r'./', 'All Files(*);;TXT (*.txt)')

    def windowexit(self):  # 触发事件动作为"关闭窗口"
        print("windowexit")
        self.close()##关闭子窗口（其他窗口不关闭）
        sys.exit(0)##关闭全部窗口（主窗口+所有的子窗口）


    def titlelist(self):  # 触发事件动作为"输入环境变量列表"
        print("list")
        FullFileName, _ = QFileDialog.getSaveFileName(self, '文件另存为', r'./', 'TXT (*.txt)')
        set_text = self.txt_view.toPlainText()
        with open(FullFileName, 'wt') as f:
            print(set_text, file=f)

    def titlecompute(self):  # 触发事件动作为"计算"
        print("compute")


    def titlejietu(self):  # 触发事件动作为"截图"
        #print("jietu")
        #self.showMinimized()##当前软件界面最小化
        self.screenshot = screenshots.ScreenShotsWin()
        self.screenshot.showFullScreen()


    def titleprocess(self): # 触发事件动作为"后处理"
        print("process")

    def titlereviewin(self):  # 触发事件动作为"缺陷模块预览和导入"
        print("reviewin")
        FileName_fault, filetype = QFileDialog.getOpenFileName(self, '打开文件', r'./', 'All Files(*);;TXT (*.txt)')

    def titlereviewpdf(self):  # 触发事件动作为"仿真分析报告预览"
        print("ireviewpdf")

        pdfmetrics.registerFont(TTFont('msyh','msyh.ttf'))
        elements=[]
        style = getSampleStyleSheet()
        title="""<para><font face ="msyh">仿真分析报告</font></para>"""
        elements.append(Paragraph(title,style['Title']))
        elements.append(Spacer(1,0.2*inch))
        description="""<para><font face ="msyh">仿真分析结果如下</font></para>"""
        elements.append(Paragraph(description,style["BodyText"]))
        elements.append(Spacer(1,0.2*inch))
        elements.append(Paragraph("""<para><font face ="msyh">仿真分析结果图</font></para>""",style["h3"]))
        img = Image('F:\\solidworks ansys\\comsol file\\dianshishow.jpg')
        elements.append(img)
        #elements.setScaledContents(True)

        elements.append(Spacer(1, 0.2 * inch))
        FullFileName, _ = QFileDialog.getSaveFileName(self, '文件另存为', r'./', 'PDF (*.pdf)')
        doc = SimpleDocTemplate(FullFileName,pagesize=(A4[0],A4[1]),topMargin=30,bottomMargin=30)
        doc.build(elements)





        #set_text = self.txt_view.toPlainText()
        # with open(FullFileName, 'wt') as f:
        #     print(set_text, file=f)
        # pdf = FPDF()
        # # 加一页
        # pdf.add_page()
        # # 设置字体的大小和字体
        # pdf.set_font('Arial', size=15)
        # # 加一个单元
        # pdf.cell(200, 10, txt='您好', ln=1, align='C')
        # # 加一个新的单元格
        # pdf.cell(200, 10, txt='this is a article.', ln=2, align='C')
        #
        # pdf.output('test.pdf')


    def titleuserbook(self):  # 触发事件动作为"软件使用说明"
        print("userbook")
        QMessageBox.about(self, "软件使用说明书", "广东电科院院高压所")

    def titlebanquan(self):  # 触发事件动作为"版权信息"
        #print("banquan")
        QMessageBox.about(self,"版权信息","广东电科院高压所")
        #self.echo(reply)

##############################model simulation page#######################################
    def init_model_device_type(self):
        self.model_device_type.addItem("开关柜")
        self.model_device_type.addItem("组合电器")
        self.model_device_type.addItem("断路器机构")
        self.model_device_type.setCurrentIndex(-1)

    def init_model_device_company(self):
        self.model_device_company.addItem("山东泰开")
        self.model_device_company.addItem("西安西电")
        self.model_device_company.addItem("河南平高")
        self.model_device_company.addItem("新东北电气")
        self.model_device_company.addItem("北京北开")
        self.model_device_company.addItem("上海思源")
        self.model_device_company.addItem("ABB")
        self.model_device_company.addItem("西门子")
        self.model_device_company.addItem("阿海珐")
        self.model_device_company.addItem("通用")
        self.model_device_company.addItem("三菱")
        self.model_device_company.addItem("东芝")
        self.model_device_company.addItem("日新")
        self.model_device_company.setCurrentIndex(-1)
    def init_modul_device_No(self):
        # self.model_device_No.addItem("KYN2-0203-0004 仪表室模块-10宽 无小母线")
        # self.model_device_No.addItem("KYN2-0501-0002 仪表室门板焊装 大电流")
        # self.model_device_No.addItem("KYN2-0502-0008 前中门板焊装 大电流 VS1 带程序锁")
        # self.model_device_No.addItem("KYN2-0203-0004 仪表室模块-10宽 无小母线")
        # self.model_device_No.addItem("KYN2-0501-0002 仪表室门板焊装 大电流")
        # self.model_device_No.addItem("KYN2-0502-0008 前中门板焊装 大电流 VS1 带程序锁")
        self.modul_device_No.setCurrentIndex(-1)
    def init_assembly_device_No(self):
        # self.model_device_No.addItem("KYN2-0203-0004 仪表室模块-10宽 无小母线")
        # self.model_device_No.addItem("KYN2-0501-0002 仪表室门板焊装 大电流")
        # self.model_device_No.addItem("KYN2-0502-0008 前中门板焊装 大电流 VS1 带程序锁")
        # self.model_device_No.addItem("KYN2-0203-0004 仪表室模块-10宽 无小母线")
        # self.model_device_No.addItem("KYN2-0501-0002 仪表室门板焊装 大电流")
        # self.model_device_No.addItem("KYN2-0502-0008 前中门板焊装 大电流 VS1 带程序锁")
        self.assembly_device_No.setCurrentIndex(-1)
    def upload_model_process(self):


        path = "F:\\solidworks ansys\\ANSYS20201211\\3Dstl model\\module model"###需要修改的路径##这里是保存模块化模型的文件夹路径
        datanames = os.listdir(path)
        for i in datanames:
            name1 = os.path.splitext(i)
            print(name1[0])
            self.modul_device_No.addItem(name1[0])
        path = "F:\\solidworks ansys\\ANSYS20201211\\3Dstl model\\assembly model"  ###需要修改的路径##这里是保存装配件模型的文件夹路径
        datanames = os.listdir(path)
        for i in datanames:
            name1 = os.path.splitext(i)
            print(name1[0])
            self.assembly_device_No.addItem(name1[0])
        print('ok')

    def load_simulation_model(self):
        #client = mph.start()
        path = "F:\\solidworks ansys\\comsol file"
        datanames = os.listdir(path)
        for i in datanames:
            name1 = os.path.splitext(i)
            #print(name1[1])
            if self.simu_model_device_number.currentText() == name1[0] and name1[1] == '.mph':
                #client = mph.start()
                #print('ok1'+self.simu_model_device_number.currentText())
                model = client.load('F:\\solidworks ansys\\comsol file\\'+i)
                print('ok1' + i)
                model.parameters()
                for (name, value) in model.parameters().items():
                    description = model.description(name)
                    print(f'{description:20} {name} = {value}')
                    if 'Voltage' in name:
                        self.model_workvoltage_edit.setText(value)
                    elif 'Current' in name:
                        self.model_workcurrent_edit.setText(value)
                    elif 'Temp' in name:
                        self.model_environmenttemp_edit.setText(value)
                        # if value > 200:
                        #     self.model_environmenttemp_unit.setCurrentIndex("K(开尔文)")
                        # elif value < 50:
                        #     self.model_environmenttemp_unit.setCurrentIndex("℃(摄氏度)")
                    elif 'Pressure' in name:
                        self.model_environpressure_edit.setText(value)







    def init_model_device_modelNumber(self):
        self.model_device_modelNumber.setCurrentIndex(-1)

    def init_model_fault_type(self):
        self.model_fault_type.addItem("局部放电")
        self.model_fault_type.addItem("过热缺陷")
        self.model_fault_type.addItem("机构缺陷")
        self.model_fault_type.setCurrentIndex(-1)

    def init_simu_model_device_number(self):
        self.simu_model_device_number.addItem("126kV GIS BUS single mf")
        self.simu_model_device_number.addItem("252kV GIS es Hz")
        self.simu_model_device_number.addItem("KYN28-12 es")
        self.simu_model_device_number.addItem("KYN28-12 ht")
        self.simu_model_device_number.addItem("126kV GIS BUS ht ec")

        self.simu_model_device_number.setCurrentIndex(-1)

    def init_model_workvoltage_unit(self):
        self.model_workvoltage_unit.addItem("KV(千伏)")
        self.model_workvoltage_unit.addItem("V(伏)")
        self.model_workvoltage_unit.setCurrentIndex(-1)

    def init_model_workcurrent_unit(self):
        self.model_workcurrent_unit.addItem("KA(千安)")
        self.model_workcurrent_unit.addItem("A(安)")
        self.model_workcurrent_unit.setCurrentIndex(-1)

    def init_model_environmenttemp_unit(self):
        self.model_environmenttemp_unit.addItem("℃(摄氏度)")
        self.model_environmenttemp_unit.addItem("K(开尔文)")
        self.model_environmenttemp_unit.setCurrentIndex(-1)

    def init_model_environpressure_unit(self):
        self.model_environpressure_unit.addItem("KPa(千帕)")
        self.model_environpressure_unit.addItem("Pa(帕)")
        self.model_environpressure_unit.addItem("毫米汞柱")
        self.model_environpressure_unit.setCurrentIndex(-1)
    def init_model_number_input(self):
        #my_regex = QRegExp('[0-9.]+$')
        my_regex = QRegExp("^(-?[0]|-?[1-9][0-9]{0,5})(?:\\.\\d{1,4})?$|(^\\t?$)")
        my_validator = QtGui.QRegExpValidator(my_regex, self)
        self.model_workvoltage_edit.setValidator(my_validator)
        self.model_workcurrent_edit.setValidator(my_validator)
        self.model_environmenttemp_edit.setValidator(my_validator)
        self.model_environpressure_edit.setValidator(my_validator)

    def on_model_device_type_Activate(self, index):
        if self.model_device_type.currentText() == "开关柜":
            self.model_device_modelNumber.clear()
            self.model_device_modelNumber.addItem("KYN28-12")
            self.model_device_modelNumber.addItem("KYN61-40.5")
            self.model_device_modelNumber.setCurrentIndex(-1)
        elif self.model_device_type.currentText() == "组合电器":
            self.model_device_modelNumber.clear()
            self.model_device_modelNumber.addItem("ZF16-252")
            self.model_device_modelNumber.setCurrentIndex(-1)
        elif self.model_device_type.currentText() == "断路器机构":
            self.model_device_modelNumber.clear()
            self.model_device_modelNumber.addItem("CT26-252")
            self.model_device_modelNumber.setCurrentIndex(-1)

    def ansys_show(self):
        self.Simu_progressBar.setValue(100)

        #self.vtkWidgetshow = QtWidgets.QFrame()
        #QVTKRenderWindowInteractor.__init__(self.vtkContext, self.vtkContext)
        #self.vtkContext.GetRenderWindow().GetInteractor().SetInteractorStyle(vtk.vtkInteractorStyleTrackballCamera())
        if self.simu_model_type.currentText() == '电势':
            png = QtGui.QPixmap('F:\\solidworks ansys\\comsol file\\dianshishow.jpg')
            # self.label_simu_2D.setPixmap(png)
            # self.label_simu_2D.setScaledContents(True)
        elif self.simu_model_type.currentText() == '电场':
            png = QtGui.QPixmap('F:\\solidworks ansys\\comsol file\\dianchangshow.jpg')
        elif self.simu_model_type.currentText() == '温度':
            png = QtGui.QPixmap('F:\\solidworks ansys\\comsol file\\in figure\\2.png')
        elif self.simu_model_type.currentText() == '气流':
            png = QtGui.QPixmap('F:\\solidworks ansys\\comsol file\\in figure\\1.png')
        self.label_simu_2D.setPixmap(png)
        self.label_simu_2D.setScaledContents(True)


       #  self.vtkWidget = QVTKRenderWindowInteractor(self.model_ansys_show)  # 提供平台独立的响应鼠标、键盘和时钟事件的交互机制
       #  #self.verticalLayout_vtk_show.addWidget(self.vtkWidget)
       #
       #  self.ren = vtk.vtkRenderer()  # 负责管理场景的渲染过程
       #  self.ren.SetBackground(1.0, 1.0, 1.0)  # 设置页面底部颜色值
       #  self.ren.SetBackground2(0.1, 0.2, 0.4)  # 设置页面顶部颜色值
       #  self.ren.SetGradientBackground(1)  # 开启渐变色背景设置
       #
       #  self.vtkWidget.GetRenderWindow().AddRenderer(self.ren)
       #  self.iren = self.vtkWidget.GetRenderWindow().GetInteractor()
       #  # 交互器样式的一种，该样式下，用户是通过控制相机对物体作旋转、放大、缩小等操作
       #  style = vtk.vtkInteractorStyleTrackballCamera()
       #  self.iren.SetInteractorStyle(style)
       #
       #  # Read from STL file
       #  cone_a = vtk.vtkSTLReader()
       #  cone_a.SetFileName("F:\\solidworks ansys\\ANSYS202012092211\MPh-master\\stl1520.stl")
       #  #cone_a = vtk.vtkStructuredPointsReader()
       # ## cone_a = vtk.vtkUnstructuredGridReader()
       #  #cone_a = vtk.vtkPolyDataReader()
       #  ##cone_a.SetFileName('F:\\solidworks ansys\\ANSYS202012092211\\hexvtktest.vtk')
       #  ##cone_a.Update()
       #  #cone_a = vtk.vtkConeSource()
       #  #cone_a =vtk.vtkUntructuredPointsReader('F:\\solidworks ansys\\ANSYS202012092211\\MPh-master\\fieldvtk.vtu')
       #
       #  coneMapper = vtk.vtkPolyDataMapper()  # 渲染多边形几何数据
       #  coneMapper.SetInputConnection(cone_a.GetOutputPort())
       #  #coneMapper = vtk.vtkUnstructuredGridDataMapper()
       #  #coneMapper.SetInputConnection(cone_a.GetOutputPort())
       #  #grid =
       #  actor = vtk.vtkActor()
       #  actor.SetMapper(coneMapper)
       #
       #
       #  # Read from OBJ file
       #  # objReader = vtk.vtkOBJReader()
       #  # objReader.SetFileName("test.obj")
       #
       #  # Create a mapper
       #
       #  # VTK可视化管线的输入数据接口 ，对应的可视化管线输出数据的接口为GetOutputPort()；
       #  # mapper.SetInputConnection(objReader.GetOutputPort())
       #
       #  # Create an actor
       #
       #  # 设置生成几何图元的Mapper。即连接一个Actor到可视化管线的末端(可视化管线的末端就是Mapper)。
       #
       #  self.ren.AddActor(actor)
       #  self.ren.ResetCamera()
       #
       #  #self.vtkWidgetshow.setLayout(self.verticalLayout_vtk_show)
       #  #self.setCentralWidget(self.vtkWidgetshow)
       #
       #  self.vtkWidget.show()
       #  self.iren.Initialize()
       #  #self.orient.SetEnabled(1)  # Needed to set InteractiveOff
       #  #self.orient.InteractiveOff()
       #  #self.orient.SetEnabled(visible)
       #  #self.window.Render()


    def modul_solid_show(self):

        #self.vtkWidgetshow = QtWidgets.QFrame()
        #QVTKRenderWindowInteractor.__init__(self.vtkContext, self.vtkContext)
        #self.vtkContext.GetRenderWindow().GetInteractor().SetInteractorStyle(vtk.vtkInteractorStyleTrackballCamera())

        self.vtkWidget = QVTKRenderWindowInteractor(self.modul_solidworks_show)  # 提供平台独立的响应鼠标、键盘和时钟事件的交互机制
        #self.vtkWidget = QVTKRenderWindowInteractor(self.model_solidworks_show1)
        #self.verticalLayout_vtk_show.addWidget(self.vtkWidget)

        self.ren = vtk.vtkRenderer()  # 负责管理场景的渲染过程
        self.ren.SetBackground(1.0, 1.0, 1.0)  # 设置页面底部颜色值
        self.ren.SetBackground2(0.1, 0.2, 0.4)  # 设置页面顶部颜色值
        self.ren.SetGradientBackground(1)  # 开启渐变色背景设置
        axes = vtk.vtkAxesActor()
        axes.SetTotalLength(100, 100, 100)##设置背景大小

        axes.SetAxisLabels(0)  # Enable:1/disable:0 drawing the axis labels
        self.ren.AddActor(axes)  ###显示坐标系


        self.vtkWidget.GetRenderWindow().AddRenderer(self.ren)
        self.iren = self.vtkWidget.GetRenderWindow().GetInteractor()
        # 交互器样式的一种，该样式下，用户是通过控制相机对物体作旋转、放大、缩小等操作
        style = vtk.vtkInteractorStyleTrackballCamera()
        self.iren.SetInteractorStyle(style)


        # Read from STL file
        # cone_a = vtk.vtkConeSource()
        #
        # coneMapper = vtk.vtkPolyDataMapper()
        # coneMapper.SetInputConnection(cone_a.GetOutputPort())

        # actor = vtk.vtkActor()
        # actor.SetMapper(coneMapper)
        stlreader = vtk.vtkSTLReader()
        path = "F:\\solidworks ansys\\ANSYS20201211\\3Dstl model\\module model"
        datanames = os.listdir(path)
        for i in datanames:
            name1 = os.path.splitext(i)
            #print(name1[0])
            if self.modul_device_No.currentText()==name1[0]:
                stlreader.SetFileName("F:\\solidworks ansys\\ANSYS20201211\\3Dstl model\\module model\\"+i)
        #stlreader.SetFileName("F:\\solidworks ansys\\solidworkstoxtresult\\dianliuhugan1.stl")##更改相关文件名实现对stl格式的三维图形显示，显示在界面左边方框里


        # Read from OBJ file
        # objReader = vtk.vtkOBJReader()
        # objReader.SetFileName("test.obj")

        # Create a mapper
        mapper = vtk.vtkPolyDataMapper()  # 渲染多边形几何数据
        mapper.SetInputConnection(stlreader.GetOutputPort())

        # VTK可视化管线的输入数据接口 ，对应的可视化管线输出数据的接口为GetOutputPort()；
        # mapper.SetInputConnection(objReader.GetOutputPort())

        # Create an actor
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)

        # 设置生成几何图元的Mapper。即连接一个Actor到可视化管线的末端(可视化管线的末端就是Mapper)。

        self.ren.AddActor(actor)
        self.ren.ResetCamera()

        #self.vtkWidgetshow.setLayout(self.verticalLayout_vtk_show)
        #self.setCentralWidget(self.vtkWidgetshow)

        self.vtkWidget.show()
        self.iren.Initialize()
        #self.orient.SetEnabled(1)  # Needed to set InteractiveOff
        #self.orient.InteractiveOff()
        #self.orient.SetEnabled(visible)
        #self.window.Render()

    def assembly_solid_show(self):

        #self.vtkWidgetshow = QtWidgets.QFrame()
        #QVTKRenderWindowInteractor.__init__(self.vtkContext, self.vtkContext)
        #self.vtkContext.GetRenderWindow().GetInteractor().SetInteractorStyle(vtk.vtkInteractorStyleTrackballCamera())

        self.vtkWidget = QVTKRenderWindowInteractor(self.assembly_solidworks_show)  # 提供平台独立的响应鼠标、键盘和时钟事件的交互机制
        #self.vtkWidget = QVTKRenderWindowInteractor(self.model_solidworks_show1)
        #self.verticalLayout_vtk_show.addWidget(self.vtkWidget)

        self.ren = vtk.vtkRenderer()  # 负责管理场景的渲染过程
        self.ren.SetBackground(1.0, 1.0, 1.0)  # 设置页面底部颜色值
        self.ren.SetBackground2(0.1, 0.2, 0.4)  # 设置页面顶部颜色值
        self.ren.SetGradientBackground(1)  # 开启渐变色背景设置
        axes = vtk.vtkAxesActor()
        axes.SetTotalLength(100, 100, 100)##设置背景大小

        axes.SetAxisLabels(0)  # Enable:1/disable:0 drawing the axis labels
        self.ren.AddActor(axes)  ###显示坐标系


        self.vtkWidget.GetRenderWindow().AddRenderer(self.ren)
        self.iren = self.vtkWidget.GetRenderWindow().GetInteractor()
        # 交互器样式的一种，该样式下，用户是通过控制相机对物体作旋转、放大、缩小等操作
        style = vtk.vtkInteractorStyleTrackballCamera()
        self.iren.SetInteractorStyle(style)


        # Read from STL file
        # cone_a = vtk.vtkConeSource()
        #
        # coneMapper = vtk.vtkPolyDataMapper()
        # coneMapper.SetInputConnection(cone_a.GetOutputPort())

        # actor = vtk.vtkActor()
        # actor.SetMapper(coneMapper)
        stlreader = vtk.vtkSTLReader()
        path = "F:\\solidworks ansys\\ANSYS20201211\\3Dstl model\\assembly model"
        datanames = os.listdir(path)
        for i in datanames:
            name1 = os.path.splitext(i)
            #print(name1[0])
            if self.assembly_device_No.currentText()==name1[0]:
                stlreader.SetFileName("F:\\solidworks ansys\\ANSYS20201211\\3Dstl model\\assembly model\\"+i)
        #stlreader.SetFileName("F:\\solidworks ansys\\solidworkstoxtresult\\dianliuhugan1.stl")##更改相关文件名实现对stl格式的三维图形显示，显示在界面左边方框里
        if self.model_device_modelNumber.currentText()=="CT26-252":
            stlreader.SetFileName("F:\\solidworks ansys\\ansys202003201652\\Part library\\CT26-252.stl")
        elif self.model_device_modelNumber.currentText()=="ZF16-252":
            stlreader.SetFileName("F:\\solidworks ansys\\ansys202003201652\\Part library\\ZF16-252.stl")
        elif self.model_device_modelNumber.currentText()=="KYN28-12":
            stlreader.SetFileName("F:\\solidworks ansys\\ansys202003201652\\Part library\\KYN28-12.stl")
        elif self.model_device_modelNumber.currentText()=="KYN61-40.5":
            stlreader.SetFileName("F:\\solidworks ansys\\ansys202003201652\\Part library\\KYN61-40.5.stl")

        # Read from OBJ file
        # objReader = vtk.vtkOBJReader()
        # objReader.SetFileName("test.obj")

        # Create a mapper
        mapper = vtk.vtkPolyDataMapper()  # 渲染多边形几何数据
        mapper.SetInputConnection(stlreader.GetOutputPort())

        # VTK可视化管线的输入数据接口 ，对应的可视化管线输出数据的接口为GetOutputPort()；
        # mapper.SetInputConnection(objReader.GetOutputPort())

        # Create an actor
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)

        # 设置生成几何图元的Mapper。即连接一个Actor到可视化管线的末端(可视化管线的末端就是Mapper)。

        self.ren.AddActor(actor)
        self.ren.ResetCamera()

        #self.vtkWidgetshow.setLayout(self.verticalLayout_vtk_show)
        #self.setCentralWidget(self.vtkWidgetshow)

        self.vtkWidget.show()
        self.iren.Initialize()
        #self.orient.SetEnabled(1)  # Needed to set InteractiveOff
        #self.orient.InteractiveOff()
        #self.orient.SetEnabled(visible)
        #self.window.Render()






    def on_save(self):
        FullFileName,_=QFileDialog.getSaveFileName (self, '文件另存为', r'./','TXT (*.txt)')
        set_text=self.txt_view.toPlainText()
        with open(FullFileName,'wt') as f:
            print(set_text, file = f)
    def playout_3D_show(self):
       # grid = pv.UnstructuredGrid('F:\\solidworks ansys\\ansys202003201652\\MPh-master\\HeEF1605VTU.vtu')
        if self.simu_model_type.currentText() == '电势':
           grid = pv.UnstructuredGrid('F:\solidworks ansys\comsol file\\dianshi3Dshow.vtu')
           #png = QtGui.QPixmap('F:\\solidworks ansys\\comsol file\\dianshishow.jpg')
        elif self.simu_model_type.currentText() == '电场':
           grid = pv.UnstructuredGrid('F:\solidworks ansys\comsol file\\dianchang3Dshow.vtu')
        grid.plot()
    def mesh_process(self):
        path = "F:\\solidworks ansys\\comsol file"
        datanames = os.listdir(path)
        self.Simu_progressBar.setValue(25)
        for i in datanames:
            name1 = os.path.splitext(i)
            # print(name1[1])
            if self.simu_model_device_number.currentText() == name1[0] and name1[1] == '.mph':
                #client = mph.start()
                # print('ok1'+self.simu_model_device_number.currentText())
                model = client.load('F:\\solidworks ansys\\comsol file\\' + i)
        model.parameter('Voltage', self.model_workvoltage_edit.text())
        model.parameter('Current', self.model_workcurrent_edit.text())
        model.parameter('Temp', self.model_environmenttemp_edit.text())
        model.parameter('Pressure', self.model_environpressure_edit.text())
        model.build()
        model.mesh()
        model.export('mesh', 'meshshow.jpg')
        #model.export('meshvtu', 'mesh3Dshow.vtu')
                #model.solve()
                #model.save()
        png = QtGui.QPixmap('F:\\solidworks ansys\\comsol file\\meshshow.jpg')
        #time.sleep(10)
        self.label_simu_2D.setPixmap(png)
        self.label_simu_2D.setScaledContents(True)
        print('okfinish')
        self.Simu_progressBar.setValue(80)
        model.clear()


       # client = mph.start()
        #print('ok1')
        #self.Simu_progressBar.setValue(25)
        #time.sleep(2)
        #model = client.load('F:\\solidworks ansys\\comsol file\\KYN28-12 es.mph')
        #time.sleep(2)
        #print('load success')
        # model.export('electric filed', 'static field11111.jpg')
        # model.export('electric potential', 'static potential11111.jpg')
        # model.export('electric filed 3d', 'static field111113d.vtu')
        # model.export('electric potential 3d', 'static potential111113d.vtu')
        #time.sleep(2)
        #self.Simu_progressBar.setValue(50)
        #time.sleep(1)
        #model.parameter('U', '1 [V]')
        #model.parameter('d', '1 [mm]')
        #print('ok3')
        #time.sleep(2)
        #self.Simu_progressBar.setValue(75)
        #time.sleep(1)
        # model.solve()
        # model.save()
        ##print('solve success')
        #time.sleep(2)
        #model.export('electric field', 'static field11111.jpg')
        #model.export('electric potential', 'static potential11111.jpg')
       # model.export('electric field 3d', 'static field111113d.vtu')
        #model.export('electric potential 3d', 'static potential111113d.vtu')
        #self.Simu_progressBar.setValue(100)
        #C = model.evaluate('2*es.intWe/U^2', 'pF')
        # print(f'capacitance C = {C:.3f} pF')

    def on_open(self):
        #txtstr=""
        global SwFileName
        global swfile_format


        SwFileName, Swfiletype = QFileDialog.getOpenFileName(self, '打开', r'./',  '装配文件(*.prt *.sldprt *.sldasm);;所有文件（*.*);;')
        print(SwFileName, Swfiletype)
        SwFileNameSplit=SwFileName.split(".")
        print(SwFileNameSplit)
        print(len(SwFileNameSplit))
        print(type(SwFileName))
        # self.show_fault_URL.setText(SwFileName)
        swYearLastDigit = 8  # sw 2014
        swApp = win32com.client.DispatchEx("SldWorks.Application.%d" % (20 + (swYearLastDigit - 2)))
        # # swApp = win32com.client.Dispatch('SldWorks.Application')
        swApp.Visible = 1  ###solidworks软件可视化
        if SwFileNameSplit[len(SwFileNameSplit)-1] =='SLDPRT':
            Model_showin_sw = swApp.OpenDoc(SwFileName,1)
            swfile_format = 1
        elif SwFileNameSplit[len(SwFileNameSplit)-1] == 'SLDASM':
            Model_showin_sw = swApp.OpenDoc(SwFileName, 2)
            swfile_format = 2
        # #session.invalidate();


    def open_ansys(self):
        filename = examples.hexarchivefile

        # Read ansys archive file
        archive = pyansys.Archive(filename)

        # Print raw data from cdb
        for key in archive.raw:
            print("%s : %s" % (key, archive.raw[key]))

        # Create a vtk unstructured grid from the raw data and plot it
        grid = archive.parse_vtk(force_linear=True)
        grid.plot(color='w', show_edges=False)#color 物体颜色 show_edges 网格是否显示
        print(type(grid))
        print("hello,type")
        self.widget_ansys_show.show(grid)
        #grid.
    def save_ansys(self):
        path = os.getcwd()
        ansys = pyansys.Mapdl(run_location=path, interactive_plotting=True)

        # create a square area using keypoints
        ansys.prep7()  # 前处理
        # ansys.k(1, 0, 0, 0)#点坐标（编号，三维）
        # ansys.k(2, 1, 0, 0)
        # ansys.k(3, 1, 1, 0)
        # #ansys.k(4, 0, 1, 0)
        # ansys.l(1, 2)#两点连线
        # ansys.l(2, 3)
        # ansys.l(3, 1)
        # #ansys.l(4, 1)
        # ansys.al(1, 2, 3)
        #ansys.parain("1", "x_t", "F:/solidworks ansys/examp", "SOLIDS", "0", "0", )
        ansys.parain("5XS363011", "x_t", "F:\\solidworks ansys\\solidworkstoxtresult\\", "SOLIDS", "0", "0", )

        ansys.facet()
        ansys.view(1, 1, 1, 1)
        ansys.angle(1)

        ansys.vplot()
        # grid = pv.UnstructuredGrid('F:\\solidworks ansys\\solidworkstoxtresult\\2.x_t')
        # grid.plot()
        # ansys.facet()
        # plt.show()
        ansys.save()
        ansys.exit()
        # filename = examples.TEST11  # 打开sample里的cdb文件
        # # examples.show_hex_archive()
        # examples.ansys_cylinder_demo()
        # # Read ansys archive file
        # archive = pyansys.Archive(filename)
        #
        # # Print raw data from cdb#打印cdb文件里初始数据
        # for key in archive.raw:
        #     print("%s : %s" % (key, archive.raw[key]))
        #
        # # Create a vtk unstructured grid from the raw data and plot it
        # grid = archive.parse_vtk(force_linear=True)
        # grid.plot(color='r', show_edges=True)
        #
        # # write this as a vtk xml file
        # grid.save('hex.vtu')
        #
        # # or as a vtk binary
        # grid.save('hex.vtk')
        #path = os.getcwd()
        #ansys = pyansys.Mapdl(run_location=path, interactive_plotting=True)

        # create a square area using keypoints
        #ansys.prep7()  # 前处理
        # ansys.k(1, 0, 0, 0)  # 点坐标（编号，三维）
        # ansys.k(2, 1, 0, 0)
        # ansys.k(3, 1, 1, 0)
        # # ansys.k(4, 0, 1, 0)
        # ansys.l(1, 2)  # 两点连线
        # ansys.l(2, 3)
        # ansys.l(3, 1)
        # # ansys.l(4, 1)
        # ansys.al(1, 2, 3)
        # ansys.aplot()
        # # plt.show()
        # ansys.save()
        # ansys.exit()
        #ansys.parain(self, "1", "x_t", "F:/solidworks ansys/examp", "SOLIDS", "0", "0", )
        #ansys.aplot()
        #ansys.save()
        #ansys.exit()

        #print(grid.type)
        print("hello,type")
    def saveas_xt_and_showin_ansys_function(self):
        # all_file = os.listdir('F:\\solidworks ansys\\solidworkstoxt\\')
        swYearLastDigit = 8  # sw 2014
        swApp = win32com.client.DispatchEx("SldWorks.Application.%d" % (20 + (swYearLastDigit - 2)))
         # swApp = win32com.client.Dispatch('SldWorks.Application')
        swApp.Visible = 1###solidworks软件可视化
        print("SwFilename="+SwFileName)

        #print("format type is"+type(swfile_format))
        Model = swApp.OpenDoc(SwFileName, swfile_format)
        print("format=" + str(swfile_format))
        #ModelnameSplit = Model.split('.')
        SwFileNameSplit = SwFileName.split("/")
        Model_name = ""
        print(SwFileNameSplit)
        SwFileNameSplit = SwFileNameSplit[len(SwFileNameSplit)-1].split(".")
        print(SwFileNameSplit)
        for i in range(len(SwFileNameSplit) - 1):
            Model_name = Model_name + SwFileNameSplit[i]+'.'
        Model_name = Model_name + 'x_t'
        print("Model_name:"+Model_name)
        result = Model.SaveAs('F:\\solidworks ansys\\solidworkstoxtresult\\'+Model_name)
        #swApp.CloseAllDocuments(True)
        Modelname_xt_to_ansys= Model_name[:-4]
        print(Modelname_xt_to_ansys)


        #swApp.ExitApp()
        path = os.getcwd()
        ansys = pyansys.Mapdl(run_location=path, interactive_plotting=True)

        # create a square area using keypoints
        ansys.prep7()  # 前处理
        ansys.parain(Modelname_xt_to_ansys, "x_t", "F:\\solidworks ansys\\solidworkstoxtresult\\", "SOLIDS", "0", "0", )

        ansys.facet()
        ansys.view(1, 1, 1, 1)
        ansys.angle(1)

        ansys.vplot()
        # grid = pv.UnstructuredGrid('F:\\solidworks ansys\\solidworkstoxtresult\\2.x_t')
        # grid.plot()
        # ansys.facet()
        # plt.show()
        ansys.save()
        ansys.exit()
    def calcuate_ansys_prcoess(self):
        path = "F:\\solidworks ansys\\comsol file"
        datanames = os.listdir(path)
        #self.Simu_progressBar.setValue(25)
        for i in datanames:
            name1 = os.path.splitext(i)
            # print(name1[1])
            if self.simu_model_device_number.currentText() == name1[0] and name1[1] == '.mph':
                # client = mph.start()
                # print('ok1'+self.simu_model_device_number.currentText())
                model = client.load('F:\\solidworks ansys\\comsol file\\' + i)
        model.parameter('Voltage', self.model_workvoltage_edit.text())
        model.parameter('Current', self.model_workcurrent_edit.text())
        model.parameter('Temp', self.model_environmenttemp_edit.text())
        model.parameter('Pressure', self.model_environpressure_edit.text())
        model.build()
        model.mesh()
        model.solve()
        #model.save()
        model.export('dianshi', 'dianshishow.jpg')
        model.export('dianchang', 'dianchangshow.jpg')
        model.export('dianshivtu', 'dianshi3Dshow.vtu')
        model.export('dianchangvtu', 'dianchang3Dshow.vtu')
        self.Simu_progressBar.setValue(100)
        model.clear()
        # if self.model_workcurrent_edit.text() =="":
        #     QMessageBox.warning(self, "警告", "工作电流值为空，请检查")
        # else:
        #     model_workcurrent = float(self.model_workcurrent_edit.text())
        #
        #     path = os.getcwd()
        #     # ansys = pyansys.Mapdl(run_location="E:/ansys/pycharmansys", jobname='file20200317', nproc=6, interactive_plotting=True)
        #     ansys = pyansys.Mapdl(run_location=path, nproc=2)
        #     # create a square area using keypoints
        #     ansys.prep7()  # 前处理
        #     # ansys.run("kggtest1", mode='w')
        #     ansys.run("~PARAIN,'daotibufen','x_t','F:/3/',SOLIDS,0,0   ")
        #     ansys.run("/NOPR   ")
        #     ansys.run("/GO ")
        #     ansys.run("/REPLOT,RESIZE  ")
        #     ansys.run("/facet  ")
        #     ansys.run("BLOCK,1.6499957,0.3,0.5,-1.5,2.2035,-0.1,   ")
        #     ansys.run("VSEL,U, , ,     594 ")
        #     ansys.run("FLST,2,593,6,ORDE,2 ")
        #     ansys.run("FITEM,2,1   ")
        #     ansys.run("FITEM,2,-593")
        #     ansys.run("VGLUE,P51X  ")
        #     ansys.run("numcmp,all  ")
        #     ansys.run("ALLSEL,ALL  ")
        #     ansys.run("FLST,2,594,6,ORDE,2 ")
        #     ansys.run("FITEM,2,1   ")
        #     ansys.run("FITEM,2,-594")
        #     ansys.run("VOVLAP,P51X ")
        #     ansys.run("numcmp,all  ")
        #     ansys.run("!*  ")
        #     ansys.run("ET,1,SOLID236   ")
        #     ansys.run("!*  ")
        #     ansys.run("ET,2,SOLID236   ")
        #     ansys.run("!*  ")
        #     ansys.run("ET,3,SOLID236   ")
        #     ansys.run("!*  ")
        #     ansys.run("ET,4,SOLID236   ")
        #     ansys.run("!*  ")
        #     ansys.run("ET,5,SOLID236   ")
        #     ansys.run("!*  ")
        #     ansys.run("ET,6,SOLID236   ")
        #     ansys.run("!*  ")
        #     ansys.run("ET,7,SOLID236   ")
        #     ansys.run("!*  ")
        #     ansys.run("KEYOPT,1,1,1")
        #     ansys.run("KEYOPT,1,2,0")
        #     ansys.run("KEYOPT,1,5,0")
        #     ansys.run("KEYOPT,1,7,0")
        #     ansys.run("KEYOPT,1,8,0")
        #     ansys.run("!*  ")
        #     ansys.run("KEYOPT,2,1,1")
        #     ansys.run("KEYOPT,2,2,0")
        #     ansys.run("KEYOPT,2,5,0")
        #     ansys.run("KEYOPT,2,7,0")
        #     ansys.run("KEYOPT,2,8,0")
        #     ansys.run("!*  ")
        #     ansys.run("KEYOPT,3,1,1")
        #     ansys.run("KEYOPT,3,2,0")
        #     ansys.run("KEYOPT,3,5,0")
        #     ansys.run("KEYOPT,3,7,0")
        #     ansys.run("KEYOPT,3,8,0")
        #     ansys.run("!*  ")
        #     ansys.run("KEYOPT,4,1,1")
        #     ansys.run("KEYOPT,4,2,0")
        #     ansys.run("KEYOPT,4,5,0")
        #     ansys.run("KEYOPT,4,7,0")
        #     ansys.run("KEYOPT,4,8,0")
        #     ansys.run("!*  ")
        #     ansys.run("KEYOPT,5,1,1")
        #     ansys.run("KEYOPT,5,2,0")
        #     ansys.run("KEYOPT,5,5,0")
        #     ansys.run("KEYOPT,5,7,0")
        #     ansys.run("KEYOPT,5,8,0")
        #     ansys.run("!*  ")
        #     ansys.run("KEYOPT,6,1,1")
        #     ansys.run("KEYOPT,6,2,0")
        #     ansys.run("KEYOPT,6,5,0")
        #     ansys.run("KEYOPT,6,7,0")
        #     ansys.run("KEYOPT,6,8,0")
        #     ansys.run("!*  ")
        #     ansys.run("!*  ")
        #     ansys.run("MPTEMP,,,,,,,,  ")
        #     ansys.run("MPTEMP,1,0  ")
        #     ansys.run("MPDATA,MURX,1,,1")
        #     ansys.run("MPTEMP,,,,,,,,  ")
        #     ansys.run("MPTEMP,1,0  ")
        #     ansys.run("MPDATA,RSVX,1,,1.777462e-8  ")
        #     ansys.run("MPTEMP,,,,,,,,  ")
        #     ansys.run("MPTEMP,1,0  ")
        #     ansys.run("MPDATA,MURX,2,,1")
        #     ansys.run("MPTEMP,,,,,,,,  ")
        #     ansys.run("MPTEMP,1,0  ")
        #     ansys.run("MPDATA,RSVX,2,,1.65e-8  ")
        #     ansys.run("MPTEMP,,,,,,,,  ")
        #     ansys.run("MPTEMP,1,0  ")
        #     ansys.run("MPDATA,MURX,3,,1")
        #     ansys.run("MPTEMP,,,,,,,,  ")
        #     ansys.run("MPTEMP,1,0  ")
        #     ansys.run("MPDATA,RSVX,3,,7.496e-8 ")
        #     ansys.run("MPTEMP,,,,,,,,  ")
        #     ansys.run("MPTEMP,1,0  ")
        #     ansys.run("MPDATA,MURX,4,,1")
        #     ansys.run("MPTEMP,,,,,,,,  ")
        #     ansys.run("MPTEMP,1,0  ")
        #     ansys.run("MPDATA,RSVX,4,,7.0922e-8")
        #     ansys.run("MPTEMP,,,,,,,,  ")
        #     ansys.run("MPTEMP,1,0  ")
        #     ansys.run("MPDATA,MURX,5,,1")
        #     ansys.run("FLST,5,246,6,ORDE,4 ")
        #     ansys.run("FITEM,5,16  ")
        #     ansys.run("FITEM,5,-256")
        #     ansys.run("FITEM,5,263 ")
        #     ansys.run("FITEM,5,-267")
        #     ansys.run("CM,_Y,VOLU  ")
        #     ansys.run("VSEL, , , ,P51X ")
        #     ansys.run("CM,_Y1,VOLU ")
        #     ansys.run("CMSEL,S,_Y  ")
        #     ansys.run("!*  ")
        #     ansys.run("CMSEL,S,_Y1 ")
        #     ansys.run("VATT,       2, ,   2,       0   ")
        #     ansys.run("CMSEL,S,_Y  ")
        #     ansys.run("CMDELE,_Y   ")
        #     ansys.run("CMDELE,_Y1  ")
        #     ansys.run("!*  ")
        #     ansys.run("FLST,5,6,6,ORDE,2   ")
        #     ansys.run("FITEM,5,551 ")
        #     ansys.run("FITEM,5,-556")
        #     ansys.run("CM,_Y,VOLU  ")
        #     ansys.run("VSEL, , , ,P51X ")
        #     ansys.run("CM,_Y1,VOLU ")
        #     ansys.run("CMSEL,S,_Y  ")
        #     ansys.run("!*  ")
        #     ansys.run("CMSEL,S,_Y1 ")
        #     ansys.run("VATT,       3, ,   3,       0   ")
        #     ansys.run("CMSEL,S,_Y  ")
        #     ansys.run("CMDELE,_Y   ")
        #     ansys.run("CMDELE,_Y1  ")
        #     ansys.run("!*  ")
        #     ansys.run("FLST,5,9,6,ORDE,5   ")
        #     ansys.run("FITEM,5,13  ")
        #     ansys.run("FITEM,5,-15 ")
        #     ansys.run("FITEM,5,572 ")
        #     ansys.run("FITEM,5,-576")
        #     ansys.run("FITEM,5,593 ")
        #     ansys.run("CM,_Y,VOLU  ")
        #     ansys.run("VSEL, , , ,P51X ")
        #     ansys.run("CM,_Y1,VOLU ")
        #     ansys.run("CMSEL,S,_Y  ")
        #     ansys.run("!*  ")
        #     ansys.run("CMSEL,S,_Y1 ")
        #     ansys.run("VATT,       4, ,   4,       0   ")
        #     ansys.run("CMSEL,S,_Y  ")
        #     ansys.run("CMDELE,_Y   ")
        #     ansys.run("CMDELE,_Y1  ")
        #     ansys.run("!*  ")
        #     ansys.run("FLST,5,6,6,ORDE,5   ")
        #     ansys.run("FITEM,5,561 ")
        #     ansys.run("FITEM,5,-562")
        #     ansys.run("FITEM,5,569 ")
        #     ansys.run("FITEM,5,-571")
        #     ansys.run("FITEM,5,592 ")
        #     ansys.run("CM,_Y,VOLU  ")
        #     ansys.run("VSEL, , , ,P51X ")
        #     ansys.run("CM,_Y1,VOLU ")
        #     ansys.run("CMSEL,S,_Y  ")
        #     ansys.run("!*  ")
        #     ansys.run("CMSEL,S,_Y1 ")
        #     ansys.run("VATT,       1, ,   5,       0   ")
        #     ansys.run("CMSEL,S,_Y  ")
        #     ansys.run("CMDELE,_Y   ")
        #     ansys.run("CMDELE,_Y1  ")
        #     ansys.run("!*  ")
        #     ansys.run("FLST,5,246,6,ORDE,2 ")
        #     ansys.run("FITEM,5,295 ")
        #     ansys.run("FITEM,5,-540")
        #     ansys.run("CM,_Y,VOLU  ")
        #     ansys.run("VSEL, , , ,P51X ")
        #     ansys.run("CM,_Y1,VOLU ")
        #     ansys.run("CMSEL,S,_Y  ")
        #     ansys.run("!*  ")
        #     ansys.run("CMSEL,S,_Y1 ")
        #     ansys.run("VATT,       1, ,   6,       0   ")
        #     ansys.run("CMSEL,S,_Y  ")
        #     ansys.run("CMDELE,_Y   ")
        #     ansys.run("CMDELE,_Y1  ")
        #     ansys.run("!*  ")
        #     ansys.run("CM,_Y,VOLU  ")
        #     ansys.run("VSEL, , , ,     594 ")
        #     ansys.run("CM,_Y1,VOLU ")
        #     ansys.run("CMSEL,S,_Y  ")
        #     ansys.run("!*  ")
        #     ansys.run("CMSEL,S,_Y1 ")
        #     ansys.run("VATT,       5, ,   7,       0   ")
        #     ansys.run("CMSEL,S,_Y  ")
        #     ansys.run("CMDELE,_Y   ")
        #     ansys.run("CMDELE,_Y1  ")
        #     ansys.run("!*  ")
        #     ansys.run("SMRT,6  ")
        #     ansys.run("SMRT,7  ")
        #     ansys.run("SMRT,8  ")
        #     ansys.run("MSHAPE,1,3D ")
        #     ansys.run("MSHKEY,0")
        #     ansys.run("!*  ")
        #     ansys.run("FLST,5,593,6,ORDE,2 ")
        #     ansys.run("FITEM,5,1   ")
        #     ansys.run("FITEM,5,-593")
        #     ansys.run("CM,_Y,VOLU  ")
        #     ansys.run("VSEL, , , ,P51X ")
        #     ansys.run("CM,_Y1,VOLU ")
        #     ansys.run("CHKMSH,'VOLU'   ")
        #     ansys.run("CMSEL,S,_Y  ")
        #     ansys.run("!*  ")
        #     ansys.run("VMESH,_Y1   ")
        #     ansys.run("!*  ")
        #     ansys.run("CMDELE,_Y   ")
        #     ansys.run("CMDELE,_Y1  ")
        #     ansys.run("CMDELE,_Y2  ")
        #     ansys.run("!*  ")
        #     ansys.run("ESIZE,0.250,0,  ")
        #     ansys.run("FLST,2,6250,5,ORDE,2")
        #     ansys.run("FITEM,2,1   ")
        #     ansys.run("FITEM,2,-6250   ")
        #     ansys.run("AESIZE,P51X,0.22,   ")
        #     ansys.run("FLST,5,12,4,ORDE,2  ")
        #     ansys.run("FITEM,5,11734   ")
        #     ansys.run("FITEM,5,-11745  ")
        #     ansys.run("CM,_Y,LINE  ")
        #     ansys.run("LSEL, , , ,P51X ")
        #     ansys.run("CM,_Y1,LINE ")
        #     ansys.run("CMSEL,,_Y   ")
        #     ansys.run("!*  ")
        #     ansys.run("LESIZE,_Y1,0.2, , , , , , ,1")
        #     ansys.run("!*  ")
        #     ansys.run("CM,_Y,VOLU  ")
        #     ansys.run("VSEL, , , ,     594 ")
        #     ansys.run("CM,_Y1,VOLU ")
        #     ansys.run("CHKMSH,'VOLU'   ")
        #     ansys.run("CMSEL,S,_Y  ")
        #     ansys.run("!*  ")
        #     ansys.run("VMESH,_Y1   ")
        #     ansys.run("!*  ")
        #     ansys.run("CMDELE,_Y   ")
        #     ansys.run("CMDELE,_Y1  ")
        #     ansys.run("CMDELE,_Y2  ")
        #     ansys.run("!*  ")
        #     ansys.run("/solu")
        #     ansys.run("esel,s,type,,1")
        #     ansys.run("esel,a,type,,2")
        #     ansys.run("esel,a,type,,3")
        #     ansys.run("esel,a,type,,4")
        #     ansys.run("esel,a,type,,5")
        #     ansys.run("esel,a,type,,6")
        #     ansys.run("esel,a,type,,7")
        #     ansys.run("nsel,s,ext")
        #     ansys.run("d,all,az,0")
        #     ansys.run("vsel,all")
        #     ansys.run("asel,s,,,3")
        #     ansys.run("nsla,s,1")
        #     ansys.run("cp,1,volt,all")
        #     ansys.run("*get,n1,node,,num,min")
        #     ansys.f("n1", "AMPS", model_workcurrent)
        #     #ansys.run("f,n1,amps,'model_workcurrent'")
        #     ansys.run("vsel,all")
        #     ansys.run("asel,s,,,15")
        #     ansys.run("nsla,s,1")
        #     ansys.run("cp,2,volt,all")
        #     ansys.run("*get,n2,node,,num,min")
        #     ansys.f("n2", "AMPS", -model_workcurrent*0.5, model_workcurrent*0.866)
        #     #ansys.run("f,n2,amps,-3465*0.5,3465*0.866")
        #
        #     ansys.run("vsel,all")
        #     ansys.run("asel,s,,,18")
        #     ansys.run("nsla,s,1")
        #     ansys.run("cp,3,volt,all")
        #     ansys.run("*get,n3,node,,num,min")
        #     ansys.f("n3", "AMPS", -model_workcurrent * 0.5, -model_workcurrent * 0.866)
        #     #ansys.run("f,n3,amps,-3465*0.5,-3465*0.866")
        #
        #     ansys.run("vsel,all")
        #     ansys.run("asel,s,,,6")
        #     ansys.run("nsla,s,1")
        #     ansys.run("d,all,volt,0")
        #
        #     ansys.run("vsel,all")
        #     ansys.run("asel,s,,,9")
        #     ansys.run("nsla,s,1")
        #     ansys.run("d,all,volt,0")
        #
        #     ansys.run("vsel,all")
        #     ansys.run("asel,s,,,12")
        #     ansys.run("nsla,s,1")
        #     ansys.run("d,all,volt,0")
        #     ansys.run("vsel,s,type,,1")
        #     ansys.run("nslv,s,1")
        #     ansys.run("eslv,s")
        #     ansys.run("nsle")
        #     ansys.run("bfe,all,fvin,,0,1")
        #
        #     ansys.run("vsel,s,type,,2")
        #     ansys.run("nslv,s,1")
        #     ansys.run("eslv,s")
        #     ansys.run("nsle")
        #     ansys.run("bfe,all,fvin,,0,2")
        #
        #     ansys.run("vsel,s,type,,3")
        #     ansys.run("nslv,s,1")
        #     ansys.run("eslv,s")
        #     ansys.run("nsle")
        #     ansys.run("bfe,all,fvin,,0,3")
        #
        #     ansys.run("vsel,s,type,,4")
        #     ansys.run("nslv,s,1")
        #     ansys.run("eslv,s")
        #     ansys.run("nsle")
        #     ansys.run("bfe,all,fvin,,0,4")
        #
        #     ansys.run("vsel,s,type,,5")
        #     ansys.run("nslv,s,1")
        #     ansys.run("eslv,s")
        #     ansys.run("nsle")
        #     ansys.run("bfe,all,fvin,,0,5")
        #
        #     ansys.run("vsel,s,type,,6")
        #     ansys.run("nslv,s,1")
        #     ansys.run("eslv,s")
        #     ansys.run("nsle")
        #     ansys.run("bfe,all,fvin,,0,6")
        #     ansys.run("/solu")
        #     ansys.run("antype,harmic,new")
        #     ansys.run("harfrq,50")
        #     ansys.run("eqslv,sparse")
        #     ansys.run("allsel,all")
        #     ansys.run("solve")
        #     ansys.run("finish")
        #     ansys.run("/post1")
        #     ansys.run("exun,volu,disp,comm,si")
        #     ansys.run("exun,volu,hgen,comm,si")
        #     ansys.run("expr,volu,hgen,1,'heat1',CFXcu,csv")
        #     ansys.run("expr,volu,hgen,2,'heat2',CFXag,csv")
        #     ansys.run("expr,volu,hgen,3,'heat3',CFXfe,csv")
        #     ansys.run("expr,volu,hgen,4,'heat4',CFXcucr,csv")
        #     ansys.run("expr,volu,hgen,5,'heat5',CFXmiecu,csv")
        #     ansys.run("expr,volu,hgen,6,'heat6',CFXchuzhi,csv")
        #     # path = os.getcwd()
        #     # ansys = pyansys.Mapdl(run_location=path, interactive_plotting=True)
        #     # ansys.prep7()  # 前处理
        #     # ansys.parain("1", "x_t", "F:/solidworks ansys/examp", "SOLIDS", "0", "0", )
        #     # ansys.nopr()
        #     # ansys.slashgo()
        #     # ansys.facet()
        #     # # ansys.view(1,1,1,1)#view(self, wn="", xv="", yv="", zv="", **kwargs)
        #     # ###############建立工作平面和空气域#####################
        #     # ansys.block(-0.01, 0.01, -0.01, 0.01, 0, 0.01)
        #     # # ansys.vplot()##这一步没问题
        #     # ansys.dist(1, 0.019)
        #     # # ansys.dist(1,0.02,0)##dist(self, wn="窗口号", dval="0.05-3之间数越小，体积越大，数越大，体积越小", kfact="", **kwargs)放大缩小(0.05-2)
        #     # ansys.angle(1, 4.2)
        #     # # ansys.angle(1,4.2,"ZS",1)##angle(self, wn="窗口号，默认为1", theta="角度大小", axis="绕哪个轴旋转", kincr="", **kwargs):旋转角度
        #     # # ansys.vplot()##这一步没问题
        #     # ansys.numcmp("ALL")  ##所有统一编号
        #     # # ansys.vplot()##这一步没问题
        #     # ##############进行布尔运算######################
        #     # ansys.flst(2, 2, 6, "ORDER",
        #     #            2)  ##flst(self, nfield="", narg="", type="6 - Volume numbers", otype="ORDER - Data is in an ordered list", leng="Length of number of items describing the list", **kwargs):
        #     # ansys.fitem(2, 1)  ##fitem(self, nfield="", item="", itemy="", itemz="", **kwargs
        #     # ansys.fitem(2, -2)
        #     # ansys.vovlap(
        #     #     "P51X")  # vovlap(self, nv1="", nv2="", nv3="", nv4="", nv5="", nv6="", nv7="", nv8="", nv9="", **kwargs):
        #     # ansys.numcmp("ALL")
        #     #
        #     # # ansys.vplot()
        #     # # ansys.dist(1,1.082226,1)
        #     # ##############设计单元与材料属性#######################
        #     # ansys.et(1, "SOLID236")  ##et(self, itype="", ename="", kop1="", kop2="", kop3="", kop4="", kop5="", kop6="", inopr="", **kwargs):
        #     # ansys.keyopt(1, 1, 1)  ##keyopt(self, itype="", knum="", value="", **kwargs):
        #     # ansys.keyopt(1, 2, 0)
        #     # ansys.keyopt(1, 5, 0)
        #     # ansys.keyopt(1, 7, 0)
        #     # ansys.keyopt(1, 8, 0)
        #     # ansys.et(2, "SOLID236")
        #     # ansys.keyopt(2, 1, 0)
        #     # ansys.keyopt(2, 2, 0)
        #     # ansys.keyopt(2, 5, 0)
        #     # ansys.keyopt(2, 7, 0)
        #     # ansys.keyopt(2, 8, 0)
        #     # ##ansys.vplot()##这一步没有问题
        #     # ansys.mptemp("", "", "", "", "", "", "")  ##mptemp(self, sloc="", t1="", t2="", t3="", t4="", t5="", t6="",**kwargs)
        #     # ansys.mptemp(1, 0)
        #     # ansys.mpdata("MURX", 1, "", 1)  ##mpdata(self, lab="MURX - Magnetic relative permeabilities (also MURY, MURZ).", mat="", sloc="", c1="", c2="", c3="", c4="", c5="", c6="", **kwargs):
        #     # ansys.mptemp("", "", "", "", "", "", "")
        #     # ansys.mptemp(1, 0)
        #     # ansys.mpdata("RSVX", 1, "", 1.75e-8)  ##mpdata(self, lab="RSVX - Electrical resistivities (also RSVY, RSVZ).", mat="", sloc="", c1="", c2="", c3="", c4="", c5="", c6="", **kwargs):
        #     # ansys.mptemp("", "", "", "", "", "", "")  ##mptemp(self, sloc="", t1="", t2="", t3="", t4="", t5="", t6="",**kwargs)
        #     # ansys.mptemp(1, 0)
        #     # ansys.mpdata("MURX", 2, "", 1)  ##mpdata(self, lab="MURX - Magnetic relative permeabilities (also MURY, MURZ).", mat="", sloc="", c1="", c2="", c3="", c4="", c5="", c6="", **kwargs):
        #     # ansys.mptemp("", "", "", "", "", "", "")
        #     # ansys.mptemp(1, 0)
        #     # ansys.mpdata("RSVX", 2, "", )  ##mpdata(self, lab="RSVX - Electrical resistivities (also RSVY, RSVZ).", mat="", sloc="", c1="", c2="", c3="", c4="", c5="", c6="", **kwargs):
        #     # # ansys.vplot()##这一步没问题#这一步下面有点问题
        #     # # ansys.menu("ON")
        #     # ##################给每个体分别赋予单元与材料##############
        #     # ansys.cm("_Y", "VOLU")  ##Groups geometry items into a component.cm(self, cname="", entity="VOLU - Volumes.", **kwargs):
        #     # ansys.vsel("", "", "", 1)  ##vsel(self, type="", item="", comp="", vmin="1", vmax="", vinc="", kswp="", **kwargs):
        #     # ansys.cm("_Y1", "VOLU")  ##cm(self, cname="", entity="VOLU - Volumes.", **kwargs):
        #     # ansys.cmsel("S", "_Y")  ##cmsel(self, type="S - Select a new set (default).", name="", entity="", **kwargs):
        #     # ansys.cmsel("S", "_Y1")
        #     # ansys.vatt(1, "", 1, 0)  ##vatt(self, mat="", real="", type="", esys="", secnum="", **kwargs):
        #     # ansys.cmsel("S", "_Y")
        #     # ansys.cmdele("_Y")  ##Deletes a component or assembly definition.cmdele(self, name="", **kwargs):
        #     # ansys.cmdele("_Y1")
        #     # ansys.cm("_Y", "VOLU")  ##Groups geometry items into a component.cm(self, cname="", entity="VOLU - Volumes.", **kwargs):
        #     # ansys.vsel("", "", "", 2)  ##vsel(self, type="", item="", comp="", vmin="2", vmax="", vinc="", kswp="", **kwargs):
        #     # ansys.cm("_Y1", "VOLU")  ##cm(self, cname="", entity="VOLU - Volumes.", **kwargs):
        #     # ansys.cmsel("S", "_Y")
        #     # ansys.cmsel("S", "_Y1")
        #     # ansys.vatt(2, "", 2, 0)  ##vatt(self, mat="", real="", type="", esys="", secnum="", **kwargs):
        #     # ansys.cmsel("S", "_Y")
        #     # ansys.cmdele("_Y")
        #     # ansys.cmdele("_Y1")
        #     # # ansys.vplot()##这一步没问题#这一步是紫绿图
        #     # # ansys.menu("ON")
        #     # ##########网格划分###############################
        #     # ansys.smrtsize(2)  ##smrtsize(self, sizlvl="2", fac="", expnd="", trans="", angl="", angh="", gratio="", smhlc="", smanc="", mxitr="", sprx="", **kwargs):
        #     # ansys.mshape(1, "3D")  ##mshape(self, key="1 - Mesh with triangle-shaped elements when Dimension = 2-D mesh with tetrahedral-shaped elements when Dimension = 3-D.", dimension="3D - 3-D model (volume mesh)", **kwargs):
        #     # ansys.mshkey(0)  ##mshkey(self, key="0 - Use free meshing (the default).", **kwargs):
        #     # ansys.flst(5, 2, 6, "ORDER", 2)  ##Specifies data required for a picking operation (GUI).flst(self, nfield="5", narg="2", type="6 - Volume numbers", otype="ORDER - Data is in an ordered list (such as for the E,P51X and A,P51X commands, in which the order of the data items is significant for the picking operation).", leng="2", **kwargs):
        #     # ansys.fitem(5, 1)  ##fitem(self, nfield="", item="", itemy="", itemz="", **kwargs):
        #     # ansys.fitem(5, -2)
        #     # ansys.cm("_Y", "VOLU")
        #     # ansys.vsel("", "", "", "P51X")
        #     # ansys.cm("_Y1", "VOLU")
        #     # ansys.chkmsh("'VOLU'")  # chkmsh(self, comp="", **kwargs)
        #     # ansys.cmsel("S", "_Y")
        #     # ansys.vmesh("_Y1")  ##vmesh(self, nv1="", nv2="", ninc="", **kwargs):
        #     # ansys.cmdele("_Y")
        #     # ansys.cmdele("_Y1")
        #     # ansys.cmdele("_Y2")
        #     # # ansys.ui("MESH","OFF")
        #     # # ansys.vplot()##这一步没问题##这一步没有网格图
        #     # ansys.finish()  ## Exits normally from a processor.finish(self, **kwargs):
        #     # #################设置边界条件与添加激励源#######################
        #     #
        #     # ansys.slashsolu()  ##Enters the solution processor.slashsolu(self, **kwargs):
        #     # ansys.esel("S", "type", "", 1)  ##esel(self, type="S - Select a new set (default).", item="type", comp="", vmin="1", vmax="", vinc="", kabs="", **kwargs):
        #     # ansys.esel("A", "type", "", 2)  ##esel(self, type=" A - Additionally select a set and extend the current set.", item="type", comp="", vmin="2", vmax="", vinc="", kabs="", **kwargs):
        #     # ansys.nsel("S", "EXT")  ##nsel(self, type="S - Select a new set (default).", item="", comp="", vmin="", vmax="", vinc="", kabs="", **kwargs):
        #     # ansys.d("ALL", "AZ", 0)  ##d(self, node="", lab="", value="", value2="", nend="", ninc="", lab2="", lab3="", lab4="", lab5="", lab6="", **kwargs):
        #     # # ansys.vplot()
        #     #
        #     # ansys.vsel("ALL")
        #     # ansys.asel("S", "", "", 3)
        #     # ansys.nsla("S", 1)
        #     # ansys.cp(1, "VOLT", "ALL")  # cp(self, nset="", lab="VOLT(voltage)", node1="", node2="", node3="", node4="", node5="", node6="", node7="", node8="", node9="", node10="", node11="", node12="", node13="", node14="", node15="", node16="", node17="", **kwargs):
        #     # ansys.get("n1", "NODE", "", "num", "min")  ##get(self, par="n1", entity="NODE", entnum="", item1="num", it1num="min", item2="", it2num="", **kwargs):
        #     # ansys.f("n1", "AMPS", model_workcurrent)  ##f(self, node="n1", lab="AMPS", value="100", value2="", nend="", ninc="", **kwargs):
        #     # ansys.vsel("ALL")
        #     # ansys.asel("S", "", "", 4)
        #     # ansys.nsla("S", 1)
        #     # ansys.d("ALL", "VOLT", 0)
        #     # # #ansys.vplot()
        #     #
        #     # ansys.vsel("S", "type", "", 1)
        #     # ansys.nslv("S", 1)  ##nslv(self, type="S - Select a new set (default).", nkey="1 - Select all nodes (interior to volume, interior to areas, interior to lines, and at keypoints) associated with the selected volumes.", **kwargs):
        #     # ansys.eslv("S")  ##eslv(self, type="S - Select a new set (default).", **kwargs):
        #     # ansys.nsle()  ##nsle(self, type="", nodetype="", num="", **kwargs):
        #     # ansys.bfe("ALL", "fvin", "", 0, 1)  ##bfe(self, elem="", lab="", stloc="", val1="", val2="", val3="", val4="", **kwargs):
        #     # # ansys.vplot()
        #     # ##############设置谐态求解器进行求解##################33
        #     #
        #     # ansys.slashsolu()
        #     # ansys.antype("HARMIC", "NEW")  ##antype(self, antype=" HARMIC or 3 - Perform a harmonic analysis.  Valid for structural, fluid, magnetic, and electrical degrees of freedom.", status="NEW - Specifies a new analysis (default). If NEW, the remaining fields on this command are ignored.", ldstep="", substep="", action="", **kwargs):
        #     # ansys.harfrq(50)  ##harfrq(self, freqb="50", freqe="", logopt="", freqarr="", toler="", **kwargs):
        #     # ansys.eqslv("SPARSE")  ##eqslv(self, lab="SPARSE - Sparse direct equation solver. ", toler="", mult="", keepfile="", **kwargs):
        #     # ansys.allsel("ALL")  ##allsel(self, labt=" ALL - Selects all items of the specified entity type and all items of lower entity types (default).", entity="", **kwargs):
        #     # # ansys.aplot()
        #     # # ansys.vplot()
        #     # ansys.solve()  ##solve(self, action="", **kwargs):
        #     # ansys.finish()  #### Exits normally from a processor.finish(self, **kwargs):
        #     # # ansys.vplot()
        #     #
        #     # #############后处理#################################
        #     #
        #     # ansys.post1()  ##post1(self, **kwargs):
        #     # ansys.exunit("VOLU", "DISP", "COMM", "SI")  ##exunit(self, ldtype="", load="", untype="", name="", **kwargs):
        #     # ansys.exunit("VOLU", "HGEN", "COMM", "SI")  ##没有hgen
        #     # ansys.exprofile("VOLU", "HGEN", 1, "heat1", "CFXcu", "csv")  ##没有hgen
        #     # # ansys.save()
        #     # ansys.plesol("JHEAT", "SUM", 0)
        #     # # ansys.plnsol()
        #     # ansys.exit()
###################################另一个元件的仿真#########################33
            #model_workcurrent = float(self.model_workcurrent_edit.text())
            # path = os.getcwd()
            # ansys = pyansys.Mapdl(run_location=path, interactive_plotting=True)
            # ansys.prep7()  # 前处理
            # ansys.parain("daotibufen", "x_t", "F:/solidworks ansys/examp", "SOLIDS", "0", "0", )
            # ansys.nopr()
            # ansys.slashgo()
            # ansys.facet()
            # # ansys.view(1,1,1,1)#view(self, wn="", xv="", yv="", zv="", **kwargs)
            # ###############建立工作平面和空气域#####################
            # ansys.block(1.6499957, 0.3, 0.5, -1.5, 2.2035, -0.1,)
            # # ansys.vplot()##这一步没问题
            # ansys.dist(1, 0.019)
            # # ansys.dist(1,0.02,0)##dist(self, wn="窗口号", dval="0.05-3之间数越小，体积越大，数越大，体积越小", kfact="", **kwargs)放大缩小(0.05-2)
            # ansys.angle(1, 4.2)
            # # ansys.angle(1,4.2,"ZS",1)##angle(self, wn="窗口号，默认为1", theta="角度大小", axis="绕哪个轴旋转", kincr="", **kwargs):旋转角度
            # # ansys.vplot()##这一步没问题
            # #ansys.numcmp("ALL")  ##所有统一编号
            # # ansys.vplot()##这一步没问题
            # ansys.vsel("U", "","",594)#####
            # ##############进行布尔运算######################
            # ansys.flst(2, 593, 6, "ORDER",
            #            2)  ##flst(self, nfield="", narg="", type="6 - Volume numbers", otype="ORDER - Data is in an ordered list", leng="Length of number of items describing the list", **kwargs):
            # ansys.fitem(2, 1)  ##fitem(self, nfield="", item="", itemy="", itemz="", **kwargs
            # ansys.fitem(2, -593)
            # ansys.vglue("P51X")  # vovlap(self, nv1="", nv2="", nv3="", nv4="", nv5="", nv6="", nv7="", nv8="", nv9="", **kwargs):
            # ansys.numcmp("ALL")
            # ansys.allsel("ALL")
            # ansys.flst(2, 594, 6, "ORDER",
            #            2)
            # ansys.fitem(2, 1)  ##fitem(self, nfield="", item="", itemy="", itemz="", **kwargs
            # ansys.fitem(2, -594)
            # ansys.vovlap("P51X")
            # ansys.numcmp("ALL")
            #
            #
            #
            # # ansys.vplot()
            # # ansys.dist(1,1.082226,1)
            # ##############设计单元与材料属性#######################
            # ansys.et(1,
            #          "SOLID236")
            # ansys.et(2,
            #          "SOLID236")
            # ansys.et(3,
            #          "SOLID236")
            # ansys.et(4,
            #          "SOLID236")
            # ansys.et(5,
            #          "SOLID236")
            # ansys.et(6,
            #          "SOLID236")
            # ansys.et(7,
            #          "SOLID236")
            # ##et(self, itype="", ename="", kop1="", kop2="", kop3="", kop4="", kop5="", kop6="", inopr="", **kwargs):
            # ansys.keyopt(1, 1, 1)  ##keyopt(self, itype="", knum="", value="", **kwargs):
            # ansys.keyopt(1, 2, 0)
            # ansys.keyopt(1, 5, 0)
            # ansys.keyopt(1, 7, 0)
            # ansys.keyopt(1, 8, 0)
            # #ansys.et(2, "SOLID236")
            # ansys.keyopt(2, 1, 1)
            # ansys.keyopt(2, 2, 0)
            # ansys.keyopt(2, 5, 0)
            # ansys.keyopt(2, 7, 0)
            # ansys.keyopt(2, 8, 0)
            #
            # ansys.keyopt(3, 1, 1)  ##keyopt(self, itype="", knum="", value="", **kwargs):
            # ansys.keyopt(3, 2, 0)
            # ansys.keyopt(3, 5, 0)
            # ansys.keyopt(3, 7, 0)
            # ansys.keyopt(3, 8, 0)
            # # ansys.et(2, "SOLID236")
            # ansys.keyopt(4, 1, 1)
            # ansys.keyopt(4, 2, 0)
            # ansys.keyopt(4, 5, 0)
            # ansys.keyopt(4, 7, 0)
            # ansys.keyopt(4, 8, 0)
            #
            # ansys.keyopt(5, 1, 1)  ##keyopt(self, itype="", knum="", value="", **kwargs):
            # ansys.keyopt(5, 2, 0)
            # ansys.keyopt(5, 5, 0)
            # ansys.keyopt(5, 7, 0)
            # ansys.keyopt(5, 8, 0)
            # # ansys.et(2, "SOLID236")
            # ansys.keyopt(6, 1, 1)
            # ansys.keyopt(6, 2, 0)
            # ansys.keyopt(6, 5, 0)
            # ansys.keyopt(6, 7, 0)
            # ansys.keyopt(6, 8, 0)
            # ##ansys.vplot()##这一步没有问题
            # ansys.mptemp("", "", "", "", "", "",
            #              "", "")  ##mptemp(self, sloc="", t1="", t2="", t3="", t4="", t5="", t6="",**kwargs)
            # ansys.mptemp(1, 0)
            # ansys.mpdata("MURX", 1, "",
            #              1)  ##mpdata(self, lab="MURX - Magnetic relative permeabilities (also MURY, MURZ).", mat="", sloc="", c1="", c2="", c3="", c4="", c5="", c6="", **kwargs):
            # ansys.mptemp("", "", "", "", "", "", "", "")
            # ansys.mptemp(1, 0)
            # ansys.mpdata("RSVX", 1, "",
            #              1.777462e-8)  ##mpdata(self, lab="RSVX - Electrical resistivities (also RSVY, RSVZ).", mat="", sloc="", c1="", c2="", c3="", c4="", c5="", c6="", **kwargs):
            # ansys.mptemp("", "", "", "", "", "",
            #              "", "")  ##mptemp(self, sloc="", t1="", t2="", t3="", t4="", t5="", t6="",**kwargs)
            # ansys.mptemp(1, 0)
            # ansys.mpdata("MURX", 2, "",
            #              1)  ##mpdata(self, lab="MURX - Magnetic relative permeabilities (also MURY, MURZ).", mat="", sloc="", c1="", c2="", c3="", c4="", c5="", c6="", **kwargs):
            # ansys.mptemp("", "", "", "", "", "", "", "")
            # ansys.mptemp(1, 0)
            # ansys.mpdata("RSVX", 2,
            #              "", 1.65e-8)  ##mpdata(self, lab="RSVX - Electrical resistivities (also RSVY, RSVZ).", mat="", sloc="", c1="", c2="", c3="", c4="", c5="", c6="", **kwargs):
            #
            # ansys.mptemp("", "", "", "", "", "",
            #              "", "")  ##mptemp(self, sloc="", t1="", t2="", t3="", t4="", t5="", t6="",**kwargs)
            # ansys.mptemp(1, 0)
            # ansys.mpdata("MURX", 3, "",
            #              1)  ##mpdata(self, lab="MURX - Magnetic relative permeabilities (also MURY, MURZ).", mat="", sloc="", c1="", c2="", c3="", c4="", c5="", c6="", **kwargs):
            # ansys.mptemp("", "", "", "", "", "", "", "")
            # ansys.mptemp(1, 0)
            # ansys.mpdata("RSVX", 3,
            #              "", 7.496e-8)
            #
            # ansys.mptemp("", "", "", "", "", "",
            #              "", "")  ##mptemp(self, sloc="", t1="", t2="", t3="", t4="", t5="", t6="",**kwargs)
            # ansys.mptemp(1, 0)
            # ansys.mpdata("MURX", 4, "",
            #              1)  ##mpdata(self, lab="MURX - Magnetic relative permeabilities (also MURY, MURZ).", mat="", sloc="", c1="", c2="", c3="", c4="", c5="", c6="", **kwargs):
            # ansys.mptemp("", "", "", "", "", "", "")
            # ansys.mptemp(1, 0)
            # ansys.mpdata("RSVX", 4,
            #              "", 7.0922e-8)
            #
            # ansys.mptemp("", "", "", "", "", "",
            #              "", "")  ##mptemp(self, sloc="", t1="", t2="", t3="", t4="", t5="", t6="",**kwargs)
            # ansys.mptemp(1, 0)
            # ansys.mpdata("MURX", 5, "",
            #              1)  ##mpdata(self, lab="MURX - Magnetic relative permeabilities (also MURY, MURZ).", mat="", sloc="", c1="", c2="", c3="", c4="", c5="", c6="", **kwargs):
            # ansys.flst(5, 246, 6, "ORDER",
            #            4)
            # ansys.fitem(5, 16)  ##fitem(self, nfield="", item="", itemy="", itemz="", **kwargs
            # ansys.fitem(5, -256)
            # ansys.fitem(5, 263)  ##fitem(self, nfield="", item="", itemy="", itemz="", **kwargs
            # ansys.fitem(5, -267)
            # # ansys.vplot()##这一步没问题#这一步下面有点问题
            # # ansys.menu("ON")
            # ##################给每个体分别赋予单元与材料##############
            # ansys.cm("_Y",
            #          "VOLU")  ##Groups geometry items into a component.cm(self, cname="", entity="VOLU - Volumes.", **kwargs):
            # ansys.vsel("", "", "",
            #            "P51X")  ##vsel(self, type="", item="", comp="", vmin="1", vmax="", vinc="", kswp="", **kwargs):
            # ansys.cm("_Y1", "VOLU")  ##cm(self, cname="", entity="VOLU - Volumes.", **kwargs):
            # ansys.cmsel("S", "_Y")  ##cmsel(self, type="S - Select a new set (default).", name="", entity="", **kwargs):
            # ansys.cmsel("S", "_Y1")
            # ansys.vatt(2, "", 2, 0)  ##vatt(self, mat="", real="", type="", esys="", secnum="", **kwargs):
            # ansys.cmsel("S", "_Y")
            # ansys.cmdele("_Y")  ##Deletes a component or assembly definition.cmdele(self, name="", **kwargs):
            # ansys.cmdele("_Y1")
            # ansys.flst(5, 6, 6, "ORDER",
            #            2)
            # ansys.fitem(5, 551)  ##fitem(self, nfield="", item="", itemy="", itemz="", **kwargs
            # ansys.fitem(5, -556)
            # ansys.cm("_Y",
            #          "VOLU")  ##Groups geometry items into a component.cm(self, cname="", entity="VOLU - Volumes.", **kwargs):
            # ansys.vsel("", "", "",
            #            "P51X")  ##vsel(self, type="", item="", comp="", vmin="2", vmax="", vinc="", kswp="", **kwargs):
            # ansys.cm("_Y1", "VOLU")  ##cm(self, cname="", entity="VOLU - Volumes.", **kwargs):
            # ansys.cmsel("S", "_Y")
            # ansys.cmsel("S", "_Y1")
            # ansys.vatt(3, "", 3, 0)  ##vatt(self, mat="", real="", type="", esys="", secnum="", **kwargs):
            # ansys.cmsel("S", "_Y")
            # ansys.cmdele("_Y")
            # ansys.cmdele("_Y1")
            #
            # ansys.flst(5, 9, 6, "ORDER",
            #            5)
            # ansys.fitem(5, 13)  ##fitem(self, nfield="", item="", itemy="", itemz="", **kwargs
            # ansys.fitem(5, -15)
            # ansys.fitem(5, 572)  ##fitem(self, nfield="", item="", itemy="", itemz="", **kwargs
            # ansys.fitem(5, -576)
            # ansys.fitem(5, 593)  ##fitem(self, nfield="", item="", itemy="", itemz="", **kwargs
            #
            # ansys.cm("_Y",
            #          "VOLU")  ##Groups geometry items into a component.cm(self, cname="", entity="VOLU - Volumes.", **kwargs):
            # ansys.vsel("", "", "",
            #            "P51X")  ##vsel(self, type="", item="", comp="", vmin="2", vmax="", vinc="", kswp="", **kwargs):
            # ansys.cm("_Y1", "VOLU")  ##cm(self, cname="", entity="VOLU - Volumes.", **kwargs):
            # ansys.cmsel("S", "_Y")
            # ansys.cmsel("S", "_Y1")
            # ansys.vatt(4, "", 4, 0)  ##vatt(self, mat="", real="", type="", esys="", secnum="", **kwargs):
            # ansys.cmsel("S", "_Y")
            # ansys.cmdele("_Y")
            # ansys.cmdele("_Y1")
            # ansys.flst(5, 6, 6, "ORDER",
            #            5)
            # ansys.fitem(5, 561)  ##fitem(self, nfield="", item="", itemy="", itemz="", **kwargs
            # ansys.fitem(5, -562)
            # ansys.fitem(5, 569)  ##fitem(self, nfield="", item="", itemy="", itemz="", **kwargs
            # ansys.fitem(5, -571)
            # ansys.fitem(5, 592)  ##fitem(self, nfield="", item="", itemy="", itemz="", **kwargs
            #
            # ansys.cm("_Y",
            #          "VOLU")  ##Groups geometry items into a component.cm(self, cname="", entity="VOLU - Volumes.", **kwargs):
            # ansys.vsel("", "", "",
            #            "P51X")  ##vsel(self, type="", item="", comp="", vmin="2", vmax="", vinc="", kswp="", **kwargs):
            # ansys.cm("_Y1", "VOLU")  ##cm(self, cname="", entity="VOLU - Volumes.", **kwargs):
            # ansys.cmsel("S", "_Y")
            # ansys.cmsel("S", "_Y1")
            # ansys.vatt(1, "", 5, 0)  ##vatt(self, mat="", real="", type="", esys="", secnum="", **kwargs):
            # ansys.cmsel("S", "_Y")
            # ansys.cmdele("_Y")
            # ansys.cmdele("_Y1")
            # ansys.flst(5, 246, 6, "ORDER",
            #            2)
            # ansys.fitem(5, 295)  ##fitem(self, nfield="", item="", itemy="", itemz="", **kwargs
            # ansys.fitem(5, -540)
            # ansys.cm("_Y",
            #          "VOLU")  ##Groups geometry items into a component.cm(self, cname="", entity="VOLU - Volumes.", **kwargs):
            # ansys.vsel("", "", "",
            #            "P51X")  ##vsel(self, type="", item="", comp="", vmin="2", vmax="", vinc="", kswp="", **kwargs):
            # ansys.cm("_Y1", "VOLU")  ##cm(self, cname="", entity="VOLU - Volumes.", **kwargs):
            # ansys.cmsel("S", "_Y")
            # ansys.cmsel("S", "_Y1")
            # ansys.vatt(1, "", 6, 0)  ##vatt(self, mat="", real="", type="", esys="", secnum="", **kwargs):
            # ansys.cmsel("S", "_Y")
            # ansys.cmdele("_Y")
            # ansys.cmdele("_Y1")
            # ansys.cm("_Y",
            #          "VOLU")  ##Groups geometry items into a component.cm(self, cname="", entity="VOLU - Volumes.", **kwargs):
            # ansys.vsel("", "", "",
            #            594)  ##vsel(self, type="", item="", comp="", vmin="2", vmax="", vinc="", kswp="", **kwargs):
            # ansys.cm("_Y1", "VOLU")  ##cm(self, cname="", entity="VOLU - Volumes.", **kwargs):
            # ansys.cmsel("S", "_Y")
            # ansys.cmsel("S", "_Y1")
            # ansys.vatt(5, "", 7, 0)  ##vatt(self, mat="", real="", type="", esys="", secnum="", **kwargs):
            # ansys.cmsel("S", "_Y")
            # ansys.cmdele("_Y")
            # ansys.cmdele("_Y1")
            # # ansys.vplot()##这一步没问题#这一步是紫绿图
            # # ansys.menu("ON")
            # ##########网格划分###############################
            # ansys.smrtsize(
            #     8)  ##smrtsize(self, sizlvl="2", fac="", expnd="", trans="", angl="", angh="", gratio="", smhlc="", smanc="", mxitr="", sprx="", **kwargs):
            # ansys.mshape(1,
            #              "3D")  ##mshape(self, key="1 - Mesh with triangle-shaped elements when Dimension = 2-D mesh with tetrahedral-shaped elements when Dimension = 3-D.", dimension="3D - 3-D model (volume mesh)", **kwargs):
            # ansys.mshkey(0)  ##mshkey(self, key="0 - Use free meshing (the default).", **kwargs):
            # ansys.flst(5, 593, 6, "ORDER",
            #            2)  ##Specifies data required for a picking operation (GUI).flst(self, nfield="5", narg="2", type="6 - Volume numbers", otype="ORDER - Data is in an ordered list (such as for the E,P51X and A,P51X commands, in which the order of the data items is significant for the picking operation).", leng="2", **kwargs):
            # ansys.fitem(5, 1)  ##fitem(self, nfield="", item="", itemy="", itemz="", **kwargs):
            # ansys.fitem(5, -593)
            # ansys.cm("_Y", "VOLU")
            # ansys.vsel("", "", "", "P51X")
            # ansys.cm("_Y1", "VOLU")
            # ansys.chkmsh("'VOLU'")  # chkmsh(self, comp="", **kwargs)
            # ansys.cmsel("S", "_Y")
            # ansys.vmesh("_Y1")  ##vmesh(self, nv1="", nv2="", ninc="", **kwargs):
            # ansys.cmdele("_Y")
            # ansys.cmdele("_Y1")
            # ansys.cmdele("_Y2")
            # ansys.esize(0.250,0,)
            # ansys.flst(2, 6250, 5, "ORDER",
            #            2)  ##Specifies data required for a picking operation (GUI).flst(self, nfield="5", narg="2", type="6 - Volume numbers", otype="ORDER - Data is in an ordered list (such as for the E,P51X and A,P51X commands, in which the order of the data items is significant for the picking operation).", leng="2", **kwargs):
            # ansys.fitem(2, 1)  ##fitem(self, nfield="", item="", itemy="", itemz="", **kwargs):
            # ansys.fitem(2, -6250)
            # ansys.aesize("P51X",0.22,)
            # ansys.flst(5, 12, 4, "ORDER",
            #            2)  ##Specifies data required for a picking operation (GUI).flst(self, nfield="5", narg="2", type="6 - Volume numbers", otype="ORDER - Data is in an ordered list (such as for the E,P51X and A,P51X commands, in which the order of the data items is significant for the picking operation).", leng="2", **kwargs):
            # ansys.fitem(5, 11734)  ##fitem(self, nfield="", item="", itemy="", itemz="", **kwargs):
            # ansys.fitem(5, -11745)
            # ansys.cm("_Y", "LINE")
            # ansys.lsel("", "", "", "P51X")
            # ansys.cm("_Y1", "LINE")
            # ansys.cmsel("","_Y")
            # #ansys.chkmsh("'VOLU'")  # chkmsh(self, comp="", **kwargs)
            # ansys.lesize("_Y1",0.2,"","","","","","",1)
            # ansys.cm("_Y", "VOLU")
            # ansys.vsel("", "", "", 594)
            # ansys.cm("_Y1", "VOLU")
            # ansys.chkmsh("'VOLU'")  # chkmsh(self, comp="", **kwargs)
            # ansys.cmsel("S", "_Y")
            # ansys.vmesh("_Y1")  ##vmesh(self, nv1="", nv2="", ninc="", **kwargs):
            # ansys.cmdele("_Y")
            # ansys.cmdele("_Y1")
            # ansys.cmdele("_Y2")
            # # ansys.ui("MESH","OFF")
            # # ansys.vplot()##这一步没问题##这一步没有网格图
            # #ansys.finish()  ## Exits normally from a processor.finish(self, **kwargs):
            # #################设置边界条件与添加激励源#######################
            #
            # ansys.slashsolu()  ##Enters the solution processor.slashsolu(self, **kwargs):
            # ansys.esel("S", "type", "",
            #            1)  ##esel(self, type="S - Select a new set (default).", item="type", comp="", vmin="1", vmax="", vinc="", kabs="", **kwargs):
            # ansys.esel("A", "type", "",
            #            2)  ##esel(self, type=" A - Additionally select a set and extend the current set.", item="type", comp="", vmin="2", vmax="", vinc="", kabs="", **kwargs):
            # ansys.esel("A", "type", "",
            #            3)
            # ansys.esel("A", "type", "",
            #            4)
            # ansys.esel("A", "type", "",
            #            5)
            # ansys.esel("A", "type", "",
            #            6)
            # ansys.esel("A", "type", "",
            #            7)
            #
            # ansys.nsel("S",
            #            "EXT")  ##nsel(self, type="S - Select a new set (default).", item="", comp="", vmin="", vmax="", vinc="", kabs="", **kwargs):
            # ansys.d("ALL", "AZ",
            #         0)  ##d(self, node="", lab="", value="", value2="", nend="", ninc="", lab2="", lab3="", lab4="", lab5="", lab6="", **kwargs):
            # # ansys.vplot()
            #
            # ansys.vsel("ALL")
            # ansys.asel("S", "", "", 3)
            # ansys.nsla("S", 1)
            # ansys.cp(1, "VOLT",
            #          "ALL")  # cp(self, nset="", lab="VOLT(voltage)", node1="", node2="", node3="", node4="", node5="", node6="", node7="", node8="", node9="", node10="", node11="", node12="", node13="", node14="", node15="", node16="", node17="", **kwargs):
            # ansys.get("n1", "NODE", "", "num",
            #           "min")  ##get(self, par="n1", entity="NODE", entnum="", item1="num", it1num="min", item2="", it2num="", **kwargs):
            # ansys.f("n1", "AMPS",
            #         3465)  ##f(self, node="n1", lab="AMPS", value="100", value2="", nend="", ninc="", **kwargs):
            # ansys.vsel("ALL")
            # ansys.asel("S", "", "", 15)
            # ansys.nsla("S", 1)
            # ansys.cp(2, "VOLT",
            #          "ALL")  # cp(self, nset="", lab="VOLT(voltage)", node1="", node2="", node3="", node4="", node5="", node6="", node7="", node8="", node9="", node10="", node11="", node12="", node13="", node14="", node15="", node16="", node17="", **kwargs):
            # ansys.get("n2", "NODE", "", "num",
            #           "min")  ##get(self, par="n1", entity="NODE", entnum="", item1="num", it1num="min", item2="", it2num="", **kwargs):
            # ansys.f("n2", "AMPS",
            #         -3465*0.5,3465*0.866)
            # #ansys.d("ALL", "VOLT", 0)
            # # #ansys.vplot()
            # ansys.vsel("ALL")
            # ansys.asel("S", "", "", 18)
            # ansys.nsla("S", 1)
            # ansys.cp(3, "VOLT",
            #          "ALL")  # cp(self, nset="", lab="VOLT(voltage)", node1="", node2="", node3="", node4="", node5="", node6="", node7="", node8="", node9="", node10="", node11="", node12="", node13="", node14="", node15="", node16="", node17="", **kwargs):
            # ansys.get("n3", "NODE", "", "num",
            #           "min")  ##get(self, par="n1", entity="NODE", entnum="", item1="num", it1num="min", item2="", it2num="", **kwargs):
            # ansys.f("n3", "AMPS",
            #         -3465 * 0.5, -3465 * 0.866)
            # ansys.vsel("ALL")
            # ansys.asel("S", "", "", 6)
            # ansys.nsla("S", 1)
            # ansys.d("ALL", "VOLT", 0)
            #
            # ansys.vsel("ALL")
            # ansys.asel("S", "", "", 9)
            # ansys.nsla("S", 1)
            # ansys.d("ALL", "VOLT", 0)
            #
            # ansys.vsel("ALL")
            # ansys.asel("S", "", "", 12)
            # ansys.nsla("S", 1)
            # ansys.d("ALL", "VOLT", 0)
            #
            # ansys.vsel("S", "type", "", 1)
            # ansys.nslv("S",
            #            1)  ##nslv(self, type="S - Select a new set (default).", nkey="1 - Select all nodes (interior to volume, interior to areas, interior to lines, and at keypoints) associated with the selected volumes.", **kwargs):
            # ansys.eslv("S")  ##eslv(self, type="S - Select a new set (default).", **kwargs):
            # ansys.nsle()  ##nsle(self, type="", nodetype="", num="", **kwargs):
            # ansys.bfe("ALL", "fvin", "", 0,
            #           1)  ##bfe(self, elem="", lab="", stloc="", val1="", val2="", val3="", val4="", **kwargs):
            #
            # ansys.vsel("S", "type", "", 2)
            # ansys.nslv("S",
            #            1)  ##nslv(self, type="S - Select a new set (default).", nkey="1 - Select all nodes (interior to volume, interior to areas, interior to lines, and at keypoints) associated with the selected volumes.", **kwargs):
            # ansys.eslv("S")  ##eslv(self, type="S - Select a new set (default).", **kwargs):
            # ansys.nsle()  ##nsle(self, type="", nodetype="", num="", **kwargs):
            # ansys.bfe("ALL", "fvin", "", 0,
            #           2)
            #
            # ansys.vsel("S", "type", "", 3)
            # ansys.nslv("S",
            #            1)  ##nslv(self, type="S - Select a new set (default).", nkey="1 - Select all nodes (interior to volume, interior to areas, interior to lines, and at keypoints) associated with the selected volumes.", **kwargs):
            # ansys.eslv("S")  ##eslv(self, type="S - Select a new set (default).", **kwargs):
            # ansys.nsle()  ##nsle(self, type="", nodetype="", num="", **kwargs):
            # ansys.bfe("ALL", "fvin", "", 0,
            #           3)
            #
            # ansys.vsel("S", "type", "", 4)
            # ansys.nslv("S",
            #            1)  ##nslv(self, type="S - Select a new set (default).", nkey="1 - Select all nodes (interior to volume, interior to areas, interior to lines, and at keypoints) associated with the selected volumes.", **kwargs):
            # ansys.eslv("S")  ##eslv(self, type="S - Select a new set (default).", **kwargs):
            # ansys.nsle()  ##nsle(self, type="", nodetype="", num="", **kwargs):
            # ansys.bfe("ALL", "fvin", "", 0,
            #           4)
            #
            # ansys.vsel("S", "type", "", 5)
            # ansys.nslv("S",
            #            1)  ##nslv(self, type="S - Select a new set (default).", nkey="1 - Select all nodes (interior to volume, interior to areas, interior to lines, and at keypoints) associated with the selected volumes.", **kwargs):
            # ansys.eslv("S")  ##eslv(self, type="S - Select a new set (default).", **kwargs):
            # ansys.nsle()  ##nsle(self, type="", nodetype="", num="", **kwargs):
            # ansys.bfe("ALL", "fvin", "", 0,
            #           5)
            #
            # ansys.vsel("S", "type", "", 6)
            # ansys.nslv("S",
            #            1)  ##nslv(self, type="S - Select a new set (default).", nkey="1 - Select all nodes (interior to volume, interior to areas, interior to lines, and at keypoints) associated with the selected volumes.", **kwargs):
            # ansys.eslv("S")  ##eslv(self, type="S - Select a new set (default).", **kwargs):
            # ansys.nsle()  ##nsle(self, type="", nodetype="", num="", **kwargs):
            # ansys.bfe("ALL", "fvin", "", 0,
            #           6)
            # # ansys.vplot()
            # ##############设置谐态求解器进行求解##################33
            #
            # ansys.slashsolu()
            # ansys.antype("HARMIC",
            #              "NEW")  ##antype(self, antype=" HARMIC or 3 - Perform a harmonic analysis.  Valid for structural, fluid, magnetic, and electrical degrees of freedom.", status="NEW - Specifies a new analysis (default). If NEW, the remaining fields on this command are ignored.", ldstep="", substep="", action="", **kwargs):
            # ansys.harfrq(50)  ##harfrq(self, freqb="50", freqe="", logopt="", freqarr="", toler="", **kwargs):
            # ansys.eqslv(
            #     "SPARSE")  ##eqslv(self, lab="SPARSE - Sparse direct equation solver. ", toler="", mult="", keepfile="", **kwargs):
            # ansys.allsel(
            #     "ALL")  ##allsel(self, labt=" ALL - Selects all items of the specified entity type and all items of lower entity types (default).", entity="", **kwargs):
            # # ansys.aplot()
            # # ansys.vplot()
            # ansys.solve()  ##solve(self, action="", **kwargs):
            # ansys.finish()  #### Exits normally from a processor.finish(self, **kwargs):
            # # ansys.vplot()
            #
            # #############后处理#################################
            #
            # ansys.post1()  ##post1(self, **kwargs):
            # ansys.exunit("VOLU", "DISP", "COMM",
            #              "SI")  ##exunit(self, ldtype="", load="", untype="", name="", **kwargs):
            # ansys.exunit("VOLU", "HGEN", "COMM", "SI")  ##没有hgen
            # ansys.exprofile("VOLU", "HGEN", 1, "'heat1'", "CFXcu", "csv")  ##没有hgen
            # ansys.exprofile("VOLU", "HGEN", 2, "'heat2'", "CFXag", "csv")
            # ansys.exprofile("VOLU", "HGEN", 3, "'heat3'", "CFXfe", "csv")
            # ansys.exprofile("VOLU", "HGEN", 4, "'heat4'", "CFXcucr", "csv")
            # ansys.exprofile("VOLU", "HGEN", 5, "'heat5'", "CFXmiecu", "csv")
            # ansys.exprofile("VOLU", "HGEN", 6, "'heat6'", "CFXchuzhi", "csv")
            # ansys.save()
            # ansys.plesol("JHEAT", "SUM", 0)
            # # ansys.plnsol()
            # ansys.exit()

    def openworkbenchprocess(self):
        ANSYSpath = r'"D:\Program Files\ANSYS Inc\v190\Framework\bin\Win64\runwb2"'
        #filepath4 = '-F Electricfield.wbpj'
        filepath4 = '-F F:\\test\\Electricfield.wbpj'        # subprocess.Popen("%s %s" % (ANSYSpath, filepath4))
        # print(cmdline)
        try:
            # os.system(cmdline)
            os.system("%s %s" % (ANSYSpath, filepath4))
        except Exception:
            print('Failed to launch ANSYS Workbench!')
            sys.exit(0)




    #########################fault diagnosis page#########################################
    def init_diagnosis_device_type(self):
        self.diagnosis_device_type.addItem("开关柜")
        self.diagnosis_device_type.addItem("组合电器")
        self.diagnosis_device_type.addItem("断路器机构")
        self.diagnosis_device_type.setCurrentIndex(-1)

    def init_diagnosis_device_company(self):
        self.diagnosis_device_company.addItem("厂家1")
        self.diagnosis_device_company.addItem("厂家2")
        self.diagnosis_device_company.addItem("厂家3")
        self.diagnosis_device_company.setCurrentIndex(-1)

    def init_diagnosis_device_modelNumber(self):
        self.diagnosis_device_modelNumber.addItem("xinghao1")
        self.diagnosis_device_modelNumber.addItem("xinghao2")
        self.diagnosis_device_modelNumber.addItem("xinghao3")
        self.diagnosis_device_modelNumber.setCurrentIndex(-1)

    def init_diagnosis_fault_type(self):
        self.diagnosis_fault_type.addItem("局部放电")
        self.diagnosis_fault_type.addItem("过热缺陷")
        self.diagnosis_fault_type.addItem("机构缺陷")
        self.diagnosis_fault_type.setCurrentIndex(-1)




    def on_diagnosis_fault_type_Activate(self, index):
        # print(self.comboBox_type.count())
        # print(self.comboBox_type.currentIndex())
        # print(self.comboBox_type.currentText())
        # print(self.comboBox_type.currentData())
        # print(self.comboBox_type.itemData(self.comboBox_type.currentIndex()))
        # print(self.comboBox_type.itemText(self.comboBox_type.currentIndex()))
        # print(self.comboBox_type.itemText(index))
        self.label_type_show.setText("正在进行"+self.diagnosis_fault_type.currentText()+"故障类型诊断")
    def open_fault_data(self):
        FileName_fault, filetype = QFileDialog.getOpenFileName(self, '打开文件', r'./', 'All Files(*);;TXT (*.txt)')
        print(FileName_fault,filetype)
        self.show_fault_URL.setText(FileName_fault)

        #headtime = time.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')  # 时间命名
        fig_show = np.genfromtxt(FileName_fault)
        #plt.figure(num)
        os.chdir('ontestfile')
        plt.figure(figsize=(8, 5))
        plt.plot(fig_show[1], fig_show[0], 'bo')
        plt.xticks([0, 90, 180, 270, 360])
        plt.xlim(-10, 370)
        plt.yticks([])
        plt.rcParams['savefig.dpi'] = 10
        head = QDateTime.currentDateTime().toString("yyyy-MM-dd-hh-mm-ss")
        #print(head,type(head))
        plt.savefig('5_ontest.jpg')
        os.chdir(os.path.abspath(os.path.join(os.getcwd(), "..")))
        print(os.getcwd())
        #os.chdir(currentpath)
        sys.stdin.flush()
        os.chdir('fault figure')
        plt.figure(figsize=(120, 120))
        #plt.figure(figsize=(240, 150))
        plt.plot(fig_show[1], fig_show[0], 'bo')
        plt.xticks([0, 90, 180, 270, 360])
        plt.xlim(-10, 370)
        plt.yticks([])
        plt.rcParams['savefig.dpi'] = 150
        plt.savefig(head+"_big.jpg")
        png = QtGui.QPixmap(head+'_big.jpg')
        # # 在l1里面，调用setPixmap命令，建立一个图像存放框，并将之前的图像png存放在这个框框里。
        self.label_fault_show.setPixmap(png)
        self.label_fault_show.setScaledContents(True)
        os.chdir(os.path.abspath(os.path.join(os.getcwd(), "..")))
        print(os.getcwd())
        # os.chdir(currentpath)
        sys.stdin.flush()
        answer = giscnn.giscnn('ontestfile')
        #answer = giscnn.giscnn('F:/solidworks ansys/ansys202001170946/test data','testdata001.txt')
        #print(type(answer))
        if answer == 0:
            jufang_predict= "悬浮"
        elif answer == 1:
            jufang_predict = "尖刺"
        elif answer == 2:
            jufang_predict = "沿面"
        elif answer == 3:
            jufang_predict = "气隙"
        elif answer == 4:
            jufang_predict = "颗粒"

        self.lineEdit.setText("故障类型为："+ jufang_predict)

#############################fault analysis page######################################
    def init_analysis_device_type(self):
        self.analysis_device_type.addItem("开关柜")
        self.analysis_device_type.addItem("组合电器")
        self.analysis_device_type.addItem("断路器机构")
        self.analysis_device_type.setCurrentIndex(-1)

    def init_analysis_device_company(self):
        self.analysis_device_company.addItem("厂家1")
        self.analysis_device_company.addItem("厂家2")
        self.analysis_device_company.addItem("厂家3")
        self.analysis_device_company.setCurrentIndex(-1)

    def init_analysis_device_modelNumber(self):
        self.analysis_device_modelNumber.addItem("型号1")
        self.analysis_device_modelNumber.addItem("型号2")
        self.analysis_device_modelNumber.addItem("型号3")
        self.analysis_device_modelNumber.setCurrentIndex(-1)

    def init_analysis_fault_type(self):
        self.analysis_fault_type.addItem("局部放电")
        self.analysis_fault_type.addItem("过热缺陷")
        self.analysis_fault_type.addItem("机构缺陷")
        self.analysis_fault_type.setCurrentIndex(-1)



    def init_analysis_workvoltage_unit_a(self):
        self.analysis_workvoltage_unit_a.addItem("KV(千伏)")
        self.analysis_workvoltage_unit_a.addItem("V(伏)")
        self.analysis_workvoltage_unit_a.setCurrentIndex(-1)
    def init_analysis_workvoltage_unit_b(self):
        self.analysis_workvoltage_unit_b.addItem("KV(千伏)")
        self.analysis_workvoltage_unit_b.addItem("V(伏)")
        self.analysis_workvoltage_unit_b.setCurrentIndex(-1)
    def init_analysis_workvoltage_unit_c(self):
        self.analysis_workvoltage_unit_c.addItem("KV(千伏)")
        self.analysis_workvoltage_unit_c.addItem("V(伏)")
        self.analysis_workvoltage_unit_c.setCurrentIndex(-1)

    #
    def init_analysis_workcurrent_unit_a(self):
        self.analysis_workcurrent_unit_a.addItem("KA(千安)")
        self.analysis_workcurrent_unit_a.addItem("A(安)")
        self.analysis_workcurrent_unit_a.setCurrentIndex(-1)
    def init_analysis_workcurrent_unit_b(self):
        self.analysis_workcurrent_unit_b.addItem("KA(千安)")
        self.analysis_workcurrent_unit_b.addItem("A(安)")
        self.analysis_workcurrent_unit_b.setCurrentIndex(-1)
    def init_analysis_workcurrent_unit_c(self):
        self.analysis_workcurrent_unit_c.addItem("KA(千安)")
        self.analysis_workcurrent_unit_c.addItem("A(安)")
        self.analysis_workcurrent_unit_c.setCurrentIndex(-1)
    def init_analysis_workgamma_unit_a(self):
        self.analysis_workgamma_unit_a.addItem("S/m")
        self.analysis_workgamma_unit_a.setCurrentIndex(-1)
    def init_analysis_workgamma_unit_b(self):
        self.analysis_workgamma_unit_b.addItem("S/m")
        self.analysis_workgamma_unit_b.setCurrentIndex(-1)
    def init_analysis_workgamma_unit_c(self):
        self.analysis_workgamma_unit_c.addItem("S/m")
        self.analysis_workgamma_unit_c.setCurrentIndex(-1)




    def init_analysis_environmenttemp_unit(self):
        self.analysis_environmenttemp_unit.addItem("℃(摄氏度)")
        self.analysis_environmenttemp_unit.addItem("K(开尔文)")
        self.analysis_environmenttemp_unit.setCurrentIndex(-1)
    def init_analysis_environpressure_unit(self):
        self.analysis_environpressure_unit.addItem("KPa(千帕)")
        self.analysis_environpressure_unit.addItem("Pa(帕)")
        self.analysis_environpressure_unit.addItem("毫米汞柱")
        self.analysis_environpressure_unit.setCurrentIndex(-1)
    # def init_analysis_physicsfield_type(self):
    #     self.analysis_physicsfield_type.addItem("电场")
    #     self.analysis_physicsfield_type.addItem("磁场")
    #     self.analysis_physicsfield_type.addItem("热场")
    #     self.analysis_physicsfield_type.addItem("气流场")
    #     self.analysis_physicsfield_type.setCurrentIndex(-1)
    # def init_analysis_fault_set(self):
    #     self.analysis_fault_set.addItem("shezhi1")
    #     self.analysis_fault_set.addItem("shezhi2")
    #     self.analysis_fault_set.addItem("shezhi3")
    #     self.analysis_fault_set.addItem("shezhi4")
    #     self.analysis_fault_set.setCurrentIndex(-1)
    # def init_analysis_number_input(self):
    #     #my_regex = QRegExp('[0-9.]+$')
    #     my_regex = QRegExp("^(-?[0]|-?[1-9][0-9]{0,5})(?:\\.\\d{1,4})?$|(^\\t?$)")
    #     my_validator = QtGui.QRegExpValidator(my_regex, self)
    #     self.analysis_workvoltage_edit.setValidator(my_validator)
    #     self.analysis_workcurrent_edit.setValidator(my_validator)
    #     self.analysis_environmenttemp_edit.setValidator(my_validator)
    #     self.analysis_environpressure_edit.setValidator(my_validator)


    def analysis_calculate_1(self):
        analysis_workvoltage = float(self.analysis_workvoltage_edit.text())
        #analysis_workvoltage = float('%.4f' % analysis_workvoltage_input)
        #analysis_workvoltage.setValidator(QDoubleValidator(0.00, 1000000.00, 2))
        analysis_workcurrent = float(self.analysis_workcurrent_edit.text())
        # analysis_workcurrent = float('%.4f' % analysis_workcurrent_input)
        analysis_environmenttemp = float(self.analysis_environmenttemp_edit.text())
        # analysis_environmenttemp = float('%.4f' % analysis_workcurrent_input)
        analysis_environpressure = float(self.analysis_environpressure_edit.text())
        # analysis_environpressure = float('%.4f' % analysis_workcurrent_input)
        self.analysis_result1.setText("工作电压:" + str(analysis_workvoltage) + self.analysis_workvoltage_unit.currentText()
                                    + "/n工作电流："+str(analysis_workcurrent) + self.analysis_workcurrent_unit.currentText()
                                    + "/n环境温度：" + str(analysis_environmenttemp) + self.analysis_environmenttemp_unit.currentText()
                                    + "/n环境温度：" + str(analysis_environpressure) + self.analysis_environpressure_unit.currentText()
                                    + "/n总计：" + str(analysis_workvoltage+analysis_workcurrent+analysis_environmenttemp+analysis_environpressure))

    def load_simulation_model_fault(self):
        # client = mph.start()
        print("ok")
        path = "F:\\solidworks ansys\\comsol file"
        datanames = os.listdir(path)
        for i in datanames:
            name1 = os.path.splitext(i)
            # print(name1[1])
            if self.simu_model_device_number_fault.currentText() == name1[0] and name1[1] == '.mph':
                # client = mph.start()
                # print('ok1'+self.simu_model_device_number.currentText())
                model = client.load('F:\\solidworks ansys\\comsol file\\' + i)
                print('ok1' + i)
                model.parameters()
                for (name, value) in model.parameters().items():
                    description = model.description(name)
                    print(f'{description:20} {name} = {value}')
                    if 'VoltageA' in name:
                        self.fault_workvoltage_a.setText(value)
                    elif 'VoltageB' in name:
                        self.fault_workvoltage_b.setText(value)
                    elif 'VoltageC' in name:
                        self.fault_workvoltage_c.setText(value)
                    elif 'IA' in name:
                        self.fault_workcurrent_a.setText(value)
                    elif 'IB' in name:
                        self.fault_workcurrent_b.setText(value)
                    elif 'IC' in name:
                        self.fault_workcurrent_c.setText(value)
                    elif 'GamaA' in name:
                        self.analysis_workgamma_a.setText(value)
                    elif 'GamaB' in name:
                        self.analysis_workgamma_b.setText(value)
                    elif 'GamaC' in name:
                        self.analysis_workgamma_c.setText(value)

                    elif 'Temp' in name:
                        self.analysis_environmenttemp_edit.setText(value)
                        # if value > 200:
                        #     self.model_environmenttemp_unit.setCurrentIndex("K(开尔文)")
                        # elif value < 50:
                        #     self.model_environmenttemp_unit.setCurrentIndex("℃(摄氏度)")
                    elif 'Pressure' in name:
                        self.analysis_environpressure_edit.setText(value)

    def playout_3D_show_fault(self):
        # grid = pv.UnstructuredGrid('F:\\solidworks ansys\\ansys202003201652\\MPh-master\\HeEF1605VTU.vtu')
        if self.simu_model_type_fault.currentText() == '电势(ec)':
            grid = pv.UnstructuredGrid('F:\solidworks ansys\comsol file\\dianshiec3Dshow.vtu')
            # png = QtGui.QPixmap('F:\\solidworks ansys\\comsol file\\dianshishow.jpg')
        elif self.simu_model_type_fault.currentText() == '导体温度(ht)':
            grid = pv.UnstructuredGrid('F:\solidworks ansys\comsol file\\daotiwenduht3Dshow.vtu')
        elif self.simu_model_type_fault.currentText() == '等温线(ht)':
            grid = pv.UnstructuredGrid('F:\solidworks ansys\comsol file\\dengwenxianht3Dshow.vtu')
        elif self.simu_model_type_fault.currentText() == '气体温度(ht2)':
            grid = pv.UnstructuredGrid('F:\solidworks ansys\comsol file\\qitiwenduht23Dshow.vtu')
        elif self.simu_model_type_fault.currentText() == '等温线(ht2)':
            grid = pv.UnstructuredGrid('F:\solidworks ansys\comsol file\\dengwenxianht23Dshow.vtu')
        elif self.simu_model_type_fault.currentText() == '电位(es)':
            grid = pv.UnstructuredGrid('F:\solidworks ansys\comsol file\\dianweies3Dshow.vtu')
        elif self.simu_model_type_fault.currentText() == '电场强度(es)':
            grid = pv.UnstructuredGrid('F:\solidworks ansys\comsol file\\dianchangqiangdues3Dshow.vtu')
        #elif self.simu_model_type.currentText() == '电场':
         #   grid = pv.UnstructuredGrid('F:\solidworks ansys\comsol file\\dianchang3Dshow.vtu')
        grid.plot()

    def mesh_process_fault(self):
        path = "F:\\solidworks ansys\\comsol file"
        datanames = os.listdir(path)
        self.Simu_progressBar.setValue(25)
        for i in datanames:
            name1 = os.path.splitext(i)
            # print(name1[1])
            if self.simu_model_device_number_fault.currentText() == name1[0] and name1[1] == '.mph':
                #client = mph.start()
                # print('ok1'+self.simu_model_device_number.currentText())
                model = client.load('F:\\solidworks ansys\\comsol file\\' + i)
        model.parameter('VoltageA', self.fault_workvoltage_a.text())
        model.parameter('VoltageB', self.fault_workvoltage_b.text())
        model.parameter('VoltageC', self.fault_workvoltage_c.text())
        model.parameter('IA', self.fault_workcurrent_a.text())
        model.parameter('IB', self.fault_workcurrent_b.text())
        model.parameter('IC', self.fault_workcurrent_c.text())
        model.parameter('GamaA', self.analysis_workgamma_a.text())
        model.parameter('GamaB', self.analysis_workgamma_b.text())
        model.parameter('GamaC', self.analysis_workgamma_c.text())

        model.parameter('Temp', self.analysis_environmenttemp_edit.text())
        model.parameter('Pressure', self.analysis_environpressure_edit.text())
        model.build()
        model.mesh()
        model.export('mesh', 'meshshow.jpg')
        #model.export('meshvtu', 'mesh3Dshow.vtu')
                #model.solve()
                #model.save()
        png = QtGui.QPixmap('F:\\solidworks ansys\\comsol file\\meshshow.jpg')
        #time.sleep(10)
        self.label_simu_2D_fault.setPixmap(png)
        self.label_simu_2D_fault.setScaledContents(True)
        print('okfinish')
        self.Simu_progressBar_fault.setValue(80)
        model.clear()
    def calcuate_ansys_prcoess_fault(self):
        path = "F:\\solidworks ansys\\comsol file"
        datanames = os.listdir(path)
        #self.Simu_progressBar.setValue(25)
        for i in datanames:
            name1 = os.path.splitext(i)
            # print(name1[1])
            if self.simu_model_device_number_fault.currentText() == name1[0] and name1[1] == '.mph':
                # client = mph.start()
                # print('ok1'+self.simu_model_device_number.currentText())
                model = client.load('F:\\solidworks ansys\\comsol file\\' + i)
        model.parameter('VoltageA', self.fault_workvoltage_a.text())
        model.parameter('VoltageB', self.fault_workvoltage_b.text())
        model.parameter('VoltageC', self.fault_workvoltage_c.text())
        model.parameter('IA', self.fault_workcurrent_a.text())
        model.parameter('IB', self.fault_workcurrent_b.text())
        model.parameter('IC', self.fault_workcurrent_c.text())
        model.parameter('GamaA', self.analysis_workgamma_a.text())
        model.parameter('GamaB', self.analysis_workgamma_b.text())
        model.parameter('GamaC', self.analysis_workgamma_c.text())

        model.parameter('Temp', self.analysis_environmenttemp_edit.text())
        model.parameter('Pressure', self.analysis_environpressure_edit.text())
        model.build()
        model.mesh()
        model.solve()
        #model.save()
        model.export('dianshiec', 'dianshiecshow.jpg')
        #model.export('dianchang', 'dianchangshow.jpg')
        model.export('daotiwendu', 'daotiwendushow.jpg')
        model.export('dengwenxianht', 'dengwenxianhtshow.jpg')
        model.export('qitiwenduht2', 'qitiwenduht2show.jpg')
        model.export('dengwenxianht2', 'dengwenxianht2show.jpg')
        model.export('dianweies', 'dianweiesshow.jpg')
        model.export('dianchangqiangdues', 'dianchangqiangduesshow.jpg')

        model.export('dianshiecvtu', 'dianshiec3Dshow.vtu')
        #model.export('dianchangvtu', 'dianchang3Dshow.vtu')
        model.export('daotiwenduhtvtu', 'daotiwenduht3Dshow.vtu')
        model.export('dengwenxianhtvtu', 'dengwenxianht3Dshow.vtu')
        model.export('qitiwenduht2vtu', 'qitiwenduht23Dshow.vtu')
        model.export('dengwenxianht2vtu', 'dengwenxianht23Dshow.vtu')
        model.export('dianweiesvtu', 'dianweies3Dshow.vtu')
        model.export('dianchangqiangduesvtu', 'dianchangqiangdues3Dshow.vtu')
        self.Simu_progressBar_fault.setValue(100)
        model.clear()
    def ansys_show_fault(self):
        self.Simu_progressBar_fault.setValue(100)

        #self.vtkWidgetshow = QtWidgets.QFrame()
        #QVTKRenderWindowInteractor.__init__(self.vtkContext, self.vtkContext)
        #self.vtkContext.GetRenderWindow().GetInteractor().SetInteractorStyle(vtk.vtkInteractorStyleTrackballCamera())
        if self.simu_model_type_fault.currentText() == '电势(ec)':
            png = QtGui.QPixmap('F:\\solidworks ansys\\comsol file\\dianshiecshow.jpg')
            # self.label_simu_2D.setPixmap(png)
            # self.label_simu_2D.setScaledContents(True)
        elif self.simu_model_type_fault.currentText() == '导体温度(ht)':
            png = QtGui.QPixmap('F:\\solidworks ansys\\comsol file\\daotiwenduhtshow.jpg')
        elif self.simu_model_type_fault.currentText() == '等温线(ht)':
            png = QtGui.QPixmap('F:\\solidworks ansys\\comsol file\\dengwenxianhtshow.jpg')
        elif self.simu_model_type_fault.currentText() == '气体温度(ht2)':
            png = QtGui.QPixmap('F:\\solidworks ansys\\comsol file\\qitiwenduht2show.jpg')
        elif self.simu_model_type_fault.currentText() == '等温线(ht2)':
            png = QtGui.QPixmap('F:\\solidworks ansys\\comsol file\\dengwenxianht2show.jpg')
        elif self.simu_model_type_fault.currentText() == '电位(es)':
            png = QtGui.QPixmap('F:\\solidworks ansys\\comsol file\\dianweiesshow.jpg')
        elif self.simu_model_type_fault.currentText() == '电场强度(es)':
            png = QtGui.QPixmap('F:\\solidworks ansys\\comsol file\\dianchangqiangduesshow.jpg')

        self.label_simu_2D_fault.setPixmap(png)
        self.label_simu_2D_fault.setScaledContents(True)





if __name__=='__main__':
    app=QApplication(sys.argv)
    md=MainCode()
    md.show()
    sys.exit(app.exec_())
