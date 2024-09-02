import tkinter as tk
from tkinter import ttk, messagebox, filedialog, Text
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from risk_calculation import calculate_risk_score, add_risk
from model_training import train_models, predict_risk_score
from visualization import visualize_risks, visualize_risk_scoring_chart
from database import setup_database, export_to_csv, generate_pdf_report

# OWASP 300 Vulnerabilities List
owasp_300 = {
    "A1": "Injection",
    "A2": "Broken Authentication",
    "A3": "Sensitive Data Exposure",
    "A4": "XML External Entities (XXE)",
    "A5": "Broken Access Control",
    "A6": "Security Misconfiguration",
    "A7": "Cross-Site Scripting (XSS)",
    "A8": "Insecure Deserialization",
    "A9": "Using Components with Known Vulnerabilities",
    "A10": "Insufficient Logging & Monitoring",
    "A11": "Unrestricted File Upload",
    "A12": "Buffer Overflow",
    "A13": "Directory Traversal",
    "A14": "Cross-Site Request Forgery (CSRF)",
    "A15": "Server-Side Request Forgery (SSRF)",
    "A16": "Insecure Direct Object References (IDOR)",
    "A17": "Security Misconfiguration",
    "A18": "Command Injection",
    "A19": "SQL Injection",
    "A20": "LDAP Injection",
    "A21": "XML Injection",
    "A22": "XPath Injection",
    "A23": "Unvalidated Redirects and Forwards",
    "A24": "Insufficient Transport Layer Protection",
    "A25": "Security Misconfiguration",
    "A26": "Open Redirects",
    "A27": "Insecure Cryptographic Storage",
    "A28": "Broken Access Control",
    "A29": "Clickjacking",
    "A30": "Malicious File Execution",
    "A31": "Improper Error Handling",
    "A32": "Insecure Data Storage",
    "A33": "Information Leakage",
    "A34": "Insecure Communication",
    "A35": "Cross-Site Scripting (XSS)",
    "A36": "Insufficient Authorization",
    "A37": "Brute Force",
    "A38": "Replay Attack",
    "A39": "Privilege Escalation",
    "A40": "Session Fixation",
    "A41": "Insecure Session Management",
    "A42": "Insecure Password Storage",
    "A43": "Exposure of Sensitive Information",
    "A44": "Denial of Service",
    "A45": "Weak Password Recovery Implementations",
    "A46": "Insecure Randomness",
    "A47": "Insufficient Input Validation",
    "A48": "Weak SSL/TLS Configuration",
    "A49": "Man-in-the-Middle Attack",
    "A50": "Improper Access Control",
    "A51": "Weak Cryptographic Algorithms",
    "A52": "Improper Resource Shutdown",
    "A53": "Improper Initialization",
    "A54": "Insecure Logging Practices",
    "A55": "Security Misconfiguration",
    "A56": "Improper Exception Handling",
    "A57": "Open Redirects",
    "A58": "Insecure Object References",
    "A59": "Insecure API",
    "A60": "Exposed Administrative Interfaces",
    "A61": "Client-Side Enforcement of Server-Side Security",
    "A62": "Insecure Mobile Configuration",
    "A63": "Sensitive Data Exposure in Transit",
    "A64": "Client-Side Caching",
    "A65": "Weak Session Management",
    "A66": "Improper Input Sanitization",
    "A67": "SQL Injection in Third-Party Libraries",
    "A68": "Hardcoded Credentials",
    "A69": "Insecure Code Repositories",
    "A70": "Remote Code Execution",
    "A71": "Deserialization of Untrusted Data",
    "A72": "Security Misconfiguration",
    "A73": "Use of Insecure Functions",
    "A74": "Failure to Restrict URL Access",
    "A75": "Improper Key Management",
    "A76": "Insecure DevOps Practices",
    "A77": "No Rate Limiting",
    "A78": "Excessive Data Exposure",
    "A79": "Mass Assignment",
    "A80": "Insecure Deployment Process",
    "A81": "Security Logging and Monitoring Failures",
    "A82": "Command Injection in Third-Party Software",
    "A83": "Improper Validation of Integrity Check Values",
    "A84": "Improper Data Validation",
    "A85": "Failure to Encrypt Sensitive Data",
    "A86": "Insufficient Authorization Checks",
    "A87": "Insecure User Authentication",
    "A88": "Improper Management of Internal Resources",
    "A89": "Lack of Security Documentation",
    "A90": "Insecure Password Reset Mechanisms",
    "A91": "Weak Encryption of Sensitive Data",
    "A92": "Client-Side Validation",
    "A93": "Use of Deprecated Libraries",
    "A94": "Insecure Network Configuration",
    "A95": "Lack of HTTP Security Headers",
    "A96": "Unauthorized Access to Admin Functions",
    "A97": "Unrestricted Cross-Domain Requests",
    "A98": "Improper Use of WebSockets",
    "A99": "Broken Authentication in Mobile Apps",
    "A100": "Session Hijacking",
    "A101": "Unrestricted Upload of File with Dangerous Type",
    "A102": "Improper Neutralization of Special Elements in Output Used by a Downstream Component",
    "A103": "Improper Neutralization of CRLF Sequences in HTTP Headers",
    "A104": "Failure to Protect Stored Data",
    "A105": "Improper Restriction of Excessive Authentication Attempts",
    "A106": "Improper Restriction of Operations within the Bounds of a Memory Buffer",
    "A107": "Failure to Ensure that Web Page is Free of Malicious Content",
    "A108": "Improper Certificate Validation",
    "A109": "Improper Privilege Management",
    "A110": "Improper Restriction of Communication Channel to Intended Endpoints",
    "A111": "Improper Verification of Cryptographic Signature",
    "A112": "Exposure of Sensitive Information to an Unauthorized Actor",
    "A113": "Incorrect Authorization",
    "A114": "Use of Hard-coded Cryptographic Key",
    "A115": "Improper Control of Generation of Code",
    "A116": "Exposure of Resource to Wrong Sphere",
    "A117": "Path Traversal: '\\..\\Filename'",
    "A118": "Missing Authorization",
    "A119": "Incorrect Permission Assignment for Critical Resource",
    "A120": "Insecure Webhooks",
    "A121": "Use of a Broken or Risky Cryptographic Algorithm",
    "A122": "Improper Verification of Integrity Check Value",
    "A123": "Insecure Dependency Resolution",
    "A124": "Use of a Cryptographic Primitive with a Risky or Broken Mode of Operation",
    "A125": "Race Condition in Web Applications",
    "A126": "Server-Side Request Forgery (SSRF) in Legacy Code",
    "A127": "Insecure Default Password",
    "A128": "Failure to Sanitize Data into a Different Format",
    "A129": "Improper Access Control in Legacy Code",
    "A130": "Failure to Invalidate Sessions after Logout",
    "A131": "Lack of Process Separation",
    "A132": "Exposure of Private Information to Unauthorized Entities",
    "A133": "Uncontrolled Resource Consumption",
    "A134": "Insecure Third-Party APIs",
    "A135": "Improper Restriction of XML External Entity Reference",
    "A136": "Code Injection",
    "A137": "Execution with Unnecessary Privileges",
    "A138": "Improper Neutralization of Input During Web Page Generation",
    "A139": "Cleartext Storage of Sensitive Information in a Cookie",
    "A140": "Improper Protection of Alternative Paths",
    "A141": "Improper Authorization in Microservices",
    "A142": "Weak Security Mechanisms for Cloud Services",
    "A143": "Improper Lock Mechanism in Mobile Devices",
    "A144": "Missing Function Level Access Control",
    "A145": "Improper Limitation of a Pathname to a Restricted Directory",
    "A146": "Insufficient Entropy in Cryptographic Systems",
    "A147": "Improper Authentication of Device Connection",
    "A148": "Improper Data Sanitization in Cloud Environments",
    "A149": "Insecure Deserialization in Legacy Code",
    "A150": "Failure to Rotate Credentials Regularly",
    "A151": "Insecure API Gateways",
    "A152": "Failure to Protect Against Cross-Site Scripting in Legacy Systems",
    "A153": "Improper Access Control in APIs",
    "A154": "Missing or Incomplete Certificate Validation",
    "A155": "Improper Removal of Sensitive Data Before Storage or Transfer",
    "A156": "Insecure Use of HTTP Methods",
    "A157": "Improper Handling of Insufficient Permissions",
    "A158": "Insecure Shell Scripting",
    "A159": "Improper Authentication in Service-Oriented Architectures",
    "A160": "Use of Obsolete Cryptographic Functions",
    "A161": "Improper Management of Environment Variables",
    "A162": "Failure to Lock Account after Excessive Login Attempts",
    "A163": "Use of a Key Past its Expiration Date",
    "A164": "Improper Input Validation in WebSockets",
    "A165": "Insecure Handling of Secrets in Containers",
    "A166": "Improper Use of Cryptographic Algorithms",
    "A167": "Unvalidated Redirects and Forwards in Microservices",
    "A168": "Improper Data Handling in Serverless Architectures",
    "A169": "Insecure Token Management",
    "A170": "Failure to Use Secure Defaults",
    "A171": "Improper Input Validation in APIs",
    "A172": "Insecure Session Handling in Cloud Services",
    "A173": "Improper Session Handling in Mobile Applications",
    "A174": "Improper Configuration of Cloud Services",
    "A175": "Use of Obsolete Cryptographic Primitives",
    "A176": "Insecure Management of Multi-Tenant Data",
    "A177": "Improper Use of Hardware Security Modules (HSMs)",
    "A178": "Insecure Use of Cloud Storage",
    "A179": "Improper Use of Secure Sockets Layer (SSL)",
    "A180": "Failure to Encrypt Data in Motion",
    "A181": "Improper Credential Management",
    "A182": "Insecure Configuration of Database Connections",
    "A183": "Improper Use of Platform-Specific Features",
    "A184": "Improper Isolation of Shared Resources",
    "A185": "Insecure Handling of Untrusted Inputs in Data Structures",
    "A186": "Improper Use of Secure Transport Protocols",
    "A187": "Failure to Implement Defense in Depth",
    "A188": "Improper Use of Tokens for Authentication",
    "A189": "Insecure Implementation of OAuth",
    "A190": "Improper Use of Access Control Lists (ACLs)",
    "A191": "Insecure Cryptographic Storage in Cloud Environments",
    "A192": "Improper Validation of File Types in Cloud Environments",
    "A193": "Improper Management of Security Policies",
    "A194": "Insecure Use of Web Services",
    "A195": "Improper Validation of Input in Cloud Applications",
    "A196": "Failure to Implement Multi-Factor Authentication",
    "A197": "Insecure Handling of Cryptographic Keys in Microservices",
    "A198": "Improper Configuration of Secure Shell (SSH)",
    "A199": "Insecure Use of Hash Functions for Passwords",
    "A200": "Improper Use of Secure Channels for Communication",
    "A201": "Insecure Use of Message Queues",
    "A202": "Failure to Enforce Secure Coding Guidelines",
    "A203": "Insecure Default Configurations in Software",
    "A204": "Improper Use of Security Tokens",
    "A205": "Insecure Session Management in Distributed Systems",
    "A206": "Insecure Implementation of Single Sign-On (SSO)",
    "A207": "Improper Validation of Input in Mobile Applications",
    "A208": "Insecure Management of Cloud Resources",
    "A209": "Insecure Use of Environment Variables in Containers",
    "A210": "Improper Validation of Input in Serverless Functions",
    "A211": "Failure to Implement Security Controls in DevOps Pipelines",
    "A212": "Improper Use of Cryptographic Modules in Cloud Environments",
    "A213": "Insecure Use of Application Programming Interfaces (APIs)",
    "A214": "Improper Validation of Input in Microservices",
    "A215": "Insecure Implementation of Authentication Mechanisms",
    "A216": "Failure to Secure Containers in Cloud Environments",
    "A217": "Improper Validation of Input in Embedded Systems",
    "A218": "Insecure Use of Web Application Frameworks",
    "A219": "Improper Validation of Input in IoT Devices",
    "A220": "Insecure Handling of Secrets in Distributed Systems",
    "A221": "Improper Use of Security Controls in Cloud Applications",
    "A222": "Insecure Default Configurations in Containers",
    "A223": "Failure to Implement Secure Development Practices",
    "A224": "Insecure Use of Database Connections in Cloud Environments",
    "A225": "Improper Validation of Input in Web Applications",
    "A226": "Insecure Implementation of Security Controls in Microservices",
    "A227": "Improper Use of Secure Development Tools",
    "A228": "Failure to Secure Communications in Distributed Systems",
    "A229": "Improper Validation of Input in Legacy Applications",
    "A230": "Insecure Management of Cloud-based Services",
    "A231": "Improper Use of Secure Programming Techniques",
    "A232": "Failure to Implement Secure Authentication Mechanisms",
    "A233": "Insecure Handling of Cryptographic Materials",
    "A234": "Improper Use of Secure Coding Practices",
    "A235": "Insecure Configuration of Web Servers",
    "A236": "Improper Management of Security Certificates",
    "A237": "Failure to Implement Security Controls in Cloud Applications",
    "A238": "Insecure Use of Secure Sockets Layer (SSL) Certificates",
    "A239": "Improper Validation of Input in Cloud Services",
    "A240": "Failure to Secure Data at Rest",
    "A241": "Improper Use of Security Tools in Development",
    "A242": "Insecure Management of Security Patches",
    "A243": "Improper Validation of Input in Secure Channels",
    "A244": "Insecure Use of Web Services in Cloud Applications",
    "A245": "Improper Management of Cloud Security Policies",
    "A246": "Failure to Implement Secure Transport Mechanisms",
    "A247": "Insecure Use of Security Tokens in Cloud Environments",
    "A248": "Improper Use of Security Features in Web Applications",
    "A249": "Insecure Handling of Cryptographic Keys",
    "A250": "Failure to Implement Secure Development Processes",
    "A251": "Insecure Use of Message Queues in Distributed Systems",
    "A252": "Improper Validation of Input in DevOps Pipelines",
    "A253": "Insecure Implementation of Security Features",
    "A254": "Improper Use of Security Tools in Cloud Environments",
    "A255": "Failure to Secure Cloud-based Services",
    "A256": "Insecure Handling of Authentication Mechanisms",
    "A257": "Improper Validation of Input in Containers",
    "A258": "Insecure Implementation of Cryptographic Controls",
    "A259": "Failure to Secure Data in Motion",
    "A260": "Improper Use of Security Controls in Mobile Applications",
    "A261": "Insecure Use of Security Controls in Cloud Applications",
    "A262": "Improper Management of Secure Channels",
    "A263": "Insecure Use of Secure Sockets Layer (SSL) in Distributed Systems",
    "A264": "Improper Validation of Input in Security Modules",
    "A265": "Insecure Use of Secure Coding Techniques in Cloud Environments",
    "A266": "Failure to Implement Security Best Practices",
    "A267": "Insecure Implementation of Secure Sockets Layer (SSL)",
    "A268": "Improper Validation of Input in Web Services",
    "A269": "Insecure Handling of Cryptographic Keys in Cloud Applications",
    "A270": "Improper Use of Secure Channels in Microservices",
    "A271": "Insecure Use of Web Services in Distributed Systems",
    "A272": "Improper Validation of Input in Secure Channels",
    "A273": "Insecure Implementation of Security Controls in Cloud Services",
    "A274": "Failure to Secure Data at Rest in Cloud Applications",
    "A275": "Improper Management of Secure Channels in Cloud Environments",
    "A276": "Insecure Use of Secure Sockets Layer (SSL) in Cloud Services",
    "A277": "Improper Validation of Input in Microservices Architectures",
    "A278": "Insecure Implementation of Security Features in Cloud Applications",
    "A279": "Failure to Secure Communications in Microservices Architectures",
    "A280": "Improper Management of Security Policies in Cloud Services",
    "A281": "Insecure Use of Security Controls in Cloud Environments",
    "A282": "Improper Validation of Input in Cloud Services",
    "A283": "Insecure Handling of Authentication Mechanisms in Cloud Applications",
    "A284": "Failure to Implement Security Controls in Microservices Architectures",
    "A285": "Improper Use of Secure Development Tools in Cloud Environments",
    "A286": "Insecure Use of Security Features in Microservices Architectures",
    "A287": "Improper Validation of Input in Distributed Systems",
    "A288": "Insecure Handling of Cryptographic Materials in Microservices",
    "A289": "Failure to Secure Cloud-based Applications",
    "A290": "Improper Validation of Input in Web Services in Cloud Applications",
    "A291": "Insecure Implementation of Secure Sockets Layer (SSL) in Cloud Environments",
    "A292": "Improper Use of Secure Channels in Cloud Applications",
    "A293": "Insecure Use of Security Tools in Distributed Systems",
    "A294": "Improper Validation of Input in Secure Channels in Microservices",
    "A295": "Failure to Implement Secure Coding Guidelines in Cloud Environments",
    "A296": "Insecure Handling of Authentication Mechanisms in Microservices Architectures",
    "A297": "Improper Use of Secure Development Tools in Microservices Architectures",
    "A298": "Insecure Implementation of Security Controls in Distributed Systems",
    "A299": "Improper Validation of Input in Secure Sockets Layer (SSL)",
    "A300": "Insecure Use of Security Tokens in Microservices Architectures"
}

def setup_gui():
    app = tb.Window(themename="superhero")
    app.title("Advanced Cybersecurity Risk Assessment Tool")
    app.geometry("1200x800")

    # Frame for input fields
    input_frame = ttk.Frame(app, padding=10)
    input_frame.pack(pady=10)

    # Instruction text box
    instructions = Text(app, width=50, height=20, wrap=tk.WORD)
    instructions.pack(side=tk.RIGHT, padx=10, pady=10)
    instructions.insert(tk.END, "Instructions:\n\n"
                                "1. Add a risk by selecting the Threat from the dropdown, and filling out all the fields, "
                                "then click 'Add Risk'.\n\n"
                                "2. Click 'Calculate Risk Score' to see the calculated risk score.\n\n"
                                "3. To train the models, click 'Train Models'. Ensure that you have added "
                                "enough data before training.\n\n"
                                "4. Use the prediction buttons to predict the risk score using Linear Regression "
                                "or Random Forest models.\n\n"
                                "5. Click 'Visualize Risks' to see a graphical representation of the risks.\n\n"
                                "6. Click 'Visualize Risk Scoring' to see a histogram of the risk score distribution.\n\n"
                                "7. Use the 'Export to CSV' and 'Generate PDF Report' buttons to save your data.")

    # Dropdown menu for selecting OWASP vulnerabilities
    ttk.Label(input_frame, text="Select Threat:").grid(row=0, column=0, sticky=tk.W)
    threat_var = tk.StringVar()
    threat_menu = ttk.Combobox(input_frame, textvariable=threat_var, values=list(owasp_300.values()), width=47)  
    threat_menu.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)

    # Likelihood entry
    ttk.Label(input_frame, text="Likelihood (1-5):").grid(row=1, column=0, sticky=tk.W)
    likelihood_var = tk.StringVar()
    likelihood_entry = ttk.Entry(input_frame, textvariable=likelihood_var, width=5)
    likelihood_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)

    # Impact entry
    ttk.Label(input_frame, text="Impact (1-5):").grid(row=2, column=0, sticky=tk.W)
    impact_var = tk.StringVar()
    impact_entry = ttk.Entry(input_frame, textvariable=impact_var, width=5)
    impact_entry.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)

    # Exposure entry
    ttk.Label(input_frame, text="Exposure (1-5):").grid(row=3, column=0, sticky=tk.W)
    exposure_var = tk.StringVar()
    exposure_entry = ttk.Entry(input_frame, textvariable=exposure_var, width=5)
    exposure_entry.grid(row=3, column=1, padx=5, pady=5, sticky=tk.W)

    # Mitigation entry
    ttk.Label(input_frame, text="Mitigation (1-5):").grid(row=4, column=0, sticky=tk.W)
    mitigation_var = tk.StringVar()
    mitigation_entry = ttk.Entry(input_frame, textvariable=mitigation_var, width=5)
    mitigation_entry.grid(row=4, column=1, padx=5, pady=5, sticky=tk.W)

    # Asset Value entry
    ttk.Label(input_frame, text="Asset Value (1-5):").grid(row=5, column=0, sticky=tk.W)
    asset_value_var = tk.StringVar()
    asset_value_entry = ttk.Entry(input_frame, textvariable=asset_value_var, width=5)
    asset_value_entry.grid(row=5, column=1, padx=5, pady=5, sticky=tk.W)

    # Threat Intelligence entry
    ttk.Label(input_frame, text="Threat Intelligence (1-10):").grid(row=6, column=0, sticky=tk.W)
    threat_intel_var = tk.StringVar()
    threat_intel_entry = ttk.Entry(input_frame, textvariable=threat_intel_var, width=5)
    threat_intel_entry.grid(row=6, column=1, padx=5, pady=5, sticky=tk.W)

    # Vulnerability Severity entry
    ttk.Label(input_frame, text="Vulnerability Severity (1-10):").grid(row=7, column=0, sticky=tk.W)
    vulnerability_severity_var = tk.StringVar()
    vulnerability_severity_entry = ttk.Entry(input_frame, textvariable=vulnerability_severity_var, width=5)
    vulnerability_severity_entry.grid(row=7, column=1, padx=5, pady=5, sticky=tk.W)

    # Control Effectiveness entry
    ttk.Label(input_frame, text="Control Effectiveness (1-5):").grid(row=8, column=0, sticky=tk.W)
    control_effectiveness_var = tk.StringVar()
    control_effectiveness_entry = ttk.Entry(input_frame, textvariable=control_effectiveness_var, width=5)
    control_effectiveness_entry.grid(row=8, column=1, padx=5, pady=5, sticky=tk.W)

    # RTO entry
    ttk.Label(input_frame, text="RTO (Hours):").grid(row=9, column=0, sticky=tk.W)
    rto_var = tk.StringVar()
    rto_entry = ttk.Entry(input_frame, textvariable=rto_var, width=5)
    rto_entry.grid(row=9, column=1, padx=5, pady=5, sticky=tk.W)

    # Add Risk button
    ttk.Button(input_frame, text="Add Risk", command=lambda: add_risk(threat_var.get(), likelihood_var.get(), impact_var.get(), exposure_var.get(), mitigation_var.get(), asset_value_var.get(), threat_intel_var.get(), vulnerability_severity_var.get(), control_effectiveness_var.get(), rto_var.get())).grid(row=10, column=1, padx=5, pady=5, sticky=tk.E)

    # Calculate Risk Score button
    ttk.Button(input_frame, text="Calculate Risk Score", command=lambda: calculate_and_display_risk_score()).grid(row=11, column=1, padx=5, pady=5, sticky=tk.E)

    # Train Models button
    ttk.Button(input_frame, text="Train Models", command=train_models).grid(row=12, column=1, padx=5, pady=5, sticky=tk.E)

    # Predict Risk Score buttons
    ttk.Button(input_frame, text="Predict Risk (Linear Regression)", command=lambda: predict_risk_score(model='linear')).grid(row=13, column=1, padx=5, pady=5, sticky=tk.E)
    ttk.Button(input_frame, text="Predict Risk (Random Forest)", command=lambda: predict_risk_score(model='forest')).grid(row=14, column=1, padx=5, pady=5, sticky=tk.E)

    # Visualize Risks button
    ttk.Button(input_frame, text="Visualize Risks", command=visualize_risks).grid(row=15, column=1, padx=5, pady=5, sticky=tk.E)

    # Visualize Risk Scoring button
    ttk.Button(input_frame, text="Visualize Risk Scoring", command=visualize_risk_scoring_chart).grid(row=16, column=1, padx=5, pady=5, sticky=tk.E)

    # Export to CSV button
    ttk.Button(app, text="Export to CSV", command=export_to_csv).pack(side=tk.LEFT, padx=10)

    # Generate PDF Report button
    ttk.Button(app, text="Generate PDF Report", command=generate_pdf_report).pack(side=tk.LEFT, padx=10)

    # Risk and Risk Level Labels
    risk_label = ttk.Label(app, text="Risk Score:", font=('Helvetica', 14))
    risk_label.pack(pady=10)

    risk_level_label = ttk.Label(app, text="Risk Level:", font=('Helvetica', 14))
    risk_level_label.pack(pady=10)

    app.mainloop()

def calculate_and_display_risk_score():
    risk_score, risk_level = calculate_risk_score(
        likelihood_var.get(),
        impact_var.get(),
        exposure_var.get(),
        mitigation_var.get(),
        asset_value_var.get(),
        threat_intel_var.get(),
        vulnerability_severity_var.get(),
        control_effectiveness_var.get(),
        rto_var.get()
    )
    if risk_score is not None:
        risk_label.config(text=f"Risk Score: {risk_score:.2f}")
        risk_level_label.config(text=f"Risk Level: {risk_level}")

if __name__ == "__main__":
    setup_gui()