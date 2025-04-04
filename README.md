# Hcmus-Project-Hashiwokakero
#####Hướng dẫn chạy chương trình giải Hashiwokakero#####
-----------------------------------------------------------
#1. Tổng quan dự án
Dự án này triển khai chương trình giải bài toán Hashiwokakero bằng logic CNF, thư viện PySAT và một số thuật toán khác. Mục tiêu là nối tất cả các đảo trên lưới bằng các cây cầu tuân thủ các quy tắc sau:
- Mỗi đảo phải có đúng số cầu như giá trị được biển diễn trên đảo.
- Cầu phải là đường thẳng ngang hoặc dọc(không chéo).
- Tối đa hai cầu có thể nối một cặp đảo.
- Cầu không được cắt nhau hoặc đi qua đảo khác.
- Kết quả cuối cùng phải tạo thành một nhóm đơn.
------------------------------------------------
#2. Cấu trúc thư mục source code
.
├── core
│   ├── Astar.py           # Chứa source code chính của thuật toán A*
│   ├── bridge.py          # Class Bridge (quản lý dữ liệu cầu)
│   ├── utils.py           # Các hàm hỗ trợ xử lý I/O
│   ├── cnf_generator.py   # Sinh các ràng buộc CNF
│   ├── solver.py          # Thuật toán PySAT, A*, Brute-force, Backtracking
│   ├── logic_variable.py  # Class lưu trữ các biến logic
│
├── Inputs
│   ├── input-01.txt
│   ├── input-02.txt
│
├── Outputs
│   ├── output-01.txt
│   ├── output-02.txt
│
├── main.py              # Tập tin dùng để chạy toàn chương trình
├── requirements.txt     # Danh sách các module cần cài đặt
└── README.txt
------------------------------------------------
#3. Hướng dẫn cài đặt các module cần thiết
a. Chạy lệnh sau để cài đặt các module:
    pip install -r requirements.txt
b. Hoặc có thể cài đặt từng cái riêng biệt bằng:
    pip install <module>
------------------------------------------------
#4. Biên dịch và chạy chương trình
Để chạy chương trình, chúng ta sử dụng lệnh sau:
    python main.py
##Lưu ý: Kết quả sẽ được đồng thời hiển thị trên màn hình và lưu vào thư mục `Outputs/`.
------------------------------------------------
#5. Cách thiết lập file input và đọc output
a.Thiết lập file input
- Mỗi ô trong lưới được phân tách bằng dấu phẩy.
- Giá trị '0' biểu diễn cho vị trí có thể đặt cầu được.
- Các giá trị từ 1->8 dùng để biển diễn đảo và số cầu cần của mỗi đảo.
b. Định dạng file output
- Mỗi ô trong lưới được phân tách bằng dấu phẩy.
- Các giá trị '0' là các vị trí trống.
- Các giá trị từ 1->8 dùng để biển diễn đảo.
- Kí hiệu '|' có nghĩa là 1 cầu thẳng đứng.
- Kí hiệu '$' có nghĩa là 2 cầu thẳng đứng.
- Kí hiệu '-' có nghĩa là 1 cầu thẳng ngang.
- Kí hiệu '=' có nghĩa là 2 cầu thẳng ngang.
-----------------------------------------------------------
