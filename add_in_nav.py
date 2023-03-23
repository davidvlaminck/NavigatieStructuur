from __future__ import annotations

from pathlib import Path
from typing import List, Optional

import pydantic as pydantic
from pydantic import BaseModel


class NavElement(BaseModel):
    name: str
    children: Optional[List[NavElement]] = []
    uri: Optional[str]
    uitGebruik: bool

    def navigate_to(self, name: str) -> NavElement:
        return next((c for c in self.children if c.name == name), None)


class RootElement(BaseModel):
    name: str
    children: List[NavElement]

    def navigate_to(self, name: str) -> NavElement:
        return next((c for c in self.children if c.name == name), None)


NavElement.update_forward_refs()


if __name__ == '__main__':
    nav_json = pydantic.parse_file_as(path=Path('OTL_Navigatie_202239.json'), type_=RootElement)

    sb_270 = nav_json.navigate_to('SB270')
    sb_270.children.append(
        NavElement(name='Detectiesysteem', uitGebruik=False, children=[
            NavElement(name='Wilddetectiesysteem', uitGebruik=False, uri='https://wegenenverkeer.data.vlaanderen.be/ns/installatie#Wilddetectiesysteem'),
            NavElement(name='Bewegingssensor', uitGebruik=False, uri='https://wegenenverkeer.data.vlaanderen.be/ns/onderdeel#Bewegingssensor')
        ]))

    with open(Path('OTL_Navigatie_nieuw.json'), 'w') as file:
        file.write(nav_json.json())
