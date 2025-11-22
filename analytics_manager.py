from data.data_loader import DataLoader
from analyzers.country_analyzer import CountryAnalyzer
from analyzers.browser_analyzer import BrowserAnalyzer
from analyzers.reader_analyzer import ReaderAnalyzer
from analyzers.recommendation import RecommendationAnalyzer
from visualization.graph_visualizer import GraphVisualizer

class AnalyticsManager:
    def __init__(self, file_path=None):
        self.data_loader = DataLoader(file_path)
        self.data = self.data_loader.load_data()
        
        # Initialize analyzers for tasks 1-4
        self.country_analyzer = CountryAnalyzer(self.data)
        self.browser_analyzer = BrowserAnalyzer(self.data)
        self.reader_analyzer = ReaderAnalyzer(self.data)
        
        # Initialize analyzers for tasks 5-8
        self.recommendation_analyzer = RecommendationAnalyzer(self.data_loader)
        self.graph_visualizer = GraphVisualizer()
    
    def load_data(self):
        return self.data
    
    # Methods for tasks 5-8
    def get_also_likes(self, doc_uuid, visitor_uuid=None):
        return self.recommendation_analyzer.get_top_also_likes(doc_uuid, visitor_uuid)
    
    def generate_also_likes_graph(self, doc_uuid, visitor_uuid=None):
        graph_data = self.recommendation_analyzer.get_also_likes_graph_data(doc_uuid, visitor_uuid)
        return self.graph_visualizer.generate_also_likes_graph(graph_data)
    
    def run_cli(self):
        from interfaces.cli import CLI
        cli = CLI(self)
        cli.run()
    
    def run_gui(self):
        from interfaces.gui import GUI
        gui = GUI(self)
        gui.run()