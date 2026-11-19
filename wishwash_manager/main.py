"""main.py - demo konsol untuk progres minggu ini (tampilan GUI nya menyusulll)."""

import os

from services import PesananService
from storage import PesananStorage
from validasi import LAYANAN_HARGA

LOKASI = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "pesanan.csv")

def cetak(daftar):
    """Mencetak daftar pesanan sebagai tabel teks."""
    print(f"{'ID':<9}{'Nama':<18}{'Layanan':<14}{'Jml':>5}{'Total':>9}  {'Status':<10}Tanggal")
    for p in daftar:
        print(f"{p.id_pesanan:<9}{p.nama_pelanggan:<18}{p.layanan:<14}{p.jumlah:>5g}"
              f"{p.total:>9}  {p.status:<10}{p.tanggal_masuk}")
    print(f"({len(daftar)} pesanan)")

def main():
    """Memuat data, lalu menjalankan menu konsol sederhana."""
    service = PesananService(PesananStorage(LOKASI))
    for pesan in service.muat():
        print("Peringatan:", pesan)
    while True:
        print("\n1. Tampilkan\n2. Cari nama\n3. Urutkan\n4. Tambah\n0. Keluar")
        pilihan = input("Pilih: ").strip()
        try:
            if pilihan == "1":
                cetak(service.semua())
            elif pilihan == "2":
                cetak(service.cari_nama(input("Kata kunci: ")))
            elif pilihan == "3":
                kolom = input("Kolom (total/jumlah/nama_pelanggan/tanggal_masuk): ").strip()
                menurun = input("Menurun? (y/n): ").strip().lower() == "y"
                cetak(service.urutkan(service.semua(), kolom, menurun))
            elif pilihan == "4":
                p = service.tambah(input("Nama: "), input(f"Layanan {list(LAYANAN_HARGA)}: "), input("Jumlah: "))
                print("Ditambahkan:", p.id_pesanan)
            elif pilihan == "0":
                break
        except ValueError as galat:  # input salah ditangkap, program tidak crash
            print("Input tidak valid:", galat)


if __name__ == "__main__":
    main()
