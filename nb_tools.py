from IPython.display import FileLink, FileLinks
import os
import subprocess

def get_user_and_token():
    '''
    Try to get authenticated user's CANFAR username
    and token from the token file. If there is no
    token file, then the user is ananymous.
    '''

    try:
        token_file = '/home/nugrid/.token'
    except:
        return None, None

#    TOKEN = subprocess.check_output('cat '+token_file)
#    part = subprocess.check_output('echo " ' + TOKEN + ' " | cut -d"&" -f1')
#    canfaruser = subprocess.check_output('echo " ' + part + ' " | cut -d"=" -f2')

    TOKEN = os.popen('cat '+token_file).read().replace('\n','')
    part = os.popen('echo " ' + TOKEN + ' " | cut -d"&" -f1').read().replace('\n','')
    canfaruser = os.popen('echo " ' + part + ' " | cut -d"=" -f2').read().replace('\n','')
    canfaruser = canfaruser.strip()

    return canfaruser, TOKEN

def list_sessions():
    '''
    List all sessions in the user's NuGrid VOSpace user directory
    '''

    canfaruser, TOKEN = get_user_and_token()
    
    if canfaruser is None:
        print 'You must be authenticated to do that.'
    else:
        command = 'vls vos:nugrid/nb-users/'+canfaruser+\
            '/notebooks --token="'+TOKEN+'" '
#        print command
        out = os.popen(command).read()
        print out

def pull_session(name):
    '''
    Pull session into running container.
        
    Parameters
    ----------
    name : string
        The name of the session that you want to pull.
        
    Examples
    --------
    
    pull_session('my_first_notebook')
    '''
    if '.ipynb' not in name: name += '.ipynb'

    canfaruser, TOKEN = get_user_and_token()
    if canfaruser is None:
        print 'You must be authenticated to do that.'
    else:
        command = 'vcp vos:nugrid/nb-users/'+canfaruser+\
            '/notebooks/'+name+' . --token="'+TOKEN+'" '
#        print command
        os.system(command)


def save_session(name):
    '''
    Save a notebook session to your NuGrid VOspace user
    directory (only for authenticated users).
        
    The notebook will appear in the notebook home directory.
        
    Parameters
    ----------
    name : string
        The name of the notebook session to load. This is either
        the full URL of the .ipynb file in the GitHub repository
        or the name of the notebook as it appears in your VOSpace
        notebook directory.
    '''
    if '.ipynb' not in name: name += '.ipynb'
    
    canfaruser, TOKEN = get_user_and_token()
    if canfaruser is None:
        print 'You must be authenticated to do that.'
    else:
        command = 'vcp '+name+' vos:nugrid/nb-users/'+canfaruser+\
            '/notebooks/'+name+' --token="'+TOKEN+'" '
#        print command
        os.system(command)














