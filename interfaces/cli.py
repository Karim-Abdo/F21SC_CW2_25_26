import argparse
import sys
import os


#Helper to print sorted top N view of a mapping
def _print_top_counts(counter_dict, top_n=10, name='items'):
    if not counter_dict:
        print("  (no data)")
        return

    # Sort by count descending
    items = sorted(counter_dict.items(), key=lambda x: x[1], reverse=True)
    total = sum(v for _, v in items)
    print(f"Top {min(top_n, len(items))} {name} (total {total}):")
    for i, (k, v) in enumerate(items[:top_n], start=1):
        print(f"  {i:2d}. {k} — {v} views ({(v/total*100):.2f}%)")
    print()

  
  #Command line interface to run tasks in analytics_manager The CLI prints textual results 
class CLI:
    def __init__(self, analytics_manager):
        self.analytics_manager = analytics_manager

    def parse_arguments(self):
        parser = argparse.ArgumentParser(description='Document Tracker Analytics CLI')
        parser.add_argument('-u', '--user_uuid', help='User UUID (optional)')
        parser.add_argument('-d', '--doc_uuid', help='Document UUID (required)')
        parser.add_argument('-t', '--task_id', required=True,
                            choices=['2a', '2b', '3a', '3b', '4', '5d', '6', '7'],
                            help='Task ID to execute')
        parser.add_argument('-f', '--file_name', required=True,
                            help='Input JSON file name (path to JSONL file)')
        parser.add_argument('--top', type=int, default=10,
                            help='Number of top results to print (default: 10)')
        return parser.parse_args()

    def run(self):
        args = self.parse_arguments()

        # Validate file path
        file_path = args.file_name
        if not os.path.exists(file_path):
            print(f"Error: File not found: {file_path}", file=sys.stderr)
            sys.exit(2)

        # Update DataLoader and reload data and analyzers
        self.analytics_manager.data_loader.file_path = file_path
        try:
            data = self.analytics_manager.load_data()
        except Exception as e:
            print(f"Error loading data from {file_path}: {e}", file=sys.stderr)
            sys.exit(3)

        # Dispatch tasks
        try:
            if args.task_id == '2a':
                if not args.doc_uuid:
                    print("Error: -d/--doc_uuid is required for task 2a", file=sys.stderr)
                    sys.exit(4)
                counts = self.analytics_manager.country_analyzer.get_views_by_country(args.doc_uuid)
                _print_top_counts(counts, top_n=args.top, name='countries')

            elif args.task_id == '2b':
                if not args.doc_uuid:
                    print("Error: -d/--doc_uuid is required for task 2b", file=sys.stderr)
                    sys.exit(4)
                counts = self.analytics_manager.country_analyzer.get_views_by_continent(args.doc_uuid)
                _print_top_counts(counts, top_n=args.top, name='continents')

            elif args.task_id == '3a':
                counts = self.analytics_manager.browser_analyzer.get_raw_browser_counts()
                _print_top_counts(counts, top_n=args.top, name='raw user agent strings')

            elif args.task_id == '3b':
                counts = self.analytics_manager.browser_analyzer.get_browser_counts()
                _print_top_counts(counts, top_n=args.top, name='browsers ')

            elif args.task_id == '4':
                # Try several method names to be robust to different impls
                ra = self.analytics_manager.reader_analyzer
                if hasattr(ra, 'get_top_readers'):
                    top_n = getattr(ra, 'get_top_readers')
                    readers = ra.get_top_readers(n=args.top) if callable(top_n) else ra.get_top_readers()
                elif hasattr(ra, 'get_top_readers_list'):
                    readers = ra.get_top_readers_list(args.top)
                elif hasattr(ra, 'get_top_readers'):
                    readers = ra.get_top_readers(args.top)
                elif hasattr(ra, 'top_readers'):
                    readers = ra.top_readers(args.top)
                else:
                    # Try more generic name
                    if hasattr(ra, 'get_top_readers'):
                        readers = ra.get_top_readers(args.top)
                    else:
                        raise AttributeError("ReaderAnalyzer does not expose a top readers method")

                if not readers:
                    print("No reader stats found.")
                else:
                    print(f"Top {len(readers)} readers (visitor_uuid, total_time_seconds):")
                    for i, (visitor_uuid, total_time) in enumerate(readers, start=1):
                        print(f"  {i:2d}. {visitor_uuid} — {total_time}")
                    print()

            elif args.task_id == '5d':
                if not args.doc_uuid:
                    print("Error: -d/--doc_uuid is required for task 5d", file=sys.stderr)
                    sys.exit(4)
                results = self.analytics_manager.get_also_likes(args.doc_uuid, args.user_uuid)
                if not results:
                    print("(no also like results)")
                else:
                    print(f"Top {len(results)} also liked documents for {args.doc_uuid}:")
                    for i, doc in enumerate(results, start=1):
                        # handle both tuples or just docs
                        if isinstance(doc, (list, tuple)) and len(doc) >= 1:
                            doc_id = doc[0]
                            metric = doc[1] if len(doc) > 1 else None
                            if metric is not None:
                                print(f"  {i:2d}. {doc_id} — {metric}")
                            else:
                                print(f"  {i:2d}. {doc_id}")
                        else:
                            print(f"  {i:2d}. {doc}")

            elif args.task_id == '6':
                if not args.doc_uuid:
                    print("Error: -d/--doc_uuid is required for task 6", file=sys.stderr)
                    sys.exit(4)
                dot_file, ps_file, pdf_file = self.analytics_manager.generate_also_likes_graph(
                    args.doc_uuid, args.user_uuid
                )
                print("Also likes graph generated:")
                print(f"  DOT: {dot_file}")
                if ps_file:
                    print(f"  PS:  {ps_file}")
                if pdf_file:
                    print(f"  PDF: {pdf_file}")

            elif args.task_id == '7':
                # launches GUI after generating graph
                if not args.doc_uuid:
                    print("Error: -d/--doc_uuid is required for task 7", file=sys.stderr)
                    sys.exit(4)

                # Generate graph first 
                self.analytics_manager.generate_also_likes_graph(args.doc_uuid, args.user_uuid)

                # Import GUI 
                from interfaces.gui import GUI
                gui = GUI(self.analytics_manager)

                # Pre fill fields if they exist on GUI instance
                try:
                    if args.doc_uuid and hasattr(gui, 'graph_doc_entry'):
                        gui.graph_doc_entry.delete(0, 'end')
                        gui.graph_doc_entry.insert(0, args.doc_uuid)
                    if args.user_uuid and hasattr(gui, 'graph_visitor_entry'):
                        gui.graph_visitor_entry.delete(0, 'end')
                        gui.graph_visitor_entry.insert(0, args.user_uuid)
                except Exception:
                    pass

                print("Launching GUI...")
                gui.run()

        except Exception as e:
            print(f"Error executing task {args.task_id}: {e}", file=sys.stderr)
            sys.exit(5)
