from import_from_object import ModuleContainer

mondo = ModuleContainer("mondo")

from mondo import ciao, come

ciao()
come()

coso = ModuleContainer("coso")

import coso

coso.ciao()
coso.come()
