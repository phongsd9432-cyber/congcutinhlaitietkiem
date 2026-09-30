def format_tien(so_tien):
    """Định dạng tiền tệ sang dạng số có dấu phẩy ngăn cách hàng nghìn."""
    return f"{round(so_tien):,}".replace(",", ".") + " VNĐ"


def tinh_lai_don(goc, lai_suat_nam, thang):
    """Công thức lãi đơn:

    Lãi = Gốc * (Lãi suất năm / 12) * Số tháng
    """
    lai_thang = (lai_suat_nam / 100) / 12
    tien_lai = goc * lai_thang * thang
    tong_tien = goc + tien_lai
    return tien_lai, tong_tien


def tinh_lai_kep(goc, lai_suat_nam, thang):
    """Công thức lãi kép (nhập gốc hàng tháng):

    Tổng tiền = Gốc * (1 + Lãi suất tháng) ^ Số tháng
    """
    lai_thang = (lai_suat_nam / 100) / 12
    tong_tien = goc * ((1 + lai_thang) ** thang)
    tien_lai = tong_tien - goc
    return tien_lai, tong_tien


def tinh_tiet_kiem_tich_luy(goc_hang_thang, lai_suat_nam, thang):
    """Gửi góp tích lũy: Mỗi tháng gửi thêm một khoản cố định vào đầu tháng."""
    lai_thang = (lai_suat_nam / 100) / 12
    tong_tien = 0

    for _ in range(thang):
        tong_tien = (tong_tien + goc_hang_thang) * (1 + lai_thang)

    tong_goc_da_gui = goc_hang_thang * thang
    tien_lai = tong_tien - tong_goc_da_gui
    return tong_goc_da_gui, tien_lai, tong_tien


def main():
    print("=" * 45)
    print("   ỨNG DỤNG TÍNH LÃI TIẾT KIỆM (PYTHON)   ")
    print("=" * 45)

    print("Chọn phương thức tính:")
    print("1. Gửi 1 lần - Lãi đơn (nhận lãi cuối kỳ)")
    print("2. Gửi 1 lần - Lãi kép (lãi nhập gốc hàng tháng)")
    print("3. Gửi góp tích lũy đều đặn mỗi tháng")

    lua_chon = input("\nNhập lựa chọn của bạn (1/2/3): ").strip()

    if lua_chon not in ["1", "2", "3"]:
        print("Lựa chọn không hợp lệ, vui lòng chạy lại chương trình!")
        return

    try:
        if lua_chon in ["1", "2"]:
            tien_goc = float(input("Nhập số tiền gốc ban đầu (VNĐ): "))
        else:
            tien_goc = float(input("Nhập số tiền gửi định kỳ mỗi tháng (VNĐ): "))

        lai_suat = float(input("Nhập lãi suất gửi (%/năm, ví dụ 5.8): "))
        so_thang = int(input("Nhập kỳ hạn gửi (tháng, ví dụ 6, 12): "))

        if tien_goc <= 0 or lai_suat <= 0 or so_thang <= 0:
            print("Các giá trị nhập vào phải lớn hơn 0.")
            return

    except ValueError:
        print("Lỗi: Vui lòng chỉ nhập số hợp lệ.")
        return

    print("\n" + "-" * 45)
    print("KẾT QUẢ TÍNH TOÁN:")
    print("-" * 45)

    if lua_chon == "1":
        tien_lai, tong_tien = tinh_lai_don(tien_goc, lai_suat, so_thang)
        print(f"• Phương thức:       Lãi đơn (nhận cuối kỳ)")
        print(f"• Số tiền gốc:       {format_tien(tien_goc)}")
        print(f"• Kỳ hạn gửi:        {so_thang} tháng (lãi {lai_suat}%/năm)")
        print(f"• Tiền lãi nhận:     {format_tien(tien_lai)}")
        print(f"• Tổng tiền nhận:    {format_tien(tong_tien)}")

    elif lua_chon == "2":
        tien_lai, tong_tien = tinh_lai_kep(tien_goc, lai_suat, so_thang)
        print(f"• Phương thức:       Lãi kép (nhập gốc mỗi tháng)")
        print(f"• Số tiền gốc:       {format_tien(tien_goc)}")
        print(f"• Kỳ hạn gửi:        {so_thang} tháng (lãi {lai_suat}%/năm)")
        print(f"• Tiền lãi nhận:     {format_tien(tien_lai)}")
        print(f"• Tổng tiền nhận:    {format_tien(tong_tien)}")

    elif lua_chon == "3":
        tong_goc, tien_lai, tong_tien = tinh_tiet_kiem_tich_luy(
            tien_goc, lai_suat, so_thang
        )
        print(f"• Phương thức:       Gửi góp tích lũy hàng tháng")
        print(f"• Gửi mỗi tháng:     {format_tien(tien_goc)}")
        print(f"• Tổng gốc đã nộp:   {format_tien(tong_goc)} ({so_thang} tháng)")
        print(f"• Tiền lãi nhận:     {format_tien(tien_lai)}")
        print(f"• Tổng tiền nhận:    {format_tien(tong_tien)}")

    print("=" * 45)


# Chạy hàm chính
if __name__ == "__main__":
    main()
