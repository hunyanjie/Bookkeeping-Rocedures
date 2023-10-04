import os
import tkinter as tk
import webbrowser
from datetime import date
from tkinter import ttk, messagebox, filedialog
global encode

def select_date():
    year = year_var.get()
    month = month_var.get().zfill(2)
    day = cal_var.get().zfill(2)
    selected_date = f"{year}{month}{day}"
    date_entry.delete(0, tk.END)
    date_entry.insert(tk.END, selected_date)
def select_file():
    # 单个文件选择
    global select_path
    select_path = filedialog.askopenfilename()  # 使用askopenfilename函数选择单个文件
    if os.path.isfile(select_path):
        file_show['text'] = os.path.basename(select_path)
        status['text'] = '可以开始填写'
        status['fg'] = 'blue'
def update_days(*args):
    month_value = int(month_var.get())
    year_value = int(year_var.get())
    if month_value == 2:
        if (year_value % 4 == 0 and year_value % 100 != 0) or (year_value % 400 == 0):
            days = list(range(1, 30))
        else:
            days = list(range(1, 29))
    elif month_value in [4, 6, 9, 11]:
        days = list(range(1, 31))
    else:
        days = list(range(1, 32))
        # 如果当前选择的日期不在新的日期选项中，则将日期选择框的值设置为新的日期选项的最后一天
    if int(cal_var.get()) not in days:
        cal_var.set(str(days[-1]).zfill(2))
    cal['values'] = days
def save(new_text, topic, target_line=99999, encode='utf-8'):
    try:
        f = open(select_path, encoding=encode)
        f.close()
    except FileNotFoundError:
        status['text'] = '未选择文件！！'
        status['fg'] = 'red'
        return
    except PermissionError:
        status['text'] = '所选文件没权限读写！！！'
        status['fg'] = 'red'
        return
    with open(select_path, 'r', encoding=encode) as datas:
        lines = datas.readlines()[:]
    if len(lines) == 0:
        lines.append(f'【{topic}】\n')
        lines.append(new_text + '\n')
    elif f'【{topic}】\n' in lines:
        section_line = None
        section_lines = []
        i = 0
        for i, line in enumerate(lines):
            info = line.replace('\n', '').replace(' ', '')
            if info != '':
                if line.startswith(f'【{topic}】'):
                    section_line = i
                if line.startswith('【') and section_line is not None:
                    section_lines = lines[section_line:i]
                    if section_lines:
                        break
        if target_line > len(section_lines):
            if (i + 1) >= len(lines):
                lines.append(new_text + '\n')
            else:
                # 在节的最后一行之后插入新行
                lines.insert(i, new_text)
        else:
            # 在指定的行号处插入新行
            lines.insert(section_line + target_line, new_text)
    else:
        for i, line in enumerate(lines):
            info = line.replace('/n', '').replace(' ', '')
            if info != '':
                if line.startswith('【') and line.endswith('】\n'):
                    if float(line.replace('【', '').replace('】', '').replace('\n', '').replace(' ', '')) > topic:
                        lines.insert(i, new_text + '\n')
                        lines.insert(i, f'【{topic}】\n')
                        break
            if (i + 1) >= len(lines):
                lines.append(f'【{topic}】\n')
                lines.append(new_text + '\n')
                break

    with open(select_path, 'w', encoding=encode) as f:
        for data in lines:
            if data[-1:] != '\n':
                data += '\n'
            f.write(data)
def save_to_file(*args):
    try:
        f = open(select_path)
        f.close()
    except FileNotFoundError:
        status['text'] = '未选择文件！！'
        status['fg'] = 'red'
        return
    except PermissionError:
        status['text'] = '所选文件没权限读写！！！'
        status['fg'] = 'red'
        return
    date = date_entry.get().replace('\n', '').replace('：', '')  # 日期
    amount = amount_entry.get().replace('\n', '').replace('：', '')  # 金额
    payment_method = payment_method_combobox.get().replace('\n', '').replace('：', '')  # 支付平台
    specific_payment_method = specific_payment_method_combobox.get().replace('\n', '').replace('：', '')  # 具体支付方式
    payment_method_order_number = payment_method_order_number_entry.get().replace('\n', '').replace('：', '')  # 支付平台订单编号
    platform = platform_combobox.get().replace('\n', '').replace('：', '')  # 购买平台
    platform_order_number = platform_order_number_entry.get().replace('\n', '').replace('：', '')  # 购买平台订单编号
    purpose = purpose_combobox.get().replace('\n', '').replace('：', '')  # 用途
    remark = remark_entry.get().replace('\n', '').replace('：', '')  # 用途
    if not (
            date and amount and payment_method and specific_payment_method and payment_method_order_number and platform and purpose
    ):
        status['text'] = '请填写完整！'
        status['fg'] = 'red'
        return
    if not platform_order_number:
        if not remark:
            text = str(
                f"{amount}（{payment_method}（{specific_payment_method}））：{platform}：{purpose}：订单编号（{payment_method}：{payment_method_order_number}）")
        else:
            text = str(
                f"{amount}（{payment_method}（{specific_payment_method}））：{platform}：{purpose}：{remark}：订单编号（{payment_method}：{payment_method_order_number}）")
    else:
        if not remark:
            text = str(
                f"{amount}（{payment_method}（{specific_payment_method}））：{platform}：{purpose}：订单编号（{payment_method}：{payment_method_order_number}、{platform}：{payment_method_order_number}）")
        else:
            text = str(
                f"{amount}（{payment_method}（{specific_payment_method}））：{platform}：{purpose}：{remark}：订单编号（{payment_method}：{payment_method_order_number}、{platform}：{payment_method_order_number}）")
    save(text, int(date))
    status['text'] = '保存成功！'
    status['fg'] = 'green'
def clear_entries():
    date_entry.delete(0, tk.END)
    amount_entry.delete(0, tk.END)
    payment_method_combobox.set("")
    specific_payment_method_combobox.set("")
    payment_method_order_number_entry.delete(0, tk.END)
    platform_combobox.set("")
    platform_order_number_entry.delete(0, tk.END)
    specific_payment_method_combobox['values'] = ["--请先选择支付方式--"]
    specific_payment_method_combobox.current(0)
    purpose_combobox['values'] = ["", "网上购物", "线下购物", "外卖", "转账", "红包", "餐厅消费", "交通", "旅行",
                                  '快递', "生活缴费", "工资", "退款", "商家转账"]
    purpose_combobox.current(0)
    remark_entry.delete(0, tk.END)
    save_button.config(text="保存", command=save_to_file)
    status['text'] = '已清空！可以继续填写'
    status['fg'] = 'blue'
def import_from_file(*args):
    try:
        with open(select_path, "r", encoding="UTF-8") as file:
            lines = file.readlines()

        # 解析导入的内容并填充到输入框中
        date_entry.delete(0, tk.END)
        amount_entry.delete(0, tk.END)
        payment_method_combobox.set("")
        specific_payment_method_combobox.set("")
        payment_method_order_number_entry.delete(0, tk.END)
        platform_combobox.set("")
        platform_order_number_entry.delete(0, tk.END)
        purpose_combobox.delete(0, tk.END)

        in_a_day = False
        for line in lines:
            line = line.strip()
            if not in_a_day:
                if line.startswith("【"):
                    tmp_date = line.split("【")[1].split("】")[0].strip()
                    data = {
                        'date': tmp_date
                    }
                    in_a_day = True
            elif in_a_day:
                line.strip()
                if line.strip() != '':
                    count = 0
                    start_index = -1
                    for i, char in enumerate(line.split("：")[0]):
                        if char == "（":
                            count += 1
                            if count == 2 and start_index == -1:
                                start_index = i
                        elif char == "）":
                            count -= 1
                            if count == 1 and start_index != -1:
                                data["specific_payment_method"] = line.split("：")[0][start_index + 1:i]
                                break
                    data["amount"] = line.split("：")[0].split("（")[0]  # 金额
                    data["payment_method"] = line.split("：")[0].split("（")[1]  # 支付平台
                    data["platform"] = line.split("：")[1]  # 购买平台
                    data["purpose"] = line.split("：")[2]  # 用途
                    tmp_data = [line.split("：")[3].split("（")[1], line.split("：")[4].split("、")[0],
                                line.split("：")[4].split("、")[1], line.split("：")[5].split("）")[0]]
                    next_prepare_one = None
                    next_prepare_two = None
                    for data_info in tmp_data:
                        if data["payment_method"] == data_info:
                            next_prepare_one = 'payment_method'
                        elif data["platform"] == data_info:
                            next_prepare_two = 'platform'
                        elif next_prepare_one == 'payment_method':
                            data["payment_method_order_number"] = data_info  # 支付平台订单编号
                        elif next_prepare_two == 'platform':
                            data["platform_order_number"] = data_info  # 购买平台订单编号
                    date_entry.insert(tk.END, data["date"])  # 日期
                    amount_entry.insert(tk.END, data["amount"])  # 金额
                    payment_method_combobox.set(data["payment_method"])  # 支付平台
                    specific_payment_method_combobox.set(data["specific_payment_method"])  # 具体支付方式
                    payment_method_order_number_entry.insert(tk.END, data["payment_method_order_number"])  # 支付平台订单编号
                    platform_combobox.set(data["platform"])  # 购买平台
                    platform_order_number_entry.insert(tk.END, data["platform_order_number"])  # 购买平台订单编号
                    purpose_combobox.insert(tk.END, data["purpose"])
        payment_method_select(None)
    except FileNotFoundError:
        messagebox.showerror("错误", "没有找到保存的订单文件")
def payment_method_select(*args):
    if payment_method_combobox.get() == '支付宝':
        specific_payment_method_combobox['values'] = ['', '账户余额', '银行卡', '亲情卡', '余额宝', '小荷包']
    elif payment_method_combobox.get() == '微信':
        specific_payment_method_combobox['values'] = ['', '零钱', '银行卡']
    else:
        specific_payment_method_combobox['values'] = ['']
    status_check(None)
# 屏幕键盘
def click_1():
    amount_entry.insert(tk.END, '1')
def click_2():
    amount_entry.insert(tk.END, '2')
def click_3():
    amount_entry.insert(tk.END, '3')
def click_4():
    amount_entry.insert(tk.END, '4')
def click_5():
    amount_entry.insert(tk.END, '5')
def click_6():
    amount_entry.insert(tk.END, '6')
def click_7():
    amount_entry.insert(tk.END, '7')
def click_8():
    amount_entry.insert(tk.END, '8')
def click_9():
    amount_entry.insert(tk.END, '9')
def click_0():
    amount_entry.insert(tk.END, '0')
def click_sub():
    amount_entry.insert(tk.END, '-')
def click_del():
    info = amount_entry.get()
    amount_entry.delete(0, tk.END)
    amount_entry.insert(tk.END, info[0:len(info) - 1])
def click_dot():
    amount_entry.insert(tk.END, '.')
# 完整性检查
def status_check(*args):
    date = date_entry.get().replace('\n', '').replace('：', '')  # 日期
    amount = amount_entry.get().replace('\n', '').replace('：', '')  # 金额
    payment_method = payment_method_combobox.get().replace('\n', '').replace('：', '')  # 支付平台
    specific_payment_method = specific_payment_method_combobox.get().replace('\n', '').replace('：', '')  # 具体支付方式
    payment_method_order_number = payment_method_order_number_entry.get().replace('\n', '').replace('：', '')  # 支付平台订单编号
    platform = platform_combobox.get().replace('\n', '').replace('：', '')  # 购买平台
    purpose = purpose_combobox.get().replace('\n', '').replace('：', '')  # 用途
    if not (
            date and amount and payment_method and specific_payment_method and payment_method_order_number and platform and purpose):
        # messagebox.showerror("错误", "请填写所有字段")
        status['text'] = '未填写完整'
        status['fg'] = 'black'
    else:
        status['text'] = '可以提交'
        status['fg'] = 'blue'
def purpose_check(*args):
    amount = amount_entry.get().replace('\n', '').replace('：', '')  # 金额
    if amount.isdigit():
        purpose_combobox['values'] = ["", "红包", '转账', "工资", "红包", "退款", "商家转账"]
    elif amount.startswith('-') and amount.count('-') == 1 and amount.replace('-', '').isdigit():
        purpose_combobox['values'] = ["", "网上购物", "线下购物", "外卖", "转账", "红包", "餐厅消费", "交通", "旅行",
                                      '快递', "生活缴费"]
    else:
        purpose_combobox['values'] = ["", "网上购物", "线下购物", "外卖", "转账", "红包", "餐厅消费", "交通", "旅行",
                                      '快递', "生活缴费", "工资", "退款", "商家转账"]
    status_check(None)
def day_month_check(*args):
    day_month_choose_get_var = day_month_choose_var.get()
    if day_month_choose_get_var == 'month':
        frame_cal['state'] = 'disabled'
    else:
        frame_cal['state'] = 'active'
def frame_update_days(*args):
    frame_month_value = int(frame_month_var.get())
    frame_year_value = int(frame_year_var.get())
    if frame_month_value == 2:
        if (frame_year_value % 4 == 0 and frame_year_value % 100 != 0) or (frame_year_value % 400 == 0):
            days = list(range(1, 30))
        else:
            days = list(range(1, 29))
    elif frame_month_value in [4, 6, 9, 11]:
        days = list(range(1, 31))
    else:
        days = list(range(1, 32))
        # 如果当前选择的日期不在新的日期选项中，则将日期选择框的值设置为新的日期选项的最后一天
    if int(frame_cal_var.get()) not in days:
        frame_cal_var.set(str(days[-1]).zfill(2))
    frame_cal['values'] = days
def select_day_or_month(*args, encode='utf-8'):
    day_month_choose_get_var = day_month_choose_var.get()
    section_lines = []
    global check_selected_date
    try:
        f = open(select_path, encoding=encode)
        f.close()
    except FileNotFoundError:
        status['text'] = '未选择文件！！'
        status['fg'] = 'red'
        return
    except PermissionError:
        status['text'] = '所选文件没权限读写！！！'
        status['fg'] = 'red'
        return
    with open(select_path, 'r', encoding=encode) as datas:
        lines = datas.readlines()[:]
    if day_month_choose_get_var == 'month':
        year = frame_year_var.get()
        month = frame_month_var.get().zfill(2)
        check_selected_date = f"{year}{month}"
        frame_date_show_label['text'] = check_selected_date
        section_lines = []
        section_line = None
        for i, line in enumerate(lines):
            info = line.replace('\n', '').replace(' ', '')
            if info != '':
                if line.startswith('【') and not line.startswith(f'【{check_selected_date}'):
                    section_line = None
                if line.startswith(f'【{check_selected_date}'):
                    section_line = i
                if section_line is not None:
                    section_lines.append(line)
        if len(section_lines) - 1 <= 0:
            frame_trade_times_show_label['text'] = 0
        else:
            frame_trade_times_show_label['text'] = len(section_lines) - 1
        all_money = 0  # 总流水
        trade_out = 0  # 支出笔数
        trade_in = 0  # 入账笔数
        all_money_total = 0  # 盈余
        all_money_out = 0  # 总支出
        all_money_in = 0  # 总入账
        for line in section_lines:
            line = line.strip()
            if not line.startswith("【"):
                line.strip()
                if line.strip() != '':
                    money = float(line.split("：")[0].split("（")[0])  # 金额
                    all_money += abs(money)  # 总流水
                    all_money_total += money  # 盈余
                    if money >= 0:
                        trade_in += 1  # 入账笔数
                        all_money_in += money  # 总入账
                    elif money < 0:
                        trade_out += 1  # 支出笔数
                        all_money_out += money  # 总支出
        frame_all_money_show_label['text'] = all_money
        frame_trade_out_times_show_label['text'] = trade_out
        frame_trade_in_times_show_label['text'] = trade_in
        frame_all_money_total_times_show_label['text'] = all_money_total
        frame_all_money_out_times_show_label['text'] = all_money_out
        frame_all_money_in_times_show_label['text'] = all_money_in
        order_show_listbox.delete(0, "end")
        if not section_lines:
            order_show_listbox.insert("end", '*无*')  # 插入新的项目
        else:
            for order in section_lines:
                order_show_listbox.insert("end", order)  # 插入新的项目
    else:
        year = frame_year_var.get()
        month = frame_month_var.get().zfill(2)
        day = frame_cal_var.get().zfill(2)
        check_selected_date = f"{year}{month}{day}"
        frame_date_show_label['text'] = check_selected_date
        section_lines = []
        section_line = None
        if f'【{check_selected_date}】\n' in lines:
            for i, line in enumerate(lines):
                info = line.replace('\n', '').replace(' ', '')
                if info != '':
                    if line.startswith(f'【{check_selected_date}】'):
                        section_line = i
                    if section_line is not None:
                        section_lines.append(line)
                        if line.startswith('【'):
                            section_lines = lines[section_line:i]
                            if section_lines:
                                break
        if len(section_lines) - 1 <= 0:
            frame_trade_times_show_label['text'] = 0
        else:
            frame_trade_times_show_label['text'] = len(section_lines) - 1

        all_money = 0.00  # 总流水
        trade_out = 0  # 支出笔数
        trade_in = 0  # 入账笔数
        all_money_total = 0.00  # 盈余
        all_money_out = 0.00  # 总支出
        all_money_in = 0.00  # 总入账
        for line in section_lines:
            line = line.strip()
            if not line.startswith("【"):
                line.strip()
                if line.strip() != '':
                    money = float(line.split("：")[0].split("（")[0])  # 金额
                    all_money += abs(money)  # 总流水
                    all_money_total += money  # 盈余
                    if money >= 0:
                        trade_in += 1  # 入账笔数
                        all_money_in += money  # 总入账
                    elif money < 0:
                        trade_out += 1  # 支出笔数
                        all_money_out += money  # 总支出
        frame_all_money_show_label['text'] = all_money
        frame_trade_out_times_show_label['text'] = trade_out
        frame_trade_in_times_show_label['text'] = trade_in
        frame_all_money_total_times_show_label['text'] = all_money_total
        frame_all_money_out_times_show_label['text'] = all_money_out
        frame_all_money_in_times_show_label['text'] = all_money_in
        order_show_listbox.delete(0, "end")
        if not section_lines:
            order_show_listbox.insert("end", '*无*')  # 插入新的项目
        else:
            for order in section_lines:
                if not order.startswith('【'):
                    order_show_listbox.insert("end", order)  # 插入新的项目
# 修改所选定的内容
def amend_choose(*args):
    global bill, data
    bill = order_show_listbox.get(order_show_listbox.curselection())
    count = 0
    start_index = -1
    data = {
        'date': check_selected_date,
        'amount': None,
        'payment_method': None,
        'specific_payment_method': None,
        'payment_method_order_number': None,
        'platform': None,
        'platform_order_number': None,
        'purpose': None,
        'remark': None
    }
    for i, char in enumerate(bill.split("：")[0]):
        if char == "（":
            count += 1
            if count == 2 and start_index == -1:
                start_index = i
        elif char == "）":
            count -= 1
            if count == 1 and start_index != -1:
                data["specific_payment_method"] = bill.split("：")[0][start_index + 1:i]
                break
    try:
        data["amount"] = bill.split("：")[0].split("（")[0]  # 金额
        data["payment_method"] = bill.split("：")[0].split("（")[1]  # 支付平台
        data["platform"] = bill.split("：")[1]  # 购买平台
        data["purpose"] = bill.split("：")[2]  # 用途
    except:
        status['text'] = '请选择有效的内容！'
        status['fg'] = 'red'
        return
    try:
        data["remark"] = bill.split("：")[3]  # 备注
        tmp_data = [bill.split("：")[4].split("（")[1], bill.split("：")[5].split("、")[0]]
        try:
            tmp_data.append(bill.split("：")[5].split("、")[1])
            tmp_data.append(bill.split("：")[6].split("）")[0])
        except:
            pass
    except:
        tmp_data = [bill.split("：")[3].split("（")[1], bill.split("：")[4].split("、")[0]]
        try:
            tmp_data.append(bill.split("：")[4].split("、")[1])
            tmp_data.append(bill.split("：")[5].split("）")[0])
        except:
            pass
    next_prepare_one = None
    next_prepare_two = None
    for data_info in tmp_data:
        if data["payment_method"] == data_info:
            next_prepare_one = 'payment_method'
        elif data["platform"] == data_info:
            next_prepare_two = 'platform'
        elif next_prepare_one == 'payment_method':
            data["payment_method_order_number"] = data_info  # 支付平台订单编号
            next_prepare_one = None
        elif next_prepare_two == 'platform':
            data["platform_order_number"] = data_info  # 购买平台订单编号
            next_prepare_two = None
    # 解析导入的内容并填充到输入框中
    date_entry.delete(0, tk.END)
    amount_entry.delete(0, tk.END)
    payment_method_combobox.set("")
    specific_payment_method_combobox.set("")
    payment_method_order_number_entry.delete(0, tk.END)
    platform_combobox.set("")
    platform_order_number_entry.delete(0, tk.END)
    specific_payment_method_combobox['values'] = ["--请先选择支付方式--"]
    specific_payment_method_combobox.current(0)
    purpose_combobox['values'] = ["", "网上购物", "线下购物", "外卖", "转账", "红包", "餐厅消费", "交通", "旅行",
                                  '快递', "生活缴费", "工资", "退款", "商家转账"]
    purpose_combobox.current(0)
    remark_entry.delete(0, tk.END)

    date_entry.insert(tk.END, data["date"])  # 日期
    amount_entry.insert(tk.END, data["amount"])  # 金额
    payment_method_combobox.set(data["payment_method"])  # 支付平台
    specific_payment_method_combobox.set(data["specific_payment_method"])  # 具体支付方式
    payment_method_order_number_entry.insert(tk.END, data["payment_method_order_number"])  # 支付平台订单编号
    platform_combobox.set(data["platform"])  # 购买平台
    try:
        platform_order_number_entry.insert(tk.END, data["platform_order_number"])  # 购买平台订单编号
    except:
        pass
    purpose_combobox.insert(tk.END, data["purpose"])  # 用途
    try:
        remark_entry.insert(tk.END, data["remark"])  # 备注
    except:
        pass
    save_button.config(text='修改', command=lambda: amend_to_file(bill))
def amend_to_file(old_data):
    try:
        f = open(select_path)
        f.close()
    except FileNotFoundError:
        status['text'] = '未选择文件！！'
        status['fg'] = 'red'
        return
    except PermissionError:
        status['text'] = '所选文件没权限读写！！！'
        status['fg'] = 'red'
        return
    date = date_entry.get().replace('\n', '').replace('：', '')  # 日期
    amount = amount_entry.get().replace('\n', '').replace('：', '')  # 金额
    payment_method = payment_method_combobox.get().replace('\n', '').replace('：', '')  # 支付平台
    specific_payment_method = specific_payment_method_combobox.get().replace('\n', '').replace('：', '')  # 具体支付方式
    payment_method_order_number = payment_method_order_number_entry.get().replace('\n', '').replace('：', '')  # 支付平台订单编号
    platform = platform_combobox.get().replace('\n', '').replace('：', '')  # 购买平台
    platform_order_number = platform_order_number_entry.get().replace('\n', '').replace('：', '')  # 购买平台订单编号
    purpose = purpose_combobox.get().replace('\n', '').replace('：', '')  # 用途
    remark = remark_entry.get().replace('\n', '').replace('：', '')  # 用途
    if not (
            date and amount and payment_method and specific_payment_method and payment_method_order_number and platform and purpose
    ):
        status['text'] = '请填写完整！'
        status['fg'] = 'red'
        return
    if not platform_order_number:
        if not remark:
            text = str(
                f"{amount}（{payment_method}（{specific_payment_method}））：{platform}：{purpose}：订单编号（{payment_method}：{payment_method_order_number}）")
        else:
            text = str(
                f"{amount}（{payment_method}（{specific_payment_method}））：{platform}：{purpose}：{remark}：订单编号（{payment_method}：{payment_method_order_number}）")
    else:
        if not remark:
            text = str(
                f"{amount}（{payment_method}（{specific_payment_method}））：{platform}：{purpose}：订单编号（{payment_method}：{payment_method_order_number}、{platform}：{payment_method_order_number}）")
        else:
            text = str(
                f"{amount}（{payment_method}（{specific_payment_method}））：{platform}：{purpose}：{remark}：订单编号（{payment_method}：{payment_method_order_number}、{platform}：{payment_method_order_number}）")
    status['text'] = '保存成功！'
    status['fg'] = 'green'
    with open(select_path, "r", encoding="utf-8") as f:
        data = f.readlines()
    line_number = data.index(old_data)
    del data[line_number]
    data.insert(line_number, text)
    with open(select_path, 'w', encoding=encode) as lines:
        for data in lines:
            if data[-1:] != '\n':
                data += '\n'
            f.write(data)
def about():
    # 创建一个顶级窗口
    about_window = tk.Toplevel(root)
    about_window.title("关于")
    about_window.wm_attributes('-topmost', 1)
    about_window.wm_attributes('-alpha', 0.9)
    tk.Label(about_window, text="关于本程序", font=('宋体', 20, 'bold')).pack()
    tk.Label(about_window, text="本程序由【魂魇桀】制作，完全免费，禁止收费！！！", font=('宋体', 10)).pack()
    tk.Label(about_window, text="", font=('宋体', 10)).pack()
    tk.Label(about_window, text="使用本程序前，请先提供一个可供读写编码为‘UTF-8’的文件", font=('宋体', 10)).pack()
    tk.Label(about_window, text="", font=('宋体', 10)).pack()
    tk.Label(about_window, text="反馈", font=('宋体', 20, 'bold')).pack()
    feedback = tk.StringVar(value='https://www.wjx.cn/vm/mcaTU5k.aspx#')
    tk.Entry(about_window, textvariable=feedback, width=50, state='readonly').pack()
    tk.Button(about_window, text="点击打开网址", width=10, command=lambda: webbrowser.open('https://www.wjx.cn/vm/mcaTU5k.aspx#', new=0)).pack()
    tk.Label(about_window, text="Copyright (c) 2023 魂魇桀(hunyanjie) All rights reserved", font=('宋体', 10, 'bold')).pack()


root = tk.Tk()
root.title("账单程序v1.0  本程序由【魂魇桀】制作，完全免费，禁止收费！！")
select_path = ''
encode = 'UTF-8'
check_selected_date = None
root.wm_attributes('-topmost', 1)
# 创建年份选择框
year_var = tk.StringVar(value=date.today().year)
year = ttk.Combobox(root, textvariable=year_var, state="readonly", width=4)
year['values'] = tuple(map(str, range(1900, 2201)))
year.grid(row=0, column=0)
year.bind("<<ComboboxSelected>>", update_days)
# 创建年份标签
tk.Label(root, text="年").grid(row=0, column=1)
# 创建月份选择框
month_var = tk.StringVar(value=date.today().month)
month = ttk.Combobox(root, textvariable=month_var, state="readonly", width=2)
month['values'] = tuple(map(lambda x: str(x).zfill(2), range(1, 13)))
month.grid(row=0, column=2)
month.bind("<<ComboboxSelected>>", update_days)
# 创建月份标签
tk.Label(root, text="月").grid(row=0, column=3)
# 创建日期选择框
cal_var = tk.StringVar(value=date.today().day)
cal = ttk.Combobox(root, textvariable=cal_var, state="readonly", width=2)
cal.grid(row=0, column=4)
# 创建日期标签
day_label = tk.Label(root, text="日")
day_label.grid(row=0, column=5)
# 初始化日期下拉框的选项
update_days()
# 创建按钮
tk.Button(root, text="选择日期", command=select_date).grid(row=0, column=6)

# 状态栏
status_head = tk.LabelFrame(root, text="状态：")
status = tk.Label(status_head, text="请先选择文件→", fg='magenta')
status.pack()
status_head.grid(row=0, column=8, columnspan=2)

# 文件选择
file_choose_frame = tk.LabelFrame(root, text='文件选择')
file_show = tk.Label(file_choose_frame, text="-*未选择*-", width=16)
file_show.grid(row=0, column=0, columnspan=3)
file_choose_button = tk.Button(file_choose_frame, text="选择文件", command=select_file)
file_choose_button.grid(row=0, column=3, columnspan=1)
file_choose_frame.grid(row=0, column=10, columnspan=4)

# 创建日期输入栏
column_number = 0
column_span_number = 2
tk.Label(root, text="日期").grid(row=1, column=column_number, columnspan=column_span_number)
date_entry = tk.Entry(root, width=10)
date_entry.bind_class('Entry', '<KeyRelease>', status_check)
date_entry.grid(row=2, column=column_number, columnspan=column_span_number)
# 创建支出、收入单选框
column_number = column_number + column_span_number
column_span_number = 3
tk.Label(root, text="金额").grid(row=1, column=column_number, columnspan=column_span_number)
amount_entry = tk.Entry(root, width=12)
amount_entry.grid(row=2, column=column_number, columnspan=column_span_number)
# 创建支付平台栏选择
column_number = column_number + column_span_number
column_span_number = 3
tk.Label(root, text="支付平台").grid(row=1, column=column_number, columnspan=column_span_number)
payment_methods = ["", "支付宝", "微信"]
payment_method_combobox = ttk.Combobox(root, values=payment_methods, width=12)
payment_method_combobox.grid(row=2, column=column_number, columnspan=column_span_number)
payment_method_combobox.bind('<<ComboboxSelected>>', payment_method_select)
# 创建具体支付方式栏
column_number = column_number + column_span_number
column_span_number = 3
tk.Label(root, text="具体支付方式").grid(row=1, column=column_number, columnspan=column_span_number)
specific_payment_method_combobox = ttk.Combobox(root, values=["--请先选择支付方式--"], width=20)
specific_payment_method_combobox.current(0)
specific_payment_method_combobox.grid(row=2, column=column_number, columnspan=column_span_number)
# 创建输入支付平台订单编号栏
column_number = column_number + column_span_number
column_span_number = 3
tk.Label(root, text="支付平台订单编号").grid(row=1, column=column_number, columnspan=column_span_number)
payment_method_order_number_entry = tk.Entry(root)
payment_method_order_number_entry.grid(row=2, column=column_number, columnspan=column_span_number)
# 创建购买平台选择栏
column_number = column_number + column_span_number
column_span_number = 1
tk.Label(root, text="购买平台").grid(row=1, column=column_number, columnspan=column_span_number)
platforms = ["", "朴朴超市", "美团", "抖音", "淘宝", "京东", "饿了么", "拼多多", "永辉网上超市", "闲鱼", "抖阿里巴巴"]
platform_combobox = ttk.Combobox(root, values=platforms, width=12)
platform_combobox.grid(row=2, column=column_number, columnspan=column_span_number)
platform_combobox.bind('<<ComboboxSelected>>', status_check)
# 创建输入购买平台订单编号栏
column_number = column_number + column_span_number
column_span_number = 1
tk.Label(root, text="购买平台订单编号").grid(row=1, column=column_number, columnspan=column_span_number)
platform_order_number_entry = tk.Entry(root)
platform_order_number_entry.bind_class('Entry', '<Return>', save_to_file)
platform_order_number_entry.grid(row=2, column=column_number, columnspan=column_span_number)
# 创建用途输入栏
column_number = column_number + column_span_number
column_span_number = 1
tk.Label(root, text="用途").grid(row=1, column=column_number, columnspan=column_span_number)
purpose = ["", "网上购物", "线下购物", "外卖", "转账", "红包", "餐厅消费", "交通", "旅行", '快递', "生活缴费", "工资",
           "退款", "商家转账"]
purpose_combobox = ttk.Combobox(root, values=purpose, width=12)
purpose_combobox.grid(row=2, column=column_number, columnspan=column_span_number)
purpose_combobox.bind('<<ComboboxSelected>>', purpose_check)
# 创建备注输入栏
column_number = column_number + column_span_number
column_span_number = 1
tk.Label(root, text="备注").grid(row=1, column=column_number, columnspan=column_span_number)
remark_entry = tk.Entry(root)
remark_entry.grid(row=2, column=column_number, columnspan=column_span_number)

column_number = column_number + column_span_number
column_span_number = 1
save_button = tk.Button(root, text="保存", command=save_to_file)
save_button.grid(row=2, column=column_number, columnspan=column_span_number)
column_number = column_number + column_span_number
column_span_number = 1
tk.Button(root, text="清空", command=clear_entries).grid(row=2, column=column_number, columnspan=column_span_number)

tk.Button(root, text="1", command=click_1, width=2).grid(row=3, column=2, columnspan=column_span_number)
tk.Button(root, text="2", command=click_2, width=2).grid(row=3, column=3, columnspan=column_span_number)
tk.Button(root, text="3", command=click_3, width=2).grid(row=3, column=4, columnspan=column_span_number)
tk.Button(root, text="4", command=click_4, width=2).grid(row=4, column=2, columnspan=column_span_number)
tk.Button(root, text="5", command=click_5, width=2).grid(row=4, column=3, columnspan=column_span_number)
tk.Button(root, text="6", command=click_6, width=2).grid(row=4, column=4, columnspan=column_span_number)
tk.Button(root, text="7", command=click_7, width=2).grid(row=5, column=2, columnspan=column_span_number)
tk.Button(root, text="8", command=click_8, width=2).grid(row=5, column=3, columnspan=column_span_number)
tk.Button(root, text="9", command=click_9, width=2).grid(row=5, column=4, columnspan=column_span_number)
tk.Button(root, text="-", command=click_sub, width=2).grid(row=6, column=2, columnspan=column_span_number)
tk.Button(root, text="0", command=click_0, width=2).grid(row=6, column=3, columnspan=column_span_number)
tk.Button(root, text=".", command=click_dot, width=2).grid(row=6, column=4, columnspan=column_span_number)
tk.Button(root, text="←", command=click_del, width=2).grid(row=3, column=5, columnspan=column_span_number)

# 计数Frame
count_label_frame = tk.LabelFrame(root, text="查询")
# 创建年份选择框
frame_year_var = tk.StringVar(value=date.today().year)
frame_year = ttk.Combobox(count_label_frame, textvariable=frame_year_var, state="readonly", width=4)
frame_year['values'] = tuple(map(str, range(1900, 2201)))
frame_year.grid(row=0, column=0)
frame_year.bind("<<ComboboxSelected>>", frame_update_days)
# 创建年份标签
tk.Label(count_label_frame, text="年").grid(row=0, column=1)
# 创建月份选择框
frame_month_var = tk.StringVar(value=date.today().month)
frame_month = ttk.Combobox(count_label_frame, textvariable=frame_month_var, state="readonly", width=2)
frame_month['values'] = tuple(map(lambda x: str(x).zfill(2), range(1, 13)))
frame_month.grid(row=0, column=2)
frame_month.bind("<<ComboboxSelected>>", frame_update_days)
# 创建月份标签
tk.Label(count_label_frame, text="月").grid(row=0, column=3)
# 创建日期选择框
frame_cal_var = tk.StringVar(value=date.today().day)
frame_cal = ttk.Combobox(count_label_frame, textvariable=frame_cal_var, state="readonly", width=2)
frame_cal.grid(row=0, column=4)
# 创建日期标签
frame_day_label = tk.Label(count_label_frame, text="日")
frame_day_label.grid(row=0, column=5)
# 选择范围为月或日
day_month_choose_var = tk.StringVar()
day_month_choose = tk.Checkbutton(count_label_frame, text='整月', variable=day_month_choose_var, onvalue='month',
                                  offvalue='day', command=day_month_check)
day_month_choose.deselect()
day_month_choose.grid(row=0, column=6)
# 初始化日期下拉框的选项
frame_update_days()
# 创建按钮
tk.Button(count_label_frame, text="选择日期", command=select_day_or_month).grid(row=0, column=7)
# 日期
date_label_frame = tk.LabelFrame(count_label_frame, text="日期")
frame_date_show_label = tk.Label(date_label_frame, text="未选择", width=10)
frame_date_show_label.grid(row=0, column=0, columnspan=2)
date_label_frame.grid(row=1, column=0, rowspan=1, columnspan=2)
# 交易总数
trade_times_label_frame = tk.LabelFrame(count_label_frame, text="交易总数")
frame_trade_times_show_label = tk.Label(trade_times_label_frame, text="*请选择日期*", width=8)
frame_trade_times_show_label.grid(row=0, column=0, columnspan=2)
trade_times_label_frame.grid(row=1, column=2, rowspan=1, columnspan=2)
# 总流水
all_money_label_frame = tk.LabelFrame(count_label_frame, text="总流水")
frame_all_money_show_label = tk.Label(all_money_label_frame, text="*请选择日期*", width=8)
frame_all_money_show_label.grid(row=0, column=0, columnspan=2)
all_money_label_frame.grid(row=1, column=4, rowspan=1, columnspan=2)
# 具体交易笔数
trade_info_label_frame = tk.LabelFrame(count_label_frame, text="交易数量详情")
frame_trade_out_times_label = tk.Label(trade_info_label_frame, text="支出笔数：")
frame_trade_out_times_label.grid(row=0, column=0)
frame_trade_out_times_show_label = tk.Label(trade_info_label_frame, text="*请选择日期*", width=8)
frame_trade_out_times_show_label.grid(row=0, column=1, columnspan=2)
frame_trade_info_dec_show_label = tk.Label(trade_info_label_frame, text="|")
frame_trade_info_dec_show_label.grid(row=0, column=3, columnspan=1)
frame_trade_in_times_label = tk.Label(trade_info_label_frame, text="入账笔数：")
frame_trade_in_times_label.grid(row=0, column=4)
frame_trade_in_times_show_label = tk.Label(trade_info_label_frame, text="*请选择日期*", width=8)
frame_trade_in_times_show_label.grid(row=0, column=5, columnspan=2)
trade_info_label_frame.grid(row=2, column=0, rowspan=1, columnspan=7)
# 具体流水
all_money_info_label_frame = tk.LabelFrame(count_label_frame, text="流水详情")
frame_all_money_total_times_label = tk.Label(all_money_info_label_frame, text="盈余：")
frame_all_money_total_times_label.grid(row=0, column=0)
frame_all_money_total_times_show_label = tk.Label(all_money_info_label_frame, text="*请选择日期*", width=8)
frame_all_money_total_times_show_label.grid(row=0, column=1, columnspan=2)
frame_all_money_info_dec_show_label_two = tk.Label(all_money_info_label_frame, text="|")
frame_all_money_info_dec_show_label_two.grid(row=0, column=3)
frame_all_money_out_times_label = tk.Label(all_money_info_label_frame, text="总支出：")
frame_all_money_out_times_label.grid(row=0, column=4)
frame_all_money_out_times_show_label = tk.Label(all_money_info_label_frame, text="*请选择日期*", width=8)
frame_all_money_out_times_show_label.grid(row=0, column=5, columnspan=2)
frame_all_money_info_dec_show_label_one = tk.Label(all_money_info_label_frame, text="|")
frame_all_money_info_dec_show_label_one.grid(row=0, column=7)
frame_all_money_in_times_label = tk.Label(all_money_info_label_frame, text="总入账：")
frame_all_money_in_times_label.grid(row=0, column=8)
frame_all_money_in_times_show_label = tk.Label(all_money_info_label_frame, text="*请选择日期*", width=8)
frame_all_money_in_times_show_label.grid(row=0, column=9, columnspan=2)
all_money_info_label_frame.grid(row=3, column=0, rowspan=1, columnspan=12)
# 账单列表
order_show_frame = tk.Frame(count_label_frame)
order_show_scrollbar_x = tk.Scrollbar(order_show_frame, orient=tk.HORIZONTAL)
order_show_scrollbar_y = tk.Scrollbar(order_show_frame, orient=tk.VERTICAL)
content = tk.StringVar()
content.set('*请选择日期*')
order_show_listbox = tk.Listbox(order_show_frame, listvariable=content, width=80, height=8,
                                xscrollcommand=order_show_scrollbar_x.set, yscrollcommand=order_show_scrollbar_y.set)
order_show_scrollbar_x.config(command=order_show_listbox.xview)
order_show_scrollbar_y.config(command=order_show_listbox.yview)
order_show_scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
order_show_listbox.bind('<Double-1>', amend_choose)
order_show_listbox.pack()
order_show_scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
order_show_frame.grid(row=0, column=13, rowspan=12, columnspan=7)
amend_button = tk.Button(count_label_frame, text="修改", command=amend_choose)
amend_button.grid(row=1, column=8)
# 创建Frame
count_label_frame.grid(row=3, column=6, rowspan=10, columnspan=100)

# 创建一个顶级菜单
menubar = tk.Menu(root)
menubar.add_command(label="关于", command=about)
menubar.add_command(label="退出", command=root.quit)
# 显示菜单
root.config(menu=menubar)

root.wm_attributes('-topmost', 0)
about()

root.mainloop()
