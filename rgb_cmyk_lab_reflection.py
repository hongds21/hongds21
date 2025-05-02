
import streamlit as st
import math

def rgb_to_cmyk(r, g, b):
    if (r, g, b) == (0, 0, 0):
        return 0, 0, 0, 1
    c = 1 - r / 255
    m = 1 - g / 255
    y = 1 - b / 255
    min_cmy = min(c, m, y)
    c = (c - min_cmy) / (1 - min_cmy)
    m = (m - min_cmy) / (1 - min_cmy)
    y = (y - min_cmy) / (1 - min_cmy)
    k = min_cmy
    return round(c, 2), round(m, 2), round(y, 2), round(k, 2)

def cmyk_to_rgb(c, m, y, k):
    r = 255 * (1 - c) * (1 - k)
    g = 255 * (1 - m) * (1 - k)
    b = 255 * (1 - y) * (1 - k)
    return int(round(r)), int(round(g)), int(round(b))

def delta_e_lab(lab1, lab2):
    return round(math.sqrt((lab1[0] - lab2[0])**2 + (lab1[1] - lab2[1])**2 + (lab1[2] - lab2[2])**2), 2)

def get_absorbed_reflected(rgb):
    absorbed = []
    reflected = []

    if rgb[0] > 100:
        reflected.append("Đỏ")
    else:
        absorbed.append("Đỏ")
    if rgb[1] > 100:
        reflected.append("Xanh lá")
    else:
        absorbed.append("Xanh lá")
    if rgb[2] > 100:
        reflected.append("Xanh dương")
    else:
        absorbed.append("Xanh dương")

    return absorbed, reflected

st.set_page_config(page_title="RGB ↔ CMYK & ΔE & Absorption", layout="centered")
st.title("🎨 Chuyển đổi RGB ↔ CMYK | ΔE | Hấp thụ - Phản xạ")

tab1, tab2, tab3, tab4 = st.tabs(["🔵 RGB → CMYK", "🟠 CMYK → RGB", "🧪 LAB → ΔE", "🌈 Hấp thụ & Phản xạ"])

with tab1:
    st.subheader("Nhập màu RGB")
    r = st.slider("R (Red)", 0, 255, 255)
    g = st.slider("G (Green)", 0, 255, 255)
    b = st.slider("B (Blue)", 0, 255, 255)
    c, m, y, k = rgb_to_cmyk(r, g, b)

    st.markdown(f"**CMYK:** C={c}, M={m}, Y={y}, K={k}")
    st.markdown("**Màu RGB hiển thị:**")
    st.color_picker(" ", value=f'#{r:02x}{g:02x}{b:02x}', label_visibility="collapsed", key="rgb_color")

with tab2:
    st.subheader("Nhập màu CMYK")
    c = st.slider("C (Cyan)", 0.0, 1.0, 0.0)
    m = st.slider("M (Magenta)", 0.0, 1.0, 0.0)
    y = st.slider("Y (Yellow)", 0.0, 1.0, 0.0)
    k = st.slider("K (Black)", 0.0, 1.0, 0.0)

    r, g, b = cmyk_to_rgb(c, m, y, k)
    st.markdown(f"**RGB:** R={r}, G={g}, B={b}")
    st.markdown("**Màu RGB hiển thị:**")
    st.color_picker(" ", value=f'#{r:02x}{g:02x}{b:02x}', label_visibility="collapsed", key="cmyk_color")

with tab3:
    st.subheader("Nhập hai màu LAB để tính ΔE")

    st.markdown("**Màu 1**")
    L1 = st.number_input("L1", 0.0, 100.0, 50.0, key="L1")
    a1 = st.number_input("a1", -128.0, 127.0, 0.0, key="a1")
    b1 = st.number_input("b1", -128.0, 127.0, 0.0, key="b1")

    st.markdown("**Màu 2**")
    L2 = st.number_input("L2", 0.0, 100.0, 60.0, key="L2")
    a2 = st.number_input("a2", -128.0, 127.0, 10.0, key="a2")
    b2 = st.number_input("b2", -128.0, 127.0, 5.0, key="b2")

    delta_e = delta_e_lab((L1, a1, b1), (L2, a2, b2))
    st.markdown(f"### ✅ ΔE = {delta_e}")

with tab4:
    st.subheader("Chọn màu để xem ánh sáng bị hấp thụ & phản xạ")
    selected_color = st.color_picker("Chọn màu bất kỳ", "#ff0000", key="reflection_tab_color")
    r = int(selected_color[1:3], 16)
    g = int(selected_color[3:5], 16)
    b = int(selected_color[5:7], 16)

    absorbed, reflected = get_absorbed_reflected((r, g, b))

    st.markdown(f"**Màu bạn chọn có RGB = ({r}, {g}, {b})**")
    st.markdown(f"✅ **Phản xạ:** {', '.join(reflected)}")
    st.markdown(f"🚫 **Hấp thụ:** {', '.join(absorbed)}")

    st.markdown("**Minh họa màu chọn:**")
    st.color_picker(" ", value=selected_color, label_visibility="collapsed", key="reflection_preview")
