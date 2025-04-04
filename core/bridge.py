class Bridge:
    def __init__(self, start, end, count=1):
        self.start = start  # Tọa độ điểm đầu (hàng, cột)
        self.end = end      # Tọa độ điểm cuối (hàng, cột)
        self.count = count  # Số lượng cầu (1 hoặc 2)

    def __repr__(self):
        """Hiển thị thông tin cầu nối (dùng để debug)."""
        return f"Bridge({self.start} → {self.end}, count={self.count})"
