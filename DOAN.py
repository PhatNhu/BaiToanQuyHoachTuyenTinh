import tkinter as tk
from tkinter import filedialog, messagebox
import numpy as np

# Hàm đọc dữ liệu từ file
def read_file(file_path):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            c = list(map(float, lines[0].strip().split()))  # Hệ số hàm mục tiêu (c)
            num_variables = len(c)  # Số lượng biến (có thể thay đổi)
            
            # Đọc ma trận các hệ số (A) với số lượng cột tương ứng với số biến
            A = [list(map(float, row.strip().split())) for row in lines[1:-1]]  # Các ràng buộc
            b = list(map(float, lines[-1].strip().split()))  # Vế phải b

            # Kiểm tra dữ liệu hợp lệ
            if len(A) != len(b):
                raise ValueError("Số lượng ràng buộc không khớp với số phần tử trong vector b")
            if len(A[0]) != num_variables:
                raise ValueError("Số cột của ma trận A không khớp với số biến trong c")

            return c, A, b, num_variables
    except Exception as e:
        messagebox.showerror("Lỗi", f"Lỗi khi đọc file: {e}")
        return None, None, None, None

# Hàm tính giá trị hàm mục tiêu
def calculate_objective(c, x):
    return sum(c[i] * x[i] for i in range(len(c)))

# Thuật toán Orchard
def orchard_algorithm(c, A, b, num_variables, num_iterations, log_interval):
    best_x = None
    min_value = float('inf')
    log_results = []

    for iteration in range(num_iterations):
        # Tạo ngẫu nhiên giá trị cho các biến quyết định trong giới hạn [0, 1]
        x = np.random.uniform(0, 1, num_variables)

        # Kiểm tra xem giá trị này có thỏa mãn ràng buộc Ax >= b không
        valid = True
        for i in range(len(A)):
            if sum(A[i][j] * x[j] for j in range(num_variables)) < b[i]:
                valid = False
                break

        # Nếu thỏa mãn, tính giá trị hàm mục tiêu
        if valid:
            value = calculate_objective(c, x)
            if value < min_value:
                min_value = value
                best_x = x

        # Log kết quả trung gian
        if (iteration + 1) % log_interval == 0:
            log_results.append((iteration + 1, min_value, best_x.copy() if best_x is not None else None))

    return min_value, best_x, log_results

# Hàm giải bài toán
def solve_problem(file_path, num_iterations, log_interval):
    c, A, b, num_variables = read_file(file_path)
    if c is None or A is None or b is None or num_variables is None:
        return

    # Gọi thuật toán Orchard
    min_value, best_x, log_results = orchard_algorithm(c, A, b, num_variables, num_iterations, log_interval)

    # Hiển thị kết quả cuối cùng
    result_text = "Kết quả sau khi hoàn thành tất cả các vòng lặp:\n"
    if best_x is not None:
        result_text += (
            f"Giá trị nhỏ nhất của hàm mục tiêu Z: {min_value:.4f}\n"
            f"Giá trị của các biến x dẫn đến Z min: {np.round(best_x, 4)}\n\n"
        )
    else:
        result_text += "Không tìm thấy nghiệm thỏa mãn.\n"

    # Hiển thị kết quả từng mốc
    result_text += "Kết quả trung gian theo mốc vòng lặp:\n"
    for log in log_results:
        iteration, value, x_vals = log
        result_text += f"- Sau {iteration} vòng lặp: Z = {value:.4f}, x = {np.round(x_vals, 4) if x_vals is not None else None}\n"

    show_result(result_text)

# Hàm hiển thị kết quả trong cửa sổ mới
def show_result(result_text):
    result_window = tk.Toplevel()
    result_window.title("Kết quả")
    result_label = tk.Text(result_window, wrap="word", width=80, height=30)
    result_label.insert(tk.END, result_text)
    result_label.pack(padx=20, pady=20)
    result_label.configure(state="disabled")  # Không cho phép chỉnh sửa
    close_button = tk.Button(result_window, text="Đóng", command=result_window.destroy)
    close_button.pack(pady=10)

# Hàm chọn file
def select_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if file_path:
        try:
            num_iterations = int(iterations_entry.get())
            log_interval = int(interval_entry.get())
            solve_problem(file_path, num_iterations, log_interval)
        except ValueError:
            messagebox.showerror("Lỗi", "Vui lòng nhập số vòng lặp và mốc hợp lệ!")

# Tạo giao diện
def create_gui():
    root = tk.Tk()
    root.title("Tối ưu hóa - Thuật toán Orchard")

    label = tk.Label(root, text="Chọn file chứa dữ liệu bài toán:")
    label.pack(pady=10)

    browse_button = tk.Button(root, text="Chọn file", command=select_file)
    browse_button.pack(pady=5)

    global iterations_entry, interval_entry
    iterations_label = tk.Label(root, text="Nhập số vòng lặp:")
    iterations_label.pack(pady=5)
    iterations_entry = tk.Entry(root)
    iterations_entry.pack(pady=5)

    interval_label = tk.Label(root, text="Nhập mốc log (số vòng lặp):")
    interval_label.pack(pady=5)
    interval_entry = tk.Entry(root)
    interval_entry.pack(pady=5)
    
    exit_button = tk.Button(root, text="Thoát", command=root.quit)
    exit_button.pack(pady=5)

    root.mainloop()

# Khởi chạy giao diện
create_gui()
