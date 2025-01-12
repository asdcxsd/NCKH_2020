from Framework.Valueconfig import ValueStatus
from re import escape
import docker
from docker.types import containers
client = docker.from_env()

class ImagesDocker:
    name = ""
    def __init__(self, name):
        self.name = name
    def __init__(self):
        pass
    def check_exist(self):
        if self.name == "":
            return True
        for img in client.images.list(all=True):
            for image_name in img.attrs['RepoTags']:
                if self.name in image_name :
                    return True
        return False
    def add_images(self, data):
        with open(data, "rb") as file:
            img =  client.images.load(file)
            self.name = img[0].attrs['RepoTags']
    def pull_images(self, link):
        try:
            image = client.images.pull(link)
        except Exception as e:
            print("Error pull images:", e)
    def remove_images(self):
        try:
            client.images.remove(self.name, force=True)
            return True
        except Exception as e:
            print("Error remove docker", e)
            return False

class ContainersDocker:
    name = ''
    name_container = ''
    container = None
    def __init__(self, name):
        self.name = name
    def __del__(self):
        self.remove_containers()
    def check_exist(self):
        if self.name == "":
            return False
        for container in client.containers.list(all=True):
            if self.name_container in container.name:
                self.container = container
                return True
        return False
    def run_containers(self, port = None, device = None , detachs =True ):
        images  = ImagesDocker()
        images.name = self.name
        if not images.check_exist(): 
            raise Exception("Images not exist!")
        if port != None and device != None:
            self.container = client.containers.run(image=self.name, ports =port ,devices=device, detach=detachs )
        elif port != None: 
            self.container = client.containers.run(image=self.name, ports =port, detach=detachs )
        elif device != None: 
            self.container = client.containers.run(image=self.name, devices=device, detach=detachs )
    def run_containers_cmd(self, *args, **kwargs ):
        images  = ImagesDocker()
        images.name = self.name
        if not images.check_exist(): 
            raise Exception("Images not exist!")
 
        self.container = client.containers.create(image=self.name, **kwargs)
        self.container.start()
        self.name_container = self.container.name

    def get_comtainers_output(self):
        status = self.containers_status 
        if status == ValueStatus.Running:
            return False, ValueStatus.Running
        elif status == False:
            return False, ValueStatus.Error
        else: 
            return True,  self.container.logs()
    
    def containers_status(self):
        if self.check_exist() == False:
            return False
        return self.container.status
    def remove_containers(self):
        if self.container != None:
            try:
                if self.check_exist():
                    self.container.stop()
                    self.container.remove()
                return True
            except Exception as e:
                print("Error docker:",e)
        return False
    def stop_containers(self):
        if self.container != None:
            try:
                if self.check_exist():
                    self.container.stop()
                return True
            except Exception as e:
                print("Error docker:",e)
        return False
class ContainerStatus():
    Running  = "running"
    Restarting = "restarting"
    Pause = "paused"
    Exited = "exited"
def run():
    name  = "rootzoll/web-screenshot"
    #sreenshort = ImagesDocker()
    container = ContainersDocker(name)
    container.run_containers()
    import time 
    time.sleep(10)
    #sreenshort.name = name
    #sreenshort.remove_images()
    #file = "/home/asdcxsd/project/NCKH_2020/docjer/web-screenshot.tar"
    #sreenshort.add_images(file)

    #print(sreenshort.name)
if __name__ == "__main__":
    run()    