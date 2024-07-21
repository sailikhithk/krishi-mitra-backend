import os
from dotenv import load_dotenv
load_dotenv()

COUNTRIES = [
    "Afghanistan", "Albania", "Algeria", "Andorra", "Angola", "Antigua and Barbuda", "Argentina", "Armenia", 
    "Australia", "Austria", "Azerbaijan", "Bahamas", "Bahrain", "Bangladesh", "Barbados", "Belarus", "Belgium", 
    "Belize", "Benin", "Bhutan", "Bolivia", "Bosnia and Herzegovina", "Botswana", "Brazil", "Brunei", "Bulgaria", 
    "Burkina Faso", "Burundi", "Cabo Verde", "Cambodia", "Cameroon", "Canada", "Central African Republic", "Chad", 
    "Chile", "China", "Colombia", "Comoros", "Congo, Democratic Republic of the", "Congo, Republic of the", 
    "Costa Rica", "Cote d'Ivoire", "Croatia", "Cuba", "Cyprus", "Czech Republic", "Denmark", "Djibouti", "Dominica", 
    "Dominican Republic", "Ecuador", "Egypt", "El Salvador", "Equatorial Guinea", "Eritrea", "Estonia", "Eswatini", 
    "Ethiopia", "Fiji", "Finland", "France", "Gabon", "Gambia", "Georgia", "Germany", "Ghana", "Greece", "Grenada", 
    "Guatemala", "Guinea", "Guinea-Bissau", "Guyana", "Haiti", "Honduras", "Hungary", "Iceland", "India", "Indonesia", 
    "Iran", "Iraq", "Ireland", "Israel", "Italy", "Jamaica", "Japan", "Jordan", "Kazakhstan", "Kenya", "Kiribati", 
    "Korea, North", "Korea, South", "Kosovo", "Kuwait", "Kyrgyzstan", "Laos", "Latvia", "Lebanon", "Lesotho", "Liberia", 
    "Libya", "Liechtenstein", "Lithuania", "Luxembourg", "Madagascar", "Malawi", "Malaysia", "Maldives", "Mali", "Malta", 
    "Marshall Islands", "Mauritania", "Mauritius", "Mexico", "Micronesia", "Moldova", "Monaco", "Mongolia", "Montenegro", 
    "Morocco", "Mozambique", "Myanmar", "Namibia", "Nauru", "Nepal", "Netherlands", "New Zealand", "Nicaragua", "Niger", 
    "Nigeria", "North Macedonia", "Norway", "Oman", "Pakistan", "Palau", "Palestine", "Panama", "Papua New Guinea", 
    "Paraguay", "Peru", "Philippines", "Poland", "Portugal", "Qatar", "Romania", "Russia", "Rwanda", "Saint Kitts and Nevis", 
    "Saint Lucia", "Saint Vincent and the Grenadines", "Samoa", "San Marino", "Sao Tome and Principe", "Saudi Arabia", 
    "Senegal", "Serbia", "Seychelles", "Sierra Leone", "Singapore", "Slovakia", "Slovenia", "Solomon Islands", "Somalia", 
    "South Africa", "South Sudan", "Spain", "Sri Lanka", "Sudan", "Suriname", "Sweden", "Switzerland", "Syria", "Taiwan", 
    "Tajikistan", "Tanzania", "Thailand", "Timor-Leste", "Togo", "Tonga", "Trinidad and Tobago", "Tunisia", "Turkey", 
    "Turkmenistan", "Tuvalu", "Uganda", "Ukraine", "United Arab Emirates", "United Kingdom", "United States", "Uruguay", 
    "Uzbekistan", "Vanuatu", "Vatican City", "Venezuela", "Vietnam", "Yemen", "Zambia", "Zimbabwe"
]

ROLES = ["Admin", "Teacher", "Student", "Super Admin"]

BRANCHS = [
    "Mumbai","Delhi","Bangalore","Hyderabad","Ahmedabad","Chennai","Kolkata"
    ,"Pune","Surat","Jaipur","Lucknow","Kanpur","Nagpur","Indore","Thane"
    ,"Bhopal","Visakhapatnam","Patna","Vadodara","Ghaziabad","Agra","Nashik","Faridabad","Rajkot","Varanasi"
]

DEPARTMENTS = ["Finance", "Marketing", "Operations", "HR", "Sales", "Customer Service", "IT", "Engineering", "R&D", "Supply Chain", "Manufacturing", "Quality Control", "Accounting", "Communications", "Public Relations", "Legal", "Compliance", "Administration", "Facilities", "Maintenance", "Security", "Risk Management", "Investor Relations", "Training", "Recruiting", "Strategy", "Business Development", "Project Management", "Procurement", "Logistics", "Inventory", "Billing", "Pricing", "Auditing", "Tax", "Treasury", "Investments", "Payroll", "Benefits", "Compensation", "Talent Acquisition", "Organizational Development", "Analytics", "Fraud", "Collections", "Partnerships", "Mergers & Acquisitions", "Product Management", "Program Management", "Content", "Design", "Editorial", "Writing", "Translation", "Language Services", "Oversight", "Complaints", "Ethics", "Diversity", "Inclusion", "Proposals", "Grants", "Export", "Import", "Licensing", "Real Estate", "Facilities", "Catering", "Travel", "Records", "Archives", "Mailroom", "Printing", "Fleet", "Distribution", "Warehousing", "3D Printing", "Appraisal", "Assessment", "Actuarial", "Economics", "Piloting", "Flight Operations", "Aircraft Maintenance", "Navigation", "Meteorology", "Healthcare Services", "Pharmacy", "Laboratory", "Radiology", "Cardiology", "Oncology", "Surgery", "Accounting"]

COURSES = ["UG", "PG"]

UPLOAD_USER_FILE_STUDENT_HEADERS = ["first_name", "last_name", "phone_number", "email", "branch", "course", "department", "password", "student_id", "role_id"]

UPLOAD_USER_FILE_TEACHER_HEADERS = ["first_name", "address", "phone_number", "email", "branch", "course", "department", "password"]

UPLOAD_USER_FILE_PLACEMENT_TRACKER_HEADERS = ['Student ID', 'First Name', 'Last Name', 'Department Name', 'Status', 'Company Name', 'Company Type', 'Offer', 'Offer Type']

HARD_SKILLS = [
    "Programming Language (Python)","Programming Language (Java)","Programming Language (C)","Programming Language (C++)","Programming Language (Go)",
    "Data Analysis","Data Science","AI and Machine Learning (TensorFlow)", "AI and Machine Learning (PyTorch)",
    "Web Development (React)","Web Development (Angular)","Web Development (Node.js)","Web Development (GraphQL)","Web Development (Web 3)",
    "Databases (Oracle)","Databases (MySQL)","Databases (Microsoft SQL Server)","Databases (PostgreSQL)","Databases (MongoDB)","Databases (Redis)","Databases (Cassandra)","Databases (Amazon DynamoDB)",
    "Cloud Computing (AWS)","Cloud Computing (Azure)","Cloud Computing (GCP)",
    "DevOps (Docker)","DevOps (Kubernetes)","DevOps (Jenkins)",
    "Cybersecurity","Software Testing", "Networking",
    "Mobile App Development (Swift)","Mobile App Development (Kotlin)",   
    "Big Data Technologies (Hadoop)"," Big Data Technologies (Spark)",
    "Operations (Supply Chain Management)", "Operations (Inventory Management)", "Operations (ERP Systems)",
    "Operations (Process Mapping & Optimization)", "Operations (Quality Assurance & Control)", "Operations (Lean/Six Sigma Principles)",
    "Operations (Risk Management)", "Operations (Budgeting & Financial Forecasting)", "Operations (Vendor Management Systems)",
    "Operations (Production Scheduling)", "Operations (Safety & Compliance Systems)" 
    "Data Analysis (Python)", "Data Analysis (Tableau)", "Data Analysis (Power BI)", 
    "Data Analysis (Excel)", "Data Analysis (R)", "Data Analysis (Jupyter Notebook)", 
    "Data Analysis (SAS)", "Data Analysis (SPSS)", "Data Analysis (KNIME)", 
    "Data Analysis (Alteryx)", "Data Analysis (MATLAB)", "Data Analysis (RapidMiner)", 
    "Data Analysis (QlikView)", "Data Analysis (Splunk)", "Data Analysis (Weka)", 
    "Data Analysis (Orange)", "Data Analysis (Pentaho)", "Data Analysis (D3.js)", 
    "Data Analysis (ClickView)", "Data Analysis (Looker)", "Project Management",
    "Project management (Asana)", "Project management (Trello)", "Project management (Jira)",  
    "Project management (ClickUp)", "Project management (Basecamp)", "Project management (Smartsheet)", 
    "Project management (Microsoft Project)", "Project management (Wrike)", "Requirement Gathering Techniques",
    "Agile Methodologies", "Scrum Methodologies", 
    
    "Cost Benefit Analysis", "Customer Journey Mapping", "Use Case Development", "Gap Analysis", 
    "Process Modeling Tool (Microsoft Visio)", "Process Modeling Tool (Lucidchart)", "Process Modeling Tool (Bizagi)", 
    "Process Modeling Tool (Signavio)", "Process Modeling Tool (TIBCO Nimbus Control)", "Process Modeling Tool (Nintex Promapp)", 
    "Process Modeling Tool (Draw.io)", "Process Modeling Tool (IBM Blueworks Live)", "Process Modeling Tool (ARIS)", 
    "Process Modeling Tool (Camunda)", "Process Modeling Tool (Creately)", "Process Modeling Tool (iGrafx)", 
    "Process Modeling Tool (Oracle BPM Suite)", "Process Modeling Tool (Visual Paradigm)", "Process Modeling Tool (MEGA)", 
    "Process Modeling Tool (BIC Cloud BPM)", "Process Modeling Tool (KiSSFLOW)", "Process Modeling Tool (Appian)", 
    "Process Modeling Tool (ERP Maestro)", "Process Modeling Tool (Pega Platform)", 

    "Agribusiness Management (Agricultural Economics)","Agribusiness Management (Precision Agriculture)","Agribusiness Management (Commodity Markets & Trading)",
    "Agribusiness Management (Farm Management Systems)","Agribusiness Management (Crop & Soil Analysis)","Agribusiness Management (Livestock Management)",
    "Agribusiness Management (Supply Chain Management for Agri-products)","Agribusiness Management (Agri Finance & Budgeting)",
    "Agribusiness Management (Agri Marketing & Sales)","Agribusiness Management (Sustainability & Conservation Techniques)",
    "Agribusiness Management (Agronomy & Techniques)","Agribusiness Management (Pest & Disease Management Systems)",
    "Agribusiness Management (Regulatory & Compliance Systems for Agribusiness)",

    "Marketing (SEO And SEM)","Marketing (Pay-Per-Click)","Marketing (Content Management Systems)","Marketing (Customer Relationship Management)"   

    "Sales (Product Knowledge)","Sales (Customer Relationship Management (CRM) Software)","Sales (Data Analysis and Interpretation)","Sales (Lead Qualification)",
    "Sales (Sales Pipeline Management)","Sales (Negotiation Techniques)","Sales (Contract Drafting and Management)","Sales (Prospecting Skills)",
    "Sales (Presentation Skills)","Sales (Closing Techniques)","Sales (Financial Acumen)","Sales (Market Research)",
    "Sales (Sales Forecasting)","Sales (Time Management)","Sales (E-commerce Platforms)","Sales (Social Media for Sales)",
    "Sales (Email Marketing)","Sales (Sales Automation Tools)","Sales (Pricing Strategies)","Sales (Technical Product Skills)",
    "Sales (Cold Calling)","Sales (Networking)","Sales (Digital Marketing)","Sales (Reporting)",
    "Sales (Compliance and Regulation Knowledg)","Sales (Strategy Development)","Sales (Account Management)",
    "Sales (B2B Skills)","Sales (B2C Skills)","Sales (Cross-selling and Upselling Techniques)",
    "Sales (Sales Demonstrations and Product Walkthroughs)","Sales (Objection Handling)","Sales (Point of Sale (POS) Systems)",
    "Sales (Business Development)","Sales (Strategic Planning Skills)","Sales (Territory Management)","Sales (Multilingual Communication)",
    "Sales (Sales Process Management)","Sales (Sales Enablement Tools)","Sales (Sales Analytics and Metrics)","Sales (Quota Attainment)",
    "Sales (Understanding of Buyer Behavior)","Sales (Customer Segmentation)","Sales (Sales Operation Management)","Sales (Sales Funnel Management)",
    "Sales (Client Acquisition Techniques)","Sales (Solution Selling)","Sales (Complex Sales Negotiation)","Sales (Proposal Creation)",
    "Sales (Competitor Analysis)","Sales (Software-as-a-Service (SaaS) Sales)","Sales (Technical Writing for Proposals)","Sales (Online Demo and Webinar Hosting)",
    "Sales (Use of Sales Intelligence Tools)","Sales (Channel Sales)","Sales (Inbound Sales Methodologies)","Sales (Outbound Sales Methodologies)",
    "Sales (Trade Show and Event Sales)","Sales (Value-Based Selling)","Sales (Consultative Selling Techniques)","Sales (Customer Success Strategies)",
    "Sales (Key Account Management)","Sales (International Sales and Global Business)","Sales (Team Leadership and Sales Team Management)","Sales (Product Lifecycle Management)",
    "Sales (Sales Training and Coaching)","Sales (CRM Database Management)","Sales (Mobile Sales Applications)","Sales (Sales Tax Knowledge)",
    "Sales (Knowledge of Sales Psychology)","Sales (Order Management Systems)","Sales (Inventory Control Basics for Sales)","Sales (E-signature Software)",
    "Sales (Document Management Tools)","Sales (Knowledge of Compliance Software (for regulated industries))",
    "Sales (Remote Sales Techniques)","Sales (Social Selling Skills)","Sales (Cybersecurity Basics for Sales Processes)","Sales (Understanding of Supply Chain Processes)",
    "Sales (Digital Contracting and Closing Tools)"

    "Space (Astrodynamics)","Space (Orbital Mechanics)","Space (Satellite Technology)","Space (Spacecraft Design and Integration)",
    "Space (Payload Engineering)","Space (Propulsion Systems)","Space (Thermal Analysis and Control)",
    "Space (Structural Analysis)","Space (Aerodynamics and Fluid Dynamics)","Space (Systems Engineering)",
    "Space (Space Environment and its Effects)","Space (Materials Science for Space Applications)",
    "Space (Electrical Engineering for Spacecraft Systems)","Space (RF Engineering and Communications)",
    "Space (Navigation and Control Systems)","Space (Computer-Aided Design (CAD))","Space (Finite Element Analysis (FEA))",
    "Space (Computational Fluid Dynamics (CFD))","Space (Software Development for Space Applications)",
    "Space (Embedded Systems Design)","Space (Robotics and Automation for Spacecraft)","Space (Instrumentation and Sensor Technology)",
    "Space (Project Management)","Space (Data Analysis and Statistics)","Space (Mission Planning and Design)",
    "Space (Space Operations and Ground Support Systems)","Space (Space Policy and International Space Law)",
    "Space (Space Economics and Business)","Space (Quality Assurance for Space Systems)","Space (Radiation Analysis and Protection)",
    "Space (Human Factors and Ergonomics for Space Travel)","Space (Astrophysics)","Space (Remote Sensing and Earth Observation)",
    "Space (Planetary Science)","Space (Space Medicine and Life Support Systems)",
    "Space (Additive Manufacturing (3D Printing) for Space Parts)","Space (Space Resource Utilization)",
    "Space (Space Debris Mitigation and Management)","Space (Rocket Testing and Launch Operations)",
    "Space (Spacecraft Telemetry, Tracking, and Command)","Space (Avionics and Flight Software)","Space (Research and Development Skills)",
    "Space (Technical Documentation and Specification Writing)","Space (Cybersecurity for Space Systems)","Space (Spacecraft Testing and Validation)",
    "Space (Space Simulation Environments)","Space (Artificial Intelligence and Machine Learning for Space Missions)",
    "Space (Space Weather Forecasting)","Space (Interplanetary Trajectory Design)","Space (Spacecraft Docking Systems)",
    "Space (High-Temperature Materials for Re-entry Vehicles)","Space (Optical Engineering for Telescopes and Space Cameras)",
    "Space (Cryogenics for Space Applications)","Space (Space Tourism and Commercial Spaceflight Operations)",
    "Space (Environmental Control and Life Support Systems (ECLSS))","Space (Space Farming and Biological Life Support)",
    "Space (Space Education and Outreach)","Space (Knowledge of Launch Vehicle Configurations and Design)",
    "Space (Hypersonic and Supersonic Flight Principles)","Space (Space Surveillance and Situational Awareness)"
    
]

SOFT_SKILLS = [
    "Communication","Teamwork","Problem-Solving","Adaptability",
    "Time Management","Leadership","Critical Thinking","Creativity",
    "Conflict Resolution","Decision Making","Emotional Intelligence","Stress Management",
    "Attention to Detail","Interpersonal Skills","Negotiation","Empathy","Active Listening",
    "Customer Service","Presentation Skills","Organizational Skills","Networking",
    "Self-Motivation","Flexibility","Patience","Open-Mindedness"
]

INTERVIEW_IMPROVEMENTS = [
"Know Your Audience: Understand the background and expectations of your interviewers.",
"Practice, Practice, Practice: Rehearse your presentation multiple times to build confidence.",
"Structure Your Presentation: Use a clear structure like Introduction, Body, and Conclusion.",
"Stay Concise: Avoid unnecessary details and stay on point.",
"Use Visuals Wisely: Incorporate visuals, but don't overload with them.",
"Speak Clearly and Slowly: Enunciate your words and maintain a steady pace.",
"Maintain Eye Contact: Make eye contact with your audience to appear more engaged.",
"Body Language: Use confident body language, such as standing or sitting up straight.",
"Connect with Stories: Share anecdotes or examples to make your points memorable.",
"Engage Your Audience: Encourage questions or interaction during the presentation.",
"Dress Appropriately: Choose attire that suits the company's culture.",
"Time Management: Keep track of time and ensure you don't run over the allocated time.",
"Research the Company: Show your knowledge about the company and its industry.",
"Address Potential Concerns: Anticipate questions or concerns and address them proactively.",
"Use Positive Language: Frame your ideas in a positive and constructive manner.",
"Be Yourself: Don't try to be someone you're not; authenticity is valued.",
"Emphasize Achievements: Highlight your achievements and relevant experiences.",
"Explain Gaps: If there are gaps in your resume, explain them briefly.",
"Stay Updated: Know the latest industry trends and developments.",
"Prepare for Technical Issues: Be ready for technical glitches and have a backup plan.",
"Learn from Feedback: Accept feedback graciously and use it to improve.",
"Embrace Nervousness: It's normal to be nervous; use the energy to your advantage.",
"Follow Up Questions: Expect follow-up questions and have answers prepared.",
"Polish Your Resume: Ensure your resume aligns with your presentation.",
"Bring Copies: Have copies of your resume and presentation materials.",
"Ask Questions: Be prepared to ask thoughtful questions about the company.",
"Relaxation Techniques: Practice relaxation techniques to manage anxiety.",
"Use a Strong Opening: Begin with a strong opening statement or a hook.",
"Professional Etiquette: Be polite, respectful, and professional at all times.",
"Express Gratitude: Conclude by expressing gratitude for the opportunity."
]
BACKEND_SERVER_URL = os.environ.get("BACKEND_SERVER_URL")
UI_SERVER_URL = os.environ.get("UI_SERVER_URL")
EMAIL_PASSWORD = os.environ.get("GOOGLE_EMAIL_PASSWORD")
EMAIL_USERNAME = os.environ.get("GOOGLE_EMAIL_USERNAME")