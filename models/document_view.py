class DocumentView:
    """Represents a single document view event from the JSON data"""
    
    def __init__(self, json_data):
        self.visitor_uuid = json_data.get('visitor_uuid', '')
        self.doc_uuid = json_data.get('env_doc_id', '')
        self.country = json_data.get('visitor_country', '')
        self.continent = json_data.get('visitor_continent', '')
        self.useragent = json_data.get('visitor_useragent', '')
        self.readtime = json_data.get('event_readtime', 0)
        self.timestamp = json_data.get('ts', '')
        
    def __repr__(self):
        doc_short = self.doc_uuid[:8] if self.doc_uuid else 'None'
        visitor_short = self.visitor_uuid[:8] if self.visitor_uuid else 'None'
        return f"DocumentView(doc={doc_short}..., visitor={visitor_short}..., country={self.country})"