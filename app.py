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

# CSS 스타일 수정
st.markdown("""
    <style>
        /* 모바일 최적화 */
        @media (max-width: 768px) {
            .main > div {
                padding: 0 !important;
            }
            .block-container {
                padding: 0.5rem !important;
                max-width: none !important;
            }
            .metric-container {
                margin: 0.3rem 0 !important;
                padding: 0.75rem !important;
            }
            .row-widget.stHorizontalBlock {
                flex-wrap: nowrap !important;
                gap: 0.5rem !important;
            }
            /* 열 사이의 간격 조정 */
            .row-widget.stHorizontalBlock > div {
                flex: 1 1 calc(50% - 0.5rem) !important;
                min-width: calc(50% - 0.5rem) !important;
            }
            [data-testid="column"] {
                width: calc(50% - 0.5rem) !important;
                flex: 1 1 calc(50% - 0.5rem) !important;
                min-width: calc(50% - 0.5rem) !important;
            }
        }
        
        /* 공통 스타일 */
        .main > div {
            padding: 1rem;
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
            margin: 0.5rem 0;
            box-sizing: border-box;
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
        
        /* Streamlit 기본 패딩 제거 */
        .css-1y4p8pa {
            padding: 0 !important;
        }
        .css-1r6slb0 {
            padding: 0 !important;
        }
        /* 열 간격 조정 */
        .css-12w0qpk {
            gap: 0.5rem !important;
        }
    </style>
""", unsafe_allow_html=True)

def get_sensor_data(target_time):
    data = {
        'internal_temp': 21.1,
        'internal_humidity': 60.8,
        'external_temp': 15.4,
        'wind_direction': '좌',
        'wind_speed': 1.1,
        'dew_point': 12.7,
        'solar_radiation': 247
    }
    return data

def get_historical_data():
    data = {
        '저장시간': pd.date_range(start='2018-05-10 09:30:00',
                              end='2018-05-10 10:00:00', freq='1min'),
        '내부온도': [19.5, 19.5, 19.6, 19.6, 19.7, 19.7, 19.7, 19.8, 19.8, 19.8,
                  19.8, 19.8, 19.8, 19.8, 19.8, 19.9, 19.9, 20.1, 20.2, 20.3,
                  20.4, 20.6, 20.9, 21.1, 21.3, 21.3, 21.3, 21.3, 21.2, 21.2, 21.1],
        '내부습도': [65.6, 65.5, 64.9, 64.9, 64.2, 64.2, 64.7, 64.2, 63.6, 63.5,
                  63.5, 63.5, 63.5, 63.2, 63.2, 62.5, 62.9, 63.8, 63.6, 63.9,
                  63.1, 61.9, 61.4, 61.6, 61.6, 61.3, 61.0, 60.9, 60.7, 60.6, 60.8]
    }
    return pd.DataFrame(data)

def get_prediction_data():
    data = {
        '예측시간': pd.date_range(start='2018-05-10 10:00:00',
                              end='2018-05-10 10:05:00', freq='1min'),
        '예측온도': [21.1, 21.2, 21.3, 21.4, 21.5, 21.6],
        '예측습도': [60.8, 60.5, 60.2, 59.9, 59.6, 59.3]
    }
    return pd.DataFrame(data)

def create_metric_card(label, value):
    return f"""
        <div class="metric-container">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
        </div>
    """

def create_combined_graph(historical_data, prediction_data):
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # 실제 온도 데이터
    fig.add_trace(
        go.Scatter(
            x=historical_data['저장시간'],
            y=historical_data['내부온도'],
            name="실제 온도",
            line=dict(color="#FF4B4B", width=2)
        ),
        secondary_y=False,
    )

    # 예측 온도 데이터
    fig.add_trace(
        go.Scatter(
            x=prediction_data['예측시간'],
            y=prediction_data['예측온도'],
            name="예측 온도",
            line=dict(color="#FF4B4B", width=2, dash='dash')
        ),
        secondary_y=False,
    )

    # 실제 습도 데이터
    fig.add_trace(
        go.Scatter(
            x=historical_data['저장시간'],
            y=historical_data['내부습도'],
            name="실제 습도",
            line=dict(color="#4B4BFF", width=2)
        ),
        secondary_y=True,
    )

    # 예측 습도 데이터
    fig.add_trace(
        go.Scatter(
            x=prediction_data['예측시간'],
            y=prediction_data['예측습도'],
            name="예측 습도",
            line=dict(color="#4B4BFF", width=2, dash='dash')
        ),
        secondary_y=True,
    )

    # 현재 시점을 나타내는 수직선 및 텍스트 추가
    current_time = historical_data['저장시간'].iloc[-1]

    fig.update_layout(
        margin=dict(l=50, r=50, t=30, b=30),
        height=600,  # 고정 높이
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(size=12),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        xaxis=dict(
            showgrid=True,
            gridcolor='lightgray',
            showline=True,
            linewidth=1,
            linecolor='lightgray'
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='lightgray',
            showline=True,
            linewidth=1,
            linecolor='lightgray',
            title_text="온도 (°C)"
        ),
        yaxis2=dict(
            showgrid=False,
            showline=True,
            linewidth=1,
            linecolor='lightgray',
            title_text="습도 (%)"
        ),
        shapes=[
            # 현재 시점을 나타내는 수직선
            dict(
                type="line",
                xref="x",
                yref="paper",
                x0=current_time,
                y0=0,
                x1=current_time,
                y1=1,
                line=dict(
                    color="gray",
                    width=1,
                    dash="dot",
                )
            )
        ],
        annotations=[
            # 현재 시점 텍스트
            dict(
                x=current_time,
                y=1.05,
                xref="x",
                yref="paper",
                text="현재",
                showarrow=False,
                font=dict(size=12)
            )
        ]
    )

    # y축 제목 업데이트
    fig.update_yaxes(title_text="온도 (°C)", secondary_y=False)
    fig.update_yaxes(title_text="습도 (%)", secondary_y=True)

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
    col1, col2 = st.columns([1, 1], gap="small")
    
    with col1:
        st.markdown(
            create_metric_card("내부 온도", f"{sensor_data['internal_temp']} °C"),
            unsafe_allow_html=True
        )
    with col2:
        st.markdown(
            create_metric_card("내부 습도", f"{sensor_data['internal_humidity']} %"),
            unsafe_allow_html=True
        )

    # 2. 외부 환경 데이터 - 모바일에서는 2열로 표시
    st.subheader('외부 환경', anchor=False)
    col1, col2 = st.columns([1, 1], gap="small")
    
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