from flask import Blueprint, render_template, redirect, url_for, flash, request
from app import db
from app.models.company import Company
from app.forms.company import CompanyForm

company_bp = Blueprint('company', __name__)

@company_bp.route('/')
def index():
    companies = Company.query.all()
    return render_template('company/index.html', companies=companies)

@company_bp.route('/new', methods=['GET', 'POST'])
def new():
    form = CompanyForm()
    if form.validate_on_submit():
        company = Company(
            name=form.name.data,
            total_mandays=form.total_mandays.data
        )
        db.session.add(company)
        db.session.commit()
        flash('Company added successfully!', 'success')
        return redirect(url_for('company.index'))
    return render_template('company/form.html', form=form, title='Add Company')

@company_bp.route('/<int:id>/edit', methods=['GET', 'POST'])
def edit(id):
    company = Company.query.get_or_404(id)
    form = CompanyForm(obj=company)
    if form.validate_on_submit():
        company.name = form.name.data
        company.total_mandays = form.total_mandays.data
        db.session.commit()
        flash('Company updated successfully!', 'success')
        return redirect(url_for('company.index'))
    return render_template('company/form.html', form=form, title='Edit Company')

@company_bp.route('/<int:id>/delete', methods=['POST'])
def delete(id):
    company = Company.query.get_or_404(id)
    db.session.delete(company)
    db.session.commit()
    flash('Company deleted successfully!', 'success')
    return redirect(url_for('company.index'))

@company_bp.route('/<int:id>')
def view(id):
    company = Company.query.get_or_404(id)
    return render_template('company/view.html', company=company) 