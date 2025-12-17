# zwutils/payroll.py
class Payroll:
    def __init__(
        self,
        employee_id,
        first_name=None,
        last_name=None,
        company=None,
        department=None,
        company_address=None,
        company_phone=None,
        company_email=None,
        period=None,
        currency="USD",
        template=None,
        designation=None,
        date_of_joining=None,
        total_leave_days=None,
        leave_days_taken=None,
        logo_path=None,
        
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
        self.logo_path = logo_path

        # Components
        self.earnings = []    
        self.deductions = []    
        self.tax_credits = []    


        self.track_nssa_balance=0
        self.total_ensurable=0
        self.allowable_deduction=0
        self.total_taxable_income=0
        self.basic_salary=0

        self.nssa_percentage=0.0
        self.aids_levy_percentage=0.0

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
        if name.upper() == "BASIC SALARY":
            self.basic_salary += amount
        self.earnings.append({"name": name, "amount": amount})
    
    def add_credits(self, name, amount):
        """Add an earning component, raise error if invalid"""
        if not name:
            raise ValueError("Earning name cannot be empty or None")
        if amount is None or amount == 0:
            raise ValueError("Earning amount cannot be None or 0")
        self.tax_credits.append({"name": name, "amount": amount})


    def add_deduction(self, name, amount=None, is_allowable_deduction=False, percentage=0):
        name_upper = name.upper()

        # --- VALIDATION ---
        if name_upper == "AIDS LEVY":
            paye_exists = any(d['name'].upper() == "PAYE" for d in self.deductions)
            if not paye_exists:
                raise ValueError("Cannot add AIDS Levy before PAYE has been added.")

        # --- SPECIAL DEDUCTIONS ---
        if name_upper in ["NSSA", "PAYE", "AIDS LEVY"]:
            if not any(d['name'].upper() == name_upper for d in self.deductions):
                self.deductions.append({"name": name_upper, "amount": 0})
                if name_upper == "AIDS LEVY":
                    self.aids_levy_percentage = percentage if percentage > 0 else 3
                elif name_upper == "NSSA":
                    self.nssa_percentage = percentage if percentage > 0 else 4.5
        
        # --- ALLOWABLE DEDUCTIONS ---
        if is_allowable_deduction and name_upper not in ["NSSA", "PAYE", "AIDS LEVY"]:
            against = ""
            if name_upper == "NEC":
                against = self.total_ensurable
            else:
                against = self.basic_salary
                
            deduction_amount = percentage * against / 100
            self.allowable_deduction += deduction_amount
            self.deductions.append({"name": name, "amount": deduction_amount})
        # --- NORMAL DEDUCTIONS ---
        else:
            if amount is None and name_upper not in ["NSSA", "PAYE", "AIDS LEVY"]:
                raise ValueError(f"Amount must be provided for {name}")
            else:
                if name_upper not in ["NSSA", "PAYE", "AIDS LEVY"]:
                    self.deductions.append({"name": name, "amount": amount})
              
    def total_earnings(self):
        return sum(e["amount"] for e in self.earnings)
    def author(self):
        return "name: Munyaradzi Chirove | email :chirovemunyaradzi@gmail.com | Happy Coding!!!!"          
    def total_tax_credits(self):
        return sum(t["amount"] for t in self.tax_credits)


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

        nssa = next((d for d in self.deductions if d['name'].upper() == "NSSA"), None)
        if nssa:
            nssa_amount =self.nssa_percentage *  self.track_nssa_balance /100
            nssa['amount'] = nssa_amount
            self.allowable_deduction +=nssa_amount
        paye = next((d for d in self.deductions if d['name'].upper() == "PAYE"), None)
        if paye:
            self.total_taxable_income = self.total_ensurable - self.allowable_deduction
            paye['amount'] = max(self.payee_against_slab_usd(self.total_taxable_income)-self.total_tax_credits(),0)
        aids_levy = next((d for d in self.deductions if d['name'].upper() == "AIDS LEVY"), None)
        if aids_levy:
            paye_amount = next((d['amount'] for d in self.deductions if d['name'].upper() == "PAYE"), None)
            if paye_amount:
                aids_levy['amount'] = paye_amount * self.aids_levy_percentage /100


    def rearrange_deductions(self):
        """Rearrange deductions list so that NSSA is first, followed by PAYE and AIDS Levy."""
        order = ["NSSA", "PAYE", "AIDS LEVY"]
        self.deductions.sort(key=lambda x: order.index(x['name'].upper()) if x['name'].upper() in order else len(order))


    def payee_against_slab_usd(self,amount):
        payee = 0.0
        slabs = [
            (0.00, 100.00, 0.0, 0.00),
            (100.01, 300.00, 0.20, 20.00),
            (300.01, 1000.00, 0.25, 35.00),
            (1000.01, 2000.00, 0.30, 85.00),
            (2000.01, 3000.00, 0.35, 185.00),
            (3000.01, 1000000.00, 0.40, 335.00),
        ]
        for lower, upper, percent, fixed in slabs:
            if lower <= amount <= upper:
                payee = ( amount * percent) - fixed
                break
        return float(payee)


    def payee_against_slab_zwg(self,amount):
        payee = 0.0
        slabs = [
            (0.00, 2800.00, 0.0, 0.00),
            (2800.01, 8400.00, 0.20, 560.00),
            (8400.01, 28000.00, 0.25, 980.00),
            (28000.01, 56000.00, 0.30, 2380.00),
            (56000.01, 84000.00, 0.35, 5180.00),
            (84000.01, 1000000.00, 0.40, 9380.00),
        ]
        for lower, upper, percent, fixed in slabs:
            if lower <= amount <= upper:
                payee = ( amount * percent) - fixed
                print(f"{amount} ----------percent {percent} --fixed {fixed}-----------payee {payee}")
                break

        return float(payee)
