from datetime import datetime 
import hashlib 

ts = datetime.today().timestamp() 
bts = str(ts).encode()  

md5 = hashlib.md5() 
md5.update(bts)  

print(md5.hexdigest())
