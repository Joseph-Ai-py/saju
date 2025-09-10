import streamlit as st
from datetime import datetime
from parser import chain
import plotly.graph_objects as go

st.set_page_config(page_title="사주 명리 분석 리포트", layout="wide")
st.title("사주 명리 분석 리포트")

with st.form("saju_input_form"):
    name = st.text_input("이름", "이름을 입력해주세요")
    country = st.text_input("국가", "대한민국")
    city = st.text_input("도시", "태어난 지역을 입력해주세요")
    birth_date = st.text_input("출생일 (YYYY-MM-DD)", "출생일을 입력해주세요")
    birth_time = st.text_input("출생 시간 (HH:MM)", "출생 시간을 입력해주세요. 없으면 입력 안해도 됩니다.")
    gender = st.selectbox("성별", ["남성", "여성"])
    calendar_type = st.selectbox("달력 종류", ["양력", "음력"])
    analysis_date = st.text_input("분석 기준일 (YYYY-MM-DD)", str(datetime.now().date()))
    submitted = st.form_submit_button("분석하기")

if submitted:
    with st.spinner("AI 분석 중입니다..."):
        input_data = {
            "name": name,
            "country": country,
            "city": city,
            "yyyymmdd_hhmm": f"{birth_date} {birth_time}",
            "sex": gender,
            "calendar_type": calendar_type,
            "analysis_date": analysis_date
        }
        answer = chain.invoke(input_data)

        user_info = answer.get('input', {})
        won_guk = answer.get('won_guk', {})
        five_elements = answer.get('five_elements', {})
        yin_percent = five_elements.get('yin_percent', 0)
        yang_percent = five_elements.get('yang_percent', 0)
        balance_index = five_elements.get('balance_index', 0)
        content = answer.get('content', '')
        markdown_report = answer.get('markdown_report', '')

        # 1️⃣ 기본 정보
        with st.expander("1️⃣ 기본 정보", expanded=True):
            st.write(f"**이름:** {user_info.get('name', '')}")
            st.write(f"**성별:** {user_info.get('gender', '')}")
            st.write(f"**출생일시:** {user_info.get('calendar_type', '')} {user_info.get('birth_date', '')} {user_info.get('birth_time', '')} ({user_info.get('birth_place', '')})")
            st.write(f"**분석 기준일:** {user_info.get('analysis_date', '')}")

        # 2️⃣ 사주 원국 (표)
        with st.expander("2️⃣ 사주 원국", expanded=True):
            st.markdown(
                f"""
                <table>
                    <tr>
                        <th>연주</th><th>월주</th><th>일주</th><th>시주</th>
                    </tr>
                    <tr>
                        <td>{won_guk.get('year', {}).get('stem', '')} {won_guk.get('year', {}).get('branch', '')}</td>
                        <td>{won_guk.get('month', {}).get('stem', '')} {won_guk.get('month', {}).get('branch', '')}</td>
                        <td>{won_guk.get('day', {}).get('stem', '')} {won_guk.get('day', {}).get('branch', '')}</td>
                        <td>{won_guk.get('hour', {}).get('stem', '')} {won_guk.get('hour', {}).get('branch', '')}</td>
                    </tr>
                </table>
                """,
                unsafe_allow_html=True
            )


        # 3️⃣ 오행(五行) 정량·정성 분석 (도넛차트)
        with st.expander("3️⃣ 오행(五行) 정량·정성 분석", expanded=True):
            labels = ["목", "화", "토", "금", "수"]
            values = [
                five_elements.get('wood', {}).get('percent', 0),
                five_elements.get('fire', {}).get('percent', 0),
                five_elements.get('earth', {}).get('percent', 0),
                five_elements.get('metal', {}).get('percent', 0),
                five_elements.get('water', {}).get('percent', 0)
            ]
            colors = ["#2ecc40", "#ff4136", "#b7950b", "#7f8c8d", "#3498db"]
            fig = go.Figure(
                data=[go.Pie(
                    labels=labels,
                    values=values,
                    hole=0.5,
                    marker=dict(colors=colors),
                    textinfo='label+percent',
                )]
            )
            fig.update_layout(showlegend=True)
            st.plotly_chart(fig, use_container_width=True)

        # 4️⃣ 일간(일주) 중심 십신(十神) 분석 (도넛차트)
        with st.expander("4️⃣ 일간(일주) 중심 십신(十神) 분석", expanded=True):
            ten_gods = answer.get('ten_gods', {})
            ten_god_labels = []
            ten_god_values = []
            ten_god_colors = ["#e67e22", "#9b59b6", "#16a085", "#34495e", "#f1c40f", "#c0392b", "#2980b9", "#27ae60", "#d35400", "#7f8c8d"]
            for k, v in ten_gods.items():
                ten_god_labels.append(k)
                ten_god_values.append(v.get('percent', 0))
            if ten_god_labels:
                fig3 = go.Figure(
                    data=[go.Pie(
                        labels=ten_god_labels,
                        values=ten_god_values,
                        hole=0.5,
                        marker=dict(colors=ten_god_colors[:len(ten_god_labels)]),
                        textinfo='label+percent',
                    )]
                )
                fig3.update_layout(showlegend=True)
                st.plotly_chart(fig3, use_container_width=True)

        # 4️⃣ 음/양 비율 (도넛 그래프)
        with st.expander("4️⃣ 음/양 비율", expanded=True):
            fig2 = go.Figure(
                data=[go.Pie(
                    labels=['음', '양'],
                    values=[yin_percent, yang_percent],
                    hole=0.5
                )]
            )
            st.plotly_chart(fig2, use_container_width=True)

        # 5️⃣ 분석 내용
        with st.expander("5️⃣ 분석 내용", expanded=True):
            st.markdown(content)