"""validasi.py - validasi input pesanan; kesalahan dilaporkan dengan raise ValueError."""

import math
from datetime import datetime

# Layanan dan harga satuannya (Rp per kg atau per item), disimpan di satu tempat.
LAYANAN_HARGA = {"Cuci Kering": 6000, "Cuci Setrika": 8000, "Setrika Saja": 5000,
                "Selimut": 25000, "Jaket": 15000}
DAFTAR_STATUS = ["Diterima", "Dicuci", "Disetrika", "Selesai", "Diambil"]

def _teks_wajib(nilai, nama_field):
    """Memastikan teks tidak kosong; mengembalikan teks yang sudah dirapikan."""
    if nilai is None or not str(nilai).strip():
        raise ValueError(f"{nama_field} wajib diisi.")
    return " ".join(str(nilai).split())

def _pilihan(nilai, daftar, nama_field):
    """Memastikan nilai termasuk dalam daftar pilihan yang tersedia."""
    if nilai not in daftar:
        raise ValueError(f"{nama_field} tidak dikenal. Pilih: {', '.join(daftar)}.")
    return nilai

def validasi_jumlah(jumlah):
    """Jumlah (kg/item) harus angka lebih dari 0; koma desimal diterima."""
    try:
        angka = float(str(jumlah).strip().replace(",", "."))
    except ValueError:
        raise ValueError("Jumlah harus berupa angka.") from None
    if not math.isfinite(angka) or angka <= 0:
        raise ValueError("Jumlah harus lebih dari 0.")
    return angka

def validasi_harga(harga):
    """Harga satuan harus bilangan bulat dan tidak boleh negatif."""
    try:
        angka = int(str(harga).strip())
    except ValueError:
        raise ValueError("Harga harus berupa bilangan bulat.") from None
    if angka < 0:
        raise ValueError("Harga tidak boleh negatif.")
    return angka

def validasi_tanggal(tanggal):
    """Tanggal harus berformat YYYY-MM-DD dan ada di kalender."""
    try:
        datetime.strptime(str(tanggal).strip(), "%Y-%m-%d")
    except ValueError:
        raise ValueError("Tanggal harus berformat YYYY-MM-DD.") from None
    return str(tanggal).strip()

def validasi_pesanan(id_pesanan, nama_pelanggan, layanan, jumlah,
                     harga_satuan, status, tanggal_masuk):
    """Menjalankan semua validasi, mengembalikan dict nilai bersih atau melempar ValueError."""
    return {
        "id_pesanan": _teks_wajib(id_pesanan, "ID pesanan").upper(),
        "nama_pelanggan": _teks_wajib(nama_pelanggan, "Nama pelanggan"),
        "layanan": _pilihan(layanan, LAYANAN_HARGA, "Layanan"),
        "jumlah": validasi_jumlah(jumlah),
        "harga_satuan": validasi_harga(harga_satuan),
        "status": _pilihan(status, DAFTAR_STATUS, "Status"),
        "tanggal_masuk": validasi_tanggal(tanggal_masuk),
    }
