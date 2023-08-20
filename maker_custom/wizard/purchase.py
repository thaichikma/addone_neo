from functools import reduce
from odoo import models , fields, api, _
from odoo.modules.module import get_module_resource
from datetime import datetime
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError


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
        purchase = self.env['purchase.order'].search([('id', '=', purchase_id)])
        company = purchase.company_id or " "
        name_company = company.name or " "
        street_company = company.street or " "
        sheet.insert_image('H1', get_module_resource('maker_custom', 'images', 'logoinfo.png'),
                           {'x_scale': 1, 'y_scale': 1})

        sheet.merge_range("D5:G6", 'PURCHASE ORDER', quotation_format)

        company_kh = purchase.partner_id or " "
        name_company_kh = company_kh.name or " "
        street_company_kh = company_kh.street or " "
        phone_1 = company_kh.phone or " "
        phone_2 = company_kh.phone_sanitized or " "
        contact = purchase.x_contact_id.name or " "
        email = company_kh.email
        function = purchase.x_contact_id.function
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

        sheet.write("G7", "PURCHASE No.", header_right)
        sheet.write("G8", "Date", header_right)
        sheet.write("G9", "Delivery Term.", header_right)
        sheet.write("G10", "Destination.", header_right)
        sheet.write("G11", "Delivery time.", header_right)
        sheet.write("G12", "Payment Term.", header_right)
        sheet.write("G13", "Staffcode", header_right)
        sheet.write("G14", "Your Quotation", header_right)
        sheet.write("G15", "End-user", header_right)
        sheet.write("G15", "Collaboration Job", header_right)

        # Tạo chuỗi định dạng "X week(s)"
        purchase_no = purchase.name or ' '
        x_purchase_date = purchase.date_approve or " "
        formatted_date = x_purchase_date.strftime('%d-%b-%Y')
        effective = purchase.effective_date or " "
        effective_date = effective.strftime('%d-%b-%Y')


        sheet.insert_image('J7', get_module_resource('maker_custom', 'images', 'logo3.png'),
                           {'x_scale': 1, 'y_scale': 1})

        sheet.merge_range("H7:I7", purchase_no, header_right3)
        sheet.merge_range("H8:I8", formatted_date, header_right3)
        sheet.merge_range("H9:I9", effective_date, header_right1)
        sheet.merge_range("H10:I10", "x_lead_time", header_right1)
        sheet.merge_range("H11:I11", "partner_shipping_id", header_right1)
        sheet.merge_range("H12:J12", "formatted_string", header_right1)
        sheet.merge_range("H13:J13", "payment_term", header_right1)
        sheet.merge_range("H14:J14", "amount_total", header_right2)


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

        sheet.write("A17", "No.", le_tren)
        sheet.merge_range("B17:D17", "ITEMS / DESCRIPTION", le_tren)
        sheet.write("E17", "MODEL", le_tren)
        sheet.write("F17", "Quantity", le_tren)
        sheet.write("G17", "Unit", le_tren)
        sheet.write("H17", "AMOUNT (VND)", le_tren)
        sheet.write("I17", "MAKER", le_tren)
        # table data
        row = 18
        stt = 0
        for report in result:
            sheet.write(row, 0, stt + 1, table_data)
            sheet.merge_range(row, 1,row, 3, report[0], product)
            sheet.write(row, 4, report[1], product)
            sheet.write(row, 5, report[2], table_data)
            sheet.write(row, 6, report[3], table_data)
            sheet.write(row, 7, report[4], quantity)
            sheet.write(row, 8, report[5], quantity)
            row += 1
            stt += 1
        amount_tax = purchase.amount_tax
        amount_total = purchase.amount_total
        amount_untaxed = purchase.amount_untaxed
        sheet.write(row, 7, "Sub Total", table_data)
        sheet.write(row + 1, 7, "Tax VAT", table_data)
        sheet.write(row + 2, 7, "GRAND TOTAL", table_data)
        sheet.write(row, 8, amount_untaxed, table_data)
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
        sheet.write(row+4, 1, "Terms and Conditions", bottun_left1)
        sheet.merge_range(row+4, 0,row+4, 6, "①	    Please inform the Deliver schedule once you approved this Order.", bottun_left1)
        sheet.merge_range(row+5, 0,row+5, 6, "②	    Please send back the PO confirmation.", bottun_left)
        sheet.merge_range(row+6, 0,row+6, 6, "③	    (for Service Order) All tax obligations that arise in Vietnam will be paid by Nihon Denkei Vietnam.", bottun_left)

        sheet.merge_range(row+7, 1,row+7, 3, "TOSHIBA TRANSMITION", bottun_left)
        sheet.merge_range(row + 8, 1, row + 8, 3, "We hereby agree and confirm our ", bottun_left)
        sheet.merge_range(row + 9, 1, row + 9, 3, "acceptance of this order", bottun_left)

        sheet.merge_range(row+7, 7,row+7, 9, "NEOTECH SOLUTION JSC", bottun_left)

        sheet.fit_to_pages(1, 0)

