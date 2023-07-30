#Some imports
from krita import DockWidgetFactory, DockWidgetFactoryBase
from .esins_shading_helper import *

#Defining the docker and stuff
DOCKER_ID = 'shading_helper'
instance = Krita.instance()
ShadingDocker = DockWidgetFactory(DOCKER_ID,
                                        DockWidgetFactoryBase.DockRight,
                                        EsinsShadingDocker)

#Adding the docker (I think)
instance.addDockWidgetFactory(ShadingDocker)
