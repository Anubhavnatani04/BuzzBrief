# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.
from .ChildrensPost import ChildrenspostSpider
from .Economic_times import EconomicTimesSpider
from .Newsahoot import NewsahootSpider
from .Outlook import OutlookSpider
from .Robinage import RobinageSpider
from .time_for_kids import TimeForKidsSpider
from .TOI_Kids import TOI_kidsSpider
from .HindustanTimes import HindustantimesSpider
from .IndianExpress import IndianexpressSpider
from .IndiaToday import IndiatodaySpider
from .RepublicWorld import RepublicworldSpider
from .TheHindu import ThehinduSpider
from .TimesOfIndia import TimesofindiaSpider
from .TheStatesman import ThestatesmanSpider
from .Tatva import TatvaSpider

__all__ = [
    'ChildrenspostSpider',
    'EconomicTimesSpider',
    'NewsahootSpider',
    'OutlookSpider',
    'RobinageSpider',
    'TimeForKidsSpider',
    'TOI_kidsSpider', 
    'HindustantimesSpider',
    'IndianexpressSpider',
    'IndiatodaySpider',
    'ThestatesmanSpider',
    'RepublicworldSpider',
    'ThehinduSpider',
    'TimesofindiaSpider',
    'TatvaSpider'
    ]