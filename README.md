anarcho
=======

Android archives hosting

Setup environment:
```
    virtualenv venv --no-site-packages
    source venv/bin/activate
```
 
Install from PyPi:
```
    pip install anarcho

```

Start:
```
    anarcho init_db
    anarcho start
```

===================================================
Prepare for develop:
```
    python setup.py develop
```

Fill db with some stub data:
```
    anarcho init_db_stub
```

Start for develop:
```
    anarcho start_dev
```
