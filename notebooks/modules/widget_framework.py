from IPython.html import widgets
from IPython.utils import traitlets
from IPython.display import display

class framework():
    def __init__(self):
        self._state = ""
        
        #global defaults
        self._default_io_style = {}
        self._default_display_style = {}

        #object lists
        self._object_list = {}
        self._link_object = {}

        #state specific properties
        self._attributes = {}
        self._links = {}
        self._callbacks = {}
        self._children = {}
        self._roots = {}
        
        #registration lists
        self._state_list = []
        self._display_list = []
        self._io_list = []

        self.add_state("default")
        
    def update(self):
        self._update()#apply all default settings
        if self._state != "default":
            self._update(self._state)#apply state specific settings
        
    def _update(self, state="default"):
        if state == "default":
            for obj_name in self._object_list:
                if obj_name in self._display_list:
                    self.set_attributes(obj_name, **self._default_display_style)
                elif obj_name in self._io_list:
                    self.set_attributes(obj_name, **self._default_io_style)
                else:
                    raise ValueError("the object: "+obj_name+" is not assigned as a io or display object")
                self._object_list[obj_name].visible=False

        if state in self._attributes:
            for obj_name in self._attributes[state]:
                self.set_attributes(obj_name, **self._attributes[state][obj_name])
                
        if state in self._links:
            for obj_name in self._links[state]:
                for link_name in self._link_object:
                    self._link_object[link_name].unlink()
                self._link_objects = {}
                for link_name in self._links[state]:
                    directional, links_list = self._links[state][link_name]
                    links = []
                    for link in links_list:
                        links.append((self._object_list[link[0]], link[1]))
                    if directional:
                        self._link_objects[link_name] = traitlets.dlink(*links)
                    else:
                        self._link_objects[link_name] = traitlets.link(*links)
        
        if state in self._callbacks:
            for obj_name in self._callbacks[state]:
                for type in self._callbacks[state][obj_name]:
                    if hasattr(self._object_list[obj_name], type):
                        if type == "on_trait_change":
                            self._object_list[obj_name].on_trait_change(*self._callbacks[state][obj_name][type])
                        elif type == "on_click":
                            self._object_list[obj_name].on_click(self._callbacks[state][obj_name][type][0])
                        elif type == "on_submit":
                            self._object_list[obj_name].on_submit(self._callbacks[state][obj_name][type][0])
                        else:
                            raise ValueError("Widget have no method called: "+type)

        if state in self._children:
            for obj_name in self._children[state]:
                children_list = [self._object_list[child_name] for child_name in self._children[state][obj_name]]
                self._object_list[obj_name].children = children_list
        
#        if state in self._roots:
#            if len(self._roots[state]) > 0:
#                root_list = [self._object_list[obj_name] for obj_name in self._roots[state]]
#                display(*root_list)

    def add_state(self, state_name):
        if state_name in self._state_list:
            raise ValueError("the state: "+state_name+" is already defined!")
        else:
            self._state_list.append(state_name)
    
    def switch_state(self, state):
        if state in self._state_list:
            self._state = state
            self.update()
        else:
            raise ValueError("no state: "+state+" defined!")

    def set_state_callbacks(self, obj_name, callback, attribute=None, state="default", type="on_trait_change"):
        """ 
        Set callback for the object obj_name when the state is state.
        type must be one of "on_trait_change", "on_click", "on_submit"
        """
        if obj_name in self._object_list:
            if state in self._state_list:
                if type in ["on_trait_change", "on_click", "on_submit"]:
                    if not (state in self._callbacks):
                        self._callbacks[state]={}
                    if not (obj_name in self._callbacks[state]):
                        self._callbacks[state][obj_name]={}
                    if (type == "on_trait_change") and (attribute==None):
                        raise ValueError("if type == 'on_trait_change' then attribute must be defined")
                    self._callbacks[state][obj_name][type] = [callback, attribute]
                else:
                    raise ValueError("no callback: "+type+" defined!")
            else:
                raise ValueError("no state: "+state+" defined!")
        else:
            raise ValueError("no object: "+obj_name+" defined!")
            
    def set_state_links(self, link_name, links, state="default", directional=False):
        """ 
        Set links for the state. links should be of the form [("obj_name", "atribute"), ("obj_name", "attribute")]
        """
        if state in self._state_list:
            if not (state in self._links):
                self._links[state]={}
            if not (link_name in self._links[state]):
                self._links[state][link_name]=[]
            self._links[state][link_name] = [directional, links]
        else:
            raise ValueError("no state: "+state+" defined!")
            
    def set_state_attribute(self, obj_name, state="default", **kwargs):
        """ 
        Set attributes of the object: obj_name when the current state is state
        """
        if obj_name in self._object_list:
            if state in self._state_list:
                if not (state in self._attributes):
                    self._attributes[state]={}
                if not (obj_name in self._attributes[state]):
                    self._attributes[state][obj_name]={}
                for key in kwargs:
                    self._attributes[state][obj_name][key] = kwargs[key]
            else:
                raise ValueError("no state: "+state+" defined!")
        else:
            raise ValueError("no object: "+obj_name+" defined!")
            
    def set_state_children(self, obj_name, children, state="default"):
        """ 
        Set chidren of the display widgets, children should be a list of names
        """
        if state in self._state_list:
            if obj_name in self._display_list:
                if not (state in self._children):
                    self._children[state]={}
                if not (obj_name in self._children[state]):
                    self._children[state][obj_name] = []
                for child_name in children:
                    if child_name in self._object_list:
                        if not (child_name in self._children[state][obj_name]):
                            self._children[state][obj_name].append(child_name)
                    else:
                        raise ValueError("no object: "+child_name+" defined!")
            else:
                if obj_name in self._object_list:
                    raise ValueError("object: "+obj_name+" must be a display object to be a parent object")
                else:
                    raise ValueError("no object: "+obj_name+" defined!")
        else:
            raise ValueError("no state: "+state+" defined!")
    
    def set_state_root_objects(self, roots, state="default"):
        """ 
        Set root objects for the state, roots should be a list of names.
        """
        if state in self._state_list:
            if not (state in self._roots):
                self._roots[state] = []
            for obj_name in roots:
                if obj_name in self._object_list:
                    if not (obj_name in self._roots[state]):
                        self._roots[state].append(obj_name)
                else:
                    raise ValueError("no object: "+obj_name+" defined!")
        else:
            raise ValueError("no state: "+state+" defined!")
   
    def add_display_object(self, obj_name):
        """ 
        add display widget, these widgets should all be container type
        widgets.
        """
        if (obj_name in self._display_list) or (obj_name in self._object_list):
            raise ValueError("The object: " + obj_name+" is already defined!")
        else:
            self._display_list.append(obj_name)
            self._object_list[obj_name] = None

    def add_io_object(self, obj_name):
        """ 
        add io widget.
        """
        if (obj_name in self._io_list) or (obj_name in self._object_list):
            raise ValueError("The object: " + obj_name+" is already defined!")
        else:
            self._io_list.append(obj_name)
            self._object_list[obj_name] = None
            
    def set_object(self, obj_name, object):
        if obj_name in self._object_list:
            self._object_list[obj_name] = object
        else:
            raise ValueError("The object: "+obj_name+" is not defined!")
        
    def set_default_io_style(self, **kwargs):
        self._default_io_style = kwargs
        
    def set_default_display_style(self, **kwargs):
        self._default_display_style = kwargs
        
    def set_attributes(self, obj_name, **kwargs):
        if obj_name in self._object_list:
            obj = self._object_list[obj_name]
            for attr in kwargs:
                if hasattr(obj,attr):
                    setattr(obj, attr, kwargs[attr])
                else:
                    raise AttributeError(obj_name+" does not have attribute "+attr)
        else:
            raise ValueError("The object: "+obj_name+" is not defined!")

    def get_attribute(self, obj_name, attribute):
        if obj_name in self._object_list:
            obj = self._object_list[obj_name]
            if hasattr(obj,attribute):
                return getattr(obj, attribute)
            else:
                raise AttributeError(obj_name+" does not have attribute "+attribute)
        else:
            raise ValueError("The object: "+obj_name+" is not defined!")
            
