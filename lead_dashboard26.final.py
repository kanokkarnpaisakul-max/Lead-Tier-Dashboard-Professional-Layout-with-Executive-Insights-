import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

# -----------------------------
# 1. Mock data
# -----------------------------
np.random.seed(42)
num_rows = 100000
date_range = pd.date_range(start='2025-01-01', end='2025-09-25', freq='D')
dates = np.random.choice(date_range, size=num_rows)

data = {
    "Lead_ID": range(1, num_rows + 1),
    "อายุรถ(ปี)": np.random.randint(1, 11, size=num_rows),
    "อาชีพ": np.random.choice([
        "พนักงานบริษัทใหญ่", "ค้าขาย", "ฟรีแลนซ์",
        "พนักงานบริษัทเล็ก", "นักศึกษา", "พนักงานรัฐ", "ธุรกิจส่วนตัว"
    ], size=num_rows),
    "ภูมิภาค": np.random.choice([
        "กรุงเทพ", "ภาคเหนือ", "ภาคกลาง", "ภาคใต้",
        "ภาคตะวันออก", "ภาคตะวันออกเฉียงเหนือ"
    ], size=num_rows),
    "คะแนนเครดิต": np.random.randint(1, 6, size=num_rows),
    "วันที่สร้าง Lead": dates
}

df = pd.DataFrame(data)

# -----------------------------
# 2. Weighted Score + Tier + Engagement Strategy
# -----------------------------
job_weight = {
    "พนักงานบริษัทใหญ่": 1.0,
    "ค้าขาย": 0.8,
    "ฟรีแลนซ์": 0.7,
    "พนักงานบริษัทเล็ก": 0.6,
    "นักศึกษา": 0.5,
    "พนักงานรัฐ": 0.9,
    "ธุรกิจส่วนตัว": 0.85
}

df['Weighted Score'] = (
    df['คะแนนเครดิต'] * 0.7 +
    (11 - df['อายุรถ(ปี)']) * 0.2 +
    df['อาชีพ'].map(job_weight) * 2.0
)

def assign_weighted_tier(score):
    if score >= 7:
        return "Tier A"
    elif score >= 4:
        return "Tier B"
    else:
        return "Tier C"

df['Tier'] = df['Weighted Score'].apply(assign_weighted_tier)

strategy_map = {
    "Tier A": "Personalized Offer / High-touch",
    "Tier B": "Automation / Nurture Campaign",
    "Tier C": "Low-cost Automation"
}
df['Engagement_Strategy'] = df['Tier'].map(strategy_map)

tier_cost = {"Tier A":1200, "Tier B":800, "Tier C":400}
tier_revenue = {"Tier A":5000, "Tier B":2500, "Tier C":600}
df['Cost'] = df['Tier'].map(tier_cost)
df['Revenue'] = df['Tier'].map(tier_revenue)

# -----------------------------
# 3. Page config + Theme
# -----------------------------
st.set_page_config(page_title="Lead Tier Dashboard", layout="wide")
st.markdown("""
<style>
.stButton>button {background-color: #1f77b4; color: white; border-radius: 8px; margin:2px;}
.stDownloadButton>button {background-color: #2ca02c; color: white; border-radius: 8px; margin:2px;}
</style>
""", unsafe_allow_html=True)

st.title("Lead Tier Dashboard (Professional Layout with Executive Insights)")

# -----------------------------
# 4. Filters
# -----------------------------
job_options = df["อาชีพ"].unique().tolist()
selected_jobs = st.multiselect("เลือกอาชีพ", job_options, default=job_options)

region_options = df[df["อาชีพ"].isin(selected_jobs)]["ภูมิภาค"].unique().tolist()
selected_regions = st.multiselect("เลือกภูมิภาค", region_options, default=region_options)

age_options = df[
    (df["อาชีพ"].isin(selected_jobs)) & (df["ภูมิภาค"].isin(selected_regions))
]["อายุรถ(ปี)"].sort_values().unique().tolist()
selected_ages = st.multiselect("เลือกอายุรถ (ปี)", age_options, default=age_options)

filtered_df = df[
    (df["อาชีพ"].isin(selected_jobs)) &
    (df["ภูมิภาค"].isin(selected_regions)) &
    (df["อายุรถ(ปี)"].isin(selected_ages))
]

st.write(f"จำนวน Lead ที่ตรงกับเงื่อนไข: {len(filtered_df)}")

# -----------------------------
# 5. Executive Insights / Strategic Narrative
# -----------------------------
st.markdown("## Executive Insights / Strategic Narrative")
st.markdown(f"""
- **Total Leads:** {len(filtered_df):,}  
- **Tier A Leads:** {len(filtered_df[filtered_df['Tier']=='Tier A']):,} (conversion สูงสุด)  
- **ROI per Tier:** Tier A ให้ผลตอบแทนสูงสุดเมื่อเทียบ resource ที่ใช้  
- **Engagement Strategy:**  
    - Tier A → Personalized Offer / High-touch  
    - Tier B → Automation / Nurture Campaign  
    - Tier C → Low-cost Automation  
- **Actionable Insight:** ทีมขายและการตลาดควร prioritize Tier A เพื่อ maximize ROI  
- **Trend & Heatmap:** แสดงช่วงเวลาที่ lead สูงและภูมิภาคที่มีโอกาสสูง  
""")

# -----------------------------
# 6. KPI Cards
# -----------------------------
total_leads = len(filtered_df)
tier_a = len(filtered_df[filtered_df['Tier']=='Tier A'])
conversion_rate = tier_a / total_leads * 100 if total_leads > 0 else 0

st.subheader("Key Metrics")
col1, col2, col3 = st.columns(3)
col1.metric("Total Leads", f"{total_leads:,}")
col2.metric("Tier A Leads", f"{tier_a:,}")
col3.metric("Conversion % (Tier A)", f"{conversion_rate:.1f}%")

# -----------------------------
# 7. ROI Summary Table
# -----------------------------
roi_df = filtered_df.groupby('Tier').agg(
    Total_Leads=('Lead_ID','count'),
    Total_Cost=('Cost','sum'),
    Total_Revenue=('Revenue','sum')
).reset_index()
roi_df['ROI %'] = ((roi_df['Total_Revenue'] - roi_df['Total_Cost'])/roi_df['Total_Cost']*100).round(1)
roi_df['Engagement_Strategy'] = roi_df['Tier'].map(strategy_map)

# -----------------------------
# 8. Two-column layout for charts
# -----------------------------
col_left, col_right = st.columns(2)

with col_left:
    # ROI Weighted Tier (%)
    chart_roi_bar = alt.Chart(roi_df).mark_bar().encode(
        x=alt.X('ROI %:Q', title='ROI %'),
        y=alt.Y('Tier:N', sort=['Tier A','Tier B','Tier C']),
        color=alt.Color('Tier:N', scale=alt.Scale(range=['#1f77b4','#ffbb78','#2ca02c'])),
        tooltip=['Tier','ROI %','Total_Leads']
    ).properties(height=250, width='container', title="ROI Weighted Tier (%)")
    st.altair_chart(chart_roi_bar)

    # Pie chart
    tier_count = filtered_df.groupby("Tier").size().reset_index(name="จำนวน Lead")
    all_tiers = pd.DataFrame({'Tier':['Tier A','Tier B','Tier C']})
    tier_count = all_tiers.merge(tier_count, on='Tier', how='left').fillna(0)
    tier_count['percent'] = tier_count['จำนวน Lead']/tier_count['จำนวน Lead'].sum()*100 if len(filtered_df)>0 else 0

    chart_pie = alt.Chart(tier_count).mark_arc().encode(
        theta=alt.Theta('percent:Q'),
        color=alt.Color('Tier:N', scale=alt.Scale(range=['#1f77b4','#ffbb78','#2ca02c'])),
        tooltip=['Tier','percent','จำนวน Lead']
    ).properties(height=250, width='container', title="สัดส่วน Lead ตาม Tier (%)")
    st.altair_chart(chart_pie)

    # Grouped Bar
    grouped_count = filtered_df.groupby(["อาชีพ","Tier"]).size().reset_index(name="จำนวน Lead")
    all_combinations = pd.MultiIndex.from_product([filtered_df['อาชีพ'].unique(), ['Tier A','Tier B','Tier C']], names=['อาชีพ','Tier'])
    grouped_count = grouped_count.set_index(['อาชีพ','Tier']).reindex(all_combinations, fill_value=0).reset_index()

    chart_grouped = alt.Chart(grouped_count).mark_bar().encode(
        x='อาชีพ:N',
        y='จำนวน Lead:Q',
        color='Tier:N',
        column='Tier:N',
        tooltip=['อาชีพ','Tier','จำนวน Lead']
    ).properties(height=350, width=200, title="จำนวน Lead ตามอาชีพ (Grouped by Tier)")
    st.altair_chart(chart_grouped)

with col_right:
    st.subheader("ROI Weighted Tier + Dynamic Table")
    st.dataframe(roi_df, height=250)

    # Heatmap
    heatmap_data = filtered_df.groupby(["อาชีพ","ภูมิภาค"]).size().reset_index(name="จำนวน Lead")
    chart_heatmap = alt.Chart(heatmap_data).mark_rect().encode(
        x='อาชีพ',
        y='ภูมิภาค',
        color='จำนวน Lead:Q',
        tooltip=['อาชีพ','ภูมิภาค','จำนวน Lead']
    ).properties(height=250, width='container', title="Heatmap: อาชีพ × ภูมิภาค")
    st.altair_chart(chart_heatmap)

    # Trend
    trend_data = filtered_df.groupby(['วันที่สร้าง Lead','Tier']).size().reset_index(name='จำนวน Lead')
    chart_trend = alt.Chart(trend_data).mark_line(point=True).encode(
        x='วันที่สร้าง Lead:T',
        y='จำนวน Lead:Q',
        color='Tier:N',
        tooltip=['วันที่สร้าง Lead','Tier','จำนวน Lead']
    ).properties(height=250, width='container', title="Trend จำนวน Lead ตาม Tier")
    st.altair_chart(chart_trend)

# -----------------------------
# 9. Export CSV
# -----------------------------
csv = filtered_df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="ดาวน์โหลดข้อมูล filtered CSV",
    data=csv,
    file_name='filtered_leads.csv',
    mime='text/csv'
)
