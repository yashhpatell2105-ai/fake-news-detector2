"""Sample data and demo articles for testing TRUTH system"""

SAMPLE_ARTICLES = [
    {
        "title": "Breaking: New Study Shows Vaccines Are 99% Effective",
        "content": """
        A comprehensive study conducted by leading medical researchers has confirmed that 
        vaccines are highly effective at preventing serious diseases. According to the World 
        Health Organization, vaccination programs have saved millions of lives globally.
        
        The research, published in reputable medical journals, examined data from over 
        1 million participants across 50 countries. Researchers found that properly vaccinated 
        individuals had a 99% protection rate against severe illness.
        
        "These findings are consistent with decades of scientific evidence," said Dr. Jane Smith, 
        lead researcher at the National Health Institute. "Vaccines remain one of our most 
        powerful public health tools."
        
        Health authorities worldwide recommend vaccination as a key measure for disease prevention.
        """,
        "source": "https://www.health-news.org/article",
        "is_fake": False
    },
    {
        "title": "SHOCKING: 5G Networks Cause Mutation in Birds!!!",
        "content": """
        BREAKING NEWS!!! Scientists have FINALLY discovered the truth that governments 
        don't want you to know! 5G networks are causing BIRDS to MUTATE!!!
        
        According to sources (unnamed), 5G radiation is turning birds into government surveillance 
        drones! This is NOT a conspiracy theory - it's happening RIGHT NOW!
        
        Wake up sheeple! They're watching us! The evidence is EVERYWHERE if you just open your eyes!
        
        SHARE THIS BEFORE THEY DELETE IT!!!
        
        #5GTruth #BirdsDroneTheory #GovernmentCoverup
        """,
        "source": "https://www.conspiracy-blog.net/article",
        "is_fake": True
    },
    {
        "title": "Climate Change Report Released by Scientists",
        "content": """
        The Intergovernmental Panel on Climate Change (IPCC) has released their latest assessment 
        report on global climate trends. The comprehensive report, based on peer-reviewed research, 
        documents rising global temperatures and their impacts on ecosystems.
        
        "The evidence is unambiguous," states the report. "Human activities have warmed the climate 
        system since pre-industrial times."
        
        According to the IPCC, 97% of actively publishing climate scientists agree that climate 
        change is real and human-caused. The report recommends immediate action to reduce greenhouse 
        gas emissions.
        
        Scientists from around the world contributed to this assessment, which took several years 
        to complete. The findings are consistent with previous research on climate change.
        """,
        "source": "https://www.climate-science.org/report",
        "is_fake": False
    },
    {
        "title": "EXPOSED: Secret Underground Bases DISCOVERED!",
        "content": """
        UNBELIEVABLE!!! Hidden camera footage shows MASSIVE underground bases where 
        ALIENS are working with world governments!!! This will SHOCK you!!!
        
        An anonymous source (who definitely exists and is 100% credible) claims to have 
        discovered shocking evidence of extraterrestrial collaboration. The video "proof" 
        is too blurry to see anything clearly, but experts on YouTube say it PROVES everything!
        
        The mainstream media is COVERING THIS UP because they want to control your mind! 
        Don't believe their LIES!
        
        This is the TRUTH that governments don't want revealed!
        """,
        "source": "https://www.fake-news-today.net/secret-bases",
        "is_fake": True
    }
]

def get_sample_articles():
    """Return all sample articles"""
    return SAMPLE_ARTICLES

def get_fake_articles():
    """Return only fake articles"""
    return [a for a in SAMPLE_ARTICLES if a['is_fake']]

def get_real_articles():
    """Return only real articles"""
    return [a for a in SAMPLE_ARTICLES if not a['is_fake']]
