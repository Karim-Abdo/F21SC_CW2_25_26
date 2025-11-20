import matplotlib.pyplot as plt
from collections import Counter
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from utils.country_mapper import CountryMapper


class CountryAnalyzer:
    """Analyzes document views by country and continent"""
    
    def __init__(self, data):
        self.data = data
        self.country_mapper = CountryMapper()
    
    def get_views_by_country(self, doc_uuid):
        country_counts = Counter()
        
        for record in self.data:
            if record.get('env_doc_id') == doc_uuid:
                country = record.get('visitor_country', '')
                if country:
                    country_counts[country] += 1
        
        return dict(country_counts)
    
    def get_views_by_continent(self, doc_uuid):
        continent_counts = Counter()
        
        for record in self.data:
            if record.get('env_doc_id') == doc_uuid:
                # Use the continent from data if available
                continent = record.get('visitor_continent', '')
                if continent:
                    pass  # Use as is
                else:
                    # Otherwise map from country code
                    country = record.get('visitor_country', '')
                    if country:
                        continent = self.country_mapper.get_continent(country)
                    else:
                        continent = 'Unknown'
                
                continent_counts[continent] += 1
        
        return dict(continent_counts)
    
    def plot_country_histogram(self, doc_uuid, top_n=20):
        country_counts = self.get_views_by_country(doc_uuid)
        
        if not country_counts:
            print(f"No data found for document {doc_uuid}")
            return
        
        # Sort by count and take top N
        sorted_countries = sorted(
            country_counts.items(), 
            key=lambda x: x[1], 
            reverse=True
        )[:top_n]
        
        countries = [c[0] for c in sorted_countries]
        counts = [c[1] for c in sorted_countries]
        
        # Create histogram
        plt.figure(figsize=(14, 7))
        plt.bar(countries, counts, color='steelblue', edgecolor='navy', alpha=0.7)
        plt.xlabel('Country Code', fontsize=12)
        plt.ylabel('Number of Views', fontsize=12)
        plt.title(f'Document Views by Country (Top {len(countries)})\nDocument: {doc_uuid[:16]}...', 
                  fontsize=14, fontweight='bold')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.grid(axis='y', alpha=0.3, linestyle='--')
        plt.show()
        
        # Print summary
        print(f"\nTop {len(countries)} countries viewing document {doc_uuid[:16]}...:")
        total_views = sum(counts)
        for country, count in sorted_countries:
            percentage = (count / total_views) * 100
            print(f"  {country:4s}: {count:5d} views ({percentage:5.2f}%)")
        print(f"Total: {total_views} views from {len(country_counts)} countries\n")
    
    def plot_continent_histogram(self, doc_uuid):
        continent_counts = self.get_views_by_continent(doc_uuid)
        
        if not continent_counts:
            print(f"No data found for document {doc_uuid}")
            return
        
        # Sort by count
        sorted_continents = sorted(
            continent_counts.items(), 
            key=lambda x: x[1], 
            reverse=True
        )
        
        continents = [c[0] for c in sorted_continents]
        counts = [c[1] for c in sorted_continents]
        
        # Create histogram
        plt.figure(figsize=(12, 7))
        plt.bar(continents, counts, color='coral', edgecolor='darkred', alpha=0.7)
        plt.xlabel('Continent', fontsize=12)
        plt.ylabel('Number of Views', fontsize=12)
        plt.title(f'Document Views by Continent\nDocument: {doc_uuid[:16]}...', 
                  fontsize=14, fontweight='bold')
        plt.xticks(rotation=30, ha='right')
        plt.tight_layout()
        plt.grid(axis='y', alpha=0.3, linestyle='--')
        plt.show()
        
        # Print summary
        print(f"\nContinents viewing document {doc_uuid[:16]}...:")
        total_views = sum(counts)
        for continent, count in sorted_continents:
            percentage = (count / total_views) * 100
            print(f"  {continent:20s}: {count:5d} views ({percentage:5.2f}%)")
        print(f"Total: {total_views} views from {len(continent_counts)} continents\n")
