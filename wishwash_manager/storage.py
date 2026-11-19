"""storage.py - class PesananStorage: baca/tulis data pesanan ke berkas dengan with open().
Mode yang dipakai: 'r' (muat), 'x' (buat berkas baru), 'a' (tambah satu baris)."""

import csv
import os

from services import KOLOM, Pesanan


class PesananStorage:
    """Penyimpanan data pesanan ke berkas pada `path`."""

    def __init__(self, path):
        self.path = path

    def muat(self):
        """Membaca semua pesanan. Mengembalikan (daftar_pesanan, daftar_peringatan).
        Berkas hilang atau baris rusak tidak membuat program crash."""
        hasil, peringatan = [], []
        try:
            with open(self.path, "r", newline="", encoding="utf-8") as berkas:
                for nomor, baris in enumerate(csv.DictReader(berkas), start=2):
                    try:
                        hasil.append(Pesanan.dari_baris(baris))
                    except ValueError as galat:
                        peringatan.append(f"Baris {nomor} dilewati: {galat}")
        except FileNotFoundError:
            self._buat_berkas_kosong()
            peringatan.append("Berkas data belum ada, berkas baru dibuat.")
        except ValueError as galat:  # isi berkas tidak terbaca sama sekali
            hasil = []
            peringatan.append(f"Berkas data rusak ({galat}), mulai dengan data kosong.")
        return hasil, peringatan

    def tambah_baris(self, pesanan):
        """Menambah satu pesanan di akhir berkas (mode 'a')."""
        perlu_header = not os.path.exists(self.path) or os.path.getsize(self.path) == 0
        with open(self.path, "a", newline="", encoding="utf-8") as berkas:
            penulis = csv.DictWriter(berkas, fieldnames=KOLOM)
            if perlu_header:
                penulis.writeheader()
            penulis.writerow(pesanan.ke_baris())

    def _buat_berkas_kosong(self):
        """Membuat berkas baru berisi header saja (mode 'x': gagal jika sudah ada)."""
        os.makedirs(os.path.dirname(self.path) or ".", exist_ok=True)
        try:
            with open(self.path, "x", newline="", encoding="utf-8") as berkas:
                csv.DictWriter(berkas, fieldnames=KOLOM).writeheader()
        except FileExistsError:
            pass
