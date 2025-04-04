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
#2. Cách thiết lập file input và đọc output
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
