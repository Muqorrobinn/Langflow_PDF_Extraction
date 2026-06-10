# Langflow_PDF_Extraction
Make a flow of AI automation use Langflow

create table public.paper_reviews (
  id uuid not null default gen_random_uuid (),
  created_at timestamp with time zone not null default timezone ('utc'::text, now()),
  metadata jsonb not null,
  problem_statement text not null,
  novelty text not null,
  methodology jsonb not null,
  key_metrics text not null,
  limitations text not null,
  relevance text not null,
  constraint paper_reviews_pkey primary key (id)
) TABLESPACE pg_default;

create index IF not exists idx_paper_metadata on public.paper_reviews using gin (metadata) TABLESPACE pg_default;

create index IF not exists idx_paper_methodology on public.paper_reviews using gin (methodology) TABLESPACE pg_default;


Mendefinisikan “faktual” vs “interpretatif”
# Faktual:
  ## metadata: judul, tahun, penulis, venue.
  ## methodology (bagian “Algoritma”, “Dataset”, dsb.) sepanjang itu tertulis eksplisit di paper.
  ## key_metrics: angka-angka performa, nama metrik.
# Interpretatif: problem_statement, novelty, limitations, relevance.

Atur rule pribadi
# Analisis kuantitatif (tabel komparasi PCA vs ICA vs K-Means, dsb.) hanya boleh pakai field faktual + baris dengan status_review = 'fully_verified'.
# Field interpretatif hanya “bahan awal” yang wajib Anda baca dan koreksi sebelum dijadikan argumentasi di tesis/paper.

Dokumentasi singkat proyek ini:
# Diagram singkat arsitektur (boleh ASCII dulu):
  Langflow (Read File → Gemini → SupabaseInsert) → Supabase → Streamlit.

Cara menjalankan:
# Jalankan flow di Langflow,
# Jalankan streamlit run dashboard_riset.py,
# Filter Fully Verified sebelum analisis.

Catatan metodologis:
# “Data faktual diekstrak otomatis, tetapi hanya baris status_review = 'fully_verified' yang digunakan dalam analisis penelitian.”

Ini adalah “fondasi manajemen versi”
Tujuan: sebelum mengubah apa pun, Anda punya “checkpoint” sehingga aman kalau nanti eksperimen gagal.
Langkah konkret:
# Export flow Langflow saat ini
  ## Di Langflow, export flow sebagai file .json (yang sudah Anda kirim ke saya). [High confidence – fitur standar Langflow]
  ## Simpan di repo Git (misal flows/literature_v1.json) dengan pesan commit jelas.

# Snapshot skema Supabase
  ## Di Supabase, cek struktur tabel paper_reviews (kolom, tipe data).
  ## Dokumentasikan di README atau file markdown singkat: kolom apa, tipe apa, contoh isi.

# Tag versi kode Streamlit
  ## Buat branch baru misalnya literature-v1 di Git, simpan versi yang sekarang berjalan.
  ## Mulai pengembangan perbaikan di branch literature-v2.
