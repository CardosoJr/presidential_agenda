from crawler import crawler
import yaml 
from datetime import date, datetime, timedelta
CONFIG_PATH = "crawler\config.yaml"

if __name__ == "__main__":
    with open(CONFIG_PATH, 'r') as stream:
        config_data = yaml.safe_load(stream)

    print("Scraping Presidential Agenda")
    print(config_data)

    config_data['begin'] = datetime.strptime(config_data['begin'],'%d-%m-%Y')
    config_data['end'] = datetime.strptime(config_data['end'],'%d-%m-%Y')

    crawObj = crawler.PresidentialAgendaCrawler(csv_path = config_data['data'], base_url = config_data['url'])
    crawObj.scrape_datarange(config_data['begin'], config_data['end'])