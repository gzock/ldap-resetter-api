import pymongo
from bson import objectid
from datetime import datetime

class MongoController(object):
  __client = None
  __db = None
  __co = None
  
  def __init__(self, host, port):
    self.__client = pymongo.MongoClient(host, port)
    self.__db = self.__client.vuv

  def __del__(self):
    self.close()

  def select_coll_targets(self):
    self.__co = self.__db.targets
  
  def select_coll_hosts(self):
    self.__co = self.__db.hosts
  
  def select_coll_scan(self):
    self.__co = self.__db.scan
  
  def add_target(self, json):
    self.select_coll_targets()
    exists_target = self.get_target_by_ipaddr(json["ip_address"])
    
    if exists_target:
      return exists_target["_id"]
    else:
      exists_target = self.get_target_by_name(json["name"])
    
      if exists_target:
        exists_host = self.get_host_by_target_id(exists_target["_id"])
        self.select_coll_targets()
        if exists_host:
          if json["ip_address"] in exists_host["ip_address"]:
            return exists_target["_id"]
            
      ret =  self.__co.insert_one(json)
      return ret.inserted_id

  def add_host(self, json):
    self.select_coll_hosts()
    return self.__co.insert_one(json)

  def set_host(self, json):
    self.select_coll_hosts()
    self.__co.save(json)

  def set_target(self, json):
    self.select_coll_targets()
    self.__co.save(json)
  
  def get_target(self, id):
    self.select_coll_targets()
    return self.__co.find_one({"_id": id})

  def get_target_by_ipaddr(self, ipaddr):
    self.select_coll_targets()
    return self.__co.find_one({"ip_address": {"$in": [ipaddr]}})

  def get_target_by_name(self, name):
    self.select_coll_targets()
    return self.__co.find_one({"name": name})

  def get_all_targets(self):
    self.select_coll_targets()
    return [data for data in self.__co.find()]

  def get_host(self, id):
    self.select_coll_hosts()
    return self.__co.find_one({"_id": id})

  def get_host_by_target_id(self, id):
    self.select_coll_hosts()
    if type(id) is str:
      return self.__co.find_one({"target": objectid.ObjectId(id)})
    return self.__co.find_one({"target": id})

  def get_all_hosts(self):
    self.select_coll_hosts()
    return [data for data in self.__co.find()]

  def get_scan(self):
    self.select_coll_scan()
    ret = self.__co.find_one()
    return ret if ret is not None else {}

  def get_scan_found_results(self):
    self.select_coll_targets()

    scan_found_results = []
    targets =  self.get_all_targets()
    today = datetime.today()

    for target in targets:
      tdatetime = datetime.strptime(target["date"]["register"], '%Y/%m/%d %H:%M:%S')
      if tdatetime.year == today.year \
        and tdatetime.month == today.month \
        and tdatetime.day == today.day:
        scan_found_results.append(target)
    return scan_found_results
    
  def get_scan_error(self):
    ret = self.get_scan()
    return ret["error_hosts"] if "error_hosts" in ret else []

  def get_scan_param(self):
    ret = self.get_scan()
    return ret["param"] if "param" in ret else {}

  def get_targets_count(self):
    self.select_coll_targets()
    return self.__co.count()

  def get_scout_result(self):
    self.select_coll_targets()
    ret = { 
            "success_count": self.__co.find({"error.occur": False}).count(),
            "fail_count": self.__co.find({"error.occur": True}).count(),
            "scan_success_count": len(self.get_scan_found_results()),
            "vulnerable_match_count": 0
          }
    return ret

  def set_scan(self, json):
    self.select_coll_scan()
    self.__co.save(json)
    return

  def set_scan_error(self, error_list):
    ret = self.get_scan()
    ret["error_hosts"] = error_list
    self.set_scan(ret)
    return

  def set_scan_param(self, json):
    ret = self.get_scan()
    ret["param"] = json
    self.set_scan(ret)
    return

  def set_scan_param_snmp(self, comm_list):
    ret = self.get_scan_param()
    ret["snmp"] = {"community": comm_list}
    self.set_scan_param(ret)
    return

  def set_scan_param_ignorenw(self, nw_list):
    ret = self.get_scan_param()
    ret["ignore_nw"] = nw_list
    self.set_scan_param(ret)
    return

  def set_category(self, id, main, sub=""):
    if id and main:
      self.select_coll_targets()
      target = self.__co.find_one({"_id": objectid.ObjectId(id)})
      if target:
        target["category"] = {"main": main, "sub": sub}
        self.__co.save(target)
        return True
    return False


  def close(self):
    self.__client.close()

