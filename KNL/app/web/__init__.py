from flask import Blueprint,render_template

web = Blueprint('web',__name__)

@web.app_errorhandler(404)
def not_found(e):
    #AOP思想 面向切片编程
    return render_template('404.html'),404



from . import auth
from . import main
from . import api
#from . import book
#from . import drift
#from . import gift
#from . import wish
#from app.user import *
