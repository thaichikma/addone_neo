from functools import reduce
from odoo import models , fields, api, _
from odoo.modules.module import get_module_resource
from datetime import datetime
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError


class AbstractInventoryReport(models.AbstractModel):
    _name = "report.maker_custom.delivery"
    _inherit = "report.report_xlsx.abstract"

    def generate_xlsx_report(self, workbook, data, partner):
        picking_id = partner['id']
        query = f"""
                    select COALESCE(sm.name, ''),
                        COALESCE(pt.x_model, ''),
                        COALESCE(sm.quantity_done, 0),
                        uom.name ->> 'en_US' as uom,
                        COALESCE(sm.origin, ''),
                        COALESCE(pt.note, '')
                    from stock_move as sm
                        left join product_product as pp on sm.product_id = pp.id
                        left join product_template as pt on pp.product_tmpl_id = pt.id
                        left join uom_uom as uom on s_line.product_uom = uom.id
                    where sm.picking_id = '{picking_id}'
                """

        self._cr.execute(query)
        result = self._cr.fetchall()
        # set sheet name
        sheet = workbook.add_worksheet("Delivery")
        # set column width, row
        sheet.set_column("A:A", 7)
        sheet.set_column("B:B", 12)
        sheet.set_column("C:C", 14)
        sheet.set_column("D:D", 14)
        sheet.set_column("E:E", 15)
        sheet.set_column("G:G", 18)
        sheet.set_column("H:H", 17)
        sheet.set_column("I:I", 17)
        sheet.set_column("J:J", 18)
        sheet.set_row(0, 20)
        sheet.set_row(1, 20)
        sheet.set_row(2, 20)
        sheet.set_row(3, 20)
        sheet.set_row(4, 25)
        sheet.set_row(5, 25)
        sheet.set_row(15, 25)
        # style format
        normal = workbook.add_format({"font_size": 11,
                                      "font_name": "Times New Roman"})
        normal_border = workbook.add_format({"font_size": 12, "border": 2, "font_name": "Times New Roman"})
        normal.set_text_wrap()
        normal_border.set_text_wrap()
        table_header = workbook.add_format({
            "font_size": 11,
            "font_name": "Times New Roman",
            "border": 1,
            "align": "left", "valign": "vcenter", "text_wrap": True
        })
        table_header.set_text_wrap()

        table_data = workbook.add_format({
            "font_size": 11, "border": 1,
            "font_name": "Times New Roman",
            "align": "center", "valign": "vcenter"
        })
        product = workbook.add_format({
            "font_size": 11, "border": 1,
            "font_name": "Times New Roman",
            "align": "left", "valign": "vcenter", "text_wrap": True
        })
        quantity = workbook.add_format({
            "font_size": 11, "border": 1,
            "font_name": "Times New Roman",
            "align": "right", "valign": "vcenter"
        })
        tieude = workbook.add_format({
            "font_size": 11,
            "font_name": "Times New Roman",
            "align": "left",
        })
        quotation_format = workbook.add_format({
            "font_size": 36,"bold": True,
            "font_name": "Calibri",
            "align": "center",
        })

        header_tieude = workbook.add_format({
            "bold": True, "font_size": 11, "font_name": "Times New Roman",
            "align": "right", "valign": "vcenter"
        })
        header_right = workbook.add_format({
            "bold": True, "font_size": 11, "font_name": "Calibri",
            "align": "left", "valign": "vcenter"
        })
        header_right3 = workbook.add_format({
            "bold": True, "font_size": 11, "font_name": "Calibri",
            "align": "left", "valign": "vcenter","bottom": 1,
        })

        header_right1 = workbook.add_format({
            "font_size": 11, "font_name": "Calibri",
            "align": "left", "valign": "vcenter","bottom": 1,
        })
        header_right2 = workbook.add_format({
            "bold": True, "font_size": 11, "font_name": "Calibri",
            "align": "left", "valign": "vcenter","font_color": "#FF0000",
        })
        # add logo
        sheet.insert_image('A1', get_module_resource('maker_custom', 'images', 'logo.png'),
                           {'x_scale': 0.22, 'y_scale': 0.22})
        delivery = self.env['stock.move'].search([('id', '=', picking_id)])
        company = delivery.company_id or " "
        name_company = company.name or " "
        street_company = company.street or " "
        sheet.insert_image('H1', get_module_resource('maker_custom', 'images', 'logoinfo.png'),
                           {'x_scale': 1, 'y_scale': 1})

        sheet.merge_range("D5:G6", 'Quotation', quotation_format)

        company_kh = delivery.partner_id or " "
        name_company_kh = company_kh.name or " "
        street_company_kh = company_kh.street or " "
        phone_1 = company_kh.phone or " "
        phone_2 = company_kh.phone_sanitized or " "
        contact = delivery.x_contact_id.name or " "
        email = company_kh.email
        function = delivery.x_contact_id.function
        sheet.write("A7", "Messrs.", header_tieude)
        sheet.insert_image('A9', get_module_resource('maker_custom', 'images', 'icon_location.png'),
                           {'x_scale': 1, 'y_scale': 1})
        sheet.insert_image('A10', get_module_resource('maker_custom', 'images', 'icon_mobile.png'),
                           {'x_scale': 1, 'y_scale': 1})
        sheet.insert_image('A11', get_module_resource('maker_custom', 'images', 'icon_telephone.png'),
                           {'x_scale': 1, 'y_scale': 1})
        sheet.insert_image('A12', get_module_resource('maker_custom', 'images', 'icon_contact.png'),
                           {'x_scale': 1, 'y_scale': 1})
        sheet.insert_image('A13', get_module_resource('maker_custom', 'images', 'icon_position.png'),
                           {'x_scale': 1, 'y_scale': 1})
        sheet.insert_image('A14', get_module_resource('maker_custom', 'images', 'icon_email.png'),
                           {'x_scale': 1, 'y_scale': 1})

        sheet.merge_range("B8:D8", name_company_kh, tieude)
        sheet.merge_range("B9:D9", street_company_kh, tieude)
        sheet.merge_range("B10:D10", phone_1, tieude)
        sheet.merge_range("B11:D11", phone_2, tieude)
        sheet.merge_range("B12:D12", contact, tieude)
        sheet.merge_range("B13:D13", function, tieude)
        sheet.merge_range("B14:D14", email, tieude)
        # sheet.set_border(6, 0, 13, 3, 1)

        sheet.write("G7", "DELIVERY No.", header_right)
        sheet.write("G8", "Date", header_right)
        sheet.write("G9", "Delivery Term.", header_right)
        sheet.write("G10", "Destination.", header_right)
        sheet.write("G11", "Delivery time.", header_right)
        sheet.write("G12", "Payment Term.", header_right)
        sheet.write("G14", "Your PO No", header_right)

        x_validity_day = delivery.x_validity_day or " "


        # Tạo chuỗi định dạng "X week(s)"

        x_quotation_date = delivery.x_quotation_date or " "
        formatted_date = x_quotation_date.strftime('%d-%b-%Y')
        commitment_date = delivery.commitment_date or " "
        weeks_difference = (commitment_date - x_quotation_date).days // 7
        formatted_string = f"{weeks_difference} week(s)"

        payment_term = delivery.payment_term_id.name or " "
        x_lead_time = delivery.x_lead_time or " "
        amount_total = delivery.amount_total
        sheet.insert_image('J7', get_module_resource('maker_custom', 'images', 'logo3.png'),
                           {'x_scale': 1, 'y_scale': 1})
        partner_shipping_id = delivery.partner_shipping_id.street
        sheet.merge_range("H7:I7", "QUOTATION No.", header_right3)
        sheet.merge_range("H8:I8", formatted_date, header_right3)
        sheet.merge_range("H9:I9", str(x_validity_day)+' day(s)', header_right1)
        sheet.merge_range("H10:I10", x_lead_time, header_right1)
        sheet.merge_range("H11:I11", partner_shipping_id, header_right1)
        sheet.merge_range("H12:J12", formatted_string, header_right1)
        sheet.merge_range("H13:J13", payment_term, header_right1)
        sheet.merge_range("H14:J14", amount_total, header_right2)


        # table header
        le_tren = workbook.add_format({
            "bold": True, "font_size": 11,
            "font_name": "Calibri",
            "align": "center", "valign": "vcenter",
            "bg_color": "#000000",  # Đặt màu nền đen
            "font_color": "#FFFFFF",  # Đặt màu chữ trắng
            "border": 1,  # Thêm viền
            "border_color": "#FFFFFF"
        })

        sheet.write("A16", "No.", le_tren)
        sheet.merge_range("B16:D16", "ITEMS / DESCRIPTION", le_tren)
        sheet.write("E16", "MODEL", le_tren)
        sheet.write("F16", "Quantity", le_tren)
        sheet.write("G16", "Unit", le_tren)
        sheet.write("H16", "CHECK", le_tren)
        sheet.merge_range("I16:J16", "REMARK", le_tren)
        # table data
        row = 17
        stt = 0
        for report in result:
            sheet.write(row, 0, stt + 1, table_data)
            sheet.merge_range(row, 1,row, 3, report[0], product)
            sheet.write(row, 4, report[1], product)
            sheet.write(row, 5, report[2], table_data)
            sheet.write(row, 6, report[3], table_data)
            sheet.write(row, 7, report[4], quantity)
            sheet.merge_range(row, 8,row,9, report[5], quantity)

            row += 1
            stt += 1
        sheet.merge_range(row, 0,row,9, 'II – Shipping and payment documents come with', quantity)
        amount_tax = delivery.amount_tax
        sheet.write(row, 7, "Sub Total", table_data)
        sheet.write(row+1, 7, "Tax VAT", table_data)
        sheet.write(row+2, 7, "GRAND TOTAL", table_data)
        sheet.write(row, 8, "???", table_data)
        sheet.write(row + 1, 8, amount_tax, table_data)
        sheet.write(row + 2, 8, amount_total, table_data)

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
        sheet.merge_range(row + 4, 7, row + 4, 9, "NEOTECH SOLUTION JSC ", bottun_center)
        sheet.write(row+4, 1, "Remark:", bottun_left1)
        sheet.merge_range(row + 4, 2, row + 4, 6, "Warranty as manufacturer's standard and applied for main unit only.", bottun_left1)
        sheet.merge_range(row + 4, 2, row + 4, 6, "By sign into this document, you confirm to receive the goods:",bottun_left1)
        sheet.merge_range(row+5, 0,row+5, 6, "①    	Goods in good conditions and Same as mentioned on your PO.", bottun_left)
        sheet.merge_range(row+6, 0,row+6, 6, "②	    All Appropriate documents shown above for this shipment.", bottun_left)
        sheet.merge_range(row+7, 0,row+8, 6, "③	    All goods are completely installed and calibrated.", bottun_left)

        sheet.merge_range(row+10, 0,row+11, 6, "for TOSHIBA TRANSMISSION & DISTRIBUTION SYSTEMS (VIETNAM) LTD", bottun_left)
        sheet.merge_range(row+10, 7,row+10, 9, "for NEOTECH SOLUTION JSC", bottun_left)

        sheet.fit_to_pages(1, 0)

