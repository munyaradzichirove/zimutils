import base64
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
import os

def load_base64_image(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

def generate_payslip_pdf(payroll, output_path, template_dir):
    # Load logo as base64
    try: 

         logo_base64 = load_base64_image(payroll.logo_path)
    except:
        logo_base64=''


    # Load HTML template
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template("payslip_template.html")

    html_content = template.render(
        # --- Company Info ---
        company=payroll.company,
        company_address=payroll.company_address,
        company_phone=payroll.company_phone,
        company_email=payroll.company_email,

        # --- Employee Info ---
        employee_id=payroll.employee_id,
        first_name=payroll.first_name,
        last_name=payroll.last_name,
        department=payroll.department,
        designation=payroll.designation,
        date_of_joining=payroll.date_of_joining,
        total_leave_days=payroll.total_leave_days,
        leave_days_taken=payroll.leave_days_taken,
        period=payroll.period,

        # --- Salary ---
        earnings=payroll.earnings,
        deductions=payroll.deductions,
        total_earnings=payroll.total_earnings(),
        total_deductions=payroll.total_deductions(),
        net_salary=payroll.net_salary(),
        tax_credits=payroll.total_tax_credits(),

        # --- System ---
        powered_by="ZWUtils",
        logo_base64=logo_base64,
    )

    # Generate PDF
    HTML(string=html_content).write_pdf(output_path)
