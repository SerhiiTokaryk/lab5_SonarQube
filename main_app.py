import tkinter as tk
from tkinter import messagebox, scrolledtext, filedialog
import threading
import math
import random
import os

from logic import lab1_logic as logic1
from logic import lab2_logic as logic2
from logic import lab3_logic as logic3
from logic import lab4_logic as logic4
from logic import lab5_logic as logic5

COLOR_BG_MAIN = "#ECF0F1"
COLOR_SIDEBAR = "#2C3E50"
COLOR_ACCENT = "#3498DB"
COLOR_BTN_HOVER = "#2980B9"
COLOR_TEXT = "#2C3E50"


class ModernButton(tk.Button):
    def __init__(self, master, hover_color=None, **kwargs):
        self.default_bg = kwargs.get('bg', 'SystemButtonFace')
        self.hover_color = hover_color if hover_color else self.default_bg
        super().__init__(master, **kwargs)
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, e):
        self['bg'] = self.hover_color

    def on_leave(self, e):
        self['bg'] = self.default_bg


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("КСЗІ | Лабораторні роботи")
        self.geometry("900x700")
        self.configure(bg=COLOR_BG_MAIN)

        self.container = tk.Frame(self, bg=COLOR_BG_MAIN)
        self.container.pack(fill="both", expand=True)

        self.frames = {}

        for F in (StartPage, Lab1Page, Lab2Page, Lab3Page, Lab4Page, Lab5Page):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=COLOR_BG_MAIN)
        self.controller = controller

        center_frame = tk.Frame(self, bg=COLOR_BG_MAIN)
        center_frame.place(relx=0.5, rely=0.5, anchor="center")

        lbl_title = tk.Label(center_frame, text="Комплексна система захисту інформації",
                             font=("Segoe UI", 24, "bold"), bg=COLOR_BG_MAIN, fg=COLOR_TEXT)
        lbl_title.pack(pady=(0, 10))

        lbl_subtitle = tk.Label(center_frame, text="Оберіть лабораторну роботу:",
                                font=("Segoe UI", 14), bg=COLOR_BG_MAIN, fg="#7F8C8D")
        lbl_subtitle.pack(pady=(0, 30))

        labs = [
            ("Лабораторна №1: ГПВЧ", "Lab1Page"),
            ("Лабораторна №2: Хешування MD5", "Lab2Page"),
            ("Лабораторна №3: Шифрування RC5", "Lab3Page"),
            ("Лабораторна №4: Шифрування RSA", "Lab4Page"),
            ("Лабораторна №5: Цифровий підпис DSS", "Lab5Page"),
        ]

        for text, page_name in labs:
            state = "normal" if page_name else "disabled"
            bg_color = COLOR_SIDEBAR if page_name else "#95A5A6"

            btn = ModernButton(center_frame, text=text, font=("Segoe UI", 12),
                               bg=bg_color, fg="white", hover_color=COLOR_BTN_HOVER,
                               width=40, height=2, bd=0, state=state,
                               command=lambda p=page_name: controller.show_frame(p) if p else None)
            btn.pack(pady=10)

        btn_exit = ModernButton(center_frame, text="Вихід", font=("Segoe UI", 12, "bold"),
                                bg="#C0392B", fg="white", hover_color="#E74C3C",
                                width=40, height=2, bd=0, command=controller.quit)
        btn_exit.pack(pady=(30, 0))


class Lab1Page(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=COLOR_BG_MAIN)
        self.controller = controller

        header = tk.Frame(self, bg="white", height=60)
        header.pack(fill="x")

        btn_back = ModernButton(header, text="⬅ Назад", bg="#95A5A6", fg="white",
                                font=("Segoe UI", 10, "bold"), bd=0, hover_color="#7F8C8D",
                                command=lambda: controller.show_frame("StartPage"))
        btn_back.pack(side="left", padx=10, pady=10)

        lbl_header = tk.Label(header, text="Лабораторна робота №1: Генератор (LCG) та Тест Чезаро",
                              font=("Segoe UI", 14, "bold"), bg="white", fg=COLOR_TEXT)
        lbl_header.pack(side="left", padx=20)

        content = tk.Frame(self, bg=COLOR_BG_MAIN)
        content.pack(fill="both", expand=True, padx=20, pady=20)

        param_frame = tk.LabelFrame(content, text=" Параметри генерації ", font=("Segoe UI", 11, "bold"),
                                    bg=COLOR_BG_MAIN, fg=COLOR_TEXT)
        param_frame.pack(fill="x", pady=5)

        self.entries = {}
        params = [
            ("Модуль (m)", logic1.DEFAULT_M),
            ("Множник (a)", logic1.DEFAULT_A),
            ("Приріст (c)", logic1.DEFAULT_C),
            ("Початкове (X0)", logic1.DEFAULT_X0),
            ("Кількість (N)", logic1.DEFAULT_COUNT)
        ]

        grid_frame = tk.Frame(param_frame, bg=COLOR_BG_MAIN)
        grid_frame.pack(fill="x", padx=10, pady=10)

        for i, (label_text, default_val) in enumerate(params):
            f = tk.Frame(grid_frame, bg=COLOR_BG_MAIN)
            f.pack(side="left", expand=True, fill="x", padx=5)
            tk.Label(f, text=label_text, bg=COLOR_BG_MAIN, font=("Segoe UI", 9)).pack(anchor="w")
            ent = tk.Entry(f, font=("Consolas", 11), bd=1, relief="solid")
            ent.insert(0, str(default_val))
            ent.pack(fill="x", ipady=3)
            self.entries[label_text] = ent

        btn_frame = tk.Frame(content, bg=COLOR_BG_MAIN)
        btn_frame.pack(fill="x", pady=15)

        self.btn_gen = ModernButton(btn_frame, text="▶ Згенерувати та Тестувати", bg="#27AE60",
                                    hover_color="#2ECC71", fg="white", font=("Segoe UI", 11, "bold"),
                                    bd=0, command=self.run_generation)
        self.btn_gen.pack(side="left", padx=(0, 10), ipady=8, ipadx=20)

        self.btn_period = ModernButton(btn_frame, text="⏱ Знайти період", bg="#E67E22",
                                       hover_color="#D35400", fg="white", font=("Segoe UI", 11, "bold"),
                                       bd=0, command=self.start_period_thread)
        self.btn_period.pack(side="left", padx=10, ipady=8, ipadx=20)

        self.output_area = scrolledtext.ScrolledText(content, font=("Consolas", 10), height=15,
                                                     bd=1, relief="solid")
        self.output_area.pack(fill="both", expand=True, pady=10)

    def get_params(self):
        try:
            m = int(self.entries["Модуль (m)"].get())
            a = int(self.entries["Множник (a)"].get())
            c = int(self.entries["Приріст (c)"].get())
            x0 = int(self.entries["Початкове (X0)"].get())
            count = int(self.entries["Кількість (N)"].get())

            if m <= 0 or count <= 0: raise ValueError
            return m, a, c, x0, count
        except ValueError:
            messagebox.showerror("Помилка", "Введіть коректні цілі числа (>0).")
            return None

    def run_generation(self):
        params = self.get_params()
        if not params: return
        m, a, c, x0, count = params

        self.output_area.delete(1.0, tk.END)
        self.output_area.insert(tk.END, f"⏳ Генерація {count} чисел та виконання тесту Чезаро...\n")
        self.update()

        try:
            my_nums = logic1.lcg_generator(x0, a, c, m, count)
            sys_nums = [random.randint(0, m) for _ in range(count)]

            pi_my = logic1.cesaro_test(my_nums)
            pi_sys = logic1.cesaro_test(sys_nums)
            pi_real = math.pi

            res = ""
            res += f"Вхідні параметри:\n m = {m}\n a = {a}\n c = {c}\n X0 = {x0}\n Кількість (N) = {count}\n"
            res += "-" * 50 + "\n"

            res += "1. Згенерована послідовність(10):\n"
            res += f"   {my_nums[:10]} ...\n\n"

            res += "2. Результати статистичного тестування:\n"
            res += f"   Еталонне значення Pi: {pi_real:.6f}\n"
            res += f"   -> Мій генератор:     {pi_my:.6f} (Похибка: {abs(pi_real - pi_my):.6f})\n"
            res += f"   -> Random:     {pi_sys:.6f} (Похибка: {abs(pi_real - pi_sys):.6f})\n"

            res += "\n3. Висновок:\n"
            if abs(pi_real - pi_my) < 0.15:
                res += "   Генератор пройшов перевірку на рівномірність (допустима похибка).\n"
            else:
                res += "   Висока похибка. Параметри можуть бути невдалими або вибірка замала.\n"

            self.output_area.insert(tk.END, res)

            with open("lab1_results.txt", "w", encoding="utf-8") as f:
                f.write(res)
                f.write("\n\nПОВНИЙ СПИСОК ЧИСЕЛ\n")
                f.write(str(my_nums))

            messagebox.showinfo("Успіх", "Результати розраховані та збережені у 'lab1_results.txt'")

        except Exception as e:
            self.output_area.insert(tk.END, f"\n Критична помилка: {e}")

    def start_period_thread(self):
        params = self.get_params()
        if not params: return

        self.btn_period.config(state="disabled", text=" Рахуємо...", bg="#95a5a6")
        self.output_area.insert(tk.END, "\nАналіз періоду генератора\nЗапущено пошук...\n")

        thread = threading.Thread(target=self.bg_period_task, args=(params,))
        thread.daemon = True
        thread.start()

    def bg_period_task(self, params):
        m, a, c, x0, count = params
        try:
            period = logic1.find_period_floyd(x0, a, c, m)
            self.after(0, lambda: self.on_period_found(period, m))
        except Exception as e:
            self.after(0, lambda: self.output_area.insert(tk.END, f"Помилка потоку: {e}\n"))

    def on_period_found(self, period, m):
        msg = f"Знайдений період: {period}\n"

        msg += "Висновок щодо періоду: "
        if period >= m - 1:
            msg += "Максимальний період. Відмінно для LCG.\n"
        elif period > 100000:
            msg += "Великий період. Придатний для простих задач.\n"
        else:
            msg += "Критично малий період. НЕ придатний для криптографії.\n"

        self.output_area.insert(tk.END, msg)
        self.output_area.see(tk.END)
        self.btn_period.config(state="normal", text="⏱ Знайти період", bg="#E67E22")
        messagebox.showinfo("Період знайдено", f"Період: {period}")


class Lab2Page(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=COLOR_BG_MAIN)
        self.controller = controller

        header = tk.Frame(self, bg="white", height=60)
        header.pack(fill="x")

        btn_back = ModernButton(header, text="⬅ Назад", bg="#95A5A6", fg="white",
                                font=("Segoe UI", 10, "bold"), bd=0, hover_color="#7F8C8D",
                                command=lambda: controller.show_frame("StartPage"))
        btn_back.pack(side="left", padx=10, pady=10)

        lbl_header = tk.Label(header, text="Лабораторна робота №2: Алгоритм хешування MD5",
                              font=("Segoe UI", 14, "bold"), bg="white", fg=COLOR_TEXT)
        lbl_header.pack(side="left", padx=20)

        content = tk.Frame(self, bg=COLOR_BG_MAIN)
        content.pack(fill="both", expand=True, padx=20, pady=20)

        str_frame = tk.LabelFrame(content, text=" Хешування рядка ", font=("Segoe UI", 11, "bold"),
                                  bg=COLOR_BG_MAIN, fg=COLOR_TEXT)
        str_frame.pack(fill="x", pady=5)

        tk.Label(str_frame, text="Введіть текст:", bg=COLOR_BG_MAIN).pack(side="left", padx=10, pady=10)
        self.str_entry = tk.Entry(str_frame, font=("Consolas", 11), width=50)
        self.str_entry.pack(side="left", padx=10, pady=10, expand=True, fill="x")

        ModernButton(str_frame, text="Хешувати текст", bg=COLOR_ACCENT, fg="white", hover_color=COLOR_BTN_HOVER,
                     font=("Segoe UI", 10, "bold"), command=self.hash_string_action).pack(side="right", padx=10)

        btn_frame = tk.Frame(content, bg=COLOR_BG_MAIN)
        btn_frame.pack(fill="x", pady=10)

        ModernButton(btn_frame, text="📄 Хешувати файл", bg="#8E44AD", fg="white", hover_color="#9B59B6",
                     font=("Segoe UI", 10, "bold"), width=20, command=self.hash_file_action).pack(side="left", padx=5)

        ModernButton(btn_frame, text="🛡 Перевірити цілісність", bg="#E67E22", fg="white", hover_color="#D35400",
                     font=("Segoe UI", 10, "bold"), width=20, command=self.check_integrity_action).pack(side="left",
                                                                                                        padx=5)

        ModernButton(btn_frame, text="⚙ Запустити тести RFC 1321", bg="#27AE60", fg="white", hover_color="#2ECC71",
                     font=("Segoe UI", 10, "bold"), width=25, command=self.run_rfc_tests).pack(side="right", padx=5)

        self.output_area = scrolledtext.ScrolledText(content, font=("Consolas", 11), height=15, bd=1, relief="solid")
        self.output_area.pack(fill="both", expand=True, pady=10)

        ModernButton(content, text="💾 Зберегти результати", bg=COLOR_SIDEBAR, fg="white",
                     font=("Segoe UI", 10, "bold"), command=self.save_results).pack(anchor="e")

    def log(self, msg, clear=False):
        if clear:
            self.output_area.delete(1.0, tk.END)
        self.output_area.insert(tk.END, msg + "\n")
        self.output_area.see(tk.END)

    def hash_string_action(self):
        text = self.str_entry.get()
        if not text:
            messagebox.showwarning("Увага", "Введіть текст для хешування!")
            return

        res = logic2.md5_string(text)
        self.log(f"--- Хешування рядка ---", clear=True)
        self.log(f"Вхід: '{text}'")
        self.log(f"MD5:  {res}\n")

    def hash_file_action(self):
        filepath = filedialog.askopenfilename(title="Оберіть файл для хешування")
        if not filepath:
            return

        self.log(f"--- Хешування файлу ---", clear=True)
        self.log(f"Файл: {os.path.basename(filepath)}")
        self.log("Обчислення...")
        self.update()

        def task():
            try:
                res = logic2.md5_file(filepath)
                self.after(0, lambda: self.log(f"MD5:  {res}\n"))
            except Exception as e:
                self.after(0, lambda: messagebox.showerror("Помилка", str(e)))

        threading.Thread(target=task, daemon=True).start()

    def check_integrity_action(self):
        messagebox.showinfo("Інструкція", "Спочатку оберіть цільовий файл, а потім .txt файл з його хешем.")

        target_file = filedialog.askopenfilename(title="Крок 1: Оберіть файл для перевірки")
        if not target_file: return

        hash_file = filedialog.askopenfilename(title="Крок 2: Оберіть .txt файл з хешем",
                                               filetypes=[("Text files", "*.txt")])
        if not hash_file: return

        self.log(f"--- Перевірка цілісності ---", clear=True)
        self.log(f"Файл: {os.path.basename(target_file)}")
        self.log(f"Хеш-файл: {os.path.basename(hash_file)}")
        self.update()

        def task():
            try:
                is_valid, actual, expected = logic2.check_integrity(target_file, hash_file)
                msg = f"\nФактичний хеш:  {actual}\nОчікуваний хеш: {expected}\n"
                if is_valid:
                    msg += "✅ Результат: ЦІЛІСНІСТЬ ПІДТВЕРДЖЕНО\n"
                else:
                    msg += "❌ Результат: ЦІЛІСНІСТЬ ПОРУШЕНО\n"
                self.after(0, lambda: self.log(msg))
            except Exception as e:
                self.after(0, lambda: messagebox.showerror("Помилка", str(e)))

        threading.Thread(target=task, daemon=True).start()

    def run_rfc_tests(self):
        self.log("--- Запуск тестових векторів RFC 1321 ---", clear=True)
        passed_all = True

        for msg, expected in logic2.RFC_1321_TESTS.items():
            actual = logic2.md5_string(msg)
            status = "✅ OK" if actual == expected else "❌ FAIL"
            if actual != expected: passed_all = False

            display_msg = msg if len(msg) < 30 else msg[:27] + "..."
            self.log(f"Повідомлення: '{display_msg}'\nОчікувано: {expected}\nФактично:  {actual}\nСтатус: {status}\n")

        if passed_all:
            self.log("Всі тести RFC 1321 пройдено успішно! Алгоритм працює правильно.")

    def save_results(self):
        content = self.output_area.get(1.0, tk.END).strip()
        if not content:
            messagebox.showwarning("Увага", "Немає результатів для збереження.")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                 title="Зберегти результати",
                                                 filetypes=[("Text files", "*.txt")])
        if file_path:
            try:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(content)
                messagebox.showinfo("Успіх", "Результати успішно збережено!")
            except Exception as e:
                messagebox.showerror("Помилка", f"Не вдалося зберегти файл:\n{e}")


class Lab3Page(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=COLOR_BG_MAIN)
        self.controller = controller

        header = tk.Frame(self, bg="white", height=60)
        header.pack(fill="x")

        btn_back = ModernButton(header, text="⬅ Назад", bg="#95A5A6", fg="white",
                                font=("Segoe UI", 10, "bold"), bd=0, hover_color="#7F8C8D",
                                command=lambda: controller.show_frame("StartPage"))
        btn_back.pack(side="left", padx=10, pady=10)

        lbl_header = tk.Label(header, text="Лабораторна робота №3: RC5 (CBC-Pad)",
                              font=("Segoe UI", 14, "bold"), bg="white", fg=COLOR_TEXT)
        lbl_header.pack(side="left", padx=20)

        content = tk.Frame(self, bg=COLOR_BG_MAIN)
        content.pack(fill="both", expand=True, padx=20, pady=20)

        pass_frame = tk.LabelFrame(content, text=" Налаштування ключа ", font=("Segoe UI", 11, "bold"),
                                   bg=COLOR_BG_MAIN, fg=COLOR_TEXT)
        pass_frame.pack(fill="x", pady=5)

        tk.Label(pass_frame, text="Парольна фраза:", bg=COLOR_BG_MAIN).pack(side="left", padx=10, pady=10)
        self.pass_entry = tk.Entry(pass_frame, font=("Consolas", 11), width=40, show="*")
        self.pass_entry.pack(side="left", padx=10, pady=10)

        btn_frame = tk.Frame(content, bg=COLOR_BG_MAIN)
        btn_frame.pack(fill="x", pady=15)

        ModernButton(btn_frame, text="🔒 Зашифрувати файл", bg="#E74C3C", fg="white", hover_color="#C0392B",
                     font=("Segoe UI", 11, "bold"), width=25, command=self.encrypt_action).pack(side="left", padx=10)

        ModernButton(btn_frame, text="🔓 Розшифрувати файл", bg="#2ECC71", fg="white", hover_color="#27AE60",
                     font=("Segoe UI", 11, "bold"), width=25, command=self.decrypt_action).pack(side="left", padx=10)

        self.output_area = scrolledtext.ScrolledText(content, font=("Consolas", 10), height=15, bd=1, relief="solid")
        self.output_area.pack(fill="both", expand=True, pady=10)

    def log(self, msg):
        self.output_area.insert(tk.END, msg + "\n")
        self.output_area.see(tk.END)

    def encrypt_action(self):
        password = self.pass_entry.get()
        if not password:
            messagebox.showwarning("Увага", "Введіть парольну фразу!")
            return

        input_path = filedialog.askopenfilename(title="Оберіть файл для шифрування")
        if not input_path: return

        output_path = filedialog.asksaveasfilename(title="Зберегти зашифрований файл як",
                                                   defaultextension=".enc")
        if not output_path: return

        self.log(f"--- Шифрування ---")
        self.log(f"Файл: {os.path.basename(input_path)}")
        self.log("Процес пішов, зачекайте...")
        self.update()

        def task():
            try:
                logic3.rc5_encrypt_file(input_path, output_path, password)
                self.after(0, lambda: self.log("✅ Успішно зашифровано!\n"))
            except Exception as e:
                self.after(0, lambda: messagebox.showerror("Помилка", str(e)))

        threading.Thread(target=task, daemon=True).start()

    def decrypt_action(self):
        password = self.pass_entry.get()
        if not password:
            messagebox.showwarning("Увага", "Введіть парольну фразу!")
            return

        input_path = filedialog.askopenfilename(title="Оберіть зашифрований файл")
        if not input_path: return

        output_path = filedialog.asksaveasfilename(title="Зберегти розшифрований файл як")
        if not output_path: return

        self.log(f"--- Дешифрування ---")
        self.log(f"Файл: {os.path.basename(input_path)}")
        self.log("Розшифровуємо...")
        self.update()

        def task():
            try:
                logic3.rc5_decrypt_file(input_path, output_path, password)
                self.after(0, lambda: self.log("✅ Успішно розшифровано!\n"))
            except Exception as e:
                self.after(0, lambda: messagebox.showerror("Помилка",
                                                           f"Помилка дешифрування: {e}\n(Можливо, невірний пароль)"))
                self.after(0, lambda: self.log("❌ Помилка розшифрування.\n"))

        threading.Thread(target=task, daemon=True).start()


class Lab4Page(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=COLOR_BG_MAIN)
        self.controller = controller

        self.public_key = None
        self.private_key = None

        header = tk.Frame(self, bg="white", height=60)
        header.pack(fill="x")

        btn_back = ModernButton(header, text="⬅ Назад", bg="#95A5A6", fg="white",
                                font=("Segoe UI", 10, "bold"), bd=0, hover_color="#7F8C8D",
                                command=lambda: controller.show_frame("StartPage"))
        btn_back.pack(side="left", padx=10, pady=10)

        lbl_header = tk.Label(header, text="Лабораторна робота №4: RSA",
                              font=("Segoe UI", 14, "bold"), bg="white", fg=COLOR_TEXT)
        lbl_header.pack(side="left", padx=20)

        content = tk.Frame(self, bg=COLOR_BG_MAIN)
        content.pack(fill="both", expand=True, padx=20, pady=20)

        key_frame = tk.LabelFrame(content, text=" Керування ключами RSA ", font=("Segoe UI", 11, "bold"),
                                  bg=COLOR_BG_MAIN, fg=COLOR_TEXT)
        key_frame.pack(fill="x", pady=5)

        btn_key_frame = tk.Frame(key_frame, bg=COLOR_BG_MAIN)
        btn_key_frame.pack(fill="x", pady=10)

        ModernButton(btn_key_frame, text="🔑 Згенерувати нові ключі", bg="#8E44AD", fg="white", hover_color="#9B59B6",
                     font=("Segoe UI", 10, "bold"), width=25, command=self.generate_keys_action).pack(side="left",
                                                                                                      padx=10)

        ModernButton(btn_key_frame, text="📂 Завантажити Public Key", bg="#34495E", fg="white", hover_color="#2C3E50",
                     font=("Segoe UI", 10, "bold"), width=25, command=self.load_public_action).pack(side="left",
                                                                                                    padx=10)

        ModernButton(btn_key_frame, text="📂 Завантажити Private Key", bg="#34495E", fg="white", hover_color="#2C3E50",
                     font=("Segoe UI", 10, "bold"), width=25, command=self.load_private_action).pack(side="left",
                                                                                                     padx=10)

        self.lbl_key_status = tk.Label(key_frame, text="Ключі не завантажено", bg=COLOR_BG_MAIN, fg="#E74C3C",
                                       font=("Segoe UI", 10, "bold"))
        self.lbl_key_status.pack(pady=(0, 10))

        action_frame = tk.Frame(content, bg=COLOR_BG_MAIN)
        action_frame.pack(fill="x", pady=15)

        ModernButton(action_frame, text="🔒 Зашифрувати файл", bg="#E74C3C", fg="white", hover_color="#C0392B",
                     font=("Segoe UI", 11, "bold"), width=25, command=self.encrypt_action).pack(side="left", padx=10)

        ModernButton(action_frame, text="🔓 Розшифрувати файл", bg="#2ECC71", fg="white", hover_color="#27AE60",
                     font=("Segoe UI", 11, "bold"), width=25, command=self.decrypt_action).pack(side="left", padx=10)

        self.output_area = scrolledtext.ScrolledText(content, font=("Consolas", 10), height=12, bd=1, relief="solid")
        self.output_area.pack(fill="both", expand=True, pady=10)

    def log(self, msg):
        self.output_area.insert(tk.END, msg + "\n")
        self.output_area.see(tk.END)

    def update_key_status(self):
        status = []
        if self.public_key: status.append("Public: OK")
        if self.private_key: status.append("Private: OK")

        if not status:
            self.lbl_key_status.config(text="Ключі не завантажено", fg="#E74C3C")
        else:
            self.lbl_key_status.config(text=" | ".join(status), fg="#27AE60")

    def generate_keys_action(self):
        dir_path = filedialog.askdirectory(title="Оберіть папку для збереження ключів")
        if not dir_path: return

        self.log("Генерація ключів (2048 біт)... Зачекайте.")
        self.update()

        def task():
            try:
                priv, pub = logic4.generate_keys(2048)
                priv_path = os.path.join(dir_path, "private.pem")
                pub_path = os.path.join(dir_path, "public.pem")

                logic4.save_private_key(priv, priv_path)
                logic4.save_public_key(pub, pub_path)

                self.private_key = priv
                self.public_key = pub

                self.after(0, lambda: self.log(f"✅ Ключі згенеровано та збережено в:\n{dir_path}\n"))
                self.after(0, self.update_key_status)
            except Exception as e:
                self.after(0, lambda: messagebox.showerror("Помилка", str(e)))

        threading.Thread(target=task, daemon=True).start()

    def load_public_action(self):
        filepath = filedialog.askopenfilename(title="Оберіть Public Key (PEM)",
                                              filetypes=[("PEM Files", "*.pem"), ("All Files", "*.*")])
        if not filepath: return
        try:
            self.public_key = logic4.load_public_key(filepath)
            self.log(f"Завантажено Public Key: {os.path.basename(filepath)}")
            self.update_key_status()
        except Exception as e:
            messagebox.showerror("Помилка", f"Не вдалося завантажити ключ:\n{e}")

    def load_private_action(self):
        filepath = filedialog.askopenfilename(title="Оберіть Private Key (PEM)",
                                              filetypes=[("PEM Files", "*.pem"), ("All Files", "*.*")])
        if not filepath: return
        try:
            self.private_key = logic4.load_private_key(filepath)
            self.log(f"Завантажено Private Key: {os.path.basename(filepath)}")
            self.update_key_status()
        except Exception as e:
            messagebox.showerror("Помилка", f"Не вдалося завантажити ключ:\n{e}")

    def encrypt_action(self):
        if not self.public_key:
            messagebox.showwarning("Увага", "Спочатку завантажте або згенеруйте Public Key!")
            return

        input_path = filedialog.askopenfilename(title="Оберіть файл для шифрування")
        if not input_path: return

        output_path = filedialog.asksaveasfilename(title="Зберегти зашифрований файл як", defaultextension=".enc")
        if not output_path: return

        self.log(f"--- Шифрування RSA ---")
        self.log(f"Файл: {os.path.basename(input_path)}")
        self.log("Процес пішов, зачекайте...")
        self.update()

        def task():
            try:
                logic4.rsa_encrypt_file(input_path, output_path, self.public_key)
                self.after(0, lambda: self.log("✅ Успішно зашифровано!\n"))
            except Exception as e:
                self.after(0, lambda: messagebox.showerror("Помилка", str(e)))

        threading.Thread(target=task, daemon=True).start()

    def decrypt_action(self):
        if not self.private_key:
            messagebox.showwarning("Увага", "Спочатку завантажте або згенеруйте Private Key!")
            return

        input_path = filedialog.askopenfilename(title="Оберіть зашифрований файл")
        if not input_path: return

        output_path = filedialog.asksaveasfilename(title="Зберегти розшифрований файл як")
        if not output_path: return

        self.log(f"--- Дешифрування RSA ---")
        self.log(f"Файл: {os.path.basename(input_path)}")
        self.log("Розшифровуємо...")
        self.update()

        def task():
            try:
                logic4.rsa_decrypt_file(input_path, output_path, self.private_key)
                self.after(0, lambda: self.log("✅ Успішно розшифровано!\n"))
            except Exception as e:
                self.after(0, lambda: messagebox.showerror("Помилка", f"Помилка дешифрування: {e}"))
                self.after(0, lambda: self.log("❌ Помилка розшифрування.\n"))

        threading.Thread(target=task, daemon=True).start()


class Lab5Page(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=COLOR_BG_MAIN)
        self.controller = controller

        self.public_key = None
        self.private_key = None

        header = tk.Frame(self, bg="white", height=60)
        header.pack(fill="x")

        btn_back = ModernButton(header, text="⬅ Назад", bg="#95A5A6", fg="white",
                                font=("Segoe UI", 10, "bold"), bd=0, hover_color="#7F8C8D",
                                command=lambda: controller.show_frame("StartPage"))
        btn_back.pack(side="left", padx=10, pady=10)

        lbl_header = tk.Label(header, text="Лабораторна робота №5: Цифровий підпис (DSS/DSA)",
                              font=("Segoe UI", 14, "bold"), bg="white", fg=COLOR_TEXT)
        lbl_header.pack(side="left", padx=20)

        content = tk.Frame(self, bg=COLOR_BG_MAIN)
        content.pack(fill="both", expand=True, padx=20, pady=20)

        # Фрейм керування ключами
        key_frame = tk.LabelFrame(content, text=" Керування ключами DSA ", font=("Segoe UI", 11, "bold"),
                                  bg=COLOR_BG_MAIN, fg=COLOR_TEXT)
        key_frame.pack(fill="x", pady=5)

        btn_key_frame = tk.Frame(key_frame, bg=COLOR_BG_MAIN)
        btn_key_frame.pack(fill="x", pady=10)

        ModernButton(btn_key_frame, text="🔑 Згенерувати ключі", bg="#8E44AD", fg="white", hover_color="#9B59B6",
                     font=("Segoe UI", 10, "bold"), width=20, command=self.generate_keys_action).pack(side="left",
                                                                                                      padx=5)

        ModernButton(btn_key_frame, text="📂 Завантажити Public", bg="#34495E", fg="white", hover_color="#2C3E50",
                     font=("Segoe UI", 10, "bold"), width=20, command=self.load_public_action).pack(side="left", padx=5)

        ModernButton(btn_key_frame, text="📂 Завантажити Private", bg="#34495E", fg="white", hover_color="#2C3E50",
                     font=("Segoe UI", 10, "bold"), width=20, command=self.load_private_action).pack(side="left",
                                                                                                     padx=5)

        self.lbl_key_status = tk.Label(key_frame, text="Ключі не завантажено", bg=COLOR_BG_MAIN, fg="#E74C3C",
                                       font=("Segoe UI", 10, "bold"))
        self.lbl_key_status.pack(pady=(0, 10))

        # Фрейм підпису
        action_frame = tk.Frame(content, bg=COLOR_BG_MAIN)
        action_frame.pack(fill="x", pady=10)

        tk.Label(action_frame, text="Текст:", bg=COLOR_BG_MAIN, font=("Segoe UI", 10)).pack(side="left")
        self.text_entry = tk.Entry(action_frame, font=("Consolas", 11), width=30)
        self.text_entry.pack(side="left", padx=10)

        ModernButton(action_frame, text="✍ Підписати текст", bg="#2980B9", fg="white", hover_color="#3498DB",
                     font=("Segoe UI", 10, "bold"), command=self.sign_string_action).pack(side="left", padx=5)

        ModernButton(action_frame, text="📄 Підписати файл", bg="#E67E22", fg="white", hover_color="#D35400",
                     font=("Segoe UI", 10, "bold"), command=self.sign_file_action).pack(side="left", padx=5)

        ModernButton(action_frame, text="🛡 Перевірити файл", bg="#27AE60", fg="white", hover_color="#2ECC71",
                     font=("Segoe UI", 10, "bold"), command=self.verify_file_action).pack(side="right", padx=5)

        self.output_area = scrolledtext.ScrolledText(content, font=("Consolas", 10), height=12, bd=1, relief="solid")
        self.output_area.pack(fill="both", expand=True, pady=10)

    def log(self, msg, clear=False):
        if clear:
            self.output_area.delete(1.0, tk.END)
        self.output_area.insert(tk.END, msg + "\n")
        self.output_area.see(tk.END)

    def update_key_status(self):
        status = []
        if self.public_key: status.append("Public: OK")
        if self.private_key: status.append("Private: OK")

        if not status:
            self.lbl_key_status.config(text="Ключі не завантажено", fg="#E74C3C")
        else:
            self.lbl_key_status.config(text=" | ".join(status), fg="#27AE60")

    def generate_keys_action(self):
        dir_path = filedialog.askdirectory(title="Оберіть папку для збереження ключів DSA")
        if not dir_path: return

        self.log("Генерація ключів DSA (2048 біт)...", clear=True)
        self.update()

        def task():
            try:
                priv, pub = logic5.generate_dsa_keys(2048)
                priv_path = os.path.join(dir_path, "dsa_private.pem")
                pub_path = os.path.join(dir_path, "dsa_public.pem")

                logic5.save_private_key(priv, priv_path)
                logic5.save_public_key(pub, pub_path)

                self.private_key = priv
                self.public_key = pub

                self.after(0, lambda: self.log(f"✅ Ключі згенеровано та збережено в:\n{dir_path}\n"))
                self.after(0, self.update_key_status)
            except Exception as e:
                self.after(0, lambda: messagebox.showerror("Помилка", str(e)))

        threading.Thread(target=task, daemon=True).start()

    def load_public_action(self):
        filepath = filedialog.askopenfilename(title="Оберіть Public Key (PEM)",
                                              filetypes=[("PEM Files", "*.pem"), ("All Files", "*.*")])
        if not filepath: return
        try:
            self.public_key = logic5.load_public_key(filepath)
            self.log(f"Завантажено Public Key: {os.path.basename(filepath)}")
            self.update_key_status()
        except Exception as e:
            messagebox.showerror("Помилка", f"Не вдалося завантажити ключ:\n{e}")

    def load_private_action(self):
        filepath = filedialog.askopenfilename(title="Оберіть Private Key (PEM)",
                                              filetypes=[("PEM Files", "*.pem"), ("All Files", "*.*")])
        if not filepath: return
        try:
            self.private_key = logic5.load_private_key(filepath)
            self.log(f"Завантажено Private Key: {os.path.basename(filepath)}")
            self.update_key_status()
        except Exception as e:
            messagebox.showerror("Помилка", f"Не вдалося завантажити ключ:\n{e}")

    def sign_string_action(self):
        if not self.private_key:
            messagebox.showwarning("Увага", "Для підпису потрібен Private Key!")
            return

        text = self.text_entry.get()
        if not text:
            messagebox.showwarning("Увага", "Введіть текст для підпису!")
            return

        self.log("--- Підпис рядка ---", clear=True)
        try:
            sig_hex = logic5.sign_string(self.private_key, text)
            self.log(f"Текст: '{text}'\nПідпис (HEX):\n{sig_hex}\n")
        except Exception as e:
            messagebox.showerror("Помилка", str(e))

    def sign_file_action(self):
        if not self.private_key:
            messagebox.showwarning("Увага", "Для підпису потрібен Private Key!")
            return

        filepath = filedialog.askopenfilename(title="Оберіть файл для підпису")
        if not filepath: return

        sig_path = filedialog.asksaveasfilename(title="Зберегти підпис як", defaultextension=".sig")
        if not sig_path: return

        self.log(f"--- Підпис файлу ---", clear=True)
        self.log(f"Файл: {os.path.basename(filepath)}")
        self.log("Обчислення підпису...")
        self.update()

        def task():
            try:
                sig_hex = logic5.sign_file(self.private_key, filepath)
                with open(sig_path, 'w') as f:
                    f.write(sig_hex)
                self.after(0, lambda: self.log(f"✅ Успіх! Підпис збережено у:\n{sig_path}\n"))
            except Exception as e:
                self.after(0, lambda: messagebox.showerror("Помилка", str(e)))

        threading.Thread(target=task, daemon=True).start()

    def verify_file_action(self):
        if not self.public_key:
            messagebox.showwarning("Увага", "Для перевірки потрібен Public Key!")
            return

        messagebox.showinfo("Інструкція",
                            "Крок 1: Оберіть файл, який треба перевірити.\nКрок 2: Оберіть .sig файл з його підписом.")

        filepath = filedialog.askopenfilename(title="Крок 1: Оберіть файл для перевірки")
        if not filepath: return

        sig_path = filedialog.askopenfilename(title="Крок 2: Оберіть файл підпису (.sig)",
                                              filetypes=[("Signature Files", "*.sig"), ("All Files", "*.*")])
        if not sig_path: return

        self.log(f"--- Перевірка підпису ---", clear=True)
        self.log(f"Файл: {os.path.basename(filepath)}")
        self.log(f"Підпис: {os.path.basename(sig_path)}")
        self.update()

        def task():
            try:
                with open(sig_path, 'r') as f:
                    sig_hex = f.read().strip()

                is_valid = logic5.verify_file(self.public_key, filepath, sig_hex)
                if is_valid:
                    self.after(0, lambda: self.log("✅ Результат: ПІДПИС ДІЙСНИЙ\n"))
                else:
                    self.after(0,
                               lambda: self.log("❌ Результат: ПІДПИС НЕ ДІЙСНИЙ\n"))
            except Exception as e:
                self.after(0, lambda: messagebox.showerror("Помилка", f"Помилка перевірки:\n{e}"))

        threading.Thread(target=task, daemon=True).start()

if __name__ == "__main__":
    app = App()
    app.mainloop()