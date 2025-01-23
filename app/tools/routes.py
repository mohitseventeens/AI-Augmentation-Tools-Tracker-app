from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.tools.forms import ToolForm
from app.models import Tool, Tag

tools_bp = Blueprint('tools', __name__)

@tools_bp.route('/tools')
@login_required
def index():
    tools = Tool.query.filter_by(user_id=current_user.id).all()
    return render_template('tools/index.html', tools=tools)

@tools_bp.route('/tools/add', methods=['GET', 'POST'])
@login_required
def add_tool():
    form = ToolForm()
    if form.validate_on_submit():
        tool = Tool(
            name=form.name.data,
            category=form.category.data,
            description=form.description.data,
            url=form.url.data,
            notes=form.notes.data,
            rating=form.rating.data,
            user_id=current_user.id
        )
        db.session.add(tool)
        db.session.commit()
        flash('Tool added successfully!', 'success')
        return redirect(url_for('tools.index'))
    return render_template('tools/add.html', form=form)

@tools_bp.route('/tools/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_tool(id):
    tool = Tool.query.get_or_404(id)
    if tool.user_id != current_user.id:
        flash('You are not authorized to edit this tool', 'danger')
        return redirect(url_for('tools.index'))
    
    form = ToolForm(obj=tool)
    if form.validate_on_submit():
        tool.name = form.name.data
        tool.category = form.category.data
        tool.description = form.description.data
        tool.url = form.url.data
        tool.notes = form.notes.data
        tool.rating = form.rating.data
        db.session.commit()
        flash('Tool updated successfully!', 'success')
        return redirect(url_for('tools.index'))
    return render_template('tools/edit.html', form=form, tool=tool)

@tools_bp.route('/tools/<int:id>/delete', methods=['POST'])
@login_required
def delete_tool(id):
    tool = Tool.query.get_or_404(id)
    if tool.user_id != current_user.id:
        flash('You are not authorized to delete this tool', 'danger')
        return redirect(url_for('tools.index'))
    
    db.session.delete(tool)
    db.session.commit()
    flash('Tool deleted successfully', 'success')
    return redirect(url_for('tools.index'))