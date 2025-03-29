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

- Windows operating system
- Python 3.8 or higher installed
- Chrome browser installed
- Internet connection

## Installation & Usage

1. Download or clone this repository
2. Double-click `setup.bat`
3. If this is your first time running the tool:
   - The script will check if Python is installed
   - Create a virtual environment
   - Install required packages
   - Ask for your AVAC credentials
   - Save your credentials securely
4. The tool will automatically start and:
   - Log in to the AVAC system
   - Process all tennis programs
   - Show attendance records
   - Prompt for re-enrollment decisions
   - Register students for the next month
   - Display a final summary

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
- Your credentials are stored securely in a `.env` file

## Troubleshooting

If you encounter any issues:
1. Make sure Python is installed and added to PATH
2. Ensure Chrome is installed and up to date
3. Check your internet connection
4. Try running `setup.bat` again

## Contributing

Feel free to submit issues and enhancement requests! 