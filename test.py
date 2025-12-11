from zwutils.payroll import Payroll
from zwutils.pdf import generate_payslip_pdf

# Create payroll
salary_slip = Payroll(
    first_name="Munyaradzi", 
    last_name="Chirove",
    company="Obsidian XI",
    company_address="232 Cnr First and Mandela Harare Zimbabwe",
    company_phone="+263 78 610 3016",company_email="chirovemunyaradzi@gmail.com",
    department="IT",
    period="December 2025",
    employee_id="EMP-232377",
    currency="USD",
    total_leave_days=11,
    leave_days_taken=3,
    date_of_joining="12/03/2025"
)
# Add earnings
salary_slip.add_earning(name="Basic Salary",amount=1000,track_nssa=True)
salary_slip.add_earning("Bonus", 200,track_nssa=False)
salary_slip.add_earning("Transport Allowance", 50)

# Add deductions
salary_slip.add_deduction(name="Fuel", amount=120)
salary_slip.add_deduction(name="NSSA", amount=20)
salary_slip.add_deduction(name="PAYE", amount=250)
salary_slip.add_deduction(name="ZIBAWU", amount=80)
salary_slip.add_deduction(name="AIDS Levy", amount=7.5)
salary_slip.add_deduction(name="Loan Repayment", amount=343)
salary_slip.add_deduction(name="UFAWUZ", amount=343)
salary_slip.finalize_deductions()
salary_slip.rearrange_deductions()


generate_payslip_pdf(
    payroll=salary_slip,
    output_path="payslip.pdf",
    template_dir="zwutils/templates",
    logo_path="zwutils/logo.webp"
)