from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time

def wait_and_click(driver, by, value, timeout=10):
    """Wait for element to be clickable and click it"""
    try:
        # Wait for element to be clickable
        element = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((by, value))
        )
        # Scroll element into view
        driver.execute_script("arguments[0].scrollIntoView(true);", element)
        time.sleep(0.2)  # Reduced delay for scroll
        
        # Try regular click first
        try:
            element.click()
        except:
            # If regular click fails, try JavaScript click
            try:
                driver.execute_script("arguments[0].click();", element)
            except:
                # If both fail, try to refresh the element and click again
                element = WebDriverWait(driver, timeout).until(
                    EC.element_to_be_clickable((by, value))
                )
                driver.execute_script("arguments[0].click();", element)
        return True
    except Exception as e:
        print(f"Error clicking element {value}: {str(e)}")
        return False

def wait_for_element(driver, by, value, timeout=10):
    """Wait for element to be present"""
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )
        return element
    except TimeoutException:
        print(f"Timeout waiting for element: {value}")
        return None

def wait_for_element_visible(driver, by, value, timeout=10):
    """Wait for element to be visible"""
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located((by, value))
        )
        return element
    except TimeoutException:
        print(f"Timeout waiting for element to be visible: {value}")
        return None

def select_program(driver, program_id):
    """Select a program by its ID"""
    program_link = f"row_program_{program_id}"
    try:
        # First check if the program is already selected
        element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, program_link))
        )
        if "selected_row" in element.get_attribute("class"):
            return True
        return wait_and_click(driver, By.ID, program_link)
    except TimeoutException:
        return False

def select_session(driver, session_id):
    """Select a session by its ID"""
    session_link = f"row_session_{session_id}"
    return wait_and_click(driver, By.ID, session_link)

def select_day(driver, day_id):
    """Select a day by its ID"""
    day_link = f"row_day_{day_id}"
    return wait_and_click(driver, By.ID, day_link)

def register_student(driver, student_name: str, program_name: str, day_name: str):
    """Register a student in the current class"""
    try:
        # First check if student is already enrolled in this class
        table_body = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "table-body"))
        )
        
        # Check all rows for the student's name
        rows = table_body.find_elements(By.TAG_NAME, "tr")
        for row in rows:
            try:
                if "separator" in row.get_attribute("class") or "attendance-separator" in row.get_attribute("class"):
                    continue
                    
                if not row.find_elements(By.CSS_SELECTOR, "td"):
                    continue
                    
                name_element = row.find_element(By.CSS_SELECTOR, ".second-col a")
                full_name = name_element.text.strip()
                last_name, first_name = full_name.split(", ")
                current_name = f"{first_name} {last_name}"
                
                if current_name == student_name:
                    print(f"  ⚠️  Student already enrolled: {student_name}")
                    return False
                    
            except NoSuchElementException:
                continue
            except Exception:
                continue
        
        # If student is not enrolled, proceed with registration
        print(f"  Attempting to register: {student_name}")
        
        # Click the Register User button using JavaScript
        register_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "registerUserLink"))
        )
        driver.execute_script("arguments[0].click();", register_button)
        time.sleep(0.3)  # Reduced wait time
        
        # Find and fill the input field
        input_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "userInput"))
        )
        input_field.clear()  # Clear any existing text
        input_field.send_keys(student_name)  # Type the student name
        time.sleep(0.3)  # Reduced wait time
        
        # Wait for the dropdown menu to appear
        dropdown = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "ac_ul"))
        )
        
        # Get all matching student entries
        student_entries = dropdown.find_elements(By.XPATH, f".//span[contains(., '{student_name}')]")
        
        if not student_entries:
            print(f"  ✗ No matching accounts found for: {student_name}")
            return False
            
        if len(student_entries) > 1:
            print(f"\n⚠️  Scheduler Alert: Multiple accounts found for {student_name} in {program_name} - {day_name}")
            print("   Please manually select the correct account.")
            return False
            
        # Get the parent element that contains the full student info
        student_element = student_entries[0].find_element(By.XPATH, "./..")
        
        # Click the student entry using JavaScript
        driver.execute_script("arguments[0].click();", student_element)
        time.sleep(0.3)  # Reduced wait time
        
        # Click the Add button using JavaScript
        add_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input.button.bold[value='Add']"))
        )
        driver.execute_script("arguments[0].click();", add_button)
        
        # Wait for the registration to complete
        time.sleep(0.5)  # Reduced wait time
        
        # Verify the student was actually registered
        table_body = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "table-body"))
        )
        rows = table_body.find_elements(By.TAG_NAME, "tr")
        for row in rows:
            try:
                if "separator" in row.get_attribute("class") or "attendance-separator" in row.get_attribute("class"):
                    continue
                    
                if not row.find_elements(By.CSS_SELECTOR, "td"):
                    continue
                    
                name_element = row.find_element(By.CSS_SELECTOR, ".second-col a")
                full_name = name_element.text.strip()
                last_name, first_name = full_name.split(", ")
                current_name = f"{first_name} {last_name}"
                
                if current_name == student_name:
                    print(f"  ✓ Successfully registered: {student_name}")
                    return True
                    
            except NoSuchElementException:
                continue
            except Exception:
                continue
        
        print(f"  ✗ Failed to register: {student_name}")
        return False
        
    except Exception as e:
        print(f"Failed to register student {student_name}: {str(e)}")
        return False

def process_students(driver, program_name: str, day_name: str, student_names: list):
    """Process students for a specific class"""
    print(f"\n🔄 Processing students for {program_name} - {day_name}")
    
    # Click the program
    program_id = driver.find_element(By.CSS_SELECTOR, "a[id^='row_program_'].selected_row").get_attribute("id").replace("row_program_", "")
    if not select_program(driver, program_id):
        return
    
    # Get all session links
    session_list = wait_for_element_visible(driver, By.ID, f"program_{program_id}_list")
    if not session_list:
        return
    
    session_links = session_list.find_elements(By.CSS_SELECTOR, "a[id^='row_session_']")
    if not session_links:
        return
    
    # Select the last month (April 2025)
    last_session = session_links[-1]
    session_id = last_session.get_attribute("id").replace("row_session_", "")
    if not select_session(driver, session_id):
        return
    
    # Get the first day
    day_list = wait_for_element_visible(driver, By.ID, f"session_{session_id}_list")
    if not day_list:
        return
    
    day_links = day_list.find_elements(By.CSS_SELECTOR, "a[id^='row_day_']")
    if not day_links:
        return
    
    # Select the first day
    first_day = day_links[0]
    day_id = first_day.get_attribute("id").replace("row_day_", "")
    if not select_day(driver, day_id):
        return
    
    # Process attendance page
    if not wait_and_click(driver, By.ID, "attendance"):
        return
    
    # Register each student
    for student_name in student_names:
        print(f"  Attempting to register: {student_name}")
        if register_student(driver, student_name, program_name, day_name):
            print(f"  ✓ Successfully registered: {student_name}")
        else:
            print(f"  ✗ Failed to register: {student_name}")

def process_attendance(driver, program_name: str, day_name: str) -> tuple:
    """Process the attendance page and return list of participant names and waitlisted students"""
    # Click the Attendance button with retry
    max_retries = 3
    for attempt in range(max_retries):
        if wait_and_click(driver, By.ID, "attendance"):
            break
        if attempt == max_retries - 1:
            print(f"Failed to access attendance for {program_name} - {day_name}")
            return [], []
        time.sleep(1)
    
    # Wait for the attendance table to load
    try:
        table_body = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "table-body"))
        )
    except TimeoutException:
        print(f"No attendance data found for {program_name} - {day_name}")
        return [], []
    
    names = []
    waitlist_names = []
    low_attendance_students = []
    
    # Find all rows in the table
    rows = table_body.find_elements(By.TAG_NAME, "tr")
    
    for row in rows:
        try:
            # Check for waitlist section
            if "attendance-separator" in row.get_attribute("class"):
                separator_text = row.find_element(By.CSS_SELECTOR, "td.separator").text
                if "Waitlisted" in separator_text:
                    # Get waitlisted student names
                    waitlist_rows = row.find_elements(By.XPATH, "following-sibling::tr[not(contains(@class, 'separator')) and not(contains(@class, 'attendance-separator'))]")
                    for waitlist_row in waitlist_rows:
                        if waitlist_row.find_elements(By.CSS_SELECTOR, "td"):
                            name_element = waitlist_row.find_element(By.CSS_SELECTOR, ".second-col a")
                            full_name = name_element.text.strip()
                            last_name, first_name = full_name.split(", ")
                            waitlist_names.append(f"{first_name} {last_name}")
                    
                    if waitlist_names:
                        print(f"\n⚠️  Scheduler Alert: {len(waitlist_names)} student(s) on waitlist for {program_name} - {day_name}")
                        print("   Consider enrolling them if there is space available.")
                    break
                elif "Make-up" in separator_text:
                    break
                    
            # Skip separator rows and empty rows
            if "separator" in row.get_attribute("class") or "attendance-separator" in row.get_attribute("class"):
                continue
                
            if not row.find_elements(By.CSS_SELECTOR, "td"):
                continue
                
            # Get the full name and split it into first and last
            name_element = row.find_element(By.CSS_SELECTOR, ".second-col a")
            full_name = name_element.text.strip()
            last_name, first_name = full_name.split(", ")
            current_name = f"{first_name} {last_name}"
            
            # Get phone number if available
            try:
                phone_element = row.find_element(By.CSS_SELECTOR, ".staff-phone")
                phone_number = phone_element.text.strip()
            except NoSuchElementException:
                phone_number = "No phone number available"
            
            # Count present checkboxes
            present_count = 0
            checkbox_cells = row.find_elements(By.CSS_SELECTOR, "td.date")
            for cell in checkbox_cells:
                try:
                    checkbox = cell.find_element(By.CSS_SELECTOR, "a.checkbox")
                    if "active" in checkbox.get_attribute("class"):
                        present_count += 1
                except NoSuchElementException:
                    continue
            
            # If student has less than 3 present checkboxes, add to low attendance list
            if present_count < 3:
                low_attendance_students.append({
                    "name": current_name,
                    "phone": phone_number,
                    "present_count": present_count
                })
            
            names.append(current_name)
            
        except NoSuchElementException:
            continue  # Silently skip rows without name elements
        except Exception:
            continue  # Silently skip any other errors
    
    # Print attendance summary
    if names:
        print(f"\n{program_name} - {day_name}:")
        for name in names:
            print(f"  {name}")
    
    # Alert about low attendance students
    if low_attendance_students:
        print(f"\n⚠️  Scheduler Alert: {len(low_attendance_students)} student(s) with low attendance in {program_name} - {day_name}")
        for student in low_attendance_students:
            print(f"\n  Student: {student['name']}")
            print(f"  Phone: {student['phone']}")
            print(f"  Present: {student['present_count']} out of 4 sessions")
            response = input("  Would you like to re-enroll this student? (y/n): ")
            if response.lower() == 'y':
                print(f"  ✓ Added to re-enrollment list: {student['name']}")
                names.append(student['name'])
    
    return names, waitlist_names

def process_programs(driver):
    """Process all programs and their associated sessions and days"""
    # Store all names by program and day for summary
    all_names = {}
    
    # Wait for the all-events container to be present
    try:
        events_container = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "all-events-container"))
        )
    except TimeoutException:
        print("Failed to load events container")
        return

    # Wait for the events block to be present
    try:
        events_block = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "eventsBlock"))
        )
    except TimeoutException:
        print("Failed to load events block")
        return

    # Get all program links from the first column
    program_links = driver.find_elements(By.CSS_SELECTOR, "#programBlock a[id^='row_program_']")
    
    for program_link in program_links:
        program_id = program_link.get_attribute("id").replace("row_program_", "")
        program_name = program_link.text
        
        # Initialize the program's dictionary if it doesn't exist
        if program_name not in all_names:
            all_names[program_name] = {}
        
        # Click the program
        if not select_program(driver, program_id):
            continue
            
        # Wait for the session list to be visible
        session_list = wait_for_element_visible(driver, By.ID, f"program_{program_id}_list")
        if not session_list:
            continue
            
        # Get all session links from the visible list
        session_links = session_list.find_elements(By.CSS_SELECTOR, "a[id^='row_session_']")
        
        # Select previous month (second-to-last month)
        if len(session_links) >= 2:
            previous_session = session_links[-2]  # Second to last month
            previous_session_id = previous_session.get_attribute("id").replace("row_session_", "")
            previous_session_name = previous_session.text
            
            # Click the previous session
            if not select_session(driver, previous_session_id):
                continue
                
            # Wait for the day list to be visible
            previous_day_list = wait_for_element_visible(driver, By.ID, f"session_{previous_session_id}_list")
            if not previous_day_list:
                continue
                
            # Get all day links from the visible list
            previous_day_links = previous_day_list.find_elements(By.CSS_SELECTOR, "a[id^='row_day_']")
            
            # Process both Monday and Wednesday in previous month
            for previous_day_link in previous_day_links[:2]:  # Only process first two days (Monday and Wednesday)
                previous_day_id = previous_day_link.get_attribute("id").replace("row_day_", "")
                previous_day_name = previous_day_link.text
                
                # Click the previous day
                if not select_day(driver, previous_day_id):
                    continue
                    
                # Process previous month attendance and collect names
                previous_names, _ = process_attendance(driver, program_name, previous_day_name)
                if previous_names:
                    all_names[program_name][previous_day_name] = previous_names
                
                # Go back to program selection
                if not select_program(driver, program_id):
                    break
            
            # Now select current month (last month) for registration
            current_session = session_links[-1]  # Last month
            current_session_id = current_session.get_attribute("id").replace("row_session_", "")
            current_session_name = current_session.text
            
            # Click the current session
            if not select_session(driver, current_session_id):
                continue
                
            # Wait for the current day list to be visible
            current_day_list = wait_for_element_visible(driver, By.ID, f"session_{current_session_id}_list")
            if not current_day_list:
                continue
                
            # Get all current day links
            current_day_links = current_day_list.find_elements(By.CSS_SELECTOR, "a[id^='row_day_']")
            
            # Process both Monday and Wednesday in current month
            for current_day_link in current_day_links[:2]:  # Only process first two days (Monday and Wednesday)
                current_day_id = current_day_link.get_attribute("id").replace("row_day_", "")
                current_day_name = current_day_link.text
                
                # Click the current day
                if not select_day(driver, current_day_id):
                    continue
                
                # Click attendance button
                if not wait_and_click(driver, By.ID, "attendance"):
                    continue
                
                # Register students for this day
                if current_day_name in all_names[program_name]:
                    print(f"\n🔄 Registering students for {program_name} - {current_day_name}")
                    for student_name in all_names[program_name][current_day_name]:
                        if register_student(driver, student_name, program_name, current_day_name):
                            print(f"  ✓ Successfully registered: {student_name}")
                        else:
                            print(f"  ✗ Failed to register: {student_name}")
                
                # Go back to program selection
                if not select_program(driver, program_id):
                    break

    # Print final summary
    print("\n=== Final Summary ===")
    for program, days in all_names.items():
        print(f"\n{program}:")
        for day, names in days.items():
            print(f"  {day}:")
            for name in names:
                print(f"    {name}")

chrome_options = Options()
chrome_options.add_argument('--log-level=3')  # Suppress console logs
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])  # Disable logging
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    # Login process
    driver.get("https://avac.clubautomation.com/event/view-all?eventId=243922&schedule=434013&date=03/29/2025&do_action=attendance#event-info")
    driver.implicitly_wait(3)
    driver.find_element(By.NAME, "login").send_keys("USERNAME")
    driver.find_element(By.NAME, "password").send_keys("PASSWORD")
    driver.find_element(By.ID, "loginButton").click()
    driver.implicitly_wait(3)
    driver.find_element(By.NAME, "selectPosButton").click()
    
    # Process all programs
    process_programs(driver)

finally:
    driver.quit()