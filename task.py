import tkinter as tk
from tkinter import messagebox, ttk, simpledialog
import json
import os
from datetime import datetime

TASK_FILE = "tasks.json"

def load_tasks():
    if os.path.exists(TASK_FILE):
        with open(TASK_FILE, "r") as file:
            return json.load(file)
    return []

def save_tasks():
    with open(TASK_FILE, "w") as file:
        json.dump(tasks, file, indent=4)

class TaskManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Task Manager")
        self.root.geometry("600x500")
        
        # Initialize tasks
        self.tasks = load_tasks()
        
        # Dark Mode Toggle
        self.dark_mode = False
        
        # Create a Notebook (Tab Widget)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True)
        
        # Task Tab
        self.task_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.task_tab, text="Tasks")
        
        # Completed Tab
        self.completed_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.completed_tab, text="Completed")
        
        # Task Tab Widgets
        self.task_label = tk.Label(self.task_tab, text="Task:")
        self.task_label.pack(pady=5)
        
        self.task_entry = tk.Entry(self.task_tab, width=50)
        self.task_entry.pack(pady=5)
        
        self.time_label = tk.Label(self.task_tab, text="Time (HH:MM):")
        self.time_label.pack(pady=5)
        
        self.time_entry = tk.Entry(self.task_tab, width=50)
        self.time_entry.pack(pady=5)
        
        self.priority_label = tk.Label(self.task_tab, text="Priority:")
        self.priority_label.pack(pady=5)
        
        self.priority_var = tk.StringVar(value="Low")
        self.priority_menu = ttk.Combobox(self.task_tab, textvariable=self.priority_var, values=["Low", "Medium", "High"])
        self.priority_menu.pack(pady=5)
        
        self.due_date_label = tk.Label(self.task_tab, text="Due Date (YYYY-MM-DD):")
        self.due_date_label.pack(pady=5)
        
        self.due_date_entry = tk.Entry(self.task_tab, width=50)
        self.due_date_entry.pack(pady=5)
        
        self.task_list = tk.Listbox(self.task_tab, width=70, height=10)
        self.task_list.pack(pady=10)
        
        self.button_frame = tk.Frame(self.task_tab)
        self.button_frame.pack(pady=5)
        
        self.add_button = tk.Button(self.button_frame, text="Add Task", command=self.add_task)
        self.add_button.pack(side="left", padx=5)
        
        self.edit_button = tk.Button(self.button_frame, text="Edit Task", command=self.edit_task)
        self.edit_button.pack(side="left", padx=5)
        
        self.delete_button = tk.Button(self.button_frame, text="Delete Task", command=self.delete_task)
        self.delete_button.pack(side="left", padx=5)
        
        self.complete_button = tk.Button(self.button_frame, text="Mark Completed", command=self.complete_task)
        self.complete_button.pack(side="left", padx=5)
        
        self.clear_button = tk.Button(self.button_frame, text="Clear All", command=self.clear_tasks)
        self.clear_button.pack(side="left", padx=5)
        
        self.search_label = tk.Label(self.task_tab, text="Search:")
        self.search_label.pack(pady=5)
        
        self.search_entry = tk.Entry(self.task_tab, width=50)
        self.search_entry.pack(pady=5)
        self.search_entry.bind("<KeyRelease>", self.search_tasks)
        
        self.filter_label = tk.Label(self.task_tab, text="Filter by Priority:")
        self.filter_label.pack(pady=5)
        
        self.filter_var = tk.StringVar(value="All")
        self.filter_menu = ttk.Combobox(self.task_tab, textvariable=self.filter_var, values=["All", "Low", "Medium", "High"])
        self.filter_menu.pack(pady=5)
        self.filter_menu.bind("<<ComboboxSelected>>", self.filter_tasks)
        
        # Completed Tab Widgets
        self.completed_list = tk.Listbox(self.completed_tab, width=70, height=10)
        self.completed_list.pack(pady=10)
        
        # Dark Mode Toggle
        self.dark_mode_button = tk.Button(self.root, text="Toggle Dark Mode", command=self.toggle_dark_mode)
        self.dark_mode_button.pack(pady=10)
        
        # Load tasks into the UI
        self.load_task_list()
    
    def load_task_list(self):
        self.task_list.delete(0, tk.END)
        self.completed_list.delete(0, tk.END)
        for task in self.tasks:
            item_text = f"{task['time']} - {task['task']} (Priority: {task['priority']}, Due: {task['due_date']})"
            if task.get("completed", False):
                self.completed_list.insert(tk.END, "✅ " + item_text)
            else:
                self.task_list.insert(tk.END, "❌ " + item_text)
    
    def add_task(self):
        task_text = self.task_entry.get().strip()
        task_time = self.time_entry.get().strip()
        task_priority = self.priority_var.get()
        task_due_date = self.due_date_entry.get().strip()
        
        if not task_text:
            messagebox.showwarning("Warning", "Task cannot be empty!")
            return
        
        self.tasks.append({
            "task": task_text,
            "time": task_time,
            "priority": task_priority,
            "due_date": task_due_date,
            "completed": False
        })
        save_tasks()
        self.load_task_list()
        self.task_entry.delete(0, tk.END)
        self.time_entry.delete(0, tk.END)
        self.due_date_entry.delete(0, tk.END)
    
    def edit_task(self):
        selected = self.task_list.curselection()
        if not selected:
            messagebox.showwarning("Warning", "No task selected!")
            return
        
        task = self.tasks[selected[0]]
        new_task = simpledialog.askstring("Edit Task", "Edit task:", initialvalue=task["task"])
        new_time = simpledialog.askstring("Edit Time", "Edit time (HH:MM):", initialvalue=task["time"])
        new_priority = simpledialog.askstring("Edit Priority", "Edit priority (Low/Medium/High):", initialvalue=task["priority"])
        new_due_date = simpledialog.askstring("Edit Due Date", "Edit due date (YYYY-MM-DD):", initialvalue=task["due_date"])
        
        if new_task:
            task["task"] = new_task
        if new_time:
            task["time"] = new_time
        if new_priority:
            task["priority"] = new_priority
        if new_due_date:
            task["due_date"] = new_due_date
        
        save_tasks()
        self.load_task_list()
    
    def delete_task(self):
        selected = self.task_list.curselection()
        if not selected:
            messagebox.showwarning("Warning", "No task selected!")
            return
        del self.tasks[selected[0]]
        save_tasks()
        self.load_task_list()
    
    def complete_task(self):
        selected = self.task_list.curselection()
        if not selected:
            messagebox.showwarning("Warning", "No task selected!")
            return
        self.tasks[selected[0]]["completed"] = True
        save_tasks()
        self.load_task_list()
    
    def clear_tasks(self):
        self.tasks.clear()
        save_tasks()
        self.load_task_list()
    
    def search_tasks(self, event=None):
        query = self.search_entry.get().strip().lower()
        self.task_list.delete(0, tk.END)
        for task in self.tasks:
            if query in task["task"].lower():
                item_text = f"{task['time']} - {task['task']} (Priority: {task['priority']}, Due: {task['due_date']})"
                if task.get("completed", False):
                    self.completed_list.insert(tk.END, "✅ " + item_text)
                else:
                    self.task_list.insert(tk.END, "❌ " + item_text)
    
    def filter_tasks(self, event=None):
        priority = self.filter_var.get()
        self.task_list.delete(0, tk.END)
        for task in self.tasks:
            if priority == "All" or task["priority"] == priority:
                item_text = f"{task['time']} - {task['task']} (Priority: {task['priority']}, Due: {task['due_date']})"
                if task.get("completed", False):
                    self.completed_list.insert(tk.END, "✅ " + item_text)
                else:
                    self.task_list.insert(tk.END, "❌ " + item_text)
    
    def toggle_dark_mode(self):
        self.dark_mode = not self.dark_mode
        bg_color = "#2E2E2E" if self.dark_mode else "white"
        fg_color = "white" if self.dark_mode else "black"
        
        self.root.config(bg=bg_color)
        self.task_tab.config(bg=bg_color)
        self.completed_tab.config(bg=bg_color)
        
        for widget in self.task_tab.winfo_children():
            widget.config(bg=bg_color, fg=fg_color)
        
        for widget in self.completed_tab.winfo_children():
            widget.config(bg=bg_color, fg=fg_color)

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManager(root)
    root.mainloop()