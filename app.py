import streamlit as st

def main():
    st.set_page_config(page_title="Tính Lãi Tiết Kiệm", page_icon="💰", layout="centered")
    
    st.title("💰 Ứng dụng Tính Lãi Gửi Tiết Kiệm")
    st.markdown("Nhập các thông tin bên dưới để tính toán số tiền lãi bạn sẽ nhận được.")

    # Tạo form nhập liệu
    with st.container():
        st.subheader("1. Thông tin gửi tiền")
        col1, col2 = st.columns(2)
        
        with col1:
            so_tien_gui = st.number_input("Số tiền gửi (VNĐ)", min_value=0.0, value=100000000.0, step=1000000.0, format="%f")
            ky_han = st.number_input("Kỳ hạn (Tháng)", min_value=1, value=12, step=1)
            
        with col2:
            lai_suat = st.number_input("Lãi suất (%/năm)", min_value=0.0, value=6.0, step=0.1)
            loai_lai = st.radio("Loại lãi suất", options=["Lãi đơn", "Lãi kép"])
            
        hinh_thuc = st.selectbox("Hình thức lãnh lãi", 
                                 options=["Lãnh lãi hàng tháng", "Lãnh lãi hàng quý", "Lãnh lãi cuối kỳ"])

    # Xử lý tính toán
    if st.button("Tính toán", type="primary", use_container_width=True):
        st.subheader("2. Kết quả tính toán")
        
        # Đưa lãi suất về số thập phân
        r = lai_suat / 100.0
        
        # Xác định số tháng của mỗi kỳ trả lãi
        if hinh_thuc == "Lãnh lãi hàng tháng":
            f = 1
        elif hinh_thuc == "Lãnh lãi hàng quý":
            f = 3
        else: # Cuối kỳ
            f = ky_han
            
        # Kiểm tra tính hợp lệ của kỳ hạn so với hình thức lãnh lãi
        if ky_han % f != 0:
            st.warning(f"Lưu ý: Kỳ hạn ({ky_han} tháng) không chia hết cho chu kỳ lãnh lãi ({f} tháng). Kết quả dưới đây được tính theo số kỳ chẵn.")
            
        so_ky = ky_han // f
        
        # Biến lưu kết quả
        lai_dinh_ky = 0.0
        tong_lai = 0.0
        tong_tien = 0.0
        
        if loai_lai == "Lãi đơn":
            # Lãi đơn: Lãi không cộng dồn vào gốc
            lai_dinh_ky = so_tien_gui * r * (f / 12)
            tong_lai = lai_dinh_ky * so_ky
            tong_tien = so_tien_gui + tong_lai
            
            ghi_chu_lai_dinh_ky = f"{lai_dinh_ky:,.0f} VNĐ"
            
        else:
            # Lãi kép: Lãi cộng dồn vào gốc sau mỗi kỳ
            tong_tien = so_tien_gui * ((1 + r * (f / 12)) ** so_ky)
            tong_lai = tong_tien - so_tien_gui
            
            if hinh_thuc == "Lãnh lãi cuối kỳ":
                ghi_chu_lai_dinh_ky = "Nhận 1 lần vào cuối kỳ"
            else:
                lai_ky_1 = so_tien_gui * r * (f / 12)
                ghi_chu_lai_dinh_ky = f"Kỳ đầu: {lai_ky_1:,.0f} VNĐ (Tăng dần các kỳ sau)"

        # Hiển thị kết quả bằng các Metric Card
        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric(label="Tiền lãi định kỳ", value=ghi_chu_lai_dinh_ky)
        with c2:
            st.metric(label="Tổng tiền lãi", value=f"{tong_lai:,.0f} VNĐ")
        with c3:
            st.metric(label="Tổng gốc + lãi", value=f"{tong_tien:,.0f} VNĐ")
            
        # Hiển thị chi tiết bảng tính nếu là lãi kép và nhận định kỳ
        if loai_lai == "Lãi kép" and hinh_thuc != "Lãnh lãi cuối kỳ":
            st.markdown("---")
            st.markdown("**Bảng minh họa lãi kép qua các kỳ:**")
            
            data = []
            goc_hien_tai = so_tien_gui
            for i in range(1, int(so_ky) + 1):
                lai_ky_nay = goc_hien_tai * r * (f / 12)
                goc_hien_tai += lai_ky_nay
                data.append({
                    "Kỳ": f"Kỳ {i}",
                    "Tiền lãi trong kỳ (VNĐ)": round(lai_ky_nay, 0),
                    "Tổng số dư (Gốc + Lãi)": round(goc_hien_tai, 0)
                })
                
            st.dataframe(data, use_container_width=True)

if __name__ == "__main__":
    main()
