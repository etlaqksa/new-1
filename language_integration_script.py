import re
from bs4 import BeautifulSoup

html_file_path = "/home/ubuntu/etlaq_site/index.html"

def add_language_switcher_and_logic(html_path):
    try:
        with open(html_path, "r", encoding="utf-8") as f:
            content = f.read()

        soup = BeautifulSoup(content, "html.parser")

        # 1. Add language switcher HTML
        header_container = soup.find("header").find("div", class_="container")
        if header_container:
            lang_switcher_html = """
<div id="language-switcher" style="position: absolute; top: 10px; left: 10px; z-index: 1001;">
  <button data-lang="en" onclick="setLanguage(\'en\')" style="padding: 5px 10px; margin-right: 5px; cursor: pointer; background-color: #fff; color: #1e3a8a; border: 1px solid #1e3a8a; border-radius: 3px;">English</button>
  <button data-lang="ar" onclick="setLanguage(\'ar\')" style="padding: 5px 10px; cursor: pointer; background-color: #fff; color: #1e3a8a; border: 1px solid #1e3a8a; border-radius: 3px;">العربية</button>
</div>
            """
            header_container.insert(0, BeautifulSoup(lang_switcher_html, "html.parser"))
            print("Language switcher HTML added to header.")
        else:
            print("Error: Header container not found.")
            return

        # 2. Add data-translate attributes to elements that need translation
        # This is a simplified example. A more robust solution would involve mapping all text nodes.
        # For now, we'll assume translations.js keys match specific element IDs or new data-translate attributes.
        
        # Meta tags
        title_tag = soup.find("title")
        if title_tag: title_tag["data-translate"] = "pageTitle"
        
        meta_desc = soup.find("meta", {"name": "description"})
        if meta_desc: meta_desc["data-translate-content"] = "metaDescription"
        
        meta_keys = soup.find("meta", {"name": "keywords"})
        if meta_keys: meta_keys["data-translate-content"] = "metaKeywords"

        # Tagline
        tagline = soup.find("p", class_="tagline")
        if tagline: tagline["data-translate"] = "tagline"

        # Navigation links
        nav_links_map = {
            "#home": "navHome",
            "#about": "navAbout",
            "#services": "navServices",
            "#projects": "navProjects",
            "#gallery": "navGallery",
            "#machinery": "navMachinery",
            "#industry-info": "navIndustryInfo",
            "#contact": "navContact"
        }
        for nav_a in soup.select("nav a"):
            href = nav_a.get("href")
            if href in nav_links_map:
                nav_a["data-translate"] = nav_links_map[href]

        # Section titles and content (example for a few)
        sections_map = {
            "home": [("h2", "homeTitle"), ("p", "homeIntro1", 0), ("img", "homeImageAlt", 0, True), ("p", "homeIntro2", 1), ("a", "homeLearnMoreLink", 0)],
            "about": [("h2", "aboutTitle"), ("p", "aboutIntro", 0), ("h3", "aboutVisionTitle", 0), ("p", "aboutVisionText", 1), ("h3", "aboutMissionTitle", 1), ("p", "aboutMissionText", 2), ("strong", "aboutServiceAreasTitle", 0), ("p", "aboutServiceAreasText", 3)],
            "services": [("h2", "servicesTitle"), ("p", "servicesIntro", 0)],
            "projects": [("h2", "projectsTitle"), ("p", "projectsIntro", 0)],
            "gallery": [("h2", "galleryTitle"), ("p", "galleryIntro", 0)],
            "machinery": [("h2", "machineryTitle"), ("p", "machineryIntro", 0)],
            "industry-info": [("h2", "industryInfoTitle")], # Content here is more complex, will need careful mapping
            "contact": [("h2", "contactTitle"), ("p", "contactIntro", 0)]
        }

        for section_id, elements_to_translate in sections_map.items():
            section_tag = soup.find("section", id=section_id)
            if section_tag:
                for item in elements_to_translate:
                    tag_name = item[0]
                    key = item[1]
                    index = item[2] if len(item) > 2 else 0
                    is_alt = item[3] if len(item) > 3 else False
                    
                    found_elements = section_tag.find_all(tag_name, recursive=False if tag_name == 'h2' or tag_name == 'h3' else True) # Deeper search for p, a, img
                    if index < len(found_elements):
                        element = found_elements[index]
                        if is_alt:
                            element["data-translate-alt"] = key
                        else:
                            element["data-translate"] = key
                    else:
                        print(f"Warning: Element {tag_name} at index {index} for key {key} in section {section_id} not found.")
        
        # Service items (example)
        service_items = soup.select("#services .service-item")
        if len(service_items) > 0: 
            service_items[0].find("h3")["data-translate"] = "serviceCavityProbingTitle"
            service_items[0].find_all("p")[0]["data-translate"] = "serviceCavityProbingText"
        if len(service_items) > 1: 
            service_items[1].find("h3")["data-translate"] = "serviceCementGroutingTitle"
            service_items[1].find_all("p")[0]["data-translate"] = "serviceCementGroutingText"

        # Project list items (example for first one)
        project_lis = soup.select("#projects ul li")
        if project_lis: project_lis[0]["data-translate"] = "projectRiyadhMetro" # This needs to be dynamic for all

        # Machinery table headers and example row
        machinery_table = soup.select_one("#machinery table")
        if machinery_table:
            headers = machinery_table.select("thead th")
            if len(headers) == 4:
                headers[0]["data-translate"] = "machineryColType"
                headers[1]["data-translate"] = "machineryColBrand"
                headers[2]["data-translate"] = "machineryColCount"
                headers[3]["data-translate"] = "machineryColOrigin"
            body_rows = machinery_table.select("tbody tr")
            if body_rows:
                 cells = body_rows[0].select("td")
                 if len(cells) > 0: cells[0]["data-translate"] = "machineryDrillRigAirIngersoll" # Needs dynamic mapping
        
        # Contact details
        contact_details_map = {
            "tel:+966534145922": "contactPhone", # This is tricky, need to translate the label part
            "mailto:etlaqksa@gmail.com": "contactEmail",
            "https://wa.me/966534145922": "contactWhatsApp"
        }
        # The P tags containing these need to be identified and their strong tags translated
        contact_ps = soup.select("#contact .contact-details p")
        if len(contact_ps) >= 4:
            contact_ps[0].find("strong")["data-translate"] = "contactPhone"
            contact_ps[1].find("strong")["data-translate"] = "contactEmail"
            contact_ps[2].find("strong")["data-translate"] = "contactWhatsApp"
            contact_ps[3].find("strong")["data-translate"] = "contactAddress"
            # The actual address text in contact_ps[3] also needs translation if it's not part of the strong tag.
            # For now, assuming the key "contactAddress" in translations.js includes the full string "<strong>العنوان:</strong> ..."
            # A better way is to separate label and value.
            # Let's assume contactAddress key in translations.js is for the P tag's text content after the strong tag.
            # This requires more granular data-translate attributes or more complex JS logic.
            # For simplicity, we'll assume the JS will handle replacing the P's text content based on a key for the whole P.
            contact_ps[3]["data-translate"] = "contactAddress" # This will translate the whole P, including <strong>

        # Footer
        footer_p = soup.select_one("footer .container p")
        if footer_p: footer_p["data-translate"] = "footerText"

        # Add script tags for translations.js and the translation logic
        # The translations.js file should be created separately with the translations object.
        script_tag_translations = soup.new_tag("script", src="translations.js")
        soup.body.append(script_tag_translations)

        translation_logic_script = """
function applyTranslations(lang) {
    if (!window.translations || !window.translations[lang]) {
        console.error("Translations not loaded or language not found:", lang);
        return;
    }
    const currentTranslations = window.translations[lang];
    document.documentElement.lang = lang;
    document.documentElement.dir = lang === 'ar' ? 'rtl' : 'ltr';

    document.querySelectorAll('[data-translate]').forEach(el => {
        const key = el.getAttribute('data-translate');
        if (currentTranslations[key]) {
            el.innerHTML = currentTranslations[key]; // Use innerHTML to allow for <strong> tags in translations
        }
    });
    document.querySelectorAll('[data-translate-content]').forEach(el => {
        const key = el.getAttribute('data-translate-content');
        if (currentTranslations[key]) {
            el.setAttribute('content', currentTranslations[key]);
        }
    });
    document.querySelectorAll('[data-translate-alt]').forEach(el => {
        const key = el.getAttribute('data-translate-alt');
        if (currentTranslations[key]) {
            el.setAttribute('alt', currentTranslations[key]);
        }
    });
    
    // Update specific complex elements if needed, e.g. project list, machinery table
    // This part needs to be more robust for dynamic content like lists and tables.
    // For now, the data-translate on individual items is a simplification.

    // Update language switcher button styles
    document.querySelectorAll('#language-switcher button').forEach(button => {
        if (button.getAttribute('data-lang') === lang) {
            button.style.backgroundColor = '#1e3a8a';
            button.style.color = '#fff';
        } else {
            button.style.backgroundColor = '#fff';
            button.style.color = '#1e3a8a';
        }
    });

    // Special handling for the tagline to ensure both languages are shown as per original, or just one if preferred.
    // The current translations.js has the tagline as a single string for each lang.
    // If the original dual language tagline is desired, it should be hardcoded or handled differently.
}

function setLanguage(lang) {
    localStorage.setItem('preferredLang', lang);
    applyTranslations(lang);
}

document.addEventListener('DOMContentLoaded', () => {
    const preferredLang = localStorage.getItem('preferredLang') || 'ar'; // Default to Arabic
    // Ensure translations are loaded before applying
    if (window.translations) {
       applyTranslations(preferredLang);
    } else {
        // Fallback or error if translations.js didn't load
        console.error('translations.js not loaded yet or failed to load.');
        // Attempt to apply after a short delay, in case of async loading issues
        setTimeout(() => {
            if(window.translations) applyTranslations(preferredLang);
        }, 500);
    }
});
        """
        script_tag_logic = soup.new_tag("script")
        script_tag_logic.string = translation_logic_script
        soup.body.append(script_tag_logic)
        print("Translation logic script added.")

        # Write the modified HTML back to the file
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(str(soup))
        
        print(f"Successfully added language switcher and base for translation logic to {html_path}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    add_language_switcher_and_logic(html_file_path)

