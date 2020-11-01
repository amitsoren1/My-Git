# My-Git
A Python library to clone and create a new git repository

Steps to use it.


1.  git clone 

2.  cd My-Git\

3.  python setup.py install

4.
(from command line)

python mygit\upload.py --username="<username>" --password="password" --input_repo="https://github.com/username/public-repo.git" --output_repo_name="new repo"

5.
(In other modules)

from mygit.MyGit import GitRepository

a = GitRepository(username="username",password="password",input_repo="https://github.com/username/public-repo.git",output_repo_name="new repo")

a.authenticate()

a.clone_repo()

a.create_new_repo()

a.push_to_new_repo()
