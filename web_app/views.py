from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from .models import Project, Ticket
from . import db

views = Blueprint('views', __name__)

# @ is a decorator that usese the below finction when it is hit
@views.route('/', methods=['GET'])
@login_required
def get_out():
    return redirect(url_for('views.projects'))

@views.route('/projects', methods=['GET', 'POST'])
@login_required
def projects():
    if request.method == 'POST':
        project_name = request.form.get('project_name')
        project_desc = request.form.get('project_desc')
        if len(project_name) < 1:
            flash('Project name must be greater than 1 character', category='error')
        elif len(project_name) > 50:
            flash('Project name must be less than 50 characters', category='error')
        elif len(project_desc) > 150:
            flash('Project description must be less than 150 characters', category='error')
        elif len(project_desc) == 0:
            flash('Project description cannot be blank.', category='error')
        elif len(project_name) == 0:
            flash('Project name cannot be blank.', category='error')
        else:
            flash('Project created.', category='success')
            new_project = Project(name=project_name, description=project_desc, user_id=current_user.id)
            db.session.add(new_project)
            db.session.commit()
        
    return render_template("projects.html", user=current_user)

@views.route('/projects/<project_id>', methods=['GET', 'POST'])
def view_project(project_id):
    project = Project.query.get(project_id)
    if request.method == 'POST':
        ticket_name = request.form.get('ticket_name')
        ticket_desc = request.form.get('ticket_desc')
        ticket_priority = request.form.get('priority')
        flash('Ticket created.', category='success')
        new_ticket = Ticket(name=ticket_name, description=ticket_desc, priority=ticket_priority, status="New", project_id=project.id)
        db.session.add(new_ticket)
        db.session.commit()

    return render_template("new_projects_view.html", user=current_user, current_project=project)

@views.route('/delete-project/<project_id>', methods=['GET', 'POST'])
def delete_project(project_id):
    project = Project.query.get(project_id)
    if project:
        if project.user_id == current_user.id:
            flash('Project deleted.', category='success')
            # delete the project's tickets before deleting the project itself
            for ticket in project.tickets:
                print("deleting ticket number " + str(ticket.id))
                db.session.delete(ticket)
            db.session.delete(project)
            db.session.commit()
        else:
            flash('You do not have permissions to delete that project', category='error')
    else:
        flash('That project does not exist.', category='error')

    return redirect(url_for('views.projects'))

# ticket related routes
@views.route('/delete-ticket/<ticket_id>', methods=['GET'])
def delete_ticket(ticket_id):
    ticket = Ticket.query.get(ticket_id)
    if ticket:
        # grab project id for redirect before deleting
        project_id = ticket.project_id
        flash('Ticket deleted', category='success')
        db.session.delete(ticket)
        db.session.commit()
    else:
        flash('Ticket does not exist', category='error')

    return redirect(url_for('views.view_project', project_id=project_id))

@views.route('/move-ticket/<ticket_id>/<destination>', methods=['GET'])
def move_ticket(ticket_id, destination):
    ticket = Ticket.query.get(ticket_id)
    if ticket:
        is_changed = True
        # update the ticket status
        if destination == "New":
            ticket.status = "New"
        elif destination == "Progress":
            ticket.status = "Progress"
        elif destination == "Review":
            ticket.status = "Review"
        elif destination == "QA":
            ticket.status = "QA"
        elif destination == "Complete":
            ticket.status = "Complete"
        else:
            is_changed = False
            flash('Ticket status does not exist', category='error') 
        # update db if ticket change happened
        if is_changed == True:
            db.session.commit()
    else:
        flash('Ticket does not exist', category='error')

    return redirect(url_for('views.view_project', project_id=ticket.project_id))

@views.route('/view-ticket/<ticket_id>', methods=['GET', 'POST'])
def view_ticket(ticket_id):
    ticket = Ticket.query.get(ticket_id)
    if request.method == 'POST':
        new_ticket_name = request.form.get('ticket_name')
        new_ticket_desc = request.form.get('ticket_desc')
        new_ticket_priority = request.form.get('priority')
        ticket.name = new_ticket_name
        ticket.description = new_ticket_desc
        ticket.priority = new_ticket_priority
        db.session.commit()

    return render_template("ticket_view.html", user=current_user, current_ticket=ticket)

