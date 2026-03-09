link = 'https://raw.githubusercontent.com/AstraeLabs/Domains/main/domains.json'
import json
import os
import logging
from Src.Utilities.config import setup_logging
import Src.Utilities.config as config

level = config.LEVEL
logger = setup_logging(level)

async def fetch_domain(client,site_name):
    response = await client.get(link)
    data = response.json()
    domain = data[site_name[0]]['full_url'][:-1]
    return domain
def write_config(domain,site_name):
    try:
        json_file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'config.json')

        with open(json_file_path, 'r') as json_file:
            config_data = json.load(json_file)
        try:
            config_data['Siti'][site_name[1]]['url'] = domain
            with open(json_file_path, 'w') as json_file:
                json.dump(config_data, json_file, indent=4)
            return True
        except Exception as e:
            with open(json_file_path, 'w') as json_file:
                json.dump(config_data, json_file, indent=4)
            logger.info('Failed to write into config: ',e)
            return False
    except Exception as e:
        logger.info('Failed to write into config: ',e)
        return False


async def update_site(client,site_name):
    try:
        domain =  await fetch_domain(client,site_name)
        result = write_config(domain,site_name)
        return result
    except Exception as e:
        return False
async def update_all_sites(client):
    try:
        sites = [['cb01new','CB01'],['guardaserie','Guardaserie'],['eurostreaming','Eurostreaming'],['guardaplay','Guardaflix'],['guardoserie_2','Guardoserie'],['animeworld','AnimeWorld'],['toonitalia','Toonitalia']]
        for item in sites:
            domain = await fetch_domain(client,item)
            write_config(domain,item)
        return True
    except Exception as e:
        logger.info('Failed to update domains: ',e)
        return False
async def test_update_site():
    from curl_cffi.requests import AsyncSession
    async with AsyncSession() as client:
        result = await update_site(client,['guardoserie_2','Guardoserie'])

        #result = await update_all_sites(client)
        #domain = await update_site(client,['eurostreamings','Eurostreaming'])
        #write_config(domain,['eurostreamings','Eurostreaming'])

        
if __name__ == "__main__":
    import asyncio
    asyncio.run(test_update_site()) 