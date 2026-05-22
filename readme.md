mkdir odt_to_html
cd odt_to_html
python -m venv .venv
.venv\Scripts\activate
	Ha sikerült, ezt látod:
	(.venv) C:\projekt\odt-html-converter>
pip install PySide6
pip install odfpy
------------------------------------
Első tesztprogram

main.py
-------
from PySide6.QtWidgets import QApplication, QLabel

app = QApplication([])

label = QLabel("Hello PySide6")
label.resize(300, 100)
label.show()

app.exec()
-------

Indítás:

python main.py
------------------------------------
pip install pyside6-addons
pyside6-designer
------------------------------------
Github

Igen, a .venv könyvtárat kifejezetten nem ajánlott feltölteni GitHub-ra.

A virtuális környezet:

gépfüggő,
platformfüggő,
nagy méretű,
újragenerálható.
✔ Mit tölts fel helyette?
1. .gitignore

A projekt gyökerébe:

.venv/
__pycache__/
*.pyc

minimum ezt érdemes.

PySide6 projektnél jó verzió:

# Virtual env
.venv/

# Python cache
__pycache__/
*.pyc

# Qt Designer cache
*.qmlc

# IDE
.vscode/
.idea/

# OS
.DS_Store
Thumbs.db
✔ 2. requirements.txt

Ez helyettesíti a .venv-et.

Generálás:

pip freeze > requirements.txt

Ez tartalmazza:

PySide6==...
odfpy==...
✔ 3. Hogyan tudja más újraépíteni?

Klónozás után:

python -m venv .venv

aktiválás:

Windows:

.venv\Scripts\activate

utána:

pip install -r requirements.txt

és ugyanaz a környezet felépül.

------------------------------------
