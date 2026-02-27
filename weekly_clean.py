from megclass import MegaMan
from redis_man import res
import logging
logger = logging.getLogger(__name__)
def initialize_logger ():
    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',filename='/tmp/weekly_delete.log', level=logging.INFO)
    logger.info('Started Logging from main ')



def delete_all_records():
 del_list=res.get_all_keys()
 for key in del_list:
   print(key)
   if 'mega.co.nz' not in key:
       res.delete_a_key(key)
       continue
   ret= MegaMan.delete_url(key)
   if ret ==1 or ret == -2:  #Could not get fileName for this URL (-2), delete success (1)
      res.delete_a_key(key)

def weekly_delete():
    initialize_logger ()
    delete_all_records()
weekly_delete()
