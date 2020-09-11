import os
from time import sleep

# output = os.popen("tasklist | findstr /I ass").read()
i = 0
# print(output)
while True:

    output = os.popen("tasklist | findstr /I assis").read()
    if "Assistant.exe" in output:
        print(output)
        sleep(0.5)
        continue
    else:
        i += 1
        print('------------------------------------------')
        print("Test #" + str(i))
        print("Запуск ассистента C:\Program Files (x86)\Ассистент\Assistant.exe")
        os.system(r'C:\"Program Files (x86)"\Ассистент\Assistant.exe')
        while True:
            output = os.popen("tasklist | findstr /I assis").read()
            if "Assistant.exe" in output:
                print("Ожидаеся запуск...")
                sleep(0.5)
                break
        print('------------------------------------------')
        continue
