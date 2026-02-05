import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.colors as mcolors
import numpy as np
import platform

# 1. 폰트 설정
system_name = platform.system()
if system_name == 'Windows':
    plt.rcParams['font.family'] = 'Malgun Gothic'
elif system_name == 'Darwin': # Mac
    plt.rcParams['font.family'] = 'AppleGothic'
else:
    plt.rcParams['font.family'] = 'NanumGothic'

plt.rcParams['axes.unicode_minus'] = False

def draw_gradient_rounded_box(ax, x, y, width, height, c_start, c_end, text, font_size=11, text_color='white', font_weight='bold', zorder=2):
    """
    둥근 모서리 박스 안에 그라데이션을 채우고 텍스트를 넣는 함수
    """
    # 1. 둥근 사각형 경로 생성 (클리핑용)
    box = patches.FancyBboxPatch((x, y), width, height,
                                boxstyle="round,pad=0.2,rounding_size=0.2",
                                fc='none', ec='none', zorder=zorder)
    ax.add_patch(box)

    # 2. 그라데이션 이미지 생성
    gradient = np.linspace(0, 1, 256).reshape(1, -1)
    cmap = mcolors.LinearSegmentedColormap.from_list("custom_grad", [c_start, c_end])
    
    # 3. 이미지 그리기
    im = ax.imshow(gradient, extent=(x, x + width, y, y + height), aspect='auto', cmap=cmap, zorder=zorder)
    
    # 4. 이미지를 둥근 사각형 모양으로 자르기 (Clip)
    im.set_clip_path(box)

    # 5. 그림자
    shadow = patches.FancyBboxPatch((x + 0.05, y - 0.05), width, height,
                                   boxstyle="round,pad=0.2,rounding_size=0.2",
                                   fc='gray', alpha=0.2, ec='none', zorder=zorder-1)
    ax.add_patch(shadow)

    # 6. 텍스트 추가
    ax.text(x + width / 2, y + height / 2, text, ha='center', va='center', 
            color=text_color, fontsize=font_size, fontweight=font_weight, linespacing=1.5, zorder=zorder+1)

def create_final_revised_chart():
    # 캔버스 크기
    fig, ax = plt.subplots(figsize=(14, 11), dpi=100)
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 11)
    ax.axis('off')

    # === 1. 상단 헤더 (타이틀 수정됨) ===
    # 색상 정의: 초록(MPC) -> 파랑(APF) 연결
    main_grad_start = '#00A67E' 
    main_grad_end = '#2B7AE0'   
    
    draw_gradient_rounded_box(ax, 0.5, 9.5, 11, 1.2, main_grad_start, main_grad_end, 
                              "MPC vs APF: 기존 제어 기법 비교 및 한계", font_size=24)

    # === 2. 이미지 영역 & 타이틀 ===
    # MPC (왼쪽)
    ax.text(3, 8.8, "MPC (최적화 기반)", ha='center', va='center', fontsize=16, fontweight='bold', color='#00695c')
    circle_mpc = patches.Circle((3, 7.6), 1.0, color='#f0f0f0', ec='#00A67E', lw=2)
    ax.add_patch(circle_mpc)
    ax.text(3, 7.6, "MPC 이미지\n삽입", ha='center', va='center', color='#757575', fontsize=10)

    # VS
    ax.text(6, 7.6, "VS", ha='center', va='center', fontsize=30, fontweight='black', color='#333')

    # APF (오른쪽)
    ax.text(9, 8.8, "APF (반응형)", ha='center', va='center', fontsize=16, fontweight='bold', color='#0d47a1')
    circle_apf = patches.Circle((9, 7.6), 1.0, color='#f0f0f0', ec='#2B7AE0', lw=2)
    ax.add_patch(circle_apf)
    ax.text(9, 7.6, "APF 이미지\n삽입", ha='center', va='center', color='#757575', fontsize=10)

    # === 3. 데이터 박스 ===
    rows = [
        ("특징", "미래 상태 예측\n고정밀 제어", "저연산($O(N)$)\n빠른 반응 속도"),
        ("한계", "군집 규모 증가 시\n연산량 폭증 ($O(N^3)$)", "복잡한 환경 내\n국소 최저점 및 진동"),
        ("결과", "CPU 점유율 85% 상회\n→ 시스템 지연", "잦은 가감속으로\n모터 전력 소모 15% 증가")
    ]

    y_pos = 5.5
    box_height = 0.9
    box_width = 4.2
    gap = 1.5 

    # 각 진영별 그라데이션 색상
    mpc_start, mpc_end = "#4DB6AC", "#00695c" 
    apf_start, apf_end = "#64B5F6", "#1565C0" 

    for category, left_text, right_text in rows:
        # MPC 박스
        draw_gradient_rounded_box(ax, 0.5, y_pos, box_width, box_height, mpc_start, mpc_end, left_text)
        
        # 가운데 카테고리
        ax.text(6, y_pos + box_height/2, category, ha='center', va='center', 
                color='#555', fontweight='bold', fontsize=12)
        
        # APF 박스
        draw_gradient_rounded_box(ax, 7.3, y_pos, box_width, box_height, apf_start, apf_end, right_text)
        
        y_pos -= gap

    # === 4. 하단 요약 (글자 강조) ===
    # 배경: 상단과 동일한 그라데이션
    # 텍스트: 밝은 노란색(Gold) + 폰트 키움
    draw_gradient_rounded_box(ax, 0.5, 0.8, 11, 1.0, main_grad_start, main_grad_end, 
                              "∴ 단일 기법으로는 '실시간성'과 '에너지 효율' 동시 만족 불가", 
                              font_size=16, text_color='#FFD700', font_weight='heavy') # FFD700: Gold

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    create_final_revised_chart()