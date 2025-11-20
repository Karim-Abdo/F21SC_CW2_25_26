class CountryMapper:
    """Maps country codes to continents"""
    
    COUNTRY_TO_CONTINENT = {
        # North America
        'US': 'North America', 'CA': 'North America', 'MX': 'North America',
        'GT': 'North America', 'CU': 'North America', 'HT': 'North America',
        'DO': 'North America', 'HN': 'North America', 'NI': 'North America',
        'SV': 'North America', 'CR': 'North America', 'PA': 'North America',
        'JM': 'North America', 'TT': 'North America', 'BS': 'North America',
        
        # South America
        'BR': 'South America', 'AR': 'South America', 'CL': 'South America',
        'CO': 'South America', 'PE': 'South America', 'VE': 'South America',
        'EC': 'South America', 'BO': 'South America', 'UY': 'South America',
        'PY': 'South America', 'GY': 'South America', 'SR': 'South America',
        
        # Europe
        'GB': 'Europe', 'FR': 'Europe', 'DE': 'Europe', 'IT': 'Europe',
        'ES': 'Europe', 'NL': 'Europe', 'SE': 'Europe', 'NO': 'Europe',
        'DK': 'Europe', 'FI': 'Europe', 'PL': 'Europe', 'RU': 'Europe',
        'UA': 'Europe', 'RO': 'Europe', 'BE': 'Europe', 'GR': 'Europe',
        'PT': 'Europe', 'CZ': 'Europe', 'HU': 'Europe', 'AT': 'Europe',
        'CH': 'Europe', 'IE': 'Europe', 'BG': 'Europe', 'HR': 'Europe',
        'SK': 'Europe', 'SI': 'Europe', 'LT': 'Europe', 'LV': 'Europe',
        'EE': 'Europe', 'IS': 'Europe', 'AL': 'Europe', 'MK': 'Europe',
        'RS': 'Europe', 'BA': 'Europe', 'ME': 'Europe', 'MD': 'Europe',
        'BY': 'Europe', 'LU': 'Europe', 'MT': 'Europe', 'CY': 'Europe',
        
        # Asia
        'CN': 'Asia', 'JP': 'Asia', 'IN': 'Asia', 'KR': 'Asia',
        'TH': 'Asia', 'VN': 'Asia', 'ID': 'Asia', 'MY': 'Asia',
        'SG': 'Asia', 'PH': 'Asia', 'PK': 'Asia', 'BD': 'Asia',
        'TR': 'Asia', 'IR': 'Asia', 'IQ': 'Asia', 'SA': 'Asia',
        'AE': 'Asia', 'IL': 'Asia', 'SY': 'Asia', 'JO': 'Asia',
        'LB': 'Asia', 'KW': 'Asia', 'OM': 'Asia', 'QA': 'Asia',
        'BH': 'Asia', 'YE': 'Asia', 'KZ': 'Asia', 'UZ': 'Asia',
        'MM': 'Asia', 'KH': 'Asia', 'LA': 'Asia', 'NP': 'Asia',
        'LK': 'Asia', 'AF': 'Asia', 'MN': 'Asia', 'TW': 'Asia',
        'HK': 'Asia', 'MO': 'Asia', 'TM': 'Asia', 'TJ': 'Asia',
        'KG': 'Asia', 'AM': 'Asia', 'AZ': 'Asia', 'GE': 'Asia',
        
        # Africa
        'ZA': 'Africa', 'EG': 'Africa', 'NG': 'Africa', 'KE': 'Africa',
        'ET': 'Africa', 'TZ': 'Africa', 'UG': 'Africa', 'DZ': 'Africa',
        'SD': 'Africa', 'MA': 'Africa', 'AO': 'Africa', 'GH': 'Africa',
        'MZ': 'Africa', 'MG': 'Africa', 'CM': 'Africa', 'CI': 'Africa',
        'NE': 'Africa', 'BF': 'Africa', 'ML': 'Africa', 'MW': 'Africa',
        'ZM': 'Africa', 'SN': 'Africa', 'SO': 'Africa', 'TD': 'Africa',
        'ZW': 'Africa', 'GN': 'Africa', 'RW': 'Africa', 'BJ': 'Africa',
        'TN': 'Africa', 'BI': 'Africa', 'SS': 'Africa', 'TG': 'Africa',
        'SL': 'Africa', 'LY': 'Africa', 'LR': 'Africa', 'MR': 'Africa',
        'CF': 'Africa', 'ER': 'Africa', 'GM': 'Africa', 'BW': 'Africa',
        'GA': 'Africa', 'NA': 'Africa', 'MU': 'Africa', 'SZ': 'Africa',
        
        # Oceania
        'AU': 'Oceania', 'NZ': 'Oceania', 'PG': 'Oceania', 'FJ': 'Oceania',
        'NC': 'Oceania', 'PF': 'Oceania', 'WS': 'Oceania', 'GU': 'Oceania',
        'VU': 'Oceania', 'TO': 'Oceania', 'KI': 'Oceania', 'FM': 'Oceania',
        'SB': 'Oceania', 'PW': 'Oceania', 'MH': 'Oceania', 'NR': 'Oceania',
    }
    
    @classmethod
    def get_continent(cls, country_code):
        """
        Get continent for a country code
        
        Args:
            country_code: ISO 2-letter country code (e.g., 'US', 'GB')
            
        Returns:
            str: Continent name or 'Unknown' if not found
        """
        if not country_code:
            return 'Unknown'
        return cls.COUNTRY_TO_CONTINENT.get(country_code.upper(), 'Unknown')
    
    @classmethod
    def get_all_countries(cls):
        """Get list of all supported country codes"""
        return list(cls.COUNTRY_TO_CONTINENT.keys())
    
    @classmethod
    def get_all_continents(cls):
        """Get list of all unique continents"""
        return list(set(cls.COUNTRY_TO_CONTINENT.values()))