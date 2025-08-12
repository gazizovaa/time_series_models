import os
import streamlit as st
import papermill as pm
from datetime import datetime
import time

# Sector məlumatları
SECTOR_FIELDS = {
    "Səhhiyyə": ["Həkimlərin sayı", "Xəstələrin sayı"],
    "Sənaye": ["İstehsal göstəriciləri", "İşçi sayı"],
    "Təhsil": ["Müəllimlərin sayı", "Tələbələrin sayı"],
    "Kənd Təsərrüfatı": ["Məhsul həcmi", "Fermerlərin sayı"],
}

# Səhifə konfiqurasiyası
st.set_page_config(
    page_title="AI Hesabat Generatoru",
    page_icon="🤖 ",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS stili
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #1f77b4;
        font-size: 2.5rem;
        margin-bottom: 2rem;
        font-weight: bold;
    }
    
    .sidebar-header {
        background: linear-gradient(90deg, #1f77b4, #ff7f0e);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 1.5rem;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    
    .info-box {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #1f77b4;
        margin: 1rem 0;
    }
    
    .success-box {
        background-color: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #28a745;
        margin: 1rem 0;
    }
    
    .error-box {
        background-color: #f8d7da;
        color: #721c24;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #dc3545;
        margin: 1rem 0;
    }
    
    .stButton > button {
        background: linear-gradient(90deg, #1f77b4, #ff7f0e);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.5rem 1rem;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
</style>
""", unsafe_allow_html=True)

# Başlıq
st.markdown('<h1 class="main-header">🤖 AI Hesabat Generatoru</h1>', unsafe_allow_html=True)

# Əsas məlumat bölməsi
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("""
    <div class="info-box">
        <h3>🔍 Xoş gəlmisiniz!</h3>
        <p>Bu sistem sizə müxtəlif sektorlar üzrə hesabatlar yaratmağa kömək edir. 
        Sol tərəfdə parametrləri seçərək özünüzə uyğun hesabat yarada bilərsiniz.</p>        
        <h4>📋 Mövcud sektorlar:</h4>
        <ul>
            <li><strong>Səhhiyyə</strong> - Tibb sahəsi üzrə analiz</li>
            <li><strong>Sənaye</strong> - İstehsal göstəriciləri</li>
            <li><strong>Təhsil</strong> - Təhsil statistikaları</li>
            <li><strong>Kənd Təsərrüfatı</strong> - Kənd təsərrüfatı məlumatları</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="info-box">
        <h4>📈 Proqnoz xüsusiyyətləri:</h4>
        <ul>
            <li>2020-2035 il aralığı</li>
            <li>Detallı analiz</li>
            <li>PDF formatında nəticə</li>
            <li>Avtomatik hesablama</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# Sidebar parametrləri
st.sidebar.markdown('<h2 class="sidebar-header">⚙️ Parametrlər</h2>', unsafe_allow_html=True)

# Şəxsi məlumatlar
st.sidebar.subheader("👤 Şəxsi məlumatlar")
name = st.sidebar.text_input("Ad", placeholder="Adınızı daxil edin...")
surname = st.sidebar.text_input("Soyad", placeholder="Soyadınızı daxil edin...")

# Sektor seçimi
st.sidebar.subheader("🏭 Sektor seçimi")
sector = st.sidebar.selectbox(
    "Seçilən sektor",
    options=list(SECTOR_FIELDS.keys()),
    help="Hesabat yaratmaq istədiyiniz sektoru seçin"
)

# Sahə seçimi
field = st.sidebar.selectbox(
    "Seçilən sahə",
    options=SECTOR_FIELDS.get(sector, []),
    help=f"{sector} sektoru üçün müvafiq sahəni seçin"
)

# Tarix aralığı
st.sidebar.subheader("📅 Tarix aralığı")
years = st.sidebar.slider(
    "Proqnoz olunması üçün tarix aralığı",
    min_value=2025,
    max_value=2035,
    value=(2026, 2028),
    step=1,
    help="Proqnoz etmək istədiyiniz il aralığını seçin"
)
start_year, end_year = years

# Preview məlumatları
if name and surname:
    st.sidebar.markdown("---")
    st.sidebar.subheader("👁️ Önizləmə")
    st.sidebar.info(f"""
    **Ad-Soyad:** {name} {surname}
    **Sektor:** {sector}
    **Sahə:** {field}
    **Tarix aralığı:** {start_year} - {end_year}
    """)

# Validasiya və status
def validate_inputs():
    """İnput məlumatlarını yoxlayır"""
    errors = []
    if not name.strip():
        errors.append("Ad sahəsi boş ola bilməz")
    if not surname.strip():
        errors.append("Soyad sahəsi boş ola bilməz")
    if len(name.strip()) < 2:
        errors.append("Ad ən azı 2 simvoldan ibarət olmalıdır")
    if len(surname.strip()) < 2:
        errors.append("Soyad ən azı 2 simvoldan ibarət olmalıdır")
    return errors

# PDF yaratma düyməsi
st.sidebar.markdown("---")
pdf_button = st.sidebar.button("🎯 PDF Yarat", type="primary", use_container_width=True)

# Əsas proses
if pdf_button:
    validation_errors = validate_inputs()
    
    if validation_errors:
        # Xətaları göstər
        error_text = "❌ **Xətalar:**\n" + "\n".join([f"• {error}" for error in validation_errors])
        st.sidebar.markdown(f'<div class="error-box">{error_text}</div>', unsafe_allow_html=True)
    else:
        # Progress bar
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            # Parametrləri hazırla
            params = {
                'name': name.strip(),
                'surname': surname.strip(),
                'sector': sector,
                'field': field,
                'start_year': start_year,
                'end_year': end_year,
                'generated_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            # Addım 1: Notebook icra et
            status_text.text("📝 Notebook icra edilir...")
            progress_bar.progress(25)
            
            executed_nb = 'AiLab_executed.ipynb'
            pm.execute_notebook(
                'AiLab.ipynb',
                executed_nb,
                parameters=params
            )
            
            # Addım 2: PDF yaradılması
            status_text.text("📄 PDF yaradılır...")
            progress_bar.progress(75)
            time.sleep(1)  # Vizual effekt üçün
            
            merged_pdf = 'Birləşdirilmiş_Hesabat.pdf'
            
            # Addım 3: Faylı yoxla
            status_text.text("✅ Fayl yoxlanılır...")
            progress_bar.progress(100)
            
            if not os.path.isfile(merged_pdf):
                st.error("🚫 Notebook uğurla icra edildi, lakin PDF fayl tapılmadı.")
                st.markdown("""
                <div class="error-box">
                    <strong>Mümkün səbəblər:</strong>
                    <ul>
                        <li>Notebook-da PDF yaratma prosesində xəta baş verdi</li>
                        <li>Fayl adı düzgün təyin edilmədi</li>
                        <li>Yazma icazəsi problemi</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
            else:
                # Uğurlu nəticə
                status_text.text("🎉 Tamamlandı!")
                
                with open(merged_pdf, 'rb') as f:
                    pdf_bytes = f.read()
                
                st.balloons()  # Vizual effekt
                
                st.markdown("""
                <div class="success-box">
                    <h3>🎉 PDF uğurla yaradıldı!</h3>
                    <p>Hesabatınız hazırdır və yüklənməyə əmamədir.</p>
                </div>
                """, unsafe_allow_html=True)
                
                # PDF download
                file_name = f"Hesabat_{name}_{surname}_{sector}_{start_year}-{end_year}.pdf"
                st.download_button(
                    label="📥 PDF-i yüklə",
                    data=pdf_bytes,
                    file_name=file_name,
                    mime="application/pdf",
                    type="primary",
                    use_container_width=True
                )
                
                # Statistika
                st.markdown(f"""
                **📊 Hesabat məlumatları:**
                - **Fayl ölçüsü:** {len(pdf_bytes) / 1024:.1f} KB
                - **Yaradılma tarixi:** {datetime.now().strftime("%d.%m.%Y %H:%M")}
                - **Format:** PDF
                """)
                
        except Exception as e:
            progress_bar.empty()
            status_text.empty()
            st.error(f"🚫 Xəta baş verdi: {str(e)}")
            st.markdown("""
            <div class="error-box">
                <strong>Kömək üçün:</strong>
                <ul>
                    <li>Bütün sahələrin düzgün doldurulduğundan əmin olun</li>
                    <li>Internet bağlantınızı yoxlayın</li>
                    <li>Bir az sonra yenidən cəhd edin</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    <p>🤖 AI Hesabat Generatoru v2.0 | Powered by AI Lab</p>
    <p><small>Son yenilənmə: 2025</small></p>
</div>
""", unsafe_allow_html=True)