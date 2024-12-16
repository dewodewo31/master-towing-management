from datetime import date, timedelta
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class CarsTowing(models.Model):
    _name = 'cars.towing'
    _description = 'Mobil Towing'

    name = fields.Char(string='Nama Mobil', required=True)
    license_plate = fields.Char(string='Nomor Plat Lisensi', required=True)
    license_stnk = fields.Char(string='Nomor STNK Lisensi', required=True)
    engine_num = fields.Char(string='Nomor Mesin Mobil', required=True)
    towing_type = fields.Selection([
        ('flatbed', 'Flatbed (Datar)'),
        ('wheel_lift', 'Wheel Lift (Pengangkat Roda)'),
        ('integrated', 'Integrated')
    ], string='Jenis Towing', required=True, default='flatbed')
    capacity = fields.Integer(string='Kapasitas Towing (kg)', required=True)
    status = fields.Selection([
        ('aktif', 'Aktif'),
        ('maintenance', 'Maintenance'),
        ('non_aktif', 'Non-Aktif')
    ], string='Status Mobil', default='aktif')
    registration_date = fields.Date(string='Tanggal Pendaftaran', default=fields.Date.today)
    stnk_expiry_date = fields.Date(string='Tanggal Kadaluarsa STNK')
    description = fields.Text(string='Deskripsi Towing')
    image = fields.Image(string='Foto Mobil Towing')
    stnk_status = fields.Char(string='Status STNK', compute='_compute_stnk_status', store=True)
    driver_id = fields.Many2one(
        'towing.driver',
        string='Driver',
        domain=[('status', '=', 'aktif')],
        help="Driver yang bertanggung jawab untuk mobil towing ini."
    )
    job_id = fields.Char(string='ID Pekerjaan')
    usage_count = fields.Integer(
        string='Jumlah Penggunaan Bulan Ini',
        compute='_compute_usage_count',
        store=True
    )
    sale_order_line_ids = fields.One2many(
        'sale.order.line', 
        'towing_id', 
        string='Pesanan Penjualan Terkait'
    )

    @api.depends('sale_order_line_ids.order_id.date_order', 'sale_order_line_ids.state')
    def _compute_usage_count(self):
        today = date.today()
        start_of_month = today.replace(day=1)
        end_of_month = (start_of_month + timedelta(days=32)).replace(day=1) - timedelta(days=1)
        
        for record in self:
            count = sum(1 for line in record.sale_order_line_ids
                        if start_of_month <= line.order_id.date_order.date() <= end_of_month
                        and line.state in ['sale', 'done'])
            record.usage_count = count


class TowingDriver(models.Model):
    _name = 'towing.driver'
    _description = 'Driver Towing'

    name = fields.Char(string='Nama Driver', required=True)
    employee_id = fields.Char(string='ID Karyawan', required=True)
    phone = fields.Char(string='Nomor Telepon', required=True)
    email = fields.Char(string='Email')
    license_number = fields.Char(string='Nomor SIM', required=True)
    license_expiry_date = fields.Date(string='Tanggal Kadaluarsa SIM', required=True)
    experience_years = fields.Integer(string='Pengalaman (Tahun)', required=True)
    status = fields.Selection([
        ('aktif', 'Aktif'),
        ('non_aktif', 'Non-Aktif'),
        ('cuti', 'Cuti')
    ], string='Status Driver', default='aktif')
    license_status = fields.Char(string='Status SIM', compute='_compute_license_status', store=True)
    photo = fields.Image(string='Foto Driver')
    notes = fields.Text(string='Catatan')

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    towing_id = fields.Many2one(
        'cars.towing',
        string='Mobil Towing',
        domain=[('status', '=', 'aktif')]
    )
    towing_name_and_plate = fields.Char(
        string='Detail Towing (Jenis | Plat)',
        compute='_compute_towing_name_and_plate',
        store=True
    )
    driver_name = fields.Char(
        string='Nama Driver',
        compute='_compute_driver_name',
        store=True
    )
    employee_id = fields.Char(
        string='ID Karyawan',
        compute='_compute_employee_id',
        store=True
    )

    @api.depends('towing_id')
    def _compute_towing_name_and_plate(self):
        for record in self:
            if record.towing_id:
                towing_type = dict(self.env['cars.towing'].fields_get(['towing_type'])['towing_type']['selection']).get(record.towing_id.towing_type, '')
                record.towing_name_and_plate = f"{towing_type} | {record.towing_id.license_plate}"
            else:
                record.towing_name_and_plate = ''

    @api.depends('towing_id')
    def _compute_driver_name(self):
        for record in self:
            if record.towing_id and record.towing_id.driver_id:
                record.driver_name = record.towing_id.driver_id.name
            else:
                record.driver_name = ''

    @api.depends('towing_id')
    def _compute_employee_id(self):
        for record in self:
            if record.towing_id and record.towing_id.driver_id:
                record.employee_id = record.towing_id.driver_id.employee_id
            else:
                record.employee_id = ''
