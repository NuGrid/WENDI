from IPython.display import FileLink, FileLinks
import sys

def grab_session(name):
    '''
    Get a download link a notebook session.
        
    Parameters
    ----------
    name : string
        The name of the session that you want to grab.
        
    Examples
    --------
    
    grab_session('my_first_notebook')
    '''
    if '.ipynb' not in name: name += '.ipynb'
    try:
        FileLink('~/notebooks/'+name)
    except:
        print 'session '+name+' not available.'

def load_session(name,vos=False):
    '''
    Load a notebook session from either VOspace (only for
    authenticated users) or from a public GitHub repository.
        
    The notebook will appear in the notebook home directory.
        
    Parameters
    ----------
    name : string
        The name of the notebook session to load. This is either
        the full URL of the .ipynb file in the GitHub repository
        or the name of the notebook as it appears in your VOSpace
        notebook directory.
    vos : boolean, optional
        Is the notebook session to be loaded from your VOSpace?
        (For authenticated users only)
        The default is False.
    '''

    if not vos:
        try:
            os.system("wget "+name)
        except:
            print 'could not get '+name

    else:
        print "vcp from user's VOSpace is not yet implemented"

def save_session(name):
    '''
    Permanently save a notebook session in the user's VOSpace.
    (only for authenticated users)
    '''

    print "vcp from user's VOSpace is not yet implemented"













