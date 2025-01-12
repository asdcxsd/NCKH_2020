from Framework.Framework import Framework
from Application.Function.Connect_Framework import get_class_module
def main():
    testFrame = Framework()
    list_module = testFrame.get_list_of_module()
    print("ListModule")
    print(list_module)
    info_module = []
    for module in list_module:
        info_module.append(testFrame.get_info_main_module(module))
    print("InfoModule")
    print(info_module)

    ClassPocCheck = get_class_module("PocCheck", "module")
    objectPocCheck = ClassPocCheck()
    listPoC = objectPocCheck.get_all_pocs()
    print("ListPoc")
    print(listPoC)
    infoPoc = []
    for poc in listPoC:
        infoPoc.append(objectPocCheck.get_info_pocs(poc))
    print("InfoPoc")
    print(infoPoc)
if __name__ == "__main__":
    main()