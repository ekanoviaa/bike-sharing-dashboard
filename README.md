# bike-sharing-dashboard
## 🗂️ Struktur Direktori

```
bike-sharing-dashboard/
├── dashboard/
│   ├── dashboard.py
│   └── main_data.csv 
├── data/
│   ├── day.csv      
│   └── hour.csv     
├── notebook.ipynb   
├── README.md          
├── requirements.txt      
└── url.txt              
```

---

## 🚀 Panduan Menjalankan Aplikasi

### 1. Clone Repositori

```
git clone https://github.com/ekanoviaa/bike-sharing-dashboard.git
cd bike-sharing-dashboard
```

### 2. Instalasi Library

```
pip install -r requirements.txt
```

### 3. Jalankan Dashboard

```
streamlit run dashboard.py
```
Aplikasi akan otomatis terbuka di browser pada `http://localhost:8501`

---

## 📦 Requirements

| Library | Versi Minimum | Kegunaan |
|---|---|---|
| `streamlit` | 1.32.0 | Framework dashboard interaktif |
| `pandas` | 2.0.0 | Manipulasi dan analisis data |
| `numpy` | 1.26.0 | Komputasi numerik |
| `matplotlib` | 3.8.0 | Visualisasi data |
| `seaborn` | 0.13.0 | Visualisasi data statistik |

Install semua sekaligus:

```bash
pip install streamlit pandas numpy matplotlib seaborn
```

Dashboard dapat diakses secara publik melalui Streamlit Cloud:

🔗 **[https://bike-sharing-dashboard-qhtw9mntgzsw9a9bxkz2z6.streamlit.app/]**
