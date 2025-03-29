# Tennis Class Registration Tool

This tool automates the process of registering tennis students from one month to the next based on attendance records.

## Features

- Automatically checks attendance records
- Identifies students with low attendance (less than 3 sessions)
- Prompts for re-enrollment of students with low attendance
- Handles waitlisted students
- Automatically registers students for the next month
- Provides detailed output of the registration process

## Prerequisites

- Python 3.8 or higher
- Chrome browser installed
- Internet connection

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/tennis-registration.git
cd tennis-registration
```

2. Install the required packages:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root and add your credentials:
```
AVAC_USERNAME=your_username
AVAC_PASSWORD=your_password
```

## Usage

1. Run the script:
```bash
python main.py
```

2. The script will:
   - Log in to the AVAC system
   - Process all tennis programs
   - Show attendance records
   - Prompt for re-enrollment decisions
   - Register students for the next month
   - Display a final summary

3. Follow the prompts in the terminal to:
   - Review attendance records
   - Decide whether to re-enroll students with low attendance
   - Monitor the registration process

## Output

The script will display:
- Program and day information
- List of enrolled students
- Attendance alerts for students with low attendance
- Registration status for each student
- Final summary of all processed programs

## Notes

- The script processes Monday and Wednesday classes
- Students with less than 3 present sessions will be flagged for re-enrollment
- Waitlisted students will be reported for manual review
- The script automatically handles the registration process for the next month

## Troubleshooting

If you encounter any issues:
1. Ensure Chrome is installed and up to date
2. Check your internet connection
3. Verify your credentials in the `.env` file
4. Make sure all required packages are installed

## Contributing

Feel free to submit issues and enhancement requests! 