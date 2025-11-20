import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading

class GUI:
    def __init__(self, analytics_manager):
        self.analytics_manager = analytics_manager
        self.root = tk.Tk()
        self.root.title("Document Tracker Analytics")
        self.root.geometry("900x700")
        
        self.setup_gui()
    
    def setup_gui(self):
        # Create notebook for tabs
        notebook = ttk.Notebook(self.root)
        
        # Tab 1: Country/Continent Analysis
        country_frame = ttk.Frame(notebook)
        self.setup_country_tab(country_frame)
        
        # Tab 2: Browser Analysis
        browser_frame = ttk.Frame(notebook)
        self.setup_browser_tab(browser_frame)
        
        # Tab 3: Reader Profiles
        reader_frame = ttk.Frame(notebook)
        self.setup_reader_tab(reader_frame)
        
        # Tab 4: Also Likes
        also_likes_frame = ttk.Frame(notebook)
        self.setup_also_likes_tab(also_likes_frame)
        
        # Tab 5: Graph Visualization
        graph_frame = ttk.Frame(notebook)
        self.setup_graph_tab(graph_frame)
        
        notebook.add(country_frame, text="📍 Country/Continent")
        notebook.add(browser_frame, text="🌐 Browser Analysis")
        notebook.add(reader_frame, text="👤 Reader Profiles")
        notebook.add(also_likes_frame, text="❤️ Also Likes")
        notebook.add(graph_frame, text="📊 Graph Visualization")
        notebook.pack(expand=True, fill='both', padx=10, pady=10)
    
    
    def setup_country_tab(self, parent):
        """Tab for Country/Continent Views"""
        # Title
        title = ttk.Label(parent, text="Country & Continent Analysis", 
                         font=('Arial', 14, 'bold'))
        title.pack(pady=10)
        
        # Instructions
        ttk.Label(parent, text="Enter a Document UUID to analyze views by country and continent:").pack(pady=5)
        
        # Document UUID input
        input_frame = ttk.Frame(parent)
        input_frame.pack(pady=10)
        
        ttk.Label(input_frame, text="Document UUID:").pack(side=tk.LEFT, padx=5)
        self.country_doc_entry = ttk.Entry(input_frame, width=60)
        self.country_doc_entry.pack(side=tk.LEFT, padx=5)
        
        # Buttons
        button_frame = ttk.Frame(parent)
        button_frame.pack(pady=10)
        
        ttk.Button(button_frame, text="📊 Show Country Histogram", 
                  command=self.show_country_histogram, width=35).pack(pady=5)
        
        ttk.Button(button_frame, text="🌍 Show Continent Histogram", 
                  command=self.show_continent_histogram, width=35).pack(pady=5)
        
        # Status
        self.country_status = ttk.Label(parent, text="", foreground="blue")
        self.country_status.pack(pady=10)
        
        # Info
        info_text = """
        ℹ️ This analysis shows which countries and continents are viewing the document.
        The histograms will open in separate windows.
        """
        ttk.Label(parent, text=info_text, foreground="gray").pack(pady=10)
    
    def show_country_histogram(self):
        """Show country histogram"""
        doc_uuid = self.country_doc_entry.get().strip()
        if not doc_uuid:
            messagebox.showerror("Error", "Please enter a document UUID")
            return
        
        self.country_status.config(text="Generating country histogram...")
        
        def task():
            try:
                from analyzers.country_analyzer import CountryAnalyzer
                data = self.analytics_manager.load_data()
                analyzer = CountryAnalyzer(data)
                analyzer.plot_country_histogram(doc_uuid, top_n=20)
                self.root.after(0, lambda: self.country_status.config(
                    text="✓ Country histogram displayed successfully!"
                ))
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Error", f"Failed to generate histogram:\n{str(e)}"))
                self.root.after(0, lambda: self.country_status.config(text="✗ Error occurred"))
        
        threading.Thread(target=task, daemon=True).start()
    
    def show_continent_histogram(self):
        """Show continent histogram"""
        doc_uuid = self.country_doc_entry.get().strip()
        if not doc_uuid:
            messagebox.showerror("Error", "Please enter a document UUID")
            return
        
        self.country_status.config(text="Generating continent histogram...")
        
        def task():
            try:
                from analyzers.country_analyzer import CountryAnalyzer
                data = self.analytics_manager.load_data()
                analyzer = CountryAnalyzer(data)
                analyzer.plot_continent_histogram(doc_uuid)
                self.root.after(0, lambda: self.country_status.config(
                    text="✓ Continent histogram displayed successfully!"
                ))
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Error", f"Failed to generate histogram:\n{str(e)}"))
                self.root.after(0, lambda: self.country_status.config(text="✗ Error occurred"))
        
        threading.Thread(target=task, daemon=True).start()
    
    
    def setup_browser_tab(self, parent):
        """Tab for Browser Analysis"""
        # Title
        title = ttk.Label(parent, text="Browser Analysis", 
                         font=('Arial', 14, 'bold'))
        title.pack(pady=10)
        
        # Instructions
        ttk.Label(parent, text="Analyze browser usage across all documents in the dataset:").pack(pady=5)
        
        # Buttons
        button_frame = ttk.Frame(parent)
        button_frame.pack(pady=20)
        
        ttk.Button(button_frame, text="📱 Show Raw Browser Histogram", 
                  command=self.show_raw_browsers, width=40).pack(pady=10)
        
        ttk.Button(button_frame, text="🌐 Show Simplified Browser Histogram", 
                  command=self.show_simplified_browsers, width=40).pack(pady=10)
        
        # Status
        self.browser_status = ttk.Label(parent, text="", foreground="blue")
        self.browser_status.pack(pady=10)
        
        # Info
        info_text = """
        ℹ️ Raw histogram shows detailed user agent strings.
        Simplified histogram shows browser names (Chrome, Firefox, Safari, etc.).
        The histograms will open in separate windows.
        """
        ttk.Label(parent, text=info_text, foreground="gray", wraplength=700).pack(pady=10)
    
    def show_raw_browsers(self):
        """Show raw browser histogram"""
        self.browser_status.config(text="Generating raw browser histogram...")
        
        def task():
            try:
                from analyzers.browser_analyzer import BrowserAnalyzer
                data = self.analytics_manager.load_data()
                analyzer = BrowserAnalyzer(data)
                analyzer.plot_raw_browser_histogram(top_n=15)
                self.root.after(0, lambda: self.browser_status.config(
                    text="✓ Raw browser histogram displayed successfully!"
                ))
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Error", f"Failed to generate histogram:\n{str(e)}"))
                self.root.after(0, lambda: self.browser_status.config(text="✗ Error occurred"))
        
        threading.Thread(target=task, daemon=True).start()
    
    def show_simplified_browsers(self):
        """Show simplified browser histogram"""
        self.browser_status.config(text="Generating simplified browser histogram...")
        
        def task():
            try:
                from analyzers.browser_analyzer import BrowserAnalyzer
                data = self.analytics_manager.load_data()
                analyzer = BrowserAnalyzer(data)
                analyzer.plot_browser_histogram()
                self.root.after(0, lambda: self.browser_status.config(
                    text="✓ Simplified browser histogram displayed successfully!"
                ))
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Error", f"Failed to generate histogram:\n{str(e)}"))
                self.root.after(0, lambda: self.browser_status.config(text="✗ Error occurred"))
        
        threading.Thread(target=task, daemon=True).start()
    
    
    def setup_reader_tab(self, parent):
        """Tab for Reader Profiles"""
        # Title
        title = ttk.Label(parent, text="Reader Profiles", 
                         font=('Arial', 14, 'bold'))
        title.pack(pady=10)
        
        # Instructions
        ttk.Label(parent, text="Find the most avid readers based on total reading time:").pack(pady=5)
        
        # Input frame
        input_frame = ttk.Frame(parent)
        input_frame.pack(pady=10)
        
        ttk.Label(input_frame, text="Number of Top Readers:").pack(side=tk.LEFT, padx=5)
        self.reader_n_entry = ttk.Entry(input_frame, width=10)
        self.reader_n_entry.insert(0, "10")
        self.reader_n_entry.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(input_frame, text="🔍 Show Top Readers", 
                  command=self.show_top_readers).pack(side=tk.LEFT, padx=10)
        
        # Results text area
        self.reader_text = scrolledtext.ScrolledText(parent, height=25, width=100, 
                                                     font=('Courier', 10))
        self.reader_text.pack(pady=10, padx=10, fill='both', expand=True)
        
        # Info
        info_text = "ℹ️ This shows readers ranked by total time spent reading documents."
        ttk.Label(parent, text=info_text, foreground="gray").pack(pady=5)
    
    def show_top_readers(self):
        """Show top readers"""
        try:
            n = int(self.reader_n_entry.get())
            if n <= 0:
                raise ValueError("Number must be positive")
        except ValueError as e:
            messagebox.showerror("Error", "Please enter a valid positive number")
            return
        
        def task():
            try:
                from analyzers.reader_analyzer import ReaderAnalyzer
                data = self.analytics_manager.load_data()
                analyzer = ReaderAnalyzer(data)
                top_readers = analyzer.get_top_readers(n=n)
                
                # Format results
                result = f"{'='*100}\n"
                result += f"Top {n} Readers by Total Reading Time\n"
                result += f"{'='*100}\n\n"
                result += f"{'Rank':<6} {'Visitor UUID':<45} {'Total Time (s)':>15} {'Formatted':>15}\n"
                result += "-" * 100 + "\n"
                
                if not top_readers:
                    result += "\nNo reader data found.\n"
                else:
                    for rank, (uuid, time) in enumerate(top_readers, 1):
                        hours = time // 3600
                        minutes = (time % 3600) // 60
                        seconds = time % 60
                        formatted = f"{hours}h {minutes}m {seconds}s"
                        result += f"{rank:<6} {uuid:<45} {time:>15,} {formatted:>15}\n"
                    
                    total_time = sum(t for _, t in top_readers)
                    avg_time = total_time / len(top_readers) if top_readers else 0
                    
                    result += "\n" + "="*100 + "\n"
                    result += f"Summary:\n"
                    result += f"  Total reading time (top {n}): {total_time:,} seconds\n"
                    result += f"  Average reading time: {avg_time:,.0f} seconds\n"
                    result += "="*100 + "\n"
                
                self.root.after(0, lambda: self.display_reader_results(result))
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Error", f"Failed to get reader data:\n{str(e)}"))
        
        threading.Thread(target=task, daemon=True).start()
    
    def display_reader_results(self, result):
        """Display reader results in text area"""
        self.reader_text.delete(1.0, tk.END)
        self.reader_text.insert(tk.END, result)
    
    
    def setup_also_likes_tab(self, parent):
        """Tab for Also Likes"""
        # Title
        title = ttk.Label(parent, text="Also Likes Recommendations", 
                         font=('Arial', 14, 'bold'))
        title.pack(pady=10)
        
        ttk.Label(parent, text="Document UUID:").pack(pady=5)
        self.also_likes_doc_entry = ttk.Entry(parent, width=60)
        self.also_likes_doc_entry.pack(pady=5)
        
        ttk.Label(parent, text="Visitor UUID (optional):").pack(pady=5)
        self.visitor_entry = ttk.Entry(parent, width=60)
        self.visitor_entry.pack(pady=5)
        
        ttk.Button(parent, text="Get Also Likes", 
                  command=self.show_also_likes).pack(pady=10)
        
        self.also_likes_text = scrolledtext.ScrolledText(parent, height=20, width=90)
        self.also_likes_text.pack(pady=10, fill='both', expand=True, padx=10)
    
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
                if result:
                    for i, doc in enumerate(result, 1):
                        formatted_result += f"{i}. {doc}\n"
                else:
                    formatted_result += "No also-liked documents found.\n"
                    formatted_result += "(This may happen with small datasets or isolated documents)\n"
                
                self.root.after(0, lambda: self.display_also_likes_results(formatted_result))
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Error", str(e)))
        
        threading.Thread(target=task, daemon=True).start()
    
    def display_also_likes_results(self, result):
        self.also_likes_text.delete(1.0, tk.END)
        self.also_likes_text.insert(tk.END, result)
    
    
    def setup_graph_tab(self, parent):
        """Tab for Graph Visualization"""
        # Title
        title = ttk.Label(parent, text="Also Likes Graph Visualization", 
                         font=('Arial', 14, 'bold'))
        title.pack(pady=10)
        
        ttk.Label(parent, text="Document UUID:").pack(pady=5)
        self.graph_doc_entry = ttk.Entry(parent, width=60)
        self.graph_doc_entry.pack(pady=5)
        
        ttk.Label(parent, text="Visitor UUID (optional):").pack(pady=5)
        self.graph_visitor_entry = ttk.Entry(parent, width=60)
        self.graph_visitor_entry.pack(pady=5)
        
        ttk.Button(parent, text="Generate Also Likes Graph", 
                  command=self.generate_graph).pack(pady=10)
        
        self.graph_status = ttk.Label(parent, text="", foreground="blue")
        self.graph_status.pack(pady=5)
        
        # Info
        info_text = """
        ℹ️ This generates a graph showing relationships between documents and readers.
        Note: Requires graphviz to be installed for PDF generation.
        """
        ttk.Label(parent, text=info_text, foreground="gray", wraplength=700).pack(pady=10)
    
    def generate_graph(self):
        doc_uuid = self.graph_doc_entry.get()
        visitor_uuid = self.graph_visitor_entry.get() or None
        
        if not doc_uuid:
            messagebox.showerror("Error", "Please enter a document UUID")
            return
        
        def task():
            try:
                self.root.after(0, lambda: self.graph_status.config(text="Generating graph..."))
                
                dot_file, ps_file, pdf_file = self.analytics_manager.generate_also_likes_graph(
                    doc_uuid, visitor_uuid
                )
                
                if pdf_file:
                    self.root.after(0, lambda: self.graph_status.config(
                        text=f"✓ Graph generated: {pdf_file}"
                    ))
                    # Try to open the graph
                    self.analytics_manager.display_graph()
                else:
                    self.root.after(0, lambda: self.graph_status.config(
                        text="⚠ Graph DOT file generated but PDF conversion failed (graphviz not installed)"
                    ))
                    
            except Exception as e:
                self.root.after(0, lambda: self.graph_status.config(text=f"✗ Error: {str(e)}"))
        
        threading.Thread(target=task, daemon=True).start()
    
    def run(self):
        self.root.mainloop()