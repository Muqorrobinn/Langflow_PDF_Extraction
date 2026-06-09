import streamlit as st
from supabase import create_client, Client
import pandas as pd

# ==========================================
# KONFIGURASI HALAMAN (WAJIB PERTAMA)
# ==========================================
st.set_page_config(page_title="AI Automation - Literature Review", layout="wide")

# ==========================================
# KONFIGURASI SUPABASE
# ==========================================
# Ganti dengan URL dan API Key (anon/public) Supabase Anda
SUPABASE_URL = "https://absaqtfvtbhhdkfnlpmx.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFic2FxdGZ2dGJoaGRrZm5scG14Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODA5MTY4ODQsImV4cCI6MjA5NjQ5Mjg4NH0.Pm8HCQ0vKAN-KK3Vw7J7fZiHnHmkNjHePrI_dnOEVjE" # Masukkan API Key Anda yang utuh di sini

@st.cache_resource
def init_connection() -> Client:
    return create_client(SUPABASE_URL, SUPABASE_KEY)

supabase = init_connection()

# ==========================================
# FUNGSI PENARIKAN DATA
# ==========================================
@st.cache_data(ttl=60) # Cache data selama 60 detik untuk efisiensi API
def fetch_papers():
    try:
        response = supabase.table("paper_reviews").select("*").order("created_at", desc=True).execute()
        return response.data
    except Exception as e:
        st.error(f"Gagal menarik data dari Supabase: {e}")
        return []

# ==========================================
# ANTARMUKA PENGGUNA (UI)
# ==========================================
st.title("📚 Literature Review Dashboard: PCA/ICA vs K-Means")
st.markdown("Dashboard ini menampilkan hasil ekstraksi otomatis dari pipeline Langflow Anda.")

data = fetch_papers()

if not data:
    st.warning("Belum ada data paper di database. Silakan jalankan Langflow terlebih dahulu.")
else:
    # 1. Tabel Komparasi Metodologi Cepat
    st.subheader("📊 Tabel Komparasi Metodologi")
    
    table_data = []
    for row in data:
        meta = row.get("metadata", {})
        method = row.get("methodology", {})
        
        table_data.append({
            "Tahun": meta.get("Tahun", "-"),
            "Judul": meta.get("Judul", "Tanpa Judul"),
            "Algoritma Ekstraksi": method.get("Algoritma", "-"),
            "Dataset": method.get("Dataset", "-"),
            "Key Metrics": row.get("key_metrics", "-")[:100] + "..." # Truncate panjang
        })
        
    df = pd.DataFrame(table_data)
    st.dataframe(df, use_container_width=True)

    st.divider()

    # 2. Tampilan Detail Analisis (Expanders)
    st.subheader("🔍 Detail Ekstraksi Kritis")
    
    for row in data:
        meta = row.get("metadata", {})
        judul = meta.get("Judul", "Dokumen Tanpa Judul")
        penulis = meta.get("Penulis", "Anonim")
        tahun = meta.get("Tahun", "-")
        
        with st.expander(f"{tahun} | {judul} ({penulis})"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**🎯 Problem Statement:**")
                st.info(row.get("problem_statement", "-"))
                
                st.markdown("**💡 Novelty / Kontribusi:**")
                st.success(row.get("novelty", "-"))
                
                st.markdown("**⚙️ Metodologi Detail:**")
                st.json(row.get("methodology", {}))

            with col2:
                st.markdown("**📈 Key Metrics:**")
                st.warning(row.get("key_metrics", "-"))
                
                st.markdown("**⚠️ Keterbatasan (Limitations):**")
                st.error(row.get("limitations", "-"))
                
                st.markdown("**🔗 Relevansi dengan Tesis Robin:**")
                st.markdown(f"*{row.get('relevance', '-')}*")