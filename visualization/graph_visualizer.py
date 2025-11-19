import os
import subprocess
from typing import Dict, Set

class GraphVisualizer:
    def __init__(self, output_dir: str = "output"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    def _shorten_uuid(self, uuid: str, length: int = 4) -> str:
        """Shorten UUID to last N hex digits"""
        if not uuid:
            return "none"
        return uuid[-length:] if len(uuid) >= length else uuid
    
    def generate_also_likes_graph(self, graph_data: Dict, filename: str = "also_likes"):
        """Task 6: Generate also likes graph in DOT format"""
        dot_content = self._create_dot_content(graph_data)
        
        # Write DOT file
        dot_file = os.path.join(self.output_dir, f"{filename}.dot")
        with open(dot_file, 'w') as f:
            f.write(dot_content)
        
        # Generate PS/PDF files using graphviz
        try:
            # Generate PS
            ps_file = os.path.join(self.output_dir, f"{filename}.ps")
            subprocess.run(['dot', '-Tps', '-o', ps_file, dot_file], check=True, capture_output=True)
            
            # Generate PDF
            pdf_file = os.path.join(self.output_dir, f"{filename}.pdf")
            subprocess.run(['dot', '-Tpdf', '-o', pdf_file, dot_file], check=True, capture_output=True)
            
            print(f"Graph generated: {dot_file}, {ps_file}, {pdf_file}")
            return dot_file, ps_file, pdf_file
        except subprocess.CalledProcessError as e:
            print(f"Error generating graph: {e}")
            return dot_file, None, None
        except FileNotFoundError:
            print("Graphviz not found. Please install graphviz package.")
            return dot_file, None, None
    
    def _create_dot_content(self, graph_data: Dict) -> str:
        """Create DOT format content for the graph"""
        input_doc = graph_data['input_document']
        input_visitor = graph_data['input_visitor']
        also_liked_docs = graph_data['also_liked_documents']
        relevant_readers = graph_data['relevant_readers']
        
        dot_lines = [
            "digraph AlsoLikes {",
            "  rankdir=TB;",
            "  node [shape=rectangle, style=filled];",
            "  ",
            "  // Define reader and document nodes"
        ]
        
        # Add reader nodes
        for reader in relevant_readers:
            short_reader = self._shorten_uuid(reader)
            color = "lightgreen" if reader == input_visitor else "lightblue"
            dot_lines.append(f'  reader_{short_reader} [label="{short_reader}", fillcolor="{color}"];')
        
        # Add document nodes
        short_input_doc = self._shorten_uuid(input_doc)
        dot_lines.append(f'  doc_{short_input_doc} [label="{short_input_doc}", fillcolor="lightgreen"];')
        
        for doc in also_liked_docs:
            short_doc = self._shorten_uuid(doc)
            dot_lines.append(f'  doc_{short_doc} [label="{short_doc}", fillcolor="lightcoral"];')
        
        dot_lines.append("")
        dot_lines.append("  // Define edges (read relationships)")
        
        # Add edges from readers to documents they read
        for reader in relevant_readers:
            short_reader = self._shorten_uuid(reader)
            docs_read = graph_data['reader_documents'].get(reader, set())
            
            for doc in docs_read:
                short_doc = self._shorten_uuid(doc)
                if doc == input_doc or doc in also_liked_docs:
                    dot_lines.append(f'  reader_{short_reader} -> doc_{short_doc};')
        
        dot_lines.append("}")
        
        return "\n".join(dot_lines)
    
    def display_graph(self, filename: str = "also_likes"):
        """Display the generated graph"""
        pdf_file = os.path.join(self.output_dir, f"{filename}.pdf")
        if os.path.exists(pdf_file):
            try:
                # Try to open with default viewer
                if os.name == 'nt':  # Windows
                    os.startfile(pdf_file)
                elif os.name == 'posix':  
                    subprocess.run(['xdg-open', pdf_file])
                print(f"Opened graph: {pdf_file}")
            except:
                print(f"Graph generated: {pdf_file} (open manually)")
        else:
            print("Graph PDF file not found.")