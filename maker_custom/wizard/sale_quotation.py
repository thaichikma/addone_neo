from functools import reduce
from odoo import models , fields, api, _
from odoo.modules.module import get_module_resource
from datetime import datetime
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError


class AbstractInventoryReport(models.AbstractModel):
    _name = "report.maker_custom.quotation"
    _inherit = "report.report_xlsx.abstract"

    def generate_xlsx_report(self, workbook, data, partner):
        sale_id = partner['id']
        query = f"""
                    select COALESCE(s_line.name, ''),
                        COALESCE(s_line.x_product_model, ''),
                        COALESCE(s_line.product_uom_qty, 0),
                        uom.name ->> 'en_US' as uom,
                        COALESCE(s_line.price_unit , 0),
                        COALESCE(s_line.price_subtotal ,0),
                        COALESCE(maker.name, '')
                    from sale_order_line as s_line
                        left join uom_uom as uom on s_line.product_uom = uom.id
                        left join xres_maker as maker on s_line.x_product_maker = maker.id
                    where s_line.order_id = '{sale_id}'
                """

        self._cr.execute(query)
        result = self._cr.fetchall()
        # set sheet name
        sheet = workbook.add_worksheet("Quotation")
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
        header = workbook.add_format({
            "bold": True, "font_size": 18, "font_name": "Times New Roman",
            "align": "center", "valign": "vcenter"
        })
        header_gray = workbook.add_format({
            "bold": True, "font_size": 12, "italic": True, "font_name": "Times New Roman", 'font_color': 'gray',
            "align": "center", "valign": "vcenter"
        })
        normal = workbook.add_format({"font_size": 11,
                                      "font_name": "Times New Roman"})
        normal_border = workbook.add_format({"font_size": 12, "border": 2, "font_name": "Times New Roman"})
        normal.set_text_wrap()
        normal_border.set_text_wrap()
        table_header1 = workbook.add_format({
            "font_size": 11,
            "font_name": "Times New Roman",
            "border": 1,
            "align": "center", "valign": "vcenter", "text_wrap": True
        })
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
        tieude1 = workbook.add_format({
            "font_size": 20,
            "font_name": "Calibri",
            "align": "center",
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
        italic = workbook.add_format({
            "bold": True, "font_size": 18, "font_name": "Times New Roman",
            "align": "center", "valign": "vcenter","italic": True
        })
        sheet.insert_image('A1', get_module_resource('maker_custom', 'images', 'logo.png'),
                           {'x_scale': 0.22, 'y_scale': 0.22})
        quotation = self.env['sale.order'].search([('id', '=', sale_id)])
        company = quotation.company_id or " "
        name_company = company.name or " "
        street_company = company.street or " "
        sheet.insert_image('H1', get_module_resource('maker_custom', 'images', 'logoinfo.png'),
                           {'x_scale': 1, 'y_scale': 1})

        sheet.merge_range("D5:G6", 'Quotation', quotation_format)

        company_kh = quotation.partner_id or " "
        name_company_kh = company_kh.name or " "
        street_company_kh = company_kh.street or " "
        phone_1 = company_kh.phone or " "
        phone_2 = company_kh.phone_sanitized or " "
        contact = quotation.x_contact_id.name or " "
        email = company_kh.email
        function = quotation.x_contact_id.function
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

        sheet.write("G7", "QUOTATION No.", header_right)
        sheet.write("G8", "Date", header_right)
        sheet.write("G9", "Validity.", header_right)
        sheet.write("G10", "Delivery Term.", header_right)
        sheet.write("G11", "Destination.", header_right)
        sheet.write("G12", "Delivery time.", header_right)
        sheet.write("G13", "Payment Term.", header_right)
        sheet.write("G14", "GRAND TOTAL.", header_right)

        x_validity_day = quotation.x_validity_day or " "


        # Tạo chuỗi định dạng "X week(s)"

        x_quotation_date = quotation.x_quotation_date or " "
        formatted_date = x_quotation_date.strftime('%d-%b-%Y')
        commitment_date = quotation.commitment_date or " "
        weeks_difference = (commitment_date - x_quotation_date).days // 7
        formatted_string = f"{weeks_difference} week(s)"

        payment_term = quotation.payment_term_id.name or " "
        x_lead_time = quotation.x_lead_time or " "
        amount_total = quotation.amount_total
        sheet.insert_image('J7', get_module_resource('maker_custom', 'images', 'logo3.png'),
                           {'x_scale': 1, 'y_scale': 1})
        partner_shipping_id = quotation.partner_shipping_id.street
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
        sheet.write("H16", "UNIT PRICE(USD)", le_tren)
        sheet.write("I16", "AMOUNT(USD)", le_tren)
        sheet.write("J16", "MAKER", le_tren)
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
            sheet.write(row, 8, report[5], quantity)
            sheet.write(row, 9, report[6], quantity)

            row += 1
            stt += 1
        amount_tax = quotation.amount_tax
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
        sheet.merge_range(row+4, 0,row+4, 6, "Term and Conditions", bottun_left1)
        sheet.merge_range(row+5, 0,row+5, 6, "①      Currency of payment: United States Dollar(USD)", bottun_left)
        sheet.merge_range(row+6, 0,row+6, 6, "②	     Warranty as manufacturer's standard.", bottun_left)
        sheet.merge_range(row+7, 0,row+8, 6, "③    	 This price is applied for the whole purchasing only. Price of optional accessories (if any) are applied if bought with main unit.", bottun_left)
        sheet.merge_range(row+9, 0,row+9, 6, "④	     Please confirm specification before order. Any changes in spec or quantity should be re-quoted.", bottun_left)
        sheet.merge_range(row+10, 0,row+11, 6, "⑤	   We reserve the right to confirm at your customer site existence of the goods that we will have supplied to you conforming to your PO.", bottun_left)
        sheet.merge_range(row+12, 0,row+14, 6, "⑥	   The product marked by an asterisk mark (*) at the No. column is regulated its export and/or supply by the Foreign Exchange. Act and Foreign Trade Act of Japan. Export/supply is allowed only with an appropriate governmental authorization.", bottun_left)
        sheet.merge_range(row+15, 0,row+17, 6, "⑦	     We reserve the right to cancel a part or the whole of your purchase order without any penalty even after we have acknowledged the order to you in case that the appropriate export license and/or the technology provision license are not issued to us by the Japanese government.", bottun_left)
        sheet.merge_range(row+18, 0,row+18, 6, "⑧	   Please note that the bank fee is fully covered by the payer.", bottun_left)
        sheet.merge_range(row+19, 0,row+19, 6, "⑨	   Once order has been placed, cancellation or return of items will not be accepted", bottun_left)

        sheet.fit_to_pages(1, 0)

