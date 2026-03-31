import requests
from xml.etree import ElementTree
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, String, Float, DateTime

Base = declarative_base()

class CurrencyRate(Base):
    __tablename__ = 'currency_rates'
    id = Column(String(3), primary_key=True)
    name = Column(String(100))
    value = Column(Float)
    date = Column(DateTime)
    nominal = Column(Float)

class CurrencyRates:
    _instance = None
    URL = "https://www.cbr.ru/scripts/XML_daily.asp"
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(CurrencyRates, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            self._char_codes = ['USD', 'EUR', 'GBP']
            self._rates = {}
            self.engine = create_engine('sqlite:///database.db')
            Base.metadata.create_all(self.engine)
            Session = sessionmaker(bind=self.engine)
            self.session = Session()
            self._initialized = True
    
    def update_rates(self):
        try:
            response = requests.get(self.URL)
            response.raise_for_status()
            
            tree = ElementTree.fromstring(response.content)
            self._rates = {}
            
            for valute in tree.findall('.//Valute'):
                char_code = valute.find('CharCode').text
                if char_code in self._char_codes:
                    value = float(valute.find('Value').text.replace(',', '.'))
                    nominal = float(valute.find('Nominal').text)
                    name = valute.find('Name').text
                    
                    rate = self.session.get(CurrencyRate, char_code)
                    if not rate:
                        rate = CurrencyRate(id=char_code)
                    
                    rate.value = value / nominal
                    rate.name = name
                    rate.date = datetime.now()
                    rate.nominal = nominal
                    
                    self.session.add(rate)
                    self.session.commit()
                    
                    self._rates[char_code] = {
                        'value': value / nominal,
                        'name': name,
                        'date': datetime.now()
                    }
            return True
        except Exception as e:
            print(f"Error updating rates: {e}")
            return False
    
    @property
    def char_codes(self):
        return self._char_codes
    
    @char_codes.setter
    def char_codes(self, codes):
        if all(isinstance(code, str) and len(code) == 3 for code in codes):
            self._char_codes = codes
            self.update_rates()
    
    def get_rates(self):
        return self.session.query(CurrencyRate).all()
    
    def get_rate(self, char_code):
        return self.session.get(CurrencyRate, char_code)