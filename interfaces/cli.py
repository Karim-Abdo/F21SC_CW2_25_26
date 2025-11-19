import argparse
import sys

class CLI:
    def __init__(self, analytics_manager):
        self.analytics_manager = analytics_manager
    
    def parse_arguments(self):
        parser = argparse.ArgumentParser(description='Document Tracker Analytics')
        parser.add_argument('-u', '--user_uuid', help='User UUID')
        parser.add_argument('-d', '--doc_uuid', help='Document UUID')
        parser.add_argument('-t', '--task_id', required=True, 
                          choices=['2a', '2b', '3a', '3b', '4', '5d', '6', '7'],
                          help='Task ID to execute')
        parser.add_argument('-f', '--file_name', required=True, 
                          help='Input JSON file name')
        
        return parser.parse_args()
    
    def run(self):
        args = self.parse_arguments()
        
        # Load data from specified file
        self.analytics_manager.data_loader.file_path = args.file_name
        self.analytics_manager.load_data()
        
        try:
            if args.task_id == '5d':
                if not args.doc_uuid:
                    print("Error: Document UUID required for task 5d")
                    sys.exit(1)
                result = self.analytics_manager.get_also_likes(args.doc_uuid, args.user_uuid)
                print("Top 10 Also Liked Documents:")
                for i, doc in enumerate(result, 1):
                    print(f"{i}. {doc}")
            
            elif args.task_id == '6':
                if not args.doc_uuid:
                    print("Error: Document UUID required for task 6")
                    sys.exit(1)
                dot_file, ps_file, pdf_file = self.analytics_manager.generate_also_likes_graph(
                    args.doc_uuid, args.user_uuid
                )
                print(f"Graph generated:")
                print(f"  DOT: {dot_file}")
                if ps_file:
                    print(f"  PS: {ps_file}")
                if pdf_file:
                    print(f"  PDF: {pdf_file}")
            
            elif args.task_id == '7':
                if not args.doc_uuid:
                    print("Error: Document UUID required for task 7")
                    sys.exit(1)
                
                # First generate the graph
                dot_file, ps_file, pdf_file = self.analytics_manager.generate_also_likes_graph(
                    args.doc_uuid, args.user_uuid
                )
                print(f"Graph generated for GUI display")
                
                # Then launch GUI with pre-filled values
                from interfaces.gui import GUI
                gui = GUI(self.analytics_manager)
                
                # Pre-fill the document and visitor fields in GUI
                if args.doc_uuid:
                    gui.graph_doc_entry.insert(0, args.doc_uuid)
                if args.user_uuid:
                    gui.graph_visitor_entry.insert(0, args.user_uuid)
                
                print("Launching GUI...")
                gui.run()
        
        except Exception as e:
            print(f"Error executing task {args.task_id}: {str(e)}")
            sys.exit(1)