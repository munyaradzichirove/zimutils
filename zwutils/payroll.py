# zwutils/payroll.py

class Payroll:
    def __init__(
        self,
        first_name,
        last_name,
        company=None,
        department=None,
        company_address=None,
        company_phone=None,
        company_email=None,
        period=None,
        employee_id=None,
        currency="USD",
        template=None,
        designation=None,
        date_of_joining=None,
        total_leave_days=None,
        leave_days_taken=None
        
    ):
        self.first_name = first_name
        self.last_name = last_name
        self.company = company
        self.department = department
        self.designation = designation
        self.company_address = company_address
        self.company_phone = company_phone
        self.company_email = company_email
        self.period = period
        self.employee_id = employee_id
        self.currency = currency
        self.template = template
        self.date_of_joining = date_of_joining
        self.total_leave_days=total_leave_days
        self.leave_days_taken=leave_days_taken

        # Components
        self.earnings = []    
        self.deductions = []    

        self.track_nssa_balance=0
        self.total_ensurable=0
        self.allowable_deduction=0

        self.nssa_percentage=0.045
        self.aids_levy_percentage=0.015

    def add_earning(self, name, amount,track_nssa=False,is_taxable=False):
        """Add an earning component, raise error if invalid"""
        if not name:
            raise ValueError("Earning name cannot be empty or None")
        if amount is None or amount == 0:
            raise ValueError("Earning amount cannot be None or 0")
        if track_nssa:
            self.track_nssa_balance += amount
        if is_taxable:
            self.total_ensurable +=amount
        self.earnings.append({"name": name, "amount": amount})

    def add_deduction(self, name, amount=None, is_allowable_deduction=False, percentage=0):
        name_upper = name.upper()

        # --- VALIDATION ---
        if name_upper == "AIDS LEVY":
            # Check PAYE exists BEFORE adding AIDS LEVY
            paye_exists = any(d['name'].upper() == "PAYE" for d in self.deductions)
            if not paye_exists:
                raise ValueError("Cannot add AIDS Levy before PAYE has been added.")

        # --- SPECIAL DEDUCTIONS ---
        if name_upper in ["NSSA", "PAYE", "AIDS LEVY"]:
            # Add placeholder only if not already added
            if not any(d['name'].upper() == name_upper for d in self.deductions):
                self.deductions.append({"name": name_upper, "amount": 0})
                if name_upper == "AIDS LEVY":
                    # Set the AIDS Levy percentage, default to 0.3 if not specified
                    self.aids_levy_percentage = percentage if percentage > 0 else 0.3
            deduction_amount = 0

        # --- NORMAL DEDUCTIONS ---
        else:
            if amount is None:
                raise ValueError(f"Amount must be provided for {name}")
            self.deductions.append({"name": name, "amount": amount})
            deduction_amount = amount

        # --- ALLOWABLE DEDUCTIONS ---
        if is_allowable_deduction:
            self.allowable_deduction += deduction_amount


    def total_earnings(self):
        return sum(e["amount"] for e in self.earnings)

    def total_deductions(self):
        return sum(d["amount"] for d in self.deductions)

    def net_salary(self):
        return self.total_earnings() - self.total_deductions()

    def summary(self):
        print(f"Payroll for {self.first_name} {self.last_name} - {self.period} ({self.currency})")
        print("Earnings:")
        for e in self.earnings:
            print(f"  {e['name']}: {e['amount']}")
        print("Deductions:")
        for d in self.deductions:
            print(f"  {d['name']}: {d['amount']}")
        print(f"Net Salary: {self.net_salary()}")

    def finalize_deductions(self):
        """Calculate NSSA, PAYE, and AIDS Levy in their reserved positions, and add 100 to amounts if they exist."""
        paye_amount=0

        # Check if NSSA exists and add 100 to its amount if it does
        nssa = next((d for d in self.deductions if d['name'].upper() == "NSSA"), None)
        if nssa:
            nssa['amount'] = 100  # Add 100 to NSSA amount
            # nssa['amount'] = self.track_nssa_balance * self.nssa_percentage  # Recalculate based on track_nssa_balance

        # Check if PAYE exists and add 100 to its amount if it does
        paye = next((d for d in self.deductions if d['name'].upper() == "PAYE"), None)
        if paye:
            paye['amount'] = 100  # Add 100 to PAYE amount
            # taxable_income = self.total_taxable_income - self.allowable_deduction  # Calculate taxable income
            # paye['amount'] = taxable_income * 0.25  # Recalculate PAYE amount
            paye_amount=100

        # Check if AIDS LEVY exists and add 100 to its amount if it does
        aids_levy = next((d for d in self.deductions if d['name'].upper() == "AIDS LEVY"), None)
        if aids_levy:
            aids_levy['amount'] = 100  # Add 100 to AIDS LEVY amount
            # paye_amount = next((d['amount'] for d in self.deductions if d['name'].upper() == "PAYE"), None)
            if paye_amount:
                aids_levy['amount'] = paye_amount * self.aids_levy_percentage  # Recalculate AIDS Levy based on PAYE


    def rearrange_deductions(self):
        """Rearrange deductions list so that NSSA is first, followed by PAYE and AIDS Levy."""
        # Sort the deductions list to ensure NSSA, PAYE, and AIDS LEVY are in the correct order
        order = ["NSSA", "PAYE", "AIDS LEVY"]
        # Create a new sorted list based on the order of special deductions
        self.deductions.sort(key=lambda x: order.index(x['name'].upper()) if x['name'].upper() in order else len(order))