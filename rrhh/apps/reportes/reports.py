# -*- encoding: utf-8 -*-
__author__ = 'leonel'
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from rrhh import settings

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from apps.configuraciones.models import Funcionario
from apps.vacaciones.models import Solicitud
from reportlab.lib.units import inch, mm


from io import BytesIO


class Reporte:
    def __init__(self):
        self.buffer = BytesIO()
        self.pagesize = A4
        self.width, self.height = self.pagesize
        self.doc = SimpleDocTemplate(self.buffer)

    def get_pdf(self):
        return self.buffer.getvalue()


def header_footer(canvas, doc):
    canvas.saveState()
    estilo = getSampleStyleSheet()
    estilo_header = estilo['Normal']
    estilo_header.alignment = TA_CENTER
    #logo = Image(settings.MEDIA_URL + 'archivos/logo.jpg', width=50, height=50)
    #logo.drawOn(canvas, doc.leftMargin, doc.height + doc.topMargin)
    text_header = '<b>UNIVERSIDAD NACIONAL DE ITAPÚA (U.N.I)</b> ' \
                  '<br></br>' \
                  '<font size=9>Creada por Ley 1009/96 de fecha 03 de Diciembre de 1996</font>' \
                  '<br></br>' \
                  '<font size=10><b>Departamento de Recursos Humanos</b></font>' \
                  '<br></br> ' \
                  '________________________________________________________________________'
    p_header = Paragraph(text_header, estilo_header)
    p_header.wrap(doc.width - 50, doc.topMargin)
    p_header.drawOn(canvas, doc.leftMargin + 50, doc.height + doc.topMargin)

    estilo_footer = estilo['Normal']
    estilo_footer.fontSize = 8
    text_footer = ""
    p_footer = Paragraph(text_footer, estilo_footer)
    p_footer.wrap(doc.width, doc.topMargin)
    p_footer.drawOn(canvas, inch, inch * 0.75)
    canvas.restoreState()


class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        """add page info to each page (page x of y)"""
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_number(self, page_count):
        self.setFont("Helvetica", 7)
        self.drawRightString(190 * mm, 0.75 * inch,
                             "Página %d de %d" % (self._pageNumber, page_count))


class ReporteFuncionarios(Reporte):
    def go(self):
        elementos = []
        estilos = getSampleStyleSheet()
        estilo_titulo = estilos['Heading2']
        estilo_filas = estilos['Normal']

        parrafo = Paragraph("Usuarios", estilo_titulo)
        elementos.append(parrafo)

        

        self.doc.build(elementos, onFirstPage=header_footer, onLaterPages=header_footer, canvasmaker=NumberedCanvas)

        return self.get_pdf()


class ReporteSolicitud(Reporte):
    def go(self, solicitud):
        elementos = []
        estilos = getSampleStyleSheet()
        estilo_titulo = estilos['Heading2']
        estilo_filas = estilos['Normal']

        parrafo = Paragraph("Solicitud de vacaciones", estilo_titulo)
        elementos.append(parrafo)

        parrafo = Paragraph("<h3>Numero</h3>", estilo_filas)
        elementos.append(parrafo)

        self.doc.build(elementos, onFirstPage=header_footer, onLaterPages=header_footer, canvasmaker=NumberedCanvas)

        return self.get_pdf()