# User Manual - Alkana KPI System

A guide for end users of the Alkana KPI Management System.

## Table of Contents
- [Getting Started](#getting-started)
- [Logging In](#logging-in)
- [Navigating the System](#navigating-the-system)
- [Viewing Your KPIs](#viewing-your-kpis)
- [Updating Your Profile](#updating-your-profile)
- [Viewing KPI Reports](#viewing-kpi-reports)
- [Exporting Data](#exporting-data)
- [Understanding Your KPI Scores](#understanding-your-kpi-scores)
- [Frequently Asked Questions](#frequently-asked-questions)

## Getting Started

### What is the Alkana KPI System?

The Alkana KPI (Key Performance Indicator) System helps you track and manage your performance goals throughout the year. The system:

- **Tracks your KPIs** across semesters and months
- **Calculates scores automatically** based on your achievements
- **Provides reports** to see your progress
- **Allows profile management** to keep your information current

### System Requirements

- **Web Browser**: Chrome, Firefox, Edge, or Safari (latest version)
- **Internet Connection**: Required for access
- **Login Credentials**: Username and password provided by your administrator

### Getting Help

If you need assistance:
1. Check the [FAQ section](#frequently-asked-questions)
2. Review the [Troubleshooting Guide](troubleshooting.md)
3. Contact your department administrator
4. Contact IT support

---

## Logging In

### Step 1: Access the System

1. Open your web browser
2. Navigate to: `https://yourdomain.com/login`
3. You'll see the login page

### Step 2: Enter Credentials

1. Enter your **username** (provided by admin)
2. Enter your **password**
3. Click **Login** button

### Step 3: First Login

On your first login:
1. You may be prompted to change your password
2. Choose a strong password (minimum 12 characters)
3. Mix uppercase, lowercase, numbers, and symbols
4. Don't use personal information

### Troubleshooting Login Issues

**Forgot Password?**
- Contact your administrator to reset your password
- They will provide you with a temporary password

**Account Locked?**
- After 5 failed login attempts, your account is temporarily locked
- Wait 1 hour or contact administrator

---

## Navigating the System

### Main Navigation

After logging in, you'll see the main menu:

- **Home**: View KPI reports and summaries
- **Profile**: Update your personal information
- **Admin** (if authorized): Access administrative functions
- **Logout**: Sign out of the system

### User Interface Overview

**Top Bar**:
- Welcome message with your name
- Logout link

**Side Menu** (if applicable):
- Navigation links
- Quick filters

**Main Content Area**:
- Reports, forms, and data tables

---

## Viewing Your KPIs

### Accessing Your KPI Results

1. Click **Home** from the main menu
2. Your KPI results will be displayed

### Understanding the KPI Results Table

| Column | Description |
|--------|-------------|
| **Year** | The year of the KPI (e.g., 2025) |
| **Semester** | 1st SEM (Jan-Jun) or 2nd SEM (Jul-Dec) |
| **Month** | Period within semester (1st, 2nd, 3rd, 4th, 5th, final) |
| **KPI Name** | Name of the performance indicator |
| **Target** | Your target value or percentage |
| **Achievement** | Your actual performance |
| **Weight** | Importance of this KPI (as %) |
| **Score** | Calculated result (weighted) |

### Filtering Your KPIs

Use the filter options to narrow down results:

1. **Year**: Select year (e.g., 2025)
2. **Semester**: Choose 1st SEM or 2nd SEM
3. **Month**: Select specific month or final
4. Click **Filter** or **Search** button

### Viewing Details

Click on a KPI row to see:
- Full KPI description
- Target details
- Achievement history
- Score calculation breakdown

---

## Updating Your Profile

### Access Your Profile

1. Click **Profile** in the main menu
2. Your current information is displayed

### Editable Information

You can update:
- **First Name**
- **Last Name**
- **Email Address**
- **Password** (optional)

### How to Update Profile

1. Navigate to Profile page
2. Edit the fields you want to change
3. For password change:
   - Enter **Old Password**
   - Enter **New Password**
   - Confirm **New Password**
4. Click **Save** button

### Profile Update Confirmation

- Success message appears: "Profile updated successfully"
- Error message if validation fails (e.g., incorrect old password)

**Important Notes**:
- You cannot change your username
- You cannot change your employee code or department
- Contact administrator to change these details

---

## Viewing KPI Reports

### Accessing Reports

1. Click **Home** from main menu
2. Use filters to select time period
3. View aggregated results

### Report Sections

**Summary Section**:
- Total weighted score
- Number of KPIs tracked
- Performance indicators

**Detail Table**:
- Individual KPI results
- Grouped by month/semester
- Sortable columns

**Pagination**:
- 20 results per page
- Use page numbers to navigate
- "Next" and "Previous" buttons

### Understanding Your Total Score

Your total score is the **sum of all weighted KPI scores** for the period:

**Example**:
```
KPI 1 Score: 0.30 (30% weight × 100% achievement)
KPI 2 Score: 0.18 (20% weight × 90% achievement)
KPI 3 Score: 0.15 (15% weight × 100% achievement)
────────────────────────────────────────────────
Total Score: 0.63 (out of maximum possible 0.65)
```

### Performance Indicators

| Score Range | Performance |
|-------------|-------------|
| 90-100% | Excellent |
| 80-89% | Good |
| 70-79% | Satisfactory |
| 60-69% | Needs Improvement |
| Below 60% | Unsatisfactory |

---

## Exporting Data

### Export to Excel

1. Navigate to **Home** (KPI Report)
2. Apply desired filters
3. Click **Export to Excel** button
4. File downloads automatically

### Excel File Contents

The exported file contains:
- Year, semester, month
- Your name and department
- All KPI names
- Targets and achievements
- Calculated scores
- Subtotals

### Using Exported Data

- Open in Microsoft Excel or Google Sheets
- Use for personal tracking
- Create custom charts
- Share with supervisor (if needed)

**File Format**: `.xlsx` (Excel 2007+)

**Filename Example**: `KPI_Results_2025-12-30_14-30-45.xlsx`

---

## Understanding Your KPI Scores

### How Scores Are Calculated

The system automatically calculates your score based on:

1. **Achievement vs Target**: How well you performed
2. **KPI Type**: Calculation method varies by type
3. **Weight**: Importance of the KPI
4. **Thresholds**: Minimum and maximum limits

### KPI Types

**Type 1 - Bigger is Better**:
- Higher achievement = Higher score
- Example: Sales revenue, customer satisfaction
- Formula: `(Achievement / Target) × Weight`

**Type 2 - Smaller is Better**:
- Lower achievement = Higher score
- Example: Cost reduction, cycle time
- Formula: `(Target / Achievement) × Weight`

**Type 3 - Mistake Counting**:
- Zero mistakes = Maximum score
- Example: Safety incidents, defects
- Formula: Special calculation (inverted)

### Thresholds

**Minimum Threshold** (usually 40%):
- If performance below this → Score = 0
- Must achieve at least 40% of target to get points

**Maximum Threshold** (usually 140%):
- If performance above this → Score capped at max
- Prevents extreme outliers from skewing total

**Example**:
```
Target: $1,000,000
Achievement: $300,000 (30%)
→ Below 40% minimum → Score = 0

Achievement: $2,000,000 (200%)
→ Above 140% maximum → Score capped at 140%
```

### Percentage vs Absolute Calculations

Some KPIs use percentage mode:
- System first calculates % of target achieved
- Then applies ratio calculation
- More complex but accurate for percentage-based targets

Most KPIs use direct mode:
- Direct comparison of achievement to target
- Simpler calculation

**Your score is always shown as a percentage of the maximum possible.**

---

## Frequently Asked Questions

### General Questions

**Q: How often is data updated?**  
A: Real-time. Changes are reflected immediately after saving.

**Q: Can I edit my KPI targets?**  
A: No. Only administrators can modify targets. Contact your manager if targets need adjustment.

**Q: Can I add new KPIs to my profile?**  
A: No. KPI assignments are managed by administrators. Contact your manager for KPI changes.

**Q: Who can see my KPI results?**  
A: 
- You can see your own results
- Your department manager can see your results
- Group managers can see results across their group
- Administrators can see all results

---

### Login & Access

**Q: I forgot my password. What should I do?**  
A: Contact your administrator or IT support to reset your password.

**Q: Why can't I log in?**  
A: Common reasons:
- Incorrect username or password (check caps lock)
- Account locked after failed attempts (wait 1 hour)
- Account not yet activated (contact admin)
- Password expired (contact admin for reset)

**Q: How do I change my password?**  
A: Go to Profile → Enter old password and new password → Save

---

### KPI Questions

**Q: Why is my score 0 even though I had some achievement?**  
A: Possible reasons:
- Achievement below minimum threshold (40%)
- KPI has special "zero tolerance" rule
- Data not yet entered or calculated

**Q: My achievement is higher than target, but score isn't 100%. Why?**  
A: Score depends on:
- Weight of the KPI (if weight is 25%, max score is 0.25)
- Calculation type (Type 2 KPIs work inversely)
- Multiple KPIs contribute to total score

**Q: What does "Weight %" mean?**  
A: Weight shows how important this KPI is relative to your total score. All KPI weights should sum to 100%.

**Q: Can I see historical data from previous years?**  
A: Yes. Use the year filter on the Home page to select previous years.

---

### Reports & Export

**Q: How do I print my KPI report?**  
A: 
1. Export to Excel
2. Open the Excel file
3. Use File → Print from Excel

**Q: Can I export data for my entire department?**  
A: Only if you're a manager with department-level access. Regular users can only export their own data.

**Q: The export file won't open. What's wrong?**  
A: 
- Ensure you have Excel or compatible software installed
- Try opening with Google Sheets if Excel isn't available
- Check file isn't corrupted (re-download)

---

### Data Entry

**Q: I can't edit the "Achievement" field. Why?**  
A: If the field is read-only, it means:
- Data comes from SAP system (automated import)
- You don't have permission to edit
- Contact your manager or admin

**Q: Why does "Target Input" auto-fill when I enter "Target Set"?**  
A: Some KPIs use direct calculation mode. The system auto-copies target_set to target_input. This is normal behavior.

**Q: Can I delete a KPI result?**  
A: No. Only administrators can delete records. Contact your manager if a record needs removal.

---

## Getting Additional Help

### Support Contacts

**IT Support**:
- Email: [IT support email]
- Phone: [IT support phone]
- Available: Monday-Friday, 8:00 AM - 5:00 PM

**Administrator**:
- Email: [Admin email]
- Phone: [Admin phone]

### Additional Resources

- [Installation Guide](installation-guide.md) - For technical setup
- [Admin Guide](admin-guide.md) - For administrators
- [Troubleshooting Guide](troubleshooting.md) - For common issues
- [KPI Calculation Logic](kpi-calculation-logic.md) - For detailed calculations

---

## Tips for Success

### Best Practices

1. **Check your KPIs regularly**: Review at least monthly
2. **Update profile info**: Keep contact information current
3. **Export backups**: Download reports for your records
4. **Understand your scores**: Know how your performance is measured
5. **Contact manager for questions**: Don't hesitate to ask for clarification

### Common Mistakes to Avoid

1. **Don't share your password**: Each user should have unique credentials
2. **Don't ignore low scores**: Address performance issues early
3. **Don't wait until end of period**: Track progress throughout
4. **Don't assume locked fields are errors**: Some fields are intentionally read-only

---

**Last Updated**: December 30, 2025

For technical assistance, see [Troubleshooting Guide](troubleshooting.md).
