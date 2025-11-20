import matplotlib.pyplot as plt
from collections import Counter
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from utils.browser_parser import BrowserParser


class BrowserAnalyzer:
    """Analyzes document views by browser"""
    
    def __init__(self, data):
        self.data = data
        self.browser_parser = BrowserParser()
    
    def get_raw_browser_counts(self):
        browser_counts = Counter()
        
        for record in self.data:
            useragent = record.get('visitor_useragent', '')
            if useragent:
                browser_counts[useragent] += 1
        
        return dict(browser_counts)
    
    def get_browser_counts(self):
        browser_counts = Counter()
        
        for record in self.data:
            useragent = record.get('visitor_useragent', '')
            browser_name = self.browser_parser.extract_browser_name(useragent)
            browser_counts[browser_name] += 1
        
        return dict(browser_counts)
    
    def plot_raw_browser_histogram(self, top_n=15):
        browser_counts = self.get_raw_browser_counts()
        
        if not browser_counts:
            print("No browser data found")
            return
        
        # Sort by count and take top N
        sorted_browsers = sorted(
            browser_counts.items(), 
            key=lambda x: x[1], 
            reverse=True
        )[:top_n]
        
        # Truncate long useragent strings for display
        browsers = [b[0][:60] + '...' if len(b[0]) > 60 else b[0] 
                   for b in sorted_browsers]
        counts = [b[1] for b in sorted_browsers]
        
        # Create horizontal bar chart (better for long labels)
        plt.figure(figsize=(14, 10))
        plt.barh(browsers, counts, color='lightgreen', edgecolor='darkgreen', alpha=0.7)
        plt.xlabel('Number of Views', fontsize=12)
        plt.ylabel('User Agent String', fontsize=12)
        plt.title(f'Top {top_n} Browser User Agents (Raw)', 
                  fontsize=14, fontweight='bold')
        plt.tight_layout()
        plt.grid(axis='x', alpha=0.3, linestyle='--')
        plt.gca().invert_yaxis()  # Highest at top
        plt.show()
        
        # Print summary
        print(f"\nTop {len(browsers)} browser user agents:")
        for ua, count in sorted_browsers:
            print(f"  {count:5d} views: {ua[:80]}")
        print()
    
    def plot_browser_histogram(self):
        browser_counts = self.get_browser_counts()
        
        if not browser_counts:
            print("No browser data found")
            return
        
        # Sort by count
        sorted_browsers = sorted(
            browser_counts.items(), 
            key=lambda x: x[1], 
            reverse=True
        )
        
        browsers = [b[0] for b in sorted_browsers]
        counts = [b[1] for b in sorted_browsers]
        
        # Create histogram
        plt.figure(figsize=(10, 6))
        plt.bar(browsers, counts, color='skyblue', edgecolor='darkblue', alpha=0.7)
        plt.xlabel('Browser', fontsize=12)
        plt.ylabel('Number of Views', fontsize=12)
        plt.title('Document Views by Browser (Simplified)', 
                  fontsize=14, fontweight='bold')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.grid(axis='y', alpha=0.3, linestyle='--')
        plt.show()
        
        # Print summary
        print("\nBrowser distribution:")
        total_views = sum(counts)
        for browser, count in sorted_browsers:
            percentage = (count / total_views) * 100
            print(f"  {browser:20s}: {count:6d} views ({percentage:5.2f}%)")
        print(f"Total: {total_views} views\n")
