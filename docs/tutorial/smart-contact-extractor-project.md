# Building a Smart Contact Extractor

Combine **Easy Web**, **Easy Regex**, **Easy Lists**, and **Easy Strings** to build a tool that fetches a webpage, extracts contact emails, and outputs a clean, deduplicated list in just a few lines of Python.

## What we are building

Imagine you are organizing a local tech meetup and want to reach out to the organizers of similar events. Instead of manually visiting their "About Us" pages and copying emails one by one, we can write a short script to fetch the webpage, extract the emails, and clean them up automatically.

```python
from py_simple import get_page_content, extract_emails, unique_items, to_title_case

# 1. The URL of the page we want to scan
target_url = "https://example.com"

# 2. Fetch the raw HTML content of the page
page_html = get_page_content(target_url)

if page_html:
    # 3. Extract all email addresses from the HTML text
    raw_emails = extract_emails(page_html)
    
    # 4. Clean up: make them lowercase and remove duplicates while keeping order
    clean_emails = unique_items([email.lower().strip() for email in raw_emails])
    
    print(f"Found {len(clean_emails)} unique contacts on {target_url}:\n")
    for email in clean_emails:
        # Bonus: Generate a friendly name label from the email prefix
        name_part = email.split("@")[0].replace("_", " ").replace(".", " ")
        formatted_name = to_title_case(name_part)
        print(f"{formatted_name} <{email}>")
else:
    print("Could not fetch the webpage. Check the URL.")