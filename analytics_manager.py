from data.data_loader import DataLoader
from analyzers.country_analyzer import CountryAnalyzer
from analyzers.browser_analyzer import BrowserAnalyzer
from analyzers.reader_analyzer import ReaderAnalyzer
from analyzers.recommendation import RecommendationAnalyzer
from visualization.graph_visualizer import GraphVisualizer


class AnalyticsManager:
    def __init__(self, file_path=None):
        # Data and analyzers will be initialized when load_data() is called
        self.data_loader = DataLoader(file_path)
        self.data = None

        # placeholders
        self.country_analyzer = None
        self.browser_analyzer = None
        self.reader_analyzer = None
        self.recommendation_analyzer = None
        self.graph_visualizer = GraphVisualizer()

        # If a file_path was passed, load immediately
        if file_path:
            self.load_data()


       # Load data using the DataLoader instance and reinitialise analyzers.
    def load_data(self):

        # DataLoader method load_data() that returns a list 
        self.data = self.data_loader.load_data()

        # Reinit analyzers with the newly loaded data
        self.country_analyzer = CountryAnalyzer(self.data)
        self.browser_analyzer = BrowserAnalyzer(self.data)
        self.reader_analyzer = ReaderAnalyzer(self.data)

        # keep passing the loader to recommendation so it can build indexes efficiently
        self.recommendation_analyzer = RecommendationAnalyzer(self.data_loader)

        return self.data

        #Return top also liked documents
    def get_also_likes(self, doc_uuid, visitor_uuid=None):        
        return self.recommendation_analyzer.get_top_also_likes(doc_uuid, visitor_uuid)

        #Build graph data in RecommendationAnalyzer and GraphVisualizer to create outputs
    def generate_also_likes_graph(self, doc_uuid, visitor_uuid=None):
        graph_data = self.recommendation_analyzer.get_also_likes_graph_data(doc_uuid, visitor_uuid)
        return self.graph_visualizer.generate_also_likes_graph(graph_data)

        #Bootstraps and runs the CLI interface    
    def run_cli(self):
        from interfaces.cli import CLI
        cli = CLI(self)
        cli.run()

        #Bootstraps and runs the GUI interface.
    def run_gui(self):
        from interfaces.gui import GUI
        gui = GUI(self)
        gui.run()
