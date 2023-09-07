import tkinter as tk

def get_checkbox_values():
    selected_values = []
    for i, checkbox_var in enumerate(checkbox_vars):
        if checkbox_var.get() == 1:
            selected_values.append(f"Checkbox {i+1}")

    print("te")

def clear_checkboxes():
    for checkbox_var in checkbox_vars:
        checkbox_var.set(0)


# 메인 창 생성
root = tk.Tk()
root.title("체크박스 예제")
root.geometry("250x600")
# 체크박스 변수 및 레이블 생성
checkbox_vars = [tk.IntVar() for _ in range(6)]
checkbox_labels = ["옵션 1", "옵션 2", "옵션 3", "옵션 4", "옵션 5", "옵션 6"]

for i, label_text in enumerate(checkbox_labels):
    checkbox = tk.Checkbutton(root, text=label_text, variable=checkbox_vars[i])
    checkbox.pack()

# 시작 버튼 생성
start_button = tk.Button(root, text="시작", command=get_checkbox_values)
start_button.pack()

# 종료 버튼 생성
clear_button = tk.Button(root, text="종료", command=clear_checkboxes)
clear_button.pack()

root.mainloop()
