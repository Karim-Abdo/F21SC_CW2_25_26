class BrowserParser:
    
    @staticmethod
    def extract_browser_name(useragent):
        if not useragent:
            return 'Unknown'
        
        useragent_lower = useragent.lower()
        
        # Check in order (most specific first to avoid misclassification)
        # Edge must be checked before Chrome (Edge contains "Chrome")
        if 'edg/' in useragent_lower or 'edge/' in useragent_lower:
            return 'Edge'
        # Chrome must be checked before Safari (Chrome contains "Safari")
        else:
            if 'chrome/' in useragent_lower or 'crios/' in useragent_lower or 'crmo/' in useragent_lower:
                return 'Chrome'
            # Safari (after Chrome check)
            else:
                if 'safari/' in useragent_lower:
                    return 'Safari'
                # Firefox
                else:
                    if 'firefox/' in useragent_lower or 'fxios/' in useragent_lower:
                        return 'Firefox'
                    # Opera
                    else:
                        if 'opera/' in useragent_lower or 'opr/' in useragent_lower or 'opios/' in useragent_lower:
                            return 'Opera'
                        # Internet Explorer
                        else:
                            if 'msie' in useragent_lower or 'trident/' in useragent_lower:
                                return 'Internet Explorer'
                            # Mozilla (generic, after specific checks)
                            else:
                                if 'mozilla/' in useragent_lower:
                                    return 'Mozilla'
                                # Bots/Crawlers
                                else:
                                    if any(bot in useragent_lower for bot in ['bot', 'crawler', 'spider', 'scraper']):
                                        return 'Bot/Crawler'
                                    else:
                                        return 'Other'