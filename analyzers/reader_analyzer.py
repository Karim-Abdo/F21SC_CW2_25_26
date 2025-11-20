from collections import defaultdict


class ReaderAnalyzer:
    """Analyzes reader profiles and reading time"""
    
    def __init__(self, data):
        self.data = data
    
    def get_total_readtime_by_user(self):
        user_readtime = defaultdict(int)
        
        for record in self.data:
            visitor_uuid = record.get('visitor_uuid', '')
            readtime = record.get('event_readtime', 0)
            
            if visitor_uuid and readtime:
                try:
                    readtime_int = int(readtime)
                    if readtime_int > 0:
                        user_readtime[visitor_uuid] += readtime_int
                except (ValueError, TypeError):
                    continue
        
        return dict(user_readtime)
    
    def get_top_readers(self, n=10):
        readtimes = self.get_total_readtime_by_user()
        
        # Sort by readtime (descending)
        sorted_readers = sorted(
            readtimes.items(), 
            key=lambda x: x[1], 
            reverse=True
        )
        
        return sorted_readers[:n]
    
    def print_top_readers(self, n=10):
        top_readers = self.get_top_readers(n)
        
        if not top_readers:
            print("No reader data found")
            return []
        
        print(f"\n{'='*80}")
        print(f"Top {n} Avid Readers by Total Reading Time")
        print(f"{'='*80}")
        print(f"{'Rank':<6} {'Visitor UUID':<40} {'Total Time (seconds)':>20} {'Formatted':>15}")
        print(f"{'-'*80}")
        
        for rank, (visitor_uuid, total_time) in enumerate(top_readers, 1):
            hours = total_time // 3600
            minutes = (total_time % 3600) // 60
            seconds = total_time % 60
            formatted = f"{hours}h {minutes}m {seconds}s"
            
            print(f"{rank:<6} {visitor_uuid:<40} {total_time:>20,} {formatted:>15}")
        
        print(f"{'='*80}\n")
        
        return top_readers
