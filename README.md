# Zwutils Payroll Library

A lightweight Python library to generate payrolls and salary slips, calculate deductions (NSSA, PAYE, AIDS Levy), earnings, and tax credits. Includes PDF generation using customizable HTML templates.

## Features

- Add employee earnings, deductions, and tax credits.
- Automatic calculation of NSSA, PAYE, and AIDS Levy.
- Handles allowable deductions and taxable earnings.
- Generates professional salary slip PDFs using HTML templates.
- Dynamic company logos in PDFs.
- Supports multiple currencies.

## Installation

```bash
pip install zwutils

## USAGE


from zwutils.payroll import Payroll
from zwutils.pdf import generate_payslip_pdf

# Create payroll
salary_slip = Payroll(
    employee_id="EMP-232377",
    first_name="xxxxxxxxxxxx", 
    last_name="xxxxxxxxxx",
    company="XXXXXXXXXXX",
    company_address="xxxxxxxxxxx",
    company_phone="+263 78 610 3016",
    company_email="xxxxxxxxx",
    department="IT",
    designation="Employee",
    period="December 2025",
    currency="USD",
    total_leave_days=11,
    leave_days_taken=3,
    date_of_joining="12/03/2025",
    logo_path="logo.webp"
)
# Earnings
salary_slip.add_earning(name="Basic Salary",amount=500,track_nssa=True,is_taxable=True)
salary_slip.add_earning(name="Bonus",amount=200,track_nssa=False)
salary_slip.add_earning(name="Transport Allowance",amount= 50)

# Tax Credits
salary_slip.add_credits(name="Blind",amount= 50)

# Deductions
salary_slip.add_deduction(name="Fuel", amount=120)
salary_slip.add_deduction(name="NSSA")
salary_slip.add_deduction(name="PAYE")
salary_slip.add_deduction(name="ZIBAWU",is_allowable_deduction=True, percentage=2)
salary_slip.add_deduction(name="UFAWUZ", is_allowable_deduction=True, percentage=3)
salary_slip.add_deduction(name="LAPF", is_allowable_deduction=True, percentage=6)
salary_slip.add_deduction(name="ZESCWU", is_allowable_deduction=True, percentage=1.5)
salary_slip.add_deduction(name="NECWEI", is_allowable_deduction=True, percentage=1)
salary_slip.add_deduction(name="NEC", is_allowable_deduction=True, percentage=2.4)
salary_slip.add_deduction(name="AIDS Levy")
salary_slip.add_deduction(name="Loan Repayment", amount=343)
salary_slip.finalize_deductions()
salary_slip.rearrange_deductions()


# print(salary_slip.author())


generate_payslip_pdf(
    payroll=salary_slip,
    output_path="payslip.pdf",
    template_dir="zwutils/templates",

)

Requirements

Python 3.10+

Jinja2

WeasyPrint (for PDF generation)


License

MIT License


You can adjust `path_to_your_logo.webp` to reflect how you want users to provide their logo dynamically.  

