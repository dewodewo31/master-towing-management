{
    "name": "Management Towing",
    "version": "1.0",
    "author": "Expertri.id",
    "website": "https://expertri.id/",
    "category": "Custom",
    "summary": "Modul yang digunakan untuk mengatur data kendaraan towing",
    "description": """
Modul ini memungkinkan Anda mengelola data master untuk mobil yang digunakan dalam Towing Services.
Fitur utama:
- Manajemen data kendaraan towing
- Integrasi dengan modul Sales untuk mencatat layanan terkait
    """,
    "depends": [
        "base",  # Modul utama
        "sale"   # Dibutuhkan untuk integrasi dengan Sales
    ],
    "data": [
        "security/ir.model.access.csv",  # Pengaturan hak akses
        "views/master_towing_view.xml",  # Tampilan data master towing
        "views/sale_order_views.xml"    # Integrasi dengan Sales Order
    ],
    "demo": [
        # Tambahkan file demo data jika ada, misalnya:
        # "demo/master_towing_demo.xml"
    ],
    "installable": True,
    "application": True,
    "auto_install": False,
    "license": "AGPL-3"  # Lisensi modul
}
