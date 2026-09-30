import streamlit as st
from decimal import Decimal, ROUND_HALF_UP

# =========================================================
# CẤU HÌNH TRANG
# =========================================================
st.set_page_config(
    page_title="Tính lãi tiền gửi tiết kiệm",
    page_icon="💰",
    layout="centered"
)

# =========================================================
# HÀM HỖ TRỢ
# =========================================================
def dinh_dang_tien(so_tien):
    """Định dạng tiền theo kiểu Việt Nam."""
    return f"{so_tien:,.0f} VNĐ".replace(",", ".")


def lam_tron(so):
    """Làm tròn số tiền đến đồng."""
    return float(
        Decimal(str(so)).quantize(
            Decimal("1"),
            rounding=ROUND_HALF_UP
        )
    )


def tinh_lai_don(tien_goc, lai_suat_nam, so_nam):
    """
    Công thức lãi đơn:
    I = P * r * t
    A = P + I
    """
    tien_lai = tien_goc * (lai_suat_nam / 100) * so_nam
    tong_tien = tien_goc + tien_lai

    return lam_tron(tien_lai), lam_tron(tong_tien)


def tinh_lai_kep(tien_goc, lai_suat_nam, so_nam, so_ky_ghep):
    """
    Công thức lãi kép:
    A = P * (1 + r/n)^(n*t)
    I = A - P

    so_ky_ghep:
        12 -> ghép lãi hàng tháng
        4  -> ghép lãi hàng quý
        1  -> ghép lãi cuối năm
    """
    lai_suat_ky = (lai_suat_nam / 100) / so_ky_ghep
    tong_so_ky = so_nam * so_ky_ghep

    tong_tien = tien_goc * ((1 + lai_suat_ky) ** tong_so_ky)
    tien_lai = tong_tien - tien_goc

    return lam_tron(tien_lai), lam_tron(tong_tien)


def tinh_lai_dinh_ky_lai_don(tien_goc, lai_suat_nam, tan_suat):
    """
    Tính tiền lãi của một kỳ lãnh lãi.

    tan_suat:
        12 -> tháng
        4  -> quý
        1  -> năm/cuối kỳ
    """
    return lam_tron(
        tien_goc * (lai_suat_nam / 100) / tan_suat
    )


def tinh_lai_dinh_ky_lai_kep(
    tien_goc,
    lai_suat_nam,
    tong_so_ky,
    so_ky_ghep
):
    """
    Trả về tiền lãi phát sinh ở kỳ cuối cùng.
    Dùng cho mục đích hiển thị 'tiền lãi định kỳ'.

    Với lãi kép:
    Lãi kỳ = số dư trước kỳ * lãi suất kỳ.
    """
    lai_suat_ky = (lai_suat_nam / 100) / so_ky_ghep

    if tong_so_ky <= 0:
        return 0

    # Số dư trước kỳ cuối
    so_du_truoc_ky = tien_goc * (
        (1 + lai_suat_ky) ** (tong_so_ky - 1)
    )

    lai_ky_cuoi = so_du_truoc_ky * lai_suat_ky

    return lam_tron(lai_ky_cuoi)


# =========================================================
# TIÊU ĐỀ
# =========================================================
st.title("💰 Máy tính lãi tiền gửi tiết kiệm")
st.write(
    "Tính toán tiền lãi theo phương pháp **lãi đơn** hoặc **lãi kép**."
)

# =========================================================
# NHẬP DỮ LIỆU
# =========================================================
st.subheader("Thông tin khoản tiền gửi")

tien_gui = st.number_input(
    "Số tiền gửi (VNĐ)",
    min_value=0.0,
    value=100_000_000.0,
    step=1_000_000.0,
    format="%.0f"
)

ky_han = st.number_input(
    "Kỳ hạn (tháng)",
    min_value=1,
    max_value=600,
    value=12,
    step=1
)

lai_suat = st.number_input(
    "Lãi suất (%/năm)",
    min_value=0.0,
    max_value=100.0,
    value=6.0,
    step=0.1,
    format="%.2f"
)

phuong_phap = st.selectbox(
    "Phương pháp tính lãi",
    [
        "Lãi đơn",
        "Lãi kép"
    ]
)

hinh_thuc_lanh_lai = st.selectbox(
    "Hình thức lãnh lãi",
    [
        "Lãnh lãi hàng tháng",
        "Lãnh lãi hàng quý",
        "Lãnh lãi cuối kỳ"
    ]
)

# =========================================================
# NÚT TÍNH
# =========================================================
if st.button("🧮 Tính tiền lãi", use_container_width=True):

    if tien_gui <= 0:
        st.error("Số tiền gửi phải lớn hơn 0.")
        st.stop()

    if lai_suat < 0:
        st.error("Lãi suất không được âm.")
        st.stop()

    # Kỳ hạn tính theo năm
    so_nam = ky_han / 12

    # Xác định số kỳ lãnh lãi
    if hinh_thuc_lanh_lai == "Lãnh lãi hàng tháng":
        tan_suat_lanh = 12
        ten_ky = "tháng"

    elif hinh_thuc_lanh_lai == "Lãnh lãi hàng quý":
        tan_suat_lanh = 4
        ten_ky = "quý"

    else:
        tan_suat_lanh = 1
        ten_ky = "cuối kỳ"

    # =====================================================
    # LÃI ĐƠN
    # =====================================================
    if phuong_phap == "Lãi đơn":

        tong_lai, tong_tien = tinh_lai_don(
            tien_gui,
            lai_suat,
            so_nam
        )

        # Lãi nhận trong một kỳ
        if hinh_thuc_lanh_lai == "Lãnh lãi hàng tháng":
            lai_dinh_ky = tinh_lai_dinh_ky_lai_don(
                tien_gui,
                lai_suat,
                12
            )

        elif hinh_thuc_lanh_lai == "Lãnh lãi hàng quý":
            lai_dinh_ky = tinh_lai_dinh_ky_lai_don(
                tien_gui,
                lai_suat,
                4
            )

        else:
            lai_dinh_ky = tong_lai

    # =====================================================
    # LÃI KÉP
    # =====================================================
    else:

        # Với lãi kép, chọn cách ghép lãi dựa vào kỳ lãnh lãi.
        if hinh_thuc_lanh_lai == "Lãnh lãi hàng tháng":
            so_ky_ghep = 12

        elif hinh_thuc_lanh_lai == "Lãnh lãi hàng quý":
            so_ky_ghep = 4

        else:
            # Cuối kỳ: ghép theo năm
            so_ky_ghep = 1

        tong_lai, tong_tien = tinh_lai_kep(
            tien_gui,
            lai_suat,
            so_nam,
            so_ky_ghep
        )

        tong_so_ky = ky_han * so_ky_ghep / 12

        # Số kỳ thực tế theo phương thức tính
        if hinh_thuc_lanh_lai == "Lãnh lãi hàng tháng":
            so_ky_thuc = ky_han

        elif hinh_thuc_lanh_lai == "Lãnh lãi hàng quý":
            so_ky_thuc = ky_han / 3

        else:
            so_ky_thuc = so_nam

        # Nếu kỳ hạn không chia hết cho quý/tháng,
        # vẫn hiển thị lãi kỳ cuối dựa trên công thức.
        lai_dinh_ky = tinh_lai_dinh_ky_lai_kep(
            tien_gui,
            lai_suat,
            max(1, int(so_ky_thuc * so_ky_ghep / tan_suat_lanh)),
            so_ky_ghep
        )

    # =====================================================
    # HIỂN THỊ KẾT QUẢ
    # =====================================================
    st.divider()
    st.subheader("📊 Kết quả")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            label=f"Tiền lãi định kỳ ({ten_ky})",
            value=dinh_dang_tien(lai_dinh_ky)
        )

    with col2:
        st.metric(
            label="Tổng tiền lãi",
            value=dinh_dang_tien(tong_lai)
        )

    with col3:
        st.metric(
            label="Tổng gốc + lãi",
            value=dinh_dang_tien(tong_tien)
        )

    # =====================================================
    # THÔNG TIN CHI TIẾT
    # =====================================================
    st.divider()

    st.markdown("### 📌 Thông tin khoản gửi")

    data = {
        "Nội dung": [
            "Số tiền gửi",
            "Kỳ hạn",
            "Lãi suất",
            "Phương pháp tính",
            "Hình thức lãnh lãi"
        ],
        "Giá trị": [
            dinh_dang_tien(tien_gui),
            f"{ky_han} tháng",
            f"{lai_suat:.2f}%/năm",
            phuong_phap,
            hinh_thuc_lanh_lai
        ]
    }

    st.table(data)

    # =====================================================
    # GHI CHÚ
    # =====================================================
    st.info(
        "Lưu ý: Lãi kép giả định tiền lãi được cộng vào gốc để tiếp tục "
        "sinh lãi. Nếu bạn thực tế rút tiền lãi hàng tháng hoặc hàng quý "
        "thì số tiền lãi đó không còn được tái đầu tư và cách tính thực tế "
        "sẽ khác."
    )

# =========================================================
# FOOTER
# =========================================================
st.divider()

st.caption(
    "Công cụ minh họa tính toán lãi tiền gửi — kết quả thực tế có thể "
    "khác tùy theo quy định của từng ngân hàng."
)
