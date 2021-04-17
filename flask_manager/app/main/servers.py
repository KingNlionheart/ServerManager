#!/usr/bin/python3
# @Time    : 2019-07-01
# @Author  : Kevin Kong (kfx2007@163.com)

# 用户安全相关
from flask import request, flash
from flask_login import login_required, current_user
from . import bp_main
from utils.view_util import render_template
from .forms import UserPassword
from utils.model_util import flash_errors
from app.model.servers import Server
from app.main.forms import ServerForm
from app.main.views import common_list, common_edit
from werkzeug.security import generate_password_hash
import math

@bp_main.route("/serverlist", methods=["GET"])
@login_required
def serverlist():
    id = request.args.get('id')
    page = request.args.get('page') if request.args.get('page') else 1
    length = request.args.get('length') if request.args.get('length') else 1
    name = request.args.get('name')
    ip = request.args.get('ip')
    port = request.args.get('port')
    user = request.args.get('user')
    passwd =  request.args.get('passwd')
    perm = request.args.get('perm')
    passcode = request.args.get('passcode')
    dict = {'name': name, 'ip': ip,'port': port,'user': user,'passwd': passwd,'perm': perm,'passcode': passcode,'total_page': 1, 'page': page, 'length': length}
    return render_template("server/serverlist.html", form=dict)


@bp_main.route("/serveredit", methods=["GET", "POST"])
@login_required
def serveredit():
    """用户编辑"""
    form = ServerForm()
    if request.method == "POST":
        form = ServerForm(request.form)
        if "password" in request.form:
            form.password.data  = generate_password_hash(request.form["password"])
    return common_edit(Server,form,"server/serveredit.html")
