import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading

class GUI:
    def __init__(self, analytics_manager):
        self.analytics_manager = analytics_manager
        self.root = tk.Tk()
        self.root.title("Document Tracker Analytics")
        self.root.geometry("800x600")
        self.setup_gui()
    
    def setup_gui(self):
        notebook = ttk.Notebook(self.root)
        
        # Also Likes Tab
        also_likes_frame = ttk.Frame(notebook)
        self.setup_also_likes_tab(also_likes_frame)
        
        # Graph Tab
        graph_frame = ttk.Frame(notebook)
        self.setup_graph_tab(graph_frame)
        
        notebook.add(also_likes_frame, text="Also Likes")
        notebook.add(graph_frame, text="Graph Visualization")
        notebook.pack(expand=True, fill='both')
    
    def setup_also_likes_tab(self, parent):
        ttk.Label(parent, text="Document UUID:").pack(pady=5)
        self.also_likes_doc_entry = ttk.Entry(parent, width=50)
        self.also_likes_doc_entry.pack(pady=5)
        
        ttk.Label(parent, text="Visitor UUID (optional):").pack(pady=5)
        self.visitor_entry = ttk.Entry(parent, width=50)
        self.visitor_entry.pack(pady=5)
        
        ttk.Button(parent, text="Get Also Likes", command=self.show_also_likes).pack(pady=10)
        
        self.also_likes_text = scrolledtext.ScrolledText(parent, height=20, width=80)
        self.also_likes_text.pack(pady=10, fill='both', expand=True)
    
    def setup_graph_tab(self, parent):
        ttk.Label(parent, text="Document UUID:").pack(pady=5)
        self.graph_doc_entry = ttk.Entry(parent, width=50)
        self.graph_doc_entry.pack(pady=5)
        
        ttk.Label(parent, text="Visitor UUID (optional):").pack(pady=5)
        self.graph_visitor_entry = ttk.Entry(parent, width=50)
        self.graph_visitor_entry.pack(pady=5)
        
        ttk.Button(parent, text="Generate Also Likes Graph", command=self.generate_graph).pack(pady=10)
        
        self.graph_status = ttk.Label(parent, text="")
        self.graph_status.pack(pady=5)
    
    def show_also_likes(self):
        doc_uuid = self.also_likes_doc_entry.get()
        visitor_uuid = self.visitor_entry.get() or None
        
        if not doc_uuid:
            messagebox.showerror("Error", "Please enter a document UUID")
            return
        
        def task():
            try:
                result = self.analytics_manager.get_also_likes(doc_uuid, visitor_uuid)
                formatted_result = "Top 10 Also Liked Documents:\n\n"
                for i, doc in enumerate(result, 1):
                    formatted_result += f"{i}. {doc}\n"
                
                self.root.after(0, lambda: self.display_also_likes_results(formatted_result))
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Error", str(e)))
        
        threading.Thread(target=task).start()
    
    def generate_graph(self):
        doc_uuid = self.graph_doc_entry.get()
        visitor_uuid = self.graph_visitor_entry.get() or None
        
        if not doc_uuid:
            messagebox.showerror("Error", "Please enter a document UUID")
            return
        
        def task():
            try:
                self.root.after(0, lambda: self.graph_status.config(text="Generating graph..."))
                dot_file, ps_file, pdf_file = self.analytics_manager.generate_also_likes_graph(doc_uuid, visitor_uuid)
                
                if pdf_file:
                    self.root.after(0, lambda: self.graph_status.config(text=f"Graph generated: {pdf_file}"))
                else:
                    self.root.after(0, lambda: self.graph_status.config(text="Graph DOT file created but PDF conversion failed"))
                    
            except Exception as e:
                self.root.after(0, lambda: self.graph_status.config(text=f"Error: {str(e)}"))
        
        threading.Thread(target=task).start()
    
    def display_also_likes_results(self, result):
        self.also_likes_text.delete(1.0, tk.END)
        self.also_likes_text.insert(tk.END, result)
    
    def run(self):
        self.root.mainloop()