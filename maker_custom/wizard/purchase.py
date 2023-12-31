from functools import reduce
from odoo import models , fields, api, _
from odoo.modules.module import get_module_resource
from datetime import datetime
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError
from PIL import Image
import os
import tempfile


class AbstractPurchaseReport(models.AbstractModel):
    _name = "report.maker_custom.purchase"
    _inherit = "report.report_xlsx.abstract"

    def generate_xlsx_report(self, workbook, data, partner):
        purchase_id = partner['id']
        query = f"""
                    select COALESCE(pt.name ->> 'en_US', ''),
                        COALESCE(pol.x_product_model, ''),
                        COALESCE(pol.product_qty, 0),
                        uom.name ->> 'en_US' as uom,
                        COALESCE(pol.price_unit, 0),
                        COALESCE(pol.price_subtotal, 0),
                        COALESCE(maker.name, ' ')
                    from purchase_order_line as pol
                        left join product_product as pp on pol.product_id = pp.id
                        left join product_template as pt on pp.product_tmpl_id = pt.id
                        left join uom_uom as uom on pt.uom_id = uom.id
                        left join xres_maker as maker on pol.x_product_maker = maker.id
                    where pol.order_id = '{purchase_id}'
                """
        self._cr.execute(query)
        result = self._cr.fetchall()
        # set sheet name
        sheet = workbook.add_worksheet("purchase")
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

        tieude = workbook.add_format({
            "font_size": 10,
            "font_name": "Roboto Condensed",
            "align": "left","valign": "top"
        })
        quotation_format = workbook.add_format({
            "font_size": 36,"bold": True,
            "font_name": "Roboto Condensed",
            "align": "right","font_color": "#0070C0", "valign": "top"
        })

        header_tieude = workbook.add_format({
            "bold": True, "font_size": 10, "font_name": "Roboto Condensed",
            "align": "left", "valign": "vcenter","font_color": "#5388BC"
        })
        header_right = workbook.add_format({
            "bold": True, "font_size": 10, "font_name": "Roboto Condensed",
            "align": "left", "valign": "vcenter"
        })
        purchase = self.env['purchase.order'].search([('id', '=', purchase_id)])
        company = purchase.company_id or " "
        name_company = company.name or " "
        street_company = company.street or " "


        sheet.merge_range("L1:AG4", 'PURCHASE ORDER', quotation_format)

        company_kh = purchase.partner_id or " "
        name_company_kh = company_kh.name or " "
        street_company_kh = company_kh.street or " "
        phone_1 = company_kh.phone or " "
        contact = purchase.x_contact_id.name or " "
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

        sheet.merge_range("T7:W7", "ORDER #", header_tieude)
        sheet.write("X7", ":", header_right)
        sheet.merge_range("Y7:AG7", purchase.name, tieude)

        sheet.merge_range("T8:W8", "Date", header_right)
        sheet.write("X8", ":", header_right)
        format_date = purchase.date_approve.strftime('%d/%m/%Y')
        sheet.merge_range("Y8:AG8", format_date, tieude)

        sheet.merge_range("T9:W9", "Validity", header_right)
        sheet.write("X9", ":", header_right)
        sheet.merge_range("Y9:AG9", "", tieude)

        sheet.merge_range("T10:W10", "Lead-Time", header_right)
        sheet.write("X10", ":", header_right)
        difference_days = (purchase.date_approve - purchase.date_approve).days
        difference_weeks = difference_days
        sheet.merge_range("Y10:AG10", str(difference_weeks) +" days", tieude)

        sheet.merge_range("T11:W11", "Delivery Term", header_right)
        sheet.write("X11", ":", header_right)
        format_date1 = purchase.date_planned.strftime('%d/%m/%Y')
        sheet.merge_range("Y11:AG11", format_date1, tieude)

        sheet.merge_range("T12:W12", "Payment Term", header_right)
        sheet.write("X12", ":", header_right)
        sheet.merge_range("Y12:AG13", purchase.payment_term_id.name, tieude)


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
        sub_and_vat1 = workbook.add_format({
            "bold": True, "font_size": 10,
            "font_name": "Roboto Condensed",
            "align": "right", "valign": "vcenter",
            "bg_color": "#5388BC",  # Đặt màu nền đen
            "font_color": "#FFFFFF",  # Đặt màu chữ trắng
            "border": 1,  # Thêm viền
            "border_color": "#FFFFFF"
        })
        sub_and_vat = workbook.add_format({
            "bold": True, "font_size": 10,
            "font_name": "Roboto Condensed",
            "align": "right", "valign": "vcenter",
            "bg_color": "#BFBFBF",  # Đặt màu nền đen
            "font_color": "#FFFFFF",  # Đặt màu chữ trắng
            "border_color": "#5388BC"
        })

        sheet.write("B15", "No.", le_tren)
        sheet.merge_range("C15:N15", "PRODUCTS \ ITEMS", le_tren)
        sheet.merge_range("O15:U15", "DETAILS", le_tren)
        sheet.merge_range("V15:W15", "Q'ty", le_tren)
        sheet.merge_range("X15:AB15", "UNIT PRICE(VND)", le_tren)
        sheet.merge_range("AC15:AG15", "AMOUNT(VND)", le_tren)
        # table data
        table_data = workbook.add_format({
            "font_size": 11, "border": 1, "font_name": "Roboto Condensed", "align": "center", "valign": "top",
            "border_color": "#5388BC"
        })
        product = workbook.add_format({
            "font_size": 11, "border": 1, "font_name": "Roboto Condensed", "align": "left", "valign": "top",
            "border_color": "#5388BC", "text_wrap": True
        })
        quantity = workbook.add_format({
            "font_size": 11, "border": 1, "font_name": "Roboto Condensed", "align": "right", "valign": "top",
            "border_color": "#5388BC"
        })
        row = 15
        stt = 0
        for report in result:
            sheet.set_row(row, 54)
            sheet.write(row, 1, stt + 1, table_data)
            sheet.merge_range(row, 2, row, 13, report[0], product)
            sheet.merge_range(row, 14, row, 20, 'Model: ' + str(report[1])
                              + '\nMaker: ' + str(report[6])
                              + '\nLead-Time: ', product)
            sheet.write(row, 21, report[2], quantity)
            sheet.write(row, 22, report[3], table_data)
            sheet.merge_range(row, 23, row, 27, report[4], quantity)
            sheet.merge_range(row, 28, row, 32, report[5], quantity)
            row += 1
            stt += 1
        amount_tax = purchase.amount_tax
        amount_total = purchase.amount_total
        amount_untaxed = purchase.amount_untaxed
        sheet.merge_range(row, 23, row, 27, "Sub Total", sub_and_vat)
        sheet.merge_range(row+1, 23, row+1, 27, "Tax VAT", sub_and_vat)
        sheet.merge_range(row+2, 23, row+2, 27, "GRAND TOTAL", sub_and_vat1)
        sheet.merge_range(row, 28, row, 32, amount_untaxed, sub_and_vat)
        sheet.merge_range(row+1, 28, row+1, 32, amount_tax, sub_and_vat)
        sheet.merge_range(row+2, 28, row+2, 32, amount_total, sub_and_vat1)

        bottun_left = workbook.add_format({
             "font_size": 9, "font_name": "Roboto Condensed Light",
            "align": "left", "valign": "vcenter", "text_wrap": True,"font_color": "#5388BC"
        })
        bottun_left1 = workbook.add_format({
            "font_size": 9, "font_name": "Roboto Condensed Light",
            "align": "left", "valign": "vcenter", "text_wrap": True,
        })
        bottun_center = workbook.add_format({
            "bold": True, "font_size": 9, "font_name": "Roboto Condensed Light",
            "align": "center", "valign": "vcenter", "text_wrap": True
        })
        sheet.merge_range(row + 2, 1, row + 2, 6, "Terms and Conditions", bottun_left)
        sheet.write(row + 3, 1, "1", bottun_center)
        sheet.write(row + 4, 1, "2", bottun_center)
        sheet.write(row + 5, 1, "3", bottun_center)
        sheet.merge_range(row + 3, 2, row + 3, 22, "Please inform the Deliver schedule once you confirm this Order.", bottun_left1)
        sheet.merge_range(row + 4, 2, row + 4, 22, "Please send back the PO confirmation", bottun_left1)
        sheet.merge_range(row + 5, 2, row + 6, 22, "Maker will extend local support to our engineer who is based in Hanoi,\n"
                                                   " encompassing services such as installation, trial run, basic training, and warranty support", bottun_left1)


        sheet.merge_range(row + 8, 2, row + 9, 13, name_company_kh, bottun_center)
        sheet.merge_range(row + 8, 19, row + 9, 30, "NEOTECH SOLUTION JSC", bottun_center)
        sheet.merge_range(row + 10, 2, row + 11, 13, "We hereby agree and confirm \n our acceptance of this order",
                          bottun_left1)
        sheet.merge_range(row + 15, 2, row + 15, 13, "Co. Stamp & Signature", bottun_center)


        sheet.fit_to_pages(1, 0)

