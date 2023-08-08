import sys
import os

sys.path.append(os.path.dirname(__file__))
import imp
import devTemplate
imp.reload(devTemplate)
devTemplate.main()
g=devTemplate.g
