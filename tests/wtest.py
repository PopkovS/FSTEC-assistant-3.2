import datetime

import winrm

sess = winrm.Session('c421varganov', auth=(r'safib\varganov', '1qaz@WSX'), transport='ntlm')
# sess.run_cmd('DEL /F /S /Q /A "C:\Program Files (x86)\Ассистент\log\*"')
# sess.run_cmd('type "C:\Program Files (x86)\Ассистент\log\AstCln200512_15060.log"')
r = sess.run_cmd('type "C:\Program Files (x86)\Ассистент\log\AstCln*"')
# print(r.std_out.decode("utf8", "replace"))

if "Answer id-srv for func #1 process done" in r.std_out.decode("utf8", "replace"):
    print('Есть')
else:
    print("Нет")