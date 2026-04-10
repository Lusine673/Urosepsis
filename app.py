import streamlit as st
import math

# ============================================================
# НАСТРОЙКА СТРАНИЦЫ
# ============================================================
st.set_page_config(
    page_title="Прогнозирование гестационного пиелонефрита",
    layout="centered"
)

# ============================================================
# КАСТОМНЫЕ СТИЛИ
# ============================================================
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 1rem 0;
        border-bottom: 3px solid #4A90D9;
        margin-bottom: 2rem;
    }
    .main-header h1 {
        color: #2C3E50;
        font-size: 1.8rem;
    }
    .warning-box {
        background-color: #FFF3CD;
        border: 1px solid #FFECB5;
        border-left: 4px solid #FFC107;
        border-radius: 8px;
        padding: 1rem;
        margin-bottom: 1.5rem;
        font-size: 0.95rem;
        color: #664D03;
    }
    .absolute-risk-box {
        background-color: #F8D7DA;
        border: 1px solid #F5C6CB;
        border-left: 4px solid #DC3545;
        border-radius: 8px;
        padding: 1rem;
        margin-bottom: 1.5rem;
        font-size: 0.95rem;
        color: #721C24;
    }
    .result-box {
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        margin: 1.5rem 0;
        font-size: 1.1rem;
    }
    .result-high {
        background: linear-gradient(135deg, #FDEDEC, #F5B7B1);
        border: 2px solid #E74C3C;
        color: #922B21;
    }
    .result-low {
        background: linear-gradient(135deg, #EAFAF1, #A9DFBF);
        border: 2px solid #27AE60;
        color: #1E8449;
    }
    .result-absolute {
        background: linear-gradient(135deg, #F5B7B1, #E74C3C);
        border: 2px solid #922B21;
        color: #641E16;
    }
    .recommendations-card {
        background-color: #F8F9FA;
        padding: 1.2rem;
        border-radius: 10px;
        border-left: 4px solid #4A90D9;
        margin: 1rem 0;
        font-size: 0.9rem;
    }
    .recommendations-card-high {
        border-left-color: #E74C3C;
    }
    .recommendations-card-low {
        border-left-color: #27AE60;
    }
    .info-box {
        background-color: #E8F4FD;
        border: 1px solid #B8DAFF;
        border-radius: 8px;
        padding: 0.8rem;
        margin: 1rem 0;
        font-size: 0.85rem;
        color: #004085;
    }
    .model-info {
        background-color: #F8F9FA;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
        font-size: 0.85rem;
    }
    .model-info table {
        width: 100%;
        border-collapse: collapse;
    }
    .model-info th, .model-info td {
        padding: 8px;
        text-align: left;
        border-bottom: 1px solid #dee2e6;
    }
    .model-info th {
        background-color: #4A90D9;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# ЗАГОЛОВОК
# ============================================================
st.markdown("""
<div class="main-header">
    <h1>Прогнозирование гестационного пиелонефрита</h1>
</div>
""", unsafe_allow_html=True)

# ============================================================
# БЛОК АБСОЛЮТНЫХ ФАКТОРОВ РИСКА
# ============================================================
st.markdown("### Шаг 1: Проверка абсолютных факторов риска")

st.markdown("""
<div class="warning-box">
    <strong>Внимание!</strong> При наличии хотя бы одного из указанных факторов 
    пациентка автоматически относится к группе <strong>ВЫСОКОГО РИСКА</strong> 
    развития пиелонефрита. Дальнейший расчёт не требуется.
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    chronic_pyelonephritis = st.radio(
        "Хронический пиелонефрит в анамнезе",
        options=["Нет", "Да"],
        horizontal=True,
        help="Наличие хронического пиелонефрита до беременности"
    )

with col2:
    mkb = st.radio(
        "Мочекаменная болезнь (МКБ)",
        options=["Нет", "Да"],
        horizontal=True,
        help="Наличие мочекаменной болезни"
    )

with col3:
    anomaly = st.radio(
        "Аномалии мочеполовой системы",
        options=["Нет", "Да"],
        horizontal=True,
        help="Врождённые аномалии развития мочеполовой системы"
    )

# Проверка абсолютных факторов
has_absolute_risk = (chronic_pyelonephritis == "Да" or 
                     mkb == "Да" or 
                     anomaly == "Да")

if has_absolute_risk:
    st.markdown("""
    <div class="result-box result-absolute">
        <h2 style="margin:0 0 0.5rem 0;"ВЫСОКИЙ РИСК</h2>
        <p style="margin:0;">Выявлен абсолютный фактор риска развития пиелонефрита.<br>
        Дальнейший расчёт не требуется.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("#### Рекомендации")
    st.markdown("""
    <div class="recommendations-card recommendations-card-high">
        <ul>
            <li>Консультация уролога при постановке на учёт</li>
            <li>Бактериологический посев мочи ежемесячно</li>
            <li>УЗИ почек в каждом триместре</li>
            <li>Общий анализ мочи перед каждым визитом к акушеру-гинекологу</li>
            <li>При появлении симптомов (дизурия, боли в пояснице, лихорадка) — экстренная госпитализация</li>
            <li>Профилактическая санация мочевых путей по показаниям</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

else:
    # ============================================================
    # БЛОК РАСЧЁТА (если нет абсолютных факторов)
    # ============================================================
    st.markdown("---")
    st.markdown("### Шаг 2: Расчёт индивидуального риска")
    
    st.markdown("""
    <div class="info-box">
        Абсолютные факторы риска отсутствуют. Заполните данные ниже для расчёта 
        индивидуальной вероятности развития пиелонефрита.
    </div>
    """, unsafe_allow_html=True)
    
    col4, col5 = st.columns(2)
    
    with col4:
        age_under_25 = st.radio(
            "Возраст младше 25 лет",
            options=["Нет", "Да"],
            horizontal=True,
            help="Возраст пациентки на момент постановки на учёт"
        )
        
        extragenital = st.radio(
            "Экстрагенитальные заболевания",
            options=["Нет", "Да"],
            horizontal=True,
            help="Наличие соматических заболеваний (сердечно-сосудистые, эндокринные, заболевания ЖКТ и др.)"
        )
    
    with col5:
        multipara = st.radio(
            "Повторнородящая (роды в анамнезе)",
            options=["Нет", "Да"],
            horizontal=True,
            help="Наличие родов в анамнезе (не путать с повторной беременностью)"
        )
    
    st.markdown("---")
    
    # ============================================================
    # КНОПКА РАСЧЁТА
    # ============================================================
    if st.button("Рассчитать риск", type="primary", use_container_width=True):
        
        # Преобразование в числовые значения
        x_age = 1 if age_under_25 == "Да" else 0
        x_extragenital = 1 if extragenital == "Да" else 0
        x_multipara = 1 if multipara == "Да" else 0
        
        # Коэффициенты модели
        intercept = -0.064
        coef_age = 1.191
        coef_extragenital = 1.410
        coef_multipara = -1.121
        
        # Расчёт z
        z = (intercept + 
             coef_age * x_age + 
             coef_extragenital * x_extragenital + 
             coef_multipara * x_multipara)
        
        # Расчёт вероятности (логистическая функция)
        probability = (1 / (1 + math.exp(-z))) * 100
        
        # Пороговое значение
        threshold = 75.5
        
        # Определение уровня риска
        if probability >= threshold:
            risk_label = "ВЫСОКИЙ РИСК"
            css_class = "result-high"
            risk_description = "Рекомендовано усиленное наблюдение"
        else:
            risk_label = "НИЗКИЙ РИСК"
            css_class = "result-low"
            risk_description = "Стандартное наблюдение"
        
        # ============================================================
        # РЕЗУЛЬТАТ
        # ============================================================
        st.markdown(f"""
        <div class="result-box {css_class}">
            <h2 style="margin:0 0 0.5rem 0;">{risk_label}</h2>
            <p style="margin:0;">
                Вероятность развития пиелонефрита: <b>{probability:.1f}%</b><br>
                Пороговое значение: {threshold}%<br>
                <small>{risk_description}</small>
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # --- Детализация факторов ---
        st.markdown("#### Вклад факторов риска")
        
        factors_data = []
        if x_age == 1:
            factors_data.append(("Возраст < 25 лет", "✅ Да", "OR = 3,29", "↑ Повышает риск"))
        else:
            factors_data.append(("Возраст < 25 лет", "❌ Нет", "—", "Нейтрально"))
        
        if x_extragenital == 1:
            factors_data.append(("Экстрагенитальные заболевания", "✅ Да", "OR = 4,10", "↑ Повышает риск"))
        else:
            factors_data.append(("Экстрагенитальные заболевания", "❌ Нет", "—", "Нейтрально"))
        
        if x_multipara == 1:
            factors_data.append(("Повторнородящая", "✅ Да", "OR = 0,33", "↓ Снижает риск"))
        else:
            factors_data.append(("Повторнородящая", "❌ Нет", "—", "Нейтрально"))
        
        # Таблица факторов
        table_html = """
        <div class="model-info">
        <table>
            <tr><th>Фактор</th><th>Значение</th><th>Отношение шансов</th><th>Влияние</th></tr>
        """
        for factor in factors_data:
            table_html += f"<tr><td>{factor[0]}</td><td>{factor[1]}</td><td>{factor[2]}</td><td>{factor[3]}</td></tr>"
        table_html += "</table></div>"
        
        st.markdown(table_html, unsafe_allow_html=True)
        
        # --- Рекомендации ---
        st.markdown("#### Рекомендации")
        
        if probability >= threshold:
            st.markdown("""
            <div class="recommendations-card recommendations-card-high">
                <ul>
                    <li>Консультация уролога</li>
                    <li>Бактериологический посев мочи ежемесячно</li>
                    <li>УЗИ почек в каждом триместре</li>
                    <li>Общий анализ мочи перед каждым визитом</li>
                    <li>Контроль питьевого режима (не менее 2 л/сут)</li>
                    <li>Своевременное лечение бессимптомной бактериурии</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="recommendations-card recommendations-card-low">
                <ul>
                    <li>Стандартное наблюдение согласно протоколу ведения беременности</li>
                    <li>Общий анализ мочи перед каждым визитом к врачу</li>
                    <li>Соблюдение питьевого режима</li>
                    <li>При появлении симптомов (дизурия, боли в пояснице) — обращение к врачу</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

# ============================================================
# ИНФОРМАЦИЯ О МОДЕЛИ
# ============================================================
st.markdown("---")

with st.expander("Информация о модели"):
    st.markdown("""
    ### Характеристики прогностической модели
    
    | Параметр | Значение |
    |----------|----------|
    | **AUC** | 0,750 (95% ДИ: 0,679–0,821) |
    | **Чувствительность** | 69,7% |
    | **Специфичность** | 70,0% |
    | **Пороговое значение** | 75,5% |
    | **Размер выборки** | 180 беременных женщин |
    
    ### Факторы риска в модели
    
    | Фактор | Отношение шансов (AOR) | 95% ДИ | p |
    |--------|:----------------------:|:------:|:-:|
    | Возраст < 25 лет | 3,29 | 1,37–7,93 | 0,008 |
    | Экстрагенитальные заболевания | 4,10 | 1,96–8,54 | <0,001 |
    | Повторнородящая | 0,33 (защитный) | 0,16–0,67 | 0,002 |
    
    ### Абсолютные факторы риска
    
    При наличии следующих факторов пациентка автоматически относится к группе высокого риска:
    - Хронический пиелонефрит в анамнезе
    - Мочекаменная болезнь
    - Аномалии мочеполовой системы
    
    *В исследуемой выборке данные факторы отсутствовали у 100% здоровых беременных (p < 0,001).*
    
    ### Формула расчёта
    
    ```
    P = 1 / (1 + e^(-z)) × 100%
    
    z = -0,064 + 1,191 × X₁ + 1,410 × X₂ - 1,121 × X₃
    ```
    
    Где:
    - X₁ — Возраст < 25 лет (0 = нет, 1 = да)
    - X₂ — Экстрагенитальные заболевания (0 = нет, 1 = да)
    - X₃ — Повторнородящая (0 = нет, 1 = да)
    """)

# ============================================================
# ПОДВАЛ С КОПИРАЙТОМ
# ============================================================
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #7F8C8D; font-size: 0.85rem; padding: 1.5rem 0 0.5rem 0;">
    <p style="margin: 0.5rem 0;">© 2025 Апресян С.В., Тамазова Л.Б.</p>
    <p style="margin: 0.5rem 0; font-size: 0.8rem;">Все права защищены.</p>
    <p style="margin: 0.5rem 0; font-size: 0.75rem; color: #95A5A6;">
        Калькулятор предназначен для научных и образовательных целей.<br>
        Не заменяет консультацию специалиста.
    </p>
</div>
""", unsafe_allow_html=True)
