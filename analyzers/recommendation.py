from collections import defaultdict, Counter
from typing import Dict, List, Set, Callable, Optional

class RecommendationAnalyzer:
    def __init__(self, data_loader):
        self.data_loader = data_loader
        self.visitor_to_documents: Dict[str, Set[str]] = defaultdict(set)
        self.document_to_visitors: Dict[str, Set[str]] = defaultdict(set)
        self._build_indices()
    
    #Build indices for efficient lookup
    def _build_indices(self):
        print("Building recommendation indices...")
        for entry in self.data_loader.load_data():
            visitor_uuid = entry.get('visitor_uuid')
            document_uuid = entry.get('document_uuid')
            
            if visitor_uuid and document_uuid:
                self.visitor_to_documents[visitor_uuid].add(document_uuid)
                self.document_to_visitors[document_uuid].add(visitor_uuid)
        print("Indices built successfully")
    
    def get_visitors_of_document(self, doc_uuid: str) -> Set[str]:
        return self.document_to_visitors.get(doc_uuid, set())
    
    def get_documents_of_visitor(self, visitor_uuid: str) -> Set[str]:
        return self.visitor_to_documents.get(visitor_uuid, set())
    
    def also_likes(self, doc_uuid: str, sorting_func: Callable, 
                   visitor_uuid: Optional[str] = None) -> List[str]:
        # Get all readers of the input document
        readers = self.get_visitors_of_document(doc_uuid)
        
        # If a specific visitor is provided exclude them from consideration
        if visitor_uuid and visitor_uuid in readers:
            readers.remove(visitor_uuid)
        
        # Collect all documents read by these readers 
        also_liked_docs = defaultdict(int)
        
        for reader in readers:
            reader_docs = self.get_documents_of_visitor(reader)
            for doc in reader_docs:
                if doc != doc_uuid:  # Exclude the input document
                    also_liked_docs[doc] += 1
        
        # Convert to list and sort using the provided sorting function
        sorted_docs = sorted(also_liked_docs.items(), key=sorting_func, reverse=True)
        return [doc for doc, count in sorted_docs]
    
    def get_top_also_likes(self, doc_uuid: str, visitor_uuid: Optional[str] = None, 
                          top_n: int = 10) -> List[str]:
        """Task 5d: Get top N also liked documents sorted by reader count"""
        def sorting_func(doc_count_pair):
            return doc_count_pair[1]  # Sort by count of readers
        
        all_liked = self.also_likes(doc_uuid, sorting_func, visitor_uuid)
        return all_liked[:top_n]
    
    def get_also_likes_graph_data(self, doc_uuid: str, visitor_uuid: Optional[str] = None) -> Dict:
        """Get data for generating the also likes graph"""
        # Get liked documents top 10
        also_liked_docs = set(self.get_top_also_likes(doc_uuid, visitor_uuid))
        
        # Get all readers of the input document
        input_readers = self.get_visitors_of_document(doc_uuid)
        
        # Filter readers who also read at least one of the also liked documents
        relevant_readers = set()
        for reader in input_readers:
            reader_docs = self.get_documents_of_visitor(reader)
            if reader_docs.intersection(also_liked_docs):
                relevant_readers.add(reader)
        
        return {
            'input_document': doc_uuid,
            'input_visitor': visitor_uuid,
            'also_liked_documents': also_liked_docs,
            'relevant_readers': relevant_readers,
            'reader_documents': {reader: self.get_documents_of_visitor(reader) 
                               for reader in relevant_readers}
        }