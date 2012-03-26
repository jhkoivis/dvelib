

class copySshKeys:
    
    def __init__(self):
        """
        Nothing
        """
        a = 1
        
    def everything(self):
        """
        TODO
        ssh-keygen -t rsa
          <enter>
          <enter>
          <enter>
        scp id_rsa.pub remoteMachine:~/.ssh/id_rsa_this_machine_name.pub
        ssh remoteMachine 'cat ~/.ssh/id_rsa_this_machine_name.pub >> ~/.ssh/known_hosts'
        ssh remoteMachine eval ssh-agent
        eval ssh-agent
        """
        a=1