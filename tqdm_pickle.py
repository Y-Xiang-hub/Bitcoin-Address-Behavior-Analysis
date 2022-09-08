class TQDMBytesReader(object):

    def __init__(self, fd, **kwargs):
        self.fd = fd
        from tqdm import tqdm
        self.tqdm = tqdm(**kwargs)

    def read(self, size=-1):
        bytes = self.fd.read(size)
        self.tqdm.update(len(bytes))
        return bytes

    def readline(self):
        bytes = self.fd.readline()
        self.tqdm.update(len(bytes))
        return bytes
    def readinto(self,s):
        sz=self.fd.readinto(s)
        self.tqdm.update(sz)
        return sz

    def __enter__(self):
        self.tqdm.__enter__()
        return self

    def __exit__(self, *args, **kwargs):
        return self.tqdm.__exit__(*args, **kwargs)
        
import pickle,os

def load_file(fn:str):
    total = os.path.getsize(fn)
    with open(fn,"rb") as fd:
        with TQDMBytesReader(fd, total=total) as pbfd:
            return pickle.load(pbfd)
