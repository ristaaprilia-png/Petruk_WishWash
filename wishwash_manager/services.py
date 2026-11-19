"""services.py - logika data pesanan: class Pesanan dan PesananService,
merge sort, linear search, serta fungsi dengan *args dan **kwargs."""

import re
from datetime import date

from validasi import LAYANAN_HARGA, validasi_pesanan

# Urutan kolom data (dipakai juga sebagai header berkas oleh storage.py).
KOLOM = ["id_pesanan", "nama_pelanggan", "layanan", "jumlah",
        "harga_satuan", "total", "status", "tanggal_masuk"]

class Pesanan:
    """Satu pesanan laundry; data divalidasi saat objek dibuat."""

    def __init__(self, id_pesanan, nama_pelanggan, layanan, jumlah,
                harga_satuan, status="Diterima", tanggal_masuk=None):
        data = validasi_pesanan(id_pesanan, nama_pelanggan, layanan, jumlah, harga_satuan,
                                status, tanggal_masuk or date.today().isoformat())
        for nama, nilai in data.items():
            setattr(self, nama, nilai)

    @property
    def total(self):
        """Total biaya = jumlah x harga satuan (dihitung otomatis)."""
        return int(round(self.jumlah * self.harga_satuan))

    def ke_baris(self):
        """Mengubah pesanan menjadi dict (satu baris data) untuk disimpan."""
        baris = {k: getattr(self, k) for k in KOLOM}
        baris["jumlah"] = f"{self.jumlah:g}"
        return baris

    @classmethod
    def dari_baris(cls, baris):
        """Membuat Pesanan dari dict, ValueError jika kolom hilang atau nilai tidak valid."""
        try:
            return cls(**{k: baris[k] for k in KOLOM if k != "total"})
        except KeyError as galat:
            raise ValueError(f"kolom {galat} tidak ditemukan") from None

def merge_sort(data, key=lambda x: x, menurun=False):
    """key = fungsi pembanding (lambda), menurun = urutan terbalik."""
    if len(data) <= 1:
        return list(data)
    tengah = len(data) // 2
    kiri, kanan = merge_sort(data[:tengah], key, menurun), merge_sort(data[tengah:], key, menurun)
    hasil, i, j = [], 0, 0
    while i < len(kiri) and j < len(kanan):
        a, b = key(kiri[i]), key(kanan[j])
        if (a >= b) if menurun else (a <= b):  # nilai sama: ambil kiri dulu agar stabil
            hasil.append(kiri[i])
            i += 1
        else:
            hasil.append(kanan[j])
            j += 1
    return hasil + kiri[i:] + kanan[j:]

def linear_search_nama(daftar, kata):
    """Pencarian linear berdasarkan nama pelanggan"""
    kata = kata.strip().lower()
    return [p for p in daftar if kata in p.nama_pelanggan.lower()]

def hitung_total(*args):
    """Menjumlahkan total dari sejumlah pesanan (*args)."""
    return sum(p.total for p in args)

def filter_pesanan(daftar, **kwargs):
    """Menyaring pesanan menurut atribut apa pun lewat **kwargs, contoh status="Dicuci"."""
    for nama in kwargs:
        if nama not in KOLOM:
            raise ValueError(f"Filter '{nama}' tidak dikenal.")
    return [p for p in daftar
            if all(str(getattr(p, k)).lower() == str(v).lower() for k, v in kwargs.items())]

# Kunci pengurutan per kolom (lambda): satu merge_sort melayani semua kolom.
KUNCI_URUT = {k: (lambda p, k=k: getattr(p, k)) for k in KOLOM}
KUNCI_URUT["nama_pelanggan"] = lambda p: p.nama_pelanggan.lower()

class PesananService:
    """Mengelola daftar pesanan; `storage` boleh None (data hanya di memori, untuk uji)."""

    def __init__(self, storage=None):
        self.storage = storage
        self._data = []

    def muat(self):
        """Memuat data dari penyimpanan; mengembalikan list peringatan."""
        if self.storage is None:
            return []
        self._data, peringatan = self.storage.muat()
        return peringatan

    def semua(self):
        """Salinan seluruh daftar pesanan."""
        return list(self._data)

    def id_berikutnya(self):
        """ID baru berformat ORD-001, ORD-002, ... mengikuti ID terbesar."""
        nomor = [int(m.group(1)) for p in self._data
                if (m := re.fullmatch(r"ORD-(\d+)", p.id_pesanan))]
        return f"ORD-{max(nomor, default=0) + 1:03d}"

    def tambah(self, nama_pelanggan, layanan, jumlah, harga_satuan=None,
            status="Diterima", tanggal_masuk=None, id_pesanan=None):
        """Menambah pesanan; harga kosong = harga standar layanan. ValueError jika tidak valid."""
        pesanan = Pesanan(id_pesanan or self.id_berikutnya(), nama_pelanggan, layanan, jumlah,
                          LAYANAN_HARGA.get(layanan) if harga_satuan in (None, "") else harga_satuan,
                          status, tanggal_masuk)
        if any(p.id_pesanan == pesanan.id_pesanan for p in self._data):
            raise ValueError(f"ID {pesanan.id_pesanan} sudah dipakai.")
        self._data.append(pesanan)
        if self.storage is not None:
            self.storage.tambah_baris(pesanan)  # mode 'a'
        return pesanan

    def cari_nama(self, kata):
        """Mencari pesanan menurut sebagian nama pelanggan (linear search)."""
        return linear_search_nama(self._data, kata)

    def urutkan(self, daftar, kolom, menurun=False):
        """Mengurutkan `daftar` menurut `kolom` dengan merge sort."""
        if kolom not in KUNCI_URUT:
            raise ValueError(f"Kolom '{kolom}' tidak dikenal.")
        return merge_sort(daftar, key=KUNCI_URUT[kolom], menurun=menurun)

    def pendapatan(self, **kwargs):
        """Total pendapatan seluruh pesanan, atau yang cocok dengan filter (**kwargs)."""
        return hitung_total(*filter_pesanan(self._data, **kwargs))
