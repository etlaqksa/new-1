import re
from bs4 import BeautifulSoup

html_file_path = "/home/ubuntu/etlaq_site/index.html"

def enhance_seo_accessibility(html_path):
    try:
        with open(html_path, "r", encoding="utf-8") as f:
            content = f.read()

        soup = BeautifulSoup(content, "html.parser")

        # 1. Add data-translate-alt to company logo
        company_logo_img = soup.find("img", {"id": "company-logo"})
        if company_logo_img:
            company_logo_img["data-translate-alt"] = "companyLogoAlt"
            print("Added data-translate-alt to company logo.")

        # 2. Add data-translate to the hidden H1 for company name
        # The H1 is already present and styled to be off-screen.
        # Let's ensure it has a data-translate key if it's meant to be the main site H1.
        # It seems it's already there: <h1 style="position: absolute; left: -9999px;">شركة إطلاق المتميزة المحدودة</h1>
        # We'll add a key for it for translation consistency.
        hidden_h1 = soup.select_one(".logo-container > h1")
        if hidden_h1:
            hidden_h1["data-translate"] = "mainCompanyName"
            print("Added data-translate to hidden H1.")

        # 3. Add data-translate-alt to all gallery images
        gallery_images = soup.select(".gallery-item img")
        for img in gallery_images:
            img["data-translate-alt"] = "galleryImageAlt" # Using existing key
        if gallery_images:
            print(f"Added data-translate-alt to {len(gallery_images)} gallery images.")

        # 4. Add footer if not present (based on translations.js, it should exist)
        if not soup.find("footer"):
            footer_html = """
<footer>
    <div class="container">
        <p data-translate="footerText">© 2025 شركة إطلاق المتميزة المحدودة. جميع الحقوق محفوظة.</p>
    </div>
</footer>
            """
            soup.body.append(BeautifulSoup(footer_html, "html.parser"))
            print("Added footer element.")
        else:
            # Ensure existing footer p has the data-translate attribute
            footer_p = soup.select_one("footer .container p")
            if footer_p and not footer_p.has_attr("data-translate"):
                 footer_p["data-translate"] = "footerText"
                 print("Ensured data-translate on existing footer paragraph.")

        # 5. Add ARIA roles for tab navigation
        nav_links = soup.select("nav .container a[href^='#']")
        for link in nav_links:
            link["role"] = "tab"
            section_id = link["href"][1:] # Remove #
            link["id"] = f"nav-tab-{section_id}"
            corresponding_section = soup.find("section", {"id": section_id})
            if corresponding_section:
                corresponding_section["role"] = "tabpanel"
                corresponding_section["aria-labelledby"] = link["id"]
                if "active" in link.get("class", []):
                    link["aria-selected"] = "true"
                else:
                    link["aria-selected"] = "false"
        if nav_links:
            print("Added ARIA roles to navigation tabs and sections.")

        # 6. Update showTab JavaScript function to include ARIA updates
        # The showTab function is inline in the HTML. We need to find and modify it.
        # This is complex with BeautifulSoup; direct string replacement might be safer for JS block.
        
        # Let's find the script tag containing showTab or assume it's inline in nav links' onclick
        # The current structure has onclick="showTab(\'section_id\', this)" on each nav link.
        # The showTab function itself is defined in a <script> tag, likely near the end or in head.
        # From previous analysis, it was: function showTab(tabName, element)
        
        # Find the script tag containing the showTab function definition
        all_scripts = soup.find_all("script")
        show_tab_script_tag = None
        for script_tag_content in all_scripts:
            if script_tag_content.string and "function showTab(tabName, element)" in script_tag_content.string:
                show_tab_script_tag = script_tag_content
                break
        
        if show_tab_script_tag and show_tab_script_tag.string:
            original_script = show_tab_script_tag.string
            # Add aria-selected updates
            modified_script = original_script.replace(
                "// Add active class to the clicked tab",
                "// Add active class and aria-selected to the clicked tab\n    element.setAttribute(\'aria-selected\', \'true\');\n    // Add active class to the clicked tab"
            )
            modified_script = modified_script.replace(
                "link.classList.remove(\'active-nav\');",
                "link.classList.remove(\'active-nav\');\n        link.setAttribute(\'aria-selected\', \'false\');"
            )
            # Ensure the active tab on load also gets aria-selected="true"
            # This is handled by the loop in step 5 for initial state.
            show_tab_script_tag.string = modified_script
            print("Modified showTab function for ARIA support.")
        else:
            print("Warning: showTab function definition not found or not in expected format. ARIA updates in JS might be incomplete.")
            # Fallback: if showTab is not found, we might need to inject a new one or alert user.
            # For now, we assume it's there. The initial ARIA states are set in step 5.

        # Write the modified HTML back to the file
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(str(soup))
        
        print(f"Successfully enhanced SEO and accessibility for {html_path}")

    except Exception as e:
        print(f"An error occurred during SEO/accessibility enhancement: {e}")

if __name__ == "__main__":
    enhance_seo_accessibility(html_file_path)

