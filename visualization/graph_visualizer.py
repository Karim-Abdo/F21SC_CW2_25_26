import os
import subprocess
import platform
from typing import Dict

class GraphVisualizer:
    def __init__(self, output_dir: str = "output"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    def _shorten_uuid(self, uuid: str, length: int = 4) -> str:
        if not uuid:
            return "none"
        return uuid[-length:] if len(uuid) >= length else uuid
    
    def generate_also_likes_graph(self, graph_data: Dict, filename: str = "also_likes"):
        dot_content = self._create_dot_content(graph_data)
        
        dot_file = os.path.join(self.output_dir, f"{filename}.dot")
        with open(dot_file, 'w') as f:
            f.write(dot_content)
        
        try:
            ps_file = os.path.join(self.output_dir, f"{filename}.ps")
            subprocess.run(['dot', '-Tps', '-o', ps_file, dot_file], check=True, capture_output=True)
            
            pdf_file = os.path.join(self.output_dir, f"{filename}.pdf")
            subprocess.run(['dot', '-Tpdf', '-o', pdf_file, dot_file], check=True, capture_output=True)
            
            print(f"Graph generated: {dot_file}, {ps_file}, {pdf_file}")
            
            # Automatically open the PDF
            self._open_pdf(pdf_file)
            
            return dot_file, ps_file, pdf_file
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            print(f"Graphviz not found or error generating graph: {e}")
            print("DOT file created.")
            return dot_file, None, None
    
    def _open_pdf(self, pdf_file: str):
        """Open the PDF file using the system's default PDF viewer"""
        try:
            system = platform.system()
            
            if system == "Windows":
                os.startfile(pdf_file)
            elif system == "Darwin":  # macOS
                subprocess.run(['open', pdf_file], check=False)
            else:  # Linux
                subprocess.run(['xdg-open', pdf_file], check=False)
            
            print(f"Opening PDF: {pdf_file}")
        except Exception as e:
            print(f"Could not open PDF automatically: {e}")
            print(f"Please open manually: {pdf_file}")
    
    def _create_dot_content(self, graph_data: Dict) -> str:
        input_doc = graph_data['input_document']
        input_visitor = graph_data['input_visitor']
        also_liked_docs = graph_data['also_liked_documents']
        relevant_readers = graph_data['relevant_readers']
        reader_documents = graph_data['reader_documents']
        
        dot_lines = [
            "digraph AlsoLikes {",
            "  rankdir=TB;",
            "  node [shape=rectangle, style=filled];",
            ""
        ]
        
        # Readers - all white
        for reader in relevant_readers:
            short_reader = self._shorten_uuid(reader)
            dot_lines.append(f'  reader_{short_reader} [label="{short_reader}", fillcolor="white"];')
        
        # Input document - green
        short_input_doc = self._shorten_uuid(input_doc)
        dot_lines.append(f'  doc_{short_input_doc} [label="{short_input_doc}", fillcolor="lightgreen"];')
        
        # Also-liked documents - white
        for doc in also_liked_docs:
            short_doc = self._shorten_uuid(doc)
            dot_lines.append(f'  doc_{short_doc} [label="{short_doc}", fillcolor="white"];')
        
        dot_lines.append("")
        
       
        for reader in relevant_readers:
            short_reader = self._shorten_uuid(reader)
            docs_read = reader_documents.get(reader, set())
            
            for doc in docs_read:
                short_doc = self._shorten_uuid(doc)
                if doc == input_doc or doc in also_liked_docs:
                    dot_lines.append(f'  reader_{short_reader} -> doc_{short_doc};')
        
        dot_lines.append("}")
        return "\n".join(dot_lines)