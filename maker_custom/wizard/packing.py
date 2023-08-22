from functools import reduce
from odoo import models , fields, api, _
from odoo.modules.module import get_module_resource
from datetime import datetime
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError
from PIL import Image
import os
import tempfile

class AbstractInventoryReport(models.AbstractModel):
    _name = "report.maker_custom.packing"
    _inherit = "report.report_xlsx.abstract"

    def generate_xlsx_report(self, workbook, data, partner):
        picking_id = partner['id']
        query = f"""
                    select COALESCE(sm.name, ''),
                        COALESCE(sm.x_product_model, ''),
                        COALESCE(sm.quantity_done, 0),
                        uom.name ->> 'en_US' as uom,
                        '' as net_weight,
                        '' as gross,
                        COALESCE(maker.name, ' '),
                        '' as dimension
                    from stock_move as sm
                        left join product_product as pp on sm.product_id = pp.id
                        left join product_template as pt on pp.product_tmpl_id = pt.id
                        left join uom_uom as uom on sm.product_uom = uom.id
                        left join xres_maker as maker on sm.x_product_maker = maker.id
                    where sm.picking_id = '{picking_id}'
                """

        self._cr.execute(query)
        result = self._cr.fetchall()
        # set sheet name
        sheet = workbook.add_worksheet("packing list")
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
            "align": "left", "valign": "vcenter"
        })
        packing = self.env['stock.picking'].search([('id', '=', picking_id)])
        company = packing.company_id or " "
        name_company = company.name or " "
        street_company = company.street or " "

        sheet.merge_range("L1:AG4", 'Quotation', quotation_format)

        company_kh = packing.partner_id or " "
        name_company_kh = company_kh.name or " "
        street_company_kh = company_kh.street or " "
        phone_1 = company_kh.phone or " "
        # contact = packing.x_contact_id.name or " "
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
        sheet.merge_range("D11:N11", 'contact', tieude)
        sheet.merge_range("D12:N12", phone_1, tieude)
        sheet.merge_range("D13:N13", email, tieude)
        # sheet.set_border(6, 0, 13, 3, 1)

        sheet.merge_range("T7:W7", "DELIVERY #", header_tieude)
        sheet.write("X7", ":", header_right)
        sheet.merge_range("Y7:AG7", "INVOICE #", header_right)

        sheet.merge_range("T8:W8", "Date", header_right)
        sheet.write("X8", ":", header_right)
        sheet.merge_range("Y8:AG8", packing.scheduled_date, header_right)

        sheet.merge_range("T9:W9", "Delivery Term", header_right)
        sheet.write("X9", ":", header_right)
        sheet.merge_range("Y9:AG9", "Delivery Term", header_right)

        sheet.merge_range("T10:W10", "Your PO #", header_right)
        sheet.write("X10", ":", header_right)
        sheet.merge_range("Y10:AG10", "Your PO #", header_right)

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

        sheet.write("B15", "No.", le_tren)
        sheet.merge_range("C15:N15", "PRODUCTS \ ITEMS", le_tren)
        sheet.merge_range("O15:S15", "DETAILS", le_tren)
        sheet.merge_range("T15:U15", "Q'ty", le_tren)
        sheet.merge_range("V15:X15", "NET Weight(kg)", le_tren)
        sheet.merge_range("Y15:AA15", "Gross Weight(Kg)", le_tren)
        sheet.merge_range("AB15:AG15", "Dimension(m)", le_tren)
        # table data
        row = 17
        stt = 0
        row = 15
        stt = 0
        for report in result:
            sheet.merge_range(row, 1, row + 2, 1, stt + 1, table_data)
            sheet.merge_range(row, 2, row + 2, 13, report[0], product)
            sheet.merge_range(row, 14, row, 18, 'Model: ' + str(report[1]), product)
            sheet.merge_range(row + 1, 14, row + 2, 18, 'Maker: ' + str(report[6]), product)
            sheet.merge_range(row, 19, row + 2, 19, report[2], quantity)
            sheet.merge_range(row, 20, row + 2, 20, report[3], table_data)
            sheet.merge_range(row, 21, row + 2, 23, report[4], quantity)
            sheet.merge_range(row, 24, row + 2, 26, report[5], quantity)
            sheet.merge_range(row, 27, row + 2, 32, report[7], quantity)
            row += 3
            stt += 1

        bottun_left = workbook.add_format({
             "font_size": 7, "font_name": "Calibri",
            "align": "left", "valign": "vcenter", "text_wrap": True
        })
        bottun_left1 = workbook.add_format({
            "bold": True, "font_size": 10, "font_name": "Calibri",
            "align": "left", "valign": "vcenter", "text_wrap": True,"bottom": 1
        })
        bottun_center = workbook.add_format({
            "bold": True, "font_size": 12, "font_name": "Calibri",
            "align": "center", "valign": "vcenter", "text_wrap": True
        })
        sheet.merge_range(row + 4, 24, row + 4, 30, "NEOTECH SOLUTION JSC ", bottun_center)
        sheet.merge_range(row+1, 1,row+1,2, "Remark:", bottun_left1)

        sheet.fit_to_pages(1, 0)

