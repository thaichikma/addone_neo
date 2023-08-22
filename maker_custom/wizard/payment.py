from functools import reduce
from odoo import models , fields, api, _
from odoo.modules.module import get_module_resource
from datetime import datetime
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError
from num2words import num2words
from PIL import Image
import os
import tempfile

class AbstractPaymentReport(models.AbstractModel):
    _name = "report.maker_custom.payment"
    _inherit = "report.report_xlsx.abstract"

    def generate_xlsx_report(self, workbook, data, partner):
        account_id = partner['id']

        # set sheet name
        sheet = workbook.add_worksheet("payment")
        # set column width, row
        image_path_left = get_module_resource('maker_custom', 'images', 'logo.png')
        image_1 = Image.open(image_path_left)
        new_size_logo_left = (1000, 100)
        resized_image_left = image_1.resize(new_size_logo_left)
        temp_image_left = os.path.join(tempfile.gettempdir(), 'resized_image_logo_left.png')
        resized_image_left.save(temp_image_left)
        sheet.set_header('&L&G', {'image_left': temp_image_left})  # &G để xác định hình ảnh nằm bên trái

        for col_num in range(100):
            sheet.set_column(col_num, col_num, 3)
        for set_row in range(1000):
            sheet.set_row(set_row, 18)
        # style format
        normal = workbook.add_format({"font_size": 11,
                                      "font_name": "Roboto Condensed"})
        normal_border = workbook.add_format({"font_size": 12, "border": 2, "font_name": "Times New Roman"})
        normal.set_text_wrap()
        normal_border.set_text_wrap()
        table_header = workbook.add_format({
            "font_size": 11,
            "font_name": "Roboto Condensed",
            "border": 1,
            "align": "left", "valign": "vcenter", "text_wrap": True
        })
        table_header.set_text_wrap()

        table_data = workbook.add_format({
            "font_size": 11, "border": 1,
            "font_name": "Roboto Condensed",
            "align": "center", "valign": "vcenter"
        })
        product = workbook.add_format({
            "font_size": 11, "border": 1,
            "font_name": "Roboto Condensed",
            "align": "left", "valign": "vcenter", "text_wrap": True
        })
        quantity = workbook.add_format({
            "font_size": 10, "border": 1,
            "font_name": "Roboto Condensed",
            "align": "right", "valign": "vcenter"
        })
        tieude = workbook.add_format({
            "font_size": 10,
            "font_name": "Roboto Condensed",
            "align": "left",
        })
        quotation_format = workbook.add_format({
            "font_size": 36, "bold": True,
            "font_name": "Roboto Condensed",
            "align": "center", "font_color": "#5388BC",
        })

        header_tieude = workbook.add_format({
            "bold": True, "font_size": 10, "font_name": "Times New Roman",
            "align": "right", "valign": "vcenter", "font_color": "#5388BC"
        })
        header_right = workbook.add_format({
            "bold": True, "font_size": 10, "font_name": "Calibri",
            "align": "left", "valign": "vcenter","text_wrap": True
        })
        # add logo
        account = self.env['account.move'].search([('id', '=', account_id)])
        company = account.company_id or " "
        name_company = company.name or " "
        street_company = company.street or " "

        sheet.merge_range("L1:AG4", 'PAYMENT REQUEST', quotation_format)

        company_kh = account.partner_id or " "
        name_company_kh = company_kh.name or " "
        street_company_kh = company_kh.street or " "
        phone_1 = company_kh.phone or " "
        contact = account.x_contact_id.name or " "
        email = company_kh.email
        sheet.merge_range("B6:C6", "Messrs.", header_tieude)
        sheet.insert_image('C7', get_module_resource('maker_custom', 'images', 'company.png'),
                           {'x_scale': 0.9, 'y_scale': 0.9})
        sheet.insert_image('C9', get_module_resource('maker_custom', 'images', 'addess.png'),
                           {'x_scale': 0.9, 'y_scale': 0.9})
        sheet.insert_image('C11', get_module_resource('maker_custom', 'images', 'contact.png'),
                           {'x_scale': 0.8, 'y_scale': 0.8})
        sheet.insert_image('C12', get_module_resource('maker_custom', 'images', 'phone.png'),
                           {'x_scale': 0.7, 'y_scale': 0.7})
        sheet.insert_image('C13', get_module_resource('maker_custom', 'images', 'email.png'),
                           {'x_scale': 0.7, 'y_scale': 0.7})

        sheet.merge_range("D7:N8", name_company_kh, tieude)
        sheet.merge_range("D9:N10", street_company_kh, tieude)
        sheet.merge_range("D11:N11", contact, tieude)
        sheet.merge_range("D12:N12", phone_1, tieude)
        sheet.merge_range("D13:N13", email, tieude)
        # sheet.set_border(6, 0, 13, 3, 1)

        sheet.merge_range("T7:W7", "REPUEST #", header_tieude)
        sheet.write("X7", ":", header_right)
        sheet.merge_range("Y7:AG7", "ORDER #", header_right)

        sheet.merge_range("T8:W8", "Date", header_right)
        sheet.write("X8", ":", header_right)
        sheet.merge_range("Y8:AG8", account.invoice_date, header_right)

        sheet.merge_range("T9:W9", "Our VAT #", header_right)
        sheet.write("X9", ":", header_right)
        sheet.merge_range("Y9:AG9", '', header_right)

        sheet.merge_range("T10:W10", "Your PO", header_right)
        sheet.write("X10", ":", header_right)
        sheet.merge_range("Y10:AG10", "", header_right)

        sheet.merge_range("S12:AG12", "Dear Valued Customer !", header_right)
        sheet.merge_range("S13:AG14", "We are pleased to inform you that, we had already fulfilled procedures "
                                      "and delivered all the cargos you ordered. We hereby send you the details of your payment duties as below.", header_right)


        sheet.insert_image('AD7', get_module_resource('maker_custom', 'images', 'logo3.png'),
                           {'x_scale': 1, 'y_scale': 1})


        # table header
        le_tren = workbook.add_format({
            "bold": True, "font_size": 10,
            "font_name": "Roboto Condensed",
            "align": "center", "valign": "vcenter",
            "bg_color": "#5388BC",  # Đặt màu nền đen
            "font_color": "#FFFFFF",  # Đặt màu chữ trắng
            "border": 1,  # Thêm viền
            "border_color": "#FFFFFF"
        })
        # I. Item, Descriptions, PO, Ordering amount
        table_data = workbook.add_format({
            "font_size": 11, "bold": True,
            "font_name": "Roboto Condensed",
            "align": "center", "valign": "vcenter"
        })
        sheet.merge_range("B16:AA16", "I. Item, Descriptions, PO, Ordering amount", le_tren)
        sheet.merge_range("B17:F17", "Your Purchase Order No.", table_data)
        sheet.merge_range("G17:AA17", "?????", header_right)
        sheet.merge_range("B18:C18", "Our VAT Invoice", table_data)
        sheet.merge_range("E18:I18", account.partner_id.vat, header_right)
        # II. Payment Method, Duedate
        formatted_date = account.invoice_date_due.strftime('%d-%b-%Y')
        sheet.merge_range("B20:AA20", "II. Payment Method, Duedate", le_tren)
        sheet.merge_range("B21:F21", "Payment Amount", table_data)
        sheet.merge_range("G21:AA21", "???", header_right)
        sheet.merge_range("B22:F22", "Amount in Words", table_data)
        sheet.merge_range("G22:AA22", "???", header_right)
        sheet.merge_range("B23:F23", "Payment Term", table_data)
        sheet.merge_range("G23:AA23", "???", header_right)
        sheet.merge_range("B24:F24", "Due Date", table_data)
        sheet.merge_range("G24:AA24", formatted_date, header_right)
        # III. Banking Information, Payment amount
        bank = self.env['res.partner.bank'].search([('company_id', '=', account.company_id.id)], limit=1)
        amount_in_words = num2words(account.amount_total, lang='en').replace(',', '')
        amount_in_words = amount_in_words.replace('-', ' ').replace(',', ' ').replace(' and', ' ').title()
        sheet.merge_range("B26:AA26", "IIi. Banking Information", le_tren)
        sheet.merge_range("B27:F27", "Beneficiary", table_data)
        sheet.merge_range("G27:AA27", account.company_id.name, header_right)
        sheet.merge_range("B28:F28", "Account No.", table_data)
        sheet.merge_range("G28:AA28", bank.acc_number, header_right)
        sheet.merge_range("B30:F30", "Bank Name", table_data)
        sheet.merge_range("G30:AA30", bank.bank_id.name, header_right)
        sheet.merge_range("B31:F31", "Address", table_data)
        sheet.merge_range("G31:AA31", account.partner_id.street, header_right)

        # sheet.merge_range("B25:C25", "Payment Amount", header_right)
        # sheet.merge_range("E25:I25", str(account.amount_total) + 'VND', header_right)
        # sheet.merge_range("B26:C26", "Amount in Words", header_right)
        # sheet.merge_range("E26:I26", str(amount_in_words) + ' Vietnamese Dong only', header_right)

        # bottom table
        sheet.merge_range("B34:C34", "NOTE:", header_right)
        sheet.merge_range("Y34:AF34", "NEOTECH SOLUTION JSC",
                          header_right)

        sheet.fit_to_pages(1, 0)

