from data.data_loader import DataLoader
from analyzers.recommendation import RecommendationAnalyzer
from visualization.graph_visualizer import GraphVisualizer

class AnalyticsManager:
    def __init__(self, file_path=None):
        self.data_loader = DataLoader(file_path)
        self.recommendation_analyzer = RecommendationAnalyzer(self.data_loader)
        self.graph_visualizer = GraphVisualizer()
    
    def load_data(self):
        """Load data from the data loader"""
        return self.data_loader.load_data()
    
    def get_also_likes(self, doc_uuid, visitor_uuid=None):
        """Task 5d: Get top 10 also liked documents"""
        return self.recommendation_analyzer.get_top_also_likes(doc_uuid, visitor_uuid)
    
    def generate_also_likes_graph(self, doc_uuid, visitor_uuid=None):
        """Task 6: Generate also likes graph"""
        graph_data = self.recommendation_analyzer.get_also_likes_graph_data(doc_uuid, visitor_uuid)
        return self.graph_visualizer.generate_also_likes_graph(graph_data)
    
    def display_graph(self):
        """Display the generated graph"""
        self.graph_visualizer.display_graph()
    
    def run_cli(self):
        """Task 8: Run command line interface"""
        from interfaces.cli import CLI
        cli = CLI(self)
        cli.run()
    
    def run_gui(self):
        """Task 7: Run graphical user interface"""
        from interfaces.gui import GUI
        gui = GUI(self)
        gui.run()