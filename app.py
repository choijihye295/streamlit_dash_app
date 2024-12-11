import streamlit as st
import pandas as pd
import datetime
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# 페이지 설정
st.set_page_config(
    page_title="익산 토마토셋 대시보드",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS로 모바일 최적화 및 여백 조정
st.markdown("""
    <style>
        @media (max-width: 768px) {
            .main > div {
                padding-top: 0.5rem;
                padding-bottom: 0.5rem;
            }
            .block-container {
                padding: 0.5rem 1rem;
            }
            .metric-container {
                padding: 0.75rem;
                margin-bottom: 0.5rem;
            }
            .metric-label {
                font-size: 0.9rem;
            }
            .metric-value {
                font-size: 1.2rem;
            }
            .time-display {
                font-size: 0.8rem;
                padding: 0.3rem 0.6rem;
                top: 0.3rem;
                right: 0.5rem;
            }
            .stMarkdown {
                overflow-x: hidden;
            }
        }
        
        .main > div {
            padding-top: 1rem;
            padding-bottom: 1rem;
        }
        .block-container {
            padding: 1rem 2rem;
            max-width: 100%;
        }
        .metric-container {
            background-color: #f0f2f6;
            padding: 1rem;
            border-radius: 0.5rem;
            text-align: center;
            height: 100%;
            margin-bottom: 0.5rem;
        }
        .metric-label {
            color: #666;
            margin-bottom: 0.5rem;
            font-size: 1rem;
        }
        .metric-value {
            color: #111;
            margin: 0;
            font-size: 1.5rem;
            font-weight: bold;
        }
        .time-display {
            position: fixed;
            top: 0.5rem;
            right: 1rem;
            background-color: white;
            padding: 0.5rem 1rem;
            border-radius: 0.5rem;
            font-size: 0.9rem;
            color: #666;
            z-index: 1000;
        }
        .custom-title {
            margin-bottom: 1rem;
        }
    </style>
""", unsafe_allow_html=True)

# 기존 데이터 함수들은 동일하게 유지...

def create_metric_card(label, value):
    return f"""
        <div class="metric-container">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
        </div>
    """

def create_combined_graph(historical_data, prediction_data):
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # 기존 트레이스 추가 코드는 동일...

    # 모바일에 맞는 차트 크기 설정 (9:16 비율)
    chart_width = 360  # 모바일 기준 너비
    chart_height = int(chart_width * 16/9)  # 9:16 비율

    # 레이아웃 업데이트
    fig.update_layout(
        margin=dict(l=40, r=40, t=30, b=30),
        height=chart_height,
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(size=10),  # 폰트 크기 감소
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(size=8)  # 범례 폰트 크기 감소
        ),
        xaxis=dict(
            showgrid=True,
            gridcolor='lightgray',
            showline=True,
            linewidth=1,
            linecolor='lightgray',
            tickfont=dict(size=8)  # x축 레이블 크기 감소
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='lightgray',
            showline=True,
            linewidth=1,
            linecolor='lightgray',
            title_text="온도 (°C)",
            tickfont=dict(size=8),  # y축 레이블 크기 감소
            title_font=dict(size=10)  # y축 제목 크기 감소
        ),
        yaxis2=dict(
            showgrid=False,
            showline=True,
            linewidth=1,
            linecolor='lightgray',
            title_text="습도 (%)",
            tickfont=dict(size=8),
            title_font=dict(size=10)
        )
    )

    return fig

def main():
    # 현재 시간 표시
    target_time = "2018-05-10 10:00"
    st.markdown(
        f'<div class="time-display">조회 시간: {target_time}</div>',
        unsafe_allow_html=True
    )

    # 센서 데이터 가져오기
    sensor_data = get_sensor_data(target_time)

    # 1. 내부 환경 데이터 - 모바일에서는 한 열로 표시
    st.subheader('내부 환경', anchor=False)
    col1 = st.columns(1)[0]
    
    with col1:
        st.markdown(
            create_metric_card("내부 온도", f"{sensor_data['internal_temp']} °C"),
            unsafe_allow_html=True
        )
        st.markdown(
            create_metric_card("내부 습도", f"{sensor_data['internal_humidity']} %"),
            unsafe_allow_html=True
        )

    # 2. 외부 환경 데이터 - 모바일에서는 2열로 표시
    st.subheader('외부 환경', anchor=False)
    col1, col2 = st.columns(2)
    
    metrics = [
        ("외부 온도", f"{sensor_data['external_temp']} °C"),
        ("풍향/풍속", f"{sensor_data['wind_direction']} {sensor_data['wind_speed']}m/s"),
        ("이슬점", f"{sensor_data['dew_point']} °C"),
        ("누적일사량", f"{sensor_data['solar_radiation']} J/cm²")
    ]
    
    # 2x2 그리드로 표시
    for i, (label, value) in enumerate(metrics):
        with col1 if i % 2 == 0 else col2:
            st.markdown(
                create_metric_card(label, value),
                unsafe_allow_html=True
            )

    # 그래프
    st.subheader('과거 30분 내부 환경 변화 및 예측', anchor=False)
    historical_data = get_historical_data()
    prediction_data = get_prediction_data()
    fig = create_combined_graph(historical_data, prediction_data)
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

if __name__ == '__main__':
    main()