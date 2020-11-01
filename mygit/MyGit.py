import requests
import json

import string 
import random
import argparse

from git import Repo
import os
import shutil

class GitRepository:
    url = "https://api.github.com/authorizations"
    params = ("username","password","input_repo","output_repo_name",)
    remove_files = ("LICENCE.txt","README.md",)
    def __init__(self,**kwargs):
        for param in self.params:
            if param not in kwargs:
                raise Exception(f"missing, {param} keyword arguement")

        self.username = kwargs['username']
        self.password = kwargs['password']
        self.output_repo_name = kwargs['output_repo_name']
        self.input_repo = kwargs['input_repo']
        # self.authenticate()
    
    def authenticate(self):
        url = "https://api.github.com/authorizations"# urljoin(GITHUB_API, 'authorizations')
        payload = {
        "scopes": ["public_repo"],
        "note": ''.join(random.choice(string.ascii_letters) for i in range(10))
                    }
        res = requests.post(url,auth = (self.username, self.password),data = json.dumps(payload))
        if res.status_code == 401:
            self.authorization_id = None
            raise Exception("Authentication credentials are incorrect")
        self.token = res.json()['token']
        self.authorization_id = res.json()['id']
        return "authorized"
    
    def create_new_repo(self):
        payload = { "name": self.output_repo_name}
        res = requests.post("https://api.github.com/user/repos",headers={"Authorization": "token "+self.token},data = json.dumps(payload))
        # print(res.status_code)
        if res.status_code == 422:
            raise Exception(f"repository with name, {self.output_repo_name} already exists in remote")
        self.new_repo_name = res.json()['name']
        if res.status_code == 201:
            remote = f"https://{self.username}:{self.token}@github.com/{self.username}/{res.json()['name']}.git"
            Repo.clone_from(res.json()['clone_url'], os.path.join(os.getcwd(),res.json()['name']))
        curr = os.getcwd()

        src = os.path.join(curr,self.input_repo_name)
        dst = os.path.join(curr,res.json()['name'])

        os.chdir(src)

        for filename in os.listdir():
            if filename != ".git":
                if os.path.isdir(os.path.join(src,filename)):
                    shutil.copytree(os.path.join(src,filename),os.path.join(dst,filename))
                else:
                    shutil.copy(os.path.join(src,filename),dst)
        os.chdir(curr)
        return "success"

    def push_to_new_repo(self):
        status = 1
        while status==1:
            try:
                # print("trying")
                repo_dir = os.path.join(os.getcwd(),self.new_repo_name)
                repo = Repo(repo_dir)
                repo.git.add(".")
                repo.index.commit("First commit message")
                origin = repo.remote(name="origin")
                origin.push()
                status = 2
            except:
                continue
        return "success"
    
    def clone_repo(self):
        if self.input_repo[-1] == "/":
            self.input_repo_name = self.input_repo.split("/")[-2].split(".")[0]
        else:
            self.input_repo_name = self.input_repo.split("/")[-1].split(".")[0]
        repo_owner = self.input_repo.split("/")[3]
        remote = f"https://{self.username}:{self.token}@github.com/{repo_owner}/{self.input_repo_name}.git"
        Repo.clone_from(remote, os.path.join(os.getcwd(),self.input_repo_name))
        for item in self.remove_files:
            if os.path.exists(os.path.join(os.getcwd(),self.input_repo_name,item)):
                os.remove(os.path.join(os.getcwd(),self.input_repo_name,item))
        return "success"

    def clone_and_push(self):
        self.authenticate()
        self.clone_repo()
        self.create_new_repo()
        self.push_to_new_repo()
        print("done clonning and creating new repo")


if __name__ == '__main__':
    my_parser = argparse.ArgumentParser()
    for param in GitRepository.params:
        my_parser.add_argument('--'+param, action='store', type=str)
    args = my_parser.parse_args()
    # print(vars(args))
    obj = GitRepository(username=vars(args)['username'],password=vars(args)['password'],
            input_repo=vars(args)['input_repo'],output_repo_name=vars(args)['output_repo_name'])
    obj.clone_and_push()
