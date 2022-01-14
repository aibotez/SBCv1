import os
if os.path.exists('view_zyh.py'):
    os.rename('view_zyh.py','view_zyh1.py')
else:
    os.rename('view_zyh1.py','view_zyh.py')
